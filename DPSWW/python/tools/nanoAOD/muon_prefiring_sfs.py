#saves variables only if nlep >1
from PhysicsTools.NanoAODTools.postprocessing.framework.eventloop import Module
from PhysicsTools.NanoAODTools.postprocessing.framework.datamodel import Collection 
import ROOT
import os, math
import array, numpy
from ROOT import TLorentzVector

class muon_prefiring_sfs(Module):
    def __init__(self,year,mupfmaps):
        self.mupfmaps = mupfmaps
        self.year=year
        pass
    def beginFile(self, inputFile, outputFile, inputTree, wrappedOutputTree):
        self.out = wrappedOutputTree
        self.out.branch('l1muonprefire_sf',"F")
        self.out.branch('l1muonprefire_sf_up',"F")
        self.out.branch('l1muonprefire_sf_dn',"F")


    def mupfsf_stat(self,leps,var):
        sf=[1.0,1.0,1.0];
        fName = ROOT.TFile.Open(self.mupfmaps)
        if not fName: raise RuntimeError("No such file %s"%self.mupfmaps)
        hpf =  fName.Get("muprefiringwts")
        pfP=0.0; #pfP_err=0.0; pfP_up=0.0;tmpval = 0.0;pfB=0
        nB = hpf.GetNbinsX();
        for i in range(len(leps)):
            if abs(leps[i].pdgId) == 11: continue
            pfB = max(1,min(hpf.GetXaxis().FindFixBin(abs(leps[i].eta)), nB));
            pfP = hpf.GetBinContent(pfB,3)/(math.exp((leps[i].pt - hpf.GetBinContent(pfB,1))/hpf.GetBinContent(pfB, 2) ) + 1);
            if(pfP < 0): pfP = 0.0;
            elif(pfP >1):pfP=1.0;            
            sf[0]*= (1.0 - min(1.0, pfP)); #nominal
            sf[1]*= (1.0 - min(1.0, 1.11*pfP)); #up
            sf[2]*= (1.0 - min(1.0, 0.89*pfP)); #down
        fName.Close()
        return sf[var]


    def if3(self,cond, iftrue, iffalse):
        return iftrue if cond else iffalse

    def analyze(self, event):

        # leptons
        all_leps  = [l for l in Collection(event,"LepGood")]
        nFO       = getattr(event,"nLepFO_Recl")
        chosen    = getattr(event,"iLepFO_Recl")
        leps      = [all_leps[chosen[i]] for i in xrange(nFO)]
        if self.year == "2016":
            l1muonprefire_sf_dn=self.mupfsf_stat(leps,2)        
            l1muonprefire_sf_up=self.mupfsf_stat(leps,1)        
            l1muonprefire_sf=self.mupfsf_stat(leps,0)        
        else:
            l1muonprefire_sf_dn=1.0
            l1muonprefire_sf_up=1.0
            l1muonprefire_sf=1.0
            
        self.out.fillBranch('l1muonprefire_sf_dn',l1muonprefire_sf_dn)
        self.out.fillBranch('l1muonprefire_sf_up',l1muonprefire_sf_up)
        self.out.fillBranch('l1muonprefire_sf',l1muonprefire_sf)
        return True







