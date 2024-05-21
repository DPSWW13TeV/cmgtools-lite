#!/bin/bash
echo 'these are the arguments'
echo $*

echo 'i am in this directory'
echo $PWD

cd ${1}
source /cvmfs/cms.cern.ch/cmsset_default.sh
echo "i am in this directory ${PWD}"
eval `scram runtime -sh`

echo "i am in this directory ${PWD} and making this plot ${5}"

if [[ $# -eq 3 ]]; then
    python ${2} -b -r -c ${3}  #--pf ${4} #--uS
else
    python ${2} -b -r -c ${3}  --uS #--pf ${4} --uS
fi
