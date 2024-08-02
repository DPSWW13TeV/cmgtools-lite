###FIXME : add leptight variables
from PhysicsTools.NanoAODTools.postprocessing.framework.eventloop import Module 
from PhysicsTools.NanoAODTools.postprocessing.framework.datamodel import Collection 
import ROOT as r 

from math import sqrt, cos
from PhysicsTools.NanoAODTools.postprocessing.tools import deltaR, deltaPhi
from PhysicsTools.Heppy.physicsobjects.Jet import _btagWPs

from copy import deepcopy

class saveGoodak8Jet(Module):
    def __init__(self,isMC,massVar='sD',jecs=[]):
        self.isMC=isMC
        self.jecs=jecs
        self.shift=["Up","Down"] 
        self.vars=["eta","phi","mass","pt","btagDeepB","particleNetMD_Xqq","particleNetMD_Xbb","particleNetMD_Xcc","particleNetMD_QCD","particleNet_WvsQCD","particleNet_ZvsQCD","particleNet_mass","msoftdrop","deepTag_WvsQCD","tau1","tau2","hadronFlavour","muonIdx3SJ","electronIdx3SJ","nBHadrons","nCHadrons"] if self.isMC else ["eta","phi","mass","pt","btagDeepB","particleNetMD_Xqq","particleNetMD_Xbb","particleNetMD_Xcc","particleNetMD_QCD","particleNet_WvsQCD","particleNet_ZvsQCD","particleNet_mass","deepTag_WvsQCD","tau1","tau2","msoftdrop"]
        if self.isMC: 
            self.vars+=["pt_"+jec+sh for jec in self.jecs for sh in self.shift]
            self.vars+=["msoftdrop_"+jec+sh for jec in self.jecs for sh in self.shift]
        print type(self.vars)
        self.massVar=massVar
        pass
    def beginFile(self, inputFile, outputFile, inputTree, wrappedOutputTree):
        self.out = wrappedOutputTree
        self.out.branch('event', 'L')
        self.out.branch('nak8%sMgt45'%self.massVar  ,'I')
        for var in self.vars:
            self.out.branch('ak8%sMgt45_%s'%(self.massVar,var), "F", lenVar="nak8%sMgt45"%self.massVar)
        self.out.branch('ak8%sMgt45_pNetWtagscore'%(self.massVar), "F", lenVar="nak8%sMgt45"%self.massVar)

    def beginJob(self):
        pass
    def endJob(self):
        pass
    def endFile(self, inputFile, outputFile, inputTree, wrappedOutputTree):
        pass


    def analyze(self, event):
        fjets=[f for f in Collection(event,"FatJetSel_Recl")] #FatJetSel_Recl_pt
        jindex=[];           ret={};      

        ## three working point of tagging;

        for V in self.vars:
            ret['ak8%sMgt45_%s'%(self.massVar,V)]       = [getattr(j,V) for j in fjets]

        pNetScore_wtag=[];
        for index,iJet in enumerate(fjets):
            selcut  = iJet.particleNet_mass > 45 if self.massVar == "pN" else iJet.msoftdrop  > 45
            #selcutB = iJet.particleNet_mass < 150 if self.massVar == "pN" else iJet.msoftdrop  < 150
            pnetscore=0.0;
            pnetscore=(iJet.particleNetMD_Xcc+iJet.particleNetMD_Xqq)/(iJet.particleNetMD_Xcc+iJet.particleNetMD_Xqq+iJet.particleNetMD_QCD)
            if not (selcut): continue
            jindex.append(index)
            pNetScore_wtag.append(pnetscore)
            #print pNetScore,pNetScore1,iJet.particleNetMD_Xbb

        self.out.fillBranch('event',event.event)
        self.out.fillBranch('nak8%sMgt45'%self.massVar,len(jindex))

        #print len(jindex_WPL),len(jindex_WPM),len(jindex_WPT)
        self.out.fillBranch('ak8%sMgt45_pNetWtagscore'%(self.massVar),pNetScore_wtag) #[j] for j in jindex ])
        for V in self.vars:
            self.out.fillBranch("ak8%sMgt45_%s"%(self.massVar,V), [ ret['ak8%sMgt45_%s'%(self.massVar,V)][j] for j in jindex])


        return True 
