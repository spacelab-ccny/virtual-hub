#!/bin/bash
args=("$@")
python3 arg_comp.py -M3 -I${args[0]} 1 11 2 2 3 4 44 5 6 >> device1_input.txt