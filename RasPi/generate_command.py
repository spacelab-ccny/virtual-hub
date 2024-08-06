#!/bin/python3

from bs4 import BeautifulSoup
import argparse


def generate_command (input_file, num, pid_list):
    #inspired by code from https://www.geeksforgeeks.org/reading-and-writing-xml-files-in-python/
    with open(input_file, 'r') as f:
        data = f.read()

    soup = BeautifulSoup(data, "xml")
    
    device= soup .find('device', {'id':num+1})
    print(device)

    num_devices = len(soup.findAll('device'))
    #writing the python file:
    f  = open(f'{input_file[0:-9]}command.sh', 'w')
    f.write("#!/bin/bash\n")
    f.write("args=(\"$@\")\n")
    #f.write("\n\tif mpc.parties != {}:\n\t\tprint(\"Did not reach expected number of parties. Expected \", await mpc.output({}))\n".format(num_devices, num_devices))

    count = 0
    dev_arg_list = []
    temp_arr = []

    #looping through the devices and creating a variable in the output script for each argument
    f.write(f"python3 arg_comp.py {pid_list} -I${{args[0]}}")

    args =(device.find_all('argument'))
    print(args)
    for arg in args:
        argval = arg.find('argVal').text
        count = count +1
        f.write(f" {argval}")
        temp_arr = temp_arr + [argval]
    dev_arg_list = dev_arg_list +[temp_arr]
    print(f"DEVICE\n{dev_arg_list}")
        
   
    dependencies = device.find_all('depGroup')
    num_dep = len(dependencies)

    #then, while depGroup with id "i" exists:
    for dep in range(num_dep):
            
        dep = dep+1
#Get vaule of variable with devicename.text+decvicenamenum
        dep_group = device.find('depGroup', {'id':str(dep)})
        states = dep_group.findAll('stateChange')
        #curr_dev = name_list[dev-1]+str(state)+"_combined"
        dep_devs=dep_group.find_all('depDevice')

        for ddev in range(len(dep_devs)):
            print(f"dep.dev: {dep_devs[ddev].text}")
            print(ddev)
            try:
                upper = dep_group.find('upperThreshold',{'arg':ddev+1}).text
                f.write(f" {upper}")
                temp_arr = temp_arr + [upper]
                print("upper")

            except:
                upper = 0
            try:
                print("try2")
                lower = dep_group.find('lowerThreshold',{'arg':ddev+1}).text
                print(f"lower: {lower}")
                f.write(f" {lower}")
                print("even")
                if thresh ==-1:
                    thresh = 1
                temp_arr = temp_arr + [lower]
                print("lower")

            except:
                thresh =0
            print(temp_arr)

        for state in states:
            f.write(f" {state.text}")
            temp_arr = temp_arr + [state.text]

    print(temp_arr)
    f.write(f" >> {input_file[:-9]}out.txt")
    f.write(f"\ncat  {input_file[:-9]}out.txt | grep 'runtime' | awk '{{print$2}}' >> {input_file[:-9]}time2.txt")
    f.write(f"\ncat  {input_file[:-9]}out.txt | grep 'mem' | awk '{{print$2}}' >> {input_file[:-9]}mem.txt")
    f.write(f"\ncp {input_file}  {input_file[:-9]}output.xml")
    f.write(f"\npython3 process_output.py -i {input_file[:-9]}out.txt -n {num} -f {input_file[:-9]}output.xml")
    f.write(f"\ncat  {input_file[:-9]}out.txt | grep 'TIME' | awk '{{print$2}}' >> {input_file[:-9]}time.txt")
    f.write(f"\ncat  {input_file[:-9]}out.txt | grep 'bytes sent' | awk '{{print$10}}' >> {input_file[:-9]}bytes.txt")
    f.write(f"\ncat  {input_file[:-9]}out.txt | grep 'RSS' | awk '{{print$2}}' >> {input_file[:-9]}rss.txt")
    f.write(f"\ncat  {input_file[:-9]}out.txt | grep 'VMS' | awk '{{print$2}}' >> {input_file[:-9]}vms.txt")
    f.write(f"\ncat  {input_file[:-9]}out.txt | grep 'USS' | awk '{{print$2}}' >> {input_file[:-9]}uss.txt")
    f.write(f"\nrm {input_file[:-9]}out.txt")
    f.write(f"\ncp {input_file[:-9]}output.xml {input_file}" ) 
    #f.write(f" >> {input_file[:-4]}.txt")
    f.close()
 
if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument('-i', action='store', dest='input_file', default="device1_input.xml",
                        help='Pass in the xml file corresponding to this device', type=str)
    parser.add_argument('-n', action='store', dest='device_num', default="0",
                        help='Pass in the mpc.pid corresponding to this device', type=str)
    parser.add_argument('-p', action='store', dest='pid', default="0",
                        help='Pass in the pid corresponding to this device', type=str)
    results = parser.parse_args()
    input_file = results.input_file
    device_num = int(results.device_num)
    pid_list = results.pid
    generate_command(input_file, device_num, pid_list)
    
