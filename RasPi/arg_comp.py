#!/bin/python3
from mpyc.runtime import mpc
import time
import os
import psutil
import sys

async def main():
	secint = mpc.SecInt(16)

	#Fan
	Fan1 = None
	Fan2 = None
	#Dependency 1
	Fan_upper1_0 = None
	Fan_lower1_0 = None

	Fan_upper1_1 = None

	Fan_state1_1 = None
	Fan_state1_2 = None
	#Dependency 2
	Fan_upper2_0 = None

	Fan_state2_1 = None
	#Blinds
	Blinds1 = None
	#Dependency 1
	Blinds_lower1_0 = None

	Blinds_state1_1 = None
	#Thermostat
	Thermostat1 = None
	if mpc.pid == 0:
		Fan1 = int(sys.argv[1])
		Fan2 = int(sys.argv[2])
		Fan_upper1_0 = int(sys.argv[3])
		Fan_lower1_0 = int(sys.argv[4])
		Fan_upper1_1 = int(sys.argv[5])
		Fan_state1_1 = int(sys.argv[6])
		Fan_state1_2 = int(sys.argv[7])
		Fan_upper2_0 = int(sys.argv[8])
		Fan_state2_1 = int(sys.argv[9])
	elif mpc.pid == 1:
		Blinds1 = int(sys.argv[1])
		Blinds_lower1_0 = int(sys.argv[2])
		Blinds_state1_1 = int(sys.argv[3])
	elif mpc.pid == 2:
		Thermostat1 = int(sys.argv[1])

	start=0
	async with mpc:
		start=time.time()
		pid = os.getpid()
		process = psutil.Process(pid)
		mem2 = process.memory_full_info()
		print(f"RSS: {mem2[0]}\nVMS: {mem2[1]}\nUSS: {mem2[7]}\n")

		Fan1 = mpc.input(secint(Fan1), 0)
		Fan2 = mpc.input(secint(Fan2), 0)
		Fan_upper1_0 = mpc.input(secint(Fan_upper1_0), 0)
		Fan_lower1_0 = mpc.input(secint(Fan_lower1_0), 0)
		Fan_upper1_1 = mpc.input(secint(Fan_upper1_1), 0)
		Fan_state1_1 = mpc.input(secint(Fan_state1_1), 0)
		Fan_state1_2 = mpc.input(secint(Fan_state1_2), 0)
		Fan_upper2_0 = mpc.input(secint(Fan_upper2_0), 0)
		Fan_state2_1 = mpc.input(secint(Fan_state2_1), 0)
		Blinds1 = mpc.input(secint(Blinds1), 1)
		Blinds_lower1_0 = mpc.input(secint(Blinds_lower1_0), 1)
		Blinds_state1_1 = mpc.input(secint(Blinds_state1_1), 1)
		Thermostat1 = mpc.input(secint(Thermostat1), 2)

		utruth1 =  Thermostat1 <Fan_upper1_0
		ltruth1 =  Thermostat1 > Fan_lower1_0
		in_range1 = ltruth1 == utruth1
		in_range1 = in_range1 == secint(1)
		utruth1 =  Blinds1 <Fan_upper1_1
		truth1_0 = (in_range1 * utruth1)

		out1_0_0 = await mpc.output(mpc.if_else(truth1_0, Fan_state1_1, Fan1 ), 0)
		if mpc.pid == 0:
			print(f"output Fan_state1_1 {out1_0_0}")


		out1_0_1 = await mpc.output(mpc.if_else(truth1_0, Fan_state1_2, Fan2 ), 0)
		if mpc.pid == 0:
			print(f"output Fan_state1_2 {out1_0_1}")

		utruth2 =  Thermostat1 <Fan_upper2_0
		truth1_1 = (utruth2)

		out1_1_0 = await mpc.output(mpc.if_else(truth1_1, Fan_state2_1, Fan1 ), 0)
		if mpc.pid == 0:
			print(f"output Fan_state2_1 {out1_1_0}")

		ltruth1 =  Thermostat1 > Blinds_lower1_0
		truth2_0 = (ltruth1)

		out2_2_0 = await mpc.output(mpc.if_else(truth2_0, Blinds_state1_1, Blinds1 ), 1)
		if mpc.pid == 1:
			print(f"output Blinds_state1_1 {out2_2_0}")

		end=time.time()
		total=end-start
		print(f"TIME: {total}")
mpc.run(main())