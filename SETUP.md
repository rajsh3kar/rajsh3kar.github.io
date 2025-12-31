# Academic Website - Automated Setup

This is a professional academic website powered by Jekyll and the al-folio theme, with **automated publication sync from Google Scholar**.

## 🎯 Key Features

### 1. **Automatic Google Scholar Sync**
- Publications are automatically fetched from your Google Scholar profile
- No manual BibTeX editing required
- Updates daily via GitHub Actions
- Citation counts automatically displayed

### 2. **Auto-Generated News Announcements**
- New publications automatically appear as news items
- No need to create individual announcement files
- Sorted chronologically with latest first

### 3. **Professional Layout**
- Research-focused homepage
- Clean navigation (About → Publications → News)
- Integrated CV and social links
- Mobile-responsive design

### 4. **Smart Citation Display**
- Real-time citation counts from Google Scholar
- Publication badges (Altmetric, Dimensions)
- H-index calculation
- Selected papers highlighted

## 🚀 Quick Start

### Initial Setup

1. **Update your Google Scholar ID** (already done):
   - Your Scholar ID: `wq36gfgAAAAJ`
   - Configured in `_config.yml` and automation scripts

2. **Enable GitHub Actions**:
   - Go to repository Settings → Actions → General
   - Enable "Read and write permissions" for workflows
   - This allows automatic updates to be committed

3. **First Sync** (Optional - Manual):
   ```bash
   # Install Python dependencies
   pip install -r requirements.txt
   
   # Run the sync script manually
   python scripts/fetch_scholar_publications.py
   ```

### How It Works

#### Daily Automation
- GitHub Actions runs daily at 2 AM UTC
- Fetches latest publications from Google Scholar
- Updates `_bibliography/papers.bib`
- Generates news announcements in `_news/`
- Commits and pushes changes automatically

#### Manual Trigger
You can also trigger the sync manually:
1. Go to Actions tab in GitHub
2. Select "Fetch Google Scholar Data" workflow
3. Click "Run workflow"

## 📁 File Structure

```
├── _bibliography/
│   └── papers.bib          # Auto-updated from Google Scholar
├── _data/
│   ├── publications.yml    # Auto-generated metrics (h-index, citations)
│   ├── cv.yml             # Your CV data (manual updates)
│   └── venues.yml         # Conference/journal styling
├── _news/
│   ├── auto_pub_*.md      # Auto-generated from publications
│   └── announcement_*.md  # Manual announcements (optional)
├── _pages/
│   ├── about.md           # Homepage
│   ├── publications.md    # Publications page
│   ├── news.md            # News page
│   └── cv.md              # CV page
├── scripts/
│   └── fetch_scholar_publications.py  # Main sync script
└── .github/workflows/
    └── fetch-scholar-data.yml         # Automation workflow
```

## 🔧 Configuration

### Google Scholar Settings (`_config.yml`)

```yaml
scholar_userid: wq36gfgAAAAJ  # Your Google Scholar ID

enable_publication_badges:
  google_scholar: true        # Show citation counts
  altmetric: true            # Show Altmetric badges
  dimensions: true           # Show Dimensions badges
```

### Publication Display

**Selected Papers**: Papers with >20 citations are automatically marked as "selected" and appear on the homepage.

**Venue Abbreviations**: Configured in `_data/venues.yml`:
- ICDCS, ICDCN, NOMS, MobiQuitous, JNSM

### News Announcements

**Auto-generated**: Publications from the last 2 years automatically appear as news.

**Manual**: You can still add custom announcements in `_news/`:
```markdown
---
layout: post
date: 2025-01-15
inline: true
---
Your custom announcement here.
```

## 📝 Updating Content

### CV Updates
Edit `_data/cv.yml` to update your CV:
```yaml
- title: Education
  type: time_table
  contents:
    - title: PhD
      institution: IIT Bhilai
      year: "2019 - Present"
```

### Homepage Bio
Edit `_pages/about.md` to update your bio and research interests.

### Manual Publications
While publications auto-sync from Google Scholar, you can manually add entries to `_bibliography/papers.bib` if needed.

## 🎨 Customization

### Theme Colors
Edit `_sass/_themes.scss` to customize colors.

### Navigation
Edit individual page YAML front matter to control `nav` and `nav_order`.

### Social Links
Update social media links in `_config.yml`:
```yaml
github_username: rajsh3kar
linkedin_username: kolichala-rajashekar-a20b37a3
x_username: rajsh3kar
```

## 🚨 Troubleshooting

### Publications not updating?
1. Check GitHub Actions tab for errors
2. Verify Scholar ID is correct in `_config.yml`
3. Ensure GitHub Actions has write permissions

### Build failing?
1. Check for Jekyll syntax errors in markdown files
2. Verify all dependencies are installed
3. Run `bundle install` to update gems

### Manual sync not working?
```bash
# Install/update dependencies
pip install --upgrade scholarly bibtexparser pyyaml

# Run with verbose output
python -v scripts/fetch_scholar_publications.py
```

## 📊 Analytics & Metrics

The automation script generates `_data/publications.yml` with:
- Total publications count
- Total citations
- H-index
- Recent publications list

This data can be displayed on your homepage using Liquid templates.

## 🔐 Security

- No API keys required for Google Scholar (public data)
- GitHub Actions uses built-in `GITHUB_TOKEN`
- All credentials managed via GitHub Secrets

## 📚 Resources

- [al-folio Documentation](https://github.com/alshedivat/al-folio)
- [Jekyll Documentation](https://jekyllrb.com/docs/)
- [Google Scholar Citations](https://scholar.google.com/citations?user=wq36gfgAAAAJ)

## ✨ Benefits of This Setup

1. **Zero Manual Work**: Publications sync automatically
2. **Always Up-to-Date**: Daily checks for new papers
3. **Professional**: Clean, academic-focused design
4. **SEO-Optimized**: Proper metadata for Google indexing
5. **Mobile-Friendly**: Responsive design
6. **Fast Loading**: Optimized assets and lazy loading

---

**Last Updated**: December 31, 2025
**Maintainer**: Kolichala Rajashekar
**Theme**: al-folio with custom automation
