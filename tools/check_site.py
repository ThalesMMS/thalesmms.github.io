#!/usr/bin/env python3
"""Validate the published static tree and source-link boundaries, without dependencies."""
from html.parser import HTMLParser
from pathlib import Path
from urllib.parse import urlsplit, unquote
import json
import re
import sys

ROOT = Path(__file__).resolve().parents[1]
SLUGS = {'autocomp', 'turing-lab', 'isis-dicom-viewer', 'isis-dicom-viewer-macos', 'dicom-slides', 'dicom-swift',
         'mtk', 'dicom-agent-tools', 'totalsegmentator-plugin', 'radref', 'dicom-go',
         'podcast-intelligence', 'codeatlas', 'the-legend-of-source', 'scout', 'macpgp',
         'video-subtitler', 'logisim-evolution-mobile'}
PUBLIC_REPOS = {'Turing-Lab', 'dicom-slides', 'DICOM-Swift', 'MTK', 'dicom-skill',
                'dicom-viewer-mcp-app', 'TotalSegmentator-OsiriX-Horos-Plugin', 'RadRef',
                'dicom-go', 'Podcast-Intelligence', 'MacPGP-app', 'IsiX-DICOM-Viewer-macOS',
                'Logisim-Evolution-Mobile'}
PRIVACY_REFERENCES = {'https://developer.apple.com/app-store/app-privacy-details/'}
CLOSED_SLUGS = {'autocomp','isis-dicom-viewer','codeatlas','the-legend-of-source','scout','video-subtitler'}
VOID = {'area','base','br','col','embed','hr','img','input','link','meta','param','source','track','wbr'}
SECRET_PATTERNS = [r'-----BEGIN (?:RSA |EC |OPENSSH )?PRIVATE KEY-----',
                   r'gh[pousr]_[A-Za-z0-9]{20,}', r'github_pat_[A-Za-z0-9_]{20,}',
                   r'sk-[A-Za-z0-9_-]{20,}', r'AKIA[0-9A-Z]{16}']


class Page(HTMLParser):
    def __init__(self, path):
        super().__init__(convert_charrefs=True)
        self.path, self.stack, self.ids, self.links = path, [], set(), []
        self.h1 = self.main = self.nav = self.title = 0
        self.language = self.viewport = False
        self.headings = []
        self.active_links = []
        self.text = ''

    def handle_starttag(self, tag, attrs):
        a = dict(attrs)
        assert tag not in {'script','form','iframe','object','embed'}, (self.path,tag)
        assert not any(k.startswith('on') for k in a), (self.path,'event handler')
        assert int(a.get('tabindex','0')) <= 0, (self.path,'positive tabindex')
        if tag not in VOID:
            self.stack.append(tag)
        if 'id' in a:
            assert a['id'] not in self.ids, (self.path,'duplicate id',a['id'])
            self.ids.add(a['id'])
        if tag == 'html': self.language = a.get('lang') == 'en'
        if tag == 'meta' and a.get('name') == 'viewport': self.viewport = True
        if tag == 'title': self.title += 1
        if tag == 'main': self.main += 1
        if tag == 'nav':
            self.nav += 1
            assert a.get('aria-label'), (self.path,'unlabelled nav')
        if tag == 'h1': self.h1 += 1
        if re.fullmatch('h[1-6]',tag): self.headings.append(int(tag[1]))
        if tag == 'img':
            assert 'alt' in a and 'width' in a and 'height' in a, (self.path,'image attrs')
        for k in ['href','src']:
            if k in a: self.links.append((tag,k,a[k]))
        if a.get('aria-current') == 'page': self.active_links.append(a['href'])

    def handle_endtag(self, tag):
        assert self.stack and self.stack.pop() == tag, (self.path,'unbalanced tag',tag)

    def handle_data(self, data):
        self.text += data


def main():
    expected = {ROOT/'index.html',ROOT/'404.html'} | {
        ROOT/'apps'/slug/suffix/'index.html' for slug in SLUGS for suffix in ['', 'support','privacy']}
    expected.add(ROOT/'apps/isis-dicom-viewer-macos/data-collection/index.html')
    actual = {ROOT/'index.html',ROOT/'404.html'} | set((ROOT/'apps').rglob('*.html'))
    assert actual == expected, ('route mismatch',actual ^ expected)
    assert (ROOT/'.nojekyll').exists()
    pages = {}
    for path in sorted(actual):
        p = Page(path.relative_to(ROOT)); p.feed(path.read_text()); p.close()
        assert not p.stack and p.h1 == p.main == p.title == 1, (p.path,'structure')
        assert p.language and p.viewport and p.nav, (p.path,'document metadata')
        assert 'main' in p.ids, (p.path,'skip target')
        assert not any(b > a+1 for a,b in zip(p.headings,p.headings[1:])), (p.path,'heading jump')
        if '/apps/' in str(path):
            route = '/'+str(path.relative_to(ROOT).parent)+'/'
            assert p.active_links == [route], (p.path,'active nav',p.active_links)
        pages[path] = p
    checked_links = 0
    for path,p in pages.items():
        for tag,attr,url in p.links:
            u = urlsplit(url); checked_links += 1
            if u.scheme == 'mailto':
                assert u.path == 'thalesmmsradio@gmail.com'
                continue
            if u.scheme:
                assert tag=='a' and attr=='href', (p.path,'external asset')
                if url in PRIVACY_REFERENCES:
                    continue
                assert u.scheme=='https' and u.netloc=='github.com', (p.path,'external link',url)
                parts=u.path.strip('/').split('/')
                assert len(parts)==2 and parts[0]=='ThalesMMS' and parts[1] in PUBLIC_REPOS, (p.path,'non-public source link',url)
                continue
            assert not u.netloc, (p.path,'protocol-relative asset')
            target = ROOT/u.path.lstrip('/') if u.path.startswith('/') else path.parent/u.path
            target = target/'index.html' if target.is_dir() else target
            if not u.path: target=path
            assert target.is_file(), (p.path,'broken link',url)
            if u.fragment:
                assert target in pages and unquote(u.fragment) in pages[target].ids, (p.path,'broken fragment',url)
        if path.parent.name in {'support','privacy','data-collection'}:
            assert any(url=='mailto:thalesmmsradio@gmail.com' for _,_,url in p.links), (p.path,'missing contact')
    content_files = list((ROOT/'content/apps').glob('*.json'))
    assert {file.stem for file in content_files} == SLUGS, 'Every project needs a content source'
    for file in content_files:
        data=json.loads(file.read_text())
        assert data['slug'] in SLUGS and data['slug']==file.stem
        if data['slug'] in CLOSED_SLUGS: assert data['repositories']==[], file
        assert data['features'] and data['support'] and data['privacy'],file
        if data.get('reviewed_date'):
            assert 'Description reviewed '+data['reviewed_date'] in pages[ROOT/'apps'/data['slug']/'index.html'].text, (file,'missing review date')
        for edition in data.get('editions', []):
            for suffix in ['', 'support']:
                assert edition['title'] in pages[ROOT/'apps'/data['slug']/suffix/'index.html'].text, (file,'missing edition guidance')
    for path in [*actual,*(ROOT/'content/apps').glob('*.json'),ROOT/'assets/site.css']:
        text=path.read_text()
        assert '/Users/' not in text and 'file://' not in text, (path,'local path leak')
        assert not any(re.search(p,text) for p in SECRET_PATTERNS), (path,'credential-like content')
    print(f'PASS: {len(pages)} HTML pages, {checked_links} links, {len(SLUGS)} complete project routes;')
    print('headings, landmarks, contact links, local assets, source-link allowlist, and credential-pattern checks.')


if __name__ == '__main__':
    try:
        main()
    except AssertionError as error:
        print('FAIL:',error,file=sys.stderr)
        sys.exit(1)
