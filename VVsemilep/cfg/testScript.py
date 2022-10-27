#!/usr/bin/env python
import os, sys, datetime
import subprocess
import ROOT, commands
import re
#outputdir='/eos/cms/store/cmst3/group/dpsww/Aut18nanoaodV7/' #signal2018/'
outputdir='/eos/cms/store/cmst3/group/dpsww/Signal_nanoV7/' #signal2018/'
directive='xrdcp root://cms-xrd-global.cern.ch/'
copycmd=[];
fName='/afs/cern.ch/work/a/anmehta/public/WVsemilep/version2/CMSSW_10_6_29/src/UFHZZAnalysisRun2/test_mc18.txt'
fIn=open(fName,'r')
#miniaods=[iLine.split('\n')[0] for iLine in fIn]
miniaods=[]
if not fIn: raise RuntimeError, "Cannot open "+fName+"\n"
miniaods=[iLine.split('\n')[0].strip() for iLine in fIn if not re.match("\s*#.*", (iLine.split('\n')[0]).strip())]
##amfor iLine in fIn:
##am    if not re.match("\s*#.*", iLine.split('\n')[0].strip()):
##am        miniaods.append(iLine)
print miniaods
sampleList={}
for num,fname in enumerate(miniaods):
    dasQ='dasgoclient  -query "child dataset={ds}"'.format(ds=fname)
    nano=commands.getoutput(dasQ).split()[0]
    dasQstr='dasgoclient  -query "file dataset={ds}"'.format(ds=fname)
    allF= list(commands.getoutput(dasQstr).split())
    if not ('NanoAODv9' in nano and len(allF) > 0): continue
    info=[]
    info.append(fname)
    info.append(nano)
    info.append(allF[0] if len(allF) > 0 else '')
    sampleList[num]=info
    



for ikey,ival in sampleList.iteritems():
    print "running genxsecana for %s"%ival[1]
    cmd="cmsRun /afs/cern.ch/work/a/anmehta/public/cmgtools_WVsemilep/CMSSW_10_6_29/src/CMGTools/VVsemilep/cfg/ana.py inputFiles={here}".format(here=ival[2])
    os.system(cmd)
    print "done for %s"%ival[1]

