import os
baseDir="/eos/cms/store/cmst3/group/dpsww/"
Trees="signal_FRonly_reco/2016/"
Trees="Signal_nanoV7/"
skimmedTrees="Signal_nanoV7_skim2lss"
Friends_recl_unskimmed="2_recl"
for i in "2016,2017,2018".split(","):
    #    os.system("python skimTreesNew.py  mca-skim-{yr}.txt  dps-ww/fullRun2/skim_2lss_3l_FO.txt {baseDir}/{skimmedTrees}/{yr}/ -P {baseDir}/{Trees}/{yr}/ --Fs {baseDir}/{Trees}/{yr}/{Friends_recl_unskimmed}  --skim-friends --mcc dps-ww/fullRun2/lepchoice-ttH-FO.txt -j8  --tree NanoAOD --skim-friends".format(baseDir=baseDir,skimmedTrees=skimmedTrees,yr=i,Trees=Trees,Friends_recl_unskimmed=Friends_recl_unskimmed))
    for j in ["dpsbdt_neu_ssnoeebkg_afacdps","dpsbdt_neu_ssnoeebkg_afacdps_unclEn","2_btag_SFs"]: #"3_tauCount","muPrefiring","0_jmeUnc_v2","puWts","nnpdf_rms","4_scalefactors","postFSRinfo"]: #,"dpsbdt_neu_ssnoeebkg_afacdps_unclEn"]:
        #"nnpdf_rms","4_scalefactors","2_recl_allvars"
        #,"bdt_input_vars_toInfnBeynd","dpsbdt_neu_ssnoeebkg_afacdps","dpsbdt_neu_ssnoeebkg_afacdps_unclEn"]:
        #"dpsbdt_neu_ssnoeebkg_afacdps_unclEn","dpsbdt_ssnoeebkg_afacdps","2_btag_SFs","2_recl_allvars","muPrefiring","3_tauCount","4_scalefactors","0_jmeUnc_v2","puWts"]:
        #"bdt_input_vars_toInfnBeynd",]
        os.system("python ~/public/haddFriends_v2.py /eos/cms/store/cmst3/group/dpsww/signal_FRonly_reco//{yr}/{frnd}".format(yr=i,frnd=j))
        #os.system("python ~/public/haddFriends_v2.py /eos/cms/store/cmst3/group/dpsww/signal_fullstats_skim2lss/{yr}/{frnd}".format(yr=i,frnd=j))

        #os.system("python skimFTreesNew.py {baseDir}/{skimmedTrees}/{yr}/ {baseDir}/{Trees}/{yr}/{frnd}".format(baseDir=baseDir,skimmedTrees=skimmedTrees,yr=i,Trees=Trees,frnd=j))
