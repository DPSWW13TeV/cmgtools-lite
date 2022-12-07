# COMPONENT CREATOR
from CMGTools.RootTools.samples.ComponentCreator import ComponentCreator
kreator = ComponentCreator()

# ----------------------------- 2018 pp run  ----------------------------------------

json = '/afs/cern.ch/cms/CAF/CMSCOMM/COMM_DQM/certification/Collisions18/13TeV/Legacy_2018/Cert_314472-325175_13TeV_Legacy2018_Collisions18_JSON.txt'
#/work/sesanche/FRs/CMSSW_10_4_0/src/CMGTools/TTHAnalysis/data/Cert_314472-325175_13TeV_17SeptEarlyReReco2018ABC_PromptEraD_Collisions18_JSON.txt'



# ----------------------------- Run2018A UL2018 NanoAODv9 ----------------------------------------
EGamma_Run2018A_UL18 = kreator.makeDataComponent("EGamma_Run2018A_UL18", "/EGamma/Run2018A-UL2018_MiniAODv2_NanoAODv9-v1/NANOAOD", "CMS", ".*root", json)
SingleMuon_Run2018A_UL18 = kreator.makeDataComponent("SingleMuon_Run2018A_UL18", "/SingleMuon/Run2018A-UL2018_MiniAODv2_NanoAODv9-v2/NANOAOD", "CMS", ".*root", json)
DoubleMuon_Run2018A_UL18 = kreator.makeDataComponent("DoubleMuon_Run2018A_UL18", "/DoubleMuon/Run2018A-UL2018_MiniAODv2_NanoAODv9-v1/NANOAOD", "CMS", ".*root", json)
MuonEG_Run2018A_UL18 = kreator.makeDataComponent("MuonEG_Run2018A_UL18", "/MuonEG/Run2018A-UL2018_MiniAODv2_NanoAODv9-v1/NANOAOD", "CMS", ".*root", json)


dataSamples_Run2018A_UL18 = [EGamma_Run2018A_UL18, SingleMuon_Run2018A_UL18, DoubleMuon_Run2018A_UL18, MuonEG_Run2018A_UL18]
#, MET_Run2018A_UL18, JetHT_Run2018A_UL18, Tau_Run2018A_UL18] 

# ----------------------------- Run2018B UL2018 NanoAODv9 ----------------------------------------

EGamma_Run2018B_UL18 = kreator.makeDataComponent("EGamma_Run2018B_UL18", "/EGamma/Run2018B-UL2018_MiniAODv2_NanoAODv9-v1/NANOAOD", "CMS", ".*root", json)
SingleMuon_Run2018B_UL18 = kreator.makeDataComponent("SingleMuon_Run2018B_UL18", "/SingleMuon/Run2018B-UL2018_MiniAODv2_NanoAODv9-v2/NANOAOD", "CMS", ".*root", json)
DoubleMuon_Run2018B_UL18 = kreator.makeDataComponent("DoubleMuon_Run2018B_UL18", "/DoubleMuon/Run2018B-UL2018_MiniAODv2_NanoAODv9-v1/NANOAOD", "CMS", ".*root", json)
MuonEG_Run2018B_UL18 = kreator.makeDataComponent("MuonEG_Run2018B_UL18", "/MuonEG/Run2018B-UL2018_MiniAODv2_NanoAODv9-v1/NANOAOD", "CMS", ".*root", json)
dataSamples_Run2018B_UL18 = [EGamma_Run2018B_UL18, SingleMuon_Run2018B_UL18, DoubleMuon_Run2018B_UL18, MuonEG_Run2018B_UL18]
#, MET_Run2018B_UL18, Tau_Run2018B_UL18, JetHT_Run2018B_UL18]

# ----------------------------- Run2018C UL2018 NanoAODv9 ----------------------------------------

EGamma_Run2018C_UL18 = kreator.makeDataComponent("EGamma_Run2018C_UL18", "/EGamma/Run2018C-UL2018_MiniAODv2_NanoAODv9-v1/NANOAOD", "CMS", ".*root", json)
SingleMuon_Run2018C_UL18 = kreator.makeDataComponent("SingleMuon_Run2018C_UL18", "/SingleMuon/Run2018C-UL2018_MiniAODv2_NanoAODv9-v2/NANOAOD", "CMS", ".*root", json)
DoubleMuon_Run2018C_UL18 = kreator.makeDataComponent("DoubleMuon_Run2018C_UL18", "/DoubleMuon/Run2018C-UL2018_MiniAODv2_NanoAODv9-v1/NANOAOD", "CMS", ".*root", json)
MuonEG_Run2018C_UL18 = kreator.makeDataComponent("MuonEG_Run2018C_UL18", "/MuonEG/Run2018C-UL2018_MiniAODv2_NanoAODv9-v1/NANOAOD", "CMS", ".*root", json)


dataSamples_Run2018C_UL18 = [EGamma_Run2018C_UL18, DoubleMuon_Run2018C_UL18, MuonEG_Run2018C_UL18, SingleMuon_Run2018C_UL18]
# , MET_Run2018C_UL18, Tau_Run2018C_UL18,  JetHT_Run2018C_UL18]

# ----------------------------- Run2018D UL2018 NanoAODv9  ----------------------------------------
EGamma_Run2018D_UL18 = kreator.makeDataComponent("EGamma_Run2018D_UL18", "/EGamma/Run2018D-UL2018_MiniAODv2_NanoAODv9-v3/NANOAOD", "CMS", ".*root", json) 
SingleMuon_Run2018D_UL18 = kreator.makeDataComponent("SingleMuon_Run2018D_UL18", "/SingleMuon/Run2018D-UL2018_MiniAODv2_NanoAODv9-v1/NANOAOD", "CMS", ".*root", json)
DoubleMuon_Run2018D_UL18 = kreator.makeDataComponent("DoubleMuon_Run2018D_UL18", "/DoubleMuon/Run2018D-UL2018_MiniAODv2_NanoAODv9-v2/NANOAOD", "CMS", ".*root", json)
MuonEG_Run2018D_UL18 = kreator.makeDataComponent("MuonEG_Run2018D_UL18", "/MuonEG/Run2018D-UL2018_MiniAODv2_NanoAODv9-v1/NANOAOD", "CMS", ".*root", json)

dataSamples_Run2018D_UL18 = [SingleMuon_Run2018D_UL18, DoubleMuon_Run2018D_UL18, MuonEG_Run2018D_UL18, EGamma_Run2018D_UL18]
#, Tau_Run2018D_UL18] # JetHT_Run2018D_UL18,  , , MET_Run2018D_UL18, 

dataSamples_UL2018 = [DoubleMuon_Run2018D_UL18,DoubleMuon_Run2018C_UL18,DoubleMuon_Run2018B_UL18,DoubleMuon_Run2018A_UL18] #dataSamples_Run2018A_UL18 + dataSamples_Run2018B_UL18 + dataSamples_Run2018C_UL18 + dataSamples_Run2018D_UL18



dataSamples = dataSamples_UL2018

samples = dataSamples_UL2018

# ---------------------------------------------------------------------

if __name__ == "__main__":
    from CMGTools.RootTools.samples.tools import runMain
    runMain(samples, localobjs=locals())
