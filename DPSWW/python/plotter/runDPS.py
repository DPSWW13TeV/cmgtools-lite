#!/usr/bin/env python
import optparse, subprocess, ROOT, datetime, math, array, copy, os, re, sys
import numpy as np
lumis = {
    '2016': '35.9',
    '2017': '41.4',
    '2018': '59.7',
    'all' : '35.9,41.4,59.7',
}


def simpleMCplots(trees,MCfriends,Datafriends,targetdir, fmca, fcut,fplots, enabledcuts, disabledcuts, processes,plotlist,extraopts = '',bareNano=False):

    if bareNano:
        cmd  = ' mcPlots.py -j 10 -l 35.9 --tree NanoAOD --year 2016  --pdir {td} {fmca} {fcut} {fplots} --split-factor=-1  -P {trees} '.format(td=targetdir, trees=trees, fmca=fmca, fcut=fcut, fplots=fplots)

    else:
        cmd  = ' mcPlots.py -f -j 10 -l 35.9 --tree NanoAOD --year 2016  --pdir {td} {fmca} {fcut} {fplots} --mcc dps-ww/fullRun2/lepchoice-ttH-FO.txt --WA prescaleFromSkim --mcc dps-ww/fullRun2/mcc-METFixEE2017.txt --split-factor=-1  -P {trees} '.format(td=targetdir, trees=trees, fmca=fmca, fcut=fcut, fplots=fplots)
        #        cmd += ''.join(' -W L1PreFiringWeight_Nom*puWeight')

    cmd += ''.join(' --FMCs '+frnd for frnd in MCfriends)
    cmd += ''.join(' --FDs '+frnd for frnd in Datafriends)
    cmd += ''.join(' -E ^'+cut for cut in enabledcuts )
    cmd += ''.join(' -X ^'+cut for cut in disabledcuts)

    cmd += ' --sP '+','.join(plot for plot in plotlist)
    cmd += ' -p '+','.join(processes)
    

    cmd += ' -o '+targetdir+'/'+'_AND_'.join(plot for plot in plotlist)+'.root'
    if extraopts:
        cmd += ' '+extraopts

    print 'running: python', cmd
    subprocess.call(['python']+cmd.split())#+['/dev/null'],stderr=subprocess.PIPE)




def runCards(trees, friends, MCfriends, Datafriends, targetdir, fmca, fcut, fsyst, plotbin, enabledcuts, disabledcuts, processes, scaleprocesses,applyWtsnSFs, year,extraopts = '',invertedcuts = []):
    varToFit= '{plotvar} {binning}'.format(plotvar=plotbin.split()[0], binning=plotbin.split()[1])
    cmd  = ' makeShapeCardsNew.py -f -j 8 -l {lumi} --od {CARDSOUTDIR} --tree NanoAOD --year {YEAR} --mcc dps-ww/fullRun2/lepchoice-ttH-FO.txt --WA prescaleFromSkim --mcc dps-ww/fullRun2/mcc-METFixEE2017.txt {fmca} {fcut} --amc --threshold 0.01 --neg --split-factor=-1 --unc {fsyst} -P {trees} {varName} '.format(lumi=lumis[year],CARDSOUTDIR=targetdir, trees=trees, fmca=fmca, fcut=fcut,YEAR=year,fsyst=fsyst,varName=varToFit) #--asimov signal 

    #    BDT_DPS_WZ 20,0,1.0
    cmd += ''.join(' --Fs '+frnd for frnd in friends)
    cmd += ''.join(' --FMCs '+frnd for frnd in MCfriends)
    cmd += ''.join(' --FDs '+frnd for frnd in Datafriends)

    cmd += ''.join(' -E ^'+cut for cut in enabledcuts )
    cmd += ''.join(' -X ^'+cut for cut in disabledcuts)
    #cmd += ' '.join(["--plotgroup data_fakes%s+='.*_promptsub%s'"%(x,x) for x in processes])+" --neglist '.*_promptsub.*' "
    cmd += ' -p '+','.join(processes)
    if invertedcuts:
        cmd += ''.join(' -I ^'+cut for cut in invertedcuts )
    if applyWtsnSFs:
        cmd += ''.join(' -W L1PreFiringWeight_Nom*puWeight*leptonSF_2lss* triggerSF_ttH(LepGood_pdgId[iLepFO_Recl[0]], LepGood_conePt[iLepFO_Recl[0]], LepGood_pdgId[iLepFO_Recl[1]], LepGood_conePt[iLepFO_Recl[1]],year)')

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

def runPlots(trees, friends, MCfriends, Datafriends, targetdir, fmca, fcut, fsyst, fplots, enabledcuts, disabledcuts, processes, scaleprocesses, fitdataprocess, plotlist, showratio, applyWtsnSFs, year,nLep,extraopts = '', invertedcuts = [],cutflow=False):


    #if not type(trees)==list: trees = [trees]
    #treestring = ' '.join(' -P '+ t for t in list(trees))

    if(nLep == 1):
        cmd  = ' mcPlots.py -f -j 10 -l {lumi} --tree NanoAOD --year {YEAR} --pdir {td} {fmca} {fcut} {fplots} --split-factor=-1 -P {trees} --mcc fakeRates/mcc-eleIdEmu2.txt -L fakeRates/lepton-fr/frPuReweight.cc '.format(lumi=lumis[year],td=targetdir, trees=trees, fmca=fmca, fcut=fcut, fplots=fplots,YEAR=year)
    else:
        #cmd  = " mcPlots.py -f -j 10 -l {lumi} --tree NanoAOD --year {YEAR} --mcc dps-ww/fullRun2/lepchoice-ttH-FO.txt --WA prescaleFromSkim --mcc dps-ww/fullRun2/mcc-METFixEE2017.txt --pdir {td} {fmca} {fcut} {fplots}   -P {trees}   --neglist '.*_promptsub.*' --plotgroup data_fakes+=.*_promptsub.* ".format(lumi=lumis[year],td=targetdir, trees=trees, fmca=fmca, fcut=fcut, fplots=fplots,YEAR=year)
        if (cutflow):
            cmd  = ' mcPlots.py -j 10 -l {lumi} --tree NanoAOD --year {YEAR} --mcc dps-ww/fullRun2/lepchoice-ttH-FO.txt --WA prescaleFromSkim --mcc dps-ww/fullRun2/mcc-METFixEE2017.txt --pdir {td} {fmca} {fcut} {fplots} --split-factor=-1  -P {trees} '.format(lumi=lumis[year],td=targetdir, trees=trees, fmca=fmca, fcut=fcut, fplots=fplots,YEAR=year)
        else:
            cmd  = ' mcPlots.py -f -j 10 -l {lumi} --tree NanoAOD --year {YEAR} --mcc dps-ww/fullRun2/lepchoice-ttH-FO.txt --WA prescaleFromSkim --mcc dps-ww/fullRun2/mcc-METFixEE2017.txt --pdir {td} {fmca} {fcut} {fplots} --split-factor=-1  -P {trees}  '.format(lumi=lumis[year],td=targetdir, trees=trees, fmca=fmca, fcut=fcut, fplots=fplots,YEAR=year)


    if len(fsyst) > 0:
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

    if applyWtsnSFs :
        if(nLep == 2): 
            cmd += ''.join(' -W L1PreFiringWeight_Nom*puWeight*leptonSF_2lss *triggerSF_ttH(LepGood_pdgId[iLepFO_Recl[0]], LepGood_conePt[iLepFO_Recl[0]], LepGood_pdgId[iLepFO_Recl[1]], LepGood_conePt[iLepFO_Recl[1]],2,year)')
        elif(nLep == 3):
            cmd += ' -W L1PreFiringWeight_Nom*puWeight*leptonSF_3l *triggerSF_ttH(LepGood_pdgId[iLepFO_Recl[0]], LepGood_conePt[iLepFO_Recl[0]], LepGood_pdgId[iLepFO_Recl[1]], LepGood_conePt[iLepFO_Recl[1]],3,year)'
        elif(nLep == 4):
            cmd += ' -W L1PreFiringWeight_Nom*puWeight*leptonSF_4l *triggerSF_ttH(LepGood_pdgId[iLepFO_Recl[0]], LepGood_conePt[iLepFO_Recl[0]], LepGood_pdgId[iLepFO_Recl[1]], LepGood_conePt[iLepFO_Recl[1]],3,year)'
        else:
            if(nLep == 2): 
                cmd += ''.join(' -W L1PreFiringWeight_Nom*puWeight')
            elif(nLep == 3):
                cmd += ' -W L1PreFiringWeight_Nom*puWeight'
            elif(nLep == 4):
                cmd += ' -W L1PreFiringWeight_Nom*puWeight'

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


def makeResults(year,finalState,splitCharge,doWhat,analysis):
    #trees       = '/eos/cms/store/cmst3/group/dpsww/{samples}/{year}/'.format(year=year,samples = 'NanoTrees_v7_dpsww_04092020' if analysis == 'dps' and year == '2016' else 'NanoTrees_TTH_090120_091019_v6_skim2lss')
    trees       = '/eos/cms/store/cmst3/group/dpsww/{samples}/{year}/'.format(year=year,samples = 'NanoTrees_v7_dpsww_04092020_skim2lss_mvawp_mupt90_elpt70_2021' if analysis == 'dps'  else 'NanoTrees_TTH_090120_091019_v6_skim2lss')

    friends     = [trees+'3_tauCount']#, trees+'dpsbdt']
    MCfriends   = [trees+'2_recl_allvars',trees+'3_scalefactors_EOY',trees+'0_jmeUnc_v1']#,trees+'2_scalefactors_lep_fixed']#
    Datafriends = [trees+'2_recl']
    fplots      = 'dps-ww/fullRun2/plots.txt'
    fmca        = 'dps-ww/fullRun2/mca-dpsww.txt'
    fsyst       = '' #dps-ww/fullRun2/systsUnc.txt'
    fcut        = 'dps-ww/fullRun2/cuts_2lss.txt' 

    applyWtsnSFs = True
    cutflow=False
    targetdir   = '/eos/user/a/anmehta/www/DPSWW_v2/{date}{pf}_era{year}{anal}cuts_{here}SFs/'.format(date=date, year=year,pf=('-'+postfix if postfix else '') ,here='with' if applyWtsnSFs else 'without', anal=analysis ) 
    if splitCharge: 
        loop = [ 'minusminus', 'plusplus']
    else:
        loop = [ '' ]

    print 'running for %s with charge split flag %s' %(finalState,splitCharge)


    processes = ['DPSWW','Rares','WZ_amc','ZZ','Convs01J','WZ_mllLT4','data_flips','data','data_fakes']#,'DPSWW_hg','WZ_pow']#,'dy','Flips','Convs','Wgstar','WZ_incl','promptsub']
    #processes =['data_fakes','Convs','Convs01J']
    #fRvars    = ['data_fakes_FRe_norm_Up','data_fakes_FRe_norm_Dn','data_fakes_FRe_pt_Up','data_fakes_FRe_pt_Dn','data_fakes_FRe_be_Up','data_fakes_FRe_be_Dn','data_fakes_FRm_norm_Up','data_fakes_FRm_norm_Dn','data_fakes_FRm_pt_Up','data_fakes_FRm_pt_Dn','data_fakes_FRm_be_Up','data_fakes_FRm_be_Dn']
    #processes+=fRvars

    if finalState[0] in ['mumu','elel']:
        binningBDT   = ' unroll_2Dbdt_dps_mumu(BDT_DPS_fakes,BDT_DPS_WZ_amc) 15,0.0,15.0'
    else:
        binningBDT   = ' unroll_2Dbdt_dps_elmu(BDT_DPS_fakes,BDT_DPS_WZ_amc) 15,0.0,15.0'

    exotic = ['ptRatio1','ptRatio2']#,'MVA_ptRatio','dxy1','dz1','sip3d1','dxy2','dz2','sip3d2','minMVA','maxMVA','LepGood1_motherid','LepGood2_motherid','fake_lepMVA1','fake_lepMVA2', LepGood1_genPartFlav_all','LepGood2_genPartFlav_all',LepGood1_tightId','LepGood2_tightId','LepGood1_cutBased','LepGood2_cutBased','LepGood1_mediumPromptId','LepGood1_mediumId','LepGood1_mvaFall17V2Iso','LepGood1_mvaFall17V2Iso_WPL','LepGood1_mvaId','LepGood2_mediumPromptId','LepGood2_mediumId','LepGood2_mvaFall17V2Iso','LepGood2_mvaFall17V2Iso_WPL','njets25','njets30','nBJetLoose25','nBJetMedium25','nBJetTight25','nBJetLoose40','nBJetMedium40','nBJetTight40','nTauTight','nTauFO'] 

    allvars    = ['conept1','conept2','MVA1','MVA2']#'pt1','pt2','eta1','eta2','phi1','phi2','MVA1','MVA2','met','metphi']#,'dilep_flav','tcharge1','tcharge2','njets25','mll','mt2ll','mt1','mtll','etasum','etaprod','dphill','dphil2met','dphilll2','nVert','ptll'] #'BDT_wz_amc','BDT_fakes','BDT_wz_pow','BDT_DPS_multiC','BDT_WZ_multiC','BDT_TL_multiC']'dilep_charge','puppimetphi','puppimet'
    #'conept1_WZ_sep1','conept2_WZ_sep1'

    #    configs=['elmu','mumu','elel','plusplus','minusminus']

    plotvars   = allvars #allvars #exotic 

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
            ratio   = ' --fixRatioRange  --ratioYNDiv 505 --maxRatioRange 0.45  1.69' # --ratioDen DPSWW --ratioNums DPSWW_hg --ratioYLabel=hw/py8'
            spam    = ' --topSpamSize 1.0 --noCms '
            legends = ' --legendFontSize 0.04 --legendBorder 0 --legendWidth  0.62 --legendColumns 3 '
            ubands  = '  --showMCError '
            anything = '--binname {finalState}'.format(finalState=FS) # --fitData --flp data_fakes'# --plotmode norm' # --plotmode nostack' # rm --neg ' #--plotmode norm ' #"  --neglist '.*_promptsub.*' --plotgroup data_fakes+=.*_promptsub.* " #-- uf" #" #to include neagitve evt ylds from fakes --showIndivSigs --noStackSig --plotmode nostack
            extraopts = ratio + spam + legends + ubands + anything

            if splitCharge:
                makeplots1  = ['{}_{}{}'.format(a,FS,ch)  for a in plotvars]
            else:
                makeplots1  = ['{}_{}'.format(a,FS) for a in plotvars]
            
            if 'plots' in doWhat:
                makeplots=makeplots1 #+makeplots2
                print makeplots1
                runPlots(trees, friends, MCfriends, Datafriends, targetdir, fmca, fcut, fsyst, fplots, enable, disable, processes, scalethem, fittodata,makeplots,True, applyWtsnSFs, year, 2,extraopts,invert,cutflow)

            if 'cards' in doWhat:
            ## ==================================
            ## running datacards
            ## ==================================
                #print processes
                targetcarddir = 'Cards/cards_{date}{pf}_{FS}_era{year}'.format(FS=FS,year=year,date=date, pf=('-'+postfix if postfix else '') )
                extraoptscards = ' ' #--binname {FS}{ch}'.format(year=year,FS=FS,ch=(ch if ch else ''))
                runCards(trees, friends, MCfriends, Datafriends, targetcarddir, fmca, fcut, fsyst , binningBDT, enable, disable, processes, scalethem,applyWtsnSFs, year,extraoptscards,invert)
########################################
def makeResultsGen(year,finalState,splitCharge,postFSR):
    trees       = '/eos/cms/store/cmst3/group/dpsww/signal_summer16_nanoV7/'
    MCfriends   = [trees+'postFSRinfo/']
    targetdir   = '/eos/user/a/anmehta/www/DPSWW_v2/GeneratorLevel/{date}{pf}_era{year}_{here}lep/'.format(date=date, here= 'gen' if postFSR else 'dressed', year=year,pf=('-'+postfix if postfix else ''))
    #targetdir   = '/eos/user/a/anmehta/www/DPSWW_v2/bareNano/{date}{pf}_era{year}/'.format(date=date, year=year,pf=('-'+postfix if postfix else ''))
    fplots      = 'dps-ww/fullRun2/plots.txt'
    fmca        = 'dps-ww/fullRun2/mca-dpsww-gen.txt' 
    fsyst       = ''
    fcut        = 'dps-ww/fullRun2/cuts_2lss_dpsww_gen.txt' #dps-ww/fullRun2/cuts_2lss_dpsww_basic.txt' #dps-ww/fullRun2/cuts_2lss_dpsww_dressed.txt'
    bareNano    = True

    if splitCharge: 
        loop = [ 'minusminus', 'plusplus']
    else:
        loop = [ '' ]

    print 'running for %s with charge split flag %s' %(finalState,splitCharge)
    processes = ['DPSpy8','DPShwpp']#,WZ_pow','WZ_incl','Wgstar','WZ_amc','WZ_mllLT4']#,'WZ_mllLT4']'WgStarLNuEE','WgStarLNuMuMu'
    allvars=['Electron_mvaTTH','Muon_mvaTTH']#pt_dressedLep','eta_dressedLep','pdgId_dressedLep']#'pdgIdprod_dressedLep','GenMET_pt','eta1_dressedLep','eta2_dressedLep','pt1_dressedLep','pt2_dressedLep','ndressedLep','dilep_flav_dressedLep','mll_v1_dressedLep','mll_dressedLep','mll_zoomed_dressedLep']#
    genvars=['pt1_GenLep','pt2_GenLep','eta1_GenLep','eta2_GenLep','mll_zoomed_GenLep','mll_GenLep','nGenlep','pdgIdprod_GenLep'] 
 
    plotvars   =  genvars #+allvars 

    for FS in finalState:            
        for ch in loop:
            enable=[]
            enable.append(FS); 
            if len(ch)>0 : 
                enable.append(ch)
            print enable #list(ch) + list (finalState)
            disable   = []
            ratio   = ' --fixRatioRange  --ratioYNDiv 505 --maxRatioRange 0.5  1.39'
            spam    = ' --topSpamSize 1.0 --noCms '
            legends = ' --legendFontSize 0.04 --legendBorder 0 --legendWidth  0.62 --legendColumns 2 '
            anything = ' --plotmode norm --showRatio --ratioDen DPSpy8 --ratioNums DPShwpp --ratioYLabel=hwpp/py8' # --plotmode norm' # --plotmode nostack' # rm --neg ' #--plotmode norm ' 
            extraopts = ratio + spam + legends +  anything
               
            
            if splitCharge:
                makeplots1  = ['{}_{}{}'.format(a,FS,ch)  for a in plotvars]
            else:
                makeplots1  = ['{}_{}'.format(a,FS) for a in plotvars]
            

            makeplots=makeplots1 
            print makeplots1
            simpleMCplots(trees,MCfriends,'',targetdir, fmca, fcut,fplots, enable, disable, processes,makeplots,extraopts,bareNano)


#%%%%%%%%%
def makeResults_oldMaps(year,finalState,splitCharge):
    trees       = '/eos/cms/store/cmst3/group/dpsww/NanoTrees_TTH_090120_091019_v6_skim2lss/{year}/'.format(year=year)
    friends     = [trees+'3_tauCount']#,trees+'dpsbdt']
    MCfriends   = [trees+'1_recl_allvars',trees+'2_btag_SFs',trees+'2_scalefactors_lep_fixed',trees+'0_jmeUnc_v1']
    Datafriends = [trees+'1_recl']
    targetdir   = '/eos/user/a/anmehta/www/DPSWW_v2/{date}{pf}_era{year}_witholdFRMaps/'.format(date=date, year=year,pf=('-'+postfix if postfix else '') ) 
    fplots      = 'dps-ww/fullRun2/plots.txt'
    fmca        = 'dps-ww/fullRun2/mca-dpsww_oldFRMaps.txt'
    fsyst       = '' 
    fcut        = 'dps-ww/fullRun2/cuts_2lss_oldFRMaps.txt'

    applyWtsnSFs = True

    if splitCharge: 
        loop = [ 'minusminus', 'plusplus']
    else:
        loop = [ '' ]

    print 'running for %s with charge split flag %s' %(finalState,splitCharge)

    processes = ['DPSWW','Rares','Convs','ZZ','WZ','data_flips','data_fakes','data']#,'promptsub']#



    allvars    = ['pt1','pt2','eta1','eta2','phi1','phi2','MVA1','MVA2','tcharge1','tcharge2','charge1','charge2','pdgId1','pdgId2','dilep_charge','dilep_flav','met','metphi','njets','mll','mt2ll','mt1','mtll','etasum','etaprod','dphill','dphil2met','dphilll2']#,'nVert','BDT_wz','BDT_fakes','BDT1d']        
    

    plotvars   = allvars 

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
            ubands  = '' # --showMCError '
            anything = ' ' #--plotmode norm' #--plotmode norm --neg ' #--plotmode norm ' #"  --neglist '.*_promptsub.*' --plotgroup data_fakes+=.*_promptsub.* " #-- uf" #" #to include neagitve evt ylds from fakes
            extraopts = ratio + spam + legends + ubands + anything
               

            if splitCharge:
                makeplots1  = ['{}_{}{}'.format(a,FS,ch)  for a in plotvars]
            else:
                makeplots1  = ['{}_{}'.format(a,FS) for a in plotvars]
            
    
            makeplots=makeplots1 #+makeplots2
            print makeplots1
            runPlots(trees, friends, MCfriends, Datafriends, targetdir, fmca, fcut, fsyst, fplots, enable, disable, processes, scalethem, fittodata,makeplots,False, applyWtsnSFs,year, 2,extraopts,invert)


########################################



def threelepCRPlot(year,threesome):
    print '=========================================='
    print 'running 3l control region  plots with {here}shell Z'.format(here='on' if threesome =='WZ' else 'off')
    print '=========================================='
    trees       = '/eos/cms/store/cmst3/group/dpsww/NanoTrees_v7_dpsww_04092020_skim2lss_mvawp_mupt90_elpt70_latest/{year}/'.format(year=year)
    friends     = [trees+'3_tauCount']#, trees+'dpsbdt']
    MCfriends   = [trees+'2_recl_allvars',trees+'0_jmeUnc_v1',trees+'2_scalefactors_lep_fixed'] #,trees+'2_btag_SFs
    Datafriends =  [trees+'2_recl']
    targetdir = '/eos/user/a/anmehta/www/DPSWW_v2/{date}{pf}_era{year}_{here}CR/'.format(date=date, here='WZ' if threesome =='WZ' else 'WGstar',year=year,pf=('-'+postfix if postfix else '') ) 
    fplots = 'dps-ww/fullRun2/plots.txt'
    fmca =   'dps-ww/fullRun2/mca-dpsww.txt'
    fsyst  = '' #dps-ww/fullRun2/systsUnc.txt'
    fcut   = 'dps-ww/fullRun2/cuts_3l.txt'
    processes = ['DPSWW','Rares','WZ_incl','WZ_mllLT4','data','ZZ','Convs']#,'WZ_pow','DPSWW_hg'] #'WZ_mllLT4'
    if threesome == "WZ":
        enable    = ['pt251515','zsel','met_wz','exclusive','cleanup','tauveto']
    else:
        enable    = ['pt301010','met_wg','emm','gstartomm','jpsiveto']#,'mlllt4']
    disable   = []
    fittodata = []#'WZ','ZZ']#'ZZ','WZ','Convs','Rares']#'WG_wg',
    scalethem = {}
    ratio   = ' --fixRatioRange  --ratioYNDiv 505 --maxRatioRange 0.0  1.99'
    spam    = ' --topSpamSize 1.0 --noCms '
    legends = ' --legendFontSize 0.04 --legendBorder 0 --legendWidth  0.62 --legendColumns 3 '
    ubands  = ' --showMCError '
    anything = " " #--fitData --flp WZ --sP tot_weight  " #scaleBkgToData--preFitData tot_weight --flp WZ --sP tot_weight --sp WZ " # --fitData  --flp WZ  "# --neglist '.*_promptsub.*' --plotgroup data_fakes+=.*_promptsub" # --preFitData tot_weight --plotmode norm" #to include neagitve evt ylds from fakes 
    extraopts = ratio + spam + legends + ubands + anything
    makeplots=['mll_3l','met_3l','conept1_3l','conept2_3l','conept3_3l','pt1_3l','pt2_3l','pt3_3l','mll_3l']
    if 'WGstar_excl' in processes:
        makeplots=[i+'_WGstar_excl' for i in makeplots]
        #'tot_weight','BDT_wz_3l','BDT_fakes_3l',
    runPlots(trees, friends, MCfriends, Datafriends, targetdir, fmca, fcut, fsyst, fplots, enable, disable, processes, scalethem, fittodata,makeplots,True, True,year, 3,extraopts)

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
    anything = " --neglist '.*_promptsub.*' --plotgroup data_fakes+=.*_promptsub" # --plotmode norm" #to include neagitve evt ylds from fakes 
    extraopts = ratio + spam + legends + ubands + anything
    makeplots=['BDT_wz_4l','BDT_fakes_4l','conept1_4l','conept2_4l','conept3_4l','conept4_4l','pt1_4l','pt2_4l','pt3_4l','pt4_4l']
    runPlots(trees, friends, MCfriends, Datafriends, targetdir, fmca, fcut, fsyst, fplots, enable, disable, processes, scalethem, fittodata,makeplots,True, True,year, 4,extraopts)

def onelepCRPlot(year,finalState):
    print '=========================================='
    print 'running single lepton control region  plots'
    print '=========================================='
    trees='/eos/cms/store/cmst3/group/tthlep/gpetrucc/TREES_ttH_FR_nano_v5/{year}/skim_z3/'.format(year=year)
    friends=[trees+'1_frFriends_v1']
    MCfriends = ''
    Datafriends=''
    fplots = 'fakeRates/lepton-fr/qcd1l_plots.txt'
    fmca = 'fakeRates/lepton-fr/mca-qcd1l-{year}.txt'.format(year=year)
    fsyst  = '' 
    fcut   = 'fakeRates/lepton-fr/qcd1l.txt'
    disable   = []
    fittodata = []
    scalethem = {}
    ratio   = ' --fixRatioRange  --ratioYNDiv 505 --maxRatioRange 0.0  1.99'
    spam    = ' --topSpamSize 1.0 --noCms '
    legends = ' --legendFontSize 0.04 --legendBorder 0 --legendWidth  0.62 --legendColumns 3 '
    ubands  = ' --plotmode nostack' #--showMCError '

    for FS in finalState:
        if FS == 'mu':
            processes=['WJets','DYJets','Top','data','QCDMu_red']
            enable=['conepTmu','muCR','2016_trigMu' if year == '2016' else 'trigMu']
            anything= " --xf 'SingleEl.*,DoubleEG.*,EGamma.*'"
            #anything+= " -W coneptwMuX_OR_2016(LepGood_pt,LepGood_mvaTTH,LepGood_mediumId,LepGood_jetRelIso,PV_npvsGood) '"
            targetdir = '/eos/user/a/anmehta/www/DPSWW_v2/Fakes/{date}{pf}_era{year}_1muCR/'.format(date=date,year=year,pf=('-'+postfix if postfix else '') ) 
        if FS == 'el':
            processes=['WJets','DYJets','Top','data','QCDEl_red']
            enable=['trigEl','conepTel','elCR']
            targetdir = '/eos/user/a/anmehta/www/DPSWW_v2/Fakes/{date}{pf}_era{year}_1elCR/'.format(date=date,year=year,pf=('-'+postfix if postfix else '') ) 
            anything= " --xf 'DoubleMu.*,SingleMu.*' "
            anything+= " -W coneptwEleX_OR_2016(LepGood_pt,LepGood_mvaTTH,LepGood_jetRelIso,PV_npvsGood)"
    

        extraopts = ratio + spam + legends + ubands + anything
        makeplots=['mvaTTH']#'pt','conePt','miniRelIso','mvaTTH','awayJet_pt','met','nvtx','mtW1','mtW1R']
        runPlots(trees, friends, MCfriends, Datafriends, targetdir, fmca, fcut, fsyst, fplots, enable, disable, processes, scalethem, fittodata,makeplots,True, True,year, 1,extraopts)

def fakesClosure(year,finalState):
    print '=========================================='
    print 'running closure test on fakes' 
    print '=========================================='
    trees       = '/eos/cms/store/cmst3/group/dpsww/{samples}/{year}/'.format(year=year,samples = 'NanoTrees_v7_dpsww_04092020_skim2lss_mvawp_mupt90_elpt70_2021')

    friends     = [trees+'3_tauCount']#, trees+'dpsbdt']
    MCfriends   = [trees+'2_recl_allvars',trees+'3_scalefactors_EOY',trees+'0_jmeUnc_v1']#,trees+'2_scalefactors_lep_fixed']#
    Datafriends = [trees+'2_recl']
    applySFs=False
    targetdir = '/eos/user/a/anmehta/www/DPSWW_v2/{date}{pf}_era{year}_fakesClosure/'.format(date=date,year=year,pf=('-'+postfix if postfix else '') )
    cutflow=False
    fplots = 'dps-ww/fullRun2/plots.txt'
    fmca =   'dps-ww/fullRun2/mca-fakes-closure.txt'
    fsyst  = '' #dps-ww/fullRun2/systsUnc.txt'
    fcut   = 'dps-ww/fullRun2/cuts_2lss.txt'
    processes = ['wj','wj_tl','wjinc','wjinc_tl']
    disable   = []
    fittodata = []
    scalethem = {}
    ratio   = ' --fixRatioRange  --ratioYNDiv 505 --maxRatioRange 0.0  2.5'
    spam    = ' --topSpamSize 1.0 --noCms '
    legends = ' --legendFontSize 0.04 --legendBorder 0 --legendWidth  0.62 --legendColumns 3 '
    ubands  = '' # --showMCError '
    anything = " --plotmode nostack --showRatio --ratioDen wj --ratioNums wj_tl --ratioYLabel=wj_tl/wj" 
    extraopts = ratio + spam + legends + ubands + anything
    plots    = ['njets25']#MVA1','MVA2','pt1','pt2','eta1','eta2','met','conept1','conept2']#'BDT_wz_amc','BDT_fakes','BDT_wz_pow','BDT_DPS_multiC','BDT_WZ_multiC','BDT_TL_multiC']
    for FS in finalState:
        enable=['noConvs']
        enable.append(FS); 
        makeplots=[ip + '_' + FS for ip in plots]
        runPlots(trees, friends, MCfriends, Datafriends, targetdir, fmca, fcut, fsyst, fplots, enable, disable, processes, scalethem, fittodata,makeplots,True,applySFs,year, 2,extraopts,[],cutflow)

def dpsww(finalState):
    print '=========================================='
    print 'running single lepton control region  plots'
    print '=========================================='
    trees       = '/eos/cms/store/cmst3/group/dpsww/{samples}/{year}/'.format(year='2016',samples = 'NanoTrees_v7_dpsww_04092020')
    MCfriends   = [trees+'2_recl'] 
    Datafriends = [trees+'2_recl']
    targetdir   = '/eos/user/a/anmehta/www/DPSWW_v2/{date}{pf}_era{year}unskimmed/'.format(date=date, year='2016',pf=('-'+postfix if postfix else ''))
    fplots      = 'dps-ww/fullRun2/plots.txt'
    fmca        = 'dps-ww/fullRun2/mca-dpsww.txt'
    fcut        = 'dps-ww/fullRun2/cuts_2lss_dpsww_2016.txt'
    disable   = []
##am    trees='/eos/cms/store/cmst3/group/dpsww/Lepton_id_study/'
##am    MCfriends=[trees+'coll_merged/']
##am    targetdir = '/eos/user/a/anmehta/www/DPSWW_v2/{date}{pf}/'.format(date=date,pf=('-'+postfix if postfix else '') ) 
##am    fplots = 'dps-ww/fullRun2/simple_plots.txt'
##am    fmca = 'dps-ww/fullRun2/mca-dpsww.txt' #simple_mca.txt'
##am    fsyst  = '' 
##am    fcut   = 'dps-ww/fullRun2/simple_cuts.txt'
##am    processes=['DPSWW']
    processes = ['DPSWW','DYLO','Diboson','data','TTdilep','SingleTop','WJets']#,'TTsemilep']#,'data_fakes']
    #enable=[]
    ratio   = ' --fixRatioRange  --ratioYNDiv 505 --maxRatioRange 0.0  1.99'
    spam    = ' --topSpamSize 1.0 --noCms '
    legends = ' --legendFontSize 0.04 --legendBorder 0 --legendWidth  0.62 --legendColumns 3 '
    ubands  = ' '# --plotmode norm' 
    anything =''
    extraopts = ratio + spam + legends + ubands + anything
    plots=['mvaTTH1','mvaTTH2','met','pt1','pt2','minMVA','maxMVA']
    
    for FS in finalState:
        enable=[]
        enable.append(FS); 
        makeplots=[ip + '_' + FS for ip in plots]
        simpleMCplots(trees,MCfriends,Datafriends,targetdir, fmca, fcut,fplots, enable, disable, processes,makeplots,extraopts)



def dyCRPlot(year,finalState):
    print '=========================================='
    print 'running dy control region  plots' 
    print '=========================================='
    trees       = '/eos/cms/store/cmst3/group/dpsww/NanoTrees_v7_dpsww_04092020/{year}/'.format(year=year)
    friends     = [trees+'2_recl']#, trees+'dpsbdt']
    MCfriends   = [trees+'3_scalefactors_lep_fixed_EOY']#3_scalefactors_lep_fixed']#',trees+'0_jmeUnc_v1',trees+'2_scalefactors_lep_fixed'] #,trees+'2_btag_SFs
    Datafriends =  ''
    applySFs=False
    targetdir = '/eos/user/a/anmehta/www/DPSWW_v2/DY/{date}{pf}_era{year}_{here}SFs/'.format(date=date,year=year,pf=('-'+postfix if postfix else ''),here='with' if applySFs else 'without' )
    cutflow=False
    fplots = 'dps-ww/fullRun2/plots.txt'
    fmca =   'dps-ww/fullRun2/mca-dpsww.txt'
    fsyst  = '' #dps-ww/fullRun2/systsUnc.txt'
    fcut   = 'dps-ww/fullRun2/cuts_dy.txt'
    processes = ['DYLO','Diboson','data','TTdilep','data_fakes']#,'TTsemilep']#,]'TTsemilep','SingleTop','WJets',
    disable   = []
    fittodata = []
    scalethem = {}
    ratio   = ' --fixRatioRange  --ratioYNDiv 505 --maxRatioRange 0.8  1.29'
    spam    = ' --topSpamSize 1.0 --noCms '
    legends = ' --legendFontSize 0.04 --legendBorder 0 --legendWidth  0.62 --legendColumns 3 '
    ubands  = '' # --showMCError '
    anything = " " #--fitData --flp WZ --sP tot_weight  " #scaleBkgToData--preFitData tot_weight --flp WZ --sP tot_weight --sp WZ " # --fitData  --flp WZ  "# --neglist '.*_promptsub.*' --plotgroup data_fakes+=.*_promptsub" # --preFitData tot_weight --plotmode norm" #to include neagitve evt ylds from fakes 
    extraopts = ratio + spam + legends + ubands + anything
    plots    = ['MVA1','MVA2']#'ptRatio1','ptRatio2','MVA_ptRatio']#MVA1','MVA2','minMVA','maxMVA','mll','pt1','pt2','eta1','eta2','nVert','njets','met','conept1','conept2']#'ptll','minMtW','maxMtW',minMtW']#'mtww','ptll','mll','pt1','pt2','eta1','eta2','MVA1','MVA2','nVert','njets','met']#,'phi1','phi2','MVA1','MVA2','tcharge1','tcharge2','charge1','charge2','pdgId1','pdgId2','dilep_charge','dilep_flav','met','metphi','njets','mll','mt2ll','mt1','mtll','etasum','etaprod','dphill','dphil2met','dphilll2','nVert'] #'BDT_wz_amc','BDT_fakes','BDT_wz_pow','BDT_DPS_multiC','BDT_WZ_multiC','BDT_TL_multiC']
    for FS in finalState:
        enable=[]
        enable.append(FS); 
        makeplots=[ip + '_' + FS for ip in plots]
        runPlots(trees, friends, MCfriends, Datafriends, targetdir, fmca, fcut, fsyst, fplots, enable, disable, processes, scalethem, fittodata,makeplots,True,applySFs,year, 2,extraopts,[],cutflow)

def chkUnskimmedTrees(year,finalState):
    trees       = '/eos/cms/store/cmst3/group/dpsww/NanoTrees_v7_dpsww_04092020/{year}/'.format(year=year)
    friends     = [trees+'2_recl']#, trees+'dpsbdt']
    MCfriends   = ''
    Datafriends = ''
    fplots      = 'dps-ww/fullRun2/plots.txt'
    fmca        = 'dps-ww/fullRun2/mca-dpsww.txt' 
    fsyst       = ''
    fcut        = 'dps-ww/fullRun2/cuts_2lss.txt' 

    applyWtsnSFs = False
    cutflow=False
    targetdir   = '/eos/user/a/anmehta/www/DPSWW_v2/{date}{pf}_era{year}_unskimmed/'.format(date=date, year=year,pf=('-'+postfix if postfix else '') ) 

    #processes = ['DPSWW','WZ_amc','ZZ','data','Rares','data_fakes','data_flips','Convs']
    processes = ['DPSWW','Rares','WZ_amc','ZZ','Convs','WZ_mllLT4','data','data_fakes','DPSWW_hg','WZ_pow']#,'dy','Flips','Convs','Wgstar','WZ_incl','promptsub']    'data_flips',
    allvars    = ['MVA1','MVA2','conept1','conept2','minMVA','maxMVA']

    loop=['']
    plotvars   = allvars 

    for FS in finalState:            
        enable=[]
        enable.append(FS); 
        print enable #list(ch) + list (finalState)
        disable   = []
        invert    = []
        fittodata = []
        scalethem = {}
        ratio   = ' --fixRatioRange  --ratioYNDiv 505 --maxRatioRange 0.45  1.69' 
        spam    = ' --topSpamSize 1.0 --noCms '
        legends = ' --legendFontSize 0.04 --legendBorder 0 --legendWidth  0.62 --legendColumns 3 '
        ubands  = '  --showMCError '
        anything = '--binname {finalState}'.format(finalState=FS) 
        extraopts = ratio + spam + legends + ubands + anything

        makeplots  = ['{}_{}'.format(a,FS) for a in plotvars]
            
        runPlots(trees, friends, MCfriends, Datafriends, targetdir, fmca, fcut, fsyst, fplots, enable, disable, processes, scalethem, fittodata,makeplots,False, applyWtsnSFs, year, 2,extraopts,invert,cutflow)


if __name__ == '__main__':
    parser = optparse.OptionParser(usage='usage: %prog [opts] ', version='%prog 1.0')
    parser.add_option('--pf', '--postfix', dest='postfix' , type='string', default='', help='postfix for running each module')
    parser.add_option('-d', '--date', dest='date' , type='string', default='', help='run with specified date instead of today')
    #    parser.add_option('-l', '--lumi', dest='lumi' , type='float'  , default=1.    , help='change lumi by hand')
    parser.add_option('--onelepCR',dest='onelepCR', action='store_true', default=False , help='make plots in single lep CR')
    parser.add_option('--dyCR',dest='dyCR', action='store_true', default=False , help='make plots in dy CR')
    parser.add_option('--threelepCR',dest='threelepCR', action='store_true', default=False , help='make plots in 3lep CR')
    parser.add_option('--fourlepCR',dest='fourlepCR', action='store_true' , default=False , help='make plots in 4lep CR')
    parser.add_option('--finalState',dest='finalState',type='string' , default=[], action="append", help='final state(s) to run on')
    parser.add_option('--splitCharge',dest='splitCharge',action='store_true', default=False , help='split by charge')
    parser.add_option('--year',   dest='year'  , type='string' , default='' , help='make plots/cards for specified year')
    parser.add_option('--threesome',   dest='threesome'  , type='string' , default='WGstar' , help='three lepton CR for WZ or WGstar')
    parser.add_option('--results' , '--makeResults'  , dest='results', action='store_true' , default=False , help='make plots')
    parser.add_option('--old' , dest='old', action='store_true' , default=False , help='make plots')
    parser.add_option('--dW' , '--doWhat'  , dest='doWhat', type='string' , default=[] , help='plots or cards')
    parser.add_option('--dpsww',dest='dpsww', action='store_true' , default=False , help='make plots for signal')
    parser.add_option('--analysis',dest='analysis', type='string',default='dps' , help='cut file to be used')
    parser.add_option('--genInfo', dest='genInfo', action='store_true' , default=False , help='make plots using gen level leptons')
    parser.add_option('--postFSR',dest='postFSR',action='store_true', default=True , help='use postFSR')
    parser.add_option('--fC', dest='fakesClosure', action='store_true' , default=False , help='FR closure test')
    parser.add_option('--unskimmed', dest='unskimmed', action='store_true' , default=False , help='chk ntuples before 2lss skimming')
    (opts, args) = parser.parse_args()

    global date, postfix, date
    postfix = opts.postfix
    year= opts.year
    date = datetime.date.today().isoformat()

    if opts.date:
        date = opts.date
    if opts.dyCR:
        dyCRPlot(opts.year,opts.finalState)
    if opts.threelepCR:
        threelepCRPlot(opts.year,opts.threesome)
    if opts.fourlepCR:
        fourlepCRPlot(opts.year)
    if opts.onelepCR:
        onelepCRPlot(opts.year,opts.finalState)
    if opts.results:
        print 'running plots for 2lss'
        makeResults(opts.year,opts.finalState,opts.splitCharge,opts.doWhat,opts.analysis)
    if opts.dpsww:
        dpsww(opts.finalState)
    if opts.old:
        makeResults_oldMaps(opts.year,opts.finalState,opts.splitCharge)
    if opts.genInfo:
        makeResultsGen(opts.year,opts.finalState,opts.splitCharge,opts.postFSR)
    if opts.fakesClosure:
        fakesClosure(opts.year,opts.finalState)
    if opts.unskimmed:
        chkUnskimmedTrees(opts.year,opts.finalState)
# python runDPS.py --results --dW plots --year 2016 --finalState elmu --finalState mumu
# python runDPS.py --year 2016 --finalState ll --genDressed
