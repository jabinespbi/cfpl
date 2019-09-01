import unittest

from compiler.lexical.ValidToken import ValidToken


class MyTestCase(unittest.TestCase):
    def test_check_exact(self):
        validtoken = ValidToken()
        token_found = validtoken.check("VAR", 0)
        self.assertEqual([0, 3], token_found, 'Incorrect indexes!')

    def test_check_long(self):
        validtoken = ValidToken()
        token_found = validtoken.check("VARSTOP*", 0)
        self.assertEqual([0, 7], token_found, 'Incorrect indexes!')

    def test_check2(self):
        validtoken = ValidToken()
        token_found = validtoken.check("VA*RSTOP", 0)
        self.assertEqual([0, 2], token_found, 'Incorrect indexes!')

    def test_check3(self):
        validtoken = ValidToken()
        token_found = validtoken.check("*VARSTOP", 0)
        self.assertEqual([0, 1], token_found, 'Incorrect indexes!')

    def test_check4(self):
        validtoken = ValidToken()
        token_found = validtoken.check("abcVARSTOP", 0)
        self.assertEqual([0, 10], token_found, 'Incorrect indexes!')

    def test_check5(self):
        validtoken = ValidToken()
        token_found = validtoken.check("\"abcVARSTOP\"", 0)
        self.assertEqual([0, 12], token_found, 'Incorrect indexes!')

    def test_invalid(self):
        validtoken = ValidToken()
        token_found = validtoken.check("'\"abcVARSTOP\"", 0)
        self.assertEqual(None, token_found)


if __name__ == '__main__':
    unittest.main()
