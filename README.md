# CV – Jan Musiedlak

HTML-CV-Generator mit Zinc-Teal Brand Kit. Markdown rein, druckbares HTML raus.

**Live:** https://jlhoelter.github.io/cv/

---

## Quick Start

```bash
# 1. CV generieren
./generate-html.sh

# 2. Lokal im Browser öffnen
open index.html

# 3. Online publishen
./publish-cv.sh
```

---

## Dateistruktur

```
cv/
├── CV_Jan_Musiedlak_final.md    # Source of truth
├── generate-html.py           # Generator (Python, keine Dependencies)
├── generate-html.sh           # Generate Script
├── publish-cv.sh              # Publish zu GitHub Pages
├── index.html                 # Generiertes HTML (Output)
├── jan-cv-reference.html      # Design-Referenz (Brand Kit)
├── assets/
│   ├── Jan_Musiedlak_Foto.jpeg  # Profilfoto
│   └── fonts/                 # Lokale Geist-Fonts (WOFF2)
│       ├── Geist-Regular.woff2
│       ├── Geist-Medium.woff2
│       ├── Geist-SemiBold.woff2
│       ├── Geist-Bold.woff2
│       ├── GeistMono-Regular.woff2
│       ├── GeistMono-Medium.woff2
│       ├── GeistMono-SemiBold.woff2
│       └── GeistPixel-Square.woff2
└── README.md
```

---

## Workflow

### CV aktualisieren
```bash
# 1. Markdown editieren
vim CV_Jan_Musiedlak_final.md

# 2. HTML generieren und prüfen
./generate-html.sh
open index.html

# 3. Im main workspace committen
cd /Users/jan/workspace
git add tracks/jobsuche/cv/
git commit -m "Update CV"
git push

# 4. Online publishen
cd tracks/jobsuche/cv
./publish-cv.sh
```

### PDF exportieren
1. `open index.html` im Browser
2. `Cmd+P` → Drucken
3. **"Kopf- und Fußzeilen" ausschalten**
4. "Hintergrundgrafiken" einschalten
5. Als PDF speichern

---

## Markdown-Struktur

```markdown
# Name
**Title**
*Tagline*                          ← wird als Hero Statement angezeigt

Köln, Deutschland
📧 email@example.com
📞 +49 123 456789
🔗 https://linkedin.com/in/profile

---

## Profil

Paragraph 1...

Paragraph 2...

---

## Berufserfahrung

### Firma Name                     ← kein ** im Titel
**Position**
*Zeitraum | Ort*

Optionale Beschreibung...

- Bullet 1
- Bullet 2

---

## Ausbildung

### Universität
Abschluss
*Zeitraum*

---

## Schwerpunkte

Intro-Paragraph...

### Kompetenzbereich 1
Beschreibung...

### Methoden & Arbeitsweisen
- Methode 1
- Methode 2

---

## Haltung

Intro-Paragraph...

### Prinzip 1
Beschreibung...

---

## Sprachen

- Deutsch (Muttersprache)
- Englisch (fließend)
```

### Besonderheiten
- **Tagline** (`*italic*` im Header) → großes Hero Statement über dem Profil
- **Berufserfahrung:** `### Firma` + `**Jobtitel**` → Ausgabe `"Jobtitel, Firma"`; Zeitraum und Ort aus `*Zeitraum | Ort*`
- **Schwerpunkte:** Subsections → 2-Spalten Cards; "Methoden" → Pills
- **Haltung:** Subsections → 2×2 Grid Cards; Section Label triggert Seitenumbruch
- **Sprachen:** Bullets → einzelner Text mit `·` Separator

---

## Design

- **Font:** Geist (lokal, WOFF2) – kein CDN
- **Farben:** Zinc/Teal – `bg-zinc-50` Hintergrund, `teal-600` Akzente
- **CSS:** Tailwind via CDN + Custom `.ref-card` / `.ref-tag`
- **Layout:** `max-w-[210mm]` (A4-exakt), drei Hintergrund-Zonen
- **Print:** `@page { size: A4; margin: 10mm 18mm; }`, `print:text-[0.7rem]`
- **Design-Referenz:** `jan-cv-reference.html`

---

## Troubleshooting

**"Permission denied"**
```bash
chmod +x generate-html.sh publish-cv.sh
```

**Fehlende Sektionen**
- `##` für Sektionen, `###` für Subsektionen
- Kein `**` im `###`-Titel: `### Firma Name`, nicht `### **Firma Name**`
- Bullets mit `- ` (Dash + Space)

**Print: Seite bricht falsch um**
- Chrome: Weitere Einstellungen → Kopf- und Fußzeilen ausschalten
