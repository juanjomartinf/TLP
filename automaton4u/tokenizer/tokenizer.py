import re
from typing import List

from automaton4u.tokenizer.exceptions import UnknownTokenException
from automaton4u.tokenizer.token_types import TOKEN_PATTERNS, IGNORE_CHARACTERS


class Token:
    __slots__ = ('token_type', 'value')

    def __init__(self, token_type: str, value: str):
        self.token_type = token_type
        self.value = value

    def __repr__(self):
        return f"<Token type={self.token_type}, value={self.value} >"


class Tokenizer:

    def __init__(self, code):
        self.code = code
        self._strip_code()


    def tokenize(self) -> List[Token]:
        tokens = []
        while self.code:
            tokens.append(self.single_tokenize())
        return tokens

    def _strip_code(self):
        for ignore_char in IGNORE_CHARACTERS:
            self.code = self.code.replace(ignore_char, '')

    def single_tokenize(self) -> Token:
        for token_type, regex in TOKEN_PATTERNS:
            regex = re.compile(r"\A{}".format(regex))
            value = regex.search(self.code)
            if value:
                value = value.group(0)
                self.code = self.code[len(value):]
                return Token(token_type, value)
        raise UnknownTokenException(f"Could not match token on {self.code}")
