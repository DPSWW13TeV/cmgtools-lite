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
        self.shift=["Up","Down"] 
        self.vars=["eta","phi","mass","pt","btagDeepB","particleNetMD_Xqq","particleNetMD_Xbb","particleNetMD_Xcc","particleNetMD_QCD","particleNet_WvsQCD","particleNet_ZvsQCD","particleNet_mass","msoftdrop","deepTag_WvsQCD","tau1","tau2","hadronFlavour","muonIdx3SJ","electronIdx3SJ","nBHadrons","nCHadrons"] if self.isMC else ["eta","phi","mass","pt","btagDeepB","particleNetMD_Xqq","particleNetMD_Xbb","particleNetMD_Xcc","particleNetMD_QCD","particleNet_WvsQCD","particleNet_ZvsQCD","particleNet_mass","deepTag_WvsQCD","tau1","tau2","msoftdrop"]
        if self.isMC: self.vars+=["pt_"+jec+sh for jec in self.jecs for sh in self.shift]
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
        #self.out.branch('nak8pNMgt40'  ,'I')
        self.out.branch('nak8%sMgt40'%self.massVar  ,'I')
        self.out.branch('nak8Ztagged_WPL'  ,'I')
        self.out.branch('nak8Ztagged_WPM'  ,'I')
        self.out.branch('nak8Ztagged_WPT'  ,'I')
        for var in self.vars:
            self.out.branch('ak8%sMgt40_%s'%(self.massVar,var), "F", lenVar="nak8%sMgt40"%self.massVar)

            for WP in ["L","M","T"]:
                self.out.branch('ak8Wtagged_WP%s_%s'%(WP,var), "F", lenVar="nak8Wtagged_WP"+WP)
                self.out.branch('ak8Ztagged_WP%s_%s'%(WP,var), "F", lenVar="nak8Ztagged_WP"+WP)

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
        jindex=[]
        jindex_WPL=[];jindex_zWPL=[];
        jindex_WPM=[];jindex_zWPM=[];
        jindex_WPT=[];jindex_zWPT=[];
        ret={}
        retL={}
        retM={}
        retT={}
        retzL={}
        retzM={}
        retzT={}


        ## three working point of tagging; three set of jets

        for V in self.vars:
            ret['ak8%sMgt40_%s'%(self.massVar,V)]       = [getattr(j,V) for j in fjets]
            #ret['ak8pNMgt40_%s'%V]       = [getattr(j,V) for j in fjets]
            retL['ak8Wtagged_WPL_%s'%V]  = [getattr(j,V) for j in fjets]
            retM['ak8Wtagged_WPM_%s'%V]  = [getattr(j,V) for j in fjets]
            retT['ak8Wtagged_WPT_%s'%V]  = [getattr(j,V) for j in fjets]
            retzL['ak8Ztagged_WPL_%s'%V] = [getattr(j,V) for j in fjets]
            retzM['ak8Ztagged_WPM_%s'%V] = [getattr(j,V) for j in fjets]
            retzT['ak8Ztagged_WPT_%s'%V] = [getattr(j,V) for j in fjets]


        for index,iJet in enumerate(fjets):
            selcut=iJet.particleNet_mass < 40 if self.massVar == "pN" else iJet.msoftdrop  < 40
            ##amif iJet.particleNet_mass < 40: continue
            #if iJet.msoftdrop  < 40: continue
            if not selcut: continue
            jindex.append(index)
            pNetScore_wtag=(iJet.particleNetMD_Xcc+iJet.particleNetMD_Xqq)/(iJet.particleNetMD_Xcc+iJet.particleNetMD_Xqq+iJet.particleNetMD_QCD) ##FIXME add Xbb for Z
            pNetScore_ztag=(iJet.particleNetMD_Xcc+iJet.particleNetMD_Xqq+iJet.particleNetMD_Xbb)/(iJet.particleNetMD_Xcc+iJet.particleNetMD_Xqq+iJet.particleNetMD_QCD+iJet.particleNetMD_Xbb) ##FIXME add Xbb for Z
            #pNetScore1=(iJet.particleNetMD_Xcc+iJet.particleNetMD_Xqq)/(iJet.particleNetMD_Xcc+iJet.particleNetMD_Xqq+iJet.particleNetMD_QCD) 
            #print pNetScore,pNetScore1,iJet.particleNetMD_Xbb
            if (pNetScore_wtag > self.WPL):
                jindex_WPT.append(index)
            if (pNetScore_wtag > self.WPM):
                jindex_WPM.append(index)
            if (pNetScore_wtag > self.WPL):
                jindex_WPL.append(index)
            if (pNetScore_ztag > self.WPL):
                jindex_zWPT.append(index)
            if (pNetScore_ztag > self.WPM):
                jindex_zWPM.append(index)
            if (pNetScore_ztag > self.WPL):
                jindex_zWPL.append(index)


        self.out.fillBranch('nak8%sMgt40'%self.massVar,len(jindex))
        self.out.fillBranch('nak8Wtagged_WPL',len(jindex_WPL))
        self.out.fillBranch('nak8Wtagged_WPM',len(jindex_WPM))
        self.out.fillBranch('nak8Wtagged_WPT',len(jindex_WPT))
        self.out.fillBranch('nak8Ztagged_WPL',len(jindex_zWPL))
        self.out.fillBranch('nak8Ztagged_WPM',len(jindex_zWPM))
        self.out.fillBranch('nak8Ztagged_WPT',len(jindex_zWPT))

        #print len(jindex_WPL),len(jindex_WPM),len(jindex_WPT)
        for V in self.vars:
            self.out.fillBranch("ak8%sMgt40_%s"%(self.massVar,V), [ ret['ak8%sMgt40_%s'%(self.massVar,V)][j] for j in jindex])
            self.out.fillBranch("ak8Wtagged_WPL_%s"%V, [ retL['ak8Wtagged_WPL_%s'%V][j] for j in jindex_WPL])
            self.out.fillBranch("ak8Wtagged_WPM_%s"%V, [ retM['ak8Wtagged_WPM_%s'%V][j] for j in jindex_WPM])
            self.out.fillBranch("ak8Wtagged_WPT_%s"%V, [ retT['ak8Wtagged_WPT_%s'%V][j] for j in jindex_WPT])
            self.out.fillBranch("ak8Ztagged_WPL_%s"%V, [ retzL['ak8Ztagged_WPL_%s'%V][j] for j in jindex_zWPL])
            self.out.fillBranch("ak8Ztagged_WPM_%s"%V, [ retzM['ak8Ztagged_WPM_%s'%V][j] for j in jindex_zWPM])
            self.out.fillBranch("ak8Ztagged_WPT_%s"%V, [ retzT['ak8Ztagged_WPT_%s'%V][j] for j in jindex_zWPT])

        return True 
