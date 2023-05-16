#!/bin/bash

###### analysis steps starting from nanoAOD samples -------------->
## test command:  . runFrnds_v3.sh genInfo 2018 local

##maxruntime here is in minutes

######## fixed inputs no matter what
baseDir='/eos/cms/store/cmst3/group/dpsww/'
localtest='/afs/cern.ch/work/a/anmehta/public/cmgtools_WVsemilep/CMSSW_10_6_29/src/CMGTools/VVsemilep/cfg/'
######## MVA WPs, year ans steps to run on 
runWhat=${1}; shift;
year=${1}; shift; 
runWhere=${1}; shift; #local or condor
samples=${1}; shift;
chunks=( "$@" )
echo $runWhat,$year,$runWhere


################### following should not be changed
localTrees='local_dir_NAME/'  
Trees='NanoTrees_v9_vvsemilep_06012023/'
nEvt=120000
Parent=${baseDir}/${Trees}/${year}
BCORE="python prepareEventVariablesFriendTree.py -t NanoAOD ${Parent} ${Parent}/";
CMGT="  -I CMGTools.VVsemilep.tools.nanoAOD.vvsemilep_modules";


###################################################
case ${runWhere} in
condor)
	echo "running on condor"
	cmd_1=" -q condor --maxruntime 100 --log $PWD/logs"

	;;
*) 
	echo "running in local"
	cmd_1=" "
	;;
esac

case ${runWhat} in
recl)
	basecmd="${BCORE}2_recl/  ${CMGT} recleaner_step1,recleaner_step2_mc,mcMatch_seq,triggerSequence  --dm .*Nujj_01j_aTGC_4f_NLO_FXFX_4f.*  #run on mc --de .*Run.* "
	;;

recldata)
	basecmd="${BCORE}2_recl/  ${CMGT} recleaner_step1,recleaner_step2_data,triggerSequence  --dm .*Run.* "
	;;

jme)
	basecmd="${BCORE}0_jmeUnc/ ${CMGT} jetmetUncertainties${year}All,jetmetUncertainties${year}Total,fatjetmetUncertainties${year}All,fatjetmetUncertainties${year}Total  -d WmWpToLmNujj_01j_aTGC_pTW_150toInf_mWV_600to800 -c 1 " #--de .*Run.* " WmWpToLmNujj_01j_aTGC_pTW_150toInf_mWV_600to800
	;;

top)
	echo "top pT reweighting "
	basecmd="${BCORE}2_toppT_rw  ${CMGT} topsf   --dm TT.* "
	;;

npdf)
	echo "npdf"
	basecmd="${BCORE}nnpdf_rms  ${CMGT} rms_val --de .*Run.* "
	;;


fjtagged)
	echo "fjtagged + vars"
	basecmd="${BCORE}1_ak8Vtagged  ${CMGT} taggedfj -F Friends ${Parent}/2_recl_allvars/{cname}_Friend.root -d WpWmToLpNujj_01j_aTGC_pTW_150toInf_mWV_600to800 -c 0 " #--de .*Run.* "

	;;
fjtaggeddata)
	basecmd="${BCORE}1_ak8Vtagged  ${CMGT} taggedfj_data -F Friends ${Parent}/2_recl/{cname}_Friend.root --dm .*Run.*"
	;;

recl_allvars)
	echo 'i assume you have already got jme frnds'
	basecmd="${BCORE}2_recl_allvars/   ${CMGT} recleaner_step1,recleaner_step2_mc_allvariations,mcMatch_seq,triggerSequence -F Friends ${Parent}/0_jmeUnc/{cname}_Friend.root  --de .*Run.* "
	;;

wjet)	
	
	basecmd="${BCORE}testAM/  ${CMGT} wvsemilep_tree --FMC Friends ${Parent}/4_scalefactors/{cname}_Friend.root -F Friends ${Parent}/2_recl/{cname}_Friend.root  -F Friends ${Parent}/ak8VtaggedV1/{cname}_Friend.root "
	;;

genInfo)
	echo "genInfo ${BCORE} ${CMGT}"
	basecmd="${BCORE}genInfo/${CMGT} whad_info -d Tbar_tWch_incldecays -c 1 " #--de .*Run.*
	echo $basecmd
	;; #-d WWTo1L1Nu2Q -c 1 #--dm .*aTGCmWV.* #--de .*Run.*
    

*)
	echo "enter a valid opt"
	;;

esac;



if [ -z "$chunks" ] || [ -z == "$samples" ]
then
    echo "running for the first time  ${basecmd}  ${cmd_1}"
    ${basecmd}  ${cmd_1}   
else #for running missing chunks locally
    for i in "${chunks[@]}"
    do 
	${basecmd} ${cmd_1} -d ${samples} -c ${i}
    done
fi



