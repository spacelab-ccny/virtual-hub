import argparse

def pid_string(num,pid_list):
    command_str = ''
    pids = pid_list.split(',')

    count = 0
    pid_index = 0
    while count < len(pids)+1:
        if(count == num ):
            command_str = command_str +"-P localhost "
        else:
            command_str = command_str +f"-P {pids[pid_index]} "
            pid_index=pid_index +1
        count = count +1
    print(command_str)
    return (command_str)


if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument('-n', action='store', dest='device_num', default="0",
                        help='Pass in the mpc.pid corresponding to this device', type=str)
    parser.add_argument('-p', action='store', dest='pid', default="0",
                        help='Pass in the list of pids corresponding to the devices this device will connect to', type=str)
    results = parser.parse_args()
    device_num = int(results.device_num)
    pid_list = results.pid

    pid_string(device_num, pid_list)