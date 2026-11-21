/* Universe Explorer — interactive orrery (solar system page) */
(function () {
  'use strict';

  var doc = document;

  function init() {
    var solar = doc.getElementById('solar');
    if (!solar || !window.UE_SOLAR) return;
    var stage = solar.querySelector('.solar__stage');
    var info = doc.getElementById('solarInfo');
    var data = window.UE_SOLAR;
    var dots = solar.querySelectorAll('.planet-dot');
    var orbits = solar.querySelectorAll('.orbit');
    var pauseBtn = doc.getElementById('solarPause');
    var speed = doc.getElementById('solarSpeed');
    var paused = false;
    var scale = 1;
    var current = '';

    function layout() {
      if (!stage) return;
      var w = stage.clientWidth;
      var h = stage.clientHeight;
      if (!w || !h) return;
      var maxR = Math.min(w, h) / 2 - 22;
      orbits.forEach(function (orbit) {
        var frac = parseFloat(orbit.getAttribute('data-r')) || 0.5;
        var r = maxR * frac;
        orbit.style.width = r * 2 + 'px';
        orbit.style.height = r * 2 + 'px';
      });
    }

    function durations() {
      orbits.forEach(function (orbit) {
        var rotor = orbit.querySelector('.orbit__rotor');
        var days = parseFloat(orbit.getAttribute('data-period')) || 365;
        var base = 8 * Math.pow(days / 88, 0.42);
        if (rotor) {
          rotor.setAttribute('data-base', String(base));
          rotor.style.animationDuration = base * scale + 's';
        }
      });
    }

    function show(id) {
      var planet = data[id];
      if (!planet || !info) return;
      current = id;
      var title = info.querySelector('.js-solar-title');
      var type = info.querySelector('.js-solar-type');
      var desc = info.querySelector('.js-solar-desc');
      var facts = info.querySelector('.js-solar-facts');
      var link = info.querySelector('.js-solar-link');
      if (title) title.textContent = planet.name;
      if (type) type.textContent = planet.type;
      if (desc) desc.textContent = planet.desc;
      if (facts) {
        facts.innerHTML = planet.facts.map(function (pair) {
          return '<div><dt>' + pair[0] + '</dt><dd>' + pair[1] + '</dd></div>';
        }).join('');
      }
      if (link) {
        link.href = planet.url;
        link.textContent = 'Άνοιξε τη σελίδα του ' + planet.name;
      }
      info.hidden = false;
      info.classList.remove('is-swapping');
      // restart the little fade
      void info.offsetWidth;
      info.classList.add('is-swapping');
      dots.forEach(function (dot) {
        var active = dot.getAttribute('data-planet') === id;
        dot.classList.toggle('is-active', active);
        dot.setAttribute('aria-pressed', String(active));
      });
    }

    dots.forEach(function (dot) {
      dot.addEventListener('click', function () {
        show(dot.getAttribute('data-planet'));
      });
      dot.addEventListener('mouseenter', function () {
        if (dot.getAttribute('data-planet') !== current) dot.classList.add('is-hover');
      });
      dot.addEventListener('mouseleave', function () {
        dot.classList.remove('is-hover');
      });
    });

    var sun = solar.querySelector('.solar__sun');
    if (sun) {
      sun.addEventListener('click', function () {
        show('sun');
      });
    }

    if (pauseBtn) {
      pauseBtn.addEventListener('click', function () {
        paused = !paused;
        solar.classList.toggle('is-paused', paused);
        pauseBtn.setAttribute('aria-pressed', String(paused));
        pauseBtn.querySelector('span').textContent = paused ? 'Συνέχισε την κίνηση' : 'Παύση κίνησης';
      });
    }

    if (speed) {
      speed.addEventListener('input', function () {
        scale = 0.35 + parseFloat(speed.value) / 100 * 1.65;
        orbits.forEach(function (orbit) {
          var rotor = orbit.querySelector('.orbit__rotor');
          if (!rotor) return;
          var base = parseFloat(rotor.getAttribute('data-base')) || 20;
          rotor.style.animationDuration = base * scale + 's';
        });
      });
    }

    layout();
    durations();
    show('earth');

    window.addEventListener('resize', debounce(layout, 150));
    if (window.ResizeObserver && stage) {
      new ResizeObserver(debounce(layout, 60)).observe(stage);
    }
  }

  function debounce(fn, wait) {
    var id = 0;
    return function () {
      window.clearTimeout(id);
      id = window.setTimeout(fn, wait);
    };
  }

  if (doc.readyState === 'loading') {
    doc.addEventListener('DOMContentLoaded', init);
  } else {
    init();
  }
})();
