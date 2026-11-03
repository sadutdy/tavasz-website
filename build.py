#!/usr/bin/env python3
"""Generates index.html, river-hill/index.html and manjumala-resort/index.html.

Edit the data below, run `python3 build.py`, commit. Shared look is in assets/site.css + assets/extra.css,
shared behaviour in assets/site.js. Only the River Hill page loads assets/map.js.
"""
import json, os
from html import escape as esc
from urllib.parse import quote

ROOT = os.path.dirname(os.path.abspath(__file__))
WA = "919072818506"                      # WhatsApp number for every booking button (country code, no +)
PHONES = [("+91 90728 18506", "+919072818506"), ("+91 96564 41064", "+919656441064")]
IG = "https://www.instagram.com/tavasz.co/"

# ------------------------------------------------------------------ property data
RH = dict(
    slug="river-hill", name="River Hill", full="River Hill by Tavasz", dir="img/river-hill",
    place="Anakkampoyil, Thiruvambady, Kozhikode",
    address="Near Christian Church, Karimbu Road, Anakkampoyil, Kozhikode 673603, Kerala",
    title="River Hill by Tavasz | Resort stay in Anakkampoyil, Kozhikode",
    desc="River Hill by Tavasz: cottages, a pool deck, private river access and a play area near Aripara waterfall, Anakkampoyil, Kozhikode. Book on WhatsApp.",
    h1='River Hill,<br>above the <em>clouds.</em>',
    lead="Cottages in the trees, a pool deck, private river access and room for up to 20 guests. Hidden in the Western Ghats foothills near Aripara waterfall.",
    hero=[("02", "Lawn and play area"), ("07", "Cottage with deer garden"), ("03", "Garden cottage"),
          ("04", "Viewing deck on the rock"), ("08", "Pool at night"), ("09", "Deer garden")],
    hud=[("n", "4", "rooms, AC or non-AC"), ("n", "20", "guests, whole property"), ("t", "River", "private access"), ("t", "3 PM", "check-in"), ("t", "12 PM", "check-out")],
    cards=[("01", "Pool deck", "Kids' swimming pool, 6 m by 2 m, with a timber deck. Up to 5 in the pool at a time."),
           ("03", "Cottages in the trees", "Four rooms, AC or non-AC, each with a balcony and an attached bathroom."),
           ("06", "Loft cottage", "A loft-style cottage with a sleeping platform above the living area."),
           ("04", "Viewing deck", "A deck on the rock with views over the hills. Good for photos."),
           ("10", "Play and games", "Kids' play area, swings, carrom and a shuttle court."),
           ("17", "Private river access", "The river runs just below the property. Rocks, clear water and shade.")],
    amen=[("Kids' swimming pool", "6 m by 2 m, max 5 at a time"), ("Private river access", ""), ("Trekking on foot", ""),
          ("Campfire", "Setup ₹500 extra"), ("Speaker and mic", ""), ("Photoshoot spots", ""), ("Kids' play area", ""),
          ("Carrom", ""), ("Shuttle court", ""), ("Free Wi-Fi", ""), ("Barbecue grill", ""), ("TV", ""), ("Parking", ""),
          ("Tents available", "Ask us"), ("4 rooms, AC or non-AC", "Balcony and attached bathroom"),
          ("1 outside bathroom", ""), ("Kitchen", "₹500 extra"), ("Breakfast", ""), ("Fridge", ""), ("Extra beds", "If needed")],
    rates=[("Whole property", "₹22,000", "", "Up to 20 guests. The whole property is yours for the stay."),
           ("Per person", "₹1,000", "/ guest", "Guests above 10 years. Kids 6 to 12 years: ₹500.")],
    extras=[("Campfire setup", "₹500"), ("Kitchen use", "₹500"), ("Extra beds", "On request"), ("Tent stay", "On request")],
    food=("Breakfast", ["Vellappam, porotta or noolputtu", "Kadala curry, egg curry, green peas, cherupayar", "Tea"],
          "Ask us about meals for large groups."),
    nearby=["Pathangayam", "Thusharagiri Falls (13.6 km)", "Narangthodu", "Arippara (4 km)", "Marippuzha"],
    map=True, maplink=None,
    fly=dict(vdir="video/river-hill", points=[
        ("Cottages, pool deck and viewing rock", "All in one frame, tucked into the trees."),
        ("The river below", "Rocks, clear pools and shade, a short walk down."),
        ("The hills behind", "See how green and quiet the setting is before you book.")],
        clips=[("fly-over", "Fly-over"), ("reel", "Tavasz reel")]),
    ld=dict(name="River Hill by Tavasz", addr="Anakkampoyil", region="Kozhikode", zip="673603", lat=11.4310625, lng=76.0864375),
)
MJ = dict(
    slug="manjumala-resort", name="Manjumala Resort", full="Manjumala Resort by Tavasz", dir="img/manjumala",
    place="Kodanchery, Thusharagiri, Kozhikode",
    address="Thusharagiri, Kodanchery, Kozhikode 673580, Kerala",
    title="Manjumala Resort by Tavasz | Pool resort near Thusharagiri, Kozhikode",
    desc="Manjumala Resort by Tavasz: a big swimming pool, mud football turf, terrace hall and rooms for groups near Thusharagiri waterfalls, Kodanchery, Kozhikode. Book on WhatsApp.",
    h1='Manjumala,<br>by the <em>falls.</em>',
    lead="A 16 m pool, a mud football turf, a covered terrace hall and space for groups of up to 60. Just 3.3 km from Thusharagiri waterfalls.",
    hero=[("01", "Swimming pool"), ("03", "Pool from above"), ("09", "Kids' play area"),
          ("07", "Carrom on the terrace"), ("02", "Pool in daylight"), ("19", "Guest wing at night")],
    hud=[("n", "6", "rooms, plus dormitory"), ("n", "60", "guests, max capacity"), ("t", "16 m", "swimming pool"), ("t", "3 PM", "check-in"), ("t", "12 PM", "check-out")],
    cards=[("01", "Big swimming pool", "16 m by 7 m, with a separate kids' pool (6 m by 3 m) and a slide."),
           ("06", "Terrace hall", "A large covered terrace with carrom, speaker and mic. Good for groups."),
           ("10", "Rooms and dormitory", "6 rooms, 5 with attached bathrooms, plus a dormitory for 11 adults."),
           ("09", "Kids' play area", "Swings and play equipment right next to the pool."),
           ("18", "Mud football turf", "A mud turf for the group, with goal posts and a net fence."),
           ("17", "Kitchen and dining", "A kitchen you can use (₹500 extra) and a dining area. Homely night food on request.")],
    amen=[("Big swimming pool", "16 m by 7 m"), ("Kids' pool", "6 m by 3 m"), ("Mud football turf", ""),
          ("Trekking on foot", "With a view point"), ("Campfire", "Setup ₹500 extra"), ("Speaker and mic", ""),
          ("Kids' play area", ""), ("Carrom", ""), ("Barbecue grill", ""), ("Parking", ""), ("Wi-Fi", ""),
          ("6 rooms", "5 with attached bathrooms"), ("Dormitory", "11 adults"), ("3 outside bathrooms", ""),
          ("Kitchen", "₹500 extra"), ("Breakfast", ""), ("Homely night food", "Paid"), ("Fridge", ""), ("Extra beds", "If needed")],
    rates=[("25 or more guests", "₹900", "/ guest", "Our best rate for bigger groups, up to 60 guests. Kids 6 to 12 years: ₹400."),
           ("Under 25 guests", "₹1,000", "/ guest", "Per person for smaller groups. Kids 6 to 12 years: ₹400.")],
    extras=[("Campfire setup", "₹500"), ("Kitchen use", "₹500"), ("Night food", "Paid, ask us"), ("Extra beds", "On request")],
    food=("Breakfast (vegetarian)", ["Appam, puttu or upma", "Kadala curry, green peas, cherupayar", "Tea"],
          "Homely night food is available at extra cost."),
    nearby=["Thusharagiri Waterfalls (3.3 km, about 10 min)", "Pathangayam Waterfalls", "Anakkampoyil", "Narangthodu", "Marippuzha",
            "Knowledge City", "View point", "Wayanad", "Wayanad Churam"],
    map=False, maplink="https://maps.app.goo.gl/ZqbPNL8A921zPHSq5?g_st=ic",
    fly=dict(vdir="video/manjumala", points=[
        ("The pool and kids' pool", "See the size of the pool before you plan the day."),
        ("The mud turf and open ground", "Space for a match, games and the kids to run."),
        ("The green hills around", "Palms, forest and quiet roads close to the falls.")],
        clips=[("fly-over", "Fly-over")]),
    ld=dict(name="Manjumala Resort by Tavasz", addr="Thusharagiri, Kodanchery", region="Kozhikode", zip="673580", lat=11.4537369, lng=76.0483804),
)
# gallery lists: (file number, caption)
RH["gallery"] = [("01", "Pool deck"), ("02", "Lawn and play area"), ("03", "Garden cottage"), ("04", "Viewing deck"),
                 ("05", "Bedroom with hill view"), ("06", "Loft cottage"), ("07", "Cottage with deer garden"), ("08", "Pool at night"),
                 ("09", "Deer garden"), ("10", "Swing"), ("11", "Balcony bedroom"), ("12", "Lounge"), ("13", "Loft bedroom"),
                 ("14", "Loft living area"), ("15", "Loft bed"), ("16", "Cottage balcony"), ("17", "The river"), ("18", "Courtyard"),
                 ("19", "Lawn"), ("20", "Kids' play area"), ("21", "Pool"), ("22", "Bedroom"), ("23", "Cottage"),
                 ("24", "Rock deck and cottages"), ("25", "Cottage garden")]
MJ["gallery"] = [("01", "Swimming pool"), ("02", "Pool in daylight"), ("03", "Pool from above"), ("04", "Pool and the painted wing"),
                 ("05", "Pool slide"), ("06", "Open terrace hall"), ("07", "Carrom on the terrace"), ("08", "Terrace hall"),
                 ("09", "Kids' play area"), ("10", "Bedroom"), ("11", "Bedroom"), ("12", "Bedroom"), ("13", "Bedroom"),
                 ("14", "Bedroom"), ("15", "Bedroom"), ("16", "Kitchen"), ("17", "Dining area"), ("18", "Mud football turf"),
                 ("19", "Guest wing at night"), ("20", "Entrance"), ("21", "View from the stairs"), ("22", "Bathroom"), ("23", "Slide at night")]
PROPS = [RH, MJ]

RULES = [
    "<b>Check-in 3 PM, check-out 12 PM.</b>",
    "<b>ID proof</b> is needed for every guest. Foreign guests are welcome.",
    "Loud speakers are not allowed after 10 PM.",
    "Drugs are not allowed. Ask us about alcohol before you book.",
    "Pets are not allowed.",
    "<b>No refunds.</b> You can change your dates.",
]


# ------------------------------------------------------------------ shared pieces
def head(title, desc, rel, ld=""):
    return f'''<!doctype html>
<html lang="en">
<head>
<meta charset="utf-8">
<meta name="viewport" content="width=device-width,initial-scale=1">
<title>{esc(title)}</title>
<meta name="description" content="{esc(desc)}">
<meta name="theme-color" content="#050a08">
<link rel="icon" href="{rel}assets/logo.jpg">
<link rel="apple-touch-icon" href="{rel}assets/logo.jpg">
<meta property="og:title" content="{esc(title)}">
<meta property="og:description" content="{esc(desc)}">
<meta property="og:type" content="website">
<link rel="stylesheet" href="{rel}assets/site.css">
<link rel="stylesheet" href="{rel}assets/extra.css">
{ld}
</head>
<body>
<canvas id="bg" aria-hidden="true"></canvas>
'''


def nav(rel, logo_name, logo_small, links):
    a = "".join(f'<a href="{h}">{t}</a>' for t, h in links)
    home = "#top" if rel == "" else "../"
    sm = f' <small style="font:500 12px ui-monospace,monospace;color:var(--mut);letter-spacing:.1em">{logo_small}</small>' if logo_small else ""
    return f'''<nav>
  <div class="wrap">
    <a class="logo" href="{home}"><img src="{rel}assets/logo.jpg" alt="" width="34" height="34">{esc(logo_name)}{sm}</a>
    <div class="links">{a}</div>
    <a class="btn solid" href="#book">Book now</a>
  </div>
</nav>
'''


def hero(rel, slides, caps, eyebrow, h1, lead, ctas, hud, home=False):
    s = []
    for k, (src, alt) in enumerate(slides):
        if k == 0:
            s.append(f'    <div class="s on"><img src="{rel}{src}" alt="{esc(alt)}" fetchpriority="high" decoding="async"></div>')
        else:
            s.append(f'    <div class="s"><img data-src="{rel}{src}" alt="{esc(alt)}" decoding="async"></div>')
    hud_html = ""
    for kind, val, lab in hud:
        b = f'<b data-n="{val}">0</b>' if kind == "n" else f'<b>{esc(val)}</b>'
        hud_html += f'<div>{b}<span>{esc(lab)}</span></div>'
    cta = "".join(f'<a class="btn{" solid" if i == 0 else ""}" href="{h}">{t}</a>' for i, (t, h) in enumerate(ctas))
    return f'''<header class="hero{" home" if home else ""}" id="top">
  <div class="hc" id="hc" data-caps="{esc(json.dumps(caps))}" aria-roledescription="carousel" aria-label="Photos">
{chr(10).join(s)}
  </div>
  <div class="hc-ui">
    <div class="dots" id="hcDots"></div>
    <span class="hc-cap" id="hcCap"></span>
    <div class="hc-nav"><button id="hcPrev" aria-label="Previous photo">←</button><button id="hcNext" aria-label="Next photo">→</button></div>
  </div>
  <div class="wrap">
    <span class="mono">// {eyebrow}</span>
    <h1>{h1}</h1>
    <p class="lead">{lead}</p>
    <div class="cta">{cta}</div>
    <div class="hud{" five" if len(hud) == 5 else ""}">{hud_html}</div>
  </div>
</header>
'''


def booking(prop_options, num):
    sel = ""
    if prop_options:
        opts = "".join(f'<option value="{esc(p)}">{esc(p)}</option>' for p in prop_options)
        sel = f'<div class="full"><label for="prop">Property</label><select id="prop">{opts}</select></div>'
    ph = " · ".join(f'<a href="tel:{t}" style="color:var(--g)">{d}</a>' for d, t in PHONES)
    return f'''<section id="book">
  <div class="wrap">
    <div class="book rv">
      <div>
        <span class="mono">{num} / Book</span>
        <h2>Tell us when. We reply on WhatsApp.</h2>
        <p>Fill this in and it opens WhatsApp with your request ready to send. No sign-up and no payment on this page. We confirm availability and the rate before you pay.</p>
        <p style="margin-top:22px"><b style="color:var(--txt)">Call or WhatsApp:</b><br>{ph}</p>
      </div>
      <form id="bf">
        {sel}
        <div><label for="n">Name</label><input id="n" required placeholder="Your name" autocomplete="name"></div>
        <div><label for="g">Guests</label><input id="g" type="number" min="1" value="2" inputmode="numeric"></div>
        <div><label for="d1">Check in</label><input id="d1" type="date" required></div>
        <div><label for="d2">Check out</label><input id="d2" type="date" required></div>
        <div class="full"><label for="t">Who is coming</label><select id="t"><option>Family</option><option>Couple</option><option>Friends</option><option>Mixed group</option></select></div>
        <div class="full"><label for="note">Note (optional)</label><input id="note" placeholder="Occasion, food, questions"></div>
        <div class="full"><button class="btn solid" style="width:100%;justify-content:center" type="submit">Send on WhatsApp</button><p class="note">Opens WhatsApp. Availability and rate are confirmed by the Tavasz team.</p></div>
      </form>
    </div>
  </div>
</section>
'''


def footer(left_title, left_text, extra=""):
    return f'''<footer>
  <div class="wrap">
    <div><b>{left_title}</b><br>{left_text}</div>
    <div><b>Follow</b><br><a href="{IG}" target="_blank" rel="noopener">Instagram @tavasz.co</a>{extra}</div>
    <div>© <span data-yr></span> Tavasz. All rights reserved.</div>
  </div>
</footer>
'''


def tail(prop_for_wa, scripts):
    msg = f"Hi Tavasz, I'd like to book a stay at {prop_for_wa}." if prop_for_wa else "Hi Tavasz, I'd like to book a stay."
    return f'''<a class="fab" href="https://wa.me/{WA}?text={quote(msg)}" target="_blank" rel="noopener" aria-label="Chat on WhatsApp">✆</a>
<script>window.TAVASZ={{wa:"{WA}",prop:{json.dumps(prop_for_wa or "Tavasz")}}};</script>
{scripts}
</body>
</html>
'''


# ------------------------------------------------------------------ property page
def property_page(p):
    rel = "../"
    d = p["dir"]
    slides = [(f"{d}/{n}.jpg", f"{cap} at {p['name']}") for n, cap in p["hero"]]
    caps = [c for _, c in p["hero"]]
    links = [("Stay", "#stay"), ("From above", "#flyover"), ("Rates", "#rates"), ("Gallery", "#gallery"), ("Nearby", "#nearby"), ("Book", "#book")]
    ld = json.dumps({
        "@context": "https://schema.org", "@type": "Resort", "name": p["ld"]["name"],
        "description": p["desc"], "image": f"{d}/{p['hero'][0][0]}.jpg",
        "telephone": PHONES[0][1], "checkinTime": "15:00", "checkoutTime": "12:00",
        "address": {"@type": "PostalAddress", "streetAddress": p["ld"]["addr"], "addressLocality": p["ld"]["region"],
                    "postalCode": p["ld"]["zip"], "addressRegion": "Kerala", "addressCountry": "IN"},
        "geo": {"@type": "GeoCoordinates", "latitude": p["ld"]["lat"], "longitude": p["ld"]["lng"]},
        "sameAs": [IG]})
    out = head(p["title"], p["desc"], rel, f'<script type="application/ld+json">{ld}</script>')
    out += nav(rel, p["name"], "BY TAVASZ", links)
    out += hero(rel, slides, caps, p["place"], p["h1"], p["lead"],
                [("Check availability", "#book"), ("▶ Watch from above", "#flyover")], p["hud"])

    cards = ""
    for i, (n, t, desc) in enumerate(p["cards"], start=1):
        cards += (f'<article class="card rv"><div class="glow"></div><div class="art ph"><img src="{rel}{d}/th/{n}.jpg" '
                  f'alt="{esc(t)} at {esc(p["name"])}" loading="lazy"></div><div class="body"><span class="mono">0{i}</span>'
                  f'<h3>{esc(t)}</h3><p>{esc(desc)}</p></div></article>')
    amen = "".join(f"<li>{esc(a)}{f'<small>{esc(b)}</small>' if b else ''}</li>" for a, b in p["amen"])
    out += f'''<section id="stay">
  <div class="wrap">
    <div class="sec-h rv"><span class="mono">01 / The stay</span><h2>What you get.</h2><p>{esc(p["name"])} is booked as a whole property for your group. Here is what is included.</p></div>
    <div class="grid">{cards}</div>
    <div class="sec-h rv" style="margin:64px 0 24px"><span class="mono">Amenities</span><h2 style="font-size:clamp(28px,4vw,44px)">Everything on site.</h2></div>
    <ul class="amen rv">{amen}</ul>
  </div>
</section>
'''

    fl = p["fly"]
    first = fl["clips"][0]
    pts = "".join(f"<li>{esc(a)}<small>{esc(b)}</small></li>" for a, b in fl["points"])
    chips = ""
    if len(fl["clips"]) > 1:
        chips = '<div class="clips" role="tablist" aria-label="Choose a video">' + "".join(
            f'<button type="button" role="tab" class="{"on" if i == 0 else ""}" data-src="{rel}{fl["vdir"]}/{f}.mp4" '
            f'data-poster="{rel}{fl["vdir"]}/{f}.jpg" data-label="{esc(lab)}">{esc(lab)}</button>'
            for i, (f, lab) in enumerate(fl["clips"])) + "</div>"
    out += f'''<section id="flyover">
  <div class="wrap">
    <div class="sec-h rv"><span class="mono">02 / From above</span><h2>See it from above.</h2><p>Drone footage of {esc(p["name"])}. It plays on its own while you watch and stops when you scroll away. Tap the video to pause.</p></div>
    <div class="fly rv">
      <div class="ftxt"><ul>{pts}</ul>{chips}</div>
      <div class="phone">
        <video class="fv" muted loop playsinline preload="none" poster="{rel}{fl["vdir"]}/{first[0]}.jpg" data-src="{rel}{fl["vdir"]}/{first[0]}.mp4" aria-label="Drone video of {esc(p["name"])}"></video>
        <span class="vpb" aria-hidden="true">▶</span>
        <span class="vcap">{esc(first[1])}</span>
        <div class="vbarw" aria-hidden="true"><div class="vbar"><i></i></div></div>
      </div>
    </div>
  </div>
</section>
'''

    r = "".join(f'<div class="box rate rv"><span class="mono">{esc(t)}</span><span class="price">{esc(pr)}<small>{esc(u)}</small></span><p class="sub">{esc(s)}</p></div>'
                for t, pr, u, s in p["rates"])
    ex = "".join(f"<li><b>{esc(a)}</b>: {esc(b)}</li>" for a, b in p["extras"])
    rules = "".join(f"<li>{x}</li>" for x in RULES)
    ft, fl, fn = p["food"]
    food = "".join(f"<li>{esc(x)}</li>" for x in fl)
    out += f'''<section id="rates" style="background:linear-gradient(180deg,transparent,rgba(61,255,160,.04),transparent)">
  <div class="wrap">
    <div class="sec-h rv"><span class="mono">03 / Rates and rules</span><h2>Clear prices. Simple rules.</h2><p>These are our direct rates. We confirm your dates and the final amount on WhatsApp before you pay.</p></div>
    <div class="three">{r}<div class="box rv"><h3>Extras</h3><ul>{ex}</ul></div></div>
    <div class="two" style="margin-top:22px">
      <div class="box rv"><h3>House rules</h3><ul>{rules}</ul></div>
      <div class="box rv"><h3>{esc(ft)}</h3><ul>{food}</ul><p class="srcnote">{esc(fn)}</p></div>
    </div>
  </div>
</section>
'''

    gal = "".join(f'<a href="{rel}{d}/{n}.jpg" data-lb><img src="{rel}{d}/th/{n}.jpg" alt="{esc(cap)} at {esc(p["name"])}" loading="lazy" '
                  f'style="width:100%;height:auto;display:block"><span>{esc(cap)}</span></a>' for n, cap in p["gallery"])
    out += f'''<section id="gallery">
  <div class="wrap">
    <div class="sec-h rv"><span class="mono">04 / Gallery</span><h2>See it before you book.</h2><p>Tap any photo to enlarge. More reels and guest stories on our Instagram.</p></div>
    <div class="ig rv">{gal}</div>
    <p style="margin-top:26px"><a class="btn" href="{IG}" target="_blank" rel="noopener">@tavasz.co on Instagram →</a></p>
  </div>
</section>
'''

    pills = "".join(f"<span>{esc(x)}</span>" for x in p["nearby"])
    if p["map"]:
        out += f'''<section id="nearby">
  <div class="wrap">
    <div class="sec-h rv"><span class="mono">05 / Nearby</span><h2>Your weekend map.</h2><p>Tap a place to see how far it is from {esc(p["name"])}. The map is a sketch, not to scale in direction.</p></div>
    <div class="chips rv" id="mapChips" role="tablist" aria-label="Filter places"></div>
    <div class="mapw rv">
      <div class="mapbox"><svg id="mapSvg" viewBox="-150 0 930 600" role="img" aria-label="Map of places around {esc(p["name"])}"></svg></div>
      <aside class="mpanel" id="mPanel" aria-live="polite"></aside>
    </div>
    <div class="mlist rv" id="mList"></div>
    <p class="srcnote" style="margin-top:26px">Also close by:</p>
    <div class="pills rv" style="margin-top:10px">{pills}</div>
  </div>
</section>
'''
    else:
        ml = (f'<p style="margin-top:26px"><a class="btn" href="{p["maplink"]}" target="_blank" rel="noopener">Open location in Google Maps →</a></p>'
              if p["maplink"] else "")
        out += f'''<section id="nearby">
  <div class="wrap">
    <div class="sec-h rv"><span class="mono">05 / Nearby</span><h2>Close to the best of the hills.</h2><p>Ask us for the route and timing to any of these. We plan the day with you.</p></div>
    <div class="pills rv">{pills}</div>
    {ml}
  </div>
</section>
'''

    out += booking(None, "06")
    out += footer(esc(p["full"]), esc(p["address"]), ' · <a href="../">All Tavasz stays</a>')
    scripts = '<script src="../assets/site.js"></script>\n<script src="../assets/video.js"></script>' +('\n<script src="../assets/map.js"></script>' if p["map"] else "")
    out += tail(p["name"], scripts)
    return out


# ------------------------------------------------------------------ home page
def home_page():
    rel = ""
    t = "Tavasz | Resort stays near Thusharagiri and Anakkampoyil, Kozhikode"
    dsc = "Tavasz runs pool resorts and hill stays near Thusharagiri and Anakkampoyil in Kozhikode, Kerala. River Hill and Manjumala Resort. Book direct on WhatsApp."
    ld = json.dumps({"@context": "https://schema.org", "@type": "Organization", "name": "Tavasz", "description": dsc,
                     "telephone": PHONES[0][1], "sameAs": [IG]})
    out = head(t, dsc, rel, f'<script type="application/ld+json">{ld}</script>')
    out += nav(rel, "Tavasz", "", [("Stays", "#stays"), ("Why direct", "#direct"), ("Book", "#book")])
    slides = [("img/river-hill/02.jpg", "Lawn and play area at River Hill"), ("img/manjumala/01.jpg", "Swimming pool at Manjumala Resort"),
              ("img/river-hill/07.jpg", "Cottage with deer garden at River Hill"), ("img/manjumala/03.jpg", "Manjumala Resort pool from above"),
              ("img/river-hill/04.jpg", "Viewing deck at River Hill"), ("img/manjumala/02.jpg", "Manjumala Resort pool in daylight")]
    caps = ["River Hill · Anakkampoyil", "Manjumala Resort · Thusharagiri", "River Hill · Anakkampoyil",
            "Manjumala Resort · Thusharagiri", "River Hill · Anakkampoyil", "Manjumala Resort · Thusharagiri"]
    out += hero(rel, slides, caps, "Kozhikode · Kerala", "Hills, pools<br>and <em>waterfalls.</em>",
                "Pool resorts and hill stays near Thusharagiri and Anakkampoyil, for families, couples and groups. Pick a property, send one WhatsApp message, done.",
                [("Check availability", "#book"), ("See our stays", "#stays")],
                [("n", "2", "stays online now"), ("t", "Pools", "at both properties"), ("t", "Falls", "and river trails close by"), ("t", "3 PM", "check-in"), ("t", "12 PM", "check-out")],
                home=True)

    def pcard(p, tags, frm):
        d = p["dir"]
        tg = "".join(f"<span>{esc(x)}</span>" for x in tags)
        return (f'<a class="pcard rv" href="{p["slug"]}/"><div class="pimg"><img src="{d}/th/{p["hero"][0][0]}.jpg" alt="{esc(p["name"])}" loading="lazy"></div>'
                f'<div class="pbody"><span class="mono">{esc(p["place"])}</span><h3>{esc(p["name"])}</h3><p>{esc(p["lead"])}</p>'
                f'<div class="tags">{tg}</div><div class="go"><span class="from">{frm}</span><span class="btn">View stay →</span></div></div></a>')
    c1 = pcard(RH, ["Kids' pool", "Private river", "Up to 20 guests", "Play area"], "Whole property <b>₹22,000</b>")
    c2 = pcard(MJ, ["16 m pool", "Mud turf", "Up to 60 guests", "Terrace hall"], "<b>₹900</b> per guest for 25 or more")
    out += f'''<section id="stays">
  <div class="wrap">
    <div class="sec-h rv"><span class="mono">01 / Stays</span><h2>Choose your hideout.</h2><p>Each property is booked as a whole for your group. Rates are shown on each page.</p></div>
    <div class="pgrid">{c1}{c2}
      <div class="pcard soon rv" style="grid-column:1/-1;min-height:170px"><span class="mono">Coming soon</span><h3>More Tavasz stays</h3><p>We are adding more properties. Follow us on Instagram or message us to hear first.</p></div>
    </div>
  </div>
</section>
<section id="direct" style="background:linear-gradient(180deg,transparent,rgba(61,255,160,.04),transparent)">
  <div class="wrap">
    <div class="sec-h rv"><span class="mono">02 / Book direct</span><h2>Talk to the people who run the stay.</h2><p>No agent in between. You message us, we answer, and the rate you see is the rate we charge.</p></div>
    <div class="three">
      <div class="box rv"><h3>One WhatsApp message</h3><p>Send your dates and group size. We check availability and reply on WhatsApp.</p></div>
      <div class="box rv"><h3>Clear rates</h3><p>Rates, extras and house rules are listed on every property page, so there are no surprises at check-in.</p></div>
      <div class="box rv"><h3>Simple policy</h3><p>Check-in 3 PM, check-out 12 PM. No refunds, but you can change your dates.</p></div>
    </div>
    <p style="margin-top:26px"><a class="btn" href="{IG}" target="_blank" rel="noopener">See our reels: @tavasz.co →</a></p>
  </div>
</section>
'''
    out += booking(["River Hill", "Manjumala Resort"], "03")
    out += footer("Tavasz", "Pool resorts and hill stays<br>Kozhikode, Kerala",
                  ' · <a href="river-hill/">River Hill</a> · <a href="manjumala-resort/">Manjumala Resort</a>')
    out += tail(None, '<script src="assets/site.js"></script>')
    return out


def write(path, text):
    full = os.path.join(ROOT, path)
    os.makedirs(os.path.dirname(full), exist_ok=True)
    with open(full, "w", encoding="utf-8") as f:
        f.write(text)
    print("wrote", path, f"{len(text):,} bytes")


if __name__ == "__main__":
    for p in PROPS:
        for n, _ in p["gallery"] + p["hero"]:
            assert os.path.exists(os.path.join(ROOT, p["dir"], f"{n}.jpg")), (p["slug"], n)
        for n, *_ in p["cards"]:
            assert os.path.exists(os.path.join(ROOT, p["dir"], "th", f"{n}.jpg")), (p["slug"], n)
    write("index.html", home_page())
    for p in PROPS:
        write(f'{p["slug"]}/index.html', property_page(p))
