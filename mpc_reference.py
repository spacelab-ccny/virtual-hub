#!/bin/python3
from mpyc.runtime import mpc
import sys

async def main():
	secint = mpc.SecInt(16)
	#await mpc.start()
	Fan1 = [None]
	Blinds1 = [None]
	Thermostat1 = [None]
	if mpc.pid == 0:
		Fan1[0] = (int(sys.argv[1]))
	elif mpc.pid==1:
		Blinds1[0]= (int(sys.argv[1]))
	elif mpc.pid==2:
		Thermostat1[0] = (int(sys.argv[1]))
	async with mpc:
		
		f = mpc.input(secint(Fan1[0]),0)
		b = mpc.input(secint(Blinds1[0]),1)
		t = mpc.input(secint(Thermostat1[0]),2)


		a = await mpc.output(f,0)
		print(a)

		
		#await mpc.shutdown()
mpc.run(main())