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



case ${6} in
    plots)	
	#ls /eos/user/a/anmehta/www/ || exit 11
	ls /eos/user || exit 11
	python plots_VVsemilep.py --results --dW plots  --doWJ --year ${2} --nLep 1 --finalState ${3}  --sel ${4} --lf ${5} --applylepSFs  --fCR --pv ${7} #--fCR
    ;;
    cards)
	case ${4} in
	    sig|sb_lo|sb_hi)
		echo "python plots_VVsemilep.py --results --dW cards  --doWJ --year ${2} --nLep 1 --finalState ${3}  --sel ${4} --lf ${5} --applylepSFs --WC ${7}"
		python plots_VVsemilep.py --results --dW cards  --doWJ --year ${2} --nLep 1 --finalState ${3}  --sel ${4} --lf ${5} --applylepSFs --WC ${7}
		;;
	    *)
		echo "python plots_VVsemilep.py --results --dW cards  --doWJ --year ${2} --nLep 1 --finalState ${3}  --sel ${4} --lf ${5} --applylepSFs "
	    python plots_VVsemilep.py --results --dW cards  --doWJ --year ${2} --nLep 1 --finalState ${3}  --sel ${4} --lf ${5} --applylepSFs 
	    ;;
	esac
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
