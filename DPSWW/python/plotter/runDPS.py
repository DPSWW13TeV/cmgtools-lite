#!/usr/bin/env python
import optparse, subprocess, ROOT, datetime, math, array, copy, os, re, sys
import numpy as np
lumis = {
    '2016': '35.9', #35.91
    '2017': '41.5', #41.52
    '2018': '59.7', #59.73
    'all' : '35.9,41.5,59.7',
}


def simpleMCplots(trees,MCfriends,Datafriends,targetdir, fmca, fcut,fplots, enabledcuts, disabledcuts, processes,plotlist,year,extraopts = '',bareNano=False):

    if bareNano:
        cmd  = ' mcPlots.py -f -j 10 -l {lumi}  --tree NanoAOD  --year {YEAR} --pdir {td} {fmca} {fcut} {fplots} --split-factor=-1  -P {trees} '.format(td=targetdir, trees=trees, fmca=fmca, fcut=fcut, fplots=fplots,lumi=lumis[year],YEAR=year if year!='all' else '2016,2017,2018')

    else:
        cmd  = ' mcPlots.py -f -j 10 -l {lumi} --tree NanoAOD  --year {YEAR} --pdir {td} {fmca} {fcut} {fplots} --mcc dps-ww/fullRun2/lepchoice-ttH-FO.txt --WA prescaleFromSkim --mcc dps-ww/fullRun2/mcc-METFixEE2017.txt --split-factor=-1  -P {trees} '.format(td=targetdir, trees=trees, fmca=fmca, fcut=fcut, fplots=fplots,lumi=lumis[year],YEAR=year)
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
    cmd  = ' makeShapeCardsNew.py -f -j 8 -l {lumi} --od {CARDSOUTDIR} --tree NanoAOD --year {YEAR} --mcc dps-ww/fullRun2/lepchoice-ttH-FO.txt --WA prescaleFromSkim --mcc dps-ww/fullRun2/mcc-METFixEE2017.txt {fmca} {fcut} --amc --threshold 0.01 --split-factor=-1 --unc {fsyst} -P {trees} {varName} '.format(lumi=lumis[year],CARDSOUTDIR=targetdir, trees=trees, fmca=fmca, fcut=fcut,YEAR=year if year !='all' else '2016,2017,2018',fsyst=fsyst,varName=varToFit) #--asimov signal 

    #    BDT_DPS_WZ 20,0,1.0

    cmd += ''.join(' --Fs {P}/'+frnd for frnd in friends)
    cmd += ''.join(' --FMCs {P}/'+frnd for frnd in MCfriends)
    cmd += ''.join(' --FDs {P}/'+frnd for frnd in Datafriends)

    cmd += ''.join(' -E ^'+cut for cut in enabledcuts )
    cmd += ''.join(' -X ^'+cut for cut in disabledcuts)
    #cmd += ' '.join(["--plotgroup data_fakes%s+='.*_promptsub%s'"%(x,x) for x in processes])+" --neglist '.*_promptsub.*' "
    cmd += ' -p '+','.join(processes)
    if invertedcuts:
        cmd += ''.join(' -I ^'+cut for cut in invertedcuts )
    if applyWtsnSFs:
        cmd += ''.join(' -W L1PreFiringWeight_Nom*puWeight*leptonSF_2lss *triggerSF_ttH(LepGood_pdgId[iLepFO_Recl[0]], LepGood_conePt[iLepFO_Recl[0]], LepGood_pdgId[iLepFO_Recl[1]], LepGood_conePt[iLepFO_Recl[1]],year)')

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
        cmd  = ' mcPlots.py -f -j 10 -l {lumi} --tree NanoAOD --year {YEAR} --pdir {td} {fmca} {fcut} {fplots} --split-factor=-1 --mcc fakeRates/mcc-eleIdEmu2.txt -L fakeRates/lepton-fr/frPuReweight.cc  '.format(lumi=lumis[year],td=targetdir, fmca=fmca, fcut=fcut, fplots=fplots,YEAR=year)
    else:
        cmd  = "mcPlots.py {CF} -j 10 -l {lumi} --tree NanoAOD --year {YEAR} --mcc dps-ww/fullRun2/lepchoice-ttH-FO.txt --WA prescaleFromSkim --mcc dps-ww/fullRun2/mcc-METFixEE2017.txt --pdir {td} {fmca} {fcut} {fplots} --split-factor=-1  ".format(lumi=lumis[year],td=targetdir, fmca=fmca, fcut=fcut, fplots=fplots,YEAR=year if year !='all' else '2016,2017,2018',CF='' if cutflow else '-f')


    if len(fsyst) > 0:
        cmd += ' --unc {fsyst} '.format(fsyst=fsyst)
    cmd += ''.join(' -P '+Ptree for Ptree in trees)
    cmd += ''.join(' --Fs {P}/'+frnd for frnd in friends)
    cmd += ''.join(' --FMCs {P}/'+frnd for frnd in MCfriends)
    cmd += ''.join(' --FDs {P}/'+frnd for frnd in Datafriends)
    #cmd += ''.join(' --Fs '+frnd for frnd in friends)
    #cmd += ''.join(' --FMCs '+frnd for frnd in MCfriends)
    #cmd += ''.join(' --FDs '+frnd for frnd in Datafriends)

    cmd += ''.join(' -E ^'+cut for cut in enabledcuts )
    cmd += ''.join(' -X ^'+cut for cut in disabledcuts)
    if invertedcuts:
        cmd += ''.join(' -I ^'+cut for cut in invertedcuts )

    cmd += ' --sP '+','.join(plot for plot in plotlist)
    cmd += ' -p '+','.join(processes)

    if applyWtsnSFs :
        if(nLep == 2): 
            cmd += ''.join(" -W L1PreFiringWeight_Nom*puWeight*leptonSF_2lss *triggerSF_ttH(LepGood_pdgId[iLepFO_Recl[0]], LepGood_conePt[iLepFO_Recl[0]], LepGood_pdgId[iLepFO_Recl[1]], LepGood_conePt[iLepFO_Recl[1]],2,year)")
        elif(nLep == 3):
            cmd += ' -W L1PreFiringWeight_Nom*puWeight*leptonSF_3l *triggerSF_ttH(LepGood_pdgId[iLepFO_Recl[0]], LepGood_conePt[iLepFO_Recl[0]], LepGood_pdgId[iLepFO_Recl[1]], LepGood_conePt[iLepFO_Recl[1]],3,year)'
        elif(nLep == 4):
            cmd += ' -W L1PreFiringWeight_Nom*puWeight*leptonSF_4l *triggerSF_ttH(LepGood_pdgId[iLepFO_Recl[0]], LepGood_conePt[iLepFO_Recl[0]], LepGood_pdgId[iLepFO_Recl[1]], LepGood_conePt[iLepFO_Recl[1]],2,year)'
        else:
            if(nLep == 2): 
                cmd += ''.join(" -W L1PreFiringWeight_Nom*puWeight")
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
        cmd += " "+extraopts

    print 'running: python', cmd
    subprocess.call(['python']+cmd.split())#+['/dev/null'],stderr=subprocess.PIPE)


def makeResults(year,finalState,splitCharge,doWhat,applylepSFs):
    baseDir     = '/eos/cms/store/cmst3/group/dpsww/NanoTrees_v7_dpsww_skim2lss/'
    trees      = [baseDir+'{here}'.format(here=year if year != 'all' else '')]
    friends     = ['3_tauCount', 'dpsbdt_ultimate']
    MCfriends   = ['2_recl_allvars','3_scalefactors_fixed','0_jmeUnc_v1']
    Datafriends = ['2_recl']
    fplots      = 'dps-ww/fullRun2/plots.txt'
    fmca        = 'dps-ww/fullRun2/mca-dpsww.txt'
    fsyst       = 'dps-ww/fullRun2/systsUnc.txt'
    fcut        = 'dps-ww/fullRun2/cuts_2lss.txt' 

    showratio=False
    cutflow=False
    targetdir   = '/eos/user/a/anmehta/www/DPSWW_v2/{year}/{date}{pf}{here}/'.format(date=date, year=year if year !='all' else 'fullRun2',pf=('-'+postfix if postfix else '') ,here='_withoutSFs' if not applylepSFs else '') 
    if splitCharge: 
        loop = [ 'minusminus', 'plusplus']
    else:
        loop = [ '' ]

    print 'running for %s with charge split flag %s' %(finalState,splitCharge)

    #'data','Wnjet_LO']#'WJ_LO'
    processes = ['DPSWW','WZ','Convs01J','data_fakes','data_flips','Rares','WZ_mllLT4','ZZ','data','DPSWW_hg','WZ_alt']#,'dy','Flips','Convs','Wgstar','WZ_incl','promptsub']
    if ( (year == "2018" or year == "all") and 'DPSWW_hg' in processes):
        processes.remove('DPSWW_hg')
    print processes
    #procs=[x+'_promptsub' for x in processes if not x.startswith('data')] 
    #TL
    fRvars    = ['data_fakes_FRe_pt_Up','data_fakes_FRe_pt_Dn','data_fakes_FRe_be_Up','data_fakes_FRe_be_Dn','data_fakes_FRm_pt_Up','data_fakes_FRm_pt_Dn','data_fakes_FRm_be_Up','data_fakes_FRm_be_Dn','data_fakes_FRe_norm_Up','data_fakes_FRe_norm_Dn','data_fakes_FRm_norm_Up','data_fakes_FRm_norm_Dn','promptsub_FRe_norm_Up','promptsub_FRe_norm_Dn','promptsub_FRe_pt_Up','promptsub_FRe_pt_Dn','promptsub_FRe_be_Up','promptsub_FRe_be_Dn']
    processes+=fRvars+processes

    if finalState[0] in ['mumu','elel']:
        binningBDT   = ' unroll_2Dbdt_dps_mumuN(BDTG_DPS_TLCR_withpt,BDTG_DPS_WZ_amc_withpt) 13,0.0,13.0'
        #binningBDT   = ' BDTG_DPS_WZ_amc 20,0.0,1.0'
    else:
        binningBDT   = ' unroll_2Dbdt_dps_elmuN(BDTG_DPS_TLCR_withpt,BDTG_DPS_WZ_amc_withpt) 13,0.0,13.0'

    exotic = ['ptRatio1','ptRatio2','mZ1','mZ2']#,'MVA_ptRatio','dxy1','dz1','sip3d1','dxy2','dz2','sip3d2','minMVA','maxMVA','LepGood1_motherid','LepGood2_motherid','fake_lepMVA1','fake_lepMVA2', LepGood1_genPartFlav_all','LepGood2_genPartFlav_all',LepGood1_tightId','LepGood2_tightId','LepGood1_cutBased','LepGood2_cutBased','LepGood1_mediumPromptId','LepGood1_mediumId','LepGood1_mvaFall17V2Iso','LepGood1_mvaFall17V2Iso_WPL','LepGood1_mvaId','LepGood2_mediumPromptId','LepGood2_mediumId','LepGood2_mvaFall17V2Iso','LepGood2_mvaFall17V2Iso_WPL','njets25','njets30','nBJetLoose25','nBJetMedium25','nTauTight','nTauFO'] 

    allvars    = ['met','nLepFO','nLepTight','njets25','nBJetLoose25','nBJetMedium25','njets30','conept1','conept2','pt1','pt2','eta1','eta2','met','metphi','njets25','nBJetLoose25','nBJetMedium25','njets30','mll','mt2ll','mt1','mtll','etasum','etaprod','dphill','dphil2met','dphilll2','nVert','ptll','cptll','MVA1','MVA2'] #dilep_charge','puppimetphi','puppimet''tcharge1','tcharge2','MVA1','MVA2','minMVA','dilep_flav','phi1','phi2','MVA1','MVA2',
    bdtM=['BDTG_fakes','BDTG_wzamc','BDTG1d_fakes_amc']
    bdts2d=['BDT_fakes_wzpow','BDT_fakes_wzamc','BDTG_fakes_wzpow','BDTG_fakes_wzamc']
    bdts=['BDTG1d_fakes_amc']#BDT_fakes','BDT_wzpow','BDT_wzamc','BDT1d_fakes_pow','BDT1d_fakes_amc','BDTG_fakes','BDTG_wzpow','BDTG_wzamc','BDTG1d_fakes_pow','BDTG1d_fakes_amc']
    allbdts=bdts+[i+'_withcpt' for i in bdts]
    plotvars   =  bdtM + allvars  #allvars #+bdtM #+allbdts #+allvars #allvars #exotic 

    for FS in finalState:            
        for ch in loop:
            enable=[]
            enable.append(FS);
            if len(ch)>0 : 
                enable.append(ch)
            print enable 
            disable   = []#'01jets','bVeto']
            invert    = []
            fittodata = []
            scalethem = {}
            ratio   = ' --fixRatioRange  --ratioYNDiv 505 --maxRatioRange 0.5  1.55' 
            spam    = ' --topSpamSize 1.0 --noCms '
            legends = ' --legendFontSize 0.04 --legendBorder 0 --legendWidth  0.62 --legendColumns 3 '
            ubands  = '--showMCError '
            exclude = '--xu DPSWW_shape' if year == "2018" else ' '
            #dopromptsub=    return x + ' '.join(["--plotgroup data_fakes%s+='.*_promptsub%s'"%(x,x) for x in procs])+" --neglist '.*_promptsub.*' "
            anything = " --plotmode norm   --neglist '.*_promptsub.* -plotgroup data_fakes+=.*_promptsub.* ' --binname {finalState}   ".format(finalState=FS) # --plotmode norm '.format(finalState=FS) # --fitData --flp data_fakes'# --plotmode norm' # --plotmode nostack' # ' #"  --neglist '.*_promptsub.*' --plotgroup data_fakes+=.*_promptsub.* " #-- uf" #" #to include neagitve evt ylds from fakes --showIndivSigs --noStackSig --plotmode norm  
            extraopts = ratio + spam + legends + ubands + anything + exclude

            if splitCharge:
                makeplots1  = ['{}_{}{}'.format(a,FS,ch)  for a in plotvars]
            else:
                makeplots1  = ['{}_{}'.format(a,FS) for a in plotvars]
            
            if 'plots' in doWhat:
                makeplots=makeplots1 #+makeplots2
                print makeplots1
                runPlots(trees, friends, MCfriends, Datafriends, targetdir, fmca, fcut, fsyst, fplots, enable, disable, processes, scalethem, fittodata,makeplots,showratio, applylepSFs, year, 2,extraopts,invert,cutflow)

            if 'cards' in doWhat:
                #print processes
                fsyst       = 'dps-ww/fullRun2/systsUnc.txt'
                targetcarddir = 'Cards/cards_{date}{pf}_{FS}_{year}'.format(FS=FS,year=year,date=date, pf=('-'+postfix if postfix else '') )
                extraoptscards = " --neglist '.*_promptsub.* -plotgroup data_fakes+=.*_promptsub.* ' --binname {FS}{ch}{year}".format(year=year,FS=FS,ch=(ch if ch else ''))
                runCards(trees, friends, MCfriends, Datafriends, targetcarddir, fmca, fcut, fsyst , binningBDT, enable, disable, processes, scalethem,applylepSFs,year,extraoptscards,invert)
########################################
def makeResultsGen(year,finalState,splitCharge,postFSR):
    trees       = '/eos/cms/store/cmst3/group/dpsww/Summer16nanoaodV7/'
    MCfriends   = [trees+'postFSRinfoV1/']
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
            simpleMCplots(trees,MCfriends,'',targetdir, fmca, fcut,fplots, enable, disable, processes,makeplots,year,extraopts,bareNano)


#%%%%%%%%%


def threelepCRPlot(year,wzbkg):
    print '=========================================='
    print 'running 3l control region  plots '
    print '=========================================='
    baseDir     = '/eos/cms/store/cmst3/group/dpsww/NanoTrees_v7_dpsww_skim2lss/'
    trees       = [baseDir+'{here}'.format(here=year if year != 'all' else '')]
    friends     = ['3_tauCount', 'dpsbdt_ultimate']
    MCfriends   = ['2_recl_allvars','3_scalefactors_fixed','0_jmeUnc_v1']
    Datafriends = ['2_recl']
    targetdir   = '/eos/user/a/anmehta/www/DPSWW_v2/ControlRegions/{date}{pf}_{year}_threelepCR/'.format(date=date, year=year,pf=('-'+postfix if postfix else ''))
    fplots      = 'dps-ww/fullRun2/plots.txt'
    fmca        = 'dps-ww/fullRun2/mca-mc-3l.txt'
    fsyst       = 'dps-ww/fullRun2/systsUnc.txt'
    fcut        = 'dps-ww/fullRun2/cuts_3l.txt'
    showratio   = True
    applylepSFs = True

    processes = ['WZ','WZ_mllLT4','data','ZZ'] #'WZ_mllLT4''WZ_alt','Convs01J',
    if wzbkg :
        exclude =  '-- xu  WZ_norm --xu WZ_shape'
        #enable    = ['pt251515','zsel','met_wz','exclusive','cleanup','tauveto','m3l_wz']
        fittodata = ['WZ']
    else:
        processes.append('Convs01J')
        processes.append('WZ_alt')
        fittodata = ['Convs01J']
        enable    = ['pt301010','met_zg','bVeto']
        exclude =  '-- xu  Conv_norm --xu Conv_shape1 --xu Conv_shape2'
    #elif threesome == "WG":
     #   enable    = ['pt301010','m3l_wg']#,'mlllt4']
    #else:
     #   enable    = ['pt301010','met_wg','emm','gstartomm','jpsiveto']#,'mlllt4']
    disable   = []
    fittodata = ['Convs01J']#'ZZ','WZ','Convs01J','Rares']#'WG_wg',
    scalethem = {}
    ratio   = ' --fixRatioRange  --ratioYNDiv 505 --maxRatioRange 0.0  1.99'
    spam    = ' --topSpamSize 1.0 --noCms '
    legends = ' --legendFontSize 0.04 --legendBorder 0 --legendWidth  0.62 --legendColumns 3 '
    ubands  = ' --showMCError '
    anything = " --binname 3l" #--fitData --flp WZ --sP tot_weight  " #scaleBkgToData--preFitData tot_weight --flp WZ --sP tot_weight --sp WZ " # --fitData  --flp WZ  "# --neglist '.*_promptsub.*' --plotgroup data_fakes+=.*_promptsub" # --preFitData tot_weight --plotmode norm" #to include neagitve evt ylds from fakes 
    extraopts = ratio + spam + legends + ubands + anything + exclude

    bdts=['BDT_fakes','BDT_wzpow','BDT_wzamc','BDT1d_fakes_pow','BDT1d_fakes_amc','BDTG_fakes','BDTG_wzpow','BDTG_wzamc','BDTG1d_fakes_pow','BDTG1d_fakes_amc']
    makeplots= ['conept1','conept2','conept3','met','pt1','pt2','pt3','mZ1','mZ2','mll_3l','cptll','ptll'] #bdts
    runPlots(trees, friends, MCfriends, Datafriends, targetdir, fmca, fcut, fsyst, fplots, enable, disable, processes, scalethem, fittodata,makeplots,showratio, applylepSFs,year, 3,extraopts)

def fourlepCRPlot(year):
    print '=========================================='
    print 'running 4l control region  plots'
    print '=========================================='
    baseDir     = '/eos/cms/store/cmst3/group/dpsww/NanoTrees_v7_dpsww_skim2lss/'
    trees       = [baseDir+'{here}'.format(here=year if year != 'all' else '')]
    friends     = ['3_tauCount', 'dpsbdt_ultimate']
    MCfriends   = ['2_recl_allvars','3_scalefactors_fixed','0_jmeUnc_v1']
    Datafriends = ['2_recl']
    targetdir   = '/eos/user/a/anmehta/www/DPSWW_v2/ControlRegions/{date}/{year}{pf}_fourlepCR/'.format(date=date, year=year,pf=('-'+postfix if postfix else ''))
    fplots      = 'dps-ww/fullRun2/plots.txt'
    fmca        = 'dps-ww/fullRun2/mca-mc-3l.txt'
    fsyst       = 'dps-ww/fullRun2/systsUnc.txt'
    fcut        = 'dps-ww/fullRun2/cuts_4l.txt'
    processes   = ['data','ZZ','Rares','WZ_incl','DY','ttjets','TTdilep','RaresGG']#'WZ_alt','WZ',
    enable      = []
    disable     = []
    fittodata   = ['ZZ']
    scalethem   = {}
    showratio   = True
    applylepSFs = True
    exclude     =  '-- xu  ZZ_norm --xu ZZ_shape1 --xu ZZ_shape2'
    ratio   = ' --fixRatioRange  --ratioYNDiv 505 --maxRatioRange 0.0  1.99'
    spam    = ' --topSpamSize 1.0 --noCms '
    legends = ' --legendFontSize 0.04 --legendBorder 0 --legendWidth  0.62 --legendColumns 3 '
    ubands  = ' --showMCError '
    anything = " --binname 4l" # --plotmode norm" #to include neagitve evt ylds from fakes 
    allvars    = ['nLepFO','nLepTight','njets25','nBJetLoose25','nBJetMedium25','njets30']#'conept1','conept2','pt1','pt2','eta1','eta2','met','metphi','njets25','nBJetLoose25','nBJetMedium25','njets30','mll','mt2ll','mt1','mtll','etasum','etaprod','dphill','dphil2met','dphilll2','nVert','ptll','cptll'] #dilep_charge','puppimetphi','puppimet''tcharge1','tcharge2','MVA1','MVA2','minMVA','dilep_flav','phi1','phi2','MVA1','MVA2',
    bdts=['BDT_fakes','BDT_wzpow','BDT_wzamc','BDT1d_fakes_pow','BDT1d_fakes_amc','BDTG_fakes','BDTG_wzpow','BDTG_wzamc','BDTG1d_fakes_pow','BDTG1d_fakes_amc']
    makeplots= ['nBJetLoose25','nBJetMedium25','njets30','njets25','conept1','conept2','conept3','conept4','pt1','pt2','pt3','pt4','mZ1','mZ2','m4l','met']#+bdts
    extraopts = ratio + spam + legends + ubands + anything + exclude
    runPlots(trees, friends, MCfriends, Datafriends, targetdir, fmca, fcut, fsyst, fplots, enable, disable, processes, scalethem, fittodata,makeplots,showratio, applylepSFs,year, 2,extraopts)

def onelepCRPlot(year,finalState):
    print '=========================================='
    print 'running single lepton control region  plots'
    print '=========================================='
    trees       = '/eos/cms/store/cmst3/group/dpsww/TREES_ttH_FR_nano_v5/{year}/'.format(year=year)
    #    trees='/eos/cms/store/cmst3/group/tthlep/gpetrucc/TREES_ttH_FR_nano_v5/{year}/skim_z3/'.format(year=year)
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
    ubands  = ' --plotmode nostack ' #--showMCError '

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
#############################
def fakesClosure(year,finalState):
    
    print '=========================================='
    print 'running closure test on fakes WPs for MC are defined in fakeRate-2lss-frmc-qcd.txt' 
    print '=========================================='

    baseDir     = '/eos/cms/store/cmst3/group/dpsww/NanoTrees_v7_dpsww_skim2lss/'
    trees       = [baseDir+'{here}'.format(here=year if year != 'all' else '')]
    friends     = ['3_tauCount', 'dpsbdt_ultimate']
    MCfriends   = ['2_recl_allvars','3_scalefactors_fixed','0_jmeUnc_v1']
    Datafriends = ['2_recl']
    fplots      = 'dps-ww/fullRun2/plots.txt'
    fsyst       = 'dps-ww/fullRun2/systsUnc.txt'
    fmca        = 'dps-ww/fullRun2/mca-fakes-closure.txt'
    fcut        = 'dps-ww/fullRun2/cuts_2lss.txt' 
    fsyst       = '' #dps-ww/fullRun2/systsUnc.txt'
    applylepSFs=True
    targetdir = '/eos/user/a/anmehta/www/DPSWW_v2/Fakes/{date}{pf}_era{year}_fakesClosure/'.format(date=date,year=year,pf=('-'+postfix if postfix else '') )
    cutflow=False
    showratio=True
    processes = ['wj','wj_tl']#,'wj_noM']#,'wj_LO','wj_LO_tl']
    disable   = []
    fittodata = []
    invert    = []
    scalethem = {}
    ratio   = ' --fixRatioRange  --maxRatioRange 0.0  3.5'
    spam    = ' --topSpamSize 1.0 --noCms '
    legends = ' --legendFontSize 0.04 --legendBorder 0 --legendWidth  0.62 --legendColumns 2 '
    ubands  = ' '
    anything = ' --plotmode nostack --ratioDen wj_tl --ratioNums wj --ratioYLabel= obs./pred. ' 
    extraopts = ratio + spam + legends + ubands + anything
    plots    = ['BDTG1d_fakes_amc','pt1','pt2','eta1','eta2','met','conept1','conept2']#'BDT_wz_amc','BDT_fakes','BDT_wz_pow','BDT_DPS_multiC','BDT_WZ_multiC','BDT_TL_multiC']
    for FS in finalState:
        enable=[]
        enable.append(FS); 
        makeplots=[ip + '_' + FS for ip in plots]
        runPlots(trees, friends, MCfriends, Datafriends, targetdir, fmca, fcut, fsyst, fplots, enable, disable, processes, scalethem, fittodata,makeplots,showratio, applylepSFs, year, 2,extraopts,invert,cutflow)

##%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%
def dpsww(finalState,year):
    print '=========================================='
    print 'running single lepton control region  plots'
    print '=========================================='
    trees       = '/eos/cms/store/cmst3/group/dpsww/{samples}'.format(year=year,samples = 'ULvsnV7')
    MCfriends   = '' #[trees+'2_recl'] 
    Datafriends = '' #[trees+'2_recl']
    targetdir   = '/eos/user/a/anmehta/www/DPSWW_v2/{year}/{date}{pf}_signalOnly/'.format(date=date, year=year,pf=('-'+postfix if postfix else ''))
    fplots      = 'dps-ww/fullRun2/plots.txt' #simple_plots
    fmca        = 'dps-ww/fullRun2/mca-dpsww.txt'
    fcut        = 'dps-ww/fullRun2/cuts_2lss_dpsww_basic.txt' 
    disable   = []
##am    trees='/eos/cms/store/cmst3/group/dpsww/Lepton_id_study/'
##am    MCfriends=[trees+'coll_merged/']
##am    targetdir = '/eos/user/a/anmehta/www/DPSWW_v2/{date}{pf}/'.format(date=date,pf=('-'+postfix if postfix else '') ) 
##am    fplots = 'dps-ww/fullRun2/simple_plots.txt'
##am    fmca = 'dps-ww/fullRun2/mca-dpsww.txt' #simple_mca.txt'
##am    fsyst  = '' 
##am    fcut   = 'dps-ww/fullRun2/simple_cuts.txt'
##am    processes=['DPSWW']
    processes = ['DPSWW_UL','DPSWW_n7','DPSWW_cp5_n7']#,'DPSWW_CP5']#,'DYLO','Diboson','data','TTdilep','SingleTop','WJets']#,'TTsemilep']#,'data_fakes']
    #enable=[]
    ratio   = ' --fixRatioRange  --ratioYNDiv 505 --maxRatioRange 0.0  1.99'
    spam    = ' --topSpamSize 1.0 --noCms '
    legends = ' --legendFontSize 0.04 --legendBorder 0 --legendWidth  0.62 --legendColumns 3 '
    ubands  = ' --plotmode norm' 
    anything =' --showRatio  --ratioDen DPSWW_UL --ratioNums DPSWW_n7,DPSWW_cp5_n7 --ratioYLabel=nanov7/UL' #--ratioNums DPSWW_HG,DPSWW_CP5
    extraopts = ratio + spam + legends + ubands + anything
    plots=['Electron_mvaTTH','Muon_mvaTTH'] #minMVA','maxMVA','mvaTTH2','mvaTTH1','met','pt1','pt2']
    
    for FS in finalState:
        enable=[]
        #enable.append(FS); 
        makeplots=[ip + '_' + FS for ip in plots]
        simpleMCplots(trees,MCfriends,Datafriends,targetdir, fmca, fcut,fplots, enable, disable, processes,makeplots,year,extraopts,True)


def dyCRPlot(year,finalState,applySFs):
    print '=========================================='
    print 'running dy control region  plots' 
    print '=========================================='
    baseDir     = '/eos/cms/store/cmst3/group/dpsww/NanoTrees_v7_dpsww_04092020/'
    trees       = [baseDir+'{here}'.format(here=year if year != 'all' else '')]
    WP='_muWP90_elWP70' if year == '2017' else ''
    friends     = ['3_tauCount{here}'.format(here=WP)]#,'3_scalefactors_lep_fixed_EOY'
    MCfriends   = ['2_recl_allvars{here}'.format(here=WP),'0_jmeUnc_v1{here}'.format(here=WP),'3_scalefactors{here}'.format(here=WP)]
    Datafriends = ['2_recl{here}'.format(here=WP)]
    targetdir = '/eos/user/a/anmehta/www/DPSWW_v2/DY/{date}{pf}_{year}{wp}_{here}SFs/'.format(date=date,year=year,pf=('-'+postfix if postfix else ''),wp=WP,here='with' if applySFs else 'without' )
    cutflow=False
    fplots = 'dps-ww/fullRun2/plots.txt'
    fmca =   'dps-ww/fullRun2/mca-dpsww.txt'
    fsyst  = 'dps-ww/fullRun2/systsUnc.txt'
    fcut   = 'dps-ww/fullRun2/cuts_dy.txt'
    processes = ['WZ','data_fakes','DY','WZ_mllLT4','ZZ','data','Convs01J','Rares']

    fRvars    = ['data_fakes_FRe_pt_Up','data_fakes_FRe_pt_Dn','data_fakes_FRe_be_Up','data_fakes_FRe_be_Dn','data_fakes_FRm_pt_Up','data_fakes_FRm_pt_Dn','data_fakes_FRm_be_Up','data_fakes_FRm_be_Dn','data_fakes_FRe_norm_Up','data_fakes_FRe_norm_Dn','data_fakes_FRm_norm_Up','data_fakes_FRm_norm_Dn','promptsub_FRe_norm_Up','promptsub_FRe_norm_Dn','promptsub_FRe_pt_Up','promptsub_FRe_pt_Dn','promptsub_FRe_be_Up','promptsub_FRe_be_Dn','WZ_alt']
    processes+=fRvars+processes
    for FS in finalState:
        enable=[]
        enable.append(FS); 
        disable   = []
        fittodata = []
        scalethem = {}
        ratio   = ' --fixRatioRange  --ratioYNDiv 505 --maxRatioRange 0.8  1.29'
        spam    = ' --topSpamSize 1.0 --noCms '
        legends = ' --legendFontSize 0.04 --legendBorder 0 --legendWidth  0.62 --legendColumns 3 '
        ubands  = ' --showMCError '
        anything = "   --neglist '.*_promptsub.* -plotgroup data_fakes+=.*_promptsub.* ' --binname {finalState}   ".format(finalState=FS) 
        extraopts = ratio + spam + legends + ubands + anything
        plots    = ['njets25','njets30','ptll','cptll','mll','pt1','pt2','eta1','eta2','met','MVA1','MVA2']
        makeplots=[ip + '_' + FS for ip in plots]
        runPlots(trees, friends, MCfriends, Datafriends, targetdir, fmca, fcut, fsyst, fplots, enable, disable, processes, scalethem, fittodata,makeplots,True,applySFs,year, 2,extraopts,[],cutflow)
############################
def chkUnskimmedTrees(year,finalState):
    baseDir     = '/eos/cms/store/cmst3/group/dpsww/NanoTrees_v7_dpsww_04092020/'
    trees       = [baseDir+'{here}'.format(here=year if year != 'all' else '')]
    WP='_muWP90_elWP65'
    friends     = ['2_recl{here}'.format(here=WP),'3_tauCount{here}'.format(here=WP)]#,'3_scalefactors_lep_fixed_EOY'
    MCfriends   = ['3_scalefactors{here}'.format(here=WP)]
    Datafriends = ''
    fplots      = 'dps-ww/fullRun2/plots.txt'
    fmca        = 'dps-ww/fullRun2/mca-dpsww.txt' 
    fsyst       = ''
    fcut        = 'dps-ww/fullRun2/cuts_2lss.txt' 

    applyWtsnSFs = True
    cutflow=False
    
    #targetdir   = '/eos/user/a/anmehta/www/DPSWW_v2/unskimmed/{year}/{date}{pf}_{here}/'.format(here=WP,date=date, year=year,pf=('-'+postfix if postfix else '') ) 
    targetdir   = '/eos/user/a/anmehta/www/DPSWW_v2/unskimmed/{year}/{date}{pf}_{here}/'.format(here=WP,date=date, year=year if year !='all' else '',pf=('-'+postfix if postfix else '') ) 
    processes = ['DPSWW','WZ','Convs01J','data_fakes_mu90el65','Rares','WZ_mllLT4','ZZ','data']#,'dy','Flips','Convs','Wgstar','WZ_incl','promptsub']
    nvars    = ['conept1','conept2']#nLepFO','nLepTight','njets25','nBJetLoose25','nBJetMedium25','njets30']
    allvars    = ['MVA1','MVA2','minMVA','conept1','conept2','eta1','eta2','met','njets25','njets30','nBJetLoose25','nBJetMedium25']
    bdts=['BDT_wz_amc','BDT_fakes','BDT_wz_pow','BDT1d_amc','BDT1d_pow','BDT_wz_pow','BDT1d_pow']#,'BDTfakes_BDTwz_amc','BDTfakes_BDTwz_pow']
    loop=['']
    plotvars   = nvars #+ bdts

    for FS in finalState:            
        enable=[]
        enable.append(FS); 
        print enable #list(ch) + list (finalState)
        disable   = []#'tauveto']#,'bVeto','jetVeto','TT'] #'tauveto']#,'TT']
        invert    = []
        fittodata = []
        scalethem = {}
        ratio   = ' --fixRatioRange  --ratioYNDiv 505 --maxRatioRange 0.45  1.69' 
        spam    = ' --topSpamSize 1.0 --noCms '
        legends = ' --legendFontSize 0.04 --legendBorder 0 --legendWidth  0.62 --legendColumns 3 '
        ubands  = '  ' #--showMCError '
        anything = ' --binname {finalState}'.format(finalState=FS) 
        extraopts = ratio + spam + legends + ubands + anything

        makeplots  = ['{}_{}'.format(a,FS) for a in plotvars]
            
        runPlots(trees, friends, MCfriends, Datafriends, targetdir, fmca, fcut, fsyst, fplots, enable, disable, processes, scalethem, fittodata,makeplots,True, applyWtsnSFs, year, 2,extraopts,invert,cutflow)
########################


def testBDT(year,finalState):
    trees       = 'BDT_test/'
    friends     = [trees+'bdts']
    MCfriends   = ''
    Datafriends = [trees+'2_recl']
    fplots      = 'dps-ww/fullRun2/plots.txt'
    fmca        = 'dps-ww/fullRun2/mca-dpsww.txt'
    fsyst       = ''
    fcut        = 'dps-ww/fullRun2/cuts_2lss.txt' 

    splitCharge=False
    cutflow=False
    targetdir   = '/eos/user/a/anmehta/www/DPSWW_v2/{year}/{date}{pf}/'.format(date=date, year=year,pf=('-'+postfix if postfix else ''))
    if splitCharge: 
        loop = [ 'minusminus', 'plusplus']
    else:
        loop = [ '' ]

    print 'running for %s with charge split flag %s' %(finalState,splitCharge)


    processes = ['fakes_data_pT','fakes_data'] #DPSWW','WZ_amc'


    if finalState[0] in ['mumu','elel']:
        binningBDT   = ' unroll_2Dbdt_dps_mumu(BDT_DPS_TLCR,BDT_DPS_WZ_pow) 15,0.0,15.0'
    else:
        binningBDT   = ' unroll_2Dbdt_dps_elmu(BDT_DPS_TLCR,BDT_DPS_WZ_pow) 15,0.0,15.0'


    allvars    = ['conept1','conept2','pt1','pt2','eta1','eta2','phi1','phi2','MVA1','MVA2','met','metphi','dilep_flav','njets25','mll','mt2ll','mt1','mtll','etasum','etaprod','dphill','dphil2met','dphilll2','nVert','ptll'] #dilep_charge','puppimetphi','puppimet''tcharge1','tcharge2','MVA1','MVA2','minMVA',

    bdts=['BDT_wz_amc','BDT_wz_pow','BDT_TL','BDT_fakes','BDT_TLCR','BDT_fakesCR','BDT1d_fakes_amc','BDT1d_fakes_pow','BDT1d_fakesCR_amc','BDT1d_fakesCR_pow','BDT1d_TL_amc','BDT1d_TL_pow','BDT1d_TLCR_amc','BDT1d_TLCR_pow']#,'BDT_wz_pow','BDT1d_pow','BDTfakes_BDTwz_amc','BDTfakes_BDTwz_pow'] #'BDT_DPS_multiC','BDT_WZ_multiC','BDT_TL_multiC']


    plotvars   = bdts #+allvars #allvars #exotic 

    for FS in finalState:            
        for ch in loop:
            enable=[]
            enable.append(FS); 
            if len(ch)>0 : 
                enable.append(ch)
            print enable #list(ch) + list (finalState)
            disable   = ['tauveto']
            invert    = []
            fittodata = []
            scalethem = {}
            ratio   = ' --fixRatioRange  --ratioYNDiv 505 --maxRatioRange 0.45  1.69  --ratioDen fakes_data_pT --ratioNums fakes_data --ratioYLabel=cpT/pT'
            spam    = ' --topSpamSize 1.0 --noCms '
            legends = ' --legendFontSize 0.04 --legendBorder 0 --legendWidth  0.62 --legendColumns 3 '
            ubands  = ''
            anything = ' --binname {finalState} --plotmode norm '.format(finalState=FS) # --fitData --flp data_fakes'# --plotmode norm' # --plotmode nostack' # rm --neg ' #--plotmode norm ' #"  --neglist '.*_promptsub.*' --plotgroup data_fakes+=.*_promptsub.* " #-- uf" #" #to include neagitve evt ylds from fakes --showIndivSigs --noStackSig --plotmode nostack
            extraopts = ratio + spam + legends + ubands + anything

            if splitCharge:
                makeplots1  = ['{}_{}{}'.format(a,FS,ch)  for a in plotvars]
            else:
                makeplots1  = ['{}_{}'.format(a,FS) for a in plotvars]
            

            makeplots=makeplots1 #+makeplots2
            print makeplots1
            runPlots(trees, friends, MCfriends, Datafriends, targetdir, fmca, fcut, fsyst, fplots, enable, disable, processes, scalethem, fittodata,makeplots,True, False, year, 2,extraopts,invert,cutflow)
############################################## dressed lepton info from unskimmed samples
def makeResultsDressedLep(year,finalState,splitCharge):
    trees       = '/eos/cms/store/cmst3/group/dpsww/Summer16nanoaodV7/'
    friends     = ''
    MCfriends   = ''
    Datafriends = ''
    fplots      = 'dps-ww/fullRun2/plots.txt'
    fmca        = 'dps-ww/fullRun2/mca-dpsww-gen.txt'
    fcut        = 'dps-ww/fullRun2/cuts_2lss_dpsww_dressed.txt'

    bareNano=True
    targetdir   = '/eos/user/a/anmehta/www/DPSWW_v2/GeneratorLevel/{date}{pf}_{year}dressed/'.format(date=date, year=year,pf=('-'+postfix if postfix else ''))
    if splitCharge: 
        loop = [ 'minusminus', 'plusplus']
    else:
        loop = [ '' ]

    print 'running for %s with charge split flag %s' %(finalState,splitCharge)


    processes = ['DPSpy8','DPShwpp']#'WZ_amc','WZ_pow','WZ_incl','WZ_mllLT4']#,'Wgstar','WG','ZG','ZG_lowmll']


    allvars    = ['pt1_dressedLep','mll_dressedLep_os','eta1_dressedLep','pdgIdprod_dressedLep','pt2_dressedLep','eta2_dressedLep','mll_lower_dressedLep','mll_dressedLep','mll_low_dressedLep','ndressedLep','mll_high_dressedLep']
    plotvars   = allvars 

    for FS in finalState:            
        for ch in loop:
            enable=[]
            enable.append(FS);
            if len(ch)>0 : 
                enable.append(ch)
            print enable 
            disable   = []
            invert    = []
            fittodata = []
            scalethem = {}
            ratio   = ' --fixRatioRange  --ratioYNDiv 505 --maxRatioRange 0.65  1.25'
            spam    = ' --topSpamSize 1.0 --noCms '
            legends = ' --legendFontSize 0.04 --legendBorder 0 --legendWidth  0.62 --legendColumns 2 '
            ubands  = ' '
            anything = ' --plotmode nostack'
            extraopts = ratio + spam + legends + ubands + anything

            if splitCharge:
                makeplots1  = ['{}_{}{}'.format(a,FS,ch)  for a in plotvars]
            else:
                makeplots1  = ['{}_{}'.format(a,FS) for a in plotvars]
            

            makeplots=makeplots1 #+makeplots2

            simpleMCplots(trees,MCfriends,Datafriends,targetdir, fmca, fcut,fplots, enable, disable, processes,makeplots,year,extraopts,bareNano)

####################################


if __name__ == '__main__':
    parser = optparse.OptionParser(usage='usage: %prog [opts] ', version='%prog 1.0')
    parser.add_option('--pf', '--postfix', dest='postfix' , type='string', default='', help='postfix for running each module')
    parser.add_option('-d', '--date', dest='date' , type='string', default='', help='run with specified date instead of today')
    #    parser.add_option('-l', '--lumi', dest='lumi' , type='float'  , default=1.    , help='change lumi by hand')
    parser.add_option('--onelepCR',dest='onelepCR', action='store_true', default=False , help='make plots in single lep CR')
    parser.add_option('--dyCR',dest='dyCR', action='store_true', default=False , help='make plots in dy CR')
    parser.add_option('--wzCR',dest='threelepCR', action='store_true', default=False , help='make plots in 3lep CR')
    parser.add_option('--zzCR',dest='fourlepCR', action='store_true' , default=False , help='make plots in 4lep CR')
    parser.add_option('--finalState',dest='finalState',type='string' , default=[], action="append", help='final state(s) to run on')
    parser.add_option('--splitCharge',dest='splitCharge',action='store_true', default=False , help='split by charge')
    parser.add_option('--year',   dest='year'  , type='string' , default='' , help='make plots/cards for specified year')
    parser.add_option('--wzbkg',dest='threesome', action='store_true' , default=False, help='make plots in 3lep CR enriched with WZ otherwise dominated by conversions')
    parser.add_option('--results' , '--makeResults'  , dest='results', action='store_true' , default=False , help='make plots')
    parser.add_option('--old' , dest='old', action='store_true' , default=False , help='make plots')
    parser.add_option('--dW' , '--doWhat'  , dest='doWhat', type='string' , default=[] , help='plots or cards')
    parser.add_option('--dpsww',dest='dpsww', action='store_true' , default=False , help='make plots for signal')
    ##    parser.add_option('--analysis',dest='analysis', type='string',default='dps' , help='cut file to be used')
    parser.add_option('--genInfo', dest='genInfo', action='store_true' , default=False , help='make plots using gen level leptons')
    parser.add_option('--postFSR',dest='postFSR',action='store_true', default=True , help='use postFSR')
    parser.add_option('--fC', dest='fakesClosure', action='store_true' , default=False , help='FR closure test')
    parser.add_option('--unskimmed', dest='unskimmed', action='store_true' , default=False , help='chk ntuples before 2lss skimming')
    parser.add_option('--applylepSFs',dest='applylepSFs', action='store_true', default=False , help='apply lep id/iso SFs')
    parser.add_option('--genD',dest='genDressed', action='store_true' , default=False , help='2lss using dressed leptons')
    parser.add_option('--tbdt',dest='testBDT', action='store_true' , default=False , help='compare bdts')
    (opts, args) = parser.parse_args()

    global date, postfix, date
    postfix = opts.postfix
    year= opts.year
    date = datetime.date.today().isoformat()

    if opts.date:
        date = opts.date
    if opts.dyCR:
        dyCRPlot(opts.year,opts.finalState,opts.applylepSFs)
    if opts.threelepCR:
        threelepCRPlot(opts.year,opts.threesome)
    if opts.fourlepCR:
        fourlepCRPlot(opts.year)
    if opts.onelepCR:
        onelepCRPlot(opts.year,opts.finalState)
    if opts.results:
        print 'running {here} for 2lss' .format(here=opts.doWhat)
        makeResults(opts.year,opts.finalState,opts.splitCharge,opts.doWhat,opts.applylepSFs)
    if opts.dpsww:
        dpsww(opts.finalState,opts.year)
    if opts.old:
        makeResults_oldMaps(opts.year,opts.finalState,opts.splitCharge)
    if opts.genInfo:
        makeResultsGen(opts.year,opts.finalState,opts.splitCharge,opts.postFSR)
    if opts.fakesClosure:
        fakesClosure(opts.year,opts.finalState)
    if opts.unskimmed:
        chkUnskimmedTrees(opts.year,opts.finalState)
    if opts.testBDT:
        testBDT(opts.year,opts.finalState)
    if opts.genDressed:
        makeResultsDressedLep(opts.year,opts.finalState,opts.splitCharge)
# python runDPS.py --results --dW plots --year 2016 --finalState elmu --finalState mumu --applylepSFs
# python runDPS.py --year 2016 --finalState ll --genD
# python runDPS.py --dyCR --year 2017 --finalState mumu --finalState elmu --finalState elel --applylepSFs
# python runDPS.py --results --dW cards --year 2017 --finalState elmu --finalState mumu --applylepSFs --splitCharge
# python runDPS.py --unskimmed --year 2017 --finalState elmu --finalState mumu
# python runDPS.py --fC --year 2016 --finalState elmu --finalState mumu 
