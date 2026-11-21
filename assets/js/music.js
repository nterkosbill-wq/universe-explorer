/* Universe Explorer — ambient music player (generated with Web Audio, no files) */
(function () {
  'use strict';

  var doc = document;
  var STORAGE_VOLUME = 'ue-volume';
  var STORAGE_PANEL = 'ue-music-open';

  // Slow, cinematic pad progression in D minor (Hz).
  var CHORDS = [
    [146.83, 220.0, 293.66, 349.23, 440.0], // Dm(add9)
    [116.54, 174.61, 233.08, 293.66, 349.23], // Bb maj7
    [130.81, 196.0, 261.63, 329.63, 392.0], // C sus2
    [110.0, 164.81, 220.0, 261.63, 329.63], // Am7
    [87.31, 130.81, 174.61, 220.0, 261.63], // F maj
    [98.0, 146.83, 196.0, 246.94, 293.66] // G sus
  ];

  var state = {
    ctx: null,
    master: null,
    filter: null,
    voices: [],
    noise: null,
    chord: 0,
    timer: 0,
    playing: false
  };

  function init() {
    var panel = doc.getElementById('musicPlayer');
    var fab = doc.querySelector('.music-fab');
    var headerBtn = doc.querySelector('.js-music-toggle');
    if (!panel) return;

    var playBtn = panel.querySelector('.music__play');
    var closeBtn = panel.querySelector('.js-music-close');
    var range = panel.querySelector('input[type="range"]');
    var iconPlay = panel.querySelector('.icon-play');
    var iconPause = panel.querySelector('.icon-pause');

    var volume = 0.45;
    try {
      var saved = parseFloat(localStorage.getItem(STORAGE_VOLUME));
      if (!isNaN(saved)) volume = Math.min(1, Math.max(0, saved));
    } catch (err) {}
    if (range) range.value = String(Math.round(volume * 100));

    function openPanel(open) {
      panel.classList.toggle('is-open', open);
      panel.setAttribute('aria-hidden', open ? 'false' : 'true');
      if (open) {
        var first = panel.querySelector('button, input');
        if (first) first.focus();
      }
    }

    if (fab) {
      fab.addEventListener('click', function () {
        openPanel(true);
      });
    }
    if (headerBtn) {
      headerBtn.addEventListener('click', function () {
        openPanel(!panel.classList.contains('is-open'));
      });
    }
    if (closeBtn) closeBtn.addEventListener('click', function () {
      openPanel(false);
    });

    function buildAudio() {
      var Ctx = window.AudioContext || window.webkitAudioContext;
      if (!Ctx) return false;
      var ctx = new Ctx();
      var master = ctx.createGain();
      master.gain.value = 0;
      master.connect(ctx.destination);

      var filter = ctx.createBiquadFilter();
      filter.type = 'lowpass';
      filter.frequency.value = 1400;
      filter.Q.value = 0.6;
      filter.connect(master);

      // gentle space delay for depth
      var delay = ctx.createDelay(2.0);
      delay.delayTime.value = 0.42;
      var feedback = ctx.createGain();
      feedback.gain.value = 0.32;
      var wet = ctx.createGain();
      wet.gain.value = 0.25;
      filter.connect(delay);
      delay.connect(feedback);
      feedback.connect(delay);
      delay.connect(wet);
      wet.connect(master);

      // slow filter movement
      var lfo = ctx.createOscillator();
      var lfoGain = ctx.createGain();
      lfo.frequency.value = 0.055;
      lfoGain.gain.value = 420;
      lfo.connect(lfoGain);
      lfoGain.connect(filter.frequency);
      lfo.start();

      var voices = [];
      for (var i = 0; i < 5; i++) {
        var g = ctx.createGain();
        g.gain.value = 0;
        var osc = ctx.createOscillator();
        osc.type = i === 0 ? 'sine' : i > 3 ? 'triangle' : 'sine';
        osc.frequency.value = CHORDS[0][i];
        var detune = ctx.createOscillator();
        detune.frequency.value = 0.08 + i * 0.035;
        var detuneGain = ctx.createGain();
        detuneGain.gain.value = 2.6;
        detune.connect(detuneGain);
        detuneGain.connect(osc.detune);
        detune.start();
        osc.connect(g);
        g.connect(filter);
        osc.start();
        voices.push({ osc: osc, gain: g, note: CHORDS[0][i], level: i === 0 ? 0.22 : 0.14 });
      }

      // airy noise bed
      var len = ctx.sampleRate * 4;
      var buffer = ctx.createBuffer(1, len, ctx.sampleRate);
      var data = buffer.getChannelData(0);
      for (var n = 0; n < len; n++) data[n] = (Math.random() * 2 - 1) * 0.35;
      var noise = ctx.createBufferSource();
      noise.buffer = buffer;
      noise.loop = true;
      var noiseFilter = ctx.createBiquadFilter();
      noiseFilter.type = 'bandpass';
      noiseFilter.frequency.value = 520;
      noiseFilter.Q.value = 0.5;
      var noiseGain = ctx.createGain();
      noiseGain.gain.value = 0.05;
      noise.connect(noiseFilter);
      noiseFilter.connect(noiseGain);
      noiseGain.connect(filter);
      noise.start();

      state.ctx = ctx;
      state.master = master;
      state.filter = filter;
      state.voices = voices;
      state.noise = noise;
      applyVolume();
      return true;
    }

    function applyVolume() {
      if (!state.master || !state.ctx) return;
      var target = state.playing ? volume * 0.5 : 0;
      state.master.gain.cancelScheduledValues(state.ctx.currentTime);
      state.master.gain.setTargetAtTime(target, state.ctx.currentTime, 0.6);
    }

    function nextChord() {
      if (!state.ctx) return;
      state.chord = (state.chord + 1) % CHORDS.length;
      var now = state.ctx.currentTime;
      var chord = CHORDS[state.chord];
      state.voices.forEach(function (v, i) {
        var f = chord[i];
        v.osc.frequency.setTargetAtTime(f, now, 2.4);
        v.gain.gain.setTargetAtTime(v.level * (i === 4 ? 0.5 : 1), now, 2.4);
      });
    }

    function setPlaying(next) {
      if (!state.ctx) {
        if (!buildAudio()) return;
      }
      state.playing = next;
      if (next) {
        if (state.ctx.state === 'suspended') state.ctx.resume();
        applyVolume();
        if (!state.timer) state.timer = window.setInterval(nextChord, 15000);
      } else {
        applyVolume();
        window.clearInterval(state.timer);
        state.timer = 0;
      }
      panel.classList.toggle('is-playing', next);
      if (iconPlay) iconPlay.hidden = next;
      if (iconPause) iconPause.hidden = !next;
      if (playBtn) {
        playBtn.setAttribute('aria-pressed', String(next));
        playBtn.setAttribute('aria-label', next ? 'Παύση μουσικής' : 'Αναπαραγωγή μουσικής');
      }
      if (headerBtn) headerBtn.classList.toggle('is-on', next);
      if (fab) fab.classList.toggle('is-playing', next);
    }

    if (playBtn) {
      playBtn.addEventListener('click', function () {
        setPlaying(!state.playing);
      });
    }

    if (range) {
      range.addEventListener('input', function () {
        volume = Math.min(1, Math.max(0, parseFloat(range.value) / 100));
        applyVolume();
        try {
          localStorage.setItem(STORAGE_VOLUME, String(volume));
        } catch (err) {}
      });
    }

    doc.addEventListener('visibilitychange', function () {
      if (!state.ctx) return;
      if (doc.hidden && state.playing) {
        state.ctx.suspend();
      } else if (!doc.hidden && state.playing) {
        state.ctx.resume();
      }
    });

    var wantOpen = false;
    try {
      wantOpen = localStorage.getItem(STORAGE_PANEL) === '1';
    } catch (err) {}
    if (wantOpen) openPanel(true);

    panel.addEventListener('click', function (e) {
      if (e.target === panel) openPanel(false);
    });
  }

  if (doc.readyState === 'loading') {
    doc.addEventListener('DOMContentLoaded', init);
  } else {
    init();
  }
})();
