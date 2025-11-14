#!/Usr/bin/env python
##NO tagger selection applied for W+jets CR, check before running the cards!!
import optparse, subprocess, ROOT, datetime, math, array, copy, os, re, sys
import numpy as np

lumis = {
    '2016APV'     : '19.5', #with HIPM /pre-vfp
    '2016'        : '16.8', #without HIPM
    '2017'        : '41.5',
    '2018'        : '59.8',
    'all'         : '19.5,16.8,41.5,59.8',
    'fullRun2'    : '19.5,16.8,41.5,59.8',
    'combo'       : '19.5,16.8',
#    'fullRun2'    : '19.5,16.8,41.5,59.8',
}
flavors = {
    'el': 'el',
    'mu': 'mu',
    'onelep': 'lep',
}
year_splits={
    'all': '2016,2016APV,2017,2018',
    'fullRun2':'2016,2016APV,2017,2018',
    'combo':'2016,2016APV'
}
scaleEFTylds={

    '2018':{
        'sb':{'WW':0.83,'WZ':1.16},
        'SR':{'WW':0.72,'WZ':0.9},
        'sig':{'WW':0.72,'WZ':0.9}
    },

    '2017':{
        'sb':{'WW':1.0,'WZ':1.01},
        'SR':{'WW':0.74,'WZ':0.92},
        'sig':{'WW':0.74,'WZ':0.92},
    },

    '2016':{
        'sb':{'WW':0.66,'WZ':0.98},
        'SR':{'WW':0.8,'WZ':0.8},
        'sig':{'WW':0.8,'WZ':0.8},
    },
    
    '2016APV':{
        'sb':{'WW':1.0,'WZ':1.0}, 
        'SR':{'WW':0.8,'WZ':0.85},
        'sig':{'WW':0.8,'WZ':0.85},
    },

    'fullRun2':{ 
        'sb':{'WW':0.89,'WZ':1.07},
        'SR':{'WW':0.75,'WZ':0.9},
        'sig':{'WW':0.75,'WZ':0.9}
    }

}


scaleSMEFTylds={

    '2018':{
        'sb':{'WW':1.19,'WZ':1.68},
        'sig':{'WW':0.86,'WZ':1.16}
    },

    '2017':{
        'sb':{'WW':1.21,'WZ':1.6},
        'sig':{'WW':0.89,'WZ':1.32},
    },

    '2016':{
        'sb':{'WW':1.4,'WZ':1.07},
        'sig':{'WW':0.85,'WZ':1.0},
    },
    
    '2016APV':{
        'sb':{'WW':1.4,'WZ':1.86}, 
        'sig':{'WW':1.02,'WZ':1.4},
    },

    'fullRun2':{  
        'sb':{'WW':1.21,'WZ':1.6},
        'sig':{'WW':0.89,'WZ':1.23}
    },

}

postfit_WJCR_rates={
    '2018':{
        'mu':{'WJets': 1.300,'ttbar':1.000},
        'el':{'WJets': 1.572,'ttbar':1.000},
},
    '2017':{
        'mu':{'WJets': 1.546,'ttbar':1.000},
        'el':{'WJets': 1.706,'ttbar':1.000},
},
    '2016':{
        'mu':{'WJets': 1.291,'ttbar':1.000},
        'el':{'WJets': 1.299,'ttbar':1.000},
    },
    '2016APV':{
        'mu':{'WJets': 0.951,'ttbar':1.000},
        'el':{'WJets': 1.218,'ttbar':1.000},
    },

    'fullRun2':{
        'mu':{'WJets': 1.300,'ttbar':1.000},
        'el':{'WJets': 1.572,'ttbar':1.000},
    }
}

#HEM_affected_lumi_fraction = 0.64844705699  # (Run 319077 (17.370008/pb) + Run C + Run D) / all 2018
#https://hypernews.cern.ch/HyperNews/CMS/get/JetMET/2000.html 
fitvars={
'mWV_binning_res'   : "mWV [950,1000,1058,1118,1181,1246,1313,1383,1455,1530,1607,1687,1770,1856,1945,2037,2132,2231,2332,2438,2546,2659,2775,2895,3019,3147,3279,3416,3558,3704, 3854, 4010, 4171, 4337, 4509,4550]",
'mWV_fixedbW'       : "mWV 36,950,4550",
'mWV'               : "mWV [950,1050,1150,1250,1350,1450,1550,1650,1750,1900,2100,2300,2500,2700,3000,4550]",  #3300
#'mWV'               : "mass_WV(Selak8Jet1_pt,Selak8Jet1_eta,Selak8Jet1_phi,Selak8Jet1_msoftdrop,Lep1_pt,Lep1_eta,Lep1_phi,pmet_pt,pmet_phi,0) [950,1050,1150,1250,1350,1450,1550,1650,1750,1900,2100,2300,2500,2700,3000,3300,4550]", 
'fjet_pt'           : "Selak8Jet1_pt [200,250,300,350,400,450,500,600,700,800,2000]",
'fjet_pt_fixedbW'   : "Selak8Jet1_pt 18,200,2000",
''                  : "mWV [950,1050,1150,1250,1350,1450,1550,1700,1900,2500,4550]"
}

baseDir     = '/eos/cms/store/cmst3/group/dpsww/NanoTrees_v9_vvsemilep_13112024_skimmed/' # parent trees 
ubaseDir    = '/eos/cms/store/cmst3/group/dpsww/NanoTrees_v9_vvsemilep_13112024/' #06012023/' #unskimmed parent trees
MCfriends   = ['1_recl','2_recl_allvars','4_scalefactors','2_jmeUnc','1_btag_SFs_fixedWP_v1',"3_eltrigsf_v1"]#,'nnpdf_rms'] #1_btag_SFs'
Datafriends = ['1_recl']
friends     = ['3_ak8_sdm45','0_wjest_v8']
fplots      = 'vvsemilep/fullRun2/plots.txt'
#fmca        = 'vvsemilep/fullRun2/mca-vvsemilep.txt'



####################variables for plotting 

eventvars   = ['nVert']
genvars_phi = ['jetphi_mWV','lephi_mWV','SeldLep1_pt','SelGak8Jet1_pt','SelGak8Jet1_mass','ttGenmWV_typ0_pmet_boosted','SeldLep1_eta','SeldLep1_phi','SeldLep1_pdgId','SeldLep1_pt_HF','SeldLep1_eta_HF','SeldLep1_phi_HF','nSeldLeps','SelGak8Jet1_pt','SelGak8Jet1_eta','SelGak8Jet1_phi','SelGak8Jet1_mass','SelGak8Jet1_pt_HF','SelGak8Jet1_eta_HF','SelGak8Jet1_phi_HF','SelGak8Jet1_mass_HF','nSelGak8Jets','neutrino_pt_HF','neutrino_phi_HF']    
HEM=['etaphi1','FatJet1_phi','FatJet1_eta','FatJet1_etaphi','eta1','phi1']
aTGC_chk   =['tmWV_typ0_pmet_boosted','Lep1_pt_vBins','Genptlepmet','tptleppmet','tmWV_typ0_pmet_boosted','tGenmWV_typ0_pmet_boosted','FatJet1_pt','tFatJet1_sDrop_mass','tptWV_pmet','nBJetLoose30_Recl','nBJetMedium30_Recl', 'aTGC_wt','aTGC_wt_neg','aTGC_wt_pos','aTGC_wt_SM','aTGC_wt1','aTGC_wt2','test_plot'] #
mWV=['ratio_typ0','ratio_typ1','ratio_typ2','ratio_typ3','mWV_typ0_pmet_boosted','mWV_typ01_pmet_boosted','mWV_typ10_pmet_boosted','mWV_typ11_pmet_boosted','mWV_typ20_pmet_boosted','mWV_typ21_pmet_boosted','mWV_typ30_pmet_boosted','mWV_typ31_pmet_boosted']
topCR=['mWV_typ0_met_boosted','FatJet1_pt','FatJet1_sDrop_mass']
bTag_eff=['Jet_eta_pt','Jet_partonFlavour','Jet_btagDeepFlavB','Jet_hadronFlavour','nJet30_Recl','nJet20','Jet_pt_eta']
missing=['Lep1_pt_logy']#FatJet1_pNetMD_Wtagscore']#'nBJetMedium30_Recl']

basics=['mWV_logy','mWV_den_logy']#'mWV','FatJet1_sDrop_mass_logy']

mWVs=['mWV_fitCR']#,'mWV_new','mWV_cards','mWV_res','mWV_fine','mWV','mWV_logy','mWV_fine_logy','mWV_res_logy','mWV_cards_logy','FatJet1_pNetMD_Wtagscore']
theWVultimateset=['dRfjlep','mtWlep','ptWlep','nBJetMedium30_Recl','FatJet1_pNetMD_Wtagscore','pmet_phi','nVert','dphifjpmet','dphifjlep','dphil1pmet']#,'FatJet1_eta','FatJet1_phi','mWV','mWV_den','nBJetLoose30_Recl']#,'Lep1_pt','FatJet1_pt','mWV','pmet','pmet_phi','nBJetLoose30_Recl','ptWV_pmet'],'FatJet1_sDrop_mass','mWV','FatJet1_pt'
fitCR=['mWV','mWV_logy']#,'mWV_res','mWV_fine',"mWV_fitCR","mWV_cards"] #'FatJet1_sDrop_mass','FatJet1_pt']
#,'dphijmet']##'nLepGood','nFatJet','nVert',,
theWVultimateset_log=['mWV_den_logy','mWV_logy','FatJet1_pt_logy','FatJet1_sDrop_mass_logy','Lep1_pt_logy','pmet_logy','ptWV_pmet_logy','mtWlep_logy','ptWlep_logy']
theWVultimateset_noWJ=['mt1pmet_nowj','mWV_nowj','FatJet1_sDrop_mass_nowj','FatJet1_pt_nowj','pmet_nowj']
ratios=['mWV_logy','FatJet1_pt_logy','FatJet1_sDrop_mass_logy','mWV_den_logy'] #'FatJet1_sDrop_mass_logy']'LHE_HT_mWV']#'

ak4jetvars = ['Jet1_phi_logy','Jet1_pt_logy','Jet1_eta_logy']
MConly     = ['mttbar','mttbar_logy']#'genwhad_costcm','genwhad_costcs','genwhad_cost2d','genwhad_phics','genwhad_mt','genwhad_pt','genwhad_eta','genwhad_y','recoil_whad_x','recoil_whad_y','genwlep_costcm','genwlep_costcs','genwlep_cost2d','genwlep_phics','genwlep_mt','genwlep_pt','genwlep_eta','genwlep_y','recoil_wlep_x','recoil_wlep_y','nGenJetAK8','nGenJetAK8_ptgtp2k','GenJetAK8_pt','GenJetAK8_mass','GenmWV_typ0_pmet_boosted','GenDressedLeptonpt','GenMETphi','GenMET','Genptlepmet','Genptlepfj','Genmlepfj','sum_ttbar','pdgid1','pdgid2','LHE_HT','LHE_HT_log','LHE_HT_lin','Jet1_hadronFlavour','Jet1_partonFlavour','Jet2_hadronFlavour','Jet2_partonFlavour','LHE_Vpt']
Wjets_ht   = ['LHE_HT','LHE_HT_log','LHE_Vpt_log','GenmWV_typ0_pmet_boosted','LHE_Vpt1_log'] #'LHE_HT_lin','LHE_Vpt'
dRchecks   = ['dR','dRfjj','dRjj','dRfjlep']
moreak8jetvars = ['dphifjmet','dphifjlep','dRfjlep','nFatJet_wtagged','FatJet1_tau21','FatJet1_sDrop_mass','FatJet1_pNet_mass','FatJet1_pt','FatJet1_pNetMD_Wtag','FatJet1_muonIdx3SJ_wtag','FatJet1_electronIdx3SJ_wtag','FatJet1_pNetMD_Wtag','FatJet1_eta','FatJet1_n2b1','FatJet1_n3b1','FatJet1_particleNetMD_QCD','FatJet1_particleNetMD_Xbb','FatJet1_particleNetMD_Xqq','FatJet1_particleNet_QCD','FatJet1_particleNet_WvsQCD','FatJet1_tau21','FatJet1_tau21_tau32','FatJet1_area','FatJet1_btagCSVV2','FatJet1_btagDDBvLV2','FatJet1_btagDeepB','FatJet1_deepTagMD_ZbbvsQCD','FatJet1_deepTagMD_ZvsQCD','FatJet1_deepTagMD_bbvsLight','FatJet1_deepTag_QCD','FatJet1_deepTag_QCDothers','FatJet1_particleNet_ZvsQCD','FatJet1_tau1','FatJet1_tau2','FatJet1_tau3','FatJet1_tau4','FatJet1_hadronFlavour','FatJet1_nBHadrons','FatJet1_nCHadrons','FatJet1_tau32','FatJet1_tau42']

leptons = ['Lep1_sip3d','Lep1_miniIso','Lep1_dxy','Lep1_dz','Lep1_relIso04','Lep1_relIso03'] #'Lep1_tightId',

###################
def if3(cond, iftrue, iffalse):
    return iftrue if cond else iffalse

#####################

def runCards(trees, friends, MCfriends, Datafriends, targetdir, fmca, fcut, fsyst, plotbin, enabledcuts, disabledcuts, processes, scaleprocesses,applyWtsnSFs, year,nLep,extraopts = '',invertedcuts = [],ncut=0):
    varToFit= '{plotvar} {binning}'.format(plotvar=plotbin.split()[0], binning=plotbin.split()[1]) #assumes WJ type frnds are being used  
    cmd = 'makeShapeCardsNew.py -f -j 8 -l {lumi} --od {CARDSOUTDIR} --tree NanoAOD --year {YEAR} --mcc vvsemilep/fullRun2/lepchoice-ttH-FO.txt  --mcc vvsemilep/fullRun2/mcc-METFixEE2017.txt  --WA hem_wt*prescaleFromSkim {fmca} {fcut}  --amc  --autoMCStatsThreshold 0 --threshold {ncut} --split-factor=-1 --unc {fsyst}  {varName}'.format(ncut=ncut,lumi=lumis[year],CARDSOUTDIR=targetdir, trees=trees, fmca=fmca, fcut=fcut,YEAR=year if year not in year_splits.keys()  else year_splits[year] ,fsyst=fsyst,varName=varToFit) #--asimov signal #--amc --threshold 0.01 --amc
    cmd += ''.join(' -P '+Ptree for Ptree in trees)
    cmd += ''.join(' --Fs {P}/'+frnd for frnd in friends)
    cmd += ''.join(' --FMCs {P}/'+frnd for frnd in MCfriends)
    cmd += ''.join(' --FDs {P}/'+frnd for frnd in Datafriends)
    cmd += ''.join(' -E ^'+cut for cut in enabledcuts )
    cmd += ''.join(' -X ^'+cut for cut in disabledcuts)
    cmd += ' -p '+','.join(processes)
    if invertedcuts:
        cmd += ''.join(' -I ^'+cut for cut in invertedcuts )
    if applyWtsnSFs: cmd+=" -W puWeight*L1PreFiringWeight_Nom*lepSF*btagSF*trgsf_mu*triggerSF_el "
    if scaleprocesses:
        for proc,scale in scaleprocesses.items():
            cmd += ' --scale-process {proc} {scale} '.format(proc=proc, scale=scale)
    if len(fsyst) > 0:        cmd += ' --unc {fsyst} '.format(fsyst=fsyst)
    if extraopts:        cmd += ' '+extraopts
    print ('=============================================================================================')
    print ('running: python', cmd)
    print ('=============================================================================================')
    subprocess.call(['python']+cmd.split())

#####################################
def runPlots(trees, friends, MCfriends, Datafriends, targetdir, fmca, fcut, fsyst, fplots, enabledcuts, disabledcuts, processes, scaleprocesses, fitdataprocess, plotlist, showratio, applyWtsnSFs, year,nLep,extraopts = ' ', invertedcuts = [],cutFlow=False,bareNano=False,doWJtypeplots=True):    
    cmd= ' mcPlots.py  -j 2  -l {lumi}  --tree NanoAOD  --year {YEAR} --pdir {td} {fmca} {fcut} {fplots} --split-factor=-1  -P {trees} --mcc vvsemilep/fullRun2/lepchoice-ttH-FO.txt --mcc vvsemilep/fullRun2/mcc-METFixEE2017.txt '.format(td=targetdir, trees=trees, fmca=fmca, fcut=fcut, fplots=fplots,lumi=lumis[year],YEAR=year if year not in year_splits.keys()  else year_splits[year])
    if not cutFlow:
        cmd+=''.join(' -f')
    if not bareNano:
        if doWJtypeplots:
            cmd+=" --WA hem_wt*prescaleFromSkim"
        else: 
            cmd+=" --WA prescaleFromSkim  "
    else:
        cmd+=" --WA prescaleFromSkim  "
    if len(fsyst) > 0:
        cmd += ' --unc {fsyst} '.format(fsyst=fsyst)
    cmd += ''.join(' -P '+Ptree for Ptree in trees)
    cmd += ''.join(' --Fs {P}/'+frnd for frnd in friends)
    cmd += ''.join(' --FMCs {P}/'+frnd for frnd in MCfriends)
    cmd += ''.join(' --FDs {P}/'+frnd for frnd in Datafriends)
    cmd += ''.join(' -E ^'+cut for cut in enabledcuts )
    cmd += ''.join(' -X ^'+cut for cut in disabledcuts)
    if invertedcuts:        cmd += ''.join(' -I ^'+cut for cut in invertedcuts )
    cmd += ' --sP '+','.join(plot for plot in plotlist)
    cmd += ' -p '+','.join(processes)
    if applyWtsnSFs and not bareNano:
        if doWJtypeplots:
            cmd+=" -W L1PreFiringWeight_Nom*puWeight*lepSF*btagSF*trgsf_mu*triggerSF_el "
        else:
            cmd+=" -W L1PreFiringWeight_Nom*puWeight*lepsf*btagSF*trgsf_mu*triggerSF_el " 
    else:
        if not bareNano:
            cmd += ''.join(" -W puWeight*L1PreFiringWeight_Nom")
        else: print(' there are bare nanoaods so no scale factors whatsoever are applied')
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

    print ('running: python', cmd)
    subprocess.call(['python']+cmd.split())#+['/dev/null'],stderr=subprocess.PIPE)


######################


##################
def makeResults(year,nLep,lepflav,finalState,doWhat,applylepSFs,blinded,selection,postfix,plotvars,cutflow,doWJ,notagger,smeft,proc,fitCR,postfitCR,fitCRwithcomb,WCs,varTofit,acP,acC):
    trees        = [baseDir+'{here}'.format(here=year  if year not in year_splits.keys() else '')] #['all','fullRun2'] else '')]
    fsyst        = 'vvsemilep/fullRun2/systsUnc.txt' if not cutflow else ''
    showratio    = True
    fcut         = 'vvsemilep/fullRun2/cuts_vvsemilep.txt' if not doWJ else 'vvsemilep/fullRun2/cuts_vvsemilep_wjet.txt' #
    fmca         = 'vvsemilep/fullRun2/mca-vvsemilep_smeft.txt' if smeft else 'vvsemilep/fullRun2/mca-vvsemilep_eft.txt'
    SMprocs      = ['tt','WJets','singletop','data','Others']#,'QCD'] ] 

    signal_proc=[];    morePs       =[]; mixedPs=[];
    if smeft:  #proc == "WV" or
        signal_proc=['WV']
        smeft=True
    else:
        signal_proc=['WW','WZ']
        smeft=False
    for i in signal_proc:
        SMprocs.append(i+"_sm")
        morePs.append(i+'_sm_lin_quad_'); morePs.append(i+'_quad_');
        mixedPs.append(i+'_sm_lin_quad_mixed_')
    print('SM procs',SMprocs)
    mixedOps     = []
    singleOps    = []
    Moreprocs    = []
    MMoreprocs    = []
    if 'singles' in WCs or 'all' in WCs:     
        if not smeft and  proc != "WV":
            WCs=['cw','c3w','cb','Odd_c3w','Odd_cw']
        else:
            WCs=["cW","cWtil","cHWB","cHWBtil","cHl3","cHd","cHu","cHj1","cHj3","cll1","cjj38","cju1","clu","clj3","cjj11","cjd1","clj1","cld","cjj18","cjj31","cju8","cjd8"]
    print(WCs)
    for op in WCs:
        if 'M' in op: 
            mixedOps.append(op.replace('M','_'))
            singleOps.append(op.partition('M')[0])
            singleOps.append(op.partition('M')[-1])            
        else:
            singleOps.append(op)
    
    print('running on these 1D operators',singleOps,'and mixed ops',mixedOps)
    if 'plots' in doWhat:
        for mop in mixedOps:
            Moreprocs+=[s + mop for s in mixedPs]
        for op in  singleOps:
            if not smeft:
                MMoreprocs+=[s + op for s in ['WW_sm_lin_quad_','WZ_sm_lin_quad_'] ] 
            else:
                MMoreprocs+=[s + op for s in ['WV_sm_lin_quad_'] ]

    processes=SMprocs+Moreprocs+MMoreprocs #all set for plotting 
    print(processes)
    genprocesses = ['WJetsHT10','WJetsHT7','WJetsHT250','WJetsHT120','WJetsHT60','WJetsHT40','WJetsHT20','WJetsHT80']#,,'signal','testHT','testTT']
    cuts_boosted = ['ptWlep','dRfjlep','dphifjmet','dphifjlep','mWVtyp0pmet','Mwvuppercut','Mjuppercut']
    cuts_btagEff = ['btagSR','bpartonFlav','Loosebtag','Medbtag','Tightbtag'] ##here for reference ['lightpartonFlav','cpartonFlav']
    bareNano    = False
    signal  = ''
    spam    = ' --topSpamSize 1.0 --noCms '    
    legends = ' --legendFontSize 0.026 --legendBorder 0 --legendWidth  0.62  --legendColumns 3 '
    ubands  =  ' --showMCError  --showIndivSigs --noStackSig --showSigShape'
    exclude = ' '
    ratio   = ' --ratioYNDiv 505 --fixRatioRange --maxRatioRange 0.25 2.0  '
    more    = ' ' # --plotmode nostack ' # --plotmode norm' if cutflow else ''
    extraopts = ratio + spam  + ubands  + exclude + signal + more
    disable   = [];    invert    = [];    fittodata = [];    scalethem = {}

    for pR in selection:
        if 'all' in WCs:
            legends = '  --legendFontSize 0.025 --legendBorder 0 --legendWidth  0.3  --legendColumns 1  '
        extraopts+= legends
        if 'topCR' in pR and fitCR:         fittodata.append('tt');
        if 'wj' in pR and fitCR:            fittodata.append('WJets');
        exclude = ' ' 
        #signal = if3(pR == 'sig','--sp .*c.* ', if3('topCR' in pR, ' --sp tt ', ' --sp WJets')) #separate CRs
        signal = if3(pR == 'sig','--sp .*c.* ',' --sp WJets') # combined CR-only fits 
        for LF in lepflav:
            if postfitCR:  
                #scalethem["WJets"]=postfit_WJCR_rates[year][LF]["WJets"]
                scalethem["WJets"]=1.12
                scalethem["tt"]=1.11
            for FS in finalState:
                binName = '{jet}_{lep}_{pR}'.format(lep=LF,jet=FS,pR=pR)
                print ('running %s for %s'%(doWhat,binName))
                postfix=('_'+postfix if postfix else '')+('_fittodata' if fitCR else '')+('_'+'cutflow' if cutflow else '')+('_noWJtype' if not doWJ else '')
                postfix+='_withoutTagger' if notagger else '' ##NEW
                postfix+='_postfitCR' if postfitCR else ''
                targetcarddir = 'Cards/cards_{date}{pf}_{FS}_{fv}_{year}'.format(FS=binName,year=year,date=date,fv=varTofit,pf=postfix)
                print ('{yr}/{dd}_{bN}{sf}{pf}/'.format(dd=date,yr=year if year !='all' else 'fullRun2',pf=postfix,sf='_withoutSFs' if not applylepSFs else '',bN=binName))
                enable=[]
                enable+= cuts_boosted 
                enable.append(LF); 
                enable.append(pR)
                #enable+=cuts_btagEff
                if not notagger:                    enable.append(FS);
                if 'top' not in pR: enable.append('bVeto');
                anything = "  --binname %s "%binName ##--pseudoData all, 
                extraopts+= anything
                if 'plots' in doWhat:
                    if len(acP) > 0: extraopts += ''.join(' -E ^'+cut for cut in acP )
                    if 'sig' in pR and 'data' in processes: # and blinded :  
                        processes.remove('data'); 
                        showratio   = False
                    elif  "top" in pR : extraopts+='  --xp .*quad.* ' #--xp Others  --xp QCD
                    elif  "wj" in pR: extraopts+= '   --xp .*quad.* ' #--xp Others  --xp QCD
                    makeplots  = ['{}'.format(a)  for a in plotvars]
                    print (makeplots)
                    print('running with samples',processes,pR,blinded)
                    targetdir = os.path.join(eos,'{yr}/{pR}/{dd}_{bN}{sf}{op}{basis}{pf}/'.format(basis='_smeft' if smeft else '_eft',op='_all' if len (WCs) > 0  else '',dd=date,yr=year if year !='all' else 'fullRun2',pf= postfix,sf='_withoutSFs' if not applylepSFs else '',bN=binName,pR=pR.split('_')[0]))
                    runPlots(trees, friends, MCfriends, Datafriends, targetdir, fmca, fcut, fsyst, fplots, enable, disable, processes, scalethem, fittodata, makeplots, showratio, applylepSFs, year, nLep,extraopts,invert,cutflow,bareNano,doWJ)

                else:
                    mWV_dist=" {here} ".format(here=fitvars[varTofit])
                    ncut=0 if "sig" in pR else 10.0
                    extraoptscards= ' '
                    if len(acC) > 0:extraoptscards+=''.join(' -E ^'+cut for cut in acC )
                    if fitCRwithcomb:
                        #print('im here wj',pR)
                        #add_set= " --xu CMS_top_pT_rwgt_shape --xu CMS_qcdscales_tt_ACCEPT --xu CMS_qcdscales_WJets   --xu CMS_qcdscales_WW_ACCEPT --xu CMS_qcdscales_WZ_ACCEPT  --sp WJets " #fitting CRs simult.
                        add_set= "  --xu CMS_top_pT_rwgt_shape  --xu CMS_qcdscales_WJets_ACCEPT --xu CMS_qcdscales_WW --xu CMS_qcdscales_WZ --xu CMS_qcdscales_WV --sp WV_sm --sp WW_sm --xp QCD --sp WZ_sm" #to run SM xsec meas
                        #if 'top' in pR:
                         #   print('im here',pR)
                         #   add_set= " --xu CMS_top_pT_rwgt --xu CMS_qcdscales_tt --xu CMS_qcdscales_WJets_ACCEPT  --xu CMS_qcdscales_WW_ACCEPT --xu CMS_qcdscales_WZ_ACCEPT --xu CMS_qcdscales_WV_ACCEPT --sp tt " ##for atcg 
                        #else: # "wj" in pR: 
                            #print('im here wj',pR)
                            #add_set= " --xu CMS_top_pT_rwgt_shape --xu CMS_qcdscales_tt_ACCEPT --xu CMS_qcdscales_WJets   --xu CMS_qcdscales_WW_ACCEPT --xu CMS_qcdscales_WZ_ACCEPT --xu CMS_qcdscales_WV_ACCEPT  --sp WJets "
                        processes=SMprocs  #to run SM xsec meas
                        binNamecards=binName+"_"+year
                        extraoptscards= ' --binname {bnc}  {more} '.format(bnc=binNamecards,more=add_set)
                        runCards(trees, friends, MCfriends, Datafriends, targetcarddir, fmca, fcut,fsyst, mWV_dist, enable, disable, processes, scalethem,applylepSFs,year,nLep,extraoptscards,invert,ncut)
                    else:
                        add_set=" --xu CMS_qcdscales_WJets_ACCEPT --xu CMS_qcdscales_tt_ACCEPT --xu CMS_top_pT_rwgt_shape  --xu CMS_qcdscales_WW --xu CMS_qcdscales_WZ --xu CMS_qcdscales_WV --sp WV_sm --sp WW_sm --xp QCD --sp WZ_sm --sp SM.* "
                    extraoptscards+=add_set
                    if len(WCs) > 0:
                        if len(mixedOps)>0:
                            for mop in mixedOps:
                                MoreMprocs=[];singleprocs=[];
                                binNamecards=binName+"_"+mop+"_"+year
                                MoreMprocs=[s + mop for s in mixedPs]
                                for op in singleOps:
                                    singleprocs+=[s + op for s in morePs  if len(op) > 0]
                                processes=SMprocs+singleprocs+MoreMprocs
                                print('for cards',processes)
                                extraoptscards= ' --binname {bnc}  {more}'.format(more=add_set, bnc=binNamecards)
                                print('used for mixed op',mop,processes)
                                runCards(trees, friends, MCfriends, Datafriends, targetcarddir, fmca, fcut,fsyst, mWV_dist, enable, disable, processes, scalethem,applylepSFs,year,nLep,extraoptscards,invert,ncut)
                        else: #look for single ops only if mixed ops are not there
                            for op in singleOps:
                                Moreprocs=[s + op for s in morePs  if len(op) > 0]                        
                                binNamecards=binName+"_"+op+"_"+year
                                processes=SMprocs+Moreprocs
                                print('to be used for op',op,processes)
                                extraoptscards= ' --binname {bnc}  {more} '.format(bnc=binNamecards,more=add_set)
                                runCards(trees, friends, MCfriends, Datafriends, targetcarddir, fmca, fcut,fsyst, mWV_dist, enable, disable, processes, scalethem,applylepSFs,year,nLep,extraoptscards,invert,ncut)
                    else:
                        binNamecards=binName+"_"+year                                                
                        extraoptscards= ' --xu signal_shape_WW --xu signal_shape_WZ --binname {bnc} {more} '.format(bnc=binNamecards,more=add_set)
                        runCards(trees, friends, MCfriends, Datafriends, targetcarddir, fmca, fcut,fsyst, mWV_dist, enable, disable, processes, scalethem,applylepSFs,year,nLep,extraoptscards,invert,ncut)
                                

#####################################
def alphaRatio(year,lepflav,plotvars):
    trees        = [baseDir+'{here}'.format(here=year  if year not in year_splits.keys() else '')] 
    fsyst        = 'vvsemilep/fullRun2/systsUnc.txt'
    showratio    = True
    fcut         = 'vvsemilep/fullRun2/cuts_vvsemilep_wjet.txt'
    fmca         = 'vvsemilep/fullRun2/mca-includes/mca-alphaR.txt'
    processes    = ['WJets_CR','WJets_SR','WJets_CR_hi','WJets_CR_lo']
    cuts_boosted = ['singlelep','ptWlep','dRfjlep','dphifjmet','dphifjlep','mWVtyp0pmet','Mjuppercut','Mwvuppercut']#'topCR_incl']
    cutflow      = False
    bareNano     = False
    applylepSFs  = True

    plotvars     = ['mWV','mWV_logy'] # #theWVultimateset_log+theWVultimateset
    print (processes)
    signal  = ''
    nLep    = 1 
    doWJ    = True 
    spam    = ' --topSpamSize 1.0 --noCms '
    legends = ' --legendFontSize 0.04 --legendBorder 0 --legendWidth  0.42  --legendColumns 2 '    #legends = ' --legendFontSize 0.04 --legendBorder 0 --legendWidth  0.32  --legendColumns 1 '
    ubands  =  ' --showMCError '
    exclude = '' #' --xu TTJets' if nLep ==1
    ratio   = ' --ratioYNDiv 505 --fixRatioRange --maxRatioRange 0.25 2.0 --plotmode norm --ratioDen WJets_SR --ratioNums WJets_CR,WJets_CR_lo,WJets_CR_hi --ratioYLabel=cr,lo,hi/sr' # --plotmode nostack
    more = ' '
    extraopts = ratio + spam + legends + ubands  + exclude + signal + more
    disable   = [];    invert    = [];    fittodata = [];    scalethem = {}
    signal=  '--sp WJets' 
    for LF in lepflav:
        binName = '{lep}boosted'.format(lep=LF)
        print ('running plots for %s'%binName)
        print ('{yr}/{dd}_{bN}{sf}{pf}/'.format(dd=date,yr=year  if year not in ['all','fullRun2']  else 'fullRun2',pf=('_'+postfix if postfix else ''),sf='_withoutSFs' if not applylepSFs else '',bN=binName))
        targetdir = os.path.join(eos,'{yr}/{dd}_{bN}{pf}_alphaRatio/'.format(dd=date,yr=year  if year not in ['all','fullRun2']  else 'fullRun2',pf=('_'+'cutflow' if cutflow else '' + postfix if postfix else ''),bN=LF))
        enable=[];
        enable+=cuts_boosted #FS is enabled in the mca as it's CR vs SR. 
        enable.append(LF)
        makeplots  = ['{}'.format(a)  for a in plotvars]
        anything = "  --binname %s "%binName #--showIndivSigs
        extraopts+= anything
        #runPlots(trees, friends, MCfriends, Datafriends, targetdir, fmca, fcut, fsyst, fplots, enable, disable, processes, scalethem, fittodata, makeplots, showratio, applylepSFs, year, nLep,extraopts,invert,cutflow,bareNano,doWJ)
        runPlots(trees, friends, MCfriends, Datafriends, targetdir, fmca, fcut, fsyst, fplots, enable, disable, processes, scalethem, fittodata,makeplots,showratio, applylepSFs, year, nLep,extraopts,invert,cutflow,bareNano,doWJ)

########################################
def makesimpleplots(year,sel,proc,smeft,sanitychk):
    useCorr = True
    trees       = [baseDir+'{here}'.format(here=year if year not in year_splits.keys() else '')] # if year not in ['all','fullRun2']  else '')]
    targetdir   = os.path.join(eos,'{yr}/{sel}/{date}_{proc}_{smeft}_{pf}/'.format(proc=proc,smeft='smeft' if smeft else 'eft' ,sel=sel[0].split('_')[0],yr=year,date=date,pf=('sanitychk_afterCorr' if sanitychk else 'SMvsEFT') ))
    if not useCorr:
        fmca        = 'vvsemilep/fullRun2/mca-includes/mca-mc.txt'
    else:
        fmca         = 'vvsemilep/fullRun2/mca-vvsemilep_eft.txt' if not smeft else 'vvsemilep/fullRun2/mca-vvsemilep_smeft.txt'
    fsyst       = '' #vvsemilep/fullRun2/systsUnc.txt'
    fcut        = 'vvsemilep/fullRun2/cuts_vvsemilep_wjet.txt' 
    bareNano    = False
    cutFlow     = False
    doWJtypeplots = True
    vetoplots=['WW_lin_cb','WW_lin_cHD','WW_lin_clu','WW_lin_cje','WW_lin_ceu','WW_lin_ced','WW_lin_cHl3','WW_lin_cHe','WW_lin_cHd','WW_lin_cHDD']

    WCs=['c3w'] #'cw','c3w','cb','Odd_c3w','Odd_cw']
    if smeft:
        WCs=[]#'cHDD', 'cW', 'cHWB', 'cHWBtil', 'cHWtil', 'cHd', 'cHe', 'cHj1', 'cHl1', 'cHl3', 'cHu', 'cWtil', 'ced', 'ceu', 'cje', 'cld', 'clj1', 'clj3', 'cll1', 'clu','cHj3']
    #procs=['WW_sm','WZ_sm','SM_WW','SM_WZ']
    procs=[];    Mprocs=[]; addNterms=''
    mmprocs=[];
    if smeft: 
        useThis="_smeftprod_"
        basic="_smeft_"
    else: 
        basic="_eft_HTbinned_"
        useThis="_eft_"
    if sanitychk:
        procs.append('SM_'+proc)
        Mprocs.append(proc+'_sm')
        #Mprocs.append(proc+useThis+'sm')
        #mmprocs.append(proc+"_sm")
        #Mprocs.append(proc+"_sm_gencorr")
        #Mprocs.append(proc+"_sm_pol1")
        #Mprocs.append(proc+"_sm_pol1_gencorr")
        #Mprocs.append(proc+"_eft_HTbinned") #EFT signal
        #Mprocs.append(proc+basic+'sm')
        #procs=['WW_smeft_sm','WZ_smeft_sm','SM_WW','SM_WZ','WW_eft_sm','WZ_eft_sm','WW_eft_HTbinned_sm','WZ_eft_HTbinned_sm','WZ_smeftprod_sm','WW_smeftprod_sm']
    else:
        procs.append('SM_'+proc)
        #procs.append('SMEFT_'+proc)
        Mprocs.append(proc+'_sm')
        #Mprocs.append('WW_sm')
        #Mprocs.append('WZ_sm')
        #Mprocs.append(proc+basic+'noCorr')
        #terms=['_lin_','_quad_']
        #Mprocs+=['SMEFT_WV_lin_cW','SMEFT_WV_quad_cW']
        #for op in  WCs:
         #   Mprocs+=[proc + s + op for s in terms  ] 
    addNterms=','.join(x for x in Mprocs)

    print(Mprocs)
    processes= procs+Mprocs+mmprocs
    disable   = [];    invert    = [];    fittodata = [];    scalethem = {}
    showratio=False
    applylepSFs=True
    nLep=1
    plotvars   =  ['FatJet1_sDrop_mass_spl_M'] #'FatJet1_sDrop_mass_SR']
    #['Mttbar','Mttbar_logy'] #
    disable   = []; 
    enable  = ['singlelep','ptWlep','dRfjlep','dphifjmet','dphifjlep','mWVtyp0pmet','Mjuppercut','Mwvuppercut','boosted']
    if len(sel) > 0:
        enable+=sel
    #ratio   = '  --fitRatio 1  --fixRatioRange  --ratioYNDiv 505 --maxRatioRange -0.5  1.5 ' #--xu CMS_qcdscales_WW --xu CMS_qcdscales_WZ'
    ratio   = ' --fixRatioRange  --ratioYNDiv 505 --maxRatioRange 0.5  1.95 ' #--xu CMS_qcdscales_WW --xu CMS_qcdscales_WZ'
    spam    = ' --topSpamSize 1.0 --noCms '
    legends = ' --legendFontSize 0.025 --legendBorder 0 --legendWidth  0.62  --legendColumns 2 '
    #legends = ' --legendFontSize 0.04 --legendBorder 0 --legendWidth  0.62 --legendColumns 2'
    addNterms=','.join(x for x in Mprocs)
    if sanitychk:
        anything = ' --showMCError --plotmode nostack --showRatio --ratioDen SM_%s --ratioNums %s  --ratioYLabel=aTGC#rightarrowSM/SM '%(proc,addNterms)  # --fitRatio 1 
    else:
        anything = '  --showMCError --plotmode nostack --showRatio --ratioNums %s --ratioDen SM_%s  --ratioYLabel=aTGC#rightarrowSM/SM '%(addNterms,proc) #  %s --ratioDen %s_sm  --ratioYLabel=BSM/SM '%(addNterms,proc)
    extraopts = ratio + spam + legends + anything
    makeplots  = ['{}'.format(a)  for a in plotvars]
    runPlots(trees, friends, MCfriends, Datafriends, targetdir, fmca, fcut, fsyst, fplots, enable, disable, processes, scalethem, fittodata,makeplots,showratio, applylepSFs, year, nLep,extraopts,invert,cutFlow,bareNano,doWJtypeplots) 

#%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%

def makesimpleplots_perWC(year,sel,proc,smeft,pm):
    trees       = [baseDir+'{here}'.format(here=year  if year not in year_splits.keys() else '')] #if year not in ['all','fullRun2']  else '')]
    targetdir   = os.path.join(eos,'{yr}/{sel}/{date}_{proc}_{smeft}_{pm}/'.format(smeft='smeft' if smeft else 'eft' ,proc=proc,sel=sel[0].split('_')[0],yr=year,date=date,pm=pm ))
    fmca        = 'vvsemilep/fullRun2/mca-vvsemilep_{smeft}.txt'.format(smeft='smeft' if smeft else 'eft') 
    fsyst       = '' #vvsemilep/fullRun2/systsUnc.txt'
    fcut        = 'vvsemilep/fullRun2/cuts_vvsemilep_wjet.txt' #dressed.txt' #wjet.txt' #_dressed.txt'
    bareNano    = False
    cutFlow     = False
    doWJtypeplots = True
    vetoplots=[] #'WW_lin_cb','WW_lin_cHD','WW_lin_clu','WW_lin_cje','WW_lin_ceu','WW_lin_ced','WW_lin_cHl3','WW_lin_cHe','WW_lin_cHd','WW_lin_cHDD']

    WCs=['cw','c3w','cb','Odd_c3w','Odd_cw']
    if smeft:
        WCs=["cW","cWtil","cHWB","cHWBtil","cHl3","cHd","cHu","cHj1","cHj3","cll1","cjj38","cju1","clu","clj3","cjj11","cjd1","clj1","cld","cjj18","cjj31","cju8","cjd8"]
#        WCs=['cll1','cG','cHd','cHDD','cHj3','cjj38','cHWtil','cHj1','cju1','cuu8','cdd8','cuu1','cdd1','cHG','cHe','cHl1',	'cHWB','cHl3','cju8','cjd1','clu','cWtil','clj3','cjj11','cHu','ceu','cHWBtil','ced','clj1','cjj18','cGtil','cW','cld','cje', 'cjd8','cud8','cud1','cjj31','cHGtil']

    procs=[]

    #procs.append('SM_'+proc)
    #terms=['_sm_lin_quad_'] 
    terms=['_quad_','_sm_lin_quad_','_lin_']
    #processes=['WW_sm','WZ_sm']

    for op in  WCs:
        procs=[]
        procs.append(proc+'_sm')
        procs+=[proc + s + op for s in terms  ] 
        processes= [x for x in procs if x not in vetoplots]
        disable   = [];    invert    = [];    fittodata = [];    scalethem = {}
        showratio=False
        applylepSFs=True
        nLep=1
        plotvars   = ['mWV_logy'] #ratios 
        disable   = []; 
        enable  = ['singlelep','ptWlep','dRfjlep','dphifjmet','dphifjlep','mWVtyp0pmet','Mjuppercut','Mwvuppercut','boosted']#'singlelep']
        if len(sel) > 0:
            enable+=sel
        ratio   = ' --fixRatioRange  --ratioYNDiv 505 --maxRatioRange 0.5  3.5'
        spam    = ' --topSpamSize 1.0 --noCms '
        legends = ' --legendFontSize 0.024 --legendBorder 0 --legendWidth  0.62  --legendColumns 3 '
        #legends = ' --legendFontSize 0.04 --legendBorder 0 --legendWidth  0.62 --legendColumns 2'
        addNterms=','.join(x for x in processes if '_sm' not in x)
        anything = '   --plotmode %s ' %pm #--showMCError --showRatio --ratioNums %s --ratioDen %s_sm   --ratioYLabel=BSM/SM '%(addNterms,proc) # --plotmode norm 
        extraopts = ratio + spam + legends + anything
        makeplots  = ['{}'.format(a)  for a in plotvars]
        runPlots(trees, friends, MCfriends, Datafriends, targetdir, fmca, fcut, fsyst, fplots, enable, disable, processes, scalethem, fittodata,makeplots,showratio, applylepSFs, year, nLep,extraopts,invert,cutFlow,bareNano,doWJtypeplots) 
        os.system('mv  {targetdir}/mWV_logy.pdf {targetdir}/mWV_logy_{op}.pdf'.format(op=op,targetdir=targetdir))
        os.system('mv  {targetdir}/mWV_logy.png {targetdir}/mWV_logy_{op}.png'.format(op=op,targetdir=targetdir))
        os.system('mv  {targetdir}/mWV_logy.txt {targetdir}/mWV_logy_{op}.txt'.format(op=op,targetdir=targetdir))
####################

def genCorr(year,proc,smeft):
    baseDir     = '/eos/cms/store/cmst3/group/dpsww/NanoTrees_v9_vvsemilep_13112024/' #06012023/' 
    trees       = [baseDir+'{here}'.format(here=year  if year not in ['all','fullRun2']  else '')]
    MCfriends   = []
    Datafriends = []
    friends     = [] #'1_recl']
    targetdir   = os.path.join(eos,'{yr}/{date}_gencorr_{proc}{bsm}/'.format(yr=year,date=date,proc=proc,bsm='smeft' if smeft else 'eft'))
    fmca        = 'vvsemilep/fullRun2/mca-includes/mca-mc.txt'
    fsyst       = '' #vvsemilep/fullRun2/systsUnc.txt'
    fcut        = 'vvsemilep/fullRun2/cuts_vvsemilep_dressed.txt'
    bareNano    = True #False
    cutFlow     = False
    disable     = [];    invert    = [];    fittodata = [];    scalethem = {}
    showratio     = True
    applylepSFs   = False
    doWJtypeplots = False

    procs=[];    Mprocs=[]; addNterms=''

    if smeft: 
        useThis="_smeftprod_"
        basic="_smeft_"
    else: 
        useThis="_eft_HTbinned_"
        basic="_eft_"
    #Mprocs.append(proc+"_sm")
    Mprocs.append(proc+useThis+'sm')
    #Mprocs.append(proc+"_sm_gencorr")
    #Mprocs.append(proc+"_sm_pol1")
    #Mprocs.append(proc+"_sm_pol1_gencorr")
    procs.append('SM_'+proc)

    ratio   = ' --fixRatioRange  --ratioYNDiv 505 --maxRatioRange -0.5  1.5 ' #--xu CMS_qcdscales_WW --xu CMS_qcdscales_WZ'
    spam    = ' --topSpamSize 1.0 --noCms '
    legends = ' --legendFontSize 0.025 --legendBorder 0 --legendWidth  0.62  --legendColumns 2 '
    #legends = ' --legendFontSize 0.04 --legendBorder 0 --legendWidth  0.62 --legendColumns 2'
    addNterms=','.join(x for x in Mprocs)
    anything = ' --fitRatio 1 --showMCError --plotmode nostack --showRatio --ratioDen SM_%s --ratioNums %s  --ratioYLabel=aTGC#rightarrowSM/SM '%(proc,addNterms)  # --fitRatio 1 

    processes= procs+Mprocs
    nLep=1
    plotvars   = Wjets_ht
    disable    = []; 
    enable     = ['singlelep_dressed','leadlep','fatjet','leadfatjet','ptWlepptWlep','ptWlep','mWV']
#    if len(sel) > 0:
 #       enable+=sel

    extraopts = ratio + spam + legends + anything
    makeplots  = ['{}'.format(a)  for a in plotvars]
    runPlots(trees, friends, MCfriends, Datafriends, targetdir, fmca, fcut, fsyst, fplots, enable, disable, processes, scalethem, fittodata,makeplots,showratio, applylepSFs, year, nLep,extraopts,invert,cutFlow,bareNano,doWJtypeplots) 




######################################


def makesimpleplots_trigchk(year,sel):
    baseDir     = '/eos/cms/store/cmst3/group/dpsww/WW_2018/'
    trees       = [baseDir+'{here}'.format(here=year  if year not in ['all','fullRun2']  else '')]
    MCfriends   = []
    Datafriends = []
    friends     = ['1_recl']
    targetdir   = os.path.join(eos,'{yr}/{sel}/{date}_trigchk/'.format(sel=sel[0].split('_')[0],yr=year,date=date))
    fmca        = 'vvsemilep/fullRun2/mca-vvsemilep.txt'
    fsyst       = '' #vvsemilep/fullRun2/systsUnc.txt'
    fcut        = 'vvsemilep/fullRun2/cuts_vvsemilep_temp.txt'
    bareNano    = True #False
    cutFlow     = False
    processes   = ['aTGC','SM','trig_aTGC','trig_SM'] 
    disable     = [];    invert    = [];    fittodata = [];    scalethem = {}
    showratio     = False
    applylepSFs   = False
    doWJtypeplots = False
    nLep=1
    plotvars   = ['pmet_nowj','mWV_nowj','FatJet1_pt_nowj']
    disable   = []; 
    enable  = ['mu','ptWlep','dRfjlep','dphifjmet','dphifjlep','mWVtyp0pmet','Mjuppercut','Mwvuppercut']#'singlelep']
    if len(sel) > 0:
        enable+=sel
    ratio   = ' --fixRatioRange  --ratioYNDiv 505 --maxRatioRange 0.5  2.5'
    spam    = ' --topSpamSize 1.0 --noCms '
    legends = ' --legendFontSize 0.04 --legendBorder 0 --legendWidth  0.62 --legendColumns 2'
    anything = ' ' 
    extraopts = ratio + spam + legends + anything
    makeplots  = ['{}'.format(a)  for a in plotvars]
    runPlots(trees, friends, MCfriends, Datafriends, targetdir, fmca, fcut, fsyst, fplots, enable, disable, processes, scalethem, fittodata,makeplots,showratio, applylepSFs, year, nLep,extraopts,invert,cutFlow,bareNano,doWJtypeplots) #True)



######################################



if __name__ == '__main__':
    parser = optparse.OptionParser(usage='usage: %prog [opts] ', version='%prog 1.0')
    parser.add_option('--pf', '--postfix', dest='postfix', type='string', default='', help='postfix for running each module')
    parser.add_option('-d', '--date', dest='date' , type='string', default='', help='run with specified date instead of today')
    parser.add_option('-n', '--nLep', dest='nLep' , type='int'  , default=1.    , help='number of leps')
    parser.add_option('--lf',dest='lepflav',type='string' , default=[], action="append", help='lep flav: el/mu/onelep')
    parser.add_option('--finalState',dest='finalState',type='string' , default=[], action="append", help='boosted/resolved, only boosted is optimised')
    parser.add_option('--pv',dest='plotvar',type='string' , default=[], action="append", help='make these plots')
    parser.add_option('--fv',dest='fitvar',type='string' , default='', help='create datacards using this variable and the binning scheme')
    parser.add_option('--dW' , '--doWhat'  , dest='doWhat', type='string' , default=[] , help='plots or cards')
    parser.add_option('--extra',dest='extra',type='string' , default='', help='additional cuts/settings')
    parser.add_option('--year',   dest='year'  , type='string' , default='' , help='make plots/cards for specified year')
    parser.add_option('--results',dest='results', action='store_true' , default=False , help='make plots')
    parser.add_option('--acP',type='string' , default=[], action="append", help='additional cuts for the plots')
    parser.add_option('--acC',type='string' , default=[], action="append", help='additional cuts for the cards')
    parser.add_option('--alpha' , dest='alpha', action='store_true' , default=False , help='compute alpha Ratio')
    parser.add_option('--simple', dest='simple', action='store_true' , default=False , help='make simple plots ')
    parser.add_option('--smeft', dest='smeft', action='store_true' , default=False , help='smeft int rather than dim6eft ')
    parser.add_option('--doWJ', dest='WJest', action='store_true' , default=False , help='make plots using wjest type frnds ')
    parser.add_option('--applylepSFs',dest='applylepSFs', action='store_true', default=False, help='apply lep id/iso SFs')
    parser.add_option('--runblind', dest='blinded', action='store_true' , default=False , help='make plots without datat points')
    parser.add_option('--genC', dest='genCorr', action='store_true' , default=False , help='draw gen level distributions')
    parser.add_option('--SC', dest='sanitychk', action='store_true' , default=False , help='use dressed leptons for gen lvl plots')
    parser.add_option('--trigchk', dest='trigchk', action='store_true' , default=False , help='run trigger chk for 2018 with a subset of WW and aTGC samples')
    parser.add_option('--postfitCR', dest='scaleylds', action='store_true' , default=False , help='use postfit rate params to scale process ylds')
    parser.add_option('--sel',dest='sel', action='append', default=[], help='make plots with wjCR/wjCR_lo/wjCR_hi/inclB/topCR_oneb/topCR_twobsig/sb_lo/sb_hi')
    parser.add_option('--dCF',dest='dCF', action='store_true', default=False , help='cutflow with MC & plot shapes w/o uncert')
    parser.add_option('--fCR',dest='fCR', action='store_true', default=False , help='fit to data in the CR')
    parser.add_option('--fCRwC',dest='fCRwcomb', action='store_true', default=False , help='prepare datacards to fit CRs using combine, basically redefining signal')
    #parser.add_option('--wjD',dest='wjD', type='string', default="2023-12-19", help='date to pick WJ workspace from')
    parser.add_option('--WC',dest='WC', type='string' , default=[], action="append", help='consider terms in EFT Lag. corresponding to this aTGC operator tunred on c3w/cb/cw (for now relevant to make datacards)')

    parser.add_option('--proc',dest='proc', type='string' , default='',  help='SM process')
    parser.add_option('--pm',dest='pm', type='string' , default='norm',  help='norm or nostack')
    parser.add_option('--pD',dest='plotsDir', type='string', default="/eos/user/%s/%s/www/VVsemilep/"%(os.environ['USER'][0],os.environ['USER']),help='save plots here')
    parser.add_option('--nT',dest='notagger', action='store_true', default=False , help='flag to turn off tagger requirement')
    parser.add_option('--pWC',dest='perWC', action='store_true', default=False , help='flag to turn on plots per eft op')
    

    (opts, args) = parser.parse_args()


    global date, postfix,eos 
    postfix = opts.postfix
    year= opts.year
    #print type(postfix)
    date = datetime.date.today().isoformat()
    eos = opts.plotsDir 
    if opts.date:
        date = opts.date
    if opts.results:
        print ('will make {here} {pt} for {bin}' .format(here=opts.doWhat,bin=opts.finalState,pt=(opts.plotvar if 'plots' in opts.doWhat else '')))
        makeResults(opts.year,opts.nLep,opts.lepflav,opts.finalState,opts.doWhat,opts.applylepSFs,opts.blinded,opts.sel,opts.postfix,opts.plotvar,opts.dCF,opts.WJest,opts.notagger,opts.smeft,opts.proc,opts.fCR,opts.scaleylds,opts.fCRwcomb,opts.WC,opts.fitvar,opts.acP,opts.acC)
    if opts.alpha:
        alphaRatio(opts.year,opts.lepflav,opts.plotvar)
    if opts.simple:
        if opts.perWC:
            makesimpleplots_perWC(opts.year,opts.sel,opts.proc,opts.smeft,opts.pm)
        else:
            makesimpleplots(opts.year,opts.sel,opts.proc,opts.smeft,opts.sanitychk)
        
    if opts.trigchk:
        makesimpleplots_trigchk(opts.year,opts.sel)
    if opts.genCorr:
        genCorr(opts.year,opts.proc,opts.smeft)


#python plots_VVsemilep.py --pD /eos/user/a/anmehta/www/VVsemilep/ --simple --genD --year 2018
# python plots_VVsemilep.py --pD /eos/user/a/anmehta/www/VVsemilep/ --results --finalState boosted --nLep 1 --sel sig_incl --pv FatJet1_pt  --lf onelep --year 2018 --dW plots --dCF --applylepSFs  --WC c3w --WC cw --WC cb --doWJ
#python plots_VVsemilep.py  --results --finalState boosted --nLep 1 --sel sig_incl --pv debugsel --lf mu --year 2018 --dW plots  --applylepSFs --doWJ
#python plots_VVsemilep.py  --results --finalState boosted --nLep 1 --sel sig_incl  --lf mu --year 2018 --dW cards  --applylepSFs --doWJ --fv mWV --WC cw
#python plots_VVsemilep.py  --results --finalState boosted --nLep 1 --sel sig_incl --pv mWV --lf mu --year 2018 --dW plots  --applylepSFs --doWJ --semft 
#root://eoscms.cern.ch//eos/cms









