import sys
import os
import time
from pathlib import Path
from os.path import exists

def ping(l, mode):
    cppblockerfile = "cppstopper"
    Path(cppblockerfile).touch()
    #print("pinging")
    
    #time.sleep(0.1)
    file = "test"
    if(mode == 'p'):
        file = "com/milano.py.ctrl"
    elif(mode == 'c'):
        file = "com/milano.cc.ctrl"
    else:
        print("undefined command: " + mode)
        exit(2)
    
    line = str(l)
    f = open(file,'w')
    f.write(line)
    f.close()
    os.remove(cppblockerfile)
    #print("ping ended")
    return

def checkControlFile(run):
    pystopfile = "pystopper"
    gate1 = exists(pystopfile)
    sleepcounter = 0
    sleeptime = 0.2
    while(gate1):
        message = "\rsleep because currently c++ is writing a command " + str(int(sleepcounter*sleeptime)) + "seconds"
        sys.stdout.write(message)
        sys.stdout.flush()
        sleepcounter += 1
        #print("\rsleep because currently c++ is writing a command " + str(sleepcounter))
        time.sleep(sleeptime)
        #print(gate1)
        gate1 = exists(pystopfile)
    #global run
    global life
    f = open("com/milano.py.ctrl", 'r')
    command = int(f.read())
    f.close()
    if(command == 1):
        run = True
    elif(command == 0):

        run = False
        life = False
    elif(command == 2):
        run = False
    else:
        print("unregistered command: +" + str(command) + "+")
        exit()
    time.sleep(0.1)
    return