#!/bin/sh
path=`pwd`
variations=("Up" "Down")
sources=("jesAbsolute" "jesEC2" "jesHF_year" "res_j_endcap1_year" "jesAbsolute_year" "jesEC2_year" "jesRelativeBal" "res_j_endcap2highpt_year" "jesBBEC1" "jesFlavorQCD" "jesRelativeSample_year" "res_j_endcap2lowpt_year" "jesBBEC1_year" "jesHF" "res_j_barrel_year")

for src in "${sources[@]}"
do
    for var in "${variations[@]}"
    do
	iFile=fr-${src}${var}.txt
	cat template.txt > dummy.txt
	sed -e 's/SOURCEVAR/'${src}${var}'/g' dummy.txt > $iFile
	rm dummy.txt
    done
done
