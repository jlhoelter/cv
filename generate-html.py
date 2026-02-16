#!/usr/bin/env python3
"""
CV HTML Generator
Generates minimalist HTML CV from structured markdown
"""

import sys
import re
from pathlib import Path
from typing import Dict, List, Any

class CVParser:
    """Parse structured markdown CV into data model"""

    def __init__(self, markdown_path: str):
        self.markdown = Path(markdown_path).read_text(encoding='utf-8')
        self.data = self._parse()

    def _parse(self) -> Dict[str, Any]:
        """Parse markdown into structured data"""
        lines = self.markdown.split('\n')
        data = {
            'header': self._parse_header(lines),
            'sections': self._parse_sections(lines)
        }
        return data

    def _parse_header(self, lines: List[str]) -> Dict[str, str]:
        """Extract header information (name, title, tagline, contact)"""
        header = {}

        # Name (# Title)
        for i, line in enumerate(lines):
            if line.startswith('# '):
                header['name'] = line[2:].strip()
                # Title (**bold**)
                if i+1 < len(lines) and lines[i+1].startswith('**'):
                    # Remove all ** from title
                    title_text = lines[i+1]
                    while '**' in title_text:
                        title_text = title_text.replace('**', '')
                    header['title'] = title_text.strip()
                # Tagline (*italic*)
                if i+2 < len(lines) and lines[i+2].startswith('*'):
                    header['tagline'] = lines[i+2].strip('*').strip()
                break

        # Contact info
        contact_lines = []
        for line in lines[:20]:  # First 20 lines
            if any(x in line for x in ['📧', '📞', '🔗', 'Deutschland', 'Germany']):
                contact_lines.append(line)

        header['contact'] = self._parse_contact(contact_lines)
        return header

    def _parse_contact(self, lines: List[str]) -> Dict[str, str]:
        """Parse contact information"""
        contact = {}
        for line in lines:
            if 'Deutschland' in line or 'Germany' in line:
                contact['location'] = line.strip()
            elif '📧' in line or '@' in line:
                contact['email'] = line.replace('📧', '').strip()
            elif '📞' in line or '+49' in line:
                contact['phone'] = line.replace('📞', '').strip()
            elif '🔗' in line or 'linkedin.com' in line:
                contact['linkedin'] = line.replace('🔗', '').strip()
        return contact

    def _parse_sections(self, lines: List[str]) -> List[Dict[str, Any]]:
        """Parse all sections after header"""
        sections = []
        current_section = None
        current_subsection = None

        i = 0
        while i < len(lines):
            line = lines[i].strip()

            # Section (## Title)
            if line.startswith('## '):
                if current_section:
                    sections.append(current_section)

                title = line[3:].strip()
                current_section = {
                    'title': title,
                    'type': self._section_type(title),
                    'content': [],
                    'subsections': []
                }
                current_subsection = None

            # Subsection (### Title)
            elif line.startswith('### '):
                if current_section:
                    subtitle = line[4:].strip().strip('*').strip()  # Remove ** from title
                    current_subsection = {
                        'title': subtitle,
                        'content': []
                    }
                    current_section['subsections'].append(current_subsection)

            # Job title (bold)
            elif line.startswith('**') and current_subsection:
                current_subsection['job_title'] = line.strip('*').strip()

            # Period (italic)
            elif line.startswith('*') and current_subsection and not line.startswith('**'):
                current_subsection['period'] = line.strip('*').strip()

            # Bullet point
            elif line.startswith('- ') and current_section:
                bullet = line[2:].strip()
                if current_subsection:
                    if 'bullets' not in current_subsection:
                        current_subsection['bullets'] = []
                    current_subsection['bullets'].append(bullet)
                else:
                    current_section['content'].append({'type': 'bullet', 'text': bullet})

            # Regular paragraph
            elif line and not line.startswith('#') and not line.startswith('---'):
                if current_subsection:
                    # Check if this is description (after period, before bullets)
                    if 'period' in current_subsection and 'bullets' not in current_subsection:
                        if 'description' not in current_subsection:
                            current_subsection['description'] = []
                        current_subsection['description'].append(line)
                    elif 'bullets' not in current_subsection and 'period' not in current_subsection:
                        # Content before period
                        current_subsection['content'].append(line)
                elif current_section:
                    current_section['content'].append({'type': 'text', 'text': line})

            i += 1

        if current_section:
            sections.append(current_section)

        return sections

    def _section_type(self, title: str) -> str:
        """Determine section type from title"""
        title_lower = title.lower()
        if 'profil' in title_lower or 'profile' in title_lower:
            return 'profil'
        elif 'beruf' in title_lower or 'experience' in title_lower:
            return 'berufserfahrung'
        elif 'ausbildung' in title_lower or 'education' in title_lower:
            return 'ausbildung'
        elif 'schwerpunkt' in title_lower or 'focus' in title_lower:
            return 'schwerpunkte'
        elif 'haltung' in title_lower or 'principles' in title_lower:
            return 'haltung'
        elif 'sprache' in title_lower or 'language' in title_lower:
            return 'sprachen'
        else:
            return 'generic'


class HTMLGenerator:
    """Generate HTML from parsed CV data"""

    def __init__(self, data: Dict[str, Any], photo_path: str = 'Jan_Hoelter_Foto.jpeg', lang: str = 'de'):
        self.data = data
        self.photo = photo_path
        self.lang = lang
        self.labels = self._get_labels()

    def _get_labels(self) -> Dict[str, str]:
        """UI labels based on language"""
        if self.lang == 'en':
            return {
                'print': 'Print',
                'share': 'Share',
                'link_copied': 'Link copied!'
            }
        else:
            return {
                'print': 'Drucken',
                'share': 'Teilen',
                'link_copied': 'Link kopiert!'
            }

    def generate(self) -> str:
        """Generate complete HTML"""
        header = self._generate_header()
        sections = self._generate_sections()

        return self._template(header, sections)

    def _template(self, header: str, sections: str) -> str:
        """HTML template with Tailwind styling"""
        lang_attr = 'en' if self.lang == 'en' else 'de'

        return f'''<!DOCTYPE html>
<html lang="{lang_attr}">
<head>
  <meta charset="UTF-8">
  <meta name="viewport" content="width=device-width, initial-scale=1.0">
  <title>{self.data['header']['name']}</title>
  <script src="https://cdn.tailwindcss.com"></script>
  <script>
    tailwind.config = {{
      theme: {{
        extend: {{
          fontFamily: {{
            sans: ['Inter', 'system-ui', 'sans-serif'],
          }},
        }},
      }},
    }}
  </script>
  <style>
    @import url('https://fonts.googleapis.com/css2?family=Inter:wght@300;400;500;600&display=swap');
    @page {{ size: A4; margin: 20mm; }}
    @media print {{
      body {{ -webkit-print-color-adjust: exact; print-color-adjust: exact; }}
      .no-print {{ display: none !important; }}
    }}
  </style>
</head>
<body class="font-sans text-gray-900 bg-gray-50 leading-relaxed">
  <!-- Action Buttons -->
  <div class="no-print fixed top-4 right-4 flex gap-2">
    <button onclick="window.print()" class="px-3 py-1.5 text-xs text-gray-600 border border-gray-300 rounded hover:bg-gray-50 flex items-center gap-1.5 bg-white">
      <svg class="w-3.5 h-3.5" fill="none" stroke="currentColor" viewBox="0 0 24 24">
        <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M17 17h2a2 2 0 002-2v-4a2 2 0 00-2-2H5a2 2 0 00-2 2v4a2 2 0 002 2h2m2 4h6a2 2 0 002-2v-4a2 2 0 00-2-2H9a2 2 0 00-2 2v4a2 2 0 002 2zm8-12V5a2 2 0 00-2-2H9a2 2 0 00-2 2v4h10z"></path>
      </svg>
      {self.labels['print']}
    </button>
    <button onclick="if(navigator.share){{navigator.share({{title:'{self.data['header']['name']} - CV',url:window.location.href}})}}else{{navigator.clipboard.writeText(window.location.href);alert('{self.labels['link_copied']}')}}\" class="px-3 py-1.5 text-xs text-gray-600 border border-gray-300 rounded hover:bg-gray-50 flex items-center gap-1.5 bg-white">
      <svg class="w-3.5 h-3.5" fill="none" stroke="currentColor" viewBox="0 0 24 24">
        <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M8.684 13.342C8.886 12.938 9 12.482 9 12c0-.482-.114-.938-.316-1.342m0 2.684a3 3 0 110-2.684m0 2.684l6.632 3.316m-6.632-6l6.632-3.316m0 0a3 3 0 105.367-2.684 3 3 0 00-5.367 2.684zm0 9.316a3 3 0 105.368 2.684 3 3 0 00-5.368-2.684z"></path>
      </svg>
      {self.labels['share']}
    </button>
  </div>

  <!-- Container with Shadow -->
  <div class="max-w-3xl mx-auto my-8 bg-white shadow-lg print:shadow-none">
    <div class="px-8 py-16 print:px-0 print:py-0">
{header}
{sections}
    </div>
  </div>
</body>
</html>
'''

    def _generate_header(self) -> str:
        """Generate header section"""
        h = self.data['header']
        contact = h.get('contact', {})

        # Contact items with SVG icons
        contact_items = []

        if 'location' in contact:
            contact_items.append(f'''        <span class="flex items-center gap-1.5">
          <svg class="w-3.5 h-3.5" fill="currentColor" viewBox="0 0 20 20"><path fill-rule="evenodd" d="M5.05 4.05a7 7 0 119.9 9.9L10 18.9l-4.95-4.95a7 7 0 010-9.9zM10 11a2 2 0 100-4 2 2 0 000 4z" clip-rule="evenodd"></path></svg>
          {contact['location']}
        </span>''')

        if 'email' in contact:
            contact_items.append(f'''        <span class="flex items-center gap-1.5">
          <svg class="w-3.5 h-3.5" fill="currentColor" viewBox="0 0 20 20"><path d="M2.003 5.884L10 9.882l7.997-3.998A2 2 0 0016 4H4a2 2 0 00-1.997 1.884z"></path><path d="M18 8.118l-8 4-8-4V14a2 2 0 002 2h12a2 2 0 002-2V8.118z"></path></svg>
          {contact['email']}
        </span>''')

        if 'phone' in contact:
            contact_items.append(f'''        <span class="flex items-center gap-1.5">
          <svg class="w-3.5 h-3.5" fill="currentColor" viewBox="0 0 20 20"><path d="M2 3a1 1 0 011-1h2.153a1 1 0 01.986.836l.74 4.435a1 1 0 01-.54 1.06l-1.548.773a11.037 11.037 0 006.105 6.105l.774-1.548a1 1 0 011.059-.54l4.435.74a1 1 0 01.836.986V17a1 1 0 01-1 1h-2C7.82 18 2 12.18 2 5V3z"></path></svg>
          {contact['phone']}
        </span>''')

        if 'linkedin' in contact:
            linkedin_url = contact['linkedin'] if contact['linkedin'].startswith('http') else f"https://{contact['linkedin']}"
            contact_items.append(f'''        <a href="{linkedin_url}" class="flex items-center gap-1.5 underline hover:text-gray-900">
          <svg class="w-3.5 h-3.5" fill="currentColor" viewBox="0 0 24 24"><path d="M20.447 20.452h-3.554v-5.569c0-1.328-.027-3.037-1.852-3.037-1.853 0-2.136 1.445-2.136 2.939v5.667H9.351V9h3.414v1.561h.046c.477-.9 1.637-1.85 3.37-1.85 3.601 0 4.267 2.37 4.267 5.455v6.286zM5.337 7.433c-1.144 0-2.063-.926-2.063-2.065 0-1.138.92-2.063 2.063-2.063 1.14 0 2.064.925 2.064 2.063 0 1.139-.925 2.065-2.064 2.065zm1.782 13.019H3.555V9h3.564v11.452zM22.225 0H1.771C.792 0 0 .774 0 1.729v20.542C0 23.227.792 24 1.771 24h20.451C23.2 24 24 23.227 24 22.271V1.729C24 .774 23.2 0 22.222 0h.003z"></path></svg>
          LinkedIn
        </a>''')

        contact_html = '\n'.join(contact_items)

        return f'''      <!-- Header -->
      <header class="mb-16">
        <div class="flex justify-between items-start gap-12 mb-6">
          <div class="flex-1">
            <h1 class="text-4xl font-light mb-1 tracking-tight">{h.get('name', '')}</h1>
            <p class="text-sm text-gray-600 font-medium mb-2">{h.get('title', '')}</p>
            <p class="text-sm text-gray-600 italic">
              {h.get('tagline', '')}
            </p>
          </div>
          <img src="{self.photo}" alt="{h.get('name', '')}" class="w-28 h-28 rounded-full object-cover object-top grayscale">
        </div>
        <div class="flex flex-wrap gap-x-6 gap-y-1 text-xs text-gray-600">
{contact_html}
        </div>
      </header>
'''

    def _generate_sections(self) -> str:
        """Generate all content sections"""
        sections_html = []

        for section in self.data['sections']:
            section_type = section['type']

            if section_type == 'profil':
                sections_html.append(self._generate_profil(section))
            elif section_type == 'berufserfahrung':
                sections_html.append(self._generate_berufserfahrung(section))
            elif section_type == 'ausbildung':
                sections_html.append(self._generate_ausbildung(section))
            elif section_type == 'schwerpunkte':
                sections_html.append(self._generate_schwerpunkte(section))
            elif section_type == 'haltung':
                sections_html.append(self._generate_haltung(section))
            elif section_type == 'sprachen':
                sections_html.append(self._generate_sprachen(section))
            else:
                sections_html.append(self._generate_generic(section))

        return '\n'.join(sections_html)

    def _generate_profil(self, section: Dict) -> str:
        """Generate Profil section with multi-paragraph support"""
        paragraphs = []
        for item in section['content']:
            if item['type'] == 'text':
                paragraphs.append(f'        <p>{item["text"]}</p>')

        paragraphs_html = '\n'.join(paragraphs)

        return f'''      <!-- Profil -->
      <section class="mb-14">
        <h2 class="text-xs uppercase tracking-wider text-gray-500 mb-4 font-medium">{section['title']}</h2>
        <div class="text-sm text-gray-800 space-y-3 leading-relaxed">
{paragraphs_html}
        </div>
      </section>
'''

    def _generate_berufserfahrung(self, section: Dict) -> str:
        """Generate Berufserfahrung section with timeline"""
        jobs_html = []

        for job in section['subsections']:
            # Optional description paragraph after period
            description_html = ''
            if 'description' in job:
                desc_text = ' '.join(job['description'])
                description_html = f'''        <p class="text-sm text-gray-700 mb-2 leading-relaxed">
          {desc_text}
        </p>
'''

            # Bullets
            bullets_html = ''
            if 'bullets' in job:
                bullet_items = '\n'.join([f'          <li>• {bullet}</li>' for bullet in job['bullets']])
                bullets_html = f'''        <ul class="text-xs text-gray-700 space-y-1.5 ml-4">
{bullet_items}
        </ul>'''

            job_html = f'''      <div class="mb-10">
        <div class="mb-2">
          <h3 class="text-base font-medium">{job['title']}</h3>
          <p class="text-sm font-medium text-gray-700">{job.get('job_title', '')}</p>
          <p class="text-xs text-gray-500">{job.get('period', '')}</p>
        </div>
{description_html}{bullets_html}
      </div>'''

            jobs_html.append(job_html)

        jobs_section = '\n'.join(jobs_html)

        return f'''      <!-- Berufserfahrung -->
      <section class="mb-14">
        <h2 class="text-xs uppercase tracking-wider text-gray-500 mb-6 font-medium">{section['title']}</h2>
{jobs_section}
      </section>
'''

    def _generate_ausbildung(self, section: Dict) -> str:
        """Generate Ausbildung section"""
        education_items = []

        if section['subsections']:
            # Has subsections (### University)
            for edu in section['subsections']:
                # Get degree and period from content
                degree = ''
                period = ''
                for line in edu.get('content', []):
                    if 'Bachelor' in line or 'Master' in line or 'B.Sc' in line or 'M.Sc' in line:
                        degree = line
                    elif '–' in line or '-' in line:
                        period = line

                edu_html = f'''        <div>
          <p class="text-sm font-medium">{edu['title']}</p>
          <p class="text-xs text-gray-700">{degree}</p>
          <p class="text-xs text-gray-500">{period}</p>
        </div>'''
                education_items.append(edu_html)
        else:
            # No subsections - content directly in section
            uni = ''
            degree = ''
            period = ''

            for item in section['content']:
                if item['type'] == 'text':
                    text = item['text']
                    # Check if it's bold (university name)
                    if text.startswith('**') and text.endswith('**'):
                        uni = text.strip('*').strip()
                    # Check if it's italic (period)
                    elif text.startswith('*') and text.endswith('*'):
                        period = text.strip('*').strip()
                    # Check if it's degree
                    elif 'Bachelor' in text or 'Master' in text or 'B.Sc' in text or 'M.Sc' in text:
                        degree = text

            if uni:
                edu_html = f'''        <div>
          <p class="text-sm font-medium">{uni}</p>
          <p class="text-xs text-gray-700">{degree}</p>
          <p class="text-xs text-gray-500">{period}</p>
        </div>'''
                education_items.append(edu_html)

        education_html = '\n'.join(education_items)

        return f'''      <!-- Ausbildung -->
      <section class="mb-14">
        <h2 class="text-xs uppercase tracking-wider text-gray-500 mb-4 font-medium">{section['title']}</h2>
{education_html}
      </section>
'''

    def _generate_schwerpunkte(self, section: Dict) -> str:
        """Generate Schwerpunkte section with intro paragraph and cards"""
        # Intro paragraph
        intro_paragraphs = [item['text'] for item in section['content'] if item['type'] == 'text']
        intro_html = '\n        '.join([f'<p class="text-sm text-gray-700 mb-6 leading-relaxed">\n          {p}\n        </p>' for p in intro_paragraphs[:1]])

        # Cards from subsections (except "Methoden")
        cards_html = []
        methoden_html = ''

        for subsection in section['subsections']:
            if 'Methoden' in subsection['title']:
                # Generate pills for methods
                pills = []
                for item in subsection.get('bullets', []):
                    pills.append(f'          <span class="px-3 py-1 bg-white border border-gray-300 rounded-full text-xs text-gray-700">{item}</span>')

                pills_html = '\n'.join(pills)
                methoden_html = f'''      <div class="pt-4 border-t border-gray-200">
        <p class="text-xs text-gray-500 mb-3">{subsection['title']}</p>
        <div class="flex flex-wrap gap-2">
{pills_html}
        </div>
      </div>'''
            else:
                # Regular card
                description = ' '.join([item if isinstance(item, str) else '' for item in subsection.get('content', [])])
                card_html = f'''        <div class="bg-gray-50 p-4 rounded border border-gray-200">
          <h3 class="text-sm font-medium mb-1.5">{subsection['title']}</h3>
          <p class="text-xs text-gray-700 leading-relaxed">{description}</p>
        </div>'''
                cards_html.append(card_html)

        cards_section = '\n'.join(cards_html)

        return f'''      <!-- Schwerpunkte -->
      <section class="mb-14">
        <h2 class="text-xs uppercase tracking-wider text-gray-500 mb-4 font-medium">{section['title']}</h2>
        {intro_html}
        <div class="grid grid-cols-2 gap-4 mb-6">
{cards_section}
        </div>
{methoden_html}
      </section>
'''

    def _generate_haltung(self, section: Dict) -> str:
        """Generate Haltung section with intro paragraph and cards"""
        # Intro paragraph
        intro_paragraphs = [item['text'] for item in section['content'] if item['type'] == 'text']
        intro_html = '\n        '.join([f'<p class="text-sm text-gray-700 mb-6 leading-relaxed">\n          {p}\n        </p>' for p in intro_paragraphs[:1]])

        # Cards from subsections
        cards_html = []
        for subsection in section['subsections']:
            description = ' '.join([item if isinstance(item, str) else '' for item in subsection.get('content', [])])
            card_html = f'''        <div class="bg-gray-50 p-4 rounded border border-gray-200">
          <h4 class="text-sm font-medium mb-1.5">{subsection['title']}</h4>
          <p class="text-xs text-gray-700 leading-relaxed">{description}</p>
        </div>'''
            cards_html.append(card_html)

        cards_section = '\n'.join(cards_html)

        return f'''      <!-- Haltung -->
      <section class="mb-14">
        <h2 class="text-xs uppercase tracking-wider text-gray-500 mb-4 font-medium">{section['title']}</h2>
        {intro_html}
        <div class="grid grid-cols-2 gap-4">
{cards_section}
        </div>
      </section>
'''

    def _generate_sprachen(self, section: Dict) -> str:
        """Generate Sprachen section as simple text with · separator"""
        # Collect all bullet points
        languages = []
        for item in section['content']:
            if item['type'] == 'bullet':
                languages.append(item['text'])

        languages_text = ' · '.join(languages)

        return f'''      <!-- Sprachen -->
      <section>
        <h2 class="text-xs uppercase tracking-wider text-gray-500 mb-4 font-medium">{section['title']}</h2>
        <p class="text-sm text-gray-700">{languages_text}</p>
      </section>
'''

    def _generate_generic(self, section: Dict) -> str:
        """Generate generic section"""
        content_html = []
        for item in section['content']:
            if item['type'] == 'text':
                content_html.append(f'        <p class="text-sm text-gray-700 mb-3">{item["text"]}</p>')
            elif item['type'] == 'bullet':
                content_html.append(f'        <li class="text-sm text-gray-700">• {item["text"]}</li>')

        content_section = '\n'.join(content_html)

        return f'''      <!-- {section['title']} -->
      <section class="mb-14">
        <h2 class="text-xs uppercase tracking-wider text-gray-500 mb-4 font-medium">{section['title']}</h2>
{content_section}
      </section>
'''


def main():
    """Main entry point"""
    if len(sys.argv) < 2:
        print("Usage: python3 generate-html.py <markdown> [-o OUTPUT] [-p PHOTO] [-l LANG]")
        sys.exit(1)

    # Parse arguments
    markdown_file = sys.argv[1]
    output_file = 'index.html'
    photo_file = 'Jan_Hoelter_Foto.jpeg'
    lang = 'de'

    i = 2
    while i < len(sys.argv):
        if sys.argv[i] == '-o' and i+1 < len(sys.argv):
            output_file = sys.argv[i+1]
            i += 2
        elif sys.argv[i] == '-p' and i+1 < len(sys.argv):
            photo_file = sys.argv[i+1]
            i += 2
        elif sys.argv[i] == '-l' and i+1 < len(sys.argv):
            lang = sys.argv[i+1]
            i += 2
        else:
            i += 1

    # Parse and generate
    parser = CVParser(markdown_file)
    generator = HTMLGenerator(parser.data, photo_file, lang)
    html = generator.generate()

    # Write output
    Path(output_file).write_text(html, encoding='utf-8')
    print(f"✓ Generated: {output_file}")


if __name__ == '__main__':
    main()
