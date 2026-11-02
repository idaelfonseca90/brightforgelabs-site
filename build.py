#!/usr/bin/env python3
"""Builds the Brightforge Labs website into public/.

Each page is plain HTML with the stylesheet inlined, so a visit needs a single
request to show the page. Run: python3 build.py
"""
import json
import re
from datetime import date
from pathlib import Path

ROOT = Path(__file__).parent
SRC = ROOT / "src"
OUT = ROOT / "public"

SITE = "https://brightforgelabs.app"
EMAIL = "hello@brightforgelabs.app"
UPDATED = "2026-10-31"
UPDATED_TEXT = "October 31, 2026"
DESCRIPTION = ("Brightforge Labs LLC is the Florida software company behind FadeReady for barbershops, "
               "LaneTally for trucking, SizeGuard for traders and Nail Signature for nail salons: "
               "simple, fast, beautiful apps for small businesses and independent pros.")


def css():
    text = (SRC / "styles.css").read_text()
    text = re.sub(r"/\*.*?\*/", "", text, flags=re.S)
    text = re.sub(r"\s*\n\s*", "", text)
    return text


def mark(prefix, cls="", label=None):
    svg = (SRC / "mark.svg").read_text().replace("bf-", f"{prefix}-")
    svg = svg.replace('<?xml version="1.0"?>', "")
    if label is None:
        svg = svg.replace('role="img" aria-label="Brightforge Labs"', 'aria-hidden="true" focusable="false"')
    if cls:
        svg = svg.replace("<svg ", f'<svg class="{cls}" ', 1)
    return re.sub(r">\s+<", "><", svg.strip())


def icon(paths):
    return ('<svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2.2" '
            f'stroke-linecap="round" stroke-linejoin="round" aria-hidden="true">{paths}</svg>')


ICONS = {
    "simple": icon('<path d="M20 6 9 17l-5-5"/>'),
    "fast": icon('<path d="M13 2 3 14h9l-1 8 10-12h-9z"/>'),
    "beautiful": icon('<path d="M12 3l1.9 5.1L19 10l-5.1 1.9L12 17l-1.9-5.1L5 10l5.1-1.9z"/><path d="M19 17v4M17 19h4"/>'),
    "secure": icon('<path d="M12 3 4 6v6c0 5 3.4 8.4 8 9 4.6-.6 8-4 8-9V6z"/><path d="m9 12 2 2 4-4"/>'),
    "scissors": icon('<circle cx="6" cy="6" r="3"/><circle cx="6" cy="18" r="3"/><path d="M20 4 8.12 15.88M14.47 14.48 20 20M8.12 8.12 12 12"/>'),
    "plus": icon('<path d="M12 5v14M5 12h14"/>'),
    "chart": icon('<path d="M3 3v18h18"/><path d="m7 15 4-4 3 3 6-6"/><path d="M16 8h4v4"/>'),
    "sparkle": icon('<path d="M12 3l1.9 5.1L19 10l-5.1 1.9L12 17l-1.9-5.1L5 10l5.1-1.9z"/>'),
    "mail": icon('<rect x="3" y="5" width="18" height="14" rx="2"/><path d="m3 7 9 6 9-6"/>'),
}

ORG = {
    "@type": "Organization",
    "@id": f"{SITE}/#organization",
    "name": "Brightforge Labs",
    "legalName": "Brightforge Labs LLC",
    "alternateName": ["Brightforge Labs LLC", "Brightforge"],
    "url": f"{SITE}/",
    "logo": {"@type": "ImageObject", "@id": f"{SITE}/#logo",
             "url": f"{SITE}/icons/logo-square-512.png", "width": 512, "height": 512,
             "caption": "Brightforge Labs"},
    "image": {"@id": f"{SITE}/#logo"},
    "description": DESCRIPTION,
    "slogan": "Bright ideas, forged into real apps.",
    "email": EMAIL,
    "foundingDate": "2026-10-24",
    "founder": {"@type": "Person", "name": "Idael Fonseca Hidalgo"},
    "address": {"@type": "PostalAddress", "addressRegion": "FL", "addressCountry": "US"},
    "contactPoint": {"@type": "ContactPoint", "contactType": "customer support",
                     "email": EMAIL, "url": f"{SITE}/support",
                     "availableLanguage": ["English", "Spanish"]},
    "knowsAbout": ["Trucking dispatch software", "Carrier management software", "Mobile apps", "Software for small businesses",
                   "Barbershop booking software", "Salon software",
                   "Trading tools", "Position size and stop size calculators", "Trading journals",
                   "Prop firm expense and payout tracking"],
    # Every app and website is owned directly by Brightforge Labs LLC (no separate LLC per app).
    "brand": [{"@type": "Brand", "name": "FadeReady", "url": "https://fadeready.com/"},
              {"@type": "Brand", "name": "SizeGuard", "url": "https://sizeguard.com/"},
              {"@type": "Brand", "name": "Nail Signature", "url": "https://nailsignature.com/"},
              {"@type": "Brand", "name": "LaneTally", "url": "https://lanetally.com/"}],
    # Add social profile links here as they are created, e.g. "https://www.linkedin.com/company/..."
    "sameAs": [],
}

FADEREADY = {
    "@type": "SoftwareApplication",
    "@id": f"{SITE}/#fadeready",
    "name": "FadeReady",
    "url": "https://fadeready.com/",
    "applicationCategory": "BusinessApplication",
    "description": ("FadeReady is an app for barbershops: online booking, a live line (queue), "
                    "apps for barbers and clients, bookkeeping, and license renewal reminders."),
    "author": {"@id": f"{SITE}/#organization"},
    "publisher": {"@id": f"{SITE}/#organization"},
}

APPS = [
    {"key": "fr", "slug": "fadeready", "name": "FadeReady", "ref": "FadeReady", "for": "For barbershops", "status": "soon", "icon": "scissors",
     "text": "Runs the whole barbershop day from one app. Clients book or join the line from their phone, barbers see who is next, and owners keep the books.",
     "features": ["Online booking and a live line", "Barber app and client app", "Bookkeeping and barber pay", "License renewal reminders"],
     "href": "https://fadeready.com/", "link": "Visit fadeready.com", "org": "Waiting list open"},
    {"key": "tr", "slug": "sizeguard", "name": "SizeGuard", "ref": "SizeGuard", "for": "For traders", "status": "soon", "icon": "chart",
     "text": "Everything a trader needs to plan, record and review. Built for futures, forex, stocks and crypto.",
     "features": ["Stop size calculator for 4 markets", "Trading journal and daily journal", "Prop firm tracker: evaluations, resets and fees", "Payout tracking, so you see what you really earn"],
     "href": "https://sizeguard.com/", "link": "Get launch news", "org": "In development"},
    {"key": "sl", "slug": "nail-signature", "name": "Nail Signature", "ref": "Nail Signature", "for": "For nail salons", "status": "soon", "icon": "sparkle",
     "text": "Everything FadeReady does for barbershops, made for nail salons.",
     "features": ["Online booking and a live line", "Nail tech app and client app", "Bookkeeping and team pay", "License renewal reminders"],
     "href": "https://nailsignature.com/", "link": "Visit nailsignature.com", "org": "Waiting list open"},
    {"key": "lt", "slug": "lanetally", "name": "LaneTally", "ref": "LaneTally", "for": "For trucking", "status": "soon", "icon": "chart",
     "text": "Truck dispatch and trucking accounting software for dispatchers, carriers and owner-operators. Loads, invoices, driver pay, IFTA and the books, in English and Spanish.",
     "features": ["Loads, dispatch board and live fleet map", "Driver app with stops, photos and chat", "Invoices, factoring and driver pay", "IFTA, fuel and cost per mile"],
     "href": "https://lanetally.com/", "link": "Visit lanetally.com", "org": "Waiting list open"},
]
STATUS = {"live": ('p-live', "Live"), "soon": ('p-soon', "Coming soon")}

FAQ = [
    ("What is Brightforge Labs?",
     "Brightforge Labs LLC is a software company in Florida, USA. It is the parent company that owns "
     "and builds our apps. We make simple, fast, beautiful apps for small businesses and independent pros, "
     "like barbers, salon owners and traders."),
    ("Who makes FadeReady?",
     "FadeReady is made by Brightforge Labs. FadeReady is an app for barbershops. It handles "
     "booking, the live line, barber and client apps, bookkeeping, and license renewals. "
     "FadeReady and fadeready.com are owned and run by Brightforge Labs LLC."),
    ("What apps does Brightforge Labs make?",
     "Four apps, all coming soon: FadeReady for barbershops (fadeready.com), Nail Signature for nail salons, "
     "which does everything FadeReady does (nailsignature.com), and LaneTally, truck dispatch and trucking accounting software "
     "(lanetally.com), all three with waiting lists open; plus SizeGuard, a trading toolkit with a stop size calculator "
     "for futures, forex, stocks and crypto, a trading journal, a daily journal and a prop firm tracker, "
     "in development (sizeguard.com)."),
    ("Who started Brightforge Labs?",
     "Brightforge Labs was started in 2026 by Idael Fonseca Hidalgo."),
    ("How do I contact Brightforge Labs?",
     f"Email us at {EMAIL}. We read every message."),
]

NAV = [("/#apps", "Apps"), ("/about", "About"), ("/contact", "Contact")]


def email_link(cls="", inner=None, addr=EMAIL):
    inner = inner or addr
    c = f' class="{cls}"' if cls else ""
    # email_off keeps Cloudflare from rewriting the address with an extra script.
    return f'<!--email_off--><a{c} href="mailto:{addr}">{inner}</a><!--/email_off-->'


def page(slug, title, description, body, current=None, extra_ld=(), page_type="WebPage", script=""):
    url = f"{SITE}/{slug}" if slug else f"{SITE}/"
    graph = [ORG,
             {"@type": "WebSite", "@id": f"{SITE}/#website", "url": f"{SITE}/",
              "name": "Brightforge Labs", "publisher": {"@id": f"{SITE}/#organization"},
              "inLanguage": "en-US"},
             {"@type": page_type, "@id": f"{url}#webpage", "url": url, "name": title,
              "description": description, "isPartOf": {"@id": f"{SITE}/#website"},
              "about": {"@id": f"{SITE}/#organization"}, "inLanguage": "en-US",
              "dateModified": UPDATED},
             *extra_ld]
    ld = json.dumps({"@context": "https://schema.org", "@graph": graph}, separators=(",", ":"))
    nav = "".join(
        f'<li><a href="{href}"{" aria-current=page" if label == current else ""}>{label}</a></li>'
        for href, label in NAV) + '<li><a class="nav-cta" href="/contact">Contact us</a></li>'
    foot_apps = "".join(
        f'<li><a href="/{a["slug"]}">{a["name"]}</a>{"" if a["status"] == "live" else " <small>(soon)</small>"}</li>'
        for a in APPS)
    return f"""<!doctype html>
<html lang="en">
<head>
<meta charset="utf-8">
<meta name="viewport" content="width=device-width,initial-scale=1">
<title>{title}</title>
<meta name="description" content="{description}">
<link rel="canonical" href="{url}">
<meta name="theme-color" content="#0b1220">
<meta name="color-scheme" content="light dark">
<link rel="icon" href="/favicon.ico" sizes="48x48">
<link rel="icon" href="/favicon.svg" type="image/svg+xml">
<link rel="icon" href="/favicon-96x96.png" type="image/png" sizes="96x96">
<link rel="apple-touch-icon" href="/apple-touch-icon.png">
<link rel="manifest" href="/site.webmanifest">
<meta property="og:type" content="website">
<meta property="og:site_name" content="Brightforge Labs">
<meta property="og:locale" content="en_US">
<meta property="og:title" content="{title}">
<meta property="og:description" content="{description}">
<meta property="og:url" content="{url}">
<meta property="og:image" content="{SITE}/og-image.jpg">
<meta property="og:image:width" content="1200">
<meta property="og:image:height" content="630">
<meta property="og:image:alt" content="Brightforge Labs: the company behind FadeReady, LaneTally, SizeGuard and Nail Signature.">
<meta name="twitter:card" content="summary_large_image">
<meta name="twitter:title" content="{title}">
<meta name="twitter:description" content="{description}">
<meta name="twitter:image" content="{SITE}/og-image.jpg">
<style>{css()}</style>
<script type="application/ld+json">{ld}</script>
</head>
<body>
<a class="skip" href="#main">Skip to content</a>
<header class="site-head">
<div class="wrap">
<a class="brand" href="/" aria-label="Brightforge Labs home">{mark("hd")}<span>Brightforge <b>Labs</b></span></a>
<nav aria-label="Main"><ul class="nav">{nav}</ul></nav>
</div>
</header>
<main id="main">
{body}
</main>
<footer class="site-foot">
<div class="wrap">
<div class="foot-grid">
<div class="foot-brand">
<a class="brand" href="/" aria-label="Brightforge Labs home">{mark("ft")}<span>Brightforge <b>Labs</b></span></a>
<p>Brightforge Labs LLC is a software company in Florida, USA. We own and build all our apps, including FadeReady.</p>
</div>
<div><h2>Company</h2><ul><li><a href="/about">About</a></li><li><a href="/contact">Contact</a></li><li><a href="/support">Support</a></li><li>{email_link()}</li></ul></div>
<div><h2>Apps</h2><ul>{foot_apps}</ul></div>
<div><h2>Legal</h2><ul><li><a href="/privacy">Privacy Policy</a></li><li><a href="/terms">Terms of Use</a></li></ul></div>
</div>
<div class="foot-base">
<p>© 2026 Brightforge Labs LLC. All rights reserved.</p>
<p>A Florida limited liability company · Florida, USA</p>
</div>
</div>
</footer>
{script}</body>
</html>
"""


def page_hero(kicker, h1, lead):
    return f"""<section class="page-hero">
<div class="wrap">
<p class="eyebrow"><i></i>{kicker}</p>
<h1>{h1}</h1>
<p class="lead">{lead}</p>
</div>
</section>"""


def value_list():
    items = [
        ("simple", "Simple", "Anyone can use our apps on day one. No training and no manual."),
        ("fast", "Fast", "Screens open in a blink, even on a weak phone signal."),
        ("beautiful", "Beautiful", "Clean, clear design that people enjoy using every day."),
        ("secure", "Secure", "Your data is protected and private. We never sell it."),
    ]
    return '<div class="values">' + "".join(
        f'<div class="value"><div class="ico">{ICONS[i]}</div><h3>{t}</h3><p>{d}</p></div>'
        for i, t, d in items) + "</div>"


def app_logo(key, size=56, cls="tile"):
    """The app's real icon, served small and sharp on any screen."""
    name = next(a["name"] for a in APPS if a["key"] == key)
    return (f'<img class="{cls} logo" src="/apps/{key}-128.webp" srcset="/apps/{key}-64.webp 64w, /apps/{key}-128.webp 128w, /apps/{key}-256.webp 256w" '
            f'sizes="{size}px" width="{size}" height="{size}" alt="{name} logo" decoding="async">')


def pill(status):
    cls, label = STATUS[status]
    return f'<span class="pill {cls}">{label}</span>'


def app_cards():
    out = []
    for a in APPS:
        feats = "".join(f"<li>{f}</li>" for f in a["features"])
        out.append(f"""<article class="app" id="{a['key']}">
<div class="app-top">{app_logo(a['key'])}<div><h3>{a['name']}</h3><span class="for">{a['for']}</span></div>{pill(a['status'])}</div>
<p>{a['text']}</p>
<ul class="feat">{feats}</ul>
<a class="more" href="/{a['slug']}">Learn more about {a['ref']} <span aria-hidden="true">→</span></a>
</article>""")
    return '<div class="apps">' + "".join(out) + "</div>"


def org_chart():
    kids = "".join(
        f'<li>{app_logo(a["key"], 38)}<div><b>{a["name"]}</b><small>{a["org"]}</small></div>{pill(a["status"])}</li>'
        for a in APPS)
    return f"""<div class="org" role="group" aria-label="Brightforge Labs and its apps">
<p class="org-cap">Our company</p>
<div class="org-parent">{mark("org")}<div><strong>Brightforge Labs LLC</strong><span>Parent company · Florida, USA</span></div></div>
<ul class="org-kids">{kids}</ul>
</div>"""


def forge():
    """The logo as a living forge: the spark strikes the anvil, embers fly, and the apps it made float around it."""
    m = 3.4  # logo scale inside the 400x400 emblem
    o = 200 - 32 * m
    tiles = [("fr", "o1", "scissors"), ("tr", "o2", "chart"), ("sl", "o3", "sparkle"), ("lt", "o4", "chart")]
    cards = "".join(
        f'<a class="orb {pos}" href="#{k}" aria-label="{a["name"]}: see the app">{app_logo(k, 36)}<div><b>{a["name"]}</b>{pill(a["status"])}</div></a>'
        for (k, pos, ic), a in zip(tiles, APPS))
    return f"""<div class="forge">
<div class="halo" aria-hidden="true"></div>
<svg class="emblem" viewBox="0 0 400 400" role="img" aria-label="The Brightforge Labs logo, an anvil and a spark, linked to its apps FadeReady, SizeGuard and Nail Signature">
<defs>
<linearGradient id="fg-anvil" x1="0" y1="0" x2="0" y2="1"><stop offset="0" stop-color="#FFB03A"/><stop offset="1" stop-color="#FF4A1C"/></linearGradient>
<linearGradient id="fg-spark" x1="0" y1="0" x2="0" y2="1"><stop offset="0" stop-color="#FFF6C8"/><stop offset="1" stop-color="#FFB400"/></linearGradient>
<linearGradient id="fg-line" x1="0" y1="0" x2="1" y2="0"><stop offset="0" stop-color="#ff8a3d" stop-opacity=".9"/><stop offset="1" stop-color="#b794ff" stop-opacity=".35"/></linearGradient>
<radialGradient id="fg-heat" cx=".5" cy=".5" r=".5"><stop offset="0" stop-color="#ff7a1a" stop-opacity=".75"/><stop offset="1" stop-color="#ff7a1a" stop-opacity="0"/></radialGradient>
</defs>
<g class="ring"><circle cx="200" cy="200" r="168" fill="none" stroke="rgba(255,255,255,.14)" stroke-dasharray="2 9"/></g>
<circle cx="200" cy="200" r="118" fill="none" stroke="rgba(255,170,80,.18)"/>
<g class="links" fill="none" stroke="url(#fg-line)" stroke-width="2" stroke-dasharray="5 9" stroke-linecap="round">
<path d="M115 118 L74 78"/><path d="M318 198 L342 196"/><path d="M126 292 L92 334"/><path d="M285 118 L326 78"/>
</g>
<circle class="heat" cx="200" cy="{o + 38 * m:.0f}" r="96" fill="url(#fg-heat)"/>
<g transform="translate({o:.1f} {o:.1f}) scale({m})">
<path fill="url(#fg-anvil)" d="M8 36.5h43c0 3.2-2.6 5.5-6 5.5h-6l2 6h5.5v4h-29v-4H23l2-6h-5C14.5 42 10.5 40 8 36.5z"/>
<circle class="flash" cx="32" cy="36" r="10" fill="none" stroke="#FFD27A" stroke-width=".8"/>
<path class="star" fill="url(#fg-spark)" d="M32 8.5q1.9 10.4 11.5 12.5Q33.9 23.1 32 33.5 30.1 23.1 20.5 21 30.1 18.9 32 8.5z"/>
<circle class="tw" cx="46" cy="11.5" r="2" fill="#FFD24A"/>
<circle class="tw t2" cx="18.5" cy="12.5" r="1.4" fill="#FFD24A"/>
<circle class="tw t3" cx="48.5" cy="28" r="1.2" fill="#FF9A1F"/>
</g>
</svg>
<span class="emitter" aria-hidden="true"></span>
{cards}
</div>"""


def phone():
    av = lambda t, c: f'<span class="av" style="background:{c}">{t}</span>'
    fr = f"""<div class="scr">
<div class="scr-head">{app_logo("fr", 28, "dot")}<div>FadeReady<small>Live line · Main St. Barbers</small></div></div>
<div class="scr-card"><h4>Now in the chair</h4><div class="row">{av("MJ","#3a1fa6")}<div class="grow"><b>Marcus J.</b><br><small>Skin fade · with Tony</small></div><span class="tag-now">Now</span></div></div>
<div class="scr-card"><h4>Up next · 3 waiting</h4>
<div class="row pulse">{av("DL","#e8590c")}<div class="grow"><b>Devin L.</b><br><small>Cut and beard · 8 min</small></div></div>
<div class="row">{av("AR","#0f766e")}<div class="grow"><b>Andre R.</b><br><small>Kids cut · 20 min</small></div></div>
<div class="row">{av("CS","#9d174d")}<div class="grow"><b>Chris S.</b><br><small>Lineup · 31 min</small></div></div></div>
<div class="scr-card"><div class="kv"><span>Today's sales</span><b class="pos">$1,284</b></div><div class="kv"><span>Cuts done</span><b>27</b></div></div>
</div>"""
    tr = f"""<div class="scr">
<div class="scr-head">{app_logo("tr", 28, "dot")}<div>SizeGuard<small>Stop size calculator</small></div></div>
<div class="mkts"><span class="on">Futures</span><span>Forex</span><span>Stocks</span><span>Crypto</span></div>
<div class="scr-card"><h4>Position size</h4><div class="big">3 contracts</div><div class="kv"><span>Risk</span><b>$300 (1%)</b></div><div class="kv"><span>Stop</span><b>20 ticks</b></div><div class="bar"><i></i></div></div>
<div class="scr-card"><h4>Prop firm tracker</h4><div class="kv"><span>Evaluations and resets</span><b class="neg">−$612</b></div><div class="kv"><span>Payouts</span><b class="pos">+$2,450</b></div><div class="kv"><span>Net</span><b class="pos">+$1,838</b></div></div>
<div class="scr-card"><h4>Daily journal</h4><small>Stuck to my plan. Calm, patient, no revenge trades.</small></div>
</div>"""
    sl = f"""<div class="scr">
<div class="scr-head">{app_logo("sl", 28, "dot")}<div>Nail Signature<small>Today · Polished Nail Studio</small></div></div>
<div class="scr-card"><h4>Today's bookings</h4>
<div class="slot"><time>10:00</time>{av("KM","#9d174d")}<div class="grow"><b>Kayla M.</b><br><small>Gel manicure</small></div></div>
<div class="slot pulse"><time>10:45</time>{av("SR","#e8590c")}<div class="grow"><b>Sofia R.</b><br><small>Acrylic full set</small></div></div>
<div class="slot"><time>12:00</time>{av("JT","#3a1fa6")}<div class="grow"><b>Jade T.</b><br><small>Pedicure</small></div></div></div>
<div class="scr-card"><div class="kv"><span>Walk-ins waiting</span><b>2</b></div><div class="kv"><span>Today's sales</span><b class="pos">$860</b></div></div>
</div>"""
    lt = f"""<div class="scr">
<div class="scr-head">{app_logo("lt", 28, "dot")}<div>LaneTally<small>Dispatch board · This week</small></div></div>
<div class="scr-card"><h4>Loads on the road · 3</h4>
<div class="row pulse">{av("RG","#e8590c")}<div class="grow"><b>Dallas, TX → Atlanta, GA</b><br><small>Ray G. · In transit · ETA 4:30 PM</small></div></div>
<div class="row">{av("ML","#0f766e")}<div class="grow"><b>Memphis, TN → Chicago, IL</b><br><small>Mike L. · Picked up</small></div></div>
<div class="row">{av("JP","#3a1fa6")}<div class="grow"><b>Ocala, FL → Charlotte, NC</b><br><small>Jose P. · Delivered</small></div></div></div>
<div class="scr-card"><div class="kv"><span>Gross this week</span><b class="pos">$18,450</b></div><div class="kv"><span>Cost per mile</span><b>$1.62</b></div><div class="kv"><span>Invoices due</span><b>5</b></div></div>
</div>"""
    return f"""<div class="stage" role="img" aria-label="Example screens from FadeReady, SizeGuard, Nail Signature and LaneTally">
<div class="phone" aria-hidden="true"><div class="screen">{fr}{tr}{sl}{lt}</div></div>
</div>"""


def cta_band():
    return """<section style="padding-top:0">
<div class="wrap">
<div class="band">
<div><h2>Let's talk.</h2><p>Questions, partnerships or press? Send us a note. A real person reads every message.</p></div>
<div class="btns"><a class="btn btn-primary" href="/contact">Contact us</a><a class="btn btn-line" href="/about">About the company</a></div>
</div>
</div>
</section>"""


def home():
    faq_html = "".join(
        f"<details{' open' if n == 0 else ''}><summary>{q}</summary><p>{a.replace(EMAIL, email_link())}</p></details>"
        for n, (q, a) in enumerate(FAQ))
    faq_ld = {"@type": "FAQPage", "@id": f"{SITE}/#faq",
              "mainEntity": [{"@type": "Question", "name": q,
                              "acceptedAnswer": {"@type": "Answer", "text": a}} for q, a in FAQ]}
    body = f"""<section class="hero hero-live">
<canvas class="embers" aria-hidden="true"></canvas>
<div class="wrap">
<div>
<p class="eyebrow"><i></i>Brightforge Labs LLC · Florida, USA</p>
<h1>Brightforge Labs<span class="sub">Apps for <span class="rot" aria-hidden="true"><span data-w="barbershops."></span><span data-w="traders."></span><span data-w="nail salons."></span><span data-w="trucking."></span></span><span class="sr">barbershops, traders, nail salons and trucking.</span></span></h1>
<p class="lead">We are the software company behind <b>FadeReady</b>, <b>LaneTally</b>, <b>SizeGuard</b> and <b>Nail Signature</b>. We build simple, fast and beautiful apps that help people run their work.</p>
<div class="btns"><a class="btn btn-primary" href="#apps">See our apps</a><a class="btn btn-line" href="/about">About the company</a></div>
<ul class="facts"><li><b>2026</b>Founded</li><li><b>Florida, USA</b>Headquarters</li><li><b>4 apps</b>Coming soon</li></ul>
</div>
{forge()}
</div>
</section>

<section class="alt" id="company">
<div class="wrap split">
<div>
<span class="kicker">Who we are</span>
<h2>What is Brightforge Labs?</h2>
<p class="intro">Brightforge Labs LLC is a software company in Florida, USA. It is the parent company that owns and builds our apps, so every app gets the same care, the same security and the same team behind it.</p>
</div>
{org_chart()}
</div>
</section>

<section id="apps">
<div class="wrap">
<div class="split apps-head">
<div>
<span class="kicker">Our apps</span>
<h2>Apps made by Brightforge Labs</h2>
<p class="intro">Each app does one job well for one kind of work. They all share the same promise: simple, fast, beautiful and secure.</p>
</div>
{phone()}
</div>
{app_cards()}
</div>
</section>

<section class="alt" id="values">
<div class="wrap">
<span class="kicker">Our promise</span>
<h2>Every app we make is</h2>
{value_list()}
</div>
</section>

<section id="faq">
<div class="narrow">
<span class="kicker">Quick answers</span>
<h2>Questions people ask</h2>
<div class="faq">{faq_html}</div>
</div>
</section>
{cta_band()}"""
    return page("", "Brightforge Labs: FadeReady, LaneTally, SizeGuard & Nail Signature apps",
                DESCRIPTION, body, extra_ld=[FADEREADY, faq_ld], script='<script src="/site.js" defer></script>\n')


def about():
    rows = [("Legal name", "Brightforge Labs LLC"), ("Company type", "Florida limited liability company"),
            ("Founded", "2026"), ("Founder", "Idael Fonseca Hidalgo"),
            ("What we do", "Apps for small businesses and independent pros"),
            ("Our apps", '<a href="https://fadeready.com/">FadeReady</a> (barbershops), <a href="https://lanetally.com/">LaneTally</a> (trucking), <a href="https://sizeguard.com/">SizeGuard</a> (traders) and <a href="https://nailsignature.com/">Nail Signature</a> (nail salons)'),
            ("Ownership", "All our apps and websites, including FadeReady and fadeready.com, are owned by Brightforge Labs LLC"),
            ("Location", "Florida, USA"), ("Email", email_link())]
    table = "".join(f"<tr><th scope=row>{k}</th><td>{v}</td></tr>" for k, v in rows)
    body = page_hero("About us", 'Where bright ideas are <span class="accent">forged into real products.</span>',
                     "Brightforge Labs is the parent company that owns and builds our apps. We are small, focused and in it for the long run.") + f"""
<section>
<div class="narrow prose">
<span class="kicker">Our story</span>
<h2 style="margin-top:0">Why we started</h2>
<p>People who run their own work are busy. Barbers, nail techs, shop owners and traders have no time to fight their tools. But the apps they use are often slow, confusing or ugly.</p>
<p>We thought they deserved better. So in 2026, Idael Fonseca Hidalgo started <strong>Brightforge Labs LLC</strong>, a software company in Florida, USA.</p>
<p>Our first app is <a href="https://fadeready.com/">FadeReady</a>, for barbershops. Like all our apps, FadeReady is owned and run by Brightforge Labs LLC. Next come <a href="https://nailsignature.com/">Nail Signature</a>, which brings everything FadeReady does to nail salons, <a href="https://lanetally.com/">LaneTally</a>, truck dispatch and trucking accounting software, and <a href="https://sizeguard.com/">SizeGuard</a>, a trading toolkit for traders.</p>
<h2>What our name means</h2>
<p>A forge is a hot fire where metal is shaped into strong tools. <strong>Brightforge</strong> is a place where bright ideas are shaped into real products. <strong>Labs</strong> means we never stop testing and improving.</p>
</div>
</section>

<section class="alt">
<div class="wrap">
<span class="kicker">Our values</span>
<h2>Four promises in every app</h2>
<p class="intro">Every app we make has to keep these four promises before it ships.</p>
{value_list()}
</div>
</section>

<section>
<div class="narrow prose">
<span class="kicker">Company facts</span>
<h2 style="margin-top:0">Brightforge Labs at a glance</h2>
<table class="facts-table">{table}</table>
</div>
</section>
{cta_band()}"""
    return page("about", "About Brightforge Labs: our story, values and company facts",
                "Brightforge Labs LLC is a Florida software company founded in 2026 by Idael Fonseca Hidalgo. "
                "It owns and builds simple, fast, beautiful and secure apps, like FadeReady.",
                body, current="About", page_type="AboutPage")


def contact():
    body = page_hero("Contact", 'Talk to <span class="accent">Brightforge Labs.</span>',
                     "Questions, partnerships, press or business matters? Send us an email. A real person reads every message.") + f"""
<section>
<div class="narrow prose">
<h2 style="margin-top:0">Email us</h2>
<p>{email_link("mail", ICONS["mail"] + EMAIL)}</p>
<p>We usually reply within one or two business days.</p>
<h2>Where we are</h2>
<p>Brightforge Labs LLC is based in Florida, USA. We work online, so we can help you from anywhere.</p>
<h2>Need help with an app?</h2>
<p>Go to our <a href="/support">Support page</a> for each app's help email, privacy and terms links, and how to delete your account. You can also email us and we will point you to the right place.</p>
</div>
</section>"""
    return page("contact", "Contact Brightforge Labs",
                f"Contact Brightforge Labs LLC by email at {EMAIL}. We are a software company based in Florida, USA.",
                body, current="Contact", page_type="ContactPage")


def legal(slug, title, h1, description, sections):
    body = page_hero("Legal", h1, f"Last updated: {UPDATED_TEXT}") + f"""
<section>
<div class="narrow prose">
{sections}
</div>
</section>"""
    return page(slug, title, description, body)


def privacy():
    return legal("privacy", "Privacy Policy | Brightforge Labs", "Privacy Policy",
                 "How Brightforge Labs LLC collects, uses and protects information on this website and in our apps, in plain language.",
                 f"""<p>This policy explains, in plain words, what information <strong>Brightforge Labs LLC</strong> ("Brightforge Labs", "we", "us") collects, why, and what choices you have. It covers this website (brightforgelabs.app) and all the apps and websites we own, including FadeReady (fadeready.com). Some apps, like FadeReady, may also have their own privacy policy. If they do, that policy explains the details for that app.</p>

<h2>The short version</h2>
<ul>
<li>We collect only what we need to run our website and apps.</li>
<li>We never sell your personal information.</li>
<li>This website has no ads, no tracking cookies and no analytics trackers.</li>
<li>You can ask us to see or delete your information at any time.</li>
</ul>

<h2>What we collect</h2>
<h3>On this website</h3>
<p>This website does not ask you to sign up and does not use tracking cookies. Our hosting provider, Cloudflare, may record basic technical data, such as your IP address, browser type and the pages you visit. This helps keep the site safe and working. If you email us, we receive your email address and whatever you write.</p>
<h3>In our apps</h3>
<p>When you use one of our apps, we may collect:</p>
<ul>
<li><strong>Account details</strong>, such as your name, email address and phone number.</li>
<li><strong>Business details</strong> you enter, such as appointments, services, prices and records.</li>
<li><strong>Payment details</strong>, which are handled by trusted payment companies (like Apple, Google or Stripe). We do not store full card numbers.</li>
<li><strong>Device and usage details</strong>, such as app version, crash reports and how features are used, so we can fix problems.</li>
<li><strong>Location</strong>, only if a feature needs it and you allow it.</li>
</ul>

<h2>How we use it</h2>
<ul>
<li>To run our apps and give you the features you ask for.</li>
<li>To keep accounts safe and stop fraud or misuse.</li>
<li>To answer your questions and send important messages about your account.</li>
<li>To fix bugs and make our apps better.</li>
<li>To follow the law.</li>
</ul>

<h2>Who we share it with</h2>
<p>We do <strong>not</strong> sell or rent your personal information. We share it only:</p>
<ul>
<li>With service providers who help us run our apps (like hosting, email and payment companies). They may use it only to help us.</li>
<li>With the business you choose to book with, when you use an app to book or join a line.</li>
<li>When the law requires it, or to protect people's safety.</li>
<li>If our company is sold or merged, in which case this policy still protects your information.</li>
</ul>

<h2>How we protect it</h2>
<p>We use strong security, such as encryption (HTTPS) and limited access, to protect your information. No system is perfect, but we work hard to keep your data safe.</p>

<h2>How long we keep it</h2>
<p>We keep information only as long as we need it for the reasons above, or as long as the law requires. When you delete your account, we delete or anonymize your personal information within a reasonable time.</p>

<h2>Your choices and rights</h2>
<p>You can ask us to see, fix, download or delete your personal information. You can also ask us to stop sending you marketing emails. Depending on where you live (for example, California or the European Union), you may have extra rights. To use any of these rights, email {email_link()}. We will not treat you differently for asking.</p>

<h2>Children</h2>
<p>Our website and apps are not made for children under 13, and we do not knowingly collect their information. If you think a child has given us information, please contact us and we will delete it.</p>

<h2>Changes to this policy</h2>
<p>We may update this policy. When we do, we will change the date at the top. If a change is big, we will let you know in the app or by email.</p>

<h2>Contact us</h2>
<p>Brightforge Labs LLC, Florida, USA. Email: {email_link()}</p>""")


def terms():
    return legal("terms", "Terms of Use | Brightforge Labs", "Terms of Use",
                 "The plain-language terms for using the Brightforge Labs LLC website and apps.",
                 f"""<p>These terms are the rules for using the websites and apps owned by <strong>Brightforge Labs LLC</strong> ("Brightforge Labs", "we", "us"), including FadeReady (fadeready.com). By using them, you agree to these terms. Some apps may have extra terms. If they do, those terms apply too.</p>

<h2>1. Using our website and apps</h2>
<p>You may use our website and apps for lawful purposes. Please do not:</p>
<ul>
<li>Break the law or hurt other people.</li>
<li>Try to hack, overload or break our systems.</li>
<li>Copy, resell or reverse-engineer our apps without permission.</li>
<li>Upload anything harmful, false or that you do not have the right to share.</li>
</ul>

<h2>2. Your account</h2>
<p>If an app asks you to make an account, please give true information and keep your password safe. You are responsible for what happens in your account. Tell us right away if you think someone else is using it.</p>

<h2>3. Payments and subscriptions</h2>
<p>Some apps or features may cost money. Prices are shown before you pay. If you buy through the Apple App Store or Google Play, their payment and refund rules also apply. Subscriptions renew until you cancel them, and you can cancel any time in your account or store settings.</p>

<h2>4. Your content</h2>
<p>You own the information you put into our apps. You give us permission to store and use it only to run the app for you. We protect it as described in our <a href="/privacy">Privacy Policy</a>.</p>

<h2>5. Our content</h2>
<p>Our apps, website, logos and names (like Brightforge Labs and FadeReady) belong to Brightforge Labs LLC and its companies. Please do not use them without our permission.</p>

<h2>6. Trading tools are not financial advice</h2>
<p>Our trading apps help you calculate, plan and keep records. They do not tell you what to buy or sell, and they are not financial, investment or tax advice. Trading is risky and you can lose money. You are responsible for your own trades.</p>

<h2>7. Other websites and services</h2>
<p>Our website and apps may link to other services (like payment companies or app stores). We do not control them and are not responsible for them.</p>

<h2>8. No guarantees</h2>
<p>We work hard to keep our apps running well, but we provide them "as is". We cannot promise they will always be perfect, error-free or available.</p>

<h2>9. Limits on our responsibility</h2>
<p>To the fullest extent the law allows, Brightforge Labs LLC is not responsible for indirect or surprise losses, such as lost profits or lost data, from using our website or apps. If we are responsible for something, the most we will owe is the amount you paid us in the 12 months before the problem.</p>

<h2>10. Ending use</h2>
<p>You can stop using our apps any time. We may pause or close an account that breaks these terms or puts others at risk.</p>

<h2>11. Florida law</h2>
<p>These terms follow the laws of the State of Florida, USA. Any dispute will be handled in the courts of Florida, unless the law says otherwise.</p>

<h2>12. Changes</h2>
<p>We may update these terms. When we do, we will change the date at the top. If you keep using our website or apps after a change, you accept the new terms.</p>

<h2>13. Contact us</h2>
<p>Questions about these terms? Email {email_link()}.</p>""")


APP_DETAILS = {
    "fr": {
        "title": "FadeReady: the barbershop app for booking, the live line and bookkeeping",
        "description": ("FadeReady is the barbershop app by Brightforge Labs. Clients book or join the live line "
                        "from their phone, barbers see who is next, and owners keep the books and track licenses."),
        "h1": 'FadeReady, the app that <span class="accent">runs the barbershop day.</span>',
        "lead": "Booking, the live line, barber and client apps, bookkeeping and license reminders, all in one app. Coming soon, and the waiting list is open at <a href=\"https://fadeready.com/\">fadeready.com</a>.",
        "who": "FadeReady is for barbershop owners, barbers and their clients. It works for a one-chair shop and for a busy shop with a full team.",
        "sections": [
            ("Online booking", "Clients pick a barber, a service and a time from their phone, any time of day. The shop gets fewer calls and fewer no-shows."),
            ("A live line for walk-ins", "Walk-in clients join the line from their phone and see their place in real time, so they can wait anywhere instead of in the shop."),
            ("A barber app and a client app", "Barbers see who is next, their day and their earnings. Clients see their bookings, their place in line and their favorite barbers."),
            ("Bookkeeping and barber pay", "Owners see sales, expenses and what each barber earned, without a separate spreadsheet."),
            ("License renewal reminders", "FadeReady reminds the shop before barber and shop licenses expire, so nobody gets caught out."),
        ],
        "faq": [
            ("What is FadeReady?", "FadeReady is an app for barbershops. It handles online booking, a live line for walk-ins, a barber app, a client app, bookkeeping and license renewal reminders."),
            ("Who makes FadeReady?", "FadeReady is made, owned and run by Brightforge Labs LLC, a software company in Florida, USA."),
            ("When will FadeReady be available?", "FadeReady is coming soon. Join the waiting list at fadeready.com to get early access and the founding deal."),
        ],
        "cta": ("Visit fadeready.com", "https://fadeready.com/"),
        "category": "BusinessApplication",
    },
    "tr": {
        "title": "SizeGuard: stop size calculator, trading journal and prop firm tracker",
        "description": ("SizeGuard by Brightforge Labs (coming soon) is a trading toolkit with a stop size calculator for futures, forex, "
                        "stocks and crypto, a trading journal, a daily journal and a prop firm tracker for fees and payouts."),
        "h1": 'SizeGuard, the trading toolkit to <span class="accent">plan, record and review.</span>',
        "lead": "A stop size calculator for four markets, a trading journal, a daily journal and a prop firm tracker, in one app. Coming soon at <a href=\"https://sizeguard.com/\">sizeguard.com</a>.",
        "who": "SizeGuard is for day traders, swing traders and prop firm traders who trade futures, forex, stocks or crypto and want to manage risk and keep honest records.",
        "sections": [
            ("Stop size calculator for 4 markets", "Enter your account size, your risk and your stop, and see the right position size for futures, forex, stocks or crypto. No mental math under pressure."),
            ("Trading journal", "Log every trade with entry, exit, size, result and notes, then review what works and what doesn't."),
            ("Daily journal", "Write down your plan, your mood and your lessons each day, so you can spot the habits behind good and bad days."),
            ("Prop firm tracker", "Track every evaluation, reset and monthly fee across prop firms in one place."),
            ("Payout tracking", "Record every payout next to what you spent, so you see what you really earn from prop firms."),
        ],
        "faq": [
            ("What is SizeGuard?", "SizeGuard is a trading toolkit app with a stop size calculator for futures, forex, stocks and crypto, a trading journal, a daily journal and a prop firm tracker for evaluations, resets, fees and payouts."),
            ("Is SizeGuard financial advice?", "No. It is a tool for planning and record-keeping. It does not tell you what to buy or sell, and trading carries risk."),
            ("When will SizeGuard be available?", "It is in development and will launch at sizeguard.com. Email hello@brightforgelabs.app to hear when it launches."),
        ],
        "cta": ("Visit sizeguard.com", "https://sizeguard.com/"),
        "category": "FinanceApplication",
    },
    "sl": {
        "title": "Nail Signature: the nail salon app for booking, the live line and bookkeeping",
        "description": ("Nail Signature by Brightforge Labs (coming soon) brings everything FadeReady does to nail salons: "
                        "online booking, a live line, nail tech and client apps, bookkeeping and license reminders."),
        "h1": 'Nail Signature, the app made <span class="accent">for nail salons.</span>',
        "lead": 'Everything FadeReady does for barbershops, made for nail salons: booking, the live line, team and client apps, bookkeeping and license reminders. Coming soon, and the waiting list is open at <a href="https://nailsignature.com/">nailsignature.com</a>.',
        "who": "Nail Signature is for nail salon owners, nail techs and their clients, from a single-desk studio to a busy salon.",
        "sections": [
            ("Online booking", "Clients choose a nail tech, a service and a time from their phone, day or night."),
            ("A live line for walk-ins", "Walk-in clients join the line from their phone and see when it is their turn."),
            ("A nail tech app and a client app", "Nail techs see their day and their earnings. Clients see their bookings and their place in line."),
            ("Bookkeeping and team pay", "Owners see sales, expenses and what each team member earned in one place."),
            ("License renewal reminders", "Get a reminder before nail tech and salon licenses expire."),
        ],
        "faq": [
            ("What is Nail Signature?", "Nail Signature is an app for nail salons that does everything FadeReady does for barbershops: online booking, a live line, nail tech and client apps, bookkeeping and license renewal reminders."),
            ("When will Nail Signature be available?", "Nail Signature is coming soon. Join the waiting list at nailsignature.com to get early access."),
            ("Who makes Nail Signature?", "Brightforge Labs LLC, the Florida software company that also makes FadeReady."),
        ],
        "cta": ("Visit nailsignature.com", "https://nailsignature.com/"),
        "category": "BusinessApplication",
    },
    "lt": {
        "title": "LaneTally: truck dispatch and trucking accounting software",
        "description": ("LaneTally by Brightforge Labs is truck dispatch and trucking accounting software for dispatchers, carriers and "
                        "owner-operators: loads, a driver app, invoices and factoring, driver pay, IFTA and the books, in English and Spanish."),
        "h1": 'LaneTally, dispatch software that <span class="accent">keeps every load on track.</span>',
        "lead": 'Loads, drivers, invoices, IFTA and the books for dispatchers, carriers and owner-operators, in English and Spanish. Early access is open at <a href="https://lanetally.com/">lanetally.com</a>.',
        "who": "LaneTally is for truck dispatchers, dispatch services, carriers and owner-operators, from one truck to a growing fleet. It works in English and Spanish.",
        "sections": [
            ("Loads and dispatch", "Book loads, assign drivers and follow every load from pickup to delivery on one board and a live fleet map."),
            ("A driver app", "Drivers see their stops, get directions, send photos of paperwork and chat with dispatch from their phone."),
            ("Invoices and factoring", "Turn delivered loads into invoices, track what brokers owe and keep factoring in one place."),
            ("Driver pay and dispatch fees", "See what each driver earned and what each carrier owes in dispatch fees, without spreadsheets."),
            ("IFTA, fuel and cost per mile", "Track fuel and miles by state for IFTA, and see your real cost per mile so you know which loads pay."),
        ],
        "faq": [
            ("What is LaneTally?", "LaneTally is dispatch and carrier software for trucking. It handles loads, a driver app, invoices and factoring, driver pay, dispatch fees, IFTA, fuel and cost per mile."),
            ("Who makes LaneTally?", "LaneTally is made, owned and run by Brightforge Labs LLC, a software company in Florida, USA."),
            ("Can I try LaneTally?", "Yes. There is a free demo at lanetally.com/demo. LaneTally is in beta, and you can join the waiting list on lanetally.com."),
        ],
        "cta": ("Visit lanetally.com", "https://lanetally.com/"),
        "category": "BusinessApplication",
    }
}


def app_page(a):
    d = APP_DETAILS[a["key"]]
    url = f"{SITE}/{a['slug']}"
    feats = "".join(f"<h3>{t}</h3><p>{x}</p>" for t, x in d["sections"])
    faq_html = "".join(f"<details><summary>{q}</summary><p>{x.replace(EMAIL, email_link())}</p></details>"
                       for q, x in d["faq"])
    label, href = d["cta"]
    status = "Live now" if a["status"] == "live" else "Coming soon"
    body = page_hero(f"{a['for']} · {status}", d["h1"], d["lead"]).replace(
        '<p class="eyebrow">', app_logo(a["key"], 72, "tile hero-logo") + '<p class="eyebrow">', 1) + f"""
<section>
<div class="narrow prose">
<span class="kicker">What it does</span>
<h2 style="margin-top:0">{a['name']} features</h2>
{feats}
<h2>Who it is for</h2>
<p>{d['who']}</p>
<h2>Who makes it</h2>
<p>{a['ref'][0].upper() + a['ref'][1:]} is made, owned and run by <a href="/about">Brightforge Labs LLC</a>, a software company in Florida, USA. Like every app we make, it is simple, fast, beautiful and secure.</p>
<p><a class="btn btn-primary" href="{href}">{label}</a></p>
</div>
</section>

<section class="alt">
<div class="narrow">
<span class="kicker">Quick answers</span>
<h2>{a['name']} questions</h2>
<div class="faq">{faq_html}</div>
</div>
</section>
{cta_band()}"""
    app_ld = {"@type": "SoftwareApplication", "@id": f"{url}#app", "name": a["name"],
              "url": a["href"] if a["href"].startswith("http") else url,
              "applicationCategory": d["category"], "operatingSystem": "iOS, Android, Web",
              "image": f"{SITE}/apps/{a['key']}-256.webp",
              "description": d["description"], "featureList": [t for t, _ in d["sections"]],
              "author": {"@id": f"{SITE}/#organization"}, "publisher": {"@id": f"{SITE}/#organization"}}
    if a["status"] != "live":
        app_ld["releaseNotes"] = "In development, coming soon."
    faq_ld = {"@type": "FAQPage", "@id": f"{url}#faq",
              "mainEntity": [{"@type": "Question", "name": q,
                              "acceptedAnswer": {"@type": "Answer", "text": x}} for q, x in d["faq"]]}
    crumbs = {"@type": "BreadcrumbList", "@id": f"{url}#breadcrumb", "itemListElement": [
        {"@type": "ListItem", "position": 1, "name": "Home", "item": f"{SITE}/"},
        {"@type": "ListItem", "position": 2, "name": a["name"], "item": url}]}
    return page(a["slug"], d["title"], d["description"], body, current="Apps",
                extra_ld=[app_ld, faq_ld, crumbs])


def support():
    def a(href, text=None):
        return f'<a href="{href}">{text or href}</a>'

    cards = [
        {"slug": "fadeready", "key": "fr", "name": "FadeReady", "for": "For barbershops",
         "contact": f'Email: {email_link()}<br>Support page: {a("https://fadeready.com/support/")}',
         "legal": f'{a("https://fadeready.com/privacy/", "Privacy Policy")} · {a("https://fadeready.com/terms/", "Terms of Use")}',
         "delete": ["In the app, go to <strong>Me</strong> (shop owners: <strong>Settings</strong>), then tap <strong>Delete my account</strong>.",
                    f'Or open {a("https://fadeready.com/delete-account")}.',
                    f'Or email {email_link()} from the email on your account and ask us to delete it.']},
        {"slug": "lanetally", "key": "lt", "name": "LaneTally", "for": "For trucking",
         "contact": f'Email: {email_link(addr="support@lanetally.com")}<br>We look at every message within 24 hours.',
         "legal": f'{a("https://lanetally.com/privacy/", "Privacy Policy")} · {a("https://lanetally.com/terms/", "Terms of Use")}',
         "delete": [f'Write to {email_link(addr="support@lanetally.com")} from the email on your account. Ask us to close the account and delete your company\'s data. We delete it and tell you when it is done.',
                    f'To leave the waiting list, email {email_link(addr="support@lanetally.com")} from the same email you signed up with.']},
        {"slug": "nail-signature", "key": "sl", "name": "Nail Signature", "for": "For nail salons",
         "contact": f'Email: {email_link(addr="hello@nailsignature.com")}',
         "legal": a("https://nailsignature.com/privacy/", "Privacy Policy"),
         "delete": ["In the app, go to <strong>Me</strong> (salon owners: <strong>Salon settings</strong>), then <strong>Account</strong>, then tap <strong>Delete my account</strong>.",
                    f'Or open {a("https://nailsignature.com/delete-your-account/")}.',
                    f'Or email {email_link(addr="hello@nailsignature.com")} from the email or phone number on your account. We finish within 30 days.']},
    ]
    out = []
    for c in cards:
        steps = "".join(f"<li>{x}</li>" for x in c["delete"])
        out.append(f"""<article class="app" id="{c['slug']}">
<div class="app-top">{app_logo(c['key'])}<div><h3>{c['name']}</h3><span class="for">{c['for']}</span></div></div>
<h4>Contact</h4>
<p>{c['contact']}</p>
<h4>Privacy and terms</h4>
<p>{c['legal']}</p>
<h4>Delete your account</h4>
<ul class="steps">{steps}</ul>
</article>""")
    body = page_hero("Support", 'Help and <span class="accent">account deletion.</span>',
                     "Brightforge Labs LLC makes FadeReady, LaneTally and Nail Signature. Find help for each app here, and how to delete your account.") + f"""
<section>
<div class="wrap">
<span class="kicker">Our apps</span>
<h2>Support for each app</h2>
<p class="intro">Pick your app below. Each one has its own help email, its own privacy page, and its own steps to delete your account.</p>
<div class="apps">{"".join(out)}</div>
</div>
</section>

<section class="alt">
<div class="narrow prose">
<span class="kicker">Writing to us</span>
<h2 style="margin-top:0">What to include when you write</h2>
<p>Tell us the <strong>app name</strong>, the <strong>email you sign in with</strong>, and <strong>what happened</strong>. That helps us fix it faster.</p>
<p>We answer in English or Spanish.</p>
<p>Questions about SizeGuard? Email {email_link()}.</p>
<h2>Brightforge Labs LLC</h2>
<p>2287 S Haverhill Road<br>West Palm Beach, FL 33415<br>{email_link()}</p>
</div>
</section>"""
    crumbs = {"@type": "BreadcrumbList", "@id": f"{SITE}/support#breadcrumb", "itemListElement": [
        {"@type": "ListItem", "position": 1, "name": "Home", "item": f"{SITE}/"},
        {"@type": "ListItem", "position": 2, "name": "Support", "item": f"{SITE}/support"}]}
    return page("support", "Support and account deletion | Brightforge Labs",
                "Help for FadeReady, LaneTally and Nail Signature: support emails, privacy and terms links, "
                "and how to delete your account. Made by Brightforge Labs LLC.",
                body, page_type="ContactPage", extra_ld=[crumbs])


def not_found():
    body = page_hero("Error 404", 'This page is <span class="accent">not here.</span>',
                     "The page you want may have moved. Let's get you back home.") + """
<section><div class="narrow"><p><a class="btn btn-primary" href="/">Go to the home page</a></p></div></section>"""
    html = page("404", "Page not found | Brightforge Labs", "This page could not be found.", body)
    return html.replace('<link rel="canonical" href="https://brightforgelabs.app/404">',
                        '<meta name="robots" content="noindex">')


def tidy(html):
    return re.sub(r"\n\s*\n", "\n", html)


def main():
    pages = {"index.html": home(), "about.html": about(), "contact.html": contact(), "support.html": support(),
             "privacy.html": privacy(), "terms.html": terms(), "404.html": not_found(),
             **{f"{a['slug']}.html": app_page(a) for a in APPS}}
    for name, html in pages.items():
        (OUT / name).write_text(tidy(html))
    urls = ["", *[a["slug"] for a in APPS], "about", "contact", "support", "privacy", "terms"]
    prio = {"": "1.0", "fadeready": "0.9", "sizeguard": "0.8", "nail-signature": "0.8", "lanetally": "0.9",
            "about": "0.8", "contact": "0.7", "support": "0.7"}
    sitemap = ['<?xml version="1.0" encoding="UTF-8"?>',
               '<urlset xmlns="http://www.sitemaps.org/schemas/sitemap/0.9">']
    for u in urls:
        sitemap.append(f"<url><loc>{SITE}/{u}</loc><lastmod>{UPDATED}</lastmod>"
                       f"<priority>{prio.get(u, '0.3')}</priority></url>")
    sitemap.append("</urlset>")
    (OUT / "sitemap.xml").write_text("\n".join(sitemap) + "\n")
    print("Built", ", ".join(pages), "and sitemap.xml on", date.today())


if __name__ == "__main__":
    main()
