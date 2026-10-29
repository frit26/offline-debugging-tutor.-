import unittest
from diagnostics import analyze_code

class DiagnosticTests(unittest.TestCase):
    def test_syntax_error(self):
        self.assertEqual(analyze_code('if True print("x")')[0]['kind'], 'SyntaxError')
    def test_indentation_error(self):
        self.assertEqual(analyze_code('def f():\nreturn 1')[0]['kind'], 'IndentationError')
    def test_undefined_name_candidate(self):
        result = analyze_code('print(missing_value)')
        self.assertTrue(any(item['kind'] == 'NameError' for item in result))
    def test_string_number_addition(self):
        result = analyze_code('x = "5" + 10')
        self.assertTrue(any(item['kind'] == 'TypeError' for item in result))
    def test_constant_index_out_of_range(self):
        result = analyze_code('x = [1][3]')
        self.assertTrue(any(item['kind'] == 'IndexError' for item in result))
    def test_valid_code_not_claimed_correct(self):
        result = analyze_code('print("hello")')
        self.assertEqual(result[0]['kind'], 'No supported issue found')

if __name__ == '__main__':
    unittest.main()
