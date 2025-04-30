#!/bin/env python
import ROOT
import numpy
import sys, os

dirname=sys.argv[1]
proc=sys.argv[2]
basepath_private='/eos/cms/store/group/phys_smp/ec/anmehta/Mar2025UL_FR2//%s/%s'%(dirname,proc) #
#basepath_private='/eos/cms/store/group/phys_smp/ec/anmehta/Combined_Mar2025/%s/%s'%(dirname,proc) #/Mar2025UL_FR2//%s/%s'%(dirname,proc) 
files =   [os.path.join(basepath_private,x) for x in os.listdir(basepath_private) if os.path.isfile(os.path.join(basepath_private, x)) ] 

ref=ROOT.TFile.Open(files[0])
faultyfiles=[]
def checkfaulty(fname):
    probe=ROOT.TFile.Open(fname)
    print(fname)
    for e in ref.GetListOfKeys():
        name = e.GetName()
        #print("checking" + str(name))
        obj = e.ReadObj()
        cl = ROOT.TClass.GetClass(e.GetClassName())
        inputs = ROOT.TList()
        try:
            otherObj = probe.GetListOfKeys().FindObject(name).ReadObj()
        except:
            faultyfiles.append(probe.GetName())
         #inputs.Add(otherObj)
    probe.Close()
    return True

for fn in files:
    checkfaulty(fn)
print "faulty files for process %s"%dirname,faultyfiles
