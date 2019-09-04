#!/usr/bin/env python                                                       
import os, sys, datetime, subprocess, shutil

date = datetime.date.today().isoformat()

eospath = '/eos/user/a/anmehta/DPS_trees_2016/TREES_TTH_250117_Summer16_JECV3_noClean_qgV2/'
neweospath = '/eos/user/a/anmehta/copy_DPS_trees_2016/'
files = os.listdir(eospath)
newlist=[]
skiplist=['DoubleEG_2016B_reMiniAOD','DoubleEG_2016B','DoubleEG_2016C_reMiniAOD','DoubleEG_2016C','DoubleEG_2016D_reMiniAOD','DoubleEG_2016D','DoubleEG_2016E_reMiniAOD','DoubleEG_2016E','DoubleEG_2016F_reMiniAOD','DoubleEG_2016F','DoubleEG_2016G_reMiniAOD','DoubleEG_2016G','DoubleEG_2016H_ds1_reMiniAOD','DoubleEG_2016H_ds1','DoubleEG_2016H_ds2_reMiniAOD','DoubleEG_2016H_ds2','SingleElectron_2016B','SingleElectron_2016C','SingleElectron_2016D','SingleElectron_2016E','SingleElectron_2016F','SingleElectron_2016G','SingleElectron_2016H_ds1','SingleElectron_2016H_ds2','SingleMuon_2016B','SingleMuon_2016C','SingleMuon_2016D','SingleMuon_2016E','SingleMuon_2016F','SingleMuon_2016G','SingleMuon_2016H_ds1','SingleMuon_2016H_ds2','DoubleMuon_2016B','DoubleMuon_2016C','DoubleMuon_2016D','DoubleMuon_2016E','DoubleMuon_2016F','DoubleMuon_2016G','DoubleMuon_2016H_ds1','DoubleMuon_2016H_ds2','MuonEG_2016B','MuonEG_2016C','MuonEG_2016D','MuonEG_2016E','MuonEG_2016F','MuonEG_2016G','MuonEG_2016H_ds1','MuonEG_2016H_ds2','tZq_ll_ext_highstat','tZq_ll_ext','tWll','VHToNonbb','TTHnobb_mWCutfix_ext_LHE','TTHnobb_mWCutfix_ext','TTHnobb_pow','THQ','THW']
for i in files:
    sn = i.split('_')
    treeind = sn.index([i for i in sn if 'treeProducer' in i][0])
    newlist.append('_'.join(sn[:treeind]))

for sample in newlist:
    if sample not in skiplist:
        directory = '{neweospath}/{sample}/treeProducerSusyMultilepton/'.format(neweospath=neweospath,sample=sample)
        print sample
        if not os.path.exists(directory):
            os.makedirs(directory)
            olddirectory='{eospath}/{sample}_treeProducerSusyMultilepton_tree.root'.format(eospath=eospath,sample=sample)
            shutil.copyfile(olddirectory,directory+'/tree.root')

