# CV Generator

Automatisiertes CV-Generierungssystem mit Unterstützung für HTML und Word-Formate, Mehrsprachigkeit (DE/EN) und GitHub Pages.

## Quick Start

```bash
cd /Users/jan/workspace/tracks/jobsuche/cv

# HTML generieren (Standard: Deutsch)
./generate-html.sh

# Word-Dokument generieren
./generate-cv.sh CV_Jan_Hoelter_TIMOCOM_DE.md

# Englische HTML-Version
LANG=en OUTPUT_FILE=index-en.html ./generate-html.sh
```

## Features

- ✅ **Minimalist HTML CV** mit Tailwind CSS
- ✅ **Word-Export** mit python-docx
- ✅ **Zweisprachig** (Deutsch/English)
- ✅ **Druck-optimiert** mit A4 Seitenumbrüchen
- ✅ **Share-Funktion** (Web Share API + Clipboard Fallback)
- ✅ **GitHub Pages ready**
- ✅ **Foto-Integration**
- ✅ **Minimale Claude-Nutzung** (lokales Script)

## Dateistruktur

```
cv/
├── CV_Jan_Hoelter_final.md      # Source Markdown (Deutsch)
├── Jan_Hoelter_Foto.jpeg        # Profilfoto
├── generate-html.py             # HTML-Generator (Python)
├── generate-html.sh             # HTML-Wrapper-Skript
├── generate-cv.sh               # Word-Dokument-Generator
├── index.html                   # Generiertes HTML (Deutsch)
├── index-en.html                # Generiertes HTML (Englisch, optional)
└── README.md                    # Diese Datei
```

## Verwendung

### HTML CV generieren

```bash
# Deutsch (Standard)
./generate-html.sh

# Englisch
LANG=en OUTPUT_FILE=index-en.html ./generate-html.sh

# Custom Markdown
MARKDOWN_FILE=custom-cv.md OUTPUT_FILE=output.html ./generate-html.sh
```

### Word-Dokument generieren

```bash
./generate-cv.sh <markdown-file>
```

### Python direkt

```bash
# Deutsch
python3 generate-html.py CV_Jan_Hoelter_final.md -o index.html -l de

# Englisch
python3 generate-html.py CV_Jan_Hoelter_EN.md -o index-en.html -l en
```

### Mit globalem Alias (optional)

Füge zu `~/.zshrc` oder `~/.bashrc` hinzu:

```bash
alias generate-html='/Users/jan/workspace/tracks/jobsuche/cv/generate-html.sh'
alias generate-cv='/Users/jan/workspace/tracks/jobsuche/cv/generate-cv.sh'
```

Dann von überall:

```bash
generate-html
generate-cv CV_Jan_Hoelter_COMPANY.md
```

## Markdown-Struktur

Der HTML-Generator erwartet diese Struktur:

```markdown
# Name
**Title**
*Tagline*

Location
📧 email@example.com
📞 +49 123 456789
🔗 https://linkedin.com/in/profile

---

## Sektion (z.B. Profil)

Fließtext Paragraph 1...

Fließtext Paragraph 2...

---

## Berufserfahrung

### **Firma Name**
**Position**
*Zeitraum | Ort*

Optionale Beschreibung...

- Aufzählungspunkt 1
- Aufzählungspunkt 2

### **Zweite Firma**
**Zweite Position**
*Zeitraum | Ort*

- Aufzählungspunkt 1
- Aufzählungspunkt 2

---

## Schwerpunkte

### Kompetenzbereich 1
Beschreibung...

### Kompetenzbereich 2
Beschreibung...

### Methoden & Arbeitsweisen
- Methode 1
- Methode 2

---

## Haltung

### Prinzip 1
Beschreibung...

### Prinzip 2
Beschreibung...
```

### Spezial-Sektionen

- **Schwerpunkte:** Subsections → 2-Spalten Cards, "Methoden" → Pills
- **Haltung:** Subsections → 2x2 Grid Cards
- **Berufserfahrung:** Company (###) → Timeline mit Job-Details und Bullets

## Design

### HTML Output
- **Minimalist Style:** Grayscale Farbpalette (keine Farben)
- **Typografie:** Inter Font (Google Fonts)
- **Layout:**
  - Header mit Foto (w-28 h-28, object-top, grayscale)
  - Kontakt-Icons horizontal
  - 2-Spalten Cards (Schwerpunkte, Haltung)
  - Pills für Methoden (rounded-full, border)
- **Print-Optimiert:** A4, @page margins, no-break classes
- **Responsive:** Tailwind CSS via CDN
- **Actions:** Drucken + Teilen Buttons (Web Share API)

### Word Output
- **Dateiname:** Identisch mit Input, `.md` → `.docx`
- **Foto:** Automatisch eingefügt wenn `Jan_Hoelter_Foto.jpeg` existiert
- **Layout:**
  - Schmale Margins (professionell)
  - Foto rechts oben (1.2" breit)
  - Überschriften in Dunkelblau (RGB 0,51,102)
  - Kontaktinfo in Grau, kleiner Font
  - Bullet Points mit Einzug

## Beispiele

### TIMOCOM CV generieren
```bash
./generate-cv.sh CV_Jan_Hoelter_TIMOCOM_DE.md
# → CV_Jan_Hoelter_TIMOCOM_DE.docx
```

### Kartenmacherei CV generieren
```bash
./generate-cv.sh CV_Jan_Hoelter_Kartenmacherei.md
# → CV_Jan_Hoelter_Kartenmacherei.docx
```

## GitHub Pages Setup

### Option A: Dediziertes CV Repository

```bash
cd /Users/jan/workspace/tracks/jobsuche/cv
git init
git add .
git commit -m "Initial commit: Automated CV generator with bilingual support"
git remote add origin <github-repo-url>
git push -u origin main
```

**GitHub Settings:**
- Repository → Settings → Pages
- Source: Deploy from branch `main`
- Folder: `/` (root)

**Ergebnis:** CV unter `https://username.github.io/repo-name/`

### Option B: Innerhalb bestehendem Repository

```bash
cd /Users/jan/workspace
git add tracks/jobsuche/cv/
git commit -m "Add automated CV HTML generator"
git push
```

**GitHub Settings:**
- Source: `main` branch
- Folder: `/tracks/jobsuche/cv` (wenn nested)

**Optional: Custom Domain**
- Füge `CNAME` Datei hinzu mit deiner Domain
- DNS konfigurieren (A/CNAME Records)

## Internationalisierung (i18n)

### Englische Variante erstellen

1. **Englisches Markdown erstellen:**
   ```bash
   cp CV_Jan_Hoelter_final.md CV_Jan_Hoelter_EN.md
   # Inhalt übersetzen
   ```

2. **HTML generieren:**
   ```bash
   LANG=en OUTPUT_FILE=index-en.html MARKDOWN_FILE=CV_Jan_Hoelter_EN.md ./generate-html.sh
   ```

3. **Language Switcher hinzufügen (optional):**
   In beiden HTML-Dateien im Header:
   ```html
   <div class="language-switcher">
     <a href="index.html">DE</a> | <a href="index-en.html">EN</a>
   </div>
   ```

## Troubleshooting

### HTML-Generator

**"Permission denied"**
```bash
chmod +x generate-html.sh
```

**"Photo not found"**
Skript läuft trotzdem, verwendet Default-Pfad. Setze:
```bash
PHOTO_FILE=/path/to/photo.jpg ./generate-html.sh
```

**Fehlende Sektionen**
- Prüfe Markdown-Struktur (## für Sektionen, ### für Subsektionen)
- Verwende `---` Separator zwischen Haupt-Sektionen
- Bullets müssen mit `- ` (Dash + Space) beginnen

**Print-Layout-Probleme**
- Teste mit verschiedenen Browsern (Chrome, Firefox, Safari)
- Prüfe `no-break` Klassen in generierten Sektionen
- A4-Breite nicht überschreiten

### Word-Generator

**"python-docx not found"**
```bash
pip3 install python-docx
```

**"Permission denied"**
```bash
chmod +x generate-cv.sh
```

## Vorteile

- ⚡ **Schnell:** 2 Sekunden statt mehrere Minuten
- 💰 **Kostenlos:** Keine Claude-Tokens
- 🔄 **Wiederholbar:** Immer gleiches Layout
- 🎯 **Konsistent:** Keine Variationen zwischen CVs
- 🌍 **Mehrsprachig:** DE/EN Unterstützung
- 🛠️ **Anpassbar:** Scripts können erweitert werden
- 🌐 **Hosted:** GitHub Pages für öffentliche URL

## Dependencies

- **Python 3:** Standard installation (kein pip package nötig für HTML)
- **python-docx:** Nur für Word-Export (`pip3 install python-docx`)
- **Tailwind CSS:** Via CDN (kein Build-Step)
- **Git:** Für GitHub Pages (optional)
