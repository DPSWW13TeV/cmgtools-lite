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



def computephi(l1,fj,metpt,metphi,typ):

    wv_sys = ROOT.TLorentzVector(0.,0.,0.,0.);
    neutrino=calcmassWV(l1,fj,metpt,metphi,typ,1)
    lep=ROOT.TLorentzVector(0.0,0.0,0.0,0.0);
    fjet=ROOT.TLorentzVector(0.0,0.0,0.0,0.0);
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

    r_uvec= wv_sys.Vect().Unit(); 
    z_uvec = c_wlep_boson.Vect().Unit();  ##direction of w_lep boson
    y_uvec = z_uvec.Cross(r_uvec).Unit();
    x_uvec = y_uvec.Cross(z_uvec).Unit();
    rot    = ROOT.TRotation();
    rot.SetXAxis(x_uvec);
    rot.SetYAxis(y_uvec);
    rot.SetZAxis(z_uvec);
    rotator = ROOT.TLorentzRotation(rot);
    r_wlep_boson=rotator.Inverse()*c_wlep_boson;
    r_charged_lepton= rotator.Inverse()*lep;
    r_neutrino = rotator.Inverse()*neutrino;
    r_fatjet = rotator.Inverse()*fjet;
    return r_wlep_boson,r_charged_lepton,r_neutrino,r_fatjet
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
    def analyze(self, event):
        """process event, return True (go to next module) or False (fail, go to next event)"""
        self.out.fillBranch('event',event.event)
        fatJets = filter(goodfatjets, Collection(event,"GenJetAK8"))
        leptons = filter(gooddLeptons, Collection(event,"GenDressedLepton"))
        genmet  = event.GenMET_pt
        genmet_phi = event.GenMET_phi
        if (genmet < 110 or len(fatJets) < 1 or len(leptons) < 1): return False
        self.out.fillBranch('event_presel',event.event)
        self.out.fillBranch('nSeldLeps',len(leptons))
        self.out.fillBranch('nSelGak8Jets',len(fatJets))
        r_wlep_boson,r_charged_lepton,r_neutrino,r_fatjet=computephi(leptons[0],fatJets[0],genmet,genmet_phi,0)
        for lep in range(self.lepMultiplicity):
            for var in 'pt,eta,phi,pdgId,mass,hasTauAnc'.split(','):
                self.out.fillBranch('SeldLep%d_%s'%(lep+1,var),getattr(leptons[lep],var))
            self.out.fillBranch('SeldLep%d_pt_HF'%(lep+1),r_charged_lepton.Pt())
            self.out.fillBranch('SeldLep%d_eta_HF'%(lep+1),r_charged_lepton.Eta())
            phi = r_charged_lepton.Phi() if leptons[lep].pdgId < 0 else r_charged_lepton.Phi()+pi
            if (phi > float(pi)): phi -= float(2*pi);
            elif (phi <= -float(pi)): phi += float(2*pi);
            self.out.fillBranch('SeldLep%d_phi_HF'%(lep+1),phi)
            self.out.fillBranch('SeldLep%d_mass_HF'%(lep+1),r_charged_lepton.M())
        for j in range(self.nfjets):
            for var in 'pt,eta,phi,mass,hadronFlavour,partonFlavour'.split(','): 
                self.out.fillBranch('SelGak8Jet%d_%s'%(j+1,var),getattr(fatJets[j],var))
            self.out.fillBranch('SelGak8Jet%d_pt_HF'%(j+1),r_fatjet.Pt())
            self.out.fillBranch('SelGak8Jet%d_eta_HF'%(j+1),r_fatjet.Eta())
            self.out.fillBranch('SelGak8Jet%d_phi_HF'%(j+1),r_fatjet.Phi())
            self.out.fillBranch('SelGak8Jet%d_mass_HF'%(j+1),r_fatjet.M())

        self.out.fillBranch('neutrino_pt_HF',r_neutrino.Pt())
        self.out.fillBranch('neutrino_eta_HF',r_neutrino.Eta())
        self.out.fillBranch('neutrino_phi_HF',r_neutrino.Phi())
        self.out.fillBranch('neutrino_mass_HF',r_neutrino.M())
        return True
