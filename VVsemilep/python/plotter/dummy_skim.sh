#!/bin/bash
echo 'these are the arguments'
echo $*

echo 'i am in this directory'
echo $PWD

cd ${1}
source /cvmfs/cms.cern.ch/cmsset_default.sh
eval `scram runtime -sh`
echo "i am in this directory ${PWD} and doingthis ${2}"

source ${2} ${3}
#cp -r /eos/cms/store/cmst3/group/dpsww/SMEFT_samples /eos/cms/store/group/phys_smp/ec/anmehta/

#python ${2}
