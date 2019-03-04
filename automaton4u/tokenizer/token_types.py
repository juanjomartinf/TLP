"""
Grammar definition of the automaton generator.
Kind of a meta-grammar

S -> a|bA|€
A -> c

==

['S', '->', 'a', '|', 'b', 'A', '|', '€', '\n', 'A', '->', 'c']

"""

AUTOMATON_START_STATE = 'STARTING_STATE'
AUTOMATON_STATE = 'NORMAL_STATE'
AUTOMATON_TOKEN = 'NORMAL_TOKEN'
GRAMMAR_DEFINITION_ARROW = 'ARROW'
EPSILON = 'EPSILON'
LINE_BREAK = 'LINE_BREAK'
OR = 'OR'

TOKEN_PATTERNS = [
    (AUTOMATON_START_STATE, r'S'),
    (GRAMMAR_DEFINITION_ARROW, r'->'),
    (AUTOMATON_STATE, r'[A-Z]'),
    (AUTOMATON_TOKEN, r'[a-z]'),
    (EPSILON, r'€'),
    (LINE_BREAK, '\n'),
    (OR, '\|')
]

IGNORE_CHARACTERS = [' ', '\t']
