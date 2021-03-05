# COMPONENT CREATOR
from CMGTools.RootTools.samples.ComponentCreator import ComponentCreator
kreator = ComponentCreator()


# ====== W + Jets ======
WJetsToLNu_LO = kreator.makeMCComponent("WJetsToLNu_LO","/WJetsToLNu_TuneCP5_13TeV-madgraphMLM-pythia8/RunIIAutumn18NanoAODv7-Nano02Apr2020_102X_upgrade2018_realistic_v21-v1/NANOAODSIM", "CMS", ".*root", 3* 20508.9)
WJetsToLNu = kreator.makeMCComponent("WJetsToLNu_ext","/WJetsToLNu_TuneCP5_13TeV-amcatnloFXFX-pythia8/RunIIAutumn18NanoAODv7-Nano02Apr2020_102X_upgrade2018_realistic_v21-v1/NANOAODSIM", "CMS", ".*root", 3* 20508.9, fracNegWeights=0.16)

W0JetsToLNu =  kreator.makeMCComponent("W0JetsToLNu", "/WJetsToLNu_0J_TuneCP5_13TeV-amcatnloFXFX-pythia8/RunIIAutumn18NanoAODv7-Nano02Apr2020_102X_upgrade2018_realistic_v21-v1/NANOAODSIM", "CMS", ".*root", 50131.98)

W1JetsToLNu =  kreator.makeMCComponent("W1JetsToLNu", "/WJetsToLNu_1J_TuneCP5_13TeV-amcatnloFXFX-pythia8/RunIIAutumn18NanoAODv7-Nano02Apr2020_102X_upgrade2018_realistic_v21-v1/NANOAODSIM", "CMS", ".*root", 8426.09)
W2JetsToLNu =  kreator.makeMCComponent("W2JetsToLNu", "/WJetsToLNu_2J_TuneCP5_13TeV-amcatnloFXFX-pythia8/RunIIAutumn18NanoAODv7-Nano02Apr2020_102X_upgrade2018_realistic_v21-v1/NANOAODSIM", "CMS", ".*root", 3172.96)


W1JetsToLNu_LO =  kreator.makeMCComponent("W1JetsToLNu_LO", "/W1JetsToLNu_TuneCP5_13TeV-madgraphMLM-pythia8/RunIIAutumn18NanoAODv7-Nano02Apr2020_102X_upgrade2018_realistic_v21-v1/NANOAODSIM", "CMS", ".*root",  8123*1.17)

W2JetsToLNu_LO =  kreator.makeMCComponent("W2JetsToLNu_LO", "/W2JetsToLNu_TuneCP5_13TeV-madgraphMLM-pythia8/RunIIAutumn18NanoAODv7-Nano02Apr2020_102X_upgrade2018_realistic_v21-v1/NANOAODSIM", "CMS", ".*root", 2785*1.17)


W3JetsToLNu_LO =  kreator.makeMCComponent("W3JetsToLNu_LO", "/W3JetsToLNu_TuneCP5_13TeV-madgraphMLM-pythia8/RunIIAutumn18NanoAODv7-Nano02Apr2020_102X_upgrade2018_realistic_v21-v1/NANOAODSIM", "CMS", ".*root", 993.4*1.17)


W4JetsToLNu_LO =  kreator.makeMCComponent("W4JetsToLNu_LO", "/W4JetsToLNu_TuneCP5_13TeV-madgraphMLM-pythia8/RunIIAutumn18NanoAODv7-Nano02Apr2020_102X_upgrade2018_realistic_v21-v1/NANOAODSIM", "CMS", ".*root", 542.4*1.17)



# ====== Z + Jets ======
## New FEWZ cross section 1921.8 from https://twiki.cern.ch/twiki/bin/viewauth/CMS/StandardModelCrossSectionsat13TeV
DYJetsToLL_M50_LO = kreator.makeMCComponent("DYJetsToLL_M50_LO", "/DYJetsToLL_M-50_TuneCP5_13TeV-madgraphMLM-pythia8/RunIIAutumn18NanoAODv7-Nano02Apr2020_102X_upgrade2018_realistic_v21-v1/NANOAODSIM", "CMS", ".*root", 1921.8*3)
DYJetsToLL_M50 =  kreator.makeMCComponent("DYJetsToLL_M50", "/DYJetsToLL_M-50_TuneCP5_13TeV-amcatnloFXFX-pythia8/RunIIAutumn18NanoAODv7-Nano02Apr2020_102X_upgrade2018_realistic_v21-v1/NANOAODSIM", "CMS", ".*root", 1921.8*3, fracNegWeights=0.16)
DYJetsToLL_M50_ext =  kreator.makeMCComponent("DYJetsToLL_M50_ext", "/DYJetsToLL_M-50_TuneCP5_13TeV-amcatnloFXFX-pythia8/RunIIAutumn18NanoAODv7-Nano02Apr2020_102X_upgrade2018_realistic_v21_ext2-v1/NANOAODSIM", "CMS", ".*root", 1921.8*3, fracNegWeights=0.16)


DYJetsToLL_M10to50_LO =  kreator.makeMCComponent("DYJetsToLL_M10to50_LO", "/DYJetsToLL_M-10to50_TuneCP5_13TeV-madgraphMLM-pythia8/RunIIAutumn18NanoAODv7-Nano02Apr2020_102X_upgrade2018_realistic_v21-v1/NANOAODSIM", "CMS", ".*root", 15810)
DYJetsToLL_M10to50_LO_ext =  kreator.makeMCComponent("DYJetsToLL_M10to50_LO_ext", "/DYJetsToLL_M-10to50_TuneCP5_13TeV-madgraphMLM-pythia8/RunIIAutumn18NanoAODv7-Nano02Apr2020_102X_upgrade2018_realistic_v21_ext1-v1/NANOAODSIM", "CMS", ".*root", 15810)


EWK = [ 
    WJetsToLNu_LO,
    WJetsToLNu,
    W0JetsToLNu,
    W1JetsToLNu,
    W2JetsToLNu,
    WJetsToLNu_LO,
    W1JetsToLNu_LO,
    W2JetsToLNu_LO,
    W3JetsToLNu_LO,
    W4JetsToLNu_LO,
    DYJetsToLL_M50,
    DYJetsToLL_M50_ext,
    DYJetsToLL_M50_LO,
    DYJetsToLL_M10to50_LO,
    DYJetsToLL_M10to50_LO_ext
]




# ====== TT INCLUSIVE =====

# TTbar cross section: NNLO, https://twiki.cern.ch/twiki/bin/view/LHCPhysics/TtbarNNLO (172.5)

TTJets = kreator.makeMCComponent("TTJets", "/TTJets_TuneCP5_13TeV-amcatnloFXFX-pythia8/RunIIAutumn18NanoAODv7-Nano02Apr2020_102X_upgrade2018_realistic_v21_ext1-v1/NANOAODSIM", "CMS", ".*root", 831.76, fracNegWeights=0.319)
TTJets_DiLepton = kreator.makeMCComponent("TTJets_DiLepton", "/TTJets_DiLept_TuneCP5_13TeV-madgraphMLM-pythia8/RunIIAutumn18NanoAODv7-Nano02Apr2020_102X_upgrade2018_realistic_v21-v1/NANOAODSIM"     , "CMS", ".*root", 831.76*((3*0.108)**2) )
TTW_LO = kreator.makeMCComponent("TTW_LO", "/ttWJets_TuneCP5_13TeV_madgraphMLM_pythia8/RunIIAutumn18NanoAODv7-Nano02Apr2020_102X_upgrade2018_realistic_v21_ext1-v1/NANOAODSIM", "CMS", ".*root",  0.6105 )
TTZ_LO = kreator.makeMCComponent("TTZ_LO", "/ttZJets_TuneCP5_13TeV_madgraphMLM_pythia8/RunIIAutumn18NanoAODv7-Nano02Apr2020_102X_upgrade2018_realistic_v21_ext1-v1/NANOAODSIM", "CMS", ".*root",  0.5297/0.692)


# Single top cross sections: https://twiki.cern.ch/twiki/bin/viewauth/CMS/SingleTopSigma
T_sch_lep = kreator.makeMCComponent("T_sch_lep", "/ST_s-channel_4f_leptonDecays_TuneCP5_13TeV-madgraph-pythia8/RunIIAutumn18NanoAODv7-Nano02Apr2020_102X_upgrade2018_realistic_v21_ext1-v1/NANOAODSIM", "CMS", ".*root", (7.20+4.16)*0.108*3, fracNegWeights=0.188)

T_tch = kreator.makeMCComponent("T_tch", "/ST_t-channel_top_4f_InclusiveDecays_TuneCP5_13TeV-powheg-madspin-pythia8/RunIIAutumn18NanoAODv7-Nano02Apr2020_102X_upgrade2018_realistic_v21-v1/NANOAODSIM",           "CMS", ".*root", 136.02) # inclusive sample
TBar_tch = kreator.makeMCComponent("TBar_tch", "/ST_t-channel_antitop_4f_InclusiveDecays_TuneCP5_13TeV-powheg-madspin-pythia8/RunIIAutumn18NanoAODv7-Nano02Apr2020_102X_upgrade2018_realistic_v21-v1/NANOAODSIM", "CMS", ".*root", 80.95) # inclusive sample

T_tWch_noFullyHad    = kreator.makeMCComponent("T_tWch_noFullyHad",    "/ST_tW_top_5f_NoFullyHadronicDecays_TuneCP5_13TeV-powheg-pythia8/RunIIAutumn18NanoAODv7-Nano02Apr2020_EXT_102X_upgrade2018_realistic_v21_ext1-v1/NANOAODSIM",     "CMS", ".*root",19.55)
TBar_tWch_noFullyHad = kreator.makeMCComponent("TBar_tWch_noFullyHad", "/ST_tW_antitop_5f_NoFullyHadronicDecays_TuneCP5_13TeV-powheg-pythia8/RunIIAutumn18NanoAODv7-Nano02Apr2020_EXT_102X_upgrade2018_realistic_v21_ext1-v1/NANOAODSIM", "CMS", ".*root",19.55)


TGJets_lep = kreator.makeMCComponent("TGJets_lep", "/TGJets_leptonDecays_TuneCP5_13TeV-madgraph-pythia8/RunIIAutumn18NanoAODv7-Nano02Apr2020_102X_upgrade2018_realistic_v21_ext1-v1/NANOAODSIM", "CMS", ".*root", 1.018, fracNegWeights=0.4)
TTGJets     = kreator.makeMCComponent("TTGJets", "/TTGJets_TuneCP5_13TeV-amcatnloFXFX-madspin-pythia8/RunIIAutumn18NanoAODv7-Nano02Apr2020_102X_upgrade2018_realistic_v21-v1/NANOAODSIM", "CMS", ".*root", 3.76, fracNegWeights=0.34)




Top = [ TTJets, 
        TTJets_DiLepton, 
        TTW_LO,
        TTZ_LO,
        T_sch_lep,
        T_tch, TBar_tch,
        T_tWch_noFullyHad, TBar_tWch_noFullyHad,
        TTGJets,
        TGJets_lep
]

# ====== SINGLE TOP ======

# ===  DI-BOSONS
WWDoubleTo2L           = kreator.makeMCComponent("WWDoubleTo2L", "/WWTo2L2Nu_DoubleScattering_13TeV-pythia8/RunIIAutumn18NanoAODv7-Nano02Apr2020_102X_upgrade2018_realistic_v21-v1/NANOAODSIM", "CMS", ".*root", 0.1729)
WWDoubleTo2L_herwig           = kreator.makeMCComponent("WWDoubleTo2L_herwig", "/WWTo2L2Nu_DoubleScattering_TuneCH3_13TeV-herwig7/RunIIAutumn18NanoAODv7-Nano02Apr2020_102X_upgrade2018_realistic_v21-v1/NANOAODSIM", "CMS", ".*root", 0.1729)
WWDouble_cp5 = kreator.makeMCComponent("WWDouble_cp5", "/WW_DoubleScattering_13TeV-pythia8_TuneCP5/RunIIAutumn18NanoAODv7-Nano02Apr2020_102X_upgrade2018_realistic_v21_ext1-v1/NANOAODSIM", "CMS", ".*root", 0.1729)

WZTo3LNu               = kreator.makeMCComponent("WZTo3LNu", "/WZTo3LNu_TuneCP5_13TeV-powheg-pythia8/RunIIAutumn18NanoAODv7-Nano02Apr2020_102X_upgrade2018_realistic_v21_ext1-v1/NANOAODSIM", "CMS", ".*root", 4.42965)
WZTo3LNu_fxfx          = kreator.makeMCComponent("WZTo3LNu_fxfx", "/WZTo3LNu_TuneCP5_13TeV-amcatnloFXFX-pythia8/RunIIAutumn18NanoAODv7-Nano02Apr2020_102X_upgrade2018_realistic_v21_ext1-v1/NANOAODSIM", "CMS", ".*root", 4.666, fracNegWeights=0.19)
WZTo3LNu_mllmin01      = kreator.makeMCComponent("WZTo3LNu_mllmin01", "/WZTo3LNu_mllmin01_NNPDF31_TuneCP5_13TeV_powheg_pythia8/RunIIAutumn18NanoAODv7-Nano02Apr2020_102X_upgrade2018_realistic_v21-v1/NANOAODSIM", "CMS", ".*root", 58.59*0.601644)

WWTo2L2Nu              = kreator.makeMCComponent("WWTo2L2Nu", "/WWTo2L2Nu_NNPDF31_TuneCP5_13TeV-powheg-pythia8/RunIIAutumn18NanoAODv7-Nano02Apr2020_102X_upgrade2018_realistic_v21-v1/NANOAODSIM","CMS", ".*root", 10.481)
ZZTo4L                 = kreator.makeMCComponent("ZZTo4L", "/ZZTo4L_13TeV_powheg_pythia8_TuneCP5/RunIIAutumn18NanoAODv7-Nano02Apr2020_102X_upgrade2018_realistic_v21-v1/NANOAODSIM", "CMS", ".*root", 1.256)
ZZTo4L_ext             = kreator.makeMCComponent("ZZTo4L_ext", "/ZZTo4L_TuneCP5_13TeV_powheg_pythia8/RunIIAutumn18NanoAODv7-Nano02Apr2020_102X_upgrade2018_realistic_v21_ext2-v1/NANOAODSIM", "CMS", ".*root", 1.256)
WpWpJJ                 = kreator.makeMCComponent("WpWpJJ", "/WpWpJJ_EWK-QCD_TuneCP5_13TeV-madgraph-pythia8/RunIIAutumn18NanoAODv7-Nano02Apr2020_102X_upgrade2018_realistic_v21-v1/NANOAODSIM", "CMS", ".*root", 0.03711)
WGToLNuG               = kreator.makeMCComponent("WGToLNuG", "/WGToLNuG_TuneCP5_13TeV-madgraphMLM-pythia8/RunIIAutumn18NanoAODv7-Nano02Apr2020_102X_upgrade2018_realistic_v21-v1/NANOAODSIM", "CMS", ".*root", 405.271)
WGToLNuG_01J_amcatnlo  = kreator.makeMCComponent("WGToLNuG_01J_amcatnlo", "/WGToLNuG_01J_5f_TuneCP5_13TeV-amcatnloFXFX-pythia8/RunIIAutumn18NanoAODv7-Nano02Apr2020_102X_upgrade2018_realistic_v21_ext1-v1/NANOAODSIM", "CMS", ".*root", 178.4,fracNegWeights=0.203)
ZGToLLG_01J_amcatnlo_ext                 = kreator.makeMCComponent("ZGToLLG_01J_amcatnlo_ext", "/ZGToLLG_01J_5f_TuneCP5_13TeV-amcatnloFXFX-pythia8/RunIIAutumn18NanoAODv7-Nano02Apr2020_102X_upgrade2018_realistic_v21_ext1-v1/NANOAODSIM", "CMS", ".*root", 58.83,fracNegWeights=0.202)
ZGToLLG_01J_amcatnlo                 = kreator.makeMCComponent("ZGToLLG_01J_amcatnlo", "/ZGToLLG_01J_5f_TuneCP5_13TeV-amcatnloFXFX-pythia8/RunIIAutumn18NanoAODv7-Nano02Apr2020_102X_upgrade2018_realistic_v21_ext2-v1/NANOAODSIM", "CMS", ".*root", 58.83,fracNegWeights=0.202)
ZGToLLG_01J_lowmll_amcatnlo                 = kreator.makeMCComponent("ZGToLLG_01J_lowmll_amcatnlo", "/ZGToLLG_01J_5f_lowMLL_TuneCP5_13TeV-amcatnloFXFX-pythia8/RunIIAutumn18NanoAODv7-Nano02Apr2020_102X_upgrade2018_realistic_v21-v1/NANOAODSIM", "CMS", ".*root", 97.21,fracNegWeights=0.18)



DiBosons = [
WWDoubleTo2L,
WWDoubleTo2L_herwig,
WWDouble_cp5,
WZTo3LNu,
WZTo3LNu_fxfx,
WZTo3LNu_mllmin01,
WWTo2L2Nu,              
ZZTo4L, ZZTo4L_ext,                
WpWpJJ, WGToLNuG, WGToLNuG_01J_amcatnlo,
ZGToLLG_01J_amcatnlo_ext,
ZGToLLG_01J_amcatnlo,
ZGToLLG_01J_lowmll_amcatnlo
]
# cross section from https://twiki.cern.ch/twiki/bin/view/CMS/SummaryTable1G25ns#Diboson

# ===  TRI-BOSONS

# xsec from GenXSecAnalyzer
WWW    = kreator.makeMCComponent("WWW",    "/WWW_4F_TuneCP5_13TeV-amcatnlo-pythia8/RunIIAutumn18NanoAODv7-Nano02Apr2020_102X_upgrade2018_realistic_v21_ext1-v1/NANOAODSIM", "CMS", ".*root", 0.2086, fracNegWeights=0.063)
WWW_ll = kreator.makeMCComponent("WWW_ll", "/WWW_4F_DiLeptonFilter_TuneCP5_13TeV-amcatnlo-pythia8/RunIIAutumn18NanoAODv7-Nano02Apr2020_102X_upgrade2018_realistic_v21-v1/NANOAODSIM", "CMS", ".*root", 0.007201, fracNegWeights=0.063) # xs from genXSecAna
WWZ    = kreator.makeMCComponent("WWZ",    "/WWZ_TuneCP5_13TeV-amcatnlo-pythia8/RunIIAutumn18NanoAODv7-Nano02Apr2020_102X_upgrade2018_realistic_v21_ext1-v1/NANOAODSIM", "CMS", ".*root",  0.1651, fracNegWeights=0.06 ) 
WWG    = kreator.makeMCComponent("WWG",    "/WWG_TuneCP5_13TeV-amcatnlo-pythia8/RunIIAutumn18NanoAODv7-Nano02Apr2020_102X_upgrade2018_realistic_v21_ext1-v1/NANOAODSIM", "CMS", ".*root", 0.2147, fracNegWeights=0.088)
WZZ    = kreator.makeMCComponent("WZZ",    "/WZZ_TuneCP5_13TeV-amcatnlo-pythia8/RunIIAutumn18NanoAODv7-Nano02Apr2020_102X_upgrade2018_realistic_v21_ext1-v1/NANOAODSIM", "CMS", ".*root", 0.05565, fracNegWeights=0.060)
ZZZ    = kreator.makeMCComponent("ZZZ",    "/ZZZ_TuneCP5_13TeV-amcatnlo-pythia8/RunIIAutumn18NanoAODv7-Nano02Apr2020_102X_upgrade2018_realistic_v21_ext1-v1/NANOAODSIM", "CMS", ".*root", 0.01398, fracNegWeights=0.060)



TriBosons = [
    WWW,
    WWW_ll,
    WWZ,
    WWG,
    WZZ,
    ZZZ,
]

# other Higgs processes

### gg fusion

GGHZZ4L      = kreator.makeMCComponent("GGHZZ4L", "/GluGluHToZZTo4L_M125_13TeV_powheg2_JHUGenV7011_pythia8/RunIIAutumn18NanoAODv7-Nano02Apr2020_102X_upgrade2018_realistic_v21-v1/NANOAODSIM", "CMS", ".*root", 0.01212) 
GGZZ4L       = kreator.makeMCComponent("GGZZ4L", "/GluGluToContinToZZTo4L_13TeV_TuneCP5_madgraphMLM_pythia8/RunIIAutumn18NanoAODv7-Nano02Apr2020_102X_upgrade2018_realistic_v21-v1/NANOAODSIM", "CMS", ".*root", 0.014352)
GGZZ4t_cp5   = kreator.makeMCComponent("GGZZ4t_cp5","/GluGluToContinToZZTo4tau_13TeV_TuneCP5_MCFM701_pythia8/RunIIAutumn18NanoAODv7-Nano02Apr2020_102X_upgrade2018_realistic_v21-v1/NANOAODSIM", "CMS", ".*root",0.001586)
GGZZ4m_cp5   = kreator.makeMCComponent("GGZZ4m_cp5","/GluGluToContinToZZTo4mu_13TeV_TuneCP5_MCFM701_pythia8/RunIIAutumn18NanoAODv7-Nano02Apr2020_102X_upgrade2018_realistic_v21-v1/NANOAODSIM", "CMS", ".*root",0.001586)
GGZZ4e_cp5   = kreator.makeMCComponent("GGZZ4e_cp5","/GluGluToContinToZZTo4e_13TeV_TuneCP5_MCFM701_pythia8/RunIIAutumn18NanoAODv7-Nano02Apr2020_102X_upgrade2018_realistic_v21-v1/NANOAODSIM","CMS", ".*root",0.001586)
GGZZ2m2t_cp5     = kreator.makeMCComponent("GGZZ2m2t_cp5","/GluGluToContinToZZTo2mu2tau_13TeV_TuneCP5_MCFM701_pythia8/RunIIAutumn18NanoAODv7-Nano02Apr2020_102X_upgrade2018_realistic_v21-v1/NANOAODSIM", "CMS", ".*root",0.003194)
GGZZ2e2t_cp5 = kreator.makeMCComponent("GGZZ2e2t_cp5","/GluGluToContinToZZTo2e2tau_13TeV_TuneCP5_MCFM701_pythia8/RunIIAutumn18NanoAODv7-Nano02Apr2020_102X_upgrade2018_realistic_v21-v1/NANOAODSIM", "CMS", ".*root",0.003194)
GGZZ2e2m_cp5 = kreator.makeMCComponent("GGZZ2e2m_cp5","/GluGluToContinToZZTo2e2mu_13TeV_TuneCP5_MCFM701_pythia8/RunIIAutumn18NanoAODv7-Nano02Apr2020_102X_upgrade2018_realistic_v21-v1/NANOAODSIM", "CMS", ".*root",0.003194)

GGZZ4t = kreator.makeMCComponent("GGZZ4t","/GluGluToContinToZZTo4tau_13TeV_MCFM701_pythia8/RunIIAutumn18NanoAODv7-Nano02Apr2020_102X_upgrade2018_realistic_v21-v1/NANOAODSIM", "CMS", ".*root",0.001586)
GGZZ4m = kreator.makeMCComponent("GGZZ4m","/GluGluToContinToZZTo4mu_13TeV_MCFM701_pythia8/RunIIAutumn18NanoAODv7-Nano02Apr2020_102X_upgrade2018_realistic_v21-v1/NANOAODSIM", "CMS", ".*root",0.001586)
GGZZ4e = kreator.makeMCComponent("GGZZ4e","/GluGluToContinToZZTo4e_13TeV_MCFM701_pythia8/RunIIAutumn18NanoAODv7-Nano02Apr2020_102X_upgrade2018_realistic_v21-v1/NANOAODSIM", "CMS", ".*root",0.001586)
GGZZ2m2t = kreator.makeMCComponent("GGZZ2m2t","/GluGluToContinToZZTo2mu2tau_13TeV_MCFM701_pythia8/RunIIAutumn18NanoAODv7-Nano02Apr2020_102X_upgrade2018_realistic_v21-v1/NANOAODSIM", "CMS", ".*root",0.003194)
GGZZ2e2t = kreator.makeMCComponent("GGZZ2e2t","/GluGluToContinToZZTo2e2tau_13TeV_MCFM701_pythia8/RunIIAutumn18NanoAODv7-Nano02Apr2020_102X_upgrade2018_realistic_v21-v1/NANOAODSIM", "CMS", ".*root",0.003194)
GGZZ2e2m = kreator.makeMCComponent("GGZZ2e2m","/GluGluToContinToZZTo2e2mu_13TeV_MCFM701_pythia8/RunIIAutumn18NanoAODv7-Nano02Apr2020_102X_upgrade2018_realistic_v21-v1/NANOAODSIM", "CMS", ".*root",0.003194)




GGFusion= [
    GGHZZ4L,
    GGZZ4L,
    GGZZ4t,
    GGZZ4t_cp5,
    GGZZ4m,
    GGZZ4m_cp5,
    GGZZ4e,
    GGZZ4e_cp5,
    GGZZ2m2t,
    GGZZ2m2t_cp5,
    GGZZ2e2t,
    GGZZ2e2t_cp5,
    GGZZ2e2m,
    GGZZ2e2m_cp5
]



GGFusion= [
    GGZZ4L,
    GGHZZ4L,
    GGZZ4t,
    GGZZ4m,
    GGZZ4e,
    GGZZ2m2t,
    GGZZ2e2t,
    GGZZ2e2m]


# ----------------------------- summary ----------------------------------------


#mcSamples =  Ws + DYs + VJetsQQHT + TTs + Ts + TTXs + TTXXs + DiBosons + TriBosons + Higgs
mcSamples =  EWK + Top + DiBosons + TriBosons +GGFusion

samples = mcSamples

# ---------------------------------------------------------------------

if __name__ == "__main__":
    from CMGTools.RootTools.samples.tools import runMain
    runMain(samples, localobjs=locals())
