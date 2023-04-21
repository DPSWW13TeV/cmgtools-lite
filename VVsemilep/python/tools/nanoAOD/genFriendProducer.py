import ROOT
import os, array
import numpy as np
from PhysicsTools.NanoAODTools.postprocessing.framework.eventloop import Module 
from PhysicsTools.NanoAODTools.postprocessing.framework.datamodel import Collection 
from PhysicsTools.NanoAODTools.postprocessing.tools import deltaR, deltaPhi
from math import *
from ROOT import TLorentzVector

pdgIds={1:-2/3,2:1/3,3:-1/3,4:+2/3,5:-1/3,6:2/3,11:-1,12:0,13:-1,14:0,15:-1,16:0} 

def if3(cond, iftrue, iffalse):
    return iftrue if cond else iffalse
def outgoingQs(lhepart):
    if (lhepart.status == 1 and abs(lhepart.pdgId) < 6):return True
    else: return False


def outgoingLeptons(lhepart):
    if (lhepart.status == 1 and  abs(lhepart.pdgId) in range(10,17) ): return True
    else: return False

def findW(lhe_parts):
    foundW=False; q1_index=-99;q2_index=-99;
    chargeW=0;foundWminus=False;foundWplus=False
    for i in range(len(lhe_parts)):
        if (foundW): break
        for j in range(i+1,len(lhe_parts)):
            charge_i=pdgIds[abs(lhe_parts[i].pdgId)]*abs(lhe_parts[i].pdgId)/lhe_parts[i].pdgId
            charge_j=pdgIds[abs(lhe_parts[j].pdgId)]*abs(lhe_parts[j].pdgId)/lhe_parts[j].pdgId
            chargeW=charge_i+charge_j
            if (abs(lhe_parts[i].pdgId) != abs(lhe_parts[j].pdgId) and chargeW != 0 and lhe_parts[i].pdgId*lhe_parts[j].pdgId < 0):
                foundWplus = True if chargeW > 0 else False
                foundWminus = True if chargeW < 0 else False
                q1_index = i if lhe_parts[i].pdgId >0 else j
                q2_index = j if lhe_parts[j].pdgId <0 else i
                #print 'pairs found',lhe_parts[i].pdgId,lhe_parts[j].pdgId,chargeW
            else: continue

    foundW=foundWplus or foundWminus
    chargeW = 1 if foundWplus else -1 #just to make sure 
    if foundW and chargeW == 0 : print "this is an issue",lhe_parts[q1_index].pdgId,lhe_parts[q2_index].pdgId,chargeW
    if foundW:
        return (q1_index,q2_index,chargeW) #first particle is the one with a negatively charged lepton or a quark or a neu 
    else: return (-99,-99,0)



class genFriendProducer(Module):
    def __init__(self):
        self.label = "" # "" if (label in ["",None]) else ("_"+label)
        #self.vars = ("pt","eta","phi","mass","pdgId","status","spin")
        self.beamE = 6500
        pass

    def beginJob(self):
        pass
    def endJob(self):
        pass


    def CSFrame(self,dilepton):
        pMass = 0.938272
        sign = np.sign(dilepton.Z())
        proton1 = ROOT.TLorentzVector(0.,0.,sign*self.beamE,hypot(self.beamE,pMass));  proton2 = ROOT.TLorentzVector(0.,0.,-sign*self.beamE,hypot(self.beamE,pMass))
        proton1.Boost(-dilepton.BoostVector()); proton2.Boost(-dilepton.BoostVector())
        CSAxis = (proton1.Vect().Unit()-proton2.Vect().Unit()).Unit()
        yAxis = (proton1.Vect().Unit()).Cross((proton2.Vect().Unit()));
        yAxis = yAxis.Unit();
        xAxis = yAxis.Cross(CSAxis);
        xAxis = xAxis.Unit();
        return (xAxis,yAxis,CSAxis)
    def cosThetaCS(self,lplus,lminus):
        dilep = lplus + lminus
        boostedLep = lminus #ROOT.TLorentzVector(lminus)
        boostedLep.Boost(-dilep.BoostVector())
        csframe = self.CSFrame(dilep)
        return cos(boostedLep.Angle(csframe[2]))
    def cosTheta2D(self,w,lep):
        boostedLep = lep #ROOT.TLorentzVector(lep)
        neww = ROOT.TLorentzVector()
        neww.SetPxPyPzE(w.Px(),w.Py(),0.,w.E())
        boostedLep.Boost(-neww.BoostVector())
        cost2d = (boostedLep.Px()*w.Px() + boostedLep.Py()*w.Py()) / (boostedLep.Pt()*w.Pt())
        return cost2d
    def cosThetaCM(self,lplus,lminus):
        dilep = lplus + lminus
        boostedLep = ROOT.TLorentzVector(lminus)
        boostedLep.Boost(-dilep.BoostVector())
        modw = sqrt(dilep.X()*dilep.X() + dilep.Y()*dilep.Y() + dilep.Z()*dilep.Z())
        modm = sqrt(boostedLep.X()*boostedLep.X() + boostedLep.Y()*boostedLep.Y() + boostedLep.Z()*boostedLep.Z())
        cos = (dilep.X()*boostedLep.X() + dilep.Y()*boostedLep.Y() + dilep.Z()*boostedLep.Z())/modw/modm
        return cos
    def phiCS(self,lplus,lminus):
        dilep = lplus + lminus
        boostedLep = lminus #ROOT.TLorentzVector(lminus)
        boostedLep.Boost(-dilep.BoostVector())
        csframe = self.CSFrame(dilep)
        phi = atan2((boostedLep.Vect()*csframe[1]),(boostedLep.Vect()*csframe[0]))
        if(phi<0): return phi + 2*ROOT.TMath.Pi()
        else: return phi

    def beginFile(self, inputFile, outputFile, inputTree, wrappedOutputTree):
        self.out = wrappedOutputTree
        #self.out.branch("nLHEquarks"+self.label,"I")
        #self.out.branch("costheta_Whad_CSF"+self.label,"F")
        #for V in self.vars:
        #    self.out.branch("LHEquark"+self.label+"_"+V, "F", lenVar="nLHEquarks"+self.label)

        self.out.branch("genwhad_costcm","F")
        self.out.branch("genwhad_costcs","F")
        self.out.branch("genwhad_cost2d","F")
        self.out.branch("genwhad_phics", "F")
        self.out.branch("genwhad_mt"   , "F")
        self.out.branch("genwhad_y","F")
        self.out.branch("genwhad_pt","F")
        self.out.branch("genwhad_eta","F")
        self.out.branch("genwlep_costcm","F")
        self.out.branch("genwlep_costcs","F")
        self.out.branch("genwlep_cost2d","F")
        self.out.branch("genwlep_phics", "F")
        self.out.branch("genwlep_mt"   , "F")
        self.out.branch("genwlep_y","F")
        self.out.branch("genwlep_pt","F")
        self.out.branch("genwlep_eta","F")
        self.out.branch("recoil_whad_x","F")
        self.out.branch("recoil_whad_y","F")

        self.out.branch("recoil_wlep_x","F")
        self.out.branch("recoil_wlep_y","F")

    def endFile(self, inputFile, outputFile, inputTree, wrappedOutputTree):
        pass

    def analyze(self, event):
        """process event, return True (go to next module) or False (fail, go to next event)"""
        Quarks = filter(outgoingQs, Collection(event,"LHEPart"))
        Leptons= filter(outgoingLeptons, Collection(event,"LHEPart"))

        if len(Quarks)+len(Leptons) < 4: return False
        l1,l2,charge_Wlep=findW(Leptons) #lepton (el-,mu-,tau-) & neu have pdgid >0 #first particle is the one with a negatively charged lepton or a quark or a neu 
        q1,q2,charge_Whad=findW(Quarks) #qbars have negative pdgIds
  
        #print "found these leps",l1,l2, " and quarks",q1,q2
        if len({l1,l2})+len({q1,q2}) < 4 : return False
        #print "set",({l1,l2,q1,q2})
        # convention for phiCS: use l- direction for W-, use neutrino for W+
        #neu has pdgId higher than lep
        (Lplus,Lminus)=(None,None)
        if charge_Wlep > 0: #W+couples to neu
            (Lplus,Lminus) = (Leptons[l2],Leptons[l1]) if abs(Leptons[l2].pdgId) > abs(Leptons[l1].pdgId) else (Leptons[l1],Leptons[l2]) #first particle is the ref
        else:
            (Lplus,Lminus) = (Leptons[l2],Leptons[l1]) if abs(Leptons[l2].pdgId) < abs(Leptons[l1].pdgId) else (Leptons[l1],Leptons[l2])

        (Q,Qbar)=(None,None) #q1 is always a quark 
        (Q,Qbar) = (Quarks[q1],Quarks[q2]) if charge_Whad > 0  else (Quarks[q2],Quarks[q1])

        q=ROOT.TLorentzVector(0.0,0.0,0.0,0.0);
        qbar=ROOT.TLorentzVector(0.0,0.0,0.0,0.0);
        lplus=ROOT.TLorentzVector(0.0,0.0,0.0,0.0);
        lminus=ROOT.TLorentzVector(0.0,0.0,0.0,0.0);
        genwlep=ROOT.TLorentzVector(0.0,0.0,0.0,0.0);
        genwhad=ROOT.TLorentzVector(0.0,0.0,0.0,0.0);
        q.SetPtEtaPhiM(Q.pt,Q.eta,Q.phi,Q.mass);
        qbar.SetPtEtaPhiM(Qbar.pt,Qbar.eta,Qbar.phi,Qbar.mass);
        lminus.SetPtEtaPhiM(Lminus.pt,Lminus.eta,Lminus.phi,Lminus.mass); #or a neu
        lplus.SetPtEtaPhiM(Lplus.pt,Lplus.eta,Lplus.phi,Lplus.mass); #or an anti-neu

        genwlep=lminus+lminus
        genwhad=q+qbar
        #print "charge of Wlep %d and reference particle pdgId %d"%(charge_Wlep,Lplus.pdgId)
        #print "charge of Whad %d and reference particle pdgId %d"%(charge_Whad,Q.pdgId)
        # convention for phiCS: use l- direction for W-, use neutrino for W+
        #W+ couples with q(left handed) and W- with qbar (right handed)
        #(lplus,lminus) = (neutrinos[0],dressedLeptons[0]) if lep_pdgid[0]<0 else (dressedLeptons[0],neutrinos[0])

        self.out.fillBranch("genwhad_costcm",self.cosThetaCM(q,qbar))
        self.out.fillBranch("genwhad_costcs",self.cosThetaCS(q,qbar))
        self.out.fillBranch("genwhad_cost2d",self.cosTheta2D(genwhad,q))
        self.out.fillBranch("genwhad_phics",self.phiCS(q,qbar))
        self.out.fillBranch("genwhad_mt"   , sqrt(2*q.Pt()*qbar.Pt()*(1.-cos(deltaPhi(q.Phi(),qbar.Phi())) )))
        self.out.fillBranch("genwhad_y",genwhad.Rapidity())
        self.out.fillBranch("genwhad_pt",genwhad.Pt())
        self.out.fillBranch("genwhad_eta",genwhad.Eta())
        self.out.fillBranch("recoil_whad_x",-q.Px()-qbar.Px())
        self.out.fillBranch("recoil_whad_y",-q.Py()-qbar.Py())

        self.out.fillBranch("genwlep_costcm",self.cosThetaCM(lplus,lminus))
        self.out.fillBranch("genwlep_costcs",self.cosThetaCS(lplus,lminus))
        self.out.fillBranch("genwlep_cost2d",self.cosTheta2D(genwlep,lplus))
        self.out.fillBranch("genwlep_phics",self.phiCS(lplus,lminus))
        self.out.fillBranch("genwlep_mt"   , sqrt(2*lplus.Pt()*lminus.Pt()*(1.-cos(deltaPhi(lplus.Phi(),lminus.Phi())) )))
        self.out.fillBranch("genwlep_y",genwlep.Rapidity())
        self.out.fillBranch("genwlep_pt",genwlep.Pt())
        self.out.fillBranch("genwlep_eta",genwlep.Eta())
        self.out.fillBranch("recoil_wlep_x",-lplus.Px()-lminus.Px())
        self.out.fillBranch("recoil_wlep_y",-lplus.Py()-lminus.Py())
        return True
##am
##am        if len(lhe_parts) < 2: return False
##am        foundWplus=False;foundWminus=False;
##am        q1_index=-99;q2_index=-99;
##am        for i in range(len(lhe_parts)):
##am            for j in range(i+1,len(lhe_parts)):
##am                sign_i=abs(lhe_parts[i].pdgId)/lhe_parts[i].pdgId
##am                sign_j=abs(lhe_parts[j].pdgId)/lhe_parts[j].pdgId
##am                charge_i=pdgIds[abs(lhe_parts[i].pdgId)]
##am                charge_j=pdgIds[abs(lhe_parts[j].pdgId)]
##am                chargeW=sign_i*charge_i+(sign_j*charge_j)
##am                if abs(lhe_parts[i].pdgId) == abs(lhe_parts[j].pdgId) or abs(chargeW) > 1 or lhe_parts[i].pdgId*lhe_parts[j].pdgId > 0:  
##am                    continue #W will decay to q q'bar always
##am                else:
##am                    foundWplus=True if chargeW > 0 else False
##am                    foundWminus=True if chargeW < 0 else False
##am                    q1_index=i;q2_index=j
##am                    break;
##am        q=ROOT.TLorentzVector(0.0,0.0,0.0,0.0);
##am        qbar=ROOT.TLorentzVector(0.0,0.0,0.0,0.0);
##am        genw=ROOT.TLorentzVector(0.0,0.0,0.0,0.0);
##am        pdgId_q1=lhe_parts[q1_index].pdgId;pdgId_q2=lhe_parts[q2_index].pdgId
##am        quark1=if3(pdgId_q1 >0,lhe_parts[q1_index],lhe_parts[q2_index])
##am        quark2=if3(pdgId_q1 <0,lhe_parts[q1_index],lhe_parts[q2_index])
##am        q.SetPtEtaPhiM(quark1.pt,quark1.eta,quark1.phi,quark1.mass);
##am        qbar.SetPtEtaPhiM(quark2.pt,quark2.eta,quark2.phi,quark2.mass);
##am        genw=q+qbar
##am        (lplus,lminus) = (q,qbar) if foundWplus else (qbar,q)
##am        # convention for phiCS: use l- direction for W-, use neutrino for W+
##am        #W+ couples with q(left handed) and W- with qbar (right handed)
##am        #(lplus,lminus) = (neutrinos[0],dressedLeptons[0]) if lep_pdgid[0]<0 else (dressedLeptons[0],neutrinos[0])
##am        self.out.fillBranch("genw_costcm",self.cosThetaCM(lplus,lminus))
##am        self.out.fillBranch("genw_costcs",self.cosThetaCS(lplus,lminus))
##am        self.out.fillBranch("genw_cost2d",self.cosTheta2D(genw,lplus))
##am        self.out.fillBranch("genw_phics",self.phiCS(lplus,lminus))
##am        self.out.fillBranch("genw_mt"   , sqrt(2*lplus.Pt()*lminus.Pt()*(1.-cos(deltaPhi(lplus.Phi(),lminus.Phi())) )))
##am        self.out.fillBranch("genw_y",genw.Rapidity())
##am        self.out.fillBranch("genw_pt",genw.Pt())
##am        self.out.fillBranch("genw_eta",genw.Eta())
##am        self.out.fillBranch("recoil_x",-q.Px()-qbar.Px())
##am        self.out.fillBranch("recoil_y",-q.Py()-qbar.Py())
##am
##am        return True


