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
UPDATED = "2026-10-25"
UPDATED_TEXT = "October 25, 2026"
DESCRIPTION = ("Brightforge Labs LLC is a software company in Florida, USA. "
               "We build simple, fast, beautiful apps for small businesses and independent pros, "
               "like FadeReady for barbershops and a trading toolkit for traders.")


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
                     "email": EMAIL, "availableLanguage": ["English"]},
    "knowsAbout": ["Mobile apps", "Software for small businesses",
                   "Barbershop booking software", "Salon software",
                   "Trading tools", "Position size and stop size calculators", "Trading journals",
                   "Prop firm expense and payout tracking"],
    "subOrganization": {"@type": "Organization", "@id": "https://fadeready.com/#organization",
                        "name": "FadeReady", "legalName": "FadeReady LLC",
                        "url": "https://fadeready.com/"},
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

FAQ = [
    ("What is Brightforge Labs?",
     "Brightforge Labs LLC is a software company in Florida, USA. We build simple, fast, "
     "beautiful apps for small businesses and independent pros, like barbers, salon owners and traders. "
     "Brightforge Labs is the parent company of FadeReady."),
    ("Who makes FadeReady?",
     "FadeReady is made by Brightforge Labs. FadeReady is an app for barbershops. It handles "
     "booking, the live line, barber and client apps, bookkeeping, and license renewals. "
     "FadeReady LLC is owned by Brightforge Labs LLC."),
    ("What apps does Brightforge Labs make?",
     "Our first app is FadeReady, for barbershops. Next is a trading toolkit for traders: a stop size "
     "calculator for futures, forex, stocks and crypto, a trading journal, a daily journal, and a "
     "prop firm tracker for evaluations, resets, fees and payouts. An app for nail salons is also on the way."),
    ("Who started Brightforge Labs?",
     "Brightforge Labs was started in 2026 by Idael Fonseca Hidalgo."),
    ("How do I contact Brightforge Labs?",
     f"Email us at {EMAIL}. We read every message."),
]

NAV = [("/about", "About"), ("/#apps", "Apps"), ("/contact", "Contact")]


def email_link(cls="", inner=None):
    inner = inner or EMAIL
    c = f' class="{cls}"' if cls else ""
    # email_off keeps Cloudflare from rewriting the address with an extra script.
    return f'<!--email_off--><a{c} href="mailto:{EMAIL}">{inner}</a><!--/email_off-->'


def page(slug, title, description, body, current=None, extra_ld=(), page_type="WebPage", hero=False):
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
        for href, label in NAV)
    return f"""<!doctype html>
<html lang="en">
<head>
<meta charset="utf-8">
<meta name="viewport" content="width=device-width,initial-scale=1">
<title>{title}</title>
<meta name="description" content="{description}">
<link rel="canonical" href="{url}">
<meta name="theme-color" content="#120a33">
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
<meta property="og:image:alt" content="Brightforge Labs: bright ideas, forged into real apps.">
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
<p style="margin:0">© 2026 Brightforge Labs LLC · Florida, USA</p>
<nav aria-label="Footer">
<a href="/about">About</a>
<a href="/contact">Contact</a>
<a href="/privacy">Privacy</a>
<a href="/terms">Terms</a>
</nav>
</div>
</footer>
</body>
</html>
"""


SPARKS = '<div class="sparks" aria-hidden="true">' + "<i></i>" * 7 + "</div>"


def page_hero(kicker, h1, lead):
    return f"""<section class="hero page-hero">
{SPARKS}
<div class="wrap">
<p class="eyebrow"><i></i>{kicker}</p>
<h1>{h1}</h1>
<p class="lead">{lead}</p>
</div>
</section>"""


def value_cards():
    items = [
        ("simple", "c1", "Simple", "Anyone can use our apps. No training. No manual. Just tap and go."),
        ("fast", "c2", "Fast", "Our apps open fast and feel instant, even on a slow phone signal."),
        ("beautiful", "c3", "Beautiful", "Clean, bright screens that are a joy to look at every day."),
        ("secure", "c4", "Secure", "We protect your data like it is our own. We never sell it."),
    ]
    return "".join(
        f'<div class="card"><div class="ico {c}">{ICONS[i]}</div><h3>{t}</h3><p>{d}</p></div>'
        for i, c, t, d in items)


def home():
    faq_html = "".join(
        f"<details{' open' if n == 0 else ''}><summary>{q}</summary><p>{a.replace(EMAIL, email_link())}</p></details>"
        for n, (q, a) in enumerate(FAQ))
    faq_ld = {"@type": "FAQPage", "@id": f"{SITE}/#faq",
              "mainEntity": [{"@type": "Question", "name": q,
                              "acceptedAnswer": {"@type": "Answer", "text": a}} for q, a in FAQ]}
    body = f"""<section class="hero">
{SPARKS}
{mark("hero", "hero-mark")}
<div class="wrap">
<p class="eyebrow"><i></i>Software company · Florida, USA</p>
<h1>Brightforge Labs. <span class="grad">Bright ideas, forged into real apps.</span></h1>
<p class="lead">We build simple, fast, beautiful apps that help people run their work, from the barbershop to the trading desk.</p>
<div class="btns"><a class="btn btn-hot" href="#apps">See our apps</a><a class="btn btn-ghost" href="/contact">Say hello</a></div>
</div>
</section>

<section id="what">
<div class="wrap">
<span class="kicker">What we do</span>
<h2>What is Brightforge Labs?</h2>
<p class="intro">Brightforge Labs LLC is a software company in Florida, USA. We make apps for small businesses and independent pros, like barbers, salon owners and traders. Our apps are easy for anyone to use. They are fast, they look great, and they keep your data safe.</p>
<div class="grid grid-4">{value_cards()}</div>
</div>
</section>

<section id="apps" class="alt">
<div class="wrap">
<span class="kicker">Our apps</span>
<h2>Apps made by Brightforge Labs</h2>
<p class="intro">Each app solves real problems for one kind of work. FadeReady is our first, and more are in the forge.</p>
<div class="grid">
<article class="card app featured">
<div class="app-top"><div class="app-logo app-fr">{ICONS["scissors"]}</div><div><h3>FadeReady</h3><span class="tag">Our first app · For barbershops</span></div></div>
<div class="app-body">
<p>FadeReady helps barbershops run the whole day from one app. Clients book a cut or join the line from their phone. Barbers see who is next. Owners keep the books and never miss a license renewal.</p>
<ul class="chips"><li>Booking</li><li>Live line</li><li>Barber app</li><li>Client app</li><li>Bookkeeping</li><li>License renewals</li></ul>
<a class="more" href="https://fadeready.com/">Visit fadeready.com <span aria-hidden="true">→</span></a>
</div>
</article>
<article class="card app">
<div class="app-top"><div class="app-logo app-tr">{ICONS["chart"]}</div><div><h3>Trading toolkit</h3><span class="tag">Coming soon · For traders</span></div></div>
<div class="app-body">
<p>A toolkit for traders. The calculator shows the right stop size for every trade. A trading journal and a daily journal keep track of your trades and how you feel. Prop firm traders can track what they pay for evaluations, resets and monthly fees, and every payout they get back.</p>
<ul class="chips"><li>Stop size calculator</li><li>Futures</li><li>Forex</li><li>Stocks</li><li>Crypto</li><li>Trading journal</li><li>Daily journal</li><li>Prop firm tracker</li></ul>
<a class="more" href="/contact">Get news when it launches <span aria-hidden="true">→</span></a>
</div>
</article>
<article class="card app">
<div class="app-top"><div class="app-logo app-sl">{ICONS["sparkle"]}</div><div><h3>Salon app</h3><span class="tag">Coming soon · For nail salons</span></div></div>
<div class="app-body">
<p>An app for nail salons, made with the same care as FadeReady. Easy booking for clients and a calm, simple day for the team.</p>
<ul class="chips"><li>Booking</li><li>Client app</li><li>Team app</li></ul>
<a class="more" href="/contact">Get news when it launches <span aria-hidden="true">→</span></a>
</div>
</article>
</div>
<p class="apps-more">And more apps on the way. Each one simple, fast, beautiful and secure.</p>
</div>
</section>

<section id="faq">
<div class="narrow">
<span class="kicker">Quick answers</span>
<h2>Questions people ask</h2>
<div class="faq">{faq_html}</div>
</div>
</section>

<section style="padding-top:0">
<div class="wrap">
<div class="cta">
<h2>Have an idea or a question?</h2>
<p>We would love to hear from you. Send us a note and a real person will write back.</p>
<div class="btns"><a class="btn btn-hot" href="/contact">Contact us</a></div>
</div>
</div>
</section>"""
    return page("", "Brightforge Labs: simple, fast, beautiful apps for small businesses and pros",
                DESCRIPTION, body, extra_ld=[FADEREADY, faq_ld], hero=True)


def about():
    body = page_hero("About us", 'We forge <span class="grad">bright ideas</span> into real products.',
                     "Brightforge Labs is a small software company with a big goal: make great apps that anyone can use to run their work.") + f"""
<section>
<div class="narrow prose">
<span class="kicker">Our story</span>
<h2 style="margin-top:0">Why we started</h2>
<p>People who run their own work are busy. Barbers, nail techs, shop owners and traders have no time to fight their tools. But the apps they use are often slow, confusing or ugly.</p>
<p>We thought they deserved better. So in 2026, Idael Fonseca Hidalgo started <strong>Brightforge Labs LLC</strong>, a software company in Florida, USA.</p>
<p>Our first app is <a href="https://fadeready.com/">FadeReady</a>. It helps barbershops with booking, the live line, bookkeeping and license renewals. FadeReady LLC is owned by Brightforge Labs. Next comes a trading toolkit for traders, with a stop size calculator, trading and daily journals and a prop firm tracker. An app for nail salons is on the way too.</p>
<h2>What our name means</h2>
<p>A forge is a hot fire where metal is shaped into strong tools. <strong>Brightforge</strong> is a place where bright ideas are shaped into real products. <strong>Labs</strong> means we never stop trying new things.</p>
</div>
</section>

<section class="alt">
<div class="wrap">
<span class="kicker">Our values</span>
<h2>Four promises in every app</h2>
<p class="intro">Every app we make has to pass these four tests before it ships.</p>
<div class="grid grid-4">{value_cards()}</div>
</div>
</section>

<section>
<div class="narrow prose">
<span class="kicker">Company facts</span>
<h2 style="margin-top:0">Brightforge Labs at a glance</h2>
<ul>
<li><strong>Legal name:</strong> Brightforge Labs LLC</li>
<li><strong>Type:</strong> Florida limited liability company</li>
<li><strong>Founded:</strong> 2026</li>
<li><strong>Founder:</strong> Idael Fonseca Hidalgo</li>
<li><strong>What we do:</strong> apps for small businesses and independent pros</li>
<li><strong>Our apps:</strong> <a href="https://fadeready.com/">FadeReady</a> (barbershops). Coming soon: a trading toolkit (traders) and a salon app (nail salons)</li>
<li><strong>Location:</strong> Florida, USA</li>
<li><strong>Email:</strong> {email_link()}</li>
</ul>
</div>
</section>"""
    return page("about", "About Brightforge Labs: who we are and what we believe",
                "Brightforge Labs LLC is a Florida software company founded in 2026 by Idael Fonseca Hidalgo. "
                "We make simple, fast, beautiful and secure apps for small businesses and independent pros, like FadeReady.",
                body, current="About", page_type="AboutPage")


def contact():
    body = page_hero("Contact", 'Say <span class="grad">hello</span>.',
                     "Questions, ideas or business matters? Send us an email. A real person reads every message.") + f"""
<section>
<div class="narrow prose">
<h2 style="margin-top:0">Email us</h2>
<p>{email_link("mail", ICONS["mail"] + EMAIL)}</p>
<p>We usually reply within one or two business days.</p>
<h2>Where we are</h2>
<p>Brightforge Labs LLC is based in Florida, USA. We work online, so we can help you from anywhere.</p>
<h2>Need help with FadeReady?</h2>
<p>Visit <a href="https://fadeready.com/">fadeready.com</a> for help with the app, or email us and we will point you to the right place.</p>
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
                 f"""<p>This policy explains, in plain words, what information <strong>Brightforge Labs LLC</strong> ("Brightforge Labs", "we", "us") collects, why, and what choices you have. It covers this website (brightforgelabs.app) and our apps. Some apps, like FadeReady, may also have their own privacy policy. If they do, that policy explains the details for that app.</p>

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
                 f"""<p>These terms are the rules for using the website and apps made by <strong>Brightforge Labs LLC</strong> ("Brightforge Labs", "we", "us"). By using them, you agree to these terms. Some apps may have extra terms. If they do, those terms apply too.</p>

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


def not_found():
    body = page_hero("Error 404", 'This page got <span class="grad">lost in the forge</span>.',
                     "The page you want is not here. Let's get you back home.") + """
<section><div class="narrow"><p><a class="btn btn-hot" href="/">Go to the home page</a></p></div></section>"""
    html = page("404", "Page not found | Brightforge Labs", "This page could not be found.", body)
    return html.replace('<link rel="canonical" href="https://brightforgelabs.app/404">',
                        '<meta name="robots" content="noindex">')


def tidy(html):
    return re.sub(r"\n\s*\n", "\n", html)


def main():
    pages = {"index.html": home(), "about.html": about(), "contact.html": contact(),
             "privacy.html": privacy(), "terms.html": terms(), "404.html": not_found()}
    for name, html in pages.items():
        (OUT / name).write_text(tidy(html))
    urls = ["", "about", "contact", "privacy", "terms"]
    prio = {"": "1.0", "about": "0.8", "contact": "0.7"}
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
