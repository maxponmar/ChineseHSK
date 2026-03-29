# GitHub Pages Site — Design Spec

## Goal

Build a bilingual (Spanish/English) documentation site using Astro + Starlight, deployed to GitHub Pages, that guides non-technical users (language teachers) through downloading and using the HSK Anki flashcard decks.

## Audience

HSK1 classmates who are teachers — not engineers. The site must assume zero technical knowledge. Every step needs screenshots, clear language, and no jargon.

## Tech Stack

- **Astro** with **Starlight** theme (docs framework with built-in i18n, search, responsive design)
- **GitHub Pages** for hosting
- **GitHub Actions** for automated deployment on push to main
- Site directory: `docs-site/` at the repo root (to avoid conflict with existing `docs/` folder)

## Visual Style

Friendly & warm + clean & minimal:
- Starlight's default theme with minor CSS customizations
- Soft accent colors (Chinese red `#D4380D` as primary accent)
- Rounded corners, generous spacing
- Large step numbers for guides
- Light mode as default

## i18n

- **Spanish** as default locale (primary audience)
- **English** as secondary locale
- Starlight's built-in language switcher in the header
- Content mirrored in `es/` and `en/` directories
- All UI chrome auto-translated by Starlight

## Site Structure

### Navigation Sidebar

```
Getting Started / Comenzar
  Welcome / Bienvenida
  Install Anki / Instalar Anki
  Download Deck / Descargar Mazo
  Import to Anki / Importar a Anki

How to Study / Cómo Estudiar
  Study Guide / Guía de Estudio
  Tips & Tricks / Consejos

HSK Levels / Niveles HSK
  HSK 1 (Available / Disponible)
  HSK 2 (Coming soon / Próximamente)
  HSK 3 (Coming soon / Próximamente)
  HSK 4 (Coming soon / Próximamente)
  HSK 5 (Coming soon / Próximamente)

Help / Ayuda
  FAQ / Preguntas Frecuentes
```

### Page Content

#### 1. Welcome / Bienvenida
- What is this project and who it's for
- What you'll learn (HSK vocabulary, daily phrases, work phrases, grammar)
- What the 4 card types are (Recognition, Production, Listening, Cloze)
- Prominent "Get Started" call-to-action button

#### 2. Install Anki / Instalar Anki
- Step-by-step guide with screenshots
- Download links for each platform:
  - Desktop: macOS, Windows, Linux (from apps.ankiweb.net)
  - Mobile: iOS (AnkiMobile), Android (AnkiDroid — free)
- Note about AnkiMobile being paid on iOS, AnkiDroid being free on Android
- Screenshots of the Anki interface after first launch

#### 3. Download Deck / Descargar Mazo
- Direct download link to the latest GitHub Release `.apkg` file
- The link points to the GitHub Releases page: `https://github.com/maxponmar/ChineseHSK/releases`
- Explanation that the file is safe to download
- Note about file size (~16MB for HSK1)

#### 4. Import to Anki / Importar a Anki
- Step-by-step with screenshots:
  1. Open Anki
  2. File > Import (or double-click the .apkg file)
  3. Select the downloaded file
  4. Click Import
- What to expect after import (deck appears, card count)
- "What if I already have a previous version?" — Anki merges updates and keeps progress

#### 5. Study Guide / Guía de Estudio
- Recommended daily study schedule (15-20 minutes)
- How Anki's spaced repetition works (simple explanation)
- How the 4 card types work:
  - Recognition: see Chinese, recall meaning
  - Production: see meaning, recall Chinese
  - Listening: hear audio, identify word
  - Cloze: fill in the blank in a sentence
- How to use tags to filter (by lesson, category, card type)
- How to rate cards (Again, Hard, Good, Easy)

#### 6. Tips & Tricks / Consejos
- Study in the morning when your brain is fresh
- Don't skip days — consistency matters more than duration
- Use the listening cards with headphones
- Review grammar cards separately from vocabulary
- Sync across devices with AnkiWeb (free account)

#### 7. HSK Level Pages (one per level)
- Level overview: what it covers, number of words, description
- Download button for that level's deck
- **Interactive vocabulary table** with:
  - Search box (filters by hanzi, pinyin, Spanish, or English)
  - Category filter tabs: All, Vocabulary, Daily Phrases, Work Phrases, Grammar
  - Columns: Hanzi, Pinyin, Spanish, English, Category
  - Auto-generated from the JSON data files at build time
- For levels not yet available: "Coming soon" placeholder with description of what will be included

#### 8. FAQ / Preguntas Frecuentes
- Is Anki free? (Desktop yes, Android yes, iOS paid)
- Can I use it on my phone? (Yes, with sync)
- How do I update to a new version of the deck? (Re-import, progress preserved)
- What if I lose my progress? (Use AnkiWeb sync as backup)
- How many cards should I study per day? (20 new cards + reviews)
- Can I customize the cards? (Yes, but not recommended for beginners)
- The audio isn't playing — what do I do? (Check volume, check media sync)

## Vocabulary Preview Component

An Astro component (`VocabularyTable.astro`) that:
- Receives vocabulary data as a prop (generated at build time from JSON files)
- Renders a searchable, filterable table
- Client-side JavaScript for search/filter (no server needed)
- Responsive: stacks on mobile, scrollable on small screens
- Shows hanzi in large font for readability

### Build-time data generation

A script (`docs-site/scripts/generate-vocab-data.ts`) runs at build time:
1. Reads `HSK1/data/*.json` files
2. Transforms entries into a simplified format for the frontend
3. Outputs as a TypeScript module imported by the component

## Deployment

### GitHub Actions Workflow (`deploy-site.yml`)
- Triggers on push to `main` when files in `docs-site/` change
- Installs Node.js, builds the Astro site
- Deploys to GitHub Pages using `actions/deploy-pages`
- Site URL: `https://maxponmar.github.io/ChineseHSK/`

### GitHub Pages Configuration
- Source: GitHub Actions (not branch-based)
- Custom domain: none (use default github.io URL)
- Base path: `/ChineseHSK/` (repo name)

## Project Structure

```
docs-site/
  astro.config.mjs           # Astro + Starlight config with i18n
  package.json                # Dependencies
  tsconfig.json
  scripts/
    generate-vocab-data.ts    # Reads HSK data JSONs, outputs for frontend
  src/
    content/docs/
      es/                     # Spanish content (default)
        index.mdx             # Welcome
        instalar-anki.mdx     # Install Anki
        descargar-mazo.mdx    # Download Deck
        importar-anki.mdx     # Import to Anki
        guia-estudio.mdx      # Study Guide
        consejos.mdx          # Tips & Tricks
        hsk1.mdx              # HSK1 level page
        hsk2.mdx              # HSK2 placeholder
        hsk3.mdx              # HSK3 placeholder
        hsk4.mdx              # HSK4 placeholder
        hsk5.mdx              # HSK5 placeholder
        faq.mdx               # FAQ
      en/                     # English content
        index.mdx             # Welcome
        install-anki.mdx
        download-deck.mdx
        import-anki.mdx
        study-guide.mdx
        tips.mdx
        hsk1.mdx
        hsk2.mdx
        hsk3.mdx
        hsk4.mdx
        hsk5.mdx
        faq.mdx
    components/
      VocabularyTable.astro   # Interactive vocabulary search/filter table
    data/
      hsk1-vocab.json         # Generated at build time from HSK1/data/
  public/
    images/                   # Screenshots for guides (manually captured Anki UI screenshots, added later)
```
