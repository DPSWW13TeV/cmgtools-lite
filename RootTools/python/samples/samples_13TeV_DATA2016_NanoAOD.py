from CMGTools.RootTools.samples.ComponentCreator import ComponentCreator
kreator = ComponentCreator()

json='/afs/cern.ch/cms/CAF/CMSCOMM/COMM_DQM/certification/Collisions16/13TeV/Legacy_2016/Cert_271036-284044_13TeV_Legacy2016_Collisions16_JSON.txt'


### ----------------------------- UL16 Run2016F  ----------------------------------------

SingleElectron_Run2016F_UL16 = kreator.makeDataComponent("SingleElectron_Run2016F_UL16", "/SingleElectron/Run2016F-UL2016_MiniAODv2_NanoAODv9-v1/NANOAOD", "CMS", ".*root", json)
SingleMuon_Run2016F_UL16     = kreator.makeDataComponent("SingleMuon_Run2016F_UL16"    , "/SingleMuon/Run2016F-UL2016_MiniAODv2_NanoAODv9-v1/NANOAOD"    , "CMS", ".*root", json)
dataSamples_Run2016F_UL16    = [SingleElectron_Run2016F_UL16,SingleMuon_Run2016F_UL16]


### ----------------------------- UL16 Run2016G  ----------------------------------------

SingleElectron_Run2016G_UL16 = kreator.makeDataComponent("SingleElectron_Run2016G_UL16", "/SingleElectron/Run2016G-UL2016_MiniAODv2_NanoAODv9-v1/NANOAOD", "CMS", ".*root", json)
SingleMuon_Run2016G_UL16     = kreator.makeDataComponent("SingleMuon_Run2016G_UL16"    , "/SingleMuon/Run2016G-UL2016_MiniAODv2_NanoAODv9-v1/NANOAOD"    , "CMS", ".*root", json)
dataSamples_Run2016G_UL16    = [SingleElectron_Run2016G_UL16,SingleMuon_Run2016G_UL16]


### ----------------------------- UL16 Run2016H  ----------------------------------------

SingleElectron_Run2016H_UL16 = kreator.makeDataComponent("SingleElectron_Run2016H_UL16", "/SingleElectron/Run2016H-UL2016_MiniAODv2_NanoAODv9-v1/NANOAOD", "CMS", ".*root", json)
SingleMuon_Run2016H_UL16     = kreator.makeDataComponent("SingleMuon_Run2016H_UL16"    , "/SingleMuon/Run2016H-UL2016_MiniAODv2_NanoAODv9-v1/NANOAOD"    , "CMS", ".*root", json)
dataSamples_Run2016H_UL16    = [SingleElectron_Run2016H_UL16,SingleMuon_Run2016H_UL16]

dataSamples_UL16=dataSamples_Run2016F_UL16+dataSamples_Run2016G_UL16+dataSamples_Run2016H_UL16

dataSamples =  dataSamples_UL16
samples = dataSamples

### ---------------------------------------------------------------------



if __name__ == "__main__":
    from CMGTools.RootTools.samples.tools import runMain
    runMain(samples, localobjs=locals())
