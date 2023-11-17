import ROOT
import os, array
import numpy as np
from PhysicsTools.NanoAODTools.postprocessing.framework.eventloop import Module 
from PhysicsTools.NanoAODTools.postprocessing.framework.datamodel import Collection 
from PhysicsTools.NanoAODTools.postprocessing.tools import deltaR, deltaPhi
from math import cos,sin,sqrt, pi


pdgIds={1:-2/3,2:1/3,3:-1/3,4:+2/3,5:-1/3,6:2/3,11:-1,12:0,13:-1,14:0,15:-1,16:0} 

def if3(cond, iftrue, iffalse):
    return iftrue if cond else iffalse

def goodfatjets(fjet):
    if (fjet.pt > 200 and abs(fjet.eta) < 2.4 and abs(fjet.partonFlavour) > 0 and abs(fjet.partonFlavour) !=21):return True
    else: return False
def gooddLeptons(dlep):
    if (dlep.pt > 50): return True
    else: return False

def goodlheparts(lheP):
    if (lheP.status == 1 and lheP.status !=21): return True
    else: return False


def findW(lhe_parts):
    foundW=False; q_index=-99;qbar_index=-99; lep_index=-99;neu_index=-99;
    charge_Whad=0;    charge_Wlep=0;
    for i in range(len(lhe_parts)):
        if abs(lhe_parts[i].pdgId) in [11,13,15]:            
            charge_Wlep=-1*lhe_parts[i].pdgId/abs(lhe_parts[i].pdgId)
            lep_index=i;
        elif abs(lhe_parts[i].pdgId) in [12,14,16]:
            neu_index=i;
        elif abs(lhe_parts[i].pdgId) < 7: #getting rid of gluons from radiation 
            charge_i=pdgIds[abs(lhe_parts[i].pdgId)]*abs(lhe_parts[i].pdgId)/lhe_parts[i].pdgId
            for j in range(i+1,len(lhe_parts)):
                if (abs(lhe_parts[j].pdgId) > 7 or lhe_parts[i].pdgId == lhe_parts[j].pdgId ): continue
                charge_j=pdgIds[abs(lhe_parts[j].pdgId)]*abs(lhe_parts[j].pdgId)/lhe_parts[j].pdgId
                charge_Whad=charge_i+charge_j
                if (abs(charge_Whad) ==1 and charge_Whad+charge_Wlep==0):
                    q_index = i if charge_i > 0 else j
                    qbar_index = i if charge_i < 0 else j
                else: continue
        else: conitnue
    return (lep_index,neu_index,q_index,qbar_index,charge_Wlep,charge_Whad) #first particle is the one with a negatively charged lepton or a quark or a neu 



def calcmassWV(l1,fjet,metpt,metphi,typ,opt):
    from ROOT.heppy import METzCalculator
    NeutrinoPz = METzCalculator()
    met=ROOT.TLorentzVector(0.0,0.0,0.0,0.0);
    metV=ROOT.TLorentzVector(0.0,0.0,0.0,0.0);
    lepton1=ROOT.TLorentzVector(0.0,0.0,0.0,0.0);
    fatjet1=ROOT.TLorentzVector(0.0,0.0,0.0,0.0);
    mWV=ROOT.TLorentzVector(0.0,0.0,0.0,0.0);
    met.SetPtEtaPhiM(metpt,0.,metphi,0.);
    lepton1.SetPtEtaPhiM(l1.pt,l1.eta,l1.phi,l1.mass);
    fatjet1.SetPtEtaPhiM(fjet.pt,fjet.eta,fjet.phi,fjet.mass); 
    NeutrinoPz.SetMET(met);
    NeutrinoPz.SetLepton(lepton1);
    NeutrinoPz.SetLeptonType(l1.pdgId);
    nu_pz=NeutrinoPz.Calculate(typ)
    metV.SetPxPyPzE(metpt*cos(metphi), metpt*sin(metphi),nu_pz,sqrt(metpt*metpt+nu_pz*nu_pz));
    mWV=lepton1+fatjet1+metV;
    massWV=mWV.M();
    if opt == 1: 
        #print metV.Pz(),metphi,metpt
        return metV
    else:
        return massWV


##amdef computephi_lheLvl(lheparts,typ):
##am    (lep_index,neu_index,q_index,qbar_index,charge_Wlep,charge_Whad)=findW(lheparts)
##am    
##am    wv_sys = ROOT.TLorentzVector(0.,0.,0.,0.);
##am    lep    = ROOT.TLorentzVector(0.0,0.0,0.0,0.0);
##am    fjet   = ROOT.TLorentzVector(0.0,0.0,0.0,0.0);
##am    neu    = ROOT.TLorentzVector(0.,0.,0.,0.);
##am    qbar   = ROOT.TLorentzVector(0.,0.,0.,0.);
##am    q      = ROOT.TLorentzVector(0.,0.,0.,0.); #right handed quark
##am    lep_plus=ROOT.TLorentzVector(0.0,0.0,0.0,0.0);#right handed lepton
##am
##am    
##am    neu.SetPtEtaPhiM(lheparts[neu_index].pt,lheparts[neu_index].eta,lheparts[neu_index].phi,0.);
##am    lep.SetPtEtaPhiM(lheparts[lep_index].pt,lheparts[lep_index].eta,lheparts[lep_index].phi,0.);
##am    q.SetPtEtaPhiM(lheparts[q_index].pt,lheparts[q_index].eta,lheparts[q_index].phi,0.);
##am    qbar.SetPtEtaPhiM(lheparts[qbar_index].pt,lheparts[qbar_index].eta,lheparts[qbar_index].phi,0.);
##am    lep_plus = neu if lheparts[neu_index].pdgId < 0 else lep 
##am
##am    lep_c=ROOT.TLorentzVector(0.0,0.0,0.0,0.0);
##am    fjet_c=ROOT.TLorentzVector(0.0,0.0,0.0,0.0);
##am    lep_c.SetPtEtaPhiM(l1.pt,l1.eta,l1.phi,l1.mass);
##am    fjet_c.SetPtEtaPhiM(fj.pt,fj.eta,fj.phi,fj.mass); 
##am
##am    wv_sys+=lep+fjet+neutrino
##am    wlep=lep+neutrino
##am    #print wv_sys.Pt();
##am    boost_vec=wv_sys.BoostVector()
##am    #print boost_vec.Mag()
##am    
##am    fjet.Boost(-boost_vec)
##am    lep.Boost(-boost_vec); #Make an LT for a passive boost (i.e. object velocity -= in boost direction) 
##am    neutrino.Boost(-boost_vec);
##am    # wv_sys.Boost(-boost_vec)
##am    # print wv_sys.Pt()
##am
##am
##am    c_wlep_boson=ROOT.TLorentzVector(0.,0.,0.,0.);
##am    c_wlep_boson+=lep
##am    c_wlep_boson += neutrino
##am
##am    r_uvec= wv_sys.Vect().Unit(); 
##am    z_uvec = c_wlep_boson.Vect().Unit();  ##direction of w_lep boson
##am    y_uvec = z_uvec.Cross(r_uvec).Unit();
##am    x_uvec = y_uvec.Cross(z_uvec).Unit();
##am    print y_uvec,z_uvec,x_uvec,r_uvec
##am    rot    = ROOT.TRotation();
##am    rot.SetXAxis(x_uvec);
##am    rot.SetYAxis(y_uvec);
##am    rot.SetZAxis(z_uvec);
##am## do a reverse transformation and see if it gives a unit vector 
##am    rotator = ROOT.TLorentzRotation(rot); # initialization but we need the transformation here!! replace by rotator = ROOT.TLorentzRotation(); rotator* = rot;
##am    r_wlep_boson=rotator.Inverse()*c_wlep_boson; ##replace this with -> rotator.Transform(c_wlep_boson); 
##am    r_charged_lepton= rotator.Inverse()*lep; 
##am    r_neutrino = rotator.Inverse()*neutrino;
##am    r_fatjet = rotator.Inverse()*fjet;
##am    return r_wlep_boson,r_charged_lepton,r_neutrino,r_fatjet,neu
##am    #r_charged_lepton.Phi() ##for leptons (with neg charge) = phi+pI modulo 2pi


def computephi(l1,fj,metpt,metphi,typ):

    wv_sys = ROOT.TLorentzVector(0.,0.,0.,0.);
    neutrino=calcmassWV(l1,fj,metpt,metphi,typ,1)
    lep=ROOT.TLorentzVector(0.0,0.0,0.0,0.0);
    fjet=ROOT.TLorentzVector(0.0,0.0,0.0,0.0);
    neu = ROOT.TLorentzVector(0.,0.,0.,0.);
    neu.SetPxPyPzE(metpt*cos(metphi), metpt*sin(metphi),neutrino.Pz(),sqrt(metpt*metpt+neutrino.Pz()*neutrino.Pz()));
    lep.SetPtEtaPhiM(l1.pt,l1.eta,l1.phi,l1.mass);
    fjet.SetPtEtaPhiM(fj.pt,fj.eta,fj.phi,fj.mass); 

    lep_c=ROOT.TLorentzVector(0.0,0.0,0.0,0.0);
    fjet_c=ROOT.TLorentzVector(0.0,0.0,0.0,0.0);
    lep_c.SetPtEtaPhiM(l1.pt,l1.eta,l1.phi,l1.mass);
    fjet_c.SetPtEtaPhiM(fj.pt,fj.eta,fj.phi,fj.mass); 

    wv_sys+=lep+fjet+neutrino
    wlep=lep+neutrino
    #print wv_sys.Pt();
    boost_vec=wv_sys.BoostVector()
    #print boost_vec.Mag()
    
    fjet.Boost(-boost_vec)
    lep.Boost(-boost_vec); #Make an LT for a passive boost (i.e. object velocity -= in boost direction) 
    neutrino.Boost(-boost_vec);
    # wv_sys.Boost(-boost_vec)
    # print wv_sys.Pt()


    c_wlep_boson=ROOT.TLorentzVector(0.,0.,0.,0.);
    c_wlep_boson+=lep
    c_wlep_boson += neutrino
    print "step 1",c_wlep_boson.Pt(),c_wlep_boson.Phi()
    r_uvec= wv_sys.Vect().Unit(); 
    z_uvec = c_wlep_boson.Vect().Unit();  ##direction of w_lep boson
    y_uvec = z_uvec.Cross(r_uvec).Unit();
    x_uvec = y_uvec.Cross(z_uvec).Unit();
    print "axes for new cordinate system",y_uvec.Y(),z_uvec.Z(),x_uvec.X(),r_uvec.Mag()
    rot    = ROOT.TRotation();
    rot.SetXAxis(x_uvec);
    rot.SetYAxis(y_uvec);
    rot.SetZAxis(z_uvec);
    rotator = ROOT.TLorentzRotation(rot);
    ##am    r_wlep_boson=rotator.Inverse()*c_wlep_boson; ##replace this with -> rotator.Transform(c_wlep_boson); 
    r_wlep_boson=rotator*c_wlep_boson;
    print "after rotation",r_wlep_boson.Phi(),r_wlep_boson.Pt() 
    print "rotate back",(rotator.Inverse()*r_wlep_boson).Pt(),(rotator.Inverse()*r_wlep_boson).Phi()
    r_charged_lepton= rotator*lep;
    r_neutrino = rotator*neutrino;
    r_fatjet = rotator*fjet;
    return r_wlep_boson,r_charged_lepton,r_neutrino,r_fatjet,neu
    #r_charged_lepton.Phi() ##for leptons (with neg charge) = phi+pI modulo 2pi

class compute_phi_gen_v1(Module):
    def __init__(self, lepMultiplicity=1,nfjets=1):
        self.label = "" # "" if (label in ["",None]) else ("_"+label)
        self.lepMultiplicity=lepMultiplicity
        self.nfjets=nfjets
        pass

    def beginJob(self):
        pass
    def endJob(self):
        pass
    def endFile(self, inputFile, outputFile, inputTree, wrappedOutputTree):
        pass
    def beginFile(self, inputFile, outputFile, inputTree, wrappedOutputTree):
        self.out = wrappedOutputTree
        for var in 'pt,eta,phi,pdgId,mass,hasTauAnc,pt_HF,eta_HF,phi_HF,mass_HF'.split(','):
            for l in range(self.lepMultiplicity):
                self.out.branch('SeldLep%d_%s'%(l+1,var),'F')
        self.out.branch('nSeldLeps'  ,'I')
        for var in 'pt,eta,phi,mass,hadronFlavour,partonFlavour,pt_HF,eta_HF,phi_HF,mass_HF'.split(','): 
            for j in range(self.nfjets):
                self.out.branch('SelGak8Jet%d_%s'%(j+1,var),'F')
        self.out.branch('nSelGak8Jets'  ,'I')

        self.out.branch('event', 'L')
        self.out.branch('event_presel', 'L')
        self.out.branch('neutrino_pt_HF',  'F')
        self.out.branch('neutrino_eta_HF', 'F')
        self.out.branch('neutrino_phi_HF', 'F')
        self.out.branch('neutrino_mass_HF','F')
        self.out.branch('neutrino_pt',  'F')
        self.out.branch('neutrino_eta', 'F')
        self.out.branch('neutrino_phi', 'F')

    def analyze(self, event):
        """process event, return True (go to next module) or False (fail, go to next event)"""
        self.out.fillBranch('event',event.event)
        fatJets =  filter(goodfatjets,  Collection(event,"GenJetAK8"))
        leptons =  filter(gooddLeptons, Collection(event,"GenDressedLepton"))
        lheparts = filter(goodlheparts, Collection(event,"LHEPart"))
        genmet  = event.GenMET_pt
        genmet_phi = event.GenMET_phi
        self.out.fillBranch('event_presel',event.event)
        self.out.fillBranch('nSeldLeps',len(leptons))
        self.out.fillBranch('nSelGak8Jets',len(fatJets))
        r_wlep_boson=ROOT.TLorentzVector(0.0,0.0,0.0,0.0);
        r_charged_lepton=ROOT.TLorentzVector(0.0,0.0,0.0,0.0);
        r_neutrino=ROOT.TLorentzVector(0.0,0.0,0.0,0.0);
        r_neu=ROOT.TLorentzVector(0.0,0.0,0.0,0.0);
        sel_bool= genmet > 110 and  len(fatJets) > 0 and len(leptons) == 1
        if sel_bool:
            r_wlep_boson,r_charged_lepton,r_neutrino,r_fatjet,r_neu=computephi(leptons[0],fatJets[0],genmet,genmet_phi,0)
        #if (genmet < 110 or len(fatJets) < 1 or len(leptons) < 1): return False

        for lep in range(self.lepMultiplicity):
            for var in 'pt,eta,phi,pdgId,mass,hasTauAnc'.split(','):
                self.out.fillBranch('SeldLep%d_%s'%(lep+1,var),getattr(leptons[lep],var) if sel_bool else -999)
            self.out.fillBranch('SeldLep%d_pt_HF'%(lep+1),r_charged_lepton.Pt() if sel_bool else -999)
            self.out.fillBranch('SeldLep%d_eta_HF'%(lep+1),r_charged_lepton.Eta() if sel_bool else -999)
            phi = -999;
            if sel_bool:
                phi = r_charged_lepton.Phi() if leptons[lep].pdgId < 0  else r_charged_lepton.Phi()+pi
            if (phi > float(pi)): phi -= float(2*pi);
            elif (phi <= -float(pi)): phi += float(2*pi);
            self.out.fillBranch('SeldLep%d_phi_HF'%(lep+1),phi if sel_bool else -999 )
            self.out.fillBranch('SeldLep%d_mass_HF'%(lep+1),r_charged_lepton.M() if sel_bool else -999)
        for j in range(self.nfjets):
            for var in 'pt,eta,phi,mass,hadronFlavour,partonFlavour'.split(','): 
                self.out.fillBranch('SelGak8Jet%d_%s'%(j+1,var),getattr(fatJets[j],var) if sel_bool else -999)
            self.out.fillBranch('SelGak8Jet%d_pt_HF'%(j+1),r_fatjet.Pt() if sel_bool else -999)
            self.out.fillBranch('SelGak8Jet%d_eta_HF'%(j+1),r_fatjet.Eta() if sel_bool else -999)
            self.out.fillBranch('SelGak8Jet%d_phi_HF'%(j+1),r_fatjet.Phi() if sel_bool else -999)
            self.out.fillBranch('SelGak8Jet%d_mass_HF'%(j+1),r_fatjet.M() if sel_bool else -999)

        self.out.fillBranch('neutrino_pt_HF',r_neutrino.Pt() if sel_bool else -999 )
        self.out.fillBranch('neutrino_eta_HF',r_neutrino.Eta() if sel_bool else -999)
        self.out.fillBranch('neutrino_phi_HF',r_neutrino.Phi() if sel_bool else -999 )
        self.out.fillBranch('neutrino_mass_HF',r_neutrino.M() if sel_bool else -999 )
        self.out.fillBranch('neutrino_pt',r_neu.Pt() if sel_bool else -999 )
        self.out.fillBranch('neutrino_eta',r_neu.Eta() if sel_bool else -999)
        self.out.fillBranch('neutrino_phi',r_neu.Phi() if sel_bool else -999 )


        return True
