# Website Automation Architecture

## 📊 System Overview

```
┌─────────────────────────────────────────────────────────────┐
│                    Google Scholar Profile                     │
│              https://scholar.google.com/...                   │
│         (Your publications, citations, metrics)               │
└───────────────────────┬─────────────────────────────────────┘
                        │
                        │ Fetch Daily (2 AM UTC)
                        │
                        ▼
┌─────────────────────────────────────────────────────────────┐
│              GitHub Actions Workflow                          │
│         (.github/workflows/fetch-scholar-data.yml)            │
│                                                               │
│  1. Install Python & dependencies                             │
│  2. Run fetch_scholar_publications.py                         │
│  3. Parse Google Scholar data                                 │
│  4. Generate BibTeX entries                                   │
│  5. Create news announcements                                 │
│  6. Calculate metrics (h-index, citations)                    │
│  7. Commit & push changes                                     │
└───────────────────────┬─────────────────────────────────────┘
                        │
                        │ Auto-commit
                        │
                        ▼
┌─────────────────────────────────────────────────────────────┐
│                  GitHub Repository                            │
│              rajsh3kar/rajsh3kar.github.io                    │
│                                                               │
│  Updated Files:                                               │
│  ├── _bibliography/papers.bib      (Publications)            │
│  ├── _news/auto_pub_*.md          (News items)               │
│  └── _data/publications.yml        (Metrics)                 │
└───────────────────────┬─────────────────────────────────────┘
                        │
                        │ Trigger build
                        │
                        ▼
┌─────────────────────────────────────────────────────────────┐
│                   GitHub Pages                                │
│              (Jekyll Build & Deploy)                          │
│                                                               │
│  1. Processes Liquid templates                                │
│  2. Generates HTML from Markdown                              │
│  3. Applies al-folio theme                                    │
│  4. Deploys to production                                     │
└───────────────────────┬─────────────────────────────────────┘
                        │
                        │ Live in ~2 minutes
                        │
                        ▼
┌─────────────────────────────────────────────────────────────┐
│                  Live Website                                 │
│           https://rajsh3kar.github.io                         │
│                                                               │
│  ✓ Updated publications                                       │
│  ✓ Latest citation counts                                     │
│  ✓ New announcements                                          │
│  ✓ Current metrics                                            │
└─────────────────────────────────────────────────────────────┘
```

## 🔄 Data Flow

### 1. Google Scholar → Python Script

```python
# scholarly library fetches:
- Publication titles
- Authors
- Venues (journals/conferences)
- Years
- Citation counts
- Author IDs
```

### 2. Python Script → BibTeX

```bibtex
@inproceedings{rajashekar2024towards,
  abbr={NOMS},
  title={Towards a Mobility-cum-Battery Aware...},
  author={Rajashekar, Kolichala and ...},
  year={2024},
  selected={true}  # Auto-marked if citations > 20
}
```

### 3. BibTeX → Website

```markdown
<!-- Jekyll processes BibTeX with jekyll-scholar plugin -->
<!-- Note: This works on the custom deploy workflow, not GitHub Pages default -->
Publications are automatically rendered from _bibliography/papers.bib
with venue colors, citation counts, and links.
```

### 4. News Generation

```
Publication (2024) → auto_pub_2024_1.md → News feed
Publication (2023) → auto_pub_2023_1.md → News feed
```

## 📅 Automation Schedule

```
Daily:
  02:00 UTC - Run Scholar sync
  02:05 UTC - Commit changes
  02:10 UTC - GitHub Pages builds
  02:12 UTC - Site updated

Manual:
  On push - Immediate rebuild
  On workflow dispatch - Run sync anytime
```

## 🎯 Key Components

### 1. Fetch Script (`fetch_scholar_publications.py`)
- **Input**: Google Scholar ID
- **Process**: 
  - Fetch publications
  - Convert to BibTeX
  - Generate news
  - Calculate metrics
- **Output**: 
  - Updated `papers.bib`
  - New announcement files
  - Metrics YAML

### 2. GitHub Actions (`fetch-scholar-data.yml`)
- **Trigger**: Daily cron or manual
- **Environment**: Ubuntu + Python 3.11
- **Permissions**: Read/write repository
- **Result**: Automated commits

### 3. Jekyll Scholar (`_config.yml`)
- **Source**: `_bibliography/papers.bib`
- **Template**: `_layouts/bib.liquid`
- **Features**:
  - Citation counts
  - Venue badges
  - Altmetric scores
  - PDF links

### 4. News System (`_includes/news.liquid`)
- **Source**: `_news/*.md` files
- **Sorting**: Chronological (newest first)
- **Display**: Homepage + News page
- **Types**:
  - Auto-generated (publications)
  - Manual (awards, talks, etc.)

## 🔐 Security & Permissions

```
GitHub Token (automatic):
  ✓ Read repository
  ✓ Write repository
  ✓ Commit files
  ✗ No external secrets needed

Google Scholar (public):
  ✓ Public profile data
  ✓ No authentication required
  ✗ Rate limited (handled by delays)
```

## 📈 Metrics Calculation

```python
# Automatically calculated:
- Total publications: len(publications)
- Total citations: sum(citations)
- H-index: max(i where citations[i] >= i)
- Recent papers: filter(year >= current_year - 3)
```

## 🎨 Styling & Display

```
Venue Colors (_data/venues.yml):
  ICDCS → IEEE Blue (#00539B)
  ICDCN → ACM Blue (#0085CA)
  NOMS → IEEE Blue
  JNSM → Springer Gold (#FFD700)

Publication Badges:
  ✓ Google Scholar citations
  ✓ Altmetric score
  ✓ Dimensions metrics
  ✓ Award ribbons
```

## 🚀 Performance

```
Build Time: ~30 seconds
Deploy Time: ~2 minutes
Sync Time: ~1-2 minutes
Total: ~3-4 minutes from commit to live
```

## 💡 Benefits

1. **Zero Manual Work**: Set it and forget it
2. **Always Current**: Updates within 24 hours of new publication
3. **Professional**: Clean, academic-standard presentation
4. **Discoverable**: SEO-optimized, Google Scholar linked
5. **Reliable**: Automated testing, error handling
6. **Scalable**: Handles any number of publications
7. **Flexible**: Easy to customize and extend

---

**Last Updated**: December 31, 2025  
**Architecture Version**: 1.0  
**Status**: Production Ready ✅
