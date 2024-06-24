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
  sec_list = [secint(0)]*party_num

  #for each device/party set sec_list to be a list of all 0s (as initialized) with
  #the value at index==mpc.party being the meaningful argument for that device
  #[assuming each device only has one meaningul input to the computation]
  print("check1")
  for party in range(party_num):
    if(mpc.pid ==party):
      sec_list[party] = secint(int(sys.argv[1])) if sys.argv[1:] else 0
  
  print("check2")
  for party in range(party_num):
    #combine the element of sec_list at index=party from each party/device into one list
    #and make sec_list[party] = this list of all 0s except for one meaningful value
    sec_list[party] = mpc.input(sec_list[party], range(party_num))

    #sum the values at each index of sec_list so that now sec_list is a list of all the meaningful values from each party
    #where each index of sec_list corresponds to the party from which that meaningful value was taken
    sec_list[party] = sum(sec_list[party])

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

  print(mpc.pid)  

  print('Beneath threshold?:',await mpc.output(check_vals[mpc.pid]))

  print("done")
  #there should be a way to add a device such that you can easily add rules that determine its functionality
  #start by being able to handle any number of devices given their thresholds
  #I think if you check if each is less than their threshold, making the threshold 1, for booleans and arbitrary otherwise
  #then we can abstract that comparison for each deivce
  # we can then put all these boolean values in a list and act accordingly, ANDing/ORing the necessary list components through mult/addition

  await mpc.shutdown()

mpc.run(main())
