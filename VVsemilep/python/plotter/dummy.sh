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



case ${2} in
    plots)	
	#ls /eos/user/a/anmehta/www/ || exit 11
	ls /eos/user || exit 11
	python plots_VVsemilep.py --results --dW plots  --doWJ --year ${3} --nLep 1 --finalState ${4}  --sel ${5} --lf ${6} --applylepSFs  --fCR --pv ${7} #--fCR
    ;;
    cards)
	case ${5} in
	    sig|sb_lo|sb_hi)
		if [[ $# -lt 8 ]]; then
		    echo "python plots_VVsemilep.py --results --dW cards  --doWJ --year ${3} --nLep 1 --finalState ${4}  --sel ${5} --lf ${6} --applylepSFs --WC ${7}"
		    python plots_VVsemilep.py --results --dW cards  --doWJ --year ${3} --nLep 1 --finalState ${4}  --sel ${5} --lf ${6} --applylepSFs --WC ${7} 
		else
		    echo "python plots_VVsemilep.py --results --dW cards  --doWJ --year ${3} --nLep 1 --finalState ${4}  --sel ${5} --lf ${6} --applylepSFs --WC ${7} --pf ${8}"
		    python plots_VVsemilep.py --results --dW cards  --doWJ --year ${3} --nLep 1 --finalState ${4}  --sel ${5} --lf ${6} --applylepSFs --WC ${7} --pf ${8}
		fi
		;;
	    *)
		if [[ $# -lt 7 ]]; then
		    echo "python plots_VVsemilep.py --results --dW cards  --doWJ --year ${3} --nLep 1 --finalState ${4}  --sel ${5} --lf ${6} --applylepSFs"
		    python plots_VVsemilep.py --results --dW cards  --doWJ --year ${3} --nLep 1 --finalState ${4}  --sel ${5} --lf ${6} --applylepSFs 
		else
		    echo "python plots_VVsemilep.py --results --dW cards  --doWJ --year ${3} --nLep 1 --finalState ${4}  --sel ${5} --lf ${6} --applylepSFs --pf ${7}"
		    python plots_VVsemilep.py --results --dW cards  --doWJ --year ${3} --nLep 1 --finalState ${4}  --sel ${5} --lf ${6} --applylepSFs --pf ${7}
		fi
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
