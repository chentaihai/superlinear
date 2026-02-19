# CVPR 2024 Papers Dataset Schema

## Overview
This dataset contains metadata for 2,716 papers presented at the IEEE/CVF Conference on Computer Vision and Pattern Recognition (CVPR) 2024. The data was extracted from the official Open Access website: https://openaccess.thecvf.com/CVPR2024?day=all

## Data Format
The dataset is stored as a JSON array of paper objects. Each object follows the schema described below.

## Schema Definition

### Root Object
- **Type**: Array of Paper objects
- **Count**: 2,716 papers

### Paper Object
| Field | Type | Description | Example | Notes |
|-------|------|-------------|---------|-------|
| `title` | String | Full title of the paper | "Unmixing Diffusion for Self‑Supervised Hyperspectral Image Denoising" | Always present |
| `authors` | Array of Strings | List of author names | `["Haijin Zeng", "Jiezhang Cao", "Kai Zhang", ...]` | Extracted from comma‑separated list; always present |
| `abstract` | String | Paper abstract | `""` | **Not available** on this page; field exists for future use |
| `pdf_url` | String or `null` | URL to the official CVPR PDF | `"https://openaccess.thecvf.com/content/CVPR2024/papers/Zeng_Unmixing_Diffusion_for_Self‑Supervised_Hyperspectral_Image_Denoising_CVPR_2024_paper.pdf"` | Present for most papers; may be `null` if not found |
| `supplementary_url` | String or `null` | URL to supplementary materials (PDF, ZIP, etc.) | `"https://openaccess.thecvf.com/content/CVPR2024/supplemental/Zeng_Unmixing_Diffusion_for_CVPR_2024_supplemental.pdf"` | Present for many papers; may be `null` |
| `arxiv_url` | String or `null` | URL to arXiv preprint (if available) | `"http://arxiv.org/abs/2306.09348"` | Present only if an arXiv link was provided on the page |
| `bibtex` | String or `null` | Complete BibTeX citation entry | `"@InProceedings{Zeng_2024_CVPR,\n    author    = {Zeng, Haijin and Cao, Jiezhang and Zhang, Kai and Chen, Yongyong and Luong, Hiep and Philips, Wilfried},\n    title     = {Unmixing Diffusion for Self‑Supervised Hyperspectral Image Denoising},\n    booktitle = {Proceedings of the IEEE/CVF Conference on Computer Vision and Pattern Recognition (CVPR)},\n    month     = {June},\n    year      = {2024},\n    pages     = {27820‑27830}\n}"` | Present for all papers; extracted from hidden `div.bibref` |

## Data Quality Notes
1. **Abstract**: The field is intentionally empty because the source page does not display abstracts. To obtain abstracts, you would need to scrape individual paper pages.
2. **URLs**: All PDF and supplementary URLs use the `https://openaccess.thecvf.com/` domain. arXiv URLs point to `http://arxiv.org/abs/`.
3. **BibTeX**: The BibTeX entries follow a consistent format and include the paper's pages in the proceedings.
4. **Authors**: Author names are extracted as plain text; no affiliation or ORCID information is included.
5. **Missing values**: A `null` value indicates the link was not present on the page.

## Example Paper
```json
{
  "title": "Seeing the World through Your Eyes",
  "authors": [
    "Hadi Alzayer",
    "Kevin Zhang",
    "Brandon Feng",
    "Christopher A. Metzler",
    "Jia‑Bin Huang"
  ],
  "abstract": "",
  "pdf_url": "https://openaccess.thecvf.com/content/CVPR2024/papers/Alzayer_Seeing_the_World_through_Your_Eyes_CVPR_2024_paper.pdf",
  "supplementary_url": "https://openaccess.thecvf.com/content/CVPR2024/supplemental/Alzayer_Seeing_the_World_CVPR_2024_supplemental.pdf",
  "arxiv_url": "http://arxiv.org/abs/2306.09348",
  "bibtex": "@InProceedings{Alzayer_2024_CVPR,\n    author    = {Alzayer, Hadi and Zhang, Kevin and Feng, Brandon and Metzler, Christopher A. and Huang, Jia‑Bin},\n    title     = {Seeing the World through Your Eyes},\n    booktitle = {Proceedings of the IEEE/CVF Conference on Computer Vision and Pattern Recognition (CVPR)},\n    month     = {June},\n    year      = {2024},\n    pages     = {4864‑4873}\n}"
}
```

## Extraction Script
The dataset was generated using `extract_papers_only.py`, which:
1. Fetches the HTML from the CVPR 2024 Open Access page.
2. Parses the `<dl>` structure where each paper is represented as:
   - `<dt class="ptitle">` containing the title link.
   - First `<dd>` sibling containing plain‑text author list.
   - Second `<dd>` sibling containing PDF, supplementary, arXiv links, and a hidden BibTeX `div.bibref`.
3. Outputs a clean JSON array.

## Potential Extensions
- Add abstract scraping from individual paper pages.
- Extract keywords or topics if available.
- Include DOI or other persistent identifiers.
- Add publication date and session information.

## License
The data is sourced from the publicly available CVPR 2024 Open Access proceedings. Please respect the CVF's terms of use and cite papers appropriately when using this dataset.