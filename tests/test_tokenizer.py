import unittest
from typing import List

from automaton4u.tokenizer import Tokenizer, ttypes, Token
from automaton4u.tokenizer.exceptions import UnknownTokenException


class TestTokenizer(unittest.TestCase):

    def tokenize(self, expression) -> List[Token]:
        return Tokenizer(expression).tokenize()

    def test_tokenize_empty_expression(self):
        expression = ""
        tokens = self.tokenize(expression)
        self.assertEqual(tokens, [])

    def test_repr_ok(self):
        expression = "S"
        tokens = self.tokenize(expression)
        self.assertEqual(len(tokens), 1)
        self.assertEqual(tokens[0].token_type, ttypes.AUTOMATON_START_STATE)
        self.assertIn(ttypes.AUTOMATON_START_STATE, repr(tokens[0]))

    def test_tokenize_start_state_ok(self):
        expression = "S"
        tokens = self.tokenize(expression)
        self.assertEqual(len(tokens), 1)
        self.assertEqual(tokens[0].token_type, ttypes.AUTOMATON_START_STATE)

    def test_normal_state_ok(self):
        expression = "A"
        tokens = self.tokenize(expression)
        self.assertEqual(len(tokens), 1)
        self.assertEqual(tokens[0].token_type, ttypes.AUTOMATON_STATE)

    def test_automaton_token_ok(self):
        expression = "a"
        tokens = self.tokenize(expression)
        self.assertEqual(len(tokens), 1)
        self.assertEqual(tokens[0].token_type, ttypes.AUTOMATON_TOKEN)

    def test_assert_grammar_definition_arrow_ok(self):
        expression = "->"
        tokens = self.tokenize(expression)
        self.assertEqual(len(tokens), 1)
        self.assertEqual(tokens[0].token_type, ttypes.GRAMMAR_DEFINITION_ARROW)

    def test_assert_epsilon_ok(self):
        expression = "€"
        tokens = self.tokenize(expression)
        self.assertEqual(len(tokens), 1)
        self.assertEqual(tokens[0].token_type, ttypes.EPSILON)

    def test_assert_line_break_ok(self):
        expression = "\n"
        tokens = self.tokenize(expression)
        self.assertEqual(len(tokens), 1)
        self.assertEqual(tokens[0].token_type, ttypes.LINE_BREAK)

    def test_or_ok(self):
        expression = '|'
        tokens = self.tokenize(expression)
        self.assertEqual(len(tokens), 1)
        self.assertEqual(tokens[0].token_type, ttypes.OR)

    def test_right_strip_ok(self):
        expression = "S     "
        tokens = self.tokenize(expression)
        self.assertEqual(len(tokens), 1)
        self.assertEqual(tokens[0].token_type, ttypes.AUTOMATON_START_STATE)

    def test_left_strip_ok(self):
        expression = "              S"
        tokens = self.tokenize(expression)
        self.assertEqual(len(tokens), 1)
        self.assertEqual(tokens[0].token_type, ttypes.AUTOMATON_START_STATE)

    def test_raise_unknown_token(self):
        expression = "1234"
        with self.assertRaises(UnknownTokenException):
            self.tokenize(expression)

    def test_tokenize_simple_expresssion(self):
        expression = "S -> a"
        tokens = self.tokenize(expression)
        self.assertEqual(len(tokens), 3)
        s, arrow, a = tokens
        self.assertEqual(s.token_type, ttypes.AUTOMATON_START_STATE)
        self.assertEqual(arrow.token_type, ttypes.GRAMMAR_DEFINITION_ARROW)
        self.assertEqual(a.token_type, ttypes.AUTOMATON_TOKEN)

    def test_tokenize_or_expression(self):
        expression = "S -> a | b"
        tokens = self.tokenize(expression)
        self.assertEqual(len(tokens), 5)
        s, arrow, a, _or, b = tokens
        self.assertEqual(s.token_type, ttypes.AUTOMATON_START_STATE)
        self.assertEqual(arrow.token_type, ttypes.GRAMMAR_DEFINITION_ARROW)
        self.assertEqual(a.token_type, ttypes.AUTOMATON_TOKEN)
        self.assertEqual(_or.token_type, ttypes.OR)
        self.assertEqual(b.token_type, ttypes.AUTOMATON_TOKEN)

    def test_tokenize_two_expressions(self):
        expression = """S -> a | b\nC -> d"""

        tokens = self.tokenize(expression)
        self.assertEqual(len(tokens), 9)
        s, a1, a, _or, b, nl, c, a2, d = tokens

        self.assertEqual(s.token_type, ttypes.AUTOMATON_START_STATE)
        self.assertEqual(a1.token_type, ttypes.GRAMMAR_DEFINITION_ARROW)
        self.assertEqual(a.token_type, ttypes.AUTOMATON_TOKEN)
        self.assertEqual(_or.token_type, ttypes.OR)
        self.assertEqual(b.token_type, ttypes.AUTOMATON_TOKEN)
        self.assertEqual(nl.token_type, ttypes.LINE_BREAK)
        self.assertEqual(c.token_type, ttypes.AUTOMATON_STATE)
        self.assertEqual(a2.token_type, ttypes.GRAMMAR_DEFINITION_ARROW)
        self.assertEqual(d.token_type, ttypes.AUTOMATON_TOKEN)
