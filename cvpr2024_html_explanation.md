# CVPR 2024 HTML File Documentation

## Overview
`cvpr2024.html` is a local copy of the complete CVPR 2024 Open Access repository webpage, downloaded for offline analysis, data extraction, and archival purposes. This file serves as the raw source material from which the structured JSON dataset (`cvpr2024_papers.json`) was generated.

## Why This File Was Generated

### 1. **Data Preservation and Archival**
- The official website (https://openaccess.thecvf.com/CVPR2024?day=all) contains 2,716 papers from CVPR 2024.
- Downloading the HTML ensures the data remains accessible even if:
  - The original website changes structure
  - Content is removed or modified
  - Network connectivity is unavailable
  - The website experiences downtime

### 2. **Efficient Web Scraping**
- Multiple scraping attempts can be made on the local file without:
  - Overloading the CVF servers with repeated requests
  - Violating potential rate limits
  - Encountering network latency issues
- Local processing is significantly faster than repeated HTTP requests.

### 3. **Data Integrity and Reproducibility**
- Having a fixed snapshot allows:
  - Exact reproduction of the dataset extraction process
  - Debugging and validation of parsing logic
  - Comparison between different extraction methods
  - Version control of the source data

### 4. **Ethical Web Scraping Practice**
- Downloaded once with proper attribution
- Contains all copyright notices and disclaimers from the original site
- Respects the Computer Vision Foundation's terms of use
- Minimizes impact on the CVF infrastructure

## How It Was Generated

The file was created using a simple `curl` command that downloaded the complete HTML content:

```bash
curl -s "https://openaccess.thecvf.com/CVPR2024?day=all" > cvpr2024.html
```

This command:
- Uses the `-s` flag for silent operation (no progress meter)
- Fetches the complete page with all papers (`?day=all`)
- Redirects the output to the local file `cvpr2024.html`

## File Structure and Content

### Key Structural Elements
The HTML follows a consistent pattern for each paper entry:

```html
<dt class="ptitle">
  <a href="/content/CVPR2024/html/Zeng_Unmixing_Diffusion_for_...html">
    Unmixing Diffusion for Self-Supervised Hyperspectral Image Denoising
  </a>
</dt>
<dd>
  <!-- Author names in individual form elements -->
  <form>...</form>
</dd>
<dd>
  [<a href="/content/CVPR2024/papers/Zeng_...pdf">pdf</a>]
  [<a href="/content/CVPR2024/supplemental/Zeng_...pdf">supp</a>]
  <div class="bibref">@InProceedings{...}</div>
</dd>
```

### Data Components Preserved
1. **Paper Titles**: In `<dt class="ptitle">` elements with hyperlinks
2. **Authors**: In `<dd>` elements following each title
3. **PDF Links**: Direct URLs to the full papers
4. **Supplementary Material**: Links to additional resources (PDFs, ZIPs)
5. **BibTeX Citations**: Hidden in expandable `div.bibref` elements
6. **Metadata**: Conference branding, copyright notices, search functionality

## Relationship to the JSON Dataset

### Extraction Pipeline
```
cvpr2024.html (raw HTML)
    ↓
extract_papers_only.py (Python parser)
    ↓
cvpr2024_papers.json (structured data)
```

### Extraction Logic (from `extract_papers_only.py`)
The parser:
1. Locates all `<dt class="ptitle">` elements
2. Extracts the paper title from the anchor tag
3. Finds the next `<dd>` containing author names
4. Extracts author names from comma-separated text
5. Finds the following `<dd>` containing PDF, supplementary, and BibTeX links
6. Constructs complete URLs using the base domain
7. Outputs a clean JSON array with consistent schema

### Why Not Scrape Directly Every Time?
While the Python script could fetch the webpage directly each time, using the local HTML file:
- **Reduces External Dependencies**: No internet connection required
- **Improves Reliability**: Network issues won't affect data access
- **Enables Versioning**: Track changes to source data over time
- **Facilitates Testing**: Safe environment for parser development

## Importance in the Research Workflow

### For Data Analysis
- Researchers can perform text mining on paper titles and author lists
- Bibliometric analysis of authorship patterns and collaboration networks
- Topic modeling based on paper titles and keywords

### For Machine Learning Applications
- Training data for citation prediction models
- Dataset for paper recommendation systems
- Source for academic knowledge graphs

### For Academic Research
- Reference dataset for computer vision literature reviews
- Baseline for comparing conference paper characteristics year-over-year
- Foundation for studying trends in CVPR publications

## Usage Guidelines

### Ethical Considerations
- This file contains copyrighted material
- Use only for research and educational purposes
- Cite original papers when using extracted data
- Respect the CVF's terms of service

### Technical Notes
- File size: Approximately 2.8 MB
- Encoding: UTF-8
- Line count: 24,413 lines
- Contains complete webpage including CSS, JavaScript, and images

### Recommended Workflow
1. Use `cvpr2024.html` as the authoritative source for paper metadata
2. Apply parsing scripts to extract structured data
3. Validate extracted data against the HTML source
4. Update parsing logic if website structure changes
5. Maintain the HTML file as part of the research dataset

## Updates and Maintenance

### When to Refresh the HTML
Consider downloading a fresh copy when:
1. New papers are added to the CVPR 2024 proceedings
2. Corrections are made to existing paper metadata
3. The website structure significantly changes
4. Starting a new research project requiring current data

### Version Control
- Track changes to the HTML file in version control
- Note the download date and time in commit messages
- Consider creating checksums to detect file corruption

## Conclusion

`cvpr2024.html` is more than just a downloaded webpage—it's a research artifact that:
- **Preserves** the state of CVPR 2024 publications at a specific point in time
- **Enables** reproducible data extraction and analysis
- **Supports** ethical web scraping practices
- **Facilitates** computer vision research and bibliometric studies

By maintaining this local copy alongside the extracted JSON dataset, researchers ensure data integrity, enable offline analysis, and create a foundation for reproducible research in computer vision literature analysis.