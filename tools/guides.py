#!/usr/bin/env python3
"""Guias do Comandoo (manual do app). Gera /guias, /en/guides e /es/guias.

Fontes de verdade, nesta ordem:
  1. compat.json do repositório controley-releases (branch main): marcas e status.
  2. faq.json do mesmo repositório: nomes de botões e fluxos do app.
  3. Capturas reais do app em assets/guias/ (nunca imagem inventada).
Regra: a cada versão nova do app, revisar os guias que citam recursos alterados.
"""
import html
import json
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))
import build as B  # noqa: E402

ROOT = B.ROOT
SITE = B.SITE
UPDATED = '2026-10-12'
APP_VERSION = '1.24.2'


def plain(b, n=320):
    import re
    t = re.sub(r'\s+', ' ', html.unescape(re.sub(r'<table.*?</table>|<div class="tip.*?</div>', ' ', b, flags=re.S)))
    t = re.sub(r'<[^>]+>', '', t).strip()
    t = re.sub(r'\s+([.,:])', r'\1', t)
    return t if len(t) <= n else t[:n].rsplit('. ', 1)[0] + '.'


def esc(s):
    return html.escape(s, quote=True)


def shot(file, alt, caption, wide=False):
    """Captura real do app. Se o arquivo ainda não existe, mostra o espaço reservado."""
    if (ROOT / 'assets' / 'guias' / file).exists():
        return (f'<figure class="shot"><img src="/assets/guias/{file}" alt="{esc(alt)}" loading="lazy" '
                f'width="600" height="1067"><figcaption>{caption}</figcaption></figure>')
    return f'<figure class="shot pending{" wide" if wide else ""}" role="img" aria-label="{esc(alt)}">Captura pendente<br>{caption}</figure>'


def cta_box():
    btn = (f'<a class="pill pill-dark" href="{B.PLAY_URL}" rel="noopener">{B.sym()}Baixar no Google Play</a>' if B.PLAY_URL
           else f'<span class="pill pill-dark pill-soon">{B.sym()}Em breve no Google Play</span>')
    return (f'<aside class="gcta">{B.sym("#0E120F")}<div><b>Comandoo: o controle remoto no celular</b>'
            f'<p>Grátis, sem anúncios e sem cadastro. Funciona pelo Wi-Fi de casa.</p></div>{btn}</aside>')


# ── Modelo: guia principal (PT) ───────────────────────────────────────────
PILLAR = dict(
    slug='celular-como-controle-remoto',
    title='Como usar o celular como controle remoto da TV (grátis e sem anúncios)',
    seo_title='Como usar o celular como controle remoto da TV | Comandoo',
    desc='Passo a passo para controlar a Smart TV pelo celular, pelo Wi-Fi e sem infravermelho: o que você precisa, como parear e o que fazer se a TV não aparecer.',
    h1='Como usar o celular como controle remoto da TV',
    answer=('Dá para usar o celular como controle remoto de uma Smart TV pelo Wi-Fi, sem infravermelho. '
            'Você precisa de um app de controle no celular, da TV ligada e dos dois aparelhos na mesma rede de casa. '
            'Com o Comandoo, que é grátis e sem anúncios, basta escolher a TV na lista e confirmar o pareamento uma vez.'),
    time='PT5M',
)

STEPS = [
    ('Instale o Comandoo no celular',
     '<p>O Comandoo é um app para Android. Ele chega em breve ao Google Play; o link aparece aqui assim que estiver disponível. '
     'Não é preciso criar conta nem fazer login.</p>', None),
    ('Ligue a TV e confira a rede',
     '<p>Ligue a TV (não basta estar em espera) e veja se o celular está no <strong>mesmo Wi-Fi</strong> que ela. '
     'Desligue os dados móveis e evite a rede de visitantes do roteador: muitas TVs recusam comandos vindos de outra rede.</p>', None),
    ('Abra o app e escolha a sua TV',
     '<p>Ao abrir, o Comandoo procura os aparelhos da sua rede e mostra a lista. Toque na sua TV. '
     'Se ela não aparecer, toque em <strong>Buscar aparelhos</strong>. Se mesmo assim não aparecer, use <strong>Conectar pelo IP</strong> '
     '(veja <a href="#problemas">Problemas comuns</a>).</p>',
     ('lista-de-tvs.png', 'Lista de TVs encontradas no Comandoo', 'Lista de aparelhos encontrados na rede')),
    ('Confirme o pareamento na TV',
     '<p>Na primeira vez, a TV pede uma confirmação. O jeito muda conforme a marca: aceitar um pedido na tela ou digitar um código no app.</p>'
     '<table class="pair"><thead><tr><th scope="col">Marca</th><th scope="col">O que aparece na primeira vez</th></tr></thead><tbody>'
     '<tr><td>LG</td><td>Um pedido na tela. Aceite com o controle da TV.</td></tr>'
     '<tr><td>Samsung</td><td>Um aviso pedindo para permitir o app. Aceite com o controle da TV.</td></tr>'
     '<tr><td>Android TV e Google TV</td><td>Um código de 6 letras ou números. Digite no app exatamente como aparece.</td></tr>'
     '<tr><td>Fire TV, Panasonic e Philips</td><td>Um PIN de 4 números. Digite no app.</td></tr>'
     '<tr><td>Roku</td><td>Nada: não há código.</td></tr>'
     '<tr><td>Sony Bravia</td><td>A chave (PSK) que você define na TV, em Controle IP.</td></tr>'
     '</tbody></table>'
     '<div class="tip warn"><p><strong>Sem o controle original?</strong> Na LG e na Samsung, o primeiro pedido precisa ser aceito na própria TV. '
     'Veja <a href="/guias/perdi-o-controle-da-tv/">Perdi o controle da TV: o que fazer</a>.</p></div>'
     '<p>Depois disso o app reconecta sozinho nas próximas vezes.</p>',
     ('pedido-na-tv.jpg', 'Pedido de pareamento do Comandoo na tela de uma TV LG', 'Pedido de pareamento na tela da TV (foto)', True)),
    ('Use o controle',
     '<p>Pronto: a tela Controle tem direcional e OK, voltar, início, volume, mudo e o botão de desligar. '
     'Botões que a sua TV não aceita pelo protocolo dela aparecem apagados.</p>',
     ('tela-controle.png', 'Tela Controle do Comandoo com direcional, OK e volume', 'Tela Controle, já conectada')),
]

EXTRAS = [
    ('Digitar senhas e buscas', 'Com um campo de texto aberto na TV, o que você digita no celular aparece na TV ao vivo.',
     '/guias/digitar-na-tv-pelo-celular/'),
    ('Falar em vez de digitar', 'Segure o botão de voz e diga, por exemplo, “abrir Netflix” ou “volume 15”.', None),
    ('Abrir os apps da TV', 'Seus aplicativos da TV ficam a um toque, direto no celular.', None),
    ('Controle por cima de outros apps', 'O botão flutuante abre o controle sem sair do aplicativo em que você está.', None),
]

PROBLEMS = [
    ('A TV não aparece na lista',
     '<p>Confira se a TV está ligada e se os dois aparelhos estão no mesmo Wi-Fi. Alguns roteadores separam as redes de 2,4 GHz e de 5 GHz: '
     'deixe o celular na mesma que a TV. Em algumas marcas é preciso ativar o controle pelo celular nas configurações da TV.</p>'
     '<p>Se continuar, descubra o IP da TV (em Configurações, Rede, Status da conexão) e use <strong>Conectar pelo IP</strong>. '
     'O guia <a href="/guias/celular-nao-encontra-a-tv/">Por que o celular não encontra a TV</a> tem o passo a passo completo.</p>'),
    ('A TV conecta, mas não obedece aos botões',
     '<p>Na <strong>Roku</strong>, abra Configurações, Sistema, Configurações avançadas, Controle por apps móveis e deixe o acesso à rede como Ativado. '
     'Na <strong>LG</strong>, em Ajustes do app, toque em Refazer pareamento e aceite o pedido na TV. '
     'Na <strong>Samsung</strong> e na <strong>Panasonic</strong>, confira se o celular não está no Wi-Fi de visitantes.</p>'),
    ('O app não liga a TV',
     '<p>Desligar pelo app funciona na maioria das TVs, mas ligar depende do modelo. Na LG, ative na TV a opção de ligar pela rede '
     '(Wake on LAN nas TVs 2025 ou mais novas, Mobile TV On nas anteriores). Em várias marcas a TV só desliga pela rede.</p>'),
    ('A conexão cai ou demora a voltar',
     '<p>O app tenta reconectar sozinho. Se o Android estiver economizando bateria demais, deixe o Comandoo sem restrição de bateria nas configurações do celular.</p>'),
]

FAQ = [
    ('O celular precisa ter infravermelho?', 'Não. O Comandoo usa o Wi-Fi de casa, então funciona em qualquer celular Android, com ou sem infravermelho.'),
    ('Funciona pelo 4G ou fora de casa?', 'Não. O celular precisa estar na mesma rede Wi-Fi da TV, porque os comandos vão direto de um aparelho para o outro.'),
    ('É grátis mesmo?', 'Sim. O controle não tem anúncios nem cadastro. No futuro, alguns recursos extras poderão fazer parte de um plano opcional, mas o controle básico continua grátis para sempre.'),
    ('Funciona com qualquer TV?', 'Funciona com Smart TVs conectadas ao Wi-Fi das marcas da lista de compatíveis. A LG foi testada em TV real; as outras marcas têm suporte inicial, ainda sem teste em TV real. TVs sem Wi-Fi não funcionam.'),
    ('Funciona no iPhone?', 'Ainda não. O Comandoo é um app para Android.'),
]

RELATED = [
    ('/guias/perdi-o-controle-da-tv/', 'Perdi o controle da TV: o que fazer', 'Como parear e mexer na TV sem o controle original'),
    ('/guias/celular-nao-encontra-a-tv/', 'Por que o celular não encontra a TV', 'Wi-Fi, rede de visitantes e conexão pelo IP'),
    ('/guias/digitar-na-tv-pelo-celular/', 'Como digitar senhas e buscas na TV pelo celular', 'Teclado do celular e voz na TV'),
    ('/guias/controle-remoto-tv-lg/', 'Controle remoto no celular para TV LG', 'Pareamento, ligar pela rede e dicas da LG'),
]


def schema():
    url = f'{SITE}/guias/{PILLAR["slug"]}/'
    art = {"@context": "https://schema.org", "@type": "Article", "headline": PILLAR['h1'], "description": PILLAR['desc'],
           "inLanguage": "pt-BR", "url": url, "datePublished": UPDATED, "dateModified": UPDATED,
           "author": {"@type": "Organization", "name": "Agência D3"},
           "publisher": {"@type": "Organization", "name": "Agência D3", "logo": {"@type": "ImageObject", "url": f"{SITE}/assets/icone-512.png"}},
           "image": f"{SITE}/assets/og-pt.png", "mainEntityOfPage": url}
    howto = {"@context": "https://schema.org", "@type": "HowTo", "name": PILLAR['h1'], "description": PILLAR['answer'],
             "totalTime": PILLAR['time'], "inLanguage": "pt-BR",
             "supply": [{"@type": "HowToSupply", "name": "Celular Android"}, {"@type": "HowToSupply", "name": "Smart TV no Wi-Fi"}],
             "tool": [{"@type": "HowToTool", "name": "App Comandoo"}],
             "step": [{"@type": "HowToStep", "position": i + 1, "name": h, "url": f"{url}#passo-{i+1}",
                       "text": plain(b)}
                      for i, (h, b, _) in enumerate(STEPS)]}
    faq = {"@context": "https://schema.org", "@type": "FAQPage",
           "mainEntity": [{"@type": "Question", "name": q, "acceptedAnswer": {"@type": "Answer", "text": a}} for q, a in FAQ]}
    crumbs = {"@context": "https://schema.org", "@type": "BreadcrumbList", "itemListElement": [
        {"@type": "ListItem", "position": 1, "name": "Comandoo", "item": f"{SITE}/"},
        {"@type": "ListItem", "position": 2, "name": "Guias", "item": f"{SITE}/guias/"},
        {"@type": "ListItem", "position": 3, "name": PILLAR['h1'], "item": url}]}
    return ''.join(f'<script type="application/ld+json">{json.dumps(x, ensure_ascii=False)}</script>' for x in (art, howto, faq, crumbs))


def pillar_page():
    p = PILLAR
    url = f'{SITE}/guias/{p["slug"]}/'
    steps = ''.join(
        f'<li id="passo-{i+1}"><h3>{h}</h3>{b}{shot(*s) if s else ""}</li>' for i, (h, b, s) in enumerate(STEPS))
    extras = ''.join(f'<li><strong>{h}.</strong> {d}' + (f' <a href="{l}">Ver guia</a>.' if l else '') + '</li>' for h, d, l in EXTRAS)
    probs = ''.join(f'<details><summary>{q}</summary><div>{a}</div></details>' for q, a in PROBLEMS)
    faq = ''.join(f'<details><summary>{q}</summary><div><p>{a}</p></div></details>' for q, a in FAQ)
    rel = ''.join(f'<li><a href="{u}">{t}<span>{s}</span></a></li>' for u, t, s in RELATED)
    alts = (f'<link rel="alternate" hreflang="pt-BR" href="{url}">'
            f'<link rel="alternate" hreflang="en" href="{SITE}/en/guides/phone-as-tv-remote/">'
            f'<link rel="alternate" hreflang="es" href="{SITE}/es/guias/celular-como-control-remoto/">'
            f'<link rel="alternate" hreflang="x-default" href="{url}">')
    return f'''<!doctype html>
<html lang="pt-BR">
<head>
<meta charset="utf-8">
<meta name="viewport" content="width=device-width, initial-scale=1, viewport-fit=cover">
<title>{esc(p['seo_title'])}</title>
<meta name="description" content="{esc(p['desc'])}">
<link rel="canonical" href="{url}">
{alts}
<meta name="theme-color" content="#A9ED87">
<link rel="icon" href="/favicon.svg" type="image/svg+xml">
<link rel="preload" href="/assets/figtree.woff2" as="font" type="font/woff2" crossorigin>
<meta property="og:type" content="article">
<meta property="og:site_name" content="Comandoo">
<meta property="og:title" content="{esc(p['h1'])}">
<meta property="og:description" content="{esc(p['desc'])}">
<meta property="og:url" content="{url}">
<meta property="og:image" content="{SITE}/assets/og-pt.png">
<meta property="og:locale" content="pt_BR">
<meta name="twitter:card" content="summary_large_image">
<link rel="stylesheet" href="/assets/site.css">
<link rel="stylesheet" href="/assets/guide.css">
{schema()}
</head>
<body>
<a class="skip" href="#conteudo">Pular para o conteúdo</a>
<div class="gtop"><div class="wrap">
<header class="top">
  <a class="brand" href="/">{B.sym('#0E120F')}Comandoo</a>
  <nav class="gnav" aria-label="Site"><a class="gl" href="/guias/" aria-current="true">Guias</a>
    <span class="seg"><a href="/guias/{p['slug']}/" aria-current="page" hreflang="pt" lang="pt">PT</a><a href="/en/guides/phone-as-tv-remote/" hreflang="en" lang="en">EN</a><a href="/es/guias/celular-como-control-remoto/" hreflang="es" lang="es">ES</a></span></nav>
</header>
<div class="ghead">
  <p class="crumbs"><a href="/">Comandoo</a> › <a href="/guias/">Guias</a></p>
  <h1>{p['h1']}</h1>
  <p class="answer">{p['answer']}</p>
  <ul class="meta"><li>Leitura de 4 min</li><li>Atualizado em 12/10/2026</li><li>App versão {APP_VERSION}</li></ul>
</div>
</div></div>

<main id="conteudo" class="wrap">
<article class="prose">
  <section class="need" aria-labelledby="precisa">
    <h2 id="precisa">O que você precisa</h2>
    <ul>
      <li>Um celular Android.</li>
      <li>Uma Smart TV ligada ao Wi-Fi, de uma <a href="/#compat">marca compatível</a>.</li>
      <li>Celular e TV no mesmo Wi-Fi de casa.</li>
    </ul>
  </section>

  <h2 id="passo-a-passo">Passo a passo</h2>
  <ol class="steps-g">{steps}</ol>

  <h2>O que mais dá para fazer pelo celular</h2>
  <ul>{extras}</ul>
  <p>Nem toda marca aceita todos os recursos. O app mostra só o que a sua TV permite.</p>

  <h2 id="problemas">Problemas comuns</h2>
  <p>Antes de tudo, toque na faixa verde de conexão no app e escolha <strong>Testar conexão</strong>: em poucos segundos ele confere o Wi-Fi, a TV e o pareamento, e diz o que fazer.</p>
  <div class="prob">{probs}</div>

  <h2 id="perguntas">Perguntas frequentes</h2>
  <div class="prob">{faq}</div>

  {cta_box()}
  <p class="updated">Este guia acompanha a versão {APP_VERSION} do Comandoo. Viu algo diferente no app? Escreva para <a href="mailto:{B.EMAIL}">{B.EMAIL}</a>.</p>
</article>

<nav class="related" aria-labelledby="rel"><h2 id="rel">Outros guias</h2><ul>{rel}</ul></nav>
</main>

<footer><div class="wrap foot">
  <div>
    <div class="brand">{B.sym('#A9ED87')}Comandoo</div>
    <p>{B.T['pt']['f_indep']}</p>
    <p>Contato: <a href="mailto:{B.EMAIL}">{B.EMAIL}</a></p>
    <p>© 2026 Agência D3</p>
  </div>
  <ul>
    <li><a href="/">Início</a></li>
    <li><a href="/guias/">Guias</a></li>
    <li><a href="/changelog/">Novidades do app</a></li>
    <li><a href="/privacidade">Política de privacidade</a></li>
  </ul>
</div></footer>
</body>
</html>
'''


def main():
    out = ROOT / 'guias' / PILLAR['slug'] / 'index.html'
    out.parent.mkdir(parents=True, exist_ok=True)
    out.write_text(pillar_page(), encoding='utf-8')
    print('ok', out.relative_to(ROOT))


if __name__ == '__main__':
    main()
