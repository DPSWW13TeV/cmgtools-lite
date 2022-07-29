#saves variables only if nlep >1
from PhysicsTools.NanoAODTools.postprocessing.framework.eventloop import Module
from PhysicsTools.NanoAODTools.postprocessing.framework.datamodel import Collection 
import ROOT
import os, math
import array, numpy
from ROOT import TLorentzVector

class DPSWW_vars(Module):
    def __init__(self,FRFile,histMu,histEl,year,isMC):
        self.year=year
        self.FRFile = FRFile
        self.histEl = histEl
        self.histMu = histMu
        self.isMC = isMC
        self.svars   = ['jesBBEC1_year','jesFlavorQCD','jesEC2','jesAbsolute_year','jesHF','jesHF_year','jesRelativeSample_year','jesRelativeBal','jesBBEC1','jesEC2_year','jesAbsolute','unclustEn','jerbarrel','jerendcap1','jerendcap2highpt','jerendcap2lowpt','jerforwardhighpt','jerforwardlowpt','HEM']#'jesJECTotal',

        print 'saving bdt input variables for',year,FRFile
        pass
    def beginFile(self, inputFile, outputFile, inputTree, wrappedOutputTree):
        self.out = wrappedOutputTree
        self.out.branch('mt2',"F")
        self.out.branch('mtll',"F")
        self.out.branch('met',"F")
        self.out.branch('mtl1met',"F")
        self.out.branch('dphill',"F")
        self.out.branch('cptll',"F")
        self.out.branch('mll',"F")
        self.out.branch('dphil2met',"F")
        self.out.branch('dphilll2', "F")
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
        self.out.branch("fakeRateWt","F")
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
                self.out.branch('mtl1met_%s%s'%(src,shift),"F")
                self.out.branch('mt2_%s%s'%(src,shift),"F")  
                self.out.branch('dphil2met_%s%s'%(src,shift),"F")




        
    def fakeRateWeight_2lss(self,lep1,lep2):
        nfail = (lep1.isLepTight_Recl + lep2.isLepTight_Recl)
        if (nfail == 1):
            wt = self.fakeRatefromHist(lep1) if not lep1.isLepTight_Recl else self.fakeRatefromHist(lep2)
            evtwt=wt/(1-wt)
        elif(nfail == 2):
            wt1 = self.fakeRatefromHist(lep1)
            wt2 = self.fakeRatefromHist(lep2)
            evtwt=-wt1*wt2/((1-wt1)*(1-wt2));
        else: evtwt=0
        return evtwt

    def fakeRatefromHist(self,lep):
        fName = ROOT.TFile.Open(self.FRFile)
        if not fName: raise RuntimeError("No such file %s"%self.FRFile)
        hist =  fName.Get(self.histEl if abs(lep.pdgId) == 11 else self.histMu)
        ptbin  = max(1, min(hist.GetNbinsX(), hist.GetXaxis().FindBin(lep.conePt)))
        etabin = max(1, min(hist.GetNbinsX(), hist.GetXaxis().FindBin(abs(lep.eta))))
        fr     = hist.GetBinContent(ptbin,etabin)
        fName.Close()
        return fr; 

    def if3(self,cond, iftrue, iffalse):
        return iftrue if cond else iffalse

    def phill(self,l1,l2,opt):
        
        lepton1=ROOT.TLorentzVector(0.0,0.0,0.0,0.0);
        lepton2=ROOT.TLorentzVector(0.0,0.0,0.0,0.0);
        
        lepton1.SetPtEtaPhiM(l1.conePt,l1.eta,l1.phi,l1.mass); 
        lepton2.SetPtEtaPhiM(l2.conePt,l2.eta,l2.phi,l2.mass);
        if opt == 'phi':
            toreturn = (lepton1+lepton2).Phi() 
        elif opt == 'dR':
            toreturn = lepton1.DeltaR(lepton2)
        else:
            toreturn =  self.if3((opt == 'mll'), (lepton1+lepton2).M(), (lepton1+lepton2).Pt())
        return toreturn


    def dphi(self,phi1,phi2):

        result = phi1 - phi2

        while (result > math.pi):
            result -= 2*math.pi;
        while (result <= -math.pi):
            result += 2*math.pi;
        return result


    def mt(self,pt1,phi1,pt2,phi2):
        return math.sqrt(2*pt1*pt2*(1-math.cos(phi1-phi2)));


    def calcmt2(self,l1,l2,metpt,metphi):
    
        from ROOT.heppy import Davismt2
        davismt2 = Davismt2()    

        met=ROOT.TLorentzVector(0.0,0.0,0.0,0.0);  
        lepton1=ROOT.TLorentzVector(0.0,0.0,0.0,0.0);
        lepton2=ROOT.TLorentzVector(0.0,0.0,0.0,0.0);

        met.SetPtEtaPhiM(metpt,0.,metphi,0.);
        lepton1.SetPtEtaPhiM(l1.conePt,l1.eta,l1.phi,l1.mass);
        lepton2.SetPtEtaPhiM(l2.conePt,l2.eta,l2.phi,l2.mass);

        metVec = array.array('d',[met.M(),met.Px(), met.Py()])
        lep1Vec = array.array('d',[lepton1.M(),lepton1.Px(), lepton1.Py()])
        lep2Vec = array.array('d',[lepton2.M(),lepton1.Px(),lepton2.Py()])

        davismt2.set_momenta(lep1Vec,lep2Vec,metVec);
        davismt2.set_mn(0);

        return davismt2.get_mt2()


    def analyze(self, event):

        # leptons
        all_leps  = [l for l in Collection(event,"LepGood")]
        nFO       = getattr(event,"nLepFO_Recl")
        chosen    = getattr(event,"iLepFO_Recl")
        leps      = [all_leps[chosen[i]] for i in xrange(nFO)]
        if len(leps) > 1:
            MET_pt    = getattr(event,"METFixEE2017_pt" if self.year == 2017 else "MET_pt")        
            MET_phi   = getattr(event,"METFixEE2017_phi" if self.year == 2017 else "MET_phi")
            mt2       = self.calcmt2(leps[0],leps[1],MET_pt,MET_phi)
            mtll      = self.mt(leps[0].conePt,leps[0].phi,leps[1].conePt,leps[1].phi)
            mtl1met   = self.mt(leps[0].conePt,leps[0].phi,MET_pt,MET_phi) 
            dphill    = abs(self.dphi(leps[0].phi,leps[1].phi)) 
            dphil2met = abs(self.dphi(leps[1].phi,MET_phi)) 
            dphilll2  = abs(self.dphi(self.phill(leps[0],leps[1],'phi'),leps[1].phi))
            frweight  = self.fakeRateWeight_2lss(leps[0],leps[1]) 
            cptll     = self.phill(leps[0],leps[1],'pt')  
            mll       = self.phill(leps[0],leps[1],'mll') 
            dRll      = self.phill(leps[0],leps[1],'dR')
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
                    self.out.fillBranch('mt2_%s%s'%(src,shift),self.calcmt2(leps[0],leps[1],temp_pT,temp_phi))
                    self.out.fillBranch('mtl1met_%s%s'%(src,shift),self.mt(leps[0].conePt,leps[0].phi,temp_pT,temp_phi))
                    self.out.fillBranch('dphil2met_%s%s'%(src,shift),abs(self.dphi(leps[1].phi,temp_phi)))

            self.out.fillBranch('fakeRateWt',frweight)
            self.out.fillBranch('mt2', mt2)     
            self.out.fillBranch('mtll',mtll)     
            self.out.fillBranch('met',MET_pt)  
            self.out.fillBranch('mtl1met',mtl1met)  
            self.out.fillBranch('dphill',dphill)   
            self.out.fillBranch('dphil2met',dphil2met) 
        
            self.out.fillBranch('dphilll2', dphilll2)
            self.out.fillBranch('cptll', cptll)
            self.out.fillBranch('mll', mll)
            self.out.fillBranch('Lep1_conept'   ,leps[0].conePt )
            self.out.fillBranch('Lep1_pt'       ,leps[0].pt     )
            self.out.fillBranch('Lep1_eta'      ,leps[0].eta    )
            self.out.fillBranch('Lep1_phi'      ,leps[0].phi    )
            self.out.fillBranch('Lep2_conept'   ,leps[1].conePt )
            self.out.fillBranch('Lep2_pt'       ,leps[1].pt     )
            self.out.fillBranch('Lep2_eta'      ,leps[1].eta    )
            self.out.fillBranch('Lep2_phi'      ,leps[1].phi    )
            
            self.out.fillBranch('Lep1_pdgId'      ,leps[0].pdgId           )
            self.out.fillBranch('Lep1_charge'     ,leps[0].charge          )
            self.out.fillBranch('Lep1_convVeto'   ,leps[0].convVeto        )
            self.out.fillBranch('Lep1_tightCharge',leps[0].tightCharge     )
            self.out.fillBranch('Lep1_lostHits'   ,leps[0].lostHits        )
            self.out.fillBranch('Lep1_isLepTight' ,leps[0].isLepTight_Recl )
            
            self.out.fillBranch('Lep2_pdgId'       ,leps[1].pdgId           )
            self.out.fillBranch('Lep2_charge'      ,leps[1].charge          )
            self.out.fillBranch('Lep2_convVeto'    ,leps[1].convVeto        )
            self.out.fillBranch('Lep2_tightCharge' ,leps[1].tightCharge     )
            self.out.fillBranch('Lep2_lostHits'    ,leps[1].lostHits        )
            self.out.fillBranch('Lep2_isLepTight'  ,leps[1].isLepTight_Recl )
            
            self.out.fillBranch('Lep1_dz'  ,leps[0].dz)
            self.out.fillBranch('Lep2_dz'  ,leps[1].dz)
            self.out.fillBranch('Lep1_dxy'  ,leps[0].dxy)
            self.out.fillBranch('Lep2_dxy'  ,leps[1].dxy)
            self.out.fillBranch('deltadz'  ,abs(leps[0].dz-leps[1].dz))
            self.out.fillBranch('deltadxy'  ,abs(leps[0].dxy-leps[1].dxy))
            self.out.fillBranch('dRll'  ,dRll)









 
        return True







