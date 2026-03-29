# GitHub Pages Documentation Site — Implementation Plan

> **For agentic workers:** REQUIRED SUB-SKILL: Use superpowers:subagent-driven-development (recommended) or superpowers:executing-plans to implement this plan task-by-task. Steps use checkbox (`- [ ]`) syntax for tracking.

**Goal:** Build a bilingual (ES/EN) Astro + Starlight documentation site deployed to GitHub Pages that guides non-technical users through downloading and using the HSK Anki flashcard decks.

**Architecture:** Starlight docs framework with i18n (Spanish default, English secondary). Content in Markdown, interactive vocabulary table as an Astro component reading JSON data at build time. Deployed via GitHub Actions to GitHub Pages.

**Tech Stack:** Astro 5, Starlight, TypeScript, GitHub Actions, GitHub Pages

---

## File Map

| File | Purpose |
|------|---------|
| `docs-site/package.json` | Dependencies |
| `docs-site/astro.config.mjs` | Astro + Starlight config, i18n, sidebar |
| `docs-site/tsconfig.json` | TypeScript config |
| `docs-site/src/content/docs/es/*.mdx` | 12 Spanish content pages |
| `docs-site/src/content/docs/en/*.mdx` | 12 English content pages |
| `docs-site/src/components/VocabularyTable.astro` | Interactive vocabulary table |
| `docs-site/scripts/generate-vocab-data.ts` | Build-time JSON → vocab data |
| `docs-site/src/data/hsk1-vocab.json` | Generated vocab data for frontend |
| `docs-site/src/custom.css` | Custom CSS overrides |
| `.github/workflows/deploy-site.yml` | GitHub Actions deployment |

---

### Task 1: Scaffold Astro + Starlight Project

**Files:**
- Create: `docs-site/package.json`
- Create: `docs-site/astro.config.mjs`
- Create: `docs-site/tsconfig.json`
- Create: `docs-site/src/custom.css`

- [ ] **Step 1: Create docs-site directory and initialize project**

Run:
```bash
cd /Users/maximiliano/Repositories/Personal/Chineese && mkdir -p docs-site && cd docs-site && npm init -y
```

- [ ] **Step 2: Install dependencies**

Run:
```bash
cd /Users/maximiliano/Repositories/Personal/Chineese/docs-site && npm install astro @astrojs/starlight
```

- [ ] **Step 3: Create astro.config.mjs**

```javascript
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
            { slug: 'es/index', label: 'Bienvenida', translations: { en: 'Welcome' } },
            { slug: 'es/instalar-anki', label: 'Instalar Anki', translations: { en: 'Install Anki' } },
            { slug: 'es/descargar-mazo', label: 'Descargar Mazo', translations: { en: 'Download Deck' } },
            { slug: 'es/importar-anki', label: 'Importar a Anki', translations: { en: 'Import to Anki' } },
          ],
        },
        {
          label: 'Cómo Estudiar',
          translations: { en: 'How to Study' },
          items: [
            { slug: 'es/guia-estudio', label: 'Guía de Estudio', translations: { en: 'Study Guide' } },
            { slug: 'es/consejos', label: 'Consejos', translations: { en: 'Tips & Tricks' } },
          ],
        },
        {
          label: 'Niveles HSK',
          translations: { en: 'HSK Levels' },
          items: [
            { slug: 'es/hsk1', label: 'HSK 1', translations: { en: 'HSK 1' } },
            { slug: 'es/hsk2', label: 'HSK 2', translations: { en: 'HSK 2' } },
            { slug: 'es/hsk3', label: 'HSK 3', translations: { en: 'HSK 3' } },
            { slug: 'es/hsk4', label: 'HSK 4', translations: { en: 'HSK 4' } },
            { slug: 'es/hsk5', label: 'HSK 5', translations: { en: 'HSK 5' } },
          ],
        },
        {
          label: 'Ayuda',
          translations: { en: 'Help' },
          items: [
            { slug: 'es/faq', label: 'Preguntas Frecuentes', translations: { en: 'FAQ' } },
          ],
        },
      ],
    }),
  ],
});
```

Write this to `docs-site/astro.config.mjs`.

NOTE: The sidebar `slug` values may need adjustment based on how Starlight resolves i18n slugs. When Starlight uses `defaultLocale: 'es'`, the Spanish pages become the root. The implementer should check the Starlight i18n docs and test locally. The slug pattern might need to drop the `es/` prefix for the default locale, or use `autogenerate` instead. Test with `npm run dev` and adjust.

- [ ] **Step 4: Create tsconfig.json**

```json
{
  "extends": "astro/tsconfigs/strict"
}
```

Write this to `docs-site/tsconfig.json`.

- [ ] **Step 5: Create custom.css**

```css
:root {
  --sl-color-accent-low: #fde8e0;
  --sl-color-accent: #D4380D;
  --sl-color-accent-high: #7a1f06;
  --sl-font-system: 'Noto Sans SC', -apple-system, BlinkMacSystemFont, 'Segoe UI', sans-serif;
}

/* Friendly warm styling */
.sl-markdown-content h2 {
  border-bottom: 2px solid var(--sl-color-accent-low);
  padding-bottom: 0.5rem;
}

/* Step numbers for guides */
.sl-markdown-content ol > li {
  margin-bottom: 1.5rem;
}

.sl-markdown-content ol > li::marker {
  font-size: 1.2em;
  font-weight: bold;
  color: var(--sl-color-accent);
}

/* Large hanzi in tables */
.vocab-table td:first-child {
  font-size: 1.4em;
  font-weight: bold;
}
```

Write this to `docs-site/src/custom.css`.

- [ ] **Step 6: Add scripts to package.json**

Update `docs-site/package.json` to include these scripts:
```json
{
  "scripts": {
    "dev": "astro dev",
    "build": "node scripts/generate-vocab-data.ts && astro build",
    "preview": "astro preview"
  }
}
```

- [ ] **Step 7: Create initial content directory structure**

Run:
```bash
mkdir -p docs-site/src/content/docs/es docs-site/src/content/docs/en docs-site/src/components docs-site/src/data docs-site/scripts docs-site/public/images
```

- [ ] **Step 8: Create a minimal index page to test**

Create `docs-site/src/content/docs/es/index.mdx`:
```mdx
---
title: Bienvenida
description: Aprende chino mandarín con tarjetas Anki
---

# Bienvenida

Este sitio te guiará paso a paso para aprender chino mandarín usando tarjetas de estudio Anki.
```

Create `docs-site/src/content/docs/en/index.mdx`:
```mdx
---
title: Welcome
description: Learn Mandarin Chinese with Anki flashcards
---

# Welcome

This site will guide you step by step to learn Mandarin Chinese using Anki study flashcards.
```

- [ ] **Step 9: Test local dev server**

Run:
```bash
cd /Users/maximiliano/Repositories/Personal/Chineese/docs-site && npm run dev
```

Expected: Site loads at `http://localhost:4321/ChineseHSK/` with the welcome page, language switcher, and sidebar.

If the sidebar slugs don't resolve correctly, adjust `astro.config.mjs` based on what Starlight expects. Common fix: for the default locale, slugs may not need the `es/` prefix.

- [ ] **Step 10: Commit**

```bash
cd /Users/maximiliano/Repositories/Personal/Chineese
echo "node_modules/" >> docs-site/.gitignore
git add docs-site/
git commit -m "feat: scaffold Astro + Starlight docs site with i18n"
```

---

### Task 2: Spanish Content — Getting Started Pages

**Files:**
- Create: `docs-site/src/content/docs/es/index.mdx`
- Create: `docs-site/src/content/docs/es/instalar-anki.mdx`
- Create: `docs-site/src/content/docs/es/descargar-mazo.mdx`
- Create: `docs-site/src/content/docs/es/importar-anki.mdx`

- [ ] **Step 1: Write Welcome page (es/index.mdx)**

```mdx
---
title: Bienvenida
description: Aprende chino mandarín con tarjetas Anki
template: splash
hero:
  title: Aprende Chino Mandarín
  tagline: Tarjetas de estudio Anki con audio nativo, vocabulario HSK y frases para el día a día y el trabajo.
  actions:
    - text: Comenzar
      link: /ChineseHSK/es/instalar-anki/
      icon: right-arrow
    - text: Descargar Mazo HSK1
      link: https://github.com/maxponmar/ChineseHSK/releases
      icon: external
      variant: minimal
---

import { Card, CardGrid } from '@astrojs/starlight/components';

## ¿Qué incluye?

<CardGrid>
  <Card title="Vocabulario HSK" icon="open-book">
    Todas las palabras del nivel HSK1, con pinyin, traducción al español e inglés.
  </Card>
  <Card title="Frases del día a día" icon="heart">
    Saludos, restaurantes, compras, transporte y situaciones sociales.
  </Card>
  <Card title="Frases para el trabajo" icon="laptop">
    Reuniones, tecnología, correos electrónicos y llamadas de video.
  </Card>
  <Card title="Gramática" icon="puzzle">
    Estructuras gramaticales del libro de texto HSK1.
  </Card>
</CardGrid>

## 4 tipos de tarjetas

Cada palabra genera **4 tarjetas diferentes** para un aprendizaje completo:

1. **Reconocimiento** — Ves los caracteres chinos y recuerdas el significado
2. **Producción** — Ves el significado y recuerdas los caracteres chinos
3. **Escucha** — Escuchas el audio y identifies la palabra
4. **Completar oraciones** — Completas el espacio en blanco en una oración

## ¿Para quién es esto?

Este recurso es para cualquier persona que esté aprendiendo chino mandarín, especialmente estudiantes de HSK. No necesitas conocimientos técnicos — esta guía te explica todo paso a paso.
```

- [ ] **Step 2: Write Install Anki page (es/instalar-anki.mdx)**

```mdx
---
title: Instalar Anki
description: Cómo descargar e instalar Anki en tu computadora o teléfono
---

Anki es una aplicación gratuita para estudiar con tarjetas de memoria. Usa un sistema de **repetición espaciada** que te muestra las tarjetas justo cuando estás a punto de olvidarlas.

## En computadora (Windows, Mac o Linux)

1. Abre tu navegador y ve a **[apps.ankiweb.net](https://apps.ankiweb.net)**
2. Haz clic en el botón **Download** (Descargar)
3. Selecciona la versión para tu sistema operativo (Windows, Mac o Linux)
4. Abre el archivo descargado e instala Anki como cualquier otra aplicación
5. Abre Anki — verás una pantalla vacía. ¡Eso es normal! Pronto agregaremos las tarjetas

:::note[Anki es gratuito en computadora]
La versión de escritorio de Anki es completamente gratuita para Windows, Mac y Linux.
:::

## En teléfono Android

1. Abre la **Play Store** en tu teléfono
2. Busca **"AnkiDroid"**
3. Instala la aplicación (es gratuita)
4. Ábrela — verás una pantalla vacía

:::note[AnkiDroid es gratuito]
AnkiDroid es la versión oficial para Android y es completamente gratis.
:::

## En iPhone o iPad

1. Abre la **App Store**
2. Busca **"AnkiMobile Flashcards"**
3. La aplicación cuesta aproximadamente $24.99 USD
4. Instálala y ábrela

:::caution[AnkiMobile es de pago en iOS]
La versión para iPhone/iPad cuesta dinero. Si prefieres no pagar, puedes usar Anki gratis en tu computadora y estudiar con **[AnkiWeb](https://ankiweb.net)** en el navegador de tu teléfono (es gratis).
:::

## Siguiente paso

¡Anki está instalado! Ahora vamos a [descargar el mazo de tarjetas](/ChineseHSK/es/descargar-mazo/).
```

- [ ] **Step 3: Write Download Deck page (es/descargar-mazo.mdx)**

```mdx
---
title: Descargar Mazo
description: Cómo descargar el mazo de tarjetas HSK para Anki
---

## Descargar el mazo HSK1

El mazo contiene **1,352 tarjetas** con audio en mandarín, iconos visuales y traducciones en español e inglés.

1. Haz clic en el siguiente enlace: **[Descargar HSK1 Anki Deck](https://github.com/maxponmar/ChineseHSK/releases/latest)**
2. En la página que se abre, busca la sección **"Assets"** (Archivos)
3. Haz clic en el archivo que termina en **`.apkg`** (por ejemplo, `HSK1_Complete.apkg`)
4. El archivo se descargará automáticamente a tu carpeta de descargas

:::tip[El archivo es seguro]
El archivo `.apkg` es un formato de Anki. Es completamente seguro y solo contiene tarjetas de estudio, audio e imágenes.
:::

## ¿Qué contiene el mazo?

| Categoría | Cantidad | Descripción |
|-----------|----------|-------------|
| Vocabulario HSK1 | 140 palabras | Todas las palabras del curso HSK1 |
| Frases del día a día | 70 frases | Saludos, comida, compras, vida social |
| Frases de trabajo | 80 frases | Reuniones, tecnología, correos, llamadas |
| Gramática | 48 estructuras | Patrones gramaticales del libro de texto |

## Siguiente paso

¡Ya tienes el archivo! Ahora vamos a [importarlo a Anki](/ChineseHSK/es/importar-anki/).
```

- [ ] **Step 4: Write Import to Anki page (es/importar-anki.mdx)**

```mdx
---
title: Importar a Anki
description: Cómo importar el mazo de tarjetas a Anki
---

## Importar el mazo

### Opción 1: Doble clic (la más fácil)

1. Busca el archivo **`HSK1_Complete.apkg`** en tu carpeta de descargas
2. Haz **doble clic** en el archivo
3. Anki se abrirá automáticamente y te preguntará si quieres importar
4. Haz clic en **"Importar"**
5. ¡Listo! El mazo "Chinese HSK1" aparecerá en tu lista de mazos

### Opción 2: Desde Anki

1. Abre **Anki**
2. Ve al menú **Archivo** → **Importar**
3. Busca y selecciona el archivo **`HSK1_Complete.apkg`**
4. Haz clic en **"Importar"**

:::tip[¿Ya tienes una versión anterior?]
Si ya habías importado este mazo antes, no te preocupes. Anki **actualizará** las tarjetas automáticamente y **conservará tu progreso** de estudio. No perderás nada.
:::

## ¿Qué verás después de importar?

Después de importar, verás un nuevo mazo llamado **"Chinese HSK1"** en la pantalla principal de Anki. El número al lado del mazo muestra cuántas tarjetas nuevas tienes para estudiar hoy.

## Siguiente paso

¡El mazo está listo! Ahora aprende [cómo estudiar](/ChineseHSK/es/guia-estudio/) de manera efectiva.
```

- [ ] **Step 5: Commit**

```bash
git add docs-site/src/content/docs/es/
git commit -m "feat: add Spanish Getting Started pages (welcome, install, download, import)"
```

---

### Task 3: Spanish Content — Study & Help Pages

**Files:**
- Create: `docs-site/src/content/docs/es/guia-estudio.mdx`
- Create: `docs-site/src/content/docs/es/consejos.mdx`
- Create: `docs-site/src/content/docs/es/faq.mdx`

- [ ] **Step 1: Write Study Guide page (es/guia-estudio.mdx)**

```mdx
---
title: Guía de Estudio
description: Cómo usar Anki para estudiar chino mandarín de manera efectiva
---

## Tu rutina diaria

Dedica **15-20 minutos al día** a estudiar con Anki. La consistencia es más importante que la cantidad.

### Cómo funciona Anki

Anki usa un sistema llamado **repetición espaciada**. La idea es simple:
- Las tarjetas que **recuerdas bien** se muestran con menos frecuencia
- Las tarjetas que **te cuestan más** se muestran más seguido
- Con el tiempo, todo pasa a tu memoria a largo plazo

### Los 4 tipos de tarjetas

Cada palabra tiene 4 tarjetas diferentes:

#### 1. Reconocimiento 👀
- **Frente:** Ves los caracteres chinos (汉字)
- **Reverso:** Pinyin + significado en español e inglés + oración de ejemplo + audio
- **Objetivo:** Aprender a reconocer caracteres chinos

#### 2. Producción 💭
- **Frente:** Ves el significado en español e inglés
- **Reverso:** Caracteres chinos + pinyin + audio
- **Objetivo:** Recordar cómo se escribe/dice una palabra

#### 3. Escucha 🔊
- **Frente:** Solo escuchas el audio (sin texto)
- **Reverso:** Caracteres + pinyin + significado
- **Objetivo:** Entrenar tu oído para conversaciones reales

#### 4. Completar oraciones ✏️
- **Frente:** Una oración con un espacio en blanco + traducción
- **Reverso:** La oración completa con la palabra resaltada + audio
- **Objetivo:** Aprender a usar palabras en contexto

### Cómo calificar las tarjetas

Cuando ves la respuesta, Anki te da 4 opciones:

| Botón | Cuándo usarlo |
|-------|---------------|
| **Otra vez** (rojo) | No recordaste la respuesta |
| **Difícil** | Recordaste pero con mucho esfuerzo |
| **Bien** | Recordaste correctamente |
| **Fácil** | Lo sabías inmediatamente |

:::tip[Consejo: Sé honesto]
Si no estás seguro, elige "Otra vez" o "Difícil". Es mejor repasar una tarjeta de más que olvidarla.
:::

### Usar etiquetas para filtrar

Las tarjetas tienen etiquetas (tags) que te permiten estudiar por categoría:

- `HSK1::Lesson3`, `HSK1::Lesson4`, etc. — Por lección
- `daily::greetings`, `daily::food`, etc. — Frases del día a día
- `work::meetings`, `work::tech`, etc. — Frases de trabajo
- `grammar::lesson3`, etc. — Gramática por lección

Para filtrar: en Anki, haz clic en **"Explorar"** (Browse) y usa las etiquetas en la barra lateral.
```

- [ ] **Step 2: Write Tips page (es/consejos.mdx)**

```mdx
---
title: Consejos
description: Consejos y trucos para aprender chino mandarín con Anki
---

## Consejos para aprovechar Anki al máximo

### 1. Estudia todos los días
La clave del éxito es la **consistencia**. Es mejor estudiar 10 minutos cada día que 1 hora una vez a la semana. Anki funciona mejor cuando lo usas diariamente.

### 2. Estudia en la mañana
Tu cerebro está más fresco en la mañana. Si es posible, haz tu sesión de Anki antes de empezar tu día.

### 3. Usa audífonos para las tarjetas de escucha
Las tarjetas de tipo "Escucha" son muy importantes para entrenar tu oído. Usa audífonos para escuchar mejor la pronunciación.

### 4. No agregues demasiadas tarjetas nuevas
Anki te permite configurar cuántas tarjetas nuevas ver por día. Comienza con **10-15 tarjetas nuevas por día** y aumenta gradualmente.

### 5. Estudia gramática por separado
Las tarjetas de gramática requieren más concentración. Puedes usar las etiquetas para estudiar solo gramática en sesiones separadas.

### 6. Sincroniza entre dispositivos
Con una cuenta gratuita en **[AnkiWeb](https://ankiweb.net)**, puedes sincronizar tu progreso entre tu computadora y tu teléfono:
1. Crea una cuenta en ankiweb.net
2. En Anki, haz clic en el botón **"Sincronizar"** (Sync)
3. Inicia sesión con tu cuenta
4. Repite en tu otro dispositivo

### 7. Repasa las tarjetas pendientes primero
Cuando abres Anki, primero repasa las tarjetas que ya has visto antes (repasos). Después estudia las tarjetas nuevas.

### 8. Practica con tus compañeros
Las tarjetas son solo una parte del aprendizaje. Practica hablando con tus compañeros de clase usando las frases que has aprendido.
```

- [ ] **Step 3: Write FAQ page (es/faq.mdx)**

```mdx
---
title: Preguntas Frecuentes
description: Respuestas a las preguntas más comunes sobre Anki y los mazos HSK
---

## Preguntas frecuentes

### ¿Anki es gratuito?

**En computadora:** Sí, Anki es completamente gratuito para Windows, Mac y Linux. Descárgalo en [apps.ankiweb.net](https://apps.ankiweb.net).

**En Android:** Sí, la aplicación se llama **AnkiDroid** y es gratuita en la Play Store.

**En iPhone/iPad:** No, la aplicación **AnkiMobile** cuesta aproximadamente $24.99 USD. Como alternativa gratuita, puedes usar [ankiweb.net](https://ankiweb.net) en el navegador de tu teléfono.

### ¿Puedo usarlo en mi teléfono?

Sí. Instala AnkiDroid (Android, gratis) o AnkiMobile (iOS, de pago). Crea una cuenta en [AnkiWeb](https://ankiweb.net) para sincronizar tu progreso entre dispositivos.

### ¿Cómo actualizo a una nueva versión del mazo?

Simplemente descarga el nuevo archivo `.apkg` e impórtalo a Anki. Anki **actualizará** las tarjetas automáticamente y **conservará todo tu progreso**. No perderás tus repasos ni estadísticas.

### ¿Qué pasa si pierdo mi progreso?

Para evitar esto, usa **AnkiWeb** para sincronizar tu progreso. Es gratuito y funciona como respaldo automático. También puedes exportar tu colección desde Anki como respaldo manual (Archivo → Exportar).

### ¿Cuántas tarjetas debo estudiar por día?

Te recomendamos empezar con **10-15 tarjetas nuevas por día**, más los repasos que Anki te asigne automáticamente. A medida que te sientas cómodo, puedes aumentar a 20-25.

### ¿Puedo personalizar las tarjetas?

Sí, pero no lo recomendamos si estás empezando. Las tarjetas ya están diseñadas para un aprendizaje óptimo. Si quieres hacer cambios, puedes editar tarjetas individuales desde el menú "Explorar" (Browse) en Anki.

### El audio no se reproduce, ¿qué hago?

1. Verifica que el volumen de tu dispositivo no esté en silencio
2. En Anki, ve a **Herramientas → Preferencias** y verifica que la reproducción de audio esté activada
3. Si usas AnkiDroid, verifica que hayas sincronizado completamente (el audio se descarga con la sincronización)

### ¿Necesito internet para estudiar?

No. Una vez que importas el mazo y sincronizas, todo el contenido (tarjetas, audio, imágenes) se guarda en tu dispositivo. Puedes estudiar sin conexión a internet.
```

- [ ] **Step 4: Commit**

```bash
git add docs-site/src/content/docs/es/
git commit -m "feat: add Spanish study guide, tips, and FAQ pages"
```

---

### Task 4: Spanish Content — HSK Level Pages

**Files:**
- Create: `docs-site/src/content/docs/es/hsk1.mdx`
- Create: `docs-site/src/content/docs/es/hsk2.mdx`
- Create: `docs-site/src/content/docs/es/hsk3.mdx`
- Create: `docs-site/src/content/docs/es/hsk4.mdx`
- Create: `docs-site/src/content/docs/es/hsk5.mdx`

- [ ] **Step 1: Write HSK1 page (es/hsk1.mdx)**

```mdx
---
title: HSK 1
description: Mazo Anki para el nivel HSK 1 de chino mandarín
---

import VocabularyTable from '../../components/VocabularyTable.astro';
import vocabData from '../../data/hsk1-vocab.json';

## HSK 1 — Nivel Básico

El HSK 1 es el primer nivel del examen de competencia en chino mandarín. Cubre el vocabulario y las estructuras gramaticales más básicas para la comunicación diaria.

**[⬇️ Descargar Mazo HSK1](https://github.com/maxponmar/ChineseHSK/releases/latest)**

### Contenido del mazo

| Categoría | Cantidad | Descripción |
|-----------|----------|-------------|
| 📗 Vocabulario | 140 palabras | Lecciones 3 a 15 del curso HSK1 |
| 🗣️ Frases diarias | 70 frases | Saludos, comida, compras, vida social |
| 💼 Frases de trabajo | 80 frases | Reuniones, tecnología, correos, llamadas |
| 📐 Gramática | 48 estructuras | Patrones del libro de texto HSK1 |
| **Total** | **338 entradas** | **1,352 tarjetas** (4 tipos por entrada) |

### Vista previa del vocabulario

Usa la búsqueda para encontrar palabras por caracteres chinos, pinyin, español o inglés.

<VocabularyTable data={vocabData} />
```

- [ ] **Step 2: Write HSK2-5 placeholder pages**

Create `docs-site/src/content/docs/es/hsk2.mdx`:
```mdx
---
title: HSK 2
description: Mazo Anki para el nivel HSK 2 — Próximamente
---

## HSK 2 — Nivel Elemental

:::note[Próximamente]
El mazo HSK 2 está en desarrollo. Incluirá aproximadamente 300 palabras nuevas para conversaciones elementales.
:::

### ¿Qué incluirá?

- ~300 palabras de vocabulario HSK2
- Frases para la vida diaria (nivel intermedio)
- Frases de trabajo (nivel intermedio)
- Estructuras gramaticales del libro de texto HSK2
- Audio con pronunciación nativa en mandarín

Mientras tanto, puedes descargar el [mazo HSK1](/ChineseHSK/es/hsk1/) y empezar a estudiar.
```

Create `docs-site/src/content/docs/es/hsk3.mdx`:
```mdx
---
title: HSK 3
description: Mazo Anki para el nivel HSK 3 — Próximamente
---

## HSK 3 — Nivel Intermedio

:::note[Próximamente]
El mazo HSK 3 está en desarrollo. Incluirá aproximadamente 600 palabras para comunicación diaria intermedia.
:::

### ¿Qué incluirá?

- ~600 palabras de vocabulario HSK3
- Frases de comunicación diaria intermedia
- Frases profesionales avanzadas
- Estructuras gramaticales del libro de texto HSK3
- Audio con pronunciación nativa en mandarín

Mientras tanto, puedes empezar con el [mazo HSK1](/ChineseHSK/es/hsk1/).
```

Create `docs-site/src/content/docs/es/hsk4.mdx`:
```mdx
---
title: HSK 4
description: Mazo Anki para el nivel HSK 4 — Próximamente
---

## HSK 4 — Nivel Avanzado

:::note[Próximamente]
El mazo HSK 4 está en desarrollo. Incluirá aproximadamente 1,200 palabras para temas profesionales y cotidianos avanzados.
:::

### ¿Qué incluirá?

- ~1,200 palabras de vocabulario HSK4
- Temas profesionales y cotidianos avanzados
- Estructuras gramaticales complejas
- Audio con pronunciación nativa en mandarín

Mientras tanto, puedes empezar con el [mazo HSK1](/ChineseHSK/es/hsk1/).
```

Create `docs-site/src/content/docs/es/hsk5.mdx`:
```mdx
---
title: HSK 5
description: Mazo Anki para el nivel HSK 5 — Próximamente
---

## HSK 5 — Nivel Fluido

:::note[Próximamente]
El mazo HSK 5 está en desarrollo. Incluirá aproximadamente 2,500 palabras para lectura fluida de periódicos y medios.
:::

### ¿Qué incluirá?

- ~2,500 palabras de vocabulario HSK5
- Lectura de periódicos, noticias y medios
- Expresiones formales y académicas
- Estructuras gramaticales avanzadas
- Audio con pronunciación nativa en mandarín

Mientras tanto, puedes empezar con el [mazo HSK1](/ChineseHSK/es/hsk1/).
```

- [ ] **Step 3: Commit**

```bash
git add docs-site/src/content/docs/es/
git commit -m "feat: add Spanish HSK level pages (HSK1 with vocab table, HSK2-5 placeholders)"
```

---

### Task 5: English Content — All Pages

**Files:**
- Create: `docs-site/src/content/docs/en/index.mdx`
- Create: `docs-site/src/content/docs/en/install-anki.mdx`
- Create: `docs-site/src/content/docs/en/download-deck.mdx`
- Create: `docs-site/src/content/docs/en/import-anki.mdx`
- Create: `docs-site/src/content/docs/en/study-guide.mdx`
- Create: `docs-site/src/content/docs/en/tips.mdx`
- Create: `docs-site/src/content/docs/en/hsk1.mdx`
- Create: `docs-site/src/content/docs/en/hsk2.mdx`
- Create: `docs-site/src/content/docs/en/hsk3.mdx`
- Create: `docs-site/src/content/docs/en/hsk4.mdx`
- Create: `docs-site/src/content/docs/en/hsk5.mdx`
- Create: `docs-site/src/content/docs/en/faq.mdx`

- [ ] **Step 1: Create all English pages**

Create English translations of all 12 Spanish pages. Each page mirrors its Spanish counterpart exactly but in English. The content structure, links, and components used are identical.

Key translation notes:
- All internal links must use `/ChineseHSK/en/` prefix instead of `/ChineseHSK/es/`
- The `hero` actions in the welcome page should point to English paths
- HSK1 page imports the same `VocabularyTable` and `vocabData`
- HSK2-5 placeholders use "Coming soon" instead of "Próximamente"
- FAQ answers are in English

- [ ] **Step 2: Commit**

```bash
git add docs-site/src/content/docs/en/
git commit -m "feat: add English content pages (all 12 pages)"
```

---

### Task 6: Vocabulary Table Component

**Files:**
- Create: `docs-site/src/components/VocabularyTable.astro`

- [ ] **Step 1: Create the VocabularyTable component**

```astro
---
interface VocabEntry {
  hanzi: string;
  pinyin: string;
  spanish: string;
  english: string;
  category: string;
}

interface Props {
  data: VocabEntry[];
}

const { data } = Astro.props;
const categories = [...new Set(data.map(e => e.category))];
---

<div class="vocab-container">
  <div class="vocab-controls">
    <input
      type="text"
      id="vocab-search"
      placeholder="Buscar / Search..."
      class="vocab-search"
    />
    <div class="vocab-filters">
      <button class="filter-btn active" data-filter="all">Todo / All</button>
      {categories.map(cat => (
        <button class="filter-btn" data-filter={cat}>{cat}</button>
      ))}
    </div>
  </div>

  <div class="vocab-table-wrapper">
    <table class="vocab-table">
      <thead>
        <tr>
          <th>汉字</th>
          <th>Pinyin</th>
          <th>Español</th>
          <th>English</th>
          <th>Categoría</th>
        </tr>
      </thead>
      <tbody id="vocab-body">
        {data.map(entry => (
          <tr data-category={entry.category}>
            <td class="hanzi-cell">{entry.hanzi}</td>
            <td>{entry.pinyin}</td>
            <td>{entry.spanish}</td>
            <td>{entry.english}</td>
            <td><span class="category-badge">{entry.category}</span></td>
          </tr>
        ))}
      </tbody>
    </table>
  </div>

  <p class="vocab-count">
    Mostrando <span id="visible-count">{data.length}</span> de {data.length} entradas
  </p>
</div>

<style>
  .vocab-container {
    margin: 1.5rem 0;
  }

  .vocab-controls {
    margin-bottom: 1rem;
  }

  .vocab-search {
    width: 100%;
    padding: 0.75rem 1rem;
    font-size: 1rem;
    border: 2px solid var(--sl-color-gray-4);
    border-radius: 8px;
    background: var(--sl-color-bg);
    color: var(--sl-color-text);
    margin-bottom: 0.75rem;
  }

  .vocab-search:focus {
    outline: none;
    border-color: var(--sl-color-accent);
  }

  .vocab-filters {
    display: flex;
    flex-wrap: wrap;
    gap: 0.5rem;
  }

  .filter-btn {
    padding: 0.4rem 0.8rem;
    border: 1px solid var(--sl-color-gray-4);
    border-radius: 20px;
    background: var(--sl-color-bg);
    color: var(--sl-color-text);
    cursor: pointer;
    font-size: 0.85rem;
    transition: all 0.2s;
  }

  .filter-btn:hover {
    border-color: var(--sl-color-accent);
  }

  .filter-btn.active {
    background: var(--sl-color-accent);
    color: white;
    border-color: var(--sl-color-accent);
  }

  .vocab-table-wrapper {
    overflow-x: auto;
    border-radius: 8px;
    border: 1px solid var(--sl-color-gray-5);
  }

  .vocab-table {
    width: 100%;
    border-collapse: collapse;
    font-size: 0.95rem;
  }

  .vocab-table th {
    background: var(--sl-color-gray-6);
    padding: 0.75rem;
    text-align: left;
    font-weight: 600;
    position: sticky;
    top: 0;
  }

  .vocab-table td {
    padding: 0.6rem 0.75rem;
    border-top: 1px solid var(--sl-color-gray-6);
  }

  .vocab-table tbody tr:hover {
    background: var(--sl-color-gray-7);
  }

  .hanzi-cell {
    font-size: 1.4em;
    font-weight: bold;
    font-family: 'Noto Sans SC', sans-serif;
  }

  .category-badge {
    display: inline-block;
    padding: 0.2rem 0.5rem;
    border-radius: 12px;
    font-size: 0.75rem;
    background: var(--sl-color-accent-low);
    color: var(--sl-color-accent-high);
  }

  .vocab-count {
    margin-top: 0.75rem;
    font-size: 0.85rem;
    color: var(--sl-color-gray-2);
  }

  @media (max-width: 640px) {
    .vocab-table {
      font-size: 0.85rem;
    }
    .hanzi-cell {
      font-size: 1.2em;
    }
  }
</style>

<script>
  document.addEventListener('DOMContentLoaded', () => {
    const search = document.getElementById('vocab-search') as HTMLInputElement;
    const tbody = document.getElementById('vocab-body')!;
    const rows = Array.from(tbody.querySelectorAll('tr'));
    const filterBtns = document.querySelectorAll('.filter-btn');
    const countEl = document.getElementById('visible-count')!;
    let activeFilter = 'all';

    function filterRows() {
      const query = search.value.toLowerCase();
      let visible = 0;

      rows.forEach(row => {
        const category = row.getAttribute('data-category') || '';
        const text = row.textContent?.toLowerCase() || '';
        const matchesFilter = activeFilter === 'all' || category === activeFilter;
        const matchesSearch = !query || text.includes(query);
        const show = matchesFilter && matchesSearch;
        (row as HTMLElement).style.display = show ? '' : 'none';
        if (show) visible++;
      });

      countEl.textContent = String(visible);
    }

    search.addEventListener('input', filterRows);

    filterBtns.forEach(btn => {
      btn.addEventListener('click', () => {
        filterBtns.forEach(b => b.classList.remove('active'));
        btn.classList.add('active');
        activeFilter = (btn as HTMLElement).getAttribute('data-filter') || 'all';
        filterRows();
      });
    });
  });
</script>
```

Write this to `docs-site/src/components/VocabularyTable.astro`.

- [ ] **Step 2: Commit**

```bash
git add docs-site/src/components/VocabularyTable.astro
git commit -m "feat: add interactive vocabulary table component with search and filter"
```

---

### Task 7: Build-time Vocabulary Data Generator

**Files:**
- Create: `docs-site/scripts/generate-vocab-data.ts`
- Create: `docs-site/src/data/hsk1-vocab.json`

- [ ] **Step 1: Create the generate script**

```javascript
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
```

Write this to `docs-site/scripts/generate-vocab-data.ts` (despite the `.ts` extension, use plain Node.js so no build step is needed — rename to `generate-vocab-data.js` if the implementer prefers).

- [ ] **Step 2: Run the generator**

```bash
cd /Users/maximiliano/Repositories/Personal/Chineese/docs-site && node scripts/generate-vocab-data.ts
```

Expected: `Generated 338 entries to src/data/hsk1-vocab.json`

- [ ] **Step 3: Update package.json build script**

Ensure `docs-site/package.json` scripts section has:
```json
"build": "node scripts/generate-vocab-data.ts && astro build",
"dev": "node scripts/generate-vocab-data.ts && astro dev",
"preview": "astro preview"
```

- [ ] **Step 4: Commit**

```bash
git add docs-site/scripts/ docs-site/src/data/
git commit -m "feat: add build-time vocabulary data generator from HSK JSON files"
```

---

### Task 8: GitHub Actions Deployment Workflow

**Files:**
- Create: `.github/workflows/deploy-site.yml`

- [ ] **Step 1: Create deployment workflow**

```yaml
name: Deploy Docs Site

on:
  push:
    branches: [main]
    paths:
      - 'docs-site/**'
      - 'HSK1/data/**'

  workflow_dispatch:

permissions:
  contents: read
  pages: write
  id-token: write

concurrency:
  group: pages
  cancel-in-progress: true

jobs:
  build:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v4

      - name: Setup Node.js
        uses: actions/setup-node@v4
        with:
          node-version: 20

      - name: Install dependencies
        working-directory: docs-site
        run: npm ci

      - name: Generate vocabulary data
        working-directory: docs-site
        run: node scripts/generate-vocab-data.ts

      - name: Build site
        working-directory: docs-site
        run: npx astro build

      - name: Upload artifact
        uses: actions/upload-pages-artifact@v3
        with:
          path: docs-site/dist

  deploy:
    needs: build
    runs-on: ubuntu-latest
    environment:
      name: github-pages
      url: ${{ steps.deployment.outputs.page_url }}
    steps:
      - name: Deploy to GitHub Pages
        id: deployment
        uses: actions/deploy-pages@v4
```

Write this to `.github/workflows/deploy-site.yml`.

- [ ] **Step 2: Add .superpowers to .gitignore**

Append to the repo root `.gitignore`:
```
# Visual companion brainstorming sessions
.superpowers/
```

- [ ] **Step 3: Commit**

```bash
git add .github/workflows/deploy-site.yml .gitignore
git commit -m "feat: add GitHub Actions workflow for docs site deployment"
```

---

### Task 9: Test, Fix, and Verify Locally

**Files:**
- Modify: various files as needed based on testing

- [ ] **Step 1: Install dependencies**

```bash
cd /Users/maximiliano/Repositories/Personal/Chineese/docs-site && npm install
```

- [ ] **Step 2: Generate vocabulary data**

```bash
node scripts/generate-vocab-data.ts
```

- [ ] **Step 3: Run dev server and test**

```bash
npm run dev
```

Test at `http://localhost:4321/ChineseHSK/`:
1. Welcome page loads with hero section and cards
2. Language switcher works (ES ↔ EN)
3. Sidebar navigation shows all sections
4. All pages render correctly
5. HSK1 page shows the interactive vocabulary table
6. Search and category filters work on the vocabulary table
7. Mobile responsive layout works

- [ ] **Step 4: Fix any issues found during testing**

Common issues to watch for:
- Starlight i18n slug resolution (may need to adjust `astro.config.mjs` sidebar slugs)
- Component imports in `.mdx` files (ensure paths are correct)
- Base path `/ChineseHSK/` in internal links
- JSON import in `.mdx` files (may need Astro config adjustment)

- [ ] **Step 5: Build for production**

```bash
npm run build && npm run preview
```

Verify the production build at `http://localhost:4321/ChineseHSK/`.

- [ ] **Step 6: Commit any fixes**

```bash
git add -A docs-site/
git commit -m "fix: resolve issues found during local testing"
```

---

### Task 10: Push and Enable GitHub Pages

- [ ] **Step 1: Push all commits**

```bash
git push
```

- [ ] **Step 2: Enable GitHub Pages**

Run:
```bash
gh api repos/maxponmar/ChineseHSK/pages -X PUT -f build_type=workflow
```

If that fails (pages not yet created), use:
```bash
gh api repos/maxponmar/ChineseHSK/pages -X POST -f build_type=workflow -f source='{"branch":"main","path":"/"}'
```

- [ ] **Step 3: Verify deployment**

Wait for the GitHub Actions workflow to complete:
```bash
gh run list --workflow=deploy-site.yml --limit 1
```

Once complete, verify the site at: `https://maxponmar.github.io/ChineseHSK/`

- [ ] **Step 4: Commit any final fixes**

If the deployed site has issues (broken links, base path problems), fix and push.
