#!/bin/python3
from mpyc.runtime import mpc
import sys

async def main():
	secint = mpc.SecInt(16)

	#Fan
	Fan1 = None
	#Dependency 1
	Fan_upper1_0 = None
	Fan_lower1_0 = None

	Fan_state1_1 = None
	#Dependency 2
	Fan_lower2_0 = None

	Fan_state2_1 = None
	#Thermostat
	Thermostat1 = None
	if mpc.pid == 0:
		Fan1 = int(sys.argv[1])
		Fan_upper1_0 = int(sys.argv[2])
		Fan_lower1_0 = int(sys.argv[3])
		Fan_state1_1 = int(sys.argv[4])
		Fan_lower2_0 = int(sys.argv[5])
		Fan_state2_1 = int(sys.argv[6])
	elif mpc.pid == 1:
		Thermostat1 = int(sys.argv[1])

	async with mpc:
		Fan1 = mpc.input(secint(Fan1), 0)
		Fan_upper1_0 = mpc.input(secint(Fan_upper1_0), 0)
		Fan_lower1_0 = mpc.input(secint(Fan_lower1_0), 0)
		Fan_state1_1 = mpc.input(secint(Fan_state1_1), 0)
		Fan_lower2_0 = mpc.input(secint(Fan_lower2_0), 0)
		Fan_state2_1 = mpc.input(secint(Fan_state2_1), 0)
		Thermostat1 = mpc.input(secint(Thermostat1), 1)

		utruth1 =  Thermostat1 <Fan_upper1_0
		ltruth1 =  Thermostat1 > Fan_lower1_0
		in_range1 = ltruth1 == utruth1
		in_range1 = in_range1 == secint(1)
		truth1_0 = (in_range1)

		out1_0_0 = await mpc.output(mpc.if_else(truth1_0, Fan_state1_1, Fan1 ), 0)
		if mpc.pid == 0:
			print(f"output Fan_state1_1 {out1_0_0}")

		ltruth2 =  Thermostat1 > Fan_lower2_0
		truth1_1 = (ltruth2)

		out1_1_0 = await mpc.output(mpc.if_else(truth1_1, Fan_state2_1, Fan1 ), 0)
		if mpc.pid == 0:
			print(f"output Fan_state2_1 {out1_1_0}")

mpc.run(main())