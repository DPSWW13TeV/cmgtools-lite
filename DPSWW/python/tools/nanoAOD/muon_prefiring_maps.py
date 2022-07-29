#saves variables only if nlep >1
from PhysicsTools.NanoAODTools.postprocessing.framework.eventloop import Module
from PhysicsTools.NanoAODTools.postprocessing.framework.datamodel import Collection 
import ROOT
import os, math
import array, numpy
from ROOT import TLorentzVector

class muon_prefiring_maps(Module):
    def __init__(self,year,mupfmaps):
        self.mupfmaps = mupfmaps
        self.year=year
        pass
    def beginFile(self, inputFile, outputFile, inputTree, wrappedOutputTree):
        self.out = wrappedOutputTree
        self.out.branch("nLepFO","I")
        self.out.branch('l1muonprefire_prob', "F", lenVar="nLepFO")

    def mupfsf_stat(self,lep):
        fName = ROOT.TFile.Open(self.mupfmaps)
        if not fName: raise RuntimeError("No such file %s"%self.mupfmaps)
        hpf =  fName.Get("muprefiringwts")
        pfP=0.0; #pfP_err=0.0; pfP_up=0.0;tmpval = 0.0;pfB=0
        nB = hpf.GetNbinsX();
        if abs(lep.pdgId) == 11: return pfP
        else:
            pfB = max(1,min(hpf.GetXaxis().FindFixBin(abs(lep.eta)), nB));
            pfP = hpf.GetBinContent(pfB,3)/(math.exp((lep.pt - hpf.GetBinContent(pfB,1))/hpf.GetBinContent(pfB, 2) ) + 1);
            if(pfP < 0):                 pfP = 0.0;
            elif(pfP >1):                pfP=1.0;            
        fName.Close()
        return pfP


    def if3(self,cond, iftrue, iffalse):
        return iftrue if cond else iffalse

    def analyze(self, event):

        # leptons
        all_leps  = [l for l in Collection(event,"LepGood")]
        nFO       = getattr(event,"nLepFO_Recl")
        chosen    = getattr(event,"iLepFO_Recl")
        leps      = [all_leps[chosen[i]] for i in xrange(nFO)]
        self.out.fillBranch('nLepFO',len(leps))
        l1muonprefire_wt=[]
        for lep in leps:
            if self.year == "2016":
                #print self.mupfsf_stat(lep,2)
                l1muonprefire_wt.append(self.mupfsf_stat(lep))
            else:                l1muonprefire_wt.append(-99)

        self.out.fillBranch("l1muonprefire_prob", [l1muonprefire_wt[j] for j in range(len(leps))])
        #for i in range(len(leps)):    
        #    self.out.fillBranch('l1muonprefire_wt_dn',l1muonprefire_wt_dn[i])
        #    self.out.fillBranch('l1muonprefire_wt_up',l1muonprefire_wt_up[i])
        #    self.out.fillBranch('l1muonprefire_wt',l1muonprefire_wt[i])
        return True







