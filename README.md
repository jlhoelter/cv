# CV Generator

Automatische Konvertierung von Markdown-CVs zu professionellen Word-Dokumenten mit Foto.

## Quick Start

```bash
cd /Users/jan/workspace/tracks/jobsuche/cv
./generate-cv.sh CV_Jan_Hoelter_TIMOCOM_DE.md
```

## Features

- ✅ Automatische Konvertierung Markdown → Word
- ✅ Foto-Integration (rechts oben)
- ✅ Professionelles Layout (Calibri, Farben, Abstände)
- ✅ Ausgabedatei erhält automatisch gleichen Namen wie Input
- ✅ Minimale Claude-Nutzung (lokales Script)

## Verwendung

### Aus dem CV-Ordner

```bash
./generate-cv.sh <markdown-file>
```

### Von überall (mit Alias)

Füge zu deiner `~/.zshrc` oder `~/.bashrc` hinzu:

```bash
alias generate-cv='/Users/jan/workspace/tracks/jobsuche/cv/generate-cv.sh'
```

Dann kannst du von überall:

```bash
cd /path/to/application/folder
generate-cv CV_Jan_Hoelter_COMPANY.md
```

## Markdown-Format

Das Script erwartet folgendes Markdown-Format:

```markdown
# Jan Hölter
**Untertitel/Position**
*Tagline*

Kontaktinfo
📧 email@example.com
🔗 linkedin-url

---

## Sektion (z.B. Profil)

Fließtext...

---

## Berufserfahrung

### **Firma**
**Position** | Datum

- Aufzählungspunkt 1
- Aufzählungspunkt 2

---

## Weitere Sektionen...
```

## Ausgabe

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

## Troubleshooting

### "python-docx not found"
```bash
pip3 install python-docx
```

### "Permission denied"
```bash
chmod +x generate-cv.sh
```

### "Photo not found"
Script läuft trotzdem, erstellt CV ohne Foto.

## Vorteile gegenüber manueller Claude-Nutzung

- ⚡ **Schneller:** 2 Sekunden statt mehrere Minuten
- 💰 **Kostenlos:** Keine Claude-Tokens
- 🔄 **Wiederholbar:** Immer gleiches Layout
- 🎯 **Konsistent:** Keine Variationen zwischen CVs
- 🛠️ **Anpassbar:** Script kann erweitert werden
