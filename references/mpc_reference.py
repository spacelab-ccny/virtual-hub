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

		ff = f<b
		a = await mpc.output(ff,1)
		aa= await mpc.output(b,1)
		aaa = await mpc.output(t,2)

		if(mpc.pid == 0):
			print(a)
		if(mpc.pid == 1):
			print(a)
			print(aa)
		if(mpc.pid == 2):
			print(aaa)	
		
		#await mpc.shutdown()
mpc.run(main())