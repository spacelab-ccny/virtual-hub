#!/bin/bash
args=("$@")
#should be able to pass in the device number and the list of PIDs of the other device separated by commas
num=$[${args[0]} - 1 ]
pid_list=`python3 pid_command.py -n ${num} -p ${args[1]}`
echo $pid_list

touch device1_time.txt
touch device1_bytes.txt
touch device2_time.txt
touch device2_bytes.txt

for i in $(seq 1 10);
do
    python3 generate_command.py -i device${args[0]}_input.xml -n ${num} -p "${pid_list}"
    bash device${args[0]}_command.sh ${num}
done