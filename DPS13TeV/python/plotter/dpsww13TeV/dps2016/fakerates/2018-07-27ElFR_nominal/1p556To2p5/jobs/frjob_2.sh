#! /bin/sh
ulimit -c 0
cd /afs/cern.ch/work/a/anmehta/work/Test/Test2/CMSSW_8_0_25;
eval $(scramv1 runtime -sh);
cd /afs/cern.ch/work/a/anmehta/work/Test/Test2/CMSSW_8_0_25/src/CMGTools/DPS13TeV/python/plotter;
python /afs/cern.ch/work/a/anmehta/work/Test/Test2/CMSSW_8_0_25/src/CMGTools/DPS13TeV/python/plotter/runDPS.py --fr --recalculate --doBin 2
