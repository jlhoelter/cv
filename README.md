# CV – Jan Hölter

Minimalistischer HTML-CV-Generator. Markdown rein, druckbares HTML raus.

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
├── CV_Jan_Hoelter_final.md    # Source of truth
├── Jan_Hoelter_Foto.jpeg      # Profilfoto
├── generate-html.py           # Generator (Python, keine Dependencies)
├── generate-html.sh           # Generate Script
├── publish-cv.sh              # Publish zu GitHub Pages
├── index.html                 # Generiertes HTML (Output)
├── cv-complete-final.html     # Reference Template (Design-Referenz)
└── README.md
```

---

## Workflow

### CV aktualisieren
```bash
# 1. Markdown editieren
vim CV_Jan_Hoelter_final.md

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
*Tagline*

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

### Firma Name
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
- **Schwerpunkte:** Subsections → 2-Spalten Cards; "Methoden" → Pills
- **Haltung:** Subsections → 2×2 Grid Cards
- **Sprachen:** Bullets → einzelner Text mit `·` Separator
- **Berufserfahrung:** Beschreibung nach `*Zeitraum*` → `text-xs` Paragraph vor Bullets

---

## Design

- **Font:** Inter (Google Fonts)
- **CSS:** Tailwind via CDN (kein Build-Step)
- **Layout:** max-w-3xl, Shadow-Container, A4-optimiert
- **Print:** `@page { size: A4; margin: 12mm 15mm; }`
- **Page Breaks:** Sections bleiben zusammen (`no-break`), Berufserfahrung darf zwischen Jobs umbrechen

---

## Troubleshooting

**"Permission denied"**
```bash
chmod +x generate-html.sh publish-cv.sh
```

**Fehlende Sektionen**
- `##` für Sektionen, `###` für Subsektionen
- Kein `**` im `###`-Titel (z.B. `### Firma Name`, nicht `### **Firma Name**`)
- Bullets mit `- ` (Dash + Space)

**Print: Seite bricht falsch um**
- Chrome: Weitere Einstellungen → Kopf- und Fußzeilen ausschalten
