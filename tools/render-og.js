// Renders the 1200x630 social preview image (og-image.png) used when links are shared.
const { chromium } = require('playwright');
const fs = require('fs');
const path = require('path');
const root = path.join(__dirname, '..');
const mark = fs.readFileSync(path.join(root, 'src/mark.svg'), 'utf8');
const html = `<html><body style="margin:0;width:1200px;height:630px;overflow:hidden;font-family:ui-sans-serif,system-ui,'DejaVu Sans',sans-serif;color:#fff;
background:radial-gradient(700px 420px at 92% 110%,rgba(232,89,12,.45),transparent 65%),#0b1220">
<div style="position:absolute;left:84px;top:96px;width:700px">
<div style="display:inline-block;padding:8px 18px;border-radius:999px;background:rgba(255,255,255,.1);border:1px solid rgba(255,255,255,.2);font-size:24px;font-weight:600;color:#ffe7c7">Brightforge Labs LLC · Florida, USA</div>
<div style="font-size:92px;font-weight:800;letter-spacing:-3px;line-height:1;margin-top:34px">Brightforge Labs</div>
<div style="font-size:50px;font-weight:800;letter-spacing:-1.5px;line-height:1.1;margin-top:22px;color:#ff8a3d">The company behind<br>FadeReady and more apps.</div>
<div style="font-size:28px;color:#e9e3ff;margin-top:30px">Simple, fast, beautiful and secure apps.</div>
</div>
<div style="position:absolute;right:90px;top:155px;width:320px;height:320px;filter:drop-shadow(0 30px 60px rgba(255,106,26,.4))">${mark.replace('<svg ','<svg width="320" height="320" ')}</div>
<div style="position:absolute;left:0;right:0;bottom:0;height:8px;background:#e8590c"></div>
</body></html>`;
(async () => {
  const b = await chromium.launch();
  const p = await b.newPage({ viewport: { width: 1200, height: 630 } });
  await p.setContent(html);
  await p.screenshot({ path: path.join(root, 'public/og-image.jpg'), type: 'jpeg', quality: 86 });
  await b.close();
})();
