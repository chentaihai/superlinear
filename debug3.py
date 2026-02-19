import requests
from bs4 import BeautifulSoup
import re

url = "https://openaccess.thecvf.com/CVPR2024?day=all"
html = requests.get(url).text
soup = BeautifulSoup(html, 'html.parser')

# Find first dt with class ptitle
first_dt = soup.find('dt', class_='ptitle')
if first_dt:
    dl = first_dt.find_parent('dl')
    print("Children of DL:")
    for idx, child in enumerate(dl.children):
        if child.name:
            print(f"{idx}: {child.name} class={child.get('class')}")
            if child.name == 'dt':
                print(f"   text: {child.get_text()[:100]}")
            elif child.name == 'dd':
                print(f"   text preview: {child.get_text()[:200]}")
    # Let's get the specific dd that contains pdf links (the one after dt)
    # We'll iterate over siblings after dt
    print("\nSiblings after DT:")
    for sibling in first_dt.find_next_siblings():
        if sibling.name == 'dd':
            print(f"DD: {sibling.get_text()[:200]}")
            break

# Also check if there is a dd before dt containing authors?
prev = first_dt.find_previous_sibling()
if prev and prev.name == 'dd':
    print("\nPrevious DD (maybe authors?):", prev.get_text()[:200])