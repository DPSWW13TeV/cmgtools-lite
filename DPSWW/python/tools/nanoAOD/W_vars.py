from PhysicsTools.NanoAODTools.postprocessing.framework.eventloop import Module
from PhysicsTools.NanoAODTools.postprocessing.framework.datamodel import Collection 
import ROOT
import os, math
import array, numpy
from ROOT import TLorentzVector

class W_vars(Module):
    def __init__(self,year,isMC):
        self.year=year
        self.isMC = isMC
        self.svars   = ['jesBBEC1_year','jesFlavorQCD','jesEC2','jesAbsolute_year','jesHF','jesHF_year','jesRelativeSample_year','jesRelativeBal','jesBBEC1','jesEC2_year','jesAbsolute','unclustEn','jerbarrel','jerendcap1','jerendcap2highpt','jerendcap2lowpt','jerforwardhighpt','jerforwardlowpt','HEM']#'jesJECTotal',

        print 'saving bdt input variables for ',year
        pass
    def beginFile(self, inputFile, outputFile, inputTree, wrappedOutputTree):
        self.out = wrappedOutputTree
        self.out.branch('met',"F")
        self.out.branch('met_phi',"F")
        self.out.branch('Lep1_conept'   ,'F')
        self.out.branch('Lep1_pt'   ,'F')
        self.out.branch('Lep1_eta'  ,'F')
        self.out.branch('Lep1_phi'  ,'F')
        self.out.branch('Lep2_conept'   ,'F')
        self.out.branch('Lep2_pt'   ,'F')
        self.out.branch('Lep2_eta'  ,'F')
        self.out.branch('Lep2_phi'  ,'F')
        self.out.branch('Lep1_pdgId'   ,'I')
        self.out.branch('Lep1_charge'   ,'I')
        self.out.branch('Lep1_convVeto'   ,'I')
        self.out.branch('Lep1_tightCharge'   ,'I')
        self.out.branch('Lep1_lostHits'   ,'I')
        self.out.branch('Lep1_isLepTight'   ,'I') 
        self.out.branch('Lep2_pdgId'   ,'I')
        self.out.branch('Lep2_charge'   ,'I')
        self.out.branch('Lep2_convVeto'   ,'I')
        self.out.branch('Lep2_tightCharge'   ,'I')
        self.out.branch('Lep2_lostHits'   ,'I')
        self.out.branch('Lep2_isLepTight'   ,'I') 
        self.out.branch('Lep1_dz'  ,'F')
        self.out.branch('Lep2_dz'  ,'F')
        self.out.branch('Lep1_dxy'  ,'F')
        self.out.branch('Lep2_dxy'  ,'F')
        self.out.branch('deltadz'  ,'F')
        self.out.branch('deltadxy'  ,'F')
        self.out.branch('dRll'  ,'F')

        for src in self.svars:
            for shift in ['Up','Down']:
                self.out.branch('met_%s%s'%(src,shift),"F")


    def if3(self,cond, iftrue, iffalse):
        return iftrue if cond else iffalse

    def analyze(self, event):

        # leptons
        all_leps  = [l for l in Collection(event,"LepGood")]
        nFO       = getattr(event,"nLepFO_Recl")
        chosen    = getattr(event,"iLepFO_Recl")
        leps      = [all_leps[chosen[i]] for i in xrange(nFO)]
        if len(leps) > 0:
            MET_pt    = getattr(event,"METFixEE2017_pt" if self.year == 2017 else "MET_pt")        
            MET_phi   = getattr(event,"METFixEE2017_phi" if self.year == 2017 else "MET_phi")
        
            for src in self.svars:
                for shift in ['Up','Down']:
                    if self.isMC:
                        temp_pT= getattr(event,"MET{fix}_pt_{here}".format(fix='FixEE2017'if self.year == 2017 else '',here=src+shift))
                        temp_phi = getattr(event,"MET{fix}_phi_{here}".format(fix='FixEE2017'if self.year == 2017 else '',here=src+shift))
                        #print src+shift,temp_phi," ",MET_phi
                    else:
                        temp_pT    = getattr(event,"METFixEE2017_pt" if self.year == 2017 else "MET_pt")
                        temp_phi   = getattr(event,"METFixEE2017_phi" if self.year == 2017 else "MET_phi")
                    
                    self.out.fillBranch('met_%s%s'%(src,shift), temp_pT )
        
            self.out.fillBranch('met',MET_pt)  
            self.out.fillBranch('met_phi',MET_phi)  
            self.out.fillBranch('Lep1_conept'   ,leps[0].conePt )
            self.out.fillBranch('Lep1_pt'       ,leps[0].pt     )
            self.out.fillBranch('Lep1_eta'      ,leps[0].eta    )
            self.out.fillBranch('Lep1_phi'      ,leps[0].phi    )
            self.out.fillBranch('Lep2_conept'   ,leps[1].conePt if len(leps) > 1 else -999 )
            self.out.fillBranch('Lep2_pt'       ,leps[1].pt  if len(leps) > 1 else -999   )
            self.out.fillBranch('Lep2_eta'      ,leps[1].eta  if len(leps) > 1 else -999  )
            self.out.fillBranch('Lep2_phi'      ,leps[1].phi   if len(leps) > 1 else -999 )            
            self.out.fillBranch('Lep1_pdgId'      ,leps[0].pdgId           )
            self.out.fillBranch('Lep1_charge'     ,leps[0].charge          )
            self.out.fillBranch('Lep1_convVeto'   ,leps[0].convVeto        )
            self.out.fillBranch('Lep1_tightCharge',leps[0].tightCharge     )
            self.out.fillBranch('Lep1_lostHits'   ,leps[0].lostHits        )
            self.out.fillBranch('Lep1_isLepTight' ,leps[0].isLepTight_Recl )
            self.out.fillBranch('Lep2_pdgId'       ,leps[1].pdgId   if len(leps) > 1 else 0)
            self.out.fillBranch('Lep2_charge'      ,leps[1].charge  if len(leps) > 1 else 0  )
            self.out.fillBranch('Lep2_convVeto'    ,leps[1].convVeto  if len(leps) > 1 else 0      )
            self.out.fillBranch('Lep2_tightCharge' ,leps[1].tightCharge  if len(leps) > 1 else 0   )
            self.out.fillBranch('Lep2_lostHits'    ,leps[1].lostHits     if len(leps) > 1 else 999   )
            self.out.fillBranch('Lep2_isLepTight'  ,leps[1].isLepTight_Recl if len(leps) > 1 else -999)            
            self.out.fillBranch('Lep1_dz'  ,leps[0].dz)
            self.out.fillBranch('Lep2_dz'  ,leps[1].dz if len(leps) > 1 else -999)
            self.out.fillBranch('Lep1_dxy'  ,leps[0].dxy)
            self.out.fillBranch('Lep2_dxy'  ,leps[1].dxy if len(leps) > 1 else -999)










 
        return True







