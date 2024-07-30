#!/bin/python3

from bs4 import BeautifulSoup
import argparse


def generate_command (input_file, num):
    #inspired by code from https://www.geeksforgeeks.org/reading-and-writing-xml-files-in-python/
    with open(input_file, 'r') as f:
        data = f.read()

    soup = BeautifulSoup(data, "xml")
    
    num_devices= len(soup .find_all('device'))
    print(num_devices)

    #writing the python file:
    f  = open(f'{input_file[0:-9]}command.sh', 'w')
    f.write("#!/bin/bash\n")
    f.write("args=(\"$@\")\n")
    #f.write("\n\tif mpc.parties != {}:\n\t\tprint(\"Did not reach expected number of parties. Expected \", await mpc.output({}))\n".format(num_devices, num_devices))

    count = 0
    name_list = []
    arg_list = []
    dev_arg_list = []

    #looping through the devices and creating a variable in the output script for each argument
    f.write(f"python3 arg_comp.py -M{num_devices} -I${{args[0]}}")
    for i in range(num_devices):
        temp_arr = []
        i = 1+i
        b_name = soup.find('device', {'id':i})
        name = b_name.find('deviceName').text
        args =(b_name.find_all('argument'))
        print(args)
        name_list = name_list + [name]
        for arg in args:
            argval = arg.find('argVal').text
            count = count +1
            f.write(f" {argval}")
            temp_arr = temp_arr + [argval]
        dev_arg_list = dev_arg_list +[temp_arr]
    print(f"DEVICE\n{dev_arg_list}")
        
    #now we need to retrieve each of the conditions to change the state of each argument of each device:
    #first we retrieve the dependencies of the device

    dep_list = []
    for dev in range(len(name_list)):
        temp_arr = []
        dev =dev+1
        device = soup.find('device', {'id':str(dev)})
        #print(device)
        dependencies = device.find_all('depGroup')
        num_dep = len(dependencies)
        #list storing the threshold truths to "OR"
        or_list = []

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
                try:
                    upper = dep_group.find('upperThreshold',{'arg':ddev+1}).text
                    f.write(f" {upper}")
                    temp_arr = temp_arr + [upper]
                    print("upper")

                except:
                    upper = 0
                    f.write(f" {upper}")
                try:
                    lower = dep_group.find('lowerThreshold',{'arg':ddev+1}).text
                    f.write(f" {lower}")
                    if thresh ==-1:
                        thresh = 1
                    temp_arr = temp_arr + [lower]
                    print("lower")

                except:
                    thresh =0
                    lower = 0
                print(temp_arr)

            for state in states:
                f.write(f" {state.text}")
                temp_arr = temp_arr + [state.text]
        dep_list = dep_list + [temp_arr]

    print(dep_list)
    f.close()
 
if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument('-i', action='store', dest='input_file', default="device1_input.xml",
                        help='Pass in the xml file corresponding to this device', type=str)
    parser.add_argument('-n', action='store', dest='device_num', default="0",
                        help='Pass in the mpc.id corresponding to this device', type=str)
    results = parser.parse_args()
    input_file = results.input_file
    device_num = results.device_num
    generate_command(input_file, device_num)
    
