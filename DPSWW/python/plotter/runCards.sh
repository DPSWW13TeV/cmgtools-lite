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
pf=${when}-${spl}
outext=${year}${ppf}.txt
ext=${year}.txt
#echo ${ppf}



for FS in "elmu" "mumu"  #"elel"
do
    cardsDir=${baseDir}/Cards/cards_${pf}_${FS}_${year}
    echo combineCards.py ${cardsDir}/${FS}plusplus${ext} ${cardsDir}/${FS}minusminus${ext} > ${combDir}/${pf}_${FS}${outext}
    combineCards.py ${cardsDir}/${FS}plusplus${ext} ${cardsDir}/${FS}minusminus${ext} > ${combDir}/${pf}_${FS}${outext}
    echo will run combine -M Significance  ${combDir}/${pf}_${FS}${outext} -t -1 --expectSignal=1
    combine -M Significance  ${combDir}/${pf}_${FS}${outext} -t -1 --expectSignal=1
done


if [[ ${charge_split} ]]; then
    combineCards.py ${combDir}/${pf}_mumu${outext} ${combDir}/${pf}_elmu${outext} > file.txt #${combDir}/${pf}_noee${outext}
    cat file.txt > dummy.txt
    sed 's/afs.*afs/afs/g' dummy.txt > ${combDir}/${pf}_noee${outext}
    echo combine -M Significance ${combDir}/${pf}_noee${outext} -t -1 --expectSignal=1
    combine -M Significance ${combDir}/${pf}_noee${outext} -t -1 --expectSignal=1
else
    prefix=$baseDir}/Cards/cards_${pf}
    combineCards.py ${prefix}_mumu_${year}/mumu${ext} ${cardsDir}_elmu_${year}/elmu${ext} > ${combDir}/${pf}_noee${outext}
    echo combine -M Significance  ${combDir}/${pf}_noee${outext}  -t -1 --expectSignal=1
    combine -M Significance  ${combDir}/${pf}_noee${outext}  -t -1 --expectSignal=1
fi


#echo combineCards.py cards_${pf}_mumu_${year}/mumu${ext} cards_${pf}_elmu_${year}/elmu${ext}  > dc_${pf}_${year}_noee.txt

#echo combine -M FitDiagnostics ${cardsDir}/${FS}${ext} -t -1 --expectSignal=1
#echo python ../../../../HiggsAnalysis/CombinedLimit/test/diffNuisances.py fitDiagnostics.root  --format html > /eos/user/a/anmehta/www/DPSWW_v2/FitResults/${pf}_${FS}${year}.html


#echo combine -M FitDiagnostics Cards/dc_${pf}_${year}_noee_${ppf}.txt -t -1 --expectSignal=1
#echo python ../../../../HiggsAnalysis/CombinedLimit/test/diffNuisances.py fitDiagnostics.root  --format html > /eos/user/a/anmehta/www/DPSWW_v2/FitResults/dc_${pf}_${year}_noee_${ppf}.html
#echo combineCards.py cards_${pf}_mumu_${year}/mumu${ext} cards_${pf}_elmu_${year}/elmu${ext} cards_${pf}_elel_${year}/elel${ext} > dc_${pf}_${ext}
#combineCards.py cards_${pf}_mumu_${year}/mumu${ext} cards_${pf}_elmu_${year}/elmu${ext} cards_${pf}_elel_${year}/elel${ext} > dc_${pf}_${ext}

#echo combine -M Significance  Cards/dc_${pf}_${ext} -t -1 --expectSignal=1


cd -


#combine -M FitDiagnostics Cards/March01_fullRun2.txt -t -1 --expectSignal=1
#python ../../../../HiggsAnalysis/CombinedLimit/test/diffNuisances.py fitDiagnostics.root  --format html > /eos/user/a/anmehta/www/DPSWW_v2/FitResults/NP.html
