#!/bin/bash
  
args=("$@")
#should be able to pass in the device number and the list of PIDs of the other device separated by commas
num=$[${args[0]} - 1 ]
pid_list=`python3 pid_command.py -n ${num} -p ${args[1]}`
echo $pid_list
gnome-terminal -- bash -c "python3 generate_command.py -i device${args[0]}_input.xml -n ${args[0]-1} -p \"${pid_list}\"; bash device1_command.sh 0 ;exec bash;"