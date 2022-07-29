#!/usr/bin/env python
#usage python tmvaProducer_multiclass_v1.py --year <> --fout <outputfilename>

import sys, os, optparse
import ROOT, re

lumis = {
    '2016': 35.9,
    '2017': 41.4,
    '2018': 59.7,
}


_allfiles = []
path = '/eos/cms/store/cmst3/group/dpsww/NanoTrees_v7_dpsww_04092020/'
_allfiles = []


def load_dataset(year,name, trainclass,friends=[]): 
    lumi= lumis[year]
    #mc = 0 if name.startswith('Double') else 1 
    mc = 0 if 'Run' in name else 1 
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


def train_multiclass(year,fOutName):

    eleID     = '(abs(Lep1_pdgId)!=11 || (Lep1_convVeto && Lep1_lostHits==0 && Lep1_tightCharge>=2)) && (abs(Lep2_pdgId)!=11 || (Lep2_convVeto && Lep2_lostHits==0 && Lep2_tightCharge>=2))'
    muon      = '(abs(Lep1_pdgId)!=13 || Lep1_tightCharge>=1) && (abs(Lep2_pdgId)!=13 || Lep2_tightCharge>=1)'
    mmss      = '(Lep1_pdgId*Lep2_pdgId) == 169'
    afac      = '(abs(Lep1_pdgId*Lep2_pdgId) == 169 || abs(Lep1_pdgId*Lep2_pdgId) == 121 ||  abs(Lep1_pdgId*Lep2_pdgId) == 143)'
    afss      = '(Lep1_pdgId*Lep2_pdgId == 169 || Lep1_pdgId*Lep2_pdgId == 121 || Lep1_pdgId*Lep2_pdgId == 143)'
    TT        = 'Lep1_isLepTight &&  Lep2_isLepTight'
    TL        = 'Lep1_isLepTight + Lep2_isLepTight == 1'

    common_cuts = 'nLepFO_Recl == 2 && Lep1_conept > 25 && Lep2_conept > 20 && MET_pt > 15'
    #setting cuts for different samples
    wzcuts = ROOT.TCut('1')
    wzcuts += afss
    wzcuts += muon
    wzcuts += eleID
    wzcuts += TT
    #wzcuts += common_cuts

    dpscuts = ROOT.TCut('1')
    dpscuts += afac
    dpscuts += muon
    dpscuts += eleID
    dpscuts += TT
    #dpscuts +=common_cuts
    TLcuts = ROOT.TCut('1')
    TLcuts += afss
    TLcuts += muon
    TLcuts += eleID
    TLcuts += TL
    #TLcuts +=common_cuts


    allcuts = ROOT.TCut('1')
    #common selection cut as used in the analysis

    allcuts += common_cuts

    dsets = [
        ('WWDoubleTo2L',"signal",dpscuts,['1_recl/','bdt_input_vars/'],"puWeight * xsec * genWeight"),
        ('WZTo3LNu_fxfx',"bgWZ",wzcuts,['1_recl/','bdt_input_vars/'],"puWeight * xsec * genWeight"),
        ('DoubleMuon_Run2016B_02Apr2020',"bgTL",TLcuts,['1_recl/','bdt_input_vars/','fakeRateWt/'],"fakeRateWt"),
        ('DoubleMuon_Run2016C_02Apr2020',"bgTL",TLcuts,['1_recl/','bdt_input_vars/','fakeRateWt/'],"fakeRateWt"),
        ('DoubleMuon_Run2016D_02Apr2020',"bgTL",TLcuts,['1_recl/','bdt_input_vars/','fakeRateWt/'],"fakeRateWt"),
        ('DoubleMuon_Run2016E_02Apr2020',"bgTL",TLcuts,['1_recl/','bdt_input_vars/','fakeRateWt/'],"fakeRateWt"),
        ('DoubleMuon_Run2016F_02Apr2020',"bgTL",TLcuts,['1_recl/','bdt_input_vars/','fakeRateWt/'],"fakeRateWt"),
        ('DoubleMuon_Run2016G_02Apr2020',"bgTL",TLcuts,['1_recl/','bdt_input_vars/','fakeRateWt/'],"fakeRateWt"),
        ('DoubleMuon_Run2016H_02Apr2020',"bgTL",TLcuts,['1_recl/','bdt_input_vars/','fakeRateWt/'],"fakeRateWt")]



    
    datasets = []
    for name, trainclass, cuts, frnds, evtwt in dsets:
        tree, weight = load_dataset(year,name,trainclass,frnds)
        #print tree, weight
        datasets.append((name, trainclass, tree, weight, cuts))

    fOut = ROOT.TFile(fOutName+".root","recreate") #creating the output file 
    fOut.cd()
    # configuring tmva

    factory = ROOT.TMVA.Factory('TMVAMutliClass', fOut, "!V:!Color:DrawProgressBar:Transformations=I;D;P;G,D:AnalysisType=multiclass" )
    DL = ROOT.TMVA.DataLoader("dataset_multiclass");
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



    fOut.cd()
    ## Add trees to DL
    for name,trainclass,tree,weight,cuts in datasets:
        DL.AddTree(tree, trainclass, weight,cuts)

    #passing weights which are applied event-by-event
    for trainclass in dsets:
        #    print 'inhere', trainclass[4],trainclass[1]
        DL.SetWeightExpression(trainclass[4], trainclass[1])

    DL.PrepareTrainingAndTestTree(allcuts, "!V")
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
    #                           'NegWeightTreatment=PairNegWeightsGlobal',

    factory.TrainAllMethods()
    factory.TestAllMethods()
    factory.EvaluateAllMethods()

    fOut.Close()

if __name__ == '__main__':
    from optparse import OptionParser
    parser = OptionParser(usage="%prog OUTFILE")
    # add option to pass lumi as argument
    parser.add_option("-f","--fout", dest="fout",type="string", default='TMVA_mutliclass_dpsvsWZvsfakes')
    parser.add_option("-Y","--year", dest="year",type="string", default='2016')
    (opts, args) = parser.parse_args()
    train_multiclass(opts.year,opts.fout)






##        ('W1JetsToLNu_LO',"bgWJ",TLcuts,['friends_DPScleaner_pu_lepSF_18102019/','friends_FORtraining_22042020/'],"xsec*puw"),
##        ('W2JetsToLNu_LO',"bgWJ",TLcuts,['friends_DPScleaner_pu_lepSF_18102019/','friends_FORtraining_22042020/'],"xsec*puw"),
##        ('W3JetsToLNu_LO',"bgWJ",TLcuts,['friends_DPScleaner_pu_lepSF_18102019/','friends_FORtraining_22042020/'],"xsec*puw"),
##        ('W4JetsToLNu_LO',"bgWJ",TLcuts,['friends_DPScleaner_pu_lepSF_18102019/','friends_FORtraining_22042020/'],"xsec*puw"),
##('DoubleMuon_2016C_reMiniAOD', "bgLL",LLcuts,['friends_FORtraining_22042020/'],"fakeRateWt"),
##('DoubleMuon_2016B_part1_reMiniAOD', "bgLL",LLcuts,['friends_FORtraining_22042020/'],"fakeRateWt"),
##('DoubleMuon_2016B_part2_reMiniAOD', "bgLL",LLcuts,['friends_FORtraining_22042020/'],"fakeRateWt"),
##('DoubleMuon_2016D_reMiniAOD', "bgLL",LLcuts,['friends_FORtraining_22042020/'],"fakeRateWt"),
##('DoubleMuon_2016E_reMiniAOD', "bgLL", LLcuts,['friends_FORtraining_22042020/'],"fakeRateWt"),
##('DoubleMuon_2016F_reMiniAOD', "bgLL", LLcuts,['friends_FORtraining_22042020/'],"fakeRateWt"),
##('DoubleMuon_2016G_part1_reMiniAOD', "bgLL",LLcuts,['friends_FORtraining_22042020/'],"fakeRateWt"),
##('DoubleMuon_2016G_part2_reMiniAOD', "bgLL",LLcuts,['friends_FORtraining_22042020/'],"fakeRateWt"),
##('DoubleMuon_2016H_ds1_part1_reMiniAOD', "bgLL",LLcuts,['friends_FORtraining_22042020/'],"fakeRateWt"),
##('DoubleMuon_2016H_ds1_part2_reMiniAOD', "bgLL",LLcuts,['friends_FORtraining_22042020/'],"fakeRateWt"),
##('DoubleMuon_2016H_ds2_reMiniAOD', "bgLL",LLcuts,['friends_FORtraining_22042020/'],"fakeRateWt"),
##('DoubleMuon_2016C_reMiniAOD', "bgfakes",fakescuts,['friends_FORtraining_22042020/'],"fakeRateWt"),
##('DoubleMuon_2016B_part1_reMiniAOD', "bgfakes",fakescuts,['friends_FORtraining_22042020/'],"fakeRateWt"),
##('DoubleMuon_2016B_part2_reMiniAOD', "bgfakes",fakescuts,['friends_FORtraining_22042020/'],"fakeRateWt"),
##('DoubleMuon_2016D_reMiniAOD', "bgfakes",fakescuts,['friends_FORtraining_22042020/'],"fakeRateWt"),
##('DoubleMuon_2016E_reMiniAOD', "bgfakes", fakescuts,['friends_FORtraining_22042020/'],"fakeRateWt"),
##('DoubleMuon_2016F_reMiniAOD', "bgfakes", fakescuts,['friends_FORtraining_22042020/'],"fakeRateWt"),
##('DoubleMuon_2016G_part1_reMiniAOD', "bgfakes",fakescuts,['friends_FORtraining_22042020/'],"fakeRateWt"),
##('DoubleMuon_2016G_part2_reMiniAOD', "bgfakes",fakescuts,['friends_FORtraining_22042020/'],"fakeRateWt"),
##('DoubleMuon_2016H_ds1_part1_reMiniAOD', "bgfakes",fakescuts,['friends_FORtraining_22042020/'],"fakeRateWt"),
##('DoubleMuon_2016H_ds1_part2_reMiniAOD', "bgfakes",fakescuts,['friends_FORtraining_22042020/'],"fakeRateWt"),
##('DoubleMuon_2016H_ds2_reMiniAOD', "bgfakes",fakescuts,['friends_FORtraining_22042020/'],"fakeRateWt")
