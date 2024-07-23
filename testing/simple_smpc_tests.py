from mpyc.runtime import mpc
import sys

#ASSUMPTIONS:
#-only two parties, thermostat(mpc.pid 0) and lightbulb(mpc.pid 1)
#-inputs passed in will be valid
#     e.g. the lightbulb cannot pass in a non-zero value for temp. (zero is the default)
#-all passed in values are integers (I don't think secure floats and secure ints can be compared)


async def main():

  secint = mpc.SecInt(16)
  #secflt = mpc.SecFlt(16)

  await mpc.start()

  #collect inputs for each party
  #each party has the same input arguments
  #arg1 = temperature
  #arg2 = if light is on

  temp= secint(int(sys.argv[1])) if sys.argv[1:] else 72
  light_state = secint(int(sys.argv[2])) if sys.argv[2:] else 0

  # we store the inputs of each argument as secure lists,
  #BUT by our construction, each list will have all 0s 
  #except for the one value from the device that reflects that parameter
  #    e.g. arg1 is the temp value for the thermostat, so only the thermostat
  #    deivce would pass in a temp value and the other devices/parties would pass in 0

  sec_temp_list = mpc.input(temp, [0,1])
  sec_light_list = mpc.input(light_state, [0,1])


  #we sum the lists so now each party has access to each value passed in by each party
  #(again because by our contruction each list only has one non-zero value)
  #becuase the lists are secure, these values are also secure
  #so each party can't determine what the other parties passed in

  total_light_on = sum(sec_light_list)
  total_temp = sum(sec_temp_list)


  #arbitrary temp threshold
  threshold = secint(80)
  light_on = secint(1)

  temp_check = (total_temp > threshold)
  light = (light_on == total_light_on)


  # if temp high (1), light should be off (0)
  # if temp low (0), light should be on (1)
  # thus, if both are 0s or both are 1s, the light should change states
  change_light_state = (light == temp_check)
  

  #assumes mpc.pid==0 for thermostat and mpc.pid == 1 for lightbulb
  #passes respective outputs to respective parties
  if (mpc.pid == 0):
    temp_check = 1
    print('Temp high?:',await mpc.output(temp_check))
  if (mpc.pid == 1):
    print('Change light state?:',await mpc.output(change_light_state))

  await mpc.shutdown()

mpc.run(main())
