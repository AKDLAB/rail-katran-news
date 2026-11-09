# Rail Katran news

Collects headlines about Indian Railways from Indian newspapers (Hindi and English) every 2 hours, for the
Rail Katran clipping app. Only headlines, links and each article's public preview summary are saved, never
full articles.

- The collector is `fetcher/fetch_news.py`; newspapers, railway zones and search words are in `fetcher/sources.py`.
- `.github/workflows/collect.yml` runs it on a schedule and publishes `news.json` to the `data` branch
  (one commit, replaced each run): `https://raw.githubusercontent.com/AKDLAB/rail-katran-news/refs/heads/data/news.json`
- Run it by hand: Actions → "Collect railway news" → Run workflow.

The fetcher files are copied from the main Rail Katran project, which is where they are edited.
