#!/bin/bash

###### analysis steps starting from nanoAOD samples -------------->
## post-processing steps: base ntuples (nanoAODs postprocessor)-> recl frnds (selections from vvsemilep_modules.py) -> npdf #bdtiv -> skimming (skims the base ntuples + recl frnds) -> links to flips 
## run post-skimming frnds 
##maxruntime here is in minutes

######## fixed inputs no matter what
baseDir='/eos/cms/store/cmst3/group/dpsww/'
localtest='/afs/cern.ch/work/a/anmehta/public/cmgtools_WVsemilep/CMSSW_10_6_29/src/CMGTools/VVsemilep/cfg/'
######## MVA WPs, year ans steps to run on 
runWhat=${1}; shift;
year=${1}; shift; 
samples=${1}; shift;
chunks=( "$@" )
echo $runWhat,$year


################### following should not be changed
localTrees='local_dir_NAME/'  
Trees='NanoTrees_v9_vvsemilep_06012023/'
nEvt=120000
Parent=${baseDir}/${Trees}/${year}
BCORE="python prepareEventVariablesFriendTree.py -t NanoAOD ${Parent} ${Parent}/";
CMGT="  -I CMGTools.VVsemilep.tools.nanoAOD.vvsemilep_modules";
###################################################
case ${runWhat} in
recl)
	echo "recl"
	if [ -z "$chunks" ] || [ -z == "$samples" ]
	    then
	    echo "running for the first time"
	    ${BCORE}2_recl/  ${CMGT} recleaner_step1,recleaner_step2_mc,mcMatch_seq,triggerSequence -N ${nEvt} --de .*Run.*  -q condor --maxruntime 100 --log $PWD/logs #run on mc --de .*Run.*  
	    #${BCORE}2_recl/  ${CMGT} recleaner_step1,recleaner_step2_data,triggerSequence  -N ${nEvt} --dm .*Run.* -q condor  --maxruntime 100 --log $PWD/logs ##run on data
	    
	else #for running missing chunks locally
	    for i in "${chunks[@]}"
	    do 
		##amFIXME: check if run in the sample -> execute data friends else MC
		#${BCORE}2_recl/  ${CMGT} recleaner_step1,recleaner_step2_mc,mcMatch_seq,triggerSequence -N ${nEvt} -d ${samples} -c ${i}
		#${BCORE}2_recl/  ${CMGT} recleaner_step1,recleaner_step2_data,triggerSequence  -N ${nEvt} -d ${samples} -c ${i}
		${BCORE}0_jmeUnc/  ${CMGT} jetmetUncertainties${year}All,jetmetUncertainties${year}Total,fatjetmetUncertainties${year}All,fatjetmetUncertainties${year}Total  -N ${nEvt} -d ${samples} -c ${i}
	    done
	fi
	;;
top)
	echo "top pT reweighting "
	${BCORE}2_toppT_rw  ${CMGT} topsf   -N ${nEvt} --dm TT.* -q condor --maxruntime 40 --log $PWD/logs
	;;

npdf)
	echo "npdf"
	${BCORE}nnpdf_rms  ${CMGT} rms_val --de .*Run.* -N ${nEvt}  -q condor --maxruntime 40 --log $PWD/logs #--de .*Run.*
	;;

fjtagged)
	echo "fjtagged"
	#${BCORE}ak8VtaggedV1  ${CMGT} taggedfj_data -N ${nEvt}  -F Friends ${Parent}/2_recl/{cname}_Friend.root -d DoubleMuon_Run2018C_UL18 -c 12  #--dm .*Run.* -q condor --maxruntime 40 --log $PWD/logs 
	${BCORE}ak8VtaggedV1  ${CMGT} taggedfj -N ${nEvt}  -F Friends ${Parent}/2_recl/{cname}_Friend.root  -d WJetsToLNu_Pt250To400_part6 -c 51 #--dm WJetsToLNu_Pt.*   -q condor --maxruntime 40 --log $PWD/logs #--de .*Run.* 
	${BCORE}ak8VtaggedV1  ${CMGT} taggedfj -N ${nEvt}  -F Friends ${Parent}/2_recl/{cname}_Friend.root  -d WJetsToLNu_Pt250To400_part5 -c 12 
	;;

fjvars)
	echo "fjvars"
	#${BCORE}ak8VtaggedV1_vars  ${CMGT} taggedfjvars -N ${nEvt}  -F Friends ${Parent}/2_recl_allvars/{cname}_Friend.root --de .*Run.* -q condor --maxruntime 40 --log $PWD/logs 
	${BCORE}ak8VtaggedV1_vars  ${CMGT} taggedfjvars -N ${nEvt}  -F Friends ${Parent}/2_recl_allvars/{cname}_Friend.root --dm WJetsToLNu_Pt.*   -q condor --maxruntime 70 --log $PWD/logs #

	;;

jme)
	echo "jme"
	${BCORE}0_jmeUnc/  ${CMGT} jetmetUncertainties${year}All,jetmetUncertainties${year}Total,fatjetmetUncertainties${year}All,fatjetmetUncertainties${year}Total  -N ${nEvt} --dm WJetsToLNu_Pt.*  -q condor --maxruntime 180 --log $PWD/logs #--de .*Run.* -q condor --maxruntime 100 --log $PWD/logs # --de .*Run.*
	;;

recl_allvars)
	echo 'i assume you have already got jme frnds'
	${BCORE}2_recl_allvars/   ${CMGT} recleaner_step1,recleaner_step2_mc_allvariations,mcMatch_seq,triggerSequence -F Friends ${Parent}/0_jmeUnc/{cname}_Friend.root  -N ${nEvt} --dm WJetsToLNu_Pt.*  -q condor --maxruntime 100 --log $PWD/logs #--dm  WJetsToLNu_Pt.*          #--de .*Run.* 
	;;


*)
	echo "enter a valid opt"
	;;

esac;


##. runFrnds_v2.sh recl 2018 TTJets 182
#0_toppT_rw
##['WJetsToLNu_Pt100To250_part10_Friend.chunk7.root', 'WJetsToLNu_Pt100To250_part1_Friend.chunk31.root', 'WJetsToLNu_Pt100To250_part2_Friend.chunk5.root', 'WJetsToLNu_Pt100To250_part9_Friend.chunk24.root', 'WJetsToLNu_Pt100To250_part9_Friend.chunk66.root', 'WJetsToLNu_Pt250To400_part0_Friend.chunk23.root', 'WJetsToLNu_Pt250To400_part1_Friend.chunk51.root', 'WJetsToLNu_Pt250To400_part1_Friend.chunk52.root', 'WJetsToLNu_Pt250To400_part1_Friend.chunk9.root', 'WJetsToLNu_Pt600ToInf_Friend.chunk6.root']
