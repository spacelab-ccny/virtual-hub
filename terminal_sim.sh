#!/bin/bash
  
#gnome-terminal -e cat test.txt&
#gnome-terminal -e cat test2.txt &

#python3 arg_process_xml.py
touch device1_time.txt
touch device1_bytes.txt
touch device1_rss.txt
touch device1_vms.txt
touch device1_uss.txt

touch device2_time.txt
touch device2_bytes.txt
touch device2_rss.txt
touch device2_vms.txt
touch device2_uss.txt

for i in $(seq 1 1);
do
    gnome-terminal -- bash -c "python3 generate_command.py -i device1_input.xml -n 0; bash device1_command.sh 0; exec bash;"
    gnome-terminal -- bash -c "python3 generate_command.py -i device2_input.xml -n 1; bash device2_command.sh 1; exec bash;"
#gnome-terminal -- bash -c "python3 generate_command.py -i device3_input.xml -n 2; bash device3_command.sh 2;exec bash;"
    sleep 4
done