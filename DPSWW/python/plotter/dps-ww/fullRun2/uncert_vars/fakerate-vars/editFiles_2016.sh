#!/bin/sh
path=`pwd`
for iFile in `ls ${path}/*.txt`; do
    cat $iFile > dummy.txt
    #echo ${iFile}
    sed -e 's/fr_2017_MVA_mupt90_elpt65.root : FR_mva090_mu_data_comb/fr_2017_MVA_mupt90_elpt70.root : FR_mva090_mu_data_comb/g;s/fr_2017_MVA_mupt90_elpt65.root : FR_mva065_el_data_comb_NC/fr_2017_MVA_mupt90_elpt70.root : FR_mva070_el_data_comb_NC/g' dummy.txt > $iFile
    #sed -e 's/fr_2017_MVA_mupt90_elpt70.root : FR_mva070_el_data_comb_NC/fr_2017.root : FR_mva080_el_data_comb_NC/g' dummy.txt > $iFile
    #sed -e 's/fr_2017_MVA_mupt90_elpt70.root : FR_mva090_mu_data_comb/fr_2017.root : FR_mva085_mu_data_comb/g' dummy.txt > $iFile
    #sed -e 's/fr_2017.root : FR_mva080_el_data_comb_NC/fr_2017_MVA_mupt90_elpt65.root : FR_mva065_el_data_comb_NC/g;s/fr_2017.root : FR_mva085_mu_data_comb/fr_2017_MVA_mupt90_elpt65.root : FR_mva090_mu_data_comb/g' dummy.txt > $iFile
    #sed -e 's/fr_2017_MVA_mupt90_elpt70.root : FR_mva090_mu_data_comb/fr_2017.root : FR_mva085_mu_data_comb/g;s/fr_2017_MVA_mupt90_elpt70.root : FR_mva090_mu/fr_2017.root : FR_mva085_mu/g;s/fr_2018_recorrected.root : FR_mva085_mu_data_comb_recorrected/fr_2018.root : FR_mva085_mu_data_comb/g;s/fr_2018_recorrected.root : FR_mva080_el_data_comb_NC_recorrected/fr_2018_MVA_mupt90_elpt70.root :FR_mva070_el_data_comb_NC/g;s/fr_2018.root : FR_mva080_el/fr_2018_MVA_mupt90_elpt70.root : FR_mva070_el/g' dummy.txt > $iFile
    #sed -e 's/fr_2017_recorrected.root : FR_mva085_mu_data_comb_recorrected/fr_2017_MVA_mupt90_elpt70.root : FR_mva090_mu_data_comb/g;s/fr_2017_recorrected.root : FR_mva080_el_data_comb_NC_recorrected/fr_2017_MVA_mupt90_elpt70.root : FR_mva070_el_data_comb_NC/g;s/fr_2017.root : FR_mva085_mu/fr_2017_MVA_mupt90_elpt70.root : FR_mva090_mu/g;s/fr_2017.root : FR_mva080_el/fr_2017_MVA_mupt90_elpt70.root : FR_mva070_el/g' dummy.txt > $iFile
    rm dummy.txt
done

