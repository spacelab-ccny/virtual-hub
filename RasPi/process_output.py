import argparse
from bs4 import BeautifulSoup
from lxml import etree
import random

#need to check why the output in device1_out.txt looks weird (why is one of them 2???)
#in process of passing the value it should change into into the part that writes to the file

def rand_update(device, out):
    # get values from argval, and get the type
    print("________________________________________________________________")
    args = device.findAll('argument')
    name = device.find("deviceName")
    arg_line =[]
    val_list = []
    print(args)

    for arg in args:
        val = arg.find('argVal').text
        type = arg.find('argType').text
        arg_line = arg_line + [arg.find('argVal')]
        val_list = val_list + [[val,type]]

    update = []
    for entry in val_list:
        get_prob =random.uniform(0,1)
        print
        if get_prob <0.333:
            print("ALTERED")
            if entry[1] == 'Bool':
                print(f"ENTRY: {int(entry[0])}, OPP: {not int(entry[0])}")
                entry[0] = int(not int(entry[0]))
                print(f"from {not entry[0]} to {(entry[0])}")
            elif entry[1]== 'Int':
                if get_prob < 0.165:
                    original = entry[0]
                    entry[0] = int(entry[0]) +5
                    print(f"from {original} to {(entry[0])}")

                else:
                    original = entry[0]
                    entry[0] = int(entry[0]) -5
                    print(f"from {original} to {(entry[0])}")
        update = update +[entry[0]]

    overwrite =0
    arg_index = 0
    dev_region=''
    arg_line = arg_line + ["end"]
    print("arglines:")
    print(arg_line)
    print(val_list)

    with open(out, 'r') as f:
        lines_out = f.read().splitlines()
    with open(out, 'w') as ff:
        overwrite = 0

        for line in lines_out:
            nline = line.replace(' ','')
            nline = nline.replace('\t', '')
           

            if nline == f"{str(name)}":
                dev_region = name
                print(f"DEV:{dev_region}")
                print(arg_line[arg_index])

            if(dev_region == name and nline == str(arg_line[arg_index]).replace(' ','')):
                overwrite=1
                ff.write(f"            <argVal>{update[arg_index]}</argVal>\n")
                arg_index = arg_index+1

            if(overwrite==0):
                ff.write(line+'\n')
            else:
                overwrite=0

    #if boolean take inverse
    # if integer +/-5
    # do this change like 20% of the time?
    #write the new values to the file



def process_output(filename, num, out):
    changes =[]
    input = open(filename, 'r')
    
    with open(out, 'r') as f:
        xml= f.read()
        

    soup = BeautifulSoup(xml, "xml")
    device= soup.find('device', {'id':num+1})
    name = device.find('deviceName')
   

    lines = input.readlines()
    for line in lines:
        if line[0:6]=='output':
            changes = changes +[line[7:]]

    print(changes)
    if changes==[]:
        rand_update(device, out)
        return "none"
    args = []
    vals = []
    for change in changes:
        var, val = change.split()
        var = var[var.index('state')+5:]
        dep, state = var.split('_')
        
        arg= soup.find('argument', {'num':int(state)})
        print(f"ARRRRRRR:{arg}")
        argval = arg.find('argVal').text
        print(argval)
        a = str(arg).split('\n')
        if val != argval:
            args = args +[a[:2]]
            vals = vals + [val]

    print(args)
    print(vals)
    if vals == []:
        rand_update(device, out)
        return "none"
    no_dup_args = set()
    no_dup_vals = set()
    for arg, val in zip(args, vals):
        tup_arg = tuple(arg)
        if tup_arg not in no_dup_args:
            no_dup_args.add(tup_arg)
            no_dup_vals.add(val)

    no_dup_args = list(no_dup_args)
    no_dup_vals = list(no_dup_vals)
    print(no_dup_args)
    
    dev_region =''
    arg_region = ''
    count =0
    with open(out, 'r') as f:
        lines_out = f.read().splitlines()

    with open(out, 'w') as ff:
        overwrite = 0
        for arg, val in zip(no_dup_args, no_dup_vals):
            for line in lines_out:
                
                count = count+1
                nline = line.replace(' ','')
                nline = nline.replace('\t', '')
                #print(nline)
                if nline == f"{str(name)}":
                    dev_region = name
                    print(f"DEV:{dev_region}")
                    
                elif dev_region == name and nline == f"{arg[0].replace(' ','')}":
                    arg_region = arg[0]
                    print(f"Arg{arg_region}")
                #elif dev_region == name and arg_region==arg[0]:
                #    print(f"INREGION:{arg[1].replace(' ','')} vs {nline}")
                    
                elif dev_region == name and arg_region==arg[0] and nline ==f"{arg[1].replace(' ','')}":
                        print("CHECK")
                        ff.write(f"            <argVal>{val}</argVal>\n")
                        overwrite = 1
                    
                #if dev_region ==name:
                #    print("_____________________")
                 #   print(nline)
                 #   print(arg[0])
                #    print("______________________")

                if(overwrite==0):
                   # print("OVERWRITE")
                    ff.write(line+'\n')
                else:
                    overwrite=0
                if nline == "</device>":
                    dev_region = ''

    rand_update(device, out)        
            
           # if dev_region == name:

    print(count)

if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument('-i', action='store', dest='output_file', default="device1_out.txt",
                        help='Pass in the output txt file corresponding to this device', type=str)
    parser.add_argument('-n', action='store', dest='device_num', default="0",
                        help='Pass in the mpc.id corresponding to this device', type=str)
    parser.add_argument('-f', action='store', dest='new_xml', default="device1_output.xml",
                        help='Pass in the xml file corresponding to this device', type=str)
    results = parser.parse_args()
    results = parser.parse_args()
    #file with print statements from mpyc computation
    filename = results.output_file
    #assumes output file exists and that it is initially just a copy of the input file
    out = results.new_xml
    device_num = int(results.device_num)
    process_output(filename,  device_num, out)
    
