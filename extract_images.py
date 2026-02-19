import re
import sys
import json

def extract_image_urls(html_content):
    # Patterns for Instagram image URLs
    patterns = [
        r'https://[^\s"\']*\.(?:jpg|jpeg|png|gif|webp)(?:\?[^\s"\']*)?',
        r'https://[^\s"\']*cdninstagram\.com[^\s"\']*',
        r'https://[^\s"\']*instagram\.com[^\s"\']*/p/[^\s"\']*',
        r'src="([^"]+)"',  # generic src attributes
    ]
    
    urls = set()
    for pattern in patterns:
        matches = re.findall(pattern, html_content, re.IGNORECASE)
        for match in matches:
            # Clean up URL
            url = match.strip()
            if url.startswith('"') or url.startswith("'"):
                url = url[1:]
            if url.endswith('"') or url.endswith("'"):
                url = url[:-1]
            # Filter out non-image URLs
            if any(ext in url.lower() for ext in ['.jpg', '.jpeg', '.png', '.gif', '.webp', '/image/', '/photo/']):
                urls.add(url)
            elif 'cdninstagram.com' in url:
                urls.add(url)
    
    return sorted(urls)

def main():
    # Read HTML from stdin or file
    if len(sys.argv) > 1:
        with open(sys.argv[1], 'r', encoding='utf-8') as f:
            html_content = f.read()
    else:
        html_content = sys.stdin.read()
    
    urls = extract_image_urls(html_content)
    
    print(f"Found {len(urls)} image URLs:")
    for i, url in enumerate(urls, 1):
        print(f"{i}. {url}")
    
    # Optionally save to JSON
    if urls:
        with open('instagram_image_urls.json', 'w') as f:
            json.dump(urls, f, indent=2)
        print(f"\nSaved to instagram_image_urls.json")

if __name__ == '__main__':
    main()