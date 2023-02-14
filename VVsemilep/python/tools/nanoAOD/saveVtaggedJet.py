from PhysicsTools.NanoAODTools.postprocessing.framework.eventloop import Module 
from PhysicsTools.NanoAODTools.postprocessing.framework.datamodel import Collection 
import ROOT as r 

from math import sqrt, cos
from PhysicsTools.NanoAODTools.postprocessing.tools import deltaR, deltaPhi
from PhysicsTools.Heppy.physicsobjects.Jet import _btagWPs

from copy import deepcopy

class saveVtaggedJet(Module):
    def __init__(self,isMC):
        self.isMC=isMC
        self.vars=("eta","phi","mass","pt","btagDeepB","particleNetMD_Xqq","particleNetMD_Xbb","particleNetMD_Xcc","particleNetMD_QCD","particleNet_WvsQCD","particleNet_ZvsQCD","particleNet_mass","deepTag_WvsQCD","tau1","tau2","hadronFlavour","muonIdx3SJ","electronIdx3SJ","nBHadrons","nCHadrons") if self.isMC else ("eta","phi","mass","pt","btagDeepB","particleNetMD_Xqq","particleNetMD_Xbb","particleNetMD_Xcc","particleNetMD_QCD","particleNet_WvsQCD","particleNet_ZvsQCD","particleNet_mass","deepTag_WvsQCD","tau1","tau2") 
        print type(self.vars)
        self.WPL = 0.64
        self.WPM = 0.85
        self.WPT = 0.91
        pass
    def beginFile(self, inputFile, outputFile, inputTree, wrappedOutputTree):
        self.out = wrappedOutputTree
        self.out.branch('nak8Vtagged_WPL'  ,'I')
        self.out.branch('nak8Vtagged_WPM'  ,'I')
        self.out.branch('nak8Vtagged_WPT'  ,'I')
        self.out.branch('nak8pNMgt40'  ,'I')
        for var in self.vars:
            self.out.branch('ak8pNMgt40_%s'%var, "F", lenVar="nak8pNMgt40")
            for WP in ["L","M","T"]:
                self.out.branch('ak8Vtagged_%s_WP%s'%(var,WP), "F", lenVar="nak8Vtagged_WP"+WP)

    def beginJob(self):
        pass
    def endJob(self):
        pass
    def endFile(self, inputFile, outputFile, inputTree, wrappedOutputTree):
        pass


    def analyze(self, event):
        all_fjets = [l for l in Collection(event,"FatJet")]
        nfj = getattr(event,"nFatJetSel_Recl")
        chosen = getattr(event,"iFatJetSel_Recl")
        fjets = [all_fjets[chosen[i]] for i in xrange(nfj)]
        jindex=[]
        jindex_WPL=[]
        jindex_WPM=[]
        jindex_WPT=[]
        ret={}
        retL={}
        retM={}
        retT={}


        ## three working point of tagging; three set of jets

        for V in self.vars:
            ret['ak8pNMgt40_%s'%V]      = [getattr(j,V) for j in fjets]
            retL['ak8Vtagged_%s_WPL'%V] = [getattr(j,V) for j in fjets]
            retM['ak8Vtagged_%s_WPM'%V] = [getattr(j,V) for j in fjets]
            retT['ak8Vtagged_%s_WPT'%V] = [getattr(j,V) for j in fjets]

        for index,iJet in enumerate(fjets):
            if iJet.particleNet_mass < 40: continue
            jindex.append(index)
            #            Xbb= 0.0 if getattr(ev,''))
            pNetScore=(iJet.particleNetMD_Xcc+iJet.particleNetMD_Xqq+iJet.particleNetMD_Xbb)/(iJet.particleNetMD_Xcc+iJet.particleNetMD_Xqq+iJet.particleNetMD_QCD+iJet.particleNetMD_Xbb) ##FIXME add Xbb for Z
            #pNetScore1=(iJet.particleNetMD_Xcc+iJet.particleNetMD_Xqq)/(iJet.particleNetMD_Xcc+iJet.particleNetMD_Xqq+iJet.particleNetMD_QCD) 
            #print pNetScore,pNetScore1,iJet.particleNetMD_Xbb
            if (pNetScore > self.WPL):
                #print index
                jindex_WPT.append(index)
            elif (pNetScore > self.WPM):
                jindex_WPM.append(index)
            elif (pNetScore > self.WPL):
                jindex_WPL.append(index)
            else: continue
            
        self.out.fillBranch('nak8pNMgt40',len(jindex))
        self.out.fillBranch('nak8Vtagged_WPL',len(jindex_WPL))
        self.out.fillBranch('nak8Vtagged_WPM',len(jindex_WPM))
        self.out.fillBranch('nak8Vtagged_WPT',len(jindex_WPT))
        #print len(jindex_WPL),len(jindex_WPM),len(jindex_WPT)
        for V in self.vars:
            self.out.fillBranch("ak8pNMgt40_%s"%V, [ ret['ak8pNMgt40_%s'%V][j] for j in jindex])
            self.out.fillBranch("ak8Vtagged_%s_WPL"%V, [ retL['ak8Vtagged_%s_WPL'%V][j] for j in jindex_WPL])
            self.out.fillBranch("ak8Vtagged_%s_WPM"%V, [ retM['ak8Vtagged_%s_WPM'%V][j] for j in jindex_WPM])
            self.out.fillBranch("ak8Vtagged_%s_WPT"%V, [ retT['ak8Vtagged_%s_WPT'%V][j] for j in jindex_WPT])
        return True 
