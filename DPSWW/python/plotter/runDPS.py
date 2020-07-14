#!/usr/bin/env python
import optparse, subprocess, ROOT, datetime, math, array, copy, os, re, sys
import numpy as np
lumis = {
    '2016': '35.9',
    '2017': '41.4',
    '2018': '59.7',
    'all' : '35.9,41.4,59.7',
}





def runCards(trees, friends, MCfriends, Datafriends, targetdir, fmca, fcut, fsyst, plotbin, enabledcuts, disabledcuts, processes, scaleprocesses, year,extraopts = '',invertedcuts = []):
    varToFit= '{plotvar} {binning}'.format(plotvar=plotbin.split()[0], binning=plotbin.split()[1])
    cmd  = ' makeShapeCardsNew.py --s2v -f -j 8 -l {lumi} --od {CARDSOUTDIR} --tree NanoAOD --year {YEAR} --mcc dps-ww/fullRun2/lepchoice-ttH-FO.txt --WA prescaleFromSkim --mcc dps-ww/fullRun2/mcc-METFixEE2017.txt {fmca} {fcut} --asimov signal --amc --threshold 0.01 --neg --split-factor=-1 --unc {fsyst} -P {trees} {varName} '.format(lumi=lumis[year],CARDSOUTDIR=targetdir, trees=trees, fmca=fmca, fcut=fcut,YEAR=year,fsyst=fsyst,varName=varToFit)
    #    BDT_DPS_WZ 20,0,1.0
    cmd += ''.join(' --Fs '+frnd for frnd in friends)
    cmd += ''.join(' --FMCs '+frnd for frnd in MCfriends)
    cmd += ''.join(' --FDs '+frnd for frnd in Datafriends)

    cmd += ''.join(' -E ^'+cut for cut in enabledcuts )
    cmd += ''.join(' -X ^'+cut for cut in disabledcuts)

    cmd += ' -p '+','.join(processes)
    if invertedcuts:
        cmd += ''.join(' -I ^'+cut for cut in invertedcuts )

    cmd += ' -W L1PreFiringWeight_Nom*puWeight*leptonSF_2lss *triggerSF_ttH(LepGood_pdgId[iLepFO_Recl[0]], LepGood_conePt[iLepFO_Recl[0]], LepGood_pdgId[iLepFO_Recl[1]], LepGood_conePt[iLepFO_Recl[1]],year)'

    if scaleprocesses:
        for proc,scale in scaleprocesses.items():
            cmd += ' --scale-process {proc} {scale} '.format(proc=proc, scale=scale)
    if len(fsyst) > 0:
        cmd += ' --unc {fsyst} '.format(fsyst=fsyst)
    if extraopts:
        cmd += ' '+extraopts


    print '============================================================================================='
    print 'running: python', cmd
    print '============================================================================================='
    subprocess.call(['python']+cmd.split())#+['/dev/null'],stderr=subprocess.PIPE)

def runplots(trees, friends, MCfriends, Datafriends, targetdir, fmca, fcut, fsyst, fplots, enabledcuts, disabledcuts, processes, scaleprocesses, fitdataprocess, plotlist, showratio, year,nLep,extraopts = '', invertedcuts = []):


    #if not type(trees)==list: trees = [trees]
    #treestring = ' '.join(' -P '+ t for t in list(trees))

    #cmd  = ' mcPlots.py -f -j 8 -l {lumi} --tree NanoAOD --year {YEAR} --mcc dps-ww/lepchoice-ttH-FO.txt --WA prescaleFromSkim --mcc dps-ww/mcc-METFixEE2017.txt --pdir {td} -P {trees} --FMCs {trees}/0_jmeUnc_v1 --FDs {trees}/1_recl --FMCs {trees}/1_recl_allvars --FMCs {trees}/2_btag_SFs --FMCs {trees}/2_scalefactors_lep_fixed --Fs {trees}/3_tauCount {fmca} {fcut} {fplots} --split-factor=-1 --unc {fsyst}'.format(lumi=lumis[year],td=targetdir, trees=trees, fmca=fmca, fcut=fcut, fplots=fplots,YEAR=year,fsyst=fsyst)

    cmd  = ' mcPlots.py -f -j 10 -l {lumi} --tree NanoAOD --year {YEAR} --mcc dps-ww/fullRun2/lepchoice-ttH-FO.txt --WA prescaleFromSkim --mcc dps-ww/fullRun2/mcc-METFixEE2017.txt --pdir {td} {fmca} {fcut} {fplots} --split-factor=-1  -P {trees}'.format(lumi=lumis[year],td=targetdir, trees=trees, fmca=fmca, fcut=fcut, fplots=fplots,YEAR=year)#,fsyst=fsyst)

    if fsyst:
        cmd += ' --unc {fsyst} '.format(fsyst=fsyst)

    cmd += ''.join(' --Fs '+frnd for frnd in friends)
    cmd += ''.join(' --FMCs '+frnd for frnd in MCfriends)
    cmd += ''.join(' --FDs '+frnd for frnd in Datafriends)

    cmd += ''.join(' -E ^'+cut for cut in enabledcuts )
    cmd += ''.join(' -X ^'+cut for cut in disabledcuts)
    if invertedcuts:
        cmd += ''.join(' -I ^'+cut for cut in invertedcuts )

    cmd += ' --sP '+','.join(plot for plot in plotlist)
    cmd += ' -p '+','.join(processes)

    if(nLep == 3):
        cmd += ' -W L1PreFiringWeight_Nom*puWeight*leptonSF_3l *triggerSF_ttH(LepGood_pdgId[iLepFO_Recl[0]], LepGood_conePt[iLepFO_Recl[0]], LepGood_pdgId[iLepFO_Recl[1]], LepGood_conePt[iLepFO_Recl[1]],3,year)'
    elif(nLep == 4):
        cmd += ' -W L1PreFiringWeight_Nom*puWeight*leptonSF_4l *triggerSF_ttH(LepGood_pdgId[iLepFO_Recl[0]], LepGood_conePt[iLepFO_Recl[0]], LepGood_pdgId[iLepFO_Recl[1]], LepGood_conePt[iLepFO_Recl[1]],3,year)'
    else:
        cmd += ' -W L1PreFiringWeight_Nom*puWeight*leptonSF_2lss *triggerSF_ttH(LepGood_pdgId[iLepFO_Recl[0]], LepGood_conePt[iLepFO_Recl[0]], LepGood_pdgId[iLepFO_Recl[1]], LepGood_conePt[iLepFO_Recl[1]],year)'

    cmd += ' -o '+targetdir+'/'+'_AND_'.join(plot for plot in plotlist)+'.root'
    if fitdataprocess:
        cmd+= ' --fitData '
        cmd+= ''.join(' --flp '+proc for proc in fitdataprocess)
    if scaleprocesses:
        for proc,scale in scaleprocesses.items():
            cmd += ' --scale-process {proc} {scale} '.format(proc=proc, scale=scale)
    showrat   = ''
    if showratio:
        showrat = ' --showRatio '
    cmd += showrat
    if extraopts:
        cmd += ' '+extraopts

    print 'running: python', cmd
    subprocess.call(['python']+cmd.split())#+['/dev/null'],stderr=subprocess.PIPE)


def makeResults(year,finalState,splitCharge,doWhat):
    trees='/eos/cms/store/cmst3/group/dpsww/NanoTrees_TTH_090120_091019_v6_skim2lss/{year}/'.format(year=year)
    friends=[trees+'3_tauCount',trees+'dpsbdt']
    MCfriends = [trees+'1_recl_allvars',trees+'2_btag_SFs',trees+'2_scalefactors_lep_fixed',trees+'0_jmeUnc_v1']
    Datafriends=[trees+'1_recl']
    targetdir = '/eos/user/a/anmehta/www/DPSWW_v2/{date}{pf}_era{year}/'.format(date=date, year=year,pf=('-'+postfix if postfix else '') ) 
    fplots = 'dps-ww/fullRun2/plots.txt'
    fmca = 'dps-ww/fullRun2/mca-dpsww.txt'
    fsyst  = 'dps-ww/fullRun2//systsUnc.txt' #dps-ww/fullRun2/syst.txt'
    fcut   = 'dps-ww/fullRun2/cuts_2lss.txt'


    print '=========================================='
    print 'run results for something'
    print '=========================================='
    print 'confirm the binning of 1D BDT histogram'
    print '=========================================='

    if splitCharge: 
        loop = [ 'minusminus', 'plusplus']
    else:
        loop = [ '' ]

    print 'running for %s with charge split flag %s' %(finalState,splitCharge)

    processes=['DPSWW','Rares','Convs','ZZ','WZ','data_flips','data_fakes','promptsub','data']
    #processes=['DPSWW','Rares','Convs','ZZ','WZ','data_flips','data_fakes','promptsub','data']
    fRvars= ['_FRe_norm_Up','_FRe_norm_Dn','_FRe_pt_Up','_FRe_pt_Dn','_FRe_be_Up','_FRe_be_Dn','_FRm_norm_Up','_FRm_norm_Dn','_FRm_pt_Up','_FRm_pt_Dn','_FRm_be_Up','_FRm_be_Dn']




    if finalState[0] in ['mumu','elel']:
        binningBDT   = ' unroll_2Dbdt_dps_mumu(BDT_DPS_fakes,BDT_DPS_WZ) 15,0.0,15.0'

    else:
        binningBDT   = ' unroll_2Dbdt_dps_elmu(BDT_DPS_fakes,BDT_DPS_WZ) 15,0.0,15.0'

    essentials=['tcharge1','tcharge2']#conept1','conept2','pt1','pt2','MVA1','MVA2','met','nBJetLoose25','nBJetMedium25','nBJetTight25','nBJetLoose40','nBJetMedium40','nBJetTight40','nTauTight']

    allvars=['conept1','conept2','pt1','pt2','eta1','eta2','phi1','phi2','MVA1','MVA2','tcharge1','tcharge2','charge1','charge2','pdgId1','pdgId2','dilep_charge','dilep_flav','met','metphi','njets','mll','mt2ll','mt1','mtll','etasum','etaprod','dphill','dphil2met','dphilll2','nVert','BDT_wz','BDT_fakes','BDT1d']        
    
    #    configs=['elmu','mumu','elel','plusplus','minusminus']
    plotvars=essentials

    for FS in finalState:            
        for ch in loop:
            enable=[]
            enable.append(FS); 
            if len(ch)>0 : 
                enable.append(ch)
            print enable #list(ch) + list (finalState)
            disable   = []
            invert    = []
            fittodata = []
            scalethem = {}
            ratio   = ' --fixRatioRange  --ratioYNDiv 505 --maxRatioRange 0.0  1.99'
            spam    = ' --topSpamSize 1.0 --noCms '
            legends = ' --legendFontSize 0.04 --legendBorder 0 --legendWidth  0.62 --legendColumns 3 '
            ubands  = ' --showMCError '
            anything = "  --neglist '.*_promptsub.*' --plotgroup data_fakes+=.*_promptsub" #" #to include neagitve evt ylds from fakes --plotmode norm
            extraopts = ratio + spam + legends + ubands + anything
               

            if splitCharge:
                makeplots1  = ['{}_{}{}'.format(a,FS,ch)  for a in plotvars]
            else:
                makeplots1  = ['{}_{}'.format(a,FS) for a in plotvars]
            
            if 'plots' in doWhat:
                makeplots=makeplots1 #+makeplots2
                print makeplots1
                runplots(trees, friends, MCfriends, Datafriends, targetdir, fmca, fcut, fsyst, fplots, enable, disable, processes, scalethem, fittodata,makeplots,True, year, 2,extraopts,invert)

            if 'cards' in doWhat:
            ## ==================================
            ## running datacards
            ## ==================================
                #processes+=['data_fakes'+i for i in fRvars]
                targetcarddir = 'Cards/cards_{date}{pf}_{FS}_era{year}'.format(FS=FS,year=year,date=date, pf=('-'+postfix if postfix else '') )
                extraoptscards = ' --binname dpsww_{year}_{FS}{ch}'.format(year=year,FS=FS,ch=(ch if ch else ''))
                runCards(trees, friends, MCfriends, Datafriends, targetcarddir, fmca, fcut, fsyst , binningBDT, enable, disable, processes, scalethem, year,extraoptscards,invert)
########################################



def threelepCRPlot(year):
    print '=========================================='
    print 'running 3l control region  plots'
    print '=========================================='
    trees='/eos/cms/store/cmst3/group/dpsww/NanoTrees_TTH_090120_091019_v6_skim2lss/{year}/'.format(year=year)
    friends=[trees+'3_tauCount',trees+'dpsbdt']
    MCfriends = [trees+'1_recl_allvars',trees+'2_btag_SFs',trees+'2_scalefactors_lep_fixed',trees+'0_jmeUnc_v1']
    Datafriends=[trees+'1_recl']
    targetdir = '/eos/user/a/anmehta/www/DPSWW_v2/{date}{pf}_era{year}_3lCR/'.format(date=date, year=year,pf=('-'+postfix if postfix else '') ) 
    fplots = 'dps-ww/fullRun2/plots.txt'
    fmca = 'dps-ww/fullRun2/mca-3lCR.txt'
    fsyst  = 'dps-ww/fullRun2//systsUnc.txt' #dps-ww/fullRun2/syst.txt'
    fcut   = 'dps-ww/fullRun2/cuts_3l.txt'
    processes=['DPSWW','WZ','data','ZZ','Rares']#,'WZ','ZZ','data','Rares']#'WG_wg',
    enable    = []
    disable   = []
    fittodata = []#'WZ','ZZ']#'ZZ','WZ','Convs','Rares']#'WG_wg',
    scalethem = {}
    ratio   = ' --fixRatioRange  --ratioYNDiv 505 --maxRatioRange 0.0  1.99'
    spam    = ' --topSpamSize 1.0 --noCms '
    legends = ' --legendFontSize 0.04 --legendBorder 0 --legendWidth  0.62 --legendColumns 3 '
    ubands  = ' --showMCError '
    anything = " --fitData --flp WZ --sP tot_weight " #scaleBkgToData--preFitData tot_weight --flp WZ --sP tot_weight --sp WZ " # --fitData  --flp WZ  "# --neglist '.*_promptsub.*' --plotgroup data_fakes+=.*_promptsub" # --preFitData tot_weight --plotmode norm" #to include neagitve evt ylds from fakes 
    extraopts = ratio + spam + legends + ubands + anything
    makeplots=['tot_weight','BDT_wz_3l','BDT_fakes_3l','met_3l','conept1_3l','conept2_3l','conept3_3l','pt1_3l','pt2_3l','pt3_3l']
    runplots(trees, friends, MCfriends, Datafriends, targetdir, fmca, fcut, fsyst, fplots, enable, disable, processes, scalethem, fittodata,makeplots,True, year, 3,extraopts)

def fourlepCRPlot(year):
    print '=========================================='
    print 'running 4l control region  plots'
    print '=========================================='
    trees='/eos/cms/store/cmst3/group/dpsww/NanoTrees_TTH_090120_091019_v6_skim2lss/{year}/'.format(year=year)
    friends=[trees+'3_tauCount',trees+'dpsbdt']
    MCfriends = [trees+'1_recl_allvars',trees+'2_btag_SFs',trees+'2_scalefactors_lep_fixed',trees+'0_jmeUnc_v1']
    Datafriends=[trees+'1_recl']
    targetdir = '/eos/user/a/anmehta/www/DPSWW_v2/{date}{pf}_era{year}_4lCR/'.format(date=date, year=year,pf=('-'+postfix if postfix else '') ) 
    fplots = 'dps-ww/fullRun2/plots.txt'
    fmca = 'dps-ww/fullRun2/mca-dpsww.txt'
    fsyst  = 'dps-ww/fullRun2//systsUnc.txt' #dps-ww/fullRun2/syst.txt'
    fcut   = 'dps-ww/fullRun2/cuts_4l.txt'
    processes=['ZZ','data']
    enable    = []
    disable   = []
    fittodata = ['ZZ']
    scalethem = {}
    ratio   = ' --fixRatioRange  --ratioYNDiv 505 --maxRatioRange 0.0  1.99'
    spam    = ' --topSpamSize 1.0 --noCms '
    legends = ' --legendFontSize 0.04 --legendBorder 0 --legendWidth  0.62 --legendColumns 3 '
    ubands  = ' --showMCError '
    anything = " --s2v --neglist '.*_promptsub.*' --plotgroup data_fakes+=.*_promptsub" # --plotmode norm" #to include neagitve evt ylds from fakes 
    extraopts = ratio + spam + legends + ubands + anything
    makeplots=['BDT_wz_4l','BDT_fakes_4l','conept1_4l','conept2_4l','conept3_4l','conept4_4l','pt1_4l','pt2_4l','pt3_4l','pt4_4l']
    runplots(trees, friends, MCfriends, Datafriends, targetdir, fmca, fcut, fsyst, fplots, enable, disable, processes, scalethem, fittodata,makeplots,True, year, 4,extraopts)

if __name__ == '__main__':
    parser = optparse.OptionParser(usage='usage: %prog [opts] ', version='%prog 1.0')
    parser.add_option('--pf', '--postfix', dest='postfix' , type='string', default='', help='postfix for running each module')
    parser.add_option('-d', '--date', dest='date' , type='string', default='', help='run with specified date instead of today')
    #    parser.add_option('-l', '--lumi', dest='lumi' , type='float'  , default=1.    , help='change lumi by hand')
    parser.add_option('--threelepCR',dest='threelepCR', action='store_true', default=False , help='make plots in 3lep CR')
    parser.add_option('--fourlepCR',dest='fourlepCR', action='store_true' , default=False , help='make plots in 4lep CR')
    parser.add_option('--finalState',dest='finalState',type='string' , default=[], action="append", help='final state(s) to run on')
    parser.add_option('--splitCharge',dest='splitCharge',action='store_true', default=False , help='split by charge')
    parser.add_option('--year',   dest='year'  , type='string' , default='2016' , help='make plots for specified year')
    parser.add_option('--results' , '--makeResults'  , dest='results', action='store_true' , default=True , help='make plots')
    #    parser.add_option('--rC' , '--runCards'  , dest='runCards', action='store_true' , default=False , help='make plots')
    parser.add_option('--dW' , '--doWhat'  , dest='doWhat', type='string' , default=[] , help='make plots')

    (opts, args) = parser.parse_args()

    global date, postfix, date
    postfix = opts.postfix
    year= opts.year
    date = datetime.date.today().isoformat()

    if opts.date:
        date = opts.date

    if opts.threelepCR:
        threelepCRPlot(opts.year)
    if opts.fourlepCR:
        fourlepCRPlot(opts.year)
    if opts.results:
        print 'running plots for 2lss'
        makeResults(opts.year,opts.finalState,opts.splitCharge,opts.doWhat)

