#!/bin/bash
spl=$2 
year=$1
charge_split=true
when=$(date +"%Y-%m-%d")


baseDir=${PWD} #/Cards
cd ${baseDir}

combDir=${PWD}/Cards/combination
case ${charge_split} in
    true) ppf="_cs"
	;;
    *) ppf=""
	;;
esac
#pf=${when}-${spl}
outext=${year}${ppf}.txt
ext=${year}.txt
pf="2021-11-03-SoBord_sqV3"
#echo ${ppf}



combineCards.py ${baseDir}/Cards/cards_${pf}_elmu_${year}/elmu${year}minusminus.txt ${baseDir}/Cards/cards_${pf}_elmu_${year}/elmu${year}plusplus.txt ${baseDir}/Cards/cards_${pf}_mumu_${year}/mumu${year}minusminus.txt ${baseDir}/Cards/cards_${pf}_mumu_${year}/mumu${year}plusplus.txt > dc_${pf}_ll_noee${year}.txt

combineCards.py signal_region=dc_${pf}_ll_noee${year}.txt wz_cr=Cards/cards_${pf}_cr3l_${year}/cr${year}3l.txt zz_cr=Cards/cards_${pf}_cr4l_${year}/cr${year}4l.txt > dc_${pf}_ll_noee_${year}_combined.txt
echo "norm_WZ       rateParam *  WZ 1 [0,5]" >> dc_${pf}_ll_noee_${year}_combined.txt
echo "norm_ZZ       rateParam *  ZZ 1 [0,5]" >> dc_${pf}_ll_noee_${year}_combined.txt

mv dc_${pf}_ll_noee${year}.txt ${combDir}/
mv dc_${pf}_ll_noee_${year}_combined.txt ${combDir}/
combine -M Significance  ${combDir}/dc_${pf}_ll_noee_${year}_combined.txt -t -1 --expectSignal=1

##
##
##
##if [[ ${charge_split} ]]; then
##    combineCards.py ${combDir}/${pf}_mumu${outext} ${combDir}/${pf}_elmu${outext} > file.txt #${combDir}/${pf}_noee${outext}
##    cat file.txt > dummy.txt
##    sed 's/afs.*afs/afs/g' dummy.txt > ${combDir}/${pf}_noee${outext}
##    echo combine -M Significance ${combDir}/${pf}_noee${outext} -t -1 --expectSignal=1
##    combine -M Significance ${combDir}/${pf}_noee${outext} -t -1 --expectSignal=1
##else
##    prefix=$baseDir}/Cards/cards_${pf}
##    combineCards.py ${prefix}_mumu_${year}/mumu${ext} ${cardsDir}_elmu_${year}/elmu${ext} > ${combDir}/${pf}_noee${outext}
##    echo combine -M Significance  ${combDir}/${pf}_noee${outext}  -t -1 --expectSignal=1
##    combine -M Significance  ${combDir}/${pf}_noee${outext}  -t -1 --expectSignal=1
##fi


#echo combineCards.py cards_${pf}_mumu_${year}/mumu${ext} cards_${pf}_elmu_${year}/elmu${ext}  > dc_${pf}_${year}_noee.txt

#echo combine -M FitDiagnostics ${cardsDir}/${FS}${ext} -t -1 --expectSignal=1
#echo python ../../../../HiggsAnalysis/CombinedLimit/test/diffNuisances.py fitDiagnostics.root  --format html > /eos/user/a/anmehta/www/DPSWW_v2/FitResults/${pf}_${FS}${year}.html


#echo combine -M FitDiagnostics Cards/dc_${pf}_${year}_noee_${ppf}.txt -t -1 --expectSignal=1
#echo python ../../../../HiggsAnalysis/CombinedLimit/test/diffNuisances.py fitDiagnostics.root  --format html > /eos/user/a/anmehta/www/DPSWW_v2/FitResults/dc_${pf}_${year}_noee_${ppf}.html
#echo combineCards.py cards_${pf}_mumu_${year}/mumu${ext} cards_${pf}_elmu_${year}/elmu${ext} cards_${pf}_elel_${year}/elel${ext} > dc_${pf}_${ext}
#combineCards.py cards_${pf}_mumu_${year}/mumu${ext} cards_${pf}_elmu_${year}/elmu${ext} cards_${pf}_elel_${year}/elel${ext} > dc_${pf}_${ext}

#echo combine -M Significance  Cards/dc_${pf}_${ext} -t -1 --expectSignal=1


#cd -


#combine -M FitDiagnostics Cards/March01_fullRun2.txt -t -1 --expectSignal=1
#python ../../../../HiggsAnalysis/CombinedLimit/test/diffNuisances.py fitDiagnostics.root  --format html > /eos/user/a/anmehta/www/DPSWW_v2/FitResults/NP.html
##amcombineCards.py Cards/cards_2021-11-01-SoBord_sqV3_elmu_2016/elmu2016minusminus.txt Cards/cards_2021-11-01-SoBord_sqV3_elmu_2016/elmu2016plusplus.txt Cards/cards_2021-11-01-SoBord_sqV3_mumu_2016/mumu2016plusplus.txt Cards/cards_2021-11-01-SoBord_sqV3_mumu_2016/mumu2016minusminus.txt > ll_noee_2016.txt
##amcombineCards.py signal_region=ll_noee_2016.txt wz_cr=Cards/cards_2021-11-01-SoBord_sqV3_cr3l_2016/cr20163l.txt zz_cr=Cards/cards_2021-11-01-SoBord_sqV3_cr4l_2016/cr20164l.txt > combined_2016.txt
##amcombine -M Significance  combined_2016.txt -t -1 --expectSignal=1
##am
##ammv combined_${year}.txt ${combDir}/
