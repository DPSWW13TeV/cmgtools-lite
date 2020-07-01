import ROOT, os
ROOT.PyConfig.IgnoreCommandLineOptions = True
import math
from CMGTools.DPS13TeV.postprocessing.framework.datamodel import Collection
from CMGTools.DPS13TeV.postprocessing.framework.eventloop import Module
from PhysicsTools.HeppyCore.utils.deltar import deltaR,deltaPhi


from ROOT import TLorentzVector


#ROOT.gROOT.ProcessLine('.L %s/src/CMGTools/DPS13TeV/python/plotter/functions.cc+' % os.environ['CMSSW_BASE']);
def phill(pt1,eta1,phi1,m1,pt2,eta2,phi2,m2):

    lep1=ROOT.TLorentzVector(0.0,0.0,0.0,0.0); lep2=ROOT.TLorentzVector(0.0,0.0,0.0,0.0);

    lep1.SetPtEtaPhiM(pt1,eta1,phi1,m1); 
    lep2.SetPtEtaPhiM(pt2,eta2,phi2,m2);
    return (lep1+lep2).Phi();

def dphi(phi1,phi2):

    result = phi1 - phi2

    while (result > math.pi):
        result -= 2*math.pi;
    while (result <= -math.pi):
        result += 2*math.pi;

    return result


def mt(pt1,phi1,pt2,phi2):
    return math.sqrt(2*pt1*pt2*(1-math.cos(phi1-phi2)));


def calcmt2(l1,l2,metpt,metphi):
    
    import array
    import numpy

    from ROOT.heppy import Davismt2
    davismt2 = Davismt2()    

    met=ROOT.TLorentzVector(0.0,0.0,0.0,0.0);  
    lep1=ROOT.TLorentzVector(0.0,0.0,0.0,0.0);
    lep2=ROOT.TLorentzVector(0.0,0.0,0.0,0.0);

    met.SetPtEtaPhiM(metpt,0.,metphi,0.);
    lep1.SetPtEtaPhiM(l1.pt,l1.eta,l1.phi,l1.mass);
    lep2.SetPtEtaPhiM(l2.pt,l2.eta,l2.phi,l2.mass);

    metVec = array.array('d',[met.M(),met.Px(), met.Py()])
    lep1Vec = array.array('d',[lep1.M(),lep1.Px(), lep1.Py()])
    lep2Vec = array.array('d',[lep2.M(),lep1.Px(),lep2.Py()])

    davismt2.set_momenta(lep1Vec,lep2Vec,metVec);
    davismt2.set_mn(0);

    return davismt2.get_mt2()

def fakeRateWeight_2lssmva_smoothed_FR(elhist,muhist,lep1,lep2,WP=0.9):

    nfail = (lep1.mvaTTH < WP)+(lep2.mvaTTH < WP)
    if (nfail == 1):
        wt = fakeRatefromHist(elhist,muhist,lep1) if (lep1.mvaTTH < lep2.mvaTTH) else fakeRatefromHist(elhist,muhist,lep2)
        evtwt=wt/(1-wt)
    elif(nfail == 2):
        wt1 = fakeRatefromHist(elhist,muhist,lep1)
        wt2 = fakeRatefromHist(elhist,muhist,lep2)
        evtwt=-wt1*wt2/((1-wt1)*(1-wt2));
    else: evtwt=0
    return evtwt

def fakeRatefromHist(elhist,muhist,lep):

    if (abs(lep.pdgId) == 11):
        fName=ROOT.TFile.Open(elhist)
    else:
        fName=ROOT.TFile.Open(muhist)
    hist=fName.Get('fakerates_smoothed_data')

    
    etabin = max(1, min(hist.GetNbinsX(), hist.GetXaxis().FindBin(abs(lep.eta))))
    #print 'bin in eta is %d' %etabin
    p0 = hist.GetBinContent(etabin, 1);
    p1 = hist.GetBinContent(etabin, 2);
    #print 'pt is %f' %lep.pt	    
    fr = (p0 + p1*lep.pt) if lep.pt < 45.0 else  (p0 + p1*45)
    #print p0,p1,fr
    return fr;


class fakeRateWtSaver(Module):
    def __init__(self,muFile,elFile):
        self.label = "" 
        self.FilewithMuFRhist='%s/src/CMGTools/DPS13TeV/python/plotter/dpsww13TeV/dps2016/fakerates/%s' % (os.environ['CMSSW_BASE'],muFile)
        self.FilewithElFRhist='%s/src/CMGTools/DPS13TeV/python/plotter/dpsww13TeV/dps2016/fakerates/%s' % (os.environ['CMSSW_BASE'],elFile)
        pass
    def beginJob(self):
        pass
    def endJob(self):
        pass
    def beginFile(self, inputFile, outputFile, inputTree, wrappedOutputTree):
        self.out = wrappedOutputTree
        #self.out.branch("nLepGood","I")
        self.out.branch("fakeRateWt","F")
        self.out.branch('mt2',"F")
        self.out.branch('mtll',"F")
        self.out.branch('mtl1met',"F")
        self.out.branch('dphill',"F")
        self.out.branch('dphil2met',"F")
        self.out.branch('dphilll2', "F")


    def endFile(self, inputFile, outputFile, inputTree, wrappedOutputTree):
        pass

    def lepF0(self,lep):
        if (lep.pt > 20.0 and abs(lep.eta) < (2.5 if abs(lep.pdgId) == 11 else 2.4) and lep.tightCharge > 1 ):
            if abs(lep.pdgId)==11:
                return (lep.chargeConsistency >= 3 and lep.idEmuTTH and (abs(lep.eta) < 1.442 or abs(lep.eta) > 1.556) and lep.convVeto > 0)
            else: 
                return (lep.mediumMuonId > 0 and lep.lostHits ==  0 ) #
        else:
            return False

    def analyze(self, event):
        """process event, return True (go to next module) or False (fail, go to next event)"""
        #FOleps = [l for l in filter(self.lepF0,Collection(event,"LepGood"))]
        #lep=Collection(event,"LepGood")
        FOleps = [l for l in Collection(event,"LepGood","nLepGood")]

        weight=  fakeRateWeight_2lssmva_smoothed_FR(self.FilewithElFRhist,self.FilewithMuFRhist,FOleps[0],FOleps[1],0.9) if len(FOleps) > 1 else 1.0;
        met_pt  = getattr(event, "met_pt")
        met_phi = getattr(event, "met_phi")
        mt2        = calcmt2(FOleps[0],FOleps[1],met_pt,met_phi) if len(FOleps) > 1 else 0;
        mtll    = mt(FOleps[0].pt,FOleps[0].phi,FOleps[1].pt,FOleps[1].phi) if len(FOleps) > 1 else 0;
        mtl1met = mt(FOleps[0].pt,FOleps[0].phi,met_pt,met_phi) if len(FOleps) > 1 else 0;
        dphill  = abs(dphi(FOleps[0].phi,FOleps[1].phi)) if len(FOleps) > 1 else -999;
        dphil2met = abs(dphi(FOleps[1].phi,met_phi)) if len(FOleps) > 1 else -999;
        dphilll2  = abs(dphi(phill(FOleps[0].pt,FOleps[0].eta,FOleps[0].phi,FOleps[0].mass,FOleps[1].pt,FOleps[1].eta,FOleps[1].phi,FOleps[1].mass),FOleps[1].phi)) if len(FOleps) > 1 else -999;
        #print weight
        self.out.fillBranch('fakeRateWt',weight)
        self.out.fillBranch('mt2', mt2)     
        self.out.fillBranch('mtll',mtll)     
        self.out.fillBranch('mtl1met',mtl1met)  
        self.out.fillBranch('dphill',dphill)   
        self.out.fillBranch('dphil2met',dphil2met) 
        self.out.fillBranch('dphilll2', dphilll2)



        return True

eventWt = lambda : fakeRateWtSaver("fakerate_promptrate_mu_smoothed_data_2018-06-27.root","2018-07-27ElFR_nominal/fakerate_promptrate_el_smoothed_data.root")


