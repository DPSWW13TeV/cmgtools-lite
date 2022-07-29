#!/usr/bin/env python
#usage python tmvaProducer_WZnfakes.py outputfilename

import sys, os, pickle
import ROOT, re


_allfiles = []
path = '/eos/cms/store/cmst3/group/dpsww/DPS_trees_2016/'
lumi= 36000.0 #total luminosity of the collected data in pb

def get_file(url):
    if os.path.exists(url):
        return url
    if not os.path.exists('%s.url'%url):
        raise RuntimeError('File not found: %s'%url)

    url = open('%s.url'%url, 'r').read().strip()
    return url


def load_dataset(name, trainclass,friends=[]): 

    mc = 0 if name.startswith('Double') else 1
    #addw = 1.0 if name.startswith('Double') else lumi

    fileloc = get_file(os.path.join(path,name, 'treeProducerSusyMultilepton/tree.root'))
    infile = ROOT.TFile.Open(fileloc)
    _allfiles.append(infile)

    tree = infile.Get('tree')
    
    try: tree.GetName()
    except ReferenceError:
        raise RuntimeError("'tree' not found in %s" % fileloc)

    for friend in friends:
        friendloc = get_file(os.path.join(path,friend, 'tree_Friend_%s.root' % name))
        #infile1 = ROOT.TFile.Open(friendloc)
        #_allfiles.append(friendloc)
        print "Adding friend from", friendloc
        tree.AddFriend('Friends', friendloc) #friend tree name for 2016 samples 

    if(mc == 0):
        weight = 1.0 # since it's data so weight factor is 1
    else:
        for iev in tree:
            addw = lumi*iev.xsec
            break;
        ## get counts from the histograms instead of pickle file
        histo_count        = infile.Get('Count')
        histo_sumgenweight = infile.Get('SumGenWeights')
        n_count=0;            #n_sumgenweight=0.0
        if histo_count:
            #print 'reading number of events from histogram' 
            n_count        = histo_count       .GetBinContent(1)
            #n_sumgenweight = (histo_sumgenweight.GetBinContent(1) if histo_sumgenweight else n_count)
        weight= 1.0*addw/n_count #won't handle the negative wts, could be added later

    print ('Added %s dataset, category %s, with weight %f' %
               (name, trainclass,weight))

    return tree, weight

def train_multiclass(fOutName):


    ##tightcharge = '(LepGood_chargeConsistency[0] ==2 || abs(LepGood_pdgId[0]) == 13) && (LepGood_chargeConsistency[1] == 2 || abs(LepGood_pdgId[1]) == 13)'
    tightcharge = '( (LepGood_chargeConsistency[0] >=3 || abs(LepGood_pdgId[0]) == 11) && (LepGood_chargeConsistency[1] >= 3 || abs(LepGood_pdgId[1]) == 11) ) && LepGood_tightCharge[0] > 1 && LepGood_tightCharge[1] > 1'
    mmss        = '(LepGood_pdgId[0]*LepGood_pdgId[1]) == 169'

    afac        = '(abs(LepGood_pdgId[0]*LepGood_pdgId[1]) == 169 || abs(LepGood_pdgId[0]*LepGood_pdgId[1]) == 121 ||  abs(LepGood_pdgId[0]*LepGood_pdgId[1]) == 143)'

    afss        = '(LepGood_pdgId[0]*LepGood_pdgId[1] == 169 || LepGood_pdgId[0]*LepGood_pdgId[1] == 121 || LepGood_pdgId[0]*LepGood_pdgId[1] == 143)'

    TT          = 'LepGood_mvaTTH[0] > 0.9 && LepGood_mvaTTH[1] > 0.9'

    TL          = '((LepGood_mvaTTH[0] > 0.9 && LepGood_mvaTTH[1] < 0.9) || (LepGood_mvaTTH[0] < 0.9 && LepGood_mvaTTH[1] > 0.9))' 
    LL          = 'LepGood_mvaTTH[0] < 0.9 && LepGood_mvaTTH[1] < 0.9'

    fakes    = '(LepGood_mvaTTH[0] < 0.9 && LepGood_mvaTTH[1] < 0.9) || ((LepGood_mvaTTH[0] > 0.9 && LepGood_mvaTTH[1] < 0.9) || (LepGood_mvaTTH[0] < 0.9 && LepGood_mvaTTH[1] > 0.9))' 


    #setting cuts for different samples
    wzcuts = ROOT.TCut('1')
    wzcuts += afss
    wzcuts += tightcharge
    wzcuts += TT

    dpscuts = ROOT.TCut('1')
    dpscuts += afac
    dpscuts += tightcharge
    dpscuts += TT

    TLcuts = ROOT.TCut('1')
    TLcuts += afss
    TLcuts += tightcharge
    TLcuts += TL

    LLcuts = ROOT.TCut('1')
    LLcuts += mmss
    LLcuts += tightcharge
    LLcuts += LL

    fakescuts = ROOT.TCut('1')
    fakescuts += mmss
    fakescuts += tightcharge
    fakescuts += fakes


    allcuts = ROOT.TCut('1')
    #common selection cut as used in the analysis
    common_cuts = 'nLepGood==2 && LepGood_pt[0]>25. && LepGood_pt[1]>20. && met_pt > 15.'
    allcuts += common_cuts

    dsets = [

        ('WWDoubleTo2L',"Signal",dpscuts,['friends_DPScleaner_pu_lepSF_18102019/','friends_FORtraining_22042020/'],"puw"),
        ('WZTo3LNu',"bgWZ",wzcuts,['friends_DPScleaner_pu_lepSF_18102019/','friends_FORtraining_22042020/'],"puw"),
        ('DoubleMuon_2016B_part1_reMiniAOD', "bgTL",TLcuts,['friends_FORtraining_22042020/'],"fakeRateWt"),
        ('DoubleMuon_2016B_part2_reMiniAOD', "bgTL",TLcuts,['friends_FORtraining_22042020/'],"fakeRateWt"),
        ('DoubleMuon_2016C_reMiniAOD', "bgTL",TLcuts,['friends_FORtraining_22042020/'],"fakeRateWt"),
        ('DoubleMuon_2016D_reMiniAOD', "bgTL",TLcuts,['friends_FORtraining_22042020/'],"fakeRateWt"),
        ('DoubleMuon_2016E_reMiniAOD', "bgTL", TLcuts,['friends_FORtraining_22042020/'],"fakeRateWt"),
        ('DoubleMuon_2016F_reMiniAOD', "bgTL", TLcuts,['friends_FORtraining_22042020/'],"fakeRateWt"),
        ('DoubleMuon_2016G_part1_reMiniAOD', "bgTL",TLcuts,['friends_FORtraining_22042020/'],"fakeRateWt"),
        ('DoubleMuon_2016G_part2_reMiniAOD', "bgTL",TLcuts,['friends_FORtraining_22042020/'],"fakeRateWt"),
        ('DoubleMuon_2016H_ds1_part1_reMiniAOD', "bgTL",TLcuts,['friends_FORtraining_22042020/'],"fakeRateWt"),
        ('DoubleMuon_2016H_ds1_part2_reMiniAOD', "bgTL",TLcuts,['friends_FORtraining_22042020/'],"fakeRateWt"),
        ('DoubleMuon_2016H_ds2_reMiniAOD', "bgTL",TLcuts,['friends_FORtraining_22042020/'],"fakeRateWt")
  ]

    
    datasets = []
    for name, trainclass, cuts, frnds, evtwt in dsets:
        tree, weight = load_dataset(name,trainclass,frnds)
        #print tree, weight
        datasets.append((name, trainclass, tree, weight, cuts))

    fOut = ROOT.TFile(fOutName+".root","recreate") #creating the output file 
    fOut.cd()
    # configuring tmva

    factory = ROOT.TMVA.Factory('TMVAMutliClass', fOut, "!V:!Color:DrawProgressBar:Transformations=I;D;P;G,D:AnalysisType=multiclass" )
    DL = ROOT.TMVA.DataLoader("dataset");
    # adding list of vars to train on
    DL.AddVariable('pt1 := LepGood_pt[0]','p_{T1}', 'F')
    DL.AddVariable('pt2 := LepGood_pt[1]','p_{T2}', 'F') 
    DL.AddVariable('met := met_pt', 'F')
    DL.AddVariable('mt2','MT2_{ll}', 'F')
    DL.AddVariable('mtll','MT l1 l2', 'F') 
    DL.AddVariable('mtl1met','MT l1 met', 'F') 
    DL.AddVariable('dphill','#Delta #phi l1 l2', 'F') 
    DL.AddVariable('dphil2met','#Delta #phi l2 met', 'F') 
    DL.AddVariable('dphilll2','#Delta #phi l1l2 l2', 'F')
    DL.AddVariable('etaprod  := LepGood_eta[0]*LepGood_eta[1]','#eta_{1}*#eta_{2}', 'F')
    DL.AddVariable('etasum := abs(LepGood_eta[0]+LepGood_eta[1])','abs(#eta_{1}+#eta_{2})','F')

    fOut.cd()
    ## Add trees to DL
    for name,trainclass,tree,weight,cuts in datasets:
        DL.AddTree(tree, trainclass, weight,cuts)

    #passing weights which are applied event-by-event
    for trainclass in dsets:
        #    print 'inhere', trainclass[4],trainclass[1]
        DL.SetWeightExpression(trainclass[4], trainclass[1])

    #DL.PrepareTrainingAndTestTree(allcuts, "SplitMode=Random:NormMode=EqualNumEvents:!V")
    #DL.PrepareTrainingAndTestTree(allcuts, "SplitMode=Random:NormMode=NumEvents:!V")
    #DL.PrepareTrainingAndTestTree(allcuts, "SplitMode=Random:NormMode=None:!V")
    DL.PrepareTrainingAndTestTree(allcuts, "!V")
    #DL.PrepareTrainingAndTestTree(allcuts, "SplitMode=Block:NormMode=None:MixMode=Random:!V")
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
    #parser.add_option("-P","--treepath", dest="treepath",type="string", default=None)
    #parser.add_option("-F","--friend", dest="friends",type="string", default=[], action="append")
    (options, args) = parser.parse_args()

    if not len(args):
        parser.print_help()
        sys.exit(-1)

    train_multiclass(args[0])






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
