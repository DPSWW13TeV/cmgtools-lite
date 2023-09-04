#!/usr/bin/env python
import optparse, subprocess, ROOT, datetime, math, array, copy, os, re, sys
import numpy as np
eos='/eos/user/a/anmehta/www/VVsemilep/' ##save plots here
afs_am=os.getcwd()+'/'
lumis = {
    '2016APV': '19.5',
    '2016': '16.8',
    '2017': '41.5',
    '2018': '59.8',
    'all' : '19.5,16.8,41.5,59.8',
}
flavors = {
    'el': 'el',
    'mu': 'mu',
    'onelep': 'lep',
}
#HEM_affected_lumi_fraction = 0.64844705699  # (Run 319077 (17.370008/pb) + Run C + Run D) / all 2018
#https://hypernews.cern.ch/HyperNews/CMS/get/JetMET/2000.html 

baseDir     = '/eos/cms/store/cmst3/group/dpsww/NanoTrees_v9_vvsemilep_06012023/' #parent trees 
ubaseDir    = '/eos/cms/store/cmst3/group/dpsww/NanoTrees_v9_vvsemilep_06012023/' #unskimmed
MCfriends   = ['1_recl','4_scalefactors','1_jmeUnc']#,'ak8VtaggedV1_vars']#,'nnpdf_rms']#,'2_recl_allvars','2_btag_SFs'] #,"postFSRinfo"]
Datafriends = ['1_recl']
friends     = ['2_ak8Vtagged']
fplots      = 'vvsemilep/fullRun2/plots.txt'
fmca        = 'vvsemilep/fullRun2/mca-vvsemilep.txt'
eventvars   = ['nVert']
HEM=['puppimetphi','FatJet1_etaphi','eta1','phi1','etaphi1','FatJet1_phi','FatJet1_eta']
cutflow = ['puppimet1','mWV1_typ0_pmet_boosted','lep1_ptt','FatJet1_pNet_mass','FatJet1_ptt','FatJet1_pNetMD_Wtagscoret']
aTGC_chk=['aTGC_wt','aTGC_wt_neg','aTGC_wt_pos','aTGC_wt_SM','aTGC_wt1','aTGC_wt2','test_plot'] #
#theWVultimateset=['puppimet','puppimet_1','FatJet1_sDrop_mass','mWV_typ0_pmet_boosted','nBJetMedium30_Recl','nFatJet','FatJet1_pt','puppimetphi','lep1_pt','dphifjpmet','dphifjlep','ptWV_pmet','dphil1pmet','dphifjpmet','ptleppmet','neupzpmet_typ0','nJet30_Recl','lep1_eta','FatJet1_eta','FatJet1_mass','FatJet1_pNetMD_Wtagscore','FatJet1_tau21','FatJet1_pNet_mass']#,'FatJet1_pNetMD_Ztagscore','mWV_typ1_pmet_boosted','mWV_typ2_pmet_boosted','neupzpmet','neupzpmet_typ1','neupzpmet_typ2','neupzpmet_typ3','mt1pmet',','nLepGood','nLepFO',,'FatJet1_pNetMD_Wtagscore_wXbb','sumBoosted',
theWVultimateset=['puppimet','FatJet1_sDrop_mass','mWV_typ0_pmet_boosted','FatJet1_pt','puppimetphi','lep1_pt','ptWV_pmet','FatJet1_pNet_mass']


topCR=theWVultimateset+['sumBoosted','nFatJet']
ak4jetvars = ['nBJetLoose30_Recl,','nBJetMedium30_Recl','nJet30_Recl','Jet1_pt','Jet2_pt']#'htJet30','Jet1_qgl','Jet1_btagDeepFlavB','Jet1_btagCSVV2','Jet2_qgl','Jet2_btagDeepFlavB','Jet2_btagCSVV2','Jet1_pt','Jet2_pt','mjj','mt1']#'Jet1_eta','Jet1_mass','Jet2_eta','Jet2_mass','nJet30','htJet30j_Recl','mhtJet30_Recl',','htJet25j_Recl','mhtJet25_Recl',

MConly     = ['Mttbar']#genwhad_costcm','genwhad_costcs','genwhad_cost2d','genwhad_phics','genwhad_mt','genwhad_pt','genwhad_eta','genwhad_y','recoil_whad_x','recoil_whad_y','genwlep_costcm','genwlep_costcs','genwlep_cost2d','genwlep_phics','genwlep_mt','genwlep_pt','genwlep_eta','genwlep_y','recoil_wlep_x','recoil_wlep_y','nGenJetAK8','nGenJetAK8_ptgtp2k','GenJetAK8_pt','GenJetAK8_mass','GenmWV_typ0_pmet_boosted','GenDressedLeptonpt','GenMETphi','GenMET','Genptlepmet','Genptlepfj','Genmlepfj']#'Mttbar']#'sum_ttbar','pdgid1','pdgid2']#,'LHE_HT']#,'LHE_HT_log','LHE_HT_lin']#,'Jet1_hadronFlavour','Jet1_partonFlavour','Jet2_hadronFlavour','Jet2_partonFlavour']'LHE_Vpt']
dRchecks   = ['dR','dRfjj','dRjj','dRfjlep']
moreak8jetvars = ['dphifjmet','dphifjlep','dRfjlep']#'nFatJet_wtagged','FatJet1_tau21','FatJet1_sDrop_mass','FatJet1_pNet_mass','FatJet1_pt','FatJet1_pNetMD_Wtag','FatJet1_muonIdx3SJ_wtag','FatJet1_electronIdx3SJ_wtag','FatJet1_pNetMD_Wtag','FatJet1_eta','FatJet1_n2b1','FatJet1_n3b1','FatJet1_particleNetMD_QCD','FatJet1_particleNetMD_Xbb','FatJet1_particleNetMD_Xqq','FatJet1_particleNet_QCD','FatJet1_particleNet_WvsQCD','FatJet1_tau21','FatJet1_tau21_tau32','FatJet1_area','FatJet1_btagCSVV2','FatJet1_btagDDBvLV2','FatJet1_btagDeepB','FatJet1_deepTagMD_ZbbvsQCD','FatJet1_deepTagMD_ZvsQCD','FatJet1_deepTagMD_bbvsLight','FatJet1_deepTag_QCD','FatJet1_deepTag_QCDothers','FatJet1_particleNet_ZvsQCD','FatJet1_tau1','FatJet1_tau2','FatJet1_tau3','FatJet1_tau4','FatJet1_hadronFlavour','FatJet1_nBHadrons','FatJet1_nCHadrons','FatJet1_tau32','FatJet1_tau42']

lepvars     = ['nLepGood','lep1_pt','lep1_hpt','puppimet','ptleppmet']

moreWVvars=['ptWV_met','neupz','neupz_typ0','neupz_typ1','neupz_typ2','neupz_typ3','dphil1met','mt1','met','ptlepfj','mlepfj','dphifjlep','dphifjmet','mWV_typ0_met_boosted','mWV_typ1_met_boosted','mWV_typ2_met_boosted','mWV_typ3_met_boosted','metphi','dRfjlep','ptlepmet']

ZVvars     =  ['mll','lep2_pt','dilep_charge','dilep_flav','ptZV','ptll']
allvars    = eventvars+lepvars

exotic     = ['ptRatio1','ptRatio2','mZ1','mZ2','MVA_ptRatio','dxy1','dz1','sip3d1','dxy2','dz2','sip3d2','minMVA','maxMVA','LepGood1_motherid','LepGood2_motherid','fake_lepMVA1','fake_lepMVA2', 'LepGood1_genPartFlav_all','LepGood2_genPartFlav_all','LepGood1_tightId','LepGood2_tightId','LepGood1_cutBased','LepGood2_cutBased','LepGood1_mediumPromptId','LepGood1_mediumId','LepGood1_mvaFall17V2Iso','LepGood1_mvaFall17V2Iso_WPL','LepGood1_mvaId','LepGood2_mediumPromptId','LepGood2_mediumId','LepGood2_mvaFall17V2Iso','LepGood2_mvaFall17V2Iso_WPL','njets25','njets30','nBJetLoose25','nBJetMedium25'] 
MVAS      = ['minMVA','maxMVA']

wjest =['Lep1_pt','Lep1_eta','nSelak8Jets','nBJetMedium30','Selak8Jet_pt','Selak8Jet_eta','Selak8Jet_mass','Selak8Jet_particleNet_mass','Selak8Jet_pNetWtagscore','Selak8Jet_pNetZtagscore','nBJetMedium30','pmet','pmet_phi','mWV']

barelepvars=['etaprod_absetamin_genlep','etaprod_phs_genlep','etaprod_nhs_genlep','dilep_flav_genlep','dilep_charge_genlep','dphilll2_genlep','dphill_genlep','etaprod_genlep','etasum_genlep','pt1_genlep','pt2_genlep','eta1_genlep','eta2_genlep','phi1_genlep','phi2_genlep','etasum_genlep','etaprod_genlep','nGenlep']
dressedLepvars = ['dilep_flav_dressedlep','dilep_charge_dressedlep','pt_dressedlep','eta_dressedlep','ndressedLep','etasum_dressedlep','mll_dressedlep','cptll_dressedlep','etaprod_dressedlep']#,'etaprod_phs_dressedlep','etaprod_nhs_dressedlep','etaprod_etamin_dressedlep','etaprod_absetamin_dressedlep']
moredressedLepvars=['pt1_dressedlep','eta1_dressedlep','pdgIdprod_dressedlep','pt2_dressedlep','eta2_dressedlep','mll_lower_dressedlep','mll_dressedlep','mll_low_dressedlep','ndressedLep','mll_high_dressedlep','etasum_dressedlep','etaprod_dressedlep','mll_dressedlep_os']
###################
def if3(cond, iftrue, iffalse):
    return iftrue if cond else iffalse


#####################

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

def runPlots(trees, friends, MCfriends, Datafriends, targetdir, fmca, fcut, fsyst, fplots, enabledcuts, disabledcuts, processes, scaleprocesses, fitdataprocess, plotlist, showratio, applyWtsnSFs,applypNetSFs, year,nLep,extraopts = '', invertedcuts = [],cutFlow=False,bareNano=False):

    if bareNano:
        cmd  = ' mcPlots.py {CF} -j 10 -l {lumi}  --tree NanoAOD  --year {YEAR} --pdir {td} {fmca} {fcut} {fplots} --split-factor=-1  -P {trees} '.format(td=targetdir, trees=trees, fmca=fmca, fcut=fcut, fplots=fplots,lumi=lumis[year],YEAR=year if year!='all' else '2016APV,2016,2017,2018',CF='' if cutFlow else '-f')
    else:    
        cmd  = "mcPlots.py {CF}  -j 10 -l {lumi} --tree NanoAOD --year {YEAR} --mcc vvsemilep/fullRun2/lepchoice-ttH-FO.txt --WA prescaleFromSkim --mcc vvsemilep/mcc-METFixEE2017.txt --pdir {td} {fmca} {fcut} {fplots} --split-factor=-1  ".format(lumi=lumis[year],td=targetdir, fmca=fmca, fcut=fcut, fplots=fplots,YEAR=year if year !='all' else '2016APV,2016,2017,2018',CF='' if cutFlow else '-f') # -L ttH-multilepton/functionsTTH.cc

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
        #if applypNetSFs :pNetSF="pNetSFMD_WvsQCD(ak8pNMgt40_pt[0],year,suberaId,0)"
        if(nLep == 1): 
            if applypNetSFs:
                #cmd +=''.join(" -W evt_wt*lepsf ")
                cmd +=''.join(" -W L1PreFiringWeight_Nom*puWeight*lepsf *pNetSFMD_WvsQCD(ak8sDMgt40_pt[0],year,suberaId,0) *triggerSF_ttH(LepGood_pdgId[iLepFO_Recl[0]], LepGood_pt[iLepFO_Recl[0]], LepGood_pdgId[iLepFO_Recl[0]], LepGood_pt[iLepFO_Recl[0]], 1,year, suberaId)" )
            else:
                cmd +=''.join(" -W L1PreFiringWeight_Nom*puWeight*lepsf *triggerSF_ttH(LepGood_pdgId[iLepFO_Recl[0]], LepGood_pt[iLepFO_Recl[0]], LepGood_pdgId[iLepFO_Recl[0]], LepGood_pt[iLepFO_Recl[0]], 1,year, suberaId)" )
        else: 
            if applypNetSFs:
                cmd+=" '-W L1PreFiringWeight_Nom*puWeight*pNetSFMD_WvsQCD(ak8sDMgt40_pt[0],year,suberaId,0)*lepsf*triggerSF_ttH(LepGood_pdgId[iLepFO_Recl[0]], LepGood_pt[iLepFO_Recl[0]], LepGood_pdgId[iLepFO_Recl[1]], LepGood_pt[iLepFO_Recl[1]],2,year,suberaId) ' "
            else:
                cmd+=" '-W L1PreFiringWeight_Nom*puWeight*lepsf*triggerSF_ttH(LepGood_pdgId[iLepFO_Recl[0]], LepGood_pt[iLepFO_Recl[0]], LepGood_pdgId[iLepFO_Recl[1]], LepGood_pt[iLepFO_Recl[1]],2,year,suberaId) ' "
                

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
def makeResults(year,nLep,lepflav,finalState,doWhat,applylepSFs,blinded,selection,postfix,plotvars,cutflow):
    print "vorsichtig sein!! du hast tagging auswahl im top CR geloschen"
    trees        = [baseDir+'{here}'.format(here=year if year != 'all' else '')]
    fsyst        = 'vvsemilep/fullRun2/systsUnc.txt' if not cutflow else ''
    showratio    = True
    fplots       = 'vvsemilep/fullRun2/plots.txt'
    fcut         = 'vvsemilep/fullRun2/cuts_vvsemilep.txt'
    fmca         = 'vvsemilep/fullRun2/mca-vvsemilep.txt'
    processes   = ['WV','data','WJets','tt','singletop','higgs','QCD']
    #processes    = ['aTGC_WW_SM','aTGC_WZ_SM','aTGC_WW_SM_incl','aTGC_WZ','aTGC_WW','WW','WZ','aTGC_WW_cwww','aTGC_WW_cw','aTGC_WW_cb']
    #processes    = ['aTGC_WW_SM_incl','WW','WpWm_150to600','WpWm_600to800','WpWm_800toInf','WmWp_150to600','WmWp_600to800','WmWp_800toInf']#'aTGC_WW_SM','WZ','aTGC_WZ_SM',,'aTGC_WW','WW','aTGC_WW_SM_incl']#,'aTGC_WZ','data'] #'aTGC_WW_SM','aTGC_WZ_SM','aTGC_incl','data'] #,'WW','WZ','WJets','tt','singletop','higgs','QCD']#,TTSEMI'aTGC'] 'tt','tt_mtt1ktoinf','tt_mttp7kto1k','data',if nLep ==1 else ['lhefdy']#'ZV','data','lhefdy']##'TTJets','TTSemi','tthighmass'] #'data',['WW','aTGC']#'WW','aTGC','aTGC_incl']#
    #processes =['aTGC_WW_cwww','aTGC_WW_cw','aTGC_WW_cb','aTGC_WW_SM','WW']
    genprocesses = ['WJetsHT10','WJetsHT7','WJetsHT250','WJetsHT120','WJetsHT60','WJetsHT40','WJetsHT20','WJetsHT80']#,,'signal','testHT','testTT']
    cuts_boosted = ['filters','singlelep','ptWlep','dRfjlep','dphifjmet','dphifjlep','mWVtyp0pmet','etael1']
    cuts_onelep  = cuts_boosted + ['SR'] 
    cuts_2los    = ['dileptrg','etael2','cleanup','ll','oppsign','twolep','ptll','etael1'] #for now aall flavors 
    cuts_wjCR    = cuts_boosted+['wjCR']
    cuts_topCR   = cuts_boosted+['topCR']
    cuts_inclB   = cuts_boosted+['inclB']
    cuts_WJest   = ['WJEST']
    applypNetSFs = False 
    #procs=[x+'_promptsub' for x in processes if not x.startswith('data')] 
    print processes
    signal  = ''
    spam    = ' --topSpamSize 1.0 --noCms '
    legends = ' --legendFontSize 0.04 --legendBorder 0 --legendWidth  0.62  --legendColumns 3 '    
    legends_1col = ' --legendFontSize 0.025 --legendBorder 0 --legendWidth  0.3  --legendColumns 1 '
    ubands  =  ' --showMCError' # --noStackSig --showSigShape'
    exclude = ' '  #--xu CMS_vvsl18_pNetscore' 
    ratio   = ' --ratioYNDiv 505 --fixRatioRange --maxRatioRange 0.45 1.75' #  --plotmode norm --ratioDen WW --ratioNums aTGC,aTGC_incl' # --plotmode nostack --ratioNums DPSWW_newsim,DPSWW_hw --ratioDen DPSWW ' #-1 3 --plotmode norm --ratioDen DPSWW --ratioNums WZ' #  --plotmode norm --ratioDen DPSWW --ratioNums DPSWW_newsim,DPSWW_hg --ratioYLabel=hw,ns/py8.'
    #' --showSigShape --noStackSig --showIndivSigs 
    more = ' --plotmode norm' if cutflow else ''
    extraopts = ratio + spam + legends + ubands  + exclude + signal + more
    disable   = [];    invert    = [];    fittodata = [];    scalethem = {}
    ##amif cutflow: showratio =False; processes.remove('data')
    if blinded and 'data' in processes:
        showratio   = False
        fsyst=''
        processes.remove('data')
    for pR in selection:
        if "SR" in pR and 'data' in processes:  
            processes.remove('data')
            showratio   = False
            fsyst=''
        applypNetSFs=False if 'wjCR' in pR else True
        exclude = ' --xu CMS_vvsl18_pNetscore' if 'wjCR' not in pR else  ' '
        signal= if3(pR == 'SR',if3(nLep > 1,'--sp ZV','--sp aTGC_WW --sp aTGC_WZ'), if3('top' in pR, ' --sp tt --sp singletop', ' --sp WJets'))
        for LF in lepflav:
            lepSel= if3(LF == 'mu','muOnly',if3(LF == 'el','elOnly','trigger')) if not 'wjest' in pR else '1'
            for FS in finalState:
                binName = '{lep}{jet}'.format(lep=if3(nLep > 1,'2los',flavors[LF]),jet=FS)
                print 'running plots for %s'%binName
                targetcarddir = 'Cards/cards_{date}{pf}_{FS}_{year}'.format(FS=pR+FS,year=year,date=date, pf=('_'+postfix if postfix else '') )
                print '{yr}/{dd}_{bN}{sf}{pf}/'.format(dd=date,yr=year if year !='all' else 'fullRun2',pf=('_'+postfix if postfix else ''),sf='_withoutSFs' if not applylepSFs else '',bN=binName)
                targetdir = eos+'{yr}/{pR}/{dd}_{bN}{sf}{pf}/'.format(dd=date,yr=year if year !='all' else 'fullRun2',pf=('_'+'cutflow' if cutflow else '' + postfix if postfix else ''),sf='_withoutSFs' if not applylepSFs else '',bN=binName,pR=pR)
                enable=[]
                enable=cuts_WJest if 'wjest' in pR else if3(pR == 'SR',if3(nLep > 1,cuts_2los,cuts_onelep),if3(pR=='topCR',cuts_topCR,if3(pR=='wjCR',cuts_wjCR,cuts_inclB)))
                enable.append(lepSel); 
                if "wjCR" not in pR:    enable.append(FS); 
                makeplots  = ['{}'.format(a)  for a in plotvars]
                print makeplots
                anything = "  --binname %s "%binName #--showIndivSigs
                extraopts+= anything
                print 'plot settings:  ',extraopts
                if 'plots' in doWhat:
                    ##print 'gotta do'
                    runPlots(trees, friends, MCfriends, Datafriends, targetdir, fmca, fcut, fsyst, fplots, enable, disable, processes, scalethem, fittodata,makeplots,showratio, applylepSFs, applypNetSFs,year, nLep,extraopts,invert,cutflow)
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
##am                runPlots(trees, friends, MCfriends, Datafriends, targetdir, fmca, fcut, fsyst, fplots, enable, disable, processes, scalethem, fittodata,makeplots,showratio, applylepSFs,year, nlep,extraoptCRs,invert,cutFlow)                
##am            else:
##am                runCards(trees, friends, MCfriends, Datafriends, targetcarddir, fmca, fcut, fsyst , binningBDT, enable, disable, processes, scalethem,applylepSFs,year,nlep,extraoptsCRcards,invert)


#####################################


def alphaRatio(year,nLep,lepflav,finalState,applylepSFs,postfix,plotvars):
    trees        = [baseDir+'{here}'.format(here=year if year != 'all' else '')]
    fsyst        = 'vvsemilep/fullRun2/systsUnc.txt'
    showratio    = True
    fplots       = 'vvsemilep/fullRun2/plots.txt'
    fcut         = 'vvsemilep/fullRun2/cuts_vvsemilep.txt'
    fmca         = 'vvsemilep/fullRun2/mca-includes/mca-alphaR.txt'
    processes    = ['WJetsCR','WJetsSR']
    cuts_WV      = ['singlelep','trigger','ptWlep','dRfjlep','dphifjmet','dphifjlep','mWVtyp0pmet','bVeto','etael1']
    applypNetSFs = False
    cutflow      = False
    print processes
    signal  = ''
    spam    = ' --topSpamSize 1.0 --noCms '
    legends = ' --legendFontSize 0.04 --legendBorder 0 --legendWidth  0.42  --legendColumns 2 '    #legends = ' --legendFontSize 0.04 --legendBorder 0 --legendWidth  0.32  --legendColumns 1 '
    ubands  =  ' ' #--showMCError '
    exclude = '' #' --xu TTJets' if nLep ==1
    ratio   = ' --ratioYNDiv 505 --fixRatioRange --maxRatioRange 0.25 2.0 --plotmode norm --ratioNums WJetsSR --ratioDen WJetsCR --ratioYLabel=SR/CR' # --plotmode norm' # --plotmode nostack --ratioNums DPSWW_newsim,DPSWW_hw --ratioDen DPSWW ' #-1 3 --plotmode norm --ratioDen DPSWW --ratioNums WZ' #  --plotmode norm --ratioDen DPSWW --ratioNums DPSWW_newsim,DPSWW_hg --ratioYLabel=hw,ns/py8.'
    more = ' '
    extraopts = ratio + spam + legends + ubands  + exclude + signal + more
    disable   = [];    invert    = [];    fittodata = [];    scalethem = {}


    signal=  '--sp WJetsSR' 
    for LF in lepflav:
        lepSel= if3(LF == 'mu','muOnly',if3(LF == 'el','elOnly','trigger'))
        for FS in finalState:
            binName = '{lep}{jet}'.format(lep=if3(nLep > 1,'2los',flavors[LF]),jet=FS)
            print 'running plots for %s'%binName
            print '{yr}/{dd}_{bN}{sf}{pf}/'.format(dd=date,yr=year if year !='all' else 'fullRun2',pf=('_'+postfix if postfix else ''),sf='_withoutSFs' if not applylepSFs else '',bN=binName)
            targetdir = eos+'{yr}/alphaRatio/{dd}_{bN}{sf}{pf}/'.format(dd=date,yr=year if year !='all' else 'fullRun2',pf=('_'+'cutflow' if cutflow else '' + postfix if postfix else ''),sf='_withoutSFs' if not applylepSFs else '',bN=binName)
            enable=[];
            enable=cuts_WV #FS is enabled in the mca as it's CR vs SR. 
            enable.append(lepSel)
            makeplots  = ['{}'.format(a)  for a in plotvars]
            print makeplots
            anything = "  --binname %s "%binName #--showIndivSigs
            extraopts+= anything
            print 'plot settings:  ',extraopts
            runPlots(trees, friends, MCfriends, Datafriends, targetdir, fmca, fcut, fsyst, fplots, enable, disable, processes, scalethem, fittodata,makeplots,showratio, applylepSFs, applypNetSFs,year, nLep,extraopts,invert,cutflow)

########################################
def makesimpleplots(year,useDressed=True):
    #baseDir = '/eos/cms/store/cmst3/group/dpsww/testWJ_htbinned/'
    trees        = [baseDir+'{here}'.format(here=year if year != 'all' else '')]
    MCfriends   = ['2_toppT_rw']#genInfo'] #'2_toppT_rw']
    Datafriends = []
    friends     = []
    targetdir = '/eos/user/a/anmehta/www/VVsemilep/GenLevel/{date}{pf}/'.format(date=date,pf=('_dressed' if useDressed else '') )
    fmca        = 'vvsemilep/fullRun2/mca-includes/mca-mc.txt' #mca-semilep-gen.txt'
    fsyst       = ''
    fplots      = 'vvsemilep/fullRun2/plots.txt'
    fcut        = 'vvsemilep/fullRun2/cuts_vvsemilep_{cf}.txt'.format(cf='gen' if not useDressed else 'dressed' )
    bareNano    = False
    cutFlow     = False
    processes   = ['tt']#'WW','aTGC','aTGC_SM','aTGC_incl']##'WJetsToLNu']#'ttmtt1ktoinf','ttmttp7kto1k','ttsemi']#'WJetsToLNu']#'WW','aTGC']#'ttmtt1ktoinf','ttmttp7kto1k','Rwtttsemi']#'ttsemi']
    #'WJetsHT10','WJetsHT7','WJetsHT250','WJetsHT120','WJetsHT80','WJetsHT60','WJetsHT40','WJetsHT20']
    #cuts_onelep   = ['singlelep']
    disable   = [];    invert    = [];    fittodata = [];    scalethem = {}

    showratio=False
    applylepSFs=False
    nLep=1
    plotvars   = MConly #dressedLepvars if useDressed else barelepvars 

    disable   = []; enable=['ttbar','nQ']#'WhadpT','mWV','leadfatjet','fatjet','ptWlep','leadlep','etacutl1'] #'ttbar','nQ']
    ratio   = ' --fixRatioRange  --ratioYNDiv 505 --maxRatioRange 0.5  1.75'
    spam    = ' --topSpamSize 1.0 --noCms '
    legends = ' --legendFontSize 0.04 --legendBorder 0 --legendWidth  0.62 --legendColumns 2'
    anything = ' --showRatio   --showMCError --ratioNums aTGC,aTGC_SM,aTGC_incl --ratioDen WW --ratioYLabel=/SM(e) ' #--ratioDen py8_cuet_2017_bareNano --ratioNums py8_cp5_bareNano,newsim_bareNano,py8_cuet_bareNano,py8_cp5_2017_bareNano,py8_cp5_2018_bareNano,hw7_2017_bareNano,hw7_2018_bareNano,hwpp_bareNano  --ratioYLabel=py_cp5,hw,dSh/py_cuet' # --uf ' # --plotmode norm' # --plotmode nostack' # rm --neg  --uf' #  --ratioDen pdf13 --ratioNums pdf14,pdf5,pdf17,pdf18 --ratioYLabel=var/nom' 
    extraopts = ratio + spam + legends + anything
    makeplots  = ['{}'.format(a)  for a in plotvars]
    applypNetSFs=False
    #    runPlots(trees, friends, MCfriends, Datafriends, targetdir, fmca, fcut, fsyst, fplots, enable, disable, processes, scalethem, fittodata,makeplots,showratio, applylepSFs, applypNetSFs,year, nLep,extraopts,invert,cutflow)

    runPlots(trees, friends, MCfriends, Datafriends, targetdir, fmca, fcut, fsyst, fplots, enable, disable, processes, scalethem, fittodata,makeplots,showratio, applylepSFs,applypNetSFs, year, nLep,extraopts,invert,cutFlow)

#################################################################################
def testTreesforWJest(year):
    #baseDir = '/eos/cms/store/cmst3/group/dpsww/testWJ_htbinned/'
    trees        = [baseDir+'{here}'.format(here=year if year != 'all' else '')]
    #MCfriends   = []
    #Datafriends = []
    #friends     = ['testAM']
    targetdir   = '/eos/user/a/anmehta/www/VVsemilep/WJest/{year}/plots_{date}/'.format(year=year,date=date)
    fmca        = 'vvsemilep/fullRun2/mca-includes/mca-mc.txt' #mca-semilep-gen.txt'
    fsyst       = ''
    fplots      = 'vvsemilep/fullRun2/plots.txt'
    fcut        = 'vvsemilep/fullRun2/cuts_vvsemilep.txt'
    bareNano    = False
    cutFlow     = False
    processes   = ['WJets','WW','WZ','singletop','tt','data']
    #cuts_onelep   = ['singlelep']
    disable   = [];    invert    = [];    fittodata = [];    scalethem = {}
    showratio=False
    applylepSFs=False
    nLep=1
    plotvars   = wjest #dressedLepvars if useDressed else barelepvars 

    disable   = []; enable=['testwjCR']
    ratio     = ' --fixRatioRange  --ratioYNDiv 505 --maxRatioRange 0.5  1.75'
    spam      = ' --topSpamSize 1.0 --noCms '
    legends   = ' --legendFontSize 0.04 --legendBorder 0 --legendWidth  0.62 --legendColumns 2'
    anything  = ' --plotmode norm  --showMCError' # --ratioNums aTGC,aTGC_SM,aTGC_incl --ratioDen WW --ratioYLabel=/SM(e) ' #--ratioDen py8_cuet_2017_bareNano --ratioNums py8_cp5_bareNano,newsim_bareNano,py8_cuet_bareNano,py8_cp5_2017_bareNano,py8_cp5_2018_bareNano,hw7_2017_bareNano,hw7_2018_bareNano,hwpp_bareNano  --ratioYLabel=py_cp5,hw,dSh/py_cuet' # --uf ' # --plotmode norm' # --plotmode nostack' # rm --neg  --uf' #  --ratioDen pdf13 --ratioNums pdf14,pdf5,pdf17,pdf18 --ratioYLabel=var/nom' 
    extraopts = ratio + spam + legends +  anything
    makeplots  = ['{}'.format(a)  for a in plotvars]
    applypNetSFs=False


    runPlots(trees, friends, MCfriends, Datafriends, targetdir, fmca, fcut, fsyst, fplots, enable, disable, processes, scalethem, fittodata,makeplots,showratio, applylepSFs,applypNetSFs, year, nLep,extraopts,invert,cutFlow)

##############################################################################################



if __name__ == '__main__':
    parser = optparse.OptionParser(usage='usage: %prog [opts] ', version='%prog 1.0')
    parser.add_option('--pf', '--postfix', dest='postfix', type='string', default='', help='postfix for running each module')
    parser.add_option('-d', '--date', dest='date' , type='string', default='', help='run with specified date instead of today')
    parser.add_option('-n', '--nLep', dest='nLep' , type='int'  , default=1.    , help='number of leps')
    parser.add_option('--lf',dest='lepflav',type='string' , default=[], action="append", help='lep flav: el/mu/onelep')
    parser.add_option('--finalState',dest='finalState',type='string' , default=[], action="append", help='final state(s) to run on')
    parser.add_option('--pv',dest='plotvar',type='string' , default=[], action="append", help='make these plots')
    parser.add_option('--vtp',dest='vtp',type='string' , default=[], action="append", help='variables to plot')
    parser.add_option('--dW' , '--doWhat'  , dest='doWhat', type='string' , default=[] , help='plots or cards')
    parser.add_option('--extra',dest='extra',type='string' , default='', help='additional cuts/settings')
    parser.add_option('--year',   dest='year'  , type='string' , default='' , help='make plots/cards for specified year')
    parser.add_option('--results',dest='results', action='store_true' , default=False , help='make plots')
    parser.add_option('--alpha' , dest='alpha', action='store_true' , default=False , help='compute alpha Ratio')
    parser.add_option('--simple', dest='simple', action='store_true' , default=False , help='make simple plots ')
    parser.add_option('--WJest', dest='WJest', action='store_true' , default=False , help='make plots for wjest ')
    parser.add_option('--postFSR',dest='postFSR',action='store_true', default=True , help='use postFSR')
    parser.add_option('--applylepSFs',dest='applylepSFs', action='store_true', default=False, help='apply lep id/iso SFs')
    #    parser.add_option('--applypNetSFs',dest='applypNetSFs', action='store_true', default=False, help='apply pNet SFs')
    parser.add_option('--runblind', dest='blinded', action='store_true' , default=False , help='make plots without datat points')
    parser.add_option('--genD', dest='genDressed', action='store_true' , default=False , help='use dressed leptons for gen lvl plots')
    parser.add_option('--sel',dest='sel', action='append', default=[], help='make plots with SR/ttbarCR/incl')
    parser.add_option('--dCF',dest='dCF', action='store_true', default=False , help='cutflow with MC & plot shapes w/o uncert')

    (opts, args) = parser.parse_args()

    global date, postfix
    postfix = opts.postfix
    year= opts.year
    #print type(postfix)
    date = datetime.date.today().isoformat()

    if opts.date:
        date = opts.date
    if opts.results:
        print 'will make {here} {pt} for {bin}' .format(here=opts.doWhat,bin=opts.finalState,pt=(opts.plotvar if 'plots' in opts.doWhat else ''))
        #makeResults(year,nLep,finalState,doWhat,applylepSFs,blinded,selection,postfix,plotvars):
        makeResults(opts.year,opts.nLep,opts.lepflav,opts.finalState,opts.doWhat,opts.applylepSFs,opts.blinded,opts.sel,opts.postfix,opts.plotvar,opts.dCF)
    if opts.alpha:
        alphaRatio(opts.year,opts.nLep,opts.lepflav,opts.finalState,opts.applylepSFs,opts.postfix,opts.plotvar)
    if opts.WJest:
        testTreesforWJest(opts.year)
    if opts.simple:
        makesimpleplots(opts.year,opts.genDressed)
        #    if opts.fid:
        #       makeResultsFiducial(opts.year,opts.finalState,opts.splitCharge)


# python plots_VVsemilep.py --results --dW plots --year 2018 --nLep 1 --finalState boosted --pv FatJet1_pt --pv FatJet1_mass --pv FatJet1_particleNet_mass  --pf nom --sel wjCR --applylepSFs --lf onelep
# python plots_VVsemilep.py --results --dW plots --year 2018 --nLep 1 --finalState boosted --pv FatJet1_pt --pf nom --sel SR --applylepSFs --lf mu 
# python plots_VVsemilep.py --results --dW plots --year 2018 --nLep 1 --finalState boosted --pv phi1 --sel wjCR --applylepSFs --lf el 
# python plots_VVsemilep.py --results --dW plots --year 2016 --nLep 1 #--finalState 3l --applylepSFs
# python plots_VVsemilep.py --results --dW plots --year all --finalState ll --nlep 2 #  --applylepSFs
# python plots_VVsemilep.py --results --dW plots --year all --finalState ll --nlep 1 #  --applylepSFs
# python plots_VVsemilep.py --results --dW cards --year 2016 --finalState elmu --finalState mumu --applylepSFs 
# python plots_VVsemilep.py --results --dW cards --year 2016 --finalState 3l m3l --applylepSFs
# python plots_VVsemilep.py --results --dW cards --year 2016 --finalState 4l m4l --applylepSFs
#python plots_VVsemilep.py --results --dW plots --year 2018 --nLep 1 --finalState boosted --pv dRfjj 
# python plots_VVsemilep.py --results --dW plots --year 2018 --nLep 1 --finalState boosted --pv LHE_HT --pf chkHT
#python plots_VVsemilep.py --alpha --year 2018 --nLep 1 --finalState boosted --pv  mWV1_typ0_pmet_boosted --applylepSFs --lf mu
#python plots_VVsemilep.py --simple --genD --year 2018


#python plots_VVsemilep.py --results --finalState boosted --nLep 1 --sel SR --pv FatJet1_pt --applylepSFs --lf mu --year 2018 --dW plots
