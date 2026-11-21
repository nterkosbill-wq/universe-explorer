/* Universe Explorer — page interactions: quiz, facts, cosmic timeline, tabs, calculator, TOC */
(function () {
  'use strict';

  var doc = document;

  function el(tag, cls, html) {
    var node = doc.createElement(tag);
    if (cls) node.className = cls;
    if (html != null) node.innerHTML = html;
    return node;
  }

  function shuffle(list) {
    var a = list.slice();
    for (var i = a.length - 1; i > 0; i--) {
      var j = Math.floor(Math.random() * (i + 1));
      var tmp = a[i];
      a[i] = a[j];
      a[j] = tmp;
    }
    return a;
  }

  /* ---------------- quiz ---------------- */
  function quiz() {
    var app = doc.getElementById('quizApp');
    if (!app || !window.UE_QUIZ || !window.UE_QUIZ.length) return;
    var pool = window.UE_QUIZ;
    var perRun = Math.min(10, pool.length);
    var questions = [];
    var index = 0;
    var score = 0;
    var answered = false;

    function start() {
      questions = shuffle(pool).slice(0, perRun).map(function (q) {
        var correctText = q.options[q.correct];
        var options = shuffle(q.options);
        return {
          q: q.q,
          options: options,
          correct: options.indexOf(correctText),
          why: q.why
        };
      });
      index = 0;
      score = 0;
      answered = false;
      renderShell();
      renderQuestion();
    }

    function renderShell() {
      app.innerHTML =
        '<div class="quiz__top">' +
        '<span class="quiz__score">Ερώτηση <b class="js-q-num">1</b> από <b>' + perRun + '</b></span>' +
        '<span class="quiz__score">Σωστές: <b class="js-score">0</b></span>' +
        '</div>' +
        '<div class="quiz__bar"><i class="js-bar" style="width:0%"></i></div>' +
        '<h2 class="quiz__q js-question"></h2>' +
        '<div class="quiz__options js-options"></div>' +
        '<div class="quiz__feedback js-feedback" hidden></div>' +
        '<div class="quiz__foot">' +
        '<span class="quiz__summary js-progress"></span>' +
        '<button type="button" class="btn btn--sm js-next" hidden>Επόμενη ερώτηση</button>' +
        '</div>' +
        '<div class="quiz__result js-result" hidden></div>';

      app.querySelector('.js-next').addEventListener('click', next);
    }

    function renderQuestion() {
      var q = questions[index];
      answered = false;
      app.querySelector('.js-q-num').textContent = String(index + 1);
      app.querySelector('.js-score').textContent = String(score);
      app.querySelector('.js-bar').style.width = (index / perRun) * 100 + '%';
      app.querySelector('.js-question').textContent = q.q;
      app.querySelector('.js-feedback').hidden = true;
      app.querySelector('.js-next').hidden = true;
      app.querySelector('.js-progress').textContent = 'Ερώτηση ' + (index + 1) + ' από ' + perRun;

      var box = app.querySelector('.js-options');
      box.innerHTML = '';
      q.options.forEach(function (text, i) {
        var btn = el('button', 'quiz__option', '<em>' + String.fromCharCode(65 + i) + '</em><span>' + text + '</span><span class="quiz__mark"></span>');
        btn.type = 'button';
        btn.addEventListener('click', function () {
          choose(i, btn);
        });
        box.appendChild(btn);
      });
    }

    function choose(i, btn) {
      if (answered) return;
      answered = true;
      var q = questions[index];
      var nodes = app.querySelectorAll('.quiz__option');
      var correct = i === q.correct;
      if (correct) score++;
      nodes.forEach(function (node, n) {
        node.disabled = true;
        if (n === q.correct) {
          node.classList.add('is-correct');
          node.querySelector('.quiz__mark').textContent = '✓';
        } else if (n === i) {
          node.classList.add('is-wrong');
          node.querySelector('.quiz__mark').textContent = '✕';
        } else {
          node.classList.add('is-muted');
        }
      });
      app.querySelector('.js-score').textContent = String(score);
      app.querySelector('.js-bar').style.width = ((index + 1) / perRun) * 100 + '%';

      var fb = app.querySelector('.js-feedback');
      fb.hidden = false;
      fb.innerHTML = '<strong>' + (correct ? 'Σωστά!' : 'Όχι ακριβώς.') + '</strong> ' + q.why;
      var nextBtn = app.querySelector('.js-next');
      nextBtn.hidden = false;
      nextBtn.textContent = index + 1 >= perRun ? 'Δες το αποτέλεσμα' : 'Επόμενη ερώτηση';
      nextBtn.focus();
    }

    function next() {
      index++;
      if (index >= perRun) {
        finish();
        return;
      }
      renderQuestion();
    }

    function finish() {
      app.querySelector('.quiz__bar').style.width = '100%';
      app.querySelector('.js-question').textContent = '';
      app.querySelector('.js-options').innerHTML = '';
      app.querySelector('.js-feedback').hidden = true;
      app.querySelector('.js-next').hidden = true;
      app.querySelector('.js-progress').textContent = 'Ολοκλήρωσες το κουίζ.';

      var pct = Math.round((score / perRun) * 100);
      var verdict;
      if (pct === 100) verdict = 'Αστροφυσικός επιπέδου NASA. Το σύμπαν δεν έχει μυστικά για σένα.';
      else if (pct >= 80) verdict = 'Εξαιρετική γνώση του διαστήματος — λίγη ακόμη μελέτη και φτάνεις στα άστρα.';
      else if (pct >= 50) verdict = 'Καλή αρχή! Έχεις τις βάσεις, συνέχισε την εξερεύνηση.';
      else verdict = 'Το ταξίδι μόλις ξεκίνησε. Εξερεύνησε τις ενότητες και δοκίμασε ξανά.';

      var result = app.querySelector('.js-result');
      result.hidden = false;
      result.innerHTML =
        '<div class="quiz__ring" style="--pct:' + pct + '"><div><strong>' + pct + '%</strong><span>' + score + ' / ' + perRun + '</span></div></div>' +
        '<p class="quiz__verdict">' + verdict + '</p>' +
        '<div class="btn-row"><button type="button" class="btn js-restart">Δοκίμασε ξανά</button>' +
        '<a class="btn btn--ghost" href="solar-system.html">Εξερεύνησε το Ηλιακό Σύστημα</a></div>';
      result.querySelector('.js-restart').addEventListener('click', start);
      result.scrollIntoView({ block: 'nearest', behavior: 'smooth' });
    }

    start();
  }

  /* ---------------- did you know ---------------- */
  function facts() {
    var card = doc.getElementById('factCard');
    if (!card || !window.UE_FACTS || !window.UE_FACTS.length) return;
    var text = card.querySelector('.js-fact-text');
    var tag = card.querySelector('.js-fact-tag');
    var nextBtn = card.querySelector('.js-fact-next');
    var facts = window.UE_FACTS;
    var i = Math.floor(Math.random() * facts.length);

    function paint() {
      var fact = facts[i];
      text.classList.add('is-swapping');
      window.setTimeout(function () {
        text.textContent = fact.text;
        if (tag) tag.textContent = fact.tag || 'Ήξερες ότι;';
        text.classList.remove('is-swapping');
      }, 220);
    }

    paint();
    if (nextBtn) {
      nextBtn.addEventListener('click', function () {
        i = (i + 1 + Math.floor(Math.random() * (facts.length - 1))) % facts.length;
        paint();
      });
    }
  }

  /* ---------------- cosmic timeline ---------------- */
  function cosmic() {
    var wrap = doc.getElementById('cosmic');
    if (!wrap || !window.UE_COSMIC) return;
    var steps = wrap.querySelectorAll('.cosmic-step');
    var title = wrap.querySelector('.js-cosmic-title');
    var body = wrap.querySelector('.js-cosmic-text');
    var badge = wrap.querySelector('.js-cosmic-badge');
    var detail = wrap.querySelector('.cosmic-detail');
    var data = window.UE_COSMIC;

    function select(n) {
      var item = data[n];
      if (!item) return;
      steps.forEach(function (step, k) {
        step.classList.toggle('is-active', k === n);
        step.setAttribute('aria-selected', String(k === n));
      });
      detail.classList.remove('is-visible');
      window.setTimeout(function () {
        title.textContent = item.title;
        body.textContent = item.text;
        badge.textContent = item.badge;
        detail.classList.add('is-visible');
      }, 140);
    }

    steps.forEach(function (step) {
      step.addEventListener('click', function () {
        select(parseInt(step.getAttribute('data-step'), 10) || 0);
      });
    });
    select(0);
  }

  /* ---------------- tabs ---------------- */
  function tabs() {
    doc.querySelectorAll('.tabs').forEach(function (group) {
      var buttons = group.querySelectorAll('button[data-tab]');
      buttons.forEach(function (btn) {
        btn.addEventListener('click', function () {
          var target = btn.getAttribute('data-tab');
          buttons.forEach(function (b) {
            b.setAttribute('aria-selected', String(b === btn));
          });
          doc.querySelectorAll('[data-panel]').forEach(function (panel) {
            panel.hidden = panel.getAttribute('data-panel') !== target;
          });
        });
      });
    });
  }

  /* ---------------- black hole time dilation ---------------- */
  function blackhole() {
    var slider = doc.getElementById('bhSlider');
    if (!slider) return;
    var dist = doc.querySelector('.js-bh-dist');
    var dilation = doc.querySelector('.js-bh-dilation');
    var orbit = doc.querySelector('.js-bh-orbit');
    var perHour = doc.querySelector('.js-bh-hour');

    function update() {
      var r = parseFloat(slider.value); // in Schwarzschild radii
      var factor = Math.sqrt(Math.max(0, 1 - 1 / r));
      var hours = 60 * 60 * factor;
      if (dist) dist.textContent = r.toFixed(2).replace('.', ',') + ' rₛ';
      if (dilation) dilation.textContent = factor.toFixed(3).replace('.', ',');
      if (perHour) perHour.textContent = Math.floor(hours / 60) + ' λεπτά ' + Math.round(hours % 60) + ' δευτ.';
      if (orbit) orbit.textContent = Math.sqrt(1 / (2 * (r - 1))).toFixed(2).replace('.', ',') + ' c';
    }

    slider.addEventListener('input', update);
    update();
  }

  /* ---------------- table of contents highlight ---------------- */
  function toc() {
    var links = doc.querySelectorAll('.toc a[href^="#"]');
    if (!links.length || !('IntersectionObserver' in window)) return;
    var map = {};
    links.forEach(function (link) {
      var id = link.getAttribute('href').slice(1);
      var target = doc.getElementById(id);
      if (target) map[id] = link;
    });
    var io = new IntersectionObserver(function (entries) {
      entries.forEach(function (entry) {
        if (!entry.isIntersecting) return;
        links.forEach(function (l) {
          l.classList.remove('is-active');
        });
        var link = map[entry.target.id];
        if (link) link.classList.add('is-active');
      });
    }, { rootMargin: '-20% 0px -65% 0px' });
    Object.keys(map).forEach(function (id) {
      io.observe(doc.getElementById(id));
    });
  }

  function init() {
    quiz();
    facts();
    cosmic();
    tabs();
    blackhole();
    toc();
  }

  if (doc.readyState === 'loading') {
    doc.addEventListener('DOMContentLoaded', init);
  } else {
    init();
  }
})();
