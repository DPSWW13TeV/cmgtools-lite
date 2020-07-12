#!/usr/bin/env python
#usage python tmvaProducer_WZnfakes.py outputfilename

import sys, os, optparse, subprocess
import ROOT, re


if "/functions_cc.so" not in ROOT.gSystem.GetLibraries():
    ROOT.gROOT.ProcessLine(".L %s/src/CMGTools/DPSWW/python/plotter/functions.cc+" % os.environ['CMSSW_BASE']);

lumis = {
    '2016': 35.9,
    '2017': 41.4,
    '2018': 59.7,
}


_allfiles = []
#path = '/eos/user/s/sesanche/nanoAOD/NanoTrees_TTH_090120_091019_v6_skim2lss/'
path = '/eos/cms/store/cmst3/group/dpsww/NanoTrees_TTH_090120_091019_v6_skim2lss/'


def load_dataset(year,name, trainclass,friends=[]): 
    lumi= lumis[year]
    mc = 0 if name.startswith('Double') else 1 

    fileloc = os.path.join(path,year,'%s.root' %name)
    infile = ROOT.TFile.Open(fileloc)
    _allfiles.append(infile)

    tree = infile.Get('Events')
    
    try: tree.GetName()
    except ReferenceError:
        raise RuntimeError("'tree' not found in %s" % fileloc)

    for friend in friends:
        friendloc = os.path.join(path,year,friend,'%s_Friend.root' % name)
        print "Adding friend from", friendloc
        tree.AddFriend('Friends', friendloc) 

    tree_wts = infile.Get('Runs')
    sum_wts=0.0
    
    if(mc == 0):
        weight = 1.0 # since it's data so weight factor is 1
    else:
        for iev in tree_wts:
            sum_wts+= iev.genEventSumw_
        weight= lumi/sum_wts

    print ('Added %s dataset, category %s, with weight %f' %
               (name, trainclass,weight))

    return tree, weight

def train_classification(year,bkg):


   
    eleID       = '(abs(LepGood_pdgId[iLepFO_Recl[0]])!=11 || (LepGood_convVeto[iLepFO_Recl[0]] && LepGood_lostHits[iLepFO_Recl[0]]==0 && LepGood_tightCharge[iLepFO_Recl[0]]>=2)) && (abs(LepGood_pdgId[iLepFO_Recl[1]])!=11 || (LepGood_convVeto[iLepFO_Recl[1]] && LepGood_lostHits[iLepFO_Recl[1]]==0 && LepGood_tightCharge[iLepFO_Recl[1]]>=2))'

    muon        = '(abs(LepGood_pdgId[iLepFO_Recl[0]])!=13 || LepGood_tightCharge[iLepFO_Recl[0]]>=1) && (abs(LepGood_pdgId[iLepFO_Recl[1]])!=13 || LepGood_tightCharge[iLepFO_Recl[1]]>=1)'

    mmss        = '(LepGood_pdgId[iLepFO_Recl[0]]*LepGood_pdgId[iLepFO_Recl[1]]) == 169'

    afac        = '(abs(LepGood_pdgId[iLepFO_Recl[0]]*LepGood_pdgId[iLepFO_Recl[1]]) == 169 || abs(LepGood_pdgId[iLepFO_Recl[0]]*LepGood_pdgId[iLepFO_Recl[1]]) == 121 ||  abs(LepGood_pdgId[iLepFO_Recl[0]]*LepGood_pdgId[iLepFO_Recl[1]]) == 143)'

    afss        = '(LepGood_pdgId[iLepFO_Recl[0]]*LepGood_pdgId[iLepFO_Recl[1]] == 169 || LepGood_pdgId[iLepFO_Recl[0]]*LepGood_pdgId[iLepFO_Recl[1]] == 121 || LepGood_pdgId[iLepFO_Recl[0]]*LepGood_pdgId[iLepFO_Recl[1]] == 143)'

    TT          = 'LepGood_isLepTight_Recl[iLepFO_Recl[0]] &&  LepGood_isLepTight_Recl[iLepFO_Recl[1]]'
    TL          = 'LepGood_isLepTight_Recl[iLepFO_Recl[0]] + LepGood_isLepTight_Recl[iLepFO_Recl[1]] == 1'

    #    bkgSel         = '(run != 1 && LepGood_isLepTight_Recl[iLepFO_Recl[0]] + LepGood_isLepTight_Recl[iLepFO_Recl[1]] == 1 ) || (run ==1 && LepGood_isLepTight_Recl[iLepFO_Recl[0]] &&  LepGood_isLepTight_Recl[iLepFO_Recl[1]]) '



    if bkg == 'WZ':
        bkgSel = TT
        dsets = [
            ('WWTo2L2Nu_DPS',"Signal",['1_recl_allvars/','dpsvars/']),  
            ('WZTo3LNu_pow',"Background",['1_recl_allvars/','dpsvars/'])]
    else :
        bkgSel = TL
        dsets = [
            ('WWTo2L2Nu_DPS',"Signal",['1_recl_allvars/','dpsvars/']),
            ('DoubleMuon_Run2016B_25Oct2019',"Background",['1_recl/','dpsvars/']),
            ('DoubleMuon_Run2016C_25Oct2019',"Background",['1_recl/','dpsvars/']),
            ('DoubleMuon_Run2016D_25Oct2019',"Background",['1_recl/','dpsvars/']),
            ('DoubleMuon_Run2016E_25Oct2019',"Background",['1_recl/','dpsvars/']),
            ('DoubleMuon_Run2016F_25Oct2019',"Background",['1_recl/','dpsvars/']),
            ('DoubleMuon_Run2016G_25Oct2019',"Background",['1_recl/','dpsvars/']),
            ('DoubleMuon_Run2016H_25Oct2019',"Background",['1_recl/','dpsvars/'])]
        

    #common selection cut as used in the analysis
    common_cuts = 'nLepFO_Recl == 2 && LepGood_conePt[iLepFO_Recl[0]] > 25 && LepGood_conePt[iLepFO_Recl[1]] > 20 && MET_pt > 15'


    bkgcuts = ROOT.TCut('1');
    bkgcuts += mmss
    bkgcuts += muon
    bkgcuts += eleID
    bkgcuts += common_cuts
    bkgcuts += bkgSel

    
    dpscuts = ROOT.TCut('1')
    dpscuts += afac
    dpscuts += muon
    dpscuts += eleID
    dpscuts +=TT
    dpscuts +=common_cuts

    
    datasets = []
    for name, trainclass, frnds in dsets:
        tree, glbwt = load_dataset(year,name,trainclass,frnds)
        #print tree, weight
        datasets.append((name, trainclass, tree, glbwt))

    fOut = ROOT.TFile("TMVA_classification_dpsvs"+bkg+".root","recreate") #creating the output file 
    fOut.cd()
    # configuring tmva

    factory = ROOT.TMVA.Factory('TMVAClassification', fOut, "!V:!Color:DrawProgressBar:Transformations=I;D;P;G,D:AnalysisType=Classification" )
    DL = ROOT.TMVA.DataLoader("dataset");
    # adding list of vars to train on
    DL.AddVariable('pt1 := LepGood_conePt[iLepFO_Recl[0]]','p_{T1}', 'F')
    DL.AddVariable('pt2 := LepGood_conePt[iLepFO_Recl[1]]','p_{T2}', 'F') 
    DL.AddVariable('met := MET_pt', 'F')
    DL.AddVariable('mt2 := mt2','F')
    DL.AddVariable('mtll','mTll', 'F') 
    DL.AddVariable('mtl1met','mTl1met', 'F') 
    DL.AddVariable('dphill','#Delta#phill', 'F')
    DL.AddVariable('dphil2met','#Delta #phi l2 met', 'F')
    DL.AddVariable('dphilll2','d#phi(ll,l2)', 'F')
    DL.AddVariable('etaprod   := LepGood_eta[iLepFO_Recl[0]]*LepGood_eta[iLepFO_Recl[1]]','#eta_{1}*#eta_{2}', 'F')
    DL.AddVariable('etasum    := abs(LepGood_eta[iLepFO_Recl[0]]+LepGood_eta[iLepFO_Recl[1]])','abs(#eta_{1}+#eta_{2})','F')


    for name,trainclass,tree,glbwt in datasets:
        if trainclass == "Signal":
            DL.AddSignalTree(tree,glbwt)
        else:
            DL.AddBackgroundTree(tree,glbwt)

    #evtwt_sig = "puw * (min(LepGood_mvaTTH[0],LepGood_mvaTTH[1]) > 0.9)"
    #evtwt  = "run == 1 ? (puWeight * xsec * genWeight * {TTsel} ) : 1.0 ".format(TTsel=TT)    #run number is set to 1 for MC samples 

    DL.SetSignalWeightExpression("puWeight * xsec * genWeight")
    #DL.SetWeightExpression(evtwt)

    if bkg == 'WZ':
        DL.SetBackgroundWeightExpression("puWeight * xsec * genWeight")
    else :
        DL.SetBackgroundWeightExpression("1.0");



    DL.PrepareTrainingAndTestTree(dpscuts,bkgcuts, "!V")

    factory.BookMethod(DL,ROOT.TMVA.Types.kBDT, 'BDTG',
                       ':'.join([
                           '!H',
                           '!V',
                           'NTrees=1000',
                           'BoostType=Grad',
                           'Shrinkage=0.10',
                           'UseBaggedBoost',
                           'BaggedSampleFraction=0.50',
                           'nCuts=20',
                           'MaxDepth=2',
                           'NegWeightTreatment=IgnoreNegWeightsInTraining'
                       ]))

##  factory.BookMethod(DL,ROOT.TMVA.Types.kBDT, 'BDT',
##                     ':'.join([
##                         '!H',
##                         '!V',
##                         'NTrees=1000',
##                         'MinNodeSize=2.5%',
##                         'MaxDepth=3',
##                         'BoostType=AdaBoost',
##                         'AdaBoostBeta=0.5'
##                         'UseBaggedBoost',
##                         'BaggedSampleFraction=0.50',
##                         'nCuts=20',
##                         'NegWeightTreatment=IgnoreNegWeightsInTraining'
##                     ]))
##
##  factory.BookMethod(DL,ROOT.TMVA.Types.kBDT, 'BDTB',
##                     ':'.join([
##                         '!H',
##                         '!V',
##                         'NTrees=400',
##                         'MinNodeSize=5%',
##                         'MaxDepth=3',
##                         'BoostType=Bagging',
##                         'nCuts=20',
##                         'NegWeightTreatment=IgnoreNegWeightsInTraining'
##                     ]))
##  
##
##  factory.BookMethod(DL,ROOT.TMVA.Types.kBDT, 'BDTF',
##                     ':'.join([
##                         '!H',
##                         '!V',
##                         'NTrees=50',
##                         'MinNodeSize=2.5%',
##                         'UseFisherCuts',
##                         'MaxDepth=3',
##                         'BoostType=AdaBoost',
##                         'AdaBoostBeta=0.5'
##                         'nCuts=20',
##                         'NegWeightTreatment=IgnoreNegWeightsInTraining'
##                     ]))


    factory.TrainAllMethods()
    factory.TestAllMethods()
    factory.EvaluateAllMethods()

    fOut.Close()

if __name__ == '__main__':

    parser = optparse.OptionParser(usage='usage: %prog [opts] ', version='%prog 1.0')
    parser.add_option("-b","--bkg", dest="bkg",type="string", default='WZ')
    parser.add_option("-Y","--year", dest="year",type="string", default='2016')
    #parser.add_option("-P","--treepath", dest="treepath",type="string", default=None)
    #parser.add_option("-F","--friend", dest="friends",type="string", default=[], action="append")
    (opts, args) = parser.parse_args()

    train_classification(opts.year,opts.bkg)




