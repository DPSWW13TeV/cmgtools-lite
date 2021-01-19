#!/bin/sh
path=`pwd`
for iFile in 'fakeRate-2lss-frdata-e-be1_test.txt'; do #`ls ${path}/*.txt`; do
    cp $iFile  dummy.txt
    #echo ${iFile}
    cat dummy.txt
    #sed -e 's/fr_2016_recorrected.root : FR_mva085_mu_data_comb_recorrected/fr_2016_MVA_mupt90_elpt70.root : FR_mva090_mu_data_comb/g;s/fr_2016_recorrected.root : FR_mva080_el_data_comb_NC_recorrected/fr_2016_MVA_mupt90_elpt70.root : FR_mva070_el_data_comb_NC/g'dummy.txt > dummy1.txt
    #mv dummy1.txt $iFile
done
