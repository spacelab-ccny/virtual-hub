#!/bin/bash
args=("$@")
python3 arg_comp.py -M3 -I${args[0]} 7 8 9 >> device2_input.txt