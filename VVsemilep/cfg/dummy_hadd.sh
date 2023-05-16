#!/bin/bash
echo 'these are the arguments'
echo $*

echo 'i am in this directory'
echo $PWD

cd /afs/cern.ch/work/a/anmehta/public/cmgtools_WVsemilep/CMSSW_10_6_29/src/CMGTools/VVsemilep/cfg/
echo "i am in this directory ${PWD}"
eval $(scramv1 runtime -sh);

#cp -r ${1} /eos/cms/store/cmst3/group/dpsww/
#haddChunks.py -n  --max-size 40 /eos/cms/store/cmst3/group/dpsww/${1}
##amcd /eos/cms/store/cmst3/group/dpsww/NanoTrees_v9_vvsemilep_06012023/2018
##am#echo "i am in this directory ${PWD}"

python runhaddNano.py ${1}
#if [[ $# -eq 3 ]]; then
#haddnano.py ${1} ${2} ${3}
#else
#haddnano.py ${1} ${2} ${3} ${4}
#fi


