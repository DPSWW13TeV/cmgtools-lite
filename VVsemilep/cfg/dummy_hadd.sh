#!/bin/bash
echo 'these are the arguments'
echo $*

echo 'i am in this directory'
echo $PWD

cd ${1}
echo "i am in this directory ${PWD}"
eval $(scramv1 runtime -sh);

#cp -r ${1} /eos/cms/store/cmst3/group/dpsww/
#haddChunks.py -n  --max-size 40 /eos/cms/store/cmst3/group/dpsww/${1}
##amcd /eos/cms/store/cmst3/group/dpsww/NanoTrees_v9_vvsemilep_06012023/2018
##am#echo "i am in this directory ${PWD}"

#python checkfaulty_nAODfiles.py ${2}
python runhaddNano.py ${2}
#if [[ $# -eq 3 ]]; then
#haddnano.py ${1} ${2} ${3}
#else
#haddnano.py ${1} ${2} ${3} ${4}
#fi


