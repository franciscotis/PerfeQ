import sys

from perfeq.analyzer.perfeq import Perfeq


def analyze():
    args = sys.argv

    if len(args) == 1:
        raise ValueError("No input file/path was provided")

    path = args[1]
    
    perfeq = Perfeq(path)
    perfeq.analyze()
    


if __name__ == "__main__":
    analyze()