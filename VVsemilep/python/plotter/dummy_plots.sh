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


if [[ $# -eq 6 ]]; then
    python plots_VVsemilep.py --results --dW plots --year ${2} --nLep 1 --finalState ${3} --pv ${6}  --sel ${4} --lf ${5} --pD /eos/user/a/anmehta/www/VVsemilep/ --applylepSFs 
    python plots_VVsemilep.py --results --dW plots --year ${2} --nLep 1 --finalState ${3} --pv ${6}  --sel ${4} --lf ${5} --pD /eos/user/a/anmehta/www/VVsemilep/ --applylepSFs  --doWJ
    # --pf nopNETSF --doWJ #--dCF #--pf FC #--doWJ --pf FC ##--dCF ##--runblind 
    #    python plots_VVsemilep.py --results --dW plots --year ${2} --nLep 1 --finalState ${3} --pv ${6}  --sel ${4} --lf ${5} --pD /eos/user/a/anmehta/www/VVsemilep/ --applylepSFs  --doWJ --dCF #--pf withHEMwt #--pf sdMlt150--dCF 
else
    python plots_VVsemilep.py --results --dW plots --year ${2} --nLep 1 --finalState ${3} --pv ${6}  --sel ${4} --lf ${5} --WC ${8} --pD /eos/user/a/anmehta/www/VVsemilep/ --applylepSFs  --pf withHEMwt ##--runblind --dCF
fi

#python runDPS.py --asym --dW plots --year ${2} --finalState ${3}  --applylepSFs  --pf asym_chk 

#--perBin
