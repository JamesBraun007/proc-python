#!/usr/bin/python3
from math import inf
from multiprocessing import process
import sys
import os
import time

# procinfo [-t secs] pattern
#
# prints PID, CMD, USER, Memory Usage, CPU time, and number of threads 
# of processes with a command # that matches "pattern"
#
# If the [-t secs] option is passed, then it will loop and print the information
# every "secs" secods.
#
# If no pattern is given, it prints an error that a pattern is missing.
#

def retrieveInfo(pattern):
    # sending processes of all users with user names to text file
    os.system("ps -ef > process_info.txt")

    # need to parse text file and extract PID, PPID, User(UID), and CMD
    # make sure to only retrieve PID that have CMD that contains pattern
    info_file = open("process_info.txt", "r")

    print("{:<8} {:<8} {:<12} {:<12} {:<10} {:<10} {:<10}".format("PID", "PPID", "CMD", "USER", "MEM", "CPU", "THREADS"))
    for line in info_file:
        if pattern in line:
            info = line.split()
            USER = info[0]
            PID = info[1]
            PPID = info[2]


            # getting CPU info in stat file
            cpu_file = open(f"/proc/{PID}/stat", "r")
            cpu_string = cpu_file.read()
            cpu_data = cpu_string.split()

            # getting both user time and kernel time
            cpu_time = int((int(cpu_data[13]) + int(cpu_data[14]))/100)
            

            # getting Threads and MEM info in status file
            threads_MEM_file = open(f"/proc/{PID}/status", "r")
            threads_MEM_data = threads_MEM_file.read()
            
            for info in threads_MEM_data.split("\n"):
                if info.startswith("Threads:"):
                    threads = info.split()[1]
            
                
                if info.startswith("VmRSS"):
                    mem = int(info.split()[1])
                    mem_mb = int(mem/1024)

            # need to align this properly
            print("{:<8} {:<8} {:<12} {:<12} {:<10} {:<10} {:<10}".format(PID, PPID, f"({pattern})", USER, f"{mem_mb}MB", f"{cpu_time}secs", f"{threads}Thr"))  

    info_file.close()
    cpu_file.close()
    threads_MEM_file.close()  

def main():
 
    # first check if pattern is present
    if len(sys.argv) != 2 and len(sys.argv) != 4:
        print("Error: a pattern is missing or there incorrect number of arguments")

    elif len(sys.argv) == 4:

        # printing every "secs" seconds
        while True:
            pattern = sys.argv[3]
            retrieveInfo(pattern)
            time.sleep(int(sys.argv[2]))
            

    # otherwise, only print once
    else:
        pattern = sys.argv[1]
        retrieveInfo(pattern)        
      

if __name__ == "__main__":
    main()
