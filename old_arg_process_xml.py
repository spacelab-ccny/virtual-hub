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

#writing the python file:
f  = open('arg_comp.py', 'w')
f.write("#!/bin/python3")
f.write("\nfrom mpyc.runtime import mpc\nimport sys\n\nasync def main():\n\tsecint = mpc.SecInt(16)\n\tawait mpc.start()")
#f.write("\n\tif mpc.parties != {}:\n\t\tprint(\"Did not reach expected number of parties. Expected \", await mpc.output({}))\n".format(num_devices, num_devices))

count = 0
name_list = []
arg_list = []

#looping through the devices and creating a variable in the output script for each argument
for i in range(num_devices):
    i = 1+i
    b_name = soup.find('device', {'id':i})
    name = b_name.find('deviceName').text
    num_args = len(b_name.find_all('argument'))
    name_list = name_list + [name]
    for j in range(num_args):
        j=j+1
        count = count +1
        f.write("\n\t{}{} = secint(int(sys.argv[{}])) if sys.argv[{}:] else secint(0)".format(name,j,count,count))
        arg_list = arg_list + [name+str(j)]
print(name_list)
f.write("\n")
for i in range(len(arg_list)):
    f.write("\n\t{}_combined = sum(mpc.input({}, range({})))".format(arg_list[i],arg_list[i], num_devices))
    
f.write("\n")
#now we need to retrieve each of the conditions to change the state of each argument of each device:
#first we retrieve the dependencies of the device
for dev in range(len(name_list)):
    f.write(f"\n\t#{name_list[dev]}")
    dev =dev+1
    device = soup.find('device', {'id':str(dev)})
    num_args = len(device.find_all('argument'))
    for j in range(num_args):
        j=j+1
        count = count +1
        f.write("\n\t{}{} = None".format(name,j))
        #f.write("\n\t{}{} = secint(int(sys.argv[{}])) if sys.argv[{}:] else secint(0)".format(name,j,count,count))
        arg_list = arg_list + [name+str(j)]
    #print(device)
    dependencies = device.find_all('depGroup')
    num_dep = len(dependencies)
    print(num_dep)
    #list storing the threshold truths to "OR"
    or_list = []

#then, while depGroup with id "i" exists:
    for dep in range(num_dep):
        
        dep = dep+1
        f.write(f"\n\t#Dependency {dep}")
#Get vaule of variable with devicename.text+decvicenamenum
        dep_group = device.find('depGroup', {'id':str(dep)})
        dep_devs=dep_group.find_all('depDevice')
        #print(dep_devs)

        for ddev in range(len(dep_devs)):
            cur_dep= dep_devs[ddev].text+dep_devs[ddev]['num']+'_combined'
            print(cur_dep)
            thresh =-1
            try:
                upper = dep_group.find('upperThreshold',{'arg':ddev+1}).text
                #f.write(f"\n\tutruth{dep} = -1")
                thresh =2
                count = count +1
                #f.write("\n\tupper{} = secint(int(sys.argv[{}])) if sys.argv[{}:] else secint(0)".format(dep, count, count))
                f.write("\n\tupper{} = None".format(dep))
                #f.write("\n\tupper{} = sum(mpc.input(upper{}, range({})))".format(dep, dep, num_devices))
                #f.write(f"\n\tutruth{dep} =  {cur_dep} <  upper{dep}")
                or_list = or_list +["utruth"+str(dep)]

            except:
                upper = 'none'
            try:
                lower = dep_group.find('lowerThreshold',{'arg':ddev+1}).text
                #f.write(f"\n\tltruth{dep} = -1")
                count = count +1
                #f.write("\n\tlower{} = secint(int(sys.argv[{}])) if sys.argv[{}:] else secint(0)".format(dep, count, count))
                f.write("\n\tlower{} = None".format(dep))
                #f.write("\n\tlower{} = sum(mpc.input(lower{}, range({})))".format(dep, dep, num_devices))
                #f.write(f"\n\tltruth{dep} = {cur_dep} > lower{dep}")
                or_list = or_list +["ltruth"+str(dep)]
                if thresh ==-1:
                    thresh = 1
            except:
                thresh =0
                lower = 'none'
            if(thresh==2):
                #f.write("\n")
                or_list = or_list[:-2]
                #f.write(f"\n\tin_range{dep} = ltruth{dep} * utruth{dep}")
                or_list = or_list +["in_range"+str(dep)]
                #f.write("\n")
                
            print(f"upper {upper} lower {lower}")
            f.write("\n")

        dep_str =''
        for truth_val in or_list[len(or_list)-len(dep_devs):]:
            dep_str = dep_str + truth_val +' + '
        dep_str = "("+dep_str[:-3]+")"
        print(dep_str)
        or_list = or_list[:-len(dep_devs)]
        or_list = or_list + [dep_str]

        states = dep_group.find('stateChange')
        print(f"state {states}")
        state_count = 0
        f.write(f"\n\ttruth = {dep_str}")
        for state in states:
            count = count+1
            f.write("\n\t{}_state{}_{} = secint(int(sys.argv[{}])) if sys.argv[{}:] else secint(0)".format(name_list[dev-1], int(state)+1, dep, count, count))
            f.write("\n\t{}_state{}_{} = sum(mpc.input({}_state{}_{}, range({})))".format(name_list[dev-1], int(state)+1, dep, name_list[dev-1], int(state)+1, dep, num_devices))
            f.write("\n\t{}_state{}_{}_change = truth * {}_state{}_{}".format(name_list[dev-1], int(state)+1, dep, name_list[dev-1], int(state)+1, dep))
            f.write(f"\n\tif mpc.pid == {dev-1}:")
            f.write("\n\t\tprint('{}_state{}_{}:',await mpc.output({}_state{}_{}_change))".format(name_list[dev-1], int(state)+1, dep, name_list[dev-1], int(state)+1, dep))
        

    cond_str = ''
    for truth_val in or_list:
        cond_str = cond_str + truth_val +' + '
    cond_str = cond_str[:-3]
    print(cond_str)


#shutdown mpc and call main to end file
f.write("\n\tawait mpc.shutdown()\nmpc.run(main())")
f.close()
 
 
