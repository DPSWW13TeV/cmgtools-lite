#!/bin/bash
baseDir='/eos/cms/store/cmst3/group/dpsww/'
Trees='NanoTrees_v7_dpsww_04092020' # trees (unskimmed)
skimmedTrees='2017elWP60'
#skimmedTrees='NanoTrees_v7_dpsww_skim2lss'
Friends_recl_unskimmed='2_recl_elWP60'

years=("2017") # "2017" "2018")
for yr in "${years[@]}"
do
    echo "running skimming for $yr"
    python skimTreesNew.py mca-skim-${yr}.txt dps-ww/fullRun2/skim_2lss_3l_FO.txt ${baseDir}/${skimmedTrees}/${yr}/ -P ${baseDir}/${Trees}/${yr}/  --Fs ${baseDir}/${Trees}/${yr}/${Friends_recl_unskimmed} --skim-friends --mcc dps-ww/fullRun2/lepchoice-ttH-FO.txt -j8  --tree NanoAOD --skim-friends


done


   
##Syntax: python skimTreesNew.py <mca.txt> <sel.txt> <outdir> -P <indir with trees> --Fs <unkimmed recl frnds> <--skim-friends if want to skim frnds as well> -mcc <FO.txt> 


#python skimFTreesNew.py ${baseDir}/${Trees}_skim2lss_mvawp_mupt90_elpt70_2021/2017/ ${baseDir}/${Trees}/2017/dpsbdt/


#python skimTreesNew.py mca-skim-2016.txt dps-ww/fullRun2/skim_2lss_3l_FO.txt ${baseDir}/${Trees}_skim2lss_mvawp_mupt90_elpt70_2021/2016/ -P ${baseDir}/${Trees}/2016/  --Fs ${baseDir}/${Trees}/2016/2_recl/ --skim-friends --mcc dps-ww/fullRun2/lepchoice-ttH-FO.txt -j8  --tree NanoAOD --skim-friends


#mv ${baseDir}/${Trees}_skim2lss_mvawp_mupt90_elpt70/2016/1_recl_mvawp_mupt90_elpt70 ${baseDir}/${Trees}_skim2lss_mvawp_mupt90_elpt70/2016/1_recl 



