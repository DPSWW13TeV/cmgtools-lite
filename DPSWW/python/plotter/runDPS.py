#!/usr/bin/env python
import optparse, subprocess, ROOT, datetime, math, array, copy, os, re, sys
import numpy as np
eos='/eos/user/a/anmehta/www/DPSWW_v2/'
afs_am=os.getcwd()+'/'
lumis = {
    '2016': '36', #36.33
    '2017': '42', #41.53
    '2018': '60', #59.74
    'All_gen': '138',#137.6
    'all' : '36,42,60',
}

binningSchemes = {
    'new'        : ' unroll_2Dbdt_dps(BDTG_DPS_TLCR_raw_withpt,BDTG_DPS_WZ_amc_raw_withpt) 10,0.0,10.0',
    'wz_nb13'    : ' BDTG_DPS_WZ_amc_raw_withpt 13,-1.0,1.0',
    'wz_nb10'    : ' BDTG_DPS_WZ_amc_raw_withpt 10,-1.0,1.0',
    'wz_nb15'    : ' BDTG_DPS_WZ_amc_raw_withpt 15,-1.0,1.0',
    'iwz'        : ' BDTG_DPS_WZ_amc_raw_withpt [-1.0,-0.9,-0.8,-0.6,-0.45,-0.2,0,0.2,0.4,0.6,0.8,1.0]',
    'i1wz'       : ' BDTG_DPS_WZ_amc_raw_withpt [-1.0,-0.85,-0.75,-0.65,-0.4,-0.2,0.2,0.5,0.7,0.85,1.0]',
    'i2wz'       : ' BDTG_DPS_WZ_amc_raw_withpt [-1.0,-0.8,-0.7,-0.6,-0.35,-0.2,0.1,0.4,0.5,0.7,0.8,1.0]',
    'i3wz'       : ' BDTG_DPS_WZ_amc_raw_withpt [-1.0,-0.8,-0.7,-0.6,-0.35,-0.2,0.2,0.6,0.8,1.0]',
    'prod_20'    : ' BDTG_DPS_TLCR_raw_withpt*BDTG_DPS_WZ_amc_raw_withpt 20,-0.2,1.0',
    'prod_13'    : ' BDTG_DPS_TLCR_raw_withpt*BDTG_DPS_WZ_amc_raw_withpt 13,-0.2,1.0',
    'diag'       : ' unroll_2Dbdt_dps_SoBord_diag(BDTG_DPS_TLCR_raw_withpt,BDTG_DPS_WZ_amc_raw_withpt) 13,0.0,13.0',
    'diag_pc'    : ' unroll_2Dbdt_dps_SoBord_diag_pc(BDTG_DPS_TLCR_raw_withpt,BDTG_DPS_WZ_amc_raw_withpt) 11,0.0,11.0',
    'diag_pcN'   : ' unroll_2Dbdt_dps_SoBord_diag_pcN(BDTG_DPS_TLCR_raw_withpt,BDTG_DPS_WZ_amc_raw_withpt) 10,0.0,10.0',
    ''           : ' unroll_2Dbdt_dps_SoBord_sqV3(BDTG_DPS_TLCR_raw_withpt,BDTG_DPS_WZ_amc_raw_withpt) 13,0.0,13.0',
    'SoBord_sqV3': ' unroll_2Dbdt_dps_SoBord_sqV3(BDTG_DPS_TLCR_raw_withpt,BDTG_DPS_WZ_amc_raw_withpt) 13,0.0,13.0',
    'SoBord_sqV2': ' unroll_2Dbdt_dps_SoBord_sqV2(BDTG_DPS_TLCR_raw_withpt,BDTG_DPS_WZ_amc_raw_withpt) 13,0.0,13.0',
    'SoBord_sqV1': ' unroll_2Dbdt_dps_SoBord_sqV1(BDTG_DPS_TLCR_raw_withpt,BDTG_DPS_WZ_amc_raw_withpt) 12,0.0,12.0',
    'sq'         : ' unroll_2Dbdt_dps_SoBord_sq(BDTG_DPS_TLCR_raw_withpt,BDTG_DPS_WZ_amc_raw_withpt) 10,0.0,10.0',
    'm4l'        : ' m4l 30,180,480',
    'm3l'        : ' mass_3lep(LepGood1_conePt,LepGood1_eta,LepGood1_phi,LepGood2_conePt,LepGood2_eta,LepGood2_phi,LepGood3_conePt,LepGood3_eta,LepGood3_phi) 24,100,400',
    'mt3lnu'     : ' mt_lllv(LepGood1_conePt,LepGood1_phi,LepGood2_conePt,LepGood2_phi,LepGood3_conePt,LepGood3_phi,MET_pt,MET_phi) 24,100,400'        
}

baseDir      = '/eos/cms/store/cmst3/group/dpsww/NanoTrees_v7_dpsww_skim2lss/' 
ubaseDir     = '/eos/cms/store/cmst3/group/dpsww/NanoTrees_v7_dpsww_04092020/' #unskimmed
MCfriends   = ['2_recl_allvars','4_scalefactors','0_jmeUnc_v2','2_btag_SFs',"muPrefiring","nnpdf_rms"] #,"postFSRinfo"]
Datafriends = ['2_recl']
friends     = ['3_tauCount','dpsbdt_neu_ssnoeebkg_afacdps','dpsbdt_neu_ssnoeebkg_afacdps_unclEn']
fplots      = 'dps-ww/fullRun2/plots.txt'


metvars     = ['met','met_HEMUp','met_HEMDn','met_unclUp','met_unclDn','met_jecUp','met_jecDn']
jetvars     = ['nj','nj_jecUp','nj_jecDn']
allbdts     = ['BDT_WZ','BDT_fakes','BDT1d']

bdtiv      = ['conept1','conept2','met','mt2ll','mt1','mtll','etasum','etaprod','dphill','dphil2met','dphilll2']
asymvar    = ['etaprod_absetamin']
only       = ['BDTG1d_fakes_amc_raw_SoB_sqV3']
bdtGM      = ['BDTG_wzamc_raw','BDTG_fakes_raw']#,'BDTG1d_fakes_amc_raw_SoB_sqV3'] 
allvars    = bdtiv + bdtGM #['mll','cptll','nBJetLoose25','njets30','nVert'] + bdtGM #'etaprod_absetamin',
moreVars   = ['minMVA','nVert','nLepFO','nLepTight','eta1','eta2','etaprod_phs','etaprod_nhs','deltaz','dilep_charge','tcharge1','tcharge2','minMVA','dilep_flav','phi1','phi2','metphi','njets25','pt1','pt2','nBJetMedium25','deltaz','ptll','dR','deltaxy','deltaz','etadiff','etasum','etaprod_etamin','bnVert','nLepGood','dilep_flav'] #
exotic     = ['ptRatio1','ptRatio2','mZ1','mZ2','MVA_ptRatio','dxy1','dz1','sip3d1','dxy2','dz2','sip3d2','minMVA','maxMVA','LepGood1_motherid','LepGood2_motherid','fake_lepMVA1','fake_lepMVA2', 'LepGood1_genPartFlav_all','LepGood2_genPartFlav_all','LepGood1_tightId','LepGood2_tightId','LepGood1_cutBased','LepGood2_cutBased','LepGood1_mediumPromptId','LepGood1_mediumId','LepGood1_mvaFall17V2Iso','LepGood1_mvaFall17V2Iso_WPL','LepGood1_mvaId','LepGood2_mediumPromptId','LepGood2_mediumId','LepGood2_mvaFall17V2Iso','LepGood2_mvaFall17V2Iso_WPL','njets25','njets30','nBJetLoose25','nBJetMedium25','nTauTight','nTauFO','puppimetphi','puppimet'] 
MVAS      = ['minMVA','maxMVA']
Nm1Study  = ['nBJetLoose20','cptll','met','njets30','nBJetLoose25']
bdtG2d    = ['BDTG_fakes_wzamc_raw'] 
all1Ds    = ['BDTG1d_fakes_amc_raw_SoB_sq','BDTG1d_fakes_amc_raw_SoB_sqV1','BDTG1d_fakes_amc_raw_SoB_diag_pc','BDTG1d_fakes_amc_raw_SoB_diag','BDTG1d_fakes_amc_raw_SoB_sq','BDTG1d_fakes_amc_raw_SoB_diag_pcN','BDTG1d_fakes_amc_raw_SoB_sqV2','BDTG1d_fakes_amc_raw_SoB_sqV3','BDTG_prod_raw','BDTG_i1wz_raw','BDTG_iwz_raw']
dnn       = ['DNN_fakes','DNN_wzamc','DNN_fakes_wzamc']

dyCR      = ['mtll','conept1','conept2','met','njets30','nBJetLoose25','mll','cptll']
plwzCR    = ['m3l','mt3lnu','mtw_3l','m3l_M','mll_3l','mZ1','mZ_3l','conept1','conept2','conept3','met','mZ1','mZ2','mll_3l','cptll']+bdtGM 
plzzCR    = ['m4l','mZ1','mZ2','conept1','conept2','conept3','conept4','mZ1','mZ2','m4l','met']+bdtGM 


barelepvars=['etaprod_absetamin_genlep','etaprod_phs_genlep','etaprod_nhs_genlep','dilep_flav_genlep','dilep_charge_genlep','dphilll2_genlep','dphill_genlep','etaprod_genlep','etasum_genlep','pt1_genlep','pt2_genlep','eta1_genlep','eta2_genlep','phi1_genlep','phi2_genlep','etasum_genlep','etaprod_genlep','nGenlep']
dressedLepvars = ['dilep_flav_dressedlep','dilep_charge_dressedlep','pt_dressedlep','eta_dressedlep','ndressedLep','etasum_dressedlep','mll_dressedlep','cptll_dressedlep','etaprod_dressedlep']#,'etaprod_phs_dressedlep','etaprod_nhs_dressedlep','etaprod_etamin_dressedlep','etaprod_absetamin_dressedlep']
moredressedLepvars=['pt1_dressedlep','eta1_dressedlep','pdgIdprod_dressedlep','pt2_dressedlep','eta2_dressedlep','mll_lower_dressedlep','mll_dressedlep','mll_low_dressedlep','ndressedLep','mll_high_dressedlep','etasum_dressedlep','etaprod_dressedlep','mll_dressedlep_os']


#####################
def simpleMCplots(trees,MCfriends,Datafriends,targetdir, fmca, fcut,fplots, enabledcuts, disabledcuts, processes,plotlist,year,extraopts = '',bareNano=False,cutflow=False):

    if bareNano:
        cmd  = ' mcPlots.py {CF} -j 10 -l {lumi}  --tree NanoAOD  --year {YEAR} --pdir {td} {fmca} {fcut} {fplots} --split-factor=-1  -P {trees} '.format(td=targetdir, trees=trees, fmca=fmca, fcut=fcut, fplots=fplots,lumi=lumis[year],YEAR=year if year!='all' else '2016,2017,2018',CF='' if cutflow else '-f')

    else:
        cmd  = ' mcPlots.py {CF} -j 10 -l {lumi} --tree NanoAOD  --year {YEAR} --pdir {td} {fmca} {fcut} {fplots} --mcc dps-ww/fullRun2/lepchoice-ttH-FO.txt --WA prescaleFromSkim --mcc dps-ww/fullRun2/mcc-METFixEE2017.txt --split-factor=-1  -P {trees} '.format(td=targetdir, trees=trees, fmca=fmca, fcut=fcut, fplots=fplots,lumi=lumis[year],YEAR=year,CF='' if cutflow else '-f')


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




def runCards(trees, friends, MCfriends, Datafriends, targetdir, fmca, fcut, fsyst, plotbin, enabledcuts, disabledcuts, processes, scaleprocesses,applyWtsnSFs, year,nLep=2,extraopts = '',invertedcuts = []):
    
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

def runPlots(trees, friends, MCfriends, Datafriends, targetdir, fmca, fcut, fsyst, fplots, enabledcuts, disabledcuts, processes, scaleprocesses, fitdataprocess, plotlist, showratio, applyWtsnSFs, year,nLep,extraopts = '', invertedcuts = [],cutflow=False,bareNano=False):

    #if not type(trees)==list: trees = [trees]
    #treestring = ' '.join(' -P '+ t for t in list(trees))
    if bareNano:
        cmd  = ' mcPlots.py {CF} -j 10 -l {lumi}  --tree NanoAOD  --year {YEAR} --pdir {td} {fmca} {fcut} {fplots} --split-factor=-1  -P {trees} '.format(td=targetdir, trees=trees, fmca=fmca, fcut=fcut, fplots=fplots,lumi=lumis[year],YEAR=year if year!='all' else '2016,2017,2018',CF='' if cutflow else '-f')
    else:    
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
    #cmd += ' '.join(["--plotgroup data_fakes%s+='.*_promptsub%s'"%(x,x) for x in processes if 'data' not in x])+" --neglist '.*_promptsub.*' "
    if invertedcuts:
        cmd += ''.join(' -I ^'+cut for cut in invertedcuts )

    cmd += ' --sP '+','.join(plot for plot in plotlist)
    cmd += ' -p '+','.join(processes)

    if applyWtsnSFs and not bareNano:
        if(nLep == 1): 
            cmd += ''.join(" -W puWeight")
        elif(nLep == 2): 
            cmd += ''.join(" -W l1muonprefire_sf*L1PreFiringWeight_Nom*btagSF_shape*puWeight*leptonSF_2lss *triggerSF_ttH(LepGood_pdgId[iLepFO_Recl[0]], LepGood_conePt[iLepFO_Recl[0]], LepGood_pdgId[iLepFO_Recl[1]], LepGood_conePt[iLepFO_Recl[1]],2,year)")
        elif(nLep == 3):
            cmd += ' -W l1muonprefire_sf*L1PreFiringWeight_Nom*btagSF_shape*puWeight*leptonSF_3l *triggerSF_ttH(LepGood_pdgId[iLepFO_Recl[0]], LepGood_conePt[iLepFO_Recl[0]], LepGood_pdgId[iLepFO_Recl[1]], LepGood_conePt[iLepFO_Recl[1]],2,year)'
        else:
            cmd += ' -W l1muonprefire_sf*L1PreFiringWeight_Nom*btagSF_shape*puWeight*leptonSF_4l *triggerSF_ttH(LepGood_pdgId[iLepFO_Recl[0]], LepGood_conePt[iLepFO_Recl[0]], LepGood_pdgId[iLepFO_Recl[1]], LepGood_conePt[iLepFO_Recl[1]],2,year)'
    else:
        if not bareNano:
            cmd += ''.join(" -W puWeight*l1muonprefire_sf*L1PreFiringWeight_Nom*btagSF_shape")
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
def makeResults(year,finalState,splitCharge,doWhat,applylepSFs,binningSch,blinded):
    trees       = [baseDir+'{here}'.format(here=year if year != 'all' else '')]
    fsyst       = 'dps-ww/fullRun2/systsUnc.txt' 
    showratio   = False
    cutflow     = False
    fplots      = 'dps-ww/fullRun2/plots_copy.txt'
    loop        = ['minusminus', 'plusplus',''] if splitCharge else [''] 
    print 'running for %s with charge split flag %s' %(finalState,splitCharge)
    processes_QCDscale=['WZ','WZ_scaleV0','WZ_scaleV1','WZ_scaleV3','WZ_scaleV4','WZ_scaleV5','WZ_scaleV7','WZ_scaleV8']#
    processesdYCR=['WZ_incl','ZZ','DY','Top','WW','data_fakes','data','promptsub']
    processes    = ['DPSWW','WZ','Convs','Rares','Wgstar','ZZ','VVV','DPSWW_alt','data_fakes','data_flips','data']#,'Convs_promptsub']'DPSWW_newsim','DPSWW_hw',
    #,'WZ_ewk']
    #,'promptsub']#'WZTo3LNu_ewk','DPSWW_newsim']'WZ_alt',,'DPSWW_hw','DPSWW_newsim']#
    fRvars    = ['data_fakes_FRe_pt_Up','data_fakes_FRe_pt_Dn','data_fakes_FRe_be_Up','data_fakes_FRe_be_Dn','data_fakes_FRm_pt_Up','data_fakes_FRm_pt_Dn','data_fakes_FRm_be_Up','data_fakes_FRm_be_Dn','data_fakes_FRe_norm_Up','data_fakes_FRe_norm_Dn','data_fakes_FRm_norm_Up','data_fakes_FRm_norm_Dn','promptsub_FRe_norm_Up','promptsub_FRe_norm_Dn','promptsub_FRe_pt_Up','promptsub_FRe_pt_Dn','promptsub_FRe_be_Up','promptsub_FRe_be_Dn']#,'DPSWW_jecDn','DPSWW_jecUp','WZ_jecDn','WZ_jecUp']#,
    if blinded:
        showratio   = False
        fsyst=''
        processes.remove('data')
        processes.remove('DPSWW_alt')
    else:
        print 'plots will be made with data points on top of the stack'
    processes=fRvars+processes 
    
    #procs=[x+'_promptsub' for x in processes if not x.startswith('data')] 
    print processes
    #processes=procs+fRvars+processes
    spam    = ' --topSpamSize 1.0 --noCms '
    legends = ' --legendFontSize 0.04 --legendBorder 0 --legendWidth  0.32  --legendColumns 1 '
    ubands  =  ' ' #--showMCError '
    exclude = '  ' #--xu DPSWW_shape '
    ratio   = ' --ratioYNDiv 505 --fixRatioRange --maxRatioRange 0.45 1.75 --plotmode norm' #--plotmode nostack --ratioNums DPSWW_newsim,DPSWW_hw --ratioDen DPSWW ' #-1 3 --plotmode norm --ratioDen DPSWW --ratioNums WZ' #  --plotmode norm --ratioDen DPSWW --ratioNums DPSWW_newsim,DPSWW_hg --ratioYLabel=hw,ns/py8.' # --plotmode nostack --ratioDen WZ --ratioNums WZ_scaleV1,WZ_scaleV2,WZ_scaleV3,WZ_scaleV4,WZ_scaleV5,WZ_scaleV6 --ratioYLabel=var./nom.' 
    extraopts = ratio + spam + legends + ubands  + exclude
    disable   = [];    invert    = [];    fittodata = [];    scalethem = {}

    for FS in finalState:
        binningBDT = binningSchemes[binningSch]
        binName = FS if  re.search(r'^\d',FS) else '2lss'
        fmca        = 'dps-ww/fullRun2/mca-{here}.txt'.format(here='dpsww' if binName == '2lss' else 'mc-3l')
        fcut        = 'dps-ww/fullRun2/cuts_{here}.txt'.format(here=binName)
        targetcarddir = 'Cards/cards_{date}{pf}_{FS}_{year}'.format(FS=(FS if binName == '2lss' else 'cr'+binName),year=year,date=date, pf=('-'+postfix if postfix else '') )
        targetdir = eos+'{yr}/{dd}{pf}{sf}_{bN}_suppMaterial_shapesForPaper/'.format(dd=date,yr=year if year !='all' else 'fullRun2',pf=('_'+postfix if postfix else ''),sf='_withoutSFs' if not applylepSFs else '',bN=binName)
        
        if binName == '2lss':
            plotvars= allvars #['ndressedLep'] #asymvar #only #bdtGM if blinded else allvars 
            for ch in loop:
                enable=[] #'dressed'] 
                enable.append(FS);
                if len(ch)>0 :                     enable.append(ch)
                makeplots  = ['{}_{}{}'.format(a,FS,ch)  for a in plotvars]
                bN=FS+year+(ch if ch else '')
                anything = "  --neglist '.*_promptsub.* -plotgroup data_fakes+=.*_promptsub.* ' --binname %s "%bN
                extraopts+= anything
                print 'plot settings:  ',extraopts
                if 'plots' in doWhat:
                    runPlots(trees, friends, MCfriends, Datafriends, targetdir, fmca, fcut, fsyst, fplots, enable, disable, processes, scalethem, fittodata,makeplots,showratio, applylepSFs, year, 2,extraopts,invert,cutflow)
                else:
                    extraoptscards=anything
                    runCards(trees, friends, MCfriends, Datafriends, targetcarddir, fmca, fcut, fsyst,binningBDT, enable, disable, processes, scalethem,applylepSFs,year,2,extraoptscards,invert)
        else:
            enable=[]
            nlep=3 if binName == '3l' else 4
            makeplots= plwzCR if binName == '3l' else plzzCR
            more= '--xp Rares --xp WZ --xp VVV ' if binName == '4l' else ''
            anything = " --binname cr%s%s "%(binName,year)
            ratio   = ' --fixRatioRange  --ratioYNDiv 505 --fixRatioRange --maxRatioRange 0.5 2.0 '
            extraoptCRs= anything +more + ratio + spam + legends + ubands
            extraoptsCRcards=anything +more
            if 'plots' in doWhat:
                runPlots(trees, friends, MCfriends, Datafriends, targetdir, fmca, fcut, fsyst, fplots, enable, disable, processes, scalethem, fittodata,makeplots,showratio, applylepSFs,year, nlep,extraoptCRs,invert,cutflow)                
            else:
                runCards(trees, friends, MCfriends, Datafriends, targetcarddir, fmca, fcut, fsyst , binningBDT, enable, disable, processes, scalethem,applylepSFs,year,nlep,extraoptsCRcards,invert)


########################################

def makeAsymResults(year,finalState,splitCharge,doWhat,applylepSFs,binningSch,signal):
    trees       = [baseDir+'{here}'.format(here=year if year != 'all' else '')]
    fsyst       = 'dps-ww/fullRun2/systsUnc.txt'
    showratio   = False
    cutflow     = False
    loop        = ['minusminus', 'plusplus',''] if splitCharge else [''] 
    etaloop     = {'poshem': ['plusplus','p'],'neghem':['minusminus','n'],'':['','']}
    print 'running for %s with charge split flag %s' %(finalState,splitCharge)
    spam    = ' --topSpamSize 1.0 --noCms '
    legends = ' --legendFontSize 0.04 --legendBorder 0 --legendWidth  0.62 --legendColumns 3 '
    ubands  =  ' --showMCError '
    exclude = ' --xu CMS_DPSWW_shape '
    ratio   = ' --ratioYNDiv 505 --fixRatioRange --maxRatioRange 0.5 2.25 ' 
    extraopts = ratio + spam + legends + ubands  + exclude
    disable   = [];    invert    = [];    fittodata = [];    scalethem = {}

    for FS in finalState:
        binningBDT = binningSchemes[binningSch]
        binName = FS if  re.search(r'^\d',FS) else '2lss'
        fmca        = 'dps-ww/fullRun2/mca-{here}.txt'.format(here='dpsww' if binName == '2lss' else 'mc-3l')
        fcut        = 'dps-ww/fullRun2/cuts_{here}.txt'.format(here=binName)
        targetcarddir = 'AsymCards/cards_{date}{pf}_{FS}_{year}'.format(FS=(FS if binName == '2lss' else 'cr'+binName),year=year,date=date, pf=('-'+postfix if postfix else '') )
        targetdir = eos+'{yr}/{dd}{pf}{sf}_{bN}/'.format(dd=date,yr=year if year !='all' else 'fullRun2',pf=('_'+postfix if postfix else ''),sf='_withoutSFs' if not applylepSFs else '',bN=binName)
        
        if binName == '2lss':
            plotvars= only #['ndressedLep'] #asymvar #only #bdtGM if blinded else allvars 
            for ch in loop:
                for hem,nn in etaloop.iteritems():
                    processes  = []#'WZ','Convs','Rares','Wgstar','ZZ','VVV','data_fakes','data_flips','data']#'DPSWW_alt',
                    fRvars    = []#'data_fakes_FRe_pt_Up','data_fakes_FRe_pt_Dn','data_fakes_FRe_be_Up','data_fakes_FRe_be_Dn','data_fakes_FRm_pt_Up','data_fakes_FRm_pt_Dn','data_fakes_FRm_be_Up','data_fakes_FRm_be_Dn','data_fakes_FRe_norm_Up','data_fakes_FRe_norm_Dn','data_fakes_FRm_norm_Up','data_fakes_FRm_norm_Dn','promptsub_FRe_norm_Up','promptsub_FRe_norm_Dn','promptsub_FRe_pt_Up','promptsub_FRe_pt_Dn','promptsub_FRe_be_Up','promptsub_FRe_be_Dn']
                    processes=fRvars+processes 

                    sigSim       = 'DPSWW%s_'%nn[1]+ signal[0] if 'py' not in signal else 'DPSWW%s'%nn[1]
                    processes.append(sigSim)
                    if  "newsim" in signal:         processes.append('DPSWW_tau')
                    print processes    
                    targetdir = eos+'{yr}/{dd}{pf}{sf}_{bN}_{sig}/'.format(sig=sigSim,dd=date,yr=year if year !='all' else 'fullRun2',pf=('_'+postfix if postfix else ''),sf='_withoutSFs' if not applylepSFs else '',bN=binName)
                    enable=[] 
                    enable.append(FS);
                    if len(ch)>0 :                     enable.append(ch)
                    if len(hem)>0 : enable.append(hem)
                    print enable
                    makeplots  = ['{}_{}{}'.format(a,FS,nn[0])  for a in plotvars]
                    bN=FS+year+(nn[0] if nn[0] else '')
                    anything = "  --neglist '.*_promptsub.* -plotgroup data_fakes+=.*_promptsub.* ' --binname %s "%bN
                    extraopts+= anything
                    if 'plots' in doWhat:
                        runPlots(trees, friends, MCfriends, Datafriends, targetdir, fmca, fcut, fsyst, fplots, enable, disable, processes, scalethem, fittodata,makeplots,showratio, applylepSFs, year, 2,extraopts,invert,cutflow)
                    else:
                        extraoptscards=anything+exclude
                        runCards(trees, friends, MCfriends, Datafriends, targetcarddir, fmca, fcut, fsyst,binningBDT, enable, disable, processes, scalethem,applylepSFs,year,2,extraoptscards,invert)
        else:
            enable=[]
            nlep=3 if binName == '3l' else 4
            makeplots= plwzCR if binName == '3l' else plzzCR
            more= '--xp Rares --xp WZ --xp VVV ' if binName == '4l' else ''
            anything = " --binname cr%s%s "%(binName,year)
            ratio   = ' --fixRatioRange  --ratioYNDiv 505 --fixRatioRange --maxRatioRange 0.5 2.0 '
            extraoptCRs= anything +more + ratio + spam + legends + ubands
            extraoptsCRcards=anything +more
            if 'plots' in doWhat:
                runPlots(trees, friends, MCfriends, Datafriends, targetdir, fmca, fcut, fsyst, fplots, enable, disable, processes, scalethem, fittodata,makeplots,showratio, applylepSFs,year, nlep,extraoptCRs,invert,cutflow)                
            else:
                runCards(trees, friends, MCfriends, Datafriends, targetcarddir, fmca, fcut, fsyst , binningBDT, enable, disable, processes, scalethem,applylepSFs,year,nlep,extraoptsCRcards,invert)


########################################
def makeResultsFiducial(year,finalState,splitCharge):
    baseDir     = "/eos/cms/store/cmst3/group/dpsww/signal_FRonly_reco/" 
    #baseDir     = "/eos/cms/store/cmst3/group/dpsww/signal_fullstats_nosel/"
    #MCfriends   = [] #["postFSRinfo"]
    #friends     = []
    trees       = [baseDir+'{here}'.format(here=year if year != 'all' else '')]
    fsyst       = 'dps-ww/fullRun2/systsUnc.txt'
    fmca        = 'dps-ww/fullRun2/mca-dpsww.txt'
    fcut        = 'dps-ww/fullRun2/cuts_2lss.txt' #cuts_2lss_dpsww_dressed.txt' #cuts_2lss_dpsww_gen.txt' #cuts_2lss.txt'
    showratio   = False
    cutflow     = True
    disable     = [];    invert    = [];    fittodata = [];    scalethem = {}
    loop        = ['minusminus', 'plusplus',''] if splitCharge else ['']
    print 'running for %s with charge split flag %s' %(finalState,splitCharge)
    processes   = ['DPSWW','DPSWW_alt','DPSWW_newsim','DPSWW_hw']#'DPSWW_gen','DPSWW_gen_hw','DPSWW_gen_newsim']#,'DPSWW_gen_notau','DPSWW_gen_notau_hw','DPSWW_gen_tau','DPSWW_gen_tau_hw']#'WZ',,'DPSWW_alt','DPSWW_newsim',
    binName     = '2lss'
    spam        = ' --topSpamSize 1.0 --noCms '
    legends     = '  --legendFontSize 0.04 --legendBorder 0 --legendWidth  0.62 --legendColumns 3 '
    ubands      =  ' ' #--showMCError ' 
    exclude     = ' '
    ratio       = '  --fixRatioRange  --ratioYNDiv 505  --maxRatioRange 0.5 1.5  ' #--plotmode norm --ratioNums DPSWW_gen_newsim,DPSWW_gen_hw --ratioDen DPSWW_gen' #-1 3 --plotmode norm --ratioDen DPSWW --ratioNums WZ' #  --ratioYLabel=var./nom.' 
    targetdir = eos+'{yr}/{dd}_2lss_signalRecofromFR/'.format(dd=date,yr=year if year !='all' else 'fullRun2')
    extraopts = ratio + spam + legends + ubands  + exclude

    for FS in finalState:
        plotvars   = ['met'] #['ndressedLep'] #'etaprod_absetamin_genlep'] #dressedLepvars #  ['nGenlep'] #'ndressedLep']#
        for ch in loop:
            enable=[] 
            enable.append(FS);
            print enable
            if len(ch)>0 :                     enable.append(ch)
            makeplots  = ['{}_{}{}'.format(a,FS,ch)  for a in plotvars]
            bN=FS+year+(ch if ch else '')
            anything = " --binname %s "%bN
            extraopts+= anything
            print 'plot settings:  ',extraopts
            runPlots(trees, friends, MCfriends, Datafriends, targetdir, fmca, fcut, fsyst, fplots, enable, disable, processes, scalethem, fittodata,makeplots,showratio, True, year, 2,extraopts,invert,cutflow,bareNano=False)
            #def runPlots(trees, friends, MCfriends, Datafriends, targetdir, fmca, fcut, fsyst, fplots, enabledcuts, disabledcuts, processes, scaleprocesses, fitdataprocess, plotlist, showratio, applyWtsnSFs, year,nLep,extraopts = '', invertedcuts = [],cutflow=False,bareNano=False):
########################################

def plotFRvars(year,finalState):
    baseDir     = '/eos/cms/store/cmst3/group/dpsww/NanoTrees_v7_dpsww_skim2lss/'
    trees      = [baseDir+'{here}'.format(here=year if year != 'all' else '')]
    fmca        = 'dps-ww/fullRun2/mca-2lss-data-frdata-vars.txt'
    fsyst       = '' #dps-ww/fullRun2/systsUnc.txt'
    fcut        = 'dps-ww/fullRun2/cuts_2lss.txt' 

    showratio=True

    targetdir   = '/eos/user/a/anmehta/www/DPSWW_v2/{year}/{date}{pf}FRvars/'.format(date=date, year=year if year !='all' else 'fullRun2',pf=('-'+postfix if postfix else '')) 

    print 'running fr variation plots for  %s' %(finalState)


    processesM = ['data_fakes','data_fakes_m_up','data_fakes_m_down','data_fakes_m_be1','data_fakes_m_be2','data_fakes_m_pt1','data_fakes_m_pt2']
    fRElvars   = ['data_fakes_e_up','data_fakes_e_down','data_fakes_e_be1','data_fakes_e_be2','data_fakes_e_pt1','data_fakes_e_pt2']

    
    plotvars   =  bdtGM #+ all1Ds

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
        ratio   = "--fixRatioRange  --ratioYNDiv 505 --maxRatioRange 0.5  1.5"
        spam    = ' --topSpamSize 1.0 --noCms '
        legends = ' --legendFontSize 0.04 --legendBorder 0 --legendWidth  0.62 --legendColumns 3 '
        anything = " --plotmode nostack   --ratioDen data_fakes --ratioNums data_fakes_m_up,data_fakes_m_down,data_fakes_m_be1,data_fakes_m_be2,data_fakes_m_pt1,data_fakes_m_pt2,data_fakes_e_up,data_fakes_e_down,data_fakes_e_be1,data_fakes_e_be2,data_fakes_e_pt1,data_fakes_e_pt2"
        extraopts = ratio+spam+legends+anything

        makeplots1  = ['{}_{}'.format(a,FS) for a in plotvars]
            
        
        makeplots=makeplots1 #+makeplots2
        print makeplots1
        runPlots(trees, friends, MCfriends, Datafriends, targetdir, fmca, fcut, fsyst, fplots, enable, disable, processes, scalethem, fittodata,makeplots,showratio, False, year, 2,extraopts,invert,False)


############################################ plots using barenano/gen/dressed leptons
def makesimpleplots(year,finalState,splitCharge,useDressed=True):
    #trees="/eos/cms/store/cmst3/group/dpsww/NANOGEN/"
    trees="/eos/cms/store/cmst3/group/dpsww/NANOGEN_v1/"
    #trees       = '/eos/cms/store/cmst3/group/dpsww/bufferZone/Signal_nanoV7/All_gen/'
    MCfriends   = '' #['/eos/cms/store/cmst3/group/dpsww/bufferZone/Signal_nanoV7/All_gen/postFSRinfo'] 
    targetdir   = '/eos/user/a/anmehta/www/DPSWW_v2/GeneratorLevel/{date}{pf}/'.format(date=date,pf=('_dressed' if useDressed else '') )
    fmca        = 'dps-ww/fullRun2/mca-dpsww-gen.txt' #mca-dpsww.txt' 
    fsyst       = ''
    fcut        = 'dps-ww/fullRun2/{cf}'.format(cf='cuts_2lss_dpsww_gen.txt' if not useDressed else 'cuts_2lss_dpsww_dressed.txt' )
    bareNano    = True
    cutFlow     = False
    loop = [ 'minusminus', 'plusplus'] if splitCharge else ['']

    print 'running for %s with charge split flag %s' %(finalState,splitCharge)
    #processes = ['pdf13','pdf14','pdf17','pdf18','pdf5']   #
    #processes = ['py8_all','hw_all','ns_all']
    processes=['incl_dpsWW','excl_dpsWW']#'py8_cp5_bareNano','newsim_bareNano','hw7_2018_bareNano','hwpp_bareNano','py8_cuet_2017_bareNano','py8_cuet_bareNano']#,'py8_cp5_2017_bareNano','py8_cp5_2018_bareNano','hw7_2017_bareNano']

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
            legends = ' --legendFontSize 0.04 --legendBorder 0 --legendWidth  0.62 --legendColumns 2' # --plotmode nostack'
            anything = '  --showRatio --plotmode norm  --ratioNums incl_dpsWW --ratioDen excl_dpsWW' #--ratioDen py8_cuet_2017_bareNano --ratioNums py8_cp5_bareNano,newsim_bareNano,py8_cuet_bareNano,py8_cp5_2017_bareNano,py8_cp5_2018_bareNano,hw7_2017_bareNano,hw7_2018_bareNano,hwpp_bareNano  --ratioYLabel=py_cp5,hw,dSh/py_cuet' # --uf ' # --plotmode norm' # --plotmode nostack' # rm --neg  --uf' #  --ratioDen pdf13 --ratioNums pdf14,pdf5,pdf17,pdf18 --ratioYLabel=var/nom' 
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
    fmca        = 'dps-ww/fullRun2/mca-mc-3l_test.txt' #'dps-ww/fullRun2/mca-mc-3l.txt'
    fsyst       = '' #dps-ww/fullRun2/systsUnc.txt'
    fcut        = 'dps-ww/fullRun2/cuts_2lss.txt' #3l.txt'
    showratio   = False #True
    applylepSFs = True

    processes = ['Convs']#'WZ','Wgstar','ZZ','Convs','Rares','VVV'] #'Wgstar''WZ_alt','Convs01J',
    fittodata = [] #'Convs']
    enable    = ['elmu']#'pt251515','cptll','bVeto','m3l_wg']
    exclude =  '' #-- xu  Conv_norm --xu Conv_shape1 --xu Conv_shape2'


    disable   = []#'met_wz','pt301010','m3l_wz','zsel']
    scalethem = {}

    ratio   = ' --fixRatioRange  --ratioYNDiv 505 --maxRatioRange 0.0  1.99'
    spam    = ' --topSpamSize 1.0 --noCms '
    legends = ' --legendFontSize 0.04 --legendBorder 0 --legendWidth  0.62 --legendColumns 3 '
    ubands  = ' --showMCError '
    anything = "  --binname 3l --plotmode norm" #--fitData --flp WZ --sP tot_weight  " #scaleBkgToData--preFitData tot_weight --flp WZ --sP tot_weight --sp WZ " # --fitData  --flp WZ  "# --neglist '.*_promptsub.*' --plotgroup data_fakes+=.*_promptsub" # --preFitData tot_weight --plotmode norm" #to include neagitve evt ylds from fakes 
    extraopts = ratio + spam + legends + ubands + anything + exclude

    makeplots= ['conept1','conept2','mll_3l','cptll']#,'conept3','met','mZ1','mZ2','mll_3l','cptll']+bdtGM 
    invert=[]
    #runPlots(trees, friends, MCfriends, Datafriends, targetdir, fmca, fcut, fsyst, fplots, enable, disable, processes, scalethem, fittodata,makeplots,showratio, applylepSFs,year, 3,extraopts)
    runPlots(trees, friends, MCfriends, Datafriends, targetdir, fmca, fcut, fsyst, fplots, enable, disable, processes, scalethem, fittodata,makeplots,showratio, applylepSFs, year, 2,extraopts,invert)

def fourlepCRPlot(year):
    print '=========================================='
    print 'running 4l control region  plots'
    print '=========================================='
    trees       = [baseDir+'{here}'.format(here=year if year != 'all' else '')]
    targetdir   = '/eos/user/a/anmehta/www/DPSWW_v2/ControlRegions/{date}{pf}{year}_fourlepCR/'.format(date=date, year=year,pf=('-'+postfix if postfix else ''))
    fmca        = 'dps-ww/fullRun2/mca-mc-3l.txt'
    fsyst       = 'dps-ww/fullRun2/systsUnc.txt'
    fcut        = 'dps-ww/fullRun2/cuts_4l.txt'
    processes   = ['data','ZZ','VVV','Rares','WZ']#,'ttjets','TTdilep','RaresGG']#'WZ_alt','WZ',
    enable      = []
    disable     = []
    fittodata   = [] #['ZZ']
    scalethem   = {} #{'WZ':1.1}
    showratio   = True
    applylepSFs = True
    exclude     =  '-- xu  ZZ_norm --xu ZZ_shape1 --xu ZZ_shape2 --xu WZ_norm --xu WZ_shape'
    ratio   = ' --fixRatioRange  --ratioYNDiv 505 --maxRatioRange 0.0  1.99'
    spam    = ' --topSpamSize 1.0 --noCms '
    legends = ' --legendFontSize 0.04 --legendBorder 0 --legendWidth  0.62 --legendColumns 3 '
    ubands  = ' --showMCError '
    anything = " --binname cr4l" # --plotmode norm" #to include neagitve evt ylds from fakes 
    allvars    = ['nLepFO','nLepTight','njets25','nBJetLoose25','nBJetMedium25','njets30']#'conept1','conept2','pt1','pt2','eta1','eta2','met','metphi','njets25','nBJetLoose25','nBJetMedium25','njets30','mll','mt2ll','mt1','mtll','etasum','etaprod','dphill','dphil2met','dphilll2','nVert','ptll','cptll'] #dilep_charge','puppimetphi','puppimet''tcharge1','tcharge2','MVA1','MVA2','minMVA','dilep_flav','phi1','phi2','MVA1','MVA2',
    makeplots= ['conept1'] #,'conept2','conept3','conept4','mZ1','mZ2','m4l','met']+bdtGM 'nBJetLoose25','nBJetMedium25','njets30','njets25',
    extraopts = ratio + spam + legends + ubands + anything + exclude
    runPlots(trees, friends, MCfriends, Datafriends, targetdir, fmca, fcut, fsyst, fplots, enable, disable, processes, scalethem, fittodata,makeplots,showratio, applylepSFs,year, 2,extraopts)
#########################################################
def onelepCRPlot(year,finalState):
    print '=========================================='
    print 'running single lepton control region  plots'
    print '=========================================='
    baseDir='/eos/cms/store/cmst3/group/dpsww/TREES_ttH_FR_nano_v5/'
    trees  = [baseDir+'{here}'.format(here=year if year != 'all' else '')]
    friends =['1_frFriends_v1']
    MCfriends = ''
    Datafriends=''
    fplots = 'fakeRates/lepton-fr/qcd1l_plots.txt'
    fmca = 'fakeRates/lepton-fr/mca-qcd1l-{year}.txt'.format(year=year)
    fsyst  = '' 
    fcut   = 'fakeRates/lepton-fr/qcd1l.txt'
    disable   = []
    fittodata = []
    scalethem = {}
    ratio   = ' ' #--fixRatioRange  --ratioYNDiv 505 --maxRatioRange 0.0  1.99'
    spam    = ' --topSpamSize 1.0 --noCms '
    legends = ' --legendFontSize 0.04 --legendBorder 0 --legendWidth  0.62 --legendColumns 3 '
    ubands  = ' ' #--plotmode nostack ' #--showMCError '

    for FS in finalState:
        if FS == 'mu':
            processes=['WJets','DYJets','Top','data','QCDMu_red']
            enable=['conepTmu','muCR','num_v1p0_plot','2016_trigMu' if year == '2016' else 'trigMu'] #'mu_den_v1p0_plot',
            anything= " --xf 'SingleEl.*,DoubleEG.*,EGamma.*'"
            anything= " -W coneptwMuX_OR_2016(LepGood_pt,LepGood_mvaTTH,LepGood_jetRelIso,PV_npvsGood" #%year
            targetdir = '/eos/user/a/anmehta/www/DPSWW_v2/Fakes/{date}_era{year}_1muCRpass/'.format(date=date,year=year)
        if FS == 'el':
            processes=['WJets','DYJets','Top','QCDEl_red','QCDEl_redNC','QCDEl_conv','WJets_NC']#'data'
            enable=['conepTel','elCR','el_den_v1p0_plot','num_v1p0_plot','flav']#'trigEl',
            targetdir = '/eos/user/a/anmehta/www/DPSWW_v2/Fakes/{date}_era{year}_1elCRpass/'.format(date=date,year=year)
            anything= " --xf 'DoubleMu.*,SingleMu.*' "
            anything+= " --plotmode nostack " # -W coneptwEleX_OR_2016(LepGood_pt,LepGood_mvaTTH,LepGood_jetRelIso,PV_npvsGood)"
    

        extraopts = ratio + spam + legends + ubands + anything
        makeplots=['mtW1R','pt','conePt','miniRelIso','mvaTTH','awayJet_pt','met','nvtx','mtW1','mtW1R']
        runPlots(trees, friends, MCfriends, Datafriends, targetdir, fmca, fcut, fsyst, fplots, enable, disable, processes, scalethem, fittodata,makeplots,False, True,year, 1,extraopts)
        #runPlots(trees, friends, MCfriends, Datafriends, targetdir, fmca, fcut, fsyst, fplots, enabledcuts, disabledcuts, processes, scaleprocesses, fitdataprocess, plotlist, showratio, applyWtsnSFs, year,nLep,extraopts = '', invertedcuts = [],cutflow=False,bareNano=False):

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
def tempResults(year,finalState,extra):
    trees       = [baseDir+'{here}'.format(here=year if year != 'all' else '')]
    fsyst       = 'dps-ww/fullRun2/systsUnc.txt'
    fmca        = 'dps-ww/fullRun2/mca-dpsww_temp.txt'
    fcut        = 'dps-ww/fullRun2/cuts_2lss.txt' #cuts_temp.txt' 
    MCfriends   = ['2_recl_allvars','4_scalefactors','0_jmeUnc_v2','2_btag_SFs',"muPrefiring","nnpdf_rms","postFSRinfo"]
    showratio   = True
    targetdir   = '/eos/user/a/anmehta/www/DPSWW_v2/{year}/{date}{pf}_suppMaterial_scaledtopostfit_FORPAPER/'.format(date=date, year=year if year !='all' else 'fullRun2',pf=('_'+postfix if postfix else '') ) 
    processes    = ['DPSWW','WZ','data_fakes','Convs','Rares','Wgstar','ZZ','VVV','DPSWW_alt','data_fakes','data_flips','data']#,'Convs_promptsub']'DPSWW_newsim','DPSWW_hw',
    #processes    = ['DPSWW','DPSWW_newsim','DPSWW_hw']#,'data_fakes','Convs_promptsub']#'DPSWW_tau','DPSWW_tau_alt','DPSWW_newsim','DPSWW_notau','DPSWW_notau_alt','DPSWW','DPSWW_alt']#,'data_fakesConv'] #'WG01J',WG,'DPSWW','WZ','Convs','Rares','Wgstar','ZZ','VVV','data_fakes','data_flips']#,'DPSWW_alt','data']#,'WZ_ewk']
    fRvars    = ['data_fakes_FRe_pt_Up','data_fakes_FRe_pt_Dn','data_fakes_FRe_be_Up','data_fakes_FRe_be_Dn','data_fakes_FRm_pt_Up','data_fakes_FRm_pt_Dn','data_fakes_FRm_be_Up','data_fakes_FRm_be_Dn','data_fakes_FRe_norm_Up','data_fakes_FRe_norm_Dn','data_fakes_FRm_norm_Up','data_fakes_FRm_norm_Dn','promptsub_FRe_norm_Up','promptsub_FRe_norm_Dn','promptsub_FRe_pt_Up','promptsub_FRe_pt_Dn','promptsub_FRe_be_Up','promptsub_FRe_be_Dn']#,'DPSWW_jecDn','DPSWW_jecUp','WZ_jecDn','WZ_jecUp']#,
    processes+=fRvars
    #processes  = ['DPSWW','DPSWW_hw','DPSWW_newsim']#'Convs','Rares','Wgstar','ZZ','VVV','WZ','data_fakes','data_flips']
    print processes

    cutflow=False
    applylepSFs=True
    for FS in finalState:            
        enable=[] #'ssWW','noTaus'] #'nVertH']
        enable.append(FS);
        disable   = []#'01jets']#'cptll','01jets','bVeto','metpt']
        invert    = []
        fittodata = []
        ratio   = ' --ratioYNDiv 505 --fixRatioRange --maxRatioRange 0.45 1.75' # --plotmode norm --ratioDen DPSWW --ratioNums DPSWW_hw,DPSWW_newsim --ratioYLabel=hw,dSh/py '#--plotmode nostack --ratioDen data_fakes --ratioNums Convs --ratioYLabel=Convs/nonprompt'
        # --ratioDen DPSWW --ratioNums DPSWW_alt --ratioYLabel=hw/py'
        #--plotmode norm --ratioDen DPSWW --ratioNums DPSWW_newsim,DPSWW_hw --ratioYLabel=var./nom.' # --ratioDen WZ --ratioNums DPSWW   --ratioYLabel=DPS/WZ' # --plotmode nostack --ratioDen WZ --ratioNums WZ_scaleV1,WZ_scaleV2,WZ_scaleV3,WZ_scaleV4,WZ_scaleV5,WZ_scaleV6 --ratioYLabel=var./nom.' --plotmode norm --ratioDen DPSWW --ratioNums WZ,WpWpJJ --ratioYLabel=bkg./sig.--ratioDen WZ --ratioNums WZ_alt DPSWW_newsim,
        spam    = ' --topSpamSize 1.0 --noCms '
        legends = ' --legendFontSize 0.04 --legendBorder 0 --legendWidth  0.62 --legendColumns 3 --showMCError'
        ubands  =  ' ' 
        anything = " --binname %s "%finalState
        procs = [ '' ]
        procs += ['_FRe_norm_Up','_FRe_norm_Dn','_FRe_pt_Up','_FRe_pt_Dn','_FRe_be_Up','_FRe_be_Dn','_FRm_norm_Up','_FRm_norm_Dn','_FRm_pt_Up','_FRm_pt_Dn','_FRm_be_Up','_FRm_be_Dn']
        anything += ' '.join(["--plotgroup data_fakes%s+='.*_promptsub%s'"%(x,x) for x in procs ])+" --neglist '.*_promptsub.*' "
        #'.*_promptsub.* -plotgroup data_fakes+=.*_promptsub.* '
        extraopts = ratio + spam + legends + ubands + anything
        plotvars   =  allvars #['MVA2','MVA1'] #+all1Ds  #['dphill_T','absdphill','met_absdphill','cptll_dphill'] #bdtiv #bdtG2d #allvars + bdtGM + all1Ds #bdtGvarsUp + bdtGvarsDn + allbdts 
        makeplots  = ['{}_{}'.format(a,FS) for a in plotvars]
        #scalethem={}            
        scalethem = {'ZZ':1.36,'WZ':1.06,'Rares':0.98,'VVV':0.77,'data_fakes':0.70,'Convs':1.15,'DPSWW':1.01,'Wgstar':1.65,'data_flips':1.08}
        runPlots(trees, friends, MCfriends, Datafriends, targetdir, fmca, fcut, fsyst, fplots, enable, disable, processes, scalethem, fittodata,makeplots,showratio, applylepSFs, year, 2,extraopts,invert,cutflow)
#%%%%%%%%%%%%%%%%
def plotsystvars(year,finalState,splitCharge=True):
    trees       = [baseDir+'{here}'.format(here=year if year != 'all' else '')]
    showratio   = False
    loop        = ['minusminus', 'plusplus'] if splitCharge else [''] 
    targetdir   = '/eos/user/a/anmehta/www/DPSWW_v2/{year}/{date}{pf}_puvars/'.format(date=date, year=year if year !='all' else 'fullRun2',pf=('_'+postfix if postfix else '') ) 
    fmca        = 'dps-ww/fullRun2/mca-2lss-mc-systvars.txt'
    fsyst       = ''    
    fcut        = 'dps-ww/fullRun2/cuts_2lss.txt' 
    print 'running fr variation plots for  %s' %(finalState)
    invert    = []
    fittodata = []
    scalethem = {}
    processes  = ['DPSWW','Convs','Rares','Wgstar','ZZ','VVV','WZ']
    processes+=[i+'_puDn' for i in processes]
    processes+=[i+'_puUp' for i in processes]
    plotvars   =  bdtGM #+ allvars
    for FS in finalState:            
        for ch in loop:
            enable=[]
            enable.append(FS); 
            if len(ch)>0 : 
                enable.append(ch)
            print enable 
            disable   = []
            ratio   = "--fixRatioRange  --ratioYNDiv 505 --maxRatioRange 0.5  1.55"
            spam    = ' --topSpamSize 1.0 --noCms '
            legends = ' --legendFontSize 0.04 --legendBorder 0 --legendWidth  0.62 --legendColumns 3 '
            anything = " --plotmode norm" # 
            extraopts = ratio+spam+legends+anything
            makeplots  = ['{}_{}{}'.format(a,FS,ch)  for a in plotvars]            
            runPlots(trees, friends, MCfriends, Datafriends, targetdir, fmca, fcut, fsyst, fplots, enable, disable, processes, scalethem, fittodata,makeplots,showratio, True, year, 2,extraopts,invert,False)

#########################




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
    parser.add_option('--simple', dest='simple', action='store_true' , default=False , help='make simple plots ')
    parser.add_option('--postFSR',dest='postFSR',action='store_true', default=True , help='use postFSR')
    parser.add_option('--fC', dest='runClosure', action='store_true' , default=False , help='FR closure test')
    parser.add_option('--fakes',dest='usefakes', action='store_true' , default=False, help='run closure test for fakes otherwise on flips')
    ##    parser.add_option('--unskimmed', dest='unskimmed', action='store_true' , default=False , help='chk ntuples before 2lss skimming')
    parser.add_option('--applylepSFs',dest='applylepSFs', action='store_true', default=False, help='apply lep id/iso SFs')
    parser.add_option('--genD',dest='genDressed', action='store_true' , default=False , help='2lss using dressed leptons')
    parser.add_option('--frV',dest='frVars', action='store_true' , default=False , help='plot FR variations')
    parser.add_option('--binning',dest='binningSch', type='string' , default='', help='binning scheme for datacards')
    parser.add_option('--temp', dest='temp', action='store_true' , default=False , help='make temp plots ')
    parser.add_option('--fid', dest='fid', action='store_true' , default=False , help='make plots with fiducial region and sr cuts')
    parser.add_option('--syst', dest='syst', action='store_true' , default=False , help='make plots with syst vars')
    parser.add_option('--asym', dest='asym', action='store_true' , default=False , help='make plots or cards categorized in terms of  etaprod')
    parser.add_option('--sig', dest='signal', type='string' , default=[],action="append", help='py/hw/newSim')
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
    if opts.asym:
        print 'running {here} for {bin}' .format(here=opts.doWhat,bin=opts.finalState)
        makeAsymResults(opts.year,opts.finalState,opts.splitCharge,opts.doWhat,opts.applylepSFs,opts.binningSch,opts.signal)
    if opts.old:
        makeResults_oldMaps(opts.year,opts.finalState,opts.splitCharge)
    if opts.simple:
        makesimpleplots(opts.year,opts.finalState,opts.splitCharge,opts.genDressed)
    if opts.runClosure:
        runClosure(opts.year,opts.finalState,opts.usefakes)
    if opts.frVars:
        plotFRvars(opts.year,opts.finalState)
    if opts.temp:
        tempResults(opts.year,opts.finalState,opts.extra)
    if opts.fid:
        makeResultsFiducial(opts.year,opts.finalState,opts.splitCharge)
    if opts.syst:
        plotsystvars(opts.year,opts.finalState)

# python runDPS.py --results --dW plots --year 2016 --finalState elmu --finalState mumu --applylepSFs
# python runDPS.py --results --dW plots --year 2016 --finalState 4l --finalState 3l --applylepSFs
# python runDPS.py --results --dW plots --year all --finalState ll_noee  --applylepSFs
# python runDPS.py --results --dW cards --year 2016 --finalState elmu --finalState mumu --applylepSFs --splitCharge
# python runDPS.py --results --dW cards --year 2016 --finalState 3l m3l --applylepSFs
# python runDPS.py --results --dW cards --year 2016 --finalState 4l m4l --applylepSFs
# python runDPS.py --year 2016 --finalState ll_noee --simple --genD
# python runDPS.py --dyCR --year 2017 --finalState mumu --finalState elmu --finalState elel --applylepSFs
# python runDPS.py --unskimmed --year 2017 --finalState elmu --finalState mumu
# python runDPS.py --fC --fakes --year 2016 --finalState elmu --finalState mumu 
# python runDPS.py --fC --year 2016 --finalState elmu 
# python runDPS.py --wzCR --wzbkg --year 2016
# python runDPS.py --zzCR --year 2016

# python runDPS.py --frV --finalState elmu --finalState mumu --year 2016 
 
#python runDPS.py --simple --genD --year 2018 --finalState ll_noee
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




#makeResultsFiducial run it when postFSR frnds are ready
#bdtGvarsUp  = ['BDT1d_unclUp','BDT_fakes_unclUp','BDT_WZ_unclUp']#,'BDT_fakes_jerbUp','BDT_fakes_jerec1Up','BDT_fakes_jerec2hptUp','BDT_fakes_jerec2lptUp','BDT_fakes_jerfwdhptUp','BDT_fakes_jerfwdlptUp',,'BDT_WZ_jecUp','BDT_WZ_jerbUp','BDT_WZ_jerec1Up','BDT_WZ_jerec2hptUp','BDT_WZ_jerec2lptUp','BDT_WZ_jerfwdhptUp','BDT_WZ_jerfwdlptUp','BDT1d_jecUp','BDT1d_jerbUp','BDT1d_jerec1Up','BDT1d_jerec2hptUp','BDT1d_jerec2lptUp','BDT1d_jerfwdhptUp','BDT1d_jerfwdlptUp','BDT_fakes_jecUp']'BDT_fakes_HEMUp','BDT_WZ_HEMUp','BDT1d_HEMUp',
#bdtGvarsDn = ['BDT_fakes_unclDn','BDT_WZ_unclDn','BDT1d_unclDn']#,'BDT_fakes_jecDn','BDT_fakes_jerbDn','BDT_fakes_jerec1Dn','BDT_fakes_jerec2hptDn','BDT_fakes_jerec2lptDn','BDT_fakes_jerfwdhptDn','BDT_fakes_jerfwdlptDn','BDT_fakes_HEMDn','BDT_WZ_jecDn','BDT_WZ_jerbDn','BDT_WZ_jerec1Dn','BDT_WZ_jerec2hptDn','BDT_WZ_jerec2lptDn','BDT_WZ_jerfwdhptDn', 'BDT_WZ_jerfwdlptDn','BDT1d_jerbDn','BDT1d_jecDn', 'BDT1d_jerec1Dn', 'BDT1d_jerec2hptDn','BDT1d_jerec2lptDn','BDT1d_jerfwdhptDn','BDT1d_jerfwdlptDn',]'BDT_fakes_HEMDn','BDT1d_HEMDn','BDT_WZ_HEMDn',
