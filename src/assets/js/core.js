/* Universe Explorer — core: starfield, preloader, header, nav, reveal, transitions */
(function () {
  'use strict';

  var doc = document;
  var reduceMotion = window.matchMedia('(prefers-reduced-motion: reduce)').matches;

  function debounce(fn, wait) {
    var id = 0;
    return function () {
      window.clearTimeout(id);
      id = window.setTimeout(fn, wait);
    };
  }

  /* ---------- starfield ---------- */
  function starfield() {
    var canvas = doc.getElementById('starfield');
    if (!canvas || !canvas.getContext) return;
    var ctx = canvas.getContext('2d');
    var stars = [];
    var meteors = [];
    var w = 0;
    var h = 0;
    var dpr = 1;
    var raf = 0;
    var last = 0;
    var running = false;

    function seed() {
      var count = Math.max(55, Math.min(200, Math.round((w * h) / 11000)));
      stars = [];
      for (var i = 0; i < count; i++) {
        var layer = Math.random();
        stars.push({
          x: Math.random() * w,
          y: Math.random() * h,
          r: (layer > 0.9 ? 1.5 : layer > 0.65 ? 1.05 : 0.65) * (0.7 + Math.random() * 0.7),
          a: 0.18 + Math.random() * 0.7,
          ph: Math.random() * Math.PI * 2,
          sp: 0.0004 + Math.random() * 0.0011,
          hue: layer > 0.93 ? '200, 226, 255' : layer > 0.8 ? '255, 232, 205' : '224, 228, 255',
          dy: 0.004 + layer * 0.01
        });
      }
    }

    function resize() {
      dpr = Math.min(window.devicePixelRatio || 1, 2);
      w = canvas.clientWidth;
      h = canvas.clientHeight;
      canvas.width = Math.round(w * dpr);
      canvas.height = Math.round(h * dpr);
      ctx.setTransform(dpr, 0, 0, dpr, 0, 0);
      seed();
      drawStatic();
    }

    function drawStatic() {
      ctx.clearRect(0, 0, w, h);
      for (var i = 0; i < stars.length; i++) {
        var s = stars[i];
        ctx.beginPath();
        ctx.fillStyle = 'rgba(' + s.hue + ',' + (s.a * 0.8).toFixed(3) + ')';
        ctx.arc(s.x, s.y, s.r, 0, Math.PI * 2);
        ctx.fill();
      }
    }

    function spawnMeteor() {
      if (reduceMotion || meteors.length > 1) return;
      meteors.push({
        x: Math.random() * w * 0.9,
        y: Math.random() * h * 0.4,
        len: 90 + Math.random() * 130,
        life: 0,
        dur: 1100 + Math.random() * 900,
        angle: Math.PI / 4 + (Math.random() - 0.5) * 0.2
      });
    }

    function frame(t) {
      if (!running) return;
      var dt = Math.min(48, t - (last || t));
      last = t;
      ctx.clearRect(0, 0, w, h);
      for (var i = 0; i < stars.length; i++) {
        var s = stars[i];
        s.ph += s.sp * dt;
        s.y += s.dy * dt * 0.06;
        if (s.y < -2) s.y = h + 2;
        var a = s.a * (0.6 + 0.4 * Math.sin(s.ph));
        ctx.beginPath();
        ctx.fillStyle = 'rgba(' + s.hue + ',' + a.toFixed(3) + ')';
        ctx.arc(s.x, s.y, s.r, 0, Math.PI * 2);
        ctx.fill();
      }
      for (var m = meteors.length - 1; m >= 0; m--) {
        var mt = meteors[m];
        mt.life += dt;
        var k = mt.life / mt.dur;
        if (k >= 1) {
          meteors.splice(m, 1);
          continue;
        }
        var travel = mt.len * 3.2 * k;
        var x = mt.x + Math.cos(mt.angle) * travel;
        var y = mt.y + Math.sin(mt.angle) * travel;
        var tx = x - Math.cos(mt.angle) * mt.len;
        var ty = y - Math.sin(mt.angle) * mt.len;
        var grad = ctx.createLinearGradient(tx, ty, x, y);
        grad.addColorStop(0, 'rgba(255,255,255,0)');
        grad.addColorStop(0.7, 'rgba(190,220,255,' + (0.4 * (1 - k)).toFixed(3) + ')');
        grad.addColorStop(1, 'rgba(255,255,255,' + (0.85 * (1 - k)).toFixed(3) + ')');
        ctx.strokeStyle = grad;
        ctx.lineWidth = 1.4;
        ctx.beginPath();
        ctx.moveTo(tx, ty);
        ctx.lineTo(x, y);
        ctx.stroke();
      }
      raf = window.requestAnimationFrame(frame);
    }

    function start() {
      if (running) return;
      running = true;
      last = 0;
      raf = window.requestAnimationFrame(frame);
    }

    function stop() {
      running = false;
      window.cancelAnimationFrame(raf);
    }

    resize();
    window.addEventListener('resize', debounce(resize, 180));

    if (reduceMotion) {
      drawStatic();
      return;
    }

    start();
    window.setInterval(spawnMeteor, 5200);

    doc.addEventListener('visibilitychange', function () {
      if (doc.hidden) {
        stop();
        running = false;
      } else if (!running) {
        start();
      }
    });
  }

  /* ---------- preloader (first visit per session) ---------- */
  function preloader() {
    var el = doc.getElementById('preloader');
    if (!el) return;
    var seen = false;
    try {
      seen = sessionStorage.getItem('ue-visited') === '1';
    } catch (err) {}
    if (seen) {
      el.remove();
      return;
    }
    try {
      sessionStorage.setItem('ue-visited', '1');
    } catch (err) {}
    var done = false;
    function hide() {
      if (done) return;
      done = true;
      el.classList.add('is-done');
      window.setTimeout(function () {
        el.remove();
      }, 700);
    }
    window.addEventListener('load', function () {
      window.setTimeout(hide, 320);
    });
    window.setTimeout(hide, 2400);
  }

  /* ---------- header + scroll progress ---------- */
  function chrome() {
    var header = doc.getElementById('siteHeader');
    var bar = doc.querySelector('.scroll-progress');
    var queued = false;

    function update() {
      queued = false;
      var y = window.scrollY || 0;
      if (header) header.classList.toggle('is-scrolled', y > 24);
      if (bar) {
        var max = doc.documentElement.scrollHeight - window.innerHeight;
        bar.style.transform = 'scaleX(' + (max > 0 ? Math.min(1, y / max) : 0) + ')';
      }
    }

    window.addEventListener('scroll', function () {
      if (queued) return;
      queued = true;
      window.requestAnimationFrame(update);
    }, { passive: true });
    update();
  }

  /* ---------- mobile navigation ---------- */
  function mobileNav() {
    var nav = doc.getElementById('mobileNav');
    var toggle = doc.querySelector('.nav-toggle');
    var closeBtn = doc.querySelector('.js-nav-close');
    if (!nav || !toggle) return;
    var open = false;
    var lastFocus = null;

    function setOpen(next) {
      open = next;
      nav.classList.toggle('is-open', open);
      doc.body.classList.toggle('nav-open', open);
      toggle.setAttribute('aria-expanded', String(open));
      if (open) {
        lastFocus = doc.activeElement;
        var first = nav.querySelector('a, button');
        if (first) {
          window.setTimeout(function () {
            first.focus();
          }, 60);
        }
      } else if (lastFocus && lastFocus.focus) {
        lastFocus.focus();
      }
    }

    toggle.addEventListener('click', function () {
      setOpen(!open);
    });
    if (closeBtn) {
      closeBtn.addEventListener('click', function () {
        setOpen(false);
      });
    }
    nav.addEventListener('click', function (e) {
      if (e.target === nav) setOpen(false);
    });

    doc.addEventListener('keydown', function (e) {
      if (!open) return;
      if (e.key === 'Escape') {
        setOpen(false);
        return;
      }
      if (e.key !== 'Tab') return;
      var f = nav.querySelectorAll('a, button');
      if (!f.length) return;
      var first = f[0];
      var last = f[f.length - 1];
      if (e.shiftKey && doc.activeElement === first) {
        e.preventDefault();
        last.focus();
      } else if (!e.shiftKey && doc.activeElement === last) {
        e.preventDefault();
        first.focus();
      }
    });

    window.matchMedia('(min-width: 1121px)').addEventListener('change', function (e) {
      if (e.matches && open) setOpen(false);
    });
  }

  /* ---------- reveal on scroll ---------- */
  function reveal() {
    var items = doc.querySelectorAll('.reveal');
    if (!items.length) return;
    if (!('IntersectionObserver' in window) || reduceMotion) {
      for (var i = 0; i < items.length; i++) items[i].classList.add('is-visible');
      return;
    }
    var io = new IntersectionObserver(function (entries) {
      entries.forEach(function (entry) {
        if (!entry.isIntersecting) return;
        entry.target.classList.add('is-visible');
        io.unobserve(entry.target);
      });
    }, { rootMargin: '0px 0px -8% 0px', threshold: 0.08 });
    items.forEach(function (el) {
      io.observe(el);
    });
  }

  /* ---------- page transitions ---------- */
  function transitions() {
    if (reduceMotion) return;
    doc.addEventListener('click', function (e) {
      if (e.defaultPrevented || e.button !== 0 || e.metaKey || e.ctrlKey || e.shiftKey || e.altKey) return;
      var a = e.target.closest ? e.target.closest('a') : null;
      if (!a) return;
      var href = a.getAttribute('href');
      if (!href || a.target === '_blank' || a.hasAttribute('download')) return;
      if (href.charAt(0) === '#' || href.indexOf('mailto:') === 0) return;
      var url;
      try {
        url = new URL(a.href, location.href);
      } catch (err) {
        return;
      }
      if (url.host !== location.host) return;
      if (url.pathname === location.pathname && url.hash === location.hash) return;
      if (!/\.html$/.test(url.pathname) && url.pathname !== '/') return;
      e.preventDefault();
      doc.body.classList.add('is-leaving');
      window.setTimeout(function () {
        location.href = url.href;
      }, 300);
    });
    window.addEventListener('pageshow', function (e) {
      if (e.persisted) doc.body.classList.remove('is-leaving');
    });
  }

  /* ---------- hero pointer parallax ---------- */
  function heroParallax() {
    if (reduceMotion) return;
    var planet = doc.querySelector('.hero__planet');
    var hero = doc.querySelector('.hero');
    if (!planet || !hero || window.matchMedia('(hover: none)').matches) return;
    hero.addEventListener('mousemove', function (e) {
      var r = hero.getBoundingClientRect();
      var dx = (e.clientX - r.left) / r.width - 0.5;
      var dy = (e.clientY - r.top) / r.height - 0.5;
      planet.style.transform = 'translate3d(' + (dx * 18).toFixed(1) + 'px,' + (dy * 14).toFixed(1) + 'px,0)';
    });
    hero.addEventListener('mouseleave', function () {
      planet.style.transform = '';
    });
  }

  function init() {
    starfield();
    preloader();
    chrome();
    mobileNav();
    reveal();
    transitions();
    heroParallax();
  }

  if (doc.readyState === 'loading') {
    doc.addEventListener('DOMContentLoaded', init);
  } else {
    init();
  }
})();
