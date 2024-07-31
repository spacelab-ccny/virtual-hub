If you want to run the computation between devices that require some sort of network connection, do as follows:
1. Create the file input.xml with each deice name, placeholders for possible state values it would pass in, dependencies, and thresholds to change the device state based on dependecies. Don't actually put in the numerical values. Create the appropriate tags and leave them blank. This file should exist on every device you use in the MPC.

2. On each device separately, using the same outline as for the input.xml, name a device#_input.xml file fill out the numerical values relevant to that device. Note, here # should be replaced with the number of that device (starting from 1 onwards).

3. On each device separately, run "python3 arg_process_xml.py". It'll automatically read from input.xml and generate the script needed for our mpc computation.

4. On each device separately, run "bash run_mpc.sh $DEVICE_NUM $PID_LIST". The $DEVICE_NUM argument should be the number you assigned to the deivce (1,2,3,..etc) and the $PID_LIST argument should be a comma separated list (no spaces) of the pids of each of the other devices in the MPC. Note, don't include the PID of the deivce you run this on in this list.

5. If done properly, after the last device runs the above command the MPC computation should take place.