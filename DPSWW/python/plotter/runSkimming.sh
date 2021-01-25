#!/bin/bash

years=("2018") # "2017" "2018")
for yr in "${years[@]}"
do
    echo "running skimming for $yr"
    python skimTreesNew.py mca-skim-${yr}.txt dps-ww/fullRun2/skim_2lss_3l_FO.txt /eos/cms/store/cmst3/group/dpsww/NanoTrees_v7_dpsww_04092020_skim2lss_mvawp_mupt90_elpt70_2021/${yr}/ -P /eos/cms/store/cmst3/group/dpsww/NanoTrees_v7_dpsww_04092020/${yr}/  --Fs /eos/cms/store/cmst3/group/dpsww/NanoTrees_v7_dpsww_04092020/${yr}/2_recl/ --skim-friends --mcc dps-ww/fullRun2/lepchoice-ttH-FO.txt -j8  --tree NanoAOD --skim-friends


done


   
##Syntax: python skimTreesNew.py <mca.txt> <sel.txt> <outdir> -P <indir with trees> --Fs <unkimmed recl frnds> <--skim-friends if want to skim frnds as well> -mcc <FO.txt> 


#python skimFTreesNew.py /eos/cms/store/cmst3/group/dpsww/NanoTrees_v7_dpsww_04092020_skim2lss_mvawp_mupt90_elpt70_2021/2016/ /eos/cms/store/cmst3/group/dpsww/NanoTrees_v7_dpsww_04092020/2016/dpsbdt/


#python skimTreesNew.py mca-skim-2016.txt dps-ww/fullRun2/skim_2lss_3l_FO.txt /eos/cms/store/cmst3/group/dpsww/NanoTrees_v7_dpsww_04092020_skim2lss_mvawp_mupt90_elpt70_2021/2016/ -P /eos/cms/store/cmst3/group/dpsww/NanoTrees_v7_dpsww_04092020/2016/  --Fs /eos/cms/store/cmst3/group/dpsww/NanoTrees_v7_dpsww_04092020/2016/2_recl/ --skim-friends --mcc dps-ww/fullRun2/lepchoice-ttH-FO.txt -j8  --tree NanoAOD --skim-friends


#mv /eos/cms/store/cmst3/group/dpsww/NanoTrees_v7_dpsww_04092020_skim2lss_mvawp_mupt90_elpt70/2016/1_recl_mvawp_mupt90_elpt70 /eos/cms/store/cmst3/group/dpsww/NanoTrees_v7_dpsww_04092020_skim2lss_mvawp_mupt90_elpt70/2016/1_recl 



