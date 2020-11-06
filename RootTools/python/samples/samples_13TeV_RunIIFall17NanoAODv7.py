from CMGTools.RootTools.samples.ComponentCreator import ComponentCreator
kreator = ComponentCreator()


TTJets = kreator.makeMCComponent("TTJets", "/TTJets_TuneCP5_13TeV-amcatnloFXFX-pythia8/RunIIFall17NanoAODv7-PU2017_12Apr2018_Nano02Apr2020_new_pmx_102X_mc2017_realistic_v8-v1/NANOAODSIM", "CMS", ".*root", 831.76, fracNegWeights=0.319)
TTJets_DiLepton = kreator.makeMCComponent("TTJets_DiLepton", "/TTJets_DiLept_TuneCP5_13TeV-madgraphMLM-pythia8/RunIIFall17NanoAODv7-PU2017_12Apr2018_Nano02Apr2020_102X_mc2017_realistic_v8-v1/NANOAODSIM", "CMS", ".*root", 831.76*((3*0.108)**2) )

Top = [
TTJets,
TTJets_DiLepton,
]




### V+jets inclusive (from https://twiki.cern.ch/twiki/bin/viewauth/CMS/StandardModelCrossSectionsat13TeV)

WJetsToLNu_LO = kreator.makeMCComponent("WJetsToLNu_LO","/WJetsToLNu_TuneCP5_13TeV-madgraphMLM-pythia8/RunIIFall17NanoAODv7-PU2017_12Apr2018_Nano02Apr2020_102X_mc2017_realistic_v8-v1/NANOAODSIM", "CMS", ".*root", 3* 20508.9)
WJetsToLNu_LO_ext =  kreator.makeMCComponent("WJetsToLNu_LO_ext", "/WJetsToLNu_TuneCP5_13TeV-madgraphMLM-pythia8/RunIIFall17NanoAODv7-PU2017_12Apr2018_Nano02Apr2020_102X_mc2017_realistic_v8_ext1-v1/NANOAODSIM", "CMS", ".*root", 61526.7)



DYJetsToLL_M10to50_LO = kreator.makeMCComponent("DYJetsToLL_M10to50", "/DYJetsToLL_M-10to50_TuneCP5_13TeV-madgraphMLM-pythia8/RunIIFall17NanoAODv7-PU2017_12Apr2018_Nano02Apr2020_102X_mc2017_realistic_v8_ext1-v1/NANOAODSIM", "CMS", ".*root", 15810)

DYJetsToLL_M10to50_LO_newpmx = kreator.makeMCComponent("DYJetsToLL_M10to50_ext", "/DYJetsToLL_M-10to50_TuneCP5_13TeV-madgraphMLM-pythia8/RunIIFall17NanoAODv7-PU2017_12Apr2018_Nano02Apr2020_new_pmx_102X_mc2017_realistic_v8-v1/NANOAODSIM", "CMS", ".*root", 15810)

DYJetsToLL_M50_LO =  kreator.makeMCComponent("DYJetsToLL_M50_LO", "/DYJetsToLL_M-50_TuneCP5_13TeV-madgraphMLM-pythia8/RunIIFall17NanoAODv7-PU2017RECOSIMstep_12Apr2018_Nano02Apr2020_102X_mc2017_realistic_v8-v1/NANOAODSIM", "CMS", ".*root", 1921.8*3)

DYJetsToLL_M50_LO_ext =  kreator.makeMCComponent("DYJetsToLL_M50_LO", "/DYJetsToLL_M-50_TuneCP5_13TeV-madgraphMLM-pythia8/RunIIFall17NanoAODv7-PU2017RECOSIMstep_12Apr2018_Nano02Apr2020_102X_mc2017_realistic_v8_ext1-v1/NANOAODSIM", "CMS", ".*root", 1921.8*3)

DYJetsToLL_M50 =  kreator.makeMCComponent("DYJetsToLL_M50", "/DYJetsToLL_M-50_TuneCP5_13TeV-amcatnloFXFX-pythia8/RunIIFall17NanoAODv7-PU2017_12Apr2018_Nano02Apr2020_102X_mc2017_realistic_v8-v1/NANOAODSIM", "CMS", ".*root", 1921.8*3, fracNegWeights=0.16)
DYJetsToLL_M50_ext = kreator.makeMCComponent("DYJetsToLL_M50_ext", "/DYJetsToLL_M-50_TuneCP5_13TeV-amcatnloFXFX-pythia8/RunIIFall17NanoAODv7-PU2017_12Apr2018_Nano02Apr2020_new_pmx_102X_mc2017_realistic_v8_ext1-v1/NANOAODSIM", 1921.8*3, fracNegWeights=0.16)



VJets = [

WJetsToLNu_LO,
WJetsToLNu_LO_ext,
DYJetsToLL_M10to50_LO,
DYJetsToLL_M10to50_LO_newpmx,
DYJetsToLL_M50_LO,
DYJetsToLL_M50_LO_ext,
DYJetsToLL_M50,
DYJetsToLL_M50_ext,

]






### DiBosons
WWDoubleTo2L           = kreator.makeMCComponent("WWDoubleTo2L", "/WWTo2L2Nu_DoubleScattering_13TeV-pythia8/RunIIFall17NanoAODv7-PU2017_12Apr2018_Nano02Apr2020_102X_mc2017_realistic_v8-v1/NANOAODSIM", "CMS", ".*root", 0.1729)

WWDoubleTo2L_hw           = kreator.makeMCComponent("WWDoubleTo2L_hw", "/WWTo2L2Nu_DoubleScattering_TuneCH3_13TeV-herwig7/RunIIFall17NanoAODv7-PU2017_12Apr2018_Nano02Apr2020_102X_mc2017_realistic_v8-v1/NANOAODSIM", "CMS", ".*root", 0.1729)

WWDouble_cp5           = kreator.makeMCComponent("WWDouble_cp5", "/WW_DoubleScattering_13TeV-pythia8_TuneCP5/RunIIFall17NanoAODv7-PU2017_12Apr2018_Nano02Apr2020_102X_mc2017_realistic_v8-v1/NANOAODSIM", "CMS", ".*root", 0.1729)



WZTo3LNu               = kreator.makeMCComponent("WZTo3LNu", "/WZTo3LNu_13TeV-powheg-pythia8/RunIIFall17NanoAODv7-PU2017_12Apr2018_Nano02Apr2020_102X_mc2017_realistic_v8-v1/NANOAODSIM", "CMS", ".*root", 4.42965)


WZTo3LNu_fxfx          = kreator.makeMCComponent("WZTo3LNu_fxfx", "/WZTo3LNu_TuneCP5_13TeV-amcatnloFXFX-pythia8/RunIIFall17NanoAODv7-PU2017_12Apr2018_Nano02Apr2020_new_pmx_102X_mc2017_realistic_v8-v1/NANOAODSIM", "CMS", ".*root", 4.666, fracNegWeights=0.19)


WZTo3LNu_mllmin01      = kreator.makeMCComponent("WZTo3LNu_mllmin01", "/WZTo3LNu_mllmin01_NNPDF31_TuneCP5_13TeV_powheg_pythia8/RunIIFall17NanoAODv7-PU2017_12Apr2018_Nano02Apr2020_102X_mc2017_realistic_v8-v1/NANOAODSIM", "CMS", ".*root", 58.59*0.601644)


WWTo2L2Nu              = kreator.makeMCComponent("WWTo2L2Nu", "/WWTo2L2Nu_NNPDF31_TuneCP5_13TeV-powheg-pythia8/RunIIFall17NanoAODv7-PU2017_12Apr2018_Nano02Apr2020_102X_mc2017_realistic_v8-v1/NANOAODSIM", "CMS", ".*root", 10.481)
ZZTo4L                 = kreator.makeMCComponent("ZZTo4L", "/ZZTo4L_13TeV_powheg_pythia8/RunIIFall17NanoAODv7-PU2017_12Apr2018_Nano02Apr2020_102X_mc2017_realistic_v8-v1/NANOAODSIM", "CMS", ".*root", 1.256)
WpWpJJ                 = kreator.makeMCComponent("WpWpJJ", "/WpWpJJ_EWK-QCD_TuneCP5_13TeV-madgraph-pythia8/RunIIFall17NanoAODv7-PU2017_12Apr2018_Nano02Apr2020_102X_mc2017_realistic_v8-v1/NANOAODSIM", "CMS", ".*root", 0.03711)

ZGTo2LG                = kreator.makeMCComponent("ZGTo2LG", "/ZGToLLG_01J_5f_TuneCP5_13TeV-amcatnloFXFX-pythia8/RunIIFall17NanoAODv7-PU2017_12Apr2018_Nano02Apr2020_102X_mc2017_realistic_v8-v1/NANOAODSIM", "CMS", ".*root", 131.3, fracNegWeights=0.16)

WGToLNuG               = kreator.makeMCComponent("WGToLNuG", "/WGToLNuG_TuneCP5_13TeV-madgraphMLM-pythia8/RunIIFall17NanoAODv7-PU2017_12Apr2018_Nano02Apr2020_102X_mc2017_realistic_v8-v1/NANOAODSIM", "CMS", ".*root", 585.8)
WGToLNuG_amcatnlo    = kreator.makeMCComponent("WGToLNuG_amcatnlo", "/WGToLNuG_01J_5f_TuneCP5_13TeV-amcatnloFXFX-pythia8/RunIIFall17NanoAODv7-PU2017_12Apr2018_Nano02Apr2020_102X_mc2017_realistic_v8-v1/NANOAODSIM", "CMS", ".*root", 511.2, fracNegWeights=0.18) 





DiBosons = [
WWDoubleTo2L,
WZTo3LNu,
WZTo3LNu_fxfx,
WZTo3LNu_mllmin01,
WWTo2L2Nu,              
ZZTo4L,                 
WpWpJJ,
ZGTo2LG,
WGToLNuG,
WGToLNuG_amcatnlo,
]


### TriBosons
# cross section from https://twiki.cern.ch/twiki/bin/view/CMS/SummaryTable1G25ns#Triboson

WWW = kreator.makeMCComponent("WWW", "/WWW_4F_TuneCP5_13TeV-amcatnlo-pythia8/RunIIFall17NanoAODv7-PU2017_12Apr2018_Nano02Apr2020_102X_mc2017_realistic_v8-v1/NANOAODSIM", "CMS", ".*root", 0.2086, fracNegWeights=0.053)

WWZ = kreator.makeMCComponent("WWZ", "/WWZ_4F_TuneCP5_13TeV-amcatnlo-pythia8/RunIIFall17NanoAODv7-PU2017_12Apr2018_Nano02Apr2020_102X_mc2017_realistic_v8-v1/NANOAODSIM", "CMS", ".*root",  0.1651 , fracNegWeights=0.06)
WZZ = kreator.makeMCComponent("WZZ", "/WZZ_TuneCP5_13TeV-amcatnlo-pythia8/RunIIFall17NanoAODv7-PU2017_12Apr2018_Nano02Apr2020_102X_mc2017_realistic_v8-v1/NANOAODSIM", "CMS", ".*root",  0.05565 , fracNegWeights=0.060)
ZZZ = kreator.makeMCComponent("ZZZ", "/ZZZ_TuneCP5_13TeV-amcatnlo-pythia8/RunIIFall17NanoAODv7-PU2017_12Apr2018_Nano02Apr2020_102X_mc2017_realistic_v8-v1/NANOAODSIM", "CMS", ".*root",  0.01398 , fracNegWeights=0.060)

WWW_ll = kreator.makeMCComponent("WWW_ll", "/WWW_4F_DiLeptonFilter_TuneCP5_13TeV-amcatnlo-pythia8/RunIIFall17NanoAODv7-PU2017_12Apr2018_Nano02Apr2020_102X_mc2017_realistic_v8-v1/NANOAODSIM", "CMS", ".*root", 0.007201, fracNegWeights=0.063)  # xs from genXSecAna



TriBosons = [
WWW,
WZZ,
WWZ,
ZZZ,
WWW_ll,
]

### rares


TTW_LO = kreator.makeMCComponent("TTW_LO", "/ttWJets_TuneCP5_13TeV_madgraphMLM_pythia8/RunIIFall17NanoAODv7-PU2017_12Apr2018_Nano02Apr2020_102X_mc2017_realistic_v8-v1/NANOAODSIM", "CMS", ".*root",  0.6105 )
TTZ_LO = kreator.makeMCComponent("TTZ_LO", "/ttZJets_TuneCP5_13TeV_madgraphMLM_pythia8/RunIIFall17NanoAODv7-PU2017_12Apr2018_Nano02Apr2020_102X_mc2017_realistic_v8-v1/NANOAODSIM", "CMS", ".*root",  0.5297/0.692)


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
