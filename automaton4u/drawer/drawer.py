from typing import Dict, List
from automaton4u.parser.parser import AutomatonState, Parser
from automaton4u.tokenizer import Tokenizer, ttypes, Token

import os, sys, inspect, io

cmd_folder = os.path.realpath(
    os.path.dirname(
        os.path.abspath(os.path.split(inspect.getfile(inspect.currentframe()))[0])))

if cmd_folder not in sys.path:
    sys.path.insert(0, cmd_folder)

from transitions.extensions import MachineFactory

"""
Example code:
    https://github.com/pytransitions/transitions/blob/master/examples/Graph%20MIxin%20Demo%20Nested.ipynb
    https://github.com/pytransitions/transitions/blob/master/examples/Graph%20MIxin%20Demo.ipynb
"""


class Matter(object):
    def is_hot(self):
        return True

    def is_too_hot(self):
        return False

    def show_graph(self, **kwargs):
        # print(self.get_graph(**kwargs).string())
        stream = io.BytesIO()
        self.get_graph(**kwargs).draw(stream, prog='dot', format='png')
        return stream.getvalue()


def get_states(parent_state: AutomatonState, states: Dict[str, AutomatonState]) -> Dict[str, AutomatonState]:
    for state_name, state in parent_state.other_automaton_states.items():
        if state_name not in states:
            states[state_name] = state
            states = {**states, **get_states(state, states)}

    return states


def get_transitions(states: Dict[str, AutomatonState]) -> List[List]:
    transitions = list()
    states['FINAL'] = AutomatonState(state_name="FINAL")
    pocessed_states = list(states.keys())
    i = 0
    for state_name, state in states.items():
        for transition in state.transitions:
            transition_buffer = []
            last_transition = transition.pop(0)
            last_state = state


            while transition:
                sub_transition = transition.pop(0)
                if last_transition.token_type == sub_transition.token_type == ttypes.AUTOMATON_TOKEN:
                    transition_buffer.append([last_transition.value, last_state.state_name, f"I{i}"])
                    last_state = AutomatonState(state_name=f'I{i}')
                    pocessed_states.append(last_state.state_name)
                    i += 1
                else: # aA
                    transition_buffer.append([last_transition.value, last_state.state_name, sub_transition.value])
                last_transition = sub_transition

            if last_transition.token_type == ttypes.AUTOMATON_TOKEN:
                transition_buffer.append([last_transition.value, last_state.state_name, states['FINAL'].state_name])
            elif len(transition_buffer) == 0 and last_transition.token_type == ttypes.AUTOMATON_STATE:
                transition_buffer.append(["€", last_state.state_name, last_transition.value])
            elif len(transition_buffer) == 0 and last_transition.token_type == ttypes.EPSILON:
                transition_buffer.append(["€", last_state.state_name, states['FINAL'].state_name])

            transitions += transition_buffer


    return pocessed_states, transitions


def draw(automaton_state: AutomatonState):
    automaton_states = dict()
    automaton_states[automaton_state.state_name] = automaton_state
    automaton_states = {**automaton_states, **get_states(automaton_state, automaton_states)}

    states, transitions = get_transitions(automaton_states)

    graph_machine = MachineFactory.get_predefined(graph=True, nested=True)

    model = Matter()
    machine = graph_machine(model=model,
                            states=states,
                            transitions=transitions,
                            auto_transitions=False,
                            initial=states[0],
                            title="Automaton",
                            show_conditions=True)
    return model.show_graph()
