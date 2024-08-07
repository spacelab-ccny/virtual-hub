#!/bin/bash
args=("$@")
python3 arg_comp.py -P 100.84.161.127 -P 100.83.110.106 -P localhost  -I${args[0]} 90 >> device3_out.txt
cat  device3_out.txt | grep 'runtime' | awk '{print$2}' >> device3_time2.txt
cat  device3_out.txt | grep 'mem' | awk '{print$2}' >> device3_mem.txt
cp device3_input.xml  device3_output.xml
python3 process_output.py -i device3_out.txt -n 2 -f device3_output.xml
cat  device3_out.txt | grep 'TIME' | awk '{print$2}' >> device3_time.txt
cat  device3_out.txt | grep 'bytes sent' | awk '{print$10}' >> device3_bytes.txt
cat  device3_out.txt | grep 'RSS' | awk '{print$2}' >> device3_rss.txt
cat  device3_out.txt | grep 'VMS' | awk '{print$2}' >> device3_vms.txt
cat  device3_out.txt | grep 'USS' | awk '{print$2}' >> device3_uss.txt
rm device3_out.txt
cp device3_output.xml device3_input.xml