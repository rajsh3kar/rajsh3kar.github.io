# Kolichala Rajashekar - Academic Portfolio

Modern, fast academic portfolio built with Astro and Tailwind CSS.

## 🚀 Features

- ⚡ Lightning-fast static site generation with Astro
- 🎨 Modern, responsive design with Tailwind CSS
- 📚 Automatic Google Scholar publication sync
- 🔄 Daily automated updates via GitHub Actions
- 📱 Mobile-friendly and accessible
- 🚀 Deployed automatically to GitHub Pages

## 🛠️ Tech Stack

- **Framework:** Astro 4.0
- **Styling:** Tailwind CSS 3.4
- **Deployment:** GitHub Pages + GitHub Actions
- **Data Source:** Google Scholar API (via scholarly)

## 📦 Local Development

```bash
# Install dependencies
npm install

# Start dev server
npm run dev

# Build for production
npm run build

# Preview production build
npm run preview
```

## 🔄 Automated Updates

The site automatically:
1. Fetches publications from Google Scholar daily at 2 AM UTC
2. Updates publication data in `src/data/publications.json`
3. Commits changes and triggers rebuild
4. Deploys to GitHub Pages

## 📝 Configuration

- **Google Scholar ID:** Set in `.github/workflows/fetch-scholar.yml`
- **Site URL:** Set in `astro.config.mjs`
- **Personal Info:** Update in `src/pages/index.astro`

## 🎯 Benefits Over Jekyll/al-folio

- **10x faster builds** (seconds vs minutes)
- **No Ruby/Jekyll complexity**
- **Modern JavaScript ecosystem**
- **Better developer experience**
- **Simpler deployment** (no Jekyll plugins issues)
- **Easier to customize** (just HTML/CSS/JS)

## 📄 License

MIT

## 👤 Author

Kolichala Rajashekar  
PhD Scholar, IIT Bhilai  
[Google Scholar](https://scholar.google.com/citations?user=wq36gfgAAAAJ) | [GitHub](https://github.com/rajsh3kar)
