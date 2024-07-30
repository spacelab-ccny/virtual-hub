#!/bin/bash
args=("$@")
python3 arg_comp.py -M3 -I${args[0]} 10 >> device3_input.txt