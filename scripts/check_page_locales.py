"""Check canonical app pages without third-party dependencies or executing page JS."""
import argparse
import json
import re
from dataclasses import dataclass, field
from html.parser import HTMLParser
from pathlib import Path


@dataclass
class Node:
    tag: str
    attrs: dict = field(default_factory=dict)
    children: list = field(default_factory=list)

    def walk(self):
        yield self
        for child in self.children:
            if isinstance(child, Node):
                yield from child.walk()

    def raw_text(self):
        return ''.join(c.raw_text() if isinstance(c, Node) else c for c in self.children)


class Parser(HTMLParser):
    VOID = set('area base br col embed hr img input link meta param source track wbr'.split())

    def __init__(self, html):
        super().__init__(convert_charrefs=True)
        self.root = Node('root')
        self.stack = [self.root]
        self.feed(html)
        self.close()

    def handle_starttag(self, tag, attrs):
        node = Node(tag, dict(attrs))
        self.stack[-1].children.append(node)
        if tag not in self.VOID:
            self.stack.append(node)

    def handle_startendtag(self, tag, attrs):
        self.handle_starttag(tag, attrs)
        if tag not in self.VOID:
            self.handle_endtag(tag)

    def handle_endtag(self, tag):
        for i in range(len(self.stack) - 1, 0, -1):
            if self.stack[i].tag == tag:
                del self.stack[i:]
                break

    def handle_data(self, data):
        self.stack[-1].children.append(data)


def has_text(text):
    return isinstance(text, str) and bool(re.sub(r'[\s\u200b\ufeff]', '', text))


def visible_text(node, locale, config, locale_root=False):
    # support.js toggles hidden on locale containers; their initial hidden is expected.
    if node.tag in {'script', 'style', 'template'}:
        return ''
    if 'data-page-locale' in node.attrs and node.attrs['data-page-locale'] != locale:
        return ''
    if not locale_root and 'data-page-locale' not in node.attrs and 'hidden' in node.attrs:
        return ''
    if re.search(r'(display\s*:\s*none|visibility\s*:\s*hidden)', node.attrs.get('style', ''), re.I):
        return ''
    if 'data-support-text' in node.attrs:
        value = config.get(node.attrs['data-support-text'])
        if isinstance(value, str):
            return value  # textContent replaces the fallback, including with an empty string.
    if 'data-support-faqs' in node.attrs:
        faqs = config.get('faqs', [])
        if not isinstance(faqs, list):
            return ''
        return ' '.join(str(f.get(k, '')) for f in faqs if isinstance(f, dict)
                        for k in ('question', 'answer'))
    return ''.join(visible_text(c, locale, config) if isinstance(c, Node) else c
                   for c in node.children)


def inspect_page(html, path):
    root = Parser(html).root
    nodes = list(root.walk())
    findings = []

    def report(locale, kind):
        item = {'file': path, 'locale': locale, 'kind': kind}
        if item not in findings:
            findings.append(item)

    selector = next((n for n in nodes if n.attrs.get('id') == 'language-selector'), None)
    config_node = next((n for n in nodes if n.attrs.get('id') == 'support-page-config'), None)
    blocks = [n for n in nodes if 'data-page-locale' in n.attrs]
    if not selector and not config_node and not blocks:
        # Pages with no language-switching UI are intentionally single-language.
        return findings
    options = [n.attrs.get('value', n.raw_text().strip()) for n in selector.walk()
               if n.tag == 'option'] if selector else []
    if not options:
        report('*', 'missing-selector')
    try:
        config = json.loads(config_node.raw_text()) if config_node else None
        if not isinstance(config, dict) or not isinstance(config.get('locales'), dict):
            raise ValueError('missing locales')
        if any(not isinstance(v, dict) for v in config['locales'].values()):
            raise ValueError('invalid locale data')
    except (ValueError, TypeError):
        report('*', 'invalid-config')
        return findings
    locales = config['locales']
    faq_nodes = [n for n in nodes if 'data-support-faqs' in n.attrs]
    policy_nodes = [n for n in nodes if 'policy-stack' in n.attrs.get('class', '').split()
                    and 'data-page-locale' not in n.attrs]
    for locale in sorted(set(options) | set(locales)):
        if locale not in options:
            report(locale, 'missing-option')
        if locale not in locales:
            report(locale, 'missing-config-locale')
        matching = [n for n in blocks if n.attrs['data-page-locale'] == locale]
        data = locales.get(locale, {})
        if blocks or not (faq_nodes or policy_nodes):
            if not matching:
                report(locale, 'missing-block')
            elif not has_text(''.join(visible_text(n, locale, data, True) for n in matching)):
                report(locale, 'empty-body')
        # The gym support page uses config-driven FAQ bodies instead of locale blocks.
        else:
            dynamic_nodes = faq_nodes + policy_nodes
            for node in policy_nodes:
                if any('data-support-text' in n.attrs and not has_text(data.get(n.attrs['data-support-text']))
                       for n in node.walk()):
                    report(locale, 'missing-dynamic-text')
            if not has_text(''.join(visible_text(n, locale, data) for n in dynamic_nodes)):
                report(locale, 'empty-body')
    for block in blocks:
        locale = block.attrs['data-page-locale']
        if locale not in options and locale not in locales:
            report(locale, 'orphan-block')
    return findings


def canonical_pages(root):
    readme = (root / 'README.md').read_text(encoding='utf-8')
    slugs = list(dict.fromkeys(re.findall(
        r'^\|[^\n]+\| https://mailerdenight\.github\.io/([^/\s]+)/ \|$', readme, re.M)))
    if not slugs:
        raise ValueError('README canonical URL table contains no apps')
    return [f'{slug}/{suffix}' for slug in slugs
            for suffix in ('index.html', 'support/index.html', 'privacy/index.html')]


def scan(root):
    pages = canonical_pages(root)
    findings = []
    for path in pages:
        file = root / path
        if not file.is_file():
            findings.append({'file': path, 'locale': '*', 'kind': 'missing-page'})
        else:
            findings.extend(inspect_page(file.read_text(encoding='utf-8'), path))
    return pages, findings


def key(item):
    return item['file'], item['locale'], item['kind']


def classify(findings, baseline):
    known = {key(i) for i in baseline}
    actual = {key(i) for i in findings}
    return ([i for i in findings if key(i) not in known],
            [i for i in findings if key(i) in known],
            [i for i in baseline if key(i) not in actual])


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--root', type=Path, default=Path(__file__).resolve().parents[1])
    parser.add_argument('--strict', action='store_true', help='Fail on known issues too')
    args = parser.parse_args()
    try:
        pages, findings = scan(args.root)
        baseline = json.loads((args.root / 'scripts/page-locales-baseline.json').read_text())['issues']
        if any(not all(isinstance(i.get(k), str) and i[k] for k in ('file', 'locale', 'kind', 'reason'))
               for i in baseline) or len({key(i) for i in baseline}) != len(baseline):
            raise ValueError('baseline entries require unique file/locale/kind and a reason')
        new, known, resolved = classify(findings, baseline)
    except (OSError, ValueError, KeyError, TypeError, AttributeError) as error:
        print(f'ERROR: {error}')
        return 1
    for status, items in [('NEW', new), ('KNOWN', known), ('RESOLVED', resolved)]:
        for item in items:
            print(f"{status}: {item['file']} [{item['locale']}] {item['kind']}")
    print(f'{len(pages)} pages: {len(new)} new, {len(known)} known, {len(resolved)} resolved')
    # Resolved entries are reminders, not failures: independent translation PRs can land.
    return int(bool(new or (args.strict and known)))


if __name__ == '__main__':
    raise SystemExit(main())
