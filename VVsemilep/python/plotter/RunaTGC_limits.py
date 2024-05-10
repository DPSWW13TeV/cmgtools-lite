import optparse, subprocess, datetime, math, array, copy, os, re, sys,shutil


outDir="/eos/user/a/anmehta/www/VVsemilep/EFT_nllscans/"
date="2024-02-21"

##date_wjest_ws="" AM add an option to replace the existing date if needed

def combineCards(yr,FS,WC,pf,usetopCR=False):
    date_dC=date+"_"+pf
    if FS == "onelep":
        finalDC='dc_{date_dC}_{FS}_{yr}{op}.txt'.format(date_dC=date_dC,yr=yr,op=WC,FS=FS)
        CRpart= '''top_cr_{year}=Cards/cards_{date_dC}_boosted_onelep_topCR_{year}/boosted_onelep_topCR_{year}.txt'''
        cmd1 = 'combineCards.py el_sb_lo_{year}=Cards/cards_{date_dC}_boosted_el_sb_lo_{year}/boosted_el_sb_lo_{WC}_{year}.txt  el_sb_hi_{year}=Cards/cards_{date_dC}_boosted_el_sb_hi_{year}/boosted_el_sb_hi_{WC}_{year}.txt   el_sig_{year}=Cards/cards_{date_dC}_boosted_el_sig_{year}/boosted_el_sig_{WC}_{year}.txt  mu_sb_lo_{year}=Cards/cards_{date_dC}_boosted_mu_sb_lo_{year}/boosted_mu_sb_lo_{WC}_{year}.txt  mu_sb_hi_{year}=Cards/cards_{date_dC}_boosted_mu_sb_hi_{year}/boosted_mu_sb_hi_{WC}_{year}.txt   mu_sig_{year}=Cards/cards_{date_dC}_boosted_mu_sig_{year}/boosted_mu_sig_{WC}_{year}.txt {topCR}  > {dc}'.format(year=yr,date_dC=date_dC,dc=finalDC,WC=WC,topCR=(CRpart if usetopCR else ''))
        os.system(cmd1)
        dC = open(finalDC, 'a')
        dC.write('''
Deco_WJets0_sim_el_WPM_mlvj_13TeV_eig1  param  0.0 2.0
Deco_WJets0_sim_el_WPM_mlvj_13TeV_eig0  param  0.0 2.0
Deco_WJets0_sim_el_WPM_mlvj_13TeV_eig3  param  0.0 2.0
Deco_WJets0_sim_el_WPM_mlvj_13TeV_eig2  param  0.0 2.0 
Deco_WJets0_sim_mu_WPM_mlvj_13TeV_eig1  param  0.0 2.0
Deco_WJets0_sim_mu_WPM_mlvj_13TeV_eig0  param  0.0 2.0
Deco_WJets0_sim_mu_WPM_mlvj_13TeV_eig3  param  0.0 2.0
Deco_WJets0_sim_mu_WPM_mlvj_13TeV_eig2  param  0.0 2.0 
slope_nuis    param  1.0 0.05
normvar_WJets_mu           flatParam
normvar_WJets_el           flatParam
rrv_c_ChiSq_WJets0_mu      flatParam
rrv_n_ExpN_WJets0_sb_mu    flatParam
rrv_c_ExpN_WJets0_sb_mu    flatParam
rrv_shift_ChiSq_WJets0_el  flatParam
rrv_c_ChiSq_WJets0_el      flatParam
rrv_shift_ChiSq_WJets0_mu  flatParam
rrv_n_ExpN_WJets0_sb_el    flatParam
rrv_c_ExpN_WJets0_sb_el    flatParam
''')
        dC.close()
        #commandsToRun(finalDC,pf,outDir)
    else:
        dC1='dc_{date_dC}_{FS}_{yr}{op}.txt'.format(date_dC=date_dC,yr=yr,op=WC,FS=FS)
        cmd1 = 'combineCards.py {FS}_sb_lo_{year}=Cards/cards_{date_dC}_boosted_{FS}_sb_lo_{year}/boosted_{FS}_sb_lo_{WC}_{year}.txt  {FS}_sb_hi_{year}=Cards/cards_{date_dC}_boosted_{FS}_sb_hi_{year}/boosted_{FS}_sb_hi_{WC}_{year}.txt   {FS}_sig_{year}=Cards/cards_{date_dC}_boosted_{FS}_sig_{year}/boosted_{FS}_sig_{WC}_{year}.txt top_cr_{year}=Cards/cards_{date_dC}_boosted_onelep_topCR_{year}/boosted_onelep_topCR_{year}.txt  > {dc}'.format(year=yr,date_dC=date_dC,dc=dC1,FS=FS,WC=WC)
        os.system(cmd1)
        dC = open(dC1, 'a')
        dC.write('''norm_tt       rateParam *{yr}  tt 1 [0,5]
Deco_WJets0_sim_{FS}_WPM_mlvj_13TeV_eig1  param  0.0 2.0
Deco_WJets0_sim_{FS}_WPM_mlvj_13TeV_eig0  param  0.0 2.0
Deco_WJets0_sim_{FS}_WPM_mlvj_13TeV_eig3  param  0.0 2.0
Deco_WJets0_sim_{FS}_WPM_mlvj_13TeV_eig2  param  0.0 2.0    '''.format(yr=yr,FS=FS))
        dC.close()
    
    return True


def commandsToRun(dc,pf,outDir):
    baseDir=os.getcwd()
    combdir='Cards/'
    outdir=os.path.join(baseDir,combdir)

    os.chdir(outdir)
    print "i am here",os.getcwd()
    dCard_str_wpath=dc.split('.txt')[0]
    dCard_str=dCard_str_wpath.replace('/','_')
    os.system("cp %s.txt %s" %(dCard_str_wpath,outDir))
    os.system("text2workspace.py  %s.txt -P HiggsAnalysis.AnalyticAnomalousCoupling.AnomalousCouplingEFTNegative:analiticAnomalousCouplingEFTNegative  --X-allow-no-signal  -o  model_%s.root   --PO eftOperators=cwww" %(dCard_str,dCard_str)) #  --X-allow-no-signal
    os.system("combine -M MultiDimFit model_%s.root  --algo=grid --points 1000  -m 125  -t -1  --redefineSignalPOIs k_cwww  --freezeParameters r --setParameters r=1   --setParameterRanges k_cwww=-10,10  --X-rtd MINIMIZER_MaxCalls=400000  --cminDefaultMinimizerTolerance 0.5 --cminDefaultMinimizerStrategy 0 --X-rtd SIMNLL_NO_LEE --X-rtd NO_ADDNLL_FASTEXIT  --alignEdges 1  --verbose 9"%(dCard_str_wpath))
    os.system("mkEFTScan.py higgsCombineTest.MultiDimFit.mH125.root  -p k_cwww -maxNLL 10 -lumi 58 -cms -preliminary -o %s/scan_%s_%s.png -xlabel \"c_{www}*3.6 [TeV^{-2}]\"" %(outDir,dCard_str,pf))
    os.system("mkEFTScan.py higgsCombineTest.MultiDimFit.mH125.root  -p k_cwww -maxNLL 10 -lumi 58 -cms -preliminary -o %s/scan_%s_%s.pdf -xlabel \"c_{www}*3.6 [TeV^{-2}]\"" %(outDir,dCard_str,pf))
    os.system("combine  -M FitDiagnostics  model_%s.root  -t -1 --redefineSignalPOIs k_cwww --freezeParameters r --cminDefaultMinimizerStrategy 0 --toysFrequentist --setParameters r=1    --setParameterRanges k_cwww=-10,10 --robustFit=1  --verbose 3 --saveNormalizations  --saveShapes --plots "%(dCard_str_wpath)) #--plots --toysFile higgsCombineTest.GenerateOnly.mH125.123456.root -t -1 

    return True





if __name__ == '__main__':

    #year=sys.argv[1]
    pf="" #sys.argv[1]
    date=datetime.date.today().isoformat() #"2021-12-02" #

    extra="" #_bb17c50f50" #_VGN50"
    #vartopCR="mWV"+extra
    #baseDir=os.getcwd()
    #combdir='Cards/combination/'
    #outdir=os.path.join(baseDir,combdir)
    #print outdir
    #cspf=['plusplus','minusminus']
    #dC16=combineCards("2016")
    #dC17=combineCards("2017")
    #dC18=combineCards("2018","onelep","cwww",pf)
    commandsToRun("aC_WWWZ_simfit_2018_2024-02-21.txt",pf,outDir)
    #commandsToRun()
    ##amsuperdC='dc_{pf}_onelep_FR2{cg}.txt'.format(cg=cc,pf=str(date+"-"+bS2lss+vartopCR+bS4l))
    ##amcmd='combineCards.py {yr1} {yr2} {yr3} > {dc}'.format(dc=superdC,yr1=dC16,yr2=dC17,yr3=dC18)
    ##amos.system(cmd)
    ##amrunCombine='combine -M Significance  {finalDC}'.format(finalDC=superdC)
    ##amos.system(runCombine)
    ##amos.system("text2workspace.py {finalDC} -m 125".format(finalDC=superdC))
    ##amos.system("cp {finalDC}.root {finalDC}_workspace.root".format(finalDC=superdC))
    ##amos.system('mv finalDC* {od}/'.format(od=outdir,finalDC=superdC))
    


#text2workspace.py Cards/combination/dc_2022-01-24-SoBord_sqV3m3lm4l_ll_noee_FR2_cs_combined.txt -o dc_2022-01-24_FR2_workspace.root

#combine -M FitDiagnostics dc_2022-01-24_FR2_workspace.root  -t -1 --saveShapes --saveWithUncertainties --saveNormalizations --saveOverallShapes

#python test/diffNuisances.py -a fitDiagnosticsTest.root -g plots.root --abs --all --format text > /eos/user/a/anmehta/www/datacard_review/diffnuisance_asimov.txt

#os.system("combine -M GenerateOnly model_test.root --toysFrequentist -t -1 --saveToys  -m 125 --redefineSignalPOIs k_cwww  --freezeParameters r   --setParameters r=1    --setParameterRanges k_cwww=-10,10")# --X-rtd SIMNLL_NO_LEE --X-rtd NO_ADDNLL_FASTEXIT")



#os.system("combine  -M FitDiagnostics   model_test.root --toysFile higgsCombineTest.GenerateOnly.mH125.123456.root -t -1 --redefineSignalPOIs k_cwww --freezeParameters r --cminDefaultMinimizerStrategy 0 --toysFrequentist --setParameters r=1    --setParameterRanges k_cwww=-10,10 --robustFit=1  --rMin -10 --rMax 10 --verbose 9")# --X-rtd SIMNLL_NO_LEE --X-rtd NO_ADDNLL_FASTEXIT") # --freezeParameters r



