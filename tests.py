import time
import unittest

from python_spell.checker import SpellChecker


class SpellCheckerTests(unittest.TestCase):

    def setUp(self):
        self.spell_checker = SpellChecker()

    def test_bucketize_time(self):
        start_time = time.time()
        self.spell_checker.bucketize()
        end_time = time.time()
        self.assertLess(end_time - start_time, 1)

    def test_check_lang(self):
        self.assertTrue(self.spell_checker.check_lang('english'))
        self.assertFalse(self.spell_checker.check_lang('japanese'))

    def test_check_time(self):
        words = ["hello", "world"]
        start_time = time.time()
        self.spell_checker.check(words)
        end_time = time.time()
        self.assertLess(end_time - start_time, 1)

    def test_check_echo(self):
        words = ["hello", "world"]
        statistics = self.spell_checker.check(words, echo=True)
        self.assertIn('total_words', statistics)

    def test_check_no_typos(self):
        words = ["hello", "world"]
        statistics = self.spell_checker.check(words)
        self.assertFalse(statistics['has_typos'])

    def test_check_typos(self):
        # retourne False parce qu'on convertit en minuscule
        words1 = ["hello", "worlD"]
        statistics = self.spell_checker.check(words1)
        self.assertFalse(statistics['has_typos'])
        words2 = ["hello", "wordl"]
        statistics = self.spell_checker.check(words2)
        self.assertTrue(statistics['has_typos'])

    def test_check_exclude(self):
        words = ["hello", "world"]
        self.spell_checker.check(words)
        self.spell_checker.exclude('world')
        typos_wo_excluded_words = self.spell_checker.get_typos(exclude=['world'])
        self.assertEqual(typos_wo_excluded_words, set())

    def test_check_exclude_temp(self):
        words = ["helol", "wolrd"]
        self.spell_checker.check(words)
        typos_wo_excluded_words = self.spell_checker.exclude('wolrd', temp=True)
        self.assertEqual(typos_wo_excluded_words, {'helol'})
        self.assertEqual(self.spell_checker.get_typos(), {'helol', 'wolrd'})

    def test_check_exclude_multiple(self):
        words = ["hello", "world"]
        self.spell_checker.check(words)
        self.spell_checker.exclude(['hello', 'world'])
        typos_wo_excluded_words = self.spell_checker.get_typos()
        self.assertEqual(typos_wo_excluded_words, set())

    def test_check_exclude_temp_multiple(self):
        words = ["helol", "wordl"]
        typos_wo_excluded_words = self.spell_checker.exclude(words, temp=True)
        self.assertEqual(typos_wo_excluded_words, set())
        self.assertSetEqual(self.spell_checker.get_typos(), set())

    def test_check_exclude_all(self):
        words = ["hello", "world"]
        self.spell_checker.check(words)
        self.spell_checker.exclude(self.spell_checker.get_typos())
        typos_wo_excluded_words = self.spell_checker.get_typos()
        self.assertEqual(typos_wo_excluded_words, set())

    def test_check_exclude_all_temp(self):
        words = ["hello", "world"]
        self.spell_checker.check(words)
        typos_wo_excluded_words = self.spell_checker.exclude(
            self.spell_checker.get_typos(), temp=True)
        self.assertEqual(typos_wo_excluded_words, set())
        self.assertEqual(self.spell_checker.get_typos(), set())

    def test_number_of_typos(self):
        words = ["hello", "wolrd", "wolrd"]
        self.spell_checker.check(words)
        self.assertEqual(self.spell_checker.number_of_typos(), 1)
        self.assertEqual(self.spell_checker.number_of_typos(duplicates=True), 2)

    def test_get_typos(self):
        words = ["hello", "wordl"]
        self.spell_checker.check(words)
        typos = self.spell_checker.get_typos()
        self.assertIn('wordl', typos)
        self.assertNotIn('Hello', typos)

    def test_get_typos_duplicates(self):
        words = ["helol", "wordl", "wordl"]
        self.spell_checker.check(words)
        typos = self.spell_checker.get_typos(duplicates=True)
        self.assertEqual(sorted(typos), sorted(["helol", "wordl", "wordl"]))
        self.assertIn('wordl', typos)
        self.assertIn('helol', typos)

    def test_get_typos_exclude(self):
        words = ["hello", "world"]
        self.spell_checker.check(words)
        self.spell_checker.exclude('world')
        typos = self.spell_checker.get_typos()
        self.assertNotIn('world', typos)

    def test_get_typos_exclude_temp(self):
        words = ["hello", "wordl"]
        self.spell_checker.check(words)
        excluded_words = self.spell_checker.exclude('wordl', temp=True)
        self.assertEqual(excluded_words, set())
        typos = self.spell_checker.get_typos()
        self.assertIn('wordl', typos)

    def test_get_typos_exclude_multiple(self):
        words = ["hello", "world"]
        self.spell_checker.check(words)
        self.spell_checker.exclude(['hello', 'world'])
        typos = self.spell_checker.get_typos()
        self.assertEqual(typos, set())

    def test_get_typos_exclude_temp_multiple(self):
        words = ["hello", "wordl"]
        self.spell_checker.check(words)
        excluded_words = self.spell_checker.exclude(['hello', 'world'], temp=True)
        self.assertEqual(excluded_words, {'wordl'})
        typos = self.spell_checker.get_typos()
        self.assertNotIn('hello', typos)
        self.assertIn('wordl', typos)

    def test_get_typos_exclude_all(self):
        words = ["hello", "world"]
        self.spell_checker.check(words)
        self.spell_checker.exclude(self.spell_checker.get_typos())
        typos = self.spell_checker.get_typos()
        self.assertEqual(typos, set())

    def test_get_typos_exclude_all_temp(self):
        words = ["hello", "world"]
        self.spell_checker.check(words)
        self.spell_checker.exclude(self.spell_checker.get_typos(), temp=True)
        typos = self.spell_checker.get_typos()
        self.assertEqual(typos, set())

    def test_visualize(self):
        words = ["hello", "world"]
        statistics = self.spell_checker.check(words, echo=True)
        self.assertIn('total_words', statistics)


if __name__ == '__main__':
    unittest.main()
