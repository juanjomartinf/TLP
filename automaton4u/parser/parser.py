from typing import List, Set, Union

from automaton4u.parser.exceptions import UnexpectedTokenTypeException, StateNotFoundException
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


class AutomatonState:

    def __init__(self, state_name: str, transitions: List[List[Token]] = None, other_automaton_states=None):
        self.state_name = state_name
        self.transitions = transitions or []
        self.other_automaton_states = other_automaton_states or {}

    @property
    def is_terminal(self):
        if not self.other_automaton_states:
            return True

        for transition in self.transitions:
            if all(token.token_type != ttypes.AUTOMATON_STATE for token in transition):
                return True
        return False

    def __repr__(self):
        all_transitions = []
        for transition in self.transitions:
            transition_str = "".join(t.value for t in transition)
            all_transitions.append(transition_str)
        return f"{self.state_name} -> {' | '.join(all_transitions)}"


class Parser:

    def __init__(self, tokens: List[Token]):
        self.tokens = tokens

    def parse(self) -> AutomatonState:
        automaton_state_list = self._parse_grammar()
        states = {automaton_state.state_name: automaton_state for automaton_state in automaton_state_list}

        for automaton_state in automaton_state_list:
            for transitions in automaton_state.transitions:
                for transition in transitions:
                    if transition.token_type in [ttypes.AUTOMATON_STATE, ttypes.AUTOMATON_START_STATE]:
                        if transition.value not in states:
                            raise StateNotFoundException(f"State {transition.value} mentioned but not declared.")
                        automaton_state.other_automaton_states[transition.value] = states[transition.value]

        starting_state = states.get('S', None)
        if starting_state is None:
            starting_state = AutomatonState(state_name='S',
                                            transitions=[[Token(ttypes.AUTOMATON_STATE, value=state.state_name)] for
                                                         state in automaton_state_list], other_automaton_states=states)

        return starting_state

    def _parse_grammar(self) -> List[AutomatonState]:
        automaton_state_list = [self._parse_automaton_assignation()]

        while self.peek(ttypes.LINE_BREAK):
            self.consume(ttypes.LINE_BREAK)
            automaton_state_list.append(self._parse_automaton_assignation())

        return automaton_state_list

    def _parse_automaton_assignation(self) -> AutomatonState:
        if self.peek(ttypes.AUTOMATON_START_STATE):
            state_token = self.consume(ttypes.AUTOMATON_START_STATE)
        else:
            state_token = self.consume(ttypes.AUTOMATON_STATE)

        self.consume(ttypes.GRAMMAR_DEFINITION_ARROW)

        state = AutomatonState(state_token.value, transitions=self._parse_grammar_list())

        return state

    def _parse_grammar_list(self) -> List[List[Token]]:
        grammar_token_list = [self._parse_grammar_atomic()]

        while self.peek(ttypes.OR):
            self.consume(ttypes.OR)
            grammar_token_list.append(self._parse_grammar_atomic())

        return grammar_token_list

    def _parse_grammar_atomic(self) -> List[Token]:
        token_list = []
        while self.peek([ttypes.AUTOMATON_STATE, ttypes.AUTOMATON_TOKEN]):
            token_list.append(self.consume([ttypes.AUTOMATON_STATE, ttypes.AUTOMATON_TOKEN]))

        if self.peek(ttypes.EPSILON):
            token_list.append(self.consume(ttypes.EPSILON))
        if not token_list:
            raise UnexpectedTokenTypeException(f"Expected token type {ttypes.AUTOMATON_STATE} but got NONE.")
        return token_list

    def consume(self, expected_type: Union[str, List[str]]) -> Token:
        expected_type = [expected_type] if isinstance(expected_type, str) else expected_type
        token = self.tokens.pop(0)

        if token.token_type in expected_type:
            return token
        else:
            raise UnexpectedTokenTypeException(f"Expected token type {expected_type} but got {token.token_type}")

    def peek(self, expected_type: Union[str, List[str]]) -> bool:
        expected_type = [expected_type] if isinstance(expected_type, str) else expected_type
        return self.tokens and self.tokens[0].token_type in expected_type
