#!/bin/python3
#File used to process input xml file and generate a python script that uses mpyc to create a multiparty computation scheme between all involved devices
#what we need from the xml
#number of parties
#initial arguments for each party
#the rules for each party
#a way to check the conditions of the rules for each party

#current plan is to have each device's individual xml file eb the same as the initial xml file but with 0s where it doesn't need the values
#if we instead have each xml only including the information relevant to that device it won't know how many arguments to pass in
#process:
#intial xml file used to generate the computation script
#python script that process initial xml and generates computation python script
#at this point we have a computation script that can be run with the appropriate number of parties and arguments passed in

from bs4 import BeautifulSoup
 #taken from https://www.geeksforgeeks.org/reading-and-writing-xml-files-in-python/
 
# Reading the data inside the xml
# file to a variable under the name 
# data
with open('input.xml', 'r') as f:
    data = f.read()
 
# Passing the stored data inside
# the beautifulsoup parser, storing
# the returned object 
soup = BeautifulSoup(data, "xml")
 
num_devices= len(soup .find_all('device'))
print(num_devices)
 
# Using find() to extract attributes the function
# of the first instance of the tag
b_name = soup .find('device', {'id':'1'})
val = b_name.find('deviceName').text
print(val)


b_name = soup.find('device', {'id':'3'})
val = b_name.find('depGroup', {'id':'1'})
gfg = soup.find(lambda tag: tag.name == "deviceName" and 'Fan' in tag.text)


 
print(val)
#print(gfg.parent)

#writing the python file:
f  = open('command.sh', 'w')
f.write("#!/bin/bash\n")
f.write("args=(\"$@\")\n")
#f.write("\n\tif mpc.parties != {}:\n\t\tprint(\"Did not reach expected number of parties. Expected \", await mpc.output({}))\n".format(num_devices, num_devices))

count = 0
name_list = []
arg_list = []

#looping through the devices and creating a variable in the output script for each argument
f.write(f"python3 arg_comp.py -M{num_devices} -I${{args[0]}}")
for i in range(num_devices):
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
    
#now we need to retrieve each of the conditions to change the state of each argument of each device:
#first we retrieve the dependencies of the device
for dev in range(len(name_list)):
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
        state = dep_group.find('stateChange')['num']
        curr_dev = name_list[dev-1]+str(state)+"_combined"
        dep_devs=dep_group.find_all('depDevice')

        for ddev in range(len(dep_devs)):
            try:
                upper = dep_group.find('upperThreshold',{'arg':ddev+1}).text
                f.write(f"{upper}")

            except:
                upper = 0
                f.write(f"{upper}")
            try:
                lower = dep_group.find('lowerThreshold',{'arg':ddev+1}).text
                f.write(f"{lower}")
                if thresh ==-1:
                    thresh = 1
            except:
                thresh =0
                lower = 0
                

f.close()
 
 
