#!/usr/bin/env python3
"""
CV HTML Generator
Generates HTML CV from structured markdown using Zinc-Teal Brand Kit (Geist fonts)
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
        self._validate(data)
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
                    subtitle = line[4:].strip().strip('*').strip()
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
                    if 'period' in current_subsection and 'bullets' not in current_subsection:
                        if 'description' not in current_subsection:
                            current_subsection['description'] = []
                        current_subsection['description'].append(line)
                    elif 'bullets' not in current_subsection and 'period' not in current_subsection:
                        current_subsection['content'].append(line)
                elif current_section:
                    current_section['content'].append({'type': 'text', 'text': line})

            i += 1

        if current_section:
            sections.append(current_section)

        return sections

    def _validate(self, data: Dict) -> None:
        """Warn about likely markdown format issues (writes to stderr, never stops generation)"""
        for section in data['sections']:
            if section['type'] == 'berufserfahrung':
                for sub in section['subsections']:
                    if not sub.get('job_title'):
                        print(f"⚠  Kein Jobtitel in Station: {sub['title']}", file=sys.stderr)
                    if not sub.get('period'):
                        print(f"⚠  Kein Zeitraum in Station: {sub['title']}", file=sys.stderr)
            elif section['type'] == 'ausbildung':
                for sub in section['subsections']:
                    has_period = sub.get('period') or any(
                        '–' in l or re.match(r'\d{4}', l)
                        for l in sub.get('content', [])
                    )
                    if not has_period:
                        print(f"⚠  Kein Zeitraum in Ausbildung: {sub['title']}", file=sys.stderr)

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


# SVG icon strings for contact badges
_SVG_LOCATION = (
    '<svg class="text-teal-400" xmlns="http://www.w3.org/2000/svg" viewBox="0 0 24 24" width="14" height="14" fill="currentColor">'
    '<path d="M12 23.7279L5.63604 17.364C2.12132 13.8492 2.12132 8.15076 5.63604 4.63604C9.15076 1.12132 14.8492 1.12132 18.364 4.63604'
    'C21.8787 8.15076 21.8787 13.8492 18.364 17.364L12 23.7279ZM16.9497 15.9497C19.6834 13.2161 19.6834 8.78392 16.9497 6.05025'
    'C14.2161 3.31658 9.78392 3.31658 7.05025 6.05025C4.31658 8.78392 4.31658 13.2161 7.05025 15.9497L12 20.8995L16.9497 15.9497Z'
    'M12 13C10.8954 13 10 12.1046 10 11C10 9.89543 10.8954 9 12 9C13.1046 9 14 9.89543 14 11C14 12.1046 13.1046 13 12 13Z"></path>'
    '</svg>'
)
_SVG_EMAIL = (
    '<svg class="text-teal-400" xmlns="http://www.w3.org/2000/svg" viewBox="0 0 24 24" width="14" height="14" fill="currentColor">'
    '<path d="M3 3H21C21.5523 3 22 3.44772 22 4V20C22 20.5523 21.5523 21 21 21H3C2.44772 21 2 20.5523 2 20V4C2 3.44772 2.44772 3 3 3Z'
    'M20 7.23792L12.0718 14.338L4 7.21594V19H20V7.23792ZM4.51146 5L12.0619 11.662L19.501 5H4.51146Z"></path>'
    '</svg>'
)
_SVG_PHONE = (
    '<svg class="text-teal-400" xmlns="http://www.w3.org/2000/svg" viewBox="0 0 24 24" width="14" height="14" fill="currentColor">'
    '<path d="M7 4V20H17V4H7ZM6 2H18C18.5523 2 19 2.44772 19 3V21C19 21.5523 18.5523 22 18 22H6C5.44772 22 5 21.5523 5 21V3'
    'C5 2.44772 5.44772 2 6 2ZM12 17C12.5523 17 13 17.4477 13 18C13 18.5523 12.5523 19 12 19C11.4477 19 11 18.5523 11 18'
    'C11 17.4477 11.4477 17 12 17Z"></path>'
    '</svg>'
)
_SVG_LINKEDIN = (
    '<svg class="text-teal-400" xmlns="http://www.w3.org/2000/svg" viewBox="0 0 24 24" width="14" height="14" fill="currentColor">'
    '<path d="M4.00098 3H20.001C20.5533 3 21.001 3.44772 21.001 4V20C21.001 20.5523 20.5533 21 20.001 21H4.00098'
    'C3.44869 21 3.00098 20.5523 3.00098 20V4C3.00098 3.44772 3.44869 3 4.00098 3ZM5.00098 5V19H19.001V5H5.00098Z'
    'M7.50098 9C6.67255 9 6.00098 8.32843 6.00098 7.5C6.00098 6.67157 6.67255 6 7.50098 6C8.3294 6 9.00098 6.67157 9.00098 7.5'
    'C9.00098 8.32843 8.3294 9 7.50098 9ZM6.50098 10H8.50098V17.5H6.50098V10Z'
    'M12.001 10.4295C12.5854 9.86534 13.2665 9.5 14.001 9.5C16.072 9.5 17.501 11.1789 17.501 13.25V17.5H15.501V13.25'
    'C15.501 12.2835 14.7175 11.5 13.751 11.5C12.7845 11.5 12.001 12.2835 12.001 13.25V17.5H10.001V10H12.001V10.4295Z"></path>'
    '</svg>'
)


class HTMLGenerator:
    """Generate HTML from parsed CV data using Zinc-Teal Brand Kit"""

    def __init__(self, data: Dict[str, Any], photo_path: str = 'assets/Jan_Hoelter_Foto.jpeg', lang: str = 'de'):
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
                'link_copied': 'Link copied!',
                'copy_link': 'Copy link',
                'share_email': 'Share via email',
            }
        else:
            return {
                'print': 'Drucken',
                'share': 'Teilen',
                'link_copied': 'Link kopiert!',
                'copy_link': 'Link kopieren',
                'share_email': 'Per E-Mail teilen',
            }

    def _get_timestamp(self) -> str:
        """Get current timestamp for source comment"""
        from datetime import datetime
        return datetime.now().strftime('%Y-%m-%d %H:%M')

    def _html_escape(self, text: str) -> str:
        """Escape HTML special characters"""
        return text.replace('&', '&amp;').replace('<', '&lt;').replace('>', '&gt;')

    def _badge(self, svg: str, text: str, href: str = '') -> str:
        """Render a teal contact badge – linked (href) or plain span"""
        base = 'flex items-center gap-1.5 text-teal-600 py-1 px-3 rounded-md bg-teal-50 border border-teal-100'
        hover = ' hover:text-teal-700 hover:bg-teal-100 no-underline transition-colors duration-200'
        if href:
            return (
                f'              <a href="{href}"\n'
                f'                class="{base}{hover}">\n'
                f'                {svg}\n'
                f'                {text}\n'
                f'              </a>'
            )
        else:
            return (
                f'              <span class="{base}">\n'
                f'                {svg}\n'
                f'                {text}\n'
                f'              </span>'
            )

    def _render_card(self, title: str, description: str) -> str:
        """Render a ref-card (used in Schwerpunkte and Haltung)"""
        return (
            f'          <div class="ref-card no-break">\n'
            f'            <p class="font-medium text-zinc-900 text-[1rem] mb-2">{title}</p>\n'
            f'            <p class="text-zinc-600 text-[0.85rem] print:text-[0.75rem] leading-relaxed">{description}</p>\n'
            f'          </div>'
        )

    def generate(self) -> str:
        """Generate complete HTML"""
        sections_by_group = self._group_sections()
        return self._template(sections_by_group)

    def _group_sections(self) -> Dict[str, List]:
        """Group sections into the three background zones"""
        groups = {'white1': [], 'zinc50': [], 'white2': []}

        for section in self.data['sections']:
            t = section['type']
            if t in ('profil',):
                groups['white1'].append(section)
            elif t in ('berufserfahrung', 'ausbildung'):
                groups['zinc50'].append(section)
            elif t in ('schwerpunkte', 'haltung', 'sprachen', 'generic'):
                groups['white2'].append(section)

        return groups

    def _template(self, sections_by_group: Dict) -> str:
        """Load template.html and replace placeholders with generated content"""
        lang_attr = 'en' if self.lang == 'en' else 'de'
        name = self._html_escape(self.data['header'].get('name', ''))
        title = self._html_escape(self.data['header'].get('title', ''))

        # Generate section HTML for each zone
        white1_html = self._generate_header() + '\n'.join(
            self._generate_section(s) for s in sections_by_group['white1']
        )
        zinc50_html = '\n'.join(
            self._generate_section(s) for s in sections_by_group['zinc50']
        )
        white2_html = '\n'.join(
            self._generate_section(s) for s in sections_by_group['white2']
        )

        # Load template relative to this script
        template_path = Path(__file__).parent / 'template.html'
        html = template_path.read_text(encoding='utf-8')

        replacements = {
            '{{HEAD_TITLE}}':        f'{name} \u2013 {title}',
            '{{GENERATED}}':         self._get_timestamp(),
            '{{PHOTO}}':             self.photo,
            '{{LANG}}':              lang_attr,
            '{{ZONE_WHITE1}}':       white1_html,
            '{{ZONE_ZINC50}}':       zinc50_html,
            '{{ZONE_WHITE2}}':       white2_html,
            '{{PRINT_LABEL}}':       self.labels['print'],
            '{{SHARE_LABEL}}':       self.labels['share'],
            '{{COPY_LINK_LABEL}}':   self.labels['copy_link'],
            '{{SHARE_EMAIL_LABEL}}': self.labels['share_email'],
            '{{LINK_COPIED_LABEL}}': self.labels['link_copied'],
        }

        for placeholder, value in replacements.items():
            html = html.replace(placeholder, value)

        return html


    def _generate_section(self, section: Dict) -> str:
        """Dispatch to correct section generator"""
        t = section['type']
        if t == 'profil':
            return self._generate_profil(section)
        elif t == 'berufserfahrung':
            return self._generate_berufserfahrung(section)
        elif t == 'ausbildung':
            return self._generate_ausbildung(section)
        elif t == 'schwerpunkte':
            return self._generate_schwerpunkte(section)
        elif t == 'haltung':
            return self._generate_haltung(section)
        elif t == 'sprachen':
            return self._generate_sprachen(section)
        else:
            return self._generate_generic(section)

    def _generate_header(self) -> str:
        """Generate header with portrait, name, title and teal contact badges"""
        h = self.data['header']
        contact = h.get('contact', {})
        name = self._html_escape(h.get('name', ''))
        title = self._html_escape(h.get('title', ''))

        # Contact badges
        badges = []

        if 'location' in contact:
            loc = self._html_escape(contact['location'])
            badges.append(self._badge(_SVG_LOCATION, loc))

        if 'email' in contact:
            email = self._html_escape(contact['email'])
            badges.append(self._badge(_SVG_EMAIL, email, href=f'mailto:{email}'))

        if 'phone' in contact:
            phone = self._html_escape(contact['phone'])
            phone_href = phone.replace(' ', '')
            badges.append(self._badge(_SVG_PHONE, phone, href=f'tel:{phone_href}'))

        if 'linkedin' in contact:
            linkedin_url = contact['linkedin']
            if not linkedin_url.startswith('http'):
                linkedin_url = f'https://{linkedin_url}'
            linkedin_url = self._html_escape(linkedin_url)
            badges.append(self._badge(_SVG_LINKEDIN, 'LinkedIn', href=linkedin_url))

        badges_html = '\n'.join(badges)

        return f'''      <!-- Header -->
      <header class="mb-10">
        <div class="flex items-start gap-8">
          <img src="{self.photo}" alt="{name}"
            class="w-[110px] h-[110px] rounded-full object-cover object-top flex-shrink-0 grayscale"
            style="-webkit-print-color-adjust: exact; print-color-adjust: exact;">
          <div class="flex-1">
            <h1 class="text-[1.5em] font-medium text-zinc-900 mb-3 leading-[1.1]">{name}</h1>
            <p class="text-[1rem] text-zinc-700">{title}</p>
            <div class="flex flex-wrap gap-x-2 gap-y-2 text-[0.75rem] mt-6">
{badges_html}
            </div>
          </div>
        </div>
      </header>
'''

    def _generate_profil(self, section: Dict) -> str:
        """Generate Profil: tagline as hero statement, all content paragraphs as body"""
        # Tagline from header = hero statement
        tagline = self.data['header'].get('tagline', '')
        hero_html = ''
        if tagline:
            hero_html = f'      <p class="text-zinc-900 leading-[1.35] text-[1.4em] font-medium">\n        {self._html_escape(tagline)}\n      </p>\n'

        # All profil paragraphs → body (no special treatment for first)
        paragraphs = [item['text'] for item in section['content'] if item['type'] == 'text']
        body_html = ''
        if paragraphs:
            body_items = [f'          <p>{self._html_escape(p)}</p>' for p in paragraphs]
            body_html = '      <div class="text-zinc-700 max-w-[44em] text-[1em] leading-relaxed mt-4 space-y-3">\n' + '\n'.join(body_items) + '\n      </div>\n'

        return f'''      <!-- Profil / Hero -->
      <section class="mb-10">
{hero_html}{body_html}      </section>
'''

    def _generate_berufserfahrung(self, section: Dict) -> str:
        """Generate Berufserfahrung with grid timeline layout"""
        label = self._html_escape(section['title'])
        jobs_html = []

        for job in section['subsections']:
            company = self._html_escape(job['title'])
            job_title = self._html_escape(job.get('job_title', ''))
            period_raw = job.get('period', '')

            # Period may contain "Zeitraum | Ort" → split on |
            period = ''
            location = ''
            if '|' in period_raw:
                parts = period_raw.split('|', 1)
                period = self._html_escape(parts[0].strip())
                location = self._html_escape(parts[1].strip())
            else:
                period = self._html_escape(period_raw)

            # Optional description
            description_html = ''
            if 'description' in job:
                desc = self._html_escape(' '.join(job['description']))
                description_html = f'\n              <p class="mt-2 text-zinc-600 max-w-[44em] leading-relaxed">{desc}</p>'

            # Bullets
            bullets_html = ''
            if 'bullets' in job:
                items = '\n'.join([
                    f'                <li>{self._html_escape(b)}</li>'
                    for b in job['bullets']
                ])
                bullets_html = f'\n              <ul class="mt-2 text-zinc-600 max-w-[44em] list-disc list-outside ml-4 space-y-1 leading-relaxed">\n{items}\n              </ul>'

            # Heading: "Jobtitel, Firma" – ### = Firma, **bold** = Jobtitel
            if job_title and company:
                heading = f'{job_title}, {company}'
            else:
                heading = job_title or company

            location_html = ''
            if location:
                location_html = f'\n              <p class="text-[0.85rem] text-zinc-500 mt-0.5">{location}</p>'

            jobs_html.append(f'''          <div class="grid grid-cols-[9rem_1fr] gap-x-6 no-break">
            <div><span class="text-[0.85rem] text-zinc-500 whitespace-nowrap">{period}</span></div>
            <div>
              <h3 class="font-medium text-zinc-900 text-[1rem]">{heading}</h3>{location_html}{description_html}{bullets_html}
            </div>
          </div>''')

        jobs_section = '\n\n'.join(jobs_html)

        return f'''      <!-- Berufserfahrung -->
      <section class="mb-16">
        <p class="font-mono text-[0.72rem] font-medium uppercase tracking-wider text-zinc-600 mb-8">{label}</p>
        <div class="space-y-10">
{jobs_section}
        </div>
      </section>
'''

    def _generate_ausbildung(self, section: Dict) -> str:
        """Generate Ausbildung section"""
        label = self._html_escape(section['title'])
        items_html = []

        if section['subsections']:
            for edu in section['subsections']:
                uni = self._html_escape(edu['title'])
                degree = ''
                period = ''

                for line in edu.get('content', []):
                    if any(x in line for x in ['Bachelor', 'Master', 'B.Sc', 'M.Sc', 'Diplom']):
                        degree = self._html_escape(line)
                    elif '–' in line or ' - ' in line or re.match(r'\d{4}', line):
                        period = self._html_escape(line)

                # If period is still empty, check for italic period parsed by parser
                if not period and 'period' in edu:
                    period = self._html_escape(edu['period'])

                degree_html = f'\n          <p class="text-zinc-600 text-[0.85rem]">{degree}</p>' if degree else ''
                period_html = f'\n          <p class="text-zinc-500 text-[0.85rem]">{period}</p>' if period else ''

                items_html.append(f'''        <div>
          <p class="font-medium text-zinc-900 text-[1rem]">{uni}</p>{degree_html}{period_html}
        </div>''')
        else:
            # Flat content fallback
            uni = ''
            degree = ''
            period = ''
            for item in section['content']:
                text = item['text']
                if text.startswith('**') and text.endswith('**'):
                    uni = self._html_escape(text.strip('*').strip())
                elif text.startswith('*') and text.endswith('*'):
                    period = self._html_escape(text.strip('*').strip())
                elif any(x in text for x in ['Bachelor', 'Master', 'B.Sc', 'M.Sc', 'Diplom']):
                    degree = self._html_escape(text)

            if uni:
                degree_html = f'\n          <p class="text-zinc-600 text-[0.85rem]">{degree}</p>' if degree else ''
                period_html = f'\n          <p class="text-zinc-500 text-[0.85rem]">{period}</p>' if period else ''
                items_html.append(f'''        <div>
          <p class="font-medium text-zinc-900 text-[1rem]">{uni}</p>{degree_html}{period_html}
        </div>''')

        education_html = '\n'.join(items_html)

        return f'''      <!-- Ausbildung -->
      <section class="mb-16 no-break">
        <p class="font-mono text-[0.72rem] font-medium uppercase tracking-wider text-zinc-600 mb-8">{label}</p>
{education_html}
      </section>
'''

    def _generate_schwerpunkte(self, section: Dict) -> str:
        """Generate Schwerpunkte with hero intro, ref-card grid, ref-tag pills"""
        label = self._html_escape(section['title'])

        # Intro paragraph(s)
        intro_paragraphs = [item['text'] for item in section['content'] if item['type'] == 'text']
        hero_html = ''
        if intro_paragraphs:
            hero = self._html_escape(intro_paragraphs[0])
            hero_html = f'        <p class="text-zinc-900 leading-[1.35] mb-10 text-[1.4em] font-medium">\n          {hero}\n        </p>\n'

        # Cards and Methoden
        cards_html = []
        methoden_html = ''

        for sub in section['subsections']:
            if 'Methoden' in sub['title'] or 'Methods' in sub['title']:
                # Pills
                pills = []
                for b in sub.get('bullets', []):
                    escaped_b = self._html_escape(b)
                    pills.append(f'            <span class="ref-tag">{escaped_b}</span>')
                pills_html = '\n'.join(pills)
                methoden_title = self._html_escape(sub['title'])
                methoden_html = f'''        <div class="no-break">
          <p class="font-medium text-zinc-900 text-[1rem] mb-3">{methoden_title}</p>
          <div class="flex flex-wrap gap-2">
{pills_html}
          </div>
        </div>'''
            else:
                sub_title = self._html_escape(sub['title'])
                description = self._html_escape(' '.join(sub.get('content', [])))
                cards_html.append(self._render_card(sub_title, description))

        cards_section = '\n'.join(cards_html)
        grid_html = f'        <div class="grid grid-cols-1 sm:grid-cols-2 gap-4 mb-10">\n{cards_section}\n        </div>\n' if cards_html else ''

        return f'''      <!-- Schwerpunkte -->
      <section class="mb-16">
        <p class="font-mono text-[0.72rem] font-medium uppercase tracking-wider text-zinc-600 mb-8">{label}</p>
{hero_html}{grid_html}{methoden_html}
      </section>
'''

    def _generate_haltung(self, section: Dict) -> str:
        """Generate Haltung with page-break label, hero intro, ref-card 2x2 grid"""
        label = self._html_escape(section['title'])

        # Intro paragraph(s)
        intro_paragraphs = [item['text'] for item in section['content'] if item['type'] == 'text']
        hero_html = ''
        if intro_paragraphs:
            hero = self._html_escape(intro_paragraphs[0])
            hero_html = f'        <p class="text-zinc-900 leading-[1.35] mb-10 text-[1.4em] font-medium">\n          {hero}\n        </p>\n'

        # Cards
        cards_html = []
        for sub in section['subsections']:
            sub_title = self._html_escape(sub['title'])
            description = self._html_escape(' '.join(sub.get('content', [])))
            cards_html.append(self._render_card(sub_title, description))

        cards_section = '\n'.join(cards_html)

        return f'''      <!-- Haltung -->
      <section class="mb-16">
        <p class="font-mono text-[0.72rem] font-medium uppercase tracking-wider text-zinc-600 mb-4 page-break">{label}</p>
{hero_html}        <div class="grid grid-cols-1 sm:grid-cols-2 gap-4">
{cards_section}
        </div>
      </section>
'''

    def _generate_sprachen(self, section: Dict) -> str:
        """Generate Sprachen as simple text with · separator"""
        label = self._html_escape(section['title'])
        languages = [item['text'] for item in section['content'] if item['type'] == 'bullet']
        languages_text = ' · '.join(self._html_escape(l) for l in languages)

        return f'''      <!-- Sprachen -->
      <section class="no-break">
        <p class="font-mono text-[0.72rem] font-medium uppercase tracking-wider text-zinc-600 mb-4">{label}</p>
        <p class="text-zinc-600 text-[0.85rem]">{languages_text}</p>
      </section>
'''

    def _generate_generic(self, section: Dict) -> str:
        """Generate generic section"""
        label = self._html_escape(section['title'])
        content_html = []
        for item in section['content']:
            if item['type'] == 'text':
                content_html.append(f'        <p class="text-zinc-700 text-[0.95rem] mb-3">{self._html_escape(item["text"])}</p>')
            elif item['type'] == 'bullet':
                content_html.append(f'        <li class="text-zinc-700 text-[0.95rem]">• {self._html_escape(item["text"])}</li>')

        content_section = '\n'.join(content_html)

        return f'''      <!-- {label} -->
      <section class="mb-14">
        <p class="font-mono text-[0.72rem] font-medium uppercase tracking-wider text-zinc-600 mb-8">{label}</p>
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
    photo_file = 'assets/Jan_Hoelter_Foto.jpeg'
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
