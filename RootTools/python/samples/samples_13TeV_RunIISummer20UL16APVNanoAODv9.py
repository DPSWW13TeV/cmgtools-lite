# COMPONENT CREATOR
from CMGTools.RootTools.samples.ComponentCreator import ComponentCreator
kreator = ComponentCreator()
import os 

basepath_eos="/eos/cms/store/group/phys_smp/ec/anmehta/Combined_aTGC_Oct2024_UL16preVFP/"
WmZToLmNujj_01j_aTGC_pTZ_150toInf_mWV_150to600=kreator.makeMCComponentSimple('WmZToLmNujj_01j_aTGC_pTZ_150toInf_mWV_150to600',"/WZToLNujj_01j_aTGC/RunIISummer20UL18NanoAODv9-Dummy/NANOAODSIM",basepath_eos,5.401e-01*0.69911,prefix='root://xrootd-cms.infn.it/')
WmZToLmNujj_01j_aTGC_pTZ_150toInf_mWV_600to800=kreator.makeMCComponentSimple('WmZToLmNujj_01j_aTGC_pTZ_150toInf_mWV_600to800',"/WZToLNujj_01j_aTGC/RunIISummer20UL18NanoAODv9-Dummy/NANOAODSIM",basepath_eos,8.544e-02*0.69911,prefix='root://xrootd-cms.infn.it/')
WmZToLmNujj_01j_aTGC_pTZ_150toInf_mWV_800toInf=kreator.makeMCComponentSimple('WmZToLmNujj_01j_aTGC_pTZ_150toInf_mWV_800toInf',"/WZToLNujj_01j_aTGC/RunIISummer20UL18NanoAODv9-Dummy/NANOAODSIM",basepath_eos,9.101e-02*0.69911,prefix='root://xrootd-cms.infn.it/')
WpZToLpNujj_01j_aTGC_pTZ_150toInf_mWV_150to600=kreator.makeMCComponentSimple('WpZToLpNujj_01j_aTGC_pTZ_150toInf_mWV_150to600',"/WZToLNujj_01j_aTGC/RunIISummer20UL18NanoAODv9-Dummy/NANOAODSIM",basepath_eos,8.658e-01*0.69911,prefix='root://xrootd-cms.infn.it/')
WpZToLpNujj_01j_aTGC_pTZ_150toInf_mWV_600to800=kreator.makeMCComponentSimple('WpZToLpNujj_01j_aTGC_pTZ_150toInf_mWV_600to800',"/WZToLNujj_01j_aTGC/RunIISummer20UL18NanoAODv9-Dummy/NANOAODSIM",basepath_eos,1.561e-01*0.69911,prefix='root://xrootd-cms.infn.it/')
WpZToLpNujj_01j_aTGC_pTZ_150toInf_mWV_800toInf=kreator.makeMCComponentSimple('WpZToLpNujj_01j_aTGC_pTZ_150toInf_mWV_800toInf',"/WZToLNujj_01j_aTGC/RunIISummer20UL18NanoAODv9-Dummy/NANOAODSIM",basepath_eos,2.199e-01*0.69911,prefix='root://xrootd-cms.infn.it/')

WmWpToLmNujj_01j_aTGC_pTW_150toInf_mWV_150to600=kreator.makeMCComponentSimple('WmWpToLmNujj_01j_aTGC_pTW_150toInf_mWV_150to600',"/WWToLNujj_01j_aTGC/RunIISummer20UL18NanoAODv9-Dummy/NANOAODSIM",basepath_eos,2.109*0.6741,prefix='root://xrootd-cms.infn.it/')
WmWpToLmNujj_01j_aTGC_pTW_150toInf_mWV_600to800=kreator.makeMCComponentSimple('WmWpToLmNujj_01j_aTGC_pTW_150toInf_mWV_600to800',"/WWToLNujj_01j_aTGC/RunIISummer20UL18NanoAODv9-Dummy/NANOAODSIM",basepath_eos,3.568e-01*0.6741,prefix='root://xrootd-cms.infn.it/')
WmWpToLmNujj_01j_aTGC_pTW_150toInf_mWV_800toInf=kreator.makeMCComponentSimple('WmWpToLmNujj_01j_aTGC_pTW_150toInf_mWV_800toInf',"/WWToLNujj_01j_aTGC/RunIISummer20UL18NanoAODv9-Dummy/NANOAODSIM",basepath_eos,3.806e-01*0.6741,prefix='root://xrootd-cms.infn.it/')
WpWmToLpNujj_01j_aTGC_pTW_150toInf_mWV_150to600=kreator.makeMCComponentSimple('WpWmToLpNujj_01j_aTGC_pTW_150toInf_mWV_150to600',"/WWToLNujj_01j_aTGC/RunIISummer20UL18NanoAODv9-Dummy/NANOAODSIM",basepath_eos,2.014e+00*0.6741,prefix='root://xrootd-cms.infn.it/')
WpWmToLpNujj_01j_aTGC_pTW_150toInf_mWV_600to800=kreator.makeMCComponentSimple('WpWmToLpNujj_01j_aTGC_pTW_150toInf_mWV_600to800',"/WWToLNujj_01j_aTGC/RunIISummer20UL18NanoAODv9-Dummy/NANOAODSIM",basepath_eos,3.467e-01*0.6741,prefix='root://xrootd-cms.infn.it/')
WpWmToLpNujj_01j_aTGC_pTW_150toInf_mWV_800toInf=kreator.makeMCComponentSimple('WpWmToLpNujj_01j_aTGC_pTW_150toInf_mWV_800toInf',"/WWToLNujj_01j_aTGC/RunIISummer20UL18NanoAODv9-Dummy/NANOAODSIM",basepath_eos,3.713e-01*0.6741,prefix='root://xrootd-cms.infn.it/')

##ambasepath_smeft="/eos/cms/store/cmst3/group/dpsww/SMEFT_samples/2016/"
##amWmZToLmNujj_SMEFT_LO=kreator.makeMCComponentSimple('WmZToLmNujj_SMEFT_LO',"/WmZToLmNujj_SMEFT_LO/RunIISummer20UL18NanoAODv9-Dummy/NANOAODSIM",basepath_smeft,3.10204*0.69911,prefix='root://xrootd-cms.infn.it/')
##amWpZToLpNujj_SMEFT_LO=kreator.makeMCComponentSimple('WpZToLpNujj_SMEFT_LO',"/WpZToLpNujj_SMEFT_LO/RunIISummer20UL18NanoAODv9-Dummy/NANOAODSIM",basepath_smeft,4.91575*0.69911,prefix='root://xrootd-cms.infn.it/')
##amWpWmToLpNujj_SMEFT_LO=kreator.makeMCComponentSimple('WpWmToLpNujj_SMEFT_LO',"/WpWmToLpNujj_SMEFT_LO/RunIISummer20UL18NanoAODv9-Dummy/NANOAODSIM",basepath_smeft,21.4765*0.69911,prefix='root://xrootd-cms.infn.it/')
##amWmWpToLmNujj_SMEFT_LO=kreator.makeMCComponentSimple('WmWpToLmNujj_SMEFT_LO',"/WmWpToLmNujj_SMEFT_LO/RunIISummer20UL18NanoAODv9-Dummy/NANOAODSIM",basepath_smeft,20.736*0.69911,prefix='root://xrootd-cms.infn.it/')


ZZTo2Q2L              = kreator.makeMCComponent("ZZTo2Q2L", "/ZZTo2Q2L_mllmin4p0_TuneCP5_13TeV-amcatnloFXFX-pythia8/RunIISummer20UL16NanoAODAPVv9-106X_mcRun2_asymptotic_preVFP_v11-v1/NANOAODSIM", "CMS", ".*root", 3.689, fracNegWeights=0.1756)
WZTo1L1Nu2Q           = kreator.makeMCComponent("WZTo1L1Nu2Q","/WZTo1L1Nu2Q_4f_TuneCP5_13TeV-amcatnloFXFX-pythia8/RunIISummer20UL16NanoAODAPVv9-106X_mcRun2_asymptotic_preVFP_v11-v1/NANOAODSIM", "CMS", ".*root", 9.370, fracNegWeights=2.049e-01)
WWTo1L1Nu2Q           = kreator.makeMCComponent("WWTo1L1Nu2Q","/WWTo1L1Nu2Q_4f_TuneCP5_13TeV-amcatnloFXFX-pythia8/RunIISummer20UL16NanoAODAPVv9-106X_mcRun2_asymptotic_preVFP_v11-v1/NANOAODSIM", "CMS", ".*root",5.090e+01,fracNegWeights=2.011e-01)

DiBosons = [ZZTo2Q2L,
            WZTo1L1Nu2Q,
            WWTo1L1Nu2Q,
            WmWpToLmNujj_01j_aTGC_pTW_150toInf_mWV_150to600,
            WpWmToLpNujj_01j_aTGC_pTW_150toInf_mWV_150to600,
            WpWmToLpNujj_01j_aTGC_pTW_150toInf_mWV_600to800,
            WpWmToLpNujj_01j_aTGC_pTW_150toInf_mWV_800toInf,
            WmWpToLmNujj_01j_aTGC_pTW_150toInf_mWV_600to800,
            WmWpToLmNujj_01j_aTGC_pTW_150toInf_mWV_800toInf,
            WmZToLmNujj_01j_aTGC_pTZ_150toInf_mWV_150to600,
            WmZToLmNujj_01j_aTGC_pTZ_150toInf_mWV_600to800,
            WpZToLpNujj_01j_aTGC_pTZ_150toInf_mWV_800toInf,
            WpZToLpNujj_01j_aTGC_pTZ_150toInf_mWV_150to600,
            WpZToLpNujj_01j_aTGC_pTZ_150toInf_mWV_600to800,
            WmZToLmNujj_01j_aTGC_pTZ_150toInf_mWV_800toInf,
]



WminusH = kreator.makeMCComponent("WminusH","/WminusH_HToBB_WToLNu_M-125_TuneCP5_13TeV-powheg-pythia8/RunIISummer20UL16NanoAODAPVv9-106X_mcRun2_asymptotic_preVFP_v11-v1/NANOAODSIM", "CMS", ".*root",1.770e-01,fracNegWeights=2.703e-02)
WplusH = kreator.makeMCComponent("WplusH","/WplusH_HToBB_WToLNu_M-125_TuneCP5_13TeV-powheg-pythia8/RunIISummer20UL16NanoAODAPVv9-106X_mcRun2_asymptotic_preVFP_v11-v1/NANOAODSIM", "CMS", ".*root", 2.832e-01,fracNegWeights=2.980e-02)
ZH = kreator.makeMCComponent("ZH","/ZH_HToBB_ZToLL_M-125_TuneCP5_13TeV-powheg-pythia8/RunIISummer20UL16NanoAODAPVv9-106X_mcRun2_asymptotic_preVFP_v11-v1/NANOAODSIM", "CMS", ".*root", 7.977e-02,fracNegWeights=2.661e-02)
VHToNonbb = kreator.makeMCComponent("VHToNonbb", "/VHToNonbb_M125_TuneCP5_13TeV-amcatnloFXFX_madspin_pythia8/RunIISummer20UL16NanoAODAPVv9-106X_mcRun2_asymptotic_preVFP_v11-v2/NANOAODSIM", "CMS", ".*root", 0.9561, fracNegWeights=0.26) 


Higgs = [
    ZH,WminusH,WplusH,
    VHToNonbb,

]

WJetsToLNu_NLO            = kreator.makeMCComponent("WJetsToLNu_NLO","/WJetsToLNu_TuneCP5_13TeV-amcatnloFXFX-pythia8/RunIISummer20UL16NanoAODAPVv9-106X_mcRun2_asymptotic_preVFP_v11-v2/NANOAODSIM", "CMS", ".*root",6.748e+04,fracNegWeights=1.589e-01)
WJetsToLNu_012JetsNLO_34JetsLO         = kreator.makeMCComponent("WJetsToLNu_012JetsNLO_34JetsLO","/WJetsToLNu_012JetsNLO_34JetsLO_EWNLOcorr_13TeV-sherpa/RunIISummer20UL16NanoAODAPVv9-106X_mcRun2_asymptotic_preVFP_v11-v1/NANOAODSIM", "CMS", ".*root",61526.7)
WJetsToLNu_HT70to100      = kreator.makeMCComponent("WJetsToLNu_HT70to100",   "/WJetsToLNu_HT-70To100_TuneCP5_13TeV-madgraphMLM-pythia8/RunIISummer20UL16NanoAODAPVv9-106X_mcRun2_asymptotic_preVFP_v11-v1/NANOAODSIM", "CMS", ".*root",1271*1.21)
WJetsToLNu_HT100to200     = kreator.makeMCComponent("WJetsToLNu_HT100to200",  "/WJetsToLNu_HT-100To200_TuneCP5_13TeV-madgraphMLM-pythia8/RunIISummer20UL16NanoAODAPVv9-106X_mcRun2_asymptotic_preVFP_v11-v1/NANOAODSIM", "CMS", ".*root",1253*1.21) 
WJetsToLNu_HT200to400     = kreator.makeMCComponent("WJetsToLNu_HT200to400",  "/WJetsToLNu_HT-200To400_TuneCP5_13TeV-madgraphMLM-pythia8/RunIISummer20UL16NanoAODAPVv9-106X_mcRun2_asymptotic_preVFP_v11-v1/NANOAODSIM", "CMS", ".*root",335.9*1.21) 
WJetsToLNu_HT400to600     = kreator.makeMCComponent("WJetsToLNu_HT400to600",  "/WJetsToLNu_HT-400To600_TuneCP5_13TeV-madgraphMLM-pythia8/RunIISummer20UL16NanoAODAPVv9-106X_mcRun2_asymptotic_preVFP_v11-v1/NANOAODSIM", "CMS", ".*root",45.21*1.21) 
WJetsToLNu_HT600to800     = kreator.makeMCComponent("WJetsToLNu_HT600to800",  "/WJetsToLNu_HT-600To800_TuneCP5_13TeV-madgraphMLM-pythia8/RunIISummer20UL16NanoAODAPVv9-106X_mcRun2_asymptotic_preVFP_v11-v1/NANOAODSIM", "CMS", ".*root",10.99*1.21) 
WJetsToLNu_HT800to1200    = kreator.makeMCComponent("WJetsToLNu_HT800to1200", "/WJetsToLNu_HT-800To1200_TuneCP5_13TeV-madgraphMLM-pythia8/RunIISummer20UL16NanoAODAPVv9-106X_mcRun2_asymptotic_preVFP_v11-v1/NANOAODSIM", "CMS", ".*root",4.936*1.21) 
WJetsToLNu_HT1200to2500   = kreator.makeMCComponent("WJetsToLNu_HT1200to2500","/WJetsToLNu_HT-1200To2500_TuneCP5_13TeV-madgraphMLM-pythia8/RunIISummer20UL16NanoAODAPVv9-106X_mcRun2_asymptotic_preVFP_v11-v1/NANOAODSIM", "CMS", ".*root",1.156*1.21) 
WJetsToLNu_HT2500toInf    = kreator.makeMCComponent("WJetsToLNu_HT2500toInf", "/WJetsToLNu_HT-2500ToInf_TuneCP5_13TeV-madgraphMLM-pythia8/RunIISummer20UL16NanoAODAPVv9-106X_mcRun2_asymptotic_preVFP_v11-v2/NANOAODSIM", "CMS", ".*root",0.0263*1.21) 
WJetsToLNu_LO             = kreator.makeMCComponent("WJetsToLNu_LO","/WJetsToLNu_TuneCP5_13TeV-madgraphMLM-pythia8/RunIISummer20UL16NanoAODAPVv9-20UL16APVJMENano_106X_mcRun2_asymptotic_preVFP_v11-v2/NANOAODSIM", "CMS", ".*root", 3* 20508.9) 



WJetsToLNu_Pt100To250 = kreator.makeMCComponent("WJetsToLNu_Pt100To250","/WJetsToLNu_Pt-100To250_MatchEWPDG20_TuneCP5_13TeV-amcatnloFXFX-pythia8/RunIISummer20UL16NanoAODAPVv9-106X_mcRun2_asymptotic_preVFP_v11-v1/NANOAODSIM", "CMS", ".*root", 763.7,fracNegWeights=3.106e-01)
WJetsToLNu_Pt250To400 = kreator.makeMCComponent("WJetsToLNu_Pt250To400","/WJetsToLNu_Pt-250To400_MatchEWPDG20_TuneCP5_13TeV-amcatnloFXFX-pythia8/RunIISummer20UL16NanoAODAPVv9-106X_mcRun2_asymptotic_preVFP_v11-v1/NANOAODSIM", "CMS", ".*root", 27.55,fracNegWeights=2.992e-01)
WJetsToLNu_Pt400To600 = kreator.makeMCComponent("WJetsToLNu_Pt400To600","/WJetsToLNu_Pt-400To600_MatchEWPDG20_TuneCP5_13TeV-amcatnloFXFX-pythia8/RunIISummer20UL16NanoAODAPVv9-106X_mcRun2_asymptotic_preVFP_v11-v1/NANOAODSIM", "CMS", ".*root", 3.477,fracNegWeights=2.981e-01)
WJetsToLNu_Pt600ToInf = kreator.makeMCComponent("WJetsToLNu_Pt600ToInf","/WJetsToLNu_Pt-600ToInf_MatchEWPDG20_TuneCP5_13TeV-amcatnloFXFX-pythia8/RunIISummer20UL16NanoAODAPVv9-106X_mcRun2_asymptotic_preVFP_v11-v1/NANOAODSIM", "CMS", ".*root", 0.5415,fracNegWeights=2.725e-01)
WJetsToLNu_0J = kreator.makeMCComponent("WJetsToLNu_0J","/WJetsToLNu_0J_TuneCP5_13TeV-amcatnloFXFX-pythia8/RunIISummer20UL16NanoAODAPVv9-106X_mcRun2_asymptotic_preVFP_v11-v1/NANOAODSIM", "CMS", ".*root", 53330,fracNegWeights=9.929e-02)
WJetsToLNu_1J = kreator.makeMCComponent("WJetsToLNu_1J","/WJetsToLNu_1J_TuneCP5_13TeV-amcatnloFXFX-pythia8/RunIISummer20UL16NanoAODAPVv9-106X_mcRun2_asymptotic_preVFP_v11-v1/NANOAODSIM", "CMS", ".*root", 8875,fracNegWeights=2.579e-01)
WJetsToLNu_2J = kreator.makeMCComponent("WJetsToLNu_2J","/WJetsToLNu_2J_TuneCP5_13TeV-amcatnloFXFX-pythia8/RunIISummer20UL16NanoAODAPVv9-106X_mcRun2_asymptotic_preVFP_v11-v1/NANOAODSIM", "CMS", ".*root", 3338,fracNegWeights= 3.385e-01)


Ws = [ 
    WJetsToLNu_0J,
    WJetsToLNu_1J,
    WJetsToLNu_2J,
    WJetsToLNu_Pt100To250,
    WJetsToLNu_Pt250To400,
    WJetsToLNu_Pt400To600,
    WJetsToLNu_Pt600ToInf,
    #WJetsToLNu_LO,
    #W2JetsToLNu_LO,
    #W3JetsToLNu_LO,
    #W4JetsToLNu_LO,
    WJetsToLNu_NLO,
    WJetsToLNu_012JetsNLO_34JetsLO,
]

WJetsToLNuHT = [
                WJetsToLNu_HT70to100,
                WJetsToLNu_HT100to200,
                WJetsToLNu_HT200to400,
                WJetsToLNu_HT400to600,
                WJetsToLNu_HT600to800,
                WJetsToLNu_HT800to1200,
                WJetsToLNu_HT1200to2500,
                WJetsToLNu_HT2500toInf,
]




# # QCD enriched (cross sections form genXSecAna)
QCD_Mu15            = kreator.makeMCComponent("QCD_Mu15"            , "/QCD_Pt-20_MuEnrichedPt15_TuneCP5_13TeV-pythia8/RunIISummer20UL16NanoAODAPVv9-106X_mcRun2_asymptotic_preVFP_v11-v1/NANOAODSIM"      , "CMS" , ".*root", 237800) 
QCD_Pt20to30_Mu5    = kreator.makeMCComponent("QCD_Pt20to30_Mu5"    , "/QCD_Pt-20To30_MuEnrichedPt5_TuneCP5_13TeV-pythia8/RunIISummer20UL16NanoAODAPVv9-106X_mcRun2_asymptotic_preVFP_v11-v2/NANOAODSIM"   , "CMS" , ".*root", 2.49e+06)   
QCD_Pt30to50_Mu5    = kreator.makeMCComponent("QCD_Pt30to50_Mu5"    , "/QCD_Pt-30To50_MuEnrichedPt5_TuneCP5_13TeV-pythia8/RunIISummer20UL16NanoAODAPVv9-106X_mcRun2_asymptotic_preVFP_v11-v2/NANOAODSIM"   , "CMS" , ".*root", 1.364e+06)     
QCD_Pt50to80_Mu5    = kreator.makeMCComponent("QCD_Pt50to80_Mu5"    , "/QCD_Pt-50To80_MuEnrichedPt5_TuneCP5_13TeV-pythia8/RunIISummer20UL16NanoAODAPVv9-106X_mcRun2_asymptotic_preVFP_v11-v2/NANOAODSIM"   , "CMS" , ".*root", 377400)
QCD_Pt80to120_Mu5   = kreator.makeMCComponent("QCD_Pt80to120_Mu5"   , "/QCD_Pt-80To120_MuEnrichedPt5_TuneCP5_13TeV-pythia8/RunIISummer20UL16NanoAODAPVv9-106X_mcRun2_asymptotic_preVFP_v11-v2/NANOAODSIM"  , "CMS" , ".*root", 88350)     
QCD_Pt120to170_Mu5  = kreator.makeMCComponent("QCD_Pt120to170_Mu5"  , "/QCD_Pt-120To170_MuEnrichedPt5_TuneCP5_13TeV-pythia8/RunIISummer20UL16NanoAODAPVv9-106X_mcRun2_asymptotic_preVFP_v11-v2/NANOAODSIM" , "CMS" , ".*root", 21250)    
QCD_Pt170to300_Mu5  = kreator.makeMCComponent("QCD_Pt170to300_Mu5"  , "/QCD_Pt-170To300_MuEnrichedPt5_TuneCP5_13TeV-pythia8/RunIISummer20UL16NanoAODAPVv9-106X_mcRun2_asymptotic_preVFP_v11-v2/NANOAODSIM" , "CMS" , ".*root", 6969) 
QCD_Pt300to470_Mu5  = kreator.makeMCComponent("QCD_Pt300to470_Mu5"  , "/QCD_Pt-300To470_MuEnrichedPt5_TuneCP5_13TeV-pythia8/RunIISummer20UL16NanoAODAPVv9-106X_mcRun2_asymptotic_preVFP_v11-v2/NANOAODSIM" , "CMS" , ".*root", 619.5)
QCD_Pt470to600_Mu5  = kreator.makeMCComponent("QCD_Pt470to600_Mu5"  , "/QCD_Pt-470To600_MuEnrichedPt5_TuneCP5_13TeV-pythia8/RunIISummer20UL16NanoAODAPVv9-106X_mcRun2_asymptotic_preVFP_v11-v2/NANOAODSIM" , "CMS" , ".*root", 58.9)
QCD_Pt600to800_Mu5  = kreator.makeMCComponent("QCD_Pt600to800_Mu5"  , "/QCD_Pt-600To800_MuEnrichedPt5_TuneCP5_13TeV-pythia8/RunIISummer20UL16NanoAODAPVv9-106X_mcRun2_asymptotic_preVFP_v11-v2/NANOAODSIM" , "CMS" , ".*root", 18.36)
QCD_Pt800to1000_Mu5 = kreator.makeMCComponent("QCD_Pt800to1000_Mu5" , "/QCD_Pt-800To1000_MuEnrichedPt5_TuneCP5_13TeV-pythia8/RunIISummer20UL16NanoAODAPVv9-106X_mcRun2_asymptotic_preVFP_v11-v2/NANOAODSIM", "CMS" , ".*root", 3.253)
#QCD_Pt1000toInf_Mu5 = kreator.makeMCComponent("QCD_Pt1000toInf_Mu5" , "/QCD_Pt-1000_MuEnrichedPt5_TuneCP5_13TeV-pythia8/RunIISummer20UL16NanoAODAPVv9-106X_mcRun2_asymptotic_preVFP_v11-v2/NANOAODSIMM"    , "CMS" , ".*root", 1.075)

QCD_Mu5s = [QCD_Mu15,
    QCD_Pt20to30_Mu5,
    QCD_Pt30to50_Mu5,
    QCD_Pt50to80_Mu5,
    QCD_Pt80to120_Mu5,
    QCD_Pt120to170_Mu5,
    QCD_Pt170to300_Mu5,
    QCD_Pt300to470_Mu5,QCD_Pt470to600_Mu5,QCD_Pt600to800_Mu5,QCD_Pt800to1000_Mu5 #,QCD_Pt1000toInf_Mu5
 ]
QCD_Mus = QCD_Mu5s 

# # QCD EMEnr  (cross sections form genXSecAna)
QCD_Pt15to20_EMEnriched   = kreator.makeMCComponent("QCD_Pt15to20_EMEnriched"  ,"/QCD_Pt-15to20_EMEnriched_TuneCP5_13TeV-pythia8/RunIISummer20UL16NanoAODAPVv9-106X_mcRun2_asymptotic_preVFP_v11-v2/NANOAODSIM"  , "CMS", ".*root",  1.33e+06)
QCD_Pt20to30_EMEnriched   = kreator.makeMCComponent("QCD_Pt20to30_EMEnriched"  ,"/QCD_Pt-20to30_EMEnriched_TuneCP5_13TeV-pythia8/RunIISummer20UL16NanoAODAPVv9-106X_mcRun2_asymptotic_preVFP_v11-v1/NANOAODSIM"  , "CMS", ".*root", 4.928e+06)
QCD_Pt30to50_EMEnriched   = kreator.makeMCComponent("QCD_Pt30to50_EMEnriched"  ,"/QCD_Pt-30to50_EMEnriched_TuneCP5_13TeV-pythia8/RunIISummer20UL16NanoAODAPVv9-106X_mcRun2_asymptotic_preVFP_v11-v2/NANOAODSIM"  , "CMS", ".*root",  6.41e+06)
QCD_Pt50to80_EMEnriched   = kreator.makeMCComponent("QCD_Pt50to80_EMEnriched", "/QCD_Pt-50to80_EMEnriched_TuneCP5_13TeV-pythia8/RunIISummer20UL16NanoAODAPVv9-106X_mcRun2_asymptotic_preVFP_v11-v2/NANOAODSIM"   , "CMS", ".*root",  1.986e+06)
QCD_Pt80to120_EMEnriched  = kreator.makeMCComponent("QCD_Pt80to120_EMEnriched" ,"/QCD_Pt-80to120_EMEnriched_TuneCP5_13TeV-pythia8/RunIISummer20UL16NanoAODAPVv9-106X_mcRun2_asymptotic_preVFP_v11-v2/NANOAODSIM" , "CMS", ".*root",  370900)
QCD_Pt120to170_EMEnriched = kreator.makeMCComponent("QCD_Pt120to170_EMEnriched","/QCD_Pt-120to170_EMEnriched_TuneCP5_13TeV-pythia8/RunIISummer20UL16NanoAODAPVv9-106X_mcRun2_asymptotic_preVFP_v11-v2/NANOAODSIM", "CMS", ".*root",  66760) 
QCD_Pt170to300_EMEnriched = kreator.makeMCComponent("QCD_Pt170to300_EMEnriched","/QCD_Pt-170to300_EMEnriched_TuneCP5_13TeV-pythia8/RunIISummer20UL16NanoAODAPVv9-106X_mcRun2_asymptotic_preVFP_v11-v2/NANOAODSIM", "CMS", ".*root",  16430) 
QCD_Pt300toInf_EMEnriched = kreator.makeMCComponent("QCD_Pt300toInf_EMEnriched","/QCD_Pt-300toInf_EMEnriched_TuneCP5_13TeV-pythia8/RunIISummer20UL16NanoAODAPVv9-106X_mcRun2_asymptotic_preVFP_v11-v2/NANOAODSIM", "CMS", ".*root",  1101) #  https://cms-pdmv.cern.ch/mcm/requests?prepid=HIG-RunIISummer20UL16GENAPV-00054

QCD_EMs = [
    QCD_Pt15to20_EMEnriched,
    QCD_Pt20to30_EMEnriched,
    QCD_Pt30to50_EMEnriched,
    QCD_Pt50to80_EMEnriched,
    QCD_Pt80to120_EMEnriched,
    QCD_Pt120to170_EMEnriched,
    QCD_Pt170to300_EMEnriched,
    QCD_Pt300toInf_EMEnriched
 ]

QCD_Pt15to20_bcToE   = kreator.makeMCComponent("QCD_Pt15to20_bcToE",   "/QCD_Pt_15to20_bcToE_TuneCP5_13TeV_pythia8/RunIISummer20UL16NanoAODAPVv9-106X_mcRun2_asymptotic_preVFP_v11-v1/NANOAODSIM"  , "CMS", ".*root", 187000)
QCD_Pt20to30_bcToE   = kreator.makeMCComponent("QCD_Pt20to30_bcToE",   "/QCD_Pt_20to30_bcToE_TuneCP5_13TeV_pythia8/RunIISummer20UL16NanoAODAPVv9-106X_mcRun2_asymptotic_preVFP_v11-v2/NANOAODSIM"  , "CMS", ".*root",313500)
QCD_Pt30to80_bcToE   = kreator.makeMCComponent("QCD_Pt30to80_bcToE",   "/QCD_Pt_30to80_bcToE_TuneCP5_13TeV_pythia8/RunIISummer20UL16NanoAODAPVv9-106X_mcRun2_asymptotic_preVFP_v11-v2/NANOAODSIM"  , "CMS", ".*root", 361500)
QCD_Pt80to170_bcToE  = kreator.makeMCComponent("QCD_Pt80to170_bcToE",  "/QCD_Pt_80to170_bcToE_TuneCP5_13TeV_pythia8/RunIISummer20UL16NanoAODAPVv9-106X_mcRun2_asymptotic_preVFP_v11-v2/NANOAODSIM" , "CMS", ".*root", 33770)
QCD_Pt170to250_bcToE = kreator.makeMCComponent("QCD_Pt170to250_bcToE", "/QCD_Pt_170to250_bcToE_TuneCP5_13TeV_pythia8/RunIISummer20UL16NanoAODAPVv9-106X_mcRun2_asymptotic_preVFP_v11-v2/NANOAODSIM", "CMS", ".*root", 2126)
QCD_Pt250toInf_bcToE = kreator.makeMCComponent("QCD_Pt250toInf_bcToE", "/QCD_Pt_250toInf_bcToE_TuneCP5_13TeV_pythia8/RunIISummer20UL16NanoAODAPVv9-106X_mcRun2_asymptotic_preVFP_v11-v2/NANOAODSIM", "CMS", ".*root", 563.1)

QCD_bcToE = [
    QCD_Pt15to20_bcToE,
    QCD_Pt20to30_bcToE,
    QCD_Pt30to80_bcToE,
    QCD_Pt80to170_bcToE,
    QCD_Pt170to250_bcToE,
    QCD_Pt250toInf_bcToE,
]

# # ====== W + Jets ======
                                                          

TTSemi_pow = kreator.makeMCComponent("TTSemi_pow", "/TTToSemiLeptonic_TuneCP5_13TeV-powheg-pythia8/RunIISummer20UL16NanoAODAPVv9-106X_mcRun2_asymptotic_preVFP_v11-v1/NANOAODSIM", "CMS", ".*root", 831.76*2*(3*0.108)*(1-3*0.108) )
TT_mttp7kto1k = kreator.makeMCComponent("TT_mttp7kto1k","/TT_Mtt-700to1000_TuneCP5_13TeV-powheg-pythia8/RunIISummer20UL16NanoAODAPVv9-106X_mcRun2_asymptotic_preVFP_v11-v1/NANOAODSIM", "CMS", ".*root", 6.472e+01*1.21)
TT_mtt1ktoinf = kreator.makeMCComponent("TT_mtt1ktoinf","/TT_Mtt-1000toInf_TuneCP5_13TeV-powheg-pythia8/RunIISummer20UL16NanoAODAPVv9-106X_mcRun2_asymptotic_preVFP_v11-v1/NANOAODSIM", "CMS", ".*root", 1.644e+01*1.21)


T_sch = kreator.makeMCComponent("T_sch", "/ST_s-channel_4f_leptonDecays_TuneCP5_13TeV-amcatnlo-pythia8/RunIISummer20UL16NanoAODAPVv9-106X_mcRun2_asymptotic_preVFP_v11-v1/NANOAODSIM", "CMS", ".*root", 3.549e+00)
T_tch = kreator.makeMCComponent("T_tch", "/ST_t-channel_top_4f_InclusiveDecays_TuneCP5_13TeV-powheg-madspin-pythia8/RunIISummer20UL16NanoAODAPVv9-106X_mcRun2_asymptotic_preVFP_v11-v1/NANOAODSIM",           "CMS", ".*root", 136.02)
TBar_tch = kreator.makeMCComponent("TBar_tch", "/ST_t-channel_antitop_4f_InclusiveDecays_TuneCP5_13TeV-powheg-madspin-pythia8/RunIISummer20UL16NanoAODAPVv9-106X_mcRun2_asymptotic_preVFP_v11-v1/NANOAODSIM", "CMS", ".*root", 80.95) 
T_tWch_noFullyHad    = kreator.makeMCComponent("T_tWch_noFullyHad",    "/ST_tW_top_5f_NoFullyHadronicDecays_TuneCP5_13TeV-powheg-pythia8/RunIISummer20UL16NanoAODAPVv9-106X_mcRun2_asymptotic_preVFP_v11-v1/NANOAODSIM",     "CMS", ".*root",19.55)
TBar_tWch_noFullyHad = kreator.makeMCComponent("TBar_tWch_noFullyHad", "/ST_tW_antitop_5f_NoFullyHadronicDecays_TuneCP5_13TeV-powheg-pythia8/RunIISummer20UL16NanoAODAPVv9-106X_mcRun2_asymptotic_preVFP_v11-v1/NANOAODSIM", "CMS", ".*root",19.55)
top = [ 
        TTSemi_pow,T_sch,
         T_tch, TBar_tch,
         T_tWch_noFullyHad, TBar_tWch_noFullyHad,TT_mtt1ktoinf,TT_mttp7kto1k
]





mcSamples =  WJetsToLNuHT+  top  +  Higgs + QCD_bcToE + QCD_EMs + QCD_Mus + Ws + DiBosons



samples = mcSamples

# ---------------------------------------------------------------------

if __name__ == "__main__":
    from CMGTools.RootTools.samples.tools import runMain
    runMain(samples, localobjs=locals())
