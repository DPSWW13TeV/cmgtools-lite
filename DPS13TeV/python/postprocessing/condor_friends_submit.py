#!/usr/bin/env python                                                       
import os, sys, datetime, subprocess
import ROOT
date = datetime.date.today().isoformat()

#eospath = '/afs/cern.ch/user/p/peruzzi/work/tthtrees/TREES_TTH_190418_Fall17_skim2lss3l/'
#eospath = '/afs/cern.ch/work/a/anmehta/work/Test/Test2/CMSSW_8_0_25/src/CMGTools/DPS13TeV/python/postprocessing/copy_Friends_2017_WZ_Oct26/'
#test_DPS_trees2017/'
#eospath = '/eos/user/a/anmehta/copy_DPS_trees_2016/'
#eospath = '/eos/user/m/mdunser/dps-13TeV-combination/DPS_QCD_2017/'
eospath ='/eos/user/a/anmehta/copy_DPS_trees_2016/'
#/afs/cern.ch/work/a/anmehta/work/Test/Test2/CMSSW_8_0_25/src/CMGTools/DPS13TeV/python/plotter/2017_trees_friends/test_DPS_trees2017/'
#eospath = '/eos/user/m/mdunser/dps-13TeV-combination/TREES_WZ_2017/'
outputdir='/afs/cern.ch/work/a/anmehta/work/Test/Test2/CMSSW_8_0_25/src/CMGTools/DPS13TeV/python/plotter/frnds2016_unskimmed/'
logdir='logs2016/'

samplelist2016=['WZTo3LNu_fxfx_part1']#,'WZTo3LNu_fxfx_part2','DYJetsToLL_M10to50_LO','DYJetsToLL_M50_LO_ext_part1','DYJetsToLL_M50_LO_ext_part2','DYJetsToLL_M50_LO_ext_part3','WWDoubleTo2L','WW_DPS_herwig','WpWpJJ','WWW','TTZ_LO','ZGTo2LG_ext','ZZTo4L','WZTo3LNu','WZTo3LNu_amcatnlo','WGToLNuG_amcatanlo_ext','WGToLNuG','WGToLNuG_amcatanlo_ext1','WGToLNuG_amcatanlo_ext2','WGToLNuG_amcatanlo_ext1','WZTo3LNu_mll01','WZTo3LNu_mll01_ext_part2','WZTo3LNu_mll01_ext_part3','W1JetsToLNu_LO','W2JetsToLNu_LO','W3JetsToLNu_LO','W4JetsToLNu_LO','SingleElectron_2016B_reMiniAOD','SingleElectron_2016C_reMiniAOD','SingleElectron_2016D_reMiniAOD','SingleElectron_2016E_reMiniAOD','SingleElectron_2016F_reMiniAOD','SingleElectron_2016G_reMiniAOD','SingleElectron_2016H_ds1_reMiniAOD','SingleElectron_2016H_ds2_reMiniAOD','SingleMuon_2016B_reMiniAOD','SingleMuon_2016C_reMiniAOD','SingleMuon_2016D_reMiniAOD','SingleMuon_2016E_reMiniAOD','SingleMuon_2016F_reMiniAOD','SingleMuon_2016G_reMiniAOD','SingleMuon_2016H_ds1_reMiniAOD','SingleMuon_2016H_ds2_reMiniAOD','DoubleMuon_2016B_part1_reMiniAOD','DoubleMuon_2016B_part2_reMiniAOD','DoubleMuon_2016C_reMiniAOD','DoubleMuon_2016D_reMiniAOD','DoubleMuon_2016E_reMiniAOD','DoubleMuon_2016F_reMiniAOD','DoubleMuon_2016G_part1_reMiniAOD','DoubleMuon_2016G_part2_reMiniAOD','DoubleMuon_2016H_ds1_part1_reMiniAOD','DoubleMuon_2016H_ds1_part2_reMiniAOD','DoubleMuon_2016H_ds2_reMiniAOD','MuonEG_2016B_reMiniAOD','MuonEG_2016C_reMiniAOD','MuonEG_2016D_reMiniAOD','MuonEG_2016E_reMiniAOD','MuonEG_2016F_reMiniAOD','MuonEG_2016G_reMiniAOD','MuonEG_2016H_ds1_reMiniAOD','MuonEG_2016H_ds2_reMiniAOD']

samplelistQCD2016=['QCD_Mu15','QCD_Pt170to250_bcToE','QCD_Pt250toInf_bcToE','QCD_Pt50to80_EMEnriched','QCD_Pt120to170_EMEnriched','QCD_Pt170to300_EMEnriched','QCD_Pt300toInf_EMEnriched','QCD_Pt80to120_EMEnriched','QCD_Pt15to20_EMEnriched','QCD_Pt20to30_EMEnriched','QCD_Pt30to50_EMEnriched','QCD_Pt80to170_bcToE','QCD_Pt15to20_bcToE','QCD_Pt20to30_bcToE','QCD_Pt30to80_bcToE']

samplelistforjec2017=['WZTo3LNu_fxfx','WW_DPS_leptonic_pythia']
samplelistforjec2016=['WZTo3LNu','WWDoubleTo2L']

samplelist2017=['DY1JetsToLL_M50_LO_skimSameSign','DY2JetsToLL_M50_LO_skimSameSign','DY3JetsToLL_M50_LO_skimSameSign','DY4JetsToLL_M50_LO_skimSameSign','DY4JetsToLL_M50_LO_skimSameSign','DYJetsToLL_M10to50_LO','DYJetsToLL_M4to50_HT100to200_skimSameSign', 'DYJetsToLL_M4to50_HT200to400_skimSameSign', 'DYJetsToLL_M4to50_HT400to600_skimSameSign','DYJetsToLL_M4to50_HT600toInf_skimSameSign','DYJetsToLL_M4to50_HT70to100_skimSameSign','DYJetsToLL_M50_LO','TTJets_DiLepton_part2', 'TTJets_DiLepton_part1','TTZ_LO','W1JetsToLNu_LO_skimSameSign','W2JetsToLNu_LO_skimSameSign','W3JetsToLNu_LO_skimSameSign','W4JetsToLNu_LO_skimSameSign','WGToLNuG','WJetsToLNu_LO','WWW_4F','WWZ_4F','WW_DPS','WW_DPS_herwig','WW_DPS_leptonic_pythia','WpWpJJ','WZG','WZTo3LNu_fxfx','WZZ','ZZTo4L','ZZZ','DoubleEG_2017B','DoubleEG_2017B_forFlips','DoubleEG_2017C','DoubleEG_2017C_forFlips','DoubleEG_2017D','DoubleEG_2017D_forFlips','DoubleEG_2017E','DoubleEG_2017E_forFlips','DoubleEG_2017F','DoubleEG_2017F_forFlips','DoubleMuon_2017B','DoubleMuon_2017B_forFlips','DoubleMuon_2017C','DoubleMuon_2017C_forFlips','DoubleMuon_2017D','DoubleMuon_2017D_forFlips','DoubleMuon_2017E','DoubleMuon_2017E_forFlips','DoubleMuon_2017F','DoubleMuon_2017F_forFlips','MuonEG_2017B','MuonEG_2017B_forFlips','MuonEG_2017C','MuonEG_2017C_forFlips','MuonEG_2017D','MuonEG_2017D_forFlips','MuonEG_2017E','MuonEG_2017E_forFlips','MuonEG_2017F','MuonEG_2017F_forFlips','SingleElectron_2017B','SingleElectron_2017B_forFlips','SingleElectron_2017C','SingleElectron_2017C_forFlips','SingleElectron_2017D','SingleElectron_2017D_forFlips','SingleElectron_2017E','SingleElectron_2017E_forFlips','SingleElectron_2017F','SingleElectron_2017F_forFlips','SingleMuon_2017B','SingleMuon_2017B_forFlips','SingleMuon_2017C','SingleMuon_2017C_forFlips','SingleMuon_2017D','SingleMuon_2017D_forFlips','SingleMuon_2017E','SingleMuon_2017E_forFlips','SingleMuon_2017F','SingleMuon_2017F_forFlips']
samplelistWNjets=['W1JetsToLNu_LO','W2JetsToLNu_LO','W3JetsToLNu_LO','W4JetsToLNu_LO']              
samplelist=['WZTo3LNu_powheg']
dirs = os.listdir(eospath)
list1 = [] 
for sample in samplelist2016: 
    list1.extend( list( i for i in dirs if sample in i and i not in list1) )
for proc in list1 :
    cmd='python submitFriendsCondor.py -d {treePath} -o {outdir} -s {sample} -N 170000'.format(treePath=eospath,outdir=outputdir, sample=proc)
    print cmd
    os.system(cmd)


