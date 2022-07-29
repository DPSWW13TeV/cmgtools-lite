import os
import ROOT 
conf = dict(
        muPt = 5, 
        elePt = 7, 
        miniRelIso = 0.4, 
        sip3d = 8, 
        dxy =  0.05, 
        dz = 0.1, 
        eleId = "mvaFall17V2noIso_WPL",
)
elMVA_WP=0.70
muMVA_WP=0.90

#FR_selection_cut = ("nGenDressedLepton == 2 && GenDressedLepton_pdgId[0]*GenDressedLepton_pdgId[1] > 0 &&"+ 
#                    "GenDressedLepton_pt[0] > 25 && GenDressedLepton_pt[1] > 20 && "+
#                    "(abs(GenDressedLepton_eta[0]) < (abs(GenDressedLepton_pdgId[0])==13 ? 2.4 : 2.5)) && " + 
#                    "(abs(GenDressedLepton_eta[1]) < (abs(GenDressedLepton_pdgId[1])==13 ? 2.4 : 2.5)) && " + 
#                    "(abs(GenDressedLepton_pdgId[0]) == 13 || (abs(GenDressedLepton_eta[0]) < 1.442 || abs(GenDressedLepton_eta[0]) > 1.556 && abs(GenDressedLepton_pdgId[0])==11)) && "+
#                    "(abs(GenDressedLepton_pdgId[1]) == 13 || (abs(GenDressedLepton_eta[1]) < 1.442 || abs(GenDressedLepton_eta[1]) > 1.556 && abs(GenDressedLepton_pdgId[1])==11)) && "+
#                    "(abs(GenDressedLepton_pdgId[0]*GenDressedLepton_pdgId[1]) == 143 || abs(GenDressedLepton_pdgId[0]*GenDressedLepton_pdgId[1]) == 169) && "+
#                    "(GenDressedLepton_hasTauAnc[0] == 0 && GenDressedLepton_hasTauAnc[1] == 0) && "+
#
#                    cptll	    : if3((abs(GenDressedLepton_pdgId[0]) == 11 || abs(GenDressedLepton_pdgId[1]) == 11),ptll(GenDressedLepton_pt[0], GenDressedLepton_eta[0], GenDressedLepton_phi[0], GenDressedLepton_mass[0], GenDressedLepton_pt[1], GenDressedLepton_eta[1], GenDressedLepton_phi[1], GenDressedLepton_mass[1]) > 20,1)
#                    mll         : mass_2(GenDressedLepton_pt[0],GenDressedLepton_eta[0],GenDressedLepton_phi[0],GenDressedLepton_mass[0],GenDressedLepton_pt[1],GenDressedLepton_eta[1],GenDressedLepton_phi[1],GenDressedLepton_mass[1]) > 12
#                )


ttH_skim_cut = ("nMuon + nElectron >= 2 &&" + 
       "Sum$(Muon_pt > {muPt} && Muon_miniPFRelIso_all < {miniRelIso} && Muon_sip3d < {sip3d}) +"
       "Sum$(Electron_pt > {muPt} && Electron_miniPFRelIso_all < {miniRelIso} && Electron_sip3d < {sip3d} && Electron_{eleId}) >= 2").format(**conf)

loose_skim_cut = ("nMuon + nElectron >= 1 &&" + 
       "Sum$(Muon_pt > {muPt} && Muon_miniPFRelIso_all < {miniRelIso} && Muon_sip3d < {sip3d}) +"
       "Sum$(Electron_pt > {muPt} && Electron_miniPFRelIso_all < {miniRelIso} && Electron_sip3d < {sip3d} && Electron_{eleId}) >= 2").format(**conf)


muonSelection     = lambda l : abs(l.eta) < 2.4 and l.pt > conf["muPt" ] and l.miniPFRelIso_all < conf["miniRelIso"] and l.sip3d < conf["sip3d"] and abs(l.dxy) < conf["dxy"] and abs(l.dz) < conf["dz"]
electronSelection = lambda l : abs(l.eta) < 2.5 and l.pt > conf["elePt"] and l.miniPFRelIso_all < conf["miniRelIso"] and l.sip3d < conf["sip3d"] and abs(l.dxy) < conf["dxy"] and abs(l.dz) < conf["dz"] and getattr(l, conf["eleId"])

muonSelectionV1     = lambda l : abs(l.eta) < 2.4 and l.pt > conf["muPt" ] 
electronSelectionV1 = lambda l : abs(l.eta) < 2.5 and l.pt > conf["elePt"] 


from CMGTools.DPSWW.tools.nanoAOD.dpswwfidevtskimmer import dpswwfidevtskimmer
frskim = dpswwfidevtskimmer(ndleps=2, ssWW = True, noTaus = True)
from CMGTools.DPSWW.tools.nanoAOD.ttHPrescalingLepSkimmer import ttHPrescalingLepSkimmer
# NB: do not wrap lepSkim a lambda, as we modify the configuration in the cfg itself 
lepSkim = ttHPrescalingLepSkimmer(5, 
                muonSel = muonSelection, electronSel = electronSelection,
                minLeptonsNoPrescale = 2, # things with less than 2 leptons are rejected irrespectively of the prescale
                minLeptons = 2, requireSameSignPair = True,
                jetSel = lambda j : j.pt > 25 and abs(j.eta) < 2.4 and j.jetId > 0, 
                minJets = 4, minMET = 70)

from PhysicsTools.NanoAODTools.postprocessing.modules.common.collectionMerger import collectionMerger
lepMerge = collectionMerger(input = ["Electron","Muon"], 
                            output = "LepGood", 
                            selector = dict(Muon = muonSelection, Electron = electronSelection))
lepMergeOnly = collectionMerger(input = ["Electron","Muon"], 
                                output = "LepGood", 
                                selector = dict(Muon = muonSelectionV1, Electron = electronSelectionV1))


from CMGTools.DPSWW.tools.nanoAOD.ttHLeptonCombMasses import ttHLeptonCombMasses
lepMasses = ttHLeptonCombMasses( [ ("Muon",muonSelection), ("Electron",electronSelection) ], maxLeps = 4)

from CMGTools.DPSWW.tools.nanoAOD.autoPuWeight import autoPuWeight
from CMGTools.DPSWW.tools.nanoAOD.yearTagger import yearTag
from CMGTools.DPSWW.tools.nanoAOD.xsecTagger import xsecTag
from CMGTools.DPSWW.tools.nanoAOD.lepJetBTagAdder import lepJetBTagCSV, lepJetBTagDeepCSV, lepJetBTagDeepFlav, lepJetBTagDeepFlavC

ttH_sequence_step1 = [lepSkim, lepMerge, autoPuWeight, yearTag, xsecTag, lepJetBTagCSV, lepJetBTagDeepCSV, lepJetBTagDeepFlav, lepMasses]

dps_fidR_sequence_step1 = [frskim, lepSkim, lepMerge, autoPuWeight, yearTag, xsecTag, lepJetBTagCSV, lepJetBTagDeepCSV, lepJetBTagDeepFlav, lepMasses]
simple_sequence_step1 = dps_fidR_sequence_step1  #[yearTag, xsecTag, frskim] 
simple_skim_cut=("1")
loose_sequence_step1 = [lepMerge, autoPuWeight, yearTag, xsecTag,lepJetBTagCSV, lepJetBTagDeepCSV, lepJetBTagDeepFlav]
#==== 
from PhysicsTools.NanoAODTools.postprocessing.tools import deltaR
from CMGTools.DPSWW.tools.nanoAOD.ttHLepQCDFakeRateAnalyzer import ttHLepQCDFakeRateAnalyzer
centralJetSel = lambda j : j.pt > 25 and abs(j.eta) < 2.4 and j.jetId > 0
lepFR = ttHLepQCDFakeRateAnalyzer(jetSel = centralJetSel,
                                  pairSel = lambda pair : deltaR(pair[0].eta, pair[0].phi, pair[1].eta, pair[1].phi) > 0.7,
                                  maxLeptons = 1, requirePair = True)
from CMGTools.DPSWW.tools.nanoAOD.nBJetCounter import nBJetCounter
nBJetDeepCSV25NoRecl = lambda : nBJetCounter("DeepCSV25", "btagDeepB", centralJetSel)
nBJetDeepFlav25NoRecl = lambda : nBJetCounter("DeepFlav25", "btagDeepFlavB", centralJetSel)

ttH_sequence_step1_FR = [m for m in ttH_sequence_step1 if m != lepSkim] + [ lepFR, nBJetDeepCSV25NoRecl, nBJetDeepFlav25NoRecl ]
ttH_skim_cut_FR = ("nMuon + nElectron >= 1 && nJet >= 1 && Sum$(Jet_pt > 25 && abs(Jet_eta)<2.4) >= 1 &&" + 
       "Sum$(Muon_pt > {muPt} && Muon_miniPFRelIso_all < {miniRelIso} && Muon_sip3d < {sip3d}) +"
       "Sum$(Electron_pt > {muPt} && Electron_miniPFRelIso_all < {miniRelIso} && Electron_sip3d < {sip3d} && Electron_{eleId}) >= 1").format(**conf)


#==== items below are normally run as friends ====

def ttH_idEmu_cuts_E3(lep):
    if (abs(lep.pdgId)!=11): return True
    if (lep.hoe>=(0.10-0.00*(abs(lep.eta+lep.deltaEtaSC)>1.479))): return False
    if (lep.eInvMinusPInv<=-0.04): return False
    if (lep.sieie>=(0.011+0.019*(abs(lep.eta+lep.deltaEtaSC)>1.479))): return False
    return True

def conept_TTH(lep):
    if (abs(lep.pdgId)!=11 and abs(lep.pdgId)!=13): return lep.pt
    if (abs(lep.pdgId)==13 and lep.mediumId>0 and lep.mvaTTH > muMVA_WP) or (abs(lep.pdgId) == 11 and lep.mvaTTH > elMVA_WP): return lep.pt ##here
    else: return 0.90 * lep.pt * (1 + lep.jetRelIso)

def smoothBFlav(jetpt,ptmin,ptmax,year,scale_loose=1.0):
    wploose = (0.0614, 0.0521, 0.0494)
    wpmedium = (0.3093, 0.3033, 0.2770)
    x = min(max(0.0, jetpt - ptmin)/(ptmax-ptmin), 1.0)
    return x*wploose[year-2016]*scale_loose + (1-x)*wpmedium[year-2016]

def clean_and_FO_selection_TTH(lep,year):
    bTagCut = 0.3093 if year==2016 else 0.3033 if year==2017 else 0.2770
    return lep.conept>10 and lep.jetBTagDeepFlav<bTagCut and (abs(lep.pdgId)!=11 or (ttH_idEmu_cuts_E3(lep) and lep.convVeto and lep.lostHits == 0)) \
        and (lep.mvaTTH>(muMVA_WP if abs(lep.pdgId)==13 else elMVA_WP) or \
             (abs(lep.pdgId)==13 and lep.jetBTagDeepFlav< smoothBFlav(0.9*lep.pt*(1+lep.jetRelIso), 20, 45, year) and lep.jetRelIso < 0.50) or \
             (abs(lep.pdgId)==11 and lep.mvaFall17V2noIso_WP80 and lep.jetRelIso < 0.70))

tightLeptonSel = lambda lep,year : clean_and_FO_selection_TTH(lep,year) and (abs(lep.pdgId)!=13 or lep.mediumId>0) and lep.mvaTTH > (muMVA_WP if abs(lep.pdgId)==13 else elMVA_WP)

foTauSel = lambda tau: tau.pt > 20 and abs(tau.eta)<2.3 and abs(tau.dxy) < 1000 and abs(tau.dz) < 0.2 and tau.idDecayModeNewDMs and (int(tau.idDeepTau2017v2p1VSjet)>>1 & 1) # VVLoose WP
tightTauSel = lambda tau: (int(tau.idDeepTau2017v2p1VSjet)>>2 & 1) # VLoose WP

from CMGTools.DPSWW.tools.nanoAOD.jetmetGrouper import groups as jecGroups
from CMGTools.DPSWW.tools.combinedObjectTaggerForCleaning import CombinedObjectTaggerForCleaning
from CMGTools.DPSWW.tools.nanoAOD.fastCombinedObjectRecleaner import fastCombinedObjectRecleaner
recleaner_step1 = lambda : CombinedObjectTaggerForCleaning("InternalRecl",
                                                           looseLeptonSel = lambda lep : lep.miniPFRelIso_all < 0.4 and lep.sip3d < 8 and (abs(lep.pdgId)!=11 or lep.lostHits<=1) and (abs(lep.pdgId)!=13 or lep.looseId),
                                                           cleaningLeptonSel = clean_and_FO_selection_TTH,
                                                           FOLeptonSel = clean_and_FO_selection_TTH,
                                                           tightLeptonSel = tightLeptonSel,
                                                           FOTauSel = foTauSel,
                                                           tightTauSel = tightTauSel,
                                                           selectJet = lambda jet: jet.jetId > 0, # pt and eta cuts are (hard)coded in the step2 
                                                           coneptdef = lambda lep: conept_TTH(lep),
)
recleaner_step2_mc_allvariations = lambda : fastCombinedObjectRecleaner(label="Recl", inlabel="_InternalRecl",
                                                                        cleanTausWithLooseLeptons=True,
                                                                        cleanJetsWithFOTaus=True,
                                                                        doVetoZ=False, doVetoLMf=False, doVetoLMt=False,
                                                                        jetPts=[25,40],
                                                                        jetPtsFwd=[25,60], # second number for 2.7 < abseta < 3, the first for the rest
                                                                        btagL_thr=99, # they are set at runtime 
                                                                        btagM_thr=99,
                                                                        isMC = True,
                                                                        variations= [ 'jes%s'%v for v in jecGroups] + ['jer%s'%x for x in ['barrel','endcap1','endcap2highpt','endcap2lowpt' ,'forwardhighpt','forwardlowpt']  ]  + ['HEM']
)
recleaner_step2_mc = lambda : fastCombinedObjectRecleaner(label="Recl", inlabel="_InternalRecl",
                                                          cleanTausWithLooseLeptons=True,
                                                          cleanJetsWithFOTaus=True,
                                                          doVetoZ=False, doVetoLMf=False, doVetoLMt=False,
                                                          jetPts=[25,40],
                                                          jetPtsFwd=[25,60], # second number for 2.7 < abseta < 3, the first for the rest
                                                          btagL_thr=99, # they are set at runtime 
                                                          btagM_thr=99,
                                                          isMC = True,
                                                          
)
recleaner_step2_data = lambda : fastCombinedObjectRecleaner(label="Recl", inlabel="_InternalRecl",
                                         cleanTausWithLooseLeptons=True,
                                         cleanJetsWithFOTaus=True,
                                         doVetoZ=False, doVetoLMf=False, doVetoLMt=False,
                                         jetPts=[25,40],
                                         jetPtsFwd=[25,60], # second number for 2.7 < abseta < 3, the first for the rest
                                         btagL_thr=-99., # they are set at runtime  
                                         btagM_thr=-99., # they are set at runtime  
                                         isMC = False,
                                         variations = []

)



from CMGTools.DPSWW.tools.eventVars_2lss import EventVars2LSS
eventVars = lambda : EventVars2LSS('','Recl')
eventVars_allvariations = lambda : EventVars2LSS('','Recl',variations = [ 'jes%s'%v for v in jecGroups] + ['jer%s'%x for x in ['barrel','endcap1','endcap2highpt','endcap2lowpt' ,'forwardhighpt','forwardlowpt']  ]  + ['HEM'])

from CMGTools.DPSWW.tools.hjDummCalc import HjDummyCalc
hjDummy = lambda : HjDummyCalc(variations  = [ 'jes%s'%v for v in jecGroups] + ['jer%s'%x for x in ['barrel','endcap1','endcap2highpt','endcap2lowpt' ,'forwardhighpt','forwardlowpt']  ]  + ['HEM'])

from CMGTools.DPSWW.tools.objTagger import ObjTagger
isMatchRightCharge = lambda : ObjTagger('isMatchRightCharge','LepGood', [lambda l,g : (l.genPartFlav==1 or l.genPartFlav == 15) and (g.pdgId*l.pdgId > 0) ], linkColl='GenPart',linkVar='genPartIdx')
mcMatchId     = lambda : ObjTagger('mcMatchId','LepGood', [lambda l : (l.genPartFlav==1 or l.genPartFlav == 15) ])
mcPromptGamma = lambda : ObjTagger('mcPromptGamma','LepGood', [lambda l : (l.genPartFlav==22)])
mcMatch_seq   = [ isMatchRightCharge, mcMatchId ,mcPromptGamma]

countTaus = lambda : ObjTagger('Tight','TauSel_Recl', [lambda t : t.idDeepTau2017v2p1VSjet&4])

from CMGTools.DPSWW.tools.nanoAOD.jetmetGrouper import jetMetCorrelate2016,jetMetCorrelate2017,jetMetCorrelate2018
from PhysicsTools.NanoAODTools.postprocessing.modules.jme.jetmetHelperRun2 import createJMECorrector


jetmetUncertainties2016All = createJMECorrector(dataYear=2016, jesUncert="All")
jetmetUncertainties2017All = createJMECorrector(dataYear=2017, jesUncert="All", metBranchName="METFixEE2017")
jetmetUncertainties2018All = createJMECorrector(dataYear=2016, jesUncert="All")

jme2016_allvariations = [jetmetUncertainties2016All,jetMetCorrelate2016] 
jme2017_allvariations = [jetmetUncertainties2017All,jetMetCorrelate2017]
jme2018_allvariations = [jetmetUncertainties2018All,jetMetCorrelate2018]

jetmetUncertainties2016 = createJMECorrector(dataYear=2016, jesUncert="Total")
jetmetUncertainties2017 = createJMECorrector(dataYear=2017, jesUncert="Total", metBranchName="METFixEE2017")
jetmetUncertainties2018 = createJMECorrector(dataYear=2016, jesUncert="Total")

jme2016 = [jetmetUncertainties2016,jetMetCorrelate2016] 
jme2017 = [jetmetUncertainties2017,jetMetCorrelate2017]
jme2018 = [jetmetUncertainties2018,jetMetCorrelate2018]



def _fires(ev, path):
    if "/hasfiredtriggers_cc.so" not in ROOT.gSystem.GetLibraries():
        ROOT.gROOT.ProcessLine(".L %s/src/CMGTools/Production/src/hasfiredtriggers.cc+O" % os.environ['CMSSW_BASE'])
    if not hasattr(ev,path): return False 
    if ev.run == 1:  # is MC
        return getattr( ev,path ) 
    return getattr(ROOT, 'fires_%s_%d'%(path,ev.year))( ev.run, getattr(ev,path))

triggerGroups=dict(
    Trigger_1e={
        2016 : lambda ev : _fires(ev,'HLT_Ele27_WPTight_Gsf') or _fires(ev,'HLT_Ele25_eta2p1_WPTight_Gsf') or _fires(ev,'HLT_Ele27_eta2p1_WPLoose_Gsf'),
        2017 : lambda ev : _fires(ev,'HLT_Ele32_WPTight_Gsf') or _fires(ev,'HLT_Ele35_WPTight_Gsf'),
        2018 : lambda ev : _fires(ev,'HLT_Ele32_WPTight_Gsf'),
    },
    Trigger_1m={
        2016 : lambda ev : _fires(ev,'HLT_IsoMu24') or _fires(ev,'HLT_IsoTkMu24') or _fires(ev,'HLT_IsoMu22_eta2p1') or _fires(ev,'HLT_IsoTkMu22_eta2p1') or _fires(ev,'HLT_IsoMu22') or _fires(ev,'HLT_IsoTkMu22'),
        2017 : lambda ev : _fires(ev,'HLT_IsoMu24') or _fires(ev,'HLT_IsoMu27'),
        2018 : lambda ev : _fires(ev,'HLT_IsoMu24'),
    },
    Trigger_2e={
        2016 : lambda ev : _fires(ev,'HLT_Ele23_Ele12_CaloIdL_TrackIdL_IsoVL_DZ'),
        2017 : lambda ev : _fires(ev,'HLT_Ele23_Ele12_CaloIdL_TrackIdL_IsoVL'),
        2018 : lambda ev : _fires(ev,'HLT_Ele23_Ele12_CaloIdL_TrackIdL_IsoVL'),
    },
    Trigger_2m={
        2016 : lambda ev : _fires(ev,'HLT_Mu17_TrkIsoVVL_Mu8_TrkIsoVVL') or _fires(ev,'HLT_Mu17_TrkIsoVVL_TkMu8_TrkIsoVVL') or  _fires(ev,'HLT_Mu17_TrkIsoVVL_Mu8_TrkIsoVVL_DZ') or _fires(ev,'HLT_Mu17_TrkIsoVVL_TkMu8_TrkIsoVVL_DZ'),
        2017 : lambda ev : _fires(ev,'HLT_Mu17_TrkIsoVVL_Mu8_TrkIsoVVL_DZ_Mass8') or _fires(ev,'HLT_Mu17_TrkIsoVVL_Mu8_TrkIsoVVL_DZ_Mass3p8'),
        2018 : lambda ev : _fires(ev,'HLT_Mu17_TrkIsoVVL_Mu8_TrkIsoVVL_DZ_Mass3p8'),
    },
    Trigger_em={
        2016 :  lambda ev : _fires(ev, 'HLT_Mu8_TrkIsoVVL_Ele23_CaloIdL_TrackIdL_IsoVL') or _fires(ev,'HLT_Mu8_TrkIsoVVL_Ele23_CaloIdL_TrackIdL_IsoVL_DZ') \
        or _fires(ev, 'HLT_Mu23_TrkIsoVVL_Ele8_CaloIdL_TrackIdL_IsoVL') or _fires(ev,'HLT_Mu23_TrkIsoVVL_Ele8_CaloIdL_TrackIdL_IsoVL_DZ'),
        2017 :  lambda ev : _fires(ev,'HLT_Mu23_TrkIsoVVL_Ele12_CaloIdL_TrackIdL_IsoVL')\
        or _fires(ev,'HLT_Mu23_TrkIsoVVL_Ele12_CaloIdL_TrackIdL_IsoVL_DZ')\
        or _fires(ev,'HLT_Mu12_TrkIsoVVL_Ele23_CaloIdL_TrackIdL_IsoVL_DZ')\
        or _fires(ev,'HLT_Mu8_TrkIsoVVL_Ele23_CaloIdL_TrackIdL_IsoVL_DZ'),
        2018 :  lambda ev : _fires(ev,'HLT_Mu23_TrkIsoVVL_Ele12_CaloIdL_TrackIdL_IsoVL')\
        or _fires(ev,'HLT_Mu8_TrkIsoVVL_Ele23_CaloIdL_TrackIdL_IsoVL_DZ')\
        or _fires(ev,'HLT_Mu12_TrkIsoVVL_Ele23_CaloIdL_TrackIdL_IsoVL_DZ'),
    },
    Trigger_3e={
        2016 : lambda ev : _fires(ev,'HLT_Ele16_Ele12_Ele8_CaloIdL_TrackIdL'),
        2017 : lambda ev : _fires(ev,'HLT_Ele16_Ele12_Ele8_CaloIdL_TrackIdL'),
        2018 : lambda ev : _fires(ev,'HLT_Ele16_Ele12_Ele8_CaloIdL_TrackIdL'), # prescaled in the two years according to https://twiki.cern.ch/twiki/bin/view/CMS/EgHLTRunIISummary#2018
    },
    Trigger_3m={
        2016 : lambda ev : _fires(ev,'HLT_TripleMu_12_10_5'),
        2017 : lambda ev : _fires(ev,'HLT_TripleMu_12_10_5'),
        2018 : lambda ev : _fires(ev,'HLT_TripleMu_12_10_5'),
    },
    Trigger_mee={
        2016 : lambda ev : _fires(ev,'HLT_Mu8_DiEle12_CaloIdL_TrackIdL'),
        2017 : lambda ev : _fires(ev,'HLT_Mu8_DiEle12_CaloIdL_TrackIdL'),
        2018 : lambda ev : _fires(ev,'HLT_Mu8_DiEle12_CaloIdL_TrackIdL'),
    },
    Trigger_mme={
        2016 : lambda ev : _fires(ev,'HLT_DiMu9_Ele9_CaloIdL_TrackIdL'),
        2017 : lambda ev : _fires(ev,'HLT_DiMu9_Ele9_CaloIdL_TrackIdL_DZ'),
        2018 : lambda ev : _fires(ev,'HLT_DiMu9_Ele9_CaloIdL_TrackIdL_DZ'),
    },
    Trigger_2lss={
        2016 : lambda ev : ev.Trigger_1e or ev.Trigger_1m or ev.Trigger_2e or ev.Trigger_2m or ev.Trigger_em,
        2017 : lambda ev : ev.Trigger_1e or ev.Trigger_1m or ev.Trigger_2e or ev.Trigger_2m or ev.Trigger_em,
        2018 : lambda ev : ev.Trigger_1e or ev.Trigger_1m or ev.Trigger_2e or ev.Trigger_2m or ev.Trigger_em,
    },
    Trigger_3l={
        2016 : lambda ev : ev.Trigger_2lss or ev.Trigger_3e or ev.Trigger_3m or ev.Trigger_mee or ev.Trigger_mme,
        2017 : lambda ev : ev.Trigger_2lss or ev.Trigger_3e or ev.Trigger_3m or ev.Trigger_mee or ev.Trigger_mme,
        2018 : lambda ev : ev.Trigger_2lss or ev.Trigger_3e or ev.Trigger_3m or ev.Trigger_mee or ev.Trigger_mme,
    },
    Trigger_MET={
        2016 : lambda ev : _fires(ev,'HLT_PFMET120_PFMHT120_IDTight'),
        2017 : lambda ev : _fires(ev,'HLT_PFMET120_PFMHT120_IDTight'),
        2018 : lambda ev : _fires(ev,'HLT_PFMET120_PFMHT120_IDTight'),
    }
)


triggerGroups_dict=dict(
    Trigger_1e={
        2016 :  ['HLT_Ele27_WPTight_Gsf' , 'HLT_Ele25_eta2p1_WPTight_Gsf' , 'HLT_Ele27_eta2p1_WPLoose_Gsf'],
        2017 :  ['HLT_Ele32_WPTight_Gsf' , 'HLT_Ele35_WPTight_Gsf'],
        2018 :  ['HLT_Ele32_WPTight_Gsf'],
    },
    Trigger_1m={
        2016 :  ['HLT_IsoMu24' , 'HLT_IsoTkMu24' , 'HLT_IsoMu22_eta2p1' , 'HLT_IsoTkMu22_eta2p1' , 'HLT_IsoMu22' , 'HLT_IsoTkMu22'],
        2017 :  ['HLT_IsoMu24' , 'HLT_IsoMu27'],
        2018 :  ['HLT_IsoMu24'],
    },
    Trigger_2e={
        2016 :  ['HLT_Ele23_Ele12_CaloIdL_TrackIdL_IsoVL_DZ'],
        2017 :  ['HLT_Ele23_Ele12_CaloIdL_TrackIdL_IsoVL'],
        2018 :  ['HLT_Ele23_Ele12_CaloIdL_TrackIdL_IsoVL'],
    },
    Trigger_2m={
        2016 :  ['HLT_Mu17_TrkIsoVVL_Mu8_TrkIsoVVL' , 'HLT_Mu17_TrkIsoVVL_TkMu8_TrkIsoVVL' ,  'HLT_Mu17_TrkIsoVVL_Mu8_TrkIsoVVL_DZ' , 'HLT_Mu17_TrkIsoVVL_TkMu8_TrkIsoVVL_DZ'],
        2017 :  ['HLT_Mu17_TrkIsoVVL_Mu8_TrkIsoVVL_DZ_Mass8' , 'HLT_Mu17_TrkIsoVVL_Mu8_TrkIsoVVL_DZ_Mass3p8'],
        2018 :  ['HLT_Mu17_TrkIsoVVL_Mu8_TrkIsoVVL_DZ_Mass3p8'],
    },
    Trigger_em={
        2016 :   ['HLT_Mu8_TrkIsoVVL_Ele23_CaloIdL_TrackIdL_IsoVL' , 'HLT_Mu8_TrkIsoVVL_Ele23_CaloIdL_TrackIdL_IsoVL_DZ', 'HLT_Mu23_TrkIsoVVL_Ele8_CaloIdL_TrackIdL_IsoVL' , 'HLT_Mu23_TrkIsoVVL_Ele8_CaloIdL_TrackIdL_IsoVL_DZ'],
        2017 :   ['HLT_Mu23_TrkIsoVVL_Ele12_CaloIdL_TrackIdL_IsoVL', 'HLT_Mu23_TrkIsoVVL_Ele12_CaloIdL_TrackIdL_IsoVL_DZ'        , 'HLT_Mu12_TrkIsoVVL_Ele23_CaloIdL_TrackIdL_IsoVL_DZ'        , 'HLT_Mu8_TrkIsoVVL_Ele23_CaloIdL_TrackIdL_IsoVL_DZ'],
        2018 :   ['HLT_Mu23_TrkIsoVVL_Ele12_CaloIdL_TrackIdL_IsoVL', 'HLT_Mu8_TrkIsoVVL_Ele23_CaloIdL_TrackIdL_IsoVL_DZ'        , 'HLT_Mu12_TrkIsoVVL_Ele23_CaloIdL_TrackIdL_IsoVL_DZ'],
    },
    Trigger_3e={
        2016 :  ['HLT_Ele16_Ele12_Ele8_CaloIdL_TrackIdL'],
        2017 :  ['HLT_Ele16_Ele12_Ele8_CaloIdL_TrackIdL'],
        2018 :  ['HLT_Ele16_Ele12_Ele8_CaloIdL_TrackIdL'], # prescaled in the two years according to https://twiki.cern.ch/twiki/bin/view/CMS/EgHLTRunIISummary#2018
    },
    Trigger_3m={
        2016 :  ['HLT_TripleMu_12_10_5'],
        2017 :  ['HLT_TripleMu_12_10_5'],
        2018 :  ['HLT_TripleMu_12_10_5'],
    },
    Trigger_mee={
        2016 :  ['HLT_Mu8_DiEle12_CaloIdL_TrackIdL'],
        2017 :  ['HLT_Mu8_DiEle12_CaloIdL_TrackIdL'],
        2018 :  ['HLT_Mu8_DiEle12_CaloIdL_TrackIdL'],
    },
    Trigger_mme={
        2016 :  ['HLT_DiMu9_Ele9_CaloIdL_TrackIdL'   ],
        2017 :  ['HLT_DiMu9_Ele9_CaloIdL_TrackIdL_DZ'],
        2018 :  ['HLT_DiMu9_Ele9_CaloIdL_TrackIdL_DZ'],
    },
)


from CMGTools.DPSWW.tools.evtTagger import EvtTagger

Trigger_1e   = lambda : EvtTagger('Trigger_1e',[ lambda ev : triggerGroups['Trigger_1e'][ev.year](ev) ])
Trigger_1m   = lambda : EvtTagger('Trigger_1m',[ lambda ev : triggerGroups['Trigger_1m'][ev.year](ev) ])
Trigger_2e   = lambda : EvtTagger('Trigger_2e',[ lambda ev : triggerGroups['Trigger_2e'][ev.year](ev) ])
Trigger_2m   = lambda : EvtTagger('Trigger_2m',[ lambda ev : triggerGroups['Trigger_2m'][ev.year](ev) ])
Trigger_em   = lambda : EvtTagger('Trigger_em',[ lambda ev : triggerGroups['Trigger_em'][ev.year](ev) ])
Trigger_3e   = lambda : EvtTagger('Trigger_3e',[ lambda ev : triggerGroups['Trigger_3e'][ev.year](ev) ])
Trigger_3m   = lambda : EvtTagger('Trigger_3m',[ lambda ev : triggerGroups['Trigger_3m'][ev.year](ev) ])
Trigger_mee  = lambda : EvtTagger('Trigger_mee',[ lambda ev : triggerGroups['Trigger_mee'][ev.year](ev) ])
Trigger_mme  = lambda : EvtTagger('Trigger_mme',[ lambda ev : triggerGroups['Trigger_mme'][ev.year](ev) ])
Trigger_2lss = lambda : EvtTagger('Trigger_2lss',[ lambda ev : triggerGroups['Trigger_2lss'][ev.year](ev) ])
Trigger_3l   = lambda : EvtTagger('Trigger_3l',[ lambda ev : triggerGroups['Trigger_3l'][ev.year](ev) ])
Trigger_MET  = lambda : EvtTagger('Trigger_MET',[ lambda ev : triggerGroups['Trigger_MET'][ev.year](ev) ])

triggerSequence = [Trigger_1e,Trigger_1m,Trigger_2e,Trigger_2m,Trigger_em,Trigger_3e,Trigger_3m,Trigger_mee,Trigger_mme,Trigger_2lss,Trigger_3l]# ,Trigger_MET] am


from CMGTools.DPSWW.tools.BDT_eventReco_cpp import BDT_eventReco

BDThttTT_Hj = lambda : BDT_eventReco(os.environ["CMSSW_BASE"]+'/src/CMGTools/TTHAnalysis/data/kinMVA/tth/TMVAClassification_bloose_BDTG.weights.xml',
                                     os.environ["CMSSW_BASE"]+'/src/CMGTools/TTHAnalysis/data/kinMVA/tth/TMVAClassification_btight_BDTG.weights.xml',
                                     os.environ["CMSSW_BASE"]+'/src/CMGTools/TTHAnalysis/data/kinMVA/tth/Hjtagger_legacy_xgboost_v1.weights.xml',
                                     os.environ["CMSSW_BASE"]+'/src/CMGTools/TTHAnalysis/data/kinMVA/tth/Hjj_csv_BDTG.weights.xml',
                                     os.environ["CMSSW_BASE"]+'/src/CMGTools/TTHAnalysis/data/kinMVA/tth/resTop_xgb_csv_order_deepCTag.xml.gz',
                                     os.environ["CMSSW_BASE"]+'/src/CMGTools/TTHAnalysis/data/kinMVA/tth/HTT_HadTopTagger_2017_nomasscut_nvar17_resolved.xml',
                                     os.environ["CMSSW_BASE"]+'/src/CMGTools/TTHAnalysis/data/kinMVA/tth/TF_jets_kinfit_httTT.root',
                                     algostring = 'k_httTT_Hj',
                                     csv_looseWP = 0.5426, 
                                     csv_mediumWP = 0.8484,
                                     selection = [
                                         lambda leps,jets,event : len(leps)>=2,
                                         lambda leps,jets,event : leps[0].conePt>20 and leps[1].conePt>10,
                                     ]
)

BDThttTT_allvariations = lambda : BDT_eventReco(os.environ["CMSSW_BASE"]+'/src/CMGTools/TTHAnalysis/data/kinMVA/tth/TMVAClassification_bloose_BDTG.weights.xml',
                                                os.environ["CMSSW_BASE"]+'/src/CMGTools/TTHAnalysis/data/kinMVA/tth/TMVAClassification_btight_BDTG.weights.xml',
                                                os.environ["CMSSW_BASE"]+'/src/CMGTools/TTHAnalysis/data/kinMVA/tth/Hjtagger_legacy_xgboost_v1.weights.xml',
                                                os.environ["CMSSW_BASE"]+'/src/CMGTools/TTHAnalysis/data/kinMVA/tth/Hjj_csv_BDTG.weights.xml',
                                                os.environ["CMSSW_BASE"]+'/src/CMGTools/TTHAnalysis/data/kinMVA/tth/resTop_xgb_csv_order_deepCTag.xml.gz',
                                                os.environ["CMSSW_BASE"]+'/src/CMGTools/TTHAnalysis/data/kinMVA/tth/HTT_HadTopTagger_2017_nomasscut_nvar17_resolved.xml',
                                                os.environ["CMSSW_BASE"]+'/src/CMGTools/TTHAnalysis/data/kinMVA/tth/TF_jets_kinfit_httTT.root',
                                                algostring = 'k_httTT_Hj',
                                                csv_looseWP = 0.5426, 
                                                csv_mediumWP = 0.8484,
                                                selection = [
                                                    lambda leps,jets,event : len(leps)>=2,
                                                    lambda leps,jets,event : leps[0].conePt>20 and leps[1].conePt>10,
                                                ],
                                                variations = [ 'jes%s'%v for v in jecGroups] + ['jer%s'%x for x in ['barrel','endcap1','endcap2highpt','endcap2lowpt' ,'forwardhighpt','forwardlowpt']  ]  + ['HEM'] ,
)



from CMGTools.TTHAnalysis.tools.finalMVA_DNN import finalMVA_DNN
finalMVA = lambda : finalMVA_DNN() # use this for data
finalMVA_allVars = lambda : finalMVA_DNN( variations = [ 'jes%s'%v for v in jecGroups] + ['jer%s'%x for x in ['barrel','endcap1','endcap2highpt','endcap2lowpt' ,'forwardhighpt','forwardlowpt']  ]  + ['HEM'])

from CMGTools.TTHAnalysis.tools.finalMVA_DNN_3l import finalMVA_DNN_3l
finalMVA3L = lambda : finalMVA_DNN_3l() # use this for data
finalMVA3L_allVars = lambda : finalMVA_DNN_3l(variations = [ 'jes%s'%v for v in jecGroups] + ['jer%s'%x for x in ['barrel','endcap1','endcap2highpt','endcap2lowpt' ,'forwardhighpt','forwardlowpt']  ]  + ['HEM'])

from CMGTools.TTHAnalysis.tools.nanoAOD.finalMVA_4l import FinalMVA_4L
finalMVA_4l = lambda : FinalMVA_4L()


from PhysicsTools.NanoAODTools.postprocessing.modules.btv.btagSFProducer import btagSFProducer


btagSF2016_dj_allVars = lambda : btagSFProducer("Legacy2016",'deepjet',collName="JetSel_Recl",storeOutput=False,perJesComponents=True)
btagSF2017_dj_allVars = lambda : btagSFProducer("2017",'deepjet',collName="JetSel_Recl",storeOutput=False,perJesComponents=True)
btagSF2018_dj_allVars = lambda : btagSFProducer("2018",'deepjet',collName="JetSel_Recl",storeOutput=False,perJesComponents=True)

btagSF2016_dj = lambda : btagSFProducer("Legacy2016",'deepjet',collName="JetSel_Recl",storeOutput=False)
btagSF2017_dj = lambda : btagSFProducer("2017",'deepjet',collName="JetSel_Recl",storeOutput=False)
btagSF2018_dj = lambda : btagSFProducer("2018",'deepjet',collName="JetSel_Recl",storeOutput=False)

from CMGTools.DPSWW.tools.nanoAOD.BtagSFs import BtagSFs
bTagSFs = lambda : BtagSFs("JetSel_Recl",
                           corrs = {"" : 1.},
                           #corrs={  "AbsoluteScale": 1., "AbsoluteStat":0., "FlavorQCD":1.,"Fragmentation":1.,"PileUpDataMC":0.5,"PileUpPtBB":0.5,"PileUpPtEC1":0.5,"PileUpPtEC2":0.5,"PileUpPtHF":0.5,"PileUpPtRef":0.5,"RelativeFSR":0.5,"RelativeJEREC1":0., "RelativeJEREC2":0., "RelativeJERHF":0.5,"RelativePtBB":0.5,"RelativePtEC1":0.,"RelativePtEC2":0.,"RelativePtHF":0.5, "RelativeBal":0.5, "RelativeStatEC":0., "RelativeStatFSR":0., "RelativeStatHF":0.,"SinglePionECAL":1., "SinglePionHCAL": 1., "TimePtEta":0., "AbsoluteMPFBias": 1.} # relative sample not there 
                       )

bTagSFs_allvars = lambda : BtagSFs("JetSel_Recl",
                                   corrs=jecGroups,
                       )

from CMGTools.DPSWW.tools.nanoAOD.lepScaleFactors import lepScaleFactors
leptonSFs = lambda : lepScaleFactors()

from CMGTools.DPSWW.tools.nanoAOD.puwtProducer import puwtProducer
newpuwts = lambda : puwtProducer()


scaleFactorSequence_2016 = [btagSF2016_dj,bTagSFs] 
scaleFactorSequence_2017 = [btagSF2017_dj,bTagSFs] 
scaleFactorSequence_2018 = [btagSF2018_dj,bTagSFs]

scaleFactorSequence_allVars_2016 = [btagSF2016_dj_allVars,bTagSFs_allvars] 
scaleFactorSequence_allVars_2017 = [btagSF2017_dj_allVars,bTagSFs_allvars] 
scaleFactorSequence_allVars_2018 = [btagSF2018_dj_allVars,bTagSFs_allvars]


from CMGTools.DPSWW.tools.nanoAOD.higgsDecayFinder import higgsDecayFinder
higgsDecay = lambda : higgsDecayFinder()

from CMGTools.DPSWW.tools.nanoAOD.VHsplitter import VHsplitter
vhsplitter = lambda : VHsplitter()

# from CMGTools.DPSWW.tools.synchTools import SynchTuples
# synchTuples = lambda : SynchTuples()


# instructions to friend trees  code 

# 0_jmeUnc_v1
# mc only (per year) 
# jetmetUncertainties2016 
# jetmetUncertainties2017
# jetmetUncertainties2018

# 3_recleaner_v0 (recleaner, also containing mc matching and trigger bits) 
# recleaner_step1,recleaner_step2_mc,mcMatch_seq,higgsDecay,triggerSequence (MC)
# recleaner_step1,recleaner_step2_data,triggerSequence (data)

# 4_leptonSFs_v0 (lepton, trigger and btag scale factors, to run after recleaning) 
# mc only (per year)
# scaleFactorSequence_2016
# scaleFactorSequence_2017
# scaleFactorSequence_2018

from CMGTools.DPSWW.tools.nanoAOD.W_vars import W_vars
wvars2016MC = lambda : W_vars(2016,True)
wvars2017MC = lambda : W_vars(2017,True)
wvars2018MC = lambda : W_vars(2018,True)
from CMGTools.DPSWW.tools.nanoAOD.DPSWW_vars import DPSWW_vars

dpsvars2016MC = lambda : DPSWW_vars(os.environ["CMSSW_BASE"]+'/src/CMGTools/DPSWW/data/fakerate/fr_2016_MVA_mupt90_elpt70.root','FR_mva090_mu_data_comb','FR_mva070_el_data_comb_NC',2016,True)
dpsvars2017MC = lambda : DPSWW_vars(os.environ["CMSSW_BASE"]+'/src/CMGTools/DPSWW/data/fakerate/fr_2017_MVA_mupt90_elpt70.root','FR_mva090_mu_data_comb','FR_mva070_el_data_comb_NC',2017,True)
dpsvars2018MC = lambda : DPSWW_vars(os.environ["CMSSW_BASE"]+'/src/CMGTools/DPSWW/data/fakerate/fr_2018_MVA_mupt90_elpt70.root','FR_mva090_mu_data_comb','FR_mva070_el_data_comb_NC',2018,True)

dpsvars2016data = lambda : DPSWW_vars(os.environ["CMSSW_BASE"]+'/src/CMGTools/DPSWW/data/fakerate/fr_2016_MVA_mupt90_elpt70.root','FR_mva090_mu_data_comb','FR_mva070_el_data_comb_NC',2016,False)
dpsvars2017data = lambda : DPSWW_vars(os.environ["CMSSW_BASE"]+'/src/CMGTools/DPSWW/data/fakerate/fr_2017_MVA_mupt90_elpt70.root','FR_mva090_mu_data_comb','FR_mva070_el_data_comb_NC',2017,False)
dpsvars2018data = lambda : DPSWW_vars(os.environ["CMSSW_BASE"]+'/src/CMGTools/DPSWW/data/fakerate/fr_2018_MVA_mupt90_elpt70.root','FR_mva090_mu_data_comb','FR_mva070_el_data_comb_NC',2018,False)

from CMGTools.DPSWW.tools.nanoAOD.muon_prefiring_sfs import muon_prefiring_sfs
sfs_2016=lambda : muon_prefiring_sfs("2016",os.environ["CMSSW_BASE"]+'/src/CMGTools/DPSWW/data/L1MuonPrefiring_wts_2016.root')
sfs_2017=lambda : muon_prefiring_sfs("2017",os.environ["CMSSW_BASE"]+'/src/CMGTools/DPSWW/data/L1MuonPrefiring_wts_2016.root')
sfs_2018=lambda : muon_prefiring_sfs("2018",os.environ["CMSSW_BASE"]+'/src/CMGTools/DPSWW/data/L1MuonPrefiring_wts_2016.root')

from CMGTools.DPSWW.tools.nanoAOD.muon_prefiring_maps import muon_prefiring_maps
prefiringwt_2016=lambda : muon_prefiring_maps("2016",os.environ["CMSSW_BASE"]+'/src/CMGTools/DPSWW/data/L1MuonPrefiring_wts_2016.root')

from CMGTools.DPSWW.tools.nanoAOD.BDT_DPSWW import BDT_DPSWW

##ambdtvars_withcpt_2016 = lambda : BDT_DPSWW(2016,True)
##ambdtvars_withcpt_2017 = lambda : BDT_DPSWW(2017,True)
##ambdtvars_withcpt_2018 = lambda : BDT_DPSWW(2018,True)
bdtvars_withpt_2016  = lambda : BDT_DPSWW(2016,False)
bdtvars_withpt_2017  = lambda : BDT_DPSWW(2017,False)
bdtvars_withpt_2018  = lambda : BDT_DPSWW(2018,False)

bdtvars_withpt_2016VarU  = lambda : BDT_DPSWW(2016,False,['all'],['Up'])
bdtvars_withpt_2017VarU  = lambda : BDT_DPSWW(2017,False,['all'],['Up'])
bdtvars_withpt_2018VarU  = lambda : BDT_DPSWW(2018,False,['all'],['Up'])
bdtvars_withpt_2016VarD  = lambda : BDT_DPSWW(2016,False,['all'],['Down'])
bdtvars_withpt_2017VarD  = lambda : BDT_DPSWW(2017,False,['all'],['Down'])
bdtvars_withpt_2018VarD  = lambda : BDT_DPSWW(2018,False,['all'],['Down'])


bdtvars_withpt_2016Up  = lambda : BDT_DPSWW(2016,False,['unclustEn'],['Up'])
bdtvars_withpt_2017Up  = lambda : BDT_DPSWW(2017,False,['unclustEn'],['Up'])
bdtvars_withpt_2018Up  = lambda : BDT_DPSWW(2018,False,['unclustEn'],['Up'])
bdtvars_withpt_2016Down  = lambda : BDT_DPSWW(2016,False,['unclustEn'],['Down'])
bdtvars_withpt_2017Down  = lambda : BDT_DPSWW(2017,False,['unclustEn'],['Down'])
bdtvars_withpt_2018Down  = lambda : BDT_DPSWW(2018,False,['unclustEn'],['Down'])

##ambdtvars_withcpt_2016Down = lambda : BDT_DPSWW(2016,True,'Down')
##ambdtvars_withcpt_2017Down = lambda : BDT_DPSWW(2017,True,'Down')
##ambdtvars_withcpt_2018Down = lambda : BDT_DPSWW(2018,True,'Down')
##ambdtvars_withpt_2016Down  = lambda : BDT_DPSWW(2016,False,'Down')
##ambdtvars_withpt_2017Down  = lambda : BDT_DPSWW(2017,False,'Down')
##ambdtvars_withpt_2018Down  = lambda : BDT_DPSWW(2018,False,'Down')



from CMGTools.DPSWW.tools.nanoAOD.genInfo_py8_fur_taus import genInfo_py8_fur_taus
postfsrInfoPy_taus = lambda : genInfo_py8_fur_taus()

from CMGTools.DPSWW.tools.nanoAOD.npdf_rms import npdf_rms
rms_val = lambda : npdf_rms()


from CMGTools.DPSWW.tools.nanoAOD.genInfo_hw_fur_taus import genInfo_hw_fur_taus
postfsrInfohw_taus = lambda : genInfo_hw_fur_taus()

from CMGTools.DPSWW.tools.nanoAOD.genInfo_py8 import genInfo_py8
postfsrInfoPy = lambda : genInfo_py8()

from CMGTools.DPSWW.tools.nanoAOD.genInfo_hw import genInfo_hw
postfsrInfoHw = lambda : genInfo_hw()


from CMGTools.DPSWW.tools.nanoAOD.addTnpTree import addTnpTree
tnpvars = lambda : addTnpTree()
#tnpTrees = [autoPuWeight, tnpvars]
#from CMGTools.DPSWW.tools.nanoAOD.collectionMerger_DPSWW import collectionMerger_DPSWW
#mergedvars = collectionMerger_DPSWW() #selector = dict(Muon = muonSelection, Electron = electronSelection))


# 5_evtVars_v0
from CMGTools.DPSWW.tools.nanoAOD.ttH_gen_reco import ttH_gen_reco
#
#from CMGTools.DPSWW.tools.topRecoSemiLept import TopRecoSemiLept
#topRecoModule = lambda : TopRecoSemiLept(constraints=['kWHadMass','kWLepMass','kTopLepMass','kTopHadMass'])
