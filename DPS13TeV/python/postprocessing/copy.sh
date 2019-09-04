#!/bin/sh                                                                                                                        
for i in {1..17}
do
mkdir copy_Friends_2017_WZ_Oct26/WZ$i/
mkdir copy_Friends_2017_WZ_Oct26/WZ$i/treeProducerSusyMultilepton/
mv copy_Friends_2017_WZ_Oct26/tree_Friend_WZ$i.root copy_Friends_2017_WZ_Oct26/WZ$i/treeProducerSusyMultilepton/tree.root
#cp Friends_2017_WZ_Oct26/tree_Friend_WZ$i.root /eos/user/a/anmehta/test_WZ/WZ$i/
#ln -sf  /eos/user/a/anmehta/test_WZ/WZ$i/tree_Friend_WZ$i.root ../plotter/CollectionMerger/
done