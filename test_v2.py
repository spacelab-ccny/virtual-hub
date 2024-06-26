from mpyc.runtime import mpc
import sys

#Based on simple_smpc.py but abstracted to allow any device and rule to be added

#ASSUMPTIONS:
#-each device/party only has one value that it inputs
#-each passed in value is valid
#   e.g. a boolean valuen is boolean, not some other int
#-all passed in values are integers (I don't think secure floats and secure ints can be compared)

 

async def main():

  secint = mpc.SecInt(16)
  #secflt = mpc.SecFlt(16)

  await mpc.start()

  #determine the number of connecting parties
  party_num = len(mpc.parties)
  print(party_num)

  #make a list initialized with # 0s == # parties
  #sec_list = [secint(0)]*party_num

  #for each device/party set sec_list to be a list of all 0s (as initialized) with
  #the value at index==mpc.party being the meaningful argument for that device
  #[assuming each device only has one meaningful input to the computation]
  
  sec_list =[]
  print(f"arg: {sys.argv[1]}")
  #get value of argument for this party
  val = secint(int(sys.argv[1])) if sys.argv[1:] else secint(0)
  print(f"VAL : {val}")
  #check the value against the arbitrary threshold value
  #but how do we index into a list to get it?
  # or else is it passed in with the party?


  sec_list = mpc.input(val, range(party_num))
  num = mpc.pid
  id_list = mpc.input(secint(num), range(party_num))
  print('mpc.pid', await mpc.output(id_list))
  print(mpc.pid)
  for i in range(party_num):
    if (mpc.pid ==i):
      get = sec_list[i]

  b = mpc.input(get, range(party_num))
  j=0
  while j < party_num:
    if(mpc.pid == j):
      x = sec_list[j]
    j = j+1
  
  #c = await sec_list[party_num-1]
  a = await mpc.output(sec_list[mpc.pid])

  print(f"sec_list{sec_list}")
  print('Beneath threshold?:',await mpc.output(sec_list))
  #print('mmmmmmmmmmmmmm?:',await mpc.output(a))
  
  print("check2")

  print("check3")
  #generate some list of thresholds
  #we'll use all 1s for now for simplicity:
  thresholds = [secint(1)]*party_num
  # list to hold comparisons to thresholds
  check_vals = [0]*party_num

  print("check4")
  # iterates through thresholds checking if the value is below the threshold and printing the output to the respective party
  for party in range(party_num):
    check_vals[party] = (thresholds[party] > sec_list[party])
    print(party)
    print("--------")
    print(check_vals[party])

  #can get unsecure version of int at any single predetermined index:
  s = await mpc.output(sec_list[0])
  print(f"testing: {s}")



  count = mpc.pid
  print(count)
  # cen get unsecure version of int in sec_list for all elements in list
  for i in range(party_num):
    ss = await mpc.output(sec_list[i])
    print(f"testing: {ss}")
    if i == count:
      print(f"SECRET: {sec_list[i]}")
      print(sec_list)


  print('Beneath threshold?:',await mpc.output(check_vals[mpc.pid]))

  print("done")
  #there should be a way to add a device such that you can easily add rules that determine its functionality
  #start by being able to handle any number of devices given their thresholds
  #I think if you check if each is less than their threshold, making the threshold 1, for booleans and arbitrary otherwise
  #then we can abstract that comparison for each deivce
  #have some splitting? argument followed by arguments of dependencies, and whether the state changes if that dependency is high or low
  #but how would we account for dependencies that require MULTIPLE devices are in a certain state?
  # we can then put all these boolean values in a list and act accordingly, ANDing/ORing the necessary list components through mult/addition

  await mpc.shutdown()

mpc.run(main())
