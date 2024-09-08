# COMPONENT CREATOR
from CMGTools.RootTools.samples.ComponentCreator import ComponentCreator
kreator = ComponentCreator()

# ----------------------------- 2017 pp run  ----------------------------------------

json = '/afs/cern.ch/cms/CAF/CMSCOMM/COMM_DQM/certification/Collisions17/13TeV/Legacy_2017/Cert_294927-306462_13TeV_UL2017_Collisions17_GoldenJSON.txt'


# ----------------------------- Run2017B UL2017 ----------------------------------------

SingleElectron_Run2017B_UL2017 = kreator.makeDataComponent("SingleElectron_Run2017B_UL2017", "/SingleElectron/Run2017B-UL2017_MiniAODv2_NanoAODv9-v1/NANOAOD", "CMS", ".*root", json)
SingleMuon_Run2017B_UL2017 = kreator.makeDataComponent("SingleMuon_Run2017B_UL2017", "/SingleMuon/Run2017B-UL2017_MiniAODv2_NanoAODv9-v1/NANOAOD", "CMS", ".*root", json)
DoubleEG_Run2017B_UL2017 = kreator.makeDataComponent("DoubleEG_Run2017B_UL2017", "/DoubleEG/Run2017B-UL2017_MiniAODv2_NanoAODv9-v1/NANOAOD", "CMS", ".*root", json)
MuonEG_Run2017B_UL2017 = kreator.makeDataComponent("MuonEG_Run2017B_UL2017", "/MuonEG/Run2017B-UL2017_MiniAODv2_NanoAODv9-v1/NANOAOD", "CMS", ".*root", json)
DoubleMuon_Run2017B_UL2017 = kreator.makeDataComponent("DoubleMuon_Run2017B_UL2017", "/DoubleMuon/Run2017B-UL2017_MiniAODv2_NanoAODv9-v1/NANOAOD", "CMS", ".*root", json)


dataSamples_Run2017B_UL2017 = [SingleElectron_Run2017B_UL2017, SingleMuon_Run2017B_UL2017] #, DoubleEG_Run2017B_UL2017, MuonEG_Run2017B_UL2017, DoubleMuon_Run2017B_UL2017]

# ----------------------------- Run2017C UL2017 ----------------------------------------

SingleElectron_Run2017C_UL2017 = kreator.makeDataComponent("SingleElectron_Run2017C_UL2017", "/SingleElectron/Run2017C-UL2017_MiniAODv2_NanoAODv9-v1/NANOAOD", "CMS", ".*root", json)
SingleMuon_Run2017C_UL2017 = kreator.makeDataComponent("SingleMuon_Run2017C_UL2017", "/SingleMuon/Run2017C-UL2017_MiniAODv2_NanoAODv9-v1/NANOAOD", "CMS", ".*root", json)
DoubleEG_Run2017C_UL2017 = kreator.makeDataComponent("DoubleEG_Run2017C_UL2017", "/DoubleEG/Run2017C-UL2017_MiniAODv2_NanoAODv9-v1/NANOAOD", "CMS", ".*root", json)
MuonEG_Run2017C_UL2017 = kreator.makeDataComponent("MuonEG_Run2017C_UL2017", "/MuonEG/Run2017C-UL2017_MiniAODv2_NanoAODv9-v1/NANOAOD", "CMS", ".*root", json)
DoubleMuon_Run2017C_UL2017 = kreator.makeDataComponent("DoubleMuon_Run2017C_UL2017", "/DoubleMuon/Run2017C-UL2017_MiniAODv2_NanoAODv9-v1/NANOAOD", "CMS", ".*root", json)


dataSamples_Run2017C_UL2017 = [SingleElectron_Run2017C_UL2017, SingleMuon_Run2017C_UL2017] #,DoubleEG_Run2017C_UL2017, MuonEG_Run2017C_UL2017, DoubleMuon_Run2017C_UL2017]


# ----------------------------- Run2017D UL2017 ----------------------------------------

SingleElectron_Run2017D_UL2017 = kreator.makeDataComponent("SingleElectron_Run2017D_UL2017", "/SingleElectron/Run2017D-UL2017_MiniAODv2_NanoAODv9-v1/NANOAOD", "CMS", ".*root", json)
SingleMuon_Run2017D_UL2017 = kreator.makeDataComponent("SingleMuon_Run2017D_UL2017", "/SingleMuon/Run2017D-UL2017_MiniAODv2_NanoAODv9-v1/NANOAOD", "CMS", ".*root", json)
DoubleEG_Run2017D_UL2017 = kreator.makeDataComponent("DoubleEG_Run2017D_UL2017", "/DoubleEG/Run2017D-UL2017_MiniAODv2_NanoAODv9-v1/NANOAOD", "CMS", ".*root", json)
MuonEG_Run2017D_UL2017 = kreator.makeDataComponent("MuonEG_Run2017D_UL2017", "/MuonEG/Run2017D-UL2017_MiniAODv2_NanoAODv9-v1/NANOAOD", "CMS", ".*root", json)
DoubleMuon_Run2017D_UL2017 = kreator.makeDataComponent("DoubleMuon_Run2017D_UL2017", "/DoubleMuon/Run2017D-UL2017_MiniAODv2_NanoAODv9-v1/NANOAOD", "CMS", ".*root", json)

dataSamples_Run2017D_UL2017 = [ SingleElectron_Run2017D_UL2017, SingleMuon_Run2017D_UL2017] #,DoubleEG_Run2017D_UL2017, MuonEG_Run2017D_UL2017, DoubleMuon_Run2017D_UL2017]

# ----------------------------- Run2017E UL2017 ----------------------------------------


SingleElectron_Run2017E_UL2017 = kreator.makeDataComponent("SingleElectron_Run2017E_UL2017", "/SingleElectron/Run2017E-UL2017_MiniAODv2_NanoAODv9-v1/NANOAOD", "CMS", ".*root", json)
SingleMuon_Run2017E_UL2017 = kreator.makeDataComponent("SingleMuon_Run2017E_UL2017", "/SingleMuon/Run2017E-UL2017_MiniAODv2_NanoAODv9-v1/NANOAOD", "CMS", ".*root", json)
DoubleEG_Run2017E_UL2017 = kreator.makeDataComponent("DoubleEG_Run2017E_UL2017", "/DoubleEG/Run2017E-UL2017_MiniAODv2_NanoAODv9-v1/NANOAOD", "CMS", ".*root", json)
MuonEG_Run2017E_UL2017 = kreator.makeDataComponent("MuonEG_Run2017E_UL2017", "/MuonEG/Run2017E-UL2017_MiniAODv2_NanoAODv9-v1/NANOAOD", "CMS", ".*root", json)
DoubleMuon_Run2017E_UL2017 = kreator.makeDataComponent("DoubleMuon_Run2017E_UL2017", "/DoubleMuon/Run2017E-UL2017_MiniAODv2_NanoAODv9-v1/NANOAOD", "CMS", ".*root", json)

dataSamples_Run2017E_UL2017 = [SingleElectron_Run2017E_UL2017, SingleMuon_Run2017E_UL2017] #,DoubleEG_Run2017E_UL2017, MuonEG_Run2017E_UL2017, DoubleMuon_Run2017E_UL2017]


# ----------------------------- Run2017F UL2017 ----------------------------------------

SingleElectron_Run2017F_UL2017 = kreator.makeDataComponent("SingleElectron_Run2017F_UL2017", "/SingleElectron/Run2017F-UL2017_MiniAODv2_NanoAODv9-v1/NANOAOD", "CMS", ".*root", json)
SingleMuon_Run2017F_UL2017 = kreator.makeDataComponent("SingleMuon_Run2017F_UL2017", "/SingleMuon/Run2017F-UL2017_MiniAODv2_NanoAODv9-v1/NANOAOD", "CMS", ".*root", json)
DoubleEG_Run2017F_UL2017 = kreator.makeDataComponent("DoubleEG_Run2017F_UL2017", "/DoubleEG/Run2017F-UL2017_MiniAODv2_NanoAODv9-v1/NANOAOD", "CMS", ".*root", json)
MuonEG_Run2017F_UL2017 = kreator.makeDataComponent("MuonEG_Run2017F_UL2017", "/MuonEG/Run2017F-UL2017_MiniAODv2_NanoAODv9-v1/NANOAOD", "CMS", ".*root", json)
DoubleMuon_Run2017F_UL2017 = kreator.makeDataComponent("DoubleMuon_Run2017F_UL2017", "/DoubleMuon/Run2017F-UL2017_MiniAODv2_NanoAODv9-v1/NANOAOD", "CMS", ".*root", json)


dataSamples_Run2017F_UL2017 = [SingleElectron_Run2017F_UL2017, SingleMuon_Run2017F_UL2017] #, DoubleEG_Run2017F_UL2017, MuonEG_Run2017F_UL2017, DoubleMuon_Run2017F_UL2017]

dataSamples_UL2017 = dataSamples_Run2017B_UL2017 + dataSamples_Run2017C_UL2017 + dataSamples_Run2017D_UL2017 + dataSamples_Run2017E_UL2017 + dataSamples_Run2017F_UL2017


dataSamples =  dataSamples_UL2017
samples = dataSamples

# ---------------------------------------------------------------------

if __name__ == "__main__":
    from CMGTools.RootTools.samples.tools import runMain
    runMain(samples, localobjs=locals())
