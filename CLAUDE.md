# CLAUDE.md

This file provides guidance to Claude Code (claude.ai/code) when working with code in this repository.

## Overview

This repository is a Chinese language learning system that generates Anki flashcard packages (.apkg) from structured JSON data, with AI-generated audio (ElevenLabs) and open-source icons (OpenMoji).

## Structure

- `HSK1/data/` — JSON vocabulary and phrase files (vocabulary, daily life, work)
- `HSK1/scripts/` — Python pipeline scripts (config, data loader, icon downloader, audio generator, deck builder)
- `HSK1/templates/` — Anki card HTML templates and CSS
- `HSK1/media/` — Generated audio and icon files (git-ignored)
- `HSK1/output/` — Generated .apkg files (git-ignored)
- `HSK1/resources/` — Source PDF course materials (Spanish)
- `tests/` — pytest test suite

## Setup

```bash
cd HSK1 && python3 -m venv .venv && source .venv/bin/activate && pip install -r requirements.txt
cp .env.example .env  # Then add your ElevenLabs API key
```

## Pipeline

Run in order:
```bash
python -m HSK1.scripts.download_icons    # Fetch icons
python -m HSK1.scripts.generate_audio    # Generate audio (requires API key)
python -m HSK1.scripts.build_deck        # Build .apkg
```

## Tests

```bash
python -m pytest tests/ -v
```

## Data Schema

Each entry in the JSON data files follows this structure: id, hanzi, pinyin, spanish, english, example_zh, example_pinyin, example_es, example_en, lesson, tags, icon. See `docs/superpowers/specs/2026-03-27-anki-flashcard-system-design.md` for full spec.
