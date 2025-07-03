#!/bin/bash
echo 'these are the arguments'
echo $*

echo 'i am in this directory'
echo $PWD

cd ${1}
source /cvmfs/cms.cern.ch/cmsset_default.sh
eval `scram runtime -sh`
echo "i am in this directory ${PWD} and doingthis ${2}"

basecmd="python plots_VVsemilep.py --results --year ${3} --nLep 1 --finalState boosted  --sel ${4} --lf ${5} --applylepSFs --doWJ  " #

if [[ $# -eq 7 ]]; then
     cmd_more="  --WC ${7}"  ##loop hole: won't use the pf for the SM case 
elif [[ $# -eq 8 ]]; then
     cmd_more=" --WC ${7} --smeft "
else
    cmd_more=" "
fi

cmd_emore=" "

case ${2} in
    plots)	
	#ls /eos/user/a/anmehta/www/ || exit 11
	ls /eos/user/ || exit 11
	cmd_emore="  --dW plots --pv ${6} " # --fCR " #--postfitCR " #" # --dCF " #--fCR "
	;;
    cards)
	cmd_emore=" --dW cards --fv ${6} " #--fCRwC"
	;;    
esac
echo ${basecmd} ${cmd_more} ${cmd_emore}
${basecmd} ${cmd_more}  ${cmd_emore}



