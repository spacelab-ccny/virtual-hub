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
	utruth1 =  Thermostat1_combined <  secint( 80 )
	ltruth1 = -1
	ltruth1 = Thermostat1_combined > secint( 70 )

	in_range1 = ltruth1 * utruth1


	utruth1 = -1
	utruth1 =  Blinds1_combined <  secint( 0 )

	truth = (in_range1 + utruth1)
	print("check")
	if mpc.pid == 0:
		print("1")
		print('Condition 1 met?:',await mpc.output(truth))
	if mpc.pid == 1:
		print("1")
		print('Wait:',await mpc.output(truth))
	if mpc.pid == 2:
		print("1")
		print('Wait:',await mpc.output(truth))
	#Dependency 2
	utruth2 = -1
	utruth2 =  Thermostat1_combined <  secint( 50 )

	truth = (utruth2)
	if mpc.pid == 0:
		print("2")
		print('Condition 2 met?:',await mpc.output(truth))
	if mpc.pid == 1:
		print("2")
		print('Wait:',await mpc.output(truth))
	if mpc.pid == 2:
		print("2")
		print('Wait:',await mpc.output(truth))
	#Blinds
	#Dependency 1
	ltruth1 = -1
	ltruth1 = Thermostat1_combined > secint( 90 )

	truth = (ltruth1)
	if mpc.pid == 1:
		print("3")
		print('Condition 1 met?:',await mpc.output(truth))
	if mpc.pid == 2:
		print("3")
		print('Wait:',await mpc.output(truth))
	if mpc.pid == 0:
		print("3")
		print('Wait:',await mpc.output(truth))
	#Blinds
	#Thermostat
	await mpc.shutdown()
mpc.run(main())