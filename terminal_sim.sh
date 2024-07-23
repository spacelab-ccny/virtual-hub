#!/bin/bash
  
#gnome-terminal -e cat test.txt&
#gnome-terminal -e cat test2.txt &

gnome-terminal -- bash -c "python3 generate_command.py -i device1_input.xml; bash device1_command.sh 0; exec bash"
gnome-terminal -- bash -c "python3 generate_command.py -i device2_input.xml; bash device2_command.sh 1; exec bash"
gnome-terminal -- bash -c "python3 generate_command.py -i device3_input.xml; bash device3_command.sh 2; exec bash"