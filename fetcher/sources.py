"""Newspapers, railway zones/divisions, topics and search queries used by fetch_news.py."""

# kind: "paper" = printed newspaper, "official" = government / railway source
PAPERS = [
    # Hindi newspapers
    ("jagran.com", "Dainik Jagran", "दैनिक जागरण", "hi", "paper"),
    ("amarujala.com", "Amar Ujala", "अमर उजाला", "hi", "paper"),
    ("bhaskar.com", "Dainik Bhaskar", "दैनिक भास्कर", "hi", "paper"),
    ("livehindustan.com", "Hindustan", "हिन्दुस्तान", "hi", "paper"),
    ("navbharattimes.indiatimes.com", "Navbharat Times", "नवभारत टाइम्स", "hi", "paper"),
    ("patrika.com", "Rajasthan Patrika", "राजस्थान पत्रिका", "hi", "paper"),
    ("prabhatkhabar.com", "Prabhat Khabar", "प्रभात खबर", "hi", "paper"),
    ("punjabkesari.in", "Punjab Kesari", "पंजाब केसरी", "hi", "paper"),
    ("naidunia.com", "Nai Dunia", "नईदुनिया", "hi", "paper"),
    ("haribhoomi.com", "Haribhoomi", "हरिभूमि", "hi", "paper"),
    ("jansatta.com", "Jansatta", "जनसत्ता", "hi", "paper"),
    ("dainiktribuneonline.com", "Dainik Tribune", "दैनिक ट्रिब्यून", "hi", "paper"),
    ("navbharatlive.com", "Navbharat", "नवभारत", "hi", "paper"),
    ("deshbandhu.co.in", "Deshbandhu", "देशबन्धु", "hi", "paper"),
    ("dainiknavajyoti.com", "Dainik Navajyoti", "दैनिक नवज्योति", "hi", "paper"),
    ("sanmarg.in", "Sanmarg", "सन्मार्ग", "hi", "paper"),
    ("rashtriyasahara.com", "Rashtriya Sahara", "राष्ट्रीय सहारा", "hi", "paper"),
    ("swadeshnews.in", "Swadesh", "स्वदेश", "hi", "paper"),
    ("inextlive.com", "Inext", "आई नेक्स्ट", "hi", "paper"),
    # Varanasi-region dailies with Chandauli pages (their websites carry little; see SITE_FEEDS)
    ("janwarta.com", "Jan Varta", "जनवार्ता", "hi", "paper"),
    ("jansandeshtimes.in", "Jan Sandesh", "जनसंदेश टाइम्स", "hi", "paper"),
    ("ajhindidaily.com", "Aaj", "आज", "hi", "paper"),
    # English newspapers
    ("timesofindia.indiatimes.com", "The Times of India", "द टाइम्स ऑफ इंडिया", "en", "paper"),
    ("hindustantimes.com", "Hindustan Times", "हिन्दुस्तान टाइम्स", "en", "paper"),
    ("thehindu.com", "The Hindu", "द हिन्दू", "en", "paper"),
    ("indianexpress.com", "The Indian Express", "इंडियन एक्सप्रेस", "en", "paper"),
    ("tribuneindia.com", "The Tribune", "द ट्रिब्यून", "en", "paper"),
    ("deccanherald.com", "Deccan Herald", "डेक्कन हेराल्ड", "en", "paper"),
    ("newindianexpress.com", "The New Indian Express", "न्यू इंडियन एक्सप्रेस", "en", "paper"),
    ("deccanchronicle.com", "Deccan Chronicle", "डेक्कन क्रॉनिकल", "en", "paper"),
    ("telegraphindia.com", "The Telegraph", "द टेलीग्राफ", "en", "paper"),
    ("thestatesman.com", "The Statesman", "द स्टेट्समैन", "en", "paper"),
    ("freepressjournal.in", "Free Press Journal", "फ्री प्रेस जर्नल", "en", "paper"),
    ("mid-day.com", "Mid-Day", "मिड-डे", "en", "paper"),
    ("dnaindia.com", "DNA", "डीएनए", "en", "paper"),
    ("dailypioneer.com", "The Pioneer", "द पायनियर", "en", "paper"),
    ("business-standard.com", "Business Standard", "बिजनेस स्टैंडर्ड", "en", "paper"),
    ("economictimes.indiatimes.com", "The Economic Times", "इकोनॉमिक टाइम्स", "en", "paper"),
    ("livemint.com", "Mint", "मिंट", "en", "paper"),
    ("financialexpress.com", "Financial Express", "फाइनेंशियल एक्सप्रेस", "en", "paper"),
    ("thehindubusinessline.com", "The Hindu BusinessLine", "हिन्दू बिजनेसलाइन", "en", "paper"),
    ("thehansindia.com", "The Hans India", "द हंस इंडिया", "en", "paper"),
    ("telanganatoday.com", "Telangana Today", "तेलंगाना टुडे", "en", "paper"),
    ("assamtribune.com", "The Assam Tribune", "असम ट्रिब्यून", "en", "paper"),
    ("sentinelassam.com", "The Sentinel", "द सेंटिनल", "en", "paper"),
    ("dailyexcelsior.com", "Daily Excelsior", "डेली एक्सेलसियर", "en", "paper"),
    ("greaterkashmir.com", "Greater Kashmir", "ग्रेटर कश्मीर", "en", "paper"),
    ("orissapost.com", "Orissa Post", "ओडिशा पोस्ट", "en", "paper"),
    ("thehitavada.com", "The Hitavada", "द हितवाद", "en", "paper"),
    ("lokmattimes.com", "Lokmat Times", "लोकमत टाइम्स", "en", "paper"),
    ("millenniumpost.in", "Millennium Post", "मिलेनियम पोस्ट", "en", "paper"),
    ("asianage.com", "The Asian Age", "द एशियन एज", "en", "paper"),
    ("bhaskarenglish.in", "Bhaskar English", "भास्कर इंग्लिश", "en", "paper"),
    ("starofmysore.com", "Star of Mysore", "स्टार ऑफ मैसूर", "en", "paper"),
    ("navhindtimes.in", "The Navhind Times", "नवहिंद टाइम्स", "en", "paper"),
    ("theshillongtimes.com", "The Shillong Times", "शिलांग टाइम्स", "en", "paper"),
    # Official / government sources
    ("pib.gov.in", "PIB", "पत्र सूचना कार्यालय", "en", "official"),
    ("ddnews.gov.in", "DD News", "डीडी न्यूज़", "hi", "official"),
    ("newsonair.gov.in", "News On AIR", "आकाशवाणी समाचार", "en", "official"),
    ("indianrailways.gov.in", "Indian Railways", "भारतीय रेल", "en", "official"),
]

# Short newspaper names that the RSS "source" field sometimes uses instead of the domain.
SOURCE_ALIASES = {
    "jagran": "jagran.com", "dainik jagran": "jagran.com",
    "amar ujala": "amarujala.com", "dainik bhaskar": "bhaskar.com", "bhaskar": "bhaskar.com",
    "hindustan": "livehindustan.com", "live hindustan": "livehindustan.com",
    "navbharat times": "navbharattimes.indiatimes.com", "patrika": "patrika.com",
    "rajasthan patrika": "patrika.com", "prabhat khabar": "prabhatkhabar.com",
    "punjab kesari": "punjabkesari.in", "naidunia": "naidunia.com", "nai dunia": "naidunia.com",
    "haribhoomi": "haribhoomi.com", "jansatta": "jansatta.com", "dainik tribune": "dainiktribuneonline.com",
    "navbharat live": "navbharatlive.com", "the times of india": "timesofindia.indiatimes.com",
    "times of india": "timesofindia.indiatimes.com", "hindustan times": "hindustantimes.com",
    "the hindu": "thehindu.com", "the indian express": "indianexpress.com", "indian express": "indianexpress.com",
    "the tribune": "tribuneindia.com", "deccan herald": "deccanherald.com",
    "the new indian express": "newindianexpress.com", "deccan chronicle": "deccanchronicle.com",
    "the telegraph": "telegraphindia.com", "telegraph india": "telegraphindia.com",
    "the statesman": "thestatesman.com", "free press journal": "freepressjournal.in", "mid-day": "mid-day.com",
    "dna india": "dnaindia.com", "the pioneer": "dailypioneer.com", "business standard": "business-standard.com",
    "the economic times": "economictimes.indiatimes.com", "et infra": "economictimes.indiatimes.com",
    "livemint": "livemint.com", "mint": "livemint.com", "financial express": "financialexpress.com",
    "the financial express": "financialexpress.com", "the hindu businessline": "thehindubusinessline.com",
    "the hans india": "thehansindia.com", "telangana today": "telanganatoday.com",
    "the assam tribune": "assamtribune.com", "the sentinel assam": "sentinelassam.com",
    "daily excelsior": "dailyexcelsior.com", "greater kashmir": "greaterkashmir.com",
    "orissapost": "orissapost.com", "orissa post": "orissapost.com", "the hitavada": "thehitavada.com",
    "lokmat times": "lokmattimes.com", "millennium post": "millenniumpost.in", "bhaskar english": "bhaskarenglish.in",
    "dd news": "ddnews.gov.in", "news on air": "newsonair.gov.in", "pib": "pib.gov.in",
    "press information bureau": "pib.gov.in",
    "janwarta": "janwarta.com", "jan varta": "janwarta.com", "janvarta": "janwarta.com",
    "jansandeshtimes.in": "jansandeshtimes.in", "jansandesh times": "jansandeshtimes.in", "jan sandesh": "jansandeshtimes.in",
    "ajhindidaily.com": "ajhindidaily.com", "aaj": "ajhindidaily.com",
}

# Railway zones with their divisions. Each name is (English, Hindi).
ZONES = [
    ("NR", ("Northern Railway", "उत्तर रेलवे"), [("Delhi", "दिल्ली"), ("Ambala", "अंबाला"), ("Firozpur", "फिरोजपुर"), ("Lucknow", "लखनऊ"), ("Moradabad", "मुरादाबाद"), ("Jammu", "जम्मू")]),
    ("NER", ("North Eastern Railway", "पूर्वोत्तर रेलवे"), [("Izzatnagar", "इज्जतनगर"), ("Lucknow", "लखनऊ"), ("Varanasi", "वाराणसी"), ("Gorakhpur", "गोरखपुर")]),
    ("NFR", ("Northeast Frontier Railway", "पूर्वोत्तर सीमांत रेलवे"), [("Katihar", "कटिहार"), ("Alipurduar", "अलीपुरद्वार"), ("Rangiya", "रंगिया"), ("Lumding", "लमडिंग"), ("Tinsukia", "तिनसुकिया")]),
    ("ER", ("Eastern Railway", "पूर्व रेलवे"), [("Howrah", "हावड़ा"), ("Sealdah", "सियालदह"), ("Asansol", "आसनसोल"), ("Malda", "मालदा")]),
    ("SER", ("South Eastern Railway", "दक्षिण पूर्व रेलवे"), [("Kharagpur", "खड़गपुर"), ("Adra", "आद्रा"), ("Chakradharpur", "चक्रधरपुर"), ("Ranchi", "रांची")]),
    ("SCR", ("South Central Railway", "दक्षिण मध्य रेलवे"), [("Secunderabad", "सिकंदराबाद"), ("Hyderabad", "हैदराबाद"), ("Nanded", "नांदेड़")]),
    ("SCoR", ("South Coast Railway", "दक्षिण तट रेलवे"), [("Visakhapatnam", "विशाखापत्तनम"), ("Vijayawada", "विजयवाड़ा"), ("Guntur", "गुंटूर"), ("Guntakal", "गुंतकल")]),
    ("SR", ("Southern Railway", "दक्षिण रेलवे"), [("Chennai", "चेन्नई"), ("Tiruchchirappalli", "तिरुचिरापल्ली"), ("Madurai", "मदुरै"), ("Salem", "सेलम"), ("Palakkad", "पालक्काड"), ("Thiruvananthapuram", "तिरुवनंतपुरम")]),
    ("CR", ("Central Railway", "मध्य रेलवे"), [("Mumbai", "मुंबई"), ("Bhusawal", "भुसावल"), ("Nagpur", "नागपुर"), ("Pune", "पुणे"), ("Solapur", "सोलापुर")]),
    ("WR", ("Western Railway", "पश्चिम रेलवे"), [("Mumbai Central", "मुंबई सेंट्रल"), ("Vadodara", "वडोदरा"), ("Ahmedabad", "अहमदाबाद"), ("Ratlam", "रतलाम"), ("Rajkot", "राजकोट"), ("Bhavnagar", "भावनगर")]),
    ("SWR", ("South Western Railway", "दक्षिण पश्चिम रेलवे"), [("Hubballi", "हुबली"), ("Bengaluru", "बेंगलुरु"), ("Mysuru", "मैसूर")]),
    ("NWR", ("North Western Railway", "उत्तर पश्चिम रेलवे"), [("Jaipur", "जयपुर"), ("Ajmer", "अजमेर"), ("Bikaner", "बीकानेर"), ("Jodhpur", "जोधपुर")]),
    ("WCR", ("West Central Railway", "पश्चिम मध्य रेलवे"), [("Jabalpur", "जबलपुर"), ("Bhopal", "भोपाल"), ("Kota", "कोटा")]),
    ("NCR", ("North Central Railway", "उत्तर मध्य रेलवे"), [("Prayagraj", "प्रयागराज"), ("Agra", "आगरा"), ("Jhansi", "झांसी")]),
    ("SECR", ("South East Central Railway", "दक्षिण पूर्व मध्य रेलवे"), [("Bilaspur", "बिलासपुर"), ("Raipur", "रायपुर"), ("Nagpur", "नागपुर")]),
    ("ECoR", ("East Coast Railway", "पूर्व तटीय रेलवे"), [("Khurda Road", "खुर्दा रोड"), ("Sambalpur", "संबलपुर"), ("Rayagada", "रायगड़ा")]),
    ("ECR", ("East Central Railway", "पूर्व मध्य रेलवे"), [("Danapur", "दानापुर"), ("Dhanbad", "धनबाद"), ("Deen Dayal Upadhyaya", "दीनदयाल उपाध्याय"), ("Sonpur", "सोनपुर"), ("Samastipur", "समस्तीपुर")]),
    ("KR", ("Konkan Railway", "कोंकण रेलवे"), [("Ratnagiri", "रत्नागिरी"), ("Karwar", "कारवार")]),
]

# Extra spellings that news writers use for some division cities.
CITY_VARIANTS = {
    "फिरोजपुर": ["फिरोजपुर", "फ़िरोज़पुर", "फिरोज़पुर"], "Firozpur": ["Firozpur", "Ferozepur", "Ferozpur"],
    "झांसी": ["झांसी", "झाँसी"], "Tiruchchirappalli": ["Tiruchchirappalli", "Tiruchirappalli", "Trichy"],
    "Hubballi": ["Hubballi", "Hubli"], "हुबली": ["हुबली", "हुब्बल्ली"], "Bengaluru": ["Bengaluru", "Bangalore"],
    "Mysuru": ["Mysuru", "Mysore"], "Prayagraj": ["Prayagraj", "Allahabad"], "प्रयागराज": ["प्रयागराज", "इलाहाबाद"],
    "Deen Dayal Upadhyaya": ["Deen Dayal Upadhyaya", "DDU", "PDDU", "Mughalsarai"],
    "दीनदयाल उपाध्याय": ["दीनदयाल उपाध्याय", "डीडीयू", "पीडीडीयू", "मुगलसराय"],
    "Visakhapatnam": ["Visakhapatnam", "Vizag", "Waltair"], "Thiruvananthapuram": ["Thiruvananthapuram", "Trivandrum"],
    "Vadodara": ["Vadodara", "Baroda"], "Mumbai Central": ["Mumbai Central"], "Izzatnagar": ["Izzatnagar", "Bareilly"],
    "इज्जतनगर": ["इज्जतनगर", "बरेली"], "रांची": ["रांची", "राँची"], "खड़गपुर": ["खड़गपुर", "खड्गपुर"],
}

TOPICS = [
    ("accident", "दुर्घटना", "Accident", [
        "हादसा", "हादसे", "दुर्घटना", "टक्कर", "बेपटरी", "पटरी से उतर", "आग", "मौत", "कटकर", "चपेट", "घायल",
        "accident", "derail", "collision", "collide", "fire", "killed", "dies", "died", "run over", "mishap", "injured"]),
    ("security", "सुरक्षा व अपराध", "Security & crime", [
        "आरपीएफ", "जीआरपी", "चोरी", "गिरफ्तार", "तस्कर", "ठगी", "पत्थरबाजी", "पथराव", "लूट", "चेकिंग",
        "RPF", "GRP", "theft", "arrest", "smuggl", "robbery", "stone pelting", "fraud", "seized", "ticketless"]),
    ("services", "ट्रेन व समय-सारणी", "Trains & timings", [
        "स्पेशल ट्रेन", "नई ट्रेन", "वंदे भारत", "अमृत भारत", "ठहराव", "समय सारणी", "समय-सारणी", "रद्द", "डायवर्ट", "देरी", "लेट", "निरस्त", "फेरे",
        "special train", "new train", "Vande Bharat", "Amrit Bharat", "halt", "cancel", "divert", "delay", "timetable", "reschedul", "stoppage", "extended"]),
    ("projects", "निर्माण व परियोजना", "Projects & works", [
        "पुनर्विकास", "अमृत स्टेशन", "ओवरब्रिज", "आरओबी", "अंडरपास", "दोहरीकरण", "विद्युतीकरण", "नई लाइन", "रेल लाइन", "परियोजना", "करोड़", "निर्माण", "टेंडर",
        "project", "redevelop", "ROB", "RUB", "overbridge", "underpass", "doubling", "electrification", "new line", "gauge", "construction", "tender", "crore"]),
    ("jobs", "भर्ती व परीक्षा", "Jobs & exams", [
        "भर्ती", "आरआरबी", "परीक्षा", "नौकरी", "वैकेंसी", "आवेदन",
        "recruitment", "RRB", "vacancy", "vacancies", "exam", "jobs", "apply"]),
    ("passengers", "टिकट व यात्री सुविधा", "Tickets & amenities", [
        "टिकट", "किराया", "आईआरसीटीसी", "भीड़", "शिकायत", "सफाई", "तत्काल", "वेटिंग", "कन्फर्म",
        "passenger amenit", "ticket", "fare", "IRCTC", "crowd", "complaint", "refund", "tatkal", "waiting list", "rush"]),
    ("officials", "अधिकारी व निरीक्षण", "Officials & inspections", [
        "निरीक्षण", "महाप्रबंधक", "डीआरएम", "मंडल रेल प्रबंधक", "रेल मंत्री", "वैष्णव", "रेलवे बोर्ड", "सांसद",
        "inspection", "inspects", "general manager", "DRM", "railway minister", "Vaishnaw", "Railway Board"]),
]

# A story is kept only if its headline or summary has one of these railway words.
RAIL_WORDS_HI = ["रेल", "ट्रेन", "पटरी", "आरपीएफ", "जीआरपी", "आईआरसीटीसी", "वंदे भारत", "अमृत भारत", "डीआरएम",
                 "प्लेटफॉर्म", "प्लेटफार्म", "जंक्शन", "लोको पायलट", "मालगाड़ी", "स्टेशन"]
RAIL_WORDS_EN = [r"\brail", r"\btrains?\b", r"\bRPF\b", r"\bGRP\b", r"\bIRCTC\b", r"Vande Bharat", r"Amrit Bharat",
                 r"\bDRM\b", r"loco pilot", r"derail", r"\bstations?\b"]
# "station" alone is not enough when it is a police, bus, fire or power station.
NON_RAIL_STATION = ["ट्रेनिंग", "ट्रेनर", "ट्रेनी", "पुलिस स्टेशन", "बस स्टेशन", "फायर स्टेशन", "पावर स्टेशन", "police station", "bus station",
                    "fire station", "power station", "space station", "petrol station", "gas station", "radio station",
                    "pumping station", "pump station", "charging station", "weather station", "filling station",
                    "polling station", "sewage", "पंपिंग स्टेशन", "चार्जिंग स्टेशन", "पेट्रोल पंप"]
INDIA_WORDS = ["india", "indian", "bharat", "delhi", "mumbai", "kolkata", "chennai", "bengaluru", "hyderabad", "punjab",
               "haryana", "rajasthan", "bihar", "jharkhand", "odisha", "kerala", "karnataka", "gujarat", "maharashtra",
               "uttar pradesh", "madhya pradesh", "assam", "telangana", "andhra", "tamil nadu", "bengal", "jammu",
               "kashmir", "uttarakhand", "himachal", "chandigarh", "goa", "chhattisgarh", "irctc", "rpf", "vande",
               "railway board", "vaishnaw", "crore", "lakh"]

# Stories about other countries are dropped unless they also mention India.
FOREIGN_WORDS = ["मिस्र", "पाकिस्तान", "चीन", "जापान", "अमेरिका", "ब्रिटेन", "रूस", "यूक्रेन", "बांग्लादेश", "श्रीलंका",
                 "इंडोनेशिया", "जर्मनी", "फ्रांस", "इटली", "स्पेन", "तुर्की", "ईरान", "कनाडा", "ऑस्ट्रेलिया", "लंदन",
                 "वियतनाम", "थाईलैंड", "नॉर्वे", "यूरोप", "egypt", "pakistan", "china", "chinese", "japan", "america",
                 "u.s.", "usa", "britain", "london", "russia", "ukraine", "bangladesh", "sri lanka", "indonesia",
                 "germany", "france", "italy", "spain", "turkey", "iran", "canada", "australia", "norway", "vietnam",
                 "thailand", "malaysia", "saudi", "dubai", "europe", "european", "swiss", "switzerland",
                 "spain", "spanish", "toledo", "madrid", "mexico", "greece", "greek", "portugal", "poland", "czech",
                 "hungary", "romania", "bulgaria", "serbia", "croatia", "austria", "belgium", "netherlands", "dutch",
                 "denmark", "sweden", "finland", "israel", "gaza", "iraq", "syria", "afghanistan", "myanmar", "korea",
                 "philippines", "morocco", "algeria", "tunisia", "kenya", "nigeria", "south africa", "brazil",
                 "argentina", "peru", "chile", "colombia", "taiwan", "hong kong", "singapore", "kazakhstan",
                 "uzbekistan", "mongolia", "new zealand", "scotland", "ireland", "california", "texas", "new york",
                 "cairo", "fayoum", "aswan", "beijing", "tokyo", "moscow", "kyiv", "paris", "berlin", "rome",
                 "स्पेन", "मैक्सिको", "मेक्सिको", "ग्रीस", "इजरायल", "इज़राइल", "इराक", "सीरिया", "अफगानिस्तान", "म्यांमार",
                 "कोरिया", "ताइवान", "ब्राजील", "अर्जेंटीना", "पुर्तगाल", "पोलैंड", "नीदरलैंड", "स्वीडन", "न्यूजीलैंड",
                 "न्यूज़ीलैंड", "काहिरा", "बीजिंग", "टोक्यो", "मास्को", "मॉस्को"]
INDIA_WORDS_HI = ["भारत", "भारतीय", "दिल्ली", "मुंबई", "कोलकाता", "चेन्नई", "उत्तर प्रदेश", "यूपी", "बिहार", "राजस्थान",
                  "मध्य प्रदेश", "एमपी", "पंजाब", "हरियाणा", "गुजरात", "महाराष्ट्र", "झारखंड", "ओडिशा", "बंगाल", "असम",
                  "केरल", "कर्नाटक", "तमिलनाडु", "तेलंगाना", "आंध्र", "छत्तीसगढ़", "उत्तराखंड", "हिमाचल", "जम्मू",
                  "कश्मीर", "गोवा", "चंडीगढ़", "वैष्णव", "आईआरसीटीसी", "आरपीएफ", "वंदे भारत"]

HI_PARAMS = dict(hl="hi", gl="IN", ceid="IN:hi")
EN_PARAMS = dict(hl="en-IN", gl="IN", ceid="IN:en")


def queries():
    """Every Google News search we run, as (query, language)."""
    q = []
    for term in ["रेलवे", "ट्रेन", "रेल यात्री", "रेलवे स्टेशन", "वंदे भारत", "आरपीएफ OR जीआरपी",
                 "ट्रेन हादसा OR रेल हादसा", "रेल मंत्री OR रेलवे बोर्ड", "डीआरएम OR मंडल रेल प्रबंधक",
                 "स्पेशल ट्रेन", "रेलवे भर्ती OR आरआरबी"]:
        q.append((term, "hi"))
    for term in ["Indian Railways", "railway India", "railway station", "train India", "Vande Bharat",
                 "RPF railway", "train accident India", "Railway Board", "railway division DRM",
                 "special train", "railway project India"]:
        q.append((term, "en"))
    for dom, _en, _hi, lang, kind in PAPERS:
        if kind != "paper":
            continue
        if lang == "hi":
            q.append(("(रेलवे OR ट्रेन OR रेल) site:" + dom, "hi"))
        else:
            q.append(("(railway OR railways OR train) site:" + dom, "en"))
    for _code, (zen, zhi), divs in ZONES:
        q.append(('"%s"' % zhi, "hi"))
        q.append(('"%s"' % zen, "en"))
        q.append(("रेलवे (" + " OR ".join(d[1] for d in divs) + ")", "hi"))
        q.append(("railway (" + " OR ".join(d[0] for d in divs) + ")", "en"))
    # towns of Pt. Deen Dayal Upadhyaya (DDU) division, whose daily clipping file this app is used for
    for towns in DDU_TOWNS_HI:
        q.append(("(रेलवे OR ट्रेन OR रेल) (" + " OR ".join(towns) + ")", "hi"))
    q.append(("(railway OR train) (" + " OR ".join(DDU_TOWNS_EN) + ")", "en"))
    # the editions the DDU office reads every day: each paper's railway news from those towns, and from
    # Pt. Deen Dayal Upadhyay Nagar / Mughalsarai in every one of these papers
    for dom, towns in EDITIONS.items():
        for town in towns:
            names = (['"%s"' % t for t in TITLE_TAGS[town]] if dom in BY_TITLE else TOWN_NAMES[town]
                     + (['"%s"' % t for t in TITLE_TAGS[town]] if dom in TITLE_TOO else []))
            q.append((RAIL_Q + " (" + " OR ".join(names) + ") site:" + dom, "hi"))
        q.append((RAIL_Q + " (" + " OR ".join(DDU_NAMES) + ") site:" + dom, "hi"))
    return q


DDU_TOWNS_HI = [["पीडीडीयू", "डीडीयू", "मुगलसराय", "चंदौली", "सासाराम", "डेहरी"],
                # "गया" alone is also the everyday verb ("went"), so search for the city's own names
                ["गयाजी", "गया जंक्शन", "औरंगाबाद", "पलामू", "गढ़वा", "जपला", "डालटनगंज", "हुसैनाबाद", "सोननगर"]]
DDU_TOWNS_EN = ["DDU", "Mughalsarai", "Chandauli", "Sasaram", "Dehri", "Gaya", "Daltonganj", "Garhwa"]

# Editions read by the DDU division office (asked for by the user, 10.11.2026): paper -> towns whose railway news
# is searched separately, so it is found even on days the paper has many other railway stories.
RAIL_Q = "(रेलवे OR ट्रेन OR रेल OR स्टेशन OR जंक्शन)"
TOWN_NAMES = {
    "Gaya": ["गयाजी", '"गया जंक्शन"', '"गया जी"'],          # not plain "गया", which is also the verb "went"
    "Sasaram": ["सासाराम", "रोहतास"],
    "Aurangabad": ["औरंगाबाद", '"अनुग्रह नारायण रोड"', "रफीगंज"],
    "Palamu": ["पलामू", "डालटनगंज", "मेदिनीनगर"],
    "Arrah": ["आरा", "भोजपुर"],
    "Chandauli": ["चंदौली"],
    "Bhabhua Road": ['"भभुआ रोड"', "भभुआ", "कैमूर"],
}
# how Hindustan and Amar Ujala begin a town's stories ("Sasaram News: ...")
TITLE_TAGS = {
    "Chandauli": ["Chandauli News"], "Gaya": ["Gaya News"], "Sasaram": ["Sasaram News", "Rohtas News"],
    "Aurangabad": ["Aurangabad News"], "Arrah": ["Ara News", "Bhojpur News"], "Palamu": ["Palamu News"],
    "Bhabhua Road": ["Bhabua News", "Kaimur News"],
}
# Hindustan's pages list all its towns in their menus, so searching a town's name returns every story of the site:
# search the town's story titles instead. Amar Ujala gets both.
BY_TITLE = {"livehindustan.com"}
TITLE_TOO = {"amarujala.com"}
DDU_NAMES = ["पीडीडीयू", "डीडीयू", "मुगलसराय", '"दीनदयाल उपाध्याय"', '"दीन दयाल उपाध्याय"']
EDITIONS = {
    "bhaskar.com": ["Gaya", "Sasaram", "Aurangabad", "Palamu", "Arrah"],
    "amarujala.com": ["Chandauli"],
    "livehindustan.com": ["Chandauli", "Gaya", "Sasaram", "Aurangabad", "Arrah", "Palamu", "Bhabhua Road"],
    "jagran.com": ["Chandauli", "Gaya", "Sasaram", "Aurangabad", "Arrah", "Palamu", "Bhabhua Road"],
    "janwarta.com": ["Chandauli"],
    "jansandeshtimes.in": ["Chandauli"],
    "ajhindidaily.com": ["Chandauli"],
}

# Google News carries few stories of the three Varanasi dailies, so their own WordPress feeds are read too:
# (paper's domain, feed address, keep only items naming Chandauli / DDU / Mughalsarai?). Chandauli and DDU stories
# are often filed under Varanasi; a site search feed (?s=word&feed=rss2) finds them wherever they are filed.
AREA_WORDS = ["चंदौली", "मुगलसराय", "पीडीडीयू", "डीडीयू", "दीनदयाल उपाध्याय नगर", "दीन दयाल उपाध्याय नगर",
              "Chandauli", "Mughalsarai", "PDDU", "DDU"]
SITE_FEEDS = [
    ("janwarta.com", "https://janwarta.com/state-news/uttar-pradesh/chandauli/feed/", False),
    ("janwarta.com", "https://janwarta.com/varanasi/feed/", True),
    ("jansandeshtimes.in", "https://jansandeshtimes.in/category/state/uttar-pradesh/chandauli/feed/", False),
    ("jansandeshtimes.in", "https://jansandeshtimes.in/category/state/uttar-pradesh/varanasi/feed/", True),
    ("jansandeshtimes.in", "https://jansandeshtimes.in/feed/", True),
    ("ajhindidaily.com", "https://ajhindidaily.com/chandauli/feed", False),
    ("ajhindidaily.com", "https://ajhindidaily.com/varanasi/feed", True),
    ("ajhindidaily.com", "https://ajhindidaily.com/feed", True),
] + [(dom, "https://%s/?s=%s&feed=rss2" % (dom, word), True)
     for dom in ("janwarta.com", "jansandeshtimes.in") for word in ("चंदौली", "मुगलसराय", "पीडीडीयू", "डीडीयू")]
