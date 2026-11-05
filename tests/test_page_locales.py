import json
import tempfile
import unittest
from pathlib import Path

from scripts.check_page_locales import classify, inspect_page, scan


def page(body, locales=None, options=('ja', 'en')):
    config = {'locales': locales if locales is not None else {'ja': {}, 'en': {}}}
    return ('<select id="language-selector">' + ''.join(
        f'<option value="{code}">{code}</option>' for code in options) + '</select>'
        + body + '<script id="support-page-config" type="application/json">'
        + json.dumps(config) + '</script>')


class LocaleTests(unittest.TestCase):
    def check(self, html):
        return {(i['locale'], i['kind']) for i in inspect_page(html, 'app/index.html')}

    def test_valid_hidden_translated_body(self):
        self.assertEqual(self.check(page('<div data-page-locale="ja">日本語</div>'
                                       '<div data-page-locale="en" hidden><p>Hello &amp; bye</p></div>')), set())

    def test_missing_block(self):
        self.assertIn(('en', 'missing-block'), self.check(page('<div data-page-locale="ja">本文</div>')))

    def test_empty_markup_comments_and_whitespace(self):
        for body in ('', ' \n&nbsp;\u200b', '<!-- later -->', '<section><br><p></p></section>',
                     '<script>hello</script><style>p{}</style><template>later</template>',
                     '<p hidden>hidden</p>', '<p style="display:none">hidden</p>'):
            with self.subTest(body=body):
                self.assertIn(('en', 'empty-body'), self.check(page(
                    '<div data-page-locale="ja">本文</div><div data-page-locale="en">' + body + '</div>')))

    def test_other_locale_nested_text_does_not_count(self):
        result = self.check(page('<div data-page-locale="ja">本文</div>'
                                 '<div data-page-locale="en"><span data-page-locale="ja">本文</span></div>'))
        self.assertIn(('en', 'empty-body'), result)

    def test_missing_config_locale(self):
        self.assertIn(('en', 'missing-config-locale'), self.check(page('', {'ja': {}})))

    def test_missing_option(self):
        self.assertIn(('en', 'missing-option'), self.check(page('', options=('ja',))))

    def test_orphan(self):
        self.assertIn(('fr', 'orphan-block'), self.check(page('<div data-page-locale="fr">Bonjour</div>')))

    def test_invalid_config(self):
        self.assertIn(('*', 'invalid-config'), self.check('<select id="language-selector">'
            '<option value="en">English</option></select><script id="support-page-config">{</script>'))

    def test_single_language_page(self):
        self.assertEqual(self.check('<main><p>日本語</p></main>'), set())

    def test_selector_removed_from_multilingual_page(self):
        self.assertIn(('*', 'missing-selector'), self.check('<div data-page-locale="en">Hello</div>'))

    def test_config_faqs(self):
        self.assertEqual(self.check(page('<div data-support-faqs>Fallback</div>',
            {'ja': {'faqs': [{'question': '質問', 'answer': '回答'}]},
             'en': {'faqs': [{'question': 'Question', 'answer': 'Answer'}]}})), set())

    def test_empty_dynamic_faq_replaces_fallback(self):
        self.assertIn(('en', 'empty-body'), self.check(page('<div data-support-faqs>Fallback</div>')))

    def test_config_policy(self):
        self.assertEqual(self.check(page('<div class="policy-stack"><p data-support-text="body">本文</p></div>',
            {'ja': {'body': '本文'}, 'en': {'body': 'Policy'}})), set())

    def test_missing_dynamic_policy(self):
        self.assertIn(('en', 'missing-dynamic-text'), self.check(page(
            '<div class="policy-stack"><p data-support-text="body">Fallback</p></div>',
            {'ja': {'body': '本文'}, 'en': {}})))

    def test_dynamic_empty_text_replaces_fallback(self):
        self.assertIn(('en', 'empty-body'), self.check(page(
            '<div data-page-locale="ja">本文</div><div data-page-locale="en" data-support-text="body">Fallback</div>',
            {'ja': {}, 'en': {'body': ''}})))

    def test_multiple_blocks_with_body(self):
        self.assertEqual(self.check(page('<div data-page-locale="ja">本文</div>'
            '<div data-page-locale="en"></div><div data-page-locale="en">Hello</div>')), set())

    def test_exact_baseline_and_resolved_entries(self):
        issue = {'file': 'a.html', 'locale': 'en', 'kind': 'empty-body'}
        changed = dict(issue, kind='missing-block')
        self.assertEqual(classify([issue], [issue]), ([], [issue], []))
        self.assertEqual(classify([changed], [issue]), ([changed], [], [issue]))
        self.assertEqual(classify([], [issue]), ([], [], [issue]))

    def test_discovery_checks_three_pages_and_new_apps(self):
        with tempfile.TemporaryDirectory() as directory:
            root = Path(directory)
            (root / 'README.md').write_text('| アプリ | https://mailerdenight.github.io/new-app/ |\n')
            pages, issues = scan(root)
            self.assertEqual(len(pages), 3)
            self.assertEqual({i['kind'] for i in issues}, {'missing-page'})


if __name__ == '__main__':
    unittest.main()
