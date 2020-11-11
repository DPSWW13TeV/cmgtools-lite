#!/bin/bash
sample=''
chunks=(1)
treedir='NanoTrees_v7_dpsww_04092020_skim2lss_mvawp_mupt90_elpt70_latest'
year='2016'
for chunk in "${chunks[@]}"
do


    #python prepareEventVariablesFriendTree.py -t NanoAOD /eos/cms/store/cmst3/group/dpsww/${treedir}/${year}/ /eos/cms/store/cmst3/group/dpsww/${treedir}/${year}/1_recl/ -I CMGTools.DPSWW.tools.nanoAOD.ttH_modules recleaner_step1,recleaner_step2_mc,mcMatch_seq,higgsDecay,triggerSequence  -N 10000 -d $sample -c $chunk 
    
    #python prepareEventVariablesFriendTree.py -t NanoAOD /eos/cms/store/cmst3/group/dpsww/${treedir}/${year}/ /eos/cms/store/cmst3/group/dpsww/${treedir}/${year}/0_jmeUnc_v1/ -I CMGTools.DPSWW.tools.nanoAOD.ttH_modules jme${year}_allvariations  -N 10000 -d $sample -c $chunk 

    python prepareEventVariablesFriendTree.py -t NanoAOD ${PWD} ${PWD}/test  -I CMGTools.DPSWW.tools.nanoAOD.ttH_modules tnpvars -N 10000 -d BE7DC3B4-019E-4D40-8D0B-E7AAB81D91F7 -c $chunk
    
    #echo 'python prepareEventVariablesFriendTree.py -t NanoAOD /eos/cms/store/cmst3/group/dpsww/${treedir}/${year}/ /eos/cms/store/cmst3/group/dpsww/${treedir}/${year}/3_tauCount/  -F Friends  /eos/cms/store/cmst3/group/dpsww/${treedir}/${year}/2_recl/{cname}_Friend.root  -I CMGTools.DPSWW.tools.nanoAOD.ttH_modules countTaus -N 10000 -d $sample -c $chunk'



    python prepareEventVariablesFriendTree.py -t NanoAOD /eos/cms/store/cmst3/group/dpsww/${treedir}/${year}/ /eos/cms/store/cmst3/group/dpsww/${treedir}/${year}/2_recl_allvars/  -I CMGTools.DPSWW.tools.nanoAOD.ttH_modules recleaner_step1,recleaner_step2_mc_allvariations,mcMatch_seq,triggerSequence -F Friends /eos/cms/store/cmst3/group/dpsww/${treedir}/${year}/0_jmeUnc_v1/{cname}_Friend.root -N 10000 -d $sample -c $chunk



done 


