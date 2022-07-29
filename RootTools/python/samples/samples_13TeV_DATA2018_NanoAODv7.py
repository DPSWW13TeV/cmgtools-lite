# COMPONENT CREATOR
from CMGTools.RootTools.samples.ComponentCreator import ComponentCreator
kreator = ComponentCreator()

# ----------------------------- 2018 pp run  ----------------------------------------

json = '/afs/cern.ch/cms/CAF/CMSCOMM/COMM_DQM/certification/Collisions18/13TeV/Legacy_2018/Cert_314472-325175_13TeV_Legacy2018_Collisions18_JSON.txt'



SingleMuon_Run2018A_02Apr2020     = kreator.makeDataComponent("SingleMuon_Run2018A_02Apr2020"    , "/SingleMuon/Run2018A-02Apr2020-v1/NANOAOD"    , "CMS", ".*root", json)
SingleMuon_Run2018B_02Apr2020     = kreator.makeDataComponent("SingleMuon_Run2018B_02Apr2020"    , "/SingleMuon/Run2018B-02Apr2020-v1/NANOAOD"    , "CMS", ".*root", json)
SingleMuon_Run2018C_02Apr2020     = kreator.makeDataComponent("SingleMuon_Run2018C_02Apr2020"    , "/SingleMuon/Run2018C-02Apr2020-v1/NANOAOD"    , "CMS", ".*root", json)
SingleMuon_Run2018d_02Apr2020     = kreator.makeDataComponent("SingleMuon_Run2018D_02Apr2020"    , "/SingleMuon/Run2018D-02Apr2020-v1/NANOAOD"    , "CMS", ".*root", json)

MuonEG_Run2018A_02Apr2020      = kreator.makeDataComponent("MuonEG_Run2018A_02Apr2020" , "/MuonEG/Run2018A-02Apr2020-v1/NANOAOD"  , "CMS", ".*root", json)
MuonEG_Run2018B_02Apr2020      = kreator.makeDataComponent("MuonEG_Run2018B_02Apr2020" , "/MuonEG/Run2018B-02Apr2020-v1/NANOAOD"  , "CMS", ".*root", json)
MuonEG_Run2018C_02Apr2020      = kreator.makeDataComponent("MuonEG_Run2018C_02Apr2020" , "/MuonEG/Run2018C-02Apr2020-v1/NANOAOD"  , "CMS", ".*root", json)
MuonEG_Run2018D_02Apr2020      = kreator.makeDataComponent("MuonEG_Run2018D_02Apr2020" , "/MuonEG/Run2018D-02Apr2020-v1/NANOAOD"  , "CMS", ".*root", json)

EGamma_Run2018A_02Apr2020      = kreator.makeDataComponent("EGamma_Run2018A_02Apr2020" , "/EGamma/Run2018A-02Apr2020-v1/NANOAOD"  , "CMS", ".*root", json)
EGamma_Run2018B_02Apr2020      = kreator.makeDataComponent("EGamma_Run2018B_02Apr2020" , "/EGamma/Run2018B-02Apr2020-v1/NANOAOD"  , "CMS", ".*root", json)
EGamma_Run2018C_02Apr2020      = kreator.makeDataComponent("EGamma_Run2018C_02Apr2020" , "/EGamma/Run2018C-02Apr2020-v1/NANOAOD"  , "CMS", ".*root", json)
EGamma_Run2018D_02Apr2020      = kreator.makeDataComponent("EGamma_Run2018D_02Apr2020" , "/EGamma/Run2018D-02Apr2020-v1/NANOAOD"  , "CMS", ".*root", json)

DoubleMuon_Run2018A_02Apr2020      = kreator.makeDataComponent("DoubleMuon_Run2018A_02Apr2020" , "/DoubleMuon/Run2018A-02Apr2020-v1/NANOAOD"  , "CMS", ".*root", json)
DoubleMuon_Run2018B_02Apr2020      = kreator.makeDataComponent("DoubleMuon_Run2018B_02Apr2020" , "/DoubleMuon/Run2018B-02Apr2020-v1/NANOAOD"  , "CMS", ".*root", json)
DoubleMuon_Run2018C_02Apr2020      = kreator.makeDataComponent("DoubleMuon_Run2018C_02Apr2020" , "/DoubleMuon/Run2018C-02Apr2020-v1/NANOAOD"  , "CMS", ".*root", json)
DoubleMuon_Run2018D_02Apr2020      = kreator.makeDataComponent("DoubleMuon_Run2018D_02Apr2020" , "/DoubleMuon/Run2018D-02Apr2020-v1/NANOAOD"  , "CMS", ".*root", json)



dataSamples_02Apr2020 = [SingleMuon_Run2018A_02Apr2020,SingleMuon_Run2018B_02Apr2020,SingleMuon_Run2018C_02Apr2020,SingleMuon_Run2018d_02Apr2020,MuonEG_Run2018A_02Apr2020,MuonEG_Run2018B_02Apr2020,MuonEG_Run2018C_02Apr2020,MuonEG_Run2018D_02Apr2020,EGamma_Run2018A_02Apr2020,EGamma_Run2018B_02Apr2020,EGamma_Run2018C_02Apr2020,EGamma_Run2018D_02Apr2020,DoubleMuon_Run2018A_02Apr2020,DoubleMuon_Run2018B_02Apr2020,DoubleMuon_Run2018C_02Apr2020,DoubleMuon_Run2018D_02Apr2020]

dataSamples = dataSamples_02Apr2020 

samples = dataSamples

### ---------------------------------------------------------------------


if __name__ == "__main__":
    from CMGTools.RootTools.samples.tools import runMain
    runMain(samples, localobjs=locals())
