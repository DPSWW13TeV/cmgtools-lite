#!/bin/bash
echo 'these are the arguments'
echo $*

echo 'i am in this directory'
echo $PWD

cd ${1}
source /cvmfs/cms.cern.ch/cmsset_default.sh
eval `scram runtime -sh`
echo "i am in this directory ${PWD} and doingthis ${2}"



case ${2} in
    plots)	
	#ls /eos/user/a/anmehta/www/ || exit 11
	ls /eos/user/ || exit 11
	python plots_VVsemilep.py --results --dW plots  --doWJ --year ${3} --nLep 1 --finalState ${4}  --sel ${5} --lf ${6} --applylepSFs  --pv ${7} #--dCF #--runblind #--fCR
    ;;
    cards)
	basecmd="python plots_VVsemilep.py --results --dW cards  --doWJ --year ${3} --nLep 1 --finalState ${4}  --sel ${5} --lf ${6} --applylepSFs  --fv ${7}"
	cmd_more=" "
	if [[ $# -eq 8 ]]; then
	    cmd_more=" --WC ${8}"
	elif [[ $# -eq 9 ]]; then
	    cmd_more=" --WC ${8} --pf ${9}"  
	else
	    cmd_more=" "
	fi;
	echo ${basecmd} ${cmd_more}
	${basecmd} ${cmd_more}
	;;    

esac



##TODO: add an option to run cards without specifying any operator?
    
#if [[ $# -lt 7 ]]; then
#    #python plots_VVsemilep.py --results --dW plots --year ${2} --nLep 1 --finalState ${3} --pv ${6}  --sel ${4} --lf ${5} --pD /eos/user/a/anmehta/www/VVsemilep/ --applylepSFs 
#
#    # --dCF #--pf FC #--doWJ ##--runblind 
#else
#    python plots_VVsemilep.py --results --dW plots --year ${2} --nLep 1 --finalState ${3} --pv ${6}  --sel ${4} --lf ${5} --WC ${8} --applylepSFs  
#fi
#
##python runDPS.py --asym --dW plots --year ${2} --finalState ${3}  --applylepSFs  --pf asym_chk 

#--perBin
