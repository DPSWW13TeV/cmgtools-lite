from PhysicsTools.NanoAODTools.postprocessing.framework.eventloop import Module 
from PhysicsTools.NanoAODTools.postprocessing.framework.datamodel import Collection as Collection 
from CMGTools.VVsemilep.tools.nanoAOD.friendVariableProducerTools import writeOutput
import os, math
import ROOT

    
class toppTrwt(Module):
    def __init__(self):
        self.label = "" # "" if (label in ["",None]) else ("_"+label)
        self.vars = ("pt","eta","phi","mass","pdgId","status","statusFlags")
        pass
    def beginJob(self):
        pass
    def endJob(self):
        pass

    def beginFile(self, inputFile, outputFile, inputTree, wrappedOutputTree):
        self.out = wrappedOutputTree

        self.out.branch("nGentops"+self.label,"I")
        self.out.branch("Top_pTrw"+self.label,"F")
        for V in self.vars:
            self.out.branch("Gentops"+self.label+"_"+V, "F", lenVar="nGentops"+self.label)


    def endFile(self, inputFile, outputFile, inputTree, wrappedOutputTree):
        pass
  
    def if3(self,cond, iftrue, iffalse):
        return iftrue if cond else iffalse


    def analyze(self, event):
        """process event, return True (go to next module) or False (fail, go to next event)"""
 
        genparticles=Collection(event,"GenPart")
        tops=[];         ret={};   
        
        foundt=False;foundtbar=False; tgenPt=0.0; AtopPt=0.0;
        for iGen in genparticles:
            if abs(iGen.pdgId) == 6:
                lastcopy=ROOT.TMath.Odd(iGen.statusFlags/(1<<13))
                #       print 'in here',lastcopy
                if iGen.pdgId == 6 and lastcopy:
                    topPt=iGen.pt;foundt=True;
                    tops.append(iGen)
                if iGen.pdgId == -6 and lastcopy:
                    AtopPt=iGen.pt;foundtbar=True;
                    tops.append(iGen)
            else: continue
        #print 'num top',len(tops),
        sf=1.0
        if len(tops)==2 and foundt and foundtbar:
            sf=(math.sqrt(math.exp(0.0615 - 0.0005 * topPt) * math.exp(0.0615 - 0.0005 * AtopPt)))
        #print sf




        self.out.fillBranch('Top_pTrw'+self.label,sf)    
        self.out.fillBranch('nGentops'+self.label,len(tops))

        for V in self.vars:
            ret["Gentops"+self.label+"_"+V] = [getattr(j,V) for j in tops]

        for V in self.vars:
            self.out.fillBranch("Gentops"+self.label+"_"+V, [ ret["Gentops"+self.label+"_"+V][j] for j in range (len(tops))])

        return True
