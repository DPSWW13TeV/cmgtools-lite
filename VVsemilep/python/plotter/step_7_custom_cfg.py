# Auto generated configuration file
# using:
# Revision: 1.19
# Source: /local/reps/CMSSW/CMSSW/Configuration/Applications/python/ConfigBuilder.py,v
# with command line options: --python_filename HIG-RunIISummer20UL16NanoAODv9-04365_1_cfg.py --eventcontent NANOAODSIM --customise Configuration/DataProcessing/Utils.addMonitoring --datatier NANOAODSIM --fileout file:HIG-RunIISummer20UL16NanoAODv9-04365.root --conditions 106X_mcRun2_asymptotic_v17 --step NANO --filein file:HIG-RunIISummer20UL16MiniAODv2-03246.root --era Run2_2016,run2_nanoAOD_106Xv2 --no_exec --mc -n 10000
import FWCore.ParameterSet.Config as cms

from Configuration.Eras.Era_Run2_2016_cff import Run2_2016
from Configuration.Eras.Modifier_run2_nanoAOD_106Xv2_cff import run2_nanoAOD_106Xv2

process = cms.Process('NANO',Run2_2016,run2_nanoAOD_106Xv2)

# import of standard configurations
process.load('Configuration.StandardSequences.Services_cff')
process.load('SimGeneral.HepPDTESSource.pythiapdt_cfi')
process.load('FWCore.MessageService.MessageLogger_cfi')
process.load('Configuration.EventContent.EventContent_cff')
process.load('SimGeneral.MixingModule.mixNoPU_cfi')
process.load('Configuration.StandardSequences.GeometryRecoDB_cff')
process.load('Configuration.StandardSequences.MagneticField_cff')
process.load('PhysicsTools.NanoAOD.nano_cff')
process.load('Configuration.StandardSequences.EndOfProcess_cff')
process.load('Configuration.StandardSequences.FrontierConditions_GlobalTag_cff')
process.load("PhysicsTools.NanoAOD.genWeightsTable_cfi")
process.MessageLogger.cerr.FwkReport.reportEvery = cms.untracked.int32(500)
process.maxEvents = cms.untracked.PSet(
    input = cms.untracked.int32(500)
)

# Input source
process.source = cms.Source("PoolSource",
    fileNames = cms.untracked.vstring('/store/mc/RunIISummer20UL16MiniAODv2/WWTo1L1Nu2Q_4f_TuneCP5_13TeV-amcatnloFXFX-pythia8/MINIAODSIM/106X_mcRun2_asymptotic_v17-v2/2820000/0776A4F5-E4DD-C84F-A495-42038BF7AC6E.root'),
    secondaryFileNames = cms.untracked.vstring()
)

process.options = cms.untracked.PSet(

)

# Production Info
process.configurationMetadata = cms.untracked.PSet(
    annotation = cms.untracked.string('--python_filename nevts:10000'),
    name = cms.untracked.string('Applications'),
    version = cms.untracked.string('$Revision: 1.19 $')
)

# Output definition

process.NANOAODSIMoutput = cms.OutputModule("NanoAODOutputModule",
    compressionAlgorithm = cms.untracked.string('LZMA'),
    compressionLevel = cms.untracked.int32(9),
    dataset = cms.untracked.PSet(
        dataTier = cms.untracked.string('NANOAODSIM'),
        filterName = cms.untracked.string('')
    ),
    fileName = cms.untracked.string('file:nanoaod.root'),
    outputCommands = process.NANOAODSIMEventContent.outputCommands
)

# Additional output definition

# Other statements
from Configuration.AlCa.GlobalTag import GlobalTag
process.GlobalTag = GlobalTag(process.GlobalTag, '106X_mcRun2_asymptotic_v17', '')


# Path and EndPath definitions
process.nanoAOD_step = cms.Path(process.nanoSequenceMC)
process.endjob_step = cms.EndPath(process.endOfProcess)
process.NANOAODSIMoutput_step = cms.EndPath(process.NANOAODSIMoutput)

# Schedule definition
process.schedule = cms.Schedule(process.nanoAOD_step,process.endjob_step,process.NANOAODSIMoutput_step)
from PhysicsTools.PatAlgos.tools.helpers import associatePatAlgosToolsTask
associatePatAlgosToolsTask(process)

# customisation of the process.

# Automatic addition of the customisation function from PhysicsTools.NanoAOD.nano_cff
from PhysicsTools.NanoAOD.nano_cff import nanoAOD_customizeMC

# call to customisation function nanoAOD_customizeMC imported from PhysicsTools.NanoAOD.nano_cff
process = nanoAOD_customizeMC(process)


from PhysicsTools.NanoAOD.common_cff import Var
process.jetTable.variables.particleNetAK4_B = Var("bDiscriminator('pfParticleNetAK4DiscriminatorsJetTags:BvsAll')",float,doc="ParticleNetAK4 tagger b vs all (udsg, c) discriminator",precision=10)
process.jetTable.variables.particleNetAK4_CvsL = Var("bDiscriminator('pfParticleNetAK4DiscriminatorsJetTags:CvsL')",float,doc="ParticleNetAK4 tagger c vs udsg discriminator",precision=10)
process.jetTable.variables.particleNetAK4_CvsB = Var("bDiscriminator('pfParticleNetAK4DiscriminatorsJetTags:CvsB')",float,doc="ParticleNetAK4 tagger c vs b discriminator",precision=10)
process.jetTable.variables.particleNetAK4_QvsG = Var("bDiscriminator('pfParticleNetAK4DiscriminatorsJetTags:QvsG')",float,doc="ParticleNetAK4 tagger uds vs g discriminator",precision=10)
process.jetTable.variables.particleNetAK4_puIdDisc = Var("1-bDiscriminator('pfParticleNetAK4JetTags:probpu')",float,doc="ParticleNetAK4 tagger pileup jet discriminator",precision=10)

#from PhysicsTools.NanoTuples.nanoTuples_cff import nanoTuples_customizeMC
#process.jetTable.particleNetAK4_B = Var("bDiscriminator('pfParticleNetAK4DiscriminatorsJetTags:BvsAll')",float,doc="ParticleNetAK4 tagger b vs all (udsg, c) discriminator",precision=10)
#process.jetTable.particleNetAK4_CvsL = Var("bDiscriminator('pfParticleNetAK4DiscriminatorsJetTags:CvsL')",float,doc="ParticleNetAK4 tagger c vs udsg discriminator",precision=10)
#process.jetTable.particleNetAK4_CvsB = Var("bDiscriminator('pfParticleNetAK4DiscriminatorsJetTags:CvsB')",float,doc="ParticleNetAK4 tagger c vs b discriminator",precision=10)
#process.jetTable.particleNetAK4_QvsG = Var("bDiscriminator('pfParticleNetAK4DiscriminatorsJetTags:QvsG')",float,doc="ParticleNetAK4 tagger uds vs g discriminator",precision=10)
#process.jetTable.particleNetAK4_puIdDisc = Var("1-bDiscriminator('pfParticleNetAK4JetTags:probpu')",float,doc="ParticleNetAK4 tagger pileup jet discriminator",precision=10)
#
# Automatic addition of the customisation function from PhysicsTools.NanoTuples.nanoTuples_cff
##amfrom PhysicsTools.NanoTuples.nanoTuples_cff import nanoTuples_customizeMC

# call to customisation function nanoTuples_customizeMC imported from PhysicsTools.NanoTuples.nanoTuples_cff
#process = nanoTuples_customizeMC(process)

process.add_(cms.Service('InitRootHandlers', EnableIMT = cms.untracked.bool(False)))
#process.genWeightsTable.debug = cms.untracked.bool(True)
#process.genWeightsTable.missingLHEHeaderFile = cms.FileInPath('initrwgt_aQGC16.header')
#process.genWeightsTable.preferredPDFs = cms.VPSet(cms.PSet( name = cms.string('NNPDF31_nnlo_as_0118_nf_4_mc_hessian'), lhaid = cms.uint32(325500)))

# Automatic addition of the customisation function from Configuration.DataProcessing.Utils
from Configuration.DataProcessing.Utils import addMonitoring

# call to customisation function addMonitoring imported from Configuration.DataProcessing.Utils
process = addMonitoring(process)

# End of customisation functions

# Customisation from command line

# Add early deletion of temporary data products to reduce peak memory need
from Configuration.StandardSequences.earlyDeleteSettings_cff import customiseEarlyDelete
process = customiseEarlyDelete(process)
# End adding early deletion
