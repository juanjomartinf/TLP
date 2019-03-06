from typing import Dict, List
from automaton4u.parser.parser import AutomatonState, Parser
from automaton4u.tokenizer import Tokenizer

"""
Example code:
    https://github.com/pytransitions/transitions/blob/master/examples/Graph%20MIxin%20Demo%20Nested.ipynb
    https://github.com/pytransitions/transitions/blob/master/examples/Graph%20MIxin%20Demo.ipynb
"""

def get_states(parent_state: AutomatonState, states: Dict[str, AutomatonState]) -> Dict[str, AutomatonState]:
    for state_name, state in parent_state.other_automaton_states.items():
        if state_name not in states:
            states[state_name] = state
            states = {**states, **get_states(state, states)}

    return states

def get_transitions(states: Dict[str, AutomatonState]) -> List[List]:
    transitions = list()
    for state_name, state in states.items():
        for transition in state.transitions:
            if len(transition) == 2:
                transitions.append([transition[0].value, state.state_name, transition[1].value])

    return transitions

def draw(automaton_state: AutomatonState):
    automaton_states = dict()
    automaton_states[automaton_state.state_name] = automaton_state
    automaton_states = {**automaton_states, **get_states(automaton_state, automaton_states)}

    states = sorted(automaton_states.keys())
    transitions = get_transitions(automaton_states)

    print(states)
    print(transitions)


grammar = 'A -> aB | bC \n C -> aC | bC | cB \n B -> bB | aD | a \n D -> aD | a | bB'
tokens = Tokenizer(grammar).tokenize()
result = Parser(tokens).parse()
draw(result)
