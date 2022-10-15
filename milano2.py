 #!/usr/bin/env python3
# -*- coding: utf-8 -*-

#define dependencies.
print("program started.")
EXECUTIONPATH = "/home/mov57924/Dokumente/arTeMiDe/milano2"
#EXECUTIONPATH = "/home/mov57924/work/artemide/hpd_setup_3"
ARCHIVEPATH = EXECUTIONPATH + "/archive"
#ARCHIVEPATH = "./archive"

f=open(ARCHIVEPATH + "/structure",'r')
thepaths = f.read().splitlines()
MAINPATH = thepaths[0]
print(MAINPATH)
MAINPATH_arTeMiDe = thepaths[1]
f.close()
print(MAINPATH, MAINPATH_arTeMiDe)

logFile="minimization_runs.log"

#print("starting parameters from run? (Alternatives:  0: read parameters from python file itself., \"-n\" will use the initials of run n)")
#nParams = int(input())
nParams = 0 #does not matter anyway.

#imports
print("importing.. this takes some time")

import sys
import time
from pathlib import Path
import datetime
sys.path.append("/home/mov57924/work/artemide/pythonlib")
sys.path.append("/home/mov57924/installations/lib/python3.9")
sys.path.append("/home/mov57924/artemide/artemide-development/harpy")
sys.path.append(".")



import numpy as np
sys.path.append(MAINPATH[:-1])
print(MAINPATH)
import DataProcessor.harpyInterface
import DataProcessor.DataMultiSet
#import PyCeres as ceres # Import the Python Bindings
import harpy
from readParameters import readParameters as readParameters
from cutFunc import cutFunc as cutFunc
from os.path import exists
import os
import shutil

os.system("setenv LD_LIBRARY_PATH /temp_local/mov57924/LHAPDF/lib")
print("imports done.")

print("PYTHON IS IN ")
os.system("pwd") # show us where we are.
#accuratly starting and documenting:
python_code_file = "/home/mov57924/work/artemide/hpd_setup_3/milano2.py"
manually = False
if(manually):
    f=open("settingsfile",'r')
    thepaths = f.read().splitlines()
    iRun = int(thepaths[0][16:])
    nOrder = int(thepaths[1])
    vrs = int(thepaths[2])
    order_of_uTMDandFF = int(thepaths[3])
else:
    iRun = 999
    nOrder = 0
    vrs = 0
    order_of_uTMDandFF = 2

#pysilent = True
pysilent = False


# Disable
def blockPrint():
    sys.stdout = open(os.devnull, 'w')

# Restore
def enablePrint():
    sys.stdout = sys.__stdout__



f.close()

constfilename = "constfile_N" + str(nOrder) + "LO" #    N2LO, N3LO or N4LO

if (not(nOrder in [0,2,3,4])):
    print("abort with nOrder = " + str(nOrder))
    exit()
if (not(vrs in [0,1])):
    print("abort with version = " + str(vrs))
    exit()
if (not(order_of_uTMDandFF in [2,3])):
    print("abort with order of uTMDPDF and ..FF = " + str(order_of_uTMDandFF))
    exit()


if( vrs == 0 ):
        const_folderadd = "sv19/"
elif( vrs == 1 ):
        const_folderadd = "next1/"

#global_error_factor = 1   #multiply all errors with this to shrink it for precison testing

initial_values_file = ARCHIVEPATH + "/run" + str(nParams) + "/output_parameters"
#f=open(ARCHIVEPATH + "/rminmax",'r')
#runlimits = f.read().splitlines()
#iRmin = int(runlimits[0])
#iRmax = int(runlimits[1])
#f.close()
#iRun = iRmin # start here.
#while(exists(ARCHIVEPATH + "/run" + str(iRun) )):
#    iRun +=1
#    if(iRun > iRmax):
#        print(iRun,"max runs in directory reached.")
#        exit()

#relative_to_maindir = "../../"
constfiledir = "/home/mov57924/work/artemide/constfiles/"
if(nOrder == 0):
    constfileadress = constfiledir + "constfile_N0LO"
    if(vrs == 0):
        constfileadress += "_sv19"
else:
    constfileadress = constfiledir + const_folderadd + str(order_of_uTMDandFF) + "/" +  constfilename
print("this is run number " + str(iRun) + ".")
runDir = ARCHIVEPATH + "/run" + str(iRun)
#os.mkdir(runDir)
open(runDir + "/logfile", 'a').close()
shutil.copy2(constfileadress,runDir + "/constfile")
print("A")
print(constfileadress)
print("A")
shutil.copy2(python_code_file,runDir)

#exit(1)

path_to_constants = runDir + "/" + "constfile"

f=open(runDir + "/timestamp",'w')
current_time = datetime.datetime.now()
f.write("start=")
f.write(str(current_time.year) + " : ")
f.write(str(current_time.month) + " : ")
f.write(str(current_time.day) + " : ")
f.write(str(current_time.hour) + " : ")
f.write(str(current_time.minute) + "\n")
f.close()

#functions

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



savedTime=time.time()
def SaveToLog(text):
    global savedTime,logFile
    newTime=time.time()
    
    import socket
    PCname=socket.gethostname()
    
    passedTime=newTime-savedTime
    hours=int(passedTime/3600)
    minutes=int((passedTime-hours*3600)/60)
    seconds=int(passedTime-hours*3600-minutes*60)
    
    with open(logFile, 'a') as file:
        file.write(PCname+ ' : ' + time.ctime()+' :  [+'+str(hours)+':'+str(minutes)+':'+str(seconds)+' ]\n')
        file.write(' --> '+text+'\n')
        file.write('\n')
    savedTime=time.time()



def loadThisDataDY(listOfNames):    
    import DataProcessor.DataSet
    
    path_to_data=MAINPATH + "DataLib/unpolDY/"
    
    
    dataCollection=[]
    for name in listOfNames:
        loadedData=DataProcessor.DataSet.LoadCSV(path_to_data+name+".csv")
        dataCollection.append(loadedData)   

    return dataCollection

def loadThisDataSIDIS(listOfNames):    
    import DataProcessor.DataSet
    
    path_to_data=MAINPATH + "DataLib/unpolSIDIS/"
    
    
    dataCollection=[]
    for name in listOfNames:
        loadedData=DataProcessor.DataSet.LoadCSV(path_to_data+name+".csv")
        dataCollection.append(loadedData)   

    return dataCollection


#copied from online forum to round numbers.
from math import log10 , floor
def round_it(x, sig):
    if(x == 0):
        return 0
    else:
        return round(x, sig-int(floor(log10(abs(x))))-1)




#LOAD DATA

dataListDY = ['CDF1', 'CDF2', 'D01', 'D02', 'D02m', 
                          'A7-00y10', 'A7-10y20','A7-20y24', 
                          'A8-00y04', 'A8-04y08', 'A8-08y12', 'A8-12y16', 'A8-16y20', 'A8-20y24', 
                          'A8-46Q66', 'A8-116Q150', 
                          'CMS7', 'CMS8', 
                          'LHCb7', 'LHCb8', 'LHCb13', 
                          'PHE200', 'E228-200', 'E228-300', 'E228-400', 
                          'E772',
                          'E605']
dataListDY = ['CDF1','CMS7', 'CMS8']
dataListSIDIS = [
                      'hermes.p.vmsub.zxpt.pi+','hermes.p.vmsub.zxpt.pi-',
                      'hermes.d.vmsub.zxpt.pi+','hermes.d.vmsub.zxpt.pi-',
                      'hermes.p.vmsub.zxpt.k+','hermes.p.vmsub.zxpt.k-',
                      'hermes.d.vmsub.zxpt.k+','hermes.d.vmsub.zxpt.k-',
                      'compass.d.h+','compass.d.h-']
dataListSIDIS = ['compass.d.h+']

theData=DataProcessor.DataMultiSet.DataMultiSet("DYset",loadThisDataDY(dataListDY))
                          

setDY=theData.CutData(cutFunc)

theData=DataProcessor.DataMultiSet.DataMultiSet("SIDISset",loadThisDataSIDIS(dataListSIDIS))


setSIDIS=theData.CutData(cutFunc) 

print('Loaded ', setDY.numberOfSets, 'data sets with', sum([i.numberOfPoints for i in setDY.sets]), 'points.')
print('Loaded experiments are', [i.name for i in setDY.sets])

print('Loaded ', setSIDIS.numberOfSets, 'data sets with', sum([i.numberOfPoints for i in setSIDIS.sets]), 'points.')
print('Loaded experiments are', [i.name for i in setSIDIS.sets])

SaveToLog('Loaded '+ str(setDY.numberOfSets) + ' data sets with '+str(sum([i.numberOfPoints for i in setDY.sets])) + ' points. \n'
+'Loaded experiments are '+str([i.name for i in setDY.sets]))

datasets_file = runDir + "/datasets"

f = open(datasets_file, 'w')
f.write("DY data:\n" + str(dataListDY) + "\nSIDIS data:" + str(dataListSIDIS))
f.close()




def chi2(p):
        #print("in chi2")
        startT=time.time()
        #print(initialValues)
        #print("survived")
        global chi2_call_counter 
        chi2_call_counter += 1
        pR = p[0]
        pP = p[1]
        pF = p[2]
        x = pR + pP + pF
        #global repDataSIDIS, repDataDY
        repDataDY = setDY
        repDataSIDIS = setSIDIS
        
        totalNnew=repDataDY.numberOfPoints+repDataSIDIS.numberOfPoints
        harpy.setNPparameters(x)
        #print('np set =',["{:8.3f}".format(i) for i in p], end =" ")
        
        ccDY2,cc3=DataProcessor.harpyInterface.ComputeChi2(repDataDY)
        ccSIDIS2,cc3=DataProcessor.harpyInterface.ComputeChi2(repDataSIDIS)
        cc=(ccDY2+ccSIDIS2)/totalNnew
        #cc=ccDY2/totalNDY #THIS ONE FOR DY ONLY
        #print("D")
        endT=time.time()
        print(':->',cc,'       t=',endT-startT)
        logfile = runDir + "/logfile"
        log_step(x, cc,logfile)
        #print("chi2 quasi finished")
        #return ccDY2
        return cc
#for tests..
def chi2(p):
    x = p[1][0]
    print(x)
    y = p[1][1]
    print(y)
    #exit()
    f = (x+3)*(x+3) + (y-1)*(y-1)    
    return f

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

initialParams_fromoldrun = []
print(" use initial values from python script.")
initialTMDRValues = [2.0, 0.039487913636830296] # this is default SV19 ( i think)
initialTMDFFValues = [0.39066964680746497, 0.43884593436935954, 0.42616597768139564, 0.4799926928570539] # SV19
if(vrs==1):
    initialTMDPDFValues = [0.07136630476959344, 0.042758167553562876, 0.018835107268067305, 0.5162400047920188, 2.0981381993942765e-06, 34.74101835939999, 0.00027847396116793913, 0.7046630538705065, 1.4120038822623292e-05, 1.4820880075601222, 1.6178016221529636, 0.0] # these are for MSHT20 from "flavour bias paper"
elif(vrs==0):
    initialTMDPDFValues = [0.184739, 6.22437, 588.193, 2.44327,-2.51106, 0.0, 0.0]



initialValues = initialTMDRValues + initialTMDPDFValues + initialTMDFFValues
initialErrors = [abs( x * 0.005) for x in initialValues] #choose close too starting values (choose small errros as first steps). I start with 5% of Vals.

searchLimits = [(0,0) for x in initialValues]# to create List with same size
for i in range(0, len(initialValues)):
    x = initialValues[i]
    tolerance = 0.05
    a = tolerance * x
    b = 1/tolerance * x
    if(x > 0):
        limits = (a,b)
    else:
        limits = (b,a)
    searchLimits[i] = limits

harpy.initialize(path_to_constants)

print(initialTMDRValues)
harpy.setNPparameters_TMDR(initialTMDRValues)
print(initialTMDPDFValues)
harpy.setNPparameters_uTMDPDF(initialTMDPDFValues)
print(initialTMDFFValues)
harpy.setNPparameters_uTMDFF(initialTMDFFValues) 
#exit(2)
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
