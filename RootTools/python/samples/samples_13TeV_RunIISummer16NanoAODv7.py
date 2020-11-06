from CMGTools.RootTools.samples.ComponentCreator import ComponentCreator
kreator = ComponentCreator()


TTJets = kreator.makeMCComponent("TTJets", "/TTJets_TuneCUETP8M2T4_13TeV-amcatnloFXFX-pythia8/RunIISummer16NanoAODv7-PUMoriond17_Nano02Apr2020_102X_mcRun2_asymptotic_v8-v1/NANOAODSIM", "CMS", ".*root", 831.76, fracNegWeights=0.319)

TTJets_DiLepton = kreator.makeMCComponent("TTJets_DiLepton", "/TTJets_DiLept_TuneCUETP8M1_13TeV-madgraphMLM-pythia8/RunIISummer16NanoAODv7-PUMoriond17_Nano02Apr2020_102X_mcRun2_asymptotic_v8-v1/NANOAODSIM"     , "CMS", ".*root", 831.76*((3*0.108)**2) )

TGJets_lep = kreator.makeMCComponent("TGJets_lep", "/TGJets_leptonDecays_13TeV_amcatnlo_madspin_pythia8/RunIISummer16NanoAODv7-PUMoriond17_Nano02Apr2020_102X_mcRun2_asymptotic_v8-v1/NANOAODSIM", "CMS", ".*root", 1.018, fracNegWeights=0.4)




Top = [
TTJets,
TTJets_DiLepton,
TGJets_lep,
]




### V+jets inclusive (from https://twiki.cern.ch/twiki/bin/viewauth/CMS/StandardModelCrossSectionsat13TeV)
WJetsToLNu_ext = kreator.makeMCComponent("WJetsToLNu","/WJetsToLNu_TuneCUETP8M1_13TeV-amcatnloFXFX-pythia8/RunIISummer16NanoAODv7-PUMoriond17_Nano02Apr2020_102X_mcRun2_asymptotic_v8_ext2-v1/NANOAODSIM", "CMS", ".*root", 3* 20508.9, fracNegWeights=0.16)
WJetsToLNu = kreator.makeMCComponent("WJetsToLNu_ext","/WJetsToLNu_TuneCUETP8M1_13TeV-amcatnloFXFX-pythia8/RunIISummer16NanoAODv7-PUMoriond17_Nano02Apr2020_102X_mcRun2_asymptotic_v8-v1/NANOAODSIM", "CMS", ".*root", 3* 20508.9, fracNegWeights=0.16)
WJetsToLNu_LO = kreator.makeMCComponent("WJetsToLNu_LO","/WJetsToLNu_TuneCUETP8M1_13TeV-madgraphMLM-pythia8/RunIISummer16NanoAODv7-PUMoriond17_Nano02Apr2020_102X_mcRun2_asymptotic_v8-v1/NANOAODSIM", "CMS", ".*root", 3* 20508.9)
WJetsToLNu_LO_ext =  kreator.makeMCComponent("WJetsToLNu_LO_ext", "/WJetsToLNu_TuneCUETP8M1_13TeV-madgraphMLM-pythia8/RunIISummer16NanoAODv7-PUMoriond17_Nano02Apr2020_102X_mcRun2_asymptotic_v8_ext2-v1/NANOAODSIM", "CMS", ".*root", 61526.7)


DYJetsToLL_M10to50 = kreator.makeMCComponent("DYJetsToLL_M10to50", "/DYJetsToLL_M-10to50_TuneCUETP8M1_13TeV-amcatnloFXFX-pythia8/RunIISummer16NanoAODv7-PUMoriond17_Nano02Apr2020_102X_mcRun2_asymptotic_v8_ext1-v1/NANOAODSIM", "CMS", ".*root", 18610, fracNegWeights=0.135)

DYJetsToLL_M10to50_ext = kreator.makeMCComponent("DYJetsToLL_M10to50_ext", "/DYJetsToLL_M-10to50_TuneCUETP8M1_13TeV-amcatnloFXFX-pythia8/RunIISummer16NanoAODv7-PUMoriond17_Nano02Apr2020_102X_mcRun2_asymptotic_v8_ext1-v1/NANOAODSIM", "CMS", ".*root", 18610, fracNegWeights=0.135)

DYJetsToLL_M10to50_LO = kreator.makeMCComponent("DYJetsToLL_M10to50_LO", "/DYJetsToLL_M-10to50_TuneCUETP8M1_13TeV-madgraphMLM-pythia8/RunIISummer16NanoAODv7-PUMoriond17_Nano02Apr2020_102X_mcRun2_asymptotic_v8-v1/NANOAODSIM", "CMS", ".*root", 18610)

DYJetsToLL_M50 = kreator.makeMCComponent("DYJetsToLL_M50", "/DYJetsToLL_M-50_TuneCUETP8M1_13TeV-amcatnloFXFX-pythia8/RunIISummer16NanoAODv7-PUMoriond17_Nano02Apr2020_102X_mcRun2_asymptotic_v8_ext2-v1/NANOAODSIM", "CMS", ".*root", 2008.*3, fracNegWeights=0.16)
DYJetsToLL_M50_LO =  kreator.makeMCComponent("DYJetsToLL_M50_LO", "/DYJetsToLL_M-50_TuneCUETP8M1_13TeV-madgraphMLM-pythia8/RunIISummer16NanoAODv7-PUMoriond17_Nano02Apr2020_102X_mcRun2_asymptotic_v8_ext1-v1/NANOAODSIM", "CMS", ".*root", 2008.*3)
DYJetsToLL_M50_LO_ext =  kreator.makeMCComponent("DYJetsToLL_M50_LO_ext", "/DYJetsToLL_M-50_TuneCUETP8M1_13TeV-madgraphMLM-pythia8/RunIISummer16NanoAODv7-PUMoriond17_Nano02Apr2020_102X_mcRun2_asymptotic_v8_ext2-v1/NANOAODSIM", "CMS", ".*root", 2008.*3)


VJets = [
WJetsToLNu,
WJetsToLNu_ext,
WJetsToLNu_LO,
WJetsToLNu_LO_ext,
DYJetsToLL_M10to50,
DYJetsToLL_M10to50_ext,
DYJetsToLL_M10to50_LO,
DYJetsToLL_M50,
DYJetsToLL_M50_LO,
DYJetsToLL_M50_LO_ext,
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



### ----------------------------- summary ----------------------------------------

#mcSamples = TTs + SingleTop + VJets + DYJetsM50HT + DYJetsM5to50HT + DYNJets + WJetsToLNuHT + WJetsToLNuPT + WNJets + GJetsHT + ZJetsToNuNuHT + QCDHT + QCDPtbcToE + QCDPt + QCDPtEMEnriched + [QCD_Mu15] + QCD_Mu5 +  DiBosons + TriBosons + TTV + Higgs + Rares + EWKV2Jets

mcSamples = Top + VJets + DiBosons + TriBosons  + Rares 

samples = mcSamples

if __name__ == "__main__":
    from CMGTools.RootTools.samples.tools import runMain
    runMain(samples,localobjs=locals())
