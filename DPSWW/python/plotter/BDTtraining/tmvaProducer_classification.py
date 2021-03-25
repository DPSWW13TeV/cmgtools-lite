#!/usr/bin/env python
#usage python tmvaProducer_classification.py -b <bkg name wz_amc/wz_pow/fakes> -y <year>

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
path = '/eos/cms/store/cmst3/group/dpsww/NanoTrees_v7_dpsww_04092020/'


#friends=['2_recl_muWP90_elWP70','bdt_input_vars_muWP90_elWP70_v1']




def load_dataset(year,name, trainclass,friends=[]): 
    lumi= lumis[year]
    print lumi
    mc = 0 if 'Run' in name  else 1 

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
        weight= lumi*1000/sum_wts
        print weight
    print ('Added %s dataset, category %s, with weight %f' %
               (name, trainclass,weight))

    return tree, weight

def train_classification(year,bkg,useconept,usefr,moretxt):
    pf='_muWP90_elWP70' if year == '2017' else ''
    frnds=['2_recl','bdt_input_vars_ultramax']
    friends=[name+pf for name in frnds]
    ##eleID     = '(abs(Lep1_pdgId)!=11 || (Lep1_convVeto && Lep1_lostHits==0 && Lep1_tightCharge>=2)) && (abs(Lep2_pdgId)!=11 || (Lep2_convVeto && Lep2_lostHits==0 && Lep2_tightCharge>=2))'
    eleID     = '(abs(Lep1_pdgId)!=11 || ( Lep1_tightCharge>=2)) && (abs(Lep2_pdgId)!=11 || (Lep2_tightCharge>=2))'
    muon      = '(abs(Lep1_pdgId)!=13 || Lep1_tightCharge>=1) && (abs(Lep2_pdgId)!=13 || Lep2_tightCharge>=1)'
    mmss      = '(Lep1_pdgId*Lep2_pdgId) == 169'
    afac      = '(abs(Lep1_pdgId*Lep2_pdgId) == 169 || abs(Lep1_pdgId*Lep2_pdgId) == 121 ||  abs(Lep1_pdgId*Lep2_pdgId) == 143)'
    afss      = '(Lep1_pdgId*Lep2_pdgId == 169 || Lep1_pdgId*Lep2_pdgId == 121 || Lep1_pdgId*Lep2_pdgId == 143)'
    TT        = '(Lep1_isLepTight &&  Lep2_isLepTight)'
    TL        = '((Lep1_isLepTight &&  !Lep2_isLepTight) || (!Lep1_isLepTight &&  Lep2_isLepTight))'
    fakes     = '(!(Lep1_isLepTight &&  Lep2_isLepTight))'
    atleast1Mu = '(abs(Lep1_pdgId) == 13 || abs(Lep2_pdgId) == 13)'
    cptllCut   = '{here} || cptll > 20'.format(here=mmss)
    #cptllCut   = '{here} || cptll > 20'.format(here=atleast1Mu)
    #    bkgSel         = '(run != 1 && LepGood_isLepTight_Recl[iLepFO_Recl[0]] + LepGood_isLepTight_Recl[iLepFO_Recl[1]] == 1 ) || (run ==1 && LepGood_isLepTight_Recl[iLepFO_Recl[0]] &&  LepGood_isLepTight_Recl[iLepFO_Recl[1]]) '



    if bkg == 'wz_pow':
        bkgSel = TT + '&&'+ mmss
        dsets = [
            ('WWDoubleTo2L',"Signal",friends),  
            ('WZTo3LNu',"Background",friends)]
    elif (bkg == 'wz_amc'):
        bkgSel = TT + '&&'+ mmss
        dsets = [
            ('WWDoubleTo2L',"Signal",friends),  
            ('WZTo3LNu_fxfx',"Background",friends)]

    else: 
        bkgSel = TL + '&&'+ cptllCut + '&&'+ afss
        dsets = [
            ('WWDoubleTo2L',"Signal",friends),
            ('DoubleMuon_Run{here}B_02Apr2020'.format(here=year),"Background",friends),
            ('DoubleMuon_Run{here}C_02Apr2020'.format(here=year),"Background",friends),
            ('DoubleMuon_Run{here}D_02Apr2020'.format(here=year),"Background",friends),
            ('SingleMuon_Run{here}B_02Apr2020'.format(here=year),"Background",friends),
            ('SingleMuon_Run{here}C_02Apr2020'.format(here=year),"Background",friends),
            ('SingleMuon_Run{here}D_02Apr2020'.format(here=year),"Background",friends),
            ('MuonEG_Run{here}B_02Apr2020'.format(here=year),"Background",friends),
            ('MuonEG_Run{here}C_02Apr2020'.format(here=year),"Background",friends),
            ('MuonEG_Run{here}D_02Apr2020'.format(here=year),"Background",friends),
            
        ]
        if (year == '2016' and 'wz' not in bkg):
            dsets.append(('DoubleMuon_Run{here}E_02Apr2020'.format(here=year),"Background",friends))
            dsets.append(('DoubleMuon_Run{here}F_02Apr2020'.format(here=year),"Background",friends))
            dsets.append(('DoubleMuon_Run{here}G_02Apr2020'.format(here=year),"Background",friends))
            dsets.append(('DoubleMuon_Run{here}H_02Apr2020'.format(here=year),"Background",friends))
            dsets.append(('SingleMuon_Run{here}E_02Apr2020'.format(here=year),"Background",friends))
            dsets.append(('SingleMuon_Run{here}F_02Apr2020'.format(here=year),"Background",friends))
            dsets.append(('SingleMuon_Run{here}G_02Apr2020'.format(here=year),"Background",friends))
            dsets.append(('SingleMuon_Run{here}H_02Apr2020'.format(here=year),"Background",friends))
            dsets.append(('SingleElectron_Run{here}B_02Apr2020'.format(here=year),"Background",friends))
            dsets.append(('SingleElectron_Run{here}C_02Apr2020'.format(here=year),"Background",friends))
            dsets.append(('SingleElectron_Run{here}D_02Apr2020'.format(here=year),"Background",friends))
            dsets.append(('SingleElectron_Run{here}E_02Apr2020'.format(here=year),"Background",friends))
            dsets.append(('SingleElectron_Run{here}F_02Apr2020'.format(here=year),"Background",friends))
            dsets.append(('SingleElectron_Run{here}G_02Apr2020'.format(here=year),"Background",friends))
            dsets.append(('SingleElectron_Run{here}H_02Apr2020'.format(here=year),"Background",friends))
            dsets.append(('DoubleEG_Run{here}B_02Apr2020'.format(here=year),"Background",friends))
            dsets.append(('DoubleEG_Run{here}C_02Apr2020'.format(here=year),"Background",friends))
            dsets.append(('DoubleEG_Run{here}D_02Apr2020'.format(here=year),"Background",friends))
            dsets.append(('DoubleEG_Run{here}E_02Apr2020'.format(here=year),"Background",friends))
            dsets.append(('DoubleEG_Run{here}F_02Apr2020'.format(here=year),"Background",friends))
            dsets.append(('DoubleEG_Run{here}G_02Apr2020'.format(here=year),"Background",friends))
            dsets.append(('DoubleEG_Run{here}H_02Apr2020'.format(here=year),"Background",friends))
            dsets.append(('MuonEG_Run{here}E_02Apr2020'.format(here=year),"Background",friends))
            dsets.append(('MuonEG_Run{here}F_02Apr2020'.format(here=year),"Background",friends))
            dsets.append(('MuonEG_Run{here}G_02Apr2020'.format(here=year),"Background",friends))
            dsets.append(('MuonEG_Run{here}H_02Apr2020'.format(here=year),"Background",friends))

        elif (year == '2017' and 'wz' not in bkg):    
            dsets.append(('DoubleMuon_Run{here}E_02Apr2020'.format(here=year),"Background",friends))
            dsets.append(('DoubleMuon_Run{here}F_02Apr2020'.format(here=year),"Background",friends))
            dsets.append(('SingleMuon_Run{here}E_02Apr2020'.format(here=year),"Background",friends))
            dsets.append(('SingleMuon_Run{here}F_02Apr2020'.format(here=year),"Background",friends))
            dsets.append(('SingleElectron_Run{here}B_02Apr2020'.format(here=year),"Background",friends))
            dsets.append(('SingleElectron_Run{here}C_02Apr2020'.format(here=year),"Background",friends))
            dsets.append(('SingleElectron_Run{here}D_02Apr2020'.format(here=year),"Background",friends))
            dsets.append(('SingleElectron_Run{here}E_02Apr2020'.format(here=year),"Background",friends))
            dsets.append(('SingleElectron_Run{here}F_02Apr2020'.format(here=year),"Background",friends))
            dsets.append(('DoubleEG_Run{here}B_02Apr2020'.format(here=year),"Background",friends))
            dsets.append(('DoubleEG_Run{here}C_02Apr2020'.format(here=year),"Background",friends))
            dsets.append(('DoubleEG_Run{here}D_02Apr2020'.format(here=year),"Background",friends))
            dsets.append(('DoubleEG_Run{here}E_02Apr2020'.format(here=year),"Background",friends))
            dsets.append(('DoubleEG_Run{here}F_02Apr2020'.format(here=year),"Background",friends))
            dsets.append(('MuonEG_Run{here}E_02Apr2020'.format(here=year),"Background",friends))
            dsets.append(('MuonEG_Run{here}F_02Apr2020'.format(here=year),"Background",friends))



        elif (year == '2018' and 'wz' not in bkg):        
            dsets.append(('DoubleMuon_Run2018A_02Apr2020',"Background",friends))
            dsets.append(('SingleMuon_Run2018A_02Apr2020',"Background",friends))
            dsets.append(('EGamma_Run2018A_02Apr2020',"Background",friends))
            dsets.append(('EGamma_Run2018B_02Apr2020',"Background",friends))
            dsets.append(('EGamma_Run2018C_02Apr2020',"Background",friends))
            dsets.append(('EGamma_Run2018D_02Apr2020',"Background",friends))
            dsets.append(('MuonEG_Run2018A_02Apr2020',"Background",friends))

    if useconept:
        print 'training using conept'
        pff='_withcpt'
        common_cuts = 'nLepFO_Recl == 2 && Lep1_conept > 25 && Lep2_conept > 20 && met > 15 && mll >12'
    else:
        pff='_withpt'
        common_cuts = 'nLepFO_Recl == 2 && Lep1_pt > 25 && Lep2_pt > 20 && met > 15 && mll >12'

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
    pff1='_usingFRs' if usefr else ''
    commonstr="classification_ultramax_dpsvs"+"_"+bkg+"_"+moretxt+year+pf+pff1+pff

    #fOutname=os.path.join(outdir,commonstr)
    fOut = ROOT.TFile(commonstr+".root","recreate") 
    datasetname='dataset_'+commonstr
    fOut.cd()
    # configuring tmva
    factory = ROOT.TMVA.Factory('TMVAClassification', fOut, "!V:!Color:DrawProgressBar:Transformations=I;D;P;G,D:AnalysisType=Classification" )

    DL = ROOT.TMVA.DataLoader(datasetname)

    # adding list of vars to train on
    if useconept:
        DL.AddVariable('pt1 := Lep1_conept','p_{T1}', 'F')
        DL.AddVariable('pt2 := Lep2_conept','p_{T2}', 'F') 
    else:
        DL.AddVariable('pt1 := Lep1_pt','p_{T1}', 'F')
        DL.AddVariable('pt2 := Lep2_pt','p_{T2}', 'F') 

    DL.AddVariable('met :=  met', 'F')
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
            DL.AddSignalTree(tree,1.0)#glbwt)
        else:
            DL.AddBackgroundTree(tree,1.0)#glbwt)

    #evtwt_sig = "puw * (min(LepGood_mvaTTH[0],LepGood_mvaTTH[1]) > 0.9)"
    #evtwt  = "(run == 1) ? (puWeight * xsec * genWeight * {TTsel} ) : (1.0 * {TLsel})".format(TTsel=TT,TLsel=TL)    #run number is set to 1 for MC samples 
    #DL.SetWeightExpression(evtwt)
    


    if 'wz' in bkg:
        DL.SetWeightExpression("prescaleFromSkim *abs(genWeight)/genWeight")
    else :
        DL.SetSignalWeightExpression("prescaleFromSkim")        
        if(usefr):
            DL.SetBackgroundWeightExpression("fakeRateWt *prescaleFromSkim*Trigger_2lss");
        else:
            DL.SetBackgroundWeightExpression("prescaleFromSkim*Trigger_2lss");
    



    DL.PrepareTrainingAndTestTree(dpscuts,bkgcuts, "!V")

    factory.BookMethod(DL,ROOT.TMVA.Types.kBDT, 'BDTG',
                       ':'.join([
                           '!H',
                           '!V',
                           'NTrees=500',
                           'BoostType=Grad',
                           'Shrinkage=0.10',
                           'UseBaggedBoost',
                           'BaggedSampleFraction=0.50',
                           'nCuts=20',
                           'MaxDepth=2',
                           'CreateMVAPdfs',
                           'NegWeightTreatment=IgnoreNegWeightsInTraining'
                       ]))

    factory.BookMethod(DL,ROOT.TMVA.Types.kBDT, 'BDT',
                       ':'.join([
                           '!H',
                           '!V',
                           'NTrees=450',
                           'MinNodeSize=2.5%',
                           'MaxDepth=2',
                           'BoostType=AdaBoost',
                           'AdaBoostBeta=0.5'
                           'UseBaggedBoost',
                           'BaggedSampleFraction=0.50',
                           'nCuts=20',
                           'CreateMVAPdfs',
                           'SeparationType=GiniIndex',
                           'NegWeightTreatment=IgnoreNegWeightsInTraining'
                       ]))
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
    parser.add_option("-b","--bkg", dest="bkg",type="string", default='wz_amc')
    parser.add_option("-y","--year", dest="year",type="string", default='2016')
    parser.add_option("--cpt", dest="useconept", default=False, action='store_true')
    parser.add_option("--fr", dest="usefr", default=False, action='store_true')
    parser.add_option("--txt",dest="moretxt",type="string", default='')
    #parser.add_option("-o","--outdir", dest="outdir",type="string", default='')
    #parser.add_option("-F","--friend", dest="friends",type="string", default=[], action="append")
    (opts, args) = parser.parse_args()
    #if not os.path.isdir(opts.outdir):
    #    os.system('mkdir -p '+opts.outdir)

    train_classification(opts.year,opts.bkg,opts.useconept,opts.usefr,opts.moretxt)#,opts.outdir)




