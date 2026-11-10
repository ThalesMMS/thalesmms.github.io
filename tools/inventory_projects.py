#!/usr/bin/env python3
"""Inventory current and historical site projects against explicit local sources.

Read-only outside the output file. No network, app execution, or credential reads.
Source mappings and detailed reports belong in the ignored .site-work directory.
"""
import argparse
from datetime import datetime
from hashlib import sha256
import json
from pathlib import Path
import re
import subprocess
from zoneinfo import ZoneInfo

ROOT = Path(__file__).resolve().parents[1]


def git(root, *args):
    result = subprocess.run(
        ['git', '-C', str(root), *args], capture_output=True, text=True, check=True)
    return result.stdout.strip()


def site_at(revision):
    paths = git(ROOT, 'ls-tree', '-r', '--name-only', revision).splitlines()
    pages = [p for p in paths if re.fullmatch(r'apps/[^/]+/index.html', p)]
    projects = {}
    for path in pages:
        body = git(ROOT, 'show', f'{revision}:{path}')
        title = re.search(r'<h1[^>]*>(.*?)</h1>', body, re.S)
        projects[path.split('/')[1]] = {
            'title': title.group(1) if title else None,
            'repositories': sorted(set(re.findall(
                r'https://github\.com/ThalesMMS/[A-Za-z0-9_.-]+', body))),
        }
    return projects


def source_state(parent, source):
    path = (parent / source['path']).resolve()
    if not path.is_dir():
        return {**source, 'exists': False}
    owner = Path(git(path, 'rev-parse', '--show-toplevel'))
    files = []
    for name in source.get('evidence', []):
        file = path / name
        files.append({'path': name, 'exists': file.is_file(),
                      'sha256': sha256(file.read_bytes()).hexdigest() if file.is_file() else None})
    return {**source, 'exists': True,
            'git_root': str(owner.relative_to(parent.resolve())),
            'head': git(path, 'rev-parse', 'HEAD'),
            'branch': git(path, 'branch', '--show-current'),
            'last_commit': git(path, 'log', '-1', '--format=%cs %s'),
            'changes': git(owner, 'status', '--porcelain', '--untracked-files=normal').splitlines(),
            'evidence_files': files}


def markdown_report(report, parent):
    sources = [s for p in report['projects'].values() for s in p['sources']]
    owners = {s.get('git_root') for s in sources if s['exists']}
    lines = ['# Levantamento dos projetos do site', '',
             f"Inventário registrado em {report['reviewed_at']}, America/Sao_Paulo.", '',
             f"Foram encontrados {len(report['projects'])} projetos/seções no histórico local, "
             f"{len(report['history'])} revisões alcançáveis do site e {len(sources)} entradas de fontes "
             f'em {len(owners)} árvores Git. Entradas incluem componentes incorporados e cópias de desenvolvimento.', '',
             'O estado registra o código local, inclusive alterações não commitadas. Data do último commit não prova inatividade. '
             'Uma cópia -dev mais nova não prova que seus recursos foram distribuídos pelo repositório público.', '',
             'A revisão é estática. Não foram executados os aplicativos, consultas clínicas, logins ou inferências. '
             'Disponibilidade em lojas, funcionamento em todos os sistemas e retenção de terceiros não foram validados.', '',
             '## Projetos e versões', '']
    for slug, project in report['projects'].items():
        lines += [f"### {project['name']}", '', f'Página: `/apps/{slug}/`.', '']
        lines.extend(f'- {finding}' for finding in project['findings'])
        lines += ['', '| Fonte local | Papel | Revisão | Alterações locais |',
                  '| --- | --- | --- | --- |']
        for source in project['sources']:
            path = parent.resolve() / source['path']
            head = source.get('head', 'ausente')[:10]
            count = len(source.get('changes', []))
            lines.append(f"| [{source['path']}]({path}) | {source['role']} | `{head}` | {count} |")
        lines += ['', 'Arquivos de evidência registrados com hashes no inventário:', '']
        for source in project['sources']:
            for evidence in source.get('evidence_files', []):
                path = parent.resolve() / source['path'] / evidence['path']
                lines.append(f'- [{source["path"]}/{evidence["path"]}]({path})')
        lines += ['']
    lines += ['## Histórico do site', '',
              'O inventário JSON guarda nomes e links por revisão. Não houve projeto antigo sem correspondência no mapa atual.', '',
              '| Data do commit | Revisão | Seções de projeto |', '| --- | --- | --- |']
    lines.extend(f"| {s['date']} | `{s['revision'][:10]}` | {len(s['projects'])} |" for s in report['history'])
    lines += ['', '## Pendências e limites', '',
              '- Os mínimos declarados nos manifestos não comprovam execução no hardware ou sistema mínimo.',
              '- Políticas Safari, Apple/Android, macOS App Store e iOS mantêm escopo explícito. Suplementos e outras implementações precisam de políticas próprias antes de serem apresentados como cobertos pelas mesmas declarações.',
              '- README e AGENTS podem estar atrasados em relação ao código. Os conflitos encontrados estão registrados por projeto.',
              '- Esta revisão atualiza a cópia local do site. Publicação, assinatura, notarização e configuração de lojas não fazem parte da verificação.',
              '- O mapa e este relatório são locais, em .site-work. Não publicar caminhos ou evidências de fontes privadas.', '']
    return '\n'.join(lines)


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--map', required=True, type=Path, help='Local JSON: slug -> sources[] and findings[]')
    parser.add_argument('--parent', type=Path, default=ROOT.parent)
    parser.add_argument('--output', required=True, type=Path)
    parser.add_argument('--markdown', type=Path, help='Optional local Markdown report')
    args = parser.parse_args()
    mapping = json.loads(args.map.read_text())
    revisions = git(ROOT, 'rev-list', '--all', '--reverse', '--', 'apps', 'content/apps', 'index.html').splitlines()
    history = [{'revision': rev, 'date': git(ROOT, 'show', '-s', '--format=%cs', rev),
                'projects': site_at(rev)} for rev in revisions]
    current_paths = sorted((ROOT / 'apps').glob('*/index.html'))
    current = {p.parent.name for p in current_paths}
    cited = current | {slug for snapshot in history for slug in snapshot['projects']}
    missing = cited - mapping.keys()
    if missing:
        parser.error('Unmapped site projects: ' + ', '.join(sorted(missing)))
    report = {
        'reviewed_at': datetime.now(ZoneInfo('America/Sao_Paulo')).isoformat(timespec='seconds'),
        'site_head': git(ROOT, 'rev-parse', 'HEAD'),
        'scope': 'Current working tree and every reachable site revision; explicit local editions, not installed/store builds.',
        'history': history,
        'projects': {slug: {**mapping[slug], 'currently_listed': slug in current,
                            'sources': [source_state(args.parent, s) for s in mapping[slug]['sources']]}
                     for slug in sorted(cited)},
    }
    args.output.parent.mkdir(parents=True, exist_ok=True)
    args.output.write_text(json.dumps(report, ensure_ascii=False, indent=2) + '\n')
    if args.markdown:
        args.markdown.parent.mkdir(parents=True, exist_ok=True)
        args.markdown.write_text(markdown_report(report, args.parent))
    sources = [s for p in report['projects'].values() for s in p['sources']]
    errors = [s['path'] for s in sources if not s['exists'] or
              any(not f['exists'] for f in s.get('evidence_files', []))]
    print(f'{len(current)} current sections; {len(cited)} historical identities; {len(history)} site revisions; {len(sources)} local source entries.')
    if errors:
        parser.exit(1, 'Missing sources/evidence: ' + ', '.join(errors) + '\n')
    print(f'Inventory written to {args.output}. Source revisions and file hashes identify future drift; findings still require human review.')


if __name__ == '__main__':
    main()
