#!/bin/bash

###### analysis steps starting from nanoAOD samples -------------->
## post-processing steps: base ntuples (nanoAODs postprocessor)-> recl frnds (MVA WPs from ttH_modules.py) -> bdtiv -> skimming (skims the base ntuples + recl frnds) -> links to flips 
## run post-skimming frnds 


######## fixed inputs no matter what
baseDir='/eos/cms/store/cmst3/group/dpsww/'
#Trees='NanoTrees_v7_dpsww_04092020' 
Trees='hw_2018'
######## MVA WPs, year ans steps to run on 
year=${1} 
samples=${2}
steps=("recl") # "bdtiv") 
#options "recl" "bdtiv" "jme" "lepSFs" "taucount" "bdtDisc" "recl_allvars"  "postFSR" 


#post-skimming options : jme lepSFs taucount recl_allvars; first three can run in parallel; recl_allvars step uses jme frnds

################### following should not be changed
skimmedTrees='NanoTrees_v7_dpsww_skim2lss'

for stepToRun in "${steps[@]}"
do
    echo running ${stepToRun} frnds production for ${year}
    if [ "$(ls -A logs/)" ]; then
	echo "clean the logs before the next condor submission" 
    fi
    if [[ "${stepToRun}" == "recl" ]];
	then
	python prepareEventVariablesFriendTree.py -t NanoAOD ${baseDir}/${Trees}/${year}/ ${baseDir}/${Trees}/${year}/2_recl/ -I CMGTools.DPSWW.tools.nanoAOD.ttH_modules recleaner_step1,recleaner_step2_mc,mcMatch_seq,higgsDecay,triggerSequence  -N 60000 --de .*Run.* -q condor --maxruntime 50 --log $PWD/logs #--de .*Run.*
	python prepareEventVariablesFriendTree.py -t NanoAOD  ${baseDir}/${Trees}/${year}/  ${baseDir}/${Trees}/${year}/2_recl/ -I CMGTools.DPSWW.tools.nanoAOD.ttH_modules recleaner_step1,recleaner_step2_data,triggerSequence  -N 60000 --dm .*Run.* -q condor  --maxruntime 50 --log $PWD/logs #--dm .*Run.*
    fi

    if [[ "${stepToRun}" == "bdtiv" ]];
    then
	
	python prepareEventVariablesFriendTree.py -t NanoAOD ${baseDir}/${Trees}/${year}/ ${baseDir}/${Trees}/${year}/bdt_input_vars_toInfnBeynd -F Friends ${baseDir}/${Trees}/${year}/2_recl/{cname}_Friend.root --FMC Friends ${baseDir}/${Trees}/${year}/0_jmeUnc_v2/{cname}_Friend.root -I CMGTools.DPSWW.tools.nanoAOD.ttH_modules dpsvars${year}MC  --de .*Run.* -N 100000 -q condor --maxruntime 100 --log $PWD/logs  #

	python prepareEventVariablesFriendTree.py -t NanoAOD ${baseDir}/${Trees}/${year}/ ${baseDir}/${Trees}/${year}/bdt_input_vars_toInfnBeynd -F Friends ${baseDir}/${Trees}/${year}/2_recl/{cname}_Friend.root --FMC Friends ${baseDir}/${Trees}/${year}/0_jmeUnc_v2/{cname}_Friend.root -I CMGTools.DPSWW.tools.nanoAOD.ttH_modules dpsvars${year}data  -N 100000 --dm .*Run.* -q condor --maxruntime 70 --log $PWD/logs 
	#--dm GG.* --dm T.*G.*

    fi
   if [[ "${stepToRun}" == "bdtDisc" ]]; then
       python prepareEventVariablesFriendTree.py -t NanoAOD ${baseDir}/${Trees}/${year}/ ${baseDir}/${Trees}/${year}/dpsbdt_HEM -F Friends ${baseDir}/${Trees}/${year}/bdt_input_vars_toInfnBeynd/{cname}_Friend.root -I CMGTools.DPSWW.tools.nanoAOD.ttH_modules bdtvars_withcpt_$year,bdtvars_withpt_$year,bdtvars_withcpt_${year}Up,bdtvars_withpt_${year}Up,bdtvars_withcpt_${year}Down,bdtvars_withpt_${year}Down  -N 100000  -d $2 -c $3 # -q condor --maxruntime 200 --log  $PWD/logs  #
       #python prepareEventVariablesFriendTree.py -t NanoAOD ${baseDir}/${Trees}/${year}/ ${baseDir}/${Trees}/${year}/dpsbdt_jec -F Friends ${baseDir}/${Trees}/${year}/bdt_input_vars_toInfnBeynd/{cname}_Friend.root -I CMGTools.DPSWW.tools.nanoAOD.ttH_modules Bdtvars_withcpt_$year,Bdtvars_withpt_$year,Bdtvars_withcpt_${year}Up,Bdtvars_withpt_${year}Up,Bdtvars_withcpt_${year}Down,Bdtvars_withpt_${year}Down  -N 100000  -d WWW -q condor --maxruntime 200 --log  $PWD/logs 
       #--dm .*Run.*

       #--dm GG.* --dm T.*G.*

   fi


   if [[ "${stepToRun}" == "postFSR" ]]; then
       python prepareEventVariablesFriendTree.py -t NanoAOD  ${baseDir}/signal_summer16_nanoV7/ ${baseDir}/signal_summer16_nanoV7/postFSRinfoV1/ -I CMGTools.DPSWW.tools.nanoAOD.ttH_modules genInfo_py8 -N 50000 -d WWTo2L2Nu_DoubleScattering_13TeV-pythia8 -q condor --maxruntime -N 50000 20 --log $PWD/logs
       python prepareEventVariablesFriendTree.py -t NanoAOD  ${baseDir}/signal_summer16_nanoV7/ ${baseDir}/signal_summer16_nanoV7/postFSRinfoV1/ -I CMGTools.DPSWW.tools.nanoAOD.ttH_modules genInfo_hw -N 50000 -d WWTo2L2Nu_DoubleScattering_13TeV-herwigpp -q condor --maxruntime -N 50000 20 --log $PWD/logs
   fi
#%%%%%%%%%%%%%%%%%%%% followings can be run on both skimmed and unskimmed samples 

   if [[ "${stepToRun}" == "lepSFs" ]]; then
       if [[ ${samples} == "skim" ]];then 
	   python prepareEventVariablesFriendTree.py -t NanoAOD ${baseDir}/${skimmedTrees}/${year}/ ${baseDir}/${skimmedTrees}/${year}/3_scalefactors_fixed -F Friends ${baseDir}/${skimmedTrees}/${year}/2_recl/{cname}_Friend.root -I CMGTools.DPSWW.tools.nanoAOD.ttH_modules leptonSFs  -N 70000  --de .*Run.* -q condor --maxruntime 30 --log $PWD/logs #--de .*Run.* 
       else	   
	   python prepareEventVariablesFriendTree.py -t NanoAOD ${baseDir}/${Trees}/${year}/ ${baseDir}/${Trees}/${year}/3_scalefactors -F Friends ${baseDir}/${Trees}/${year}/2_recl/{cname}_Friend.root -I CMGTools.DPSWW.tools.nanoAOD.ttH_modules leptonSFs -N 100000  --de .*Run.*  -q condor --maxruntime 40 --log $PWD/logs 

       fi
   fi

   if [[ "${stepToRun}" == "taucount" ]]; then
       if [[ ${samples} == "skim" ]];then
	   python prepareEventVariablesFriendTree.py -t NanoAOD ${baseDir}/${skimmedTrees}/${year}/ ${baseDir}/${skimmedTrees}/${year}/3_tauCount/  -F Friends  ${baseDir}/${skimmedTrees}/${year}/2_recl/{cname}_Friend.root  -I CMGTools.DPSWW.tools.nanoAOD.ttH_modules countTaus  -N 70000  -q condor --maxruntime 50 --log $PWD/logs #--dm .*forFlips.*
       else
	   python prepareEventVariablesFriendTree.py -t NanoAOD ${baseDir}/${Trees}/${year}/ ${baseDir}/${Trees}/${year}/3_tauCount/  -F Friends  ${baseDir}/${Trees}/${year}/2_recl/{cname}_Friend.root  -I CMGTools.DPSWW.tools.nanoAOD.ttH_modules countTaus  -N 100000 -d DoubleMuon_Run2018B_02Apr2020 -q condor --maxruntime 40 --log $PWD/logs #--dm .*forFlips.*
       fi
   fi

    if [[ "${stepToRun}" == "jme" ]];
    then
	if [[ ${samples} == "skim" ]];then

	python prepareEventVariablesFriendTree.py -t NanoAOD ${baseDir}/${skimmedTrees}/${year}/ ${baseDir}/${skimmedTrees}/${year}/0_jmeUnc_v2/  -I CMGTools.DPSWW.tools.nanoAOD.ttH_modules jme${year}_allvariations  -N 70000  -d WWW #--de .*Run.* -q condor --maxruntime 40 --log $PWD/logs 
	else

	    python prepareEventVariablesFriendTree.py -t NanoAOD ${baseDir}/${Trees}/${year}/ ${baseDir}/${Trees}/${year}/0_jmeUnc_v2/  -I CMGTools.DPSWW.tools.nanoAOD.ttH_modules jme${year}_allvariations  -N 70000 -d WWW    #--de .*Run.* -q condor --maxruntime 70 --log $PWD/logs 



	fi
    fi
  if [[ "${stepToRun}" == "recl_allvars" ]]; then
      echo 'i assume you have already got jme frnds'
      if [[ ${samples} == "skim" ]];then
	  python prepareEventVariablesFriendTree.py -t NanoAOD ${baseDir}/${skimmedTrees}/${year}/ ${baseDir}/${skimmedTrees}/${year}/3_recl_allvars/  -I CMGTools.DPSWW.tools.nanoAOD.ttH_modules recleaner_step1,recleaner_step2_mc_allvariations,mcMatch_seq,triggerSequence -F Friends ${baseDir}/${skimmedTrees}/${year}/0_jmeUnc_v2/{cname}_Friend.root  -N 70000 --de .*Run.* -q condor --maxruntime 40 --log $PWD/logs        #--de .*Run.*

      else

	  python prepareEventVariablesFriendTree.py -t NanoAOD ${baseDir}/${Trees}/${year}/ ${baseDir}/${Trees}/${year}/3_recl_allvars/  -I CMGTools.DPSWW.tools.nanoAOD.ttH_modules recleaner_step1,recleaner_step2_mc_allvariations,mcMatch_seq,triggerSequence -F Friends ${baseDir}/${Trees}/${year}/0_jmeUnc_v2/{cname}_Friend.root  -N 100000  -d TGJets_lep  -c 2 #-q condor --maxruntime 100 --log $PWD/logs        #--de .*Run.*
	  #python prepareEventVariablesFriendTree.py -t NanoAOD ${baseDir}/${Trees}/${year}/ ${baseDir}/${Trees}/${year}/3_recl_allvars/  -I CMGTools.DPSWW.tools.nanoAOD.ttH_modules recleaner_step1,recleaner_step2_mc_allvariations,mcMatch_seq,triggerSequence -F Friends ${baseDir}/${Trees}/${year}/0_jmeUnc_v2/{cname}_Friend.root  -N 100000  -d GGZZ4L -c 2 
	  
	  #python prepareEventVariablesFriendTree.py -t NanoAOD ${baseDir}/${Trees}/${year}/ ${baseDir}/${Trees}/${year}/3_recl_allvars/  -I CMGTools.DPSWW.tools.nanoAOD.ttH_modules recleaner_step1,recleaner_step2_mc_allvariations,mcMatch_seq,triggerSequence -F Friends ${baseDir}/${Trees}/${year}/0_jmeUnc_v2/{cname}_Friend.root  -N 100000  -d W2JetsToLNu -c 4
	  #python prepareEventVariablesFriendTree.py -t NanoAOD ${baseDir}/${Trees}/${year}/ ${baseDir}/${Trees}/${year}/3_recl_allvars/  -I CMGTools.DPSWW.tools.nanoAOD.ttH_modules recleaner_step1,recleaner_step2_mc_allvariations,mcMatch_seq,triggerSequence -F Friends ${baseDir}/${Trees}/${year}/0_jmeUnc_v2/{cname}_Friend.root  -N 100000  -d WZTo3LNu_fxfx -c 21 
	  #python prepareEventVariablesFriendTree.py -t NanoAOD ${baseDir}/${Trees}/${year}/ ${baseDir}/${Trees}/${year}/3_recl_allvars/  -I CMGTools.DPSWW.tools.nanoAOD.ttH_modules recleaner_step1,recleaner_step2_mc_allvariations,mcMatch_seq,triggerSequence -F Friends ${baseDir}/${Trees}/${year}/0_jmeUnc_v2/{cname}_Friend.root  -N 100000  -d WZTo3LNu_mllmin01 -c 0
	  #python prepareEventVariablesFriendTree.py -t NanoAOD ${baseDir}/${Trees}/${year}/ ${baseDir}/${Trees}/${year}/3_recl_allvars/  -I CMGTools.DPSWW.tools.nanoAOD.ttH_modules recleaner_step1,recleaner_step2_mc_allvariations,mcMatch_seq,triggerSequence -F Friends ${baseDir}/${Trees}/${year}/0_jmeUnc_v2/{cname}_Friend.root  -N 100000  -d ZGToLLG_01J_amcatnlo -c 38 -c 7

      fi
  fi


  if [[ "${stepToRun}" == "bTagSF" ]]; then
      echo 'i assume you have already got jme frnds'
      if [[ ${samples} == "skim" ]];then
	  python prepareEventVariablesFriendTree.py -t NanoAOD ${baseDir}/${skimmedTrees}/${year}/ ${baseDir}/${skimmedTrees}/${year}/2_btag_SFs/  -I CMGTools.DPSWW.tools.nanoAOD.ttH_modules  scaleFactorSequence_allVars_${year} --FMC Friends ${baseDir}/${skimmedTrees}/${year}/0_jmeUnc_v1/{cname}_Friend.root  -F Friends ${baseDir}/${skimmedTrees}/${year}/2_recl_allvars/{cname}_Friend.root -N 70000 -d WWW  #--de .*Run.* -q condor --maxruntime 60 --log $PWD/logs    
      else
	  python prepareEventVariablesFriendTree.py -t NanoAOD ${baseDir}/${Trees}/${year}/ ${baseDir}/${Trees}/${year}/2_btag_SFs/  -I CMGTools.DPSWW.tools.nanoAOD.ttH_modules scaleFactorSequence_allVars_${year} --FMC Friends ${baseDir}/${Trees}/${year}/0_jmeUnc_v1/{cname}_Friend.root  -F Friends ${baseDir}/${Trees}/${year}/3_recl_allvars//{cname}_Friend.root -N 1000 -d WWW -c 0 #00  --de .*Run.*   -q condor --maxruntime 100 --log $PWD/logs        #--de .*Run.*
      fi
  fi

done


#test commands 


#python prepareEventVariablesFriendTree.py -t NanoAOD ${baseDir}/NanoTrees_TTH_090120_091019_v6_skim2lss/${year}/ test_dps -F Friends ${baseDir}/NanoTrees_TTH_090120_091019_v6_skim2lss/${year}/bdt_input_vars/{cname}_Friend.root -I CMGTools.DPSWW.tools.nanoAOD.ttH_modules BDT_DPSWW -N 1000 -d WWTo2L2Nu_DPS  -c 0


#python prepareEventVariablesFriendTree.py -t NanoAOD ${baseDir}/Lepton_id_study/WWTo2L2Nu_DoubleScattering_13TeV-pythia8/ test_dps  -I CMGTools.DPSWW.tools.nanoAOD.ttH_modules collectionMerger_DPSWW -d 0426786A-643C-B84B-A2FC-16B82CC5B955 -N 50000  

#python prepareEventVariablesFriendTree.py -t NanoAOD  /eos/cms/store/cmst3/group/dpsww/Summer16nanoaodV7/ test_DPS_CM -I CMGTools.DPSWW.tools.nanoAOD.ttH_modules lepMergeOnly -d WWTo2L2Nu_DoubleScattering_13TeV-pythia8 -N 100 -c 0

#python prepareEventVariablesFriendTree.py -t NanoAOD  /eos/cms/store/cmst3/group/dpsww/Summer16nanoaodV7/ /eos/cms/store/cmst3/group/dpsww/Summer16nanoaodV7/collection_merged_loosesel -I CMGTools.DPSWW.tools.nanoAOD.ttH_modules lepMerge -d WWTo2L2Nu_DoubleScattering_13TeV-pythia8 -N 1000000 -q condor --maxruntime 100 --log $PWD/logs 

#python prepareEventVariablesFriendTree.py -t NanoAOD ${baseDir}/NanoTrees_v7_dpsww_04092020/2016/ ${baseDir}/NanoTrees_v7_dpsww_04092020/2016/fakeRateWt -F Friends ${baseDir}/NanoTrees_v7_dpsww_04092020/2016/2_recl/{cname}_Friend.root -I CMGTools.DPSWW.tools.nanoAOD.ttH_modules frWt -N 50000 -d DoubleMuon_Run2016B_02Apr2020 -c 0




########### NOTES: ttjets_dilep for 2017 with 50k per chunk
##ttjets for 2018 too with 50k
##DoubleMuon_Run2018D_02Apr2020 -d -N 100k 
