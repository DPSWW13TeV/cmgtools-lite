#!/bin/bash
echo 'these are the arguments'
echo $*

echo 'i am in this directory'
echo $PWD

cd /afs/cern.ch/work/a/anmehta/public/cmgtools_WVsemilep/CMSSW_10_6_29/src/CMGTools/VVsemilep/python/plotter
#cd ${1}
source /cvmfs/cms.cern.ch/cmsset_default.sh
eval `scram runtime -sh`
echo "i am in this directory ${PWD} and doingthis ${2}"
#python plots_VVsemilep.py --simple --year fullRun2 --proc WV --sel sig_incl  --pm nostack --smeft --pWC

#for i in fullRun2 2017 2016 2016APV 2018; do python plots_VVsemilep.py --simple --SC --proc WW --sel boosted --year ${i}; done
#for i in fullRun2 2017 2016 2016APV 2018; do python plots_VVsemilep.py --simple --SC --proc WW --smeft --sel boosted --year ${i}; done
#for i in fullRun2 2017 2016 2016APV 2018; do python plots_VVsemilep.py --simple --SC --proc WZ --smeft --sel boosted --year ${i}; done
#for i in fullRun2 2017 2016 2016APV 2018; do python plots_VVsemilep.py --simple --SC --proc WZ --sel boosted --year ${i}; done
#. runSkimming.sh 
#source ${2} ${3}
#python ${2} ${3}

python runAllGOFs.py --doToys
#python plots_VVsemilep.py --alpha --lf onelep --year ${2}
#cp -r /eos/cms/store/cmst3/group/dpsww/SMEFT_samples /eos/cms/store/group/phys_smp/ec/anmehta/

#python ${2}
