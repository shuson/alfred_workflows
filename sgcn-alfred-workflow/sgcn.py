# -*- encoding=utf-8 -*-
import sys

import unicodedata

from bs4 import BeautifulSoup

import alfred

URL = 'http://bbs.sgcn.com/forum.php?mod=forumdisplay&fid=197&filter=author&orderby=dateline'
URL2 = 'http://bbs.sgcn.com/forum.php?mod=forumdisplay&fid=160&filter=author&orderby=dateline'

def full2half(uc):
    """Convert full-width characters to half-width characters.
    """
    return unicodedata.normalize('NFKC', uc)

def display(items):
  fb = alfred.Feedback()
  
  for item in items:
    fb.addItem(title=item['title'], subtitle=item['subtitle'], arg=item['link'])
  fb.output()

def run(query):
  url = URL
  q = query.strip()
  if q == 'phone':
    url = URL2
  
  r = alfred.request.get(url)
  r.encoding = 'utf-8'
  bs = BeautifulSoup(r.getContent(), 'html.parser')
  posts = bs.select('tbody[id^=normalthread]')

  items = []
  for p in posts:
    ptitle = p.find('a', class_='s xst')
    ptime = p.find('span').string
    pname = p.find('cite').find('a').string
    item = {
      'title': u'{subject}'.format(subject=ptitle.string),
      'subtitle': u'by: {name} | {time}'.format(name=pname, time=ptime),
      'link': ptitle['href']
    }
    items.append(item)
    if len(items) == 15: break
  
  display(items)

if __name__ == '__main__':
  if len(sys.argv) == 1:
    q = ''
  else:
    q = sys.argv[1]
  run(q)
