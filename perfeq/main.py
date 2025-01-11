import sys

import pyfiglet

from perfeq.analyzer.perfeq import Perfeq


def analyze():
    """
    Analyzes the input file/path provided as a command-line argument.
    This function expects a file path to be passed as the first command-line argument.
    If no argument is provided, it raises a ValueError. It then creates an instance
    of the Perfeq class with the provided path and calls its analyze method.
    Raises:
        ValueError: If no input file/path is provided as a command-line argument.
    """
    args = sys.argv

    if len(args) == 1:
        raise ValueError("No input file/path was provided")

    path = args[1]
    
    perfeq = Perfeq(path)
    perfeq.analyze()
    



if __name__ == "__main__":
    
    print(pyfiglet.figlet_format("PerfeQ", font="slant"))
    analyze()