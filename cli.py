import sys
import argparse


from automaton4u.drawer.drawer import draw
from automaton4u.parser.parser import Parser
from automaton4u.tokenizer import Tokenizer

if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    parser.add_argument("grammar_file", help="Input file containing the grammar definition.")
    parser.add_argument("--output_screenshot", help="Output file containing a graph view of the generated automaton")
    args = parser.parse_args()

    grammar = args.grammar_file
    output_file = args.output_screenshot or grammar.replace("a4u", 'png')


    with open(args.grammar_file) as input_file:
        input_grammar = input_file.read().strip()

    tokens = Tokenizer(input_grammar).tokenize()
    automaton_states = Parser(tokens).parse()
    output_bytes = draw(automaton_states)

    with open(output_file, 'wb') as output_file:
        output_file.write(output_bytes)
