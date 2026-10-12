#!/usr/bin/env python3
"""Manual do Comandoo: gera /guias, /en/guides, /es/guias, /changelog, sitemap.xml e robots.txt.

Uso: python3 tools/guides.py   (depois de tools/build.py)

Fontes de verdade, nesta ordem:
  1. compat.json do repositório controley-releases (branch main): marcas, status e passos.
  2. faq.json do mesmo repositório: respostas oficiais e nomes de botões.
  3. Capturas reais do app em assets/guias/{nome}-{pt|en|es}.png|jpg (nunca imagem inventada).
     Captura que ainda não existe simplesmente não aparece na página.

Manutenção: a cada versão nova do app, atualize APP_VERSION e UPDATED, revise os guias
afetados em guides_content.py, acrescente a versão em tools/changelog.json e rode este script.
"""
import html
import json
import re
import subprocess
import sys
import urllib.request
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))
import build as B  # noqa: E402
import guides_content as C  # noqa: E402

ROOT = B.ROOT
SITE = B.SITE
UPDATED = '2026-10-12'
APP_VERSION = '1.24.8'
RELEASES = Path('/home/claude/diegocruzd3/controley-releases')
RAW = 'https://raw.githubusercontent.com/diegocruzd3/controley-releases/main/'
LI = {'pt': 0, 'en': 1, 'es': 2}
SUF = {'pt': '', 'en': '_en', 'es': '_es'}
MONTHS = ['Jan', 'Feb', 'Mar', 'Apr', 'May', 'Jun', 'Jul', 'Aug', 'Sep', 'Oct', 'Nov', 'Dec']


# ── Fontes ────────────────────────────────────────────────────────────────
def load(name):
    try:
        subprocess.run(['git', '-C', str(RELEASES), 'pull', '-q'], check=False, timeout=60)
        return json.loads((RELEASES / name).read_text(encoding='utf-8'))
    except Exception:
        with urllib.request.urlopen(RAW + name, timeout=30) as r:
            return json.loads(r.read().decode('utf-8'))


def fix_name(s):
    # As fontes ainda dizem Controley (nome antigo); o site usa sempre Comandoo.
    return s.replace('Controley', 'Comandoo')


COMPAT = load('compat.json')
FAQ = {i['id']: i for i in load('faq.json')['items']}
BRAND = {b['id']: b for b in COMPAT['brands']}


# O FAQ do app ainda usa nomes antigos de botões; o site usa o texto que aparece na tela (capturas 1.24.6).
# Caminhos corrigidos conforme o código da 1.24.8 (respostas do Grok, 12/10/2026): Ajuda e suporte fica na aba Mais.
LABEL_FIX = {
    'pt': [('Conectar pelo IP', 'Usar IP'), ('(ou em Ajustes, Ajuda e suporte)', '(ou na aba Mais, em Ajuda e suporte)'),
           ('Em Ajustes, toque em Relatar um problema', 'Na aba Mais, abra Ajuda e suporte e toque em Relatar um problema')],
    'en': [('Connect by IP', 'Use IP'), ('(or Settings, Help and support)', '(or the More tab, Help and support)'),
           ('In Settings, tap Report a problem', 'In the More tab, open Help and support and tap Report a problem')],
    'es': [('Conectar por IP', 'Usar IP'), ('(o Ajustes, Ayuda y soporte)', '(o la pestaña Más, Ayuda y soporte)'),
           ('En Ajustes, toca Reportar un problema', 'En la pestaña Más, abre Ayuda y soporte y toca Reportar un problema')],
}


def fq(fid, lang):
    i = FAQ[fid]
    play = i.get('play') or {}  # a versão Play mostra a variante "play" quando existe
    q = fix_name(play.get('q' + SUF[lang]) or i['q' + SUF[lang]])
    a = fix_name(play.get('a' + SUF[lang]) or i['a' + SUF[lang]])
    for old, new in LABEL_FIX[lang]:
        q, a = q.replace(old, new), a.replace(old, new)
    return q, '<p>' + html.escape(a) + '</p>'


def esc(s):
    return html.escape(s, quote=True)


def plain(b, n=320):
    t = re.sub(r'<table.*?</table>|<div class="tip.*?</div>', ' ', b, flags=re.S)
    t = html.unescape(re.sub(r'<[^>]+>', ' ', t))
    t = re.sub(r'\s+', ' ', t).strip()
    t = re.sub(r'\s+([.,:;])', r'\1', t)
    return t if len(t) <= n else t[:n].rsplit(' ', 1)[0] + '…'


def url(aid, lang, absolute=False):
    base = C.UI[lang]['guides'] + C.SLUGS[aid][LI[lang]] + '/'
    return SITE + base if absolute else base


def links(s, lang):
    s = s.replace('{KB}', C.KEYBOARD_TAB[lang]).replace('{SEND_LG}', C.SEND_BTN_LG[lang]).replace('{SEND}', C.SEND_BTN[lang])
    for aid in C.SLUGS:
        s = s.replace('{' + aid + '}', url(aid, lang))
    return s


def fdate(d, lang):
    y, m, dd = d.split('-')
    return C.UI[lang]['date_fmt'].format(d=dd, m=m, y=y, mon=MONTHS[int(m) - 1])


# Capturas feitas em simulação (aparelho de exemplo): levam a marcação de imagem ilustrativa.
ILLUSTRATIVE = {'lista-de-tvs', 'tela-controle'}
ILLU_LABEL = {'pt': 'Imagem ilustrativa', 'en': 'Illustrative image', 'es': 'Imagen ilustrativa'}


def shot(base, alt, caption, lang):
    if base in ILLUSTRATIVE:
        caption = f'{caption} · {ILLU_LABEL[lang]}'
    for ext in ('png', 'jpg', 'webp'):
        f = ROOT / 'assets' / 'guias' / f'{base}-{lang}.{ext}'
        if f.exists():
            wide = ' wide' if ext == 'jpg' else ''
            from PIL import Image
            w, h = Image.open(f).size
            return (f'<figure class="shot{wide}"><a href="/assets/guias/{f.name}" target="_blank" rel="noopener"><img src="/assets/guias/{f.name}" alt="{esc(alt)}" width="{w}" height="{h}" loading="lazy" decoding="async"></a>'
                    f'<figcaption>{caption}</figcaption></figure>')
    return ''


def pair_table(lang):
    h1, h2, rows = C.PAIR[lang]
    body = ''.join(f'<tr><td>{a}</td><td>{b}</td></tr>' for a, b in rows)
    return f'<div class="tablewrap"><table class="pair"><thead><tr><th scope="col">{h1}</th><th scope="col">{h2}</th></tr></thead><tbody>{body}</tbody></table></div>'


# ── Normalização de artigos ───────────────────────────────────────────────
def norm_steps(raw, lang):
    out = []
    for s in raw or []:
        if s == 'INSTALL':
            h, b = C.INSTALL[lang]; out.append((h, b, None))
        elif s == 'OPEN_PICK':
            h, b = C.OPEN_PICK[lang]; out.append((h, b, None))
        else:
            h, b, sh = s
            h = links(h, lang)
            sh = tuple(links(x, lang) for x in sh) if sh else None
            out.append((h, links(b.replace('PAIR', pair_table(lang)), lang), sh))
    return out


def norm_qa(raw, lang):
    out = []
    for x in raw or []:
        if isinstance(x, str) and x.startswith('FAQ:'):
            out.append(fq(x[4:], lang))
        elif x in ('FREE', 'IPHONE', 'NO_4G'):
            q, a = getattr(C, x)[lang]; out.append((q, f'<p>{a}</p>'))
        else:
            q, a = x
            out.append((q, links(a if a.startswith('<') else f'<p>{a}</p>', lang)))
    return out


def article(aid, lang):
    """Devolve o artigo pronto para renderizar, venha ele de texto à mão ou do compat.json."""
    if aid in C.ARTICLES:
        A = C.ARTICLES[aid]; t = A[lang]
        return dict(id=aid, read=A['read'], howto=A.get('howto'), time=A.get('time'), related=A['related'],
                    seo_title=t['seo_title'], desc=links(t['desc'], lang), h1=links(t['h1'], lang), answer=links(t['answer'], lang), banner=None,
                    need=[links(n, lang) for n in (t['need'] or [])], steps=norm_steps(t['steps'], lang),
                    sections=[(h, links(b, lang)) for h, b in t['sections']],
                    problems=norm_qa(t['problems'], lang), faq=norm_qa(t['faq'], lang))
    return brand_article(aid, lang)


def brand_article(aid, lang):
    D, T, b = C.BRANDS[aid], C.BRAND_TXT[lang], BRAND[aid]
    i = LI[lang]
    label, systems = D['label'][i], D['systems'][i]
    tested = b['status'] == 'tested'
    note = fix_name(b['note' + SUF[lang]])
    raw = [fix_name(s) for s in b['steps' + SUF[lang]]]
    steps = [C.INSTALL[lang] + (None,)]
    for n, s in enumerate(raw):
        steps.append((None, f'<p>{html.escape(s)}</p>', None))
        if n == 0:
            steps.append(C.OPEN_PICK[lang] + (None,))
    steps.append((T['use_h'], T['use_b'], None))
    rq, ra = T['faq_remote']
    status_line = T['status_tested' if tested else 'status_initial']
    faq = [(rq, f'<p>{ra[0] if D["remote"][0] else ra[1]}</p>'),
           (T['faq_models'][0], '<p>' + T['faq_models'][1].format(systems=systems, status_line=status_line) + '</p>'),
           (C.FREE[lang][0], f'<p>{C.FREE[lang][1]}</p>'), (C.NO_4G[lang][0], f'<p>{C.NO_4G[lang][1]}</p>')]
    need = [T['need'][0], {'pt': 'A TV (ou o aparelho) ligada ao Wi-Fi.', 'en': 'The TV (or streaming device) connected to Wi-Fi.',
                           'es': 'La TV (o el dispositivo) conectada al Wi-Fi.'}[lang], T['need'][2]]
    return dict(id=aid, read=3, howto=True, time='PT5M', related=D['related'],
                seo_title=T['seo_title'].format(label=label), desc=T['desc_tested' if tested else 'desc_initial'].format(label=label),
                h1=T['h1'].format(label=label), answer=T['ans_tested' if tested else 'ans_initial'].format(label=label),
                works=T['works'].format(systems=systems),
                banner=None if tested else C.UI[lang]['initial_banner'].format(note=html.escape(note)),
                status=b['status'], need=need, steps=steps, sections=[],
                problems=[fq(p, lang) for p in D['problems']], faq=faq)


# ── Página ────────────────────────────────────────────────────────────────
def ld(obj):
    return f'<script type="application/ld+json">{json.dumps(obj, ensure_ascii=False)}</script>'


def head(lang, title, desc, canonical, alternates, og_type='article'):
    U = C.UI[lang]
    alts = ''.join(f'<link rel="alternate" hreflang="{C.UI[l]["html_lang"]}" href="{u}">' for l, u in alternates.items())
    alts += f'<link rel="alternate" hreflang="x-default" href="{alternates["pt"]}">'
    return f'''<!doctype html>
<html lang="{U['html_lang']}">
<head>
<meta charset="utf-8">
<meta name="viewport" content="width=device-width, initial-scale=1, viewport-fit=cover">
<title>{esc(title)}</title>
<meta name="description" content="{esc(desc)}">
<link rel="canonical" href="{canonical}">
{alts}
<meta name="theme-color" content="#A9ED87">
<link rel="icon" href="/favicon.svg" type="image/svg+xml">
<link rel="apple-touch-icon" href="/assets/icone-512.png">
<link rel="preload" href="/assets/figtree.woff2" as="font" type="font/woff2" crossorigin>
<meta property="og:type" content="{og_type}">
<meta property="og:site_name" content="Comandoo">
<meta property="og:title" content="{esc(title.split(' | ')[0])}">
<meta property="og:description" content="{esc(desc)}">
<meta property="og:url" content="{canonical}">
<meta property="og:image" content="{SITE}/assets/og-{lang}.png">
<meta property="og:locale" content="{U['og_locale']}">
<meta name="twitter:card" content="summary_large_image">
<link rel="stylesheet" href="/assets/site.css">
<link rel="stylesheet" href="/assets/guide.css">'''


def topbar(lang, alternates, crumbs, current_guides=True, current_help=False):
    U = C.UI[lang]
    seg = ''.join(f'<a href="{u.replace(SITE, "")}" hreflang="{l}" lang="{l}"' + (' aria-current="page"' if l == lang else '') + f'>{l.upper()}</a>'
                  for l, u in alternates.items())
    cr = ' › '.join(f'<a href="{h}">{t}</a>' for t, h in crumbs)
    return f'''<a class="skip" href="#conteudo">{U['skip']}</a>
<div class="gtop"><div class="wrap">
<header class="top">
  <a class="brand" href="{U['home']}">{B.sym('#0E120F')}Comandoo</a>
  <nav class="gnav" aria-label="Site"><a class="gl" href="{U['guides']}"{' aria-current="true"' if current_guides else ''}>{U['guides_label']}</a><a class="gl" href="{U['help']}"{' aria-current="true"' if current_help else ''}>{U['help_label']}</a>
    <span class="seg" aria-label="{U['lang_nav']}">{seg}</span></nav>
</header>
<div class="ghead">
  <p class="crumbs">{cr}</p>'''


def footer(lang):
    U = C.UI[lang]
    return f'''<footer><div class="wrap foot">
  <div>
    <div class="brand">{B.sym('#A9ED87')}Comandoo</div>
    <p>{U['indep']}</p>
    <p>{U['contact']}: <a href="mailto:{B.EMAIL}">{B.EMAIL}</a></p>
    <p>© 2026 Agência D3</p>
  </div>
  <ul>
    <li><a href="{U['home']}">{U['home_label']}</a></li>
    <li><a href="{U['guides']}">{U['guides_label']}</a></li>
    <li><a href="{U['help']}">{U['help_label']}</a></li>
    <li><a href="{U['changelog']}">{U['changelog_label']}</a></li>
    <li><a href="{U['privacy']}">{U['privacy_label']}</a></li>
  </ul>
</div></footer>
<script src="/assets/lang.js" defer></script>
<script src="/assets/waitlist.js" defer></script>
</body>
</html>
'''


def cta_box(lang):
    U = C.UI[lang]
    if B.PLAY_URL:
        btn = f'<a class="pill pill-dark" href="{B.PLAY_URL}" rel="noopener">{B.sym()}{U["play"]}</a>'
        return f'<aside class="gcta">{B.sym("#0E120F")}<div><b>{U["cta_t"]}</b><p>{U["cta_s"]}</p></div>{btn}</aside>'
    return f'<aside class="gcta gcta-wl">{B.sym("#0E120F")}<div><b>{U["cta_t"]}</b><p>{U["cta_s"]}</p></div>{B.waitlist(lang)}</aside>'


def details(items):
    return ''.join(f'<details><summary>{q}</summary><div>{a}</div></details>' for q, a in items)


TOC_TXT = {'pt': ('Nesta página', 'Não conectou?', 'Faça o diagnóstico guiado para a sua marca'),
           'en': ('On this page', 'Can’t connect?', 'Run the guided check for your brand'),
           'es': ('En esta página', '¿No se conecta?', 'Haz el diagnóstico guiado para tu marca')}


def slug(h):
    import unicodedata
    t = unicodedata.normalize('NFKD', re.sub('<[^>]+>', '', h)).encode('ascii', 'ignore').decode().lower()
    return re.sub('[^a-z0-9]+', '-', t).strip('-')[:48] or 'secao'


def render(aid, lang):
    U, a = C.UI[lang], article(aid, lang)
    canon = url(aid, lang, True)
    alternates = {l: url(aid, l, True) for l in C.LANGS}
    steps_html = ''
    for n, (h, b, sh) in enumerate(a['steps']):
        img = shot(sh[0], sh[1], sh[2], lang) if sh else ''
        steps_html += f'<li id="passo-{n+1}">' + (f'<h3>{h}</h3>' if h else '') + b + img + '</li>'
    need = (f'<section class="need" aria-labelledby="need"><h2 id="need">{U["need_h"]}</h2><ul>'
            + ''.join(f'<li>{x}</li>' for x in a['need']) + '</ul>'
            + (f'<p class="works">{a["works"]}</p>' if a.get('works') else '') + '</section>') if a['need'] else ''
    banner = f'<div class="tip warn"><p>{a["banner"]} <a href="mailto:{B.EMAIL}">{B.EMAIL}</a>.</p></div>' if a.get('banner') else ''
    sec_ids = [slug(h) for h, _ in a['sections']]
    secs = ''.join(f'<h2 id="{i}">{h}</h2>{b}' for i, (h, b) in zip(sec_ids, a['sections']))
    toc = ([('need', U['need_h'])] if a['need'] else []) + ([('passo-a-passo', U['steps_h'])] if a['steps'] else []) \
        + [(i, re.sub('<[^>]+>', '', h)) for i, (h, _) in zip(sec_ids, a['sections'])] \
        + [('problemas', U['problems_h']), ('perguntas', U['faq_h'])]
    T = TOC_TXT[lang]
    side = (f'<aside class="gside" aria-label="{T[0]}"><div class="gside-in"><p class="gside-h">{T[0]}</p><ol>'
            + ''.join(f'<li><a href="#{i}">{esc(t)}</a></li>' for i, t in toc)
            + f'</ol><a class="gside-card" href="{U["help"]}"><b>{T[1]}</b><span>{T[2]}</span></a></div></aside>')
    steps_block = f'<h2 id="passo-a-passo">{U["steps_h"]}</h2><ol class="steps-g">{steps_html}</ol>' if a['steps'] else ''
    rel = ''.join(f'<li><a href="{url(r, lang)}">{article(r, lang)["h1"]}<span>{U["read"].format(n=article(r, lang)["read"])}</span></a></li>'
                  for r in a['related'])
    status_chip = f'<li>{U["status"][a["status"]]}</li>' if a.get('status') else ''

    schema = [{"@context": "https://schema.org", "@type": "Article", "headline": a['h1'], "description": a['desc'],
               "inLanguage": U['html_lang'], "url": canon, "datePublished": UPDATED, "dateModified": UPDATED,
               "author": {"@type": "Organization", "name": "Agência D3"},
               "publisher": {"@type": "Organization", "name": "Agência D3", "logo": {"@type": "ImageObject", "url": f"{SITE}/assets/icone-512.png"}},
               "image": f"{SITE}/assets/og-{lang}.png", "mainEntityOfPage": canon}]
    if a['howto'] and a['steps']:
        schema.append({"@context": "https://schema.org", "@type": "HowTo", "name": a['h1'], "description": a['answer'],
                       "inLanguage": U['html_lang'], "totalTime": a.get('time') or 'PT5M',
                       "step": [{"@type": "HowToStep", "position": n + 1, "url": f"{canon}#passo-{n+1}",
                                 "name": h or plain(b, 70), "text": plain(b)} for n, (h, b, _) in enumerate(a['steps'])]})
    if a['faq']:
        schema.append({"@context": "https://schema.org", "@type": "FAQPage", "mainEntity": [
            {"@type": "Question", "name": q, "acceptedAnswer": {"@type": "Answer", "text": plain(x, 1000)}} for q, x in a['faq']]})
    schema.append({"@context": "https://schema.org", "@type": "BreadcrumbList", "itemListElement": [
        {"@type": "ListItem", "position": 1, "name": "Comandoo", "item": SITE + U['home']},
        {"@type": "ListItem", "position": 2, "name": U['guides_label'], "item": SITE + U['guides']},
        {"@type": "ListItem", "position": 3, "name": a['h1'], "item": canon}]})

    return (head(lang, a['seo_title'], a['desc'], canon, alternates) + ''.join(ld(s) for s in schema) + '\n</head>\n<body>\n'
            + topbar(lang, alternates, [('Comandoo', U['home']), (U['guides_label'], U['guides'])]) + f'''
  <h1>{a['h1']}</h1>
  <p class="answer">{a['answer']}</p>
  <ul class="meta">{status_chip}<li>{U['read'].format(n=a['read'])}</li><li>{U['updated'].format(d=fdate(UPDATED, lang))}</li><li>{U['version'].format(v=APP_VERSION)}</li></ul>
</div>
</div></div>

<main id="conteudo" class="wrap gmain">
<article class="prose">
  {banner}{need}
  {steps_block}
  {secs}
  <h2 id="problemas">{U['problems_h']}</h2>
  <p>{U['test_conn']}</p>
  <div class="prob">{details(a['problems'])}</div>
  <p class="more"><a href="{U['help']}">{U['help_more']}</a></p>
  <h2 id="perguntas">{U['faq_h']}</h2>
  <div class="prob">{details(a['faq'])}</div>
  {cta_box(lang)}
  <p class="updated">{U['footnote'].format(v=APP_VERSION)} <a href="mailto:{B.EMAIL}">{B.EMAIL}</a>.</p>
</article>
<nav class="related" aria-labelledby="rel"><h2 id="rel">{U['related_h']}</h2><ul>{rel}</ul></nav>
{side}
</main>
<script src="/assets/guide.js" defer></script>
''' + footer(lang))


def render_index(lang):
    U = C.UI[lang]
    canon = SITE + U['guides']
    alternates = {l: SITE + C.UI[l]['guides'] for l in C.LANGS}
    groups, items = '', []
    for g, ids in U['groups']:
        cards = ''
        for aid in ids:
            a = article(aid, lang)
            items.append((a['h1'], url(aid, lang, True)))
            chip = f'<em>{U["status"][a["status"]]}</em>' if a.get('status') else ''
            cards += f'<li><a href="{url(aid, lang)}">{a["h1"]}<span>{a["desc"]}</span>{chip}</a></li>'
        groups += f'<section class="gsec"><h2>{g}</h2><ul class="cards">{cards}</ul></section>'
    schema = {"@context": "https://schema.org", "@type": "CollectionPage", "name": U['idx_h1'], "description": U['idx_desc'],
              "inLanguage": U['html_lang'], "url": canon,
              "mainEntity": {"@type": "ItemList", "itemListElement": [
                  {"@type": "ListItem", "position": n + 1, "name": t, "url": u} for n, (t, u) in enumerate(items)]}}
    return (head(lang, U['idx_title'], U['idx_desc'], canon, alternates, 'website') + ld(schema) + '\n</head>\n<body>\n'
            + topbar(lang, alternates, [('Comandoo', U['home'])]) + f'''
  <h1>{U['idx_h1']}</h1>
  <p class="answer">{U['idx_lead']}</p>
</div>
</div></div>
<main id="conteudo" class="wrap gindex">{groups}{cta_box(lang)}</main>
''' + footer(lang))


LAUNCH_TXT = {'pt': ('O que vem no lançamento', 'Grátis, sem anúncios', 'Aparelhos', 'Testado em aparelho real', 'Suporte inicial',
                     'Suporte inicial quer dizer que o app foi feito com base no protocolo da marca, mas ainda não foi testado em aparelho real.',
                     'Veja a lista completa', 'os guias de cada marca'),
              'en': ('What’s coming at launch', 'Free, no ads', 'Devices', 'Tested on a real device', 'Initial support',
                     'Initial support means the app was built from the brand’s protocol but hasn’t been tested on a real device yet.',
                     'See the full list', 'the guide for each brand'),
              'es': ('Lo que llega con el lanzamiento', 'Gratis, sin anuncios', 'Dispositivos', 'Probado en un dispositivo real', 'Soporte inicial',
                     'Soporte inicial significa que la app se hizo con base en el protocolo de la marca, pero todavía no se probó en un dispositivo real.',
                     'Mira la lista completa', 'las guías de cada marca')}


def launch_preview(lang):
    """Antes do lançamento: o que o app já faz, com os mesmos textos da home e a lista do compat.json."""
    t, L = B.T[lang], LAUNCH_TXT[lang]
    feats = ''.join(f'<li><strong>{h}.</strong> {d}</li>' for _, h, d in t['feats'])
    extras = ''.join(f'<li><strong>{h}.</strong> {re.split(r"(?<=[.!]) ", d)[0]}</li>' for h, d in t['extras'])
    names = lambda st: ', '.join(b['name'] for b in COMPAT['brands'] if b['status'] == st)
    tested, initial = names('tested'), names('initial')
    dev = (f'<ul>' + (f'<li><strong>{L[3]}:</strong> {tested}.</li>' if tested else '')
           + (f'<li><strong>{L[4]}:</strong> {initial}.</li>' if initial else '') + '</ul>'
           + f'<p>{L[5]} <a href="{t["path"]}#compat">{L[6]}</a> · <a href="{C.UI[lang]["guides"]}">{L[7]}</a>.</p>')
    return (f'<h2>{L[0]}</h2><h3>{L[1]}</h3><ul>{feats}</ul>'
            f'<h3>{t["ex_h"]}</h3><p>{t["ex_sub"]}</p><ul>{extras}</ul>'
            f'<h3>{L[2]}</h3>{dev}')


def render_changelog(lang, entries):
    U = C.UI[lang]
    canon = SITE + U['changelog']
    alternates = {l: SITE + C.UI[l]['changelog'] for l in C.LANGS}
    body = ''
    for e in entries:
        notes = ''.join(f'<li>{html.escape(n)}</li>' for n in e['notes'][lang])
        guides = ''.join(f'<li><a href="{url(g, lang)}">{article(g, lang)["h1"]}</a></li>' for g in e.get('guides', []))
        body += (f'<section class="ver" id="v{e["version"]}"><h2>{e["version"]}</h2><p class="when">{fdate(e["date"], lang)}</p>'
                 f'<ul>{notes}</ul>' + (f'<h3>{U["cl_guides"]}</h3><ul>{guides}</ul>' if guides else '') + '</section>')
    if not entries:
        body = f'<p>{U["cl_pre"].format(v=APP_VERSION)}</p>' + launch_preview(lang)
    return (head(lang, U['cl_title'], U['cl_desc'], canon, alternates, 'website') + '\n</head>\n<body>\n'
            + topbar(lang, alternates, [('Comandoo', U['home'])], current_guides=False) + f'''
  <h1>{U['cl_h1']}</h1>
  <p class="answer">{U['cl_lead']}</p>
</div>
</div></div>
<main id="conteudo" class="wrap"><article class="prose">{body}{cta_box(lang)}</article></main>
''' + footer(lang))


def write(path, text):
    p = ROOT / path
    p.parent.mkdir(parents=True, exist_ok=True)
    p.write_text(text, encoding='utf-8')
    return path


def sitemap(pages):
    rows = []
    for group in pages:
        alt = ''.join(f'<xhtml:link rel="alternate" hreflang="{C.UI[l]["html_lang"]}" href="{u}"/>' for l, u in group.items())
        alt += f'<xhtml:link rel="alternate" hreflang="x-default" href="{group["pt"]}"/>'
        for l, u in group.items():
            rows.append(f'<url><loc>{u}</loc><lastmod>{UPDATED}</lastmod>{alt}</url>')
    return ('<?xml version="1.0" encoding="UTF-8"?>\n<urlset xmlns="http://www.sitemaps.org/schemas/sitemap/0.9" '
            'xmlns:xhtml="http://www.w3.org/1999/xhtml">\n' + '\n'.join(rows) + '\n</urlset>\n')


def main(extra=()):
    n = 0
    pages = [{l: SITE + C.UI[l]['home'] for l in C.LANGS}]
    for lang in C.LANGS:
        write(C.UI[lang]['guides'].strip('/') + '/index.html', render_index(lang)); n += 1
    pages.append({l: SITE + C.UI[l]['guides'] for l in C.LANGS})
    for aid in C.SLUGS:
        for lang in C.LANGS:
            write(url(aid, lang).strip('/') + '/index.html', render(aid, lang)); n += 1
        pages.append({l: url(aid, l, True) for l in C.LANGS})
    entries = json.loads((ROOT / 'tools' / 'changelog.json').read_text(encoding='utf-8'))
    for lang in C.LANGS:
        write(C.UI[lang]['changelog'].strip('/') + '/index.html', render_changelog(lang, entries)); n += 1
    pages.append({l: SITE + C.UI[l]['changelog'] for l in C.LANGS})
    pages.append({'pt': f'{SITE}/privacidade', 'en': f'{SITE}/privacidade/en', 'es': f'{SITE}/privacidade/es'})
    pages.extend(extra)
    write('sitemap.xml', sitemap(pages))
    write('robots.txt', f'User-agent: *\nAllow: /\n\nSitemap: {SITE}/sitemap.xml\n')
    print(n, 'páginas; sitemap com', sum(len(g) for g in pages), 'URLs')


if __name__ == '__main__':
    main()
