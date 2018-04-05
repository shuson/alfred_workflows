# -*- encoding=utf-8 -*-
import sys

import unicodedata

from bs4 import BeautifulSoup

import alfred

ongoing = "http://singpromos.com/bydate/ontoday/"
soon = 'http://singpromos.com/bydate/comingsoon/'

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
  url = ongoing
  q = query.strip()
  if q == 'soon':
    url = soon
    
  headers = {'User-Agent': 'Mozilla/5.0 (Windows NT 6.1; WOW64)'}
  r = alfred.request.get(url, headers=headers)
  r.encoding = 'utf-8'
  bs = BeautifulSoup(r.getContent(), 'html.parser')
  feeds = bs.select('div[class="tabs1Content"] article')

  items = []
  for f in feeds:
    fa = f.find('h3').find('a')
    falink = fa['href']
    fb = f.find('div', class_='mh-excerpt').find('p')
    item = {
      'title': u'{subject}'.format(subject=fa.text.strip()),
      'subtitle': u'{subtitle}'.format(subtitle=fb.text[:99] + ' ...'),
      'link': falink
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
