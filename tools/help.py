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


# Resultados do Testar conexão (código da 1.24.8: Diagnostics.java / L.java, via Grok em 12/10/2026).
# id da âncora = etapa-status. Título e detalhe = texto exato da tela do app.
TEST_RESULTS = [
 ('wifi-fail', 'nao-aparece',
  {'pt': ('Sem Wi-Fi', 'O celular não está no Wi-Fi. O controle precisa estar na mesma rede do aparelho, e dados móveis não servem.', 'Toque em Abrir ajustes de Wi-Fi e conecte o celular à mesma rede do aparelho.'),
   'en': ('No Wi-Fi', 'The phone is not on Wi-Fi. The remote needs the same network as the device, and mobile data will not do.', 'Tap Open Wi-Fi settings and connect the phone to the same network as the device.'),
   'es': ('Sin Wi-Fi', 'El celular no está en Wi-Fi. El control necesita la misma red que el dispositivo, y los datos móviles no sirven.', 'Toca Abrir ajustes de Wi-Fi y conecta el celular a la misma red que el dispositivo.')}),
 ('local-fail', 'nao-aparece',
  {'pt': ('Acesso à rede local bloqueado', 'O Android bloqueia o app de falar com o aparelho. Em Ajustes do Android, abra Apps, este app, Permissões, e libere Dispositivos por perto.', 'Siga o caminho do aviso nos ajustes do Android e rode o teste de novo. Só acontece no Android 17 ou superior.'),
   'en': ('Local network access blocked', 'Android is blocking the app from talking to the device. In Android Settings, open Apps, this app, Permissions, and allow Nearby devices.', 'Follow that path in Android settings and run the test again. Only happens on Android 17 or later.'),
   'es': ('Acceso a la red local bloqueado', 'Android bloquea la app para hablar con el dispositivo. En Ajustes de Android, abre Apps, esta app, Permisos, y permite Dispositivos cercanos.', 'Sigue esa ruta en los ajustes de Android y vuelve a probar. Solo pasa en Android 17 o superior.')}),
 ('host-fail', 'nao-aparece',
  {'pt': ('Nenhum aparelho salvo', 'Ainda não há um aparelho conectado neste celular.', 'Toque em Buscar aparelhos e escolha o seu na lista.'),
   'en': ('No saved device', 'There is no device connected on this phone yet.', 'Tap Find devices and pick yours from the list.'),
   'es': ('Ningún dispositivo guardado', 'Todavía no hay un dispositivo conectado en este celular.', 'Toca Buscar dispositivos y elige el tuyo en la lista.')}),
 ('net-warn', 'nao-aparece',
  {'pt': ('Celular e aparelho parecem estar em redes diferentes', 'Isso acontece com Wi-Fi de visitantes, repetidores ou quando o aparelho está em outra faixa do roteador. Ligue os dois na mesma rede.', 'Deixe o celular no mesmo Wi-Fi do aparelho (mesmo nome de rede e mesma faixa, 2,4 ou 5 GHz) e toque em Buscar aparelhos.'),
   'en': ('Phone and device seem to be on different networks', 'This happens with guest Wi-Fi, repeaters or when the device is on another band of the router. Put both on the same network.', 'Put the phone on the same Wi-Fi as the device (same network name and band, 2.4 or 5 GHz) and tap Find devices.'),
   'es': ('Celular y dispositivo parecen estar en redes distintas', 'Esto pasa con Wi-Fi de invitados, repetidores o cuando el dispositivo está en otra banda del router. Conecta ambos a la misma red.', 'Deja el celular en el mismo Wi-Fi que el dispositivo (mismo nombre de red y misma banda, 2,4 o 5 GHz) y toca Buscar dispositivos.')}),
 ('port-fail', 'nao-aparece',
  {'pt': ('O aparelho não respondeu', 'Nenhuma porta de controle do aparelho abriu. Confira se o aparelho está ligado (não em espera) e no mesmo Wi-Fi. Se o roteador mudou o endereço dele, Buscar aparelhos o encontra de novo.', 'Ligue a tela do aparelho e toque em Buscar aparelhos. Em algumas marcas é preciso ativar o controle pela rede nas configurações do aparelho.'),
   'en': ('The device did not answer', 'No control port of the device opened. Check that the device is on (not on standby) and on the same Wi-Fi. If the router changed its address, Find devices finds it again.', 'Turn the device screen on and tap Find devices. Some brands need network control turned on in the device settings.'),
   'es': ('El dispositivo no respondió', 'Ningún puerto de control del dispositivo se abrió. Comprueba que el dispositivo esté encendido (no en espera) y en el mismo Wi-Fi. Si el router cambió su dirección, Buscar dispositivos lo encuentra de nuevo.', 'Enciende la pantalla del dispositivo y toca Buscar dispositivos. Algunas marcas piden activar el control por red en los ajustes del dispositivo.')}),
 ('pair-warn', 'codigo',
  {'pt': ('Sem pareamento salvo', 'O aparelho ainda não autorizou este celular. Toque no aparelho na lista e aceite o pedido que aparece na tela dele.', 'Toque em Buscar aparelhos, escolha o aparelho e aceite o pedido ou digite o código que aparece na tela dele.'),
   'en': ('No saved pairing', 'The device has not authorized this phone yet. Tap the device in the list and accept the request that appears on its screen.', 'Tap Find devices, pick the device and accept the request or type the code shown on its screen.'),
   'es': ('Sin emparejamiento guardado', 'El dispositivo todavía no autorizó este celular. Toca el dispositivo en la lista y acepta la solicitud que aparece en su pantalla.', 'Toca Buscar dispositivos, elige el dispositivo y acepta la solicitud o escribe el código que aparece en su pantalla.')}),
 ('speed-warn', 'cai',
  {'pt': ('Resposta lenta', 'Os botões podem demorar. Aproximar o roteador do aparelho ou usar a faixa de 5 GHz costuma ajudar.', 'Se puder, aproxime o roteador do aparelho ou conecte os dois na faixa de 5 GHz.'),
   'en': ('Slow answer', 'Buttons may lag. Moving the router closer to the device or using the 5 GHz band usually helps.', 'If you can, move the router closer to the device or put both on the 5 GHz band.'),
   'es': ('Respuesta lenta', 'Los botones pueden tardar. Acercar el router al dispositivo o usar la banda de 5 GHz suele ayudar.', 'Si puedes, acerca el router al dispositivo o conecta los dos en la banda de 5 GHz.')}),
 ('ok', None,
  {'pt': ('Tudo certo: o celular e o aparelho estão se falando.', 'A rede, o aparelho, o pareamento e a velocidade passaram.', 'Se ainda assim um botão não funciona, faça o diagnóstico guiado com o problema "Conecta, mas não obedece".'),
   'en': ('All good: the phone and the device are talking.', 'Network, device, pairing and speed all passed.', 'If a button still does not work, run the guided check with the problem "Connects but doesn’t respond".'),
   'es': ('Todo bien: el celular y el dispositivo se están comunicando.', 'La red, el dispositivo, el emparejamiento y la velocidad pasaron.', 'Si aun así un botón no funciona, haz el diagnóstico guiado con el problema "Se conecta pero no responde".')}),
]
TEST_TXT = {
 'pt': dict(h='Entenda o resultado do Testar conexão', lead='O Testar conexão (na faixa verde de conexão, ou na aba Mais, em Ajuda e suporte) confere em ordem: Wi-Fi, aparelho salvo, mesma rede, resposta do aparelho, pareamento e velocidade. O título mostra o primeiro problema encontrado. Procure abaixo o título que apareceu no seu celular.',
           todo='O que fazer', diag='Abrir o diagnóstico guiado', more='Abaixo do resultado ficam sempre Testar de novo e Enviar com relato, que manda o resultado junto com o seu relato. Linhas que dizem "Não testado porque uma etapa anterior falhou" somem quando o primeiro problema é resolvido. As linhas sobre as portas 6466 e 5555 são só informação para o suporte.'),
 'en': dict(h='Understand the Test connection result', lead='Test connection (on the green connection bar, or in the More tab, under Help and support) checks in order: Wi-Fi, saved device, same network, device answer, pairing and speed. The title shows the first problem found. Find the title you saw on your phone below.',
           todo='What to do', diag='Open the guided check', more='Under the result you always see Test again and Send with a report, which attaches the result to your report. Lines saying "Not tested because an earlier step failed" go away once the first problem is fixed. Lines about ports 6466 and 5555 are information for support only.'),
 'es': dict(h='Entiende el resultado de Probar conexión', lead='Probar conexión (en la barra verde de conexión, o en la pestaña Más, en Ayuda y soporte) revisa en orden: Wi-Fi, dispositivo guardado, misma red, respuesta del dispositivo, emparejamiento y velocidad. El título muestra el primer problema encontrado. Busca abajo el título que viste en tu celular.',
           todo='Qué hacer', diag='Abrir el diagnóstico guiado', more='Debajo del resultado siempre aparecen Probar de nuevo y Enviar con un informe, que adjunta el resultado a tu reporte. Las líneas que dicen "No probado porque falló un paso anterior" desaparecen cuando se resuelve el primer problema. Las líneas sobre los puertos 6466 y 5555 son solo información para soporte.'),
}
# Assunto do Relatar por problema (Reports.java, via Grok).
REPORT_SUBJECT = {'nao-aparece': 'connect', 'codigo': 'connect', 'cai': 'connect', 'nao-obedece': 'button', 'nao-liga': 'button', 'texto': 'button'}
SUBJECT_TXT = {'connect': {'pt': 'Não consigo conectar o aparelho', 'en': 'I cannot connect the device', 'es': 'No puedo conectar el dispositivo'},
               'button': {'pt': 'Um botão ou função não funciona', 'en': 'A button or function does not work', 'es': 'Un botón o función no funciona'}}
SUBJECT_LINE = {'pt': 'No formulário, escolha o assunto “{s}” e informe a marca e o modelo.', 'en': 'In the form, choose the subject “{s}” and give the brand and model.', 'es': 'En el formulario, elige el asunto “{s}” e indica la marca y el modelo.'}


# Títulos de ação para os passos do diagnóstico (o texto embaixo continua vindo do FAQ do app).
ACTION_TITLE = {
 'tv-nao-aparece': ('Confira se o aparelho está ligado e na mesma rede', 'Check that the device is on and on the same network', 'Comprueba que el dispositivo esté encendido y en la misma red'),
 'ip-da-tv': ('Conecte pelo IP do aparelho (botão Usar IP)', 'Connect with the device’s IP (Use IP button)', 'Conecta con la IP del dispositivo (botón Usar IP)'),
 'marca-fora': ('Veja se o aparelho usa Roku ou Android TV por dentro', 'Check whether the device runs Roku or Android TV inside', 'Mira si el dispositivo usa Roku o Android TV por dentro'),
 'vestel': ('Tente como Vestel, pelo IP', 'Try it as Vestel, by IP', 'Prueba como Vestel, por IP'),
 'codigo-pin': ('Digite o código exatamente como aparece no aparelho', 'Type the code exactly as it shows on the device', 'Escribe el código tal como aparece en el dispositivo'),
 'samsung-permissao': ('Faça a Samsung pedir permissão só na primeira vez', 'Make the Samsung ask for permission only the first time', 'Haz que la Samsung pida permiso solo la primera vez'),
 'lg-permissao': ('Refaça o pareamento com a LG', 'Pair the LG again', 'Vuelve a emparejar la LG'),
 'mesma-rede': ('Tire o celular da rede de visitantes ou dos dados móveis', 'Move the phone off the guest network or mobile data', 'Saca el celular de la red de invitados o de los datos móviles'),
 'botao-desativado': ('Entenda os botões apagados', 'Understand greyed-out buttons', 'Entiende los botones en gris'),
 'roku-limitado': ('Libere o controle por apps na Roku', 'Allow control by mobile apps on the Roku', 'Habilita el control por apps en la Roku'),
 'conexao-cai': ('Deixe o app sem restrição de bateria', 'Remove battery restrictions for the app', 'Quita las restricciones de batería de la app'),
 'ligar-tv': ('Ative a opção de ligar pela rede', 'Turn on the power-on-over-network option', 'Activa la opción de encender por la red'),
 'digitar': ('Use a aba Digitar com o campo aberto no aparelho', 'Use the Type tab with the field open on the device', 'Usa la pestaña Escribir con el campo abierto en el dispositivo'),
}


def esc(s):
    return html.escape(s, quote=True)


def faq_step(fid, lang):
    q, a = G.fq(fid, lang)
    t = ACTION_TITLE.get(fid)
    return {'t': t[LI[lang]] if t else q, 'h': a}


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
            rel = faq_step('relatar', lang)
            subj = SUBJECT_TXT[REPORT_SUBJECT[sid]][lang]
            rel['h'] += '<p>' + esc(SUBJECT_LINE[lang].format(s=subj)) + '</p>'
            out.append(dict(rel, t=U['last']))
            per[sid] = out
        data[b['id']] = per
    return data


def test_section(lang):
    X, UI = TEST_TXT[lang], C.UI[lang]
    rows = ''
    for tid, sym, txt in TEST_RESULTS:
        title, detail, todo = txt[lang]
        link = (f'<p><a href="{UI["help"]}?problema={sym}#diagnostico">{X["diag"]}</a></p>' if sym else '')
        rows += (f'<details id="teste-{tid}"><summary>“{esc(title)}”<a class="anchor" href="#teste-{tid}" aria-label="Link">#</a></summary>'
                 f'<div><p>{esc(detail)}</p><p><strong>{X["todo"]}:</strong> {esc(todo)}</p>{link}</div></details>')
    return (f'<section class="prose faqall" id="testar-conexao" aria-labelledby="th"><h2 id="th">{X["h"]}</h2><p>{X["lead"]}</p>'
            f'<div class="prob">{rows}</div><p>{X["more"]}</p></section>')


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
{test_section(lang)}
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


NOT_FOUND = {
 'pt': ('Esta página não existe', 'O endereço pode ter mudado ou ter um erro de digitação. Estes caminhos levam ao que você procura:', 'Início', 'Guias', 'Central de ajuda'),
 'en': ('This page doesn’t exist', 'The address may have changed or have a typo. These links take you where you need to go:', 'Home', 'Guides', 'Help center'),
 'es': ('Esta página no existe', 'La dirección pudo cambiar o tener un error. Estos enlaces te llevan a lo que buscas:', 'Inicio', 'Guías', 'Centro de ayuda'),
}


def render_404():
    blocks = ''
    for lang in LANGS:
        h, p, a, b, c = NOT_FOUND[lang]
        UI = C.UI[lang]
        blocks += (f'<section class="nf" lang="{UI["html_lang"]}" data-l="{lang}"{"" if lang == "pt" else " hidden"}><h1>{h}</h1><p class="answer">{p}</p>'
                   f'<div class="cta"><a class="pill pill-dark" href="{UI["home"]}">{a}</a><a class="pill pill-soft" href="{UI["guides"]}">{b}</a>'
                   f'<a class="pill pill-soft" href="{UI["help"]}">{c}</a></div></section>')
    switch = ''.join(f'<a href="#" data-to="{l}" hreflang="{l}" lang="{l}">{l.upper()}</a>' for l in LANGS)
    js = """<script>(function(){var p=location.pathname,l=p.indexOf('/en/')===0?'en':p.indexOf('/es/')===0?'es':'';
if(!l){var n=(navigator.language||'pt').slice(0,2);l=(n==='en'||n==='es')?n:'pt';}
function show(x){document.querySelectorAll('.nf').forEach(function(s){s.hidden=s.getAttribute('data-l')!==x;});
document.querySelectorAll('[data-to]').forEach(function(a){if(a.getAttribute('data-to')===x)a.setAttribute('aria-current','page');else a.removeAttribute('aria-current');});
document.documentElement.lang=x==='pt'?'pt-BR':x;}
document.querySelectorAll('[data-to]').forEach(function(a){a.addEventListener('click',function(e){e.preventDefault();show(a.getAttribute('data-to'));});});show(l);})();</script>"""
    return f"""<!doctype html>
<html lang="pt-BR">
<head>
<meta charset="utf-8">
<meta name="viewport" content="width=device-width, initial-scale=1, viewport-fit=cover">
<title>Página não encontrada · Comandoo</title>
<meta name="robots" content="noindex">
<meta name="theme-color" content="#A9ED87">
<link rel="icon" href="/favicon.svg" type="image/svg+xml">
<link rel="stylesheet" href="/assets/site.css">
<link rel="stylesheet" href="/assets/guide.css">
</head>
<body>
<div class="gtop"><div class="wrap">
<header class="top"><a class="brand" href="/">{B.sym('#0E120F')}Comandoo</a><nav class="gnav" aria-label="Idioma / Language"><span class="seg">{switch}</span></nav></header>
<div class="ghead">{blocks}</div>
</div></div>
{js}
</body>
</html>
"""


def main():
    for lang in LANGS:
        G.write(C.UI[lang]['help'].strip('/') + '/index.html', render(lang))
    G.write('404.html', render_404())
    G.main(extra=[{l: SITE + C.UI[l]['help'] for l in LANGS}])
    print('ajuda ok')


if __name__ == '__main__':
    main()
