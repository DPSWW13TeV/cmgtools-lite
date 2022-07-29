#!/bin/bash

###### analysis steps starting from nanoAOD samples -------------->
## post-processing steps: base ntuples (nanoAODs postprocessor)-> recl frnds (MVA WPs from ttH_modules.py) -> bdtiv -> skimming (skims the base ntuples + recl frnds) -> links to flips 
## run post-skimming frnds 


######## fixed inputs no matter what
baseDir='/eos/cms/store/cmst3/group/dpsww/'

######## MVA WPs, year ans steps to run on 
runWhat=${1}; shift;
year=${1}; shift; 
samples=${1}; shift;
#runWhat=${1}
#steps=("bdtiv")

echo $runWhat,$year,$samples

################### following should not be changed
if [[ ${samples} == "skim" ]];then
    #Trees="signal_fullstats_skim2lss/"
    Trees='NanoTrees_v7_dpsww_skim2lss' 
    nEvt=50000
else
    #Trees='NanoTrees_v7_dpsww_04092020'
    #Trees="signal_fullstats/"
    #Trees="signal_fullstats_nosel"
    Trees="signal_FRonly_reco"
    #Trees='forWWmixing'
    nEvt=20000

fi
#########################################
Parent=${baseDir}/${Trees}/${year}
BCORE="python prepareEventVariablesFriendTree.py -t NanoAOD ${Parent} ${Parent}/";
CMGT="  -I CMGTools.DPSWW.tools.nanoAOD.ttH_modules";
###################################################
case ${runWhat} in
recl)
	echo "recl"
	${BCORE}2_recl/  ${CMGT} recleaner_step1,recleaner_step2_mc,mcMatch_seq,higgsDecay,triggerSequence -N 10000 --de .*Run.* -q condor --maxruntime 50 --log $PWD/logs #
	#${BCORE}2_recl/  ${CMGT} recleaner_step1,recleaner_step2_data,triggerSequence  -N 60000 --dm .*Run.* -q condor  --maxruntime 50 --log $PWD/logs 
	;;

bdtiv)
	echo "bdtiv"
	${BCORE}bdt_input_vars_toInfnBeynd -F Friends ${Parent}/2_recl/{cname}_Friend.root --FMC Friends ${Parent}/0_jmeUnc_v2/{cname}_Friend.root  ${CMGT} dpsvars${year}MC  -N 100000 #-q condor --maxruntime 100 --log $PWD/logs  #  --de .*Run.*
	;;
bdtDisc)
	echo "bdtDisc"
	#${BCORE}dpsbdt_neu_ssnoeebkg_afacdps -F Friends ${Parent}/bdt_input_vars_toInfnBeynd/{cname}_Friend.root  ${CMGT} bdtvars_withpt_$year -N 10000 --de .*Run.* # -q condor --maxruntime 200 --log  $PWD/logs #--de .*Run.*
	${BCORE}dpsbdt_neu_ssnoeebkg_afacdps_unclEn -F Friends ${Parent}/bdt_input_vars_toInfnBeynd/{cname}_Friend.root  ${CMGT} bdtvars_withpt_${year},bdtvars_withpt_${year}Up,bdtvars_withpt_${year}Down -N 70000 -d WWDoubleTo2L_newsim -c 0 #-q condor --maxruntime 200 --log  $PWD/logs
	;;
postFSR)
	echo "postFSR"
	#Trees="signal_fullstats_nosel/"      
	${BCORE}postFSRinfo/  ${CMGT} genInfo_py8_fur_taus --de .*herwig.* -N ${nEvt}  -q condor --maxruntime 50 --log $PWD/logs
	${BCORE}postFSRinfo/  ${CMGT} genInfo_hw_fur_taus  --dm .*herwig.* -N ${nEvt}  -q condor --maxruntime 50 --log $PWD/logs
	;;
npdf)
	echo "npdf"
	${BCORE}nnpdf_rms  ${CMGT} rms_val --de .*Run.* -N 100000  -q condor --maxruntime 50 --log $PWD/logs
	;;
lepSFs)
	echo "lepsfs"
	${BCORE}4_scalefactors -F Friends ${Parent}/2_recl/{cname}_Friend.root  ${CMGT} leptonSFs  -N ${nEvt} --de .*Run.*  -q condor --maxruntime 50 --log $PWD/logs #--de .*Run.* 
;;
puwts)
	echo "running puwts"
	${BCORE}puWts -F Friends ${Parent}/2_recl/{cname}_Friend.root  ${CMGT} newpuwts  -N 1000000 --de .*Run.*  -q condor --maxruntime 50 --log $PWD/logs #--de .*Run.* 
	;;
mupf)
	echo "running mupf"
	#${BCORE}muPrefiring -F Friends ${Parent}/2_recl/{cname}_Friend.root  ${CMGT} sfs_${year}  -N 2000000  --de .*Run.* -q condor --maxruntime 80 --log $PWD/logs #--de .*Run.* 

	${BCORE}test_am -F Friends ${Parent}/2_recl/{cname}_Friend.root  ${CMGT} prefiringwt_${year}  -N 200000  -q condor --maxruntime 80 --log $PWD/logs #--de .*Run.* 
	;;


taucount)
	echo "taucount"
	${BCORE}3_tauCount/  -F Friends  ${Parent}/2_recl/{cname}_Friend.root   ${CMGT} countTaus  -N ${nEvt} -q condor --de .*Run.* --maxruntime 50 --log $PWD/logs #-d WZTo3LNu_ewk  -q condor --maxruntime 50 --log $PWD/logs #--dm .*forFlips.*
	;;
jme)
	echo "jme"
	${BCORE}0_jmeUnc_v2/   ${CMGT} jme${year}_allvariations  -N ${nEvt} --de .*Run.*  -q condor --maxruntime 70 --log $PWD/logs # --de .*Run.*
	;;
recl_allvars)
	echo 'i assume you have already got jme frnds'
	${BCORE}2_recl_allvars/   ${CMGT} recleaner_step1,recleaner_step2_mc_allvariations,mcMatch_seq,triggerSequence -F Friends ${Parent}/0_jmeUnc_v2/{cname}_Friend.root  -N ${nEvt} --de .*Run.* -q condor --maxruntime 100 --log $PWD/logs        #--de .*Run.*    
	;;
bTagSF)
	echo 'btag'
	${BCORE}2_btag_SFs/   ${CMGT} scaleFactorSequence_allVars_${year} --FMC Friends ${Parent}/0_jmeUnc_v2/{cname}_Friend.root  -F Friends ${Parent}/2_recl_allvars//{cname}_Friend.root -N 100000  --de .*Run.*   -q condor --maxruntime 70 --log $PWD/logs        #--de .*Run.* removed total uncert from jetmetgrouper.py
	;;
step2)
	echo "jme"
	${BCORE}0_jmeUnc_v2/   ${CMGT} jme${year}_allvariations  -N ${nEvt} --de .*Run.*  -q condor --maxruntime 70 --log $PWD/logs # --de .*Run.*
	echo "npdf"
	${BCORE}nnpdf_rms  ${CMGT} rms_val --de .*Run.* -N 100000  -q condor --maxruntime 50 --log $PWD/logs
	echo "lepsfs"
	${BCORE}4_scalefactors -F Friends ${Parent}/2_recl/{cname}_Friend.root  ${CMGT} leptonSFs  -N ${nEvt} --de .*Run.*  -q condor --maxruntime 50 --log $PWD/logs #--de .*Run.* 
	#echo "running puwts"
	#${BCORE}puWts -F Friends ${Parent}/2_recl/{cname}_Friend.root  ${CMGT} newpuwts  -N 1000000 --de .*Run.*  -q condor --maxruntime 50 --log $PWD/logs #--de .*Run.* 
	echo "running mupf"
	${BCORE}muPrefiring -F Friends ${Parent}/2_recl/{cname}_Friend.root  ${CMGT} sfs_${year}  -N 2000000  --de .*Run.* -q condor --maxruntime 80 --log $PWD/logs #--de .*Run.* 
	echo "taucount"
	${BCORE}3_tauCount/  -F Friends  ${Parent}/2_recl/{cname}_Friend.root   ${CMGT} countTaus  -N ${nEvt}  --de .*Run.* -q condor --maxruntime 50 --log $PWD/logs 
	;;
step3)
	echo "bdtiv"
	${BCORE}bdt_input_vars_toInfnBeynd -F Friends ${Parent}/2_recl/{cname}_Friend.root --FMC Friends ${Parent}/0_jmeUnc_v2/{cname}_Friend.root  ${CMGT} dpsvars${year}MC  -N 100000 -q condor --maxruntime 100 --log $PWD/logs  #  --de .*Run.*
	#echo "bdtiv" for random mixing 
	#${BCORE}Wvars -F Friends ${Parent}/2_recl/{cname}_Friend.root --FMC Friends ${Parent}/0_jmeUnc_v2/{cname}_Friend.root  ${CMGT} wvars${year}MC  -N 100000 -q condor --maxruntime 100 --log $PWD/logs  #  --de .*Run.*
	echo "recl_allvars"
	${BCORE}2_recl_allvars/   ${CMGT} recleaner_step1,recleaner_step2_mc_allvariations,mcMatch_seq,triggerSequence -F Friends ${Parent}/0_jmeUnc_v2/{cname}_Friend.root  -N ${nEvt} --de .*Run.* -q condor --maxruntime 100 --log $PWD/logs        #--de .*Run.*    
	;;
step4)
	echo 'btag'
	${BCORE}2_btag_SFs/   ${CMGT} scaleFactorSequence_allVars_${year} --FMC Friends ${Parent}/0_jmeUnc_v2/{cname}_Friend.root  -F Friends ${Parent}/2_recl_allvars//{cname}_Friend.root -N 100000  --de .*Run.*   -q condor --maxruntime 70 --log $PWD/logs        #--de .*Run.* removed total uncert from jetmetgrouper.py
	echo "bdtDisc"
	${BCORE}dpsbdt_neu_ssnoeebkg_afacdps -F Friends ${Parent}/bdt_input_vars_toInfnBeynd/{cname}_Friend.root  ${CMGT} bdtvars_withpt_$year -N 10000 --de .*Run.* # -q condor --maxruntime 200 --log  $PWD/logs #--de .*Run.*
	#${BCORE}dpsbdt_neu_ssnoeebkg_afacdps_allVars -F Friends ${Parent}/bdt_input_vars_toInfnBeynd/{cname}_Friend.root  ${CMGT} bdtvars_withpt_${year}VarU,bdtvars_withpt_${year}VarD,bdtvars_withpt_${year} -N 10000 --de .*Run.*  -q condor --maxruntime 200 --log  $PWD/logs #--de .*Run.*
	${BCORE}dpsbdt_neu_ssnoeebkg_afacdps_unclEn -F Friends ${Parent}/bdt_input_vars_toInfnBeynd/{cname}_Friend.root  ${CMGT} bdtvars_withpt_${year},bdtvars_withpt_${year}Up,bdtvars_withpt_${year}Down -N 70000 #-q condor --maxruntime 200 --log  $PWD/logs
	;;
*)
	echo "enter a valid opt"
	;;

esac;
