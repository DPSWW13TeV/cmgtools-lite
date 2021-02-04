#!/bin/bash
###### analysis steps starting from nanoAOD samples -------------->
## post-processing steps: base ntuples (nanoAODs postprocessor)-> recl frnds (MVA WPs from ttH_modules.py) -> bdtiv -> skimming (skims the base ntuples + recl frnds) -> links to flips 
## run post-skimming frnds 


######## fixed inputs no matter what
baseDir='/eos/cms/store/cmst3/group/dpsww/'
Trees='NanoTrees_v7_dpsww_04092020' 


######## MVA WPs, year ans steps to run on 
pf='_muWP90_elWP60'
year='2017'
steps=("unskimmedbdtDisc")  #options "recl" "bdtiv" "jme" "lepSFs" "taucount" "bdtDisc" "unskimmedbdtDisc" "recl_allvars" "unskimmedlepSFs" "postFSR")
#pre-skimming options recl bdtiv unskimmedlepSFs unskimmedbdtDisc postFSR 
#post-skimming options : jme lepSFs taucount recl_allvars; first three can run in parallel; recl_allvars step uses jme frnds




################### following should not be changed
skimmedTrees='NanoTrees_v7_dpsww_skim2lss'${pf}
Friends_recl='2_recl'
Friends_recl_unskimmed='2_recl'${pf}
Friends_bdtiv_unskimmed='bdt_input_vars'${pf}
Friends_lepSFs_unskimmed='3_scalefactors'${pf}
Friends_bdtDisc_unskimmed='dpsbdt'${pf}




for stepToRun in "${steps[@]}"
do
    echo running ${stepToRun} frnds production for ${year} with MVA WPs ${pf}
    if [ "$(ls -A logs/)" ]; then
	echo "clean the logs before the next condor submission" 
    fi
    if [[ "${stepToRun}" == "recl" ]];
	then
	python prepareEventVariablesFriendTree.py -t NanoAOD ${baseDir}/${Trees}/${year}/ ${baseDir}/${Trees}/${year}/${Friends_recl_unskimmed}/ -I CMGTools.DPSWW.tools.nanoAOD.ttH_modules recleaner_step1,recleaner_step2_mc,mcMatch_seq,higgsDecay,triggerSequence  -N 50000 --de .*Run.* -q condor --maxruntime 50 --log $PWD/logs #
	python prepareEventVariablesFriendTree.py -t NanoAOD  ${baseDir}/${Trees}/${year}/  ${baseDir}/${Trees}/${year}/${Friends_recl_unskimmed}/ -I CMGTools.DPSWW.tools.nanoAOD.ttH_modules recleaner_step1,recleaner_step2_data,triggerSequence   -N 50000 --dm .*Run.* -q condor  --maxruntime 50 --log $PWD/logs #--dm .*Run.*
    fi

    if [[ "${stepToRun}" == "bdtiv" ]];
    then
	
	python prepareEventVariablesFriendTree.py -t NanoAOD ${baseDir}/${Trees}/${year}/ ${baseDir}/${Trees}/${year}/${Friends_bdtiv_unskimmed} -F Friends ${baseDir}/${Trees}/${year}/${Friends_recl_unskimmed}/{cname}_Friend.root -I CMGTools.DPSWW.tools.nanoAOD.ttH_modules dpsvars2017 -N 50000 -q condor --maxruntime 30 --log $PWD/logs #year needs to be changed for 2016 

    fi
    if [[ "${stepToRun}" == "unskimmedlepSFs" ]]; then
	python prepareEventVariablesFriendTree.py -t NanoAOD ${baseDir}/${Trees}/${year}/ ${baseDir}/${Trees}/${year}/${Friends_lepSFs_unskimmed} -F Friends ${baseDir}/${Trees}/${year}/${Friends_recl_unskimmed}/{cname}_Friend.root -I CMGTools.DPSWW.tools.nanoAOD.ttH_modules leptonSFs -N 50000  --de .*Run.*  -q condor --maxruntime 30 --log $PWD/logs 

    fi
   if [[ "${stepToRun}" == "unskimmedbdtDisc" ]]; then
       python prepareEventVariablesFriendTree.py -t NanoAOD ${baseDir}/${Trees}/${year}/ ${baseDir}/${Trees}/${year}/${Friends_bdtDisc_unskimmed} -F Friends ${baseDir}/${Trees}/${year}/${Friends_bdtiv_unskimmed}/{cname}_Friend.root -I CMGTools.DPSWW.tools.nanoAOD.ttH_modules bdtvars2017 -N 50000 -q condor --maxruntime 30 --log $PWD/logs #year needs to be changed for 2016 bdtvars2017
   fi
   if [[ "${stepToRun}" == "postFSR" ]]; then
       python prepareEventVariablesFriendTree.py -t NanoAOD  ${baseDir}/signal_summer16_nanoV7/ ${baseDir}/signal_summer16_nanoV7/postFSRinfoV1/ -I CMGTools.DPSWW.tools.nanoAOD.ttH_modules genInfo_py8 -N 50000 -d WWTo2L2Nu_DoubleScattering_13TeV-pythia8 -q condor --maxruntime 100 --log $PWD/logs
       python prepareEventVariablesFriendTree.py -t NanoAOD  ${baseDir}/signal_summer16_nanoV7/ ${baseDir}/signal_summer16_nanoV7/postFSRinfoV1/ -I CMGTools.DPSWW.tools.nanoAOD.ttH_modules genInfo_hw -N 50000 -d WWTo2L2Nu_DoubleScattering_13TeV-herwigpp -q condor --maxruntime 100 --log $PWD/logs
   fi

############ everything onwards is post-skimming

    if [[ "${stepToRun}" == "jme" ]];
    then
	echo "jme frnds"
	python prepareEventVariablesFriendTree.py -t NanoAOD ${baseDir}/${skimmedTrees}/${year}/ ${baseDir}/${skimmedTrees}/${year}/0_jmeUnc_v1/  -I CMGTools.DPSWW.tools.nanoAOD.ttH_modules jme${year}_allvariations  -N 70000 --de .*Run.*  -q condor --maxruntime 50 --log $PWD/logs #--de .*Run.*

    fi
  if [[ "${stepToRun}" == "recl_allvars" ]]; then
      echo 'i assume you have already got jme frnds'
      python prepareEventVariablesFriendTree.py -t NanoAOD ${baseDir}/${skimmedTrees}/${year}/ ${baseDir}/${skimmedTrees}/${year}/${Friends_recl}_allvars/  -I CMGTools.DPSWW.tools.nanoAOD.ttH_modules recleaner_step1,recleaner_step2_mc_allvariations,mcMatch_seq,triggerSequence -F Friends ${baseDir}/${skimmedTrees}/${year}/0_jmeUnc_v1/{cname}_Friend.root  -N 50000 --de .*Run.* -N 70000  -q condor --maxruntime 50 --log $PWD/logs        #
  fi
  
   if [[ "${stepToRun}" == "lepSFs" ]]; then
       python prepareEventVariablesFriendTree.py -t NanoAOD ${baseDir}/${skimmedTrees}/${year}/ ${baseDir}/${skimmedTrees}/${year}/3_scalefactors -F Friends ${baseDir}/${skimmedTrees}/${year}/${Friends_recl}/{cname}_Friend.root -I CMGTools.DPSWW.tools.nanoAOD.ttH_modules leptonSFs  -N 50000 --de .*Run.* -q condor --maxruntime 50 --log $PWD/logs 
   fi
   if [[ "${stepToRun}" == "taucount" ]]; then
      python prepareEventVariablesFriendTree.py -t NanoAOD ${baseDir}/${skimmedTrees}/${year}/ ${baseDir}/${skimmedTrees}/${year}/3_tauCount/  -F Friends  ${baseDir}/${skimmedTrees}/${year}/${Friends_recl}/{cname}_Friend.root  -I CMGTools.DPSWW.tools.nanoAOD.ttH_modules countTaus  -N 70000 -q condor --maxruntime 50 --log $PWD/logs #--dm .*forFlips.*
      
   fi
   if [[ "${stepToRun}" == "bdtDisc" ]]; then
       python prepareEventVariablesFriendTree.py -t NanoAOD ${baseDir}/${skimmedTrees}/${year}/ ${baseDir}/${skimmedTrees}/${year}/dpsbdt -F Friends ${baseDir}/${Trees}/${year}/bdt_input_vars/{cname}_Friend.root -I CMGTools.DPSWW.tools.nanoAOD.ttH_modules BDT_DPSWW -N 50000  -q condor --maxruntime 50 --log $PWD/logs
   fi

done


#test commands 


#python prepareEventVariablesFriendTree.py -t NanoAOD ${baseDir}/NanoTrees_TTH_090120_091019_v6_skim2lss/${year}/ test_dps -F Friends ${baseDir}/NanoTrees_TTH_090120_091019_v6_skim2lss/${year}/bdt_input_vars/{cname}_Friend.root -I CMGTools.DPSWW.tools.nanoAOD.ttH_modules BDT_DPSWW -N 1000 -d WWTo2L2Nu_DPS  -c 0


#python prepareEventVariablesFriendTree.py -t NanoAOD ${baseDir}/Lepton_id_study/WWTo2L2Nu_DoubleScattering_13TeV-pythia8/ test_dps  -I CMGTools.DPSWW.tools.nanoAOD.ttH_modules collectionMerger_DPSWW -d 0426786A-643C-B84B-A2FC-16B82CC5B955 -N 50000  


#python prepareEventVariablesFriendTree.py -t NanoAOD ${baseDir}/NanoTrees_v7_dpsww_04092020/2016/ ${baseDir}/NanoTrees_v7_dpsww_04092020/2016/fakeRateWt -F Friends ${baseDir}/NanoTrees_v7_dpsww_04092020/2016/${Friends_recl}/{cname}_Friend.root -I CMGTools.DPSWW.tools.nanoAOD.ttH_modules frWt -N 50000 -d DoubleMuon_Run2016B_02Apr2020 -c 0




########### NOTES: ttjets_dilep for 2017 with 50k per chunk
##ttjets for 2018 too with 50k
##DoubleMuon_Run2018D_02Apr2020 -d -N 100k 
