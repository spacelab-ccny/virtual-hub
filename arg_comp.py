#!/bin/python3
from mpyc.runtime import mpc
import sys

async def main():
	secint = mpc.SecInt(16)
	await mpc.start()
	Fan1 = secint(int(sys.argv[1])) if sys.argv[1:] else secint(0)
	Blinds1 = secint(int(sys.argv[2])) if sys.argv[2:] else secint(0)
	Thermostat1 = secint(int(sys.argv[3])) if sys.argv[3:] else secint(0)

	Fan1_combined = sum(mpc.input(Fan1, range(3)))
	Blinds1_combined = sum(mpc.input(Blinds1, range(3)))
	Thermostat1_combined = sum(mpc.input(Thermostat1, range(3)))

	#Fan
	#Dependency 1
	utruth1 = -1
	upper1 = secint(int(sys.argv[4])) if sys.argv[4:] else secint(0)
	upper1 = sum(mpc.input(upper1, range(3)))
	utruth1 =  Thermostat1_combined <  upper1
	ltruth1 = -1
	lower1 = secint(int(sys.argv[5])) if sys.argv[5:] else secint(0)
	lower1 = sum(mpc.input(lower1, range(3)))
	ltruth1 = Thermostat1_combined > lower1

	in_range1 = ltruth1 * utruth1


	utruth1 = -1
	upper1 = secint(int(sys.argv[6])) if sys.argv[6:] else secint(0)
	upper1 = sum(mpc.input(upper1, range(3)))
	utruth1 =  Blinds1_combined <  upper1

	truth = (in_range1 + utruth1)
	if mpc.pid == 0:
		print('Condition 1 met?:',await mpc.output(truth))
	if mpc.pid == 1:
		print('Wait',await mpc.output(truth))
	if mpc.pid == 2:
		print('Wait',await mpc.output(truth))
	#Dependency 2
	utruth2 = -1
	upper2 = secint(int(sys.argv[7])) if sys.argv[7:] else secint(0)
	upper2 = sum(mpc.input(upper2, range(3)))
	utruth2 =  Thermostat1_combined <  upper2

	truth = (utruth2)
	if mpc.pid == 0:
		print('Condition 2 met?:',await mpc.output(truth))
	if mpc.pid == 1:
		print('Wait',await mpc.output(truth))
	if mpc.pid == 2:
		print('Wait',await mpc.output(truth))
	#Blinds
	#Dependency 1
	ltruth1 = -1
	lower1 = secint(int(sys.argv[8])) if sys.argv[8:] else secint(0)
	lower1 = sum(mpc.input(lower1, range(3)))
	ltruth1 = Thermostat1_combined > lower1

	truth = (ltruth1)
	if mpc.pid == 0:
		print('Wait',await mpc.output(truth))
	if mpc.pid == 1:
		print('Condition 1 met?:',await mpc.output(truth))
	if mpc.pid == 2:
		print('Wait',await mpc.output(truth))
	#Thermostat
	await mpc.shutdown()
mpc.run(main())