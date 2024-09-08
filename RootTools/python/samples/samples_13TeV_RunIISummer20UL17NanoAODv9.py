# COMPONENT CREATOR
from CMGTools.RootTools.samples.ComponentCreator import ComponentCreator
kreator = ComponentCreator()
import os 


# # QCD enriched (cross sections form genXSecAna)
QCD_Mu15 = kreator.makeMyPrivateMCComponent("QCD_Mu15", "/QCD_Pt-20_MuEnrichedPt15_TuneCP5_13TeV-pythia8/sesanche-QCD_Mu15_UL17-c18b9e6b5256da8f58acfdd6c3d6d61d/USER", "PRIVATE", ".*root", 'phys03', 237800)
# QCD_Pt15to20_Mu5    = kreator.makeMCComponent("QCD_Pt15to20_Mu5"    , "/QCD_Pt-15to20_MuEnrichedPt5_TuneCP5_13TeV_pythia8/RunIIAutumn18NanoAODv4-Nano14Dec2018_102X_upgrade2018_realistic_v16-v1/NANOAODSIM", "CMS" , ".*root", 2.785e+06)
QCD_Pt20to30_Mu5    = kreator.makeMyPrivateMCComponent("QCD_Pt20to30_Mu5"    , "/QCD_Pt-20To30_MuEnrichedPt5_TuneCP5_13TeV-pythia8/sesanche-QCD_Pt20to30_Mu5_UL17-c18b9e6b5256da8f58acfdd6c3d6d61d/USER", "PRIVATE" , ".*root", 'phys03', 2.49e+06)
QCD_Pt30to50_Mu5    = kreator.makeMyPrivateMCComponent("QCD_Pt30to50_Mu5", "/QCD_Pt-30To50_MuEnrichedPt5_TuneCP5_13TeV-pythia8/sesanche-QCD_Pt30to50_Mu5_UL17-c18b9e6b5256da8f58acfdd6c3d6d61d/USER", "PRIVATE", ".*root", 'phys03', 1.364e+06)
QCD_Pt50to80_Mu5    = kreator.makeMCComponent("QCD_Pt50to80_Mu5"    , "/QCD_Pt-50To80_MuEnrichedPt5_TuneCP5_13TeV-pythia8/RunIISummer20UL17NanoAODv9-106X_mc2017_realistic_v9-v2/NANOAODSIM" , "CMS" , ".*root", 377400)
QCD_Pt80to120_Mu5   = kreator.makeMCComponent("QCD_Pt80to120_Mu5"   , "/QCD_Pt-80To120_MuEnrichedPt5_TuneCP5_13TeV-pythia8/RunIISummer20UL17NanoAODv9-106X_mc2017_realistic_v9-v2/NANOAODSIM", "CMS" , ".*root", 88350)
QCD_Pt120to170_Mu5  = kreator.makeMCComponent("QCD_Pt120to170_Mu5"  , "/QCD_Pt-120To170_MuEnrichedPt5_TuneCP5_13TeV-pythia8/RunIISummer20UL17NanoAODv9-106X_mc2017_realistic_v9-v2/NANOAODSIM", "CMS" , ".*root", 21250)
QCD_Pt170to300_Mu5  = kreator.makeMCComponent("QCD_Pt170to300_Mu5", "/QCD_Pt-170To300_MuEnrichedPt5_TuneCP5_13TeV-pythia8/RunIISummer20UL17NanoAODv9-106X_mc2017_realistic_v9-v2/NANOAODSIM", "CMS", ".*root", 6969)
QCD_Pt300to470_Mu5  = kreator.makeMCComponent("QCD_Pt300to470_Mu5"  , "/QCD_Pt-300to470_MuEnrichedPt5_TuneCP5_13TeV_pythia8/RunIIAutumn18NanoAODv4-Nano14Dec2018_102X_upgrade2018_realistic_v16-v1/NANOAODSIM", "CMS" , ".*root", 619.5)

# QCD_Pt300to470_Mu5_ext3  = kreator.makeMCComponent("QCD_Pt300to470_Mu5_ext3"  , "/QCD_Pt-300to470_MuEnrichedPt5_TuneCP5_13TeV_pythia8/RunIIAutumn18NanoAODv4-Nano14Dec2018_102X_upgrade2018_realistic_v16_ext3-v1/NANOAODSIM", "CMS" , ".*root", 619.5)
# QCD_Pt470to600_Mu5  = kreator.makeMCComponent("QCD_Pt470to600_Mu5"  , "/QCD_Pt-470to600_MuEnrichedPt5_TuneCP5_13TeV_pythia8/RunIIAutumn18NanoAODv4-Nano14Dec2018_102X_upgrade2018_realistic_v16-v1/NANOAODSIM", "CMS" , ".*root", 58.9)
# QCD_Pt470to600_Mu5_ext1  = kreator.makeMCComponent("QCD_Pt470to600_Mu5_ext1"  , "/QCD_Pt-470to600_MuEnrichedPt5_TuneCP5_13TeV_pythia8/RunIIAutumn18NanoAODv4-Nano14Dec2018_102X_upgrade2018_realistic_v16_ext1-v1/NANOAODSIM", "CMS" , ".*root", 58.9)
# QCD_Pt600to800_Mu5  = kreator.makeMCComponent("QCD_Pt600to800_Mu5", "/QCD_Pt-600to800_MuEnrichedPt5_TuneCP5_13TeV_pythia8/RunIIAutumn18NanoAODv4-Nano14Dec2018_102X_upgrade2018_realistic_v16-v1/NANOAODSIM", "CMS", ".*root", 18.36)
# QCD_Pt800to1000_Mu5 = kreator.makeMCComponent("QCD_Pt800to1000_Mu5" , "/QCD_Pt-800to1000_MuEnrichedPt5_TuneCP5_13TeV_pythia8/RunIIAutumn18NanoAODv4-Nano14Dec2018_102X_upgrade2018_realistic_v16_ext3-v1/NANOAODSIM", "CMS" , ".*root", 3.253)
# QCD_Pt1000toInf_Mu5 = kreator.makeMCComponent("QCD_Pt1000toInf_Mu5" , "/QCD_Pt-1000toInf_MuEnrichedPt5_TuneCP5_13TeV_pythia8/RunIIAutumn18NanoAODv4-Nano14Dec2018_102X_upgrade2018_realistic_v16-v1/NANOAODSIM", "CMS" , ".*root", 1.075)

QCD_Mu5s = [
    QCD_Pt20to30_Mu5,
    QCD_Pt30to50_Mu5,
    QCD_Pt50to80_Mu5,
    QCD_Pt80to120_Mu5,
    QCD_Pt120to170_Mu5,
    QCD_Pt170to300_Mu5,
 ]
QCD_Mus = [ QCD_Mu15 ] + QCD_Mu5s

# # QCD EMEnr  (cross sections form genXSecAna)
# QCD_Pt15to20_EMEnriched   = kreator.makeMCComponent("QCD_Pt15to20_EMEnriched"  ,"/QCD_Pt-15to20_EMEnriched_TuneCP5_13TeV_pythia8/RunIIAutumn18NanoAODv4-Nano14Dec2018_102X_upgrade2018_realistic_v16_ext1-v1/NANOAODSIM"  , "CMS", ".*root",  1.33e+06)
QCD_Pt20to30_EMEnriched   = kreator.makeMyPrivateMCComponent("QCD_Pt20to30_EMEnriched"  ,"/QCD_Pt-20to30_EMEnriched_TuneCP5_13TeV-pythia8/sesanche-Summer20UL17-3f0b140a720de1c801ff414923884f7b/USER"  , "PRIVATE", ".*root",  "phys03", 4.928e+06)




QCD_Pt30to50_EMEnriched   = kreator.makeMCComponent("QCD_Pt30to50_EMEnriched"  ,"/QCD_Pt-30to50_EMEnriched_TuneCP5_13TeV-pythia8/RunIISummer20UL17NanoAODv9-106X_mc2017_realistic_v9-v2/NANOAODSIM"  , "CMS", ".*root",  6.41e+06)
QCD_Pt50to80_EMEnriched   = kreator.makeMCComponent("QCD_Pt50to80_EMEnriched", "/QCD_Pt-50to80_EMEnriched_TuneCP5_13TeV-pythia8/RunIISummer20UL17NanoAODv9-106X_mc2017_realistic_v9-v2/NANOAODSIM", "CMS", ".*root",  1.986e+06)
QCD_Pt80to120_EMEnriched  = kreator.makeMCComponent("QCD_Pt80to120_EMEnriched" ,"/QCD_Pt-80to120_EMEnriched_TuneCP5_13TeV-pythia8/RunIISummer20UL17NanoAODv9-106X_mc2017_realistic_v9-v2/NANOAODSIM" , "CMS", ".*root",  370900)
QCD_Pt120to170_EMEnriched = kreator.makeMCComponent("QCD_Pt120to170_EMEnriched","/QCD_Pt-120to170_EMEnriched_TuneCP5_13TeV-pythia8/RunIISummer20UL17NanoAODv9-106X_mc2017_realistic_v9-v2/NANOAODSIM", "CMS", ".*root",  66760)
QCD_Pt170to300_EMEnriched = kreator.makeMCComponent("QCD_Pt170to300_EMEnriched","/QCD_Pt-170to300_EMEnriched_TuneCP5_13TeV-pythia8/RunIISummer20UL17NanoAODv9-106X_mc2017_realistic_v9-v2/NANOAODSIM", "CMS", ".*root",  16430)
QCD_Pt300toInf_EMEnriched = kreator.makeMCComponent("QCD_Pt300toInf_EMEnriched","/QCD_Pt-300toInf_EMEnriched_TuneCP5_13TeV-pythia8/RunIISummer20UL17NanoAODv9-106X_mc2017_realistic_v9-v2/NANOAODSIM", "CMS", ".*root",  1101)

QCD_EMs = [
     QCD_Pt20to30_EMEnriched,
     QCD_Pt30to50_EMEnriched,
     QCD_Pt50to80_EMEnriched,
     QCD_Pt80to120_EMEnriched,
     QCD_Pt120to170_EMEnriched,
     QCD_Pt170to300_EMEnriched,
     QCD_Pt300toInf_EMEnriched
 ]

QCD_Pt15to30_bcToE   = kreator.makeMCComponent("QCD_Pt15to30_bcToE","/QCD_Pt_15to30_TuneCP5_13TeV_pythia8/RunIISummer20UL17NanoAODv9-106X_mc2017_realistic_v9-v1/NANOAODSIM"  , "CMS", ".*root", 1245000000)
QCD_Pt30to80_bcToE   = kreator.makeMCComponent("QCD_Pt30to80_bcToE",   "/QCD_Pt_30to80_bcToE_TuneCP5_13TeV_pythia8/RunIISummer20UL17NanoAODv9-106X_mc2017_realistic_v9-v1/NANOAODSIM"  , "CMS", ".*root", 361500)
QCD_Pt80to170_bcToE  = kreator.makeMCComponent("QCD_Pt80to170_bcToE",  "/QCD_Pt_80to170_bcToE_TuneCP5_13TeV_pythia8/RunIISummer20UL17NanoAODv9-106X_mc2017_realistic_v9-v1/NANOAODSIM" , "CMS", ".*root", 33770)
QCD_Pt170to250_bcToE = kreator.makeMCComponent("QCD_Pt170to250_bcToE", "/QCD_Pt_170to250_bcToE_TuneCP5_13TeV_pythia8/RunIISummer20UL17NanoAODv9-106X_mc2017_realistic_v9-v1/NANOAODSIM", "CMS", ".*root", 2126)
QCD_Pt250toInf_bcToE = kreator.makeMCComponent("QCD_Pt250toInf_bcToE", "/QCD_Pt_250toInf_bcToE_TuneCP5_13TeV_pythia8/RunIISummer20UL17NanoAODv9-106X_mc2017_realistic_v9-v1/NANOAODSIM", "CMS", ".*root", 563.1)

QCD_bcToE = [
    QCD_Pt15to30_bcToE,
    #QCD_Pt20to30_bcToE,
    QCD_Pt30to80_bcToE,
    QCD_Pt80to170_bcToE,
    QCD_Pt170to250_bcToE,
    QCD_Pt250toInf_bcToE,
]

# # ====== W + Jets ======
WJetsToLNu_LO = kreator.makeMCComponent("WJetsToLNu_LO","/WJetsToLNu_TuneCP5_13TeV-madgraphMLM-pythia8/RunIISummer20UL17NanoAODv9-106X_mc2017_realistic_v9-v1/NANOAODSIM", "CMS", ".*root", 3* 20508.9)
                                                          
# ## LO XSec from genXSecAna times NNLO/LO XSec for inclusive W+jets
W1JetsToLNu_LO = kreator.makeMCComponent("W1JetsToLNu_LO","/W1JetsToLNu_TuneCP5_13TeV-madgraphMLM-pythia8/RunIISummer20UL17NanoAODv9-106X_mc2017_realistic_v9-v1/NANOAODSIM", "CMS", ".*root", 8123*1.17)
W2JetsToLNu_LO = kreator.makeMCComponent("W2JetsToLNu_LO","/W2JetsToLNu_TuneCP5_13TeV-madgraphMLM-pythia8/RunIISummer20UL17NanoAODv9-106X_mc2017_realistic_v9-v1/NANOAODSIM", "CMS", ".*root", 2785*1.17)
W3JetsToLNu_LO = kreator.makeMCComponent("W3JetsToLNu_LO","/W3JetsToLNu_TuneCP5_13TeV-madgraphMLM-pythia8/RunIISummer20UL17NanoAODv9-106X_mc2017_realistic_v9-v1/NANOAODSIM", "CMS", ".*root", 993.4*1.17)
W4JetsToLNu_LO = kreator.makeMCComponent("W4JetsToLNu_LO","/W4JetsToLNu_TuneCP5_13TeV-madgraphMLM-pythia8/RunIISummer20UL17NanoAODv9-106X_mc2017_realistic_v9-v2/NANOAODSIM", "CMS", ".*root", 542.4*1.17)

# XSec from genXSecAna
WJetsToLNu_012JetsNLO_34JetsLO = kreator.makeMCComponent("WJetsToLNu_012JetsNLO_34JetsLO","/WJetsToLNu_012JetsNLO_34JetsLO_EWNLOcorr_13TeV-sherpa/RunIISummer20UL17NanoAODv9-106X_mc2017_realistic_v9-v1/NANOAODSIM",  "CMS", ".*root", 6.228e+04)

# ### W+jets HT-binned
WJetsToLNu_HT70To100      = kreator.makeMCComponent("WJetsToLNu_HT70To100","/WJetsToLNu_HT-70To100_TuneCP5_13TeV-madgraphMLM-pythia8/RunIISummer20UL17NanoAODv9-106X_mc2017_realistic_v9-v1/NANOAODSIM", "CMS", ".*root",1271*1.21)
WJetsToLNu_HT100to200     = kreator.makeMCComponent("WJetsToLNu_HT100to200", "/WJetsToLNu_HT-100To200_TuneCP5_13TeV-madgraphMLM-pythia8/RunIISummer20UL17NanoAODv9-106X_mc2017_realistic_v9-v1/NANOAODSIM", "CMS", ".*root",1253*1.21) 
WJetsToLNu_HT200to400     = kreator.makeMCComponent("WJetsToLNu_HT200to400", "/WJetsToLNu_HT-200To400_TuneCP5_13TeV-madgraphMLM-pythia8/RunIISummer20UL17NanoAODv9-106X_mc2017_realistic_v9-v1/NANOAODSIM", "CMS", ".*root",335.9*1.21) 
WJetsToLNu_HT400to600     = kreator.makeMCComponent("WJetsToLNu_HT400to600", "/WJetsToLNu_HT-400To600_TuneCP5_13TeV-madgraphMLM-pythia8/RunIISummer20UL17NanoAODv9-106X_mc2017_realistic_v9-v1/NANOAODSIM", "CMS", ".*root",45.21*1.21) 
WJetsToLNu_HT600to800     = kreator.makeMCComponent("WJetsToLNu_HT600to800", "/WJetsToLNu_HT-600To800_TuneCP5_13TeV-madgraphMLM-pythia8/RunIISummer20UL17NanoAODv9-106X_mc2017_realistic_v9-v1/NANOAODSIM", "CMS", ".*root",10.99*1.21) 
WJetsToLNu_HT800to1200    = kreator.makeMCComponent("WJetsToLNu_HT800to1200", "/WJetsToLNu_HT-800To1200_TuneCP5_13TeV-madgraphMLM-pythia8/RunIISummer20UL17NanoAODv9-106X_mc2017_realistic_v9-v3/NANOAODSIM", "CMS", ".*root",4.936*1.21) 
WJetsToLNu_HT1200to2500   = kreator.makeMCComponent("WJetsToLNu_HT1200to2500","/WJetsToLNu_HT-1200To2500_TuneCP5_13TeV-madgraphMLM-pythia8/RunIISummer20UL17NanoAODv9-106X_mc2017_realistic_v9-v1/NANOAODSIM", "CMS", ".*root",1.156*1.21) 
WJetsToLNu_HT2500toInf    = kreator.makeMCComponent("WJetsToLNu_HT2500toInf", "/WJetsToLNu_HT-2500ToInf_TuneCP5_13TeV-madgraphMLM-pythia8/RunIISummer20UL17NanoAODv9-106X_mc2017_realistic_v9-v2/NANOAODSIM", "CMS", ".*root",0.0263*1.21) 

WJetsToLNuHT = [
    WJetsToLNu_HT70To100,
    WJetsToLNu_HT100to200,
    WJetsToLNu_HT200to400,
    WJetsToLNu_HT400to600,
    WJetsToLNu_HT600to800,
    WJetsToLNu_HT800to1200,
    WJetsToLNu_HT1200to2500,
    WJetsToLNu_HT2500toInf,
]



# # ====== TT INCLUSIVE =====

# # TTbar cross section: NNLO, https://twiki.cern.ch/twiki/bin/view/LHCPhysics/TtbarNNLO (172.5)

TTSemi_pow = kreator.makeMCComponent("TTSemi_pow", "/TTToSemiLeptonic_TuneCP5_13TeV-powheg-pythia8/RunIISummer20UL17NanoAODv9-106X_mc2017_realistic_v9-v1/NANOAODSIM", "CMS", ".*root", 831.76*2*(3*0.108)*(1-3*0.108) )

TT_mttp7kto1k = kreator.makeMCComponent("TT_mttp7kto1k","/TT_Mtt-700to1000_TuneCP5_13TeV-powheg-pythia8/RunIISummer20UL17NanoAODv9-106X_mc2017_realistic_v9-v2/NANOAODSIM", "CMS", ".*root", 6.472e+01*1.21)
TT_mtt1ktoinf = kreator.makeMCComponent("TT_mtt1ktoinf","/TT_Mtt-1000toInf_TuneCP5_13TeV-powheg-pythia8/RunIISummer20UL17NanoAODv9-106X_mc2017_realistic_v9-v2/NANOAODSIM", "CMS", ".*root", 1.644e+01*1.21) 

TTs = [ 
        TTSemi_pow,TT_mttp7kto1k,TT_mtt1ktoinf
]

# # ====== SINGLE TOP ======
# # Single top cross sections: https://twiki.cern.ch/twiki/bin/viewauth/CMS/SingleTopSigma

T_sch = kreator.makeMCComponent("T_sch","/ST_s-channel_4f_leptonDecays_TuneCP5_13TeV-amcatnlo-pythia8/RunIISummer20UL17NanoAODv9-20UL17JMENano_106X_mc2017_realistic_v9-v1/NANOAODSIM", "CMS", ".*root",3.549e+00,fracNegWeights=1.735e-01)

T_tch             = kreator.makeMCComponent("T_tch", "/ST_t-channel_top_4f_InclusiveDecays_TuneCP5_13TeV-powheg-madspin-pythia8/RunIISummer20UL17NanoAODv9-106X_mc2017_realistic_v9-v1/NANOAODSIM","CMS", ".*root", 134) # inclusive sample
Tbar_tch           = kreator.makeMCComponent("Tbar_tch", "/ST_t-channel_antitop_4f_InclusiveDecays_TuneCP5_13TeV-powheg-madspin-pythia8/RunIISummer20UL17NanoAODv9-106X_mc2017_realistic_v9-v1/NANOAODSIM", "CMS", ".*root", 80.0) # inclusive sample

T_tWch_noFullyHad    = kreator.makeMCComponent("T_tWch_noFullyHad",    "/ST_tW_top_5f_NoFullyHadronicDecays_TuneCP5_13TeV-powheg-pythia8/RunIISummer20UL17NanoAODv9-106X_mc2017_realistic_v9-v1/NANOAODSIM",     "CMS", ".*root",19.55)
Tbar_tWch_noFullyHad = kreator.makeMCComponent("Tbar_tWch_noFullyHad", "/ST_tW_antitop_5f_NoFullyHadronicDecays_TuneCP5_13TeV-powheg-pythia8/RunIISummer20UL17NanoAODv9-106X_mc2017_realistic_v9-v1/NANOAODSIM", "CMS", ".*root",19.55)

Ts = [
     T_sch,
     T_tch, Tbar_tch,
     T_tWch_noFullyHad, Tbar_tWch_noFullyHad
]

# # ====== T(T) + BOSON =====



# # ===  DI-BOSONS



basepath_eos="/eos/cms/store/group/phys_smp/ec/anmehta/Combined_aTGC_Apr2024_UL17/"


WmZToLmNujj_01j_aTGC_pTZ_150toInf_mWV_150to600=kreator.makeMCComponentSimple('WmZToLmNujj_01j_aTGC_pTZ_150toInf_mWV_150to600',"/WZToLNujj_01j_aTGC/RunIISummer20UL18NanoAODv9-Dummy/NANOAODSIM",basepath_eos,5.401e-01*0.69911,prefix='root://xrootd-cms.infn.it/')
WmZToLmNujj_01j_aTGC_pTZ_150toInf_mWV_600to800=kreator.makeMCComponentSimple('WmZToLmNujj_01j_aTGC_pTZ_150toInf_mWV_600to800',"/WZToLNujj_01j_aTGC/RunIISummer20UL18NanoAODv9-Dummy/NANOAODSIM",basepath_eos,8.544e-02*0.69911,prefix='root://xrootd-cms.infn.it/')
WmZToLmNujj_01j_aTGC_pTZ_150toInf_mWV_800toInf=kreator.makeMCComponentSimple('WmZToLmNujj_01j_aTGC_pTZ_150toInf_mWV_800toInf',"/WZToLNujj_01j_aTGC/RunIISummer20UL18NanoAODv9-Dummy/NANOAODSIM",basepath_eos,9.101e-02*0.69911,prefix='root://xrootd-cms.infn.it/')
WpZToLpNujj_01j_aTGC_pTZ_150toInf_mWV_150to600=kreator.makeMCComponentSimple('WpZToLpNujj_01j_aTGC_pTZ_150toInf_mWV_150to600',"/WZToLNujj_01j_aTGC/RunIISummer20UL18NanoAODv9-Dummy/NANOAODSIM",basepath_eos,8.658e-01*0.69911,prefix='root://xrootd-cms.infn.it/')
WpZToLpNujj_01j_aTGC_pTZ_150toInf_mWV_600to800=kreator.makeMCComponentSimple('WpZToLpNujj_01j_aTGC_pTZ_150toInf_mWV_600to800',"/WZToLNujj_01j_aTGC/RunIISummer20UL18NanoAODv9-Dummy/NANOAODSIM",basepath_eos,1.561e-01*0.69911,prefix='root://xrootd-cms.infn.it/')
WpZToLpNujj_01j_aTGC_pTZ_150toInf_mWV_800toInf=kreator.makeMCComponentSimple('WpZToLpNujj_01j_aTGC_pTZ_150toInf_mWV_800toInf',"/WZToLNujj_01j_aTGC/RunIISummer20UL18NanoAODv9-Dummy/NANOAODSIM",basepath_eos,2.199e-01*0.69911,prefix='root://xrootd-cms.infn.it/')

WmWpToLmNujj_01j_aTGC_pTW_150toInf_mWV_150to600=kreator.makeMCComponentSimple('WmWpToLmNujj_01j_aTGC_pTW_150toInf_mWV_150to600',"/WWToLNujj_01j_aTGC/RunIISummer20UL18NanoAODv9-Dummy/NANOAODSIM",basepath_eos,2.109*0.6741,prefix='root://xrootd-cms.infn.it/')
WmWpToLmNujj_01j_aTGC_pTW_150toInf_mWV_600to800=kreator.makeMCComponentSimple('WmWpToLmNujj_01j_aTGC_pTW_150toInf_mWV_600to800',"/WWToLNujj_01j_aTGC/RunIISummer20UL18NanoAODv9-Dummy/NANOAODSIM",basepath_eos,3.568e-01*0.6741,prefix='root://xrootd-cms.infn.it/')
WmWpToLmNujj_01j_aTGC_pTW_150toInf_mWV_800toInf=kreator.makeMCComponentSimple('WmWpToLmNujj_01j_aTGC_pTW_150toInf_mWV_800toInf',"/WWToLNujj_01j_aTGC/RunIISummer20UL18NanoAODv9-Dummy/NANOAODSIM",basepath_eos,3.806e-01*0.6741,prefix='root://xrootd-cms.infn.it/')
WpWmToLpNujj_01j_aTGC_pTW_150toInf_mWV_150to600=kreator.makeMCComponentSimple('WpWmToLpNujj_01j_aTGC_pTW_150toInf_mWV_150to600',"/WWToLNujj_01j_aTGC/RunIISummer20UL18NanoAODv9-Dummy/NANOAODSIM",basepath_eos,2.014e+00*0.6741,prefix='root://xrootd-cms.infn.it/')
WpWmToLpNujj_01j_aTGC_pTW_150toInf_mWV_600to800=kreator.makeMCComponentSimple('WpWmToLpNujj_01j_aTGC_pTW_150toInf_mWV_600to800',"/WWToLNujj_01j_aTGC/RunIISummer20UL18NanoAODv9-Dummy/NANOAODSIM",basepath_eos,3.467e-01*0.6741,prefix='root://xrootd-cms.infn.it/')
WpWmToLpNujj_01j_aTGC_pTW_150toInf_mWV_800toInf=kreator.makeMCComponentSimple('WpWmToLpNujj_01j_aTGC_pTW_150toInf_mWV_800toInf',"/WWToLNujj_01j_aTGC/RunIISummer20UL18NanoAODv9-Dummy/NANOAODSIM",basepath_eos,3.713e-01*0.6741,prefix='root://xrootd-cms.infn.it/')


ZZTo2Q2L = kreator.makeMCComponent("ZZTo2Q2L","/ZZTo2Q2L_mllmin4p0_TuneCP5_13TeV-amcatnloFXFX-pythia8/RunIISummer20UL17NanoAODv9-106X_mc2017_realistic_v9-v1/NANOAODSIM","CMS", ".*root",2.33)
ZH = kreator.makeMCComponent("ZH","/ZH_HToBB_ZToLL_M-125_TuneCP5_13TeV-powheg-pythia8/RunIISummer20UL17NanoAODv9-106X_mc2017_realistic_v9-v1/NANOAODSIM", "CMS", ".*root", 7.977e-02)

WZTo1L1Nu2Q           = kreator.makeMCComponent("WZTo1L1Nu2Q","/WZTo1L1Nu2Q_4f_TuneCP5_13TeV-amcatnloFXFX-pythia8/RunIISummer20UL17NanoAODv9-106X_mc2017_realistic_v9-v1/NANOAODSIM", "CMS", ".*root", 9.370, fracNegWeights=2.049e-01)
WWTo1L1Nu2Q           = kreator.makeMCComponent("WWTo1L1Nu2Q","/WWTo1L1Nu2Q_4f_TuneCP5_13TeV-amcatnloFXFX-pythia8/RunIISummer20UL17NanoAODv9-106X_mc2017_realistic_v9-v1/NANOAODSIM", "CMS", ".*root",5.090e+01,fracNegWeights=2.011e-01)



GluGluToContinToZZTo4e      =  kreator.makeMCComponent("GluGluToContinToZZTo4e", "/GluGluToContinToZZTo4e_TuneCP5_13TeV-mcfm701-pythia8/RunIISummer20UL17NanoAODv9-106X_mc2017_realistic_v9-v2/NANOAODSIM",  "CMS", ".*root", 0.00159*1.7) # generator cross section times 1.7 k-factor (SMP-19-001, AN-2019/004)
GluGluToContinToZZTo4mu     =  kreator.makeMCComponent("GluGluToContinToZZTo4mu", "/GluGluToContinToZZTo4mu_TuneCP5_13TeV-mcfm701-pythia8/RunIISummer20UL17NanoAODv9-106X_mc2017_realistic_v9-v2/NANOAODSIM",  "CMS", ".*root", 0.00159*1.7) # generator cross section times 1.7 k-factor (SMP-19-001, AN-2019/004)
GluGluToContinToZZTo4tau    =  kreator.makeMCComponent("GluGluToContinToZZTo4tau", "/GluGluToContinToZZTo4tau_TuneCP5_13TeV-mcfm701-pythia8/RunIISummer20UL17NanoAODv9-106X_mc2017_realistic_v9-v2/NANOAODSIM",  "CMS", ".*root", 0.00159*1.7) # generator cross section times 1.7 k-factor (SMP-19-001, AN-2019/004)
GluGluToContinToZZTo2e2mu   =  kreator.makeMCComponent("GluGluToContinToZZTo2e2mu", "/GluGluToContinToZZTo2e2mu_TuneCP5_13TeV-mcfm701-pythia8/RunIISummer20UL17NanoAODv9-106X_mc2017_realistic_v9-v2/NANOAODSIM",  "CMS", ".*root", 0.00319*1.7) # generator cross section times 1.7 k-factor (SMP-19-001, AN-2019/004)
GluGluToContinToZZTo2e2tau  =  kreator.makeMCComponent("GluGluToContinToZZTo2e2tau", "/GluGluToContinToZZTo2e2tau_TuneCP5_13TeV-mcfm701-pythia8/RunIISummer20UL17NanoAODv9-106X_mc2017_realistic_v9-v2/NANOAODSIM",  "CMS", ".*root", 0.00319*1.7) # generator cross section times 1.7 k-factor (SMP-19-001, AN-2019/004)
GluGluToContinToZZTo2mu2tau =  kreator.makeMCComponent("GluGluToContinToZZTo2mu2tau", "/GluGluToContinToZZTo2mu2tau_TuneCP5_13TeV-mcfm701-pythia8/RunIISummer20UL17NanoAODv9-106X_mc2017_realistic_v9-v2/NANOAODSIM",  "CMS", ".*root", 0.00319*1.7) # generator cross section times 1.7 k-factor (SMP-19-001, AN-2019/004)

WminusH = kreator.makeMCComponent("WminusH","/WminusH_HToBB_WToLNu_M-125_TuneCP5_13TeV-powheg-pythia8/RunIISummer20UL17NanoAODv9-106X_mc2017_realistic_v9-v1/NANOAODSIM", "CMS", ".*root",1.770e-01)
WplusH = kreator.makeMCComponent("WplusH","/WplusH_HToBB_WToLNu_M-125_TuneCP5_13TeV-powheg-pythia8/RunIISummer20UL17NanoAODv9-106X_mc2017_realistic_v9-v1/NANOAODSIM", "CMS", ".*root", 2.832e-01)
VHToNonbb = kreator.makeMCComponent("VHToNonbb", "/VHToNonbb_M125_TuneCP5_13TeV-amcatnloFXFX_madspin_pythia8/RunIISummer20UL17NanoAODv9-106X_mc2017_realistic_v9-v2/NANOAODSIM", "CMS", ".*root", 0.9561)


DiBosons = [ZZTo2Q2L,WZTo1L1Nu2Q,WWTo1L1Nu2Q,ZH,WminusH,WplusH,VHToNonbb,
    WmWpToLmNujj_01j_aTGC_pTW_150toInf_mWV_150to600,
    WpWmToLpNujj_01j_aTGC_pTW_150toInf_mWV_150to600,
    WpWmToLpNujj_01j_aTGC_pTW_150toInf_mWV_600to800,
    WpWmToLpNujj_01j_aTGC_pTW_150toInf_mWV_800toInf,
    WmWpToLmNujj_01j_aTGC_pTW_150toInf_mWV_600to800,
    WmWpToLmNujj_01j_aTGC_pTW_150toInf_mWV_800toInf,
    WmZToLmNujj_01j_aTGC_pTZ_150toInf_mWV_150to600,
    WmZToLmNujj_01j_aTGC_pTZ_150toInf_mWV_600to800,
    WpZToLpNujj_01j_aTGC_pTZ_150toInf_mWV_800toInf,
    WpZToLpNujj_01j_aTGC_pTZ_150toInf_mWV_150to600,
    WpZToLpNujj_01j_aTGC_pTZ_150toInf_mWV_600to800,
    WmZToLmNujj_01j_aTGC_pTZ_150toInf_mWV_800toInf,

]

# # ===  TRI-BOSONS



# # other Higgs processes

GGHZZ4L = kreator.makeMCComponent("GGHZZ4L", "/GluGluHToZZTo4L_M125_TuneCP5_13TeV_powheg2_JHUGenV7011_pythia8/RunIISummer20UL17NanoAODv9-106X_mc2017_realistic_v9-v2/NANOAODSIM", "CMS", ".*root", 0.01212)
Higgs = [
    GGHZZ4L,

]


# # ----------------------------- summary ----------------------------------------



mcSamples =  WJetsToLNuHT +  TTs + Ts +  DiBosons  + QCD_bcToE + QCD_EMs + QCD_Mus



samples = mcSamples

# ---------------------------------------------------------------------

if __name__ == "__main__":
    from CMGTools.RootTools.samples.tools import runMain
    runMain(samples, localobjs=locals())
