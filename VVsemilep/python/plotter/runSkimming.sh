#!/bin/bash
baseDir='/eos/cms/store/cmst3/group/dpsww/'
Trees='NanoTrees_v9_vvsemilep_06012023/' #'vvsemilep/' 
skimmedTrees='NanoTrees_v9_vvsemilep_skimmed' 
Friends_recl_unskimmed='2_recl'

[ ! -d "$skimmedTrees" ] && mkdir -p "$skimmedTrees"
years=("2018") # "2018") # "2016")
frnds=("dpsbdt_neu_ssnoeebkg_afacdps_unclEn" "dpsbdt_neu_ssnoeebkg_afacdps") 

for yr in "${years[@]}"
do
    echo "running skimming for $yr"

    python skimTreesNew.py mca-skim-${yr}.txt vvsemilep/fullRun2/skim_1l_2los_FO.txt ${baseDir}/${skimmedTrees}/${yr}/ -P ${baseDir}/${Trees}/${yr} --Fs ${baseDir}/${Trees}/${yr}/${Friends_recl_unskimmed}  --mcc vvsemilep/fullRun2/lepchoice-ttH-FO.txt  -j 1  --tree NanoAOD #--skim-friends

    #for frnd in "${frnds[@]}"
    #do
    #	#echo "running for ${frnd}"
    #	python skimFTreesNew.py ${baseDir}/${skimmedTrees}/${yr}/ ${baseDir}/${Trees}/${yr}/${frnd}/
    #done


done


   
##Syntax: python skimTreesNew.py <mca.txt> <sel.txt> <outdir> -P <indir with trees> --Fs <unkimmed recl frnds> <--skim-friends if want to skim frnds as well> -mcc <FO.txt> 


#python skimFTreesNew.py ${baseDir}/${Trees}_skim2lss_mvawp_mupt90_elpt70_2021/2017/ ${baseDir}/${Trees}/2017/dpsbdt/



#python skimFTreesNew.py /eos/cms/store/cmst3/group/dpsww/NanoTrees_v7_dpsww_skim2lss/2016/ /eos/cms/store/cmst3/group/dpsww/NanoTrees_v7_dpsww_04092020/2016/dpsbdt_ultimate
#python skimFTreesNew.py /eos/cms/store/cmst3/group/dpsww/NanoTrees_v7_dpsww_skim2lss_muWP90_elWP70/2017/ /eos/cms/store/cmst3/group/dpsww/NanoTrees_v7_dpsww_04092020/2017/dpsbdt_ultimate_muWP90_elWP70/
######main cmd

    #python skimTreesNew.py mca-skim-${yr}.txt dps-ww/fullRun2/skim_2lss_3l_FO.txt ${baseDir}/jobs_2016Data_skimmed/${yr}/ -P ${baseDir}/jobs_2016Data/${yr}/  --Fs ${baseDir}/jobs_2016Data/${yr}/${Friends_recl_unskimmed} --skim-friends --mcc dps-ww/fullRun2/lepchoice-ttH-FO.txt -j8  --tree NanoAOD --skim-friends
