# Automaton for you!

The framework for creating automatons for an already defined grammar
(University project)

# Installation

`sudo apt-get install python-dev graphviz libgraphviz-dev pkg-config`

Then, create a python 3.6 virtual environment:

`python3.6 -m virtualenv env` && `source env/bin/activate`

Finally, install all dependencies needed:

`pip install transitions pygraphviz`


# How to use

At the moment, only the screenshot of the automaton is drawn.

To do that, first write in a file called `grammar.a4u` your grammar definition:
```
A -> aB | bC
C -> aC | bC | cB
B -> bB | aD | a
D -> aD | a | bB
```

Then, use the `cli.py` tool to create the photo like this:

`python cli.py grammar.a4u --output_screenshot grammar.png`

The script will generate a photo containing a view of the graph in the `grammar.png` file.
