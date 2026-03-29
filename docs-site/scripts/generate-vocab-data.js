#!/usr/bin/env node

const fs = require('fs');
const path = require('path');

const REPO_ROOT = path.join(__dirname, '..', '..');
const DATA_DIR = path.join(REPO_ROOT, 'HSK1', 'data');
const OUTPUT_DIR = path.join(__dirname, '..', 'src', 'data');

const CATEGORY_MAP = {
  'vocabulary.json': 'Vocabulario',
  'daily_phrases.json': 'Frases Diarias',
  'work_phrases.json': 'Frases de Trabajo',
  'grammar_structures.json': 'Gramática',
};

function main() {
  fs.mkdirSync(OUTPUT_DIR, { recursive: true });

  const allEntries = [];

  for (const [filename, category] of Object.entries(CATEGORY_MAP)) {
    const filePath = path.join(DATA_DIR, filename);
    if (!fs.existsSync(filePath)) {
      console.warn(`Skipping missing file: ${filePath}`);
      continue;
    }

    const data = JSON.parse(fs.readFileSync(filePath, 'utf-8'));
    for (const entry of data) {
      allEntries.push({
        hanzi: entry.hanzi,
        pinyin: entry.pinyin,
        spanish: entry.spanish,
        english: entry.english,
        category: category,
      });
    }
  }

  const outputPath = path.join(OUTPUT_DIR, 'hsk1-vocab.json');
  fs.writeFileSync(outputPath, JSON.stringify(allEntries, null, 2), 'utf-8');
  console.log(`Generated ${allEntries.length} entries to ${outputPath}`);
}

main();
