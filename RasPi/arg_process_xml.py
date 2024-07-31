#!/bin/python3
#Current plan: anywhere we write the conditional comparison to the file, we now, instead, just store the string in a list. Then at the end we can just iterate through that list of strings and write them all

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
f.write("\nfrom mpyc.runtime import mpc\nimport time\nimport sys\n\nasync def main():\n\tsecint = mpc.SecInt(16)")
#f.write("\n\tif mpc.parties != {}:\n\t\tprint(\"Did not reach expected number of parties. Expected \", await mpc.output({}))\n".format(num_devices, num_devices))

count = 0
name_list = []
arg_list = []
complete_var_list=[]
all_state_changes=[]

all_comp=[]

#looping through the devices and creating a variable in the output script for each argument
for i in range(num_devices):
    i = 1+i
    b_name = soup.find('device', {'id':i})
    name = b_name.find('deviceName').text
    num_args = len(b_name.find_all('argument'))
    name_list = name_list + [name]
    
    
f.write("\n")
#now we need to retrieve each of the conditions to change the state of each argument of each device:
#first we retrieve the dependencies of the device
for dev in range(len(name_list)):
    var_list = []
    comparison_list = []
    #state_changes =[]
    f.write(f"\n\t#{name_list[dev]}")
    dev =dev+1
    device = soup.find('device', {'id':str(dev)})
    num_args = len(device.find_all('argument'))
    for j in range(num_args):
        j=j+1
        count = count +1
        f.write("\n\t{}{} = None".format(name_list[dev-1],j))
        var_list = var_list +[f"{name_list[dev-1]}{j}"]
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
        #temp_state_list = []
        dep = dep+1
        f.write(f"\n\t#Dependency {dep}")
#Get vaule of variable with devicename.text+decvicenamenum
        dep_group = device.find('depGroup', {'id':str(dep)})
        dep_devs=dep_group.find_all('depDevice')
        #print(dep_devs)

        for ddev in range(len(dep_devs)):
            cur_dep= dep_devs[ddev].text+dep_devs[ddev]['num']
            print(cur_dep)
            state_changes =[]
            thresh =-1
            try:
                upper = dep_group.find('upperThreshold',{'arg':ddev+1}).text
                #f.write(f"\n\tutruth{dep} = -1")
                thresh =2
                count = count +1
                #f.write("\n\tupper{} = secint(int(sys.argv[{}])) if sys.argv[{}:] else secint(0)".format(dep, count, count))
                f.write("\n\t{}_upper{}_{} = None".format(name_list[dev-1],dep,ddev))
                var_list = var_list +[f"{name_list[dev-1]}_upper{dep}_{ddev}"]
                #f.write("\n\tupper{} = sum(mpc.input(upper{}, range({})))".format(dep, dep, num_devices))
                comparison_list = comparison_list + [f"\n\t\tutruth{dep} =  {cur_dep} <{name_list[dev-1]}_upper{dep}_{ddev}"]
                #f.write(f"\n\tutruth{dep} =  {cur_dep} <  upper{dep}")
                or_list = or_list +["utruth"+str(dep)]

            except:
                upper = 'none'
            try:
                lower = dep_group.find('lowerThreshold',{'arg':ddev+1}).text
                #f.write(f"\n\tltruth{dep} = -1")
                count = count +1
                #f.write("\n\tlower{} = secint(int(sys.argv[{}])) if sys.argv[{}:] else secint(0)".format(dep, count, count))
                f.write("\n\t{}_lower{}_{} = None".format(name_list[dev-1],dep, ddev))
                var_list = var_list +[f"{name_list[dev-1]}_lower{dep}_{ddev}"]
                #f.write("\n\tlower{} = sum(mpc.input(lower{}, range({})))".format(dep, dep, num_devices))
                #f.write(f"\n\tltruth{dep} = {cur_dep} > lower{dep}")
                comparison_list = comparison_list + [f"\n\t\tltruth{dep} =  {cur_dep} > {name_list[dev-1]}_lower{dep}_{ddev}"]
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
                comparison_list = comparison_list + [f"\n\t\tin_range{dep} = ltruth{dep} == utruth{dep}"]
                comparison_list = comparison_list + [f"\n\t\tin_range{dep} = in_range{dep} == secint(1)"]
                or_list = or_list +["in_range"+str(dep)]
                #f.write("\n")
                
            print(f"upper {upper} lower {lower}")
            f.write("\n")

        dep_str =''
        for truth_val in or_list[len(or_list)-len(dep_devs):]:
            dep_str = dep_str + truth_val +' * '
        dep_str = "("+dep_str[:-3]+")"
        print(dep_str)
        or_list = or_list[:-len(dep_devs)]
        or_list = or_list + [dep_str]

        states = dep_group.findAll('stateChange')
        print(f"state {states}")
        state_count = 0
       # f.write(f"\n\ttruth = {dep_str}")
        comparison_list = comparison_list + [f"\n\t\ttruth{dev}_{dep-1} = {dep_str}"]
        for state in states:
            count = count+1
            state = state['num']
            f.write("\n\t{}_state{}_{} = None".format(name_list[dev-1], dep,state))
            var_list = var_list +[f"{name_list[dev-1]}_state{dep}_{state}"]
            state_changes = state_changes + [f"{name_list[dev-1]}_state{dep}_{state}"]

        all_state_changes = all_state_changes +[state_changes]
        #print(f"temp:\n {temp_state_list}")
        

    cond_str = ''
    for truth_val in or_list:
        cond_str = cond_str + truth_val +' + '
    cond_str = cond_str[:-3]
    print(cond_str)

    complete_var_list = complete_var_list +[var_list]
    #all_state_changes = all_state_changes + [temp_state_list]
    all_comp = all_comp+[comparison_list]


for dev in range(len(name_list)):
    if dev == 0:
        f.write(f"\n\tif mpc.pid == 0:")
    else:
        f.write(f"\n\telif mpc.pid == {dev}:")
    counter =1
    for var in complete_var_list[dev]:
        f.write(f"\n\t\t{var} = int(sys.argv[{counter}])")
        counter = counter +1

f.write("\n\n\tstart=0\n\tasync with mpc:\n\t\tstart=time.time()")
for dev in range(len(name_list)):
    counter =0
    for var in complete_var_list[dev]:
        f.write(f"\n\t\t{var} = mpc.input(secint({var}), {dev})")
        counter = counter +1

f.write("\n")
print("ALL state changes:")
print(f"{all_state_changes}")
print(f"COMP:\n{all_comp}")
dep =0
for i in range(len(all_comp)):
    counting=0
    for comp in all_comp[i]:
        count = 0
        f.write(f"{comp}")
        if(comp[:8]== f"\n\t\ttruth"):
            print(f"TRUE:\n{comp}")
            for state in all_state_changes[dep]:
                #f.write(f"\n\t\tout = await mpc.output(mpc.if_else(truth,{all_state_changes[i][count]} , None), {i})\n")
                #f.write(f"\n\n\t\tout{i+1}_{dep}_{count} = await mpc.output(truth{i+1}_{counting}*{state}, {i})")
                name,var, val = state.split('_')
                f.write(f"\n\n\t\tout{i+1}_{dep}_{count} = await mpc.output(mpc.if_else(truth{i+1}_{counting}, {state}, {name}{val} ), {i})")

                f.write(f"\n\t\tif mpc.pid == {i}:")
                f.write(f"\n\t\t\tprint(f\"output {all_state_changes[dep][count]} {{out{i+1}_{dep}_{count}}}\")\n")
                count = count+1
            counting = counting+1
            dep = dep+1

#print(complete_var_list)
#shutdown mpc and call main to end file
f.write("\n\t\tend=time.time()")
f.write("\n\t\ttotal=end-start")
f.write("\n\t\tprint(f\"TIME: {total}\")")
f.write("\nmpc.run(main())")

 
 
