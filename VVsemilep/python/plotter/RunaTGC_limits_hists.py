import optparse, subprocess, datetime, math, array, copy, os, re, sys,shutil


plots_odir="/eos/user/a/anmehta/www/VVsemilep/EFT_nllscans/"
baseDir=os.getcwd()
cards_dir='Cards/'

options = "--robustFit=1 --setRobustFitTolerance=0.2 --cminDefaultMinimizerStrategy=0 --X-rtd=MINIMIZER_analytic --X-rtd MINIMIZER_MaxCalls=99999999999 --cminFallbackAlgo Minuit2,Migrad,0:0.2 --stepSize=0.005 --X-rtd FITTER_NEW_CROSSING_ALGO --X-rtd FITTER_NEVER_GIVE_UP --X-rtd FITTER_BOUND"

def combineCards(yr,FS,WC,pf,splittopCR=True,vartop="mWV",varwj="mWV",varsig="mWV"): #fjet_pt
    date_dC=date+("_"+pf if len (pf) > 0 else "")
    eft_sig='_%s'%WC if len(WC)>0 else ''
    finalDC='dc_{date_dC}_{FS}_{yr}{op}_{vartop}topCR{top}_{varwj}wjCR_{varsig}sig.txt'.format(date_dC=date_dC,yr=yr,op=WC,FS=FS,vartop=vartop,top='incl' if not splittopCR else '',varwj=varwj,varsig=varsig)
    if splittopCR:
        topCRpart= '''top_cr_hi_{year}=Cards/cards_{date_dC}_boosted_onelep_topCR_hi_{vartop}_{year}/boosted_onelep_topCR_hi_{year}.txt top_cr_lo_{year}=Cards/cards_{date_dC}_boosted_onelep_topCR_lo_{vartop}_{year}/boosted_onelep_topCR_lo_{year}.txt'''.format(year=yr,date_dC=date_dC,vartop=vartop)
    else:
        topCRpart= '''top_cr_{year}=Cards/cards_{date_dC}_boosted_onelep_topCR_incl_{vartop}_{year}/boosted_onelep_topCR_incl_{year}.txt '''.format(year=yr,date_dC=date_dC,vartop=vartop)

    if FS == "onelep":
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


def commandsToRun(dc,pf,plots_odir,WC):
    outdir=os.path.join(baseDir,cards_dir)
    os.chdir(outdir)
    print "i am here",os.getcwd()
    os.chdir(baseDir)
    print "i am here",os.getcwd()
    dCard_str_wpath=dc.split('.txt')[0]
    print dCard_str_wpath
    dCard_str=dCard_str_wpath#dCard_str_wpath.replace('/','_')
    
    os.system("cp %s.txt %s" %(dCard_str_wpath,plots_odir))
    range_op="-3,3"
    points="2000"
    os.system("text2workspace.py {name}.txt -P HiggsAnalysis.AnalyticAnomalousCoupling.AnomalousCouplingEFTNegative:analiticAnomalousCouplingEFTNegative  --X-allow-no-signal  -o  model_{name}.root  --PO eftOperators={op}".format(name=dCard_str,op=WC))
    os.system("combine -M MultiDimFit model_{name}.root  --algo=grid --points {pts}  -m 125  -t -1  --redefineSignalPOIs k_{op}  --freezeParameters r --setParameters r=1,k_{op}=0  --setParameterRanges=k_{op}={range_op} {more} ".format(op=WC,name=dCard_str,pts=points,range_op=range_op,more=options)) #--verbose 3
    os.system("mkEFTScan.py higgsCombineTest.MultiDimFit.mH125.root  -p k_{op}  -lumi 58 -cms -preliminary -o {eos}/scan_{op}_{dc}.png ".format(op=WC,eos=plots_odir,dc=dCard_str))
    os.system("mkEFTScan.py higgsCombineTest.MultiDimFit.mH125.root  -p k_{op}  -lumi 58 -cms -preliminary -o {eos}/scan_{op}_{dc}.pdf " .format(op=WC,eos=plots_odir,dc=dCard_str))
    #os.system("combine  -M FitDiagnostics  model_{name}.root  -t -1 --saveNormalizations  --customStartingPoint --saveShapes --plots --redefineSignalPOIs k_{op} --freezeParameters r,k_{op} --cminDefaultMinimizerStrategy 0 --setParameters r=1,k_{op}=0 -v 1".format(name=dCard_str,op=WC)) #  # --robustFit=1  --toysFrequentist  #skip the signal fit 
    
    return True





if __name__ == '__main__':

    #year=sys.argv[1]
    #pf=sys.argv[1]

    date="2024-09-12" #datetime.date.today().isoformat() #"2021-12-02" #
    pf_input=""
    pf_output=""
    for op in ['cw']: #,'cb','c3w']:
        dC18=combineCards("2018","onelep",op,pf_input,False)
        commandsToRun(dC18,pf_output,plots_odir,op)
    #os.command('mv *%s* %s/'%(dC18.split('.txt')[0],cards_dir))

