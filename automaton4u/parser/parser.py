from typing import List, Set

from automaton4u.parser.exceptions import UnexpectedTokenTypeException
from automaton4u.tokenizer import ttypes, Token

"""
    Grammar:= <Automaton Assignation> (<LINE_BREAK > <Automaton Assignation>)*
    Automaton Assignation:= [<AUTOMATON_START_STATE>, <AUTOMATON_STATE>] <GRAMMAR_DEFINITION_ARROW> <Grammar List>
    Grammar List:= <Grammar Atomic> (<OR> <Grammar Atomic>)*
    Grammar Atomic:= (<AUTOMATON_STATE> | <AUTOMATON_TOKEN>)+ | <EPSILON>
    
    
    sigma: Terminal alphabet
    n: Non-terminal alphabet
    s: Initial symbol
    p: Production rules
"""


class Grammar:
    def __init__(self, sigma: Set[str], n: Set[str], s: str, p: Set[str]):
        self.sigma = sigma
        self.n = n
        self.s = s
        self.p = p


class Parser:
    tokens = list()
    sigma = set()
    n = set()

    def initialize(self, tokens: List[Token]):
        self.tokens = tokens

    def parse_grammar_atomic(self):
        while self.peek([ttypes.AUTOMATON_STATE, ttypes.AUTOMATON_TOKEN]):
            if self.peek([ttypes.AUTOMATON_TOKEN]):
                self.sigma = self.sigma | self.consume([ttypes.AUTOMATON_TOKEN])
            else:
                self.n = self.n | self.consume([ttypes.AUTOMATON_STATE])

        if self.peek([ttypes.EPSILON]):
            self.consume([ttypes.EPSILON])

    def parse_grammar_list(self):
        self.parse_grammar_atomic()

        while self.peek([ttypes.OR]):
            self.consume([ttypes.OR])
            self.parse_grammar_atomic()

    def consume(self, expected_type: List[str]) -> Token:
        token = self.tokens.pop(0)

        if token.token_type in expected_type:
            return token
        else:
            raise UnexpectedTokenTypeException(f"Expected token type {expected_type} but got {token.token_type}")

    def peek(self, expected_type: List[str]) -> bool:
        return self.tokens[0].token_type in expected_type
