#!/bin/bash

###### analysis steps starting from nanoAOD samples -------------->
## post-processing steps: base ntuples (nanoAODs postprocessor)-> recl frnds (MVA WPs from ttH_modules.py) -> bdtiv -> skimming (skims the base ntuples + recl frnds) -> links to flips 
## run post-skimming frnds 


######## fixed inputs no matter what
baseDir='/eos/cms/store/cmst3/group/dpsww/'

######## MVA WPs, year ans steps to run on 
runWhat=${1}; shift;
year=${1}; shift; 
samples=${1}; shift;
#runWhat=${1}
#steps=("bdtiv")

echo $runWhat,$year,$samples

################### following should not be changed
if [[ ${samples} == "skim" ]];then
    #Trees="signal_fullstats_skim2lss/"
    Trees='NanoTrees_v7_dpsww_skim2lss' 
    nEvt=50000
else
    #Trees='NanoTrees_v7_dpsww_04092020'
    Trees="signal_fullstats/"
    nEvt=20000

fi
################################

case ${runWhat} in
1)
	friends=("recl");	;;
2)
	friends=("jme" "lepSFs" "taucount" "mupf" "puwts"); ;;
3)
	friends=("bdtiv" "recl_allvars"); ;;
4)
	friends=("bTagSF" "bdtDisc"); ;;
*)
	friends=${runWhat}; ;;
esac;

######################################################## sequences 
#echo $*
#echo "The number of arguments is: $#"

for stepToRun in "${friends[@]}"
do

    if [[ "${stepToRun}" == "recl" ]];	

    then
	echo "recl"
	#python prepareEventVariablesFriendTree.py -t NanoAOD ${baseDir}/${Trees}/${year}/ ${baseDir}/${Trees}/${year}/2_recl/ -I CMGTools.DPSWW.tools.nanoAOD.ttH_modules recleaner_step1,recleaner_step2_mc,mcMatch_seq,higgsDecay,triggerSequence -N 10000  --de .*Run.* -q condor --maxruntime 50 --log $PWD/logs #--de .*Run.* -d WWDoubleTo2L_newsim
	###python prepareEventVariablesFriendTree.py -t NanoAOD  ${baseDir}/${Trees}/${year}/  ${baseDir}/${Trees}/${year}/2_recl/ -I CMGTools.DPSWW.tools.nanoAOD.ttH_modules recleaner_step1,recleaner_step2_data,triggerSequence  -N 60000 -d DoubleEG_Run2016C_02Apr2020 -q condor  --maxruntime 50 --log $PWD/logs #--dm .*Run.*

    fi

#%%%%%%%%%%%%%%%%%%%%%%%%%%%%%
 
   if [[ "${stepToRun}" == "bdtiv" ]];    

   then
	echo "bdtiv"
	#python prepareEventVariablesFriendTree.py -t NanoAOD ${baseDir}/${Trees}/${year}/ ${baseDir}/${Trees}/${year}/bdt_input_vars_toInfnBeynd -F Friends ${baseDir}/${Trees}/${year}/2_recl/{cname}_Friend.root --FMC Friends ${baseDir}/${Trees}/${year}/0_jmeUnc_v2/{cname}_Friend.root -I CMGTools.DPSWW.tools.nanoAOD.ttH_modules dpsvars${year}MC  -N 100000 #-q condor --maxruntime 100 --log $PWD/logs  #  --de .*Run.*


    fi
#%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%

   if [[ "${stepToRun}" == "bdtDisc" ]];    

   then    
       echo "bdtDisc ${stepToRun}"

       #python prepareEventVariablesFriendTree.py -t NanoAOD ${baseDir}/${Trees}/${year}/ ${baseDir}/${Trees}/${year}/dpsbdt_neu_ssnoeebkg_afacdps_allVars -F Friends ${baseDir}/${Trees}/${year}/bdt_input_vars_toInfnBeynd/{cname}_Friend.root -I CMGTools.DPSWW.tools.nanoAOD.ttH_modules bdtvars_withpt_${year}VarU,bdtvars_withpt_${year}VarD,bdtvars_withpt_${year} -N 10000 -d WZTo3LNu_ewk  -q condor --maxruntime 200 --log  $PWD/logs #--de .*Run.*
       #python prepareEventVariablesFriendTree.py -t NanoAOD ${baseDir}/${Trees}/${year}/ ${baseDir}/${Trees}/${year}/dpsbdt_neu_ssnoeebkg_afacdps_unclEn -F Friends ${baseDir}/${Trees}/${year}/bdt_input_vars_toInfnBeynd/{cname}_Friend.root -I CMGTools.DPSWW.tools.nanoAOD.ttH_modules bdtvars_withpt_${year},bdtvars_withpt_${year}Up,bdtvars_withpt_${year}Down -N 70000 #-q condor --maxruntime 200 --log  $PWD/logs 

       ##python prepareEventVariablesFriendTree.py -t NanoAOD ${baseDir}/${Trees}/${year}/ ${baseDir}/${Trees}/${year}/dpsbdt_neu_ssnoeebkg_afacdps -F Friends ${baseDir}/${Trees}/${year}/bdt_input_vars_toInfnBeynd/{cname}_Friend.root -I CMGTools.DPSWW.tools.nanoAOD.ttH_modules bdtvars_withpt_$year -N 70000 #-q condor --maxruntime 200 --log  $PWD/logs


   fi
#%%%%%%%%%%%%%%%%%%%

   if [[ "${stepToRun}" == "postFSR" ]]; 

   then
       Trees="signal_fullstats_nosel/"      
       #python prepareEventVariablesFriendTree.py -t NanoAOD ${baseDir}/${Trees}/${year}/ ${baseDir}/${Trees}/${year}/postFSRinfo/ -I CMGTools.DPSWW.tools.nanoAOD.ttH_modules genInfo_py8_fur_taus --de .*herwig.* -N ${nEvt}  -q condor --maxruntime 50 --log $PWD/logs
       #python prepareEventVariablesFriendTree.py -t NanoAOD ${baseDir}/${Trees}/${year}/ ${baseDir}/${Trees}/${year}/postFSRinfo/ -I CMGTools.DPSWW.tools.nanoAOD.ttH_modules genInfo_hw_fur_taus  --dm .*herwig.* -N ${nEvt}  -q condor --maxruntime 50 --log $PWD/logs

   fi
#%%%%%%%%%%%%%%%%%%%%%%%%%

   if [[ "${stepToRun}" == "npdf" ]];    

   then
       echo "npdf"
       #python prepareEventVariablesFriendTree.py -t NanoAOD ${baseDir}/${Trees}/${year}/ ${baseDir}/${Trees}/${year}/nnpdf_rms -I CMGTools.DPSWW.tools.nanoAOD.ttH_modules rms_val --de .*Run.* -N 100000  -q condor --maxruntime 50 --log $PWD/logs
   fi

#%%%%%% lepton scale factors 

   if [[ "${stepToRun}" == "lepSFs" ]];    

   then
       echo "lepsfs"
       #python prepareEventVariablesFriendTree.py -t NanoAOD ${baseDir}/${Trees}/${year}/ ${baseDir}/${Trees}/${year}/4_scalefactors -F Friends ${baseDir}/${Trees}/${year}/2_recl/{cname}_Friend.root -I CMGTools.DPSWW.tools.nanoAOD.ttH_modules leptonSFs  -N ${nEvt} --de .*Run.*  -q condor --maxruntime 50 --log $PWD/logs #--de .*Run.* 

   fi

#%%%%%% new puwts

   if [[ "${stepToRun}" == "puwts" ]];    

   then
       echo "running puwts"
       #python prepareEventVariablesFriendTree.py -t NanoAOD ${baseDir}/${Trees}/${year}/ ${baseDir}/${Trees}/${year}/puWts -F Friends ${baseDir}/${Trees}/${year}/2_recl/{cname}_Friend.root -I CMGTools.DPSWW.tools.nanoAOD.ttH_modules newpuwts  -N 1000000 --de .*Run.*  -q condor --maxruntime 50 --log $PWD/logs #--de .*Run.* 

   fi

############ muon prefiring wst

   if [[ "${stepToRun}" == "mupf" ]];    

   then   
       echo "running mupf"
       #python prepareEventVariablesFriendTree.py -t NanoAOD ${baseDir}/${Trees}/${year}/ ${baseDir}/${Trees}/${year}/muPrefiring -F Friends ${baseDir}/${Trees}/${year}/2_recl/{cname}_Friend.root -I CMGTools.DPSWW.tools.nanoAOD.ttH_modules sfs_${year}  -N 2000000  --de .*Run.* -q condor --maxruntime 80 --log $PWD/logs #--de .*Run.* 

   fi
########## tau count

   if [[ "${stepToRun}" == "taucount" ]];    

   then
       echo "taucount"
       #python prepareEventVariablesFriendTree.py -t NanoAOD ${baseDir}/${Trees}/${year}/ ${baseDir}/${Trees}/${year}/3_tauCount/  -F Friends  ${baseDir}/${Trees}/${year}/2_recl/{cname}_Friend.root  -I CMGTools.DPSWW.tools.nanoAOD.ttH_modules countTaus  -N ${nEvt} -q condor --de .*Run.* --maxruntime 50 --log $PWD/logs #-d WZTo3LNu_ewk  -q condor --maxruntime 50 --log $PWD/logs #--dm .*forFlips.*

   fi
############ jme 

    if [[ "${stepToRun}" == "jme" ]];       

    then
	echo "jme"
	#python prepareEventVariablesFriendTree.py -t NanoAOD ${baseDir}/${Trees}/${year}/ ${baseDir}/${Trees}/${year}/0_jmeUnc_v2/  -I CMGTools.DPSWW.tools.nanoAOD.ttH_modules jme${year}_allvariations  -N ${nEvt} --de .*Run.*  -q condor --maxruntime 70 --log $PWD/logs # --de .*Run.*
    fi

######### recl_allvars

  if [[ "${stepToRun}" == "recl_allvars" ]];   

  then
      echo 'i assume you have already got jme frnds'
      #python prepareEventVariablesFriendTree.py -t NanoAOD ${baseDir}/${Trees}/${year}/ ${baseDir}/${Trees}/${year}/2_recl_allvars/  -I CMGTools.DPSWW.tools.nanoAOD.ttH_modules recleaner_step1,recleaner_step2_mc_allvariations,mcMatch_seq,triggerSequence -F Friends ${baseDir}/${Trees}/${year}/0_jmeUnc_v2/{cname}_Friend.root  -N ${nEvt} --de .*Run.* -q condor --maxruntime 100 --log $PWD/logs        #--de .*Run.*
      
  fi
#####################

  if [[ "${stepToRun}" == "bTagSF" ]]; 

  then
      echo 'btag'
      #python prepareEventVariablesFriendTree.py -t NanoAOD ${baseDir}/${Trees}/${year}/ ${baseDir}/${Trees}/${year}/2_btag_SFs/  -I CMGTools.DPSWW.tools.nanoAOD.ttH_modules scaleFactorSequence_allVars_${year} --FMC Friends ${baseDir}/${Trees}/${year}/0_jmeUnc_v2/{cname}_Friend.root  -F Friends ${baseDir}/${Trees}/${year}/2_recl_allvars//{cname}_Friend.root -N 100000  --de .*Run.*   -q condor --maxruntime 70 --log $PWD/logs        #--de .*Run.* removed total uncert from jetmetgrouper.py
      
  fi

done
friends=""

#test commands 


###python prepareEventVariablesFriendTree.py -t NanoAOD ${baseDir}/NanoTrees_TTH_090120_091019_v6_skim2lss/${year}/ test_dps -F Friends ${baseDir}/NanoTrees_TTH_090120_091019_v6_skim2lss/${year}/bdt_input_vars/{cname}_Friend.root -I CMGTools.DPSWW.tools.nanoAOD.ttH_modules BDT_DPSWW -N 1000 -d WWTo2L2Nu_DPS  -c 0


###python prepareEventVariablesFriendTree.py -t NanoAOD ${baseDir}/Lepton_id_study/WWTo2L2Nu_DoubleScattering_13TeV-pythia8/ test_dps  -I CMGTools.DPSWW.tools.nanoAOD.ttH_modules collectionMerger_DPSWW -d 0426786A-643C-B84B-A2FC-16B82CC5B955 -N 50000  

###python prepareEventVariablesFriendTree.py -t NanoAOD  /eos/cms/store/cmst3/group/dpsww/Summer16nanoaodV7/ test_DPS_CM -I CMGTools.DPSWW.tools.nanoAOD.ttH_modules lepMergeOnly -d WWTo2L2Nu_DoubleScattering_13TeV-pythia8 -N 100 -c 0

###python prepareEventVariablesFriendTree.py -t NanoAOD  /eos/cms/store/cmst3/group/dpsww/Summer16nanoaodV7/ /eos/cms/store/cmst3/group/dpsww/Summer16nanoaodV7/collection_merged_loosesel -I CMGTools.DPSWW.tools.nanoAOD.ttH_modules lepMerge -d WWTo2L2Nu_DoubleScattering_13TeV-pythia8 -N 1000000 -q condor --maxruntime 100 --log $PWD/logs 

###python prepareEventVariablesFriendTree.py -t NanoAOD ${baseDir}/NanoTrees_v7_dpsww_04092020/2016/ ${baseDir}/NanoTrees_v7_dpsww_04092020/2016/fakeRateWt -F Friends ${baseDir}/NanoTrees_v7_dpsww_04092020/2016/2_recl/{cname}_Friend.root -I CMGTools.DPSWW.tools.nanoAOD.ttH_modules frWt -N 50000 -d DoubleMuon_Run2016B_02Apr2020 -c 0





