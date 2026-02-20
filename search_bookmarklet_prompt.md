# Prompt Library

> A simple, consistent place to store current prompts.

---

## Metadata

- Owner: 
- Created: 2026-02-20
- Updated: 2026-02-20
- Version: 1.0

---

## Usage

1. Duplicate the Prompt Template for each prompt you store.
2. Keep the Title, Purpose and Example sections updated.
3. Use Tags for easy searching.

---

## Index

| ID | Title | Tags | Last updated |
|----|-------|------|--------------|
| 1 | Search Engine Query Bookmarklet | javascript, bookmarklet, search-engine, utility | 2026-02-20 |

---

## Prompt Template

### ID: 1

- Title: Search Engine Query Bookmarklet
- Tags: javascript, bookmarklet, search-engine, utility
- Purpose: Create a JavaScript bookmarklet that extracts search queries from current page and opens them in alternative search engines.
- Context / Notes: User wants a self-contained JavaScript solution that works as a bookmarklet in browsers. Should handle multiple search engines and their query parameters.
- Model: DeepSeek-V3.2
- Temperature / Settings: temperature=0.2, max_tokens=500 (temperature controls output randomness, range 0-1, lower values produce more deterministic output; max_tokens limits maximum tokens in the generated response)
- Author: 
- Created: 2026-02-20
- Updated: 2026-02-20

#### Prompt (raw)

```
Please write a JavaScript function that captures the current search query from the URL of the search engine in the browser. The code should also be able to construct a new URL for an alternative search engine with the same query. As I want to deploy the JavaScript code in a bookmark (so it becomes a bookmarklet) in my browser, when clicked it opens up a new tab with the search query on an alternative search engine.
```

#### Example Input / Variables

- Current URL: A search engine results page URL (e.g., `https://www.google.com/search?q=javascript+tutorial`)

#### Example Output (expected)

```javascript
/**
 * Extracts the search query from the current browser URL for various search engines.
 * @returns {string|null} The extracted search query, or null if not found.
 */
function getSearchQuery() {
    const url = new URL(window.location.href);
    const hostname = url.hostname.toLowerCase();
    const searchParams = url.searchParams;
    
    // Mapping of search engine domains to their query parameter names
    const searchEngines = {
        'www.google.com': 'q',
        'google.com': 'q',
        'www.bing.com': 'q',
        'bing.com': 'q',
        'www.duckduckgo.com': 'q',
        'duckduckgo.com': 'q',
        'www.ecosia.org': 'q',
        'ecosia.org': 'q',
        'www.startpage.com': 'query',
        'startpage.com': 'query',
        'www.baidu.com': 'wd',
        'baidu.com': 'wd',
        'www.yandex.com': 'text',
        'yandex.com': 'text',
        'www.yahoo.com': 'p',
        'yahoo.com': 'p'
    };
    
    const queryParam = searchEngines[hostname];
    if (queryParam) {
        const query = searchParams.get(queryParam);
        if (query && query.trim() !== '') {
            return decodeURIComponent(query.trim());
        }
    }
    
    // Generic fallback: try common query parameter names
    const commonParams = ['q', 'query', 'search', 'p', 'wd', 'text', 's', 'term'];
    for (const param of commonParams) {
        const query = searchParams.get(param);
        if (query && query.trim() !== '') {
            return decodeURIComponent(query.trim());
        }
    }
    
    return null;
}

/**
 * Constructs a search URL for a target search engine with the given query.
 * @param {string} targetEngine - The target search engine name (e.g., 'google', 'bing', 'duckduckgo')
 * @param {string} query - The search query
 * @returns {string|null} The constructed URL, or null if target engine is not supported.
 */
function constructSearchUrl(targetEngine, query) {
    const engineTemplates = {
        'google': 'https://www.google.com/search?q={query}',
        'bing': 'https://www.bing.com/search?q={query}',
        'duckduckgo': 'https://duckduckgo.com/?q={query}',
        'ecosia': 'https://www.ecosia.org/search?q={query}',
        'startpage': 'https://www.startpage.com/search?query={query}',
        'baidu': 'https://www.baidu.com/s?wd={query}',
        'yandex': 'https://yandex.com/search/?text={query}',
        'yahoo': 'https://search.yahoo.com/search?p={query}'
    };
    
    const template = engineTemplates[targetEngine.toLowerCase()];
    if (!template) return null;
    
    const encodedQuery = encodeURIComponent(query);
    return template.replace('{query}', encodedQuery);
}

/**
 * Bookmarklet function: Opens the same search query in an alternative search engine.
 * Usage: Save as bookmarklet: javascript:(function(){...})()
 */
function openInAlternativeSearchEngine(targetEngine = 'duckduckgo') {
    const query = getSearchQuery();
    if (!query) {
        alert('Not on a search engine page or no query found.');
        return;
    }
    
    const url = constructSearchUrl(targetEngine, query);
    if (url) {
        window.open(url, '_blank');
    }
}

// Minified bookmarklet version (example):
// javascript:(function(){const u=new URL(window.location.href);let q=u.searchParams.get('q')||u.searchParams.get('query')||u.searchParams.get('p')||u.searchParams.get('wd')||u.searchParams.get('text')||u.searchParams.get('search')||u.searchParams.get('s')||u.searchParams.get('term');if(q){const e=encodeURIComponent(q.trim());window.open('https://duckduckgo.com/?q='+e,'_blank');}else{alert('No search query found.');}})();
```

#### Notes / Iterations

- v1: Initial prompt requesting a JavaScript function to capture search query from URL.
- v2: Added requirement to construct alternative search engine URLs and deploy as a bookmarklet.

---

End of template