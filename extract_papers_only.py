import requests
from bs4 import BeautifulSoup
import re
import json

url = "https://openaccess.thecvf.com/CVPR2024?day=all"
html = requests.get(url).text
soup = BeautifulSoup(html, 'html.parser')

base_url = "https://openaccess.thecvf.com"

papers = []

# Find all paper title dt elements
for dt in soup.find_all('dt', class_='ptitle'):
    title_elem = dt.find('a')
    if not title_elem:
        continue
    title = title_elem.get_text().strip()
    
    # Find the two dd siblings that contain authors and links
    # We'll iterate over next siblings until we find two dd elements with appropriate content
    authors = []
    pdf_url = None
    supp_url = None
    arxiv_url = None
    bibtex_text = None
    
    dd_candidate = dt.find_next_sibling('dd')
    while dd_candidate:
        text = dd_candidate.get_text().strip()
        # Check if this dd contains authors (no brackets, just names with commas)
        if not re.search(r'\[', text) and text and text != 'Back':
            # This is likely the authors dd
            # Extract author names: they are separated by commas and newlines
            authors_text = re.sub(r'\s+', ' ', text)  # replace newlines with spaces
            authors = [a.strip() for a in authors_text.split(',') if a.strip()]
            # Move to next dd
            dd_candidate = dd_candidate.find_next_sibling('dd')
            break
        dd_candidate = dd_candidate.find_next_sibling('dd')
    
    # Now dd_candidate should be the links dd
    if dd_candidate:
        # Extract links
        for link in dd_candidate.find_all('a'):
            href = link.get('href')
            if not href:
                continue
            link_text = link.get_text().strip().lower()
            full_url = base_url + href if not href.startswith('http') else href
            if 'pdf' in link_text:
                pdf_url = full_url
            elif 'supp' in link_text:
                supp_url = full_url
            elif 'arxiv' in link_text:
                arxiv_url = full_url
            # bibtex link may not have href, we'll extract bibtex from div.bibref
        # Extract bibtex if present
        bibref = dd_candidate.find('div', class_='bibref')
        if bibref:
            bibtex_text = bibref.get_text().strip()
    
    papers.append({
        'title': title,
        'authors': authors,
        'abstract': '',  # not available on this page
        'pdf_url': pdf_url,
        'supplementary_url': supp_url,
        'arxiv_url': arxiv_url,
        'bibtex': bibtex_text
    })

# Output only JSON
print(json.dumps(papers, indent=2))