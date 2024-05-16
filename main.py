import os
import sys
import numpy as np

from mySolver.Reader import Reader


if __name__ == "__main__":

    input_file  = sys.argv[1]
    output_file = sys.argv[2]

    analysis = Reader(input_file).export()
    analysis.analyze()
    analysis.write(output_file)
