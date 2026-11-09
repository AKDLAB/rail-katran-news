"""Collect railway news from Indian newspapers (Hindi + English) into data/news.json.

Runs every few hours on GitHub Actions. It searches Google News for railway stories
from each major newspaper and each railway zone, drops duplicates and stories that
are not about Indian railways, finds the real newspaper link, and reads the story's
public preview card (summary line and photo). Only headlines, links and the preview
summary are saved, never the full article.

    python fetcher/fetch_news.py [--max-decode N] [--days D]
"""
import argparse
import hashlib
import html
import json
import re
import sys
import time
import urllib.parse
import xml.etree.ElementTree as ET
from collections import Counter
from concurrent.futures import ThreadPoolExecutor
from datetime import datetime, timedelta, timezone
from email.utils import parsedate_to_datetime
from pathlib import Path

import requests

sys.path.insert(0, str(Path(__file__).resolve().parent))
import sources as S  # noqa: E402

ROOT = Path(__file__).resolve().parent.parent
DATA = ROOT / "data"
NEWS = DATA / "news.json"
CACHE = DATA / "link-cache.json"
UA = {
    "User-Agent": "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 "
                  "(KHTML, like Gecko) Chrome/130.0 Safari/537.36",
    "Accept-Language": "hi-IN,hi;q=0.9,en-IN;q=0.8,en;q=0.7",
}
IST = timezone(timedelta(hours=5, minutes=30))
# exit codes the Mac app's server shows as messages (1 and 2 are Python's own crash codes)
EXIT_TOO_FEW = 10
EXIT_OFFLINE = 11
MAX_TRIES = 3   # attempts per story link / preview card before giving up
PAPER_BY_DOMAIN = {p[0]: p for p in S.PAPERS}
FOREIGN_TLDS = (".vn", ".id", ".pk", ".bd", ".lk", ".np", ".cn", ".ru", ".uk", ".au", ".ca", ".de", ".fr",
                ".jp", ".kr", ".my", ".sg", ".ph", ".th", ".ae", ".sa", ".qa", ".za", ".ng", ".ke", ".br", ".it",
                ".es", ".nl", ".tr", ".ir", ".eg", ".nz", ".ie", ".pl", ".ua", ".tw", ".hk")
SKIP_SOURCES = {"facebook", "youtube", "instagram", "x.com", "twitter", "linkedin", "msn", "yahoo", "dailyhunt"}
GENERIC_IMAGE = re.compile(r"default|logo|placeholder|og-image|fallback|no-image|noimage|blank", re.I)


def log(*a):
    print(*a, flush=True)


def domain_of(url):
    try:
        host = urllib.parse.urlparse(url).hostname or ""
    except ValueError:
        return ""
    host = host.lower()
    for pre in ("www.", "m.", "amp."):
        if host.startswith(pre):
            host = host[len(pre):]
    return host


def paper_for(domain, source_name):
    """Match a story to a known newspaper by its web address, then by its name."""
    d = domain
    while d:
        if d in PAPER_BY_DOMAIN:
            return PAPER_BY_DOMAIN[d]
        if "." not in d:
            break
        d = d.split(".", 1)[1]
    alias = S.SOURCE_ALIASES.get((source_name or "").strip().lower())
    return PAPER_BY_DOMAIN.get(alias) if alias else None


def norm_title(t):
    t = re.sub(r"[^\wऀ-ॿ]+", " ", t.lower())
    return re.sub(r"\s+", " ", t).strip()


def clean_title(title, source):
    title = html.unescape(title or "").strip()
    if source and title.endswith(" - " + source):
        title = title[: -len(source) - 3]
    elif " - " in title and len(title.rsplit(" - ", 1)[1]) < 40:
        title = title.rsplit(" - ", 1)[0]
    return title.strip()


EN_RAIL = [re.compile(p, re.I) for p in S.RAIL_WORDS_EN]


def is_railway(text, lang):
    low = text.lower()
    for bad in S.NON_RAIL_STATION:
        low = low.replace(bad.lower(), " ")
    if any(re.search(r"(?<![\w\u0900-\u097F])" + re.escape(w), low) for w in S.RAIL_WORDS_HI):
        return True
    return any(p.search(low) for p in EN_RAIL)


def looks_indian(item):
    low = (item["t"] + " " + item.get("desc", "")).lower()
    india = (item.get("zones") or item.get("divs") or any(w in low for w in S.INDIA_WORDS)
             or any(w in low for w in S.INDIA_WORDS_HI))
    if any(re.search(r"(?<![\w\u0900-\u097F])" + re.escape(w), low) for w in S.FOREIGN_WORDS) and not india:
        return False
    if item["kind"] in ("paper", "official"):
        return True
    dom = item.get("domain") or domain_of(item.get("url") or "")
    if dom.endswith(".in") or dom.endswith(".gov.in"):
        return True
    if dom.endswith(FOREIGN_TLDS):
        return False
    if item["lang"] == "hi":
        return True
    return bool(india)


def rss_search(query, lang, days):
    params = dict(q="%s when:%dd" % (query, days), **(S.HI_PARAMS if lang == "hi" else S.EN_PARAMS))
    url = "https://news.google.com/rss/search?" + urllib.parse.urlencode(params)
    # short connect timeout: on a dead network each search should fail fast, not after 25 s
    r = requests.get(url, headers=UA, timeout=(6, 25))
    r.raise_for_status()
    root = ET.fromstring(r.content)
    out = []
    for it in root.iter("item"):
        src = it.find("source")
        out.append({
            "title": it.findtext("title") or "",
            "link": it.findtext("link") or "",
            "pub": it.findtext("pubDate") or "",
            "source": (src.text or "").strip() if src is not None else "",
            "source_url": src.get("url", "") if src is not None else "",
        })
    return out


# ---------- tagging ----------
def _variants(name):
    return S.CITY_VARIANTS.get(name, [name])


def _build_tagger():
    zone_names = []  # (pattern text, zone code), longest first so "North Eastern" wins over "Eastern"
    div_names = []   # (pattern text, "Zone:Division")
    for code, (zen, zhi), divs in S.ZONES:
        zone_names += [(zen, code), (zhi, code)]
        for den, dhi in divs:
            key = "%s:%s" % (code, den)
            for v in _variants(den) + _variants(dhi):
                div_names.append((v, key))
    zone_names.sort(key=lambda x: -len(x[0]))
    return zone_names, div_names


ZONE_NAMES, DIV_NAMES = _build_tagger()


B = r"[\w\u0900-\u097F]"


def has_word(text, low, w):
    """Whole word for acronyms and short words (so "आग" does not match "आगरा"), word start otherwise."""
    if w.isupper():
        return re.search(r"\b%s\b" % re.escape(w), text) is not None
    wl = w.lower()
    tail = "(?!%s)" % B if len(wl) <= 3 else ""
    return re.search("(?<!%s)%s%s" % (B, re.escape(wl), tail), low) is not None


def tag(text):
    zones, divs, topics = [], [], []
    # papers write "दक्षिण-पूर्व रेलवे" / "South-Eastern Railway"; the names in sources.py use spaces
    text = re.sub(r"(?<=\S)\s*[-‐‑–—]\s*(?=\S)", " ", text)
    rest = text
    for name, code in ZONE_NAMES:
        pat = re.compile(r"(?<![\wऀ-ॿ])" + re.escape(name), re.I)
        if pat.search(rest):
            rest = pat.sub(" ", rest)
            if code not in zones:
                zones.append(code)
    low = text.lower()
    for name, key in DIV_NAMES:
        if re.search(r"(?<![\wऀ-ॿ])" + re.escape(name.lower()), low) and key not in divs:
            divs.append(key)
    for code, _hi, _en, words in S.TOPICS:
        if any(has_word(text, low, w) for w in words):
            topics.append(code)
    return zones, divs, topics


# ---------- link decoding + preview card ----------
def decode_link(link):
    try:
        from googlenewsdecoder import gnewsdecoder
        d = gnewsdecoder(link, interval=None)
        if d.get("status") or d.get("success"):
            return d.get("decoded_url") or ""
    except Exception as e:  # noqa: BLE001
        log("   decode failed:", str(e)[:100])
    return ""


META_TAG = re.compile(r"<meta\b[^>]*>", re.I)
META_ATTR = re.compile(r"""([\w:-]+)\s*=\s*(?:"([^"]*)"|'([^']*)')""")


def meta_tags(htmltext):
    """{property-or-name: content} for every <meta> tag. Reads each tag once, so it stays fast on any page."""
    out = {}
    head = htmltext[: htmltext.lower().find("</head>") + 7] if "</head>" in htmltext.lower() else htmltext[:300000]
    for tag in META_TAG.findall(head):
        attrs = {k.lower(): (a if a is not None and a != "" else b) for k, a, b in META_ATTR.findall(tag)}
        key = (attrs.get("property") or attrs.get("name") or "").lower()
        if key and "content" in attrs and key not in out:
            out[key] = html.unescape(attrs["content"] or "").strip()
    return out


def preview_card(url):
    """The page's preview card, or None when the page could not be read (tried again on a later run)."""
    try:
        # read at most ~600 KB and give up after 20 s, so one slow site cannot hold up the run
        start = time.time()
        with requests.get(url, headers=UA, timeout=15, stream=True) as r:
            if r.status_code != 200:
                return None
            body = b""
            for chunk in r.iter_content(65536):
                body += chunk
                if len(body) > 600000 or time.time() - start > 20:
                    break
            enc = r.encoding if r.encoding and r.encoding.lower() != "iso-8859-1" else "utf-8"
        h = body.decode(enc, errors="replace")
    except Exception:  # noqa: BLE001
        return None
    m = meta_tags(h)
    desc = m.get("og:description") or m.get("description") or m.get("twitter:description") or ""
    img = m.get("og:image") or m.get("twitter:image") or ""
    if img and (GENERIC_IMAGE.search(img) or not img.startswith("http")):
        img = ""
    title = m.get("og:title") or m.get("twitter:title") or ""
    desc = re.sub(r"\s+", " ", desc)
    # Some Hindi sites put an English search-engine line before the Hindi summary.
    first_hi = re.search(r"[\u0900-\u097F]", desc)
    if first_hi and first_hi.start() > 20 and re.match(r"[A-Za-z]", desc):
        cut = desc.rfind(". ", 0, first_hi.start())
        desc = desc[cut + 2:] if cut > 0 else desc[first_hi.start():]
    if len(desc) > 320:
        desc = desc[:317].rsplit(" ", 1)[0] + "…"
    desc = desc.strip()
    if len(desc) < 25 or desc.count(" ") < 3:
        desc = ""        # "dainikbhaskar", "Indian Railway": the site's name, not a summary
    return {"desc": desc, "img": img, "title": re.sub(r"\s+", " ", title)[:300]}


def progress(stage, done, total):
    """Machine-readable progress line for the Mac app's local server."""
    print("PROGRESS %s %d %d" % (stage, done, total), flush=True)


def write_json(path, obj):
    """Write to a temp file and rename it, so a reader never sees a half-written file."""
    tmp = path.with_suffix(path.suffix + ".tmp")
    tmp.write_text(json.dumps(obj, ensure_ascii=False, separators=(",", ":")), "utf-8")
    for _ in range(40):
        try:
            tmp.replace(path)
            return
        except PermissionError:
            # Windows refuses to replace a file while the app is reading it; that read takes milliseconds
            time.sleep(0.25)
    tmp.replace(path)


def build_items(raw, now, cutoff):
    items, seen = {}, {}
    reasons = Counter()
    for g in raw:
        source = g["source"]
        if source.strip().lower() in SKIP_SOURCES:
            reasons["social"] += 1
            continue
        title = clean_title(g["title"], source)
        if not title:
            continue
        try:
            pub = parsedate_to_datetime(g["pub"]).astimezone(timezone.utc)
        except (TypeError, ValueError):
            pub = now
        if pub < cutoff:
            reasons["old"] += 1
            continue
        dom = domain_of(g["source_url"])
        paper = paper_for(dom, source)
        nt = norm_title(title)
        key = hashlib.sha1(nt.encode()).hexdigest()[:12]
        if key in items:
            continue
        item = {
            "id": key, "t": title, "src": paper[1] if paper else source, "srcHi": paper[2] if paper else "",
            "kind": paper[4] if paper else "web", "domain": dom, "lang": "hi" if re.search(r"[ऀ-ॿ]", title) else "en",
            "pub": pub.isoformat().replace("+00:00", "Z"), "g": g["link"],
        }
        if not is_railway(title, item["lang"]):
            reasons["not railway"] += 1
            continue
        # near-duplicates: same paper, same first 8 words
        sig = (item["src"], " ".join(nt.split()[:8]))
        if sig in seen:
            continue
        seen[sig] = key
        items[key] = item
    log("kept %d unique railway stories (%s)" % (len(items), dict(reasons)))
    return items


def enrich(items, cache):
    """Fill in real links, full headlines, summaries, photos and tags from the link cache."""
    out = {}
    # A summary shared by many stories of one site is the site's own blurb, not the story's.
    desc_count = Counter(v.get("desc") for k, v in cache.items() if k in items and v.get("desc"))
    img_count = Counter(v.get("img") for k, v in cache.items() if k in items and v.get("img"))
    for k, base in items.items():
        it = dict(base)
        c = cache.get(k, {})
        if c.get("url"):
            it["url"] = c["url"]
            dom = domain_of(c["url"])
            if dom:
                it["domain"] = dom
                p = paper_for(dom, it["src"])
                if p:
                    it.update(src=p[1], srcHi=p[2], kind=p[4])
        full = clean_title(c.get("title", ""), it["src"])
        for suffix in (" - " + it["src"], " | " + it["src"], " - " + it.get("srcHi", ""), " | " + it.get("srcHi", "")):
            if suffix.strip(" -|") and full.endswith(suffix):
                full = full[: -len(suffix)].strip()
        if re.search(r"(\.\.\.|…)$", it["t"]) and len(full) > len(it["t"]) - 3 and norm_title(it["t"].rstrip(".…"))[:20] == norm_title(full)[:20]:
            it["t"] = full
        if c.get("desc") and desc_count[c["desc"]] < 3 and norm_title(c["desc"]) != norm_title(it["t"]):
            it["desc"] = c["desc"]
        if c.get("img") and img_count[c["img"]] < 3:
            it["img"] = c["img"]
        z, d, tp = tag(it["t"] + " \n " + it.get("desc", ""))
        if z:
            it["zones"] = z
        if d:
            it["divs"] = d
        if tp:
            it["topics"] = tp
        out[k] = it
    return out


def publish(paths, items, cache, old, now, cutoff, stats, t0, final_run):
    """Write news.json (and the link cache). Returns False when this run found too little to replace the old file."""
    news_path, cache_path = paths
    full = enrich(items, cache)
    final = [it for it in full.values() if looks_indian(it)]
    # Keep older stories from the last file that dropped out of today's search results.
    have = {it["id"] for it in final}
    cut = cutoff.isoformat().replace("+00:00", "Z")
    for it in old:
        # stories carried over from the last file get the same India check as new ones
        if it["id"] not in have and it.get("pub", "") >= cut and looks_indian(it):
            final.append(it)
    final.sort(key=lambda it: it["pub"], reverse=True)
    for it in final:
        it.pop("domain", None)
        if it.get("url"):
            it.pop("g", None)

    if len(final) < 20 and len(old) > len(final):
        log("too few stories this run (%d); keeping the previous file" % len(final))
        return False

    if final_run:
        # Forget cached links older than a week.
        week = (now - timedelta(days=7)).isoformat()
        cache = {k: v for k, v in cache.items() if v.get("seen", "") >= week}
    write_json(cache_path, cache)

    zones = [{"code": c, "en": zen, "hi": zhi, "divs": [{"en": a, "hi": b} for a, b in divs]}
             for c, (zen, zhi), divs in S.ZONES]
    topics = [{"code": c, "hi": hi, "en": en} for c, hi, en, _w in S.TOPICS]
    papers = [{"src": p[1], "hi": p[2], "lang": p[3], "kind": p[4]} for p in S.PAPERS]
    # stamped at write time, so the app notices the second, fuller save of the same run
    stamp = datetime.now(timezone.utc)
    out = {
        "updated": stamp.isoformat().replace("+00:00", "Z"),
        "updatedIST": stamp.astimezone(IST).strftime("%d %b %Y, %I:%M %p"),
        "count": len(final),
        "complete": final_run,
        "stats": dict(stats, seconds=round(time.time() - t0)),
        "zones": zones, "topics": topics, "papers": papers,
        "items": final,
    }
    write_json(news_path, out)
    if final_run:
        by_src = Counter(it["src"] for it in final)
        log("wrote %d stories in %ds. Top sources: %s" % (len(final), time.time() - t0, by_src.most_common(12)))
    else:
        log("saved %d stories so far" % len(final))
    return True


def main():
    # Hindi headlines in the log: a Windows console or pipe may default to a code page that cannot show them
    for stream in (sys.stdout, sys.stderr):
        if hasattr(stream, "reconfigure"):
            stream.reconfigure(encoding="utf-8", errors="replace")
    # Office networks that inspect HTTPS use their own certificate, which Windows trusts but Python's bundled
    # list does not; truststore (shipped with the Windows build) makes Python use the system's certificates.
    try:
        import truststore
        truststore.inject_into_ssl()
    except Exception:  # noqa: BLE001  (not installed on the Mac build, or not supported here)
        pass
    ap = argparse.ArgumentParser()
    ap.add_argument("--max-decode", type=int, default=150, help="new links to open this run")
    ap.add_argument("--days", type=int, default=2, help="how far back each search looks")
    ap.add_argument("--keep-days", type=int, default=4, help="how many days of news to keep")
    ap.add_argument("--data", default=str(DATA), help="folder for news.json and link-cache.json")
    args = ap.parse_args()
    t0 = time.time()
    data = Path(args.data)
    data.mkdir(parents=True, exist_ok=True)
    news_path, cache_path = data / "news.json", data / "link-cache.json"

    cache = {}
    if cache_path.exists():
        try:
            cache = json.loads(cache_path.read_text("utf-8"))
        except ValueError:
            cache = {}
    old = []
    if news_path.exists():
        try:
            old = json.loads(news_path.read_text("utf-8")).get("items", [])
        except ValueError:
            old = []

    qs = S.queries()
    raw, failed, in_a_row = [], 0, 0
    for i, (q, lang) in enumerate(qs, 1):
        try:
            got = rss_search(q, lang, args.days)
            for g in got:
                g["lang"] = lang
            raw += got
            in_a_row = 0
        except Exception as e:  # noqa: BLE001
            failed += 1
            in_a_row += 1
            log("  search failed:", q, str(e)[:80])
        if in_a_row >= 8:
            log("%d searches in a row failed (no internet?); keeping the previous file" % in_a_row)
            return EXIT_OFFLINE
        if i % 25 == 0:
            log("  searched %d/%d, %d results so far" % (i, len(qs), len(raw)))
        progress("search", i, len(qs))
        time.sleep(0.35)
    log("searches: %d, failed: %d, raw results: %d" % (len(qs), failed, len(raw)))
    if failed > len(qs) * 0.8:
        log("almost every search failed (no internet?); keeping the previous file")
        return EXIT_OFFLINE

    now = datetime.now(timezone.utc)
    cutoff = now - timedelta(days=args.keep_days)
    items = build_items(raw, now, cutoff)
    stats = {"searches": len(qs), "failed": failed}
    paths = (news_path, cache_path)

    # Save the new headlines right away; real links and summaries follow.
    if not publish(paths, items, cache, old, now, cutoff, stats, t0, False):
        return EXIT_TOO_FEW

    # Open the newest new links first, newspapers before other websites. A link that failed
    # (network trouble, Google busy) is tried again on later runs, up to MAX_TRIES times.
    def wants_link(it):
        c = cache.get(it["id"])
        return c is None or (not c.get("url") and c.get("fails", 0) < MAX_TRIES)
    todo = [it for it in items.values() if wants_link(it)]
    todo.sort(key=lambda it: it["pub"], reverse=True)
    todo.sort(key=lambda it: {"paper": 0, "official": 1}.get(it["kind"], 2))
    todo = todo[: args.max_decode]
    log("opening %d new links" % len(todo))
    decoded, misses = 0, 0
    for n, it in enumerate(todo, 1):
        url = decode_link(it["g"])
        prev = cache.get(it["id"], {})
        if url:
            cache[it["id"]] = {"url": url, "seen": now.isoformat()}
            decoded += 1
            misses = 0
        else:
            cache[it["id"]] = {"url": "", "fails": prev.get("fails", 0) + 1, "seen": now.isoformat()}
            misses += 1
        if n % 40 == 0:
            log("  opened %d/%d" % (n, len(todo)))
        if n % 25 == 0:
            write_json(cache_path, cache)   # keep the work if the run is stopped
        progress("links", n, len(todo))
        if misses >= 10:
            log("10 links in a row failed (network or Google busy); the rest are tried next run")
            break
        time.sleep(0.6)

    need_card = [k for k, v in cache.items()
                 if v.get("url") and "title" not in v and v.get("cardFails", 0) < MAX_TRIES and k in items]
    progress("cards", 0, len(need_card))
    with ThreadPoolExecutor(max_workers=10) as ex:
        for n, (k, card) in enumerate(zip(need_card, ex.map(lambda k: preview_card(cache[k]["url"]), need_card)), 1):
            if card is None:
                cache[k]["cardFails"] = cache[k].get("cardFails", 0) + 1
            else:
                cache[k].update({"desc": card.get("desc", ""), "img": card.get("img", ""), "title": card.get("title", "")})
            if n % 20 == 0 or n == len(need_card):
                progress("cards", n, len(need_card))
    log("decoded %d, read %d preview cards" % (decoded, len(need_card)))

    return 0 if publish(paths, items, cache, old, now, cutoff, stats, t0, True) else EXIT_TOO_FEW


if __name__ == "__main__":
    sys.exit(main())
