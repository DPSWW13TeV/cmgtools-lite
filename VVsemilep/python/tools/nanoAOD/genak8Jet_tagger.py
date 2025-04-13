from PhysicsTools.NanoAODTools.postprocessing.framework.eventloop import Module 
from PhysicsTools.NanoAODTools.postprocessing.framework.datamodel import Collection as Collection 
from CMGTools.VVsemilep.tools.nanoAOD.friendVariableProducerTools import writeOutput
from PhysicsTools.NanoAODTools.postprocessing.tools import deltaR, deltaPhi
from PhysicsTools.NanoAODTools.postprocessing.tools import closest
import os, math
import ROOT

    
class genak8Jet_tagger(Module):
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

        self.out.branch("ak8hadflav"+self.label,"I")

    def endFile(self, inputFile, outputFile, inputTree, wrappedOutputTree):
        pass
  
    def if3(self,cond, iftrue, iffalse):
        return iftrue if cond else iffalse


    def analyze(self, event):
        """process event, return True (go to next module) or False (fail, go to next event)"""
 
        genparticles=Collection(event,"GenPart")
        fatjets= [j for j in Collection(event,"ak8sDMgt45")]
        quarks=[];  
        bosons=[]; 
        for iGen in genparticles:
            if abs(iGen.pdgId) < 6:
                lastcopy=ROOT.TMath.Odd(iGen.statusFlags/(1<<13))
                #       print 'in here',lastcopy
                if iGen.genPartIdxMother != -1 and lastcopy:
                    for m,iMa in enumerate(genparticles):
                        if m == iGen.genPartIdxMother and (abs(iMa.pdgId) in [24,23,25]): #,abs(iGen.pdgId)]):
                            bosons.append(iMa)
                            quarks.append(iGen)
                            break;
                        else: continue
        #print('found qs',len(quarks),'and vbosons',len(bosons))
        #print 'num top',len(tops),
        sf=1.0; foundCombo=False
        if len(quarks)==2 and  quarks[0].pdgId*quarks[1].pdgId <0 and len(bosons) > 0 :
            print('i found the combo')
            foundCombo=True
        if foundCombo:
            for i,j in enumerate(fatjets):
                dR1=deltaR(j.eta,j.phi,quarks[0].eta,quarks[0].phi)
                dR2=deltaR(j.eta,j.phi,quarks[1].eta,quarks[1].phi)
                print('delta R for fj',i,' ',dR1,dR2,j.pt,j.eta)
                #fJ, fJ_dr = closest(j, quarks) #this returns the mindR and associated quark
                #print('delta R for closest',' ',fJ_dr,fJ.pt,fJ.eta)
        #print sf



#
#        self.out.fillBranch('Top_pTrw'+self.label,sf)    
#        self.out.fillBranch('nGentops'+self.label,len(tops))
#        self.out.fillBranch('nGenalltops'+self.label,len(alltops))
#        for V in self.vars:
#            ret["Gentops"+self.label+"_"+V] = [getattr(j,V) for j in tops]
#            retA["Genalltops"+self.label+"_"+V] = [getattr(j,V) for j in alltops]
#        for V in self.vars:
#            self.out.fillBranch("Gentops"+self.label+"_"+V, [ ret["Gentops"+self.label+"_"+V][j] for j in range (len(tops))])
#            self.out.fillBranch("Genalltops"+self.label+"_"+V, [ retA["Genalltops"+self.label+"_"+V][j] for j in range (len(alltops))])
        return True
