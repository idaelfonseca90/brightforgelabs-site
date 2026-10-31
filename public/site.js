// The home page forge: embers fly up from the anvil in the logo, with a burst each time
// the spark strikes (every 2.4 s, in step with the CSS animation), plus a few slow embers
// drifting across the hero. Each glow is drawn once to a sprite and reused, the loop runs
// at 30 fps, and it pauses when the tab is hidden or the hero is off screen.
(function () {
  var c = document.querySelector('.embers');
  if (!c || !c.getContext || window.matchMedia('(prefers-reduced-motion: reduce)').matches) return;
  var emitter = document.querySelector('.emitter');
  var x = c.getContext('2d'), dpr = Math.min(window.devicePixelRatio || 1, 2);
  var colors = ['255,154,77', '255,196,90', '255,120,40', '255,220,140', '190,160,255'], sprites = [];
  var w, h, ex = 0, ey = 0, parts = [], running = false, seen = true, last = 0, lastPhase = 0;
  colors.forEach(function (col) {
    var s = document.createElement('canvas'); s.width = s.height = 32;
    var g = s.getContext('2d'), r = g.createRadialGradient(16, 16, 0, 16, 16, 16);
    r.addColorStop(0, 'rgba(' + col + ',1)'); r.addColorStop(0.25, 'rgba(' + col + ',.55)'); r.addColorStop(1, 'rgba(' + col + ',0)');
    g.fillStyle = r; g.fillRect(0, 0, 32, 32); sprites.push(s);
  });
  function size() {
    w = c.clientWidth; h = c.clientHeight;
    c.width = w * dpr; c.height = h * dpr; x.setTransform(dpr, 0, 0, dpr, 0, 0);
    if (emitter) {
      var a = c.getBoundingClientRect(), b = emitter.getBoundingClientRect();
      ex = b.left - a.left; ey = b.top - a.top;
    }
  }
  function drift(anywhere) {
    return { x: Math.random() * w, y: anywhere ? Math.random() * h : h + 10, vx: (Math.random() - 0.5) * 0.5,
      vy: -(0.4 + Math.random() * 0.9), g: 0, s: 5 + Math.random() * 10, a: 0.2 + Math.random() * 0.4,
      life: 1e9, i: (Math.random() * 4) | 0, t: Math.random() * 6.28 };
  }
  function spark(power) {
    var ang = -Math.PI / 2 + (Math.random() - 0.5) * 1.9, sp = (1.5 + Math.random() * 3.5) * power;
    return { x: ex + (Math.random() - 0.5) * 40, y: ey, vx: Math.cos(ang) * sp, vy: Math.sin(ang) * sp, g: 0.045,
      s: 4 + Math.random() * 9, a: 0.6 + Math.random() * 0.4, life: 40 + Math.random() * 50,
      i: (Math.random() * colors.length) | 0, t: 0 };
  }
  function draw() {
    x.clearRect(0, 0, w, h);
    for (var i = parts.length - 1; i >= 0; i--) {
      var p = parts[i];
      p.t += 0.05; p.vy += p.g; p.x += p.vx + (p.g ? 0 : Math.sin(p.t) * 0.3); p.y += p.vy; p.life--;
      if (p.life <= 0 || p.y < -20 || p.y > h + 20) {
        if (p.g) parts.splice(i, 1); else parts[i] = drift(false);
        continue;
      }
      x.globalAlpha = p.g ? p.a * Math.min(1, p.life / 30) : p.a * Math.min(1, p.y / (h * 0.85));
      x.drawImage(sprites[p.i], p.x - p.s / 2, p.y - p.s / 2, p.s, p.s);
    }
    x.globalAlpha = 1;
  }
  function loop(now) {
    if (!running) return;
    if (now - last > 33) {
      last = now;
      if (emitter && parts.length < 110) {
        if (Math.random() < 0.45) parts.push(spark(0.7));
        var phase = (document.timeline ? document.timeline.currentTime : now) % 2400;
        if (lastPhase < 2064 && phase >= 2064) for (var k = 0; k < 20; k++) parts.push(spark(1.15));
        lastPhase = phase;
      }
      draw();
    }
    requestAnimationFrame(loop);
  }
  function set() {
    var go = seen && !document.hidden;
    if (go && !running) { running = true; requestAnimationFrame(loop); }
    if (!go) running = false;
  }
  function start() {
    size();
    var n = Math.round(Math.min(30, w * h / 30000));
    for (var i = 0; i < n; i++) parts.push(drift(true));
    draw();
    if ('IntersectionObserver' in window) new IntersectionObserver(function (e) { seen = e[0].isIntersecting; set(); }).observe(c);
    document.addEventListener('visibilitychange', set);
    window.addEventListener('resize', function () { size(); draw(); });
    set();
  }
  window.addEventListener('load', function () { setTimeout(start, 600); });
})();

// Hero app badges: always jump to the app's card, even on a repeat tap, and replay its highlight.
(function () {
  document.querySelectorAll('a.orb[href^="#"]').forEach(function (a) {
    a.addEventListener('click', function (e) {
      var card = document.querySelector(a.getAttribute('href'));
      if (!card) return;
      e.preventDefault();
      card.scrollIntoView({ behavior: 'smooth', block: 'start' });
      history.replaceState(null, '', a.getAttribute('href'));
      card.classList.remove('spot'); void card.offsetWidth; card.classList.add('spot');
      card.setAttribute('tabindex', '-1'); card.focus({ preventScroll: true });
    });
  });
})();
