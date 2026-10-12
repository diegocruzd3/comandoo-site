/* Guias: marca no índice lateral a seção que está na tela. */
(function () {
  var links = document.querySelectorAll('.gside ol a');
  if (!links.length || !('IntersectionObserver' in window)) return;
  var map = {}, cur = null;
  links.forEach(function (a) { var t = document.getElementById(a.getAttribute('href').slice(1)); if (t) map[t.id] = a; });
  var io = new IntersectionObserver(function (es) {
    es.forEach(function (e) {
      if (!e.isIntersecting) return;
      if (cur) cur.removeAttribute('aria-current');
      cur = map[e.target.id]; if (cur) cur.setAttribute('aria-current', 'true');
    });
  }, { rootMargin: '0px 0px -60% 0px' });
  Object.keys(map).forEach(function (id) { io.observe(document.getElementById(id)); });
})();
