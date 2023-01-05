#!/bin/bash
echo 'these are the arguments'
echo $*

echo 'i am in this directory'
echo $PWD

cd ${1}
echo "i am in this directory ${PWD}"
eval $(scramv1 runtime -sh);

#python runDPS.py --results --dW plots --year ${2} --finalState ${3}  --applylepSFs --runblind  --splitCharge
if [[ $# -eq 6 ]]; then
    python plots_VVsemilep.py --results --sel SR --dW plots --year ${2} --nLep ${3} --finalState ${4} --pv ${5}  --sel ${6} --applylepSFs
else
    python plots_VVsemilep.py --results --sel SR --dW plots --year ${2} --nLep ${3} --finalState ${4} --pv ${5}  --sel ${6} --pf ${7} --applylepSFs
fi

#python runDPS.py --asym --dW plots --year ${2} --finalState ${3}  --applylepSFs  --pf asym_chk 
