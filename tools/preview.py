"""Makes a click-through copy of the site for the in-chat preview (relative links, no server needed)."""
import re, shutil
from pathlib import Path
root = Path(__file__).resolve().parent.parent
pub, out = root / "public", root / "preview"
shutil.rmtree(out, ignore_errors=True); out.mkdir()
links = {'"/site.js"': '"site.js"', '"/"': '"home.html"', '"/#apps"': '"home.html#apps"', '"/about"': '"about.html"',
         '"/contact"': '"contact.html"', '"/privacy"': '"privacy.html"', '"/terms"': '"terms.html"', '"/fadeready"': '"fadeready.html"', '"/trading-toolkit"': '"trading-toolkit.html"', '"/salon-app"': '"salon-app.html"'}
for src, dst in [("index.html", "home.html"), ("about.html", "about.html"), ("contact.html", "contact.html"),
                 ("privacy.html", "privacy.html"), ("terms.html", "terms.html"),
                 ("fadeready.html", "fadeready.html"), ("trading-toolkit.html", "trading-toolkit.html"),
                 ("salon-app.html", "salon-app.html")]:
    html = (pub / src).read_text()
    for a, b in links.items():
        html = html.replace("href=" + a, "href=" + b).replace("src=" + a, "src=" + b)
    (out / dst).write_text(html)
home = (out / "home.html").read_text()
title = re.search(r"<title>.*?</title>", home).group(0)
style = re.search(r"<style>.*?</style>", home, re.S).group(0)
body = re.search(r"<body>(.*)</body>", home, re.S).group(1)
(out / "index.html").write_text(f"<title>Brightforge Labs Website</title>\n{style}\n{body}")
shutil.copy(pub / "site.js", out / "site.js")
print("preview ready")
