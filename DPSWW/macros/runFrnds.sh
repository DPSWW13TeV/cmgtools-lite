Trees='NanoTrees_v7_dpsww_04092020'
skimmedTrees='NanoTrees_v7_dpsww_04092020_skim2lss_mvawp_mupt90_elpt70'
year='2016'
Friends_recl='1_recl_mvawp_mupt90_elpt70'

########>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>> step 1 recleaner (these are used for the skimming part and the ones for data are used in the  analysis as well)

#>>>>>>>>test command 

#python prepareEventVariablesFriendTree.py -t NanoAOD /eos/cms/store/cmst3/group/dpsww/${Trees}/${year}/ /eos/cms/store/cmst3/group/dpsww/${Trees}/${year}/${Friends_recl}/  -I CMGTools.DPSWW.tools.nanoAOD.ttH_modules recleaner_step1,recleaner_step2_mc,mcMatch_seq,higgsDecay,triggerSequence -d TTW_LO -N 10000 #-c 0


#>>>>>>>>>>>>>>>>>>> run on all MC samples using condor 

#python prepareEventVariablesFriendTree.py -t NanoAOD /eos/cms/store/cmst3/group/dpsww/${Trees}/${year}/ /eos/cms/store/cmst3/group/dpsww/${Trees}/${year}/${Friends_recl}/ -I CMGTools.DPSWW.tools.nanoAOD.ttH_modules recleaner_step1,recleaner_step2_mc,mcMatch_seq,higgsDecay,triggerSequence  --de .*Run.* -N 10000 -q condor --maxruntime 150 --log $PWD/logs

#>>>>>>>>>>>>>>>>>> run on data 

#python prepareEventVariablesFriendTree.py -t NanoAOD  /eos/cms/store/cmst3/group/dpsww/${Trees}/${year}/  /eos/cms/store/cmst3/group/dpsww/${Trees}/${year}/${Friends_recl}/ -I CMGTools.DPSWW.tools.nanoAOD.ttH_modules recleaner_step1,recleaner_step2_data,triggerSequence --dm .*Run.* -N 10000 -q condor  --maxruntime 150 --log $PWD/logs


########>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>> step 2 (after skimming) use skimmed trees everywhere except for the bdt input vars)


#python prepareEventVariablesFriendTree.py -t NanoAOD /eos/cms/store/cmst3/group/dpsww/${skimmedTrees}/${year}/ /eos/cms/store/cmst3/group/dpsww/${skimmedTrees}/${year}/0_jmeUnc_v1/  -I CMGTools.DPSWW.tools.nanoAOD.ttH_modules jme${year}_allvariations  --de .*Run.* -N 10000 -q condor --maxruntime 150 --log $PWD/logs

# run recleaner for mc and all variations (not necessary for data) 


#python prepareEventVariablesFriendTree.py -t NanoAOD /eos/cms/store/cmst3/group/dpsww/${skimmedTrees}/${year}/ /eos/cms/store/cmst3/group/dpsww/${skimmedTrees}/${year}/1_recl_allvars/  -I CMGTools.TTHAnalysis.tools.nanoAOD.ttH_modules recleaner_step1,recleaner_step2_mc_allvariations,mcMatch_seq,triggerSequence -F Friends /eos/cms/store/cmst3/group/dpsww/${skimmedTrees}/${year}/0_jmeUnc_v1/{cname}_Friend.root --de .*Run.* -N 10000  -q condor --maxruntime 150 --log $PWD/logs 


# lepton scale factors 

#python prepareEventVariablesFriendTree.py -t NanoAOD /eos/cms/store/cmst3/group/dpsww/${skimmedTrees}/${year}/ /eos/cms/store/cmst3/group/dpsww/${skimmedTrees}/${year}/2_scalefactors_lep_fixed -F Friends /eos/cms/store/cmst3/group/dpsww/${skimmedTrees}/${year}/1_recl/{cname}_Friend.root -I CMGTools.TTHAnalysis.tools.nanoAOD.ttH_modules leptonSFs -N 10000 --de .*Run.*  -q condor --maxruntime 100 --log $PWD/logs 

# tau count
# python prepareEventVariablesFriendTree.py -t NanoAOD /eos/cms/store/cmst3/group/dpsww/${skimmedTrees}/${year}/ /eos/cms/store/cmst3/group/dpsww/${skimmedTrees}/${year}/3_tauCount/  -F Friends  /eos/cms/store/cmst3/group/dpsww/${skimmedTrees}/${year}/1_recl/{cname}_Friend.root  -I CMGTools.TTHAnalysis.tools.nanoAOD.ttH_modules countTaus  -N 10000  -q condor --maxruntime 100 --log $PWD/logs 






#>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>> WIP 


# frnds with BDT input vars, used for BDT training and evaluation 

#python prepareEventVariablesFriendTree.py -t NanoAOD /eos/cms/store/cmst3/group/dpsww/${Trees}/${year}/ /eos/cms/store/cmst3/group/dpsww/${Trees}/${year}/dpsvars -F Friends /eos/cms/store/cmst3/group/dpsww/NanoTrees_TTH_090120_091019_v6_skim2lss/${year}/${Friends_recl}/{cname}_Friend.root -I CMGTools.DPSWW.tools.nanoAOD.ttH_modules DPSWW_vars -N 20000 -q condor --dm .*Run.*  --de .*Run*.  --maxruntime 120 --log $PWD/logs

#python prepareEventVariablesFriendTree.py -t NanoAOD /eos/cms/store/cmst3/group/dpsww/${skimmedTrees}/${year}/ /eos/cms/store/cmst3/group/dpsww/${skimmedTrees}/${year}/dpsvars -F Friends /eos/cms/store/cmst3/group/dpsww/${skimmedTrees}/${year}//{cname}_Friend.root -I CMGTools.DPSWW.tools.nanoAOD.ttH_modules DPSWW_vars -N 20000 -q condor --dm .*Run.*   --maxruntime 150 --log $PWD/logs







# frnds with BDT vars 


#python prepareEventVariablesFriendTree.py -t NanoAOD /eos/cms/store/cmst3/group/dpsww/NanoTrees_TTH_090120_091019_v6_skim2lss/${year}/ /eos/cms/store/cmst3/group/dpsww/NanoTrees_TTH_090120_091019_v6_skim2lss/${year}/dpsbdt_MET20 -F Friends /eos/cms/store/cmst3/group/dpsww/NanoTrees_TTH_090120_091019_v6_skim2lss/${year}/dpsvars/{cname}_Friend.root -I CMGTools.DPSWW.tools.nanoAOD.ttH_modules BDT_DPSWW -N 20000 -q condor --dm .*Run.*  --de .*MET*.  --maxruntime 120 --log $PWD/logs

#python prepareEventVariablesFriendTree.py -t NanoAOD /eos/cms/store/cmst3/group/dpsww/NanoTrees_TTH_090120_091019_v6_skim2lss/${year}/ /eos/cms/store/cmst3/group/dpsww/NanoTrees_TTH_090120_091019_v6_skim2lss/${year}/dpsbdt_MET20 -F Friends /eos/cms/store/cmst3/group/dpsww/NanoTrees_TTH_090120_091019_v6_skim2lss/${year}/dpsvars/{cname}_Friend.root -I CMGTools.DPSWW.tools.nanoAOD.ttH_modules BDT_DPSWW -N 20000 -q condor --de .*Run.*   --maxruntime 150 --log $PWD/logs


#test command


#python prepareEventVariablesFriendTree.py -t NanoAOD /eos/cms/store/cmst3/group/dpsww/NanoTrees_TTH_090120_091019_v6_skim2lss/${year}/ test_dps -F Friends /eos/cms/store/cmst3/group/dpsww/NanoTrees_TTH_090120_091019_v6_skim2lss/${year}/dpsvars/{cname}_Friend.root -I CMGTools.DPSWW.tools.nanoAOD.ttH_modules BDT_DPSWW -N 1000 -d WWTo2L2Nu_DPS  -c 0


#python prepareEventVariablesFriendTree.py -t NanoAOD /eos/cms/store/cmst3/group/dpsww/Lepton_id_study/WWTo2L2Nu_DoubleScattering_13TeV-pythia8/ test_dps  -I CMGTools.DPSWW.tools.nanoAOD.ttH_modules collectionMerger_DPSWW -d 0426786A-643C-B84B-A2FC-16B82CC5B955 -N 10000  

