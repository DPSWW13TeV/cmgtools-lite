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

#python runDPS.py --results --dW plots --year ${2} --finalState ${3}  --applylepSFs --runblind  --splitCharge
if [[ $# -eq 6 ]]; then
    python plots_VVsemilep.py --results --dW cards --year ${2} --finalState ${3} --sel ${4} --lf ${5} --WC ${6} --applylepSFs 
else
    python plots_VVsemilep.py --results --dW cards --year ${2} --finalState ${3}  --sel ${4} --lf ${5} --WC ${6} --pf ${7} --applylepSFs
fi


#python runDPS.py --asym --dW plots --year ${2} --finalState ${3}  --applylepSFs  --pf asym_chk 
