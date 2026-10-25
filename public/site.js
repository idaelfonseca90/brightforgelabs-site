// Slow, glowing embers rising in the home page hero. Each glow is drawn once to a
// small sprite and reused, the loop runs at 30 fps, and it pauses when hidden or off screen.
(function () {
  var c = document.querySelector('.embers');
  if (!c || !c.getContext || window.matchMedia('(prefers-reduced-motion: reduce)').matches) return;
  var x = c.getContext('2d'), dpr = Math.min(window.devicePixelRatio || 1, 2);
  var colors = ['255,154,77', '255,196,90', '255,120,40', '190,160,255'], sprites = [];
  var w, h, parts = [], running = false, seen = true, last = 0;
  colors.forEach(function (col) {
    var s = document.createElement('canvas'); s.width = s.height = 32;
    var g = s.getContext('2d'), r = g.createRadialGradient(16, 16, 0, 16, 16, 16);
    r.addColorStop(0, 'rgba(' + col + ',1)'); r.addColorStop(0.25, 'rgba(' + col + ',.55)'); r.addColorStop(1, 'rgba(' + col + ',0)');
    g.fillStyle = r; g.fillRect(0, 0, 32, 32); sprites.push(s);
  });
  function size() {
    w = c.clientWidth; h = c.clientHeight;
    c.width = w * dpr; c.height = h * dpr; x.setTransform(dpr, 0, 0, dpr, 0, 0);
  }
  function spark(anywhere) {
    return { x: Math.random() * w, y: anywhere ? Math.random() * h : h + 10, s: 6 + Math.random() * 14,
      v: 0.5 + Math.random() * 1.2, d: (Math.random() - 0.5) * 0.6, a: 0.25 + Math.random() * 0.55,
      t: Math.random() * 6.28, i: (Math.random() * sprites.length) | 0 };
  }
  function draw() {
    x.clearRect(0, 0, w, h);
    for (var i = 0; i < parts.length; i++) {
      var p = parts[i];
      p.t += 0.04; p.y -= p.v; p.x += p.d + Math.sin(p.t) * 0.4;
      if (p.y < -20) { parts[i] = spark(false); continue; }
      x.globalAlpha = p.a * Math.min(1, p.y / (h * 0.85));
      x.drawImage(sprites[p.i], p.x - p.s / 2, p.y - p.s / 2, p.s, p.s);
    }
    x.globalAlpha = 1;
  }
  function loop(now) {
    if (!running) return;
    if (now - last > 33) { last = now; draw(); }
    requestAnimationFrame(loop);
  }
  function set() {
    var go = seen && !document.hidden;
    if (go && !running) { running = true; requestAnimationFrame(loop); }
    if (!go) running = false;
  }
  function start() {
    size();
    var n = Math.round(Math.min(45, w * h / 22000));
    for (var i = 0; i < n; i++) parts.push(spark(true));
    draw();
    if ('IntersectionObserver' in window) new IntersectionObserver(function (e) { seen = e[0].isIntersecting; set(); }).observe(c);
    document.addEventListener('visibilitychange', set);
    window.addEventListener('resize', function () { size(); draw(); });
    set();
  }
  window.addEventListener('load', function () { setTimeout(start, 600); });
})();
