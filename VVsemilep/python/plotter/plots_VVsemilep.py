#!/usr/bin/env python
import optparse, subprocess, ROOT, datetime, math, array, copy, os, re, sys
import numpy as np
eos='/eos/user/a/anmehta/www/VVsemilep/'
afs_am=os.getcwd()+'/'
lumis = {
    '2016APV': '19.5',
    '2016': '16.8',
    '2017': '41.5',
    '2018': '59.7',
    'all' : '19.5,16.8,41.4,59.7',
}


baseDir      = '/eos/cms/store/cmst3/group/dpsww/vvsemilep/' 
ubaseDir     = '/eos/cms/store/cmst3/group/dpsww/vvsemilep/' #unskimmed
MCfriends   = ['2_recl'] #'2_recl_allvars','4_scalefactors','0_jmeUnc_v2','2_btag_SFs'] #,"postFSRinfo"]
Datafriends = ['2_recl']
friends     = []#'3_tauCount','dpsbdt_neu_ssnoeebkg_afacdps','dpsbdt_neu_ssnoeebkg_afacdps_unclEn']
fplots      = 'vvsemilep/fullRun2/plots.txt'
fmca        = 'vvsemilep/fullRun2/mca-vvsemilep.txt'
eventvars   = ['nVert','met','puppimet','ptWV'] #'ptZV''metphi','puppimetphi',

ak4jetvars = ['Jet1_qgl','Jet1_btagDeepFlavB','Jet1_btagCSVV2','Jet2_qgl','Jet2_btagDeepFlavB','Jet2_btagCSVV2','nJet30','Jet_pt','Jet_eta','Jet_mass','Jet1_pt','Jet1_eta','Jet1_mass','Jet2_pt','Jet2_eta','Jet2_mass','mjj','mt1']

MConly     = ['Jet1_hadronFlavour','Jet1_partonFlavour','Jet2_hadronFlavour','Jet2_partonFlavour']

ak8jetvars = ['nFatJet_wtagged','dRfjlep','FatJet2_tau21','dphifjlep','dphifjmet','FatJet_tau21','FatJet_pNetMD_Wtag']#'nFatJet','FatJet_pt','FatJet_eta','FatJet_pNet_mass','FatJet_sDrop_mass','FatJet_mass','FatJet_deepTagMD_WvsQCD','FatJet_deepTag_WvsQCD','FatJet_deepTag_ZvsQCD','FatJet_n2b1','FatJet_n3b1','FatJet_particleNetMD_QCD','FatJet_particleNetMD_Xbb','FatJet_particleNetMD_Xqq','FatJet_particleNet_QCD','FatJet_particleNet_WvsQCD','FatJet_tau21','FatJet_tau21_tau32','FatJet_pNetMD_Wtag']

ak8more   = ['FatJet_area','FatJet_btagCSVV2','FatJet_btagDDBvLV2','FatJet_btagDeepB','FatJet_deepTagMD_ZbbvsQCD','FatJet_deepTagMD_ZvsQCD','FatJet_deepTagMD_bbvsLight','FatJet_deepTag_QCD','FatJet_deepTag_QCDothers','FatJet_particleNet_ZvsQCD','FatJet_tau1','FatJet_tau2','FatJet_tau3','FatJet_tau4','FatJet_hadronFlavour','FatJet_nBHadrons','FatJet_nCHadrons','FatJet_tau32','FatJet_tau42']

lepvars     = ['neupz']#,'lep2_pt']#,'nLepGood','lep1_pt','

bdtiv      = ['conept1','conept2','met','mt2ll','mt1','mtll','etasum','etaprod','dphill','dphil2met','dphilll2']
allvars    = eventvars+lepvars

moreVars   = ['minMVA','nVert','nLepFO','nLepTight','eta1','eta2','etaprod_phs','etaprod_nhs','deltaz','dilep_charge','tcharge1','tcharge2','minMVA','dilep_flav','phi1','phi2','metphi','njets25','pt1','pt2','nBJetMedium25','deltaz','ptll','dR','deltaxy','deltaz','etadiff','etasum','etaprod_etamin','bnVert','nLepGood','dilep_flav'] #
exotic     = ['ptRatio1','ptRatio2','mZ1','mZ2','MVA_ptRatio','dxy1','dz1','sip3d1','dxy2','dz2','sip3d2','minMVA','maxMVA','LepGood1_motherid','LepGood2_motherid','fake_lepMVA1','fake_lepMVA2', 'LepGood1_genPartFlav_all','LepGood2_genPartFlav_all','LepGood1_tightId','LepGood2_tightId','LepGood1_cutBased','LepGood2_cutBased','LepGood1_mediumPromptId','LepGood1_mediumId','LepGood1_mvaFall17V2Iso','LepGood1_mvaFall17V2Iso_WPL','LepGood1_mvaId','LepGood2_mediumPromptId','LepGood2_mediumId','LepGood2_mvaFall17V2Iso','LepGood2_mvaFall17V2Iso_WPL','njets25','njets30','nBJetLoose25','nBJetMedium25'] 
MVAS      = ['minMVA','maxMVA']


dyCR      = ['mtll','conept1','conept2','met','njets30','nBJetLoose25','mll','cptll']
plwzCR    = ['m3l','mt3lnu','mtw_3l','m3l_M','mll_3l','mZ1','mZ_3l','conept1','conept2','conept3','met','mZ1','mZ2','mll_3l','cptll']
plzzCR    = ['m4l','mZ1','mZ2','conept1','conept2','conept3','conept4','mZ1','mZ2','m4l','met']


barelepvars=['etaprod_absetamin_genlep','etaprod_phs_genlep','etaprod_nhs_genlep','dilep_flav_genlep','dilep_charge_genlep','dphilll2_genlep','dphill_genlep','etaprod_genlep','etasum_genlep','pt1_genlep','pt2_genlep','eta1_genlep','eta2_genlep','phi1_genlep','phi2_genlep','etasum_genlep','etaprod_genlep','nGenlep']
dressedLepvars = ['dilep_flav_dressedlep','dilep_charge_dressedlep','pt_dressedlep','eta_dressedlep','ndressedLep','etasum_dressedlep','mll_dressedlep','cptll_dressedlep','etaprod_dressedlep']#,'etaprod_phs_dressedlep','etaprod_nhs_dressedlep','etaprod_etamin_dressedlep','etaprod_absetamin_dressedlep']
moredressedLepvars=['pt1_dressedlep','eta1_dressedlep','pdgIdprod_dressedlep','pt2_dressedlep','eta2_dressedlep','mll_lower_dressedlep','mll_dressedlep','mll_low_dressedlep','ndressedLep','mll_high_dressedlep','etasum_dressedlep','etaprod_dressedlep','mll_dressedlep_os']


#####################
def simpleMCplots(trees,MCfriends,Datafriends,targetdir, fmca, fcut,fplots, enabledcuts, disabledcuts, processes,plotlist,year,extraopts = '',bareNano=False,cutflow=False):

    if bareNano:
        cmd  = ' mcPlots.py {CF} -j 10 -l {lumi}  --tree NanoAOD  --year {YEAR} --pdir {td} {fmca} {fcut} {fplots} --split-factor=-1  -P {trees} '.format(td=targetdir, trees=trees, fmca=fmca, fcut=fcut, fplots=fplots,lumi=lumis[year],YEAR=year if year!='all' else '2016,2017,2018',CF='' if cutflow else '-f')

    else:
        cmd  = ' mcPlots.py {CF} -j 10 -l {lumi} --tree NanoAOD  --year {YEAR} --pdir {td} {fmca} {fcut} {fplots} --mcc vvsemilep/fullRun2/lepchoice-ttH-FO.txt --WA prescaleFromSkim --mcc vvsemilep/fullRun2/mcc-METFixEE2017.txt --split-factor=-1  -P {trees} '.format(td=targetdir, trees=trees, fmca=fmca, fcut=fcut, fplots=fplots,lumi=lumis[year],YEAR=year,CF='' if cutflow else '-f')


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


######################################

def runCards(trees, friends, MCfriends, Datafriends, targetdir, fmca, fcut, fsyst, plotbin, enabledcuts, disabledcuts, processes, scaleprocesses,applyWtsnSFs, year,nLep=2,extraopts = '',invertedcuts = []):
    varToFit= '{plotvar} {binning}'.format(plotvar=plotbin.split()[0], binning=plotbin.split()[1])

    cmd  = ' makeShapeCardsNew.py -f -j 8 -l {lumi} --od {CARDSOUTDIR} --tree NanoAOD --year {YEAR} --mcc vvsemilep/fullRun2/lepchoice-ttH-FO.txt --WA prescaleFromSkim --mcc vvsemilep/fullRun2/mcc-METFixEE2017.txt {fmca} {fcut} --amc --threshold 0.01 --split-factor=-1 --unc {fsyst}  {varName} '.format(lumi=lumis[year],CARDSOUTDIR=targetdir, trees=trees, fmca=fmca, fcut=fcut,YEAR=year if year !='all' else '2016,2017,2018',fsyst=fsyst,varName=varToFit) #--asimov signal 

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
    if applyWtsnSFs :
        if(nLep == 2): 
            cmd += ''.join(" -W l1muonprefire_sf*L1PreFiringWeight_Nom*btagSF_shape*puWeight*leptonSF_2lss *triggerSF_ttH(LepGood_pdgId[iLepFO_Recl[0]], LepGood_conePt[iLepFO_Recl[0]], LepGood_pdgId[iLepFO_Recl[1]], LepGood_conePt[iLepFO_Recl[1]],2,year)")
        elif(nLep == 3):
            cmd += ' -W l1muonprefire_sf*L1PreFiringWeight_Nom*btagSF_shape*puWeight*leptonSF_3l *triggerSF_ttH(LepGood_pdgId[iLepFO_Recl[0]], LepGood_conePt[iLepFO_Recl[0]], LepGood_pdgId[iLepFO_Recl[1]], LepGood_conePt[iLepFO_Recl[1]],2,year)'
        else:
            cmd += ' -W l1muonprefire_sf*L1PreFiringWeight_Nom*btagSF_shape*puWeight*leptonSF_4l *triggerSF_ttH(LepGood_pdgId[iLepFO_Recl[0]], LepGood_conePt[iLepFO_Recl[0]], LepGood_pdgId[iLepFO_Recl[1]], LepGood_conePt[iLepFO_Recl[1]],2,year)'
    else:
        #print 'dah'
        cmd += ''.join(" -W l1muonprefire_sf*L1PreFiringWeight_Nom*btagSF_shape*puWeight")


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

#####################################
def runPlots(trees, friends, MCfriends, Datafriends, targetdir, fmca, fcut, fsyst, fplots, enabledcuts, disabledcuts, processes, scaleprocesses, fitdataprocess, plotlist, showratio, applyWtsnSFs, year,nLep,extraopts = '', invertedcuts = [],cutflow=False,bareNano=False):

    if bareNano:
        cmd  = ' mcPlots.py {CF} -j 10 -l {lumi}  --tree NanoAOD  --year {YEAR} --pdir {td} {fmca} {fcut} {fplots} --split-factor=-1  -P {trees} '.format(td=targetdir, trees=trees, fmca=fmca, fcut=fcut, fplots=fplots,lumi=lumis[year],YEAR=year if year!='all' else '2016APV,2016,2017,2018',CF='' if cutflow else '-f')
    else:    
        cmd  = "mcPlots.py {CF}  -j 10 -l {lumi} --tree NanoAOD --year {YEAR} --mcc vvsemilep/fullRun2/lepchoice-ttH-FO.txt --WA prescaleFromSkim --mcc vvsemilep/mcc-METFixEE2017.txt --pdir {td} {fmca} {fcut} {fplots} --split-factor=-1  ".format(lumi=lumis[year],td=targetdir, fmca=fmca, fcut=fcut, fplots=fplots,YEAR=year if year !='all' else '2016APV,2016,2017,2018',CF='' if cutflow else '-f') # -L ttH-multilepton/functionsTTH.cc

    if len(fsyst) > 0:
        cmd += ' --unc {fsyst} '.format(fsyst=fsyst)
    cmd += ''.join(' -P '+Ptree for Ptree in trees)
    cmd += ''.join(' --Fs {P}/'+frnd for frnd in friends)
    cmd += ''.join(' --FMCs {P}/'+frnd for frnd in MCfriends)
    cmd += ''.join(' --FDs {P}/'+frnd for frnd in Datafriends)
    cmd += ''.join(' -E ^'+cut for cut in enabledcuts )
    cmd += ''.join(' -X ^'+cut for cut in disabledcuts)
    #cmd += ' '.join(["--plotgroup data_fakes%s+='.*_promptsub%s'"%(x,x) for x in processes if 'data' not in x])+" --neglist '.*_promptsub.*' "
    if invertedcuts:
        cmd += ''.join(' -I ^'+cut for cut in invertedcuts )

    cmd += ' --sP '+','.join(plot for plot in plotlist)
    cmd += ' -p '+','.join(processes)

    if applyWtsnSFs and not bareNano:
        if(nLep == 1): 
            cmd += ''.join(" -W L1PreFiringWeight_Nom*puWeight*triggerSF_ttH(LepGood_pdgId[iLepFO_Recl[0]], LepGood_pt[iLepFO_Recl[0]], LepGood_pdgId[iLepFO_Recl[0]], LepGood_pt[iLepFO_Recl[0]],1,year,suberaId)")
        else: 
            cmd += ''.join(" -W L1PreFiringWeight_Nom*puWeight*triggerSF_ttH(LepGood_pdgId[iLepFO_Recl[0]], LepGood_pt[iLepFO_Recl[0]], LepGood_pdgId[iLepFO_Recl[1]], LepGood_pt[iLepFO_Recl[1]],2,year,suberaId)")
    else:
        if not bareNano:
            cmd += ''.join(" -W puWeight*L1PreFiringWeight_Nom")
        else: print' there are bare nanoaods so no scale factors whatsoever are applied'
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

def makeResults(year,nLep,finalState,doWhat,applylepSFs,blinded,plotvars=lepvars[0],postfix=''):
    trees        = [baseDir+'{here}'.format(here=year if year != 'all' else '')]
    fsyst        = ''#'vvsemilep/fullRun2/systsUnc.txt' 
    showratio    = False #True
    cutflow      = False
    fplots       = 'vvsemilep/fullRun2/plots.txt'
    fcut         = 'vvsemilep/fullRun2/cuts_vvsemilep.txt'
    fmca         = 'vvsemilep/fullRun2/mca-vvsemilep.txt'
    #processes    = ['ZV']#,'WV']#,'WJetsLO','TTSemi','T_sch','T_tch','Tbar_tch','data','lhefdy','htbdy','TTJets','Tbar_tWch']
        #processes    = ['WV','WJetsLO','TTSemi','T_sch','T_tch','Tbar_tch','data','Tbar_tWch']
    #processes     = ['ZV','TTJets','data','DYJetsLO'] if nLep > 1 else ['WV','WJetsLO','TTJets','T_sch','T_tch','Tbar_tch','data','Tbar_tWch']
    processes     = ['test','WJtest']#'WV','WJetsHT','TTJets']#,'data', 'T_sch','T_tch','Tbar_tch','data','Tbar_tWch'] #'TTSemi','DYJetsLO']
    cuts_onelep   = ['singlelep']#,'puppimet']
    cuts_2los     = ['2los','etael2','cleanup','ll'] #for now aall flavors 
    if blinded:
        showratio   = False
        fsyst=''
        processes.remove('data')
    else:
        print 'plots will be made with data points on top of the stack'

    
    #procs=[x+'_promptsub' for x in processes if not x.startswith('data')] 
    print processes
    signal  = '--sp ZV' if nLep > 1 else '--sp WV'
    spam    = ' --topSpamSize 1.0 --noCms '
    legends = ' --legendFontSize 0.04 --legendBorder 0 --legendWidth  0.62  --legendColumns 3 '
    #legends = ' --legendFontSize 0.04 --legendBorder 0 --legendWidth  0.32  --legendColumns 1 '
    ubands  =  ' --showMCError '
    exclude = '' #' --xu TTJets' if nLep ==1
    ratio   = ' --ratioYNDiv 505 --fixRatioRange --maxRatioRange 0.5 1.5 --plotmode norm' #--plotmode nostack --ratioNums DPSWW_newsim,DPSWW_hw --ratioDen DPSWW ' #-1 3 --plotmode norm --ratioDen DPSWW --ratioNums WZ' #  --plotmode norm --ratioDen DPSWW --ratioNums DPSWW_newsim,DPSWW_hg --ratioYLabel=hw,ns/py8.' # --plotmode nostack --ratioDen WZ --ratioNums WZ_scaleV1,WZ_scaleV2,WZ_scaleV3,WZ_scaleV4,WZ_scaleV5,WZ_scaleV6 --ratioYLabel=var./nom.' 
    extraopts = ratio + spam + legends + ubands  + exclude + signal
    disable   = [];    invert    = [];    fittodata = [];    scalethem = {}

    for FS in finalState:
        binName = '{lep}{jet}'.format(lep = '2los' if  nLep > 1 else 'onelep',jet=FS) ##will be used for datacards
        print 'running plots for %s'%binName
        targetcarddir = 'Cards/cards_{date}{pf}_{FS}_{year}'.format(FS=FS,year=year,date=date, pf=('-'+postfix if postfix else '') )
        targetdir = eos+'{yr}/{dd}{pf}{sf}_{bN}/'.format(dd=date,yr=year if year !='all' else 'fullRun2',pf=('_'+postfix if postfix else ''),sf='_withoutSFs' if not applylepSFs else '',bN=binName)
        enable=[];
        enable=cuts_2los if nLep > 1 else cuts_onelep
        enable.append(FS);
        #plotvars= allvars #['ndressedLep'] #asymvar #only #bdtGM if blinded else allvars 
        #plotvars=allvars+ak4jetvars if FS == "resolved" else allvars+ak8jetvars
        makeplots  = ['{}'.format(a)  for a in plotvars]
        print makeplots
        #if nLep >1:        
        #makeplots  = ['{}_ll'.format(a)  for a in plotvars] #lep flavs to be added
        #else:makeplots  = ['{}'.format(a)  for a in plotvars]
        print makeplots
        anything = "  --binname %s "%binName #--showIndivSigs
        extraopts+= anything
        print 'plot settings:  ',extraopts
        if 'plots' in doWhat:
            print 'gotta do'
            runPlots(trees, friends, MCfriends, Datafriends, targetdir, fmca, fcut, fsyst, fplots, enable, disable, processes, scalethem, fittodata,makeplots,showratio, applylepSFs, year, nLep,extraopts,invert,cutflow)
        else:
            extraoptscards=anything
            print 'nothing to do for now'
            #runCards(trees, friends, MCfriends, Datafriends, targetcarddir, fmca, fcut, fsyst,binningBDT, enable, disable, processes, scalethem,applylepSFs,year,2,extraoptscards,invert)
##am        else:
##am            enable=[]
##am            nlep=3 if binName == '3l' else 4
##am            makeplots= plwzCR if binName == '3l' else plzzCR
##am            more= '--xp Rares --xp WZ --xp VVV ' if binName == '4l' else ''
##am            anything = " --binname cr%s%s "%(binName,year)
##am            ratio   = ' --fixRatioRange  --ratioYNDiv 505 --fixRatioRange --maxRatioRange 0.5 2.0 '
##am            extraoptCRs= anything +more + ratio + spam + legends + ubands
##am            extraoptsCRcards=anything +more
##am            if 'plots' in doWhat:
##am                runPlots(trees, friends, MCfriends, Datafriends, targetdir, fmca, fcut, fsyst, fplots, enable, disable, processes, scalethem, fittodata,makeplots,showratio, applylepSFs,year, nlep,extraoptCRs,invert,cutflow)                
##am            else:
##am                runCards(trees, friends, MCfriends, Datafriends, targetcarddir, fmca, fcut, fsyst , binningBDT, enable, disable, processes, scalethem,applylepSFs,year,nlep,extraoptsCRcards,invert)


########################################
def makesimpleplots(year,finalState,splitCharge,useDressed=True):
    #trees="/eos/cms/store/cmst3/group/dpsww/NANOGEN/"
    #trees="/eos/cms/store/cmst3/group/dpsww/NANOGEN_v1/"
    trees       = '/eos/cms/store/cmst3/group/dpsww/bufferZone/Signal_nanoV7/All_gen/'
    MCfriends   = '' #['/eos/cms/store/cmst3/group/dpsww/bufferZone/Signal_nanoV7/All_gen/postFSRinfo'] 
    targetdir   = '/eos/user/a/anmehta/www/DPSWW_v2/GeneratorLevel/{date}{pf}/'.format(date=date,pf=('_dressed' if useDressed else '') )
    fmca        = 'vvsemilep/fullRun2/mca-dpsww-gen.txt' #mca-dpsww.txt' 
    fsyst       = ''
    fcut        = 'vvsemilep/fullRun2/{cf}'.format(cf='cuts_2lss_dpsww_gen.txt' if not useDressed else 'cuts_2lss_dpsww_dressed.txt' )
    bareNano    = True
    cutFlow     = True
    loop = [ 'minusminus', 'plusplus'] if splitCharge else ['']

    print 'running for %s with charge split flag %s' %(finalState,splitCharge)
    #processes = ['pdf13','pdf14','pdf17','pdf18','pdf5']   #
    processes = ['py8_all','hw_all','ns_all']
    #processes=['incl_dpsWW','excl_dpsWW']#'py8_cp5_bareNano','newsim_bareNano','hw7_2018_bareNano','hwpp_bareNano','py8_cuet_2017_bareNano','py8_cuet_bareNano']#,'py8_cp5_2017_bareNano','py8_cp5_2018_bareNano','hw7_2017_bareNano']

    plotvars   = dressedLepvars if useDressed else barelepvars 

    for FS in finalState:            
        for ch in loop:
            enable=[] #['noTaus','ssWW']#,'osWW']
            enable.append(FS); 
            if len(ch)>0 : 
                enable.append(ch)
            disable   = []
            ratio   = ' --fixRatioRange  --ratioYNDiv 505 --maxRatioRange 0.5  1.5'
            spam    = ' --topSpamSize 1.0 --noCms '
            legends = ' --legendFontSize 0.04 --legendBorder 0 --legendWidth  0.62 --legendColumns 2 --plotmode nostack'
            anything = '  ' #--showRatio --plotmode norm  --ratioNums incl_dpsWW --ratioDen excl_dpsWW' #--ratioDen py8_cuet_2017_bareNano --ratioNums py8_cp5_bareNano,newsim_bareNano,py8_cuet_bareNano,py8_cp5_2017_bareNano,py8_cp5_2018_bareNano,hw7_2017_bareNano,hw7_2018_bareNano,hwpp_bareNano  --ratioYLabel=py_cp5,hw,dSh/py_cuet' # --uf ' # --plotmode norm' # --plotmode nostack' # rm --neg  --uf' #  --ratioDen pdf13 --ratioNums pdf14,pdf5,pdf17,pdf18 --ratioYLabel=var/nom' 
            extraopts = ratio + spam + legends +  anything
               
            
            if splitCharge:
                makeplots1  = ['{}_{}{}'.format(a,FS,ch)  for a in plotvars]
            else:
                makeplots1  = ['{}_{}'.format(a,FS) for a in plotvars]
            

            makeplots=makeplots1 
            print makeplots1
            simpleMCplots(trees,MCfriends,'',targetdir, fmca, fcut,fplots, enable, disable, processes,makeplots,year,extraopts,bareNano,cutFlow)


#%%%%%%%%%
#########################




if __name__ == '__main__':
    parser = optparse.OptionParser(usage='usage: %prog [opts] ', version='%prog 1.0')
    parser.add_option('--pf', '--postfix', dest='postfix' , type='string', default='', help='postfix for running each module')
    parser.add_option('-d', '--date', dest='date' , type='string', default='', help='run with specified date instead of today')
    parser.add_option('-n', '--nLep', dest='nLep' , type='int'  , default=1.    , help='number of leps')
    parser.add_option('--finalState',dest='finalState',type='string' , default=[], action="append", help='final state(s) to run on')
    parser.add_option('--pv',dest='plotvar',type='string' , default=[], action="append", help='make these plots')
    parser.add_option('--vtp',dest='vtp',type='string' , default=[], action="append", help='variables to plot')
    parser.add_option('--dW' , '--doWhat'  , dest='doWhat', type='string' , default=[] , help='plots or cards')
    parser.add_option('--extra',dest='extra',type='string' , default='', help='additional cuts/settings')
    parser.add_option('--year',   dest='year'  , type='string' , default='' , help='make plots/cards for specified year')
    parser.add_option('--results' , '--makeResults'  , dest='results', action='store_true' , default=False , help='make plots')
    parser.add_option('--simple', dest='simple', action='store_true' , default=False , help='make simple plots ')
    parser.add_option('--postFSR',dest='postFSR',action='store_true', default=True , help='use postFSR')
    parser.add_option('--applylepSFs',dest='applylepSFs', action='store_true', default=False, help='apply lep id/iso SFs')
    parser.add_option('--runblind', dest='blinded', action='store_true' , default=False , help='make plots without datat points')

    (opts, args) = parser.parse_args()

    global date, postfix, date
    postfix = opts.postfix
    year= opts.year
    date = datetime.date.today().isoformat()

    if opts.date:
        date = opts.date
    if opts.results:
        print 'running {here} for {bin}' .format(here=opts.doWhat,bin=opts.finalState)
        makeResults(opts.year,opts.nLep,opts.finalState,opts.doWhat,opts.applylepSFs,opts.blinded,opts.plotvar,opts.postfix)
    if opts.simple:
        makesimpleplots(opts.year,opts.finalState,opts.splitCharge,opts.genDressed)
        #    if opts.fid:
        #       makeResultsFiducial(opts.year,opts.finalState,opts.splitCharge)


# python plots_VVsemilep.py --results --dW plots --year 2018 --nLep 2 --finalState boosted --finalState resolved --pv met --pf cutflow #--applylepSFs
# python plots_VVsemilep.py --results --dW plots --year 2016 --nLep 1 #--finalState 3l --applylepSFs
# python plots_VVsemilep.py --results --dW plots --year all --finalState ll --nlep 2 #  --applylepSFs
# python plots_VVsemilep.py --results --dW plots --year all --finalState ll --nlep 1 #  --applylepSFs
# python plots_VVsemilep.py --results --dW cards --year 2016 --finalState elmu --finalState mumu --applylepSFs 
# python plots_VVsemilep.py --results --dW cards --year 2016 --finalState 3l m3l --applylepSFs
# python plots_VVsemilep.py --results --dW cards --year 2016 --finalState 4l m4l --applylepSFs
