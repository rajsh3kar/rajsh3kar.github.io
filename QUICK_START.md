# Quick Reference Guide

## 🎯 What Changed?

Your website has been transformed from a manual-update site to a **fully automated academic portfolio** that syncs with Google Scholar.

## ✨ New Features

### 1. **Auto-Sync with Google Scholar**
- ✅ Daily automatic updates (2 AM UTC)
- ✅ Publications fetched from your profile: `wq36gfgAAAAJ`
- ✅ Citation counts automatically displayed
- ✅ No manual BibTeX editing needed

### 2. **Smart News System**
- ✅ Publications auto-generate news announcements
- ✅ Awards and achievements manually added
- ✅ Sorted chronologically

### 3. **Professional Design**
- ✅ Research-focused homepage
- ✅ Clean navigation
- ✅ Venue badges (ICDCS, ICDCN, NOMS, etc.)
- ✅ Selected papers highlighted

## 🚀 Next Steps

### 1. Test the Automation (Optional)
```bash
# Install Python dependencies
pip install scholarly bibtexparser pyyaml

# Test the connection
python scripts/test_scholar_sync.py

# Run full sync manually (optional)
python scripts/fetch_scholar_publications.py
```

### 2. Enable GitHub Actions
1. Go to your GitHub repository
2. Settings → Actions → General
3. Set "Workflow permissions" to **"Read and write permissions"**
4. Save

### 3. Trigger First Sync
- Go to "Actions" tab
- Select "Fetch Google Scholar Data"
- Click "Run workflow"

### 4. Build and Deploy
```bash
# Local testing (if you have Jekyll installed)
bundle install
bundle exec jekyll serve

# Or use Docker
docker-compose up
```

## 📋 File Changes Summary

### New Files Created
- `.github/workflows/fetch-scholar-data.yml` - Daily automation
- `scripts/fetch_scholar_publications.py` - Main sync script
- `scripts/test_scholar_sync.py` - Test script
- `SETUP.md` - Complete documentation
- `QUICK_START.md` - This file

### Files Modified
- `_config.yml` - Updated Scholar ID and settings
- `_pages/about.md` - Enhanced homepage content
- `_pages/publications.md` - Better description
- `_pages/news.md` - Added to navigation
- `_pages/cv.md` - Removed from main nav
- `_pages/dropdown.md` - Simplified menu
- `_data/venues.yml` - Your conferences/journals
- `_data/repositories.yml` - Cleaned up
- `_bibliography/papers.bib` - Added venue abbreviations
- `_news/*.md` - Improved announcements
- `requirements.txt` - Added Python packages

### Files Removed
- `_posts/*` - All sample blog posts (29 files)
- `_pages/about_einstein.md` - Sample page

## 🎨 Customization Options

### Update Your Bio
Edit `_pages/about.md` - Line 19 onwards

### Add Profile Picture
Place your photo at `assets/img/prof_pic.jpeg`

### Update CV
Edit `_data/cv.yml` with your information

### Add Manual News
Create files in `_news/` folder:
```markdown
---
layout: post
date: 2025-01-15
inline: true
---
Your announcement here.
```

## 📊 What Happens Automatically?

### Daily (2 AM UTC)
1. GitHub Action wakes up
2. Fetches your Google Scholar profile
3. Updates `_bibliography/papers.bib`
4. Generates news for recent papers
5. Updates metrics in `_data/publications.yml`
6. Commits and pushes changes
7. GitHub Pages rebuilds your site

### On Every Push
- GitHub Pages automatically rebuilds
- Changes go live in ~2 minutes

## 🔧 Common Tasks

### Add a Manual Announcement
```bash
cd _news
nano announcement_5.md
# Add your content, save
git add . && git commit -m "Add announcement" && git push
```

### Update Your Research Interests
```bash
nano _pages/about.md
# Edit line 19+ with your interests
git add . && git commit -m "Update bio" && git push
```

### Disable Automation (if needed)
```bash
# Delete or rename the workflow file
mv .github/workflows/fetch-scholar-data.yml .github/workflows/fetch-scholar-data.yml.disabled
```

## 🐛 Troubleshooting

### Publications not syncing?
1. Check Actions tab for errors
2. Verify workflow permissions
3. Check rate limits on Google Scholar

### Site not building?
1. Check for YAML syntax errors
2. Run `bundle exec jekyll build` locally
3. Check GitHub Pages settings

### Test script failing?
```bash
# Update packages
pip install --upgrade scholarly bibtexparser pyyaml

# Check internet connection
ping google.com

# Try again later (rate limiting)
```

## 📞 Need Help?

- **Documentation**: See `SETUP.md` for details
- **Theme Docs**: https://github.com/alshedivat/al-folio
- **Jekyll Docs**: https://jekyllrb.com/docs/

## ✅ Checklist

- [ ] Enable GitHub Actions permissions
- [ ] Test Scholar sync (optional)
- [ ] Add profile picture
- [ ] Update CV data
- [ ] Review homepage bio
- [ ] Check publications page
- [ ] Verify news feed
- [ ] Test site locally (optional)
- [ ] Push changes and deploy

---

**Your Site**: https://rajsh3kar.github.io  
**Google Scholar**: https://scholar.google.com/citations?user=wq36gfgAAAAJ  
**Repository**: https://github.com/rajsh3kar/rajsh3kar.github.io
