from bs4 import BeautifulSoup
import requests
from json import dumps

# TODO: Check if the external URL links to a section.
def check_external_url(url):
  response = requests.get(url)
  return (response.status_code == requests.codes.ok)

# TODO: The data should only get saved once for each
# computed URL.
def check_external_urls(base, hrefs):
  for href in hrefs:
    computed_url = hrefs[href]['computed']
    if base in computed_url:
      continue
    hrefs[href]['ok'] = check_external_url(computed_url)

def compute_url(base, href):
  if base in href:
    return href
  # TODO: Use regex to match exactly 2.
  elif href.startswith('//'):
    scheme = base[0:base.index('/')]
    return '{}{}'.format(scheme, href)
  elif href.startswith('/'):
    return '{}{}'.format(base, href)
  else:
    return 'TODO'

def compute_urls(base, hrefs):
  for href in hrefs:
    hrefs[href]['computed'] = compute_url(base, href)
  return hrefs

# TODO: The hrefs section should arguably just be the
# href followed by the computed URL as a key-value
# pair.
def scrape(url):
  response = requests.get(url)
  soup = BeautifulSoup(response.content, 'html.parser')
  data = {'hrefs': {}, 'ids': []}
  for node in soup.find_all('a', attrs={'href': True}):
      data['hrefs'][node.get('href')] = {'computed': None, 'ok': None}
  for node in soup.find_all(attrs={'id': True}):
    data['ids'].append(node.get('id'))
  return data

def main():
  base = 'https://fuchsia.dev'
  report = {'targets': [base], 'data': {}, 'metadata': {}}
  while len(report['targets']) > 0:
    target = report['targets'].pop()
    report['data'][target] = scrape(target)
    hrefs = report['data'][target]['hrefs']
    hrefs = compute_urls(base, hrefs)
    hrefs = check_external_urls(base, hrefs)
  print(dumps(report, indent=2))

if __name__ == '__main__':
  main()
