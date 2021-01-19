from CMGTools.RootTools.samples.ComponentCreator import ComponentCreator
kreator = ComponentCreator()


TTJets = kreator.makeMCComponent("TTJets", "/TTJets_TuneCUETP8M2T4_13TeV-amcatnloFXFX-pythia8/RunIISummer16NanoAODv7-PUMoriond17_Nano02Apr2020_102X_mcRun2_asymptotic_v8-v1/NANOAODSIM", "CMS", ".*root", 831.76, fracNegWeights=0.319)
TTJets_ext = kreator.makeMCComponent("TTJets_ext","/TTJets_TuneCUETP8M2T4_13TeV-amcatnloFXFX-pythia8/RunIISummer16NanoAODv7-PUMoriond17_Nano02Apr2020_102X_mcRun2_asymptotic_v8-v1/NANOAODSIM" , "CMS",".*root", 831.76, fracNegWeights=0.319)
TTTo2L2Nu = kreator.makeMCComponent("TTTo2L2Nu","/TTTo2L2Nu_TuneCUETP8M2_ttHtranche3_13TeV-powheg-pythia8/RunIISummer16NanoAODv7-PUMoriond17_Nano02Apr2020_102X_mcRun2_asymptotic_v8-v1/NANOAODSIM" , "CMS",".*root", 87.310)
TTJets_DiLepton = kreator.makeMCComponent("TTJets_DiLepton", "/TTJets_DiLept_TuneCUETP8M1_13TeV-madgraphMLM-pythia8/RunIISummer16NanoAODv7-PUMoriond17_Nano02Apr2020_102X_mcRun2_asymptotic_v8-v1/NANOAODSIM"     , "CMS", ".*root", 831.76*((3*0.108)**2) )

TGJets_lep = kreator.makeMCComponent("TGJets_lep", "/TGJets_leptonDecays_13TeV_amcatnlo_madspin_pythia8/RunIISummer16NanoAODv7-PUMoriond17_Nano02Apr2020_102X_mcRun2_asymptotic_v8-v1/NANOAODSIM", "CMS", ".*root", 1.018, fracNegWeights=0.4)


TTJets_SingleLeptonFromTbar     = kreator.makeMCComponent("TTJets_SingleLeptonFromTbar"    , "/TTJets_SingleLeptFromTbar_TuneCUETP8M1_13TeV-madgraphMLM-pythia8/RunIISummer16NanoAODv7-PUMoriond17_Nano02Apr2020_102X_mcRun2_asymptotic_v8-v1/NANOAODSIM", "CMS", ".*root", 831.76*(3*0.108)*(1-3*0.108) )
TTJets_SingleLeptonFromTbar_ext = kreator.makeMCComponent("TTJets_SingleLeptonFromTbar_ext", "/TTJets_SingleLeptFromTbar_TuneCUETP8M1_13TeV-madgraphMLM-pythia8/RunIISummer16NanoAODv7-PUMoriond17_Nano02Apr2020_102X_mcRun2_asymptotic_v8_ext1-v1/NANOAODSIM", "CMS", ".*root", 831.76*(3*0.108)*(1-3*0.108) )
TTJets_SingleLeptonFromT        = kreator.makeMCComponent("TTJets_SingleLeptonFromT"       , "/TTJets_SingleLeptFromT_TuneCUETP8M1_13TeV-madgraphMLM-pythia8/RunIISummer16NanoAODv7-PUMoriond17_Nano02Apr2020_102X_mcRun2_asymptotic_v8-v1/NANOAODSIM", "CMS", ".*root", 831.76*(3*0.108)*(1-3*0.108))
TTJets_SingleLeptonFromT_ext    = kreator.makeMCComponent("TTJets_SingleLeptonFromT_ext"   , "/TTJets_SingleLeptFromT_TuneCUETP8M1_13TeV-madgraphMLM-pythia8/RunIISummer16NanoAODv7-PUMoriond17_Nano02Apr2020_102X_mcRun2_asymptotic_v8_ext1-v1/NANOAODSIM", "CMS", ".*root", 831.76*(3*0.108)*(1-3*0.108))

TTLep_pow = kreator.makeMCComponent("TTLep_pow", "/TTTo2L2Nu_TuneCUETP8M2_ttHtranche3_13TeV-powheg-pythia8/RunIISummer16NanoAODv7-PUMoriond17_Nano02Apr2020_102X_mcRun2_asymptotic_v8-v1/NANOAODSIM", "CMS", ".*root", 831.76*((3*0.108)**2) )
TTSemi_pow = kreator.makeMCComponent("TTSemi_pow", "/TTToSemilepton_TuneCUETP8M2_ttHtranche3_13TeV-powheg-pythia8/RunIISummer16NanoAODv7-PUMoriond17_Nano02Apr2020_102X_mcRun2_asymptotic_v8-v1/NANOAODSIM", "CMS", ".*root", 2*831.76*(3*0.108)*(1-3*0.108) )


Top = [
TTJets,
TTJets_ext,
TTTo2L2Nu,
TTJets_DiLepton,
TGJets_lep,
TTJets_SingleLeptonFromTbar,
TTJets_SingleLeptonFromTbar_ext,
TTJets_SingleLeptonFromT,
TTJets_SingleLeptonFromT_ext,
TTLep_pow,
TTSemi_pow
]



T_sch_lep = kreator.makeMCComponent("T_sch_lep", "/ST_s-channel_4f_leptonDecays_13TeV-amcatnlo-pythia8_TuneCUETP8M1/RunIISummer16NanoAODv7-PUMoriond17_Nano02Apr2020_102X_mcRun2_asymptotic_v8-v1/NANOAODSIM", "CMS", ".*root", (7.20+4.16)*0.108*3, fracNegWeights=0.188)
T_tch = kreator.makeMCComponent("T_tch", "/ST_t-channel_top_4f_inclusiveDecays_13TeV_PSweights-powhegV2-madspin/RunIISummer16NanoAODv7-PUMoriond17_Nano02Apr2020_102X_mcRun2_asymptotic_v8-v1/NANOAODSIM", "CMS", ".*root", 136.02) # inclusive sample
TBar_tch = kreator.makeMCComponent("TBar_tch", "/ST_t-channel_antitop_4f_inclusiveDecays_13TeV-powhegV2-madspin-pythia8_TuneCUETP8M1/RunIISummer16NanoAODv7-PUMoriond17_Nano02Apr2020_102X_mcRun2_asymptotic_v8-v1/NANOAODSIM", "CMS", ".*root", 80.95) # inclusive sample
T_tWch = kreator.makeMCComponent("T_tWch", "/ST_tW_top_5f_inclusiveDecays_13TeV-powheg-pythia8_TuneCUETP8M1/RunIISummer16NanoAODv7-PUMoriond17_Nano02Apr2020_102X_mcRun2_asymptotic_v8_ext1-v1/NANOAODSIM", "CMS", ".*root",35.6)
TBar_tWch = kreator.makeMCComponent("TBar_tWch", "/ST_tW_antitop_5f_inclusiveDecays_13TeV-powheg-pythia8_TuneCUETP8M1/RunIISummer16NanoAODv7-PUMoriond17_Nano02Apr2020_102X_mcRun2_asymptotic_v8_ext1-v1/NANOAODSIM", "CMS", ".*root",35.6)


T_tWch_noFullyHad = kreator.makeMCComponent("T_tWch_noFullyHad", "/ST_tW_top_5f_NoFullyHadronicDecays_13TeV-powheg_TuneCUETP8M1/RunIISummer16NanoAODv7-Nano02Apr2020_102X_mcRun2_asymptotic_v8_ext2-v1/NANOAODSIM", "CMS", ".*root",19.55)
T_tWch_noFullyHad_ext = kreator.makeMCComponent("T_tWch_noFullyHad_ext", "/ST_tW_top_5f_NoFullyHadronicDecays_13TeV-powheg_TuneCUETP8M1/RunIISummer16NanoAODv7-PUMoriond17_Nano02Apr2020_102X_mcRun2_asymptotic_v8-v1/NANOAODSIM", "CMS", ".*root",19.55)
T_tWch_noFullyHad_ext2 = kreator.makeMCComponent("T_tWch_noFullyHad_ext2", "/ST_tW_top_5f_NoFullyHadronicDecays_13TeV-powheg_TuneCUETP8M1/RunIISummer16NanoAODv7-PUMoriond17_Nano02Apr2020_102X_mcRun2_asymptotic_v8_ext1-v1/NANOAODSIM", "CMS", ".*root",19.55)

TBar_tWch_noFullyHad      = kreator.makeMCComponent("TBar_tWch_noFullyHad"     , "/ST_tW_antitop_5f_NoFullyHadronicDecays_13TeV-powheg_TuneCUETP8M1/RunIISummer16NanoAODv7-Nano02Apr2020_102X_mcRun2_asymptotic_v8_ext2-v1/NANOAODSIM", "CMS", ".*root",19.55)
TBar_tWch_noFullyHad_ext  = kreator.makeMCComponent("TBar_tWch_noFullyHad_ext" , "/ST_tW_antitop_5f_NoFullyHadronicDecays_13TeV-powheg_TuneCUETP8M1/RunIISummer16NanoAODv7-PUMoriond17_Nano02Apr2020_102X_mcRun2_asymptotic_v8-v1/NANOAODSIM", "CMS", ".*root",19.55)
TBar_tWch_noFullyHad_ext2 = kreator.makeMCComponent("TBar_tWch_noFullyHad_ext2", "/ST_tW_antitop_5f_NoFullyHadronicDecays_13TeV-powheg_TuneCUETP8M1/RunIISummer16NanoAODv7-PUMoriond17_Nano02Apr2020_102X_mcRun2_asymptotic_v8_ext1-v1/NANOAODSIM", "CMS", ".*root",19.55)

SingleTop = [
T_sch_lep,
T_tch,
TBar_tch,
T_tWch,
TBar_tWch,
T_tWch_noFullyHad,
T_tWch_noFullyHad_ext,
T_tWch_noFullyHad_ext2,
TBar_tWch_noFullyHad,
TBar_tWch_noFullyHad_ext,
TBar_tWch_noFullyHad_ext2,
]








### V+jets inclusive (from https://twiki.cern.ch/twiki/bin/viewauth/CMS/StandardModelCrossSectionsat13TeV)
WJetsToLNu_ext = kreator.makeMCComponent("WJetsToLNu","/WJetsToLNu_TuneCUETP8M1_13TeV-amcatnloFXFX-pythia8/RunIISummer16NanoAODv7-PUMoriond17_Nano02Apr2020_102X_mcRun2_asymptotic_v8_ext2-v1/NANOAODSIM", "CMS", ".*root", 3* 20508.9, fracNegWeights=0.16)
WJetsToLNu = kreator.makeMCComponent("WJetsToLNu_ext","/WJetsToLNu_TuneCUETP8M1_13TeV-amcatnloFXFX-pythia8/RunIISummer16NanoAODv7-PUMoriond17_Nano02Apr2020_102X_mcRun2_asymptotic_v8-v1/NANOAODSIM", "CMS", ".*root", 3* 20508.9, fracNegWeights=0.16)
WJetsToLNu_LO = kreator.makeMCComponent("WJetsToLNu_LO","/WJetsToLNu_TuneCUETP8M1_13TeV-madgraphMLM-pythia8/RunIISummer16NanoAODv7-PUMoriond17_Nano02Apr2020_102X_mcRun2_asymptotic_v8-v1/NANOAODSIM", "CMS", ".*root", 3* 20508.9)
WJetsToLNu_LO_ext =  kreator.makeMCComponent("WJetsToLNu_LO_ext", "/WJetsToLNu_TuneCUETP8M1_13TeV-madgraphMLM-pythia8/RunIISummer16NanoAODv7-PUMoriond17_Nano02Apr2020_102X_mcRun2_asymptotic_v8_ext2-v1/NANOAODSIM", "CMS", ".*root", 61526.7)






DYJetsToLL_M10to50 = kreator.makeMCComponent("DYJetsToLL_M10to50", "/DYJetsToLL_M-10to50_TuneCUETP8M1_13TeV-amcatnloFXFX-pythia8/RunIISummer16NanoAODv7-PUMoriond17_Nano02Apr2020_102X_mcRun2_asymptotic_v8_ext1-v1/NANOAODSIM", "CMS", ".*root", 18610, fracNegWeights=0.135)

DYJetsToLL_M10to50_LO = kreator.makeMCComponent("DYJetsToLL_M10to50_LO", "/DYJetsToLL_M-10to50_TuneCUETP8M1_13TeV-madgraphMLM-pythia8/RunIISummer16NanoAODv7-PUMoriond17_Nano02Apr2020_102X_mcRun2_asymptotic_v8-v1/NANOAODSIM", "CMS", ".*root", 18610)

DYJetsToLL_M50 = kreator.makeMCComponent("DYJetsToLL_M50", "/DYJetsToLL_M-50_TuneCUETP8M1_13TeV-amcatnloFXFX-pythia8/RunIISummer16NanoAODv7-PUMoriond17_Nano02Apr2020_102X_mcRun2_asymptotic_v8_ext2-v1/NANOAODSIM", "CMS", ".*root", 2008.*3, fracNegWeights=0.16)

DYJetsToLL_M50_LO_ext =  kreator.makeMCComponent("DYJetsToLL_M50_LO_ext", "/DYJetsToLL_M-50_TuneCUETP8M1_13TeV-madgraphMLM-pythia8/RunIISummer16NanoAODv7-PUMoriond17_Nano02Apr2020_102X_mcRun2_asymptotic_v8_ext1-v1/NANOAODSIM", "CMS", ".*root", 2008.*3)
DYJetsToLL_M50_LO =  kreator.makeMCComponent("DYJetsToLL_M50_LO","/DYJetsToLL_M-50_TuneCUETP8M1_13TeV-madgraphMLM-pythia8/RunIISummer16NanoAODv7-PUMoriond17_Nano02Apr2020_102X_mcRun2_asymptotic_v8_ext2-v1/NANOAODSIM", "CMS", ".*root", 2008.*3)




VJets = [
WJetsToLNu,
WJetsToLNu_ext,
WJetsToLNu_LO,
WJetsToLNu_LO_ext,
DYJetsToLL_M10to50,
#DYJetsToLL_M10to50_ext,
DYJetsToLL_M10to50_LO,
DYJetsToLL_M50,
DYJetsToLL_M50_LO,
DYJetsToLL_M50_LO_ext,
]



# DY njet bins
DY1JetsToLL_M50_LO =  kreator.makeMCComponent("DY1JetsToLL_M50_LO", "/DY1JetsToLL_M-50_TuneCUETP8M1_13TeV-madgraphMLM-pythia8/RunIISummer16NanoAODv7-PUMoriond17_Nano02Apr2020_102X_mcRun2_asymptotic_v8-v1/NANOAODSIM", "CMS", ".*root", 1012.5)
DY2JetsToLL_M50_LO =  kreator.makeMCComponent("DY2JetsToLL_M50_LO", "/DY2JetsToLL_M-50_TuneCUETP8M1_13TeV-madgraphMLM-pythia8/RunIISummer16NanoAODv7-PUMoriond17_Nano02Apr2020_102X_mcRun2_asymptotic_v8-v1/NANOAODSIM", "CMS", ".*root", 332.8)
DY3JetsToLL_M50_LO =  kreator.makeMCComponent("DY3JetsToLL_M50_LO", "/DY3JetsToLL_M-50_TuneCUETP8M1_13TeV-madgraphMLM-pythia8/RunIISummer16NanoAODv7-PUMoriond17_Nano02Apr2020_102X_mcRun2_asymptotic_v8-v1/NANOAODSIM", "CMS", ".*root", 101.8)
DY4JetsToLL_M50_LO =  kreator.makeMCComponent("DY4JetsToLL_M50_LO", "/DY4JetsToLL_M-50_TuneCUETP8M1_13TeV-madgraphMLM-pythia8/RunIISummer16NanoAODv7-PUMoriond17_Nano02Apr2020_102X_mcRun2_asymptotic_v8-v1/NANOAODSIM", "CMS", ".*root", 54.8)

DYNJets = [ 
DY1JetsToLL_M50_LO,
DY2JetsToLL_M50_LO,
DY3JetsToLL_M50_LO,
DY4JetsToLL_M50_LO,
]

# W njet bins
W1JetsToLNu_LO =  kreator.makeMCComponent("W1JetsToLNu_LO", "/W1JetsToLNu_TuneCUETP8M1_13TeV-madgraphMLM-pythia8/RunIISummer16NanoAODv7-PUMoriond17_Nano02Apr2020_102X_mcRun2_asymptotic_v8-v1/NANOAODSIM", "CMS", ".*root", 9644.5)

W2JetsToLNu_LO =  kreator.makeMCComponent("W2JetsToLNu_LO", "/W2JetsToLNu_TuneCUETP8M1_13TeV-madgraphMLM-pythia8/RunIISummer16NanoAODv7-PUMoriond17_Nano02Apr2020_102X_mcRun2_asymptotic_v8-v1/NANOAODSIM", "CMS", ".*root", 3144.5)
W2JetsToLNu_LO_ext =  kreator.makeMCComponent("W2JetsToLNu_LO_ext", "/W2JetsToLNu_TuneCUETP8M1_13TeV-madgraphMLM-pythia8/RunIISummer16NanoAODv7-PUMoriond17_Nano02Apr2020_102X_mcRun2_asymptotic_v8_ext1-v1/NANOAODSIM", "CMS", ".*root", 3144.5)

W3JetsToLNu_LO =  kreator.makeMCComponent("W3JetsToLNu_LO", "/W3JetsToLNu_TuneCUETP8M1_13TeV-madgraphMLM-pythia8/RunIISummer16NanoAODv7-PUMoriond17_Nano02Apr2020_102X_mcRun2_asymptotic_v8-v1/NANOAODSIM", "CMS", ".*root", 954.8)
W3JetsToLNu_LO_ext =  kreator.makeMCComponent("W3JetsToLNu_LO_ext", "/W3JetsToLNu_TuneCUETP8M1_13TeV-madgraphMLM-pythia8/RunIISummer16NanoAODv7-PUMoriond17_Nano02Apr2020_102X_mcRun2_asymptotic_v8_ext1-v1/NANOAODSIM", "CMS", ".*root", 954.8)

W4JetsToLNu_LO =  kreator.makeMCComponent("W4JetsToLNu_LO", "/W4JetsToLNu_TuneCUETP8M1_13TeV-madgraphMLM-pythia8/RunIISummer16NanoAODv7-PUMoriond17_Nano02Apr2020_102X_mcRun2_asymptotic_v8-v1/NANOAODSIM", "CMS", ".*root", 485.6)
W4JetsToLNu_LO_ext =  kreator.makeMCComponent("W4JetsToLNu_LO_ext", "/W4JetsToLNu_TuneCUETP8M1_13TeV-madgraphMLM-pythia8/RunIISummer16NanoAODv7-PUMoriond17_Nano02Apr2020_102X_mcRun2_asymptotic_v8_ext1-v1/NANOAODSIM", "CMS", ".*root", 485.6)
W4JetsToLNu_LO_ext1 =  kreator.makeMCComponent("W4JetsToLNu_LO_ext1", "/W4JetsToLNu_TuneCUETP8M1_13TeV-madgraphMLM-pythia8/RunIISummer16NanoAODv7-PUMoriond17_Nano02Apr2020_102X_mcRun2_asymptotic_v8_ext2-v1/NANOAODSIM", "CMS", ".*root", 485.6)


WNJets = [
W1JetsToLNu_LO,
W2JetsToLNu_LO,
W2JetsToLNu_LO_ext,
W3JetsToLNu_LO,
W3JetsToLNu_LO_ext,
W4JetsToLNu_LO,
W4JetsToLNu_LO_ext,
W4JetsToLNu_LO_ext1,
]




### DiBosons
WWDoubleTo2L           = kreator.makeMCComponent("WWDoubleTo2L", "/WWTo2L2Nu_DoubleScattering_13TeV-pythia8/RunIISummer16NanoAODv7-PUMoriond17_Nano02Apr2020_102X_mcRun2_asymptotic_v8-v1/NANOAODSIM", "CMS", ".*root", 0.1729)
WWDoubleTo2L_herwigpp           = kreator.makeMCComponent("WWDoubleTo2L_herwigpp", "/WWTo2L2Nu_DoubleScattering_13TeV-herwigpp/RunIISummer16NanoAODv7-PUMoriond17_Nano02Apr2020_102X_mcRun2_asymptotic_v8-v1/NANOAODSIM", "CMS", ".*root", 0.1729)

WZTo3LNu               = kreator.makeMCComponent("WZTo3LNu", "/WZTo3LNu_TuneCUETP8M1_13TeV-powheg-pythia8/RunIISummer16NanoAODv7-PUMoriond17_Nano02Apr2020_102X_mcRun2_asymptotic_v8-v1/NANOAODSIM", "CMS", ".*root", 4.42965)
WZTo3LNu_ext           = kreator.makeMCComponent("WZTo3LNu_ext", "/WZTo3LNu_TuneCUETP8M1_13TeV-powheg-pythia8/RunIISummer16NanoAODv7-PUMoriond17_Nano02Apr2020_102X_mcRun2_asymptotic_v8_ext1-v1/NANOAODSIM", "CMS", ".*root", 4.42965)

WZTo3LNu_fxfx          = kreator.makeMCComponent("WZTo3LNu_fxfx", "/WZTo3LNu_TuneCUETP8M1_13TeV-amcatnloFXFX-pythia8/RunIISummer16NanoAODv7-PUMoriond17_Nano02Apr2020_102X_mcRun2_asymptotic_v8-v1/NANOAODSIM", "CMS", ".*root", 4.666, fracNegWeights=0.19)


WZTo3LNu_mllmin01      = kreator.makeMCComponent("WZTo3LNu_mllmin01", "/WZTo3LNu_mllmin01_13TeV-powheg-pythia8/RunIISummer16NanoAODv7-PUMoriond17_Nano02Apr2020_102X_mcRun2_asymptotic_v8-v1/NANOAODSIM", "CMS", ".*root", 58.59*0.601644)

WZTo3LNu_mllmin01_ext = kreator.makeMCComponent("WZTo3LNu_mllmin01_ext", "/WZTo3LNu_mllmin01_13TeV-powheg-pythia8_ext1/RunIISummer16NanoAODv7-PUMoriond17_Nano02Apr2020_102X_mcRun2_asymptotic_v8_ext1-v1/NANOAODSIM", "CMS", ".*root", 58.59*0.601644)

WWTo2L2Nu              = kreator.makeMCComponent("WWTo2L2Nu", "/WWTo2L2Nu_13TeV-powheg/RunIISummer16NanoAODv7-PUMoriond17_Nano02Apr2020_102X_mcRun2_asymptotic_v8-v1/NANOAODSIM", "CMS", ".*root", 10.481)
ZZTo4L                 = kreator.makeMCComponent("ZZTo4L", "/ZZTo4L_13TeV_powheg_pythia8/RunIISummer16NanoAODv7-PUMoriond17_Nano02Apr2020_102X_mcRun2_asymptotic_v8-v1/NANOAODSIM", "CMS", ".*root", 1.256)
WpWpJJ                 = kreator.makeMCComponent("WpWpJJ", "/WpWpJJ_EWK-QCD_TuneCUETP8M1_13TeV-madgraph-pythia8/RunIISummer16NanoAODv7-PUMoriond17_Nano02Apr2020_102X_mcRun2_asymptotic_v8-v1/NANOAODSIM", "CMS", ".*root", 0.03711)
ZGTo2LG                = kreator.makeMCComponent("ZGTo2LG", "/ZGTo2LG_TuneCUETP8M1_13TeV-amcatnloFXFX-pythia8/RunIISummer16NanoAODv7-PUMoriond17_Nano02Apr2020_102X_mcRun2_asymptotic_v8-v1/NANOAODSIM", "CMS", ".*root", 131.3, fracNegWeights=0.16)
ZGTo2LG_ext          = kreator.makeMCComponent("ZGTo2LG_ext", "/ZGTo2LG_TuneCUETP8M1_13TeV-amcatnloFXFX-pythia8/RunIISummer16NanoAODv7-PUMoriond17_Nano02Apr2020_102X_mcRun2_asymptotic_v8_ext1-v1/NANOAODSIM", "CMS", ".*root", 131.3, fracNegWeights=0.16)
WGToLNuG               = kreator.makeMCComponent("WGToLNuG", "/WGToLNuG_TuneCUETP8M1_13TeV-madgraphMLM-pythia8/RunIISummer16NanoAODv7-PUMoriond17_Nano02Apr2020_102X_mcRun2_asymptotic_v8-v1/NANOAODSIM", "CMS", ".*root", 585.8)
WGToLNuG_amcatnlo    = kreator.makeMCComponent("WGToLNuG_amcatnlo", "/WGToLNuG_TuneCUETP8M1_13TeV-amcatnloFXFX-pythia8/RunIISummer16NanoAODv7-PUMoriond17_Nano02Apr2020_102X_mcRun2_asymptotic_v8_ext1-v1/NANOAODSIM", "CMS", ".*root", 511.2, fracNegWeights=0.18) 
WGToLNuG_amcatnlo_ext = kreator.makeMCComponent("WGToLNuG_amcatnlo_ext",  "/WGToLNuG_TuneCUETP8M1_13TeV-amcatnloFXFX-pythia8/RunIISummer16NanoAODv7-PUMoriond17_Nano02Apr2020_102X_mcRun2_asymptotic_v8_ext2-v1/NANOAODSIM", "CMS", ".*root", 511.2, fracNegWeights=0.18)
WGToLNuG_amcatnlo_ext1 = kreator.makeMCComponent("WGToLNuG_amcatnlo_ext1",  "/WGToLNuG_TuneCUETP8M1_13TeV-amcatnloFXFX-pythia8/RunIISummer16NanoAODv7-PUMoriond17_Nano02Apr2020_102X_mcRun2_asymptotic_v8_ext3-v1/NANOAODSIM", "CMS", ".*root", 511.2, fracNegWeights=0.18) 
WgStarLNuMuMu          = kreator.makeMCComponent("WgStarLNuMuMu", "/WGstarToLNuMuMu_012Jets_13TeV-madgraph/RunIISummer16NanoAODv7-PUMoriond17_Nano02Apr2020_102X_mcRun2_asymptotic_v8-v1/NANOAODSIM", "CMS",".*root", 2.793)
WgStarLNuEE            = kreator.makeMCComponent("WgStarLNuEE", "/WGstarToLNuEE_012Jets_13TeV-madgraph/RunIISummer16NanoAODv7-PUMoriond17_Nano02Apr2020_102X_mcRun2_asymptotic_v8-v1/NANOAODSIM", "CMS", ".*root", 3.526)


WGToLNuG_01J_amcatnlo                 = kreator.makeMCComponent("WGToLNuG_01J_amcatnlo", "/WGToLNuG_01J_5f_TuneCUETP8M1_13TeV-amcatnloFXFX-pythia8/RunIISummer16NanoAODv7-PUMoriond17_Nano02Apr2020_102X_mcRun2_asymptotic_v8-v1/NANOAODSIM", "CMS", ".*root", 178.4,fracNegWeights=0.203)
WGToLNuG_01J_amcatnlo_ext                 = kreator.makeMCComponent("WGToLNuG_01J_amcatnlo_ext", "/WGToLNuG_01J_5f_TuneCUETP8M1_13TeV-amcatnloFXFX-pythia8/RunIISummer16NanoAODv7-PUMoriond17_Nano02Apr2020_102X_mcRun2_asymptotic_v8_ext1-v1/NANOAODSIM", "CMS", ".*root", 178.4,fracNegWeights=0.203)

ZGToLLG_01J_amcatnlo                 = kreator.makeMCComponent("ZGToLLG_01J_amcatnlo", "/ZGToLLG_01J_5f_TuneCUETP8M1_13TeV-amcatnloFXFX-pythia8/RunIISummer16NanoAODv7-PUMoriond17_Nano02Apr2020_102X_mcRun2_asymptotic_v8-v1/NANOAODSIM", "CMS", ".*root", 58.83,fracNegWeights=0.2)
ZGToLLG_01J_amcatnlo_ext                 = kreator.makeMCComponent("ZGToLLG_01J_amcatnlo_ext", "/ZGToLLG_01J_5f_TuneCUETP8M1_13TeV-amcatnloFXFX-pythia8/RunIISummer16NanoAODv7-PUMoriond17_Nano02Apr2020_102X_mcRun2_asymptotic_v8_ext1-v1/NANOAODSIM", "CMS", ".*root", 58.83,fracNegWeights=0.202)

ZGToLLG_01J_lowmll_amcatnlo                 = kreator.makeMCComponent("ZGToLLG_01J_lowmll_amcatnlo", "/ZGToLLG_01J_5f_lowMLL_TuneCUETP8M1_13TeV-amcatnloFXFX-pythia8/RunIISummer16NanoAODv7-PUMoriond17_Nano02Apr2020_102X_mcRun2_asymptotic_v8-v1/NANOAODSIM", "CMS", ".*root", 97.21,fracNegWeights=0.18)




WW_ext                 = kreator.makeMCComponent("WW", "/WW_TuneCUETP8M1_13TeV-pythia8/RunIISummer16NanoAODv7-PUMoriond17_Nano02Apr2020_102X_mcRun2_asymptotic_v8_ext1-v1/NANOAODSIM", "CMS", ".*root", 63.21 * 1.82)
WW                     = kreator.makeMCComponent("WW_ext", "/WW_TuneCUETP8M1_13TeV-pythia8/RunIISummer16NanoAODv7-PUMoriond17_Nano02Apr2020_102X_mcRun2_asymptotic_v8-v1/NANOAODSIM", "CMS", ".*root", 63.21 * 1.82)



DiBosons = [
WWDoubleTo2L,
WWDoubleTo2L_herwigpp,
WZTo3LNu,
WZTo3LNu_ext,
WZTo3LNu_fxfx,
WZTo3LNu_mllmin01,
WZTo3LNu_mllmin01_ext,
WWTo2L2Nu,              
ZZTo4L,                 
WpWpJJ,
ZGTo2LG,
ZGTo2LG_ext,
WGToLNuG,
WGToLNuG_amcatnlo,
WGToLNuG_amcatnlo_ext,
WGToLNuG_amcatnlo_ext1,
WgStarLNuMuMu,         
WgStarLNuEE,            
WGToLNuG_01J_amcatnlo,
WGToLNuG_01J_amcatnlo_ext,
ZGToLLG_01J_amcatnlo,
ZGToLLG_01J_amcatnlo_ext,
ZGToLLG_01J_lowmll_amcatnlo,
WW_ext,                 
WW
]


### TriBosons
# cross section from https://twiki.cern.ch/twiki/bin/view/CMS/SummaryTable1G25ns#Triboson

WWW = kreator.makeMCComponent("WWW", "/WWW_4F_TuneCUETP8M1_13TeV-amcatnlo-pythia8/RunIISummer16NanoAODv7-PUMoriond17_Nano02Apr2020_102X_mcRun2_asymptotic_v8-v1/NANOAODSIM", "CMS", ".*root", 0.2086, fracNegWeights=0.053)

WWZ = kreator.makeMCComponent("WWZ", "/WWZ_TuneCUETP8M1_13TeV-amcatnlo-pythia8/RunIISummer16NanoAODv7-PUMoriond17_Nano02Apr2020_102X_mcRun2_asymptotic_v8-v1/NANOAODSIM", "CMS", ".*root",  0.1651 , fracNegWeights=0.06)
WZZ = kreator.makeMCComponent("WZZ", "/WZZ_TuneCUETP8M1_13TeV-amcatnlo-pythia8/RunIISummer16NanoAODv7-PUMoriond17_Nano02Apr2020_102X_mcRun2_asymptotic_v8-v1/NANOAODSIM", "CMS", ".*root",  0.05565 , fracNegWeights=0.060)
ZZZ = kreator.makeMCComponent("ZZZ", "/ZZZ_TuneCUETP8M1_13TeV-amcatnlo-pythia8/RunIISummer16NanoAODv7-PUMoriond17_Nano02Apr2020_102X_mcRun2_asymptotic_v8-v1/NANOAODSIM", "CMS", ".*root",  0.01398 , fracNegWeights=0.060)


TriBosons = [
WWW,
WZZ,
WWZ,
ZZZ,
]

### rares


TTW_LO = kreator.makeMCComponent("TTW_LO", "/ttWJets_13TeV_madgraphMLM/RunIISummer16NanoAODv7-Nano02Apr2020_102X_mcRun2_asymptotic_v8-v1/NANOAODSIM", "CMS", ".*root",  0.6105 )
TTZ_LO = kreator.makeMCComponent("TTZ_LO", "/ttZJets_13TeV_madgraphMLM-pythia8/RunIISummer16NanoAODv7-PUMoriond17_Nano02Apr2020_102X_mcRun2_asymptotic_v8-v1/NANOAODSIM", "CMS", ".*root",  0.5297/0.692)


Rares = [
TTW_LO,
TTZ_LO,
]





# qcd muenr

QCD_Mu15 = kreator.makeMCComponent("QCD_Mu15", "/QCD_Pt-20toInf_MuEnrichedPt15_TuneCUETP8M1_13TeV_pythia8/RunIISummer16NanoAODv7-PUMoriond17_Nano02Apr2020_102X_mcRun2_asymptotic_v8-v1/NANOAODSIM", "CMS", ".*root", 720.65e6*0.00042)
QCD_Pt15to20_Mu5    = kreator.makeMCComponent("QCD_Pt15to20_Mu5"    , "/QCD_Pt-15to20_MuEnrichedPt5_TuneCUETP8M1_13TeV_pythia8/RunIISummer16NanoAODv7-PUMoriond17_Nano02Apr2020_102X_mcRun2_asymptotic_v8-v1/NANOAODSIM"       , "CMS" , ".*root" , 1273190000*0.003)
QCD_Pt20to30_Mu5    = kreator.makeMCComponent("QCD_Pt20to30_Mu5"    , "/QCD_Pt-20to30_MuEnrichedPt5_TuneCUETP8M1_13TeV_pythia8/RunIISummer16NanoAODv7-PUMoriond17_Nano02Apr2020_102X_mcRun2_asymptotic_v8-v1/NANOAODSIM"      , "CMS" , ".*root" , 558528000*0.0053)
QCD_Pt30to50_Mu5    = kreator.makeMCComponent("QCD_Pt30to50_Mu5", "/QCD_Pt-30to50_MuEnrichedPt5_TuneCUETP8M1_13TeV_pythia8/RunIISummer16NanoAODv7-PUMoriond17_Nano02Apr2020_102X_mcRun2_asymptotic_v8-v1/NANOAODSIM", "CMS", ".*root", 139803000*0.01182)
QCD_Pt50to80_Mu5    = kreator.makeMCComponent("QCD_Pt50to80_Mu5"    , "/QCD_Pt-50to80_MuEnrichedPt5_TuneCUETP8M1_13TeV_pythia8/RunIISummer16NanoAODv7-PUMoriond17_Nano02Apr2020_102X_mcRun2_asymptotic_v8-v1/NANOAODSIM" , "CMS" , ".*root" , 19222500*0.02276)
QCD_Pt80to120_Mu5   = kreator.makeMCComponent("QCD_Pt80to120_Mu5"   , "/QCD_Pt-80to120_MuEnrichedPt5_TuneCUETP8M1_13TeV_pythia8/RunIISummer16NanoAODv7-PUMoriond17_Nano02Apr2020_102X_mcRun2_asymptotic_v8-v1/NANOAODSIM"     , "CMS" , ".*root" , 2758420*0.03844)
QCD_Pt80to120_Mu5_ext   = kreator.makeMCComponent("QCD_Pt80to120_Mu5_ext"   , "/QCD_Pt-80to120_MuEnrichedPt5_TuneCUETP8M1_13TeV_pythia8/RunIISummer16NanoAODv7-PUMoriond17_Nano02Apr2020_102X_mcRun2_asymptotic_v8_ext1-v1/NANOAODSIM"     , "CMS" , ".*root" , 2758420*0.03844)
QCD_Pt120to170_Mu5  = kreator.makeMCComponent("QCD_Pt120to170_Mu5"  , "/QCD_Pt-120to170_MuEnrichedPt5_TuneCUETP8M1_13TeV_pythia8/RunIISummer16NanoAODv7-PUMoriond17_Nano02Apr2020_102X_mcRun2_asymptotic_v8-v1/NANOAODSIM", "CMS" , ".*root" , 469797*0.05362)


QCD_Mu5 = [
QCD_Mu15,
QCD_Pt15to20_Mu5,
QCD_Pt20to30_Mu5,
QCD_Pt30to50_Mu5,
QCD_Pt50to80_Mu5,
QCD_Pt80to120_Mu5,
QCD_Pt80to120_Mu5_ext,
QCD_Pt120to170_Mu5,

]


# qcd emenr



QCD_Pt20to30_EMEnriched   = kreator.makeMCComponent("QCD_Pt20to30_EMEnriched" ,"/QCD_Pt-20to30_EMEnriched_TuneCUETP8M1_13TeV_pythia8/RunIISummer16NanoAODv7-PUMoriond17_Nano02Apr2020_102X_mcRun2_asymptotic_v8-v1/NANOAODSIM", "CMS", ".*root",557600000*0.0096)
QCD_Pt30to50_EMEnriched   = kreator.makeMCComponent("QCD_Pt30to50_EMEnriched"  ,"/QCD_Pt-30to50_EMEnriched_TuneCUETP8M1_13TeV_pythia8/RunIISummer16NanoAODv7-PUMoriond17_Nano02Apr2020_102X_mcRun2_asymptotic_v8-v1/NANOAODSIM"  , "CMS", ".*root", 136000000*0.073)
QCD_Pt30to50_EMEnriched_ext   = kreator.makeMCComponent("QCD_Pt30to50_EMEnriched_ext"  ,"/QCD_Pt-30to50_EMEnriched_TuneCUETP8M1_13TeV_pythia8/RunIISummer16NanoAODv7-PUMoriond17_Nano02Apr2020_102X_mcRun2_asymptotic_v8_ext1-v1/NANOAODSIM"  , "CMS", ".*root", 136000000*0.073)
QCD_Pt50to80_EMEnriched   = kreator.makeMCComponent("QCD_Pt50to80_EMEnriched", "/QCD_Pt-50to80_EMEnriched_TuneCUETP8M1_13TeV_pythia8/RunIISummer16NanoAODv7-PUMoriond17_Nano02Apr2020_102X_mcRun2_asymptotic_v8-v1/NANOAODSIM", "CMS", ".*root", 19800000*0.146)
QCD_Pt50to80_EMEnriched_ext   = kreator.makeMCComponent("QCD_Pt50to80_EMEnriched_ext", "/QCD_Pt-50to80_EMEnriched_TuneCUETP8M1_13TeV_pythia8/RunIISummer16NanoAODv7-PUMoriond17_Nano02Apr2020_102X_mcRun2_asymptotic_v8_ext1-v1/NANOAODSIM", "CMS", ".*root", 19800000*0.146)

QCD_Pt80to120_EMEnriched  = kreator.makeMCComponent("QCD_Pt80to120_EMEnriched" ,"/QCD_Pt-80to120_EMEnriched_TuneCUETP8M1_13TeV_pythia8/RunIISummer16NanoAODv7-PUMoriond17_Nano02Apr2020_102X_mcRun2_asymptotic_v8_ext1-v1/NANOAODSIM" , "CMS", ".*root", 2800000*0.125)
QCD_Pt80to120_EMEnriched_ext  = kreator.makeMCComponent("QCD_Pt80to120_EMEnriched_ext" ,"/QCD_Pt-80to120_EMEnriched_TuneCUETP8M1_13TeV_pythia8/RunIISummer16NanoAODv7-PUMoriond17_Nano02Apr2020_102X_mcRun2_asymptotic_v8-v1/NANOAODSIM" , "CMS", ".*root", 2800000*0.125)
QCD_Pt120to170_EMEnriched = kreator.makeMCComponent("QCD_Pt120to170_EMEnriched" ,"/QCD_Pt-120to170_EMEnriched_TuneCUETP8M1_13TeV_pythia8/RunIISummer16NanoAODv7-PUMoriond17_Nano02Apr2020_102X_mcRun2_asymptotic_v8-v1/NANOAODSIM", "CMS", ".*root", 477000*0.132)
QCD_Pt120to170_EMEnriched_ext = kreator.makeMCComponent("QCD_Pt120to170_EMEnriched_ext" ,"/QCD_Pt-120to170_EMEnriched_TuneCUETP8M1_13TeV_pythia8/RunIISummer16NanoAODv7-PUMoriond17_Nano02Apr2020_102X_mcRun2_asymptotic_v8_ext1-v1/NANOAODSIM", "CMS", ".*root", 477000*0.132)



QCDPtEMEnriched = [
QCD_Pt20to30_EMEnriched,
QCD_Pt30to50_EMEnriched,
QCD_Pt30to50_EMEnriched_ext,
QCD_Pt50to80_EMEnriched,
QCD_Pt50to80_EMEnriched_ext,
QCD_Pt80to120_EMEnriched,
QCD_Pt80to120_EMEnriched_ext,
QCD_Pt120to170_EMEnriched,
QCD_Pt120to170_EMEnriched_ext,
]

# qcd bctoe
QCD_Pt_15to20_bcToE   = kreator.makeMCComponent("QCD_Pt_15to20_bcToE"   , "/QCD_Pt_15to20_bcToE_TuneCUETP8M1_13TeV_pythia8/RunIISummer16NanoAODv7-PUMoriond17_Nano02Apr2020_102X_mcRun2_asymptotic_v8-v1/NANOAODSIM"  , "CMS" , ".*root" , 1272980000*0.0002)
QCD_Pt_20to30_bcToE   = kreator.makeMCComponent("QCD_Pt_20to30_bcToE"   , "/QCD_Pt_20to30_bcToE_TuneCUETP8M1_13TeV_pythia8/RunIISummer16NanoAODv7-PUMoriond17_Nano02Apr2020_102X_mcRun2_asymptotic_v8-v1/NANOAODSIM"  , "CMS" , ".*root" , 557627000*0.00059)
QCD_Pt_30to80_bcToE   = kreator.makeMCComponent("QCD_Pt_30to80_bcToE"   , "/QCD_Pt_30to80_bcToE_TuneCUETP8M1_13TeV_pythia8/RunIISummer16NanoAODv7-PUMoriond17_Nano02Apr2020_102X_mcRun2_asymptotic_v8-v1/NANOAODSIM"  , "CMS" , ".*root" , 159068000*0.00255)
QCD_Pt_80to170_bcToE  = kreator.makeMCComponent("QCD_Pt_80to170_bcToE"  , "/QCD_Pt_80to170_bcToE_TuneCUETP8M1_13TeV_pythia8/RunIISummer16NanoAODv7-PUMoriond17_Nano02Apr2020_backup_102X_mcRun2_asymptotic_v8-v1/NANOAODSIM" , "CMS" , ".*root" , 3221000*0.01183)
QCD_Pt_170to250_bcToE = kreator.makeMCComponent("QCD_Pt_170to250_bcToE" , "/QCD_Pt_170to250_bcToE_TuneCUETP8M1_13TeV_pythia8/RunIISummer16NanoAODv7-PUMoriond17_Nano02Apr2020_102X_mcRun2_asymptotic_v8-v1/NANOAODSIM", "CMS", ".*root", 105771*0.02492)
QCD_Pt_250toInf_bcToE = kreator.makeMCComponent("QCD_Pt_250toInf_bcToE" , "/QCD_Pt_250toInf_bcToE_TuneCUETP8M1_13TeV_pythia8/RunIISummer16NanoAODv7-PUMoriond17_Nano02Apr2020_102X_mcRun2_asymptotic_v8-v1/NANOAODSIM", "CMS" , ".*root" , 21094.1*0.03375)

QCDPtbcToE = [
QCD_Pt_15to20_bcToE,
QCD_Pt_20to30_bcToE,
QCD_Pt_30to80_bcToE,
QCD_Pt_80to170_bcToE,
QCD_Pt_170to250_bcToE,
QCD_Pt_250toInf_bcToE
]







### ----------------------------- summary ----------------------------------------

#mcSamples = TTs + SingleTop + VJets + DYJetsM50HT + DYJetsM5to50HT + DYNJets + WJetsToLNuHT + WJetsToLNuPT + WNJets + GJetsHT + ZJetsToNuNuHT + QCDHT + QCDPtbcToE + QCDPt + QCDPtEMEnriched + [QCD_Mu15] + QCD_Mu5 +  DiBosons + TriBosons + TTV + Higgs + Rares + EWKV2Jets

mcSamples = Top + SingleTop + VJets + DiBosons + TriBosons  + Rares + QCDPtbcToE  + QCDPtEMEnriched + QCD_Mu5 + WNJets + DYNJets

samples = mcSamples

if __name__ == "__main__":
    from CMGTools.RootTools.samples.tools import runMain
    runMain(samples,localobjs=locals())
