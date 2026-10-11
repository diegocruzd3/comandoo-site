#!/usr/bin/env python3
"""Gera a home do Comandoo em pt, en e es a partir de um único modelo.

Uso: python3 tools/build.py   (na raiz do repositório)

Quando o app estiver publicado, preencha PLAY_URL: o botão "Em breve"
vira o botão de download nas três línguas.
"""
import json
from pathlib import Path

PLAY_URL = None  # ex.: "https://play.google.com/store/apps/details?id=app.comandoo"
SITE = "https://comandoo.online"
ROOT = Path(__file__).resolve().parent.parent

LOGO = ('<svg viewBox="0 0 32 32" aria-hidden="true"><rect width="32" height="32" rx="9" fill="#a9ed87"/>'
        '<circle cx="16" cy="16" r="9" fill="none" stroke="#0f1a0b" stroke-width="2.6"/>'
        '<circle cx="16" cy="16" r="3.2" fill="#0f1a0b"/></svg>')

ARROW = {
    'u': '<path d="M6 15l6-6 6 6"/>', 'd': '<path d="M6 9l6 6 6-6"/>',
    'l': '<path d="M15 6l-6 6 6 6"/>', 'r': '<path d="M9 6l6 6-6 6"/>',
}
def arrow(k):
    return ('<svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2.4" '
            'stroke-linecap="round" stroke-linejoin="round" aria-hidden="true">' + ARROW[k] + '</svg>')

ICONS = {
    'pad': '<circle cx="12" cy="12" r="9"/><circle cx="12" cy="12" r="3"/>',
    'touch': '<rect x="3" y="5" width="18" height="14" rx="3"/><path d="M12 9v6M9 12h6"/>',
    'keyboard': '<rect x="2.5" y="6" width="19" height="12" rx="2.5"/><path d="M6 10h.01M10 10h.01M14 10h.01M18 10h.01M7 14h10"/>',
    'voice': '<rect x="9" y="3" width="6" height="11" rx="3"/><path d="M5 11a7 7 0 0 0 14 0M12 18v3"/>',
    'apps': '<rect x="4" y="4" width="6.5" height="6.5" rx="1.5"/><rect x="13.5" y="4" width="6.5" height="6.5" rx="1.5"/><rect x="4" y="13.5" width="6.5" height="6.5" rx="1.5"/><rect x="13.5" y="13.5" width="6.5" height="6.5" rx="1.5"/>',
    'volume': '<path d="M4 10v4h4l5 4V6L8 10H4z"/><path d="M16.5 8.5a5 5 0 0 1 0 7M19 6a8.5 8.5 0 0 1 0 12"/>',
}
def icon(k):
    return ('<svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="1.8" '
            'stroke-linecap="round" stroke-linejoin="round" aria-hidden="true">' + ICONS[k] + '</svg>')

T = {
 'pt': dict(
  path='/', html_lang='pt-BR', og_locale='pt_BR', label='Português', short='PT',
  title='Comandoo — Controle remoto para Smart TV no celular',
  desc='Use o celular como controle remoto da Smart TV pelo Wi-Fi. LG webOS, Samsung, Roku, Android TV e mais. Sem anúncios e sem cadastro.',
  skip='Pular para o conteúdo',
  h1='Seu celular vira o controle da TV.',
  lead='Pelo Wi-Fi de casa, sem instalar nada na TV. Sem anúncios e sem cadastro.',
  soon='Em breve no Google Play', play='Baixar no Google Play', how_link='Como funciona',
  facts=['Grátis e sem anúncios', 'Sem conta nem login', 'Português, inglês e espanhol'],
  demo_label='Demonstração do controle: use as setas para navegar pela TV',
  demo_hint='Experimente: toque nas setas do celular.',
  demo_open='Abrindo', demo_home='Tela inicial', tv_head='Início',
  tiles=['Filmes', 'Séries', 'Música', 'Esportes', 'Fotos', 'Ajustes'],
  k_vdown='Diminuir volume', k_home='Início', k_vup='Aumentar volume',
  k_up='Para cima', k_down='Para baixo', k_left='Para a esquerda', k_right='Para a direita',
  how_h='Pronto em menos de um minuto.',
  how_sub='Nada de cabo, receptor ou app na TV. O celular conversa com a TV pela sua própria rede.',
  steps=[('Mesma rede', 'Conecte o celular no mesmo Wi-Fi em que a TV está.'),
         ('Escolha a TV', 'Abra o Comandoo. Ele procura as TVs da casa e mostra a lista.'),
         ('Confirme na TV', 'Aceite o pedido que aparece na tela. Algumas TVs pedem um código.')],
  how_note='Só funciona com o celular na mesma rede da TV: pelo 4G ou fora de casa, não.',
  feat_h='Tudo o que o controle faz, e um pouco mais.',
  feats=[('pad', 'Direcional e botão OK', 'Navegue pelos menus como no controle de verdade.'),
         ('touch', 'Touchpad', 'Deslize o dedo para mover o cursor nas TVs que têm ponteiro.'),
         ('volume', 'Volume, canais e teclas coloridas', 'Inclusive mudo, voltar, início e as teclas vermelha, verde, amarela e azul.'),
         ('keyboard', 'Teclado do celular', 'Digite senhas e buscas na TV sem catar letra por letra.'),
         ('voice', 'Comando de voz', 'Fale a busca em vez de digitar.'),
         ('apps', 'Apps da TV com um toque', 'Abra seus aplicativos da TV direto do celular.')],
  ex_h='Atalhos para o dia a dia',
  ex_sub='Estes extras vêm liberados no lançamento.',
  extras=[('Botão flutuante', 'O controle por cima de outros apps, sem sair do que você está fazendo.'),
          ('Widget e atalhos rápidos', 'Comandos da TV na tela inicial e na barra de notificações.'),
          ('Fotos e vídeos na TV', 'Mostre na tela grande o que está no celular, pela rede de casa.'),
          ('Timer para desligar', 'Programe a TV para desligar sozinha.')],
  comp_h='Funciona com as principais marcas.',
  comp_sub='Testamos a fundo nas TVs LG. Nas outras marcas o Comandoo já funciona na maioria dos modelos, mas ainda pode ter limitações.',
  comp_th=('Plataforma', 'Situação'), ok='Testado', beta='Beta',
  comp_note='Encontrou um problema com a sua TV? Envie um relato pelo próprio app ou escreva para',
  priv_h='Seus dados ficam com você.',
  priv_sub='O resumo está aqui. O texto completo, com tudo o que o app usa, está na',
  priv_link='política de privacidade',
  priv=[('Os comandos ficam na sua rede', 'Vão direto do celular para a TV pelo Wi-Fi, sem passar pela internet.'),
        ('Sem conta, sem anúncios', 'Você não cria login, e o app não usa identificador de publicidade.'),
        ('Voz pelo próprio Android', 'O comando de voz usa o reconhecimento de fala do celular. O app recebe só o texto.'),
        ('Relatos só quando você envia', 'Se mandar um relato, ele vai com dados técnicos, e o app oculta IPs e e-mails antes.')],
  faq_h='Perguntas frequentes',
  faq=[('Preciso instalar alguma coisa na TV?', 'Não. O Comandoo usa os recursos de rede que a própria TV já tem. Basta a TV estar ligada e no mesmo Wi-Fi do celular.'),
       ('Funciona pelo 4G ou fora de casa?', 'Não. O celular precisa estar na mesma rede Wi-Fi da TV, porque os comandos vão direto de um aparelho para o outro.'),
       ('Minha TV não aparece na lista. O que faço?', 'Confira se a TV está ligada e se os dois aparelhos estão no mesmo Wi-Fi (alguns roteadores separam a rede de 2,4 GHz e a de 5 GHz). Se ainda não aparecer, envie um relato pelo app com a marca e o modelo da TV.'),
       ('O app é pago?', 'Não. O controle é gratuito e não tem anúncios. No futuro, alguns recursos extras poderão fazer parte de um plano opcional, mas o controle básico continua grátis para sempre.'),
       ('Funciona com qualquer TV?', 'Funciona com Smart TVs conectadas ao Wi-Fi das plataformas listadas acima. TVs sem conexão à rede, ou que só aceitam controle infravermelho, não funcionam.'),
       ('Quem faz o Comandoo?', 'A Agência D3, de Belém do Pará. O Comandoo é um app independente, sem vínculo com fabricantes de TV.')],
  close_h='Deixe o controle no sofá.',
  close_sub='O Comandoo chega em breve ao Google Play.',
  close_sub_live='Baixe grátis no Google Play.',
  f_priv='Política de privacidade', f_contact='Contato', f_indep='Comandoo é um app independente, sem vínculo com fabricantes de TV.',
  priv_url='/privacidade'),
 'en': dict(
  path='/en/', html_lang='en', og_locale='en_US', label='English', short='EN',
  title='Comandoo — Smart TV remote control on your phone',
  desc='Use your phone as a Smart TV remote over Wi-Fi. LG webOS, Samsung, Roku, Android TV and more. No ads, no sign-up.',
  skip='Skip to content',
  h1='Your phone becomes the TV remote.',
  lead='Over your home Wi-Fi, with nothing to install on the TV. No ads and no sign-up.',
  soon='Coming soon to Google Play', play='Get it on Google Play', how_link='How it works',
  facts=['Free with no ads', 'No account or login', 'English, Portuguese and Spanish'],
  demo_label='Remote demo: use the arrows to move around the TV',
  demo_hint='Try it: tap the arrows on the phone.',
  demo_open='Opening', demo_home='Home screen', tv_head='Home',
  tiles=['Movies', 'Series', 'Music', 'Sports', 'Photos', 'Settings'],
  k_vdown='Volume down', k_home='Home', k_vup='Volume up',
  k_up='Up', k_down='Down', k_left='Left', k_right='Right',
  how_h='Ready in under a minute.',
  how_sub='No cables, no receiver, no app on the TV. Your phone talks to the TV over your own network.',
  steps=[('Same network', 'Connect your phone to the same Wi-Fi as the TV.'),
         ('Pick your TV', 'Open Comandoo. It finds the TVs in your home and lists them.'),
         ('Confirm on the TV', 'Accept the request on screen. Some TVs ask for a code.')],
  how_note='Your phone must be on the same network as the TV: it won’t work over mobile data or away from home.',
  feat_h='Everything your remote does, and a bit more.',
  feats=[('pad', 'D-pad and OK button', 'Move through menus just like the real remote.'),
         ('touch', 'Touchpad', 'Swipe to move the pointer on TVs that have one.'),
         ('volume', 'Volume, channels and color keys', 'Plus mute, back, home and the red, green, yellow and blue keys.'),
         ('keyboard', 'Phone keyboard', 'Type passwords and searches without hunting letter by letter.'),
         ('voice', 'Voice search', 'Say your search instead of typing it.'),
         ('apps', 'TV apps in one tap', 'Launch your TV apps straight from the phone.')],
  ex_h='Shortcuts for every day',
  ex_sub='These extras are unlocked at launch.',
  extras=[('Floating button', 'The remote on top of other apps, without leaving what you’re doing.'),
          ('Widget and quick settings', 'TV controls on your home screen and in the notification shade.'),
          ('Photos and videos on the TV', 'Show what’s on your phone on the big screen, over your home network.'),
          ('Sleep timer', 'Set the TV to turn itself off.')],
  comp_h='Works with the major brands.',
  comp_sub='Fully tested on LG TVs. On other brands Comandoo already works with most models, but may still have limitations.',
  comp_th=('Platform', 'Status'), ok='Tested', beta='Beta',
  comp_note='Found a problem with your TV? Send a report from inside the app or write to',
  priv_h='Your data stays with you.',
  priv_sub='Here’s the short version. The full text, covering everything the app uses, is in the',
  priv_link='privacy policy',
  priv=[('Commands stay on your network', 'They go straight from phone to TV over Wi-Fi, never through the internet.'),
        ('No account, no ads', 'There’s no login, and the app doesn’t use the advertising ID.'),
        ('Voice through Android itself', 'Voice search uses your phone’s speech recognition. The app only receives the text.'),
        ('Reports only when you send them', 'If you send a report, it includes technical details, and the app hides IPs and e-mails first.')],
  faq_h='Frequently asked questions',
  faq=[('Do I need to install anything on the TV?', 'No. Comandoo uses the network features your TV already has. The TV just needs to be on and on the same Wi-Fi as your phone.'),
       ('Does it work over mobile data or away from home?', 'No. Your phone has to be on the same Wi-Fi as the TV, because commands go directly from one device to the other.'),
       ('My TV doesn’t show up. What should I do?', 'Check that the TV is on and that both devices are on the same Wi-Fi (some routers split 2.4 GHz and 5 GHz into separate networks). If it still doesn’t appear, send a report from the app with your TV’s brand and model.'),
       ('Is the app paid?', 'No. The remote is free and has no ads. In the future, some extra features may become part of an optional plan, but the basic remote stays free forever.'),
       ('Does it work with any TV?', 'It works with Wi-Fi-connected Smart TVs on the platforms listed above. TVs without a network connection, or that only accept infrared remotes, won’t work.'),
       ('Who makes Comandoo?', 'Agência D3, from Belém, Brazil. Comandoo is an independent app with no ties to any TV manufacturer.')],
  close_h='Leave the remote on the couch.',
  close_sub='Comandoo is coming soon to Google Play.',
  close_sub_live='Get it free on Google Play.',
  f_priv='Privacy policy', f_contact='Contact', f_indep='Comandoo is an independent app with no ties to any TV manufacturer.',
  priv_url='/privacidade/en'),
 'es': dict(
  path='/es/', html_lang='es', og_locale='es_ES', label='Español', short='ES',
  title='Comandoo — Control remoto para Smart TV en el celular',
  desc='Usa el celular como control remoto de la Smart TV por Wi-Fi. LG webOS, Samsung, Roku, Android TV y más. Sin anuncios y sin registro.',
  skip='Saltar al contenido',
  h1='Tu celular se convierte en el control de la TV.',
  lead='Por el Wi-Fi de casa, sin instalar nada en la TV. Sin anuncios y sin registro.',
  soon='Próximamente en Google Play', play='Descárgalo en Google Play', how_link='Cómo funciona',
  facts=['Gratis y sin anuncios', 'Sin cuenta ni inicio de sesión', 'Español, inglés y portugués'],
  demo_label='Demostración del control: usa las flechas para moverte por la TV',
  demo_hint='Pruébalo: toca las flechas del celular.',
  demo_open='Abriendo', demo_home='Pantalla de inicio', tv_head='Inicio',
  tiles=['Películas', 'Series', 'Música', 'Deportes', 'Fotos', 'Ajustes'],
  k_vdown='Bajar volumen', k_home='Inicio', k_vup='Subir volumen',
  k_up='Arriba', k_down='Abajo', k_left='Izquierda', k_right='Derecha',
  how_h='Listo en menos de un minuto.',
  how_sub='Sin cables, sin receptor y sin app en la TV. El celular habla con la TV por tu propia red.',
  steps=[('Misma red', 'Conecta el celular al mismo Wi-Fi que la TV.'),
         ('Elige la TV', 'Abre Comandoo. Busca las TVs de tu casa y te muestra la lista.'),
         ('Confirma en la TV', 'Acepta la solicitud que aparece en pantalla. Algunas TVs piden un código.')],
  how_note='El celular tiene que estar en la misma red que la TV: con datos móviles o fuera de casa no funciona.',
  feat_h='Todo lo que hace tu control, y un poco más.',
  feats=[('pad', 'Cruceta y botón OK', 'Recorre los menús como con el control de verdad.'),
         ('touch', 'Touchpad', 'Desliza el dedo para mover el puntero en las TVs que lo tienen.'),
         ('volume', 'Volumen, canales y teclas de colores', 'También silencio, atrás, inicio y las teclas roja, verde, amarilla y azul.'),
         ('keyboard', 'Teclado del celular', 'Escribe contraseñas y búsquedas sin ir letra por letra.'),
         ('voice', 'Búsqueda por voz', 'Di lo que buscas en vez de escribirlo.'),
         ('apps', 'Apps de la TV con un toque', 'Abre las aplicaciones de la TV directamente desde el celular.')],
  ex_h='Atajos para el día a día',
  ex_sub='Estos extras vienen desbloqueados en el lanzamiento.',
  extras=[('Botón flotante', 'El control encima de otras apps, sin dejar lo que estás haciendo.'),
          ('Widget y ajustes rápidos', 'Comandos de la TV en la pantalla de inicio y en la barra de notificaciones.'),
          ('Fotos y videos en la TV', 'Muestra en la pantalla grande lo que tienes en el celular, por la red de casa.'),
          ('Temporizador de apagado', 'Programa la TV para que se apague sola.')],
  comp_h='Funciona con las principales marcas.',
  comp_sub='Lo probamos a fondo en TVs LG. En las demás marcas Comandoo ya funciona en la mayoría de los modelos, pero todavía puede tener limitaciones.',
  comp_th=('Plataforma', 'Estado'), ok='Probado', beta='Beta',
  comp_note='¿Encontraste un problema con tu TV? Envía un reporte desde la app o escribe a',
  priv_h='Tus datos se quedan contigo.',
  priv_sub='Aquí está el resumen. El texto completo, con todo lo que usa la app, está en la',
  priv_link='política de privacidad',
  priv=[('Los comandos se quedan en tu red', 'Van directo del celular a la TV por Wi-Fi, sin pasar por internet.'),
        ('Sin cuenta, sin anuncios', 'No hay inicio de sesión y la app no usa el identificador de publicidad.'),
        ('Voz con el propio Android', 'La búsqueda por voz usa el reconocimiento de voz del celular. La app solo recibe el texto.'),
        ('Reportes solo si los envías', 'Si envías un reporte, va con datos técnicos, y la app oculta IPs y correos antes.')],
  faq_h='Preguntas frecuentes',
  faq=[('¿Tengo que instalar algo en la TV?', 'No. Comandoo usa las funciones de red que la TV ya tiene. Solo hace falta que la TV esté encendida y en el mismo Wi-Fi que el celular.'),
       ('¿Funciona con datos móviles o fuera de casa?', 'No. El celular tiene que estar en el mismo Wi-Fi que la TV, porque los comandos van directo de un aparato al otro.'),
       ('Mi TV no aparece en la lista. ¿Qué hago?', 'Revisa que la TV esté encendida y que los dos aparatos estén en el mismo Wi-Fi (algunos routers separan la red de 2,4 GHz y la de 5 GHz). Si sigue sin aparecer, envía un reporte desde la app con la marca y el modelo de la TV.'),
       ('¿La app es de pago?', 'No. El control es gratis y no tiene anuncios. En el futuro, algunas funciones extra podrán formar parte de un plan opcional, pero el control básico seguirá gratis para siempre.'),
       ('¿Funciona con cualquier TV?', 'Funciona con Smart TVs conectadas al Wi-Fi de las plataformas de arriba. Las TVs sin conexión a la red, o que solo aceptan control infrarrojo, no funcionan.'),
       ('¿Quién hace Comandoo?', 'Agência D3, de Belém, Brasil. Comandoo es una app independiente, sin vínculo con fabricantes de TV.')],
  close_h='Deja el control en el sofá.',
  close_sub='Comandoo llega pronto a Google Play.',
  close_sub_live='Descárgalo gratis en Google Play.',
  f_priv='Política de privacidad', f_contact='Contacto', f_indep='Comandoo es una app independiente, sin vínculo con fabricantes de TV.',
  priv_url='/privacidade/es'),
}

PLATFORMS = [('LG webOS', 'ok'), ('Samsung', 'beta'), ('Roku', 'beta'),
             ('Android TV / Google TV', 'beta'), ('Amazon Fire TV', 'beta'),
             ('Sony', 'beta'), ('Panasonic', 'beta')]
EMAIL = 'suporte@comandoo.online'


def cta(t, extra=''):
    if PLAY_URL:
        return f'<a class="btn btn-play" href="{PLAY_URL}" rel="noopener">{t["play"]}</a>{extra}'
    return f'<span class="btn btn-soon" role="text">{t["soon"]}</span>{extra}'


def page(lang):
    t = T[lang]
    url = SITE + t['path']
    alts = ''.join(f'<link rel="alternate" hreflang="{l}" href="{SITE}{T[l]["path"]}">' for l in T)
    alts += f'<link rel="alternate" hreflang="x-default" href="{SITE}/">'
    langs = ''.join(
        f'<a href="{T[l]["path"]}" hreflang="{l}" lang="{l}" title="{T[l]["label"]}"'
        + (' aria-current="page"' if l == lang else '') + f'>{T[l]["short"]}</a>' for l in T)
    ld = {
        "@context": "https://schema.org", "@type": "SoftwareApplication",
        "name": "Comandoo", "operatingSystem": "Android",
        "applicationCategory": "UtilitiesApplication", "inLanguage": ["pt-BR", "en", "es"],
        "description": t['desc'], "url": url,
        "offers": {"@type": "Offer", "price": "0", "priceCurrency": "BRL"},
        "publisher": {"@type": "Organization", "name": "Agência D3"},
    }
    if PLAY_URL:
        ld["downloadUrl"] = PLAY_URL
    tiles = ''.join(f'<div class="tile t{i+1}">{n}</div>' for i, n in enumerate(t['tiles']))
    steps = ''.join(f'<li><h3>{h}</h3><p>{p}</p></li>' for h, p in t['steps'])
    feats = ''.join(f'<div class="f">{icon(k)}<div><h3>{h}</h3><p>{p}</p></div></div>' for k, h, p in t['feats'])
    extras = ''.join(f'<li><strong>{h}</strong><span>{p}</span></li>' for h, p in t['extras'])
    rows = ''.join(f'<tr><td>{n}</td><td><span class="st st-{s}">{t[s]}</span></td></tr>' for n, s in PLATFORMS)
    priv = ''.join(f'<li><strong>{h}</strong><span>{p}</span></li>' for h, p in t['priv'])
    faq = ''.join(f'<details><summary>{q}</summary><p>{a}</p></details>' for q, a in t['faq'])
    og = f'{SITE}/assets/og-{lang}.png'
    return f'''<!doctype html>
<html lang="{t['html_lang']}">
<head>
<meta charset="utf-8">
<meta name="viewport" content="width=device-width, initial-scale=1">
<title>{t['title']}</title>
<meta name="description" content="{t['desc']}">
<link rel="canonical" href="{url}">
{alts}
<meta name="theme-color" content="#101511">
<link rel="icon" href="/favicon.svg" type="image/svg+xml">
<link rel="preload" href="/assets/bricolage.woff2" as="font" type="font/woff2" crossorigin>
<meta property="og:type" content="website">
<meta property="og:site_name" content="Comandoo">
<meta property="og:title" content="{t['title']}">
<meta property="og:description" content="{t['desc']}">
<meta property="og:url" content="{url}">
<meta property="og:image" content="{og}">
<meta property="og:image:width" content="1200"><meta property="og:image:height" content="630">
<meta property="og:locale" content="{t['og_locale']}">
<meta name="twitter:card" content="summary_large_image">
<link rel="stylesheet" href="/assets/site.css">
<script type="application/ld+json">{json.dumps(ld, ensure_ascii=False)}</script>
</head>
<body>
<a class="skip" href="#main">{t['skip']}</a>
<div class="wrap">
<header class="top">
  <a class="brand" href="{t['path']}">{LOGO}Comandoo</a>
  <nav class="langs" aria-label="Idioma / Language">{langs}</nav>
</header>
<main id="main">
<div class="hero">
  <div>
    <h1>{t['h1']}</h1>
    <p class="lead">{t['lead']}</p>
    <div class="cta">{cta(t, f'<a class="btn btn-ghost" href="#como">{t["how_link"]}</a>')}</div>
    <ul class="facts">{''.join(f'<li>{f}</li>' for f in t['facts'])}</ul>
  </div>
  <div class="demo" id="demo" role="group" aria-label="{t['demo_label']}" data-open="{t['demo_open']}" data-home="{t['demo_home']}">
    <div class="tv"><div class="screen">
      <div class="screen-head"><span>{t['tv_head']}</span><span>20:30</span></div>
      <div class="tiles">{tiles}</div>
      <div class="vol" aria-hidden="true"><i></i></div>
      <div class="toast" role="status" aria-live="polite"></div>
    </div></div>
    <div class="phone">
      <div class="phone-bar"></div>
      <div class="pad">
        <button class="u" data-k="up" aria-label="{t['k_up']}">{arrow('u')}</button>
        <button class="l" data-k="left" aria-label="{t['k_left']}">{arrow('l')}</button>
        <button class="ok" data-k="ok">OK</button>
        <button class="r" data-k="right" aria-label="{t['k_right']}">{arrow('r')}</button>
        <button class="d" data-k="down" aria-label="{t['k_down']}">{arrow('d')}</button>
      </div>
      <div class="keys">
        <button data-k="voldown" aria-label="{t['k_vdown']}">−</button>
        <button data-k="home" aria-label="{t['k_home']}">⌂</button>
        <button data-k="volup" aria-label="{t['k_vup']}">+</button>
      </div>
    </div>
    <p class="demo-hint">{t['demo_hint']}</p>
  </div>
</div>
</div>

<section id="como"><div class="wrap">
  <h2>{t['how_h']}</h2>
  <p class="sub">{t['how_sub']}</p>
  <ol class="steps">{steps}</ol>
  <p class="note">{t['how_note']}</p>
</div></section>

<section><div class="wrap">
  <h2>{t['feat_h']}</h2>
  <div class="feat">
    <div class="feat-main">{feats}</div>
    <aside class="extras"><h3>{t['ex_h']}</h3><p>{t['ex_sub']}</p><ul>{extras}</ul></aside>
  </div>
</div></section>

<section><div class="wrap">
  <h2>{t['comp_h']}</h2>
  <p class="sub">{t['comp_sub']}</p>
  <div class="compat"><table>
    <thead><tr><th scope="col">{t['comp_th'][0]}</th><th scope="col">{t['comp_th'][1]}</th></tr></thead>
    <tbody>{rows}</tbody>
  </table></div>
  <p class="note">{t['comp_note']} <a href="mailto:{EMAIL}">{EMAIL}</a>.</p>
</div></section>

<section><div class="wrap priv">
  <div>
    <h2>{t['priv_h']}</h2>
    <p class="sub">{t['priv_sub']} <a href="{t['priv_url']}">{t['priv_link']}</a>.</p>
  </div>
  <ul>{priv}</ul>
</div></section>

<section><div class="wrap">
  <h2>{t['faq_h']}</h2>
  <div class="faq">{faq}</div>
</div></section>

<section class="close"><div class="wrap">
  <h2>{t['close_h']}</h2>
  <p class="sub">{t['close_sub_live'] if PLAY_URL else t['close_sub']}</p>
  <div class="cta">{cta(t)}</div>
</div></section>
</main>

<footer><div class="wrap foot">
  <div>
    <p>{t['f_indep']}</p>
    <p>{t['f_contact']}: <a href="mailto:{EMAIL}">{EMAIL}</a></p>
    <p>© 2026 Agência D3</p>
  </div>
  <ul>
    <li><a href="/privacidade">{T['pt']['f_priv']}</a></li>
    <li><a href="/privacidade/en">{T['en']['f_priv']}</a></li>
    <li><a href="/privacidade/es">{T['es']['f_priv']}</a></li>
  </ul>
</div></footer>
<script src="/assets/site.js" defer></script>
</body>
</html>
'''


def main():
    for lang, t in T.items():
        out = ROOT / t['path'].strip('/') / 'index.html' if t['path'] != '/' else ROOT / 'index.html'
        out.parent.mkdir(parents=True, exist_ok=True)
        out.write_text(page(lang), encoding='utf-8')
        print('ok', out.relative_to(ROOT))
    (ROOT / 'favicon.svg').write_text(LOGO.replace(' aria-hidden="true"', ' xmlns="http://www.w3.org/2000/svg"'), encoding='utf-8')


if __name__ == '__main__':
    main()
