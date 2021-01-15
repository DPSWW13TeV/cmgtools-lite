#!/bin/bash
Trees='NanoTrees_v7_dpsww_04092020' #input trees (unskimmed)
skimmedTrees='NanoTrees_v7_dpsww_04092020_skim2lss_mvawp_mupt90_elpt70_2021'  #slimmed trees #NanoTrees_v7_dpsww_04092020_skim2lss_mvawp_mupt90_elpt70_latest'
year='2016'
Friends_recl='2_recl' 
Friends_recl_unskimmed='2_recl'
steps=("bdtiv")  #"taucount" "recl_allvars") #jme" "lepSFs" "taucount") #unskimmedlepSFs") #"bdtiv" "jme" "lepSFs" "taucount") # "bdtDisc")

## steps: 1_recl -> bdtiv -> skimming -> links to flips
## post-skimming jme, lepSFs, taucount, and bdtDisc can run in parallel; recl_allvars uses jme frnds...



for stepToRun in "${steps[@]}"
do
    echo 'did you clean the logs ?'
    if [[ "${stepToRun}" == "recl" ]];
	then
	python prepareEventVariablesFriendTree.py -t NanoAOD /eos/cms/store/cmst3/group/dpsww/${Trees}/${year}/ /eos/cms/store/cmst3/group/dpsww/${Trees}/${year}/${Friends_recl_unskimmed}/ -I CMGTools.DPSWW.tools.nanoAOD.ttH_modules recleaner_step1,recleaner_step2_mc,mcMatch_seq,higgsDecay,triggerSequence  --de .*Run.* -N 10000 -q condor --maxruntime 180 --log $PWD/logs
	python prepareEventVariablesFriendTree.py -t NanoAOD  /eos/cms/store/cmst3/group/dpsww/${Trees}/${year}/  /eos/cms/store/cmst3/group/dpsww/${Trees}/${year}/${Friends_recl_unskimmed}/ -I CMGTools.DPSWW.tools.nanoAOD.ttH_modules recleaner_step1,recleaner_step2_data,triggerSequence  --dm .*Run.*  -N 10000 -q condor  --maxruntime 180 --log $PWD/logs 
    fi
    if [[ "${stepToRun}" == "bdtiv" ]];
    then
	python prepareEventVariablesFriendTree.py -t NanoAOD /eos/cms/store/cmst3/group/dpsww/${Trees}/${year}/ /eos/cms/store/cmst3/group/dpsww/${Trees}/${year}/bdt_input_vars -F Friends /eos/cms/store/cmst3/group/dpsww/${Trees}/${year}/${Friends_recl_unskimmed}/{cname}_Friend.root -I CMGTools.DPSWW.tools.nanoAOD.ttH_modules DPSWW_vars -N 10000 -q condor --maxruntime 100 --log $PWD/logs
    fi
    if [[ "${stepToRun}" == "unskimmedlepSFs" ]]; then
	python prepareEventVariablesFriendTree.py -t NanoAOD /eos/cms/store/cmst3/group/dpsww/${Trees}/${year}/ /eos/cms/store/cmst3/group/dpsww/${Trees}/${year}/3_scalefactors_lep_fixed_EOY -F Friends /eos/cms/store/cmst3/group/dpsww/${Trees}/${year}/${Friends_recl_unskimmed}/{cname}_Friend.root -I CMGTools.DPSWW.tools.nanoAOD.ttH_modules leptonSFs -N 10000  --de .*Run.*  -q condor --maxruntime 150 --log $PWD/logs 

    fi


############ everything onwards is post-skimming

    if [[ "${stepToRun}" == "jme" ]];
    then
	echo "running on jme"
	python prepareEventVariablesFriendTree.py -t NanoAOD /eos/cms/store/cmst3/group/dpsww/${skimmedTrees}/${year}/ /eos/cms/store/cmst3/group/dpsww/${skimmedTrees}/${year}/0_jmeUnc_v1/  -I CMGTools.DPSWW.tools.nanoAOD.ttH_modules jme${year}_allvariations  --de .*Run.* -N 10000 -q condor --maxruntime 150 --log $PWD/logs #--de .*Run.*

    fi
  if [[ "${stepToRun}" == "recl_allvars" ]]; then
      echo 'i assume you have already got jme frnds'
      #
      python prepareEventVariablesFriendTree.py -t NanoAOD /eos/cms/store/cmst3/group/dpsww/${skimmedTrees}/${year}/ /eos/cms/store/cmst3/group/dpsww/${skimmedTrees}/${year}/${Friends_recl}_allvars/  -I CMGTools.DPSWW.tools.nanoAOD.ttH_modules recleaner_step1,recleaner_step2_mc_allvariations,mcMatch_seq,triggerSequence -F Friends /eos/cms/store/cmst3/group/dpsww/${skimmedTrees}/${year}/0_jmeUnc_v1/{cname}_Friend.root --de .*Run.*  -N 10000  -q condor --maxruntime 150 --log $PWD/logs  
      
  fi
  
   if [[ "${stepToRun}" == "lepSFs" ]]; then
       python prepareEventVariablesFriendTree.py -t NanoAOD /eos/cms/store/cmst3/group/dpsww/${skimmedTrees}/${year}/ /eos/cms/store/cmst3/group/dpsww/${skimmedTrees}/${year}/3_scalefactors_EOY -F Friends /eos/cms/store/cmst3/group/dpsww/${skimmedTrees}/${year}/${Friends_recl}/{cname}_Friend.root -I CMGTools.DPSWW.tools.nanoAOD.ttH_modules leptonSFs --de .*Run.*  -q condor --maxruntime 100 --log $PWD/logs 
   fi
   if [[ "${stepToRun}" == "taucount" ]]; then
      python prepareEventVariablesFriendTree.py -t NanoAOD /eos/cms/store/cmst3/group/dpsww/${skimmedTrees}/${year}/ /eos/cms/store/cmst3/group/dpsww/${skimmedTrees}/${year}/3_tauCount/  -F Friends  /eos/cms/store/cmst3/group/dpsww/${skimmedTrees}/${year}/${Friends_recl}/{cname}_Friend.root  -I CMGTools.DPSWW.tools.nanoAOD.ttH_modules countTaus  -N 10000 -q condor --maxruntime 100 --log $PWD/logs 
      
   fi
   if [[ "${stepToRun}" == "bdtDisc" ]]; then
       python prepareEventVariablesFriendTree.py -t NanoAOD /eos/cms/store/cmst3/group/dpsww/${skimmedTrees}/${year}/ /eos/cms/store/cmst3/group/dpsww/${skimmedTrees}/${year}/dpsbdt -F Friends /eos/cms/store/cmst3/group/dpsww/${Trees}/${year}/bdt_input_vars/{cname}_Friend.root -I CMGTools.DPSWW.tools.nanoAOD.ttH_modules BDT_DPSWW -N 10000  -q condor --maxruntime 120 --log $PWD/logs
   fi

done


#test commands (misc)


#python prepareEventVariablesFriendTree.py -t NanoAOD /eos/cms/store/cmst3/group/dpsww/NanoTrees_TTH_090120_091019_v6_skim2lss/${year}/ test_dps -F Friends /eos/cms/store/cmst3/group/dpsww/NanoTrees_TTH_090120_091019_v6_skim2lss/${year}/bdt_input_vars/{cname}_Friend.root -I CMGTools.DPSWW.tools.nanoAOD.ttH_modules BDT_DPSWW -N 1000 -d WWTo2L2Nu_DPS  -c 0


#python prepareEventVariablesFriendTree.py -t NanoAOD /eos/cms/store/cmst3/group/dpsww/Lepton_id_study/WWTo2L2Nu_DoubleScattering_13TeV-pythia8/ test_dps  -I CMGTools.DPSWW.tools.nanoAOD.ttH_modules collectionMerger_DPSWW -d 0426786A-643C-B84B-A2FC-16B82CC5B955 -N 10000  


#python prepareEventVariablesFriendTree.py -t NanoAOD /eos/cms/store/cmst3/group/dpsww/NanoTrees_v7_dpsww_04092020/2016/ /eos/cms/store/cmst3/group/dpsww/NanoTrees_v7_dpsww_04092020/2016/fakeRateWt -F Friends /eos/cms/store/cmst3/group/dpsww/NanoTrees_v7_dpsww_04092020/2016/${Friends_recl}/{cname}_Friend.root -I CMGTools.DPSWW.tools.nanoAOD.ttH_modules frWt -N 10000 -d DoubleMuon_Run2016B_02Apr2020 -c 0
#>>>>>>>>test command 

#python prepareEventVariablesFriendTree.py -t NanoAOD /eos/cms/store/cmst3/group/dpsww/${Trees}/${year}/ /eos/cms/store/cmst3/group/dpsww/${Trees}/${year}/${Friends_recl}/  -I CMGTools.DPSWW.tools.nanoAOD.ttH_modules recleaner_step1,recleaner_step2_mc,mcMatch_seq,higgsDecay,triggerSequence -d ZGTo2LG  -N 10000 -q condor --maxruntime 150 --log $PWD/logs

####################### for BDT training 
 
#>>>>>>>>>>>>>>> frnds with BDT input vars, used for BDT training and evaluation. Input should be before skimming here 



# >>>>>>>. store fr weights for Double Muon dataset for BDT_multiclass

#python prepareEventVariablesFriendTree.py -t NanoAOD /eos/cms/store/cmst3/group/dpsww/${Trees}/${year}/ /eos/cms/store/cmst3/group/dpsww/${Trees}/${year}/fakeRateWt -F Friends /eos/cms/store/cmst3/group/dpsww/${Trees}/${year}/${Friends_recl}/{cname}_Friend.root -I CMGTools.DPSWW.tools.nanoAOD.ttH_modules frWt -N 10000 -q condor  --dm DoubleMuon.* --maxruntime 150 --log $PWD/logs
##amif $missing; then
##am    for chunk in "${missingchunks[@]}"
##am    do
##am	echo 'running for' ${missingDS} 'chunk' ${chunk}
##am	#python prepareEventVariablesFriendTree.py -t NanoAOD  /eos/cms/store/cmst3/group/dpsww/${Trees}/${year}/  /eos/cms/store/cmst3/group/dpsww/${Trees}/${year}/${Friends_recl}/ -I CMGTools.DPSWW.tools.nanoAOD.ttH_modules recleaner_step1,recleaner_step2_data,triggerSequence -N 10000 -d ${missingDS} -c ${chunk}
##am	##python prepareEventVariablesFriendTree.py -t NanoAOD /eos/cms/store/cmst3/group/dpsww/${Trees}/${year}/ /eos/cms/store/cmst3/group/dpsww/${Trees}/${year}/${Friends_recl}/ -I CMGTools.DPSWW.tools.nanoAOD.ttH_modules recleaner_step1,recleaner_step2_mc,mcMatch_seq,higgsDecay,triggerSequence -N 10000 -d ${missingDS} -c ${chunk}
##am


##ammissing=false
##ammissingDS="SingleElectron_Run2016G_02Apr2020"
##ammissingchunks=(32)
