#!/usr/bin/env python3
"""Central de ajuda do Comandoo: /ajuda, /en/help, /es/ayuda.

Uso: python3 tools/help.py   (gera também os guias, o changelog e o sitemap)

Tudo vem das mesmas fontes do app: compat.json (marcas e passos) e faq.json (respostas).
Diagnóstico guiado = aparelho × problema → passos em ordem: Testar conexão, correção da marca, Relatar.
Link direto para um diagnóstico: /ajuda/?marca=<id do compat.json>&problema=<id do problema>
Link direto para uma pergunta do FAQ: /ajuda/#<id do faq.json>
"""
import html
import json
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))
import build as B  # noqa: E402
import guides as G  # noqa: E402
import guides_content as C  # noqa: E402

SITE = G.SITE
LANGS = C.LANGS
LI = G.LI
SUF = G.SUF

T = {
 'pt': dict(
  title='Central de ajuda do Comandoo: resolva problemas de conexão',
  desc='Diagnóstico guiado para quando o celular não encontra o aparelho, não conecta ou o aparelho não obedece. Respostas por marca e as perguntas frequentes do app.',
  h1='Central de ajuda',
  lead='Escolha o seu aparelho e o que está acontecendo. A central mostra, em ordem, o que fazer, com as instruções da sua marca.',
  diag_h='Diagnóstico guiado', q1='1. Qual é o seu aparelho?', q2='2. O que está acontecendo?',
  pick='Escolha o aparelho e o problema para ver o passo a passo.',
  result_h='O que fazer, em ordem', brand_steps='Passo a passo da sua marca', copy='Copiar link deste diagnóstico', copied='Link copiado',
  first='Comece pelo Testar conexão', last='Ainda não resolveu? Relate no app',
  power_step='Configuração para ligar pela rede', unsupported_t='Esta marca ainda não funciona',
  faq_h='Perguntas frequentes do app', faq_lead='As mesmas respostas que aparecem no app, em Ajustes. Cada pergunta tem um link próprio para compartilhar.',
  noscript='O diagnóstico guiado precisa de JavaScript. As respostas estão nas perguntas frequentes abaixo.',
  sections={'start': 'Começar', 'connect': 'Conectar', 'use': 'Usar', 'share': 'Compartilhar', 'app': 'O app', 'privacy': 'Privacidade e relatos'},
  symptoms=[('nao-aparece', 'Não aparece na busca'), ('codigo', 'Pede código ou permissão'), ('nao-obedece', 'Conecta, mas não obedece'),
            ('cai', 'A conexão cai'), ('nao-liga', 'Não liga pelo celular'), ('texto', 'O texto não chega')],
 ),
 'en': dict(
  title='Comandoo help center: fix connection problems',
  desc='Guided check for when your phone can’t find the device, won’t connect or the device ignores it. Answers by brand and the app’s FAQ.',
  h1='Help center',
  lead='Pick your device and what is happening. The help center shows what to do, in order, with your brand’s instructions.',
  diag_h='Guided check', q1='1. Which device do you have?', q2='2. What is happening?',
  pick='Pick the device and the problem to see the steps.',
  result_h='What to do, in order', brand_steps='Steps for your brand', copy='Copy link to this check', copied='Link copied',
  first='Start with Test connection', last='Still stuck? Report it in the app',
  power_step='Setting to turn it on over the network', unsupported_t='This brand does not work yet',
  faq_h='App FAQ', faq_lead='The same answers you see in the app, under Settings. Each question has its own link to share.',
  noscript='The guided check needs JavaScript. The answers are in the FAQ below.',
  sections={'start': 'Get started', 'connect': 'Connect', 'use': 'Use', 'share': 'Share', 'app': 'The app', 'privacy': 'Privacy and reports'},
  symptoms=[('nao-aparece', 'Doesn’t show up in the search'), ('codigo', 'Asks for a code or permission'), ('nao-obedece', 'Connects but doesn’t respond'),
            ('cai', 'Connection drops'), ('nao-liga', 'Won’t turn on from the phone'), ('texto', 'Text doesn’t arrive')],
 ),
 'es': dict(
  title='Centro de ayuda de Comandoo: resuelve problemas de conexión',
  desc='Diagnóstico guiado para cuando el celular no encuentra el dispositivo, no se conecta o el dispositivo no responde. Respuestas por marca y las preguntas frecuentes de la app.',
  h1='Centro de ayuda',
  lead='Elige tu dispositivo y lo que está pasando. El centro de ayuda muestra, en orden, qué hacer, con las instrucciones de tu marca.',
  diag_h='Diagnóstico guiado', q1='1. ¿Cuál es tu dispositivo?', q2='2. ¿Qué está pasando?',
  pick='Elige el dispositivo y el problema para ver el paso a paso.',
  result_h='Qué hacer, en orden', brand_steps='Paso a paso de tu marca', copy='Copiar enlace de este diagnóstico', copied='Enlace copiado',
  first='Empieza con Probar conexión', last='¿No se resolvió? Repórtalo en la app',
  power_step='Ajuste para encender por la red', unsupported_t='Esta marca todavía no funciona',
  faq_h='Preguntas frecuentes de la app', faq_lead='Las mismas respuestas que aparecen en la app, en Ajustes. Cada pregunta tiene su propio enlace para compartir.',
  noscript='El diagnóstico guiado necesita JavaScript. Las respuestas están en las preguntas frecuentes de abajo.',
  sections={'start': 'Empezar', 'connect': 'Conectar', 'use': 'Usar', 'share': 'Compartir', 'app': 'La app', 'privacy': 'Privacidad y reportes'},
  symptoms=[('nao-aparece', 'No aparece en la búsqueda'), ('codigo', 'Pide código o permiso'), ('nao-obedece', 'Se conecta pero no responde'),
            ('cai', 'La conexión se cae'), ('nao-liga', 'No enciende desde el celular'), ('texto', 'El texto no llega')],
 ),
}

# Itens do FAQ que ainda não valem para a versão do Play (aguardando confirmação do Grok).
FAQ_HIDE = {'atualizar'}
SECTION_ORDER = ['start', 'connect', 'use', 'share', 'app', 'privacy']

# Respostas do FAQ por problema; '*' vale para todas as marcas.
SYMPTOM_FAQ = {
    'nao-aparece': {'*': ['tv-nao-aparece', 'ip-da-tv'], 'roku': ['tv-nao-aparece', 'ip-da-tv', 'marca-fora'],
                    'androidtv': ['tv-nao-aparece', 'ip-da-tv', 'marca-fora'], 'vestel': ['tv-nao-aparece', 'vestel', 'ip-da-tv']},
    'codigo': {'*': ['codigo-pin'], 'samsung': ['samsung-permissao', 'codigo-pin'], 'lg': ['codigo-pin', 'lg-permissao']},
    'nao-obedece': {'*': ['mesma-rede', 'botao-desativado'], 'roku': ['roku-limitado', 'mesma-rede', 'botao-desativado'],
                    'lg': ['lg-permissao', 'mesma-rede', 'botao-desativado'], 'samsung': ['mesma-rede', 'samsung-permissao', 'botao-desativado']},
    'cai': {'*': ['conexao-cai', 'mesma-rede']},
    'nao-liga': {'*': ['ligar-tv']},
    'texto': {'*': ['digitar', 'botao-desativado']},
}
BRAND_STEPS_FOR = {'nao-aparece', 'codigo'}       # problemas em que entra o passo a passo da marca (compat.json)
POWER_KEYS = ('Para ligar', 'Para o app ligar')   # passos do compat.json sobre ligar pela rede (texto em pt)


def esc(s):
    return html.escape(s, quote=True)


def faq_step(fid, lang):
    q, a = G.fq(fid, lang)
    return {'t': q, 'h': a}


def brand_name(b, lang):
    return B.NAME_TR.get(b['id'], {}).get(lang, b['name'])


def diagnosis(lang):
    U = T[lang]
    data = {}
    for b in G.COMPAT['brands']:
        steps_raw = [G.fix_name(s) for s in b.get('steps' + SUF[lang], [])]
        steps_pt = b.get('steps', [])
        per = {}
        for sid, _ in U['symptoms']:
            out = [dict(faq_step('testar-conexao', lang), t=U['first'])]
            if b['status'] == 'unsupported':
                out = [{'t': U['unsupported_t'], 'h': '<p>' + esc(G.fix_name(b['note' + SUF[lang]])) + '</p>'}, faq_step('marca-fora', lang)]
            else:
                ids = SYMPTOM_FAQ[sid].get(b['id'], SYMPTOM_FAQ[sid]['*'])
                if sid in BRAND_STEPS_FOR and steps_raw:
                    out.append({'t': U['brand_steps'] + f' ({brand_name(b, lang)})',
                                'h': '<ol>' + ''.join(f'<li>{esc(s)}</li>' for s in steps_raw) + '</ol>'})
                for fid in ids:
                    out.append(faq_step(fid, lang))
                if sid == 'nao-liga':
                    for i, s in enumerate(steps_pt):
                        if s.startswith(POWER_KEYS) and i < len(steps_raw):
                            out.append({'t': U['power_step'], 'h': '<p>' + esc(steps_raw[i]) + '</p>'})
            out.append(dict(faq_step('relatar', lang), t=U['last']))
            per[sid] = out
        data[b['id']] = per
    return data


def render(lang):
    U, UI = T[lang], C.UI[lang]
    canon = SITE + UI['help']
    alternates = {l: SITE + C.UI[l]['help'] for l in LANGS}
    brands = ''.join(
        f'<label class="hchip"><input type="radio" name="marca" value="{b["id"]}"><span>{esc(brand_name(b, lang))}</span></label>'
        for b in G.COMPAT['brands'])
    syms = ''.join(f'<label class="hchip"><input type="radio" name="problema" value="{sid}"><span>{esc(lbl)}</span></label>'
                   for sid, lbl in U['symptoms'])
    # FAQ completo, por seção
    by_sec = {}
    for i in G.FAQ.values():
        if i['id'] in FAQ_HIDE:
            continue
        by_sec.setdefault(i['section'], []).append(i)
    faq_html, faq_ld = '', []
    for sec in SECTION_ORDER + [s for s in by_sec if s not in SECTION_ORDER]:
        items = by_sec.get(sec)
        if not items:
            continue
        rows = ''
        for i in items:
            q, a = G.fq(i['id'], lang)
            rows += f'<details id="{i["id"]}"><summary>{esc(q)}<a class="anchor" href="#{i["id"]}" aria-label="Link">#</a></summary><div>{a}</div></details>'
            faq_ld.append({"@type": "Question", "name": q, "acceptedAnswer": {"@type": "Answer", "text": G.plain(a, 1000)}})
        faq_html += f'<section class="fsec"><h3>{U["sections"].get(sec, sec)}</h3><div class="prob">{rows}</div></section>'
    schema = [{"@context": "https://schema.org", "@type": "FAQPage", "inLanguage": UI['html_lang'], "url": canon, "mainEntity": faq_ld},
              {"@context": "https://schema.org", "@type": "BreadcrumbList", "itemListElement": [
                  {"@type": "ListItem", "position": 1, "name": "Comandoo", "item": SITE + UI['home']},
                  {"@type": "ListItem", "position": 2, "name": U['h1'], "item": canon}]}]
    payload = {'d': diagnosis(lang), 's': {k: U[k] for k in ('pick', 'result_h', 'copy', 'copied')},
               'n': {b['id']: brand_name(b, lang) for b in G.COMPAT['brands']}, 'p': dict(U['symptoms'])}
    data_json = json.dumps(payload, ensure_ascii=False).replace('</', '<\\/')
    return (G.head(lang, U['title'], U['desc'], canon, alternates, 'website') + ''.join(G.ld(s) for s in schema)
            + '\n<link rel="stylesheet" href="/assets/help.css">\n</head>\n<body>\n'
            + G.topbar(lang, alternates, [('Comandoo', UI['home'])], current_guides=False, current_help=True) + f'''
  <h1>{U['h1']}</h1>
  <p class="answer">{U['lead']}</p>
</div>
</div></div>
<main id="conteudo" class="wrap">
<section class="diag" id="diagnostico" aria-labelledby="dh">
  <h2 id="dh">{U['diag_h']}</h2>
  <fieldset><legend>{U['q1']}</legend><div class="chips">{brands}</div></fieldset>
  <fieldset><legend>{U['q2']}</legend><div class="chips">{syms}</div></fieldset>
  <div id="resultado" class="result" aria-live="polite"><p class="hint-r">{U['pick']}</p></div>
  <noscript><p class="hint-r">{U['noscript']}</p></noscript>
</section>
<section class="prose faqall" id="perguntas" aria-labelledby="fh">
  <h2 id="fh">{U['faq_h']}</h2>
  <p>{U['faq_lead']}</p>
  {faq_html}
  {G.cta_box(lang)}
</section>
</main>
<script type="application/json" id="help-data">{data_json}</script>
<script src="/assets/help.js" defer></script>
''' + G.footer(lang))


def main():
    for lang in LANGS:
        G.write(C.UI[lang]['help'].strip('/') + '/index.html', render(lang))
    G.main(extra=[{l: SITE + C.UI[l]['help'] for l in LANGS}])
    print('ajuda ok')


if __name__ == '__main__':
    main()
