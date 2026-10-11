(function () {
  var demo = document.getElementById('demo');
  if (!demo) return;
  var tiles = demo.querySelectorAll('.tile');
  var toast = demo.querySelector('.toast');
  var vol = demo.querySelector('.vol');
  var volFill = vol.querySelector('i');
  var t = demo.dataset;
  var cols = 3, idx = 0, level = 40, toastT, volT, touched = false;

  function focus(i) {
    tiles[idx].removeAttribute('data-focus');
    idx = i;
    tiles[idx].setAttribute('data-focus', '');
  }
  function say(msg) {
    toast.textContent = msg;
    toast.classList.add('on');
    clearTimeout(toastT);
    toastT = setTimeout(function () { toast.classList.remove('on'); }, 1400);
  }
  function showVol() {
    volFill.style.height = level + '%';
    vol.classList.add('on');
    clearTimeout(volT);
    volT = setTimeout(function () { vol.classList.remove('on'); }, 1200);
  }
  function flash(k) {
    var b = demo.querySelector('[data-k="' + k + '"]');
    if (!b) return;
    b.classList.add('hit');
    setTimeout(function () { b.classList.remove('hit'); }, 160);
  }
  function press(k) {
    var r = Math.floor(idx / cols), c = idx % cols, rows = Math.ceil(tiles.length / cols);
    flash(k);
    if (k === 'up' && r > 0) focus(idx - cols);
    else if (k === 'down' && r < rows - 1) focus(idx + cols);
    else if (k === 'left' && c > 0) focus(idx - 1);
    else if (k === 'right' && c < cols - 1) focus(idx + 1);
    else if (k === 'ok') say(t.open + ' ' + tiles[idx].textContent.trim());
    else if (k === 'volup') { level = Math.min(100, level + 10); showVol(); }
    else if (k === 'voldown') { level = Math.max(0, level - 10); showVol(); }
    else if (k === 'home') { focus(0); say(t.home); }
  }

  demo.addEventListener('click', function (e) {
    var b = e.target.closest('[data-k]');
    if (!b) return;
    touched = true;
    press(b.dataset.k);
  });
  var map = { ArrowUp: 'up', ArrowDown: 'down', ArrowLeft: 'left', ArrowRight: 'right', Enter: 'ok', ' ': 'ok' };
  demo.addEventListener('keydown', function (e) {
    var k = map[e.key];
    if (!k) return;
    if (e.target.matches('button') && (e.key === 'Enter' || e.key === ' ')) return;
    e.preventDefault();
    touched = true;
    press(k);
  });

  focus(0);

  // One short self-demo on load, skipped if the visitor prefers less motion or touches the remote first.
  var calm = window.matchMedia && window.matchMedia('(prefers-reduced-motion: reduce)').matches;
  if (calm) return;
  var seq = ['right', 'right', 'down', 'ok'], i = 0;
  setTimeout(function step() {
    if (touched || i >= seq.length) return;
    press(seq[i++]);
    setTimeout(step, 650);
  }, 1200);
})();
