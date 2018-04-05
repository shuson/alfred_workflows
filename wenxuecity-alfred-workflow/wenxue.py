# -*- encoding=utf-8 -*-
import sys

import unicodedata

from bs4 import BeautifulSoup

import alfred

URL = 'http://www.wenxuecity.com'

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
  r = alfred.request.get(url)
  r.encoding = 'utf-8'
  bs = BeautifulSoup(r.getContent(), 'html.parser')
  posts = bs.select('div.col ul li')

  items = []
  for p in posts[:30]:
    if not p.find('a') or p.find('a').get('class'):
        continue
    ptitle = p.find('a').text
    
    item = {
      'title': u'{subject}'.format(subject=ptitle),
      'subtitle': " ",
      'link': URL + p.find("a")['href']
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
