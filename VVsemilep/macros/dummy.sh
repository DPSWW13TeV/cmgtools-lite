#!/bin/bash                                                                                                                       
echo 'these are the arguments'
echo $*

echo 'i am in this directory'
echo $PWD

cd /afs/cern.ch/work/a/anmehta/public/cmgtools_WVsemilep/CMSSW_10_6_29/src/CMGTools/VVsemilep/macros
echo "i am in this directory ${PWD}"
eval $(scramv1 runtime -sh);

. runFrnds_v3.sh recl_allvars ${1} local ${2} ${3} 

echo "done running"

echo "done copying"
