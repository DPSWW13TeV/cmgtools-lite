#!/usr/bin/env python
#usage python tmvaProducer_classification.py -b <bkg name wz_amc/wz_pow/fakes> -y <year>
########## change log
#changed afss selection for fakes to mmss on July 14 -> leads to bad data/MC for DNN_fakes in emu channel 2016
#July 16: trying ll_noee_ss final state for both backgrounds to see if agreement improves 
#july 17: afss selection for wz_amc and fixed the cptllCutS cut
#july19: no ee for signal
import sys, os, optparse, subprocess
import ROOT, re
from ROOT import TMVA, TFile, TTree, TCut
from subprocess import call
from os.path import isfile
if "/functions_cc.so" not in ROOT.gSystem.GetLibraries():
    ROOT.gROOT.ProcessLine(".L %s/src/CMGTools/DPSWW/python/plotter/functions.cc+" % os.environ['CMSSW_BASE']);

lumis = {
    '2016': 36.33,
    '2017': 41.53,
    '2018': 59.74,
}
_allfiles = []
path = '/eos/cms/store/cmst3/group/dpsww/NanoTrees_v7_dpsww_04092020/'

signalMC = {
    'py2016':'WWDoubleTo2L',
    'py2017':'WWDoubleTo2L',
    'py2018':'WWDoubleTo2L',
    'hw2016' :'WWDoubleTo2L_herwigpp',
    'hw2017' :'WWDoubleTo2L_herwig',
    'hw2018' :'WWDoubleTo2L_herwig_pvt',
    'ns2016':'WWDoubleTo2L_newsim',
    'ns2017':'WWDoubleTo2L_newsim',
    'ns2018':'WWDoubleTo2L_newsim'
}

def load_dataset(year,name, trainclass,friends=[]): 
    lumi= lumis[year]
    print(lumi)
    mc = 0 if 'Run' in name  else 1 

    fileloc = os.path.join(path,str(year),'%s.root' %name)
    infile = ROOT.TFile.Open(fileloc)
    _allfiles.append(infile)

    tree = infile.Get('Events')
    
    try: tree.GetName()
    except ReferenceError:
        raise RuntimeError("'tree' not found in %s" % fileloc)

    for friend in friends:
        friendloc = os.path.join(path,str(year),friend,'%s_Friend.root' % name)
        print("Adding friend from", friendloc)
        tree.AddFriend('Friends', friendloc) 

    tree_wts = infile.Get('Runs')
    sum_wts=0.0
    
    if(mc == 0):
        weight = 1.0 # since it's data so weight factor is 1
    else:
        for iev in tree_wts:
            sum_wts+= iev.genEventSumw
        weight= lumi*1000/sum_wts
        #print(weight)
    print('Added %s dataset, category %s, with weight %f' %(name, trainclass,weight))

    return tree, weight

def train_classification(year,bkg,useconept,usefr,moretxt,sigMC):
    years=[year] if year != 'all' else ["2016","2017","2018"]
    pf='' #_muWP90_elWP70' if year == '2017' else ''
    frnds=['2_recl','bdt_input_vars_toInfnBeynd'] #'lastChk']#

    friends=[name+pf for name in frnds]
    eleID  = '(abs(Lep1_pdgId)!=11 || ( Lep1_tightCharge>=2)) && (abs(Lep2_pdgId)!=11 || (Lep2_tightCharge>=2))'
    muon   = '(abs(Lep1_pdgId)!=13 || Lep1_tightCharge>=1) && (abs(Lep2_pdgId)!=13 || Lep2_tightCharge>=1)'
    mmss   = '(Lep1_pdgId*Lep2_pdgId) == 169'
    afac   = '(abs(Lep1_pdgId*Lep2_pdgId) == 169 || abs(Lep1_pdgId*Lep2_pdgId) == 121 ||  abs(Lep1_pdgId*Lep2_pdgId) == 143)'
    noee   = '(abs(Lep1_pdgId*Lep2_pdgId) == 169 ||  abs(Lep1_pdgId*Lep2_pdgId) == 143)'
    afss   = '(Lep1_pdgId*Lep2_pdgId == 169 || Lep1_pdgId*Lep2_pdgId == 121 || Lep1_pdgId*Lep2_pdgId == 143)'
    TT     = '(Lep1_isLepTight &&  Lep2_isLepTight)'
    TL     = '((Lep1_isLepTight &&  !Lep2_isLepTight) || (!Lep1_isLepTight &&  Lep2_isLepTight))'
    dimu   = '(abs(Lep1_pdgId) == 13 && abs(Lep2_pdgId) == 13)'
    ll_noee_ss      = '(Lep1_pdgId*Lep2_pdgId == 169 || Lep1_pdgId*Lep2_pdgId == 143)'

    cptllCut= '{here} || cptll > 20'.format(here=dimu)


    dsets =[]
    if ('wz' in bkg):
        cuts = 'nLepFO_Recl == 2 && Lep1_pt > 25 && Lep2_pt > 20 && met > 15 && mll >12 && Lep1_isLepTight &&  Lep2_isLepTight && ((abs(Lep1_pdgId) == 13 && abs(Lep2_pdgId) == 13) || cptll > 20) && (abs(Lep1_pdgId)!=11 || ( Lep1_tightCharge>=2)) && (abs(Lep2_pdgId)!=11 || (Lep2_tightCharge>=2)) && (abs(Lep1_pdgId)!=13 || Lep1_tightCharge>=1) && (abs(Lep2_pdgId)!=13 || Lep2_tightCharge>=1)'
        for yr in years:            
            dsets.append((signalMC[sigMC+yr],"Signal",friends,yr))
            if (bkg == 'wz_amc'):
                dsets.append(('WZTo3LNu_fxfx',"Background",friends,yr))
            else:
                dsets.append(('WZTo3LNu',"Background",friends,yr))

    else: 
        #bkgSel = TL + '&&'+ cptllCut + '&&'+ ll_noee_ss
        cuts = 'nLepFO_Recl == 2 && Lep1_pt > 25 && Lep2_pt > 20 && met > 15 && mll >12 && ((abs(Lep1_pdgId) == 13 && abs(Lep2_pdgId) == 13) || cptll > 20) &&  ( run == 1 ? ( Lep1_isLepTight &&  Lep2_isLepTight && (abs(Lep1_pdgId*Lep2_pdgId) == 169 ||  abs(Lep1_pdgId*Lep2_pdgId) == 143)) : ( ((Lep1_isLepTight &&  !Lep2_isLepTight) || (!Lep1_isLepTight &&  Lep2_isLepTight))  && (Lep1_pdgId*Lep2_pdgId == 169 || Lep1_pdgId*Lep2_pdgId == 143) )) && (abs(Lep1_pdgId)!=11 || ( Lep1_tightCharge>=2)) && (abs(Lep2_pdgId)!=11 || (Lep2_tightCharge>=2)) && (abs(Lep1_pdgId)!=13 || Lep1_tightCharge>=1) && (abs(Lep2_pdgId)!=13 || Lep2_tightCharge>=1)'
        
        for yr in years:
            dsets.append((signalMC[sigMC+yr],"Signal",friends,yr))
            #dsets.append(('WWDoubleTo2L',"Signal",friends,yr))
            ds=os.listdir(os.path.join(path,yr))
            datasets=[x.split('.root')[0] for x in ds if 'Run' in x]
            for i in datasets:
                dsets.append((i,"Background",friends,yr))

    if useconept:
        #print 'training using conept'
        pff='_withcpt'
    else:
        pff='_withpt'
    
    bkgcuts = ROOT.TCut('1');
    bkgcuts += cuts
    bkgcuts += ll_noee_ss
    dpscuts = ROOT.TCut('1')
    dpscuts += cuts
    dpscuts += afac

    datasets = []
    for name, trainclass, frnds,year in dsets:
        tree, glbwt = load_dataset(year,name,trainclass,frnds)
        print(tree,glbwt)
        datasets.append((name, trainclass, tree, glbwt))
    pff1='_usingFRs' if usefr else ''
    commonstr="Nov2021_dpsWW"+"_"+sigMC+"_"+bkg+"_"+moretxt+year+pf+pff1+pff
    # Setup TMVA
    TMVA.Tools.Instance()
    TMVA.PyMethodBase.PyInitialize()
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
    DL.AddVariable('etadiff   := (Lep1_eta-Lep2_eta)','(#eta_{1}-#eta_{2})','F')
    #DL.AddVariable('dRll := dRll','dR_{ll}','F')
    #DL.AddVariable('mll :=mll', 'F')
    #DL.AddVariable('cptll := cptll', 'F')
    #DL.AddVariable('deltadz := deltadz', 'F')
    #DL.AddVariable('deltadxy := deltadxy', 'F')


##am    DL.AddSpectator('lep1_id := Lep1_isLepTight', 'I')
##am    DL.AddSpectator('lep2_id := Lep2_isLepTight', 'I')
##am    DL.AddSpectator('dilep_flav := (Lep1_pdgId*Lep2_pdgId)', 'I')
##am    DL.AddSpectator('lep1_pdgId := Lep1_pdgId', 'I')
##am    DL.AddSpectator('lep2_pdgId := Lep2_pdgId', 'I')
##am    DL.AddSpectator('nLepFO :=nLepFO_Recl', 'I')
##am    DL.AddSpectator('lep1_tc := Lep1_tightCharge', 'I')
##am    DL.AddSpectator('lep2_tc := Lep2_tightCharge', 'I')
##am    DL.AddSpectator('run := run', 'I')

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
    # Generate model
 

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
    parser.add_option("-s","--sig",dest="sigMC",type="string", default='py')
    #parser.add_option("-o","--outdir", dest="outdir",type="string", default=os.getcwd())
    #parser.add_option("-F","--friend", dest="friends",type="string", default=[], action="append")
    (opts, args) = parser.parse_args()
    #if not os.path.isdir(opts.outdir):
    #    os.system('mkdir -p '+opts.outdir)

    train_classification(opts.year,opts.bkg,opts.useconept,opts.usefr,opts.moretxt,opts.sigMC)




