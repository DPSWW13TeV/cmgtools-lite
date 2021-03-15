from CMGTools.RootTools.samples.ComponentCreator import ComponentCreator
kreator = ComponentCreator()

#sigPy8Private = kreator.makeMCComponent("WWDoubleTo2L", "/WWTo2L2Nu_DoubleScattering_13TeV-pythia8/RunIIFall17NanoAODv7-PU2017_12Apr2018_Nano02Apr2020_102X_mc2017_realistic_v8-v1/NANOAODSIM", "CMS", ".*root", 0.1729)


#sigHWPrivate           = kreator.makeMCComponent("WWDoubleTo2L_herwig", "/WWTo2L2Nu_DoubleScattering_TuneCH3_13TeV-herwig7/RunIIFall17NanoAODv7-PU2017_12Apr2018_Nano02Apr2020_102X_mc2017_realistic_v8-v1/NANOAODSIM", "CMS", ".*root", 0.1729)

#privateProd =[sigPy8Private,sigHWPrivate]

TTJets = kreator.makeMCComponent("TTJets", "/TTJets_TuneCP5_13TeV-amcatnloFXFX-pythia8/RunIIFall17NanoAODv7-PU2017_12Apr2018_Nano02Apr2020_new_pmx_102X_mc2017_realistic_v8-v1/NANOAODSIM", "CMS", ".*root", 831.76, fracNegWeights=0.319)
TTJets_DiLepton = kreator.makeMCComponent("TTJets_DiLepton", "/TTJets_DiLept_TuneCP5_13TeV-madgraphMLM-pythia8/RunIIFall17NanoAODv7-PU2017_12Apr2018_Nano02Apr2020_102X_mc2017_realistic_v8-v1/NANOAODSIM", "CMS", ".*root", 831.76*((3*0.108)**2) )

T_sch_lep = kreator.makeMCComponent("T_sch_lep", "/ST_s-channel_4f_leptonDecays_mtop1715_TuneCP5_PSweights_13TeV-amcatnlo-pythia8/RunIIFall17NanoAODv7-PU2017_12Apr2018_Nano02Apr2020_102X_mc2017_realistic_v8-v1/NANOAODSIM", "CMS", ".*root", (7.20+4.16)*0.108*3, fracNegWeights=0.188)
T_tch = kreator.makeMCComponent("T_tch", "/ST_t-channel_top_4f_inclusiveDecays_TuneCP5_13TeV-powhegV2-madspin-pythia8/RunIIFall17NanoAODv7-PU2017_12Apr2018_Nano02Apr2020_new_pmx_102X_mc2017_realistic_v8-v1/NANOAODSIM", "CMS", ".*root", 136.02) # inclusive sample
TBar_tch = kreator.makeMCComponent("TBar_tch", "/ST_t-channel_antitop_4f_inclusiveDecays_TuneCP5_13TeV-powhegV2-madspin-pythia8/RunIIFall17NanoAODv7-PU2017_12Apr2018_Nano02Apr2020_102X_mc2017_realistic_v8-v1/NANOAODSIM", "CMS", ".*root", 80.95) # inclusive sample
T_tWch = kreator.makeMCComponent("T_tWch", "/ST_tW_top_5f_inclusiveDecays_TuneCP5_13TeV-powheg-pythia8/RunIIFall17NanoAODv7-PU2017_12Apr2018_Nano02Apr2020_102X_mc2017_realistic_v8-v1/NANOAODSIM", "CMS", ".*root",35.6)
TBar_tWch = kreator.makeMCComponent("TBar_tWch", "/ST_tW_antitop_5f_inclusiveDecays_TuneCP5_13TeV-powheg-pythia8/RunIIFall17NanoAODv7-PU2017_12Apr2018_Nano02Apr2020_102X_mc2017_realistic_v8-v1/NANOAODSIM", "CMS", ".*root",35.6)

TTW_LO = kreator.makeMCComponent("TTW_LO", "/ttWJets_TuneCP5_13TeV_madgraphMLM_pythia8/RunIIFall17NanoAODv7-PU2017_12Apr2018_Nano02Apr2020_102X_mc2017_realistic_v8-v1/NANOAODSIM", "CMS", ".*root",  0.6105 )
TTZ_LO = kreator.makeMCComponent("TTZ_LO", "/ttZJets_TuneCP5_13TeV_madgraphMLM_pythia8/RunIIFall17NanoAODv7-PU2017_12Apr2018_Nano02Apr2020_102X_mc2017_realistic_v8-v1/NANOAODSIM", "CMS", ".*root",  0.5297/0.692)

TGJets_lep = kreator.makeMCComponent("TGJets_lep", "/TGJets_TuneCP5_13TeV_amcatnlo_madspin_pythia8/RunIIFall17NanoAODv7-PU2017_12Apr2018_Nano02Apr2020_102X_mc2017_realistic_v8-v1/NANOAODSIM", "CMS", ".*root", 1.018, fracNegWeights=0.4)

TTGJets     = kreator.makeMCComponent("TTGJets",    "/TTGJets_TuneCP5_13TeV-amcatnloFXFX-madspin-pythia8/RunIIFall17NanoAODv7-PU2017_12Apr2018_Nano02Apr2020_102X_mc2017_realistic_v8-v1/NANOAODSIM", "CMS", ".*root", 3.76, fracNegWeights=0.34)
TTGJets_ext     = kreator.makeMCComponent("TTGJets_ext",    "/TTGJets_TuneCP5_13TeV-amcatnloFXFX-madspin-pythia8/RunIIFall17NanoAODv7-PU2017_12Apr2018_Nano02Apr2020_102X_mc2017_realistic_v8_ext1-v1/NANOAODSIM", "CMS", ".*root", 3.76, fracNegWeights=0.34)




Top = [
TTJets,
TTJets_DiLepton,
T_sch_lep,
T_tch,
TBar_tch,
T_tWch,
TBar_tWch,
TTW_LO,
TTZ_LO,
TGJets_lep,
TTGJets,
TTGJets_ext
]


### V+jets inclusive (from https://twiki.cern.ch/twiki/bin/viewauth/CMS/StandardModelCrossSectionsat13TeV)

WJetsToLNu_LO = kreator.makeMCComponent("WJetsToLNu_LO","/WJetsToLNu_TuneCP5_13TeV-madgraphMLM-pythia8/RunIIFall17NanoAODv7-PU2017_12Apr2018_Nano02Apr2020_102X_mc2017_realistic_v8-v1/NANOAODSIM", "CMS", ".*root", 3* 20508.9)
WJetsToLNu_LO_ext =  kreator.makeMCComponent("WJetsToLNu_LO_ext", "/WJetsToLNu_TuneCP5_13TeV-madgraphMLM-pythia8/RunIIFall17NanoAODv7-PU2017_12Apr2018_Nano02Apr2020_102X_mc2017_realistic_v8_ext1-v1/NANOAODSIM", "CMS", ".*root", 61526.7)



DYJetsToLL_M10to50_LO = kreator.makeMCComponent("DYJetsToLL_M10to50", "/DYJetsToLL_M-10to50_TuneCP5_13TeV-madgraphMLM-pythia8/RunIIFall17NanoAODv7-PU2017_12Apr2018_Nano02Apr2020_102X_mc2017_realistic_v8_ext1-v1/NANOAODSIM", "CMS", ".*root", 15810)


DYJetsToLL_M50_LO =  kreator.makeMCComponent("DYJetsToLL_M50_LO", "/DYJetsToLL_M-50_TuneCP5_13TeV-madgraphMLM-pythia8/RunIIFall17NanoAODv7-PU2017RECOSIMstep_12Apr2018_Nano02Apr2020_102X_mc2017_realistic_v8-v1/NANOAODSIM", "CMS", ".*root", 1921.8*3)

DYJetsToLL_M50_LO_ext =  kreator.makeMCComponent("DYJetsToLL_M50_LO", "/DYJetsToLL_M-50_TuneCP5_13TeV-madgraphMLM-pythia8/RunIIFall17NanoAODv7-PU2017RECOSIMstep_12Apr2018_Nano02Apr2020_102X_mc2017_realistic_v8_ext1-v1/NANOAODSIM", "CMS", ".*root", 1921.8*3)

DYJetsToLL_M50 =  kreator.makeMCComponent("DYJetsToLL_M50", "/DYJetsToLL_M-50_TuneCP5_13TeV-amcatnloFXFX-pythia8/RunIIFall17NanoAODv7-PU2017_12Apr2018_Nano02Apr2020_102X_mc2017_realistic_v8-v1/NANOAODSIM", "CMS", ".*root", 1921.8*3, fracNegWeights=0.16)


W0JetsToLNu =  kreator.makeMCComponent("W0JetsToLNu", "/WJetsToLNu_0J_TuneCP5_13TeV-amcatnloFXFX-pythia8/RunIIFall17NanoAODv7-PU2017_12Apr2018_Nano02Apr2020_102X_mc2017_realistic_v8-v1/NANOAODSIM", "CMS", ".*root", 50131.98)

W1JetsToLNu =  kreator.makeMCComponent("W1JetsToLNu", "/WJetsToLNu_1J_TuneCP5_13TeV-amcatnloFXFX-pythia8/RunIIFall17NanoAODv7-PU2017_12Apr2018_Nano02Apr2020_102X_mc2017_realistic_v8-v1/NANOAODSIM", "CMS", ".*root", 8426.09)

W1JetsToLNu_ext =  kreator.makeMCComponent("W1JetsToLNu_ext", "/WJetsToLNu_1J_TuneCP5_13TeV-amcatnloFXFX-pythia8/RunIIFall17NanoAODv7-PU2017_12Apr2018_Nano02Apr2020_102X_mc2017_realistic_v8_ext1-v1/NANOAODSIM", "CMS", ".*root", 8426.09)
W2JetsToLNu =  kreator.makeMCComponent("W2JetsToLNu", "/WJetsToLNu_2J_TuneCP5_13TeV-amcatnloFXFX-pythia8/RunIIFall17NanoAODv7-PU2017_12Apr2018_Nano02Apr2020_102X_mc2017_realistic_v8-v1/NANOAODSIM", "CMS", ".*root", 3172.96)
W2JetsToLNu_ext =  kreator.makeMCComponent("W2JetsToLNu_ext", "/WJetsToLNu_2J_TuneCP5_13TeV-amcatnloFXFX-pythia8/RunIIFall17NanoAODv7-PU2017_12Apr2018_Nano02Apr2020_102X_mc2017_realistic_v8_ext1-v1/NANOAODSIM", "CMS", ".*root", 3172.96)




EWK = [

WJetsToLNu_LO,
WJetsToLNu_LO_ext,
W0JetsToLNu,
W1JetsToLNu,
W1JetsToLNu_ext,
W2JetsToLNu,
W2JetsToLNu_ext,
DYJetsToLL_M10to50_LO,
DYJetsToLL_M50_LO,
DYJetsToLL_M50_LO_ext,
DYJetsToLL_M50,
]






### DiBosons
WWDoubleTo2L           = kreator.makeMCComponent("WWDoubleTo2L", "/WWTo2L2Nu_DoubleScattering_13TeV-pythia8/RunIIFall17NanoAODv7-PU2017_12Apr2018_Nano02Apr2020_102X_mc2017_realistic_v8-v1/NANOAODSIM", "CMS", ".*root", 0.1729)
WWDoubleTo2L_herwig           = kreator.makeMCComponent("WWDoubleTo2L_herwig", "/WWTo2L2Nu_DoubleScattering_TuneCH3_13TeV-herwig7/RunIIFall17NanoAODv7-PU2017_12Apr2018_Nano02Apr2020_102X_mc2017_realistic_v8-v1/NANOAODSIM", "CMS", ".*root", 0.1729)
WWDouble_cp5           = kreator.makeMCComponent("WWDouble_cp5", "/WW_DoubleScattering_13TeV-pythia8_TuneCP5/RunIIFall17NanoAODv7-PU2017_12Apr2018_Nano02Apr2020_102X_mc2017_realistic_v8-v1/NANOAODSIM", "CMS", ".*root", 0.1729)



WZTo3LNu               = kreator.makeMCComponent("WZTo3LNu", "/WZTo3LNu_13TeV-powheg-pythia8/RunIIFall17NanoAODv7-PU2017_12Apr2018_Nano02Apr2020_102X_mc2017_realistic_v8-v1/NANOAODSIM", "CMS", ".*root", 4.42965)


WZTo3LNu_fxfx          = kreator.makeMCComponent("WZTo3LNu_fxfx", "/WZTo3LNu_TuneCP5_13TeV-amcatnloFXFX-pythia8/RunIIFall17NanoAODv7-PU2017_12Apr2018_Nano02Apr2020_new_pmx_102X_mc2017_realistic_v8-v1/NANOAODSIM", "CMS", ".*root", 4.666, fracNegWeights=0.19)


WZTo3LNu_mllmin01      = kreator.makeMCComponent("WZTo3LNu_mllmin01", "/WZTo3LNu_mllmin01_NNPDF31_TuneCP5_13TeV_powheg_pythia8/RunIIFall17NanoAODv7-PU2017_12Apr2018_Nano02Apr2020_102X_mc2017_realistic_v8-v1/NANOAODSIM", "CMS", ".*root", 58.59*0.601644)


WWTo2L2Nu              = kreator.makeMCComponent("WWTo2L2Nu", "/WWTo2L2Nu_NNPDF31_TuneCP5_13TeV-powheg-pythia8/RunIIFall17NanoAODv7-PU2017_12Apr2018_Nano02Apr2020_102X_mc2017_realistic_v8-v1/NANOAODSIM", "CMS", ".*root", 10.481)
ZZTo4L                 = kreator.makeMCComponent("ZZTo4L", "/ZZTo4L_13TeV_powheg_pythia8/RunIIFall17NanoAODv7-PU2017_12Apr2018_Nano02Apr2020_102X_mc2017_realistic_v8-v1/NANOAODSIM", "CMS", ".*root", 1.256)
WpWpJJ                 = kreator.makeMCComponent("WpWpJJ", "/WpWpJJ_EWK-QCD_TuneCP5_13TeV-madgraph-pythia8/RunIIFall17NanoAODv7-PU2017_12Apr2018_Nano02Apr2020_102X_mc2017_realistic_v8-v1/NANOAODSIM", "CMS", ".*root", 0.03711)

ZGToLLG_01J_amcatnlo                = kreator.makeMCComponent("ZGToLLG_01J_amcatnlo", "/ZGToLLG_01J_5f_TuneCP5_13TeV-amcatnloFXFX-pythia8/RunIIFall17NanoAODv7-PU2017_12Apr2018_Nano02Apr2020_102X_mc2017_realistic_v8-v1/NANOAODSIM", "CMS", ".*root", 58.83, fracNegWeights=0.16)

ZGToLLG_01J_lowmll_amcatnlo                = kreator.makeMCComponent("ZGToLLG_01J_lowmll_amcatnlo", "/ZGToLLG_01J_5f_lowMLL_TuneCP5_13TeV-amcatnloFXFX-pythia8/RunIIFall17NanoAODv7-PU2017_12Apr2018_Nano02Apr2020_102X_mc2017_realistic_v8-v1/NANOAODSIM", "CMS", ".*root", 106.9, fracNegWeights=0.165)

WGToLNuG               = kreator.makeMCComponent("WGToLNuG", "/WGToLNuG_TuneCP5_13TeV-madgraphMLM-pythia8/RunIIFall17NanoAODv7-PU2017_12Apr2018_Nano02Apr2020_102X_mc2017_realistic_v8-v1/NANOAODSIM", "CMS", ".*root", 585.8)
WGToLNuG_01J_amcatnlo    = kreator.makeMCComponent("WGToLNuG_01J_amcatnlo", "/WGToLNuG_01J_5f_TuneCP5_13TeV-amcatnloFXFX-pythia8/RunIIFall17NanoAODv7-PU2017_12Apr2018_Nano02Apr2020_102X_mc2017_realistic_v8-v1/NANOAODSIM", "CMS", ".*root", 178.4, fracNegWeights=0.203) 






DiBosons = [
WWDoubleTo2L,
WWDoubleTo2L_herwig,
WZTo3LNu,
WZTo3LNu_fxfx,
WZTo3LNu_mllmin01,
WWTo2L2Nu,              
ZZTo4L,                 
WpWpJJ,
ZGToLLG_01J_amcatnlo,
ZGToLLG_01J_lowmll_amcatnlo,
WGToLNuG,
WGToLNuG_01J_amcatnlo
]


### TriBosons
# cross section from https://twiki.cern.ch/twiki/bin/view/CMS/SummaryTable1G25ns#Triboson

WWW = kreator.makeMCComponent("WWW", "/WWW_4F_TuneCP5_13TeV-amcatnlo-pythia8/RunIIFall17NanoAODv7-PU2017_12Apr2018_Nano02Apr2020_102X_mc2017_realistic_v8-v1/NANOAODSIM", "CMS", ".*root", 0.2086, fracNegWeights=0.053)
WWW_ll = kreator.makeMCComponent("WWW_ll", "/WWW_4F_DiLeptonFilter_TuneCP5_13TeV-amcatnlo-pythia8/RunIIFall17NanoAODv7-PU2017_12Apr2018_Nano02Apr2020_102X_mc2017_realistic_v8-v1/NANOAODSIM", "CMS", ".*root", 0.007201, fracNegWeights=0.063) #
WWZ = kreator.makeMCComponent("WWZ", "/WWZ_4F_TuneCP5_13TeV-amcatnlo-pythia8/RunIIFall17NanoAODv7-PU2017_12Apr2018_Nano02Apr2020_102X_mc2017_realistic_v8-v1/NANOAODSIM", "CMS", ".*root",  0.1651 , fracNegWeights=0.06)

WZZ = kreator.makeMCComponent("WZZ", "/WZZ_TuneCP5_13TeV-amcatnlo-pythia8/RunIIFall17NanoAODv7-PU2017_12Apr2018_Nano02Apr2020_102X_mc2017_realistic_v8-v1/NANOAODSIM", "CMS", ".*root",  0.05565 , fracNegWeights=0.060)
ZZZ = kreator.makeMCComponent("ZZZ", "/ZZZ_TuneCP5_13TeV-amcatnlo-pythia8/RunIIFall17NanoAODv7-PU2017_12Apr2018_Nano02Apr2020_102X_mc2017_realistic_v8-v1/NANOAODSIM", "CMS", ".*root",  0.01398 , fracNegWeights=0.060)

WWW_ll = kreator.makeMCComponent("WWW_ll", "/WWW_4F_DiLeptonFilter_TuneCP5_13TeV-amcatnlo-pythia8/RunIIFall17NanoAODv7-PU2017_12Apr2018_Nano02Apr2020_102X_mc2017_realistic_v8-v1/NANOAODSIM", "CMS", ".*root", 0.007201, fracNegWeights=0.063)  # xs from genXSecAna

WWG = kreator.makeMCComponent("WWG","/WWG_TuneCP5_13TeV-amcatnlo-pythia8/RunIIFall17NanoAODv7-PU2017_12Apr2018_Nano02Apr2020_102X_mc2017_realistic_v8-v1/NANOAODSIM", "CMS", ".*root", 0.2147, fracNegWeights=0.088) 

TriBosons = [
WWW,
WWW_ll,
WZZ,
WWZ,
ZZZ,
WWG
]


# QCD enriched (cross sections form genXSecAna)

QCD_Pt15to20_MuEnriched    = kreator.makeMCComponent("QCD_Pt15to20_MuEnriched"  , "/QCD_Pt-15to20_MuEnrichedPt5_TuneCP5_13TeV_pythia8/RunIIFall17NanoAODv7-PU2017_12Apr2018_Nano02Apr2020_102X_mc2017_realistic_v8-v1/NANOAODSIM", "CMS" , ".*root", 2.785e+06)
QCD_Pt20to30_MuEnriched    = kreator.makeMCComponent("QCD_Pt20to30_MuEnriched"    , "/QCD_Pt-20to30_MuEnrichedPt5_TuneCP5_13TeV_pythia8/RunIIFall17NanoAODv7-PU2017_12Apr2018_Nano02Apr2020_102X_mc2017_realistic_v8-v1/NANOAODSIM", "CMS" , ".*root", 2.49e+06)
QCD_Pt30to50_MuEnriched    = kreator.makeMCComponent("QCD_Pt30to50_MuEnriched", "/QCD_Pt-30to50_MuEnrichedPt5_TuneCP5_13TeV_pythia8/RunIIFall17NanoAODv7-PU2017_12Apr2018_Nano02Apr2020_102X_mc2017_realistic_v8-v1/NANOAODSIM", "CMS", ".*root", 1.364e+06)
QCD_Pt50to80_MuEnriched    = kreator.makeMCComponent("QCD_Pt50to80_MuEnriched"    , "/QCD_Pt-50to80_MuEnrichedPt5_TuneCP5_13TeV_pythia8/RunIIFall17NanoAODv7-PU2017_12Apr2018_Nano02Apr2020_102X_mc2017_realistic_v8-v1/NANOAODSIM" , "CMS" , ".*root", 377400)
QCD_Pt80to120_MuEnriched   = kreator.makeMCComponent("QCD_Pt80to120_MuEnriched"   , "/QCD_Pt-80to120_MuEnrichedPt5_TuneCP5_13TeV_pythia8/RunIIFall17NanoAODv7-PU2017_12Apr2018_Nano02Apr2020_102X_mc2017_realistic_v8-v1/NANOAODSIM", "CMS" , ".*root", 88350)
QCD_Pt120to170_MuEnriched  = kreator.makeMCComponent("QCD_Pt120to170_MuEnriched"  , "/QCD_Pt-120to170_MuEnrichedPt5_TuneCP5_13TeV_pythia8/RunIIFall17NanoAODv7-PU2017_12Apr2018_Nano02Apr2020_102X_mc2017_realistic_v8-v1/NANOAODSIM", "CMS" , ".*root", 21250)
QCD_Pt170to300_MuEnriched  = kreator.makeMCComponent("QCD_Pt170to300_MuEnriched", "/QCD_Pt-170to300_MuEnrichedPt5_TuneCP5_13TeV_pythia8/RunIIFall17NanoAODv7-PU2017_12Apr2018_Nano02Apr2020_102X_mc2017_realistic_v8-v1/NANOAODSIM", "CMS", ".*root", 6969)
QCD_Pt300to470_MuEnriched  = kreator.makeMCComponent("QCD_Pt300to470_MuEnriched"  , "/QCD_Pt-300to470_MuEnrichedPt5_TuneCP5_13TeV_pythia8/RunIIFall17NanoAODv7-PU2017_12Apr2018_Nano02Apr2020_102X_mc2017_realistic_v8-v1/NANOAODSIM", "CMS" , ".*root", 619.5)
QCD_Pt470to600_MuEnriched  = kreator.makeMCComponent("QCD_Pt470to600_MuEnriched"  , "/QCD_Pt-470to600_MuEnrichedPt5_TuneCP5_13TeV_pythia8/RunIIFall17NanoAODv7-PU2017_12Apr2018_Nano02Apr2020_102X_mc2017_realistic_v8-v1/NANOAODSIM", "CMS" , ".*root", 58.9)
QCD_Pt600to800_MuEnriched  = kreator.makeMCComponent("QCD_Pt600to800_MuEnriched", "/QCD_Pt-600to800_MuEnrichedPt5_TuneCP5_13TeV_pythia8/RunIIFall17NanoAODv7-PU2017_12Apr2018_Nano02Apr2020_102X_mc2017_realistic_v8-v1/NANOAODSIM", "CMS", ".*root", 18.36)
QCD_Pt800to1000_MuEnriched = kreator.makeMCComponent("QCD_Pt800to1000_MuEnriched" , "/QCD_Pt-800to1000_MuEnrichedPt5_TuneCP5_13TeV_pythia8/RunIIFall17NanoAODv7-PU2017_12Apr2018_Nano02Apr2020_102X_mc2017_realistic_v8-v1/NANOAODSIM", "CMS" , ".*root", 3.253)
QCD_Pt1000toInf_MuEnriched = kreator.makeMCComponent("QCD_Pt1000toInf_MuEnriched" , "/QCD_Pt-1000toInf_MuEnrichedPt5_TuneCP5_13TeV_pythia8/RunIIFall17NanoAODv7-PU2017_12Apr2018_Nano02Apr2020_102X_mc2017_realistic_v8-v1/NANOAODSIM", "CMS" , ".*root", 1.075)

QCD_MuEnriched = [
    QCD_Pt15to20_MuEnriched,
    QCD_Pt20to30_MuEnriched,
    QCD_Pt30to50_MuEnriched,
    QCD_Pt50to80_MuEnriched,
    QCD_Pt80to120_MuEnriched,
    QCD_Pt120to170_MuEnriched,
    QCD_Pt170to300_MuEnriched,
    QCD_Pt300to470_MuEnriched,
    QCD_Pt470to600_MuEnriched,
    QCD_Pt600to800_MuEnriched,
    QCD_Pt800to1000_MuEnriched,
    QCD_Pt1000toInf_MuEnriched,
]


# QCD EMEnr  (cross sections form genXSecAna)
QCD_Pt15to20_EMEnriched   = kreator.makeMCComponent("QCD_Pt15to20_EMEnriched"  ,"/QCD_Pt-15to20_EMEnriched_TuneCP5_13TeV_pythia8/RunIIFall17NanoAODv7-PU2017_12Apr2018_Nano02Apr2020_102X_mc2017_realistic_v8-v1/NANOAODSIM"  , "CMS", ".*root",  1.33e+06)
QCD_Pt20to30_EMEnriched   = kreator.makeMCComponent("QCD_Pt20to30_EMEnriched"  ,"/QCD_Pt-20to30_EMEnriched_TuneCP5_13TeV_pythia8/RunIIFall17NanoAODv7-PU2017_12Apr2018_Nano02Apr2020_102X_mc2017_realistic_v8-v1/NANOAODSIM"  , "CMS", ".*root",  4.928e+06)
QCD_Pt30to50_EMEnriched   = kreator.makeMCComponent("QCD_Pt30to50_EMEnriched"  ,"/QCD_Pt-30to50_EMEnriched_TuneCP5_13TeV_pythia8/RunIIFall17NanoAODv7-PU2017_12Apr2018_Nano02Apr2020_102X_mc2017_realistic_v8-v1/NANOAODSIM"  , "CMS", ".*root",  6.41e+06)
QCD_Pt50to80_EMEnriched   = kreator.makeMCComponent("QCD_Pt50to80_EMEnriched", "/QCD_Pt-50to80_EMEnriched_TuneCP5_13TeV_pythia8/RunIIFall17NanoAODv7-PU2017_12Apr2018_Nano02Apr2020_102X_mc2017_realistic_v8-v1/NANOAODSIM", "CMS", ".*root",  1.986e+06)
QCD_Pt80to120_EMEnriched  = kreator.makeMCComponent("QCD_Pt80to120_EMEnriched" ,"/QCD_Pt-80to120_EMEnriched_TuneCP5_13TeV_pythia8/RunIIFall17NanoAODv7-PU2017_12Apr2018_Nano02Apr2020_102X_mc2017_realistic_v8-v1/NANOAODSIM" , "CMS", ".*root",  370900)
QCD_Pt120to170_EMEnriched = kreator.makeMCComponent("QCD_Pt120to170_EMEnriched","/QCD_Pt-120to170_EMEnriched_TuneCP5_13TeV_pythia8/RunIIFall17NanoAODv7-PU2017_12Apr2018_Nano02Apr2020_102X_mc2017_realistic_v8-v1/NANOAODSIM", "CMS", ".*root",  66760)
QCD_Pt170to300_EMEnriched = kreator.makeMCComponent("QCD_Pt170to300_EMEnriched","/QCD_Pt-170to300_EMEnriched_TuneCP5_13TeV_pythia8/RunIIFall17NanoAODv7-PU2017_12Apr2018_Nano02Apr2020_102X_mc2017_realistic_v8-v1/NANOAODSIM", "CMS", ".*root",  16430)
QCD_Pt300toInf_EMEnriched = kreator.makeMCComponent("QCD_Pt300toInf_EMEnriched","/QCD_Pt-300toInf_EMEnriched_TuneCP5_13TeV_pythia8/RunIIFall17NanoAODv7-PU2017_12Apr2018_Nano02Apr2020_102X_mc2017_realistic_v8-v1/NANOAODSIM", "CMS", ".*root",  1101)

QCD_EMs = [
    QCD_Pt15to20_EMEnriched,
    QCD_Pt20to30_EMEnriched,
    QCD_Pt30to50_EMEnriched,
    QCD_Pt50to80_EMEnriched,
    QCD_Pt80to120_EMEnriched,
    QCD_Pt120to170_EMEnriched,
    QCD_Pt170to300_EMEnriched,
    QCD_Pt300toInf_EMEnriched
]


QCD_Pt20to30_bcToE   = kreator.makeMCComponent("QCD_Pt20to30_bcToE",   "/QCD_Pt_20to30_bcToE_TuneCP5_13TeV_pythia8/RunIIFall17NanoAODv7-PU2017_12Apr2018_Nano02Apr2020_102X_mc2017_realistic_v8-v1/NANOAODSIM"  , "CMS", ".*root", 313500)
QCD_Pt30to80_bcToE   = kreator.makeMCComponent("QCD_Pt30to80_bcToE",   "/QCD_Pt_30to80_bcToE_TuneCP5_13TeV_pythia8/RunIIFall17NanoAODv7-PU2017_12Apr2018_Nano02Apr2020_102X_mc2017_realistic_v8-v1/NANOAODSIM"  , "CMS", ".*root", 361500)
QCD_Pt80to170_bcToE  = kreator.makeMCComponent("QCD_Pt80to170_bcToE",  "/QCD_Pt_80to170_bcToE_TuneCP5_13TeV_pythia8/RunIIFall17NanoAODv7-PU2017_12Apr2018_Nano02Apr2020_102X_mc2017_realistic_v8-v1/NANOAODSIM" , "CMS", ".*root", 33770)
QCD_Pt170to250_bcToE = kreator.makeMCComponent("QCD_Pt170to250_bcToE", "/QCD_Pt_170to250_bcToE_TuneCP5_13TeV_pythia8/RunIIFall17NanoAODv7-PU2017_12Apr2018_Nano02Apr2020_102X_mc2017_realistic_v8-v1/NANOAODSIM", "CMS", ".*root", 2126)
QCD_Pt250toInf_bcToE = kreator.makeMCComponent("QCD_Pt250toInf_bcToE", "/QCD_Pt_250toInf_bcToE_TuneCP5_13TeV_pythia8/RunIIFall17NanoAODv7-PU2017_12Apr2018_Nano02Apr2020_102X_mc2017_realistic_v8-v1/NANOAODSIM", "CMS", ".*root", 563.1)

QCD_bcToE = [

    QCD_Pt20to30_bcToE,
    QCD_Pt30to80_bcToE,
    QCD_Pt80to170_bcToE,
    QCD_Pt170to250_bcToE,
    QCD_Pt250toInf_bcToE,
]

### gg fusion
GGHZZ4L      = kreator.makeMCComponent("GGHZZ4L", "/GluGluHToZZTo4L_M125_13TeV_powheg2_JHUGenV7011_pythia8/RunIIFall17NanoAODv7-PU2017_12Apr2018_Nano02Apr2020_102X_mc2017_realistic_v8_ext1-v1/NANOAODSIM", "CMS", ".*root", 0.01212) 
GGZZ4L       = kreator.makeMCComponent("GGZZ4L", "/GluGluToContinToZZTo4L_13TeV_TuneCP5_madgraphMLM_pythia8/RunIIFall17NanoAODv7-PU2017_12Apr2018_Nano02Apr2020_102X_mc2017_realistic_v8-v1/NANOAODSIM", "CMS", ".*root", 0.014352)
GGZZ4t       = kreator.makeMCComponent("GGZZ4t","/GluGluToContinToZZTo4tau_13TeV_MCFM701_pythia8/RunIIFall17NanoAODv7-PU2017_12Apr2018_Nano02Apr2020_102X_mc2017_realistic_v8-v1/NANOAODSIM", "CMS", ".*root",0.001586)
GGZZ4t_cp5   = kreator.makeMCComponent("GGZZ4t_cp5","/GluGluToContinToZZTo4tau_13TeV_TuneCP5_MCFM701_pythia8/RunIIFall17NanoAODv7-PU2017_12Apr2018_Nano02Apr2020_102X_mc2017_realistic_v8-v1/NANOAODSIM", "CMS", ".*root",0.001586)
GGZZ4m       = kreator.makeMCComponent("GGZZ4m","/GluGluToContinToZZTo4mu_13TeV_MCFM701_pythia8/RunIIFall17NanoAODv7-PU2017_12Apr2018_Nano02Apr2020_102X_mc2017_realistic_v8_ext2-v1/NANOAODSIM", "CMS", ".*root",0.001586)
GGZZ4m_ext   = kreator.makeMCComponent("GGZZ4m_ext","/GluGluToContinToZZTo4mu_13TeV_MCFM701_pythia8/RunIIFall17NanoAODv7-PU2017_12Apr2018_Nano02Apr2020_102X_mc2017_realistic_v8_ext1-v1/NANOAODSIM", "CMS", ".*root",0.001586)
GGZZ4m_cp5   = kreator.makeMCComponent("GGZZ4m_cp5","/GluGluToContinToZZTo4mu_13TeV_TuneCP5_MCFM701_pythia8/RunIIFall17NanoAODv7-PU2017_12Apr2018_Nano02Apr2020_102X_mc2017_realistic_v8-v1/NANOAODSIM", "CMS", ".*root",0.001586)

GGZZ4e       = kreator.makeMCComponent("GGZZ4e","/GluGluToContinToZZTo4e_13TeV_MCFM701_pythia8/RunIIFall17NanoAODv7-PU2017_12Apr2018_Nano02Apr2020_102X_mc2017_realistic_v8-v1/NANOAODSIM","CMS", ".*root",0.001586)
GGZZ4e_cp5   = kreator.makeMCComponent("GGZZ4e_cp5","/GluGluToContinToZZTo4e_13TeV_TuneCP5_MCFM701_pythia8/RunIIFall17NanoAODv7-PU2017_12Apr2018_Nano02Apr2020_102X_mc2017_realistic_v8-v1/NANOAODSIM","CMS", ".*root",0.001586)

GGZZ2m2t     = kreator.makeMCComponent("GGZZ2m2t","/GluGluToContinToZZTo2mu2tau_13TeV_MCFM701_pythia8/RunIIFall17NanoAODv7-PU2017_12Apr2018_Nano02Apr2020_102X_mc2017_realistic_v8_ext1-v1/NANOAODSIM", "CMS", ".*root",0.003194)
GGZZ2m2t_ext = kreator.makeMCComponent("GGZZ2m2t_ext","/GluGluToContinToZZTo2mu2tau_13TeV_MCFM701_pythia8/RunIIFall17NanoAODv7-PU2017_12Apr2018_Nano02Apr2020_102X_mc2017_realistic_v8_ext1-v1/NANOAODSIM", "CMS", ".*root",0.003194)
GGZZ2m2t_cp5 = kreator.makeMCComponent("GGZZ2m2t_cp5","/GluGluToContinToZZTo2mu2tau_13TeV_TuneCP5_MCFM701_pythia8/RunIIFall17NanoAODv7-PU2017_12Apr2018_Nano02Apr2020_102X_mc2017_realistic_v8-v1/NANOAODSIM", "CMS", ".*root",0.003194)

GGZZ2e2t     = kreator.makeMCComponent("GGZZ2e2t","/GluGluToContinToZZTo2e2tau_13TeV_MCFM701_pythia8/RunIIFall17NanoAODv7-PU2017_12Apr2018_Nano02Apr2020_102X_mc2017_realistic_v8_ext1-v1/NANOAODSIM", "CMS", ".*root",0.003194)
GGZZ2e2t_cp5 = kreator.makeMCComponent("GGZZ2e2t_cp5","/GluGluToContinToZZTo2e2tau_13TeV_TuneCP5_MCFM701_pythia8/RunIIFall17NanoAODv7-PU2017_12Apr2018_Nano02Apr2020_102X_mc2017_realistic_v8-v1/NANOAODSIM", "CMS", ".*root",0.003194)
GGZZ2e2m     = kreator.makeMCComponent("GGZZ2e2m","/GluGluToContinToZZTo2e2mu_13TeV_MCFM701_pythia8/RunIIFall17NanoAODv7-PU2017_12Apr2018_Nano02Apr2020_102X_mc2017_realistic_v8_ext1-v1/NANOAODSIM", "CMS", ".*root",0.003194)
GGZZ2e2m_ext = kreator.makeMCComponent("GGZZ2e2m_ext","/GluGluToContinToZZTo2e2mu_13TeV_MCFM701_pythia8/RunIIFall17NanoAODv7-PU2017_12Apr2018_Nano02Apr2020_102X_mc2017_realistic_v8_ext1-v1/NANOAODSIM", "CMS", ".*root",0.003194)
GGZZ2e2m_cp5 = kreator.makeMCComponent("GGZZ2e2m_cp5","/GluGluToContinToZZTo2e2mu_13TeV_TuneCP5_MCFM701_pythia8/RunIIFall17NanoAODv7-PU2017_12Apr2018_Nano02Apr2020_102X_mc2017_realistic_v8-v1/NANOAODSIM", "CMS", ".*root",0.003194)





GGFusion= [
    GGHZZ4L,
    GGZZ4L,
    GGZZ4t,
    GGZZ4t_cp5,
    GGZZ4m,
    GGZZ4m_ext,
    GGZZ4m_cp5,
    GGZZ4e,
    GGZZ4e_cp5,
    GGZZ2m2t,
    GGZZ2m2t_ext,
    GGZZ2m2t_cp5,
    GGZZ2e2t,
    GGZZ2e2t_cp5,
    GGZZ2e2m,
    GGZZ2e2m_ext,
    GGZZ2e2m_cp5
]



### ----------------------------- summary ----------------------------------------

mcSamples = Top + EWK + DiBosons + TriBosons + QCD_MuEnriched + QCD_EMs + QCD_bcToE + GGFusion #+ privateProd

samples = mcSamples

if __name__ == "__main__":
    from CMGTools.RootTools.samples.tools import runMain
    runMain(samples,localobjs=locals())
