#!/bin/python3
#File used to process input xml file and generate a python script that uses mpyc to create a multiparty computation scheme between all involved devices
#what we need from the xml
#number of parties
#initial arguments for each party
#the rules for each party
#a way to check the conditions of the rules for each party


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
f  = open('dummy.py', 'w')
f.write("from mpyc.runtime import mpc\nimport sys\n\nasync def main():\n\tsecint = mpc.SecInt(16)\n\tawait mpc.start()")
f.write("\n\tif mpc.parties != {}:\n\t\tprint(await mpc.output(\'Expected {} parties. Try again.\'))\n".format(num_devices, num_devices))

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
        f.write("\n\t{}{} = secint(int(sys.argv[{}])) if sys.argv[{}:] else 0".format(name,j,count,count))
        arg_list = arg_list + [name+str(j)]
print(name_list)
f.write("\n")
for i in range(len(arg_list)):
    f.write("\n\t{}_combined = sum(mpc.input({}, range(mpc.parties)))".format(arg_list[i],arg_list[i]))
    
f.write("\n")
#now we need to retrieve each of the conditions to change the state of each argument of each device:
#first we retrieve the dependencies of the device
for dev in range(len(name_list)):
    dev =dev+1
    device = soup.find('device', {'id':str(dev)})
    #print(device)
    dependencies = device.find_all('depGroup')
    num_dep = len(dependencies)
    print(num_dep)
#then, while depGroup with id "i" exists:
    for dep in range(num_dep):
        dep = dep+1
#Get vaule of variable with devicename.text+decvicenamenum
        dep_group = device.find('depGroup', {'id':str(dep)})
        state = dep_group.find('stateChange')['num']
        print(f"state {state}")
        curr_dev = name_list[dev-1]+str(state)+"_combined"
        print(curr_dev)
#read in thresholds into secure variables-- can't do this because the value will be dispalyed in the python script
        #print(dep_group)
        dep_devs=dep_group.find_all('depDevice')
        #print(dep_devs)
        for ddev in range(len(dep_devs)):
            cur_dep= dep_devs[ddev].text+dep_devs[ddev]['num']+'_combined'
            print(cur_dep)
            thresh =-1
            try:
                upper = dep_group.find('upperThreshold',{'arg':ddev+1}).text
                f.write("\n\tutruth = -1")
                thresh =2
                f.write(f"\n\tutruth =  {cur_dep} <  secint({upper})")
            except:
                upper = 'none'
            try:
                lower = dep_group.find('lowerThreshold',{'arg':ddev+1}).text
                f.write("\n\tltruth = -1")
                f.write(f"\n\tltruth = {cur_dep} > secint({lower})")
                if thresh ==-1:
                    thresh = 1
            except:
                thresh =0
                lower = 'none'
            if(thresh==2):
                f.write("\n")
                f.write(f"\n\tin_range = ltruth and utruth")
                f.write("\n")
            print(f"upper {upper} lower {lower}")
            f.write("\n")
#if its less than upperThreshold arg=i set "truth" variable to true

#if lowerThreshold arg=i (check existence becuase it might not have both) keep previous variable at true


#if "truth" changes the value of variable with nameList[i]+stateChange num+combined to be the desired value
    



#shutdown mpc and call main to end file
f.write("\n\tawait mpc.shutdown()\nmpc.run(main())")
f.close()
 
 
