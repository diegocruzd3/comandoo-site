#!/usr/bin/env python3
"""Leva a política de privacidade para o modelo visual do site, sem mudar uma palavra do texto.

Uso: python3 tools/privacy.py
Lê privacidade/index.html, privacidade/en/index.html e privacidade/es/index.html.
O texto da política continua sendo mantido pela sessão responsável: esta ferramenta só troca a moldura
(cabeçalho, fontes, cores, rodapé). Pode rodar de novo depois de qualquer edição do texto, no formato
antigo ou no novo: o conteúdo entre <!--priv:start--> e <!--priv:end--> é preservado como está.
"""
import re
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))
import guides as G  # noqa: E402
import guides_content as C  # noqa: E402

ROOT = Path(__file__).resolve().parent.parent
FILES = {'pt': 'privacidade/index.html', 'en': 'privacidade/en/index.html', 'es': 'privacidade/es/index.html'}


def extract(src):
    m = re.search(r'<!--priv:start-->(.*)<!--priv:end-->', src, re.S)
    if m:
        return re.sub(r'<!--priv:split-->.*?<article class="prose ppol">', '', m.group(1), flags=re.S).strip()
    body = re.search(r'<main>(.*)</main>', src, re.S).group(1)
    i = body.find('<h1')
    return body[i:].strip()


def render(lang, content):
    UI = C.UI[lang]
    canon = G.SITE + UI['privacy']
    alternates = {l: G.SITE + C.UI[l]['privacy'] for l in C.LANGS}
    title = re.sub('<[^>]+>', '', re.search(r'<h1[^>]*>(.*?)</h1>', content, re.S).group(1))
    # cabeçalho: título e a linha de atualização; o resto vai no corpo, sem alteração
    m = re.match(r'(<h1.*?</h1>\s*(?:<p class="muted">.*?</p>)?)(.*)', content, re.S)
    top, rest = m.group(1), m.group(2)
    first_p = re.search(r'<p>(.*?)</p>', rest, re.S)
    desc = G.plain(first_p.group(1), 155) if first_p else title
    body = rest.replace('<table>', '<table class="ptab">').strip()
    return (G.head(lang, f'{title} | Comandoo', desc, canon, alternates, 'website')
            + '\n<link rel="stylesheet" href="/assets/privacy.css">\n</head>\n<body>\n'
            + G.topbar(lang, alternates, [('Comandoo', UI['home'])], current_guides=False)
            + f'\n<!--priv:start-->\n{top}\n<!--priv:split-->'
            + '\n</div>\n</div></div>\n<main id="conteudo" class="wrap">\n<article class="prose ppol">\n'
            + body + '\n<!--priv:end-->\n</article>\n</main>\n' + G.footer(lang))


def main():
    for lang, rel in FILES.items():
        p = ROOT / rel
        src = p.read_text(encoding='utf-8')
        content = extract(src)
        # o marcador de início fica no cabeçalho; recompor o conteúdo completo para a próxima leitura
        out = render(lang, content)
        p.write_text(out, encoding='utf-8')
        print('ok', rel, len(out))


if __name__ == '__main__':
    main()
