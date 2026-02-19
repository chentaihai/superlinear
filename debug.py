import requests
from bs4 import BeautifulSoup
import re

url = "https://openaccess.thecvf.com/CVPR2024?day=all"
html = requests.get(url).text
soup = BeautifulSoup(html, 'html.parser')

# Find all links with 'pdf' in href
pdf_links = soup.find_all('a', href=re.compile(r'pdf'))
print("Number of PDF links:", len(pdf_links))
if pdf_links:
    first = pdf_links[0]
    print("First PDF link href:", first['href'])
    # Print parent hierarchy
    parent = first.parent
    for i in range(5):
        print(f"Parent {i}: {parent.name} class={parent.get('class')}")
        parent = parent.parent
        if parent is None:
            break

# Let's also find all dt and dd elements
print("\nAll dt elements:")
for dt in soup.find_all('dt'):
    print(dt.get_text()[:100])
    break

print("\nAll dd elements:")
for dd in soup.find_all('dd'):
    print(dd.get_text()[:100])
    break

# Maybe papers are in div with class 'paper'
print("\nDivs with class containing 'paper':")
for div in soup.find_all('div', class_=lambda c: c and 'paper' in c):
    print(div.get('class'))
    break