from bs4 import BeautifulSoup
from requests import get

response = get('https://fuchsia.dev')
soup = BeautifulSoup(response.content, 'html.parser')
for a in soup.find_all('a'):
  print(a.get('href'))