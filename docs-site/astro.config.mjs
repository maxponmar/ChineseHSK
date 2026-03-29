import { defineConfig } from 'astro/config';
import starlight from '@astrojs/starlight';

export default defineConfig({
  site: 'https://maxponmar.github.io',
  base: '/ChineseHSK',
  integrations: [
    starlight({
      title: 'Chinese HSK Flashcards',
      defaultLocale: 'es',
      locales: {
        es: { label: 'Español', lang: 'es' },
        en: { label: 'English', lang: 'en' },
      },
      customCss: ['./src/custom.css'],
      sidebar: [
        {
          label: 'Comenzar',
          translations: { en: 'Getting Started' },
          items: [
            { slug: 'index', label: 'Bienvenida', translations: { en: 'Welcome' } },
            { slug: 'instalar-anki', label: 'Instalar Anki', translations: { en: 'Install Anki' } },
            { slug: 'descargar-mazo', label: 'Descargar Mazo', translations: { en: 'Download Deck' } },
            { slug: 'importar-anki', label: 'Importar a Anki', translations: { en: 'Import to Anki' } },
          ],
        },
        {
          label: 'Cómo Estudiar',
          translations: { en: 'How to Study' },
          items: [
            { slug: 'guia-estudio', label: 'Guía de Estudio', translations: { en: 'Study Guide' } },
            { slug: 'consejos', label: 'Consejos', translations: { en: 'Tips & Tricks' } },
          ],
        },
        {
          label: 'Niveles HSK',
          translations: { en: 'HSK Levels' },
          items: [
            { slug: 'hsk1', label: 'HSK 1' },
            { slug: 'hsk2', label: 'HSK 2' },
            { slug: 'hsk3', label: 'HSK 3' },
            { slug: 'hsk4', label: 'HSK 4' },
            { slug: 'hsk5', label: 'HSK 5' },
          ],
        },
        {
          label: 'Ayuda',
          translations: { en: 'Help' },
          items: [
            { slug: 'faq', label: 'Preguntas Frecuentes', translations: { en: 'FAQ' } },
          ],
        },
      ],
    }),
  ],
});
