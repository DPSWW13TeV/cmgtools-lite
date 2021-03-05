#!/bin/bash
###### analysis steps starting from nanoAOD samples -------------->
## post-processing steps: base ntuples (nanoAODs postprocessor)-> recl frnds (MVA WPs from ttH_modules.py) -> bdtiv -> skimming (skims the base ntuples + recl frnds) -> links to flips 
## run post-skimming frnds 


######## fixed inputs no matter what
baseDir='/eos/cms/store/cmst3/group/dpsww/'
Trees='NanoTrees_v7_dpsww_04092020' 
#Trees='jobs_2016Data/'

######## MVA WPs, year ans steps to run on 
pf= '' #'_muWP90_elWP70'
year='2018'
steps=("recl_allvars") #"bdtiv" "jme" "lepSFs" "taucount") #unskimmedrecl_allvars") #"jme" "lepSFs" "taucount") # "bdtiv" "unskimmedtaucount") #"unskimmedbdtDisc")  #options "recl" "bdtiv" "jme" "lepSFs" "taucount" "bdtDisc" "unskimmedbdtDisc" "recl_allvars" "unskimmedlepSFs" "postFSR" unskimmedtaucount

#pre-skimming options recl bdtiv unskimmedlepSFs unskimmedbdtDisc postFSR 
#post-skimming options : jme lepSFs taucount recl_allvars; first three can run in parallel; recl_allvars step uses jme frnds



################### following should not be changed
skimmedTrees='NanoTrees_v7_dpsww_skim2lss'${pf} 

for stepToRun in "${steps[@]}"
do
    echo running ${stepToRun} frnds production for ${year} with MVA WPs ${pf}
    if [ "$(ls -A logs/)" ]; then
	echo "clean the logs before the next condor submission" 
    fi
    if [[ "${stepToRun}" == "recl" ]];
	then
	python prepareEventVariablesFriendTree.py -t NanoAOD ${baseDir}/${Trees}/${year}/ ${baseDir}/${Trees}/${year}/2_recl${pf}/ -I CMGTools.DPSWW.tools.nanoAOD.ttH_modules recleaner_step1,recleaner_step2_mc,mcMatch_seq,higgsDecay,triggerSequence  -N 60000 -d GGZZ4e -q condor --maxruntime 50 --log $PWD/logs
	#	python prepareEventVariablesFriendTree.py -t NanoAOD ${baseDir}/${Trees}/${year}/ ${baseDir}/${Trees}/${year}/2_recl${pf}/ -I CMGTools.DPSWW.tools.nanoAOD.ttH_modules recleaner_step1,recleaner_step2_mc,mcMatch_seq,higgsDecay,triggerSequence  -N 60000 --de .*Run.* -q condor --maxruntime 50 --log $PWD/logs #--de .*Run.*
	#python prepareEventVariablesFriendTree.py -t NanoAOD  ${baseDir}/${Trees}/${year}/  ${baseDir}/${Trees}/${year}/2_recl${pf}/ -I CMGTools.DPSWW.tools.nanoAOD.ttH_modules recleaner_step1,recleaner_step2_data,triggerSequence  -N 60000 --dm .*Run.* -q condor  --maxruntime 50 --log $PWD/logs #--dm .*Run.*
    fi

    if [[ "${stepToRun}" == "bdtiv" ]];
    then
	
	python prepareEventVariablesFriendTree.py -t NanoAOD ${baseDir}/${Trees}/${year}/ ${baseDir}/${Trees}/${year}/bdt_input_vars${pf} -F Friends ${baseDir}/${Trees}/${year}/2_recl${pf}/{cname}_Friend.root -I CMGTools.DPSWW.tools.nanoAOD.ttH_modules dpsvars$year${pf}  -N 100000  --dm GG.* --dm T.*G.* -q condor --maxruntime 40 --log $PWD/logs 
	#--dm GG.* --dm T.*G.*

    fi
    if [[ "${stepToRun}" == "unskimmedlepSFs" ]]; then
	python prepareEventVariablesFriendTree.py -t NanoAOD ${baseDir}/${Trees}/${year}/ ${baseDir}/${Trees}/${year}/3_scalefactors${pf} -F Friends ${baseDir}/${Trees}/${year}/2_recl${pf}/{cname}_Friend.root -I CMGTools.DPSWW.tools.nanoAOD.ttH_modules leptonSFs -N 100000  -d TTJets -c 78 -c 79 -c 80 #--de .*Run.*  -q condor --maxruntime 40 --log $PWD/logs 


    fi
   if [[ "${stepToRun}" == "unskimmedbdtDisc" ]]; then

       python prepareEventVariablesFriendTree.py -t NanoAOD ${baseDir}/${Trees}/${year}/ ${baseDir}/${Trees}/${year}/dpsbdt_ultimate${pf} -F Friends ${baseDir}/${Trees}/${year}/bdt_input_vars${pf}/{cname}_Friend.root -I CMGTools.DPSWW.tools.nanoAOD.ttH_modules bdtvars_withcpt_$year,bdtvars_withpt_$year  -N 100000 --dm GG.* --dm T.*G.* -q condor --maxruntime 40 --log  $PWD/logs 
       #--dm GG.* --dm T.*G.*

   fi
   if [[ "${stepToRun}" == "unskimmedtaucount" ]]; then
	  python prepareEventVariablesFriendTree.py -t NanoAOD ${baseDir}/${Trees}/${year}/ ${baseDir}/${Trees}/${year}/3_tauCount${pf}/  -F Friends  ${baseDir}/${Trees}/${year}/2_recl${pf}/{cname}_Friend.root  -I CMGTools.DPSWW.tools.nanoAOD.ttH_modules countTaus  -N 100000  -q condor --maxruntime 40 --log $PWD/logs #--dm .*forFlips.*
   fi

    if [[ "${stepToRun}" == "unskimmedjme" ]];
    then
	python prepareEventVariablesFriendTree.py -t NanoAOD ${baseDir}/${Trees}/${year}/ ${baseDir}/${Trees}/${year}/0_jmeUnc_v1${pf}/  -I CMGTools.DPSWW.tools.nanoAOD.ttH_modules jme${year}_allvariations  -N 70000 --de .*Run.* -q condor --maxruntime 70 --log $PWD/logs 
	python prepareEventVariablesFriendTree.py -t NanoAOD ${baseDir}/${Trees}/${year}/ ${baseDir}/${Trees}/${year}/0_jmeUnc_v1${pf}/  -I CMGTools.DPSWW.tools.nanoAOD.ttH_modules jme${year}_allvariations  -N 70000 -d TTW_LO -c 5

    fi
  if [[ "${stepToRun}" == "unskimmedrecl_allvars" ]]; then
      echo 'i assume you have already got jme frnds'
     # python prepareEventVariablesFriendTree.py -t NanoAOD ${baseDir}/${Trees}/${year}/ ${baseDir}/${Trees}/${year}/2_recl_allvars${pf}/  -I CMGTools.DPSWW.tools.nanoAOD.ttH_modules recleaner_step1,recleaner_step2_mc_allvariations,mcMatch_seq,triggerSequence -F Friends ${baseDir}/${Trees}/${year}/0_jmeUnc_v1${pf}/{cname}_Friend.root  -N 100000 -q condor --maxruntime 50 --log $PWD/logs        #-de .*Run.*
      python prepareEventVariablesFriendTree.py -t NanoAOD ${baseDir}/${Trees}/${year}/ ${baseDir}/${Trees}/${year}/2_recl_allvars${pf}/  -I CMGTools.DPSWW.tools.nanoAOD.ttH_modules recleaner_step1,recleaner_step2_mc_allvariations,mcMatch_seq,triggerSequence -F Friends ${baseDir}/${Trees}/${year}/0_jmeUnc_v1${pf}/{cname}_Friend.root  -N 100000 -d DYJetsToLL_M50_LO -c 10 -c 2


  fi

   if [[ "${stepToRun}" == "postFSR" ]]; then
       python prepareEventVariablesFriendTree.py -t NanoAOD  ${baseDir}/signal_summer16_nanoV7/ ${baseDir}/signal_summer16_nanoV7/postFSRinfoV1/ -I CMGTools.DPSWW.tools.nanoAOD.ttH_modules genInfo_py8 -N 50000 -d WWTo2L2Nu_DoubleScattering_13TeV-pythia8 -q condor --maxruntime -N 50000 20 --log $PWD/logs
       python prepareEventVariablesFriendTree.py -t NanoAOD  ${baseDir}/signal_summer16_nanoV7/ ${baseDir}/signal_summer16_nanoV7/postFSRinfoV1/ -I CMGTools.DPSWW.tools.nanoAOD.ttH_modules genInfo_hw -N 50000 -d WWTo2L2Nu_DoubleScattering_13TeV-herwigpp -q condor --maxruntime -N 50000 20 --log $PWD/logs
   fi

############ everything onwards is post-skimming

    if [[ "${stepToRun}" == "jme" ]];
    then
	echo "jme frnds"
	python prepareEventVariablesFriendTree.py -t NanoAOD ${baseDir}/${skimmedTrees}/${year}/ ${baseDir}/${skimmedTrees}/${year}/0_jmeUnc_v1/  -I CMGTools.DPSWW.tools.nanoAOD.ttH_modules jme${year}_allvariations  -N 70000 -d TTZ_LO -c 0 #--de .*Run.* -q condor --maxruntime 40 --log $PWD/logs #--de .*Run.*



    fi
  if [[ "${stepToRun}" == "recl_allvars" ]]; then
      echo 'i assume you have already got jme frnds'
      python prepareEventVariablesFriendTree.py -t NanoAOD ${baseDir}/${skimmedTrees}/${year}/ ${baseDir}/${skimmedTrees}/${year}/2_recl_allvars/  -I CMGTools.DPSWW.tools.nanoAOD.ttH_modules recleaner_step1,recleaner_step2_mc_allvariations,mcMatch_seq,triggerSequence -F Friends ${baseDir}/${skimmedTrees}/${year}/0_jmeUnc_v1/{cname}_Friend.root  -N 70000 -d WGToLNuG_01J_amcatnlo -q condor --maxruntime 40 --log $PWD/logs        #--de .*Run.*

  fi
  
   if [[ "${stepToRun}" == "lepSFs" ]]; then
       python prepareEventVariablesFriendTree.py -t NanoAOD ${baseDir}/${skimmedTrees}/${year}/ ${baseDir}/${skimmedTrees}/${year}/3_scalefactors_fixed -F Friends ${baseDir}/${skimmedTrees}/${year}/2_recl/{cname}_Friend.root -I CMGTools.DPSWW.tools.nanoAOD.ttH_modules leptonSFs  -N 70000  -d GGZZ4L -c 4 #--de .*Run.* -q condor --maxruntime 30 --log $PWD/logs #--de .*Run.* 
   fi
   if [[ "${stepToRun}" == "taucount" ]]; then
      python prepareEventVariablesFriendTree.py -t NanoAOD ${baseDir}/${skimmedTrees}/${year}/ ${baseDir}/${skimmedTrees}/${year}/3_tauCount/  -F Friends  ${baseDir}/${skimmedTrees}/${year}/2_recl/{cname}_Friend.root  -I CMGTools.DPSWW.tools.nanoAOD.ttH_modules countTaus  -N 70000 -q condor  --maxruntime 50 --log $PWD/logs #--dm .*forFlips.*
      
   fi


done


#test commands 


#python prepareEventVariablesFriendTree.py -t NanoAOD ${baseDir}/NanoTrees_TTH_090120_091019_v6_skim2lss/${year}/ test_dps -F Friends ${baseDir}/NanoTrees_TTH_090120_091019_v6_skim2lss/${year}/bdt_input_vars/{cname}_Friend.root -I CMGTools.DPSWW.tools.nanoAOD.ttH_modules BDT_DPSWW -N 1000 -d WWTo2L2Nu_DPS  -c 0


#python prepareEventVariablesFriendTree.py -t NanoAOD ${baseDir}/Lepton_id_study/WWTo2L2Nu_DoubleScattering_13TeV-pythia8/ test_dps  -I CMGTools.DPSWW.tools.nanoAOD.ttH_modules collectionMerger_DPSWW -d 0426786A-643C-B84B-A2FC-16B82CC5B955 -N 50000  


#python prepareEventVariablesFriendTree.py -t NanoAOD ${baseDir}/NanoTrees_v7_dpsww_04092020/2016/ ${baseDir}/NanoTrees_v7_dpsww_04092020/2016/fakeRateWt -F Friends ${baseDir}/NanoTrees_v7_dpsww_04092020/2016/2_recl/{cname}_Friend.root -I CMGTools.DPSWW.tools.nanoAOD.ttH_modules frWt -N 50000 -d DoubleMuon_Run2016B_02Apr2020 -c 0




########### NOTES: ttjets_dilep for 2017 with 50k per chunk
##ttjets for 2018 too with 50k
##DoubleMuon_Run2018D_02Apr2020 -d -N 100k 
