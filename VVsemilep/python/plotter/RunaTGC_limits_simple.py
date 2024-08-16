import optparse, subprocess, datetime, math, array, copy, os, re, sys,shutil


outDir="/eos/user/a/anmehta/www/VVsemilep/EFT_nllscans/"
#date="2024-07-29"

##date_wjest_ws="" AM add an option to replace the existing date if needed

def combineCards(yr,FS,WC,pf,vartop="fjet_pt",varwj="fjet_pt",varsig="mWV_binning"):
    date_dC=date+("_"+pf if len (pf) > 0 else "")
    eft_sig='_%s'%WC if len(WC)>0 else ''
    finalDC='dc_{date_dC}_{FS}_{yr}{op}_{vartop}topCR_{varwj}wjCR_{varsig}sig.txt'.format(date_dC=date_dC,yr=yr,op=WC,FS=FS,vartop=vartop,varwj=varwj,varsig=varsig)
    topCRpart= '''top_cr_hi_{year}=Cards/cards_{date_dC}_boosted_onelep_topCR_hi_{vartop}_{year}/boosted_onelep_topCR_hi_{year}.txt top_cr_lo_{year}=Cards/cards_{date_dC}_boosted_onelep_topCR_lo_{vartop}_{year}/boosted_onelep_topCR_lo_{year}.txt'''.format(year=yr,date_dC=date_dC,vartop=vartop)
    if FS == "onelep":
        wjCRpart_onelep= '''wj_cr_hi_{year}=Cards/cards_{date_dC}_boosted_onelep_wjCR_hi_{varwj}_{year}/boosted_onelep_wjCR_hi_{year}.txt wj_cr_lo_{year}=Cards/cards_{date_dC}_boosted_onelep_wjCR_lo_{varwj}_{year}/boosted_onelep_wjCR_lo_{year}.txt'''.format(year=yr,date_dC=date_dC,varwj=varwj)
        wjCRpart= '''mu_wj_cr_hi_{year}=Cards/cards_{date_dC}_boosted_mu_wjCR_hi_{varwj}_{year}/boosted_mu_wjCR_hi_{year}.txt mu_wj_cr_lo_{year}=Cards/cards_{date_dC}_boosted_mu_wjCR_lo_{varwj}_{year}/boosted_mu_wjCR_lo_{year}.txt   el_wj_cr_hi_{year}=Cards/cards_{date_dC}_boosted_el_wjCR_hi_{varwj}_{year}/boosted_el_wjCR_hi_{year}.txt el_wj_cr_lo_{year}=Cards/cards_{date_dC}_boosted_el_wjCR_lo_{varwj}_{year}/boosted_el_wjCR_lo_{year}.txt'''.format(year=yr,date_dC=date_dC,varwj=varwj)
        cmd1 = 'combineCards.py  el_sig_{year}=Cards/cards_{date_dC}_boosted_el_sig_{varsig}_{year}/boosted_el_sig{WC}_{year}.txt  mu_sig_{year}=Cards/cards_{date_dC}_boosted_mu_sig_{varsig}_{year}/boosted_mu_sig{WC}_{year}.txt {topCR}  {wjCRpart} > {dc}'.format(year=yr,date_dC=date_dC,dc=finalDC,topCR=topCRpart,wjCRpart=wjCRpart,varsig=varsig,WC=eft_sig)
    else:
        wjCRpart= '''{FS}_wj_cr_hi_{year}=Cards/cards_{date_dC}_boosted_{FS}_wjCR_hi_{varwj}_{year}/boosted_{FS}_wjCR_hi_{year}.txt {FS}_wj_cr_lo_{year}=Cards/cards_{date_dC}_boosted_{FS}_wjCR_lo_{varwj}_{year}/boosted_{FS}_wjCR_lo_{year}.txt '''.format(FS=FS,year=yr,date_dC=date_dC,varwj=varwj)
        cmd1 = 'combineCards.py   {FS}_sig_{year}=Cards/cards_{date_dC}_boosted_{FS}_sig_{varsig}_{year}/boosted_{FS}_sig{WC}_{year}.txt {topCR}  {wjCRpart} > {dc}'.format(year=yr,date_dC=date_dC,dc=finalDC,topCR=topCRpart,wjCRpart=wjCRpart,varsig=varsig,WC=eft_sig,FS=FS)

    print cmd1
    os.system(cmd1)
    dC = open(finalDC, 'a')
    dC.write('''norm_tt       rateParam *{yr}  tt 1 [0,5]
norm_WJets rateParam *{yr}  WJets 1 [0,5]'''.format(yr=yr))
    dC.close()
    return finalDC
    return dC


def commandsToRun(dc,pf,outDir,WC):
    baseDir=os.getcwd()
    combdir='Cards/'
    outdir=os.path.join(baseDir,combdir)

    os.chdir(outdir)
    print "i am here",os.getcwd()
    os.chdir(baseDir)
    print "i am here",os.getcwd()
    
    dCard_str_wpath=dc.split('.txt')[0]
    print dCard_str_wpath
    dCard_str=dCard_str_wpath#dCard_str_wpath.replace('/','_')
    
    os.system("cp %s.txt %s" %(dCard_str_wpath,outDir))
    os.system("text2workspace.py  %s.txt -P HiggsAnalysis.AnalyticAnomalousCoupling.AnomalousCouplingEFTNegative:analiticAnomalousCouplingEFTNegative  --X-allow-no-signal  -o  model_%s.root  --PO eftOperators=%s" %(dCard_str,dCard_str,WC)) #  --X-allow-no-signal
    os.system("combine -M MultiDimFit model_%s.root  --algo=grid --points 1000  -m 125  -t -1  --redefineSignalPOIs k_%s  --freezeParameters r --setParameters r=1  --setParameterRanges  k_%s=-5,5 --X-rtd MINIMIZER_MaxCalls=400000  --cminDefaultMinimizerTolerance 0.5 --cminDefaultMinimizerStrategy 0 --X-rtd SIMNLL_NO_LEE --X-rtd NO_ADDNLL_FASTEXIT  --alignEdges 1  --verbose 1"%(dCard_str_wpath,WC,WC))
    os.system("mkEFTScan.py higgsCombineTest.MultiDimFit.mH125.root  -p k_%s  -lumi 58 -cms -preliminary -o %s/scan_%s%s.png -xlabel \"c_{%s} [TeV^{-2}]\"" %(WC,outDir,dCard_str,WC,pf))
    os.system("mkEFTScan.py higgsCombineTest.MultiDimFit.mH125.root  -p k_%s  -lumi 58 -cms -preliminary -o %s/scan_%s%s.pdf -xlabel \"c_{%s} [TeV^{-2}]\"" %(WC,outDir,dCard_str,WC,pf))
    #os.system("combine  -M FitDiagnostics  model_%s.root  -t -1 --expectSignal 1  --redefineSignalPOIs k_%s --freezeParameters r,k_%s --cminDefaultMinimizerStrategy 0 --toysFrequentist  --robustFit=1  --setParameters r=1"%(dCard_str,WC,WC)) #--saveNormalizations  --saveShapes --plots  
    
    return True





if __name__ == '__main__':

    #year=sys.argv[1]
    #pf=sys.argv[1]
    date="2024-08-15" #datetime.date.today().isoformat() #"2021-12-02" #
    pf=""
    dC18=combineCards("2018","onelep","c3w",pf)
    commandsToRun(dC18,pf,outDir,"c3w")
    

#text2workspace.py Cards/combination/dc_2022-01-24-SoBord_sqV3m3lm4l_ll_noee_FR2_cs_combined.txt -o dc_2022-01-24_FR2_workspace.root

#combine -M FitDiagnostics dc_2022-01-24_FR2_workspace.root  -t -1 --saveShapes --saveWithUncertainties --saveNormalizations --saveOverallShapes

#python test/diffNuisances.py -a fitDiagnosticsTest.root -g plots.root --abs --all --format text > /eos/user/a/anmehta/www/datacard_review/diffnuisance_asimov.txt

#os.system("combine -M GenerateOnly model_test.root --toysFrequentist -t -1 --saveToys  -m 125 --redefineSignalPOIs k_cwww  --freezeParameters r   --setParameters r=1    --setParameterRanges k_cwww=-10,10")# --X-rtd SIMNLL_NO_LEE --X-rtd NO_ADDNLL_FASTEXIT")



#os.system("combine  -M FitDiagnostics   model_test.root --toysFile higgsCombineTest.GenerateOnly.mH125.123456.root -t -1 --redefineSignalPOIs k_cwww --freezeParameters r --cminDefaultMinimizerStrategy 0 --toysFrequentist --setParameters r=1    --setParameterRanges k_cwww=-10,10 --robustFit=1  --rMin -10 --rMax 10 --verbose 9")# --X-rtd SIMNLL_NO_LEE --X-rtd NO_ADDNLL_FASTEXIT") # --freezeParameters r



## text2workspace.py test.txt  -P HiggsAnalysis.AnalyticAnomalousCoupling.AnomalousCouplingEFTNegative:analiticAnomalousCouplingEFTNegative  --X-allow-no-signal  -o  model_test.root  --PO eftOperators=cb 

## combine -M MultiDimFit model_test.root  --algo=grid --points 1000  -m 125  -t -1  --redefineSignalPOIs k_cb  --freezeParameters r --setParameters r=1  --setParameterRanges  k_cb=-10,10 --X-rtd MINIMIZER_MaxCalls=400000  --cminDefaultMinimizerTolerance 0.5 --cminDefaultMinimizerStrategy 0 --X-rtd SIMNLL_NO_LEE --X-rtd NO_ADDNLL_FASTEXIT  --alignEdges 1 --verbose 9
#        cmd1 = 'combineCards.py el_sb_lo_{year}=Cards/cards_{date_dC}_boosted_el_sb_lo_{year}/boosted_el_sb_lo{WC}_{year}.txt  el_sb_hi_{year}=Cards/cards_{date_dC}_boosted_el_sb_hi_{year}/boosted_el_sb_hi{WC}_{year}.txt   el_sig_{year}=Cards/cards_{date_dC}_boosted_el_sig_{year}/boosted_el_sig{WC}_{year}.txt  mu_sb_lo_{year}=Cards/cards_{date_dC}_boosted_mu_sb_lo_{year}/boosted_mu_sb_lo{WC}_{year}.txt  mu_sb_hi_{year}=Cards/cards_{date_dC}_boosted_mu_sb_hi_{year}/boosted_mu_sb_hi{WC}_{year}.txt   mu_sig_{year}=Cards/cards_{date_dC}_boosted_mu_sig_{year}/boosted_mu_sig{WC}_{year}.txt {topCR}  > {dc}'.format(year=yr,date_dC=date_dC,dc=finalDC,topCR=(CRpart if usetopCR else ''),WC=eft_sig)
#        CRpart= '''top_cr_oneb_{year}=Cards/cards_{date_dC}_boosted_onelep_topCR_oneb_{year}/boosted_onelep_topCR_oneb_{year}.txt top_cr_twob_{year}=Cards/cards_{date_dC}_boosted_onelep_topCR_twob_{year}/boosted_onelep_topCR_twob_{year}.txt'''.format(year=yr,date_dC=date_dC)
