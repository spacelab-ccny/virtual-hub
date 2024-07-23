#!/bin/python3
from mpyc.runtime import mpc
import sys

async def main():
	secint = mpc.SecInt(16)
	await mpc.start() 0 0 72

	#Fan  0   0   0 
	truth = ()
	if mpc.pid == 0:
		print('Condition 1 met?:',await mpc.output(truth))
	if mpc.pid == 1:
		print('Wait',await mpc.output(truth))
	if mpc.pid == 2:
		print('Wait',await mpc.output(truth))  50 
	truth = (())
	if mpc.pid == 0:
		print('Condition 2 met?:',await mpc.output(truth))
	if mpc.pid == 1:
		print('Wait',await mpc.output(truth))
	if mpc.pid == 2:
		print('Wait',await mpc.output(truth))
	#Blinds 0  90 
	truth = ()
	if mpc.pid == 0:
		print('Wait',await mpc.output(truth))
	if mpc.pid == 1:
		print('Condition 1 met?:',await mpc.output(truth))
	if mpc.pid == 2:
		print('Wait',await mpc.output(truth))
	#Thermostat
	await mpc.shutdown()
mpc.run(main())