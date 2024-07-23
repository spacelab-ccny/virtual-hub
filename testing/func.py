from mpyc.runtime import mpc
import sys

async def main():

    #define the secint with 16 bytes
    secint = mpc.SecInt(16)

    await mpc.start()
    
    #get number of parties connecting
    party_num = len(mpc.parties)

    #create a shared variable that stores what is passed in as the first argument
    arg1 = secint(int(sys.argv[1])) if sys.argv[1:] else secint(0)

    #create the shared variable for the threshold of the value in arg1
    threshold = secint(int(sys.argv[2])) if sys.argv[2:] else secint(1)

    #check if arg1 is beneath the passed-in threshold for that value
    beneath_thresh = secint(int(sys.argv[1] < sys.argv[2])) if sys.argv[1:] else secint(0)

    #make a list containing the threshold comparisons from all the parties
    thresh_comparisons = mpc.input(beneath_thresh, range(party_num))

    #attempt to retrieve a comparison from the list
    #for i in range(party_num):
    #    ss = await mpc.output(thresh_comparisons[i])
    #    if i == mpc.pid:
    #        print('Below thresh? ', ss)

    





    await mpc.shutdown()

mpc.run(main())
