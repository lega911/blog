
import os
from jinja2 import Template
from collections import defaultdict
from utils import encode
import math
from render import render


def main():
    for path, _, files in os.walk('./source'):
        for filename in files:
            fullname = os.path.join(path, filename)

            print(fullname)
            build(fullname, parse(fullname))

    build_index()
    build_tags()


def parse(filename):
    result = {}
    key = None
    for s in open(filename, 'r'):
        s = s.rstrip()
        if s.startswith('::'):
            d = s.split(' ', 1)
            key = d[0][2:]
            assert key not in result, 'double key: ' + key
            if len(d) == 2:
                value = d[1]
                if key == 'tags':
                    value = list(map(str.strip, value.split(',')))
                elif value in {'on', 'true'}:
                    value = True
                elif value in {'off', 'false'}:
                    value = False
            else:
                value = ''
            result[key] = value
        else:
            if key:
                if result[key]:
                    result[key] += '\n' + s
                else:
                    result[key] = s

    return result


page_tpl = Template(open('./base/page.html', 'r').read())
index = {
    'list': []
}


def build(filename, data):
    if data.get('active') is False:
        return
    if data.get('visible') is False:
        return

    data['tag_list'] = tags = []
    for tag in data['tags']:
        tags.append({
            'name': tag,
            'code': encode(tag)
        })

    if 'html' not in data:
        data['html'] = render(data['body'])

    result = page_tpl.render(**data)

    if 'id' in data:
        fullname = os.path.join('./docs/post', data['id'], 'index.html')
    else:
        if 'link' in data:
            fullname = os.path.join('./docs', data['link'].lstrip('/'))
        else:
            fullname = os.path.join('./docs', filename)

    if not fullname.endswith('.html'):
        print('Warning', fullname)

    path = os.path.dirname(fullname)
    os.makedirs(path, exist_ok=True)
    open(fullname, 'w').write(result)

    data['link'] = fullname[5:]
    index['list'].append(data)


def build_index():
    tpl = Template(open('./base/index.html', 'r').read())
    index['list'] = sorted(index['list'], key=lambda p:p.get('date', ''), reverse=True)
    result = tpl.render(**index)

    open('./docs/index.html', 'w').write(result)


def build_tags():
    st = defaultdict(int)
    pages = defaultdict(list)
    for p in index['list']:
        tags = p['tags']
        if not tags:
            continue

        for tag in tags:
            st[tag] += 1
            pages[tag].append(p)

    lmax = math.log2(max(st.values()))

    tag_list = []
    for tag, count in sorted(st.items()):
        lcount = math.log2(count) or 1
        tag_list.append({
            'name': tag,
            'code': encode(tag),
            'size': 10 + round(30/lmax*lcount)
        })

    os.makedirs('docs/tags', exist_ok=True)
    tpl_index = Template(open('./base/tag_index.html', 'r').read())
    tpl = Template(open('./base/tag.html', 'r').read())
    open('./docs/tags/index.html', 'w').write(tpl_index.render(list=tag_list))

    for tag in st.keys():
        plist = sorted(pages[tag], key=lambda p:p['date'], reverse=True)
        path = './docs/tags/' + encode(tag)
        os.makedirs(path, exist_ok=True)
        open(path + '/index.html', 'w').write(tpl.render(list=plist, title=tag))

main()
