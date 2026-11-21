/* Universe Explorer — global search overlay */
(function () {
  'use strict';

  var doc = document;

  function normalise(value) {
    return String(value)
      .toLowerCase()
      .normalize('NFD')
      .replace(/[\u0300-\u036f]/g, '')
      .replace(/ς/g, 'σ')
      .replace(/[^a-z0-9α-ω\s]/g, ' ')
      .replace(/\s+/g, ' ')
      .trim();
  }

  function escapeHtml(value) {
    return String(value).replace(/[&<>"']/g, function (ch) {
      return { '&': '&amp;', '<': '&lt;', '>': '&gt;', '"': '&quot;', "'": '&#39;' }[ch];
    });
  }

  function iconSvg(kind) {
    if (kind === 'planet') {
      return '<svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="1.4"><circle cx="12" cy="12" r="7"/><ellipse cx="12" cy="12" rx="11" ry="4"/></svg>';
    }
    if (kind === 'star') {
      return '<svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="1.4"><path d="M12 2.5l2.6 7.4h7.4l-6 4.5 2.3 7.4-6.3-4.6-6.2 4.6 2.3-7.4-6-4.5h7.4z"/></svg>';
    }
    if (kind === 'blackhole') {
      return '<svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="1.4"><circle cx="12" cy="12" r="3.4"/><path d="M3 12c4-5 14-5 18 0"/><path d="M4.5 16.5c4.5-3 10-3 15 0"/></svg>';
    }
    if (kind === 'rocket') {
      return '<svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="1.4"><path d="M12 2c3.6 2.4 5 6 5 9.4L12 16l-5-4.6C7 8 8.4 4.4 12 2z"/><circle cx="12" cy="8.6" r="1.7"/><path d="M9 16.5L7 22l5-2.6L17 22l-2-5.5"/></svg>';
    }
    return '<svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="1.4"><path d="M12 3v18M3 12h18"/></svg>';
  }

  function scoreItem(item, terms) {
    var title = normalise(item.title);
    var desc = normalise(item.desc || '');
    var keys = normalise((item.keywords || []).join(' '));
    var cat = normalise(item.cat || '');
    var total = 0;
    for (var i = 0; i < terms.length; i++) {
      var t = terms[i];
      if (!t) continue;
      var hit = 0;
      if (title === t) hit += 14;
      else if (title.indexOf(t) === 0) hit += 10;
      else if (title.indexOf(t) > -1) hit += 7;
      if (keys.indexOf(t) > -1) hit += 4;
      if (desc.indexOf(t) > -1) hit += 2;
      if (cat.indexOf(t) > -1) hit += 1;
      if (!hit) return 0;
      total += hit;
    }
    return total;
  }

  function init() {
    var overlay = doc.getElementById('search');
    var input = doc.getElementById('searchInput');
    var results = doc.getElementById('searchResults');
    if (!overlay || !input || !results) return;

    var data = window.UE_SEARCH || [];
    var items = [];
    var active = -1;
    var lastFocus = null;
    var openers = doc.querySelectorAll('.js-search-open');

    function open() {
      lastFocus = doc.activeElement;
      overlay.classList.add('is-open');
      overlay.setAttribute('aria-hidden', 'false');
      doc.body.classList.add('search-open');
      window.setTimeout(function () {
        input.focus();
        input.select();
      }, 40);
    }

    function close() {
      overlay.classList.remove('is-open');
      overlay.setAttribute('aria-hidden', 'true');
      doc.body.classList.remove('search-open');
      if (lastFocus && lastFocus.focus) lastFocus.focus();
    }

    function hint() {
      var chips = ['Κρόνος', 'μαύρη τρύπα', 'James Webb', 'εξωπλανήτες', 'σκοτεινή ύλη', 'Voyager'];
      var html = '<div class="search__hint"><p>Δημοφιλείς αναζητήσεις</p><div class="search__chips">';
      chips.forEach(function (label) {
        html += '<button type="button" class="chip" data-q="' + escapeHtml(label) + '">' + escapeHtml(label) + '</button>';
      });
      html += '</div></div>';
      results.innerHTML = html;
    }

    function render() {
      var q = normalise(input.value);
      items = [];
      active = -1;
      if (!q) {
        hint();
        return;
      }
      var terms = q.split(' ');
      var found = [];
      data.forEach(function (item) {
        var s = scoreItem(item, terms);
        if (s > 0) found.push({ item: item, s: s });
      });
      found.sort(function (a, b) {
        return b.s - a.s;
      });
      items = found.slice(0, 15).map(function (r) {
        return r.item;
      });

      if (!items.length) {
        results.innerHTML = '<p class="search__empty">Δεν βρέθηκε τίποτα για «' + escapeHtml(input.value) + '».<br>Δοκίμασε «πλανήτες», «άστρα» ή «γαλαξίες».</p>';
        return;
      }

      var html = '';
      var lastCat = '';
      items.forEach(function (it) {
        if (it.cat !== lastCat) {
          html += '<p class="search__group">' + escapeHtml(it.cat) + '</p>';
          lastCat = it.cat;
        }
        html += '<a class="search-result" href="' + escapeHtml(it.url) + '">' +
          '<span class="search-result__icon">' + iconSvg(it.icon) + '</span>' +
          '<span><span class="search-result__title">' + escapeHtml(it.title) + '</span>' +
          '<span class="search-result__meta">' + escapeHtml(it.desc) + '</span></span>' +
          '<span class="search-result__cat">' + escapeHtml(it.cat) + '</span></a>';
      });
      results.innerHTML = html;
    }

    function move(delta) {
      var nodes = results.querySelectorAll('.search-result');
      if (!nodes.length) return;
      active = (active + delta + nodes.length) % nodes.length;
      for (var i = 0; i < nodes.length; i++) nodes[i].classList.toggle('is-active', i === active);
      nodes[active].scrollIntoView({ block: 'nearest' });
    }

    openers.forEach(function (btn) {
      btn.addEventListener('click', open);
    });

    doc.addEventListener('keydown', function (e) {
      var tag = (e.target.tagName || '').toLowerCase();
      var typing = tag === 'input' || tag === 'textarea' || e.target.isContentEditable;
      if ((e.key === 'k' || e.key === 'K') && (e.metaKey || e.ctrlKey)) {
        e.preventDefault();
        open();
        return;
      }
      if (e.key === '/' && !typing && !overlay.classList.contains('is-open')) {
        e.preventDefault();
        open();
        return;
      }
      if (!overlay.classList.contains('is-open')) return;
      if (e.key === 'Escape') {
        close();
      } else if (e.key === 'ArrowDown') {
        e.preventDefault();
        move(1);
      } else if (e.key === 'ArrowUp') {
        e.preventDefault();
        move(-1);
      } else if (e.key === 'Enter') {
        var nodes = results.querySelectorAll('.search-result');
        var target = nodes[active > -1 ? active : 0];
        if (target) {
          e.preventDefault();
          target.click();
        }
      }
    });

    input.addEventListener('input', render);
    results.addEventListener('click', function (e) {
      var chip = e.target.closest ? e.target.closest('[data-q]') : null;
      if (!chip) return;
      input.value = chip.getAttribute('data-q');
      render();
      input.focus();
    });

    overlay.addEventListener('click', function (e) {
      if (e.target === overlay) close();
    });
    var closeBtn = overlay.querySelector('.search__close');
    if (closeBtn) closeBtn.addEventListener('click', close);

    hint();
  }

  if (doc.readyState === 'loading') {
    doc.addEventListener('DOMContentLoaded', init);
  } else {
    init();
  }
})();
