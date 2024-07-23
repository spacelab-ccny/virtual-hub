#!/bin/bash
  
#gnome-terminal -e cat test.txt&
#gnome-terminal -e cat test2.txt &

gnome-terminal -- bash -c "python3 generate_command.py; bash command.sh 0; exec bash"
gnome-terminal -- bash -c "python3 generate_command.py; bash command.sh 1; exec bash"
gnome-terminal -- bash -c "python3 generate_command.py; bash command.sh 2; exec bash"
gnome-terminal -- bash -c "python3 generate_command.py; bash command.sh 3; exec bash"