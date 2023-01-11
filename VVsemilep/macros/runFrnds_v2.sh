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
		${BCORE}2_recl/  ${CMGT} recleaner_step1,recleaner_step2_mc,mcMatch_seq,triggerSequence -N ${nEvt} -d ${samples} -c ${i}
		##am${BCORE}2_recl/  ${CMGT} recleaner_step1,recleaner_step2_data,triggerSequence  -N ${nEvt} -d ${samples} -c ${i}
	    done
	fi
	;;
top)
	echo "top pT reweighting "
	${BCORE}0_toppT_rw  ${CMGT} topsf   -N ${nEvt} --dm TT.* -q condor --maxruntime 50 --log $PWD/logs
	;;

npdf)
	echo "npdf"
	${BCORE}nnpdf_rms  ${CMGT} rms_val --de .*Run.* -N ${nEvt}  -q condor --maxruntime 50 --log $PWD/logs #--de .*Run.*
	;;

jme)
	echo "jme"
	${BCORE}0_jmeUnc/   ${CMGT} jetmetUncertainties${year}All,jetmetUncertainties${year}Total,fatjetmetUncertainties${year}All,fatjetmetUncertainties${year}Total  -N ${nEvt} --de .*Run.* -q condor --maxruntime 100 --log $PWD/logs # --de .*Run.*
	;;

recl_allvars)
	echo 'i assume you have already got jme frnds'
	${BCORE}2_recl_allvars/   ${CMGT} recleaner_step1,recleaner_step2_mc_allvariations,mcMatch_seq,triggerSequence -F Friends ${Parent}/0_jmeUnc/{cname}_Friend.root  -N ${nEvt} --de .*Run.* -q condor --maxruntime 100 --log $PWD/logs        #--de .*Run.*    
	;;

step2)
	echo "jme"
	${BCORE}0_jmeUnc/   ${CMGT} jetmetUncertainties${year}All,jetmetUncertainties${year}Total,fatjetmetUncertainties${year}All,fatjetmetUncertainties${year}Total  -N ${nEvt} --de .*Run.* -q condor --maxruntime 100 --log $PWD/logs # --de .*Run.*
	echo "npdf"
	${BCORE}nnpdf_rms  ${CMGT} rms_val --de .*Run.* -N 100000  -q condor --maxruntime 50 --log $PWD/logs
    	echo "top pT reweighting "
	${BCORE}0_toppT_rw  ${CMGT} topsf   -N ${nEvt} --dm TT.* -q condor --maxruntime 50 --log $PWD/logs
	;;

step3)
	echo "recl_allvars"
	echo 'i assume you have already got jme frnds'
	${BCORE}2_recl_allvars/   ${CMGT} recleaner_step1,recleaner_step2_mc_allvariations,mcMatch_seq,triggerSequence -F Friends ${Parent}/0_jmeUnc/{cname}_Friend.root  -N ${nEvt} --de .*Run.* -q condor --maxruntime 100 --log $PWD/logs        #--de .*Run.*    
	;;

*)
	echo "enter a valid opt"
	;;

esac;


##. runFrnds_v2.sh recl 2018 TTJets 182
#0_toppT_rw
