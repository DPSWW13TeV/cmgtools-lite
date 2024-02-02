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
if [[ $# -eq 8 ]]; then
    python plots_VVsemilep.py --results --dW plots --year ${2} --nLep ${3} --finalState ${4} --pv ${5}   --sel ${6} --lf ${7} --WC ${8} --applylepSFs  #--dCF ##--applylepSFs ##--runblind --dCF
else
    python plots_VVsemilep.py --results --dW plots --year ${2} --nLep ${3} --finalState ${4} --pv ${5}   --sel ${6} --lf ${7} --WC ${8} --pf ${9} --applylepSFs #--dCF   ##--applylepSFs   --runblind --dCF
fi

#python runDPS.py --asym --dW plots --year ${2} --finalState ${3}  --applylepSFs  --pf asym_chk 
