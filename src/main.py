from bs4 import BeautifulSoup
from requests import get
from json import dumps

def compute_urls(base, data):
  for href in data:
    if base in href:
      data[href]['computed'] = False
    elif href.startswith('//'):
      scheme = href[0:href.index('/')]
      print(scheme)
      data[href]['computed'] = '{}{}'.format(scheme, href)
    elif href.startswith('/'):
      data[href]['computed'] = '{}{}'.format(base, href)
  return data

def scrape(url):
  response = get(url)
  soup = BeautifulSoup(response.content, 'html.parser')
  data = {'hrefs': {}, 'ids': {}, 'xrefs': []}
  for node in soup.find_all('a'):
    data['hrefs'][node.get('href')] = {'computed': None, 'ok': None}
  for node in soup.find_all(attrs={'id': True}):
    data['ids'][node.get('id')] = {'xrefs': []}
  return data

def main():
  base = 'https://fuchsia.dev'
  targets = [base]
  data = {}
  while len(targets) > 0:
    target = targets.pop()
    data[target] = scrape(target)
    data[target]['hrefs'] = compute_urls(base, data[target]['hrefs'])
  # print(dumps(data, indent=2))

if __name__ == '__main__':
  main()