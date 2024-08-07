#!/usr/bin/env python
import optparse, subprocess, ROOT, datetime, math, array, copy, os, re, sys
import numpy as np
#eos='/eos/user/a/anmehta/www/VVsemilep/' ##save plots here
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
mWV_binning_res="[950,1000,1058,1118,1181,1246,1313,1383,1455,1530,1607,1687,1770,1856,1945,2037,2132,2231,2332,2438,2546,2659,2775,2895,3019,3147,3279,3416,3558,3704, 3854, 4010, 4171, 4337, 4509,4550]"
mWV_binning_simple=" 36,950,4550"
mWV_binning="[950,1000,1058,1118,1181,1246,1313,1383,1455,1530,1607,1687,1770,1856,1945,2037,2132,2231,2332,2438,3000]"
mWV_fxn="mass_WV(Selak8Jet1_pt,Selak8Jet1_eta,Selak8Jet1_phi,Selak8Jet1_msoftdrop,Lep1_pt,Lep1_eta,Lep1_phi,pmet_pt,pmet_phi,0)"


baseDir     = '/eos/cms/store/cmst3/group/dpsww/NanoTrees_v9_vvsemilep_06012023/' #parent trees 
ubaseDir    = '/eos/cms/store/cmst3/group/dpsww/NanoTrees_v9_vvsemilep_06012023/' #unskimmed
MCfriends   = ['1_recl','2_recl_allvars','4_scalefactors','2_jmeUnc','1_btag_SFs']
Datafriends = ['1_recl']
friends     = ['3_ak8_sdm45','0_wjest_v4']
fplots      = 'vvsemilep/fullRun2/plots.txt'
fmca        = 'vvsemilep/fullRun2/mca-vvsemilep.txt'


####################variables for plotting 
eventvars   = ['nVert']
genvars_phi = ['jetphi_mWV','lephi_mWV','SeldLep1_pt','SelGak8Jet1_pt','SelGak8Jet1_mass','ttGenmWV_typ0_pmet_boosted','SeldLep1_eta','SeldLep1_phi','SeldLep1_pdgId','SeldLep1_pt_HF','SeldLep1_eta_HF','SeldLep1_phi_HF','nSeldLeps','SelGak8Jet1_pt','SelGak8Jet1_eta','SelGak8Jet1_phi','SelGak8Jet1_mass','SelGak8Jet1_pt_HF','SelGak8Jet1_eta_HF','SelGak8Jet1_phi_HF','SelGak8Jet1_mass_HF','nSelGak8Jets','neutrino_pt_HF','neutrino_phi_HF']    
HEM=['puppimetphi','etaphi1','FatJet1_phi','FatJet1_eta','FatJet1_etaphi','eta1','phi1']
aTGC_chk   =['tmWV_typ0_pmet_boosted','FatJet1_pt_vBins','Lep1_pt_vBins','Genptlepmet','tptleppmet','tmWV_typ0_pmet_boosted','tGenmWV_typ0_pmet_boosted','FatJet1_pt','tFatJet1_sDrop_mass','tptWV_pmet','nBJetLoose30_Recl','nBJetMedium30_Recl', 'aTGC_wt','aTGC_wt_neg','aTGC_wt_pos','aTGC_wt_SM','aTGC_wt1','aTGC_wt2','test_plot'] #
mWV=['ratio_typ0','ratio_typ1','ratio_typ2','ratio_typ3','mWV_typ0_pmet_boosted','mWV_typ01_pmet_boosted','mWV_typ10_pmet_boosted','mWV_typ11_pmet_boosted','mWV_typ20_pmet_boosted','mWV_typ21_pmet_boosted','mWV_typ30_pmet_boosted','mWV_typ31_pmet_boosted']
topCR=['mWV_typ0_met_boosted','FatJet1_pt','FatJet1_sDrop_mass']
bTag_eff=['Jet_eta_pt','Jet_partonFlavour','Jet_btagDeepFlavB','Jet_hadronFlavour','nJet30_Recl','nJet20','Jet_pt_eta']
theWVfullset=['FatJet1_sDrop_mass','FatJet1_pt','mWV','mWV_vBins','FatJet1_pNetMD_Wtagscore']#'Lep1_pt','pmet',"nBJetMedium30_Recl",'mWV','FatJet1_pt']#, 'puppimetphi','Lep1_pt','nBJetMedium30_Recl','nFatJet','puppimet','dphifjpmet','dphifjlep','ptWV_pmet','dphil1pmet','dphifjpmet','ptleppmet','nJet30_Recl','Lep1_eta','FatJet1_eta','FatJet1_mass','FatJet1_pNetMD_Wtagscore','FatJet1_tau21','FatJet1_pNet_mass''mt1pmet','nLepGood','nLepFO','sumBoosted']"Lep1_pt_vBins",'pmet_vBins',

theWVultimateset=['mWV',"FatJet1_sDrop_mass","FatJet1_pt"]#'puppimetphi','ptWV_pmet','mWV','puppimet','Lep1_pt','FatJet1_sDrop_mass','FatJet1_pt','dphifjpmet','dphifjlep','dphil1pmet','nBJetLoose30_Recl']
ak4jetvars = ['nBJetLoose30_Recl','nBJetMedium30_Recl','nJet30_Recl','Jet1_pt','Jet2_pt','htJet30','Jet1_qgl','Jet1_btagDeepFlavB','Jet1_btagCSVV2','Jet2_qgl','Jet2_btagDeepFlavB','Jet2_btagCSVV2','Jet1_pt','Jet2_pt','mjj','mt1','Jet1_eta','Jet1_mass','Jet2_eta','Jet2_mass','nJet30','htJet30j_Recl','mhtJet30_Recl','htJet25j_Recl','mhtJet25_Recl']
MConly     = ['Mttbar','genwhad_costcm','genwhad_costcs','genwhad_cost2d','genwhad_phics','genwhad_mt','genwhad_pt','genwhad_eta','genwhad_y','recoil_whad_x','recoil_whad_y','genwlep_costcm','genwlep_costcs','genwlep_cost2d','genwlep_phics','genwlep_mt','genwlep_pt','genwlep_eta','genwlep_y','recoil_wlep_x','recoil_wlep_y','nGenJetAK8','nGenJetAK8_ptgtp2k','GenJetAK8_pt','GenJetAK8_mass','GenmWV_typ0_pmet_boosted','GenDressedLeptonpt','GenMETphi','GenMET','Genptlepmet','Genptlepfj','Genmlepfj','sum_ttbar','pdgid1','pdgid2','LHE_HT','LHE_HT_log','LHE_HT_lin','Jet1_hadronFlavour','Jet1_partonFlavour','Jet2_hadronFlavour','Jet2_partonFlavour','LHE_Vpt']
dRchecks   = ['dR','dRfjj','dRjj','dRfjlep']
moreak8jetvars = ['dphifjmet','dphifjlep','dRfjlep','nFatJet_wtagged','FatJet1_tau21','FatJet1_sDrop_mass','FatJet1_pNet_mass','FatJet1_pt','FatJet1_pNetMD_Wtag','FatJet1_muonIdx3SJ_wtag','FatJet1_electronIdx3SJ_wtag','FatJet1_pNetMD_Wtag','FatJet1_eta','FatJet1_n2b1','FatJet1_n3b1','FatJet1_particleNetMD_QCD','FatJet1_particleNetMD_Xbb','FatJet1_particleNetMD_Xqq','FatJet1_particleNet_QCD','FatJet1_particleNet_WvsQCD','FatJet1_tau21','FatJet1_tau21_tau32','FatJet1_area','FatJet1_btagCSVV2','FatJet1_btagDDBvLV2','FatJet1_btagDeepB','FatJet1_deepTagMD_ZbbvsQCD','FatJet1_deepTagMD_ZvsQCD','FatJet1_deepTagMD_bbvsLight','FatJet1_deepTag_QCD','FatJet1_deepTag_QCDothers','FatJet1_particleNet_ZvsQCD','FatJet1_tau1','FatJet1_tau2','FatJet1_tau3','FatJet1_tau4','FatJet1_hadronFlavour','FatJet1_nBHadrons','FatJet1_nCHadrons','FatJet1_tau32','FatJet1_tau42']



###################
def if3(cond, iftrue, iffalse):
    return iftrue if cond else iffalse

#####################

def runCards(trees, friends, MCfriends, Datafriends, targetdir, fmca, fcut, fsyst, plotbin, enabledcuts, disabledcuts, processes, scaleprocesses,applyWtsnSFs, year,nLep,lepflav,selstr,wj_date,extraopts = '',invertedcuts = []):
    varToFit= '{plotvar} {binning}'.format(plotvar=plotbin.split()[0], binning=plotbin.split()[1]) #assumes WJ type frnds are being used  
    cmd = 'makeShapeCardsNew.py -f -j 8 -l {lumi} --od {CARDSOUTDIR} --tree NanoAOD --year {YEAR} --mcc vvsemilep/fullRun2/lepchoice-ttH-FO.txt  --mcc vvsemilep/fullRun2/mcc-METFixEE2017.txt  --WA evt_wt {fmca} {fcut}  --threshold 0.01 --split-factor=-1 --unc {fsyst}  {varName} --lf {lepflav} --wjD {wj_date} --sel {selstr}'.format(lumi=lumis[year],selstr=selstr,CARDSOUTDIR=targetdir, trees=trees, fmca=fmca, fcut=fcut,YEAR=year if year !='all' else '2016APV,2016,2017,2018',fsyst=fsyst,varName=varToFit,wj_date=wj_date,lepflav=lepflav) #--asimov signal #--amc --threshold 0.01 --amc
    cmd += ''.join(' -P '+Ptree for Ptree in trees)
    cmd += ''.join(' --Fs {P}/'+frnd for frnd in friends)
    cmd += ''.join(' --FMCs {P}/'+frnd for frnd in MCfriends)
    cmd += ''.join(' --FDs {P}/'+frnd for frnd in Datafriends)
    cmd += ''.join(' -E ^'+cut for cut in enabledcuts )
    cmd += ''.join(' -X ^'+cut for cut in disabledcuts)
    cmd += ' -p '+','.join(processes)
    if invertedcuts:
        cmd += ''.join(' -I ^'+cut for cut in invertedcuts )
    if applyWtsnSFs: cmd+=" -W lepSF*btagSF*triggerSF_ttH(Lep1_pdgId,Lep1_pt,0,0,1,year,suberaId) "
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
def runPlots(trees, friends, MCfriends, Datafriends, targetdir, fmca, fcut, fsyst, fplots, enabledcuts, disabledcuts, processes, scaleprocesses, fitdataprocess, plotlist, showratio, applyWtsnSFs, year,nLep,extraopts = ' ', invertedcuts = [],cutFlow=False,bareNano=False,doWJtypeplots=False):    
    cmd= ' mcPlots.py  -j 10 -l {lumi}  --tree NanoAOD  --year {YEAR} --pdir {td} {fmca} {fcut} {fplots} --split-factor=-1  -P {trees} --mcc vvsemilep/fullRun2/lepchoice-ttH-FO.txt --mcc vvsemilep/fullRun2/mcc-METFixEE2017.txt '.format(td=targetdir, trees=trees, fmca=fmca, fcut=fcut, fplots=fplots,lumi=lumis[year],YEAR=year if year!='all' else '2016APV,2016,2017,2018')
    if not cutFlow:
        cmd+=''.join(' -f')
    if not bareNano:
        if doWJtypeplots:
            cmd+=" --WA evt_wt "
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
            cmd+=" -W lepSF*btagSF*triggerSF_ttH(Lep1_pdgId,Lep1_pt,0,0,1,year,suberaId) "
        else:
            cmd+=" -W L1PreFiringWeight_Nom*puWeight*lepsf*btagSF*triggerSF_ttH(Lep1_pdgId, Lep1_pt,0,0,1,year, suberaId)" 
    else:
        if not bareNano:
            cmd += ''.join(" -W puWeight*L1PreFiringWeight_Nom*btagSF")
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

##################
def makeResults(year,nLep,lepflav,finalState,doWhat,applylepSFs,blinded,selection,postfix,plotvars,cutflow,doWJ,fitCR,WCs,acP,acC,wjDate):
    #    print ("vorsichtig sein!! du hast tagging auswahl im top CR geloschen")
    trees        = [baseDir+'{here}'.format(here=year if year != 'all' else '')]
    fsyst        = 'vvsemilep/fullRun2/systsUnc.txt' if not cutflow else ''
    showratio    = True
    fcut         = 'vvsemilep/fullRun2/cuts_vvsemilep.txt' if not doWJ else 'vvsemilep/fullRun2/cuts_vvsemilep_wjet.txt' #
    fmca         = 'vvsemilep/fullRun2/mca-vvsemilep.txt'  if not doWJ else 'vvsemilep/fullRun2/mca-vvsemilep_wj.txt'
    processes    = ['tt','data','WJets','singletop','Others','WW_sm','WZ_sm']
    #, 'WZ_sm_lin_quad_cw','WZ_quad_cw','WW_quad_cw','WW_sm_lin_quad_cw']#,'WZ_quad_c3w','WW_quad_cb','WW_quad_c3w','WW_sm_lin_quad_cb']    #'WZ_cw','WZ_c3w','WW_cw','WW_cb','WW_c3w']#,'SM_WW','SM_WZ'] 'SM_WW','WW_sm','WZ_sm','WV_sm','WZ_sm_lin_quad_cw','WZ_quad_cw','WZ_quad_c3w','WZ_sm_lin_quad_cw','WW_quad_cw','WW_quad_cb','WW_quad_c3w','WW_sm_lin_quad_cw','WW_sm_lin_quad_cb']
    vetoPlots=['WW_sm_lin_quad_c3w','WZ_sm_lin_quad_c3w','WZ_sm_lin_quad_cb','WZ_quad_cb']
    WCs=['cw']#,'c3w','cb']
    for ops in WCs:
        morePs=['WZ_sm_lin_quad_','WZ_quad_','WW_sm_lin_quad_','WW_quad_']
        processes+=[s + ops for s in morePs if s not in vetoPlots]
    genprocesses = ['WJetsHT10','WJetsHT7','WJetsHT250','WJetsHT120','WJetsHT60','WJetsHT40','WJetsHT20','WJetsHT80']#,,'signal','testHT','testTT']
    cuts_boosted = ['ptWlep','dRfjlep','dphifjmet','dphifjlep','mWVtyp0pmet','Mjuppercut','Mwvuppercut']
    cuts_cards_opts=['sb_lo','sb_hi','sig']#
    cuts_btagEff = ['btagSR','bpartonFlav','Loosebtag','Medbtag','Tightbtag'] ##here for reference ['lightpartonFlav','cpartonFlav']
    cuts_WJest   = ['cuts_wjest']
    bareNano    = False
    print (processes)
    signal  = ''
    spam    = ' --topSpamSize 1.0 --noCms '
    legends = ' --legendFontSize 0.03 --legendBorder 0 --legendWidth  0.62  --legendColumns 3 ' 
    #legends = ' --perBin  --legendFontSize 0.025 --legendBorder 0 --legendWidth  0.3  --legendColumns 1 '
    ubands  =  ' --showMCError  --showIndivSigs --noStackSig --showSigShape'
    exclude = ' '  #--xu CMS_vvsl18_pNetscore' 
    ratio   = ' --ratioYNDiv 505 --fixRatioRange --maxRatioRange 0.25 2.5 ' # --ratioNums WW_SMEFT_sm,WW_sm   --ratioDen SM_WW --ratioYLabel=aTGC/SM  --plotmode nostack ' # --ratioNums WW_sm_lin_quad_2p25_cw,WW_quad_2p25_cw,WW_sm_lin_quad_cw,WW_quad_cw,WW_sm_lin_quad_1p8_c3w,WW_quad_1p8_c3w,WW_sm_lin_quad_c3w,WW_quad_c3w  --ratioDen WW_sm --ratioYLabel=aTGC/SM  --plotmode nostack ' #

    more = '' # --plotmode norm' if cutflow else ''
    extraopts = ratio + spam + legends + ubands  + exclude + signal + more
    disable   = [];    invert    = [];    fittodata = [];    scalethem = {}
    if doWhat == "plots" and ('SR' in selection or "sig" in selection):
        blinded=True
    for pR in selection:
        if 'topCR_twob' in pR and fitCR:         fittodata.append('tt');
        if 'topCR_oneb' in pR and fitCR:         fittodata.append('singletop');
        if 'wj' in pR and fitCR:          fittodata.append('WJets');
        exclude = ' ' #--xu CMS_vvsl18_pNetscore' if 'wjCR' not in pR else  ' '
        #signal= if3(pR == 'SR',if3(nLep > 1,'--sp ZV','--sp aTGC_WW --sp aTGC_WZ'), if3('top' in pR, ' --sp tt --sp singletop', ' --sp WJets'))
        signal = if3(pR == 'SR' or pR == 'sig','--sp .*cw.* --sp .*cb.*', if3('topCR' in pR, if3(pR == 'topCR_oneb',' --sp tt ',' --sp singletop '), ' --sp WJets'))

        for LF in lepflav:
            for FS in finalState:
                binName = '{jet}_{lep}_{pR}'.format(lep=LF,jet=FS,pR=pR)
                print ('running %s for %s'%(doWhat,binName))
                postfix=('_'+postfix if postfix else '')+('_fittodata' if fitCR else '')+('_'+'cutflow' if cutflow else '')+('_noWJtype' if not doWJ else '')
                targetcarddir = 'Cards/cards_{date}{pf}_{FS}_{year}'.format(FS=binName,year=year,date=date, pf=postfix )
                print ('{yr}/{dd}_{bN}{sf}{pf}/'.format(dd=date,yr=year if year !='all' else 'fullRun2',pf=postfix,sf='_withoutSFs' if not applylepSFs else '',bN=binName))
                targetdir = os.path.join(eos,'{yr}/{pR}/{dd}_{bN}{sf}{pf}/'.format(dd=date,yr=year if year !='all' else 'fullRun2',pf= postfix,sf='_withoutSFs' if not applylepSFs else '',bN=binName,pR=pR.split('_')[0]))
                enable=[]
                enable+= cuts_boosted 
                enable.append(LF); 
                enable.append(pR)
                #enable+=cuts_btagEff
                #if "wjCR" not in pR:   
                enable.append(FS); #now tagger
                anything = "  --binname %s "%binName #--showIndivSigs #--pseudoData all
                extraopts+= anything
                if 'plots' in doWhat:
                    if len(acP) > 0: extraopts += ''.join(' -E ^'+cut for cut in acP )
                    if "SR" in pR and 'data' in processes and blinded :  
                        processes.remove('data')
                        showratio   = False
                        fsyst=''
                    elif  "top" in pR and fitCR:
                        extraopts+= ' --xp Others --xp .*quad.*  --xp QCD'
                    elif  "wj" in pR and fitCR:
                        extraopts+= ' --xp .*quad.* '
                    makeplots  = ['{}'.format(a)  for a in plotvars]
                    print (makeplots)
                    runPlots(trees, friends, MCfriends, Datafriends, targetdir, fmca, fcut, fsyst, fplots, enable, disable, processes, scalethem, fittodata, makeplots, showratio, applylepSFs, year, nLep,extraopts,invert,cutflow,bareNano,doWJ)

                else:
                    if "top" in pR or 'wj' in pR: 
                        mWV_dist=" {here} {binning} ".format(here=mWV_fxn,binning=mWV_binning)
                        binNamecards=binName+"_"+year
                        extraoptscards= ' --xp Others --xp .*quad.*  --sp WW_sm --sp WZ_sm  --binname %s %s '%(binNamecards, '--xp QCD ' if 'top' in pR else '')
                        if len(acC) > 0:extraoptscards += ''.join(' -E ^'+cut for cut in acC )
                        runCards(trees, friends, MCfriends, Datafriends, targetcarddir, fmca, fcut,fsyst, mWV_dist, enable, disable, processes, scalethem,applylepSFs,year,nLep,LF,pR,wjDate,extraoptscards,invert)
                    else:
                        for op in WCs:
                            mWV_dist=" {here} {binning} ".format(here=mWV_fxn,binning=mWV_binning)
                            binNamecards=binName+"_"+op+"_"+year
                            extraoptscards= ' --sp WW_sm --sp WZ_sm --binname %s '%(binNamecards) ##signal process SM for checks
                            if len(acC) > 0:extraoptscards+=''.join(' -E ^'+cut for cut in acC )
                            runCards(trees, friends, MCfriends, Datafriends, targetcarddir, fmca, fcut,fsyst, mWV_dist, enable, disable, processes, scalethem,applylepSFs,year,nLep,LF,pR,wjDate,extraoptscards,invert)


#####################################
#################


def alphaRatio(year,nLep,lepflav,finalState,applylepSFs,postfix,plotvars,doWJ):
    trees        = [baseDir+'{here}'.format(here=year if year != 'all' else '')]
    fsyst        = 'vvsemilep/fullRun2/systsUnc.txt'
    showratio    = True
    fcut         = 'vvsemilep/fullRun2/cuts_vvsemilep_wjet.txt' #
    fmca         = 'vvsemilep/fullRun2/mca-vvsemilep_wj.txt'
    processes    = ['WJetsCR','WJetsSR','WJetsCR_lo','WJetsCR_hi']
    cuts_boosted = ['ptWlep','dRfjlep','dphifjmet','dphifjlep','mWVtyp0pmet','Mjuppercut','Mwvuppercut','bVeto']
    cutflow      = False
    bareNano =False
    print (processes)
    signal  = ''
    spam    = ' --topSpamSize 1.0 --noCms '
    legends = ' --legendFontSize 0.04 --legendBorder 0 --legendWidth  0.42  --legendColumns 2 '    #legends = ' --legendFontSize 0.04 --legendBorder 0 --legendWidth  0.32  --legendColumns 1 '
    ubands  =  ' ' #--showMCError '
    exclude = '' #' --xu TTJets' if nLep ==1
    ratio   = ' --ratioYNDiv 505 --fixRatioRange --maxRatioRange 0.25 2.0 --plotmode norm --ratioDen WJetsSR --ratioNums WJetsCR.WJetsCR_lo,WJetsCR_hi --ratioYLabel=CR/SR' # --plotmode nostack  --ratioDen DPSWW --ratioNums DPSWW_newsim,DPSWW_hg --ratioYLabel=hw,ns/py8.'
    more = ' '
    extraopts = ratio + spam + legends + ubands  + exclude + signal + more
    disable   = [];    invert    = [];    fittodata = [];    scalethem = {}
    signal=  '--sp WJets' 
    for LF in lepflav:
        for FS in finalState:
            binName = '{lep}{jet}'.format(lep=if3(nLep > 1,'2los',flavors[LF]),jet=FS)
            print ('running plots for %s'%binName)
            print ('{yr}/{dd}_{bN}{sf}{pf}/'.format(dd=date,yr=year if year !='all' else 'fullRun2',pf=('_'+postfix if postfix else ''),sf='_withoutSFs' if not applylepSFs else '',bN=binName))
            targetdir = os.path.join(eos,'{yr}/alphaRatio/{dd}_{bN}{sf}{pf}/'.format(dd=date,yr=year if year !='all' else 'fullRun2',pf=('_'+'cutflow' if cutflow else '' + postfix if postfix else ''),sf='_withoutSFs' if not applylepSFs else '',bN=binName))
            enable=[];
            enable+=cuts_boosted #FS is enabled in the mca as it's CR vs SR. 
            enable.append(LF)
            makeplots  = ['{}'.format(a)  for a in plotvars]
            anything = "  --binname %s "%binName #--showIndivSigs
            extraopts+= anything
            #runPlots(trees, friends, MCfriends, Datafriends, targetdir, fmca, fcut, fsyst, fplots, enable, disable, processes, scalethem, fittodata, makeplots, showratio, applylepSFs, year, nLep,extraopts,invert,cutflow,bareNano,doWJ)

            runPlots(trees, friends, MCfriends, Datafriends, targetdir, fmca, fcut, fsyst, fplots, enable, disable, processes, scalethem, fittodata,makeplots,showratio, applylepSFs, year, nLep,extraopts,invert,cutflow,bareNano,doWJ)

########################################
def makesimpleplots(year,useDressed=True):
    #baseDir = '/eos/cms/store/cmst3/group/dpsww/testWJ_htbinned/'
    trees        = [baseDir+'{here}'.format(here=year if year != 'all' else '')]
    MCfriends   = [] #'phi_var_v2']#2_toppT_rw']#genInfo'] #'2_toppT_rw']
    Datafriends = []
    friends     = []
    targetdir = os.path.join(eos,'/GenLevel/{date}{pf}/'.format(date=date,pf=('_dressed' if useDressed else '') ))
    fmca        = 'vvsemilep/fullRun2/mca-vvsemilep.txt' #mca-semilep-gen.txt'
    fsyst       = ''
    fplots      = 'vvsemilep/fullRun2/plots.txt'
    fcut        = 'vvsemilep/fullRun2/cuts_vvsemilep_{cf}.txt'.format(cf='gen' if not useDressed else 'dressed' )
    bareNano    = False
    cutFlow     = False
    processes   = ['WW_sm','SM_WW','WW_SMEFT_LO']#,'tt']#plus_sm_lin_quad_c3w','sm']#,'minus_sm_lin_quad_c3w']#'WW','aTGC','aTGC_SM','aTGC_incl']##'WJetsToLNu']#'ttmtt1ktoinf','ttmttp7kto1k','ttsemi']#'WJetsToLNu']#'WW','aTGC']#'ttmtt1ktoinf','ttmttp7kto1k','Rwtttsemi']#'ttsemi']
    #'WJetsHT10','WJetsHT7','WJetsHT250','WJetsHT120','WJetsHT80','WJetsHT60','WJetsHT40','WJetsHT20']
    #cuts_onelep   = ['singlelep']
    disable   = [];    invert    = [];    fittodata = [];    scalethem = {}

    showratio=True
    applylepSFs=False
    nLep=1
    plotvars   = ['mWV_typ0_pmet_boosted']#Jet_pt_eta']#genvars_phi #MConly #dressedLepvars if useDressed else barelepvars 

    disable   = []; 
    #enable=['ttbar','nQ']#'WhadpT','mWV','leadfatjet','fatjet','ptWlep','leadlep','etacutl1'] #'ttbar','nQ']
    enable=[]#'phi_var']#,'ptWlep']
    ratio   = ' --fixRatioRange  --ratioYNDiv 505 --maxRatioRange 0.5  2.15'
    spam    = ' --topSpamSize 1.0 --noCms '
    legends = ' --legendFontSize 0.04 --legendBorder 0 --legendWidth  0.62 --legendColumns 2'
    anything = '  --showRatio  --ratioNums WW_sm,WW_SMEFT_LO --ratioDen SM_WW   --ratioYLabel=aTGC,SMEFT/SM --plotmode nostack' #sm,sm_lin_quad_c3w,aTGC_WW_SM_incl --ratioDen WW  #--ratioDen py8_cuet_2017_bareNano --ratioNums py8_cp5_bareNano,newsim_bareNano,py8_cuet_bareNano,py8_cp5_2017_bareNano,py8_cp5_2018_bareNano,hw7_2017_bareNano,hw7_2018_bareNano,hwpp_bareNano  --ratioYLabel=py_cp5,hw,dSh/py_cuet' # --uf ' # --plotmode norm' # --plotmode nostack' # rm --neg  --uf' #  --ratioDen pdf13 --ratioNums pdf14,pdf5,pdf17,pdf18 --ratioYLabel=var/nom' 
    extraopts = ratio + spam + legends + anything
    makeplots  = ['{}'.format(a)  for a in plotvars]

    runPlots(trees, friends, MCfriends, Datafriends, targetdir, fmca, fcut, fsyst, fplots, enable, disable, processes, scalethem, fittodata,makeplots,showratio, applylepSFs, year, nLep,extraopts,invert,cutFlow)
######################################



if __name__ == '__main__':
    parser = optparse.OptionParser(usage='usage: %prog [opts] ', version='%prog 1.0')
    parser.add_option('--pf', '--postfix', dest='postfix', type='string', default='', help='postfix for running each module')
    parser.add_option('-d', '--date', dest='date' , type='string', default='', help='run with specified date instead of today')
    parser.add_option('-n', '--nLep', dest='nLep' , type='int'  , default=1.    , help='number of leps')
    parser.add_option('--lf',dest='lepflav',type='string' , default=[], action="append", help='lep flav: el/mu/onelep')
    parser.add_option('--finalState',dest='finalState',type='string' , default=[], action="append", help='boosted/resolved, only boosted is optimised')
    parser.add_option('--pv',dest='plotvar',type='string' , default=[], action="append", help='make these plots')
    parser.add_option('--dW' , '--doWhat'  , dest='doWhat', type='string' , default=[] , help='plots or cards')
    parser.add_option('--extra',dest='extra',type='string' , default='', help='additional cuts/settings')
    parser.add_option('--year',   dest='year'  , type='string' , default='' , help='make plots/cards for specified year')
    parser.add_option('--results',dest='results', action='store_true' , default=False , help='make plots')
    parser.add_option('--acP',type='string' , default=[], action="append", help='additional cuts for the plots')
    parser.add_option('--acC',type='string' , default=[], action="append", help='additional cuts for the cards')
    parser.add_option('--alpha' , dest='alpha', action='store_true' , default=False , help='compute alpha Ratio')
    parser.add_option('--simple', dest='simple', action='store_true' , default=False , help='make simple plots ')
    parser.add_option('--doWJ', dest='WJest', action='store_true' , default=False , help='make plots using wjest type frnds ')
    parser.add_option('--postFSR',dest='postFSR',action='store_true', default=True , help='use postFSR')
    parser.add_option('--applylepSFs',dest='applylepSFs', action='store_true', default=False, help='apply lep id/iso SFs')
    parser.add_option('--runblind', dest='blinded', action='store_true' , default=False , help='make plots without datat points')
    parser.add_option('--genD', dest='genDressed', action='store_true' , default=False , help='use dressed leptons for gen lvl plots')
    parser.add_option('--sel',dest='sel', action='append', default=[], help='make plots with SR/wjCR/wjCR_lo/wjCR_hi/inclB/topCR_oneb/topCR_twobsig/sb_lo/sb_hi')
    parser.add_option('--dCF',dest='dCF', action='store_true', default=False , help='cutflow with MC & plot shapes w/o uncert')
    parser.add_option('--fCR',dest='fCR', action='store_true', default=False , help='fit to data in the CR')
    parser.add_option('--wjD',dest='wjD', type='string', default="2023-12-19", help='date to pick WJ workspace from')
    parser.add_option('--WC',dest='WC', type='string' , default=['cw'], action="append", help='consider terms in EFT Lag. corresponding to this aTGC operator tunred on c3w/cb/cw (for now relevant to make datacards)')
    parser.add_option('--pD',dest='plotsDir', type='string', default="/eos/user/%s/%s/www/VVsemilep/"%(os.environ['USER'][0],os.environ['USER']),help='save plots here')
    

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
        #makeResults(year,nLep,finalState,doWhat,applylepSFs,blinded,selection,postfix,plotvars):
        plotV=opts.plotvar if 'plots' in opts.doWhat else 'mWV_typ0_met_boosted'
        makeResults(opts.year,opts.nLep,opts.lepflav,opts.finalState,opts.doWhat,opts.applylepSFs,opts.blinded,opts.sel,opts.postfix,plotV,opts.dCF,opts.WJest,opts.fCR,opts.WC,opts.acP,opts.acC,opts.wjD)
    if opts.alpha:
        alphaRatio(opts.year,opts.nLep,opts.lepflav,opts.finalState,opts.applylepSFs,opts.postfix,opts.plotvar,opts.WJest)
    if opts.simple:
        makesimpleplots(opts.year,opts.genDressed)
        #    if opts.fid:
        #       makeResultsFiducial(opts.year,opts.finalState,opts.splitCharge)


# python plots_VVsemilep.py --pD /eos/user/a/anmehta/www/VVsemilep/ --results --dW plots --year 2018 --nLep 1 --finalState boosted --pv FatJet1_pt --pv FatJet1_mass --pv FatJet1_particleNet_mass  --pf nom --sel wjCR --applylepSFs --lf onelep
# python plots_VVsemilep.py --pD /eos/user/a/anmehta/www/VVsemilep/ --results --dW plots --year 2018 --nLep 1 --finalState boosted --pv FatJet1_pt --pf nom --sel SR --applylepSFs --lf mu 
# python plots_VVsemilep.py --pD /eos/user/a/anmehta/www/VVsemilep/ --results --dW plots --year 2018 --nLep 1 --finalState boosted --pv phi1 --sel wjCR --applylepSFs --lf el 
# python plots_VVsemilep.py --pD /eos/user/a/anmehta/www/VVsemilep/ --results --dW plots --year 2016 --nLep 1 #--finalState 3l --applylepSFs
# python plots_VVsemilep.py --pD /eos/user/a/anmehta/www/VVsemilep/ --results --dW plots --year all --finalState ll --nlep 2 #  --applylepSFs
# python plots_VVsemilep.py --pD /eos/user/a/anmehta/www/VVsemilep/ --results --dW plots --year all --finalState ll --nlep 1 #  --applylepSFs
# python plots_VVsemilep.py --pD /eos/user/a/anmehta/www/VVsemilep/ --results --dW cards --year 2016 --finalState elmu --finalState mumu --applylepSFs 
# python plots_VVsemilep.py --pD /eos/user/a/anmehta/www/VVsemilep/ --results --dW cards --year 2016 --finalState 3l m3l --applylepSFs
# python plots_VVsemilep.py --pD /eos/user/a/anmehta/www/VVsemilep/ --results --dW cards --year 2016 --finalState 4l m4l --applylepSFs
#python plots_VVsemilep.py --pD /eos/user/a/anmehta/www/VVsemilep/ --results --dW plots --year 2018 --nLep 1 --finalState boosted --pv dRfjj 
# python plots_VVsemilep.py --pD /eos/user/a/anmehta/www/VVsemilep/ --results --dW plots --year 2018 --nLep 1 --finalState boosted --pv LHE_HT --pf chkHT
#python plots_VVsemilep.py --pD /eos/user/a/anmehta/www/VVsemilep/ --alpha --year 2018 --nLep 1 --finalState boosted --pv  mWV_typ0_pmet_boosted --applylepSFs --lf mu
#python plots_VVsemilep.py --pD /eos/user/a/anmehta/www/VVsemilep/ --simple --genD --year 2018


#python plots_VVsemilep.py --pD /eos/user/a/anmehta/www/VVsemilep/ --results --finalState boosted --nLep 1 --sel SR --pv mWV_typ0_pmet_boosted  --lf mu --lf el --year 2018 --dW plots --applylepSFs --WC c3w --WC ccw --WC cb

# python plots_VVsemilep.py --pD /eos/user/a/anmehta/www/VVsemilep/ --results --finalState boosted --nLep 1 --sel SR --pv FatJet1_pt --pv FatJet1_pt_vBins --pv tGenJetAK8_pt --pv tGenmWV_typ0_pmet_boosted --pv tmWV_typ0_pmet_boosted --lf onelep --year 2018 --dW plots --dCF --applylepSFs
#python plots_VVsemilep.py --pD /eos/user/a/anmehta/www/VVsemilep/ --results --finalState boosted --nLep 1 --sel SR --pv Jet_pt_eta --lf onelep --year 2018 --dW plots
#python plots_VVsemilep.py --pD /eos/user/a/anmehta/www/VVsemilep/ --results --finalState boosted --nLep 1 --sel SR --pv Jet_pt_eta --lf mu --year 2018 --dW cards

#python plots_VVsemilep.py --pD /eos/user/a/anmehta/www/VVsemilep/ --results --finalState boosted --nLep 1 --sel SR --pv FatJet1_sDrop_mass --pv mWV_typ0_pmet_boosted --lf mu --year 2018 --dW plots  --applylepSFs 
#python plots_VVsemilep.py --pD /eos/user/a/anmehta/www/VVsemilep/ --results --finalState boosted --nLep 1 --sel SR --pv debugsel --lf mu --year 2018 --dW plots  --applylepSFs --doWJ


#root://eoscms.cern.ch//eos/cms
