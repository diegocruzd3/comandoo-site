/* Comandoo — o site é um controle remoto.
   1) O celular do topo controla a TV desenhada ao lado.
   2) O botão flutuante (igual ao do app) controla a própria página como se fosse uma TV. */
(function () {
  var calm = window.matchMedia && matchMedia('(prefers-reduced-motion: reduce)').matches;
  function buzz() { try { if (navigator.vibrate) navigator.vibrate(8); } catch (e) {} }
  function flash(btn) {
    if (!btn) return;
    btn.classList.add('hit');
    setTimeout(function () { btn.classList.remove('hit'); }, 150);
  }

  /* ───────── 1. Celular → TV ───────── */
  var stage = document.getElementById('stage');
  if (stage) {
    var S = JSON.parse(stage.getAttribute('data-s'));
    var tv = document.getElementById('tv');
    var tiles = stage.querySelectorAll('.tile');
    var osd = stage.querySelector('.osd');
    var vbar = stage.querySelector('.vbar'), vfill = vbar.querySelector('i');
    var vnum = stage.querySelector('.vnum'), vtxt = vnum.querySelector('em'), vtrack = vnum.querySelector('.vtrack i');
    var app = document.getElementById('tvapp'), search = document.getElementById('tvsearch');
    var chip = stage.querySelector('.chip'), muteBtn = stage.querySelector('.mute');
    var cols = 3, idx = 0, vol = 12, muted = false, on = false, opened = false, touched = false;
    var inputs = ['HDMI 1', 'HDMI 2', 'TV'], inputIdx = 0, osdT, volT, typeT;

    function say(msg) {
      osd.textContent = msg; osd.classList.add('on');
      clearTimeout(osdT); osdT = setTimeout(function () { osd.classList.remove('on'); }, 1500);
    }
    function focusTile(i) { tiles[idx].removeAttribute('data-focus'); idx = i; tiles[idx].setAttribute('data-focus', ''); }
    function paintVol() {
      vtxt.textContent = muted ? '—' : vol;
      vtrack.style.width = (muted ? 0 : vol) + '%';
      vnum.classList.toggle('muted', muted);
      muteBtn.classList.toggle('on', muted);
      vfill.style.height = (muted ? 0 : vol) + '%';
      vbar.classList.add('on'); clearTimeout(volT);
      volT = setTimeout(function () { vbar.classList.remove('on'); }, 1200);
    }
    function closeApp() { app.classList.remove('on'); opened = false; }
    function power(want) {
      on = (want === undefined) ? !on : want;
      chip.classList.toggle('is-off', !on);
      if (on) {
        tv.classList.remove('off', 'shutting'); tv.classList.add('booting');
        setTimeout(function () { tv.classList.remove('booting'); }, 600);
      } else {
        closeApp(); search.classList.remove('on');
        tv.classList.add('shutting');
        setTimeout(function () { tv.classList.add('off'); tv.classList.remove('shutting'); }, calm ? 0 : 400);
      }
    }
    function voice() {
      var q = S.voice, i = 0, box = search.querySelector('.q');
      clearInterval(typeT); box.textContent = ''; search.classList.add('on');
      typeT = setInterval(function () {
        box.textContent = q.slice(0, ++i);
        if (i >= q.length) {
          clearInterval(typeT);
          setTimeout(function () { search.classList.remove('on'); focusTile(0); say(S.o_ok + ' ' + q); }, 900);
        }
      }, calm ? 0 : 55);
    }

    function press(k) {
      if (k === 'power') { power(); return; }
      if (!on) { if (k !== 'chip') power(true); return; }
      var r = Math.floor(idx / cols), c = idx % cols, rows = Math.ceil(tiles.length / cols);
      switch (k) {
        case 'up': if (!opened && r > 0) focusTile(idx - cols); break;
        case 'down': if (!opened && r < rows - 1) focusTile(idx + cols); break;
        case 'left': if (!opened && c > 0) focusTile(idx - 1); break;
        case 'right': if (!opened && c < cols - 1) focusTile(idx + 1); break;
        case 'ok':
          if (opened) break;
          var t = tiles[idx];
          app.style.background = getComputedStyle(t).backgroundImage;
          app.querySelector('b').textContent = t.textContent;
          app.querySelector('span').textContent = S.app_sub;
          app.classList.add('on'); opened = true; break;
        case 'back': if (opened) closeApp(); else say(S.o_back); break;
        case 'home': closeApp(); focusTile(0); say(S.o_home); break;
        case 'input': inputIdx = (inputIdx + 1) % inputs.length; say(S.o_input + ': ' + inputs[inputIdx]); break;
        case 'mute': muted = !muted; paintVol(); say(muted ? S.o_mute : S.o_unmute); break;
        case 'vup': muted = false; vol = Math.min(100, vol + 2); paintVol(); break;
        case 'vdown': muted = false; vol = Math.max(0, vol - 2); paintVol(); break;
        case 'mic': voice(); break;
        case 'chip': say(chip.textContent.trim()); break;
      }
    }

    stage.addEventListener('click', function (e) {
      var b = e.target.closest('[data-tv]');
      if (!b) return;
      touched = true; buzz(); flash(b); press(b.getAttribute('data-tv'));
    });
    focusTile(0);

    // Abertura: o celular "aponta", sai o sinal e a TV liga. Depois, uma navegação curta sozinha.
    if (calm) { power(true); }
    else {
      setTimeout(function () {
        stage.classList.add('go');
        flash(stage.querySelector('[data-tv="power"]'));
        setTimeout(function () { power(true); }, 380);
        var seq = ['right', 'right', 'down', 'ok', 'back'], i = 0;
        setTimeout(function step() {
          if (touched || i >= seq.length) return;
          var k = seq[i++]; flash(stage.querySelector('[data-tv="' + k + '"]')); press(k);
          setTimeout(step, k === 'ok' ? 1100 : 520);
        }, 1500);
      }, 500);
    }
  }

  /* ───────── 2. Botão flutuante → a página vira TV ───────── */
  var fab = document.getElementById('fab'), fabBtn = document.getElementById('fabbtn');
  var bubble = document.getElementById('bubble'), rc = document.getElementById('minirc');
  var blackout = document.getElementById('blackout');
  if (!fab) return;
  var cur = null, isOpen = false, bubbled = false;
  var bandEl = document.querySelector('.band');

  // Aparece quando o topo sai da tela (como o botão flutuante do app, que fica por cima de tudo).
  if ('IntersectionObserver' in window) {
    new IntersectionObserver(function (es) {
      var away = !es[0].isIntersecting;
      fab.classList.toggle('show', away || isOpen);
      if (away && !bubbled) {
        bubbled = true;
        bubble.classList.add('on');
        setTimeout(function () { bubble.classList.remove('on'); }, 6000);
      }
    }, { threshold: 0.05 }).observe(document.querySelector('.hero'));
  } else { fab.classList.add('show'); }

  function setOpen(v) {
    isOpen = v;
    fab.classList.toggle('open', v);
    fabBtn.setAttribute('aria-expanded', v);
    fabBtn.setAttribute('aria-label', fabBtn.getAttribute(v ? 'data-close' : 'data-open'));
    bubble.classList.remove('on');
    if (!v) mark(null);
    else if (!cur) mark(firstVisible(), true);
  }
  fabBtn.addEventListener('click', function () { buzz(); setOpen(!isOpen); });

  function items() {
    return Array.prototype.filter.call(document.querySelectorAll('[data-nav]'), function (el) {
      return el.offsetParent !== null || el.getClientRects().length;
    });
  }
  function firstVisible() {
    var list = items(), h = innerHeight;
    for (var i = 0; i < list.length; i++) {
      var r = list[i].getBoundingClientRect();
      if (r.top >= 0 && r.bottom <= h) return list[i];
    }
    return list[0];
  }
  function mark(el, quiet) {
    if (cur) cur.classList.remove('rc-target');
    cur = el;
    if (!el) return;
    el.classList.add('rc-target');
    try { el.focus({ preventScroll: true }); } catch (e) { el.focus(); }
    // Deixa o item escolhido na parte da tela que o controle não cobre.
    var r = el.getBoundingClientRect(), zone = innerHeight;
    if (isOpen && innerWidth < 760) zone = rc.getBoundingClientRect().top - 12;
    if (quiet && r.top >= 12 && r.bottom <= zone) return;
    var y = scrollY + r.top - Math.max(16, (zone - r.height) / 2);
    scrollTo({ top: Math.max(0, y), behavior: calm ? 'auto' : 'smooth' });
  }
  function center(r) { return { x: r.left + r.width / 2, y: r.top + r.height / 2 }; }
  function move(dir) {
    if (!cur) { mark(firstVisible()); return; }
    var a = cur.getBoundingClientRect(), ca = center(a), best = null, bestScore = Infinity;
    items().forEach(function (el) {
      if (el === cur) return;
      var b = el.getBoundingClientRect(), cb = center(b);
      var dx = cb.x - ca.x, dy = cb.y - ca.y, s;
      if (dir === 'down') { if (b.top < a.bottom - 4 && dy <= 8) return; s = Math.max(dy, 1) + Math.abs(dx) * 2; }
      else if (dir === 'up') { if (b.bottom > a.top + 4 && dy >= -8) return; s = Math.max(-dy, 1) + Math.abs(dx) * 2; }
      else if (dir === 'right') { if (dx <= 8 || Math.abs(dy) > Math.max(a.height, b.height)) return; s = dx + Math.abs(dy) * 3; }
      else { if (dx >= -8 || Math.abs(dy) > Math.max(a.height, b.height)) return; s = -dx + Math.abs(dy) * 3; }
      if (s < bestScore) { bestScore = s; best = el; }
    });
    if (best) mark(best);
    else if (dir === 'down' || dir === 'up') scrollBy({ top: (dir === 'down' ? 1 : -1) * innerHeight * 0.5, behavior: calm ? 'auto' : 'smooth' });
  }
  function sections() { return [bandEl].concat(Array.prototype.slice.call(document.querySelectorAll('main section, .closing'))); }
  function jump(step) {
    var list = sections(), y = cur ? cur.getBoundingClientRect().top : 0, at = 0;
    list.forEach(function (s, i) { if (s.getBoundingClientRect().top <= y + 1) at = i; });
    var target = list[Math.max(0, Math.min(list.length - 1, at + step))];
    var first = target.querySelector('[data-nav]');
    if (first) mark(first);
    else target.scrollIntoView({ behavior: calm ? 'auto' : 'smooth' });
  }
  function ok() {
    if (!cur) return;
    if (cur.matches('a, summary, button')) { cur.click(); return; }
    cur.animate && !calm && cur.animate([{ transform: 'scale(1)' }, { transform: 'scale(.97)' }, { transform: 'scale(1)' }], { duration: 220 });
  }
  function back() {
    var d = cur && cur.closest('details');
    if (d && d.open) { d.open = false; return; }
    mark(document.querySelector('[data-nav]'));
  }

  // Desligar o site, como um CRT.
  function pageOff() {
    setOpen(false);
    document.body.classList.remove('page-on');
    document.body.classList.add('page-off');
    setTimeout(function () { blackout.classList.add('on'); document.getElementById('wake').focus(); }, calm ? 0 : 420);
  }
  function pageOn() {
    blackout.classList.remove('on');
    document.body.classList.remove('page-off');
    document.body.classList.add('page-on');
    setTimeout(function () { document.body.classList.remove('page-on'); fabBtn.focus(); }, 650);
  }
  document.getElementById('wake').addEventListener('click', function () { buzz(); pageOn(); });
  document.addEventListener('keydown', function (e) {
    if (blackout.classList.contains('on') && (e.key === 'Enter' || e.key === ' ' || e.key === 'Escape')) { e.preventDefault(); pageOn(); }
  });

  function rcPress(k) {
    switch (k) {
      case 'up': case 'down': case 'left': case 'right': move(k); break;
      case 'ok': ok(); break;
      case 'back': back(); break;
      case 'prev': jump(-1); break;
      case 'next': jump(1); break;
      case 'power': pageOff(); break;
    }
  }
  rc.addEventListener('click', function (e) {
    var b = e.target.closest('[data-rc]');
    if (!b) return;
    buzz(); flash(b); rcPress(b.getAttribute('data-rc'));
  });

  // Com o controle aberto, as setas do teclado também navegam pela página.
  var keymap = { ArrowUp: 'up', ArrowDown: 'down', ArrowLeft: 'left', ArrowRight: 'right', PageUp: 'prev', PageDown: 'next' };
  document.addEventListener('keydown', function (e) {
    if (!isOpen || e.altKey || e.ctrlKey || e.metaKey) return;
    if (e.key === 'Escape') { setOpen(false); fabBtn.focus(); return; }
    var k = keymap[e.key];
    if (!k) return;
    e.preventDefault();
    flash(rc.querySelector('[data-rc="' + k + '"]'));
    rcPress(k);
  });
  document.addEventListener('focusin', function (e) {
    if (cur && e.target !== cur && !rc.contains(e.target) && e.target !== fabBtn) { cur.classList.remove('rc-target'); cur = null; }
  });

  // A variação "Apontando" pulsa o sinal quando o fim da página aparece.
  var closing = document.getElementById('closing');
  if (closing && 'IntersectionObserver' in window) {
    var io = new IntersectionObserver(function (es) {
      if (es[0].isIntersecting) { closing.classList.add('seen'); io.disconnect(); }
    }, { threshold: 0.4 });
    io.observe(closing);
  }
})();
