#!/bin/bash
baseDir='/eos/cms/store/cmst3/group/dpsww/'
Trees='NanoTrees_v7_dpsww_04092020' # trees (unskimmed)
skimmedTrees='NanoTrees_v7_dpsww_skim2lss' #_muWP90_elWP70'
Friends_recl_unskimmed='2_recl' #_muWP90_elWP70'

years=("2017") # "2018") # "2016")
for yr in "${years[@]}"
do
    echo "running skimming for $yr"
    
    ##ampython skimFTreesNew.py /eos/cms/store/cmst3/group/dpsww/NanoTrees_v7_dpsww_skim2lss/${yr}/ /eos/cms/store/cmst3/group/dpsww/NanoTrees_v7_dpsww_04092020/${yr}/dpsbdt_allyrs_unclEn/
    ##ampython skimFTreesNew.py /eos/cms/store/cmst3/group/dpsww/NanoTrees_v7_dpsww_skim2lss/${yr}/ /eos/cms/store/cmst3/group/dpsww/NanoTrees_v7_dpsww_04092020/${yr}/dpsbdt_allyrs/
    ##ampython skimFTreesNew.py /eos/cms/store/cmst3/group/dpsww/NanoTrees_v7_dpsww_skim2lss/${yr}/ /eos/cms/store/cmst3/group/dpsww/NanoTrees_v7_dpsww_04092020/${yr}/dpsbdt_neu_ssnoeebkg_afacdps_unclEn/
    ##ampython skimFTreesNew.py /eos/cms/store/cmst3/group/dpsww/NanoTrees_v7_dpsww_skim2lss/${yr}/ /eos/cms/store/cmst3/group/dpsww/NanoTrees_v7_dpsww_04092020/${yr}/dpsbdt_neu_ssnoeebkg_afacdps/
    ##ampython skimFTreesNew.py /eos/cms/store/cmst3/group/dpsww/NanoTrees_v7_dpsww_skim2lss/${yr}/ /eos/cms/store/cmst3/group/dpsww/NanoTrees_v7_dpsww_04092020/${yr}/3_scalefactors_fixed/
    ##ampython skimFTreesNew.py /eos/cms/store/cmst3/group/dpsww/NanoTrees_v7_dpsww_skim2lss/${yr}/ /eos/cms/store/cmst3/group/dpsww/NanoTrees_v7_dpsww_04092020/${yr}/postFSRinfo/
    ##ampython skimFTreesNew.py /eos/cms/store/cmst3/group/dpsww/NanoTrees_v7_dpsww_skim2lss/${yr}/ /eos/cms/store/cmst3/group/dpsww/NanoTrees_v7_dpsww_04092020/${yr}/3_recl_allvars/
    ##ampython skimFTreesNew.py /eos/cms/store/cmst3/group/dpsww/NanoTrees_v7_dpsww_skim2lss/${yr}/ /eos/cms/store/cmst3/group/dpsww/NanoTrees_v7_dpsww_04092020/${yr}/0_jmeUnc_v2/
    ##ampython skimFTreesNew.py /eos/cms/store/cmst3/group/dpsww/NanoTrees_v7_dpsww_skim2lss/${yr}/ /eos/cms/store/cmst3/group/dpsww/NanoTrees_v7_dpsww_04092020/${yr}/3_tauCount
    python skimFTreesNew.py /eos/cms/store/cmst3/group/dpsww/NanoTrees_v7_dpsww_skim2lss/${yr}/ /eos/cms/store/cmst3/group/dpsww/NanoTrees_v7_dpsww_04092020/${yr}/4_scalefactorsV1

######main cmd
    #python skimTreesNew.py mca-skim-${yr}.txt dps-ww/fullRun2/skim_2lss_3l_FO.txt ${baseDir}/${skimmedTrees}/${yr}/ -P ${baseDir}/${Trees}/${yr}/  --Fs ${baseDir}/${Trees}/${yr}/${Friends_recl_unskimmed} --skim-friends --mcc dps-ww/fullRun2/lepchoice-ttH-FO.txt -j8  --tree NanoAOD --skim-friends

    #python skimTreesNew.py mca-skim-${yr}.txt dps-ww/fullRun2/skim_2lss_3l_FO.txt ${baseDir}/jobs_2016Data_skimmed/${yr}/ -P ${baseDir}/jobs_2016Data/${yr}/  --Fs ${baseDir}/jobs_2016Data/${yr}/${Friends_recl_unskimmed} --skim-friends --mcc dps-ww/fullRun2/lepchoice-ttH-FO.txt -j8  --tree NanoAOD --skim-friends


done


   
##Syntax: python skimTreesNew.py <mca.txt> <sel.txt> <outdir> -P <indir with trees> --Fs <unkimmed recl frnds> <--skim-friends if want to skim frnds as well> -mcc <FO.txt> 


#python skimFTreesNew.py ${baseDir}/${Trees}_skim2lss_mvawp_mupt90_elpt70_2021/2017/ ${baseDir}/${Trees}/2017/dpsbdt/


#python skimTreesNew.py mca-skim-2016.txt dps-ww/fullRun2/skim_2lss_3l_FO.txt ${baseDir}/${Trees}_skim2lss_mvawp_mupt90_elpt70_2021/2016/ -P ${baseDir}/${Trees}/2016/  --Fs ${baseDir}/${Trees}/2016/2_recl/ --skim-friends --mcc dps-ww/fullRun2/lepchoice-ttH-FO.txt -j8  --tree NanoAOD --skim-friends


#mv ${baseDir}/${Trees}_skim2lss_mvawp_mupt90_elpt70/2016/1_recl_mvawp_mupt90_elpt70 ${baseDir}/${Trees}_skim2lss_mvawp_mupt90_elpt70/2016/1_recl 



#python skimFTreesNew.py /eos/cms/store/cmst3/group/dpsww/NanoTrees_v7_dpsww_skim2lss/2016/ /eos/cms/store/cmst3/group/dpsww/NanoTrees_v7_dpsww_04092020/2016/dpsbdt_ultimate
#python skimFTreesNew.py /eos/cms/store/cmst3/group/dpsww/NanoTrees_v7_dpsww_skim2lss_muWP90_elWP70/2017/ /eos/cms/store/cmst3/group/dpsww/NanoTrees_v7_dpsww_04092020/2017/dpsbdt_ultimate_muWP90_elWP70/
