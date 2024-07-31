#!/bin/bash
args=("$@")
python3 arg_comp.py -P localhost -P 00.00101.11 -P 22.2212.1  -I${args[0]} 7 8 9