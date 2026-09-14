import copy
import importlib.util
import json
import tempfile
import unittest
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
SPEC = importlib.util.spec_from_file_location('checker', ROOT / 'scripts/check_submission.py')
MODULE = importlib.util.module_from_spec(SPEC)
SPEC.loader.exec_module(MODULE)
RULES = json.loads((ROOT / 'references/applied-energy.rules.json').read_text())


class Checks(unittest.TestCase):
    def setUp(self):
        self.temp = tempfile.TemporaryDirectory()
        self.base = Path(self.temp.name)
        # These files only exercise path checks; they are not real manuscript documents.
        for name in ('manuscript.tex', 'highlights.txt', 'conflicts.docx'):
            (self.base / name).write_text('LOCAL TEST ONLY, never upload')
        self.data = json.loads((ROOT / 'assets/submission.template.json').read_text())
        self.data.update(article_type='Local test research article', title='Local test title', abstract=' '.join(['word'] * 250), keywords=['Storage'], highlights=['x' * 85, 'Second local test highlight.', 'Third local test highlight.'], source_author_order=['a1', 'a2'], corresponding_author_id='a2', submitting_author_id='a2')
        self.data['journal']['guide_checked_on'] = RULES['checked_on']
        self.data['affiliations'] = [{'id': 'f1', 'institution': 'Local Test Institute', 'country_or_region': 'Test region'}]
        self.data['authors'] = [{'id': aid, 'given_name': 'Sample', 'family_name': aid, 'email': aid + '@example.invalid', 'affiliation_ids': ['f1'], 'credit_roles': ['Methodology']} for aid in ('a1', 'a2')]
        self.data['funding'] = {'status': 'none', 'sources': []}
        self.data['declarations'] = {'competing_interests': {'status': 'none'}, 'ai_use': {'status': 'none'}, 'ethics': {'status': 'not_applicable', 'statement': 'Local fictional fixture only.'}, 'all_authors_approved': True, 'not_under_review_elsewhere': True}
        self.data['data_availability'] = {'status': 'not_applicable', 'statement': 'Local fictional fixture only.'}
        self.data['files'] = [{'role': r, 'path': p} for r, p in [('manuscript', 'manuscript.tex'), ('highlights', 'highlights.txt'), ('competing_interests', 'conflicts.docx')]]
        self.data['provenance'] = [{'field': 'all', 'source': 'LOCAL FICTIONAL FIXTURE'}]

    def tearDown(self):
        self.temp.cleanup()

    def check(self):
        return MODULE.check_submission(self.data, self.base, RULES)

    def codes(self):
        return {i['code'] for i in self.check()['issues']}

    def test_boundary_and_no_mutation(self):
        original = copy.deepcopy(self.data)
        report = self.check()
        self.assertEqual(report['errors'], 0)
        self.assertEqual(report['submission_ready'], 'not_determined')
        self.assertEqual(self.data, original)

    def test_overlong_abstract(self):
        self.data['abstract'] += ' extra'
        self.assertIn('abstract_too_long', self.codes())

    def test_overlong_highlight(self):
        self.data['highlights'][0] += ' '
        self.assertIn('highlight_too_long', self.codes())

    def test_keyword_range(self):
        self.data['keywords'] = ['k' + str(i) for i in range(8)]
        self.assertIn('too_many_items', self.codes())

    def test_wrong_order(self):
        self.data['authors'].reverse()
        self.assertIn('author_order_mismatch', self.codes())

    def test_broken_affiliation(self):
        self.data['authors'][1]['affiliation_ids'] = ['missing']
        self.assertIn('broken_affiliation', self.codes())

    def test_unknowns_not_false(self):
        self.data['funding']['status'] = 'unknown'
        self.data['declarations']['all_authors_approved'] = None
        self.data['declarations']['ethics']['status'] = 'unknown'
        codes = self.codes()
        self.assertTrue({'funding_unconfirmed', 'author_confirmation_needed', 'declaration_unconfirmed'}.issubset(codes))

    def test_no_funding_with_funder_conflict(self):
        self.data['funding']['sources'] = [{'organization': 'Local fictional funder'}]
        self.assertIn('funding_conflict', self.codes())

    def test_missing_file(self):
        (self.base / 'manuscript.tex').unlink()
        self.assertIn('file_not_found', self.codes())

    def test_wrong_journal(self):
        self.data['journal']['code'] = 'OTHER'
        self.data['abstract'] = ' '.join(['word'] * 251)
        codes = self.codes()
        self.assertIn('wrong_journal_rules', codes)
        self.assertNotIn('abstract_too_long', codes)

    def test_blank_template_not_ready(self):
        self.data = json.loads((ROOT / 'assets/submission.template.json').read_text())
        self.assertGreater(self.check()['errors'], 0)

    def test_malformed_arrays(self):
        self.data['authors'] = {'unexpected': 'object'}
        self.assertIn('array_required', self.codes())


if __name__ == '__main__':
    unittest.main(verbosity=2)
