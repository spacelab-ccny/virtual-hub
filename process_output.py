import argparse
from bs4 import BeautifulSoup
from lxml import etree

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

    
    args = []
    for change in changes:
        var, val = change.split()
        var = var[var.index('state')+5:]
        dep, state = var.split('_')
        
        arg= soup .find('argument', {'num':int(state)})
        a = str(arg).split('\n')
        args = args +[a[:2]]

    
    no_dup_args = set()
    for arg in args:
        tup_arg = tuple(arg)
        if tup_arg not in no_dup_args:
            no_dup_args.add(tup_arg)

    no_dup_args = list(no_dup_args)
    print(no_dup_args)
    
    dev_region =''
    arg_region = ''
    count =0
    with open(out, 'r') as f:
        lines_out = f.read().splitlines()
    with open(out, 'w') as ff:
        overwrite = 0
        for line in lines_out:
            for arg in no_dup_args:
                count = count+1
                nline = line.replace(' ','')
                if nline == f"{str(name)}":
                    dev_region = name
                    print(f"DEV:{dev_region}")
                    
                elif dev_region == name and nline == f"{arg[0].replace(' ','')}":
                    arg_region = arg[0]
                    print(f"Arg{arg_region}")
                    
                elif dev_region == name and arg_region==arg[0].replace(' ','') and nline ==f"{arg[1].replace(' ','')}":
                    print("CHECK")
                    ff.write("\t\t<argVal></argVal>\n")
                    overwrite = 1
                #if dev_region ==name:
                #    print("_____________________")
                 #   print(nline)
                 #   print(arg[0])
                #    print("______________________")

            if(overwrite==0):
                ff.write(line+'\n')

                
            
           # if dev_region == name:


            if line == "</device>":
                dev_region = ''
    print(count)

if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument('-i', action='store', dest='output_file', default="device1_input.txt",
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
    
