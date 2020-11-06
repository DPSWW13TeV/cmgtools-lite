from CMGTools.RootTools.samples.ComponentCreator import ComponentCreator
kreator = ComponentCreator()

json='/afs/cern.ch/cms/CAF/CMSCOMM/COMM_DQM/certification/Collisions16/13TeV/ReReco/Final/Cert_271036-284044_13TeV_ReReco_07Aug2017_Collisions16_JSON.txt'

### ----------------------------- Run2016B 02Apr2020 ----------------------------------------



SingleElectron_Run2016B_02Apr2020 = kreator.makeDataComponent("SingleElectron_Run2016B_02Apr2020", "/SingleElectron/Run2016B-02Apr2020_ver2-v1/NANOAOD", "CMS", ".*root", json)
SingleMuon_Run2016B_02Apr2020     = kreator.makeDataComponent("SingleMuon_Run2016B_02Apr2020"    , "/SingleMuon/Run2016B-02Apr2020_ver2-v1/NANOAOD"    , "CMS", ".*root", json)
DoubleEG_Run2016B_02Apr2020     = kreator.makeDataComponent("DoubleEG_Run2016B_02Apr2020"    , "/DoubleEG/Run2016B-02Apr2020_ver2-v1/NANOAOD"    , "CMS", ".*root", json)
DoubleMuon_Run2016B_02Apr2020     = kreator.makeDataComponent("DoubleMuon_Run2016B_02Apr2020"    , "/DoubleMuon/Run2016B-02Apr2020_ver2-v1/NANOAOD"    , "CMS", ".*root", json)
MuonEG_Run2016B_02Apr2020     = kreator.makeDataComponent("MuonEG_Run2016B_02Apr2020"    , "/MuonEG/Run2016B-02Apr2020_ver2-v1/NANOAOD"    , "CMS", ".*root", json)




dataSamples_Run2016B_02Apr2020 = [SingleElectron_Run2016B_02Apr2020,SingleMuon_Run2016B_02Apr2020,DoubleEG_Run2016B_02Apr2020,DoubleMuon_Run2016B_02Apr2020,MuonEG_Run2016B_02Apr2020]


### ----------------------------- Run2016C 02Apr2020 ----------------------------------------

SingleElectron_Run2016C_02Apr2020 = kreator.makeDataComponent("SingleElectron_Run2016C_02Apr2020", "/SingleElectron/Run2016C-02Apr2020-v1/NANOAOD", "CMS", ".*root", json)
SingleMuon_Run2016C_02Apr2020     = kreator.makeDataComponent("SingleMuon_Run2016C_02Apr2020"    , "/SingleMuon/Run2016C-02Apr2020-v1/NANOAOD"    , "CMS", ".*root", json)
DoubleEG_Run2016C_02Apr2020     = kreator.makeDataComponent("DoubleEG_Run2016C_02Apr2020"    , "/DoubleEG/Run2016C-02Apr2020-v1/NANOAOD"    , "CMS", ".*root", json)
DoubleMuon_Run2016C_02Apr2020     = kreator.makeDataComponent("DoubleMuon_Run2016C_02Apr2020"    , "/DoubleMuon/Run2016C-02Apr2020-v1/NANOAOD"    , "CMS", ".*root", json)
MuonEG_Run2016C_02Apr2020     = kreator.makeDataComponent("MuonEG_Run2016C_02Apr2020"    , "/MuonEG/Run2016C-02Apr2020-v1/NANOAOD"    , "CMS", ".*root", json)

dataSamples_Run2016C_02Apr2020 = [SingleElectron_Run2016C_02Apr2020,SingleMuon_Run2016C_02Apr2020,DoubleEG_Run2016C_02Apr2020,DoubleMuon_Run2016C_02Apr2020,MuonEG_Run2016C_02Apr2020]


### ----------------------------- Run2016D 02Apr2020 v2 ----------------------------------------

SingleElectron_Run2016D_02Apr2020 = kreator.makeDataComponent("SingleElectron_Run2016D_02Apr2020", "/SingleElectron/Run2016D-02Apr2020-v1/NANOAOD", "CMS", ".*root", json)
SingleMuon_Run2016D_02Apr2020     = kreator.makeDataComponent("SingleMuon_Run2016D_02Apr2020"    , "/SingleMuon/Run2016D-02Apr2020-v1/NANOAOD"    , "CMS", ".*root", json)
DoubleEG_Run2016D_02Apr2020     = kreator.makeDataComponent("DoubleEG_Run2016D_02Apr2020"    , "/DoubleEG/Run2016D-02Apr2020-v1/NANOAOD"    , "CMS", ".*root", json)
DoubleMuon_Run2016D_02Apr2020     = kreator.makeDataComponent("DoubleMuon_Run2016D_02Apr2020"    , "/DoubleMuon/Run2016D-02Apr2020-v1/NANOAOD"    , "CMS", ".*root", json)
MuonEG_Run2016D_02Apr2020     = kreator.makeDataComponent("MuonEG_Run2016D_02Apr2020"    , "/MuonEG/Run2016D-02Apr2020-v1/NANOAOD"    , "CMS", ".*root", json)

dataSamples_Run2016D_02Apr2020 = [SingleElectron_Run2016D_02Apr2020,SingleMuon_Run2016D_02Apr2020,DoubleEG_Run2016D_02Apr2020,DoubleMuon_Run2016D_02Apr2020,MuonEG_Run2016D_02Apr2020]

### ----------------------------- Run2016D 02Apr2020 v2 ----------------------------------------

SingleElectron_Run2016E_02Apr2020 = kreator.makeDataComponent("SingleElectron_Run2016E_02Apr2020", "/SingleElectron/Run2016E-02Apr2020-v1/NANOAOD", "CMS", ".*root", json)
SingleMuon_Run2016E_02Apr2020     = kreator.makeDataComponent("SingleMuon_Run2016E_02Apr2020"    , "/SingleMuon/Run2016E-02Apr2020-v1/NANOAOD"    , "CMS", ".*root", json)
DoubleEG_Run2016E_02Apr2020     = kreator.makeDataComponent("DoubleEG_Run2016E_02Apr2020"    , "/DoubleEG/Run2016E-02Apr2020-v1/NANOAOD"    , "CMS", ".*root", json)
DoubleMuon_Run2016E_02Apr2020     = kreator.makeDataComponent("DoubleMuon_Run2016E_02Apr2020"    , "/DoubleMuon/Run2016E-02Apr2020-v1/NANOAOD"    , "CMS", ".*root", json)
MuonEG_Run2016E_02Apr2020     = kreator.makeDataComponent("MuonEG_Run2016E_02Apr2020"    , "/MuonEG/Run2016E-02Apr2020-v2/NANOAOD"    , "CMS", ".*root", json)

dataSamples_Run2016E_02Apr2020 = [SingleElectron_Run2016E_02Apr2020,SingleMuon_Run2016E_02Apr2020,DoubleEG_Run2016E_02Apr2020,DoubleMuon_Run2016E_02Apr2020,MuonEG_Run2016E_02Apr2020]
### ----------------------------- Run2016D 02Apr2020 v2 ----------------------------------------

SingleElectron_Run2016F_02Apr2020 = kreator.makeDataComponent("SingleElectron_Run2016F_02Apr2020", "/SingleElectron/Run2016F-02Apr2020-v1/NANOAOD", "CMS", ".*root", json)
SingleMuon_Run2016F_02Apr2020     = kreator.makeDataComponent("SingleMuon_Run2016F_02Apr2020"    , "/SingleMuon/Run2016F-02Apr2020-v1/NANOAOD"    , "CMS", ".*root", json)
DoubleEG_Run2016F_02Apr2020     = kreator.makeDataComponent("DoubleEG_Run2016F_02Apr2020"    , "/DoubleEG/Run2016F-02Apr2020-v1/NANOAOD"    , "CMS", ".*root", json)
DoubleMuon_Run2016F_02Apr2020     = kreator.makeDataComponent("DoubleMuon_Run2016F_02Apr2020"    , "/DoubleMuon/Run2016F-02Apr2020-v1/NANOAOD"    , "CMS", ".*root", json)
MuonEG_Run2016F_02Apr2020     = kreator.makeDataComponent("MuonEG_Run2016F_02Apr2020"    , "/MuonEG/Run2016F-02Apr2020-v1/NANOAOD"    , "CMS", ".*root", json)

dataSamples_Run2016F_02Apr2020 = [SingleElectron_Run2016F_02Apr2020,SingleMuon_Run2016F_02Apr2020,DoubleEG_Run2016F_02Apr2020,DoubleMuon_Run2016F_02Apr2020,MuonEG_Run2016F_02Apr2020]
### ----------------------------- Run2016D 02Apr2020 v2 ----------------------------------------

SingleElectron_Run2016G_02Apr2020 = kreator.makeDataComponent("SingleElectron_Run2016G_02Apr2020", "/SingleElectron/Run2016G-02Apr2020-v1/NANOAOD", "CMS", ".*root", json)
SingleMuon_Run2016G_02Apr2020     = kreator.makeDataComponent("SingleMuon_Run2016G_02Apr2020"    , "/SingleMuon/Run2016G-02Apr2020-v1/NANOAOD"    , "CMS", ".*root", json)
DoubleEG_Run2016G_02Apr2020     = kreator.makeDataComponent("DoubleEG_Run2016G_02Apr2020"    , "/DoubleEG/Run2016G-02Apr2020-v1/NANOAOD"    , "CMS", ".*root", json)
DoubleMuon_Run2016G_02Apr2020     = kreator.makeDataComponent("DoubleMuon_Run2016G_02Apr2020"    , "/DoubleMuon/Run2016G-02Apr2020-v1/NANOAOD"    , "CMS", ".*root", json)
MuonEG_Run2016G_02Apr2020     = kreator.makeDataComponent("MuonEG_Run2016G_02Apr2020"    , "/MuonEG/Run2016G-02Apr2020-v1/NANOAOD"    , "CMS", ".*root", json)

dataSamples_Run2016G_02Apr2020 = [SingleElectron_Run2016G_02Apr2020,SingleMuon_Run2016G_02Apr2020,DoubleEG_Run2016G_02Apr2020,DoubleMuon_Run2016G_02Apr2020,MuonEG_Run2016G_02Apr2020]

### ----------------------------- Run2016G 02Apr2020 v2 ----------------------------------------

SingleElectron_Run2016H_02Apr2020 = kreator.makeDataComponent("SingleElectron_Run2016H_02Apr2020", "/SingleElectron/Run2016H-02Apr2020-v1/NANOAOD", "CMS", ".*root", json)
SingleMuon_Run2016H_02Apr2020     = kreator.makeDataComponent("SingleMuon_Run2016H_02Apr2020"    , "/SingleMuon/Run2016H-02Apr2020-v1/NANOAOD"    , "CMS", ".*root", json)
DoubleEG_Run2016H_02Apr2020     = kreator.makeDataComponent("DoubleEG_Run2016H_02Apr2020"    , "/DoubleEG/Run2016H-02Apr2020-v1/NANOAOD"    , "CMS", ".*root", json)
DoubleMuon_Run2016H_02Apr2020     = kreator.makeDataComponent("DoubleMuon_Run2016H_02Apr2020"    , "/DoubleMuon/Run2016H-02Apr2020-v1/NANOAOD"    , "CMS", ".*root", json)
MuonEG_Run2016H_02Apr2020     = kreator.makeDataComponent("MuonEG_Run2016H_02Apr2020"    , "/MuonEG/Run2016H-02Apr2020-v1/NANOAOD"    , "CMS", ".*root", json)

dataSamples_Run2016H_02Apr2020 = [SingleElectron_Run2016H_02Apr2020,SingleMuon_Run2016H_02Apr2020,DoubleEG_Run2016H_02Apr2020,DoubleMuon_Run2016H_02Apr2020,MuonEG_Run2016H_02Apr2020]




dataSamples_02Apr2020 = dataSamples_Run2016B_02Apr2020  + dataSamples_Run2016C_02Apr2020 + dataSamples_Run2016D_02Apr2020 + dataSamples_Run2016E_02Apr2020 + dataSamples_Run2016F_02Apr2020 + dataSamples_Run2016G_02Apr2020 + dataSamples_Run2016H_02Apr2020

dataSamples = dataSamples_02Apr2020 

samples = dataSamples

### ---------------------------------------------------------------------


if __name__ == "__main__":
    from CMGTools.RootTools.samples.tools import runMain
    runMain(samples, localobjs=locals())
