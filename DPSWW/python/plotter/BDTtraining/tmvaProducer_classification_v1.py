#!/usr/bin/env python
#usage python tmvaProducer_classification_v1.py --b <bkg name WZ/fakes>

import sys, os, optparse, subprocess
import ROOT, re


#if "/functions_cc.so" not in ROOT.gSystem.GetLibraries():
#    ROOT.gROOT.ProcessLine(".L %s/src/CMGTools/DPSWW/python/plotter/functions.cc+" % os.environ['CMSSW_BASE']);

lumis = {
    '2016': 35.9,
    '2017': 41.4,
    '2018': 59.7,
}


_allfiles = []
#path = '/eos/user/s/sesanche/nanoAOD/NanoTrees_TTH_090120_091019_v6_skim2lss/'
path = '/eos/cms/store/cmst3/group/dpsww/NanoTrees_v7_dpsww_04092020/'


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
            sum_wts+= iev.genEventSumw
        weight= lumi/sum_wts

    print ('Added %s dataset, category %s, with weight %f' %
               (name, trainclass,weight))

    return tree, weight

def train_classification(year,bkg):


   
    eleID     = '(abs(Lep1_pdgId)!=11 || (Lep1_convVeto && Lep1_lostHits==0 && Lep1_tightCharge>=2)) && (abs(Lep2_pdgId)!=11 || (Lep2_convVeto && Lep2_lostHits==0 && Lep2_tightCharge>=2))'
    muon      = '(abs(Lep1_pdgId)!=13 || Lep1_tightCharge>=1) && (abs(Lep2_pdgId)!=13 || Lep2_tightCharge>=1)'
    mmss      = '(Lep1_pdgId*Lep2_pdgId) == 169'
    afac      = '(abs(Lep1_pdgId*Lep2_pdgId) == 169 || abs(Lep1_pdgId*Lep2_pdgId) == 121 ||  abs(Lep1_pdgId*Lep2_pdgId) == 143)'
    afss      = '(Lep1_pdgId*Lep2_pdgId == 169 || Lep1_pdgId*Lep2_pdgId == 121 || Lep1_pdgId*Lep2_pdgId == 143)'
    TT        = 'Lep1_isLepTight &&  Lep2_isLepTight'
    TL        = 'Lep1_isLepTight + Lep2_isLepTight == 1'

    #    bkgSel         = '(run != 1 && LepGood_isLepTight_Recl[iLepFO_Recl[0]] + LepGood_isLepTight_Recl[iLepFO_Recl[1]] == 1 ) || (run ==1 && LepGood_isLepTight_Recl[iLepFO_Recl[0]] &&  LepGood_isLepTight_Recl[iLepFO_Recl[1]]) '



    if bkg == 'WZ':
        bkgSel = TT
        dsets = [
            ('WWDoubleTo2L',"Signal",['2_recl/','bdt_input_vars/']),  
            #('WZTo3LNu_fxfx',"Background",['2_recl/','bdt_input_vars/'])]
            ('WZTo3LNu',"Background",['2_recl/','bdt_input_vars/'])]
    else :
        bkgSel = TL
        dsets = [
            ('WWDoubleTo2L',"Signal",['2_recl/','bdt_input_vars/']),
            ('DoubleMuon_Run2016B_02Apr2020',"Background",['2_recl/','bdt_input_vars/']),
            ('DoubleMuon_Run2016C_02Apr2020',"Background",['2_recl/','bdt_input_vars/']),
            ('DoubleMuon_Run2016D_02Apr2020',"Background",['2_recl/','bdt_input_vars/']),
            ('DoubleMuon_Run2016E_02Apr2020',"Background",['2_recl/','bdt_input_vars/']),
            ('DoubleMuon_Run2016F_02Apr2020',"Background",['2_recl/','bdt_input_vars/']),
            ('DoubleMuon_Run2016G_02Apr2020',"Background",['2_recl/','bdt_input_vars/']),
            ('DoubleMuon_Run2016H_02Apr2020',"Background",['2_recl/','bdt_input_vars/'])]
        

    #common selection cut as used in the analysis
    common_cuts = 'nLepFO_Recl == 2 && Lep1_conept > 25 && Lep2_conept > 20 && MET_pt > 15'


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
    #DL = ROOT.TMVA.DataLoader(fOutName+"dataset");

    # adding list of vars to train on
    DL.AddVariable('pt1 := Lep1_conept','p_{T1}', 'F')
    DL.AddVariable('pt2 := Lep2_conept','p_{T2}', 'F') 
    DL.AddVariable('met := MET_pt', 'F')
    DL.AddVariable('mt2 := mt2','F')
    DL.AddVariable('mtll:= mtll', 'F') 
    DL.AddVariable('mtl1met := mtl1met', 'F') 
    DL.AddVariable('dphill := dphill','#Delta#phill', 'F')
    DL.AddVariable('dphil2met := dphil2met','#Delta #phi l2 met', 'F')
    DL.AddVariable('dphilll2 := dphilll2','d#phi(ll,l2)', 'F')
    DL.AddVariable('etaprod   := Lep1_eta*Lep2_eta','#eta_{1}*#eta_{2}', 'F')
    DL.AddVariable('etasum    := abs(Lep1_eta+Lep2_eta)','abs(#eta_{1}+#eta_{2})','F')


    for name,trainclass,tree,glbwt in datasets:
        if trainclass == "Signal":
            DL.AddSignalTree(tree,glbwt)
        else:
            DL.AddBackgroundTree(tree,glbwt)

    #evtwt_sig = "puw * (min(LepGood_mvaTTH[0],LepGood_mvaTTH[1]) > 0.9)"
    evtwt  = "run == 1 ? (puWeight * xsec * genWeight * {TTsel} ) : 1.0 ".format(TTsel=TT)    #run number is set to 1 for MC samples 
    DL.SetWeightExpression(evtwt)
    

    ##amDL.SetSignalWeightExpression("puWeight * xsec * genWeight")
    ##amif bkg == 'WZ':
    ##am    DL.SetBackgroundWeightExpression("puWeight * xsec * genWeight")
    ##amelse :
    ##am    DL.SetBackgroundWeightExpression("1.0");

    #evtwt  = "!isData ? (puw * (min(LepGood_mvaTTH[0],LepGood_mvaTTH[1]) > 0.9)) : (fakeRateWt * {TLsel})".format(TLsel=TL)



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
                           'CreateMVAPdfs',
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




