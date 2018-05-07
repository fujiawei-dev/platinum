'''HTML Parsing'''

from requests_html import HTML


def html_parsing(fp=r'platinum/commands.py'):
    with open(r'html/List of Chromium Command Line Switches « Peter Beverloo.html', encoding='utf-8') as f:
        doc = f.read()

    html = HTML(html=doc)
    condition = html.xpath('//tr/@id')
    explanation = html.xpath('//tr/td[2]/text()')
    
    for i, j in zip(condition, explanation):
        k = i.split('   ')[0].replace("'", '').replace('-', '_').upper()
        if len(k) < 1 or not k[0].isalpha():
            continue
        print(f'{k} = {i.strip()!r}   # {j.strip()}', file=open(fp, 'a', encoding='utf-8'))


if __name__ == '__main__':
    html_parsing()