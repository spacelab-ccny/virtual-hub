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

  #make a list initialized with # 0s == # parties
  sec_list = [secint(0)]*party_num

  #
  for party in range(party_num):
    if(mpc.pid ==party):
      sec_list[party] = secint(int(sys.argv[1])) if sys.argv[1:] else 0
  
  print(sec_list)

  for party in range(party_num):
    sec_list[party] = mpc.input(sec_list[party], range(party_num))
  
  print(sec_list)

  #generate some list of thresholds

  #there should be a way to add a device such that you can easily add rules that determine its functionality
  #start by being able to handle any number of devices given their thresholds
  #I think if you check if each is less than their threshold, making the threshold 1, for booleans and arbitrary otherwise
  #then we can abstract that comparison for each deivce
  # we can then put all these boolean values in a list and act accordingly, ANDing/ORing the necessary list components through mult/addition

  await mpc.shutdown()

mpc.run(main())
