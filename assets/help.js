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
    html += '<div class="solved"><p class="solved-q">' + D.s.solved_q + '</p><div class="solved-b">'
      + '<button type="button" data-v="1" aria-pressed="false">' + D.s.yes + '</button>'
      + '<button type="button" data-v="0" aria-pressed="false">' + D.s.no + '</button></div>'
      + '<p class="solved-msg" aria-live="polite"></p></div>';
    out.innerHTML = html;
    var url = location.pathname + '?marca=' + encodeURIComponent(m) + '&problema=' + encodeURIComponent(p) + '#diagnostico';
    var msg = out.querySelector('.solved-msg');
    out.querySelectorAll('.solved-b button').forEach(function (b) {
      b.addEventListener('click', function () {
        out.querySelectorAll('.solved-b button').forEach(function (x) { x.setAttribute('aria-pressed', x === b ? 'true' : 'false'); });
        if (b.getAttribute('data-v') === '1') { msg.textContent = D.s.solved_yes; return; }
        var subj = D.s.mail_subj.replace('{b}', D.n[m]).replace('{p}', D.p[p]);
        var href = 'mailto:' + D.s.mail + '?subject=' + encodeURIComponent(subj) + '&body=' + encodeURIComponent(location.origin + url);
        var parts = D.s.solved_no.split('{mail}');
        msg.textContent = parts[0];
        var a = document.createElement('a'); a.href = href; a.textContent = D.s.mail; msg.appendChild(a);
        msg.appendChild(document.createTextNode(parts[1] || ''));
      });
    });
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

  // Busca nas respostas: filtra os resultados do Testar conexão e as perguntas enquanto a pessoa digita
  var box = document.getElementById('buscar'), q = document.getElementById('q'), st = document.getElementById('qstatus');
  if (!box || !q) return;
  box.hidden = false;
  function norm(t) { return t.normalize('NFD').replace(/[\u0300-\u036f]/g, '').toLowerCase(); }
  var items = [].slice.call(document.querySelectorAll('.faqall details')).map(function (d) { return { d: d, t: norm(d.textContent) }; });
  var groups = [].slice.call(document.querySelectorAll('.faqall .fsec, #testar-conexao'));
  var timer;
  function filter() {
    var v = norm(q.value.trim()), words = v.split(/\s+/).filter(Boolean), n = 0;
    items.forEach(function (it) {
      var ok = !words.length || words.every(function (w) { return it.t.indexOf(w) !== -1; });
      it.d.hidden = !ok; if (ok) n++;
    });
    groups.forEach(function (g) { g.hidden = words.length > 0 && !g.querySelector('details:not([hidden])'); });
    var lead = document.querySelector('#perguntas > p'); if (lead) lead.hidden = words.length > 0;
    if (!words.length) { st.textContent = ''; return; }
    if (!n) { st.textContent = D.s.search_none.replace('{q}', q.value.trim()); return; }
    st.textContent = n === 1 ? D.s.search_1 : D.s.search_n.replace('{n}', n);
    if (n <= 3) items.forEach(function (it) { if (!it.d.hidden) it.d.open = true; });
  }
  q.addEventListener('input', function () { clearTimeout(timer); timer = setTimeout(filter, 120); });
})();
