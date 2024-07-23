from mpyc.runtime import mpc
import sys
async def main():

  secint = mpc.SecInt(16)
  secflt = mpc.SecFlt(16)
  # thermostat, pid=0
  # outputs temperature

  #lightbulb, pid=1
  #outputs on or off

  #ac, pid=2
  #outputs set temp, and on/off

  await mpc.start()

  sec_temp = 72
  sec_on = 0
  light_on = 0
  temp = 0

  
  if (mpc.pid == 0):
    print("TESTING")
    print(float(sys.argv[1]) if sys.argv[1:] else 72)
    #therm_temp 
    val= float(sys.argv[1]) if sys.argv[1:] else 72 # default 72

  elif (mpc.pid == 1):
    #light_on
    val = int(sys.argv(2) if sys.argv[1:] else 0 # 1 or 0 for on/off
  
  inputs = mpc.input(secint(val))
  print(inputs)




  if (total_temp > 80):
    if(mpc.pid ==0):
      print("business as usual")
    elif(mpc.pid == 1):
      light_on = 0
      print("turning light off")
 # elif(sec_temp <=80 and not sec_on):
 #   if(mpc.pid ==0):
  #    print("business as usual1")
   # elif(mpc.pid == 1):
  #    light_on = 1
  #    print("turning light on")
#  else:
 #   if(mpc.pid ==0):
  #    print("business as usual2")
  #  if(mpc.pid == 1):
 #     print("business as usual")
  await mpc.shutdown()

mpc.run(main())
