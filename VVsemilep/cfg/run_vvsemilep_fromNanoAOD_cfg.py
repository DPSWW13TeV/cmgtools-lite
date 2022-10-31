import re, os, sys
from CMGTools.RootTools.samples.configTools import printSummary, mergeExtensions, doTestN, configureSplittingFromTime, cropToLumi
from CMGTools.RootTools.samples.autoAAAconfig import autoAAA
from PhysicsTools.HeppyCore.framework.heppy_loop import getHeppyOption

import ssl
ssl._create_default_https_context = ssl._create_unverified_context

from CMGTools.RootTools.samples.ComponentCreator import ComponentCreator
kreator = ComponentCreator()
def byCompName(components, regexps):
    return [ c for c in components if any(re.match(r, c.name) for r in regexps) ]

year = getHeppyOption("year", "2018")
analysis = getHeppyOption("analysis", "main")
preprocessor = getHeppyOption("nanoPreProcessor")
selectComponents = getHeppyOption("selectComponents","both")
#selectComponents = getHeppyOption("selectComponents","DATA")
#selectComponents = getHeppyOption("selectComponents","ALL")
test = getHeppyOption("test","") #"testam")

if year == '2018':
    from CMGTools.RootTools.samples.samples_13TeV_RunIISummer20UL18NanoAODv9 import samples as mcSamples_
    from CMGTools.RootTools.samples.samples_13TeV_DATA2018_NanoAOD import dataSamples_UL2018 as allData
elif year == '2017':
    from CMGTools.RootTools.samples.samples_13TeV_RunIISummer20UL17NanoAODv9 import samples as mcSamples_
    from CMGTools.RootTools.samples.samples_13TeV_DATA2017_NanoAOD import dataSamples_UL2017 as allData
elif year == '2016':
    from CMGTools.RootTools.samples.samples_13TeV_RunIISummer20UL16NanoAODv9 import samples as mcSamples_
    from CMGTools.RootTools.samples.samples_13TeV_DATA2016_NanoAOD import dataSamples_UL16 as allData
elif year == '2016APV':
    from CMGTools.RootTools.samples.samples_13TeV_RunIISummer20UL16APVNanoAODv9 import samples as mcSamples_
    from CMGTools.RootTools.samples.samples_13TeV_DATA2016APV_NanoAOD import dataSamples_UL16APV as allData

autoAAA(mcSamples_+allData, quiet=not(getHeppyOption("verboseAAA",False)), redirectorAAA="xrootd-cms.infn.it") # must be done before mergeExtensions
#autoAAA(mcSamples_+allData, quiet=not(getHeppyOption("verboseAAA",False)), redirectorAAA="cms-xrd-global.cern.ch/",site="T2_CH_CSCS")
mcSamples_, _ = mergeExtensions(mcSamples_)

# Triggers
if year == '2018':
    from CMGTools.RootTools.samples.triggers_13TeV_DATA2018 import all_triggers as triggers
elif year == '2017':
    from CMGTools.RootTools.samples.triggers_13TeV_DATA2017 import all_triggers as triggers
    triggers["FR_1mu_iso"] = [] # they probably existed but we didn't use them in 2017
elif year in ['2016','2016APV']:
    from CMGTools.RootTools.samples.triggers_13TeV_DATA2016 import all_triggers as triggers
    triggers["FR_1mu_noiso_smpd"] = [] 

from CMGTools.VVsemilep.tools.nanoAOD.vvsemilep_modules import triggerGroups_dict

DatasetsAndTriggers = []
theyear=int(year) if year != '2016APV' else 2016
if analysis == "main":
    mcSamples =  byCompName(mcSamples_, [
        # diboson
        "ZZTo2Q2L", "WZTo2Q2L",
        "WZTo1L1Nu2Q","WWTo1L1Nu2Q"
        "W.*JetsToLNu.*LO","DYJets.*LHEFilter.*",
         #Ttbar + single top + tW
        "TTJets",
##am        "TT(Lep|Semi)_pow",
        "T_sch",        "T_tch", "TBar_tch", "T_tWch.*", "TBar_tWch.*",
##am        # conversions
       #"WGToLNuG", "ZGTo2LG", # , "TGJets_lep",
##am        #  # diboson + DPS + WWss
##am        "ZZTo4L", #"WWTo2L2Nu",  "WZTo3LNu_fxfx",   # "WW_DPS", falta dps y wpwp "WWTo2L2Nu_DPS", "WpWpJJ", # "WZTo3LNu_pow",
##am        #  # triboson
##am        "WWW",  "WWZ", "WZG", "WZZ", "ZZZ", # "WWW_ll", <- not there, but its just a leptonic filter

     ])
    DatasetsAndTriggers.append( ("DoubleMuon", triggerGroups_dict["Trigger_2m"][theyear] + triggerGroups_dict["Trigger_3m"][theyear]) )
    DatasetsAndTriggers.append( ("EGamma",     triggerGroups_dict["Trigger_2e"][theyear] + triggerGroups_dict["Trigger_3e"][theyear] + triggerGroups_dict["Trigger_1e"][theyear]) if theyear == 2018 else
                                ("DoubleEG",   triggerGroups_dict["Trigger_2e"][theyear] + triggerGroups_dict["Trigger_3e"][theyear]) )
    DatasetsAndTriggers.append( ("MuonEG",     triggerGroups_dict["Trigger_em"][theyear] + triggerGroups_dict["Trigger_mee"][theyear] + triggerGroups_dict["Trigger_mme"][theyear]) )
    DatasetsAndTriggers.append( ("SingleMuon", triggerGroups_dict["Trigger_1m"][theyear]) )
    DatasetsAndTriggers.append( ("SingleElectron", triggerGroups_dict["Trigger_1e"][theyear]) if theyear != 2018 else (None,None) )
    # DatasetsAndTriggers.append( ("MET", triggerGroups_dict["Trigger_MET"][theyear]) )

elif analysis == "frqcd":
    print [x.name for x in mcSamples_]
    mcSamples = byCompName(mcSamples_, [
        "QCD_Pt20to30_EMEnriched",
        "QCD_Mu15", "QCD_Pt(20|30|50|80|120|170)to.*_Mu5", 
        "QCD_Pt(20|30|50|80|120|170)to.*_EMEn.*", 
        "QCD_Pt(20|30|50|80|120|170)to.*_bcToE.*",
        "DYJetsToLL_M50_LO", "DYJetsToLL_M10to50_LO",
        "TT(Lep|Semi)_pow",
        "WJetsToLNu_012JetsNLO_34JetsLO"
    ])
    egfrpd = {2016:"DoubleEG", 2017:"SingleElectron", 2018:"EGamma"}[theyear]
    DatasetsAndTriggers.append( ("DoubleMuon", triggers["FR_1mu_noiso"] + triggers["FR_1mu_iso"]) )
    DatasetsAndTriggers.append( (egfrpd,       triggers["FR_1e_noiso"] + triggers["FR_1e_iso"]) )
    DatasetsAndTriggers.append( ("SingleMuon", triggers["FR_1mu_noiso_smpd"]) )


# make MC
mcTriggers = sum((trigs for (pd,trigs) in DatasetsAndTriggers if trigs), [])
if getHeppyOption('applyTriggersInMC'):
    for comp in mcSamples:
        comp.triggers = mcTriggers

# make data
dataSamples = []; vetoTriggers = []
for pd, trigs in DatasetsAndTriggers:
    if not trigs: continue
    if pd=='MET': # do not include MET dataset in cross-cleaning of datasets
        for comp in byCompName(allData, [pd]):
            comp.triggers = trigs[:]
            dataSamples.append(comp)
        continue

    for comp in byCompName(allData, [pd]):
        comp.triggers = trigs[:]
        comp.vetoTriggers = vetoTriggers[:]
        dataSamples.append(comp)
    vetoTriggers += trigs[:]

selectedComponents = getHeppyOption('selectComponents')
if selectComponents=='MC':
    selectedComponents = mcSamples
elif selectComponents=='DATA':
    selectedComponents = dataSamples
else:
    selectedComponents = mcSamples+dataSamples #byCompName(selectedComponents, getHeppyOption('selectComponents').split(","))

autoAAA(selectedComponents, quiet=not(getHeppyOption("verboseAAA",False)), redirectorAAA="xrootd-cms.infn.it")
configureSplittingFromTime(dataSamples,5,12)
configureSplittingFromTime(mcSamples,10,12)
selectedComponents, _ = mergeExtensions(selectedComponents)



def setFilesPerJob(comps,filesperjob):
    #print comps,filesperjob
    for comp in comps:
        comp.splitFactor=len(comp.files) / filesperjob

if analysis == "main":
    cropToLumi(byCompName(selectedComponents,["DYJetsToLL", "T_","TBar_","TT(Lep|Semi)_pow"]),50.)
    cropToLumi(byCompName(selectedComponents,["ZZTo4L"]),40.)

if analysis == "frqcd":
    cropToLumi(selectedComponents, 5.0)
    #cropToLumi(byCompName(selectedComponents,["QCD"]), 0.3)
    #cropToLumi(byCompName(selectedComponents,["QCD_Pt\d+to\d+$"]), 0.1)

    configureSplittingFromTime(selectedComponents, 5, 3, maxFiles=8)
    configureSplittingFromTime(byCompName(selectedComponents, ["EGamma","Single.*Run2017.*","SingleMuon_Run2018.*"]), 0.5, 12, maxFiles=5) 
    setFilesPerJob( selectedComponents, 1)
    #configureSplittingFromTime(byCompName(selectedComponents, [r"QCD_Pt\d+to\d+$","QCD.*EME"]), 5, 1, maxFiles=6) 
else:    
    setFilesPerJob( selectedComponents, 1)

# print summary of components to process
if getHeppyOption("justSummary"): 
    printSummary(selectedComponents)
    sys.exit(0)

from CMGTools.VVsemilep.tools.nanoAOD.vvsemilep_modules import *

from PhysicsTools.NanoAODTools.postprocessing.framework.postprocessor import PostProcessor

# in the cut string, keep only the main cuts to have it simpler
modules = vvsemilep_sequence_step1
cut = vvsemilep_skim_cut
compression = "ZLIB:3" #"LZ4:4" #"LZMA:9"
branchsel_in = os.environ['CMSSW_BASE']+"/src/CMGTools/VVsemilep/python/tools/nanoAOD/branchsel_in.txt"
branchsel_out = os.environ['CMSSW_BASE']+"/src/CMGTools/VVsemilep/python/tools/nanoAOD/branchsel_out.txt"

if analysis == "frqcd":
    modules = ttH_sequence_step1_FR
    cut = ttH_skim_cut_FR
    compression = "LZMA:9"
    branchsel_out = os.environ['CMSSW_BASE']+"/src/CMGTools/VVsemilep/python/plotter/ttH-multilepton/lepton-fr/qcd1l-skim-ec.txt"

POSTPROCESSOR = PostProcessor(None, [], modules = modules,
        cut = cut, prefetch = True, longTermCache = False,
        branchsel = branchsel_in, outputbranchsel = branchsel_out, compression = compression)

test = getHeppyOption("test")
if test == "94X-MC":
    json="/work/sesanche/FRs/CMSSW_10_4_0/src/CMGTools/TTHAnalysis/data/Cert_314472-325175_13TeV_17SeptEarlyReReco2018ABC_PromptEraD_Collisions18_JSON.txt"
    TTLep_pow = kreator.makeDataComponent("SingleElectron_Run2017C_14Dec2018", "/SingleElectron/Run2017C-Nano14Dec2018-v1/NANOAOD", "CMS", ".*root", json)
    TTLep_pow.files = ["/pnfs/psi.ch/cms/trivcat/store/user/sesanche/NanoAOD_ULv9_jan21///store/data/Run2018D/SingleMuon/NANOAOD/UL2018_MiniAODv2_NanoAODv9-v1/280000/37F54D98-B6E7-8147-ACA8-0DBA4821F03F_Skim.root"]
    lepSkim.requireSameSignPair = False
    lepSkim.minJets = 0
    lepSkim.minMET = 0
    lepSkim.prescaleFactor = 0
    selectedComponents = [TTLep_pow]
if test == "synch-2016":
    TTLep_pow = kreator.makeMCComponent("TTLep_pow", "/TTTo2L2Nu_TuneCP5up_PSweights_13TeV-powheg-pythia8/RunIISummer16NanoAODv7-PUMoriond17_Nano02Apr2020_102X_mcRun2_asymptotic_v8-v1/NANOAODSIM", "CMS", ".*root", 831.76*((3*0.108)**2) )
    TTLep_pow.files = ["/pnfs/psi.ch/cms/trivcat/store/user/sesanche/ttH_synch/input/NANO_RunIISummer16MiniAODv3_NANO.root"]
    selectedComponents = [TTLep_pow]
elif test == "94X-MC-miniAOD":
    TTLep_pow = kreator.makeMCComponent("TTLep_pow", "/TTTo2L2Nu_mtop166p5_TuneCP5_PSweights_13TeV-powheg-pythia8/RunIIFall17MiniAOD-94X_mc2017_realistic_v10-v1/MINIAODSIM", "CMS", ".*root", 831.76*((3*0.108)**2) )
    TTLep_pow.files = [ 'root://cms-xrd-global.cern.ch//store/mc/RunIIFall17MiniAOD/TTTo2L2Nu_mtop166p5_TuneCP5_PSweights_13TeV-powheg-pythia8/MINIAODSIM/94X_mc2017_realistic_v10-v1/70000/3CC234EB-44E0-E711-904F-FA163E0DF774.root' ]
    localfile = os.path.expandvars("/tmp/$USER/%s" % os.path.basename(TTLep_pow.files[0]))
    if os.path.exists(localfile): TTLep_pow.files = [ localfile ] 
    from CMGTools.Production.nanoAODPreprocessor import nanoAODPreprocessor
    TTLep_pow.preprocessor = nanoAODPreprocessor("/afs/cern.ch/work/g/gpetrucc/ttH/CMSSW_10_4_0/src/nanov4_NANO_cfg.py")
    selectedComponents = [TTLep_pow]
elif test == "102X-MC":
    TTLep_pow = kreator.makeMCComponent("TTLep_pow", "/TTTo2L2Nu_TuneCP5_13TeV-powheg-pythia8/RunIIAutumn18NanoAODv4-Nano14Dec2018_102X_upgrade2018_realistic_v16-v1/NANOAODSIM", "CMS", ".*root", 831.76*((3*0.108)**2), useAAA=True )
    TTLep_pow.files = TTLep_pow.files[:1]
    selectedComponents = [TTLep_pow]

elif test == "testam":
    WZTo1L1Nu2Q           = kreator.makeMCComponent("WZTo1L1Nu2Q","/WZTo1L1Nu2Q_4f_TuneCP5_13TeV-amcatnloFXFX-pythia8/RunIISummer20UL18NanoAODv9-106X_upgrade2018_realistic_v16_L1v1-v1/NANOAODSIM", "CMS", ".*root", 9.370, fracNegWeights=2.049e-01)

    WZTo1L1Nu2Q.files = WZTo1L1Nu2Q.files[:1]
    selectedComponents = [WZTo1L1Nu2Q]
    modules = vvsemilep_sequence_step1
    cut = vvsemilep_skim_cut
    compression = "ZLIB:3" #"LZ4:4" #"LZMA:9"
    branchsel_in = os.environ['CMSSW_BASE']+"/src/CMGTools/VVsemilep/python/tools/nanoAOD/branchsel_in.txt"
    branchsel_out = os.environ['CMSSW_BASE']+"/src/CMGTools/VVsemilep/python/tools/nanoAOD/branchsel_out.txt"
    selectedComponents =[WZTo1L1Nu2Q]

elif test == "94X-data":
    json = 'Cert_294927-306462_13TeV_EOY2017ReReco_Collisions17_JSON_v1.txt'
    SingleElectron_Run2017C_14Dec2018 = kreator.makeDataComponent("SingleElectron_Run2017C_14Dec2018", "/SingleElectron/Run2017C-Nano14Dec2018-v1/NANOAOD", "CMS", ".*root", json)
    SingleElectron_Run2017C_14Dec2018.files = ["0450ACEF-E1E5-1345-8660-28CF5ABE26BE.root"]
    SingleElectron_Run2017C_14Dec2018.triggers = triggerGroups_dict["Trigger_1e"][year]
    SingleElectron_Run2017C_14Dec2018.vetoTriggers = triggerGroups_dict["Trigger_2m"][year] + triggerGroups_dict["Trigger_3m"][year]+triggerGroups_dict["Trigger_2e"][year] + triggerGroups_dict["Trigger_3e"][year]+triggerGroups_dict["Trigger_em"][year] + triggerGroups_dict["Trigger_mee"][year] + triggerGroups_dict["Trigger_mme"][year]+triggerGroups_dict["Trigger_1m"][year]
    
    selectedComponents = [SingleElectron_Run2017C_14Dec2018]
elif test in ('2','3','3s'):
    doTestN(test, selectedComponents)
