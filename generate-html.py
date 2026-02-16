#!/usr/bin/env python3
"""
CV HTML Generator
Converts markdown CV to minimalist HTML using Tailwind CSS
Supports German/English variants
"""

import re
import sys
from pathlib import Path
from typing import Dict, List, Tuple

class CVParser:
    """Parse structured markdown CV into data model"""

    def __init__(self, markdown_path: str):
        self.markdown_path = Path(markdown_path)
        self.content = self.markdown_path.read_text(encoding='utf-8')

    def parse(self) -> Dict:
        """Parse markdown into structured data"""
        lines = self.content.split('\n')
        cv_data = {
            'header': {},
            'sections': []
        }

        i = 0
        # Parse Header (first ~10 lines)
        cv_data['header'] = self._parse_header(lines[:15])

        # Find first section (##)
        while i < len(lines) and not lines[i].startswith('## '):
            i += 1

        # Parse sections
        current_section = None
        current_subsection = None

        while i < len(lines):
            line = lines[i].strip()

            if line.startswith('## '):
                # New section
                if current_section:
                    cv_data['sections'].append(current_section)
                current_section = {
                    'title': line[3:].strip(),
                    'content': [],
                    'subsections': []
                }
                current_subsection = None

            elif line.startswith('### '):
                # Subsection or job
                subsection_title = line[4:].strip()
                current_subsection = {
                    'title': subsection_title,
                    'content': [],
                    'items': []
                }
                current_section['subsections'].append(current_subsection)

            elif line.startswith('**') and current_subsection and 'title' in current_subsection:
                # Job title or metadata
                current_subsection['content'].append(line)

            elif line.startswith('*') and current_subsection:
                # Period/Location
                current_subsection['content'].append(line)

            elif line.startswith('- '):
                # Bullet point
                bullet_text = line[2:].strip()
                if current_subsection:
                    current_subsection['items'].append(bullet_text)
                else:
                    current_section['content'].append(line)

            elif line.startswith('---'):
                # Separator - ignore
                pass

            elif line and current_section:
                # Regular paragraph
                if current_subsection:
                    current_subsection['content'].append(line)
                else:
                    current_section['content'].append(line)

            i += 1

        # Append last section
        if current_section:
            cv_data['sections'].append(current_section)

        return cv_data

    def _parse_header(self, lines: List[str]) -> Dict:
        """Parse header section"""
        header = {
            'name': '',
            'title': '',
            'tagline': '',
            'location': '',
            'email': '',
            'phone': '',
            'linkedin': ''
        }

        for line in lines:
            line = line.strip()
            if line.startswith('# '):
                header['name'] = line[2:].strip()
            elif line.startswith('**') and line.endswith('**'):
                header['title'] = line.strip('*').strip()
            elif line.startswith('*') and not line.startswith('**'):
                header['tagline'] = line.strip('*').strip()
            elif '📧' in line:
                header['email'] = line.split('📧')[1].strip()
            elif '📞' in line or '📱' in line:
                header['phone'] = re.sub(r'[📞📱]', '', line).strip()
            elif '🔗' in line:
                header['linkedin'] = line.split('🔗')[1].strip()
            elif line and not line.startswith('#') and not line.startswith('*'):
                if not header['location']:
                    header['location'] = line

        return header


class HTMLGenerator:
    """Generate HTML from parsed CV data"""

    def __init__(self, cv_data: Dict, photo_path: str = None, lang: str = 'de'):
        self.cv_data = cv_data
        self.photo_path = photo_path or 'Jan_Hoelter_Foto.jpeg'
        self.lang = lang

    def generate(self) -> str:
        """Generate complete HTML document"""

        sections_html = []
        for section in self.cv_data['sections']:
            section_html = self._generate_section(section)
            if section_html:
                sections_html.append(section_html)

        return self._template(
            header_html=self._generate_header(),
            sections_html='\n\n'.join(sections_html)
        )

    def _generate_header(self) -> str:
        """Generate header HTML"""
        h = self.cv_data['header']

        return f'''      <!-- Header Section -->
      <header class="mb-16">
        <div class="flex justify-between items-start gap-12 mb-6">
          <div class="flex-1">
            <h1 class="text-4xl font-light tracking-tight text-gray-900 mb-2">{h['name']}</h1>
            <p class="text-sm text-gray-600 font-medium mb-2">{h['title']}</p>
            <p class="text-xs text-gray-500 italic">{h['tagline']}</p>
          </div>
          <img src="{self.photo_path}" alt="{h['name']}" class="w-28 h-28 rounded-full object-cover object-top grayscale">
        </div>

        <div class="flex flex-wrap gap-x-6 gap-y-1 text-xs text-gray-600">
          <span class="flex items-center gap-1.5">
            <svg class="w-3.5 h-3.5" fill="none" stroke="currentColor" viewBox="0 0 24 24">
              <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M17.657 16.657L13.414 20.9a1.998 1.998 0 01-2.827 0l-4.244-4.243a8 8 0 1111.314 0z"/>
              <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M15 11a3 3 0 11-6 0 3 3 0 016 0z"/>
            </svg>
            {h['location']}
          </span>
          <span class="flex items-center gap-1.5">
            <svg class="w-3.5 h-3.5" fill="none" stroke="currentColor" viewBox="0 0 24 24">
              <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M3 8l7.89 5.26a2 2 0 002.22 0L21 8M5 19h14a2 2 0 002-2V7a2 2 0 00-2-2H5a2 2 0 00-2 2v10a2 2 0 002 2z"/>
            </svg>
            {h['email']}
          </span>
          <span class="flex items-center gap-1.5">
            <svg class="w-3.5 h-3.5" fill="none" stroke="currentColor" viewBox="0 0 24 24">
              <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M3 5a2 2 0 012-2h3.28a1 1 0 01.948.684l1.498 4.493a1 1 0 01-.502 1.21l-2.257 1.13a11.042 11.042 0 005.516 5.516l1.13-2.257a1 1 0 011.21-.502l4.493 1.498a1 1 0 01.684.949V19a2 2 0 01-2 2h-1C9.716 21 3 14.284 3 6V5z"/>
            </svg>
            {h['phone']}
          </span>
          <span class="flex items-center gap-1.5">
            <svg class="w-3.5 h-3.5" fill="currentColor" viewBox="0 0 24 24">
              <path d="M19 0h-14c-2.761 0-5 2.239-5 5v14c0 2.761 2.239 5 5 5h14c2.762 0 5-2.239 5-5v-14c0-2.761-2.238-5-5-5zm-11 19h-3v-11h3v11zm-1.5-12.268c-.966 0-1.75-.79-1.75-1.764s.784-1.764 1.75-1.764 1.75.79 1.75 1.764-.783 1.764-1.75 1.764zm13.5 12.268h-3v-5.604c0-3.368-4-3.113-4 0v5.604h-3v-11h3v1.765c1.396-2.586 7-2.777 7 2.476v6.759z"/>
            </svg>
            <a href="{h['linkedin']}" class="hover:underline hover:text-gray-900">LinkedIn</a>
          </span>
        </div>
      </header>'''

    def _generate_section(self, section: Dict) -> str:
        """Generate section HTML based on title"""
        title = section['title']

        if title == 'Profil' or title == 'Profile':
            return self._generate_profil(section)
        elif title == 'Berufserfahrung' or title == 'Professional Experience':
            return self._generate_berufserfahrung(section)
        elif title == 'Ausbildung' or title == 'Education':
            return self._generate_ausbildung(section)
        elif title == 'Schwerpunkte' or title == 'Core Competencies':
            return self._generate_schwerpunkte(section)
        elif title == 'Haltung' or title == 'Principles':
            return self._generate_haltung(section)
        elif title == 'Sprachen' or title == 'Languages':
            return self._generate_sprachen(section)
        else:
            return self._generate_generic_section(section)

    def _generate_profil(self, section: Dict) -> str:
        """Generate profile section"""
        paragraphs = '\n          '.join([f'<p>{p}</p>' for p in section['content'] if p])

        return f'''      <!-- Profil Section -->
      <section class="mb-12">
        <h2 class="text-xl font-medium text-gray-900 mb-4 pb-2 border-b border-gray-200">{section['title']}</h2>
        <div class="text-xs text-gray-700 space-y-3 leading-relaxed">
          {paragraphs}
        </div>
      </section>'''

    def _generate_berufserfahrung(self, section: Dict) -> str:
        """Generate experience section"""
        jobs_html = []

        for subsection in section['subsections']:
            company = subsection['title'].strip('*').strip()  # Remove ** from company name

            # Parse job details from content
            job_title = ''
            period_location = ''
            description = []

            for content_line in subsection['content']:
                if content_line.startswith('**') and not company in content_line:
                    job_title = content_line.strip('*').strip()
                elif content_line.startswith('*'):
                    period_location = content_line.strip('*').strip()
                elif content_line and not content_line.startswith('**'):
                    description.append(content_line)

            # Build bullets
            bullets_html = '\n              '.join([f'<li>• {item}</li>' for item in subsection['items']])

            description_html = ''
            if description:
                description_html = f'\n            <p class="text-xs text-gray-600 mb-3">{" ".join(description)}</p>'

            job_html = f'''        <div class="mb-10">
          <h3 class="text-base font-semibold text-gray-900 mb-3">{company}</h3>
          <div class="mb-2">
            <p class="text-sm font-medium text-gray-800">{job_title}</p>
            <p class="text-xs text-gray-500 italic">{period_location}</p>
          </div>{description_html}
          <ul class="text-xs text-gray-700 space-y-1.5 ml-4">
              {bullets_html}
          </ul>
        </div>'''

            jobs_html.append(job_html)

        return f'''      <!-- Berufserfahrung Section -->
      <section class="mb-12">
        <h2 class="text-xl font-medium text-gray-900 mb-4 pb-2 border-b border-gray-200">{section['title']}</h2>
{chr(10).join(jobs_html)}
      </section>'''

    def _generate_ausbildung(self, section: Dict) -> str:
        """Generate education section"""
        items_html = []

        # Check if content is in subsections or directly in section
        if section['subsections']:
            # Has subsections (###)
            for subsection in section['subsections']:
                uni = subsection['title']
                degree = ''
                period = ''

                for content_line in subsection['content']:
                    if 'Bachelor' in content_line or 'Master' in content_line:
                        degree = content_line
                    elif content_line.startswith('*'):
                        period = content_line.strip('*').strip()

                item_html = f'''        <div class="mb-2">
          <p class="font-semibold text-gray-900">{uni}</p>
          <p class="text-gray-700">{degree}</p>
          <p class="text-sm text-gray-600 italic">{period}</p>
        </div>'''
                items_html.append(item_html)
        else:
            # Content directly in section (no ###)
            uni = ''
            degree = ''
            period = ''

            for line in section['content']:
                if line.startswith('**') and line.endswith('**'):
                    uni = line.strip('*').strip()
                elif 'Bachelor' in line or 'Master' in line or 'B.Sc.' in line or 'M.Sc.' in line:
                    degree = line.strip()
                elif line.startswith('*'):
                    period = line.strip('*').strip()

            if uni:
                item_html = f'''        <div class="mb-2">
          <p class="font-semibold text-gray-900">{uni}</p>
          <p class="text-gray-700">{degree}</p>
          <p class="text-sm text-gray-600 italic">{period}</p>
        </div>'''
                items_html.append(item_html)

        return f'''      <!-- Ausbildung Section -->
      <section class="mb-12">
        <h2 class="text-xl font-medium text-gray-900 mb-4 pb-2 border-b border-gray-200">{section['title']}</h2>
{chr(10).join(items_html)}
      </section>'''

    def _generate_schwerpunkte(self, section: Dict) -> str:
        """Generate core competencies with cards and pills"""
        cards_html = []
        methoden_items = []

        for subsection in section['subsections']:
            title = subsection['title']

            # Check if this is "Methoden" subsection
            if 'Methoden' in title or 'Methods' in title:
                methoden_items = subsection['items']
            else:
                # Regular card
                description = ' '.join(subsection['content'])
                card_html = f'''          <div class="bg-gray-50 p-4 rounded border border-gray-200">
            <h3 class="text-sm font-medium text-gray-900 mb-1.5">{title}</h3>
            <p class="text-xs text-gray-700 leading-relaxed">{description}</p>
          </div>'''
                cards_html.append(card_html)

        # Build methoden pills
        methoden_html = ''
        if methoden_items:
            pills = '\n            '.join([f'<span class="px-3 py-1 bg-white border border-gray-300 rounded-full text-xs text-gray-700 whitespace-nowrap">{item}</span>' for item in methoden_items])

            methoden_title = 'Methoden & Arbeitsweisen' if self.lang == 'de' else 'Methods & Practices'
            methoden_html = f'''
        <div class="mt-6 pt-4 border-t border-gray-200">
          <p class="text-xs text-gray-500 mb-3">{methoden_title}</p>
          <div class="flex flex-wrap gap-2">
            {pills}
          </div>
        </div>'''

        return f'''      <!-- Schwerpunkte Section -->
      <section class="mb-12">
        <h2 class="text-xl font-medium text-gray-900 mb-4 pb-2 border-b border-gray-200">{section['title']}</h2>
        <div class="grid grid-cols-2 gap-4">
{chr(10).join(cards_html)}
        </div>{methoden_html}
      </section>'''

    def _generate_haltung(self, section: Dict) -> str:
        """Generate principles with cards"""
        cards_html = []

        for subsection in section['subsections']:
            title = subsection['title']
            description = ' '.join(subsection['content'])

            card_html = f'''          <div class="bg-gray-50 p-4 rounded border border-gray-200">
            <h4 class="text-sm font-medium text-gray-900 mb-1.5">{title}</h4>
            <p class="text-xs text-gray-700 leading-relaxed">{description}</p>
          </div>'''
            cards_html.append(card_html)

        return f'''      <!-- Haltung Section -->
      <section class="mb-12">
        <h2 class="text-xl font-medium text-gray-900 mb-4 pb-2 border-b border-gray-200">{section['title']}</h2>
        <div class="grid grid-cols-2 gap-4">
{chr(10).join(cards_html)}
        </div>
      </section>'''

    def _generate_sprachen(self, section: Dict) -> str:
        """Generate languages section"""
        items_html = '\n          '.join([f'<li>{item[2:]}</li>' for item in section['content'] if item.startswith('- ')])

        # If no items in content, check subsections
        if not items_html:
            for subsection in section['subsections']:
                items_html += '\n          '.join([f'<li>{item}</li>' for item in subsection['items']])

        return f'''      <!-- Sprachen Section -->
      <section class="mb-12">
        <h2 class="text-xl font-medium text-gray-900 mb-4 pb-2 border-b border-gray-200">{section['title']}</h2>
        <ul class="text-xs text-gray-700 space-y-1">
          {items_html}
        </ul>
      </section>'''

    def _generate_generic_section(self, section: Dict) -> str:
        """Generate generic section for unknown types"""
        content_html = '\n          '.join([f'<p>{p}</p>' for p in section['content'] if p])

        return f'''      <!-- {section['title']} Section -->
      <section class="mb-12">
        <h2 class="text-xl font-medium text-gray-900 mb-4 pb-2 border-b border-gray-200">{section['title']}</h2>
        <div class="text-xs text-gray-700 space-y-2">
          {content_html}
        </div>
      </section>'''

    def _template(self, header_html: str, sections_html: str) -> str:
        """HTML document template"""

        title = 'Lebenslauf' if self.lang == 'de' else 'CV'
        print_btn = 'Drucken' if self.lang == 'de' else 'Print'
        share_btn = 'Teilen' if self.lang == 'de' else 'Share'
        link_copied = 'Link kopiert!' if self.lang == 'de' else 'Link copied!'

        return f'''<!DOCTYPE html>
<html lang="{self.lang}">
<head>
  <meta charset="UTF-8">
  <meta name="viewport" content="width=device-width, initial-scale=1.0">
  <title>{title} – {self.cv_data['header']['name']}</title>
  <script src="https://cdn.tailwindcss.com"></script>
  <style>
    @import url('https://fonts.googleapis.com/css2?family=Inter:wght@300;400;500;600;700&display=swap');

    @page {{
      size: A4;
      margin: 16mm 18mm;
    }}

    @media print {{
      body {{
        -webkit-print-color-adjust: exact;
        print-color-adjust: exact;
      }}
      .page-break {{ page-break-before: always; }}
      .no-break {{ break-inside: avoid; }}
      .no-print {{ display: none !important; }}
    }}

    body {{
      font-family: 'Inter', system-ui, -apple-system, sans-serif;
    }}
  </style>
</head>

<body class="font-sans text-gray-800 bg-gray-50">

  <!-- Action Bar -->
  <div class="no-print fixed top-4 right-4 flex gap-2 z-50">
    <button onclick="window.print()"
      class="bg-white px-3 py-2 border border-gray-200 rounded-lg text-gray-600 hover:text-gray-800 hover:border-gray-400 transition-colors shadow-sm flex items-center gap-2">
      <svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 24 24" width="18" height="18" fill="currentColor">
        <path d="M17 2C17.5523 2 18 2.44772 18 3V7H21C21.5523 7 22 7.44772 22 8V18C22 18.5523 21.5523 19 21 19H18V21C18 21.5523 17.5523 22 17 22H7C6.44772 22 6 21.5523 6 21V19H3C2.44772 19 2 18.5523 2 18V8C2 7.44772 2.44772 7 3 7H6V3C6 2.44772 6.44772 2 7 2H17ZM16 17H8V20H16V17ZM20 9H4V17H6V16C6 15.4477 6.44772 15 7 15H17C17.5523 15 18 15.4477 18 16V17H20V9ZM8 10V12H5V10H8ZM16 4H8V7H16V4Z"></path>
      </svg>
      {print_btn}
    </button>
    <button onclick="if(navigator.share){{navigator.share({{title:'{self.cv_data['header']['name']} - CV',url:window.location.href}})}}else{{navigator.clipboard.writeText(window.location.href);alert('{link_copied}')}}"
      class="bg-white px-3 py-2 border border-gray-200 rounded-lg text-gray-600 hover:text-gray-800 hover:border-gray-400 transition-colors shadow-sm flex items-center gap-2">
      <svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 24 24" width="18" height="18" fill="currentColor">
        <path d="M13.1202 17.0228L8.92129 14.7324C8.19135 15.5125 7.15261 16 6 16C3.79086 16 2 14.2091 2 12C2 9.79086 3.79086 8 6 8C7.15255 8 8.19125 8.48746 8.92118 9.26746L13.1202 6.97713C13.0417 6.66441 13 6.33707 13 6C13 3.79086 14.7909 2 17 2C19.2091 2 21 3.79086 21 6C21 8.20914 19.2091 10 17 10C15.8474 10 14.8087 9.51251 14.0787 8.73246L9.87977 11.0228C9.9583 11.3355 10 11.6629 10 12C10 12.3371 9.95831 12.6644 9.87981 12.9771L14.0788 15.2675C14.8087 14.4875 15.8474 14 17 14C19.2091 14 21 15.7909 21 18C21 20.2091 19.2091 22 17 22C14.7909 22 13 20.2091 13 18C13 17.6629 13.0417 17.3355 13.1202 17.0228ZM6 14C7.10457 14 8 13.1046 8 12C8 10.8954 7.10457 10 6 10C4.89543 10 4 10.8954 4 12C4 13.1046 4.89543 14 6 14ZM17 8C18.1046 8 19 7.10457 19 6C19 4.89543 18.1046 4 17 4C15.8954 4 15 4.89543 15 6C15 7.10457 15.8954 8 17 8ZM17 20C18.1046 20 19 19.1046 19 18C19 16.8954 18.1046 16 17 16C15.8954 16 15 16.8954 15 18C15 19.1046 15.8954 20 17 20Z"></path>
      </svg>
      {share_btn}
    </button>
  </div>

  <!-- CV Container -->
  <div class="max-w-4xl mx-auto my-8 bg-white shadow-lg print:shadow-none">
    <div class="px-12 py-10 print:px-0 print:py-0">

{header_html}

{sections_html}

    </div>
  </div>

</body>
</html>'''


def main():
    """Main entry point"""
    import argparse

    parser = argparse.ArgumentParser(description='Generate HTML CV from Markdown')
    parser.add_argument('markdown', help='Path to markdown CV file')
    parser.add_argument('-o', '--output', default='index.html', help='Output HTML file (default: index.html)')
    parser.add_argument('-p', '--photo', default='Jan_Hoelter_Foto.jpeg', help='Photo file path')
    parser.add_argument('-l', '--lang', choices=['de', 'en'], default='de', help='Language (de or en)')

    args = parser.parse_args()

    # Parse markdown
    parser = CVParser(args.markdown)
    cv_data = parser.parse()

    # Generate HTML
    generator = HTMLGenerator(cv_data, photo_path=args.photo, lang=args.lang)
    html = generator.generate()

    # Write output
    output_path = Path(args.output)
    output_path.write_text(html, encoding='utf-8')

    print(f"✓ Generated {output_path}")
    print(f"  Language: {args.lang}")
    print(f"  Photo: {args.photo}")


if __name__ == '__main__':
    main()
