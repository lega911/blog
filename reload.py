
from pymongo import MongoClient
import os
from utils import encode as word_code


def main():
    db = MongoClient()['pymy']

    for post in db.post.find():
        if not post['active']:
            continue
        #for k in {'_id', 'time_create', 'title', 'body', 'html', 'shows', 'html_pre', 'tags', 'active',
        #          'is_note', '_ns', 'author', 'time_change'}:
        #    if k in post:
        #        del post[k]
        #print(post)

        code = word_code(post['title'])
        t = post['time_create']
        filename = 'source/{}/{:02d}/{:02d}/{}'.format(t.year, t.month, t.day, code)

        page = []
        page.append('::id ' + str(post['_id']))
        page.append('::date ' + t.strftime('%Y-%m-%d'))
        page.append('::title ' + post['title'])
        page.append('::tags ' + ', '.join(post['tags']))
        page.append('::body\n' + post['body'])
        page.append('::html\n' + post['html'])

        raw = '\n'.join(page).encode('utf8')

        path = os.path.dirname(filename)
        if not os.path.isdir(path):
            os.makedirs(path)

        print(filename)
        #assert not os.path.isfile(filename), 'File exisis ' + filename
        if os.path.isfile(filename):
            filename += '_' + str(post['_id'])
        open(filename, 'wb').write(raw)

main()
