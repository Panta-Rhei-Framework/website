# Panta Rhei Books

[![Deploy to GitHub Pages](https://github.com/Panta-Rhei-Framework/website/actions/workflows/pages.yml/badge.svg)](https://github.com/Panta-Rhei-Framework/website/actions/workflows/pages.yml)

Source code for the official website of the **Panta Rhei** seven-volume research book series.

## The Series

| Vol. | Title | Theme |
|------|-------|-------|
| I | Categorical Foundations | Category theory & mathematical logic |
| II | Categorical Holomorphy | Complex analysis & holomorphic structures |
| III | Categorical Spectrum | Spectral theory & operator algebras |
| IV | Categorical Microcosm | Quantum structure & microscale physics |
| V | Categorical Macrocosm | Cosmology & large-scale structure |
| VI | Categorical Life | Mathematics of living systems |
| VII | Categorical Metaphysics | Foundations of reality & synthesis |

A unified mathematical framework following one continuous arc from categorical foundations through structure, physics, cosmology, life, and metaphysics.

## Development

```bash
bundle install
bundle exec jekyll serve --livereload
```

Open [http://127.0.0.1:4000](http://127.0.0.1:4000).

## Architecture

- **Jekyll 4.4** static site generator
- **GitHub Pages** deployment via GitHub Actions
- Pure HTML / CSS / vanilla JS — no frameworks, no build tools
- Responsive dark design system ("Structural Cosmos")
- Data-driven content from YAML files (`_data/`)

## Project Structure

```
_books/          7 book collection pages (one per volume)
_data/           Site config, navigation, resources, retailers, press assets
_includes/       Reusable template partials (header, footer, book card)
_layouts/        Page templates (default, book, post)
_posts/          Updates and announcements
assets/          CSS design system, fonts, images, JS
```

## Authors

**Dr. Thorsten Fuchs** & **Anna-Sophie Fuchs**

## License

Content and design © 2025–2026 Thorsten Fuchs & Anna-Sophie Fuchs. All rights reserved.
