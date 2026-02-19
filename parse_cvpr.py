import requests
from bs4 import BeautifulSoup
import json
import re

url = "https://openaccess.thecvf.com/CVPR2024?day=all"
response = requests.get(url)
html = response.text
soup = BeautifulSoup(html, 'html.parser')

# Find the main content area. Let's search for all dt or dd elements.
# We'll try to locate each paper block. Looking at the page, each paper seems to be in a <dt> for title and <dd> for details.
# Actually, the page might use <dt> for paper title and <dd> for authors and links.
# Let's find all <dt> elements with class 'ptitle' (maybe).
papers = []
for dt in soup.find_all('dt'):
    # Check if it contains a paper title
    title_elem = dt.find('a')
    if not title_elem:
        continue
    title = title_elem.get_text().strip()
    # The href for the paper page maybe, not the PDF directly.
    # The next sibling <dd> may contain authors and links.
    dd = dt.find_next_sibling('dd')
    if not dd:
        continue
    # Extract authors: might be in a <i> tag or just text.
    authors_text = dd.get_text().strip()
    # Split by newline? Let's just capture everything before the first '['.
    # Actually, authors are listed with commas and newlines.
    # We'll find all text until the first '['.
    import re
    authors_part = re.split(r'\[', authors_text)[0].strip()
    authors = [a.strip() for a in authors_part.split(',')]
    # Extract links
    pdf_link = None
    supp_link = None
    arxiv_link = None
    bibtex_link = None
    for a in dd.find_all('a'):
        href = a.get('href', '')
        text = a.get_text().strip().lower()
        if 'pdf' in text:
            pdf_link = href
        elif 'supp' in text:
            supp_link = href
        elif 'arxiv' in text:
            arxiv_link = href
        elif 'bibtex' in text:
            bibtex_link = href
    # Construct full URLs
    base_url = "https://openaccess.thecvf.com"
    if pdf_link and not pdf_link.startswith('http'):
        pdf_link = base_url + pdf_link
    if supp_link and not supp_link.startswith('http'):
        supp_link = base_url + supp_link
    if arxiv_link and not arxiv_link.startswith('http'):
        arxiv_link = base_url + arxiv_link
    # Extract abstract? Not available on this page.
    abstract = ""
    papers.append({
        'title': title,
        'authors': authors,
        'abstract': abstract,
        'pdf_url': pdf_link,
        'supplementary_url': supp_link,
        'arxiv_url': arxiv_link,
        'bibtex_url': bibtex_link
    })

print(json.dumps(papers, indent=2))