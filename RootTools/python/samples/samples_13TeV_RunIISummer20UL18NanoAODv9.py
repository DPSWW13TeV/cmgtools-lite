# COMPONENT CREATOR
from CMGTools.RootTools.samples.ComponentCreator import ComponentCreator
kreator = ComponentCreator()
import os 

# # QCD_Pt
# QCD_Pt80to120 = kreator.makeMCComponent("QCD_Pt80to120", "/QCD_Pt_80to120_TuneCP5_13TeV_pythia8/RunIIAutumn18NanoAODv4-Nano14Dec2018_102X_upgrade2018_realistic_v16-v1/NANOAODSIM", "CMS", ".*root", 2.345e+06*1.17805)
# QCD_Pt120to170 = kreator.makeMCComponent("QCD_Pt120to170", "/QCD_Pt_120to170_TuneCP5_13TeV_pythia8/RunIIAutumn18NanoAODv4-Nano14Dec2018_102X_upgrade2018_realistic_v16-v1/NANOAODSIM", "CMS", ".*root", 407800*1.15522)
# QCD_Pt170to300 = kreator.makeMCComponent("QCD_Pt170to300", "/QCD_Pt_170to300_TuneCP5_13TeV_pythia8/RunIIAutumn18NanoAODv4-Nano14Dec2018_102X_upgrade2018_realistic_v16-v1/NANOAODSIM", "CMS", ".*root", 103400*1.1342)
# QCD_Pt300to470 = kreator.makeMCComponent("QCD_Pt300to470",  "/QCD_Pt_300to470_TuneCP5_13TeV_pythia8/RunIIAutumn18NanoAODv4-Nano14Dec2018_102X_upgrade2018_realistic_v16-v1/NANOAODSIM", "CMS", ".*root", 6838*1.14405)
# QCD_Pt470to600 = kreator.makeMCComponent("QCD_Pt470to600",  "/QCD_Pt_470to600_TuneCP5_13TeV_pythia8/RunIIAutumn18NanoAODv4-Nano14Dec2018_102X_upgrade2018_realistic_v16-v1/NANOAODSIM", "CMS", ".*root", 551.1*1.17619)
# QCD_Pt470to600_ext1 = kreator.makeMCComponent("QCD_Pt470to600_ext1",  "/QCD_Pt_470to600_TuneCP5_13TeV_pythia8/RunIIAutumn18NanoAODv4-Nano14Dec2018_102X_upgrade2018_realistic_v16_ext1-v1/NANOAODSIM", "CMS", ".*root", 551.1*1.17619)
# QCD_Pt600to800 = kreator.makeMCComponent("QCD_Pt600to800", "/QCD_Pt_600to800_TuneCP5_13TeV_pythia8/RunIIAutumn18NanoAODv4-Nano14Dec2018_102X_upgrade2018_realistic_v16-v1/NANOAODSIM", "CMS", ".*root", 156.4*1.19501)
# QCD_Pt800to1000 = kreator.makeMCComponent("QCD_Pt800to1000", "/QCD_Pt_800to1000_TuneCP5_13TeV_pythia8/RunIIAutumn18NanoAODv4-Nano14Dec2018_102X_upgrade2018_realistic_v16_ext1-v1/NANOAODSIM", "CMS", ".*root", 32.293)
# QCD_Pt1000to1400 = kreator.makeMCComponent("QCD_Pt1000to1400", "/QCD_Pt_1000to1400_TuneCP5_13TeV_pythia8/RunIIAutumn18NanoAODv4-Nano14Dec2018_102X_upgrade2018_realistic_v16-v1/NANOAODSIM", "CMS", ".*root", 7.466*1.26149)
# QCD_Pt1400to1800 = kreator.makeMCComponent("QCD_Pt1400to1800", "/QCD_Pt_1400to1800_TuneCP5_13TeV_pythia8/RunIIAutumn18NanoAODv4-Nano14Dec2018_102X_upgrade2018_realistic_v16-v1/NANOAODSIM", "CMS", ".*root", 0.6481*1.30019)
# QCD_Pt1400to1800_ext1 = kreator.makeMCComponent("QCD_Pt1400to1800_ext1", "/QCD_Pt_1400to1800_TuneCP5_13TeV_pythia8/RunIIAutumn18NanoAODv4-Nano14Dec2018_102X_upgrade2018_realistic_v16_ext1-v1/NANOAODSIM", "CMS", ".*root", 0.6481*1.30019)
# QCD_Pt1800to2400 = kreator.makeMCComponent("QCD_Pt1800to2400", "/QCD_Pt_1800to2400_TuneCP5_13TeV_pythia8/RunIIAutumn18NanoAODv4-Nano14Dec2018_102X_upgrade2018_realistic_v16-v1/NANOAODSIM", "CMS", ".*root", 0.08741*1.31499)
# QCD_Pt1800to2400_ext1 = kreator.makeMCComponent("QCD_Pt1800to2400_ext1", "/QCD_Pt_1800to2400_TuneCP5_13TeV_pythia8/RunIIAutumn18NanoAODv4-Nano14Dec2018_102X_upgrade2018_realistic_v16_ext1-v1/NANOAODSIM", "CMS", ".*root", 0.08741*1.31499)
# QCD_Pt2400to3200 = kreator.makeMCComponent("QCD_Pt2400to3200", "/QCD_Pt_2400to3200_TuneCP5_13TeV_pythia8/RunIIAutumn18NanoAODv4-Nano14Dec2018_102X_upgrade2018_realistic_v16-v1/NANOAODSIM", "CMS", ".*root", 0.00522*1.30839)
# QCD_Pt2400to3200_ext1 = kreator.makeMCComponent("QCD_Pt2400to3200_ext1", "/QCD_Pt_2400to3200_TuneCP5_13TeV_pythia8/RunIIAutumn18NanoAODv4-Nano14Dec2018_102X_upgrade2018_realistic_v16_ext1-v1/NANOAODSIM", "CMS", ".*root", 0.00522*1.30839)
# QCD_Pt3200toInf = kreator.makeMCComponent("QCD_Pt3200toInf", "/QCD_Pt_3200toInf_TuneCP5_13TeV_pythia8/RunIIAutumn18NanoAODv4-Nano14Dec2018_102X_upgrade2018_realistic_v16-v1/NANOAODSIM", "CMS", ".*root", 0.0001349*1.22643)
# QCD_Pt3200toInf_ext2 = kreator.makeMCComponent("QCD_Pt3200toInf_ext2", "/QCD_Pt_3200toInf_TuneCP5_13TeV_pythia8/RunIIAutumn18NanoAODv4-Nano14Dec2018_102X_upgrade2018_realistic_v16_ext2-v1/NANOAODSIM", "CMS", ".*root", 0.0001349*1.22643)

# QCDPt = [
#     QCD_Pt80to120,
#     QCD_Pt120to170,
#     QCD_Pt170to300,
#     QCD_Pt300to470,
#     QCD_Pt470to600,
#     QCD_Pt470to600_ext1,
#     QCD_Pt600to800,
#     QCD_Pt800to1000,
#     QCD_Pt1000to1400,
#     QCD_Pt1400to1800,
#     QCD_Pt1400to1800_ext1,
#     QCD_Pt1800to2400,
#     QCD_Pt1800to2400_ext1,
#     QCD_Pt2400to3200,
#     QCD_Pt2400to3200_ext1,
#     QCD_Pt3200toInf,
#     QCD_Pt3200toInf_ext2
# ]


# # QCD HT bins (cross sections from McM)
# QCD_HT100to200 = kreator.makeMCComponent("QCD_HT100to200", "/QCD_HT100to200_TuneCP5_13TeV-madgraphMLM-pythia8/RunIIAutumn18NanoAODv4-Nano14Dec2018_102X_upgrade2018_realistic_v16-v1/NANOAODSIM", "CMS", ".*root", 2.463e+07*1.13073)
# QCD_HT200to300 = kreator.makeMCComponent("QCD_HT200to300", "/QCD_HT200to300_TuneCP5_13TeV-madgraphMLM-pythia8/RunIIAutumn18NanoAODv4-Nano14Dec2018_102X_upgrade2018_realistic_v16-v1/NANOAODSIM", "CMS", ".*root", 1.553e+06*1.1056)
# QCD_HT300to500 = kreator.makeMCComponent("QCD_HT300to500", "/QCD_HT300to500_TuneCP5_13TeV-madgraphMLM-pythia8/RunIIAutumn18NanoAODv4-Nano14Dec2018_102X_upgrade2018_realistic_v16-v1/NANOAODSIM", "CMS", ".*root", 347500*1.01094)
# QCD_HT500to700 = kreator.makeMCComponent("QCD_HT500to700", "/QCD_HT500to700_TuneCP5_13TeV-madgraphMLM-pythia8/RunIIAutumn18NanoAODv4-Nano14Dec2018_102X_upgrade2018_realistic_v16-v1/NANOAODSIM", "CMS", ".*root", 29930*1.0568)
# QCD_HT700to1000 = kreator.makeMCComponent("QCD_HT700to1000", "/QCD_HT700to1000_TuneCP5_13TeV-madgraphMLM-pythia8/RunIIAutumn18NanoAODv4-Nano14Dec2018_102X_upgrade2018_realistic_v16-v1/NANOAODSIM", "CMS", ".*root", 6370*1.06782)
# QCD_HT1000to1500 = kreator.makeMCComponent("QCD_HT1000to1500", "/QCD_HT1000to1500_TuneCP5_13TeV-madgraphMLM-pythia8/RunIIAutumn18NanoAODv4-Nano14Dec2018_102X_upgrade2018_realistic_v16-v1/NANOAODSIM", "CMS", ".*root", 1100*1.09636)
# QCD_HT1500to2000 = kreator.makeMCComponent("QCD_HT1500to2000", "/QCD_HT1500to2000_TuneCP5_13TeV-madgraphMLM-pythia8/RunIIAutumn18NanoAODv4-Nano14Dec2018_102X_upgrade2018_realistic_v16-v1/NANOAODSIM", "CMS", ".*root", 98.71)
# QCD_HT2000toInf = kreator.makeMCComponent("QCD_HT2000toInf", "/QCD_HT2000toInf_TuneCP5_13TeV-madgraphMLM-pythia8/RunIIAutumn18NanoAODv4-Nano14Dec2018_102X_upgrade2018_realistic_v16-v1/NANOAODSIM", "CMS", ".*root", 20.2)

# QCDHT = [
#     QCD_HT100to200,
#     QCD_HT200to300,
#     QCD_HT300to500,
#     QCD_HT500to700,
#     QCD_HT700to1000,
#     QCD_HT1000to1500,
#     QCD_HT1500to2000,
#     QCD_HT2000toInf,
# ]

# # QCD enriched (cross sections form genXSecAna)
QCD_Mu15 = kreator.makeMCComponent("QCD_Mu15", "/QCD_Pt-20_MuEnrichedPt15_TuneCP5_13TeV-pythia8/RunIISummer20UL18NanoAODv9-106X_upgrade2018_realistic_v16_L1v1-v2/NANOAODSIM", "CMS", ".*root", 237800)
# QCD_Pt15to20_Mu5    = kreator.makeMCComponent("QCD_Pt15to20_Mu5"    , "/QCD_Pt-15to20_MuEnrichedPt5_TuneCP5_13TeV_pythia8/RunIIAutumn18NanoAODv4-Nano14Dec2018_102X_upgrade2018_realistic_v16-v1/NANOAODSIM", "CMS" , ".*root", 2.785e+06)
QCD_Pt20to30_Mu5    = kreator.makeMCComponent("QCD_Pt20to30_Mu5"    , "/QCD_Pt-20To30_MuEnrichedPt5_TuneCP5_13TeV-pythia8/RunIISummer20UL18NanoAODv9-106X_upgrade2018_realistic_v16_L1v1-v2/NANOAODSIM", "CMS" , ".*root",2.49e+06) 
QCD_Pt30to50_Mu5    = kreator.makeMCComponent("QCD_Pt30to50_Mu5",     "/QCD_Pt-30To50_MuEnrichedPt5_TuneCP5_13TeV-pythia8/RunIISummer20UL18NanoAODv9-106X_upgrade2018_realistic_v16_L1v1-v2/NANOAODSIM", "CMS", ".*root", 1.364e+06)
QCD_Pt50to80_Mu5    = kreator.makeMCComponent("QCD_Pt50to80_Mu5"    , "/QCD_Pt-50To80_MuEnrichedPt5_TuneCP5_13TeV-pythia8/RunIISummer20UL18NanoAODv9-106X_upgrade2018_realistic_v16_L1v1-v2/NANOAODSIM" , "CMS" , ".*root", 377400) 
QCD_Pt80to120_Mu5   = kreator.makeMCComponent("QCD_Pt80to120_Mu5"   , "/QCD_Pt-80To120_MuEnrichedPt5_TuneCP5_13TeV-pythia8/RunIISummer20UL18NanoAODv9-106X_upgrade2018_realistic_v16_L1v1-v2/NANOAODSIM", "CMS" , ".*root", 88350)  
QCD_Pt120to170_Mu5  = kreator.makeMCComponent("QCD_Pt120to170_Mu5"  , "/QCD_Pt-120To170_MuEnrichedPt5_TuneCP5_13TeV-pythia8/RunIISummer20UL18NanoAODv9-106X_upgrade2018_realistic_v16_L1v1-v2/NANOAODSIM", "CMS" , ".*root", 21250) 
QCD_Pt170to300_Mu5  = kreator.makeMCComponent("QCD_Pt170to300_Mu5", "/QCD_Pt-170To300_MuEnrichedPt5_TuneCP5_13TeV-pythia8/RunIISummer20UL18NanoAODv9-106X_upgrade2018_realistic_v16_L1v1-v2/NANOAODSIM", "CMS", ".*root", 6969)     

# QCD_Pt300to470_Mu5  = kreator.makeMCComponent("QCD_Pt300to470_Mu5"  , "/QCD_Pt-300to470_MuEnrichedPt5_TuneCP5_13TeV_pythia8/RunIIAutumn18NanoAODv4-Nano14Dec2018_102X_upgrade2018_realistic_v16-v1/NANOAODSIM", "CMS" , ".*root", 619.5)
# QCD_Pt300to470_Mu5_ext3  = kreator.makeMCComponent("QCD_Pt300to470_Mu5_ext3"  , "/QCD_Pt-300to470_MuEnrichedPt5_TuneCP5_13TeV_pythia8/RunIIAutumn18NanoAODv4-Nano14Dec2018_102X_upgrade2018_realistic_v16_ext3-v1/NANOAODSIM", "CMS" , ".*root", 619.5)
# QCD_Pt470to600_Mu5  = kreator.makeMCComponent("QCD_Pt470to600_Mu5"  , "/QCD_Pt-470to600_MuEnrichedPt5_TuneCP5_13TeV_pythia8/RunIIAutumn18NanoAODv4-Nano14Dec2018_102X_upgrade2018_realistic_v16-v1/NANOAODSIM", "CMS" , ".*root", 58.9)
# QCD_Pt470to600_Mu5_ext1  = kreator.makeMCComponent("QCD_Pt470to600_Mu5_ext1"  , "/QCD_Pt-470to600_MuEnrichedPt5_TuneCP5_13TeV_pythia8/RunIIAutumn18NanoAODv4-Nano14Dec2018_102X_upgrade2018_realistic_v16_ext1-v1/NANOAODSIM", "CMS" , ".*root", 58.9)
# QCD_Pt600to800_Mu5  = kreator.makeMCComponent("QCD_Pt600to800_Mu5", "/QCD_Pt-600to800_MuEnrichedPt5_TuneCP5_13TeV_pythia8/RunIIAutumn18NanoAODv4-Nano14Dec2018_102X_upgrade2018_realistic_v16-v1/NANOAODSIM", "CMS", ".*root", 18.36)
# QCD_Pt800to1000_Mu5 = kreator.makeMCComponent("QCD_Pt800to1000_Mu5" , "/QCD_Pt-800to1000_MuEnrichedPt5_TuneCP5_13TeV_pythia8/RunIIAutumn18NanoAODv4-Nano14Dec2018_102X_upgrade2018_realistic_v16_ext3-v1/NANOAODSIM", "CMS" , ".*root", 3.253)
# QCD_Pt1000toInf_Mu5 = kreator.makeMCComponent("QCD_Pt1000toInf_Mu5" , "/QCD_Pt-1000toInf_MuEnrichedPt5_TuneCP5_13TeV_pythia8/RunIIAutumn18NanoAODv4-Nano14Dec2018_102X_upgrade2018_realistic_v16-v1/NANOAODSIM", "CMS" , ".*root", 1.075)

QCD_Mu5s = [
    QCD_Pt20to30_Mu5,
    QCD_Pt30to50_Mu5,
    QCD_Pt50to80_Mu5,
    QCD_Pt80to120_Mu5,
    QCD_Pt120to170_Mu5,
    QCD_Pt170to300_Mu5,
 ]
QCD_Mus = [ QCD_Mu15 ] + QCD_Mu5s

# # QCD EMEnr  (cross sections form genXSecAna)
# QCD_Pt15to20_EMEnriched   = kreator.makeMCComponent("QCD_Pt15to20_EMEnriched"  ,"/QCD_Pt-15to20_EMEnriched_TuneCP5_13TeV_pythia8/RunIIAutumn18NanoAODv4-Nano14Dec2018_102X_upgrade2018_realistic_v16_ext1-v1/NANOAODSIM"  , "CMS", ".*root",  1.33e+06)
QCD_Pt20to30_EMEnriched   = kreator.makeMCComponent("QCD_Pt20to30_EMEnriched"  ,"/QCD_Pt-20to30_EMEnriched_TuneCP5_13TeV-pythia8/RunIISummer20UL18NanoAODv9-106X_upgrade2018_realistic_v16_L1v1-v1/NANOAODSIM"  , "CMS", ".*root",  4.928e+06)
QCD_Pt30to50_EMEnriched   = kreator.makeMCComponent("QCD_Pt30to50_EMEnriched"  ,"/QCD_Pt-30to50_EMEnriched_TuneCP5_13TeV-pythia8/RunIISummer20UL18NanoAODv9-106X_upgrade2018_realistic_v16_L1v1-v2/NANOAODSIM"  , "CMS", ".*root",  6.41e+06)
QCD_Pt50to80_EMEnriched   = kreator.makeMCComponent("QCD_Pt50to80_EMEnriched", "/QCD_Pt-50to80_EMEnriched_TuneCP5_13TeV-pythia8/RunIISummer20UL18NanoAODv9-106X_upgrade2018_realistic_v16_L1v1-v2/NANOAODSIM", "CMS", ".*root",  1.986e+06)
QCD_Pt80to120_EMEnriched  = kreator.makeMCComponent("QCD_Pt80to120_EMEnriched" ,"/QCD_Pt-80to120_EMEnriched_TuneCP5_13TeV-pythia8/RunIISummer20UL18NanoAODv9-106X_upgrade2018_realistic_v16_L1v1-v2/NANOAODSIM" , "CMS", ".*root",  370900)
QCD_Pt120to170_EMEnriched = kreator.makeMCComponent("QCD_Pt120to170_EMEnriched","/QCD_Pt-120to170_EMEnriched_TuneCP5_13TeV-pythia8/RunIISummer20UL18NanoAODv9-106X_upgrade2018_realistic_v16_L1v1-v2/NANOAODSIM", "CMS", ".*root",  66760)
QCD_Pt170to300_EMEnriched = kreator.makeMCComponent("QCD_Pt170to300_EMEnriched","/QCD_Pt-170to300_EMEnriched_TuneCP5_13TeV-pythia8/RunIISummer20UL18NanoAODv9-106X_upgrade2018_realistic_v16_L1v1-v2/NANOAODSIM", "CMS", ".*root",  16430)
QCD_Pt300toInf_EMEnriched = kreator.makeMCComponent("QCD_Pt300toInf_EMEnriched","/QCD_Pt-300toInf_EMEnriched_TuneCP5_13TeV-pythia8/RunIISummer20UL18NanoAODv9-106X_upgrade2018_realistic_v16_L1v1-v2/NANOAODSIM", "CMS", ".*root",  1101)

QCD_EMs = [
#     QCD_Pt15to20_EMEnriched,
     QCD_Pt20to30_EMEnriched,
     QCD_Pt30to50_EMEnriched,
     QCD_Pt50to80_EMEnriched,
     QCD_Pt80to120_EMEnriched,
     QCD_Pt120to170_EMEnriched,
     QCD_Pt170to300_EMEnriched,
     QCD_Pt300toInf_EMEnriched
 ]

# #QCD_Pt15to20_bcToE   = kreator.makeMCComponent("QCD_Pt15to20_bcToE",   "/QCD_Pt_15to20_bcToE_TuneCP5_13TeV_pythia8/RunIIFall17MiniAOD-94X_mc2017_realistic_v11-v1/MINIAODSIM"  , "CMS", ".*root", 187000)
QCD_Pt20to30_bcToE   = kreator.makeMCComponent("QCD_Pt20to30_bcToE",   "/QCD_Pt_20to30_bcToE_TuneCP5_13TeV_pythia8/RunIISummer20UL18NanoAODv2-106X_upgrade2018_realistic_v15_L1v1-v1/NANOAODSIM"  , "CMS", ".*root", 313500)
QCD_Pt30to80_bcToE   = kreator.makeMCComponent("QCD_Pt30to80_bcToE",   "/QCD_Pt_30to80_bcToE_TuneCP5_13TeV_pythia8/RunIISummer20UL18NanoAODv9-106X_upgrade2018_realistic_v16_L1v1-v1/NANOAODSIM"  , "CMS", ".*root", 361500)
QCD_Pt80to170_bcToE  = kreator.makeMCComponent("QCD_Pt80to170_bcToE",  "/QCD_Pt_80to170_bcToE_TuneCP5_13TeV_pythia8/RunIISummer20UL18NanoAODv9-106X_upgrade2018_realistic_v16_L1v1-v1/NANOAODSIM" , "CMS", ".*root", 33770)
#QCD_Pt170to250_bcToE = kreator.makeMCComponent("QCD_Pt170to250_bcToE", "/QCD_Pt_170to250_bcToE_TuneCP5_13TeV_pythia8/RunIISummer20UL18NanoAODv9-106X_upgrade2018_realistic_v16_L1v1-v1/NANOAODSIM", "CMS", ".*root", 2126)
# #QCD_Pt250toInf_bcToE = kreator.makeMCComponent("QCD_Pt250toInf_bcToE", "/QCD_Pt_250toInf_bcToE_TuneCP5_13TeV_pythia8/RunIIFall17MiniAOD-94X_mc2017_realistic_v11-v1/MINIAODSIM", "CMS", ".*root", 563.1)

QCD_bcToE = [
    # #   QCD_Pt15to20_bcToE,
    QCD_Pt20to30_bcToE,
    QCD_Pt30to80_bcToE,
    QCD_Pt80to170_bcToE,
#    QCD_Pt170to250_bcToE,
# #   QCD_Pt250toInf_bcToE,
]

# # ====== W + Jets ======
WJetsToLNu_LO = kreator.makeMCComponent("WJetsToLNu_LO","/WJetsToLNu_TuneCP5_13TeV-madgraphMLM-pythia8/RunIISummer20UL18NanoAODv9-106X_upgrade2018_realistic_v16_L1v1-v1/NANOAODSIM", "CMS", ".*root", 3* 20508.9)

# ## LO XSec from genXSecAna times NNLO/LO XSec for inclusive W+jets

W1JetsToLNu_LO = kreator.makeMCComponent("W1JetsToLNu_LO","/W1JetsToLNu_TuneCP5_13TeV-madgraphMLM-pythia8/RunIISummer20UL18NanoAODv9-106X_upgrade2018_realistic_v16_L1v1-v1/NANOAODSIM", "CMS", ".*root", 8123*1.17)
W2JetsToLNu_LO = kreator.makeMCComponent("W2JetsToLNu_LO","/W2JetsToLNu_TuneCP5_13TeV-madgraphMLM-pythia8/RunIISummer20UL18NanoAODv9-106X_upgrade2018_realistic_v16_L1v1-v1/NANOAODSIM", "CMS", ".*root", 2785*1.17)
W3JetsToLNu_LO = kreator.makeMCComponent("W3JetsToLNu_LO","/W3JetsToLNu_TuneCP5_13TeV-madgraphMLM-pythia8/RunIISummer20UL18NanoAODv9-106X_upgrade2018_realistic_v16_L1v1-v1/NANOAODSIM", "CMS", ".*root", 993.4*1.17)
W4JetsToLNu_LO = kreator.makeMCComponent("W4JetsToLNu_LO","/W4JetsToLNu_TuneCP5_13TeV-madgraphMLM-pythia8/RunIISummer20UL18NanoAODv9-106X_upgrade2018_realistic_v16_L1v1-v2/NANOAODSIM", "CMS", ".*root", 542.4*1.17)

# XSec from genXSecAna
WJetsToLNu_NLO        = kreator.makeMCComponent("WJetsToLNu_NLO","/WJetsToLNu_TuneCP5_13TeV-amcatnloFXFX-pythia8/RunIISummer20UL18NanoAODv9-106X_upgrade2018_realistic_v16_L1v1-v2/NANOAODSIM", "CMS", ".*root",6.748e+04,fracNegWeights=1.589e-01)

WJetsToLNu_012JetsNLO_34JetsLO = kreator.makeMCComponent("WJetsToLNu_012JetsNLO_34JetsLO","/WJetsToLNu_012JetsNLO_34JetsLO_EWNLOcorr_13TeV-sherpa/RunIISummer20UL18NanoAODv9-106X_upgrade2018_realistic_v16_L1v1-v1/NANOAODSIM",  "CMS", ".*root", 6.228e+04)

# ### W+jets HT-binned
WJetsToLNu_HT70To100  = kreator.makeMCComponent("WJetsToLNu_HT70To100","/WJetsToLNu_HT-70To100_TuneCP5_13TeV-madgraphMLM-pythia8/RunIISummer20UL18NanoAODv9-106X_upgrade2018_realistic_v16_L1v1-v1/NANOAODSIM", "CMS", ".*root",1271*1.21)
WJetsToLNu_HT100to200 = kreator.makeMCComponent("WJetsToLNu_HT100to200", "/WJetsToLNu_HT-100To200_TuneCP5_13TeV-madgraphMLM-pythia8/RunIISummer20UL18NanoAODv9-106X_upgrade2018_realistic_v16_L1v1-v1/NANOAODSIM", "CMS", ".*root",1253*1.21) 
WJetsToLNu_HT200to400 = kreator.makeMCComponent("WJetsToLNu_HT200to400", "/WJetsToLNu_HT-200To400_TuneCP5_13TeV-madgraphMLM-pythia8/RunIISummer20UL18NanoAODv9-106X_upgrade2018_realistic_v16_L1v1-v1/NANOAODSIM", "CMS", ".*root",335.9*1.21) 
WJetsToLNu_HT400to600 = kreator.makeMCComponent("WJetsToLNu_HT400to600", "/WJetsToLNu_HT-400To600_TuneCP5_13TeV-madgraphMLM-pythia8/RunIISummer20UL18NanoAODv9-106X_upgrade2018_realistic_v16_L1v1-v1/NANOAODSIM", "CMS", ".*root",45.21*1.21) 
WJetsToLNu_HT600to800 = kreator.makeMCComponent("WJetsToLNu_HT600to800", "/WJetsToLNu_HT-600To800_TuneCP5_13TeV-madgraphMLM-pythia8/RunIISummer20UL18NanoAODv9-106X_upgrade2018_realistic_v16_L1v1-v1/NANOAODSIM", "CMS", ".*root",10.99*1.21) 
WJetsToLNu_HT800to1200 = kreator.makeMCComponent("WJetsToLNu_HT800to1200", "/WJetsToLNu_HT-800To1200_TuneCP5_13TeV-madgraphMLM-pythia8/RunIISummer20UL18NanoAODv9-106X_upgrade2018_realistic_v16_L1v1-v1/NANOAODSIM", "CMS", ".*root",4.936*1.21) 
WJetsToLNu_HT1200to2500    = kreator.makeMCComponent("WJetsToLNu_HT1200to2500","/WJetsToLNu_HT-1200To2500_TuneCP5_13TeV-madgraphMLM-pythia8/RunIISummer20UL18NanoAODv9-106X_upgrade2018_realistic_v16_L1v1-v1/NANOAODSIM", "CMS", ".*root",1.156*1.21) 
WJetsToLNu_HT2500toInf = kreator.makeMCComponent("WJetsToLNu_HT2500toInf", "/WJetsToLNu_HT-2500ToInf_TuneCP5_13TeV-madgraphMLM-pythia8/RunIISummer20UL18NanoAODv9-106X_upgrade2018_realistic_v16_L1v1-v2/NANOAODSIM", "CMS", ".*root",0.0263*1.21) 

WJetsToLNuHT = [
    WJetsToLNu_HT70To100,
    WJetsToLNu_HT100to200,
    WJetsToLNu_HT200to400,
    WJetsToLNu_HT400to600,
    WJetsToLNu_HT600to800,
    WJetsToLNu_HT800to1200,
    WJetsToLNu_HT1200to2500,
    WJetsToLNu_HT2500toInf,
]

Ws = [ 
    WJetsToLNu_LO,
    W1JetsToLNu_LO,
    W2JetsToLNu_LO,
    W3JetsToLNu_LO,
    W4JetsToLNu_LO,
    WJetsToLNu_NLO,
    WJetsToLNu_012JetsNLO_34JetsLO,
]+WJetsToLNuHT






# # ====== Z + Jets ======
# ## New FEWZ cross section 1921.8 from https://twiki.cern.ch/twiki/bin/viewauth/CMS/StandardModelCrossSectionsat13TeV


DYJetsToLL_M50 = kreator.makeMCComponent("DYJetsToLL_M50", "/DYJetsToLL_M-50_TuneCP5_13TeV-amcatnloFXFX-pythia8/RunIISummer20UL18NanoAODv9-106X_upgrade2018_realistic_v16_L1v1-v2/NANOAODSIM", "CMS", ".*root", 1921.8*3, fracNegWeights=0.16)

DYJetsToLL_M50_LO =  kreator.makeMCComponent("DYJetsToLL_M50_LO", "/DYJetsToLL_M-50_TuneCP5_13TeV-madgraphMLM-pythia8/RunIISummer20UL18NanoAODv9-106X_upgrade2018_realistic_v16_L1v1-v1/NANOAODSIM", "CMS", ".*root", 1921.8*3)
DYJetsToLL_M50_LO_ext =  kreator.makeMCComponent("DYJetsToLL_M50_LO_ext", "/DYJetsToLL_M-50_TuneCP5_13TeV-madgraphMLM-pythia8/RunIISummer20UL18NanoAODv9-106X_upgrade2018_realistic_v16_L1v1_ext1-v1/NANOAODSIM", "CMS", ".*root", 1921.8*3)
DYJetsToLL_M10to50_LO =  kreator.makeMCComponent("DYJetsToLL_M10to50_LO", "/DYJetsToLL_M-10to50_TuneCP5_13TeV-madgraphMLM-pythia8/RunIISummer20UL18NanoAODv9-106X_upgrade2018_realistic_v16_L1v1-v1/NANOAODSIM", "CMS", ".*root", 15810)


DYJets = [
    DYJetsToLL_M50,
    DYJetsToLL_M50_LO,DYJetsToLL_M50_LO_ext,
    DYJetsToLL_M10to50_LO,
]



DYJetsToLL_M4to50_HT100to200   = kreator.makeMCComponent("DYJetsToLL_M4to50_HT100to200","/DYJetsToLL_M-4to50_HT-100to200_TuneCP5_13TeV-madgraphMLM-pythia8/RunIISummer20UL18NanoAODv9-106X_upgrade2018_realistic_v16_L1v1-v2/NANOAODSIM","CMS", ".*root",204)
DYJetsToLL_M4to50_HT600toInf   = kreator.makeMCComponent("DYJetsToLL_M4to50_HT600toInf","/DYJetsToLL_M-4to50_HT-600toInf_TuneCP5_13TeV-madgraphMLM-pythia8/RunIISummer20UL18NanoAODv9-106X_upgrade2018_realistic_v16_L1v1-v2/NANOAODSIM","CMS", ".*root",1.85)
DYJetsToLL_M50_HT100to200      = kreator.makeMCComponent("DYJetsToLL_M50_HT100to200","/DYJetsToLL_M-50_HT-100to200_TuneCP5_PSweights_13TeV-madgraphMLM-pythia8/RunIISummer20UL18NanoAODv9-106X_upgrade2018_realistic_v16_L1v1-v1/NANOAODSIM","CMS", ".*root", 161.1*1.08)
DYJetsToLL_M50_HT200to400      = kreator.makeMCComponent("DYJetsToLL_M50_HT200to400","/DYJetsToLL_M-50_HT-200to400_TuneCP5_PSweights_13TeV-madgraphMLM-pythia8/RunIISummer20UL18NanoAODv9-106X_upgrade2018_realistic_v16_L1v1-v1/NANOAODSIM","CMS", ".*root", 49.32*1.08)
DYJetsToLL_M50_HT400to600      = kreator.makeMCComponent("DYJetsToLL_M50_HT400to600","/DYJetsToLL_M-50_HT-400to600_TuneCP5_PSweights_13TeV-madgraphMLM-pythia8/RunIISummer20UL18NanoAODv9-106X_upgrade2018_realistic_v16_L1v1-v1/NANOAODSIM","CMS", ".*root", 7.021*1.08)
DYJetsToLL_M50_HT600to800      = kreator.makeMCComponent("DYJetsToLL_M50_HT600to800","/DYJetsToLL_M-50_HT-600to800_TuneCP5_PSweights_13TeV-madgraphMLM-pythia8/RunIISummer20UL18NanoAODv9-106X_upgrade2018_realistic_v16_L1v1-v1/NANOAODSIM","CMS", ".*root", 1.743*1.08 )
DYJetsToLL_M50_HT800to1200     = kreator.makeMCComponent("DYJetsToLL_M50_HT800to1200","/DYJetsToLL_M-50_HT-800to1200_TuneCP5_PSweights_13TeV-madgraphMLM-pythia8/RunIISummer20UL18NanoAODv9-106X_upgrade2018_realistic_v16_L1v1-v1/NANOAODSIM","CMS", ".*root", 0.8082*1.08 )
DYJetsToLL_M50_HT1200to2500    = kreator.makeMCComponent("DYJetsToLL_M50_HT1200to2500","/DYJetsToLL_M-50_HT-1200to2500_TuneCP5_PSweights_13TeV-madgraphMLM-pythia8/RunIISummer20UL18NanoAODv9-106X_upgrade2018_realistic_v16_L1v1-v1/NANOAODSIM","CMS", ".*root", 0.1925*1.08 )
DYJetsToLL_M50_HT2500toInf     = kreator.makeMCComponent("DYJetsToLL_M50_HT2500toInf","/DYJetsToLL_M-50_HT-2500toInf_TuneCP5_PSweights_13TeV-madgraphMLM-pythia8/RunIISummer20UL18NanoAODv9-106X_upgrade2018_realistic_v16_L1v1-v1/NANOAODSIM","CMS", ".*root", 0.003486*1.08 )

DYJetsToLLM50HT = [
    #    DYJetsToLL_M4to50_HT100to200,
    #DYJetsToLL_M4to50_HT600toInf,
    DYJetsToLL_M50_HT100to200,
    DYJetsToLL_M50_HT200to400,
    DYJetsToLL_M50_HT400to600, 
    DYJetsToLL_M50_HT600to800,
    DYJetsToLL_M50_HT800to1200,
    DYJetsToLL_M50_HT1200to2500,
    DYJetsToLL_M50_HT2500toInf,
]


DYJetsToLL_LHEFilterPtZ0to50 = kreator.makeMCComponent("DYJetsToLL_LHEFilterPtZ0to50","/DYJetsToLL_LHEFilterPtZ-0To50_MatchEWPDG20_TuneCP5_13TeV-amcatnloFXFX-pythia8/RunIISummer20UL18NanoAODv9-106X_upgrade2018_realistic_v16_L1v1-v1/NANOAODSIM", "CMS", ".*root", 1.493e+03, fracNegWeights=2.453e-01)
DYJetsToLL_LHEFilterPtZ50to100 = kreator.makeMCComponent("DYJetsToLL_LHEFilterPtZ50to100","/DYJetsToLL_LHEFilterPtZ-50To100_MatchEWPDG20_TuneCP5_13TeV-amcatnloFXFX-pythia8/RunIISummer20UL18NanoAODv9-106X_upgrade2018_realistic_v16_L1v1-v1/NANOAODSIM", "CMS", ".*root", 3.956e+02, fracNegWeights=2.932e-01) 

DYJetsToLL_LHEFilterPtZ100to250 = kreator.makeMCComponent("DYJetsToLL_LHEFilterPtZ100to250","/DYJetsToLL_LHEFilterPtZ-100To250_MatchEWPDG20_TuneCP5_13TeV-amcatnloFXFX-pythia8/RunIISummer20UL18NanoAODv9-106X_upgrade2018_realistic_v16_L1v1-v1/NANOAODSIM", "CMS", ".*root", 1.101e+02, fracNegWeights=2.653e-01)

DYJetsToLL_LHEFilterPtZ250to400  = kreator.makeMCComponent("DYJetsToLL_LHEFilterPtZ250to400","/DYJetsToLL_LHEFilterPtZ-250To400_MatchEWPDG20_TuneCP5_13TeV-amcatnloFXFX-pythia8/RunIISummer20UL18NanoAODv9-106X_upgrade2018_realistic_v16_L1v1-v1/NANOAODSIM", "CMS", ".*root", 3.784e+00 , fracNegWeights=2.877e-01)

DYJetsToLL_LHEFilterPtZ400to650 = kreator.makeMCComponent("DYJetsToLL_LHEFilterPtZ400to650","/DYJetsToLL_LHEFilterPtZ-400To650_MatchEWPDG20_TuneCP5_13TeV-amcatnloFXFX-pythia8/RunIISummer20UL18NanoAODv9-106X_upgrade2018_realistic_v16_L1v1-v1/NANOAODSIM", "CMS", ".*root", 5.083e-01 , fracNegWeights=2.786e-01)
DYJetsToLL_LHEFilterPtZ650toinf = kreator.makeMCComponent("DYJetsToLL_LHEFilterPtZ650toinf","/DYJetsToLL_LHEFilterPtZ-650ToInf_MatchEWPDG20_TuneCP5_13TeV-amcatnloFXFX-pythia8/RunIISummer20UL18NanoAODv9-106X_upgrade2018_realistic_v16_L1v1-v1/NANOAODSIM", "CMS", ".*root", 4.662e-02, fracNegWeights=2.823e-01)



DYJetsPtbinned = [
    DYJetsToLL_LHEFilterPtZ0to50,
    DYJetsToLL_LHEFilterPtZ50to100,
    DYJetsToLL_LHEFilterPtZ100to250,
    DYJetsToLL_LHEFilterPtZ250to400,
    DYJetsToLL_LHEFilterPtZ400to650,
    DYJetsToLL_LHEFilterPtZ650toinf,
]

    
DYs = DYJets + DYJetsToLLM50HT + DYJetsPtbinned


# # ====== TT INCLUSIVE =====

# # TTbar cross section: NNLO, https://twiki.cern.ch/twiki/bin/view/LHCPhysics/TtbarNNLO (172.5)
TT_mttp7kto1k = kreator.makeMCComponent("TT_mttp7kto1k","/TT_Mtt-700to1000_TuneCP5_13TeV-powheg-pythia8/RunIISummer20UL18NanoAODv9-106X_upgrade2018_realistic_v16_L1v1-v1/NANOAODSIM", "CMS", ".*root", 6.513e+01, fracNegWeights=1.002e-02)
TT_mtt1ktoinf = kreator.makeMCComponent("TT_mtt1ktoinf","/TT_Mtt-1000toInf_TuneCP5_13TeV-powheg-pythia8/RunIISummer20UL18NanoAODv9-106X_upgrade2018_realistic_v16_L1v1-v1/NANOAODSIM", "CMS", ".*root", 1.652e+01, fracNegWeights=2.629e-02)

TTJets = kreator.makeMCComponent("TTJets", "/TTJets_TuneCP5_13TeV-amcatnloFXFX-pythia8/RunIISummer20UL18NanoAODv9-106X_upgrade2018_realistic_v16_L1v1-v1/NANOAODSIM", "CMS", ".*root", 831.76, fracNegWeights=0.319)
TTLep_pow  = kreator.makeMCComponent("TTLep_pow", "/TTTo2L2Nu_TuneCP5_13TeV-powheg-pythia8/RunIISummer20UL18NanoAODv9-106X_upgrade2018_realistic_v16_L1v1-v1/NANOAODSIM", "CMS", ".*root", 831.76*((3*0.108)**2) )
TTSemi_pow = kreator.makeMCComponent("TTSemi_pow", "/TTToSemiLeptonic_TuneCP5_13TeV-powheg-pythia8/RunIISummer20UL18NanoAODv9-106X_upgrade2018_realistic_v16_L1v1-v1/NANOAODSIM", "CMS", ".*root", 831.76*2*(3*0.108)*(1-3*0.108) )


TTs = [ TTJets, 
        TTLep_pow,
        TTSemi_pow, TT_mttp7kto1k,TT_mtt1ktoinf
]

# # ====== SINGLE TOP ======
# # Single top cross sections: https://twiki.cern.ch/twiki/bin/viewauth/CMS/SingleTopSigma




T_sch = kreator.makeMCComponent("T_sch","/ST_s-channel_4f_leptonDecays_TuneCP5_13TeV-amcatnlo-pythia8/RunIISummer20UL18NanoAODv9-106X_upgrade2018_realistic_v16_L1v1-v1/NANOAODSIM", "CMS", ".*root",3.549e+00,fracNegWeights=1.735e-01)

T_tch = kreator.makeMCComponent("T_tch","/ST_t-channel_top_5f_InclusiveDecays_TuneCP5_13TeV-powheg-pythia8/RunIISummer20UL18NanoAODv9-106X_upgrade2018_realistic_v16_L1v1-v1/NANOAODSIM", "CMS", ".*root",1.197e+02,fracNegWeights=3.146e-03)
Tbar_tch = kreator.makeMCComponent("Tbar_tch","/ST_t-channel_antitop_5f_InclusiveDecays_TuneCP5_13TeV-powheg-pythia8/RunIISummer20UL18NanoAODv9-106X_upgrade2018_realistic_v16_L1v1-v1/NANOAODSIM", "CMS", ".*root",7.175e+01,fracNegWeights=2.854e-03)

T_tWch_noFullyHad    = kreator.makeMCComponent("T_tWch_noFullyHad",    "/ST_tW_top_5f_NoFullyHadronicDecays_TuneCP5_13TeV-powheg-pythia8/RunIISummer20UL18NanoAODv9-106X_upgrade2018_realistic_v16_L1v1-v1/NANOAODSIM",     "CMS", ".*root",19.55)
Tbar_tWch_noFullyHad = kreator.makeMCComponent("Tbar_tWch_noFullyHad","/ST_tW_antitop_5f_NoFullyHadronicDecays_TuneCP5_13TeV_PDFWeights-powheg-pythia8/RunIISummer20UL18NanoAODv9-106X_upgrade2018_realistic_v16_L1v1-v2/NANOAODSIM", "CMS", ".*root",35.85*0.543,fracNegWeights=3.132e-05)

Tbar_tWch_incldecays = kreator.makeMCComponent("Tbar_tWch_incldecays","/ST_tW_antitop_5f_inclusiveDecays_TuneCP5_13TeV-powheg-pythia8/RunIISummer20UL18NanoAODv9-106X_upgrade2018_realistic_v16_L1v1-v2/NANOAODSIM", "CMS", ".*root",3.251e+01)
T_tWch_incldecays = kreator.makeMCComponent("T_tWch_incldecays","/ST_tW_top_5f_inclusiveDecays_TuneCP5_13TeV-powheg-pythia8/RunIISummer20UL18NanoAODv9-106X_upgrade2018_realistic_v16_L1v1-v2/NANOAODSIM", "CMS", ".*root",3.245e+01,fracNegWeights=2.273e-05)


Ts = [
    T_sch,
    Tbar_tch,T_tch,
    T_tWch_noFullyHad, Tbar_tWch_noFullyHad,Tbar_tWch_incldecays,T_tWch_incldecays

]


# # ===  DI-BOSONS

# # cross section from https://twiki.cern.ch/twiki/bin/view/CMS/SummaryTable1G25ns#Diboson
WW = kreator.makeMCComponent("WW", "/WW_TuneCP5_13TeV-pythia8/RunIISummer20UL18NanoAODv9-106X_upgrade2018_realistic_v16_L1v1-v1/NANOAODSIM", "CMS", ".*root", 63.21 * 1.82)
WZ = kreator.makeMCComponent("WZ", "/WZ_TuneCP5_13TeV-pythia8/RunIISummer20UL18NanoAODv9-106X_upgrade2018_realistic_v16_L1v1-v1/NANOAODSIM", "CMS", ".*root", 47.13)


WWTo2L2Nu = kreator.makeMCComponent("WWTo2L2Nu", "/WWTo2L2Nu_TuneCP5_13TeV-powheg-pythia8/RunIISummer20UL18NanoAODv9-106X_upgrade2018_realistic_v16_L1v1-v2/NANOAODSIM", "CMS", ".*root", 10.481 )

WZTo3LNu_fxfx = kreator.makeMCComponent("WZTo3LNu_fxfx", "/WZTo3LNu_TuneCP5_13TeV-amcatnloFXFX-pythia8/RunIISummer20UL18NanoAODv9-106X_upgrade2018_realistic_v16_L1v1-v2/NANOAODSIM", "CMS", ".*root", 5.063, fracNegWeights=0.189 )
WZTo3LNu_pow = kreator.makeMCComponent("WZTo3LNu_pow", "/WZTo3LNu_mllmin4p0_TuneCP5_13TeV-powheg-pythia8/RunIISummer20UL18NanoAODv9-106X_upgrade2018_realistic_v16_L1v1-v2/NANOAODSIM", "CMS", ".*root", 4.664*1.19 ) # powheg times k-factor


ZZTo4L = kreator.makeMCComponent("ZZTo4L", "/ZZTo4L_TuneCP5_13TeV_powheg_pythia8/RunIISummer20UL18NanoAODv9-106X_upgrade2018_realistic_v16_L1v1-v2/NANOAODSIM", "CMS", ".*root", 1.256)
ZZTo2L2Nu = kreator.makeMCComponent("ZZTo2L2Nu", "/ZZTo2L2Nu_TuneCP5_13TeV_powheg_pythia8/RunIISummer20UL18NanoAODv9-106X_upgrade2018_realistic_v16_L1v1-v1/NANOAODSIM", "CMS", ".*root", 0.564)

WGToLNuG = kreator.makeMCComponent("WGToLNuG", "/WGToLNuG_TuneCP5_13TeV-madgraphMLM-pythia8/RunIISummer20UL18NanoAODv9-106X_upgrade2018_realistic_v16_L1v1-v1/NANOAODSIM", "CMS", ".*root", 466.1)
ZGTo2LG =  kreator.makeMCComponent("ZGTo2LG", "/ZGToLLG_01J_5f_TuneCP5_13TeV-amcatnloFXFX-pythia8/RunIISummer20UL18NanoAODv9-106X_upgrade2018_realistic_v16_L1v1-v1/NANOAODSIM", "CMS", ".*root", 55.78)


GluGluToContinToZZTo4e      =  kreator.makeMCComponent("GluGluToContinToZZTo4e", "/GluGluToContinToZZTo4e_TuneCP5_13TeV-mcfm701-pythia8/RunIISummer20UL18NanoAODv9-106X_upgrade2018_realistic_v16_L1v1-v2/NANOAODSIM",  "CMS", ".*root", 0.00159*1.7) # generator cross section times 1.7 k-factor (SMP-19-001, AN-2019/004)
GluGluToContinToZZTo4mu     =  kreator.makeMCComponent("GluGluToContinToZZTo4mu", "/GluGluToContinToZZTo4mu_TuneCP5_13TeV-mcfm701-pythia8/RunIISummer20UL18NanoAODv9-106X_upgrade2018_realistic_v16_L1v1-v2/NANOAODSIM",  "CMS", ".*root", 0.00159*1.7) # generator cross section times 1.7 k-factor (SMP-19-001, AN-2019/004)
GluGluToContinToZZTo4tau    =  kreator.makeMCComponent("GluGluToContinToZZTo4tau", "/GluGluToContinToZZTo4tau_TuneCP5_13TeV-mcfm701-pythia8/RunIISummer20UL18NanoAODv9-106X_upgrade2018_realistic_v16_L1v1-v2/NANOAODSIM",  "CMS", ".*root", 0.00159*1.7) # generator cross section times 1.7 k-factor (SMP-19-001, AN-2019/004)
GluGluToContinToZZTo2e2mu   =  kreator.makeMCComponent("GluGluToContinToZZTo2e2mu", "/GluGluToContinToZZTo2e2mu_TuneCP5_13TeV-mcfm701-pythia8/RunIISummer20UL18NanoAODv9-106X_upgrade2018_realistic_v16_L1v1-v2/NANOAODSIM",  "CMS", ".*root", 0.00319*1.7) # generator cross section times 1.7 k-factor (SMP-19-001, AN-2019/004)
GluGluToContinToZZTo2e2tau  =  kreator.makeMCComponent("GluGluToContinToZZTo2e2tau", "/GluGluToContinToZZTo2e2tau_TuneCP5_13TeV-mcfm701-pythia8/RunIISummer20UL18NanoAODv9-106X_upgrade2018_realistic_v16_L1v1-v2/NANOAODSIM",  "CMS", ".*root", 0.00319*1.7) # generator cross section times 1.7 k-factor (SMP-19-001, AN-2019/004)
GluGluToContinToZZTo2mu2tau =  kreator.makeMCComponent("GluGluToContinToZZTo2mu2tau", "/GluGluToContinToZZTo2mu2tau_TuneCP5_13TeV-mcfm701-pythia8/RunIISummer20UL18NanoAODv9-106X_upgrade2018_realistic_v16_L1v1-v2/NANOAODSIM",  "CMS", ".*root", 0.00319*1.7) # generator cross section times 1.7 k-factor (SMP-19-001, AN-2019/004)
WLLJJ_WToLNu_EWK = kreator.makeMCComponent("WLLJJ_WToLNu_EWK","/WLLJJ_WToLNu_EWK_TuneCP5_13TeV_madgraph-madspin-pythia8/RunIISummer20UL18NanoAODv9-106X_upgrade2018_realistic_v16_L1v1-v2/NANOAODSIM",  "CMS", ".*root", 0.01628) # AN-19-156


ZZTo2Q2L              = kreator.makeMCComponent("ZZTo2Q2L", "/ZZTo2Q2L_mllmin4p0_TuneCP5_13TeV-amcatnloFXFX-pythia8/RunIISummer20UL18NanoAODv9-106X_upgrade2018_realistic_v16_L1v1-v1/NANOAODSIM", "CMS", ".*root", 3.689, fracNegWeights=0.1756)
WZTo2Q2L              = kreator.makeMCComponent("WZTo2Q2L", "/WZTo2Q2L_mllmin4p0_TuneCP5_13TeV-amcatnloFXFX-pythia8/RunIISummer20UL18NanoAODv9-106X_upgrade2018_realistic_v16_L1v1-v1/NANOAODSIM", "CMS", ".*root", 6.409, fracNegWeights=0.1883)
WZTo1L1Nu2Q           = kreator.makeMCComponent("WZTo1L1Nu2Q","/WZTo1L1Nu2Q_4f_TuneCP5_13TeV-amcatnloFXFX-pythia8/RunIISummer20UL18NanoAODv9-106X_upgrade2018_realistic_v16_L1v1-v1/NANOAODSIM", "CMS", ".*root", 9.370, fracNegWeights=2.049e-01)

#basepath_private = "/eos/cms/store/cmst3/group/dpsww/WZToLNuQQ01j_5f_amcatnloFxFx_nanov9UL2018/"
#WZToLNuQQ01j_5f_amcatnloFxFx    = kreator.makeMCComponent("WZToLNuQQ01j_5f_amcatnloFxFx","/WZTo1L1Nu2Q_4f_TuneCP5_13TeV-amcatnloFXFX-pythia8/RunIISummer20UL18NanoAODv9-106X_upgrade2018_realistic_v16_L1v1-v1/NANOAODSIM", "CMS", ".*root", 9.370, fracNegWeights=2.049e-01)
#WZToLNuQQ01j_5f_amcatnloFxFx.files   = [basepath_private+x for x in os.listdir(basepath_private) if os.path.isfile(os.path.join(basepath_private, x))]

WWTo1L1Nu2Q           = kreator.makeMCComponent("WWTo1L1Nu2Q","/WWTo1L1Nu2Q_4f_TuneCP5_13TeV-amcatnloFXFX-pythia8/RunIISummer20UL18NanoAODv9-106X_upgrade2018_realistic_v16_L1v1-v1/NANOAODSIM", "CMS", ".*root",5.090e+01,fracNegWeights=2.011e-01)


DiBosons = [
    WW,
    WZ, 
    WGToLNuG ,
    ZGTo2LG,
    WWTo2L2Nu,
    WZTo3LNu_fxfx,
    WZTo3LNu_pow,
    ZZTo4L,
    ZZTo2L2Nu,
    GluGluToContinToZZTo4e      ,
    GluGluToContinToZZTo4mu     ,
    GluGluToContinToZZTo4tau    ,
    GluGluToContinToZZTo2e2mu   ,
    GluGluToContinToZZTo2e2tau  ,
    GluGluToContinToZZTo2mu2tau ,
    WLLJJ_WToLNu_EWK,
    ZZTo2Q2L,
    WZTo2Q2L,
    WZTo1L1Nu2Q,
    WWTo1L1Nu2Q,
    #    WZToLNuQQ01j_5f_amcatnloFxFx,
]

# # ===  TRI-BOSONS

# # xsec from GenXSecAnalyzer
WWW        = kreator.makeMCComponent("WWW",        "/WWW_4F_TuneCP5_13TeV-amcatnlo-pythia8/RunIISummer20UL18NanoAODv9-106X_upgrade2018_realistic_v16_L1v1-v1/NANOAODSIM", "CMS", ".*root", 0.2086, fracNegWeights=0.063)
WWZ        = kreator.makeMCComponent("WWZ",        "/WWZ_4F_TuneCP5_13TeV-amcatnlo-pythia8/RunIISummer20UL18NanoAODv9-106X_upgrade2018_realistic_v16_L1v1-v1/NANOAODSIM", "CMS", ".*root",  0.1651, fracNegWeights=0.06 ) 
WZG        = kreator.makeMCComponent("WZG",        "/WZG_TuneCP5_13TeV-amcatnlo-pythia8/RunIISummer20UL18NanoAODv9-106X_upgrade2018_realistic_v16_L1v1-v1/NANOAODSIM", "CMS", ".*root", 0.04345, fracNegWeights=0.078)
WZZ        = kreator.makeMCComponent("WZZ",        "/WZZ_TuneCP5_13TeV-amcatnlo-pythia8/RunIISummer20UL18NanoAODv9-106X_upgrade2018_realistic_v16_L1v1-v1/NANOAODSIM", "CMS", ".*root", 0.05565, fracNegWeights=0.060)
WZZ_ext    = kreator.makeMCComponent("WZZ_ext",    "/WZZ_TuneCP5_13TeV-amcatnlo-pythia8/RunIISummer20UL18NanoAODv9-106X_upgrade2018_realistic_v16_L1v1_ext1-v2/NANOAODSIM", "CMS", ".*root", 0.05565, fracNegWeights=0.060)
ZZZ        = kreator.makeMCComponent("ZZZ",        "/ZZZ_TuneCP5_13TeV-amcatnlo-pythia8/RunIISummer20UL18NanoAODv9-106X_upgrade2018_realistic_v16_L1v1-v1/NANOAODSIM", "CMS", ".*root", 0.01398, fracNegWeights=0.060)
ZZZ_ext    = kreator.makeMCComponent("ZZZ_ext",    "/ZZZ_TuneCP5_13TeV-amcatnlo-pythia8/RunIISummer20UL18NanoAODv9-106X_upgrade2018_realistic_v16_L1v1_ext1-v2/NANOAODSIM", "CMS", ".*root", 0.01398, fracNegWeights=0.060)



TriBosons = [
    WWW,
    WWZ,
    WZG,
    WZZ, WZZ_ext,
    ZZZ, ZZZ_ext,

]

# # other Higgs processes

GGHZZ4L = kreator.makeMCComponent("GGHZZ4L", "/GluGluHToZZTo4L_M125_TuneCP5_13TeV_powheg2_JHUGenV7011_pythia8/RunIISummer20UL18NanoAODv9-106X_upgrade2018_realistic_v16_L1v1-v1/NANOAODSIM", "CMS", ".*root", 0.01212)
# # note: genXSecAna is incorrect because it doesn't know of the forced decay in pythia8. for the DiLeptonFilter sample, we take the filter efficiency from the ratio of the genXSecAna reports for the two samples
VHToNonbb = kreator.makeMCComponent("VHToNonbb", "/VHToNonbb_M125_TuneCP5_13TeV-amcatnloFXFX_madspin_pythia8/RunIISummer20UL18NanoAODv9-106X_upgrade2018_realistic_v16_L1v1-v2/NANOAODSIM", "CMS", ".*root", 0.9561, fracNegWeights=0.26) 
# #VHToNonbb_ll = kreator.makeMCComponent("VHToNonbb_ll", "/VHToNonbb_M125_DiLeptonFilter_TuneCP5_13TeV_amcatnloFXFX_madspin_pythia8/-FIXME-MISSING-/NANOAODSIM", "CMS", ".*root", 0.9561*0.08878/2.509, fracNegWeights=0.26) 

ZHToTauTau = kreator.makeMCComponent("ZHToTauTau", "/ZHToTauTau_M125_CP5_13TeV-powheg-pythia8_ext1/RunIISummer20UL18NanoAODv9-106X_upgrade2018_realistic_v16_L1v1-v2/NANOAODSIM", "CMS", ".*root", 0.05544)

Higgs = [
     GGHZZ4L,
    VHToNonbb,
    #VHToNonbb_ll,
    ZHToTauTau,
]





# # ----------------------------- summary ----------------------------------------

TTH_EFT = kreator.makeMCComponentFromJSON("TTH_EFT", "/TTH_EFT/RunIISummer20UL18NanoAODv9-Dummy/NANOAODSIM", os.environ['CMSSW_BASE']+'/src/CMGTools/RootTools/data/json/UL18_ttHJet_b1.json',0.5071, prefix='/pnfs/psi.ch/cms/trivcat/store/user/sesanche/NanoAOD_ULv9_jan21/')
THQ_EFT = kreator.makeMCComponentFromJSON("THQ_EFT", "/THQ_EFT/RunIISummer20UL18NanoAODv9-Dummy/NANOAODSIM", os.environ['CMSSW_BASE']+'/src/CMGTools/RootTools/data/json/UL18_tHq_b1.json',0.07096, prefix='/pnfs/psi.ch/cms/trivcat/store/user/sesanche/NanoAOD_ULv9_jan21/')
TllQ_EFT = kreator.makeMCComponentFromJSON("TllQ_EFT", "/TllQ_EFT/RunIISummer20UL18NanoAODv9-Dummy/NANOAODSIM", os.environ['CMSSW_BASE']+'/src/CMGTools/RootTools/data/json/UL18_tllq_b1.json',0.0758, prefix='/pnfs/psi.ch/cms/trivcat/store/user/sesanche/NanoAOD_ULv9_jan21/')
TTll_EFT = kreator.makeMCComponentFromJSON("TTll_EFT", "/TTll_EFT/RunIISummer20UL18NanoAODv9-Dummy/NANOAODSIM", os.environ['CMSSW_BASE']+'/src/CMGTools/RootTools/data/json/UL18_ttllJet_b1.json',0.2529, prefix='/pnfs/psi.ch/cms/trivcat/store/user/sesanche/NanoAOD_ULv9_jan21/')
TTln_EFT = kreator.makeMCComponentFromJSON("TTln_EFT", "/TTll_EFT/RunIISummer20UL18NanoAODv9-Dummy/NANOAODSIM", os.environ['CMSSW_BASE']+'/src/CMGTools/RootTools/data/json/UL18_ttlnuJet_b1.json',0.2043, prefix='/pnfs/psi.ch/cms/trivcat/store/user/sesanche/NanoAOD_ULv9_jan21/')
TTTT_EFT = kreator.makeMCComponentFromJSON("TTTT_EFT", "/TTTT_EFT/RunIISummer20UL18NanoAODv9-Dummy/NANOAODSIM", os.environ['CMSSW_BASE']+'/src/CMGTools/RootTools/data/json/UL18_tttt_b4.json', 0.009103, prefix='/pnfs/psi.ch/cms/trivcat/store/user/sesanche/NanoAOD_ULv9_jan21/')

EFT = [TTH_EFT, THQ_EFT, TllQ_EFT, TTll_EFT, TTln_EFT, TTTT_EFT]


mcSamples =  Ws + DYs +  TTs + Ts + DiBosons + TriBosons + Higgs + QCD_bcToE + QCD_EMs + QCD_Mus + EFT 
 # VJetsQQHT +


samples = mcSamples

# ---------------------------------------------------------------------

if __name__ == "__main__":
    from CMGTools.RootTools.samples.tools import runMain
    runMain(samples, localobjs=locals())
