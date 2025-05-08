import os
import itertools
import numpy as np
import ROOT
ROOT.PyConfig.IgnoreCommandLineOptions = True

from PhysicsTools.NanoAODTools.postprocessing.framework.datamodel import Collection, Object
from PhysicsTools.NanoAODTools.postprocessing.framework.eventloop import Module
from PhysicsTools.NanoAODTools.postprocessing.tools import closest
from PhysicsTools.NanoAODTools.postprocessing.tools import deltaR, deltaPhi
#import logging
#logger = logging.getLogger('nano')
#configLogger('nano', loglevel=logging.INFO)

#lumi_dict = {2015: 19.52, 2016: 16.81, 2017: 41.48, 2018: 59.83}



class HeavyFlavBaseProducer(Module):

    def __init__(self):
        self.prefix = "fatjet_"
        pass
    def beginJob(self):
        pass
    def endJob(self):
        pass

    def beginFile(self, inputFile, outputFile, inputTree, wrappedOutputTree):
        self.out = wrappedOutputTree
        prefix=self.prefix
        self.out.branch(prefix + "dr_H", "F")
        self.out.branch(prefix + "dr_H_daus", "F")
        self.out.branch(prefix + "H_pt", "F")
        self.out.branch(prefix + "H_decay", "I")

        self.out.branch(prefix + "dr_Z", "F")
        self.out.branch(prefix + "dr_Z_daus", "F")
        self.out.branch(prefix + "Z_pt", "F")
        self.out.branch(prefix + "Z_decay", "I")
        
        # info of the closest hadGenW
        self.out.branch(prefix + "dr_W", "F")
        self.out.branch(prefix + "dr_W_daus", "F")
        self.out.branch(prefix + "W_pt", "F")
        self.out.branch(prefix + "W_decay", "I")
        self.out.branch(prefix + "dr_T", "F")
        self.out.branch(prefix + "dr_T_b", "F")
        self.out.branch(prefix + "dr_T_Wq_max", "F")
        self.out.branch(prefix + "dr_T_Wq_min", "F")
        self.out.branch(prefix + "T_Wq_max_pdgId", "I")
        self.out.branch(prefix + "T_Wq_min_pdgId", "I")
        self.out.branch(prefix + "T_pt", "F")
        

    def endFile(self, inputFile, outputFile, inputTree, wrappedOutputTree):
        pass
  
    def if3(self,cond, iftrue, iffalse):
        return iftrue if cond else iffalse


    def analyze(self, event):
        """process event, return True (go to next module) or False (fail, go to next event)"""
 
        genparts=Collection(event,"GenPart")
        fatjets= [j for j in Collection(event,"ak8sDMgt45")]
        
        for idx, gp in enumerate(genparts):
            if 'dauIdx' not in gp.__dict__:
                gp.dauIdx = []
            if gp.genPartIdxMother >= 0:
                mom = genparts[gp.genPartIdxMother]
                if 'dauIdx' not in mom.__dict__:
                    mom.dauIdx = [idx]
                else:
                    mom.dauIdx.append(idx)
        event.genparts = genparts

        lepGenTops = [];        hadGenTops = [];        hadGenWs = [];        hadGenZs = [];        hadGenHs = []

        def isHadronic(gp):
            if len(gp.dauIdx) == 0:
                raise ValueError('Particle has no daughters!')
            for idx in gp.dauIdx:
                if abs(genparts[idx].pdgId) < 6:
                    return True
            return False

        def getFinal(gp):
            for idx in gp.dauIdx:
                dau = genparts[idx]
                if dau.pdgId == gp.pdgId:
                    return getFinal(dau)
            return gp


        for gp in genparts:
            if gp.statusFlags & (1 << 13) == 0:
                continue
            if abs(gp.pdgId) == 6:
                for idx in gp.dauIdx:
                    dau = genparts[idx]
                    if abs(dau.pdgId) == 24:
                        genW = getFinal(dau)
                        gp.genW = genW
                        if isHadronic(genW):
                            hadGenTops.append(gp)
                        else:
                            lepGenTops.append(gp)
                    elif abs(dau.pdgId) in (1, 3, 5):
                        gp.genB = dau
            elif abs(gp.pdgId) == 24:
                if isHadronic(gp):
                    hadGenWs.append(gp)
            elif abs(gp.pdgId) == 23:
                if isHadronic(gp):
                    hadGenZs.append(gp)
            elif abs(gp.pdgId) == 25:
                if isHadronic(gp):
                    hadGenHs.append(gp)

        for parton in itertools.chain(lepGenTops, hadGenTops):
            parton.daus = (parton.genB, genparts[parton.genW.dauIdx[0]], genparts[parton.genW.dauIdx[1]])
            parton.genW.daus = parton.daus[1:]
        for parton in itertools.chain(hadGenWs, hadGenZs, hadGenHs):
            parton.daus = (genparts[parton.dauIdx[0]], genparts[parton.dauIdx[1]])
        if len(fatjets) > 0 :
            fj = fatjets[0]
            for fj in fatjets:
                fj.genH, fj.dr_H = closest(fj, hadGenHs)
                fj.genZ, fj.dr_Z = closest(fj, hadGenZs)
                fj.genW, fj.dr_W = closest(fj, hadGenWs)
                fj.genT, fj.dr_T = closest(fj, hadGenTops)
                fj.genLepT, fj.dr_LepT = closest(fj, lepGenTops)

            

    
                # info of the closest hadGenH
            self.out.fillBranch(self.prefix + "dr_H", fj.dr_H)
            self.out.fillBranch(self.prefix + "dr_H_daus",
                                max([deltaR(fj, dau) for dau in fj.genH.daus]) if fj.genH else 99)
            self.out.fillBranch(self.prefix + "H_pt", fj.genH.pt if fj.genH else -1)
            self.out.fillBranch(self.prefix + "H_decay", abs(fj.genH.daus[0].pdgId) if fj.genH else 0)
            
            # info of the closest hadGenZ
            self.out.fillBranch(self.prefix + "dr_Z", fj.dr_Z)
            self.out.fillBranch(self.prefix + "dr_Z_daus",
                                max([deltaR(fj, dau) for dau in fj.genZ.daus]) if fj.genZ else 99)
            self.out.fillBranch(self.prefix + "Z_pt", fj.genZ.pt if fj.genZ else -1)
            self.out.fillBranch(self.prefix + "Z_decay", abs(fj.genZ.daus[0].pdgId) if fj.genZ else 0)
            
            # info of the closest hadGenW
            self.out.fillBranch(self.prefix + "dr_W", fj.dr_W)
            self.out.fillBranch(self.prefix + "dr_W_daus",
                                max([deltaR(fj, dau) for dau in fj.genW.daus]) if fj.genW else 99)
            self.out.fillBranch(self.prefix + "W_pt", fj.genW.pt if fj.genW else -1)
            self.out.fillBranch(self.prefix + "W_decay", max([abs(d.pdgId) for d in fj.genW.daus]) if fj.genW else 0)
        
            # info of the closest hadGenTop
            drwq1, drwq2 = [deltaR(fj, dau) for dau in fj.genT.genW.daus] if fj.genT else [99, 99]
            wq1_pdgId, wq2_pdgId = [dau.pdgId for dau in fj.genT.genW.daus] if fj.genT else [0, 0]
            if drwq1 < drwq2:
                drwq1, drwq2 = drwq2, drwq1
                wq1_pdgId, wq2_pdgId = wq2_pdgId, wq1_pdgId
            self.out.fillBranch(self.prefix + "dr_T", fj.dr_T)
            self.out.fillBranch(self.prefix + "dr_T_b", deltaR(fj, fj.genT.genB) if fj.genT else 99)
            self.out.fillBranch(self.prefix + "dr_T_Wq_max", drwq1)
            self.out.fillBranch(self.prefix + "dr_T_Wq_min", drwq2)
            self.out.fillBranch(self.prefix + "T_Wq_max_pdgId", wq1_pdgId)
            self.out.fillBranch(self.prefix + "T_Wq_min_pdgId", wq2_pdgId)
            self.out.fillBranch(self.prefix + "T_pt", fj.genT.pt if fj.genT else -1)

        return True    
