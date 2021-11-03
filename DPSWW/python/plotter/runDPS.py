#!/usr/bin/env python
import optparse, subprocess, ROOT, datetime, math, array, copy, os, re, sys
import numpy as np
eos='/eos/user/a/anmehta/www/DPSWW_v2/'
lumis = {
    '2016': '36.33', #35.91
    '2017': '41.53', #41.52
    '2018': '59.74', #59.73
    'All_gen': '137.6',
    'all' : '36.33,41.53,59.74',
}

binningSchemes = {
    'wz_nb13'    : ' BDTG_DPS_WZ_amc_raw_withpt 13,-1.0,1.0',
    'wz_nb15'    : ' BDTG_DPS_WZ_amc_raw_withpt 15,-1.0,1.0',
    'iwz'        : ' BDTG_DPS_WZ_amc_raw_withpt [-1.0,-0.9,-0.8,-0.6,-0.45,-0.2,0,0.2,0.4,0.6,0.7,1.0]',
    'i1wz'       : ' BDTG_DPS_WZ_amc_raw_withpt [-1.0,-0.9,-0.8,-0.6,-0.45,-0.3,-0.2,0,0.2,0.5,0.7,0.8,1.0]',
    'prod_20'    : ' BDTG_DPS_TLCR_raw_withpt*BDTG_DPS_WZ_amc_raw_withpt 20,-0.2,1.0',
    'prod_13'    : ' BDTG_DPS_TLCR_raw_withpt*BDTG_DPS_WZ_amc_raw_withpt 13,-0.2,1.0',
    'diag'       : ' unroll_2Dbdt_dps_SoBord_diag(BDTG_DPS_TLCR_raw_withpt,BDTG_DPS_WZ_amc_raw_withpt) 13,0.0,13.0',
    'diag_pc'    : ' unroll_2Dbdt_dps_SoBord_diag_pc(BDTG_DPS_TLCR_raw_withpt,BDTG_DPS_WZ_amc_raw_withpt) 11,0.0,11.0',
    'SoBord_sqV3': ' unroll_2Dbdt_dps_SoBord_sqV3(BDTG_DPS_TLCR_raw_withpt,BDTG_DPS_WZ_amc_raw_withpt) 13,0.0,13.0',
    'SoBord_sqV2': ' unroll_2Dbdt_dps_SoBord_sqV2(BDTG_DPS_TLCR_raw_withpt,BDTG_DPS_WZ_amc_raw_withpt) 13,0.0,13.0',
    'SoBord_sqV1': ' unroll_2Dbdt_dps_SoBord_sqV1(BDTG_DPS_TLCR_raw_withpt,BDTG_DPS_WZ_amc_raw_withpt) 12,0.0,12.0',
    'sq'         : ' unroll_2Dbdt_dps_SoBord_sq(BDTG_DPS_TLCR_raw_withpt,BDTG_DPS_WZ_amc_raw_withpt) 10,0.0,10.0',
    ''           : ' unroll_2Dbdt_dps_SoBord_sqV3(BDTG_DPS_TLCR_raw_withpt,BDTG_DPS_WZ_amc_raw_withpt) 13,0.0,13.0'
}

baseDir      = '/eos/cms/store/cmst3/group/dpsww/NanoTrees_v7_dpsww_skim2lss/' 
#baseDir     = '/eos/cms/store/cmst3/group/dpsww/NanoTrees_v7_dpsww_04092020/' #unskimmed
MCfriends   = ['2_recl_allvars','4_scalefactors','0_jmeUnc_v2']#,'postFSRinfo']#,'postFSRinfo']#,'2_btag_SFs']'','3_scalefactors_fixed',
Datafriends = ['2_recl']#'4_scalefactors',

friends     = ['3_tauCount','dpsbdt_neu_ssnoeebkg_afacdps']
#,'dpsbdt_neu_ssnoeebkg_afacdps_unclEn']#'dpsbdt_allyrs']#'dnn_ultimate',] #'dnn_ll_noeessTr','dpsbdt_all']#'dpsbdt_unclEn','dpsbdt_jec','dpsbdt_HEM']#,'dnn_testChunks']

fplots      = 'dps-ww/fullRun2/plots.txt'


metvars     = ['met','met_HEMUp','met_HEMDn','met_unclUp','met_unclDn','met_jecUp','met_jecDn']
jetvars     = ['nj','nj_jecUp','nj_jecDn']
allbdts     = ['BDT_WZ','BDT_fakes','BDT1d']
bdtGvarsUp  = ['BDT1d_unclUp','BDT_fakes_unclUp','BDT_WZ_unclUp']#,'BDT_fakes_jerbUp','BDT_fakes_jerec1Up','BDT_fakes_jerec2hptUp','BDT_fakes_jerec2lptUp','BDT_fakes_jerfwdhptUp','BDT_fakes_jerfwdlptUp',,'BDT_WZ_jecUp','BDT_WZ_jerbUp','BDT_WZ_jerec1Up','BDT_WZ_jerec2hptUp','BDT_WZ_jerec2lptUp','BDT_WZ_jerfwdhptUp','BDT_WZ_jerfwdlptUp','BDT1d_jecUp','BDT1d_jerbUp','BDT1d_jerec1Up','BDT1d_jerec2hptUp','BDT1d_jerec2lptUp','BDT1d_jerfwdhptUp','BDT1d_jerfwdlptUp','BDT_fakes_jecUp']'BDT_fakes_HEMUp','BDT_WZ_HEMUp','BDT1d_HEMUp',
bdtGvarsDn = ['BDT_fakes_unclDn','BDT_WZ_unclDn','BDT1d_unclDn']#,'BDT_fakes_jecDn','BDT_fakes_jerbDn','BDT_fakes_jerec1Dn','BDT_fakes_jerec2hptDn','BDT_fakes_jerec2lptDn','BDT_fakes_jerfwdhptDn','BDT_fakes_jerfwdlptDn','BDT_fakes_HEMDn','BDT_WZ_jecDn','BDT_WZ_jerbDn','BDT_WZ_jerec1Dn','BDT_WZ_jerec2hptDn','BDT_WZ_jerec2lptDn','BDT_WZ_jerfwdhptDn', 'BDT_WZ_jerfwdlptDn','BDT1d_jerbDn','BDT1d_jecDn', 'BDT1d_jerec1Dn', 'BDT1d_jerec2hptDn','BDT1d_jerec2lptDn','BDT1d_jerfwdhptDn','BDT1d_jerfwdlptDn',]'BDT_fakes_HEMDn','BDT1d_HEMDn','BDT_WZ_HEMDn',

exotic = ['ptRatio1','ptRatio2','mZ1','mZ2','MVA_ptRatio','dxy1','dz1','sip3d1','dxy2','dz2','sip3d2','minMVA','maxMVA','LepGood1_motherid','LepGood2_motherid','fake_lepMVA1','fake_lepMVA2', 'LepGood1_genPartFlav_all','LepGood2_genPartFlav_all','LepGood1_tightId','LepGood2_tightId','LepGood1_cutBased','LepGood2_cutBased','LepGood1_mediumPromptId','LepGood1_mediumId','LepGood1_mvaFall17V2Iso','LepGood1_mvaFall17V2Iso_WPL','LepGood1_mvaId','LepGood2_mediumPromptId','LepGood2_mediumId','LepGood2_mvaFall17V2Iso','LepGood2_mvaFall17V2Iso_WPL','njets25','njets30','nBJetLoose25','nBJetMedium25','nTauTight','nTauFO','puppimetphi','puppimet'] 

bdtiv      = ['conept1','conept2','met','mt2ll','mt1','mtll','etasum','etaprod','dphill','dphil2met','dphilll2']
allvars    = bdtiv + ['mll','cptll','nBJetLoose25','njets30','nVert']
bdtGM     = ['BDTG_fakes_raw','BDTG_wzamc_raw','BDTG1d_fakes_amc_raw_SoB_sqV3']#'BDTG1d_fakes_amc_raw_SoB_diag',,'BDTG1d_fakes_amc_raw_SoB_diag_pc']
#,'minMVA','nVert','nLepFO','nLepTight','eta1','eta2','etaprod_phs','etaprod_nhs','deltaz','dilep_charge','tcharge1','tcharge2','minMVA','dilep_flav','phi1','phi2','metphi','njets25','pt1','pt2','nBJetMedium25','deltaz','ptll','dR','deltaxy','deltaz'] #
puChk     = ['bnVert','nLepGood','dilep_flav']
Nm1Study  = ['nBJetLoose20','cptll','met','njets30','nBJetLoose25']

bdtG2d    = ['BDTG_fakes_wzamc_raw'] 
all1Ds    = ['BDTG1d_fakes_amc_raw_SoB_diag','BDTG1d_fakes_amc_raw_SoB_diag_pc','BDTG1d_fakes_amc_raw_SoB_sq','BDTG1d_fakes_amc_raw_SoB_sqV1','BDTG1d_fakes_amc_raw_SoB_sqV2','BDTG1d_fakes_amc_raw_SoB_sqV3']
dnn       = ['DNN_fakes','DNN_wzamc','DNN_fakes_wzamc']
newOpts   = ['BDTG_prod_raw','BDTG_i1wz_raw','BDTG_iwz_raw']
only      = ['BDTG1d_fakes_amc_raw_SoB_sqV3']
dyCR      = ['mtll','conept1','conept2','met','njets30','nBJetLoose25','mll','cptll']
plwzCR    = ['conept1','conept2','conept3','met','mZ1','mZ2','mll_3l','cptll']+bdtGM 
plzzCR    = ['nBJetLoose25','nBJetMedium25','njets30','njets25','conept1','conept2','conept3','conept4','mZ1','mZ2','m4l','met']+bdtGM 


#####################
def simpleMCplots(trees,MCfriends,Datafriends,targetdir, fmca, fcut,fplots, enabledcuts, disabledcuts, processes,plotlist,year,extraopts = '',bareNano=False,cutflow=False):

    if bareNano:
        cmd  = ' mcPlots.py {CF} -j 10 -l {lumi}  --tree NanoAOD  --year {YEAR} --pdir {td} {fmca} {fcut} {fplots} --split-factor=-1  -P {trees} '.format(td=targetdir, trees=trees, fmca=fmca, fcut=fcut, fplots=fplots,lumi=lumis[year],YEAR=year if year!='all' else '2016,2017,2018',CF='' if cutflow else '-f')

    else:
        cmd  = ' mcPlots.py {CF} -j 10 -l {lumi} --tree NanoAOD  --year {YEAR} --pdir {td} {fmca} {fcut} {fplots} --mcc dps-ww/fullRun2/lepchoice-ttH-FO.txt --WA prescaleFromSkim --mcc dps-ww/fullRun2/mcc-METFixEE2017.txt --split-factor=-1  -P {trees} '.format(td=targetdir, trees=trees, fmca=fmca, fcut=fcut, fplots=fplots,lumi=lumis[year],YEAR=year,CF='' if cutflow else '-f')
        #cmd  = ' mcPlots.py -f -j 10 -l {lumi} --tree NanoAOD  --year {YEAR} --pdir {td} {fmca} {fcut} {fplots}  --WA prescaleFromSkim --mcc dps-ww/fullRun2/mcc-METFixEE2017.txt --split-factor=-1  -P {trees} '.format(td=targetdir, trees=trees, fmca=fmca, fcut=fcut, fplots=fplots,lumi=lumis[year],YEAR=year)

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

    cmd  = ' makeShapeCardsNew.py -f -j 8 -l {lumi} --od {CARDSOUTDIR} --tree NanoAOD --year {YEAR} --mcc dps-ww/fullRun2/lepchoice-ttH-FO.txt --WA prescaleFromSkim --mcc dps-ww/fullRun2/mcc-METFixEE2017.txt {fmca} {fcut} --amc --threshold 0.01 --split-factor=-1 --unc {fsyst}  {varName} '.format(lumi=lumis[year],CARDSOUTDIR=targetdir, trees=trees, fmca=fmca, fcut=fcut,YEAR=year if year !='all' else '2016,2017,2018',fsyst=fsyst,varName=varToFit) #--asimov signal 

    #    BDT_DPS_WZ 20,0,1.0

    cmd += ''.join(' -P '+Ptree for Ptree in trees)
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
        cmd  = "mcPlots.py {CF}  -j 10 -l {lumi} --tree NanoAOD --year {YEAR} --mcc dps-ww/fullRun2/lepchoice-ttH-FO.txt --WA prescaleFromSkim --mcc dps-ww/fullRun2/mcc-METFixEE2017.txt --pdir {td} {fmca} {fcut} {fplots} --split-factor=-1  ".format(lumi=lumis[year],td=targetdir, fmca=fmca, fcut=fcut, fplots=fplots,YEAR=year if year !='all' else '2016,2017,2018',CF='' if cutflow else '-f')


    if len(fsyst) > 0:
        cmd += ' --unc {fsyst} '.format(fsyst=fsyst)
    cmd += ''.join(' -P '+Ptree for Ptree in trees)
    cmd += ''.join(' --Fs {P}/'+frnd for frnd in friends)
    cmd += ''.join(' --FMCs {P}/'+frnd for frnd in MCfriends)
    cmd += ''.join(' --FDs {P}/'+frnd for frnd in Datafriends)
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
            cmd += ' -W L1PreFiringWeight_Nom*puWeight*leptonSF_3l *triggerSF_ttH(LepGood_pdgId[iLepFO_Recl[0]], LepGood_conePt[iLepFO_Recl[0]], LepGood_pdgId[iLepFO_Recl[1]], LepGood_conePt[iLepFO_Recl[1]],2,year)'
        else:
            cmd += ' -W L1PreFiringWeight_Nom*puWeight*leptonSF_4l *triggerSF_ttH(LepGood_pdgId[iLepFO_Recl[0]], LepGood_conePt[iLepFO_Recl[0]], LepGood_pdgId[iLepFO_Recl[1]], LepGood_conePt[iLepFO_Recl[1]],2,year)'
    else:
        #print 'dah'
        cmd += ''.join(" -W L1PreFiringWeight_Nom*puWeight")
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

##################
def makeResults(year,finalState,splitCharge,doWhat,applylepSFs,binningSch,blinded):
    trees       = [baseDir+'{here}'.format(here=year if year != 'all' else '')]
    fsyst       = 'dps-ww/fullRun2/systsUnc.txt'
    showratio   = True
    cutflow     = False     
    loop        = ['minusminus', 'plusplus'] if splitCharge else ['']
    print 'running for %s with charge split flag %s' %(finalState,splitCharge)
    processes_QCDscale=['WZ','WZ_scaleV0','WZ_scaleV1','WZ_scaleV3','WZ_scaleV4','WZ_scaleV5','WZ_scaleV7','WZ_scaleV8']#
    processesdYCR=['WZ_incl','ZZ','DY','Top','WW','data_fakes','data','promptsub']
    processes = ['DPSWW','WZ','ZGToLLG','WG','Rares','WZ_mllLT4','ZZ','data_fakes','data_flips','DPSWW_alt','data']#,'WZ_ewk']#'Convs01J
    #,'promptsub']#'WZTo3LNu_ewk','DPSWW_newsim']'WZ_alt',
    fRvars    = ['data_fakes_FRe_pt_Up','data_fakes_FRe_pt_Dn','data_fakes_FRe_be_Up','data_fakes_FRe_be_Dn','data_fakes_FRm_pt_Up','data_fakes_FRm_pt_Dn','data_fakes_FRm_be_Up','data_fakes_FRm_be_Dn','data_fakes_FRe_norm_Up','data_fakes_FRe_norm_Dn','data_fakes_FRm_norm_Up','data_fakes_FRm_norm_Dn','promptsub_FRe_norm_Up','promptsub_FRe_norm_Dn','promptsub_FRe_pt_Up','promptsub_FRe_pt_Dn','promptsub_FRe_be_Up','promptsub_FRe_be_Dn']#,'DPSWW_jecDn','DPSWW_jecUp','WZ_jecDn','WZ_jecUp']#,
    if blinded:
        showratio   = False 
        processes.remove('data')
    else:
        print 'plots will be made with data points on top of the stack'
    processes+=fRvars+processes 
    print processes    
    #procs=[x+'_promptsub' for x in processes if not x.startswith('data')] 
    binningBDT = binningSchemes[binningSch]
    spam    = ' --topSpamSize 1.0 --noCms '
    legends = ' --legendFontSize 0.04 --legendBorder 0 --legendWidth  0.62 --legendColumns 3 '
    ubands  =  ' --showMCError ' 
    exclude = '' # '--xu DPSWW_shape' if year == "2018" or year == "all" else ' '
    ratio   = ' --fixRatioRange  --ratioYNDiv 505 --maxRatioRange  0.5 1.75' #  --plotmode norm --ratioDen DPSWW --ratioNums DPSWW_newsim,DPSWW_hg --ratioYLabel=hw,ns/py8.' # --plotmode nostack --ratioDen WZ --ratioNums WZ_scaleV1,WZ_scaleV2,WZ_scaleV3,WZ_scaleV4,WZ_scaleV5,WZ_scaleV6 --ratioYLabel=var./nom.' 
    extraopts = ratio + spam + legends + ubands  + exclude
    disable   = [];    invert    = [];    fittodata = [];    scalethem = {}

    for FS in finalState:
        binName = FS if  re.search(r'^\d',FS) else '2lss'
        fmca        = 'dps-ww/fullRun2/mca-{here}.txt'.format(here='dpsww' if binName == '2lss' else 'mc-3l')
        ##binName   = '2lss' if re.search(r'mu\b',FS) else FS ->ll_noee and ll will be missed
        fcut        = 'dps-ww/fullRun2/cuts_{here}.txt'.format(here=binName)
        targetcarddir = 'Cards/cards_{date}{pf}_{FS}_{year}'.format(FS=(FS if binName == '2lss' else 'cr'+binName),year=year,date=date, pf=('-'+postfix if postfix else '') )
        targetdir = eos+'{yr}/{dd}{pf}{sf}_{bN}/'.format(dd=date,yr=year if year !='all' else 'fullRun2',pf=('_'+postfix if postfix else ''),sf='_withoutSFs' if not applylepSFs else '',bN=binName)

        if binName == '2lss':

            plotvars   = allvars
            for ch in loop:
                enable=[] #'noTaus','ssWW'] #'deepCSVL']#'jetVeto'] #'newbVeto30''nVertH']
                enable.append(FS);
                if len(ch)>0 :                     enable.append(ch)
                makeplots  = ['{}_{}{}'.format(a,FS,ch)  for a in plotvars]
                bN=FS+year+(ch if ch else '')
                anything = "  --neglist '.*_promptsub.* -plotgroup data_fakes+=.*_promptsub.* ' --binname %s "%bN
                #.format(finalState=FS if 'll' not in FS else 'll_noee_ss' ) #  --fitData --flp data_fakes'#  --plotmode nostack' # -- uf"  --showIndivSigs --noStackSig #--neglist
                extraopts+= anything
                print 'plot settings:  ',extraopts
                if 'plots' in doWhat:
                    runPlots(trees, friends, MCfriends, Datafriends, targetdir, fmca, fcut, fsyst, fplots, enable, disable, processes, scalethem, fittodata,makeplots,showratio, applylepSFs, year, 2,extraopts,invert,cutflow)
                else:
                    extraoptscards=anything
                    runCards(trees, friends, MCfriends, Datafriends, targetcarddir, fmca, fcut, fsyst , binningBDT, enable, disable, processes, scalethem,applylepSFs,year,extraoptscards,invert)
        else:
            enable=[]
            makeplots= plwzCR if binName == '3l' else plzzCR
            #more= '--sp {sig}'.format(sig='WZ' if binName == '3l' else 'ZZ')
            anything = " --binname cr%s%s "%(year,binName)
            extraoptscards= anything #+more
            if 'plots' in doWhat:
                runPlots(trees, friends, MCfriends, Datafriends, targetdir, fmca, fcut, fsyst, fplots, enable, disable, processes, scalethem, fittodata,makeplots,showratio, applylepSFs,year, 2,extraopts,invert,cutflow)                
            else:
                runCards(trees, friends, MCfriends, Datafriends, targetcarddir, fmca, fcut, fsyst , binningBDT, enable, disable, processes, scalethem,applylepSFs,year,extraoptscards,invert)


########################################
def plotFRvars(year,finalState):
    baseDir     = '/eos/cms/store/cmst3/group/dpsww/NanoTrees_v7_dpsww_skim2lss/'
    trees      = [baseDir+'{here}'.format(here=year if year != 'all' else '')]
    #friends     = ['3_tauCount', 'dpsbdt_all']
    #MCfriends   = ['3_recl_allvars','3_scalefactors_fixed','0_jmeUnc_v2']
    #Datafriends = ['2_recl']
    fmca        = 'dps-ww/fullRun2/mca-2lss-data-frdata-vars.txt'
    fsyst       = '' #dps-ww/fullRun2/systsUnc.txt'
    fcut        = 'dps-ww/fullRun2/cuts_2lss.txt' 

    showratio=False

    targetdir   = '/eos/user/a/anmehta/www/DPSWW_v2/{year}/{date}{pf}FRvars/'.format(date=date, year=year if year !='all' else 'fullRun2',pf=('-'+postfix if postfix else '')) 

    print 'running fr variation plots for  %s' %(finalState)


    processesM = ['data_fakes','data_fakes_m_up','data_fakes_m_down','data_fakes_m_be1','data_fakes_m_be2','data_fakes_m_pt1','data_fakes_m_pt2']
    fRElvars   = ['data_fakes_e_up','data_fakes_e_down','data_fakes_e_be1','data_fakes_e_be2','data_fakes_e_pt1','data_fakes_e_pt2']

    
    plotvars   =  bdtGM + all1Ds

    for FS in finalState:            
        enable=[]
        if FS != 'mumu':
            processes=processesM+fRElvars 
        else:
            processes=processesM
        enable.append(FS);
        disable   = []#'01jets','bVeto']
        invert    = []
        fittodata = []
        scalethem = {}
        ratio   = "--fixRatioRange  --ratioYNDiv 505 --maxRatioRange 0.5  1.55"
        spam    = ' --topSpamSize 1.0 --noCms '
        legends = ' --legendFontSize 0.04 --legendBorder 0 --legendWidth  0.62 --legendColumns 3 '
        anything = " --plotmode nostack" #  --ratioDen data_fakes --ratioNums data_fakes_m_up,data_fakes_m_down,data_fakes_m_be1,data_fakes_m_be2,data_fakes_m_pt1,data_fakes_m_pt2,data_fakes_e_up,data_fakes_e_down,data_fakes_e_be1,data_fakes_e_be2,data_fakes_e_pt1,data_fakes_e_pt2"
        extraopts = ratio+spam+legends+anything

        makeplots1  = ['{}_{}'.format(a,FS) for a in plotvars]
            
        
        makeplots=makeplots1 #+makeplots2
        print makeplots1
        runPlots(trees, friends, MCfriends, Datafriends, targetdir, fmca, fcut, fsyst, fplots, enable, disable, processes, scalethem, fittodata,makeplots,showratio, False, year, 2,extraopts,invert,False)



############################################ plots using barenano/gen/dressed leptons

def makesimpleplots(year,finalState,splitCharge,useDressed):
    trees       = '/eos/cms/store/cmst3/group/dpsww/Signal_nanoV7/All_gen/'
    MCfriends   = ['/eos/cms/store/cmst3/group/dpsww/Signal_nanoV7/All_gen/postFSRinfo'] 
    #['/eos/cms/store/cmst3/group/dpsww/putest2016_LooseSel/']#Summer16nanoaodV7/collection_merged_loosesel/']#collection_merger/']
    #targetdir   = '/eos/user/a/anmehta/www/DPSWW_v2/pileupChk/{date}{pf}_era{year}/'.format(date=date,year=year,pf=('-'+postfix if postfix else ''))
    targetdir   = '/eos/user/a/anmehta/www/DPSWW_v2/GeneratorLevel/{date}{pf}/'.format(date=date,pf=('-'+postfix if postfix else '') )
    fmca        = 'dps-ww/fullRun2/mca-dpsww-gen.txt' #mca-dpsww.txt' 
    fsyst       = ''
    fcut        = 'dps-ww/fullRun2/{cf}'.format(cf='cuts_2lss_dpsww_gen.txt' if not useDressed else 'cuts_2lss_dpsww_dressed.txt' )
    bareNano    = True
    cutFlow     = True
    if splitCharge: 
        loop = [ 'minusminus', 'plusplus']
    else:
        loop = [ '' ]

    print 'running for %s with charge split flag %s' %(finalState,splitCharge)
    processes = ['py8_cp5_bareNano','newsim_bareNano','hw7_2018_bareNano','hwpp_bareNano','py8_cuet_2017_bareNano','py8_cuet_bareNano']#,'py8_cp5_2017_bareNano','py8_cp5_2018_bareNano','hw7_2017_bareNano',
    #'py8_cuet_bareNano','py8_cp5_bareNano','hw7_bareNano','hwpp_bareNano','newsim_bareNano']#,'py8_notaus_cp5_bareNano']#,'py8_cp5_osWW_bareNano','py8_cuet_osWW_bareNano']#'DPSpy8','WZfxfx']#,'data']#,'DPSWW','WZ''WZ_incl','Wgstar','WZ_mllLT4','WgStarLNuEE','WgStarLNuMuMu','DPShwpp','WZ_pow',
    basicvars=['etaprod_phs_genlep','etaprod_nhs_genlep','dilep_flav_genlep','dilep_charge_genlep','dphilll2_genleps','dphill_genleps','etaprod_genleps','etasum_genleps','pt1_genleps','pt2_genleps','eta1_genleps','eta2_genleps','phi1_genleps','phi2_genleps','etasum_genleps','etaprod_genleps']#'asym_genlep','etaprod_phs_emin_genlep','etaprod_nhs_emin_genlep',
    # nWdaughters_sel']#'bnVert']#,'bdilep_flav']#,'bnLeps','bnMu','bnEl']#bnMuons','bsip3d','bdxy','bdz','bdeltazll']'mll_genleps'
    LLvars=['nLepGood']#,'bnVert']#,'bpt1','bpt2','bpt','beta1','beta2','beta']
    dressedLepvars    = ['pt1_dressedLep','eta1_dressedLep','pdgIdprod_dressedLep','pt2_dressedLep','eta2_dressedLep','mll_lower_dressedLep','mll_dressedLep','mll_low_dressedLep','ndressedLep','mll_high_dressedLep','pt_dressedLep','eta_dressedLep','etasum_dressedLep','etaprod_dressedLep','dilep_flav_dressedLep']#'mll_dressedLep_os','


    plotvars   = dressedLepvars if useDressed else basicvars # + LLvars
#using ll as final state actually invokes ll_noee cut because of reg exp. matching be careful!!

    for FS in finalState:            
        for ch in loop:
            enable=['noTaus','ssWW']#,'osWW']#'noTaudoters']#,'plusplus']#,'minusminus']'ssWW',
            enable.append(FS); 
            if len(ch)>0 : 
                enable.append(ch)
            print enable #list(ch) + list (finalState)
            disable   = []
            ratio   = ' --fixRatioRange  --ratioYNDiv 505 --maxRatioRange 0.8  1.2'
            spam    = ' --topSpamSize 1.0 --noCms '
            legends = ' --legendFontSize 0.04 --legendBorder 0 --legendWidth  0.62 --legendColumns 2 --plotmode norm'
            anything = ' --showRatio --ratioDen newsim_bareNano --ratioNums py8_cp5_bareNano,py8_cuet_2017_bareNano,py8_cuet_bareNano,py8_cp5_2017_bareNano,py8_cp5_2018_bareNano,hw7_2017_bareNano,hw7_2018_bareNano,hwpp_bareNano  --ratioYLabel=py,hw/dShr --uf ' # --plotmode norm' # --plotmode nostack' # rm --neg  --uf' # 
            extraopts = ratio + spam + legends +  anything
               
            
            if splitCharge:
                makeplots1  = ['{}_{}{}'.format(a,FS,ch)  for a in plotvars]
            else:
                makeplots1  = ['{}_{}'.format(a,FS) for a in plotvars]
            

            makeplots=makeplots1 
            print makeplots1
            simpleMCplots(trees,MCfriends,'',targetdir, fmca, fcut,fplots, enable, disable, processes,makeplots,year,extraopts,bareNano,cutFlow)


#%%%%%%%%%
def threelepCRPlot(year,wzbkg):
    print '=========================================='
    print 'running 3l control region  plots '
    print '=========================================='
    trees       = [baseDir+'{here}'.format(here=year if year != 'all' else '')]
    targetdir   = '/eos/user/a/anmehta/www/DPSWW_v2/ControlRegions/{date}{pf}_{year}_threelepCR/'.format(date=date, year=year,pf=('-'+postfix if postfix else ''))
    fmca        = 'dps-ww/fullRun2/mca-mc-3l.txt' #'dps-ww/fullRun2/mca-mc-3l.txt'
    fsyst       = 'dps-ww/fullRun2/systsUnc.txt'
    fcut        = 'dps-ww/fullRun2/cuts_3l.txt'
    showratio   = True
    applylepSFs = True

    processes = ['WZ','WZ_mllLT4','data','ZZ'] #'WZ_mllLT4''WZ_alt','Convs01J',
    if wzbkg :
        exclude =  '-- xu  WZ_norm --xu WZ_shape'
        enable    = ['pt251515','zsel','met_wz','exclusive','cleanup','tauveto','m3l_wz','bVeto','01j']
        fittodata = ['WZ']
    else:
        processes.append('Convs01J')
        processes.append('WZ_alt')
        fittodata = ['Convs01J']
        enable    = ['pt301010','met_zg','bVeto']
        exclude =  '-- xu  Conv_norm --xu Conv_shape1 --xu Conv_shape2'
        fittodata = ['Convs01J']#'ZZ','WZ','Convs01J','Rares']#'WG_wg',

    disable   = []
    if year == "2016":
        scalethem = {'ZZ':1.21}
    elif year == "2017":
        scalethem = {'ZZ':1.05}
    elif year == "2018":
        scalethem = {'ZZ':1.09}
    else:
        scalethem = {'ZZ':1.11}
    ratio   = ' --fixRatioRange  --ratioYNDiv 505 --maxRatioRange 0.0  1.99'
    spam    = ' --topSpamSize 1.0 --noCms '
    legends = ' --legendFontSize 0.04 --legendBorder 0 --legendWidth  0.62 --legendColumns 3 '
    ubands  = ' --showMCError '
    anything = " --binname 3l" #--fitData --flp WZ --sP tot_weight  " #scaleBkgToData--preFitData tot_weight --flp WZ --sP tot_weight --sp WZ " # --fitData  --flp WZ  "# --neglist '.*_promptsub.*' --plotgroup data_fakes+=.*_promptsub" # --preFitData tot_weight --plotmode norm" #to include neagitve evt ylds from fakes 
    extraopts = ratio + spam + legends + ubands + anything + exclude

    makeplots= ['conept1','conept2','conept3','met','mZ1','mZ2','mll_3l','cptll']+bdtGM 
    runPlots(trees, friends, MCfriends, Datafriends, targetdir, fmca, fcut, fsyst, fplots, enable, disable, processes, scalethem, fittodata,makeplots,showratio, applylepSFs,year, 3,extraopts)

def fourlepCRPlot(year):
    print '=========================================='
    print 'running 4l control region  plots'
    print '=========================================='
    trees       = [baseDir+'{here}'.format(here=year if year != 'all' else '')]
    targetdir   = '/eos/user/a/anmehta/www/DPSWW_v2/ControlRegions/{date}{pf}{year}_fourlepCR/'.format(date=date, year=year,pf=('-'+postfix if postfix else ''))
    fmca        = 'dps-ww/fullRun2/mca-mc-3l.txt'
    fsyst       = 'dps-ww/fullRun2/systsUnc.txt'
    fcut        = 'dps-ww/fullRun2/cuts_4l.txt'
    processes   = ['data','ZZ','WZ_incl','Rares']#,'ttjets','TTdilep','RaresGG']#'WZ_alt','WZ',
    enable      = []
    disable     = []
    fittodata   = ['ZZ']
    scalethem   = {} #{'WZ':1.1}
    showratio   = True
    applylepSFs = True
    exclude     =  '-- xu  ZZ_norm --xu ZZ_shape1 --xu ZZ_shape2 --xu WZ_norm --xu WZ_shape'
    ratio   = ' --fixRatioRange  --ratioYNDiv 505 --maxRatioRange 0.0  1.99'
    spam    = ' --topSpamSize 1.0 --noCms '
    legends = ' --legendFontSize 0.04 --legendBorder 0 --legendWidth  0.62 --legendColumns 3 '
    ubands  = ' --showMCError '
    anything = " --binname 4l" # --plotmode norm" #to include neagitve evt ylds from fakes 
    allvars    = ['nLepFO','nLepTight','njets25','nBJetLoose25','nBJetMedium25','njets30']#'conept1','conept2','pt1','pt2','eta1','eta2','met','metphi','njets25','nBJetLoose25','nBJetMedium25','njets30','mll','mt2ll','mt1','mtll','etasum','etaprod','dphill','dphil2met','dphilll2','nVert','ptll','cptll'] #dilep_charge','puppimetphi','puppimet''tcharge1','tcharge2','MVA1','MVA2','minMVA','dilep_flav','phi1','phi2','MVA1','MVA2',
    makeplots= ['nBJetLoose25','nBJetMedium25','njets30','njets25','conept1','conept2','conept3','conept4','mZ1','mZ2','m4l','met']+bdtGM 
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
def runClosure(year,finalState,fakes):
    
    print '=========================================='
    print 'running closure test on {here}'.format(here='fakes WPs for MC are defined in fakeRate-2lss-frmc-qcd.txt' if fakes else 'flips')
    print '=========================================='

    baseDir     = '/eos/cms/store/cmst3/group/dpsww/NanoTrees_v7_dpsww_skim2lss/' if fakes else '/eos/cms/store/cmst3/group/dpsww/NanoTrees_v7_dpsww_04092020/'
    trees       = [baseDir+'{here}'.format(here=year if year != 'all' else '')]
    fmca        = 'dps-ww/fullRun2/mca-fakes-closure.txt' if fakes else 'dps-ww/fullRun2/mca-flips-closure.txt'
    fcut        = 'dps-ww/fullRun2/cuts_tlCR.txt' if fakes else 'dps-ww/fullRun2/cuts_2lss.txt'
    fsyst       = 'dps-ww/fullRun2/systsUnc.txt'
    applylepSFs = True
    targetdir = '/eos/user/a/anmehta/www/DPSWW_v2/Fakes/{date}{pf}_era{year}_{here}closure/'.format(here='fakes' if fakes else 'flips',date=date,year=year,pf=('-'+postfix if postfix else '') )
    #targetdir = '/eos/user/a/anmehta/www/DPSWW_v2/Fakes/{date}{pf}_era{year}_tlCR/'.format(date=date,year=year,pf=('-'+postfix if postfix else '') )

    cutflow     = False
    showratio   = False if fakes else True
    processes = ['wj_tl','wj'] if fakes else ['data_flips','Rares']#,'mc_flips']#'data_flips', #,'wjLO','wjLO_tl','wj_noM']#,'wj_LO','wj_LO_tl']'wjTT','data_tl']#
    disable   = []
    fittodata = []
    invert    = []
    scalethem = {}
    ratio   = ' --fixRatioRange  --maxRatioRange 0.5 1.5'
    spam    = ' --topSpamSize 1.0 --noCms '
    legends = ' --legendFontSize 0.04 --legendBorder 0 --legendWidth  0.62 --legendColumns 2 '
    ubands  = ' '
    if fakes:
        anything = ' --plotmode nostack' # --ratioDen wj --ratioNums wj_tl ' # --ratioDen data_flips --ratioNums Rares --ratioYLabel= obs./pred. '
    else:
        anything = ' --plotmode nostack  --ratioDen data_flips --ratioNums Rares --ratioYLabel= obs./pred. '

    extraopts = ratio + spam + legends + ubands + anything
    plots    = ['met','nLepFO','nLepTight','nBJetLoose25','njets30','conept1','conept2','eta1','eta2','met','mll','mt2ll','mt1','mtll','etasum','etaprod','dphill','dphil2met','dphilll2','nVert','ptll','cptll','MVA1','MVA2'] 

    plots_CR    = only + bdtGM +['met','conept1','conept2','eta1','eta2']#,'BDTG1d_fakes_amc_raw_SoB_diag']#'BDT_wz_amc','BDT_fakes','BDT_wz_pow','BDT_DPS_multiC','BDT_WZ_multiC','BDT_TL_multiC']#'BDTG1d_fakes_amc_withpt',
    for FS in finalState:
        enable=[]
        enable.append(FS); 
        makeplots=[ip + '_' + FS for ip in plots_CR]
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
        enable=['onlyMuons']
        #enable.append(FS); 
        makeplots=[ip + '_' + FS for ip in plots]
        simpleMCplots(trees,MCfriends,Datafriends,targetdir, fmca, fcut,fplots, enable, disable, processes,makeplots,year,extraopts,True)
########################

def tempResults(year,finalState,extra):
    trees       = [baseDir+'{here}'.format(here=year if year != 'all' else '')]
    fmca        = 'dps-ww/fullRun2/mca-dpsww.txt'
    fsyst       = '' #dps-ww/fullRun2/systsUnc.txt'
    fcut        = 'dps-ww/fullRun2/cuts_2lss.txt' #cuts_temp.txt' 
    showratio   = True
    targetdir   = '/eos/user/a/anmehta/www/DPSWW_v2/{year}/{date}{pf}/'.format(date=date, year=year if year !='all' else 'fullRun2',pf=('-'+postfix if postfix else '') ) 
    #processes = ['WZ','WZ_scaleV1','WZ_scaleV2','WZ_scaleV3','WZ_scaleV4','WZ_scaleV5','WZ_scaleV6']#
    #processes = ['DPSWW','DPSWW_newsim','DPSWW_hg']#,'DPSWW_nojets']
    processes = ['DPSWW','DPSWW_alt']#,'data_fakes','Convs01J','Rares','WZ_mllLT4','ZZ','data_fakes','data_flips']#,'DPSWW_hg','WZ_alt','data']
    #processes = ['DPSWW','WZ']#,'Convs01J','Rares','WZ_mllLT4','ZZ','data_fakes','data_flips']#,'DPSWW_hg','WZ_alt','data']
    #processes = ['WZ','WZ_alt']
    print processes

    cutflow=False

    applylepSFs=True
    for FS in finalState:            
        enable=[]#'ssWW','noTaus'] #'nVertH']
        enable.append(FS);
        disable   = []#'01jets']#'cptll','01jets','bVeto','metpt']
        invert    = []
        fittodata = []
        ratio   = ' --fixRatioRange  --ratioYNDiv 505 --maxRatioRange 0.5  1.75    --plotmode norm   --ratioDen DPSWW --ratioNums DPSWW_alt   --ratioYLabel=var./nom.' # --plotmode nostack --ratioDen WZ --ratioNums WZ_scaleV1,WZ_scaleV2,WZ_scaleV3,WZ_scaleV4,WZ_scaleV5,WZ_scaleV6 --ratioYLabel=var./nom.' --plotmode norm --ratioDen DPSWW --ratioNums WZ,WpWpJJ --ratioYLabel=bkg./sig.--ratioDen WZ --ratioNums WZ_alt DPSWW_newsim,
        spam    = ' --topSpamSize 1.0 --noCms '
        legends = ' --legendFontSize 0.04 --legendBorder 0 --legendWidth  0.62 --legendColumns 3 '
        #ratio   = ' --fixRatioRange  --ratioYNDiv 505 --maxRatioRange 0.5  1.75 --plotmode nostack --ratioDen WZ --ratioNums WZ_scaleV1,WZ_scaleV2,WZ_scaleV3,WZ_scaleV4,WZ_scaleV5,WZ_scaleV6 --ratioYLabel=var./nom.'
            
        ubands  =  ' ' 
        exclude = ' ' # '--xu DPSWW_shape' if year == "2018" or year == "all" else ' '
        anything = ''
        extraopts = ratio + spam + legends + ubands + anything + exclude
        plotvars   =   bdtGM #bdtG2d #allvars + bdtGM + all1Ds #bdtGvarsUp + bdtGvarsDn + allbdts #['BDTG1d_fakes_amc_raw_SoB_sqV3'] #BDTG1d_fakes_amc_raw_SoB_sq']
        makeplots  = ['{}_{}'.format(a,FS) for a in plotvars]
        scalethem={}    
        
        runPlots(trees, friends, MCfriends, Datafriends, targetdir, fmca, fcut, fsyst, fplots, enable, disable, processes, scalethem, fittodata,makeplots,showratio, applylepSFs, year, 2,extraopts,invert,cutflow)


if __name__ == '__main__':
    parser = optparse.OptionParser(usage='usage: %prog [opts] ', version='%prog 1.0')
    parser.add_option('--pf', '--postfix', dest='postfix' , type='string', default='', help='postfix for running each module')
    parser.add_option('-d', '--date', dest='date' , type='string', default='', help='run with specified date instead of today')
    #    parser.add_option('-l', '--lumi', dest='lumi' , type='float'  , default=1.    , help='change lumi by hand')
    parser.add_option('--onelepCR',dest='onelepCR', action='store_true', default=False , help='make plots in single lep CR')
    parser.add_option('--wzCR',dest='threelepCR', action='store_true', default=False , help='make plots in 3lep CR')
    parser.add_option('--zzCR',dest='fourlepCR', action='store_true' , default=False , help='make plots in 4lep CR')
    parser.add_option('--finalState',dest='finalState',type='string' , default=[], action="append", help='final state(s) to run on')
    parser.add_option('--extra',dest='extra',type='string' , default='', help='additional cuts/settings')

    parser.add_option('--splitCharge',dest='splitCharge',action='store_true', default=False , help='split by charge')
    parser.add_option('--year',   dest='year'  , type='string' , default='' , help='make plots/cards for specified year')
    parser.add_option('--wzbkg',dest='threesome', action='store_true' , default=False, help='make plots in 3lep CR enriched with WZ otherwise dominated by conversions')
    parser.add_option('--results' , '--makeResults'  , dest='results', action='store_true' , default=False , help='make plots')
    parser.add_option('--old' , dest='old', action='store_true' , default=False , help='make plots')
    parser.add_option('--dW' , '--doWhat'  , dest='doWhat', type='string' , default=[] , help='plots or cards')
    parser.add_option('--dpsww',dest='dpsww', action='store_true' , default=False , help='make plots for signal')
    ##    parser.add_option('--analysis',dest='analysis', type='string',default='dps' , help='cut file to be used')
    parser.add_option('--simple', dest='simple', action='store_true' , default=False , help='make simple plots ')
    parser.add_option('--postFSR',dest='postFSR',action='store_true', default=True , help='use postFSR')
    parser.add_option('--fC', dest='runClosure', action='store_true' , default=False , help='FR closure test')
    parser.add_option('--fakes',dest='usefakes', action='store_true' , default=False, help='run closure test for fakes otherwise on flips')
    ##    parser.add_option('--unskimmed', dest='unskimmed', action='store_true' , default=False , help='chk ntuples before 2lss skimming')
    parser.add_option('--applylepSFs',dest='applylepSFs', action='store_true', default=False , help='apply lep id/iso SFs')
    parser.add_option('--genD',dest='genDressed', action='store_true' , default=False , help='2lss using dressed leptons')
    parser.add_option('--frV',dest='frVars', action='store_true' , default=False , help='plot FR variations')
    parser.add_option('--binning',dest='binningSch', type='string' , default='', help='binning scheme for datacards')
    parser.add_option('--temp', dest='temp', action='store_true' , default=False , help='make temp plots ')
    parser.add_option('--runblind', dest='blinded', action='store_true' , default=False , help='make plots without datat points')
    #parser.add_option('--sel', dest='binName', type='string' , default='2lss' , help='selection: 2lss/3l/4l')
    (opts, args) = parser.parse_args()

    global date, postfix, date
    postfix = opts.postfix
    year= opts.year
    date = datetime.date.today().isoformat()

    if opts.date:
        date = opts.date
    if opts.threelepCR:
        threelepCRPlot(opts.year,opts.threesome)
    if opts.fourlepCR:
        fourlepCRPlot(opts.year)
    if opts.onelepCR:
        onelepCRPlot(opts.year,opts.finalState)
    if opts.results:
        print 'running {here} for {bin}' .format(here=opts.doWhat,bin=opts.finalState)
        makeResults(opts.year,opts.finalState,opts.splitCharge,opts.doWhat,opts.applylepSFs,opts.binningSch,opts.blinded)
    if opts.dpsww:
        dpsww(opts.finalState,opts.year)
    if opts.old:
        makeResults_oldMaps(opts.year,opts.finalState,opts.splitCharge)
    if opts.simple:
        makesimpleplots(opts.year,opts.finalState,opts.splitCharge,opts.genDressed)
    if opts.runClosure:
        runClosure(opts.year,opts.finalState,opts.usefakes)
        #    if opts.genDressed:
        #       makeResultsDressedLep(opts.year,opts.finalState,opts.splitCharge)
    if opts.frVars:
        plotFRvars(opts.year,opts.finalState)
    if opts.temp:
        tempResults(opts.year,opts.finalState,opts.extra)
# python runDPS.py --results --dW plots --year 2016 --finalState elmu --finalState mumu --applylepSFs
# python runDPS.py --results --dW plots --year all --finalState ll_noee  --applylepSFs
# python runDPS.py --results --dW cards --year 2016 --finalState elmu --finalState mumu --applylepSFs --splitCharge
# python runDPS.py --year 2016 --finalState ll --genD
# python runDPS.py --dyCR --year 2017 --finalState mumu --finalState elmu --finalState elel --applylepSFs
# python runDPS.py --unskimmed --year 2017 --finalState elmu --finalState mumu
# python runDPS.py --fC --fakes --year 2016 --finalState elmu --finalState mumu 
# python runDPS.py --fC --year 2016 --finalState elmu 
# python runDPS.py --wzCR --wzbkg --year 2016
# python runDPS.py --zzCR --year 2016

# python runDPS.py --frV --finalState elmu --finalState mumu --year 2016 
 
#python runDPS.py --genD --year 2018 --finalState ll_noee
#python runDPS.py --temp --year all --finalState ll_noee
# python runDPS.py --simple --year All_gen  --finalState ll
##am            if year == "2016":
##am                scalethem = {'ZZ':1.21,'WZ':1.09}
##am            elif year == "2017":
##am                scalethem = {'ZZ':1.05,'WZ':1.11}
##am            elif year == "2018":
##am                scalethem = {'ZZ':1.09,'WZ':1.14}
##am            else:
##am                scalethem = {'ZZ':1.11,'WZ':1.12}
##am    if binningSch == 'wz_nb13':
##am        binningBDT   = ' BDTG_DPS_WZ_amc_raw_withpt 13,-1.0,1.0'
##am    elif binningSch == 'wz_nb15':
##am        binningBDT   = ' BDTG_DPS_WZ_amc_raw_withpt 15,-1.0,1.0'
##am    elif binningSch == 'iwz':
##am        binningBDT   = ' BDTG_DPS_WZ_amc_raw_withpt [-1.0,-0.9,-0.8,-0.6,-0.45,-0.2,0,0.2,0.4,0.6,0.7,1.0]'
##am    elif binningSch == 'i1wz':
##am        binningBDT   = ' BDTG_DPS_WZ_amc_raw_withpt [-1.0,-0.9,-0.8,-0.6,-0.45,-0.3,-0.2,0,0.2,0.5,0.7,0.8,1.0]'
##am    elif  binningSch == 'diag':
##am        binningBDT   = ' unroll_2Dbdt_dps_SoBord_diag(BDTG_DPS_TLCR_raw_withpt,BDTG_DPS_WZ_amc_raw_withpt) 13,0.0,13.0'
##am    elif binningSch == 'diag_pc':
##am        binningBDT    = ' unroll_2Dbdt_dps_SoBord_diag_pc(BDTG_DPS_TLCR_raw_withpt,BDTG_DPS_WZ_amc_raw_withpt) 11,0.0,11.0'
##am    elif binningSch == 'SoBord_sqV3':        
##am        binningBDT   = ' unroll_2Dbdt_dps_SoBord_sqV3(BDTG_DPS_TLCR_raw_withpt,BDTG_DPS_WZ_amc_raw_withpt) 13,0.0,13.0'
##am    elif binningSch == 'SoBord_sqV2':        
##am        binningBDT   = ' unroll_2Dbdt_dps_SoBord_sqV2(BDTG_DPS_TLCR_raw_withpt,BDTG_DPS_WZ_amc_raw_withpt) 13,0.0,13.0'
##am    elif binningSch == 'SoBord_sqV1':        
##am        binningBDT   = ' unroll_2Dbdt_dps_SoBord_sqV1(BDTG_DPS_TLCR_raw_withpt,BDTG_DPS_WZ_amc_raw_withpt) 12,0.0,12.0'
##am    elif binningSch == 'sq':        
##am        binningBDT   = ' unroll_2Dbdt_dps_SoBord_sq(BDTG_DPS_TLCR_raw_withpt,BDTG_DPS_WZ_amc_raw_withpt) 10,0.0,10.0'
##am    elif binningSch == 'prod_20':        
##am        binningBDT   = '  BDTG_DPS_TLCR_raw_withpt*BDTG_DPS_WZ_amc_raw_withpt 20,-0.2,1.0'
##am    elif binningSch == 'prod_13':        
##am        binningBDT   = '  BDTG_DPS_TLCR_raw_withpt*BDTG_DPS_WZ_amc_raw_withpt 13,-0.2,1.0'
##am    else:
##am        binningBDT   = ' unroll_2Dbdt_dps_SoBord_sqV3(BDTG_DPS_TLCR_raw_withpt,BDTG_DPS_WZ_amc_raw_withpt) 13,0.0,13.0'

#binName = ['2lss' if re.search(r'mu\b',i) else i for i in fS]
