#!/bin/env python
import ROOT
import numpy
import sys, os

#basepath_private='/eos/cms/store/group/phys_smp/ec/anmehta/WmWpToLpNujj_01j_aTGC_pTW-150toInf_mWV-600to800_4f_NLO_FXFX/'
dirname=sys.argv[1]
basepath_private='/eos/cms/store/group/phys_smp/ec/anmehta/Feb2024/%s/'%dirname #WpWmToLpNujj_01j_aTGC_pTW-150toInf_mWV-600to800_4f_NLO_FXFX/' #/eos/cms/store/group/phys_smp/ec/anmehta/aTGCSep2023/%s/'%dirname
files =   [os.path.join(basepath_private,x) for x in os.listdir(basepath_private) if os.path.isfile(os.path.join(basepath_private, x)) ] 

ref=ROOT.TFile.Open(files[0])
faultyfiles=[]
def checkfaulty(fname):
    probe=ROOT.TFile.Open(fname)

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
