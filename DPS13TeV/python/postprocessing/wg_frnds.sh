#!/bin/sh                                                                                                                        
for i in {1..17}
do

    python postproc_batch.py -N 170000  -t treeProducerSusyMultilepton --moduleList DEFAULT_MODULES /afs/cern.ch/work/a/anmehta/work/Test/Test2/CMSSW_8_0_25/src/CMGTools/DPS13TeV/python/plotter/Friends_2017_WZ_Oct26/ --treeName Friends  test_BDT_wg -d tree_Friend_WZ$i.root  --friend

    
done