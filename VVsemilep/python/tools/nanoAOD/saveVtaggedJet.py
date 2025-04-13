###FIXME : add leptight variables
from PhysicsTools.NanoAODTools.postprocessing.framework.eventloop import Module 
from PhysicsTools.NanoAODTools.postprocessing.framework.datamodel import Collection 
import ROOT as r 

from math import sqrt, cos
from PhysicsTools.NanoAODTools.postprocessing.tools import deltaR, deltaPhi
from PhysicsTools.Heppy.physicsobjects.Jet import _btagWPs

from copy import deepcopy

class saveVtaggedJet(Module):
    def __init__(self,isMC,massVar='sD',jecs=[]):
        self.isMC=isMC
        self.jecs=jecs
        print jecs
        self.shift=["Up","Down"] 
        self.vars=["eta","phi","mass","pt","btagDeepB","particleNetMD_Xqq","particleNetMD_Xbb","particleNetMD_Xcc","particleNetMD_QCD","particleNet_WvsQCD","particleNet_ZvsQCD","particleNet_mass","msoftdrop","deepTag_WvsQCD","tau1","tau2","hadronFlavour","muonIdx3SJ","electronIdx3SJ","nBHadrons","nCHadrons"] if self.isMC else ["eta","phi","mass","pt","btagDeepB","particleNetMD_Xqq","particleNetMD_Xbb","particleNetMD_Xcc","particleNetMD_QCD","particleNet_WvsQCD","particleNet_ZvsQCD","particleNet_mass","deepTag_WvsQCD","tau1","tau2","msoftdrop"]
        if self.isMC: 
            self.vars+=["pt_"+jec+sh for jec in self.jecs for sh in self.shift]
            self.vars+=["msoftdrop_"+jec+sh for jec in self.jecs for sh in self.shift]

        print type(self.vars)
        self.WPL = 0.64
        self.WPM = 0.85
        self.WPT = 0.91
        self.massVar=massVar
        pass
    def beginFile(self, inputFile, outputFile, inputTree, wrappedOutputTree):
        self.out = wrappedOutputTree
        self.out.branch('nak8Wtagged_WPL'  ,'I')
        self.out.branch('nak8Wtagged_WPM'  ,'I')
        self.out.branch('nak8Wtagged_WPT'  ,'I')
        #self.out.branch('nak8pNMgt45'  ,'I')
        self.out.branch('nak8%sMgt45'%self.massVar  ,'I')
        for var in self.vars:
            self.out.branch('ak8%sMgt45_%s'%(self.massVar,var), "F", lenVar="nak8%sMgt45"%self.massVar)
            for WP in ["L","M","T"]:
                self.out.branch('ak8Wtagged_WP%s_%s'%(WP,var), "F", lenVar="nak8Wtagged_WP"+WP)


    def beginJob(self):
        pass
    def endJob(self):
        pass
    def endFile(self, inputFile, outputFile, inputTree, wrappedOutputTree):
        pass


    def analyze(self, event):
        #all_fjets = [l for l in Collection(event,"FatJet")]
        #nfj = getattr(event,"nFatJetSel_Recl")
        #chosen = getattr(event,"iFatJetSel_Recl")
        #fjets = [all_fjets[chosen[i]] for i in xrange(nfj)]
        fjets=[f for f in Collection(event,"FatJetSel_Recl")] #FatJetSel_Recl_pt
        jindex=[];        jindex_WPL=[];        jindex_WPM=[];        jindex_WPT=[];
        ret={};        retL={};        retM={};        retT={}


        ## three working point of tagging;

        for V in self.vars:
            ret['ak8%sMgt45_%s'%(self.massVar,V)]       = [getattr(j,V) for j in fjets]
            #ret['ak8pNMgt45_%s'%V]       = [getattr(j,V) for j in fjets]
            retL['ak8Wtagged_WPL_%s'%V]  = [getattr(j,V) for j in fjets]
            retM['ak8Wtagged_WPM_%s'%V]  = [getattr(j,V) for j in fjets]
            retT['ak8Wtagged_WPT_%s'%V]  = [getattr(j,V) for j in fjets]


        for index,iJet in enumerate(fjets):
            selcut=iJet.particleNet_mass > 45 if self.massVar == "pN" else iJet.msoftdrop  > 45
            selcutB=iJet.particleNet_mass < 150 if self.massVar == "pN" else iJet.msoftdrop  < 150
            if not (selcut and selcutB): continue
            jindex.append(index)
            pNetScore_wtag=(iJet.particleNetMD_Xcc+iJet.particleNetMD_Xqq)/(iJet.particleNetMD_Xcc+iJet.particleNetMD_Xqq+iJet.particleNetMD_QCD) ##FIXME add Xbb for Z
            #print pNetScore,pNetScore1,iJet.particleNetMD_Xbb
            if (pNetScore_wtag > self.WPT):
                jindex_WPT.append(index)
            if (pNetScore_wtag > self.WPM):
                jindex_WPM.append(index)
            if (pNetScore_wtag > self.WPL):
                jindex_WPL.append(index)


        self.out.fillBranch('nak8%sMgt45'%self.massVar,len(jindex))
        self.out.fillBranch('nak8Wtagged_WPL',len(jindex_WPL))
        self.out.fillBranch('nak8Wtagged_WPM',len(jindex_WPM))
        self.out.fillBranch('nak8Wtagged_WPT',len(jindex_WPT))

        #print len(jindex_WPL),len(jindex_WPM),len(jindex_WPT)
        for V in self.vars:
            self.out.fillBranch("ak8%sMgt45_%s"%(self.massVar,V), [ ret['ak8%sMgt45_%s'%(self.massVar,V)][j] for j in jindex])
            self.out.fillBranch("ak8Wtagged_WPL_%s"%V, [ retL['ak8Wtagged_WPL_%s'%V][j] for j in jindex_WPL])
            self.out.fillBranch("ak8Wtagged_WPM_%s"%V, [ retM['ak8Wtagged_WPM_%s'%V][j] for j in jindex_WPM])
            self.out.fillBranch("ak8Wtagged_WPT_%s"%V, [ retT['ak8Wtagged_WPT_%s'%V][j] for j in jindex_WPT])

        return True 
