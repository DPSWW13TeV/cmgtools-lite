#!/bin/bash
echo 'these are the arguments'
echo $*

echo 'i am in this directory'
echo $PWD

cd ${1}
source /cvmfs/cms.cern.ch/cmsset_default.sh
eval `scram runtime -sh`
echo "i am in this directory ${PWD} and doingthis ${2}"

basecmd="python plots_VVsemilep.py --results --year ${3} --nLep 1 --finalState ${4}  --sel ${5} --lf ${6} --applylepSFs --doWJ " # --doWJ

if [[ $# -eq 8 ]]; then
     cmd_more="  --WC ${8}"
elif [[ $# -eq 9 ]]; then
     cmd_more=" --WC ${8} --pf ${9}"
else
    cmd_more=" "
fi

cmd_emore=" "

case ${2} in
    plots)	
	#ls /eos/user/a/anmehta/www/ || exit 11
	ls /eos/user/ || exit 11
	cmd_emore="  --dW plots --pv ${7} "
	;;
    cards)
	cmd_emore=" --dW cards --fv ${7} " #--fCRwC"
	;;    
esac
echo ${basecmd} ${cmd_more} ${cmd_emore}
${basecmd} ${cmd_more}  ${cmd_emore}



