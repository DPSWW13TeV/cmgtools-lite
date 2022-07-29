#!/usr/bin/env python 
import sys, os, optparse, subprocess
import ROOT, re
from array import array
 
# Setup TMVA

def eval_bdt(year):
    _allfiles=[]
    fin = ROOT.TFile.Open("/eos/cms/store/cmst3/group/dpsww/forWWmixing/%s/mixed/WJetsToLNu_LO_Friend.root"%year)
    _allfiles.append(fin)
    tree_in = fin.Get('Friends')

 
    branches = {}
    Lep1_pt      =array('f',[0]);Lep2_pt       =array('f',[0]);
    Lep1_eta     =array('f',[0]);Lep2_eta      =array('f',[0]);
    met          =array('f',[0]);mt2           =array('f',[0]);
    mtll         =array('f',[0]);mtl1met       =array('f',[0]);
    dphill       =array('f',[0]);dphil2met     =array('f',[0]);
    dphilll2     =array('f',[0]);
    etasum       =array('f',[0]);etaprod       =array('f',[0]);
    
 
    tree_in.SetBranchAddress("Lep1_pt",Lep1_pt)
    tree_in.SetBranchAddress("Lep2_pt",Lep2_pt)
    tree_in.SetBranchAddress("Lep1_pt",Lep1_pt)
    tree_in.SetBranchAddress("Lep2_pt",Lep2_pt)
    tree_in.SetBranchAddress("met",met)
    tree_in.SetBranchAddress("mt2",mt2)
    tree_in.SetBranchAddress("mtll",mtll) 
    tree_in.SetBranchAddress("mtl1met",mtl1met)
    tree_in.SetBranchAddress("dphill",dphill)
    tree_in.SetBranchAddress("dphil2met",dphil2met)
    tree_in.SetBranchAddress("dphilll2",dphilll2)
    
    ROOT.TMVA.Tools.Instance()
    ROOT.TMVA.PyMethodBase.PyInitialize()
    reader = ROOT.TMVA.Reader("Color:!Silent")
    cmg="/afs/cern.ch/work/a/anmehta/public/dpsww_runII/CMSSW_10_2_16_UL/src/CMGTools/DPSWW/python/plotter/BDTtraining/"
    wts_py_wz_amc  = cmg+'dataset_Oct2021_dpsWW_py_wz_amc_%s_withpt/weights/TMVAClassification_BDTG.weights.xml'%(year)
    #wts_py_TL      = cmg+'dataset_Oct2021_dpsWW_py_TL_%s_withpt/weights/TMVAClassification_BDTG.weights.xml'%("2018")

    
    reader.AddVariable("Lep1_pt",Lep1_pt)
    reader.AddVariable("Lep2_pt",Lep2_pt)
    reader.AddVariable("met",met)
    reader.AddVariable("mt2",mt2)
    reader.AddVariable("mtll",mtll) 
    reader.AddVariable("mtl1met",mtl1met)
    reader.AddVariable("dphill",dphill)
    reader.AddVariable("dphil2met",dphil2met)
    reader.AddVariable("dphilll2",dphilll2)
    reader.AddVariable("Lep1_eta*Lep2_eta",etaprod)
    reader.AddVariable("abs(Lep1_eta+Lep2_eta)",etasum)
    
 
    fout=ROOT.TFile("/eos/cms/store/cmst3/group/dpsww/forWWmixing/%s/BDTWZ/WJetsToLNu_LO_Friend.root"%year,"recreate");
    tree_out = ROOT.TTree("Friends","BDT information");
    BDTG_DPS_WZ_amc_raw_withpt=array('f',[-999]);
    #BDTG_DPS_TLCR_raw_withpt=array('f',[-999]);

    #tree_out.Branch("BDTG_DPS_TLCR_raw_withpt",BDTG_DPS_TLCR_raw_withpt,"BDTG_DPS_TLCR_raw_withpt/F");
    tree_out.Branch("BDTG_DPS_WZ_amc_raw_withpt",BDTG_DPS_WZ_amc_raw_withpt,"BDTG_DPS_WZ_amc_raw_withpt/F");

    # Book methods
    reader.BookMVA('BDTG_method',wts_py_wz_amc)
    #reader.BookMVA('BDTG_method',wts_py_TL)
 
    for  entryNum  in  range(0,tree_in.GetEntries ()):
        tree_in.GetEntry(entryNum)
        #print reader.EvaluateMVA('BDTG_method')
        BDTG_DPS_WZ_amc_raw_withpt[0]=reader.EvaluateMVA('BDTG_method')
        #BDTG_DPS_TLCR_raw_withpt[0]=reader.EvaluateMVA('BDTG_method')
        #print(DNN_score[0])
        tree_out.Fill();

    #tree_out.Write();
    fout.Write()
    fout.Close();
if __name__ == '__main__':

    parser = optparse.OptionParser(usage='usage: %prog [opts] ', version='%prog 1.0')
    parser.add_option("-y","--year", dest="year",type="string", default='2016')
    (opts, args) = parser.parse_args()
    #if not os.path.isdir(opts.outdir):
    #    os.system('mkdir -p '+opts.outdir)
    eval_bdt(opts.year)


