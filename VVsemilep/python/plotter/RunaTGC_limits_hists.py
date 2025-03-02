import optparse, subprocess, datetime, math, array, copy, os, re, sys,shutil
lumis = {
    '2016APV': '19.5', #with HIPM
    '2016': '16.8', #without HIPM
    '2017': '41.5',
    '2018': '59.8',
    'run2': '137.6',
    'fullRun2': '137.6',
    '2016combo': '36.3',
}
plots_odir="/eos/user/a/anmehta/www/VVsemilep/EFT_nllscans/"
baseDir=os.getcwd()
cards_dir='Cards/'

options = "--robustFit=1 --setRobustFitTolerance=0.2 --cminDefaultMinimizerStrategy=0 --X-rtd=MINIMIZER_analytic --X-rtd MINIMIZER_MaxCalls=99999999999 --cminFallbackAlgo Minuit2,Migrad,0:0.2 --stepSize=0.005 --X-rtd FITTER_NEW_CROSSING_ALGO --X-rtd FITTER_NEVER_GIVE_UP --X-rtd FITTER_BOUND"




def combineCards(yr,FS,WC,pf,runOn="full",splitsig=True,vartop="mWV",varwj="mWV",varsig="mWV"): #fjet_pt
    date_dC=date+("_"+pf if len (pf) > 0 else "")
    eft_sig='_%s'%WC if len(WC)>0 else ''
    finalDC='dc_{date_dC}_{FS}_{yr}{op}_{runOn}.txt'.format(date_dC=date_dC,yr=yr,op=WC,FS=FS,runOn=runOn)
    #finalDC='dc_{date_dC}_{FS}_{yr}{op}_{vartop}topCR{top}_{varwj}wjCR_{varsig}sig.txt'.format(date_dC=date_dC,yr=yr,op=WC,FS=FS,vartop=vartop,top='incl' if not splittopCR else '',varwj=varwj,varsig=varsig)
    topCRpart='';wjCRpart='';sigpart='';
    if "full" in runOn or "topCR" in runOn or "CRonly" in runOn: 
        topCRpart= '''el_top_cr_{year}=Cards/cards_{date_dC}_boosted_el_topCR_incl_{vartop}_{year}/boosted_el_topCR_incl{WC}_{year}.txt mu_top_cr_{year}=Cards/cards_{date_dC}_boosted_mu_topCR_incl_{vartop}_{year}/boosted_mu_topCR_incl{WC}_{year}.txt'''.format(year=yr,date_dC=date_dC,vartop=vartop,WC=eft_sig)
    if "full" in runOn or "wjCR" in runOn or "CRonly" in runOn:
        wjCRpart= '''mu_wj_cr_hi_{year}=Cards/cards_{date_dC}_boosted_mu_wjCR_hi_{varwj}_{year}/boosted_mu_wjCR_hi{WC}_{year}.txt mu_wj_cr_lo_{year}=Cards/cards_{date_dC}_boosted_mu_wjCR_lo_{varwj}_{year}/boosted_mu_wjCR_lo{WC}_{year}.txt   el_wj_cr_hi_{year}=Cards/cards_{date_dC}_boosted_el_wjCR_hi_{varwj}_{year}/boosted_el_wjCR_hi{WC}_{year}.txt el_wj_cr_lo_{year}=Cards/cards_{date_dC}_boosted_el_wjCR_lo_{varwj}_{year}/boosted_el_wjCR_lo{WC}_{year}.txt'''.format(year=yr,date_dC=date_dC,varwj=varwj,WC=eft_sig)
    if "full" in runOn:
        if splitsig:
            sigpart= '''mu_sig_hi{WC}_{year}=Cards/cards_{date_dC}_boosted_mu_sig_hi_{varsig}_{year}/boosted_mu_sig_hi{WC}_{year}.txt mu_sig_lo{WC}_{year}=Cards/cards_{date_dC}_boosted_mu_sig_lo_{varsig}_{year}/boosted_mu_sig_lo{WC}_{year}.txt   el_sig_hi{WC}_{year}=Cards/cards_{date_dC}_boosted_el_sig_hi_{varsig}_{year}/boosted_el_sig_hi{WC}_{year}.txt el_sig_lo{WC}_{year}=Cards/cards_{date_dC}_boosted_el_sig_lo_{varsig}_{year}/boosted_el_sig_lo{WC}_{year}.txt'''.format(year=yr,date_dC=date_dC,WC=eft_sig,varsig=varsig)
        else:
            sigpart= "el_sig{WC}_{year}=Cards/cards_{date_dC}_boosted_el_sig_{varsig}_{year}/boosted_el_sig{WC}_{year}.txt  mu_sig{WC}_{year}=Cards/cards_{date_dC}_boosted_mu_sig_{varsig}_{year}/boosted_mu_sig{WC}_{year}.txt".format(year=yr,date_dC=date_dC,WC=eft_sig)
    cmd = 'combineCards.py   {sig} {topCR}  {wjCRpart} > {dc}'.format(dc=finalDC,sig=sigpart,topCR=topCRpart,wjCRpart=wjCRpart)
    print cmd
    os.system(cmd)
    if "full" in runOn or "CRonly" in runOn: 
        dC = open(finalDC, 'a')
        dC.write('''norm_tt       rateParam *{yr}  tt 1 [0,5]
norm_WJets_mu_{yr} rateParam mu*{yr}  WJets 1 [0,5]
norm_WJets_el_{yr} rateParam el*{yr}  WJets 1 [0,5]'''.format(yr=yr))
        dC.close()
    return finalDC


def commandsToRun(yr,dc,pf,plots_odir,WC,runEFT=True):
    outdir=os.path.join(baseDir,cards_dir)
    os.chdir(outdir)
    print "i am here",os.getcwd()
    os.chdir(baseDir)
    dCard_str_wpath=dc.split('.txt')[0]
    dCard_str=dCard_str_wpath
    if runEFT:
        range_op="-3,3"
        points="2000"
        os.system("text2workspace.py {name}.txt -P HiggsAnalysis.AnalyticAnomalousCoupling.AnomalousCouplingEFTNegative:analiticAnomalousCouplingEFTNegative  --X-allow-no-signal  -o  model_{name}.root  --PO eftOperators={op}".format(name=dCard_str,op=WC))
       # os.system("combine -M MultiDimFit model_{name}.root  --algo=grid --points {pts}  -m 125  -t -1  --redefineSignalPOIs k_{op}  --freezeParameters r --setParameters r=1,k_{op}=0  --setParameterRanges=k_{op}={range_op} {more} ".format(op=WC,name=dCard_str,pts=points,range_op=range_op,more=options)) #--verbose 3
        #os.system("mkEFTScan.py higgsCombineTest.MultiDimFit.mH125.root  -p k_{op}  -lumi {lumi} -cms -preliminary -o {eos}/scan_{op}_{dc} ".format(op=WC,eos=plots_odir,dc=dCard_str,lumi=lumis[yr]))
        #os.system("cp higgsCombineTest.MultiDimFit.mH125.root higgsCombineTest.MultiDimFit.mH125_{op}_{yr}.root".format(op=WC,yr=yr))
        #os.system("cp {dc}.txt {eos}/scan_{op}_{dc}.txt" .format(op=WC,eos=plots_odir,dc=dCard_str))
        os.system("combine  -M FitDiagnostics  model_{name}.root --rMin -2 --rMax 2  -t -1 --saveNormalizations  --customStartingPoint --saveShapes --saveWithUncertainties  --redefineSignalPOIs k_{op} --freezeParameters r,k_{op} --setParameters r=0,k_{op}=0 -v 1 {mops}".format(name=dCard_str,mops=options,op=WC)) #  # --plots --robustFit=1  --toysFrequentist  #skip the signal fit 
    else:
        print('running the SM case')
        os.system("text2workspace.py {name}.txt -o {name}.root ".format(name=dCard_str))
        os.system("combine -M FitDiagnostics {name}.root ".format(name=dCard_str,mops=options))  #saveNormalizations --saveShapes --saveWithUncertainties
        os.system("mv fitDiagnosticsTest.root fitDiagnosticsTest_SM_%s.root"%dCard_str)
        #os.system("combine -M MultiDimFit {name}_SM_ws.root -m 125  --saveWorkspace -n .bestfit_SM_{name}".format(name=dCard_str))

    return True





if __name__ == '__main__':

    year=sys.argv[1]
    #pf=sys.argv[1]
    date="2025-02-11" #datetime.date.today().isoformat() #"2021-12-02" #
    pf_input=""
    pf_output=""
    doWhat=sys.argv[2]
    if "SM" in doWhat: 
        for CR in ["wjCR","topCR"]: #,"CRonly"]: 
            if year == "fullRun2":
                dC18=combineCards("2018","onelep",'',pf_input,CR,True)
                dC17=combineCards("2017","onelep",'',pf_input,CR,True)
                dC16=combineCards("2016","onelep",'',pf_input,CR,True)
                dC16_apv=combineCards("2016APV","onelep",'',pf_input,CR,True)
                superdC='dc_{date}_onelep_{yr}_{CR}.txt'.format(CR=CR,date=date,yr=year)
                cmd='combineCards.py {yr1} {yr2} {yr3} {yr4} > {dc}'.format(dc=superdC,yr1=dC16,yr2=dC16_apv,yr3=dC17,yr4=dC18)
                os.system(cmd)
            elif year  == "2016combo":
                dC16=combineCards("2016","onelep",'',pf_input,CR,True)
                dC16_apv=combineCards("2016APV","onelep",'',pf_input,CR,True)
                superdC='dc_{date}_onelep_{yr}_{CR}.txt'.format(CR=CR,date=date,yr=year)
                cmd='combineCards.py {yr1} {yr2} > {dc}'.format(dc=superdC,yr1=dC16,yr2=dC16_apv)
                os.system(cmd)
            else:
                superdC=combineCards(year,"onelep",'',pf_input,CR,True)

            #commandsToRun(year,superdC,pf_output,plots_odir,'',False)    
    else:    
        for op in ['cw']: #,'c3w','cb']:
            superdC=''
            if year == "fullRun2":
                dC18=combineCards("2018","onelep",op,pf_input,"full",True)
                dC17=combineCards("2017","onelep",op,pf_input,"full",True)
                dC16=combineCards("2016","onelep",op,pf_input,"full",True)
                dC16_apv=combineCards("2016APV","onelep",op,pf_input,"full",True)
                superdC='dc_{date}_onelep_{yr}{op}_full.txt'.format(date=date,op=op,yr=year)
                cmd='combineCards.py {yr1} {yr2} {yr3} {yr4} > {dc}'.format(dc=superdC,yr1=dC16,yr2=dC16_apv,yr3=dC17,yr4=dC18)
                os.system(cmd)
            elif year  == "2016combo":
                dC16=combineCards("2016","onelep",op,pf_input,"full",True)
                dC16_apv=combineCards("2016APV","onelep",op,pf_input,"full",True)
                superdC='dc_{date}_onelep_{yr}{op}_full.txt'.format(date=date,op=op,yr=year)
                cmd='combineCards.py {yr1} {yr2} > {dc}'.format(dc=superdC,yr1=dC16,yr2=dC16_apv)
                os.system(cmd)
            else:
                superdC=combineCards(year,"onelep",op,pf_input,"full",True)

            commandsToRun(year,superdC,pf_output,plots_odir,op)
            #os.command('mv *%s* %s/'%(dC18.split('.txt')[0],cards_dir))







