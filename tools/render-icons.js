// Renders the logo SVGs into the PNG icon sizes browsers, phones and Google use.
const { chromium } = require('playwright');
const fs = require('fs');
const path = require('path');
const root = path.join(__dirname, '..');
const jobs = [
  ['mark.svg', 'public/favicon-16x16.png', 16],
  ['mark.svg', 'public/favicon-32x32.png', 32],
  ['mark.svg', 'public/favicon-48x48.png', 48],
  ['mark.svg', 'public/favicon-96x96.png', 96],
  ['mark.svg', 'public/icons/icon-192.png', 192],
  ['mark.svg', 'public/icons/icon-512.png', 512],
  ['mark-maskable.svg', 'public/icons/maskable-512.png', 512],
  ['mark-square.svg', 'public/apple-touch-icon.png', 180],
  ['mark.svg', 'public/icons/logo-square-512.png', 512],
];
(async () => {
  const browser = await chromium.launch();
  for (const [src, out, size] of jobs) {
    const svg = fs.readFileSync(path.join(root, 'src', src), 'utf8');
    const page = await browser.newPage({ viewport: { width: size, height: size } });
    await page.setContent(`<html><body style="margin:0;background:transparent">${svg.replace('<svg ', `<svg width="${size}" height="${size}" `)}</body></html>`);
    await page.screenshot({ path: path.join(root, out), omitBackground: true });
    await page.close();
  }
  await browser.close();
})();
