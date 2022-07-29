import ROOT
ROOT.PyConfig.IgnoreCommandLineOptions = True

from PhysicsTools.NanoAODTools.postprocessing.framework.eventloop import Module
from PhysicsTools.NanoAODTools.postprocessing.framework.datamodel import Collection 
import itertools


def isGooddlep(dlep):
    if (dlep.pt > 20.0 and dlep.hasTauAnc == 0 and abs(dlep.eta) < (2.5 if abs(dlep.pdgId) == 11 else 2.4)):
        if abs(dlep.pdgId)==11:
            return (abs(dlep.eta) < 1.442 or abs(dlep.eta) > 1.556)
        else: 
            return True
    else: return False

class dpswwfidevtskimmer( Module ):
    def __init__(self, ndleps = 2, ssWW = True, noTaus = True): 

        self.ndleps=ndleps
        self.ssWW = ssWW
        self.noTau = noTaus
        pass

    def beginJob(self):
        pass

    def endJob(self):
        pass

    def beginFile(self, inputFile, outputFile, inputTree, wrappedOutputTree):
        self.out = wrappedOutputTree

    def endFile(self, inputFile, outputFile, inputTree, wrappedOutputTree):
        pass

    def analyze(self, event):
        """process event, return True (go to next module) or False (fail, go to next event)"""
        dleps = filter(isGooddlep, Collection(event,"GenDressedLepton"))
        if event.nGenDressedLepton == self.ndleps and self.ndleps == len(dleps) :
            l1=dleps[0];l2 = dleps[1]
            mll = (l1.p4() + l2.p4()).M()
            ptll = (l1.p4() + l2.p4()).Pt()
            if (mll > 12 and  ((l1.pdgId * l2.pdgId) > 0)  and (abs(l1.pdgId*l2.pdgId) ==169 or ptll > 20.0) and l1.pt > 25.0 and (abs(l1.pdgId) ==13 or  abs(l2.pdgId) ==13 ) ):
                #print 'bingo'
                return True
            else: False
        else: 
            return False
