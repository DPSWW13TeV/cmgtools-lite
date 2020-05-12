for k in  CP2_genTree CP5_genTree #dps_unshowered_had_pythia_ComCP5_MPIon #WWDPSCP5py8  #DPS2017HWpp WWTo2L2NuDPSCH3hw7 
#for k in WWTo2L2NuDPSpy8 dps_showered_had_pythia_ComCP5 dps_unshowered_had_pythia_ComCP5
do
    echo ${k}
    python treeReader.py -i ${k} -o ${PWD}
    #python jets.py -i ${k} -o ${PWD}
done
