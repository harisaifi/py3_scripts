import socket
import argparse
from threading import Thread, Lock
from queue import Queue
from colorama import init, Fore

# using some fancy colors
init()
GREEN = Fore.GREEN
GRAY = Fore.LIGHTBLACK_EX
RESET = Fore.RESET

# number of threads
NO_OF_THREADS = 50

# queue to hold port numbers
q = Queue()

# Thread lock for thread clashes
print_lock = Lock()


def port_scan(port):
    try:
        # object of socket using IPv4 and TCP type connection
        sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        sock.connect((host,port))
        with print_lock:
            print(f"{GREEN}[+] {host}:{port} is open{RESET}")
    except:
        pass


def threader():
    global q

    # infinite loop to take port number
    # from queue and scan it
    while True:
        # get a port number from queue
        worker = q.get()
        # start scanning the port
        port_scan(worker)
        # tell queue the worker has completed its work
        # tell queue scanning of that port is done
        q.task_done()


def main(host, port):
    global q

    # print information
    print(f"Scanning started with {NO_OF_THREADS} threads\nhost = {host}\nport range = {port_range}")

    # starting the threads
    for t in range(NO_OF_THREADS):
        # creating thread of method "threader"
        t = Thread(target=threader)
        # when daemon is true, the thread will end when the main thread end
        t.daemon = True
        # start the thread
        t.start()

    # put ports in queue
    for worker in ports:
        # adding ports number one by one in queue
        q.put(worker)

    # wait the threads "port scanners" to finish
    q.join()


if __name__ == "__main__":

    # parser for command-line options
    parse = argparse.ArgumentParser(description="Simple multi-threaded port scanner")

    # here "host" is positional argument (Compulsory Argument)
    parse.add_argument("host", help="host to scan")

    # ports and threads are optional argument
    # with programmer defined default values
    parse.add_argument("-p", "--ports", dest="port_range", default="0-65535", help="port range to scan, default = 0-65535")
    parse.add_argument("-t", "--threads", dest="no_of_threads", default=50, help="number of threads to use, default = 50")

    # parse arguments from user to "args"
    args = parse.parse_args()

    # assign values from parsed arguments to variables/objects
    host, port_range, NO_OF_THREADS = args.host, args.port_range, int(args.no_of_threads)

    # split port range from input "a-b" to lower = "a" and upper = "b"
    lower_port_range, upper_port_range = port_range.split("-")
    # convert values from string to int type
    lower_port_range, upper_port_range = int(lower_port_range), int(upper_port_range)

    # stores port numbers as list in ports[list] ranging from lower to upper port range
    ports = [p for p in range(lower_port_range, upper_port_range+1)]

    # calling main method
    main(host, ports)