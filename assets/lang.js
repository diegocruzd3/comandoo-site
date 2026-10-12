/* Faixa discreta de idioma: oferece a versão no idioma do navegador, sem redirecionar. */
(function () {
  var KEY = 'comandoo-lang-ok';
  function get() { try { return localStorage.getItem(KEY); } catch (e) { return null; } }
  function put() { try { localStorage.setItem(KEY, '1'); } catch (e) {} }
  document.querySelectorAll('.seg a').forEach(function (a) { a.addEventListener('click', put); });
  if (get()) return;
  var page = (document.documentElement.lang || 'pt').slice(0, 2).toLowerCase();
  var langs = navigator.languages && navigator.languages.length ? navigator.languages : [navigator.language || ''];
  var want = null;
  for (var i = 0; i < langs.length; i++) {
    var l = String(langs[i]).slice(0, 2).toLowerCase();
    if (l === 'pt' || l === 'en' || l === 'es') { want = l; break; }
  }
  if (!want || want === page) return;
  var alt = null;
  document.querySelectorAll('link[rel="alternate"][hreflang]').forEach(function (k) {
    if (k.getAttribute('hreflang').slice(0, 2).toLowerCase() === want && !alt) alt = k.getAttribute('href');
  });
  if (!alt) return;
  var T = { en: ['This page is also in English.', 'Read in English', 'Close'],
            es: ['Esta página también está en español.', 'Leer en español', 'Cerrar'],
            pt: ['Esta página também está em português.', 'Ler em português', 'Fechar'] }[want];
  var bar = document.createElement('div');
  bar.className = 'langbar'; bar.setAttribute('lang', want); bar.setAttribute('role', 'region'); bar.setAttribute('aria-label', T[1]);
  bar.innerHTML = '<span></span><a></a><button type="button">×</button>';
  bar.querySelector('span').textContent = T[0];
  var a = bar.querySelector('a'); a.textContent = T[1]; a.href = alt.replace(/^https:\/\/comandoo\.online/, ''); a.setAttribute('hreflang', want);
  a.addEventListener('click', put);
  var b = bar.querySelector('button'); b.setAttribute('aria-label', T[2]);
  b.addEventListener('click', function () { put(); bar.remove(); });
  document.body.insertBefore(bar, document.body.firstChild);
})();
