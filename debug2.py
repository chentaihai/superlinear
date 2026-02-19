import requests
from bs4 import BeautifulSoup
import re

url = "https://openaccess.thecvf.com/CVPR2024?day=all"
html = requests.get(url).text
soup = BeautifulSoup(html, 'html.parser')

# Find first PDF link
first_pdf = soup.find('a', href=re.compile(r'pdf'))
if first_pdf:
    dd = first_pdf.find_parent('dd')
    if dd:
        print("DD HTML:")
        print(dd.prettify()[:2000])
        # Also get previous dt
        dt = dd.find_previous_sibling('dt')
        if dt:
            print("\nDT HTML:")
            print(dt.prettify()[:1000])
        # Find all links in this dd
        links = dd.find_all('a')
        for link in links:
            print(f"Link text: {link.get_text()}, href: {link['href']}")
        # Get authors: maybe they are in <i> tags or just text before first link?
        # Let's get all text and split by newline
        full_text = dd.get_text()
        print("\nFull text of DD:")
        print(full_text[:500])