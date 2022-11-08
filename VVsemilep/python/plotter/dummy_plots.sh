#!/bin/bash
echo 'these are the arguments'
echo $*

echo 'i am in this directory'
echo $PWD

cd ${1}
echo "i am in this directory ${PWD}"
eval $(scramv1 runtime -sh);

#python runDPS.py --results --dW plots --year ${2} --finalState ${3}  --applylepSFs --runblind  --splitCharge
python plots_VVsemilep.py --results --dW plots --year ${2} --nLep 1 --finalState ${3}


#python runDPS.py --asym --dW plots --year ${2} --finalState ${3}  --applylepSFs  --pf asym_chk 
