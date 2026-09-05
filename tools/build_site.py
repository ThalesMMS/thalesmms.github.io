#!/usr/bin/env python3
"""Render committed HTML using Python's standard library. No runtime build needed."""
from html import escape
from pathlib import Path
import json
import re

ROOT = Path(__file__).resolve().parents[1]
DATE = 'September 5, 2026'
EMAIL = 'thalesmmsradio@gmail.com'
CATEGORIES = [
    ('imaging', 'Medical imaging & radiology', 'View images, prepare presentations, and work with radiology information.'),
    ('development', 'Developer tools & libraries', 'Explore repositories and build imaging software with reusable components.'),
    ('learning', 'Learning & simulation', 'Explore computation through interactive models.'),
    ('everyday', 'Writing, audio & utilities', 'Work with text, audio, video, and encrypted files.'),
]
ORDER = ['isis-dicom-viewer', 'dicom-slides', 'scout', 'radref', 'dicom-agent-tools',
         'totalsegmentator-plugin', 'dicom-swift', 'mtk', 'dicom-go', 'codeatlas',
         'the-legend-of-source', 'turing-lab', 'autocomp', 'podcast-intelligence',
         'macpgp', 'video-subtitler']
MARKS = {'isis-dicom-viewer': 'Is', 'dicom-slides': 'Ds', 'scout': 'Sc', 'radref': 'Rr',
         'dicom-agent-tools': 'Da', 'totalsegmentator-plugin': 'Ts', 'dicom-swift': 'Ds',
         'mtk': 'Mtk', 'dicom-go': 'Dg', 'codeatlas': 'Ca', 'the-legend-of-source': 'Ls',
         'turing-lab': 'Tl', 'podcast-intelligence': 'Pi', 'macpgp': 'Pgp', 'video-subtitler': 'Vs'}


def e(text):
    return escape(str(text), quote=True)


def link(url, label, active=False, css=None):
    attrs = (' aria-current="page"' if active else '') + (f' class="{e(css)}"' if css else '')
    return f'<a href="{e(url)}"{attrs}>{e(label)}</a>'


def base(project):
    return f'/apps/{project["slug"]}/'


def document(path, title, description, body, project=None, prose=False):
    if project:
        route = base(project)
        nav = [('/', 'All projects'), (route, project['name']),
               (route + 'support/', 'Support'), (route + 'privacy/', 'Privacy')]
        footer_links = link(route+'support/', project['name']+' support') + '<br>\n' + link(route+'privacy/', 'Privacy policy')
    else:
        nav = [('/', 'Home'), ('/#projects', 'Projects'), ('/#about', 'About'), ('/#contact', 'Contact')]
        footer_links = link('/#projects', 'All projects') + '<br>\n' + link('mailto:'+EMAIL, 'Contact')
    navigation = '\n'.join(link(u, n, u == path) for u, n in nav)
    icon = project.get('icon') if project else None
    if project and project['slug'] == 'autocomp':
        icon = {'src': '/assets/autocomp-icon.png'}
    favicon = icon['src'] if icon else '/assets/site-icon.svg'
    favicon_type = 'image/png' if icon else 'image/svg+xml'
    return f'''<!doctype html>
<html lang="en">
<head>
  <meta charset="utf-8">
  <meta name="viewport" content="width=device-width, initial-scale=1">
  <meta name="description" content="{e(description)}">
  <title>{e(title)}</title>
  <link rel="stylesheet" href="/assets/site.css">
  <link rel="icon" type="{favicon_type}" href="{e(favicon)}">
</head>
<body>
<a class="skip" href="#main">Skip to content</a>
<header>
  <div class="wrap header-row">
    <a class="brand" href="/">ThalesMMS<span aria-hidden="true"> /</span></a>
    <nav aria-label="Main navigation">
{navigation}
    </nav>
  </div>
</header>
<main id="main" tabindex="-1" class="wrap{' prose' if prose else ''}">
{body}
</main>
<footer>
  <div class="wrap">
    <p>Thales Matheus M Santos<br>Apps, libraries, and tools.</p>
    <div>{footer_links}</div>
  </div>
</footer>
</body>
</html>
'''


def section_html(section, index, prefix='section'):
    title = e(section['title'])
    content = '\n'.join(f'<p>{e(p)}</p>' for p in section.get('paragraphs', []))
    if section.get('steps'):
        content += '\n<ol>\n' + '\n'.join(f'<li>{e(step)}</li>' for step in section['steps']) + '\n</ol>'
    return f'<section id="{prefix}-{index}">\n<h2>{title}</h2>\n{content}\n</section>'


def contact(project, support=False):
    detail = ('Include the app or package version, your operating system, the steps to reproduce the problem, '
              'and a sanitized error message. Do not send patient information, private documents or source code, '
              'API keys, passwords, or private keys.') if support else (
              'If you email us, we receive your email address and the information you choose to send to respond '
              'to your request. Please omit patient information, private documents, and credentials.')
    return f'''<section class="note">
<h2>{'Contact support' if support else 'Privacy questions and support'}</h2>
<p>Contact Thales Matheus M Santos about {e(project['name'])} at {link('mailto:'+EMAIL, EMAIL)}.</p>
<p>{detail}</p>
</section>'''


def source_links(project):
    return '\n'.join(link(r['url'], r['label']) for r in project['repositories'])


def artwork(project):
    if project['slug'] == 'autocomp':
        return '<img class="project-icon" src="/assets/autocomp-icon.png" width="512" height="512" alt="">'
    if project.get('icon'):
        icon = project['icon']
        return f'<img class="project-icon" src="{e(icon["src"])}" width="{icon["width"]}" height="{icon["height"]}" alt="">'
    return f'<span class="project-mark" aria-hidden="true">{e(MARKS[project["slug"]])}</span>'


def project_page(project):
    route = base(project)
    features = '\n'.join(f'<section>\n<h2>{e(f["title"])}</h2>\n<p>{e(f["body"])}</p>\n</section>' for f in project['features'])
    repos = source_links(project)
    sources = f'<section class="source-section"><h2>Explore the source</h2><div class="source-links">{repos}</div></section>' if repos else ''
    body = f'''<div class="project-heading">
{artwork(project)}
<p class="eyebrow">{e(project['platform'])}</p>
<h1>{e(project['name'])}</h1>
<p class="lead">{e(project['summary'])}</p>
<p>{e(project['intro'])}</p>
<div class="actions">
{link(route+'support/', 'Setup & support', css='button')}
{link(route+'privacy/', 'Read the privacy policy')}
</div>
</div>
<div class="grid features">{features}</div>
{sources}'''
    return document(route, project['name']+' | ThalesMMS', project['summary'], body, project)


def support_page(project):
    route = base(project)
    sections = '\n'.join(section_html(s, i) for i, s in enumerate(project['support'], 1))
    sources = source_links(project)
    source_section = f'<section><h2>Project documentation</h2><p>Find installation details and release-specific guidance in the public project documentation.</p><div class="source-links">{sources}</div></section>' if sources else ''
    body = f'''{artwork(project) if project.get('icon') else ''}
<p class="eyebrow">{e(project['name'])} / Support</p>
<h1>{e(project['name'])} support</h1>
<p class="lead">Setup, troubleshooting, and a direct contact for help.</p>
{sections}
{source_section}
{contact(project, True)}'''
    return document(route+'support/', project['name']+' support | ThalesMMS', 'Setup guidance and troubleshooting for '+project['name']+'.', body, project, True)


def privacy_page(project):
    route = base(project)
    sections = '\n'.join(section_html(s, i) for i, s in enumerate(project['privacy'], 1))
    body = f'''{artwork(project) if project.get('icon') else ''}
<p class="eyebrow">{e(project['name'])} / Privacy</p>
<h1>{e(project['name'])} privacy policy</h1>
<p class="label">Effective {DATE}</p>
<p class="lead">How {e(project['name'])} handles data, including the services and integrations you choose to use.</p>
{sections}
<section>
<h2>This support website</h2>
<p>This static website does not use analytics scripts, forms, or third-party tracking scripts. GitHub Pages handles requests to the website under its own hosting and privacy practices. Visiting a source repository or contacting another service is subject to that service's policies.</p>
</section>
{contact(project)}
<section>
<h2>Policy updates</h2>
<p>This policy may change when the software's data handling changes. The effective date above identifies this version. Features and integrations can differ by release and platform.</p>
</section>'''
    return document(route+'privacy/', project['name']+' privacy policy | ThalesMMS', 'Data handling, storage, and service integrations for '+project['name']+'.', body, project, True)


def home(projects):
    categories = []
    for slug, name, description in CATEGORIES:
        cards = []
        for p in projects:
            if p['category'] != slug:
                continue
            route = base(p)
            cards.append(f'''<article class="catalog-card">
<div class="card-heading">{artwork(p)}<p class="label">{e(p['platform'])}</p></div>
<h3>{link(route, p['name'])}</h3>
<p>{e(p['summary'])}</p>
<div class="card-links">{link(route, 'Explore')} {link(route+'support/', 'Support')} {link(route+'privacy/', 'Privacy')}</div>
</article>''')
        categories.append(f'''<section id="{slug}" class="catalog-section" aria-labelledby="heading-{slug}">
<div class="section-heading"><h2 id="heading-{slug}">{e(name)}</h2><p>{e(description)}</p></div>
<div class="catalog-grid">{''.join(cards)}</div>
</section>''')
    jumps = '\n'.join(link('/#'+slug, name) for slug, name, _ in CATEGORIES)
    body = f'''<div class="directory-intro">
<p class="eyebrow">By Thales Matheus M Santos</p>
<h1>Software for imaging, learning, and creating.</h1>
<p class="lead">A collection of apps, libraries, and tools. Find out what each project does, how to get help, and how it handles your data.</p>
</div>
<div id="projects" class="directory-start">
<p class="label">16 projects · Presentation, support &amp; privacy</p>
<nav class="category-nav" aria-label="Project categories">{jumps}</nav>
</div>
{''.join(categories)}
<section id="about" class="about-section">
<p class="eyebrow">About the developer</p>
<h2>Clinical experience meets software engineering.</h2>
<p>I'm Thales Matheus M Santos, a physician, radiologist, and computer science undergraduate. My projects explore medical imaging, AI-assisted tools, and software development, alongside apps for learning and everyday work.</p>
</section>
<section id="contact" class="contact-section">
<h2>Get in touch</h2>
<p>For setup and troubleshooting, start with the project's support page. For other questions, email {link('mailto:'+EMAIL, EMAIL)}.</p>
</section>'''
    return document('/', 'Apps & tools by Thales Matheus M Santos', 'Explore imaging software, developer tools, learning apps, and utilities by Thales Matheus M Santos, with individual support and privacy pages.', body)


def write(path, html):
    target = ROOT / (path.lstrip('/')+'index.html' if path.endswith('/') else path.lstrip('/'))
    target.parent.mkdir(parents=True, exist_ok=True)
    target.write_text(html, encoding='utf-8')


def main():
    projects = [json.loads(p.read_text()) for p in sorted((ROOT/'content/apps').glob('*.json'))]
    projects.sort(key=lambda p: ORDER.index(p['slug']))
    for p in projects:
        route = base(p)
        write(route, project_page(p))
        write(route+'support/', support_page(p))
        write(route+'privacy/', privacy_page(p))
    # AutoComp is retained verbatim; only shared page chrome is refreshed.
    autocomp = dict(slug='autocomp',name='AutoComp',category='everyday',platform='Safari extension · macOS',summary='Inline AI autocomplete for Google Docs, connected to the HTTPS endpoint you choose.')
    for suffix in ['', 'support/', 'privacy/']:
        route = base(autocomp)+suffix
        text = (ROOT/route.lstrip('/')/'index.html').read_text()
        body = re.search(r'<main\b[^>]*>(.*?)</main>', text, re.S).group(1).strip()
        title = re.search(r'<title>(.*?)</title>',text).group(1)
        # Existing titles/descriptions are plain text and need entity decoding.
        from html import unescape
        description = re.search(r'<meta name="description" content="([^"]*)">', text).group(1)
        write(route,document(route,unescape(title),unescape(description),body,autocomp,bool(suffix)))
    projects.append(autocomp)
    projects.sort(key=lambda p: ORDER.index(p['slug']))
    write('/',home(projects))
    write('/404.html',document('/404.html','Page not found | ThalesMMS','Return to the ThalesMMS project directory.', '''<p class="eyebrow">404 / Page not found</p>
<h1>This page isn't here.</h1>
<p class="lead">Find the project you need in the directory, including its support and privacy pages.</p>
<div class="actions"><a class="button" href="/">Back to all projects</a><a href="mailto:thalesmmsradio@gmail.com">Contact</a></div>'''))
    print(f'Rendered {len(projects)} project sections and {3*len(projects)+2} HTML pages.')


if __name__ == '__main__':
    main()
