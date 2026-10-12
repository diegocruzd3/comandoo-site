/* Aviso de lançamento: envia o e-mail para a função comandoo_waitlist_join no Supabase do app. */
(function () {
  var RX = /^[^@\s]+@[^@\s]+\.[^@\s]+$/;
  document.querySelectorAll('form.wl').forEach(function (f) {
    var M = JSON.parse(f.getAttribute('data-m')), inp = f.querySelector('input[name="email"]'),
        hp = f.querySelector('.wl-hp'), btn = f.querySelector('button'), msg = f.querySelector('.wl-msg');
    function say(t, kind) { msg.textContent = t; f.setAttribute('data-state', kind || ''); }
    f.addEventListener('submit', function (e) {
      e.preventDefault();
      var v = inp.value.trim();
      if (hp.value) { say(M.ok.replace('{e}', v), 'ok'); return; }
      if (!RX.test(v) || v.length > 254) { say(M.bad, 'bad'); inp.setAttribute('aria-invalid', 'true'); inp.focus(); return; }
      inp.removeAttribute('aria-invalid'); btn.disabled = true; say(M.wait, 'wait');
      fetch(f.getAttribute('data-api'), {
        method: 'POST',
        headers: { 'Content-Type': 'application/json', apikey: f.getAttribute('data-key') },
        body: JSON.stringify({ p_email: v, p_lang: f.getAttribute('data-lang'), p_source: location.pathname })
      }).then(function (r) {
        btn.disabled = false;
        if (r.ok) { say(M.ok.replace('{e}', v), 'ok'); f.classList.add('wl-done'); return; }
        return r.json().catch(function () { return {}; }).then(function (j) {
          if (j && /invalid_email/.test(j.message || '')) say(M.bad, 'bad'); else say(M.err, 'err');
        });
      }, function () { btn.disabled = false; say(M.err, 'err'); });
    });
  });
})();
