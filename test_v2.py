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

  light_on = 0
  temp = 0

  temp= int(sys.argv[1]) if sys.argv[1:] else 72
  light_state = int(sys.argv[2]) if sys.argv[2:] else 0
  
  a = mpc.input(secint(temp), [0,1])
  b = mpc.input(secint(light_state), [0,1])

  total_light_on = sum(b)
  total_temp = sum(a)
  print(total_temp)

  threshold = secint(80)
  light_on = secint(1)

  temp_check = (total_temp > threshold)
  light = (light_on == total_light_on)
  # if temp high (1), light should be off (0)
  # if temp low (0), light should be on (1)
  # thus, if both are 0s or both are 1s, the light should change states
  change_light_state = (light == temp_check)


  #assumes 
  if (mpc.pid == 0):
    print('Temp high?:',await mpc.output(temp_check))
  if (mpc.pid == 1):
    print('Change light state?:',await mpc.output(change_light_state))

  await mpc.shutdown()

mpc.run(main())
