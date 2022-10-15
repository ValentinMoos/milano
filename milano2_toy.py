 #!/usr/bin/env python3
# -*- coding: utf-8 -*-

#define dependencies.
print("program started.")

logFile="minimization_runs.log"

#print("starting parameters from run? (Alternatives:  0: read parameters from python file itself., \"-n\" will use the initials of run n)")
#nParams = int(input())
nParams = 0 # does not matter anyway.

#imports
print("importing.. this takes some time")

import sys
import time
from pathlib import Path
import datetime
sys.path.append("/home/mov57924/Dokumente/arTeMiDe/reell_run1")
sys.path.append("/home/mov57924/work/artemide/pythonlib")
sys.path.append("/home/mov57924/installations/lib/python3.9")
sys.path.append(".")

import numpy as np
from readParameters import readParameters as readParameters
from cutFunc import cutFunc as cutFunc
from os.path import exists
import os
import shutil

#pysilent = True
pysilent = False

# Disable
def blockPrint():
    sys.stdout = open(os.devnull, 'w')

# Restore
def enablePrint():
    sys.stdout = sys.__stdout__

def log_step(x, chi2,file): # expected interpretation: x = parameters, chi2 is totalchi2 (what is being minimized) (not normalized), file is path to log file
    logfile = file
    with open(logfile,'r') as fin:   # check how many steps are stored already
        data = fin.read().splitlines(True)
    num_lines = sum(1 for line in open(logfile))
    if(num_lines >= 15):                        # if more than some number -> remove one
        with open(logfile, 'w') as fout:
            fout.writelines(data[1:])

    f = open(logfile,'a')            # append this step
    delimiter = " "
    x_string_local = delimiter.join(map(str, x))
    f.write(x_string_local)
    f.write(" " + str(chi2) + "\n")
    f.close()
    return

def checkControlFile():
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
    global run
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

iRun = -1


#for tests..
def chi2(p):
    x = p[1][0]
    print(x)
    y = p[1][1]
    print(y)
    #exit()
    f = (x+3)*(x+3) + (y-1)*(y-1)    
    return f

def cin_split_parameters(lineinput):
	parameters = lineinput.split()
	if(parameters[0] != "parameters:"):
		print("sorry but i cant deal with this: " + lineinput)
		
	return parameters

def callmilano2():
    p = readParameters(iRun,file = "milano.cc.parameters", tmdpdf_version = 0, comdir = True)
    print("ATTENTION1")
    os.system("cat com/milano.cc.parameters")
    print("ATTENTION2")
    print("ATTENTION3")
    os.remove("com/milano.cc.parameters")
    #harpy.setNPparameters(p)
    print("Python: calling chi2 with parameters")
    print(p)
    print('%.51f' % p[0][1])
    v = chi2(p)
    f = open("com/milano.py.result",'w')
    f.write(str(v))
    f.close()
    print( "function value computed is     " + str(v) )
    return

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


# starting values & minimization selection. Use rectangular brackets for TMD values but curly brackets are ok for initial values.

import fileinput

print("i write i a line here")
print("i write i a line there")
for line in fileinput.input():
    print(line + " IS WHAT PYTHON SAW")

print("i write i a line here again!!")
for line in fileinput.input():
    print(line + " IS WHAT PYTHON SAW")

exit()


life = True
print("Life begins")
chi2_call_counter = 0
if(pysilent):
    blockPrint()
while(life):
    checkControlFile()
    if(run):
        print("Python: executing", chi2_call_counter)
        #print(chi2_call_counter)
        callmilano2()
        ping(1,'c')
        #put yourself to sleep.
        ping(2,'p')
    else:
        time.sleep(0.1)
print("Python: ended ( Life is over ).")
