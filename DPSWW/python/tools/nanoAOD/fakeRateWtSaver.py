from PhysicsTools.NanoAODTools.postprocessing.framework.eventloop import Module
from PhysicsTools.NanoAODTools.postprocessing.framework.datamodel import Collection 
import ROOT

class fakeRateWtSaver( Module ):
    def __init__(self,FRFile):
        self.FRFile = FRFile #os.environ["CMSSW_BASE"]+'/src/CMGTools/DPSWW/python/plotter/plots/104X/ttH/lepMVA/v1.1/fr-comb/fr_2016_MVA_mupt90_elpt70.root' #_FRFile
        pass

    def beginFile(self, inputFile, outputFile, inputTree, wrappedOutputTree):
        self.out = wrappedOutputTree
        self.out.branch("fakeRateWt","F")
        pass
    def fakeRateWeight_2lss(self,lep1,lep2):
        nfail = (lep1.isLepTight_Recl + lep2.isLepTight_Recl)
        if (nfail == 1):
            wt = self.fakeRatefromHist(lep1) if not lep1.isLepTight_Recl else self.fakeRatefromHist(lep2)
            evtwt=wt/(1-wt)
        elif(nfail == 2):
            wt1 = self.fakeRatefromHist(lep1)
            wt2 = self.fakeRatefromHist(lep2)
            evtwt=-wt1*wt2/((1-wt1)*(1-wt2));
        else: evtwt=0
        return evtwt

    def fakeRatefromHist(self,lep):

        fName = ROOT.TFile.Open(self.FRFile)
        hist =  fName.Get('FR_mva070_el_data_comb_NC' if abs(lep.pdgId) == 11 else 'FR_mva090_mu_data_comb') 
    
        ptbin  = max(1, min(hist.GetNbinsX(), hist.GetXaxis().FindBin(lep.conePt)))
        etabin = max(1, min(hist.GetNbinsX(), hist.GetXaxis().FindBin(abs(lep.eta))))
        fr     = hist.GetBinContent(ptbin,etabin)

        return fr; 

    def analyze(self, event):
        all_leps = [l for l in Collection(event,"LepGood")]
        nFO = getattr(event,"nLepFO_Recl")
        chosen = getattr(event,"iLepFO_Recl")
        leps = [all_leps[chosen[i]] for i in xrange(nFO)]

        weight=  1.0 #self.fakeRateWeight_2lss(leps[0],leps[1]) if nFO > 1 else 1.0;
        #print weight
        self.out.fillBranch('fakeRateWt',weight)

        return True




