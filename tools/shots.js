const { chromium } = require('playwright');
(async () => {
  const b = await chromium.launch();
  const out = process.argv[2] || '.';
  const base = process.argv[3] || 'http://localhost:4173';
  const pages = (process.argv[4] || '/').split(',');
  for (const scheme of ['light', 'dark']) {
    for (const [name, vp, mobile] of [['desktop', { width: 1440, height: 900 }, false], ['phone', { width: 390, height: 844 }, true]]) {
      const ctx = await b.newContext({ viewport: vp, colorScheme: scheme, isMobile: mobile, deviceScaleFactor: mobile ? 2 : 1, reducedMotion: 'reduce' });
      const p = await ctx.newPage();
      for (const path of pages) {
        await p.goto(base + path);
        const slug = path === '/' ? 'home' : path.slice(1);
        await p.screenshot({ path: `${out}/${slug}-${name}-${scheme}.png`, fullPage: true });
        const w = await p.evaluate(() => document.documentElement.scrollWidth > innerWidth);
        if (w) console.log('HORIZONTAL OVERFLOW', path, name);
      }
      await ctx.close();
    }
  }
  await b.close();
})();
