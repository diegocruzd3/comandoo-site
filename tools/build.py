#!/usr/bin/env python3
"""Gera a home do Comandoo em pt, en e es a partir de um único modelo.

Uso: python3 tools/build.py   (na raiz do repositório)

Quando o app estiver publicado, preencha PLAY_URL: o botão "Em breve"
vira o botão de download nas três línguas.

Identidade (estudo de marca aprovado em 10/10/2026): símbolo "Anel em C",
variação "Apontando" para site e vídeo, lima #A9ED87 + grafite #0E120F, Figtree.
"""
import json
from pathlib import Path

PLAY_URL = None  # ex.: "https://play.google.com/store/apps/details?id=app.comandoo"
SITE = "https://comandoo.online"
ROOT = Path(__file__).resolve().parent.parent
EMAIL = 'suporte@comandoo.online'

# Símbolo "Anel em C" (glifo final, pontas redondas), viewBox 38 12 44 96.
SYM_D = ("M38,34 A22,22 0 0 1 82,34 L82,86 A22,22 0 0 1 38,86 Z"
         "M72.64,33.39 A16.5,16.5 0 1 0 72.64,54.61 A3.5,3.5 0 0 0 67.28,50.11 A9.5,9.5 0 1 1 67.28,37.89 A3.5,3.5 0 0 0 72.64,33.39 Z"
         "M55.5,44 A4.5,4.5 0 1 0 64.5,44 A4.5,4.5 0 1 0 55.5,44 Z"
         "M48,74 A4,4 0 1 0 56,74 A4,4 0 1 0 48,74 Z M64,74 A4,4 0 1 0 72,74 A4,4 0 1 0 64,74 Z"
         "M48,88 A4,4 0 1 0 56,88 A4,4 0 1 0 48,88 Z M64,88 A4,4 0 1 0 72,88 A4,4 0 1 0 64,88 Z")


def sym(fill='currentColor', label=None):
    a = f'role="img" aria-label="{label}"' if label else 'aria-hidden="true"'
    return f'<svg class="sym" viewBox="38 12 44 96" {a}><path fill="{fill}" fill-rule="evenodd" d="{SYM_D}"/></svg>'


# Variação "Apontando": controle inclinado com o anel em C e o sinal.
def pointing(body='#0E120F', detail='#A9ED87'):
    return (f'<svg class="point" viewBox="0 0 120 120" aria-hidden="true"><g transform="rotate(-30 60 64)">'
            f'<path class="wv" d="M44 24 A24 24 0 0 1 76 24" fill="none" stroke="{body}" stroke-width="6" stroke-linecap="round"/>'
            f'<path class="wv wv2" d="M51 31 A12 12 0 0 1 69 31" fill="none" stroke="{body}" stroke-width="6" stroke-linecap="round"/>'
            f'<rect x="40" y="42" width="40" height="68" rx="18" fill="{body}"/>'
            f'<path d="M68.34 59.18 A10 10 0 1 0 68.34 68.82" fill="none" stroke="{detail}" stroke-width="6" stroke-linecap="round"/>'
            f'<circle cx="60" cy="64" r="3.5" fill="{detail}"/><rect x="52" y="88" width="16" height="6" rx="3" fill="{detail}"/></g></svg>')


P = {  # ícones de linha, 24x24
    'up': '<path d="M6 15l6-6 6 6"/>', 'down': '<path d="M6 9l6 6 6-6"/>',
    'left': '<path d="M15 6l-6 6 6 6"/>', 'right': '<path d="M9 6l6 6-6 6"/>',
    'mic': '<rect x="9" y="3" width="6" height="11" rx="3"/><path d="M5 11a7 7 0 0 0 14 0M12 18v3"/>',
    'power': '<path d="M12 3v9"/><path d="M6.3 6.3a8 8 0 1 0 11.4 0"/>',
    'back': '<path d="M9 14L4 9l5-5"/><path d="M4 9h11a5 5 0 0 1 0 10h-3"/>',
    'home': '<path d="M3 11l9-8 9 8"/><path d="M5 10v10h14V10"/>',
    'input': '<rect x="3" y="4" width="18" height="12" rx="2"/><path d="M8 20h8M12 16v4"/>',
    'mute': '<path d="M4 9v6h4l5 4V5L8 9H4z"/><path d="M17 9l4 6M21 9l-4 6"/>',
    'minus': '<path d="M6 12h12"/>', 'plus': '<path d="M6 12h12M12 6v12"/>',
    'chev': '<path d="M6 9l6 6 6-6"/>',
    'tv': '<rect x="3" y="4" width="18" height="12" rx="2"/><path d="M8 20h8M12 16v4"/>',
    'wifi': '<path d="M2 9a15 15 0 0 1 20 0M5.5 12.5a10 10 0 0 1 13 0M9 16a5 5 0 0 1 6 0"/><circle cx="12" cy="19.5" r="1"/>',
    'check': '<path d="M5 12.5l4.5 4.5L19 7.5"/>',
    'chup': '<path d="M7 14l5-5 5 5"/><path d="M7 19l5-5 5 5" opacity=".45"/>',
    'chdown': '<path d="M7 10l5 5 5-5"/><path d="M7 5l5 5 5-5" opacity=".45"/>',
    'pad': '<circle cx="12" cy="12" r="9"/><circle cx="12" cy="12" r="3"/>',
    'touch': '<rect x="3" y="5" width="18" height="14" rx="3"/><circle cx="12" cy="12" r="2.5"/>',
    'keyboard': '<rect x="2.5" y="6" width="19" height="12" rx="2.5"/><path d="M6 10h.01M10 10h.01M14 10h.01M18 10h.01M7 14h10"/>',
    'apps': '<rect x="4" y="4" width="6.5" height="6.5" rx="1.5"/><rect x="13.5" y="4" width="6.5" height="6.5" rx="1.5"/><rect x="4" y="13.5" width="6.5" height="6.5" rx="1.5"/><rect x="13.5" y="13.5" width="6.5" height="6.5" rx="1.5"/>',
    'volume': '<path d="M4 10v4h4l5 4V6L8 10H4z"/><path d="M16.5 8.5a5 5 0 0 1 0 7M19 6a8.5 8.5 0 0 1 0 12"/>',
}


def ic(k, w=2):
    return (f'<svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="{w}" '
            f'stroke-linecap="round" stroke-linejoin="round" aria-hidden="true">{P[k]}</svg>')


RING = ('<svg class="ring" viewBox="0 0 248 248" aria-hidden="true"><path d="M168.6 102.4 A62 62 0 1 0 168.6 145.6" '
        'fill="none" stroke="#A9ED87" stroke-opacity=".35" stroke-width="3" stroke-linecap="round"/></svg>')


def dpad(t, scope):
    return (f'<div class="dpad">{RING}'
            f'<button class="u" data-{scope}="up" aria-label="{t["k_up"]}">{ic("up", 2.6)}</button>'
            f'<button class="l" data-{scope}="left" aria-label="{t["k_left"]}">{ic("left", 2.6)}</button>'
            f'<button class="ok" data-{scope}="ok">OK</button>'
            f'<button class="r" data-{scope}="right" aria-label="{t["k_right"]}">{ic("right", 2.6)}</button>'
            f'<button class="d" data-{scope}="down" aria-label="{t["k_down"]}">{ic("down", 2.6)}</button></div>')


T = {
 'pt': dict(
  path='/', html_lang='pt-BR', og_locale='pt_BR', label='Português', short='PT',
  title='Comandoo — Controle remoto para Smart TV no celular',
  desc='Use o celular como controle remoto da Smart TV pelo Wi-Fi. LG webOS, Samsung, Roku, Android TV e mais. Sem anúncios e sem cadastro.',
  skip='Pular para o conteúdo', lang_nav='Idioma',
  h1='Seu celular vira o controle da TV.',
  lead='Pelo Wi-Fi de casa, sem instalar nada na TV. Sem anúncios e sem cadastro.',
  soon='Em breve no Google Play', play='Baixar no Google Play', how_link='Como funciona',
  facts=['Grátis e sem anúncios', 'Sem conta', 'PT · EN · ES'],
  stage_label='Demonstração: use o controle do celular para mexer na TV',
  hint='Pode apertar: o controle do celular funciona.',
  tv_head='Início', tv_name='LG · Sala',
  tiles=['Filmes', 'Séries', 'Música', 'Esportes', 'Fotos', 'Ajustes'],
  app_sub='Aberto pelo Comandoo', voice='filmes de comédia',
  o_back='Voltar', o_home='Tela inicial', o_input='Entrada', o_mute='Sem som', o_unmute='Som ligado',
  o_ok='Abrindo', o_off='TV desligada',
  k_up='Para cima', k_down='Para baixo', k_left='Para a esquerda', k_right='Para a direita',
  k_back='Voltar', k_home='Início', k_input='Entradas', k_mute='Mudo', k_vdown='Diminuir volume', k_vup='Aumentar volume',
  k_mic='Falar com a TV', k_power='Ligar ou desligar a TV', k_chip='TV conectada',
  how_h='Pronto em menos de um minuto.',
  how_sub='Nada de cabo, receptor ou app na TV. O celular conversa com a TV pela sua própria rede.',
  steps=[('Mesma rede', 'Conecte o celular no mesmo Wi-Fi em que a TV está.', 'wifi', 'Wi-Fi de casa'),
         ('Escolha a TV', 'Abra o Comandoo. Ele procura as TVs da casa e mostra a lista.', 'chip', 'LG · UQ7500PSF'),
         ('Confirme na TV', 'Aceite o pedido que aparece na tela. Algumas TVs pedem um código.', 'ok', 'Conectado')],
  how_note='Só funciona com o celular na mesma rede da TV: pelo 4G ou fora de casa, não.',
  feat_h='Tudo o que o controle faz, e um pouco mais.',
  feats=[('pad', 'Direcional e OK', 'Navegue pelos menus como no controle de verdade.'),
         ('touch', 'Touchpad', 'Deslize o dedo para mover o cursor nas TVs que têm ponteiro.'),
         ('volume', 'Volume, canais e teclas coloridas', 'Também mudo, voltar, início e as teclas vermelha, verde, amarela e azul.'),
         ('keyboard', 'Teclado do celular', 'Digite senhas e buscas na TV sem catar letra por letra.'),
         ('mic', 'Comando de voz', 'Fale a busca em vez de digitar.'),
         ('apps', 'Apps da TV com um toque', 'Abra os aplicativos da TV direto do celular.')],
  seal='Premium', ex_h='Atalhos para o dia a dia', ex_sub='Recursos Premium, liberados no lançamento.',
  extras=[('Botão flutuante', 'O controle por cima de outros apps, sem sair do que você está fazendo. Tem um aqui no canto da página.'),
          ('Widget e atalhos rápidos', 'Comandos da TV na tela inicial e na barra de notificações.'),
          ('Fotos e vídeos na TV', 'Mostre na tela grande o que está no celular, pela rede de casa.'),
          ('Timer para desligar', 'Programe a TV para desligar sozinha.')],
  comp_h='Funciona com as principais marcas.',
  comp_sub='A LG foi testada em TV real. As outras marcas têm suporte inicial: o app foi feito com base no protocolo de cada uma, mas ainda não foi testado em TV real.',
  list_h='TVs compatíveis', list_n='{n} plataformas', tested='Testado', initial='Suporte inicial', unsupported='Ainda não funciona',
  guides_label='Guias', how_more='Passo a passo completo, com dicas de cada marca', changelog_label='Novidades do app',
  comp_note='Encontrou um problema com a sua TV? Envie um relato pelo próprio app ou escreva para',
  priv_h='Seus dados ficam com você.',
  priv_sub='O resumo está aqui. O texto completo, com tudo o que o app usa, está na',
  priv_link='política de privacidade',
  priv=[('Os comandos ficam na sua rede', 'Vão direto do celular para a TV pelo Wi-Fi, sem passar pela internet.'),
        ('Sem conta, sem anúncios', 'Você não cria login, e o app não usa identificador de publicidade.'),
        ('Voz pelo próprio Android', 'O comando de voz usa o reconhecimento de fala do celular. O app recebe só o texto.'),
        ('Relatos só quando você envia', 'Se mandar um relato, ele vai com dados técnicos, e o app oculta IPs e e-mails antes.'),
        ('Estatísticas só se você quiser', 'Começam desligadas. Se você ligar, vão sem nada que identifique você ou o aparelho.')],
  faq_h='Perguntas frequentes',
  faq=[('Preciso instalar alguma coisa na TV?', 'Não. O Comandoo usa os recursos de rede que a própria TV já tem. Basta a TV estar ligada e no mesmo Wi-Fi do celular.'),
       ('Funciona pelo 4G ou fora de casa?', 'Não. O celular precisa estar na mesma rede Wi-Fi da TV, porque os comandos vão direto de um aparelho para o outro.'),
       ('Minha TV não aparece na lista. O que faço?', 'Confira se a TV está ligada e se os dois aparelhos estão no mesmo Wi-Fi (alguns roteadores separam a rede de 2,4 GHz e a de 5 GHz). Se ainda não aparecer, envie um relato pelo app com a marca e o modelo da TV.'),
       ('O app é pago?', 'Não. O controle é gratuito e não tem anúncios. No futuro, alguns recursos extras poderão fazer parte de um plano opcional, mas o controle básico continua grátis para sempre.'),
       ('Funciona com qualquer TV?', 'Funciona com Smart TVs conectadas ao Wi-Fi das plataformas listadas acima. TVs sem conexão à rede, ou que só aceitam controle infravermelho, não funcionam.'),
       ('Quem faz o Comandoo?', 'A Agência D3, de Belém do Pará. O Comandoo é um app independente, sem vínculo com fabricantes de TV.')],
  close_h='Deixe o controle no sofá.',
  close_sub='O Comandoo chega em breve ao Google Play.', close_sub_live='Baixe grátis no Google Play.',
  f_priv='Política de privacidade', f_contact='Contato', f_indep='Comandoo é um app independente, sem vínculo com fabricantes de TV.',
  priv_url='/privacidade',
  rc_open='Abrir o controle do site', rc_close='Fechar o controle', rc_cap='Controle do site',
  rc_bubble='Este site também tem controle remoto. Toque e navegue pelas setas.',
  rc_back='Topo', rc_prev='Anterior', rc_next='Próxima', rc_power='Desligar o site',
  wake='Ligar o site', wake_txt='Toque para ligar'),
 'en': dict(
  path='/en/', html_lang='en', og_locale='en_US', label='English', short='EN',
  title='Comandoo — Smart TV remote control on your phone',
  desc='Use your phone as a Smart TV remote over Wi-Fi. LG webOS, Samsung, Roku, Android TV and more. No ads, no sign-up.',
  skip='Skip to content', lang_nav='Language',
  h1='Your phone becomes the TV remote.',
  lead='Over your home Wi-Fi, with nothing to install on the TV. No ads and no sign-up.',
  soon='Coming soon to Google Play', play='Get it on Google Play', how_link='How it works',
  facts=['Free with no ads', 'No account', 'EN · PT · ES'],
  stage_label='Demo: use the phone remote to control the TV',
  hint='Go ahead and press: the phone remote works.',
  tv_head='Home', tv_name='LG · Living',
  tiles=['Movies', 'Series', 'Music', 'Sports', 'Photos', 'Settings'],
  app_sub='Opened with Comandoo', voice='comedy movies',
  o_back='Back', o_home='Home screen', o_input='Input', o_mute='Muted', o_unmute='Sound on',
  o_ok='Opening', o_off='TV off',
  k_up='Up', k_down='Down', k_left='Left', k_right='Right',
  k_back='Back', k_home='Home', k_input='Inputs', k_mute='Mute', k_vdown='Volume down', k_vup='Volume up',
  k_mic='Talk to the TV', k_power='Turn the TV on or off', k_chip='Connected TV',
  how_h='Ready in under a minute.',
  how_sub='No cables, no receiver, no app on the TV. Your phone talks to the TV over your own network.',
  steps=[('Same network', 'Connect your phone to the same Wi-Fi as the TV.', 'wifi', 'Home Wi-Fi'),
         ('Pick your TV', 'Open Comandoo. It finds the TVs in your home and lists them.', 'chip', 'LG · UQ7500PSF'),
         ('Confirm on the TV', 'Accept the request on screen. Some TVs ask for a code.', 'ok', 'Connected')],
  how_note='Your phone must be on the same network as the TV: it won’t work over mobile data or away from home.',
  feat_h='Everything your remote does, and a bit more.',
  feats=[('pad', 'D-pad and OK', 'Move through menus just like the real remote.'),
         ('touch', 'Touchpad', 'Swipe to move the pointer on TVs that have one.'),
         ('volume', 'Volume, channels and color keys', 'Plus mute, back, home and the red, green, yellow and blue keys.'),
         ('keyboard', 'Phone keyboard', 'Type passwords and searches without hunting letter by letter.'),
         ('mic', 'Voice search', 'Say your search instead of typing it.'),
         ('apps', 'TV apps in one tap', 'Launch your TV apps straight from the phone.')],
  seal='Premium', ex_h='Shortcuts for every day', ex_sub='Premium features, unlocked at launch.',
  extras=[('Floating button', 'The remote on top of other apps, without leaving what you’re doing. There’s one in the corner of this page.'),
          ('Widget and quick settings', 'TV controls on your home screen and in the notification shade.'),
          ('Photos and videos on the TV', 'Show what’s on your phone on the big screen, over your home network.'),
          ('Sleep timer', 'Set the TV to turn itself off.')],
  comp_h='Works with the major brands.',
  comp_sub='LG was tested on a real TV. The other brands have initial support: the app was built on each one’s protocol, but has not been tested on a real TV yet.',
  list_h='Supported TVs', list_n='{n} platforms', tested='Tested', initial='Initial support', unsupported='Not working yet',
  guides_label='Guides', how_more='Full step by step, with tips for each brand', changelog_label='App updates',
  comp_note='Found a problem with your TV? Send a report from inside the app or write to',
  priv_h='Your data stays with you.',
  priv_sub='Here’s the short version. The full text, covering everything the app uses, is in the',
  priv_link='privacy policy',
  priv=[('Commands stay on your network', 'They go straight from phone to TV over Wi-Fi, never through the internet.'),
        ('No account, no ads', 'There’s no login, and the app doesn’t use the advertising ID.'),
        ('Voice through Android itself', 'Voice search uses your phone’s speech recognition. The app only receives the text.'),
        ('Reports only when you send them', 'If you send a report, it includes technical details, and the app hides IPs and e-mails first.'),
        ('Statistics only if you want', 'They start off. If you turn them on, nothing in them identifies you or your device.')],
  faq_h='Frequently asked questions',
  faq=[('Do I need to install anything on the TV?', 'No. Comandoo uses the network features your TV already has. The TV just needs to be on and on the same Wi-Fi as your phone.'),
       ('Does it work over mobile data or away from home?', 'No. Your phone has to be on the same Wi-Fi as the TV, because commands go directly from one device to the other.'),
       ('My TV doesn’t show up. What should I do?', 'Check that the TV is on and that both devices are on the same Wi-Fi (some routers split 2.4 GHz and 5 GHz into separate networks). If it still doesn’t appear, send a report from the app with your TV’s brand and model.'),
       ('Is the app paid?', 'No. The remote is free and has no ads. In the future, some extra features may become part of an optional plan, but the basic remote stays free forever.'),
       ('Does it work with any TV?', 'It works with Wi-Fi-connected Smart TVs on the platforms listed above. TVs without a network connection, or that only accept infrared remotes, won’t work.'),
       ('Who makes Comandoo?', 'Agência D3, from Belém, Brazil. Comandoo is an independent app with no ties to any TV manufacturer.')],
  close_h='Leave the remote on the couch.',
  close_sub='Comandoo is coming soon to Google Play.', close_sub_live='Get it free on Google Play.',
  f_priv='Privacy policy', f_contact='Contact', f_indep='Comandoo is an independent app with no ties to any TV manufacturer.',
  priv_url='/privacidade/en',
  rc_open='Open the site remote', rc_close='Close the remote', rc_cap='Site remote',
  rc_bubble='This site has a remote too. Tap it and move around with the arrows.',
  rc_back='Top', rc_prev='Previous', rc_next='Next', rc_power='Turn the site off',
  wake='Turn the site on', wake_txt='Tap to turn on'),
 'es': dict(
  path='/es/', html_lang='es', og_locale='es_ES', label='Español', short='ES',
  title='Comandoo — Control remoto para Smart TV en el celular',
  desc='Usa el celular como control remoto de la Smart TV por Wi-Fi. LG webOS, Samsung, Roku, Android TV y más. Sin anuncios y sin registro.',
  skip='Saltar al contenido', lang_nav='Idioma',
  h1='Tu celular se convierte en el control de la TV.',
  lead='Por el Wi-Fi de casa, sin instalar nada en la TV. Sin anuncios y sin registro.',
  soon='Próximamente en Google Play', play='Descárgalo en Google Play', how_link='Cómo funciona',
  facts=['Gratis y sin anuncios', 'Sin cuenta', 'ES · EN · PT'],
  stage_label='Demostración: usa el control del celular para manejar la TV',
  hint='Adelante, presiona: el control del celular funciona.',
  tv_head='Inicio', tv_name='LG · Sala',
  tiles=['Películas', 'Series', 'Música', 'Deportes', 'Fotos', 'Ajustes'],
  app_sub='Abierto con Comandoo', voice='películas de comedia',
  o_back='Atrás', o_home='Pantalla de inicio', o_input='Entrada', o_mute='Sin sonido', o_unmute='Sonido activado',
  o_ok='Abriendo', o_off='TV apagada',
  k_up='Arriba', k_down='Abajo', k_left='Izquierda', k_right='Derecha',
  k_back='Atrás', k_home='Inicio', k_input='Entradas', k_mute='Silencio', k_vdown='Bajar volumen', k_vup='Subir volumen',
  k_mic='Hablar con la TV', k_power='Encender o apagar la TV', k_chip='TV conectada',
  how_h='Listo en menos de un minuto.',
  how_sub='Sin cables, sin receptor y sin app en la TV. El celular habla con la TV por tu propia red.',
  steps=[('Misma red', 'Conecta el celular al mismo Wi-Fi que la TV.', 'wifi', 'Wi-Fi de casa'),
         ('Elige la TV', 'Abre Comandoo. Busca las TVs de tu casa y te muestra la lista.', 'chip', 'LG · UQ7500PSF'),
         ('Confirma en la TV', 'Acepta la solicitud que aparece en pantalla. Algunas TVs piden un código.', 'ok', 'Conectada')],
  how_note='El celular tiene que estar en la misma red que la TV: con datos móviles o fuera de casa no funciona.',
  feat_h='Todo lo que hace tu control, y un poco más.',
  feats=[('pad', 'Cruceta y OK', 'Recorre los menús como con el control de verdad.'),
         ('touch', 'Touchpad', 'Desliza el dedo para mover el puntero en las TVs que lo tienen.'),
         ('volume', 'Volumen, canales y teclas de colores', 'También silencio, atrás, inicio y las teclas roja, verde, amarilla y azul.'),
         ('keyboard', 'Teclado del celular', 'Escribe contraseñas y búsquedas sin ir letra por letra.'),
         ('mic', 'Búsqueda por voz', 'Di lo que buscas en vez de escribirlo.'),
         ('apps', 'Apps de la TV con un toque', 'Abre las aplicaciones de la TV directamente desde el celular.')],
  seal='Premium', ex_h='Atajos para el día a día', ex_sub='Funciones Premium, desbloqueadas en el lanzamiento.',
  extras=[('Botón flotante', 'El control encima de otras apps, sin dejar lo que estás haciendo. Hay uno en la esquina de esta página.'),
          ('Widget y ajustes rápidos', 'Comandos de la TV en la pantalla de inicio y en la barra de notificaciones.'),
          ('Fotos y videos en la TV', 'Muestra en la pantalla grande lo que tienes en el celular, por la red de casa.'),
          ('Temporizador de apagado', 'Programa la TV para que se apague sola.')],
  comp_h='Funciona con las principales marcas.',
  comp_sub='LG se probó en una TV real. Las demás marcas tienen soporte inicial: la app se hizo con el protocolo de cada una, pero aún no se probó en una TV real.',
  list_h='TVs compatibles', list_n='{n} plataformas', tested='Probado', initial='Soporte inicial', unsupported='Aún no funciona',
  guides_label='Guías', how_more='Paso a paso completo, con consejos de cada marca', changelog_label='Novedades de la app',
  comp_note='¿Encontraste un problema con tu TV? Envía un reporte desde la app o escribe a',
  priv_h='Tus datos se quedan contigo.',
  priv_sub='Aquí está el resumen. El texto completo, con todo lo que usa la app, está en la',
  priv_link='política de privacidad',
  priv=[('Los comandos se quedan en tu red', 'Van directo del celular a la TV por Wi-Fi, sin pasar por internet.'),
        ('Sin cuenta, sin anuncios', 'No hay inicio de sesión y la app no usa el identificador de publicidad.'),
        ('Voz con el propio Android', 'La búsqueda por voz usa el reconocimiento de voz del celular. La app solo recibe el texto.'),
        ('Reportes solo si los envías', 'Si envías un reporte, va con datos técnicos, y la app oculta IPs y correos antes.'),
        ('Estadísticas solo si quieres', 'Empiezan desactivadas. Si las activas, no llevan nada que te identifique a ti ni al aparato.')],
  faq_h='Preguntas frecuentes',
  faq=[('¿Tengo que instalar algo en la TV?', 'No. Comandoo usa las funciones de red que la TV ya tiene. Solo hace falta que la TV esté encendida y en el mismo Wi-Fi que el celular.'),
       ('¿Funciona con datos móviles o fuera de casa?', 'No. El celular tiene que estar en el mismo Wi-Fi que la TV, porque los comandos van directo de un aparato al otro.'),
       ('Mi TV no aparece en la lista. ¿Qué hago?', 'Revisa que la TV esté encendida y que los dos aparatos estén en el mismo Wi-Fi (algunos routers separan la red de 2,4 GHz y la de 5 GHz). Si sigue sin aparecer, envía un reporte desde la app con la marca y el modelo de la TV.'),
       ('¿La app es de pago?', 'No. El control es gratis y no tiene anuncios. En el futuro, algunas funciones extra podrán formar parte de un plan opcional, pero el control básico seguirá gratis para siempre.'),
       ('¿Funciona con cualquier TV?', 'Funciona con Smart TVs conectadas al Wi-Fi de las plataformas de arriba. Las TVs sin conexión a la red, o que solo aceptan control infrarrojo, no funcionan.'),
       ('¿Quién hace Comandoo?', 'Agência D3, de Belém, Brasil. Comandoo es una app independiente, sin vínculo con fabricantes de TV.')],
  close_h='Deja el control en el sofá.',
  close_sub='Comandoo llega pronto a Google Play.', close_sub_live='Descárgalo gratis en Google Play.',
  f_priv='Política de privacidad', f_contact='Contacto', f_indep='Comandoo es una app independiente, sin vínculo con fabricantes de TV.',
  priv_url='/privacidade/es',
  rc_open='Abrir el control del sitio', rc_close='Cerrar el control', rc_cap='Control del sitio',
  rc_bubble='Este sitio también tiene control remoto. Tócalo y muévete con las flechas.',
  rc_back='Arriba', rc_prev='Anterior', rc_next='Siguiente', rc_power='Apagar el sitio',
  wake='Encender el sitio', wake_txt='Toca para encender'),
}



# Lista de compatibilidade: fonte única é o compat.json do repositório de versões.
RELEASES = Path('/home/claude/diegocruzd3/controley-releases')


def _compat():
    import subprocess, urllib.request
    try:
        subprocess.run(['git', '-C', str(RELEASES), 'pull', '-q'], check=False, timeout=60)
        return json.loads((RELEASES / 'compat.json').read_text(encoding='utf-8'))
    except Exception:
        with urllib.request.urlopen('https://raw.githubusercontent.com/diegocruzd3/controley-releases/main/compat.json', timeout=30) as r:
            return json.loads(r.read().decode('utf-8'))


_ORDER = {'tested': 0, 'initial': 1, 'unsupported': 2}
COMPAT_ROWS = sorted(_compat()['brands'], key=lambda b: _ORDER.get(b['status'], 3))
SUF = {'pt': '', 'en': '_en', 'es': '_es'}
LI = {'pt': 0, 'en': 1, 'es': 2}
GUIDES = {'pt': '/guias/', 'en': '/en/guides/', 'es': '/es/guias/'}
CHANGELOG = {'pt': '/changelog/', 'en': '/en/changelog/', 'es': '/es/changelog/'}
PILLAR = {'pt': 'celular-como-controle-remoto', 'en': 'phone-as-tv-remote', 'es': 'celular-como-control-remoto'}
BRAND_GUIDES = {'lg': ('controle-remoto-tv-lg', 'lg-tv-remote-app', 'control-remoto-tv-lg'),
                'samsung': ('controle-remoto-tv-samsung', 'samsung-tv-remote-app', 'control-remoto-tv-samsung'),
                'roku': ('controle-remoto-roku', 'roku-remote-app', 'control-remoto-roku'),
                'androidtv': ('controle-remoto-android-tv', 'android-tv-remote-app', 'control-remoto-android-tv'),
                'firetv': ('controle-remoto-fire-tv', 'fire-tv-remote-app', 'control-remoto-fire-tv')}
NAME_TR = {'androidtv': {'en': 'Android TV and Google TV', 'es': 'Android TV y Google TV'},
           'vestel': {'en': 'Vestel (Panasonic, Toshiba, Telefunken and others)', 'es': 'Vestel (Panasonic, Toshiba, Telefunken y otras)'}}
SYS_TR = {
    'lg': {'en': 'LG Smart TVs with webOS', 'es': 'Smart TV LG con webOS'},
    'roku': {'en': 'Roku TVs and Roku players (TCL, Philips, AOC, Semp and other brands with Roku)', 'es': 'Roku TV y reproductores Roku (TCL, Philips, AOC, Semp y otras marcas con Roku)'},
    'samsung': {'en': 'Samsung Smart TVs with Tizen (2016 models and later)', 'es': 'Smart TV Samsung con Tizen (modelos de 2016 en adelante)'},
    'androidtv': {'en': 'Android TV, Google TV, Android TV boxes and Chromecast with Google TV (Sony, TCL, Philips, Xiaomi, Hisense, AOC, Semp and others)', 'es': 'Android TV, Google TV, TV Box con Android TV y Chromecast con Google TV (Sony, TCL, Philips, Xiaomi, Hisense, AOC, Semp y otras)'},
    'firetv': {'en': 'Amazon Fire TV Stick and Fire TV', 'es': 'Fire TV Stick y Fire TV de Amazon'},
    'sony': {'en': 'Sony Bravia with IP Control', 'es': 'Sony Bravia con Control IP'},
    'panasonic': {'en': 'Panasonic Viera: older models without a password and recent ones (around 2019 onward) with a PIN', 'es': 'Panasonic Viera: modelos antiguos sin contraseña y recientes (desde 2019 aprox.) con PIN'},
    'hisense': {'en': 'Hisense with the VIDAA system', 'es': 'Hisense con sistema VIDAA'},
}


def cta(t, nav=True):
    n = ' data-nav' if nav else ''
    if PLAY_URL:
        return f'<a class="pill pill-dark" href="{PLAY_URL}" rel="noopener"{n}>{sym()}{t["play"]}</a>'
    return f'<span class="pill pill-dark pill-soon">{sym()}{t["soon"]}</span>'


def mini(kind, label):
    if kind == 'wifi':
        return f'<div class="mini mini-wifi">{ic("wifi")}{label}</div>'
    if kind == 'chip':
        return f'<div class="mini mini-chip"><i></i>{label}</div>'
    return f'<div class="mini mini-ok">{ic("check", 2.6)}{label}</div>'


def page(lang):
    t = T[lang]
    url = SITE + t['path']
    alts = ''.join(f'<link rel="alternate" hreflang="{l}" href="{SITE}{T[l]["path"]}">' for l in T)
    alts += f'<link rel="alternate" hreflang="x-default" href="{SITE}/">'
    langs = ''.join(
        f'<a href="{T[l]["path"]}" hreflang="{l}" lang="{l}" title="{T[l]["label"]}" data-nav'
        + (' aria-current="page"' if l == lang else '') + f'>{T[l]["short"]}</a>' for l in T)
    ld = {"@context": "https://schema.org", "@type": "SoftwareApplication", "name": "Comandoo",
          "operatingSystem": "Android 8.0+", "applicationCategory": "UtilitiesApplication",
          "inLanguage": ["pt-BR", "en", "es"], "description": t['desc'], "url": url,
          "image": f"{SITE}/assets/icone-512.png",
          "offers": {"@type": "Offer", "price": "0", "priceCurrency": "BRL"},
          "publisher": {"@type": "Organization", "name": "Agência D3"}}
    if PLAY_URL:
        ld["downloadUrl"] = PLAY_URL
    tiles = ''.join(f'<div class="tile t{i+1}">{n}</div>' for i, n in enumerate(t['tiles']))
    steps = ''.join(f'<li tabindex="-1" data-nav><h3>{h}</h3><p>{p}</p>{mini(k, m)}</li>' for h, p, k, m in t['steps'])
    feats = ''.join(f'<div class="fk" tabindex="-1" data-nav><span class="ic">{ic(k)}</span><h3>{h}</h3><p>{p}</p></div>'
                    for k, h, p in t['feats'])
    extras = ''.join(f'<li tabindex="-1" data-nav><strong>{h}</strong><span>{p}</span></li>' for h, p in t['extras'])
    rows = ''
    for b in COMPAT_ROWS:
        st = b['status']
        cls = {'tested': 'ok', 'initial': 'beta', 'unsupported': 'no'}[st]
        sysm = b.get('systems' + SUF[lang]) or SYS_TR.get(b['id'], {}).get(lang) or b['systems']
        inner = f'{ic("tv")}<div><strong>{NAME_TR.get(b["id"], {}).get(lang, b["name"])}</strong><small>{sysm}</small></div><span class="st st-{cls}">{t[st]}</span>'
        g = BRAND_GUIDES.get(b['id'])
        rows += (f'<a class="row {cls}" href="{GUIDES[lang]}{g[LI[lang]]}/" data-nav>{inner}</a>' if g
                 else f'<div class="row {cls}" tabindex="-1" data-nav>{inner}</div>')
    priv = ''.join(f'<li tabindex="-1" data-nav><strong>{h}</strong><span>{p}</span></li>' for h, p in t['priv'])
    faq = ''.join(f'<details><summary data-nav>{q}</summary><p>{a}</p></details>' for q, a in t['faq'])
    strings = {k: t[k] for k in ('o_back', 'o_home', 'o_input', 'o_mute', 'o_unmute', 'o_ok', 'o_off', 'voice', 'app_sub')}
    og = f'{SITE}/assets/og-{lang}.png'
    return f'''<!doctype html>
<html lang="{t['html_lang']}">
<head>
<meta charset="utf-8">
<meta name="viewport" content="width=device-width, initial-scale=1, viewport-fit=cover">
<title>{t['title']}</title>
<meta name="description" content="{t['desc']}">
<link rel="canonical" href="{url}">
{alts}
<meta name="theme-color" content="#A9ED87">
<link rel="icon" href="/favicon.svg" type="image/svg+xml">
<link rel="apple-touch-icon" href="/assets/icone-512.png">
<link rel="preload" href="/assets/figtree.woff2" as="font" type="font/woff2" crossorigin>
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
<div class="band">
<div class="wrap">
<header class="top">
  <a class="brand" href="{t['path']}" data-nav>{sym('#0E120F')}Comandoo</a>
  <nav class="gnav" aria-label="Site"><a class="gl" href="{GUIDES[lang]}" data-nav>{t['guides_label']}</a><span class="seg" aria-label="{t['lang_nav']}">{langs}</span></nav>
</header>
<div class="hero" id="main">
  <div>
    <h1>{t['h1']}</h1>
    <p class="lead">{t['lead']}</p>
    <div class="cta">{cta(t)}<a class="pill pill-soft" href="#como" data-nav>{t['how_link']}</a></div>
    <ul class="facts">{''.join(f'<li>{f}</li>' for f in t['facts'])}</ul>
  </div>
  <div class="stage" id="stage" role="group" aria-label="{t['stage_label']}" data-s='{json.dumps(strings, ensure_ascii=False)}'>
    <div class="tv off" id="tv">
      <div class="screen">
        <div class="scr-on">
          <div class="scr-head"><span>{t['tv_head']}</span>{sym('#A9ED87')}<span>20:30</span></div>
          <div class="tiles">{tiles}</div>
        </div>
        <div class="app" id="tvapp"><b></b><span></span></div>
        <div class="search" id="tvsearch"><span class="mic">{sym('#0E120F')}</span><span class="q"></span><span class="caret"></span></div>
        <div class="vbar" aria-hidden="true"><i></i></div>
        <div class="osd" role="status" aria-live="polite"></div>
      </div>
    </div>
    <svg class="waves" viewBox="0 0 120 120" aria-hidden="true"><path d="M30 70 A40 40 0 0 1 70 30"/><path d="M48 88 A60 60 0 0 1 88 48" transform="translate(-6,-6)"/></svg>
    <div class="phone"><div class="ph">
      <div class="ph-band">
        <button class="chip" data-tv="chip" aria-label="{t['k_chip']}"><i></i><span>{t['tv_name']}</span>{ic('chev', 2.2)}</button>
        <button class="rb" data-tv="mic" aria-label="{t['k_mic']}">{ic('mic')}</button>
        <button class="rb pw" data-tv="power" aria-label="{t['k_power']}">{ic('power', 2.2)}</button>
      </div>
      <div class="ph-main">
        {dpad(t, 'tv')}
        <div class="keys3">
          <button class="k" data-tv="back">{ic('back')}<span>{t['k_back']}</span></button>
          <button class="k" data-tv="home">{ic('home')}<span>{t['k_home']}</span></button>
          <button class="k" data-tv="input">{ic('input')}<span>{t['k_input']}</span></button>
        </div>
        <div class="volrow">
          <button class="mute" data-tv="mute" aria-label="{t['k_mute']}">{ic('mute')}</button>
          <div class="vol">
            <button data-tv="vdown" aria-label="{t['k_vdown']}">{ic('minus', 2.6)}</button>
            <div class="vnum" aria-live="polite"><em>12</em><span class="vtrack" aria-hidden="true"><i style="width:12%"></i></span></div>
            <button data-tv="vup" aria-label="{t['k_vup']}">{ic('plus', 2.6)}</button>
          </div>
        </div>
      </div>
    </div></div>
    <p class="hint">{t['hint']}</p>
  </div>
</div>
</div>
</div>

<main>
<section id="como"><div class="wrap">
  <h2>{t['how_h']}</h2>
  <p class="sub">{t['how_sub']}</p>
  <ol class="steps">{steps}</ol>
  <p class="note">{t['how_note']}</p>
  <p class="more"><a href="{GUIDES[lang]}{PILLAR[lang]}/" data-nav>{t['how_more']}</a></p>
</div></section>

<section><div class="wrap">
  <h2>{t['feat_h']}</h2>
  <div class="feat">
    <div class="keypad">{feats}</div>
    <aside class="extras"><span class="seal">{sym('#0E120F')}{t['seal']}</span><h3>{t['ex_h']}</h3><p>{t['ex_sub']}</p><ul>{extras}</ul></aside>
  </div>
</div></section>

<section id="compat"><div class="wrap">
  <h2>{t['comp_h']}</h2>
  <p class="sub">{t['comp_sub']}</p>
  <div class="tvlist"><div class="tvlist-head"><b>{t['list_h']}</b><span>{t['list_n'].format(n=len(COMPAT_ROWS))}</span></div>{rows}</div>
  <p class="note">{t['comp_note']} <a href="mailto:{EMAIL}" data-nav>{EMAIL}</a>.</p>
</div></section>

<section><div class="wrap priv">
  <div>
    <h2>{t['priv_h']}</h2>
    <p class="sub">{t['priv_sub']} <a href="{t['priv_url']}" data-nav>{t['priv_link']}</a>.</p>
  </div>
  <ul>{priv}</ul>
</div></section>

<section><div class="wrap">
  <h2>{t['faq_h']}</h2>
  <div class="faq">{faq}</div>
</div></section>
</main>

<div class="closing" id="closing"><div class="wrap">
  {pointing()}
  <div>
    <h2>{t['close_h']}</h2>
    <p>{t['close_sub_live'] if PLAY_URL else t['close_sub']}</p>
    <div class="cta">{cta(t)}</div>
  </div>
</div></div>

<footer><div class="wrap foot">
  <div>
    <div class="brand">{sym('#A9ED87')}Comandoo</div>
    <p>{t['f_indep']}</p>
    <p>{t['f_contact']}: <a href="mailto:{EMAIL}" data-nav>{EMAIL}</a></p>
    <p>© 2026 Agência D3</p>
  </div>
  <ul>
    <li><a href="{GUIDES[lang]}" data-nav>{t['guides_label']}</a></li>
    <li><a href="{CHANGELOG[lang]}" data-nav>{t['changelog_label']}</a></li>
    <li><a href="/privacidade" data-nav>{T['pt']['f_priv']}</a></li>
    <li><a href="/privacidade/en" data-nav>{T['en']['f_priv']}</a></li>
    <li><a href="/privacidade/es" data-nav>{T['es']['f_priv']}</a></li>
  </ul>
</div></footer>

<div class="fab" id="fab">
  <div class="bubble" id="bubble">{t['rc_bubble']}</div>
  <div class="mini-rc" id="minirc" role="group" aria-label="{t['rc_cap']}">
    <div class="cap"><span>{t['rc_cap']}</span><button class="rb pw" data-rc="power" aria-label="{t['rc_power']}">{ic('power', 2.2)}</button></div>
    {dpad(t, 'rc')}
    <div class="keys3">
      <button class="k" data-rc="back">{ic('back')}<span>{t['rc_back']}</span></button>
      <button class="k" data-rc="prev">{ic('chup', 2.2)}<span>{t['rc_prev']}</span></button>
      <button class="k" data-rc="next">{ic('chdown', 2.2)}<span>{t['rc_next']}</span></button>
    </div>
  </div>
  <button class="fab-btn" id="fabbtn" aria-expanded="false" aria-controls="minirc" aria-label="{t['rc_open']}" data-close="{t['rc_close']}" data-open="{t['rc_open']}">{sym('#A9ED87')}</button>
</div>
<div class="blackout" id="blackout"><div class="line"></div><button class="wake" id="wake" aria-label="{t['wake']}">{ic('power', 2.2)}</button><span class="wake-txt">{t['wake_txt']}</span></div>
<script src="/assets/site.js" defer></script>
</body>
</html>
'''


def main():
    for lang, t in T.items():
        out = ROOT / 'index.html' if t['path'] == '/' else ROOT / t['path'].strip('/') / 'index.html'
        out.parent.mkdir(parents=True, exist_ok=True)
        out.write_text(page(lang), encoding='utf-8')
        print('ok', out.relative_to(ROOT))
    fav = (f'<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 120 120"><rect width="120" height="120" rx="26" fill="#A9ED87"/>'
           f'<g transform="translate(60,60) scale(1.08) translate(-60,-60)"><path fill="#0E120F" fill-rule="evenodd" d="{SYM_D}"/></g></svg>')
    (ROOT / 'favicon.svg').write_text(fav, encoding='utf-8')


if __name__ == '__main__':
    main()
