from CMGTools.RootTools.samples.ComponentCreator import ComponentCreator
kreator = ComponentCreator()

json='/afs/cern.ch/cms/CAF/CMSCOMM/COMM_DQM/certification/Collisions17/13TeV/Legacy_2017/Cert_294927-306462_13TeV_UL2017_Collisions17_GoldenJSON.txt'

### ----------------------------- Run2017B 02Apr2020 ----------------------------------------



SingleElectron_Run2017B_02Apr2020 = kreator.makeDataComponent("SingleElectron_Run2017B_02Apr2020", "/SingleElectron/Run2017B-02Apr2020-v1/NANOAOD", "CMS", ".*root", json)
SingleMuon_Run2017B_02Apr2020     = kreator.makeDataComponent("SingleMuon_Run2017B_02Apr2020"    , "/SingleMuon/Run2017B-02Apr2020-v1/NANOAOD"    , "CMS", ".*root", json)
DoubleEG_Run2017B_02Apr2020       = kreator.makeDataComponent("DoubleEG_Run2017B_02Apr2020"    , "/DoubleEG/Run2017B-02Apr2020-v1/NANOAOD"    , "CMS", ".*root", json)
DoubleMuon_Run2017B_02Apr2020     = kreator.makeDataComponent("DoubleMuon_Run2017B_02Apr2020"    , "/DoubleMuon/Run2017B-02Apr2020-v1/NANOAOD"    , "CMS", ".*root", json)
MuonEG_Run2017B_02Apr2020         = kreator.makeDataComponent("MuonEG_Run2017B_02Apr2020"    , "/MuonEG/Run2017B-02Apr2020-v1/NANOAOD"    , "CMS", ".*root", json)




dataSamples_Run2017B_02Apr2020 = [SingleElectron_Run2017B_02Apr2020,SingleMuon_Run2017B_02Apr2020,DoubleEG_Run2017B_02Apr2020,DoubleMuon_Run2017B_02Apr2020,MuonEG_Run2017B_02Apr2020]


### ----------------------------- Run2017C 02Apr2020 ----------------------------------------

SingleElectron_Run2017C_02Apr2020 = kreator.makeDataComponent("SingleElectron_Run2017C_02Apr2020", "/SingleElectron/Run2017C-02Apr2020-v1/NANOAOD", "CMS", ".*root", json)
SingleMuon_Run2017C_02Apr2020     = kreator.makeDataComponent("SingleMuon_Run2017C_02Apr2020"    , "/SingleMuon/Run2017C-02Apr2020-v1/NANOAOD"    , "CMS", ".*root", json)
DoubleEG_Run2017C_02Apr2020     = kreator.makeDataComponent("DoubleEG_Run2017C_02Apr2020"    , "/DoubleEG/Run2017C-02Apr2020-v1/NANOAOD"    , "CMS", ".*root", json)
DoubleMuon_Run2017C_02Apr2020     = kreator.makeDataComponent("DoubleMuon_Run2017C_02Apr2020"    , "/DoubleMuon/Run2017C-02Apr2020-v1/NANOAOD"    , "CMS", ".*root", json)
MuonEG_Run2017C_02Apr2020     = kreator.makeDataComponent("MuonEG_Run2017C_02Apr2020"    , "/MuonEG/Run2017C-02Apr2020-v1/NANOAOD"    , "CMS", ".*root", json)

dataSamples_Run2017C_02Apr2020 = [SingleElectron_Run2017C_02Apr2020,SingleMuon_Run2017C_02Apr2020,DoubleEG_Run2017C_02Apr2020,DoubleMuon_Run2017C_02Apr2020,MuonEG_Run2017C_02Apr2020]


### ----------------------------- Run2017D 02Apr2020 ----------------------------------------

SingleElectron_Run2017D_02Apr2020 = kreator.makeDataComponent("SingleElectron_Run2017D_02Apr2020", "/SingleElectron/Run2017D-02Apr2020-v1/NANOAOD", "CMS", ".*root", json)
SingleMuon_Run2017D_02Apr2020     = kreator.makeDataComponent("SingleMuon_Run2017D_02Apr2020"    , "/SingleMuon/Run2017D-02Apr2020-v1/NANOAOD"    , "CMS", ".*root", json)
DoubleEG_Run2017D_02Apr2020     = kreator.makeDataComponent("DoubleEG_Run2017D_02Apr2020"    , "/DoubleEG/Run2017D-02Apr2020-v1/NANOAOD"    , "CMS", ".*root", json)
DoubleMuon_Run2017D_02Apr2020     = kreator.makeDataComponent("DoubleMuon_Run2017D_02Apr2020"    , "/DoubleMuon/Run2017D-02Apr2020-v1/NANOAOD"    , "CMS", ".*root", json)
MuonEG_Run2017D_02Apr2020     = kreator.makeDataComponent("MuonEG_Run2017D_02Apr2020"    , "/MuonEG/Run2017D-02Apr2020-v1/NANOAOD"    , "CMS", ".*root", json)

dataSamples_Run2017D_02Apr2020 = [SingleElectron_Run2017D_02Apr2020,SingleMuon_Run2017D_02Apr2020,DoubleEG_Run2017D_02Apr2020,DoubleMuon_Run2017D_02Apr2020,MuonEG_Run2017D_02Apr2020]

### ----------------------------- Run2017D 02Apr2020  ----------------------------------------

SingleElectron_Run2017E_02Apr2020 = kreator.makeDataComponent("SingleElectron_Run2017E_02Apr2020", "/SingleElectron/Run2017E-02Apr2020-v1/NANOAOD", "CMS", ".*root", json)
SingleMuon_Run2017E_02Apr2020     = kreator.makeDataComponent("SingleMuon_Run2017E_02Apr2020"    , "/SingleMuon/Run2017E-02Apr2020-v1/NANOAOD"    , "CMS", ".*root", json)
DoubleEG_Run2017E_02Apr2020     = kreator.makeDataComponent("DoubleEG_Run2017E_02Apr2020"    , "/DoubleEG/Run2017E-02Apr2020-v1/NANOAOD"    , "CMS", ".*root", json)
DoubleMuon_Run2017E_02Apr2020     = kreator.makeDataComponent("DoubleMuon_Run2017E_02Apr2020"    , "/DoubleMuon/Run2017E-02Apr2020-v1/NANOAOD"    , "CMS", ".*root", json)
MuonEG_Run2017E_02Apr2020     = kreator.makeDataComponent("MuonEG_Run2017E_02Apr2020"    , "/MuonEG/Run2017E-02Apr2020-v1/NANOAOD"    , "CMS", ".*root", json)

dataSamples_Run2017E_02Apr2020 = [SingleElectron_Run2017E_02Apr2020,SingleMuon_Run2017E_02Apr2020,DoubleEG_Run2017E_02Apr2020,DoubleMuon_Run2017E_02Apr2020,MuonEG_Run2017E_02Apr2020]
### ----------------------------- Run2017D 02Apr2020 ----------------------------------------

SingleElectron_Run2017F_02Apr2020 = kreator.makeDataComponent("SingleElectron_Run2017F_02Apr2020", "/SingleElectron/Run2017F-02Apr2020-v1/NANOAOD", "CMS", ".*root", json)
SingleMuon_Run2017F_02Apr2020     = kreator.makeDataComponent("SingleMuon_Run2017F_02Apr2020"    , "/SingleMuon/Run2017F-02Apr2020-v1/NANOAOD"    , "CMS", ".*root", json)
DoubleEG_Run2017F_02Apr2020     = kreator.makeDataComponent("DoubleEG_Run2017F_02Apr2020"    , "/DoubleEG/Run2017F-02Apr2020-v1/NANOAOD"    , "CMS", ".*root", json)
DoubleMuon_Run2017F_02Apr2020     = kreator.makeDataComponent("DoubleMuon_Run2017F_02Apr2020"    , "/DoubleMuon/Run2017F-02Apr2020-v1/NANOAOD"    , "CMS", ".*root", json)
MuonEG_Run2017F_02Apr2020     = kreator.makeDataComponent("MuonEG_Run2017F_02Apr2020"    , "/MuonEG/Run2017F-02Apr2020-v1/NANOAOD"    , "CMS", ".*root", json)

dataSamples_Run2017F_02Apr2020 = [SingleElectron_Run2017F_02Apr2020,SingleMuon_Run2017F_02Apr2020,DoubleEG_Run2017F_02Apr2020,DoubleMuon_Run2017F_02Apr2020,MuonEG_Run2017F_02Apr2020]



dataSamples_02Apr2020 = dataSamples_Run2017B_02Apr2020  + dataSamples_Run2017C_02Apr2020 + dataSamples_Run2017D_02Apr2020 + dataSamples_Run2017E_02Apr2020 + dataSamples_Run2017F_02Apr2020 

dataSamples = dataSamples_02Apr2020 

samples = dataSamples

### ---------------------------------------------------------------------


if __name__ == "__main__":
    from CMGTools.RootTools.samples.tools import runMain
    runMain(samples, localobjs=locals())
