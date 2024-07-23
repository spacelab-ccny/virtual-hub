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

  
  sec_list =[]
  print(f"arg: {sys.argv[1]}")
  #get value of argument for this party
  val = secint(int(sys.argv[1])) if sys.argv[1:] else secint(0)
  sec_list = mpc.input(val, range(party_num))

  #generate some list of thresholds
  #we'll use all 1s for now for simplicity:
  thresholds = [secint(1)]*party_num
  # list to hold comparisons to thresholds
  check_vals = [secint(0)]*party_num

  #can get unsecure version of int at any single predetermined index:
  s = await mpc.output(sec_list[0])
  print(f"testing: {s}")

  count = mpc.pid
  check = 0
  sec =0
  print(count)
  # cen get unsecure version of int in sec_list for all elements in list
  for i in range(party_num):
    sec2 = sec_list[i]
    ss = await mpc.output(sec2)
    print(f"testing: {ss}")
    if i == count:
      print(f"SECRET: {sec_list[i]}")
      print(sec_list)
      check = check_vals[i]
      sec = sec_list[i]
      
  print(check)
  print(sec)
  shared_check = mpc.input(check, range(party_num))
  for i in range(party_num):
    if i==count:
      check2 = shared_check[i]

  #list that checks if each argument for each party is lower than its corresponding threshold
  #beneath_thresh = mpc.input(secint(int(await mpc.output(check) > await mpc.output(sec))), range(party_num))
  beneath_thresh = mpc.input(check2>sec, range(party_num))
  bool = await mpc.output (check2>sec)
  bool2= check2>sec
  a = await mpc.output(check2)
  b = await mpc.output(sec)
  c = await mpc.output(check2) > await mpc.output(sec)
  print("beneath threshold? ", await mpc.output(check2) > await mpc.output(sec))
  print("beneath threshold? ", c)
  print("sec", b)
  print("beneath threshold unsec? ", bool)
  print("beneath threshold bool2? ", await mpc.output(bool2))
  print("beneath threshold sec? ", await mpc.output(beneath_thresh))


  print("done")

  await mpc.shutdown()

mpc.run(main())
