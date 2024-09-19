from CMGTools.RootTools.samples.ComponentCreator import ComponentCreator
kreator = ComponentCreator()

json='/afs/cern.ch/cms/CAF/CMSCOMM/COMM_DQM/certification/Collisions16/13TeV/Legacy_2016/Cert_271036-284044_13TeV_Legacy2016_Collisions16_JSON.txt'

### ----------------------------- UL16 Run2016Bv1 HIPM  ----------------------------------------


SingleElectron_Run2016Bv1_HIPM_UL16 = kreator.makeDataComponent("SingleElectron_Run2016Bv1_HIPM_UL16", "/SingleElectron/Run2016B-ver1_HIPM_UL2016_MiniAODv2_NanoAODv9-v1/NANOAOD", "CMS", ".*root", json)
SingleMuon_Run2016Bv1_HIPM_UL16     = kreator.makeDataComponent("SingleMuon_Run2016Bv1_HIPM_UL16"    , "/SingleMuon/Run2016B-ver1_HIPM_UL2016_MiniAODv2_NanoAODv9-v1/NANOAOD"    , "CMS", ".*root", json)

dataSamples_Run2016Bv1_HIPM_UL16 = [SingleElectron_Run2016Bv1_HIPM_UL16,SingleMuon_Run2016Bv1_HIPM_UL16]

### ----------------------------- UL16 Run2016Bv2 HIPM  ----------------------------------------

SingleElectron_Run2016Bv2_HIPM_UL16 = kreator.makeDataComponent("SingleElectron_Run2016Bv2_HIPM_UL16", "/SingleElectron/Run2016B-ver2_HIPM_UL2016_MiniAODv2_NanoAODv9-v1/NANOAOD", "CMS", ".*root", json)
SingleMuon_Run2016Bv2_HIPM_UL16     = kreator.makeDataComponent("SingleMuon_Run2016Bv2_HIPM_UL16"    , "/SingleMuon/Run2016B-ver2_HIPM_UL2016_MiniAODv2_NanoAODv9-v1/NANOAOD"    , "CMS", ".*root", json)

dataSamples_Run2016Bv2_HIPM_UL16 = [SingleElectron_Run2016Bv2_HIPM_UL16,SingleMuon_Run2016Bv2_HIPM_UL16]

### ----------------------------- UL16 Run2016C HIPM  ----------------------------------------

SingleElectron_Run2016C_HIPM_UL16 = kreator.makeDataComponent("SingleElectron_Run2016C_HIPM_UL16", "/SingleElectron/Run2016C-HIPM_UL2016_MiniAODv2_NanoAODv9-v1/NANOAOD", "CMS", ".*root", json)
SingleMuon_Run2016C_HIPM_UL16     = kreator.makeDataComponent("SingleMuon_Run2016C_HIPM_UL16"    , "/SingleMuon/Run2016C-HIPM_UL2016_MiniAODv2_NanoAODv9-v1/NANOAOD"    , "CMS", ".*root", json)

dataSamples_Run2016C_HIPM_UL16 = [SingleElectron_Run2016C_HIPM_UL16,SingleMuon_Run2016C_HIPM_UL16]

### ----------------------------- UL16 Run2016D HIPM  ----------------------------------------

SingleElectron_Run2016D_HIPM_UL16 = kreator.makeDataComponent("SingleElectron_Run2016D_HIPM_UL16", "/SingleElectron/Run2016D-HIPM_UL2016_MiniAODv2_NanoAODv9-v1/NANOAOD", "CMS", ".*root", json)
SingleMuon_Run2016D_HIPM_UL16     = kreator.makeDataComponent("SingleMuon_Run2016D_HIPM_UL16"    , "/SingleMuon/Run2016D-HIPM_UL2016_MiniAODv2_NanoAODv9-v1/NANOAOD"    , "CMS", ".*root", json)

dataSamples_Run2016D_HIPM_UL16 = [SingleElectron_Run2016D_HIPM_UL16,SingleMuon_Run2016D_HIPM_UL16]

### ----------------------------- UL16 Run2016E HIPM  ----------------------------------------

SingleElectron_Run2016E_HIPM_UL16 = kreator.makeDataComponent("SingleElectron_Run2016E_HIPM_UL16", "/SingleElectron/Run2016E-HIPM_UL2016_MiniAODv2_NanoAODv9-v1/NANOAOD", "CMS", ".*root", json)
SingleMuon_Run2016E_HIPM_UL16     = kreator.makeDataComponent("SingleMuon_Run2016E_HIPM_UL16"    , "/SingleMuon/Run2016E-HIPM_UL2016_MiniAODv2_NanoAODv9-v1/NANOAOD"    , "CMS", ".*root", json)

dataSamples_Run2016E_HIPM_UL16 = [SingleElectron_Run2016E_HIPM_UL16,SingleMuon_Run2016E_HIPM_UL16]


### ----------------------------- UL16 Run2016F HIPM  ----------------------------------------

SingleElectron_Run2016F_HIPM_UL16 = kreator.makeDataComponent("SingleElectron_Run2016F_HIPM_UL16", "/SingleElectron/Run2016F-HIPM_UL2016_MiniAODv2_NanoAODv9-v1/NANOAOD", "CMS", ".*root", json)
SingleMuon_Run2016F_HIPM_UL16     = kreator.makeDataComponent("SingleMuon_Run2016F_HIPM_UL16"    , "/SingleMuon/Run2016F-HIPM_UL2016_MiniAODv2_NanoAODv9-v1/NANOAOD"    , "CMS", ".*root", json)

dataSamples_Run2016F_HIPM_UL16 = [SingleElectron_Run2016F_HIPM_UL16,SingleMuon_Run2016F_HIPM_UL16]

dataSamples_UL16APV=dataSamples_Run2016Bv1_HIPM_UL16+dataSamples_Run2016Bv2_HIPM_UL16+dataSamples_Run2016C_HIPM_UL16+dataSamples_Run2016D_HIPM_UL16+dataSamples_Run2016E_HIPM_UL16+dataSamples_Run2016F_HIPM_UL16
