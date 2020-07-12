#python prepareEventVariablesFriendTree.py -t NanoAOD /eos/user/s/sesanche/nanoAOD/NanoTrees_TTH_090120_091019_v6_skim2lss/2016/ /eos/cms/store/cmst3/group/dpsww/NanoTrees_TTH_090120_091019_v6_skim2lss/2016/dpsvars -F Friends /eos/user/s/sesanche/nanoAOD/NanoTrees_TTH_090120_091019_v6_skim2lss/2016/1_recl/{cname}_Friend.root -I CMGTools.DPSWW.tools.nanoAOD.ttH_modules DPSWW_vars -N 20000 -q condor --dm .*Run.*  --de .*MET*.  --maxruntime 120 --log $PWD/logs

#python prepareEventVariablesFriendTree.py -t NanoAOD /eos/user/s/sesanche/nanoAOD/NanoTrees_TTH_090120_091019_v6_skim2lss/2016/ /eos/cms/store/cmst3/group/dpsww/NanoTrees_TTH_090120_091019_v6_skim2lss/2016/dpsvars -F Friends /eos/user/s/sesanche/nanoAOD/NanoTrees_TTH_090120_091019_v6_skim2lss/2016/1_recl_allvars/{cname}_Friend.root -I CMGTools.DPSWW.tools.nanoAOD.ttH_modules DPSWW_vars -N 20000 -q condor --de .*Run.*   --maxruntime 150 --log $PWD/logs










#python prepareEventVariablesFriendTree.py -t NanoAOD /eos/user/s/sesanche/nanoAOD/NanoTrees_TTH_090120_091019_v6_skim2lss/2016/ /eos/cms/store/cmst3/group/dpsww/NanoTrees_TTH_090120_091019_v6_skim2lss/2016/dpsbdt -F Friends /eos/cms/store/cmst3/group/dpsww/NanoTrees_TTH_090120_091019_v6_skim2lss/2016/dpsvars/{cname}_Friend.root -I CMGTools.DPSWW.tools.nanoAOD.ttH_modules BDT_DPSWW -N 20000 -q condor --dm .*Run.*  --de .*MET*.  --maxruntime 120 --log $PWD/logs

python prepareEventVariablesFriendTree.py -t NanoAOD /eos/user/s/sesanche/nanoAOD/NanoTrees_TTH_090120_091019_v6_skim2lss/2016/ /eos/cms/store/cmst3/group/dpsww/NanoTrees_TTH_090120_091019_v6_skim2lss/2016/dpsbdt -F Friends /eos/cms/store/cmst3/group/dpsww/NanoTrees_TTH_090120_091019_v6_skim2lss/2016/dpsvars/{cname}_Friend.root -I CMGTools.DPSWW.tools.nanoAOD.ttH_modules BDT_DPSWW -N 20000 -q condor --de .*Run.*   --maxruntime 150 --log $PWD/logs


#test command


#python prepareEventVariablesFriendTree.py -t NanoAOD /eos/user/s/sesanche/nanoAOD/NanoTrees_TTH_090120_091019_v6_skim2lss/2016/ test_dps -F Friends /eos/cms/store/cmst3/group/dpsww/NanoTrees_TTH_090120_091019_v6_skim2lss/2016/dpsvars/{cname}_Friend.root -I CMGTools.DPSWW.tools.nanoAOD.ttH_modules BDT_DPSWW -N 1000 -d WWTo2L2Nu_DPS  -c 0



