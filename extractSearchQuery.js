/**
 * Extracts the search query from the current browser URL for various search engines.
 * This function works on Search Engine Results Pages (SERPs) and returns the user's search term.
 * 
 * @returns {string|null} The extracted search query, or null if not found or not a search engine page.
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
        'www.yahoo.com': 'p',
        'yahoo.com': 'p',
        'search.yahoo.com': 'p',
        'www.duckduckgo.com': 'q',
        'duckduckgo.com': 'q',
        'www.baidu.com': 'wd',
        'baidu.com': 'wd',
        'www.yandex.com': 'text',
        'yandex.com': 'text',
        'www.ecosia.org': 'q',
        'ecosia.org': 'q',
        'www.startpage.com': 'query',
        'startpage.com': 'query',
        'www.qwant.com': 'q',
        'qwant.com': 'q',
        'www.searx.me': 'q',
        'searx.me': 'q',
        'www.wolframalpha.com': 'i',
        'wolframalpha.com': 'i'
    };
    
    // Check if current hostname matches a known search engine
    const queryParam = searchEngines[hostname];
    
    if (queryParam) {
        // Try to get query from search parameters
        const query = searchParams.get(queryParam);
        if (query && query.trim() !== '') {
            return decodeURIComponent(query.trim());
        }
        
        // For some search engines, the query might be in the hash fragment or path
        // Additional handling for specific search engines
        if (hostname.includes('google') && url.pathname.startsWith('/search')) {
            // Google sometimes has query in path (e.g., /search?q=... is already handled above)
            // Additional fallback: check for 'q' parameter in hash
            const hashParams = new URLSearchParams(url.hash.substring(1));
            const hashQuery = hashParams.get('q');
            if (hashQuery) {
                return decodeURIComponent(hashQuery.trim());
            }
        }
        
        // Baidu may also use 'word' parameter
        if (hostname.includes('baidu')) {
            const wordQuery = searchParams.get('word');
            if (wordQuery && wordQuery.trim() !== '') {
                return decodeURIComponent(wordQuery.trim());
            }
        }
        
        // If no query found but we're on a search engine page, try to extract from URL path
        // This is a fallback for unconventional URL structures
        const pathParts = url.pathname.split('/');
        for (let i = 0; i < pathParts.length; i++) {
            if (pathParts[i] === 'search' && i + 1 < pathParts.length) {
                // Some engines use /search/query format
                const potentialQuery = pathParts[i + 1];
                if (potentialQuery && potentialQuery.trim() !== '') {
                    return decodeURIComponent(potentialQuery.trim());
                }
            }
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
    
    // Try to extract from hash fragment
    if (url.hash) {
        const hashParams = new URLSearchParams(url.hash.substring(1));
        for (const param of commonParams) {
            const query = hashParams.get(param);
            if (query && query.trim() !== '') {
                return decodeURIComponent(query.trim());
            }
        }
    }
    
    // Not a search engine page or query not found
    return null;
}

/**
 * Alternative function that returns both the search engine name and the query.
 * 
 * @returns {Object|null} Object with {engine: string, query: string} or null if not found.
 */
function getSearchEngineAndQuery() {
    const url = new URL(window.location.href);
    const hostname = url.hostname.toLowerCase();
    
    // Mapping of search engine domains to their names and query parameters
    const searchEngines = {
        'www.google.com': { name: 'Google', param: 'q' },
        'google.com': { name: 'Google', param: 'q' },
        'www.bing.com': { name: 'Bing', param: 'q' },
        'bing.com': { name: 'Bing', param: 'q' },
        'www.yahoo.com': { name: 'Yahoo', param: 'p' },
        'yahoo.com': { name: 'Yahoo', param: 'p' },
        'search.yahoo.com': { name: 'Yahoo', param: 'p' },
        'www.duckduckgo.com': { name: 'DuckDuckGo', param: 'q' },
        'duckduckgo.com': { name: 'DuckDuckGo', param: 'q' },
        'www.baidu.com': { name: 'Baidu', param: 'wd' },
        'baidu.com': { name: 'Baidu', param: 'wd' },
        'www.yandex.com': { name: 'Yandex', param: 'text' },
        'yandex.com': { name: 'Yandex', param: 'text' },
        'www.ecosia.org': { name: 'Ecosia', param: 'q' },
        'ecosia.org': { name: 'Ecosia', param: 'q' },
        'www.startpage.com': { name: 'Startpage', param: 'query' },
        'startpage.com': { name: 'Startpage', param: 'query' },
        'www.qwant.com': { name: 'Qwant', param: 'q' },
        'qwant.com': { name: 'Qwant', param: 'q' },
        'www.searx.me': { name: 'Searx', param: 'q' },
        'searx.me': { name: 'Searx', param: 'q' },
        'www.wolframalpha.com': { name: 'WolframAlpha', param: 'i' },
        'wolframalpha.com': { name: 'WolframAlpha', param: 'i' }
    };
    
    const engineInfo = searchEngines[hostname];
    if (engineInfo) {
        const query = url.searchParams.get(engineInfo.param);
        if (query && query.trim() !== '') {
            return {
                engine: engineInfo.name,
                query: decodeURIComponent(query.trim())
            };
        }
        
        // Baidu fallback for 'word' parameter
        if (engineInfo.name === 'Baidu') {
            const wordQuery = url.searchParams.get('word');
            if (wordQuery && wordQuery.trim() !== '') {
                return {
                    engine: engineInfo.name,
                    query: decodeURIComponent(wordQuery.trim())
                };
            }
        }
    }
    
    // Generic search for any engine
    const commonParams = ['q', 'query', 'search', 'p', 'wd', 'text', 's', 'term'];
    for (const param of commonParams) {
        const query = url.searchParams.get(param);
        if (query && query.trim() !== '') {
            // Try to identify engine by hostname pattern
            let engineName = 'Unknown';
            if (hostname.includes('google')) engineName = 'Google';
            else if (hostname.includes('bing')) engineName = 'Bing';
            else if (hostname.includes('yahoo')) engineName = 'Yahoo';
            else if (hostname.includes('duckduckgo')) engineName = 'DuckDuckGo';
            else if (hostname.includes('baidu')) engineName = 'Baidu';
            else if (hostname.includes('yandex')) engineName = 'Yandex';
            else if (hostname.includes('ecosia')) engineName = 'Ecosia';
            
            return {
                engine: engineName,
                query: decodeURIComponent(query.trim())
            };
        }
    }
    
    return null;
}

/**
 * Constructs a search URL for a target search engine with the given query.
 * 
 * @param {string} targetEngine - The target search engine name (e.g., 'google', 'bing', 'duckduckgo', 'ecosia', 'startpage')
 * @param {string} query - The search query
 * @returns {string|null} The constructed URL, or null if target engine is not supported.
 */
function constructSearchUrl(targetEngine, query) {
    const engineTemplates = {
        'google': 'https://www.google.com/search?q={query}',
        'bing': 'https://www.bing.com/search?q={query}',
        'yahoo': 'https://search.yahoo.com/search?p={query}',
        'duckduckgo': 'https://duckduckgo.com/?q={query}',
        'baidu': 'https://www.baidu.com/s?wd={query}',
        'yandex': 'https://yandex.com/search/?text={query}',
        'ecosia': 'https://www.ecosia.org/search?q={query}',
        'startpage': 'https://www.startpage.com/search?query={query}',
        'qwant': 'https://www.qwant.com/?q={query}',
        'searx': 'https://searx.me/search?q={query}',
        'wolframalpha': 'https://www.wolframalpha.com/input/?i={query}',
        'brave': 'https://search.brave.com/search?q={query}',
        'swisscows': 'https://swisscows.com/web?query={query}'
    };
    
    const template = engineTemplates[targetEngine.toLowerCase()];
    if (!template) {
        return null;
    }
    
    const encodedQuery = encodeURIComponent(query);
    return template.replace('{query}', encodedQuery);
}

/**
 * Gets the current search engine name (if any) and provides alternative search URLs.
 * 
 * @returns {Object|null} Object with {currentEngine: string, query: string, alternatives: Object} 
 *                        or null if not on a search engine page.
 */
function getSearchEngineAlternatives() {
    const result = getSearchEngineAndQuery();
    if (!result) {
        return null;
    }
    
    const alternatives = {};
    const engineTemplates = ['google', 'bing', 'yahoo', 'duckduckgo', 'baidu', 'yandex', 'ecosia', 'startpage', 'qwant', 'searx'];
    
    for (const engine of engineTemplates) {
        const url = constructSearchUrl(engine, result.query);
        if (url) {
            alternatives[engine] = url;
        }
    }
    
    return {
        currentEngine: result.engine,
        query: result.query,
        alternatives: alternatives
    };
}

/**
 * Bookmarklet function: Opens the same search query in an alternative search engine.
 * By default, it cycles through a predefined list of engines.
 * 
 * Usage: Save as bookmarklet: javascript:(function(){...})()
 */
function openInAlternativeSearchEngine(targetEngine = null) {
    const query = getSearchQuery();
    if (!query) {
        alert('Not on a search engine page or no query found.');
        return;
    }
    
    // Define a preferred order of alternative engines
    const enginePreference = ['duckduckgo', 'ecosia', 'startpage', 'bing', 'google'];
    
    // Get current engine info
    const currentInfo = getSearchEngineAndQuery();
    const currentEngine = currentInfo ? currentInfo.engine.toLowerCase() : null;
    
    // Determine target engine
    let target = targetEngine;
    if (!target) {
        // If no target specified, pick the first preferred engine that's not the current one
        for (const engine of enginePreference) {
            if (!currentEngine || engine !== currentEngine) {
                target = engine;
                break;
            }
        }
        // If all preferences match current engine, default to duckduckgo
        if (!target) {
            target = 'duckduckgo';
        }
    }
    
    const url = constructSearchUrl(target, query);
    if (url) {
        window.open(url, '_blank');
    } else {
        alert(`Unsupported search engine: ${target}`);
    }
}

// Export for Node.js/CommonJS environments
if (typeof module !== 'undefined' && module.exports) {
    module.exports = {
        getSearchQuery,
        getSearchEngineAndQuery,
        constructSearchUrl,
        getSearchEngineAlternatives,
        openInAlternativeSearchEngine
    };
}

// For direct browser use, attach to window object
if (typeof window !== 'undefined') {
    window.getSearchQuery = getSearchQuery;
    window.getSearchEngineAndQuery = getSearchEngineAndQuery;
    window.constructSearchUrl = constructSearchUrl;
    window.getSearchEngineAlternatives = getSearchEngineAlternatives;
    window.openInAlternativeSearchEngine = openInAlternativeSearchEngine;
}