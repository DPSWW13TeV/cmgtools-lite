#!/bin/bash                                                                                                                       
echo 'these are the arguments'
echo $*

echo 'i am in this directory'
echo $PWD

cd ${1}
echo "i am in this directory ${PWD}"
eval $(scramv1 runtime -sh);

haddChunks.py -n /eos/cms/store/cmst3/group/dpsww/${2} --max-size 25


