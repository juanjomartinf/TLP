import unittest

from automaton4u.parser.exceptions import UnexpectedTokenTypeException, StateNotFoundException
from automaton4u.parser.parser import Parser
from automaton4u.tokenizer import Tokenizer


class TestParser(unittest.TestCase):

    def parse(self, grammar):
        tokens = Tokenizer(grammar).tokenize()
        return Parser(tokens).parse()

    def test_parse_simple_grammar(self):
        grammar = "S -> a"
        result = self.parse(grammar)
        self.assertEqual(result.state_name, 'S')
        self.assertEqual(len(result.transitions), 1)
        self.assertEqual(result.transitions[0][0].value, 'a')

    def test_repr_simple_grammar(self):
        grammar = "S -> a"
        result = self.parse(grammar)
        self.assertEqual(result.state_name, 'S')
        self.assertEqual(len(result.transitions), 1)
        self.assertEqual(result.transitions[0][0].value, 'a')
        self.assertEqual(repr(result), 'S -> a')

    def test_parse_or_grammar(self):
        grammar = "S -> a | b"
        result = self.parse(grammar)
        self.assertEqual(result.state_name, 'S')
        self.assertEqual(len(result.transitions), 2)
        self.assertEqual(result.transitions[0][0].value, 'a')
        self.assertEqual(result.transitions[1][0].value, 'b')

    def test_repr_or_grammar(self):
        grammar = "S -> a | b"
        result = self.parse(grammar)
        self.assertEqual(result.state_name, 'S')
        self.assertEqual(len(result.transitions), 2)
        self.assertEqual(result.transitions[0][0].value, 'a')
        self.assertEqual(result.transitions[1][0].value, 'b')
        self.assertEqual(repr(result), 'S -> a | b')

    def test_parse_epsilon_grammar(self):
        grammar = "S -> €"
        result = self.parse(grammar)
        self.assertEqual(result.state_name, 'S')
        self.assertEqual(len(result.transitions), 1)
        self.assertEqual(result.transitions[0][0].value, '€')

    def test_parse_or_epsilon_grammar(self):
        grammar = "S -> a | €"
        result = self.parse(grammar)
        self.assertEqual(result.state_name, 'S')
        self.assertEqual(len(result.transitions), 2)
        self.assertEqual(result.transitions[0][0].value, 'a')
        self.assertEqual(result.transitions[1][0].value, '€')

    def test_parse_two_assignations(self):
        grammar = "S -> aB\nB -> c"
        result = self.parse(grammar)
        self.assertEqual(result.state_name, 'S')
        self.assertEqual(len(result.transitions), 1)
        self.assertEqual(result.transitions[0][0].value, 'a')
        self.assertEqual(result.transitions[0][1].value, 'B')
        self.assertEqual(len(result.other_automaton_states), 1)
        self.assertIn('B', result.other_automaton_states)
        B = result.other_automaton_states['B']
        self.assertEqual(len(B.transitions), 1)
        self.assertEqual(B.transitions[0][0].value, 'c')

    def test_parse_terminal_simple_assignation(self):
        grammar = "S -> a"
        result = self.parse(grammar)
        self.assertEqual(result.state_name, 'S')
        self.assertEqual(len(result.transitions), 1)
        self.assertEqual(result.transitions[0][0].value, 'a')
        self.assertTrue(result.is_terminal)

    def test_parse_non_terminal_simple_assignation(self):
        grammar = "S -> A\nA -> a"
        result = self.parse(grammar)
        self.assertEqual(result.state_name, 'S')
        self.assertEqual(len(result.transitions), 1)
        self.assertEqual(result.transitions[0][0].value, 'A')
        self.assertFalse(result.is_terminal)

    def test_parse_terminal_epsilon_assignation(self):
        grammar = "S -> €"
        result = self.parse(grammar)
        self.assertEqual(result.state_name, 'S')
        self.assertEqual(len(result.transitions), 1)
        self.assertEqual(result.transitions[0][0].value, '€')
        self.assertTrue(result.is_terminal)

    def test_parse_terminal_chained_assignation(self):
        grammar = "S -> A | A | a\nA -> a"
        result = self.parse(grammar)
        self.assertEqual(result.state_name, 'S')
        self.assertTrue(result.is_terminal)

    def test_parse_terminal_chained_epsilon_assignation(self):
        grammar = "S -> A | A | €\nA -> a"
        result = self.parse(grammar)
        self.assertEqual(result.state_name, 'S')
        self.assertTrue(result.is_terminal)

    def test_parse1_ko(self):
        bad_grammar = "S -> -> ->"

        with self.assertRaises(UnexpectedTokenTypeException):
            self.parse(bad_grammar)

    def test_parse2_ko(self):
        bad_grammar = "S |"

        with self.assertRaises(UnexpectedTokenTypeException):
            self.parse(bad_grammar)

    def test_parse_undeclared_grammar_ko(self):
        bad_grammar = "S -> A"

        with self.assertRaises(StateNotFoundException):
            self.parse(bad_grammar)
