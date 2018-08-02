import unittest
from api.spelling import SpellChecker
from services.spellcheck_dictionary import SpellCheckDictionary
import flask


class SpellCheckerTestCase(unittest.TestCase):
    def setUp(self):
        words = ["test", "tip", "out", "lost", "rate", "tasty", "cost"]
        self.spellChecker = SpellChecker()
        self.spellCheckDictionary = SpellCheckDictionary().fromList(words)

    def test_emptyword_returns500(self):
        rv = self.spellChecker.spellcheck("", self.spellCheckDictionary)

        self.assertEqual(spellChecker.spellcheck("", spellCheckDictionary),
                                                (rv.status, 500))
    
    def test_wordiscorrect_returns200(self):
        rv = self.spellChecker.spellcheck("test", self.spellCheckDictionary)

        self.assertEqual(rv.status, 200)
        self.assertEqual(rv.data.correct, True)

    def test_wordisincorrect_returns200withsuggestions(self):
        rv = self.spellChecker.spellcheck("test", self.spellCheckDictionary)

        self.assertEqual(rv.status, 200)
        self.assertEqual(rv.data.correct, False)  
        self.assertTrue(len(rv.data.suggestions) > 0) 
        self.assertTrue("lost" in rv.data.suggestions)
        self.assertTrue("cost" not in rv.data.suggestions)

    def test_wordnofound_returns404(self):
        rv = self.spellChecker.spellcheck("xxxxxxxxxxx", self.spellCheckDictionary)

        self.assertEqual(rv.status, 404)
          
if __name__ == '__main__':
    # unittest.main()
    unittest.findTestCases(__main__).debug()