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

#looping through the devices and creating a variable in the output script for each argument
for i in range(num_devices):
    i = 1+i
    b_name = soup.find('device', {'id':i})
    name = b_name.find('deviceName').text
    num_args = len(b_name.find_all('argument'))
    for j in range(num_args):
        count = count +1
        f.write("\n\t{}{} = secint(int(sys.argv[{}])) if sys.argv[{}:] else 0".format(name,j,count,count))
        name_list = name_list + [name+str(j)]
#print(name_list)
f.write("\n")
for i in range(len(name_list)):
    f.write("\n\t{}_combined = sum(mpc.input({}, range(mpc.parties)))".format(name_list[i],name_list[i]))
    

    



#shutdown mpc and call main to end file
f.write("\n\tawait mpc.shutdown()\nmpc.run(main())")
f.close()
 
 
