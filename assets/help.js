/* Central de ajuda: diagnóstico guiado (aparelho × problema). Dados gerados de compat.json + faq.json. */
(function () {
  var el = document.getElementById('help-data');
  if (!el) return;
  var D = JSON.parse(el.textContent), out = document.getElementById('resultado');
  var form = document.getElementById('diagnostico');

  function val(name) { var c = form.querySelector('input[name="' + name + '"]:checked'); return c ? c.value : null; }
  function set(name, v) { var c = form.querySelector('input[name="' + name + '"][value="' + v + '"]'); if (c) c.checked = true; }

  function render(scroll) {
    var m = val('marca'), p = val('problema');
    if (!m || !p || !D.d[m] || !D.d[m][p]) { out.innerHTML = '<p class="hint-r">' + D.s.pick + '</p>'; return; }
    var steps = D.d[m][p];
    var html = '<h3>' + D.s.result_h + '</h3><p class="ctx">' + D.n[m] + ' · ' + D.p[p] + '</p><ol class="rsteps">';
    steps.forEach(function (s) { html += '<li><b>' + s.t + '</b>' + s.h + '</li>'; });
    html += '</ol><button type="button" class="rcopy">' + D.s.copy + '</button>';
    out.innerHTML = html;
    var url = location.pathname + '?marca=' + encodeURIComponent(m) + '&problema=' + encodeURIComponent(p) + '#diagnostico';
    try { history.replaceState(null, '', url); } catch (e) {}
    out.querySelector('.rcopy').addEventListener('click', function (ev) {
      var b = ev.currentTarget, link = location.origin + url;
      var done = function () { b.textContent = D.s.copied; };
      if (navigator.clipboard) navigator.clipboard.writeText(link).then(done, function () {}); else done();
    });
    if (scroll) out.scrollIntoView({ block: 'start', behavior: matchMedia('(prefers-reduced-motion: reduce)').matches ? 'auto' : 'smooth' });
  }

  form.addEventListener('change', function (e) {
    var both = val('marca') && val('problema');
    render(both && e.target.name === 'problema');
  });

  var q = new URLSearchParams(location.search);
  if (q.get('marca')) set('marca', q.get('marca'));
  if (q.get('problema')) set('problema', q.get('problema'));
  render(false);

  // Pergunta do FAQ aberta pelo link (#id)
  function openHash() {
    var id = decodeURIComponent(location.hash.slice(1));
    var d = id && document.getElementById(id);
    if (d && d.tagName === 'DETAILS') { d.open = true; d.scrollIntoView({ block: 'start' }); }
  }
  window.addEventListener('hashchange', openHash);
  openHash();
})();
