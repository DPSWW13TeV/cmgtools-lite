#!/bin/bash
echo 'these are the arguments'
echo $*

echo 'i am in this directory'
echo $PWD

#cd ${1}
#eval $(scramv1 runtime -sh);

echo "i am in this directory ${PWD}"

#cp -r /eos/cms/store/cmst3/group/dpsww/SMEFT_samples/${1} /eos/cms/store/group/phys_smp/ec/anmehta/smeft_FEB2025_UL_FR2/

haddChunks.py -n  --max-size 40 /eos/cms/store/cmst3/group/dpsww/jobs_${2}

##amcd /eos/cms/store/cmst3/group/dpsww/NanoTrees_v9_vvsemilep_06012023/2018
##am#echo "i am in this directory ${PWD}"

#python checkfaulty_nAODfiles.py ${2} ${3}
#python runhaddNano.py ${2} ${3} ${4}

#haddnano.py ${1} ${2} ${3}
#fi


