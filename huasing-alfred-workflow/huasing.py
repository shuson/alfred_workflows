# -*- encoding=utf-8 -*-
import sys
import unicodedata

from bs4 import BeautifulSoup
import alfred

URL = 'http://bbs.huasing.org/sForum/'

def display(items):
  fb = alfred.Feedback()
  
  for item in items:
    fb.addItem(title=item['title'], subtitle=item['subtitle'], arg=item['link'])
  fb.output()

def run(query):
    r = alfred.request.get(URL + 'zsbbs.php')
    r.encoding = 'utf-8'
    bs = BeautifulSoup(r.getContent(), 'html.parser')
    posts = bs.find_all('div', 'fake-s')

    result = []
    for p in posts[5:]:
        meta = p.find_all('div')[1].string.split(',')
        title = p.find('div').contents[0]

        item = {
            'title': u'{subject} [{replies}]'.format(subject=title, replies=meta[3]),
            'subtitle': u'{forum} | {user} | {time}'.format(forum=meta[0], user=meta[9], time=meta[10].replace('\n', ' ')),
            'link': URL + 'bbs.php?B=' + p['id'][2:].replace ("-", "_")
        }

        result.append(item)
        if len(result) == 15: break

    display(result)

if __name__ == '__main__':
  if len(sys.argv) == 1:
    q = ''
  else:
    q = sys.argv[1]
  run(q)
    
