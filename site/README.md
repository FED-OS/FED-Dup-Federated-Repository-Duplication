# Fed-Dup Landing Page

A modern, animated, eye-catching landing page for the **Fed-Dup** project, designed for deployment to **GitHub Pages**.

## ✨ Features

- **Glassmorphism design** with animated gradient blobs and a dark theme
- **Animated hero** with floating shield, gradient title, and live shields
- **Animated stats counters** that count up on scroll
- **Live terminal demo** with a typing animation that runs when scrolled into view
- **Architecture diagram** showing the Source → Engine → Destination pipeline
- **Feature grid** with 12 glassmorphism cards and hover effects
- **Comparison table** with color-coded yes / no / partial indicators
- **Syntax-highlighted code blocks** in macOS-style windows
- **Scroll reveal animations** powered by IntersectionObserver
- **Fully responsive** — mobile burger menu, fluid grids, adaptive breakpoints
- **Zero build step** — pure HTML, CSS, and vanilla JS

## 📁 Files

| File | Purpose |
|------|---------|
| `index.html` | The main landing page |
| `styles.css` | All styles (animations, layout, responsive) |
| `404.html` | Custom GitHub Pages 404 page |
| `social-image.png` | Open Graph / Twitter card preview image |
| `.nojekyll` | Tells GitHub Pages to skip Jekyll processing |

## 🚀 Deploy to GitHub Pages

### Option A — Project Pages (`/repo-name/`)

1. Push the contents of this `site/` directory to the `gh-pages` branch
   (or to a `/docs` folder on your default branch):

   ```bash
   git checkout -b gh-pages
   cp -r site/* .
   git add .
   git commit -m "Deploy landing page"
   git push origin gh-pages
   ```

2. In your repository: **Settings → Pages → Source → Deploy from a branch**
   and select `gh-pages` / `root`.

3. Your site goes live at `https://<username>.github.io/fed-dup/`.

### Option B — User/Org Pages (`/`)

1. Create a repository named `<username>.github.io`.
2. Copy the contents of `site/` into the root of that repo.
3. Push to the `main` branch.
4. Your site goes live at `https://<username>.github.io/`.

### Option C — GitHub Actions

Add a workflow that deploys the `site/` directory:

```yaml
name: Deploy Site
on:
  push:
    branches: [main]
    paths: ['site/**']
permissions:
  contents: read
  pages: write
  id-token: write
jobs:
  deploy:
    runs-on: ubuntu-latest
    environment: github-pages
    steps:
      - uses: actions/checkout@v4
      - uses: actions/configure-pages@v4
      - uses: actions/upload-pages-artifact@v3
        with:
          path: site
      - uses: actions/deploy-pages@v4
```

## 🧪 Preview locally

```bash
cd site
python3 -m http.server 8080
# Open http://localhost:8080
```

## 🎨 Customization

- **Colors**: Edit the CSS custom properties in `:root` at the top of `styles.css`
- **Content**: Edit `index.html` directly — all copy is inline
- **Stats**: Update the `data-target` values on `.stat-number` elements
- **Links**: Update footer and CTA links to point to your real docs/repo

## 📄 License

Same as the Fed-Dup project — MIT.
