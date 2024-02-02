import ROOT
import os, array
import numpy as np
from PhysicsTools.NanoAODTools.postprocessing.framework.eventloop import Module 
from PhysicsTools.NanoAODTools.postprocessing.framework.datamodel import Collection 
from PhysicsTools.NanoAODTools.postprocessing.tools import deltaR, deltaPhi
from math import cos,sin,sqrt, pi,acos,tanh, hypot


pdgIds={1:-2/3,2:1/3,3:-1/3,4:+2/3,5:-1/3,6:2/3,11:-1,12:0,13:-1,14:0,15:-1,16:0} 

def if3(cond, iftrue, iffalse):
    return iftrue if cond else iffalse

def goodfatjets(fjet):
    if (fjet.pt > 200 and abs(fjet.eta) < 2.4 and abs(fjet.partonFlavour) > 0 and abs(fjet.partonFlavour) !=21):return True
    else: return False
def gooddLeptons(dlep):
    if (dlep.pt > 50 and abs(dlep.eta) < 2.5): return True
    else: return False


def goodlheparts(lheP):
    if (lheP.status == 1 and lheP.pdgId !=21 and ( abs(lheP.pdgId) < 7 or abs(lheP.pdgId) in range(11,17) )  ): return True #lepton and jet pT cuts later down the road
    else: return False


def phicorrection(phivalue,pdgId=-1):
    phi1=-999
    phi1=phivalue if pdgId<0 else phivalue+pi
    if ( phi1 > float(pi)):phi1-=float(2*pi)
    elif( phi1 <=-float(pi)):phi1+=float(2*pi)
    return phi1
def theta_lep_neu(lep_eta,neu_eta,lep_pdgid):
    if(lep_pdgid>0):
        return acos(tanh((neu_eta-lep_eta)/2))
    else:
        return acos(tanh((lep_eta-neu_eta)/2))
def pt_2(pt1, phi1, pt2, phi2): 
    phi2 -= phi1;
    return hypot(pt1 + pt2 *cos(phi2), pt2*sin(phi2))
def mass_WV(lep1,neu1,fjet,fjet2=ROOT.TLorentzVector(0.,0.,0.,0.)):
    mWVvec=ROOT.TLorentzVector(0.,0.,0.,0);
    mWVvec=lep1+neu1+fjet+fjet2
    return mWVvec.M()
def mass_WV2(l1,fjet,neu,fjet2=ROOT.TLorentzVector(0.0,0.0,0.0,0.0)):
    neutrino1=ROOT.TLorentzVector(0.0,0.0,0.0,0.0);
    lepton1=ROOT.TLorentzVector(0.0,0.0,0.0,0.0);
    fatjet1=ROOT.TLorentzVector(0.0,0.0,0.0,0.0);
    fatjet2=ROOT.TLorentzVector(0.0,0.0,0.0,0.0);
    mWV=ROOT.TLorentzVector(0.0,0.0,0.0,0.0)
    lepton1.SetPtEtaPhiM(l1.pt,l1.eta,l1.phi,l1.mass);
    fatjet1.SetPtEtaPhiM(fjet.pt,fjet.eta,fjet.phi,fjet.mass);
    fatjet2.SetPtEtaPhiM(fjet2.pt,fjet2.eta,fjet2.phi,fjet2.mass);
    neutrino1.SetPtEtaPhiM(neu.pt,neu.eta,neu.phi,neu.mass);
    mWV=lepton1+fatjet1+neutrino1+fatjet2;
    massWV=mWV.M();
    return massWV

def findW(lhe_parts):
    foundW=False; q_index=-99;qbar_index=-99; lep_index=-99;neu_index=-99;
    charge_Whad=0;    charge_Wlep=0; good_event=False;
    for i in range(len(lhe_parts)):
        if abs(lhe_parts[i].pdgId) in [11,13,15] and lhe_parts[i].pt > 50 and abs(lhe_parts[i].eta) < 2.5:
            charge_Wlep=-1*lhe_parts[i].pdgId/abs(lhe_parts[i].pdgId) 
            lep_index=i;
        elif abs(lhe_parts[i].pdgId) in [12,14,16] and lhe_parts[i].pt > 110:
            neu_index=i;
        elif abs(lhe_parts[i].pdgId) < 7: #getting rid of gluons from radiation 
            charge_i=pdgIds[abs(lhe_parts[i].pdgId)]*abs(lhe_parts[i].pdgId)/lhe_parts[i].pdgId #
            for j in range(i+1,len(lhe_parts)):
                if (abs(lhe_parts[j].pdgId) > 7 or lhe_parts[i].pdgId == lhe_parts[j].pdgId ): continue
                charge_j=pdgIds[abs(lhe_parts[j].pdgId)]*abs(lhe_parts[j].pdgId)/lhe_parts[j].pdgId
                charge_Whad=charge_i+charge_j
                if (abs(charge_Whad) ==1 and charge_Whad+charge_Wlep==0):
                    q_index = i if charge_i > 0 else j
                    qbar_index = i if charge_i < 0 else j
                else: continue
        else: continue
    fatjet = ROOT.TLorentzVector(0.0,0.0,0.0,0.0);        q    = ROOT.TLorentzVector(0.,0.,0.,0.);        qbar   = ROOT.TLorentzVector(0.,0.,0.,0.);
    if q_index>-99 or qbar_index>-99: 
        q.SetPtEtaPhiM(lhe_parts[q_index].pt,lhe_parts[q_index].eta,lhe_parts[q_index].phi,0.);        qbar.SetPtEtaPhiM(lhe_parts[qbar_index].pt,lhe_parts[qbar_index].eta,lhe_parts[qbar_index].phi,0.);
        fatjet=q+qbar
    else: 
        q.SetPtEtaPhiM(lhe_parts[0].pt,lhe_parts[0].eta,lhe_parts[0].phi,0.);        qbar.SetPtEtaPhiM(lhe_parts[0].pt,lhe_parts[0].eta,lhe_parts[0].phi,0.);
        fatjet=q+qbar
    #print len(lhe_parts),lep_index, neu_index,q_index,qbar_index
    good_event= q_index > -99 and qbar_index > -99 and  lep_index > -99  and neu_index > -99 and fatjet.Pt() > 200 and abs(fatjet.Eta()) < 2.4
    if lep_index > -99 and neu_index > -99:
        return (lhe_parts[lep_index],lhe_parts[neu_index],fatjet,charge_Wlep,charge_Whad,q_index,qbar_index,lep_index,neu_index,good_event) #first particle is the one with a negatively charged lepton or a quark or a neu 
    else:
        return (lhe_parts[0],lhe_parts[0],fatjet,charge_Wlep,charge_Whad,q_index,qbar_index,lep_index,neu_index,good_event)


def calcmassWV(l1,fjet,metpt,metphi,typ):
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
    return (metV,massWV)

def computephi(l1,fj,metpt,metphi,neutrino,useLHE=False):

    wv_sys = ROOT.TLorentzVector(0.,0.,0.,0.);
    lep  = ROOT.TLorentzVector(0.0,0.0,0.0,0.0);
    fjet = ROOT.TLorentzVector(0.0,0.0,0.0,0.0);
    neu  = ROOT.TLorentzVector(0.,0.,0.,0.);
    if not useLHE:
        neu.SetPxPyPzE(metpt*cos(metphi), metpt*sin(metphi),neutrino.Pz(),sqrt(metpt*metpt+neutrino.Pz()*neutrino.Pz()));
        lep.SetPtEtaPhiM(l1.pt,l1.eta,l1.phi,0.0);
        fjet.SetPtEtaPhiM(fj.pt,fj.eta,fj.phi,fj.mass);
    else: 
        neu.SetPtEtaPhiM(neutrino.pt,neutrino.eta,neutrino.phi,0); 
        lep.SetPtEtaPhiM(l1.pt,l1.eta,l1.phi,0.0);
        fjet.SetPtEtaPhiM(fj.Pt(),fj.Eta(),fj.Phi(),fj.M());


    wv_sys+=lep+fjet+neu
    wlep=lep+neu
    #print wv_sys.Pt();
    boost_vec=wv_sys.BoostVector()
    #print boost_vec.Mag()
    
    fjet.Boost(-boost_vec)
    lep.Boost(-boost_vec); #Make an LT for a passive boost (i.e. object velocity -= in boost direction) 
    neu.Boost(-boost_vec);
    # wv_sys.Boost(-boost_vec)
    # print wv_sys.Pt()
    c_wlep_boson=ROOT.TLorentzVector(0.,0.,0.,0.);
    c_wlep_boson+=lep
    c_wlep_boson += neu
    #print "step 1",c_wlep_boson.Pt(),c_wlep_boson.Phi(),c_wlep_boson.X(),c_wlep_boson.Y(),c_wlep_boson.Z();
    r_uvec= wv_sys.Vect().Unit(); 
    z_uvec = c_wlep_boson.Vect().Unit();  ##direction of w_lep boson
    y_uvec = z_uvec.Cross(r_uvec).Unit();
    x_uvec = y_uvec.Cross(z_uvec).Unit();
    #print "axes for new cordinate system",y_uvec.Y(),z_uvec.Z(),x_uvec.X(),r_uvec.Mag()
    rot    = ROOT.TRotation();
    rot.SetXAxis(x_uvec);
    rot.SetYAxis(y_uvec);
    rot.SetZAxis(z_uvec);
    rotator = ROOT.TLorentzRotation(rot);
    r_wlep_boson=rotator*c_wlep_boson;
    #print "after rotation",r_wlep_boson.Phi(),r_wlep_boson.Pt() 
    #print "rotate back",(rotator.Inverse()*r_wlep_boson).Pt(),(rotator.Inverse()*r_wlep_boson).Phi(),(rotator.Inverse()*r_wlep_boson).X(),(rotator.Inverse()*r_wlep_boson).Y(),(rotator.Inverse()*r_wlep_boson).Z()
    r_charged_lepton= rotator*lep;
    r_neutrino = rotator*neu;
    r_fatjet = rotator*fjet;
    return r_wlep_boson,r_charged_lepton,r_neutrino,r_fatjet    #r_charged_lepton.Phi() ##for leptons (with neg charge) = phi+pI modulo 2pi






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
        for var in 'pt,eta,phi,pdgId,hasTauAnc'.split(','):
            for l in range(self.lepMultiplicity):
                self.out.branch('SeldLep%d_%s'%(l+1,var),'F')
                self.out.branch('SeldLep%d_%s_HF_typ0'%(l+1,var),'F')
                self.out.branch('SeldLep%d_%s_HF_typ2'%(l+1,var),'F')
                
        self.out.branch('nSeldLeps'  ,'I')
        
        for var in 'pt,eta,phi,mass,hadronFlavour,partonFlavour'.split(','): 
            for j in range(self.nfjets):
                self.out.branch('SelGak8Jet%d_%s'        %(j+1,var),'F')
                self.out.branch('SelGak8Jet%d_%s_HF_typ0'%(j+1,var),'F')
                self.out.branch('SelGak8Jet%d_%s_HF_typ2'%(j+1,var),'F')

        self.out.branch('nSelGak8Jets'  ,'I')
        self.out.branch('event', 'L')
        self.out.branch('event_presel', 'L')
        self.out.branch('nSelLHEpart'  ,'I')
        for tip in 'typ0,typ2,HF_typ2,HF_typ0'.split(','):
            for var in 'theta,mWV,W_pt'.split(','):
                self.out.branch('%s_%s'%(var,tip),'F')
        for var in 'pt,eta,phi'.split(','):
            self.out.branch('neutrino_%s_typ0'   %(var), 'F')
            self.out.branch('neutrino_%s_HF_typ0'%(var),  'F')
            self.out.branch('neutrino_%s_typ2'   %(var), 'F')
            self.out.branch('neutrino_%s_HF_typ2'%(var),  'F')

        for part in 'neu,q,qbar,lep'.split(','):
            for var in 'pt,eta,phi,mass,pdgId'.split(','):
                self.out.branch('lhe_%s_%s'%(part,var),'F')
        for part in 'neu,lep'.split(','):
            for var in 'pt,eta,phi'.split(','):
                self.out.branch('lhe_%s_%s_HF'%(part,var),'F')
        for var in 'pt,eta,phi,mass'.split(','):
            self.out.branch('lhe_fjet_%s'%(var),'F')
            self.out.branch('lhe_fjet_%s_HF'%(var),'F')
        self.out.branch('lhe_theta','F')
        self.out.branch('lhe_theta_HF','F')
        self.out.branch('lhe_W_pt','F')
        self.out.branch('lhe_W_pt_HF','F')
        self.out.branch('lhe_mWV','F')
        self.out.branch('lhe_mWV_HF','F')

    

        
    def analyze(self, event):
        """process event, return True (go to next module) or False (fail, go to next event)"""
        self.out.fillBranch('event',event.event)

        fatJets =  filter(goodfatjets,  Collection(event,"GenJetAK8"))
        leptons =  filter(gooddLeptons, Collection(event,"GenDressedLepton"))
        lheparts = filter(goodlheparts, Collection(event,"LHEPart"))
        genmet  = event.GenMET_pt
        genmet_phi = event.GenMET_phi
        #print "event number",event.event
        self.out.fillBranch('event_presel',event.event)
        self.out.fillBranch('nSeldLeps',len(leptons))
        self.out.fillBranch('nSelGak8Jets',len(fatJets))
        lhe_lep,lhe_neu,lhe_fjet,charge_Wlep,charge_Whad,q_index,qbar_index,lep_index,neu_index,sel_bool_lhe=findW(lheparts)
        #print "mass of the fatty",lhe_fjet.M()
        
        r_lhe_charged_lepton=ROOT.TLorentzVector(0.0,0.0,0.0,0.0);
        r_lhe_neutrino=ROOT.TLorentzVector(0.0,0.0,0.0,0.0);
        r_lhe_neu=ROOT.TLorentzVector(0.0,0.0,0.0,0.0);

        if sel_bool_lhe:
            r_lhe_wlep_boson,r_lhe_charged_lepton,r_lhe_neutrino,r_lhe_fatjet=computephi(lhe_lep,lhe_fjet,lhe_neu.pt,lhe_neu.phi,lhe_neu,True)

        
        #print "filling starts here"
        self.out.fillBranch('lhe_theta',theta_lep_neu(lhe_lep.eta,lhe_neu.eta,lhe_lep.pdgId) if sel_bool_lhe else -999)
        self.out.fillBranch('lhe_theta_HF',theta_lep_neu(r_lhe_charged_lepton.Eta(),r_lhe_neutrino.Eta(),lhe_lep.pdgId) if sel_bool_lhe else -999)
        self.out.fillBranch('lhe_W_pt',pt_2(lhe_lep.pt,lhe_lep.phi,lhe_neu.pt,lhe_neu.phi)if sel_bool_lhe else -999)
        self.out.fillBranch('lhe_W_pt_HF',pt_2(r_lhe_charged_lepton.Pt(),phicorrection(r_lhe_charged_lepton.Phi(),lheparts[lep_index].pdgId),r_lhe_neutrino.Pt(),phicorrection(r_lhe_neutrino.Phi(),lheparts[neu_index].pdgId))if sel_bool_lhe else -999)
        self.out.fillBranch('lhe_mWV',mass_WV2(lhe_lep,lhe_neu,lheparts[int(q_index)],lheparts[int(qbar_index)])if sel_bool_lhe else -999)
        self.out.fillBranch('lhe_mWV_HF',mass_WV(r_lhe_charged_lepton, r_lhe_neutrino,r_lhe_fatjet)if sel_bool_lhe else -999)
        for var in 'pt,eta,mass,pdgId,phi'.split(','):
            #print "filling for the lhe variable",var
            self.out.fillBranch('lhe_lep_%s' %(var),getattr(lhe_lep,var)  if sel_bool_lhe else -999)
            self.out.fillBranch('lhe_neu_%s' %(var),getattr(lhe_neu,var)  if sel_bool_lhe else -999)
            self.out.fillBranch('lhe_q_%s'   %(var),getattr(lheparts[int(q_index)],var)    if sel_bool_lhe else -999)
            self.out.fillBranch('lhe_qbar_%s'%(var),getattr(lheparts[int(qbar_index)],var) if sel_bool_lhe else -999)
        self.out.fillBranch('lhe_fjet_pt',   lhe_fjet.Pt()  if sel_bool_lhe else -999)
        self.out.fillBranch('lhe_fjet_eta',  lhe_fjet.Eta() if sel_bool_lhe else -999)
        self.out.fillBranch('lhe_fjet_phi',  lhe_fjet.Phi() if sel_bool_lhe else -999)
        self.out.fillBranch('lhe_fjet_mass', lhe_fjet.M()   if sel_bool_lhe else -999)
        
        ##FIXME add same variables in the new frame of refernece for fjet, lep and neu

        self.out.fillBranch('lhe_lep_pt_HF',    r_lhe_charged_lepton.Pt()  if sel_bool_lhe else -999)
        self.out.fillBranch('lhe_lep_eta_HF',   r_lhe_charged_lepton.Eta() if sel_bool_lhe else -999)
        self.out.fillBranch('lhe_lep_phi_HF',   phicorrection(r_lhe_charged_lepton.Phi(),lheparts[lep_index].pdgId) if sel_bool_lhe else -999)
        self.out.fillBranch('lhe_neu_pt_HF',    r_lhe_neutrino.Pt()  if sel_bool_lhe else -999)
        self.out.fillBranch('lhe_neu_eta_HF',   r_lhe_neutrino.Eta() if sel_bool_lhe else -999)
        self.out.fillBranch('lhe_neu_phi_HF',   phicorrection(r_lhe_neutrino.Phi(),lheparts[neu_index].pdgId) if sel_bool_lhe else -999)

        self.out.fillBranch('lhe_fjet_pt_HF',   r_lhe_fatjet.Pt()  if sel_bool_lhe else -999)
        self.out.fillBranch('lhe_fjet_eta_HF',  r_lhe_fatjet.Eta() if sel_bool_lhe else -999)
        self.out.fillBranch('lhe_fjet_phi_HF',  phicorrection(r_lhe_fatjet.Phi(),lheparts[q_index].pdgId) if sel_bool_lhe else -999) ## FIXME AM
        self.out.fillBranch('lhe_fjet_mass_HF', r_lhe_fatjet.M() if sel_bool_lhe else -999) ## FIXME AM
        


        #print "and continues"
        sel_bool=genmet > 110 and  len(fatJets) > 0 and len(leptons) == 1
        #print "selection",sel_bool,sel_bool_lhe
        info={};
        neupdgId=-999;
        if sel_bool: neupdgId=-int(leptons[int(0)].pdgId)
        if sel_bool:
            neu,mWV =calcmassWV(leptons[0],fatJets[0],genmet,genmet_phi,00);
            info['0']=computephi(leptons[0],fatJets[0],genmet,genmet_phi,neu) ## in the HF frame
            neu1,mWV1 =calcmassWV(leptons[0],fatJets[0],genmet,genmet_phi,02);
            info['1']=computephi(leptons[0],fatJets[0],genmet,genmet_phi,neu1) ## in the HF frame
            #print "done"
        else : info={}
        self.out.fillBranch('W_pt_typ0',pt_2(leptons[0].pt,leptons[0].phi,neu.Pt(),phicorrection(neu.Phi(),neupdgId))if sel_bool else -999)
        self.out.fillBranch('W_pt_typ2',pt_2(leptons[0].pt,leptons[0].phi,neu1.Pt(),phicorrection(neu1.Phi(),neupdgId))if sel_bool else -999)
        self.out.fillBranch('W_pt_HF_typ0',pt_2(info['0'][1].Pt(),phicorrection(info['0'][1].Phi(),leptons[0].pdgId),info['0'][2].Pt(),phicorrection(info['0'][2].Phi(),neupdgId))if sel_bool else -999)
        self.out.fillBranch('W_pt_HF_typ2',pt_2(info['1'][1].Pt(),phicorrection(info['1'][1].Phi(),leptons[0].pdgId),info['1'][2].Pt(),phicorrection(info['1'][2].Phi(),neupdgId))if sel_bool else -999)

        self.out.fillBranch('mWV_typ0',mWV  if sel_bool else -999)
        self.out.fillBranch('mWV_typ2',mWV1  if sel_bool else -999)
        self.out.fillBranch('mWV_HF_typ0',mass_WV(info['0'][1],info['0'][2],info['0'][3])  if sel_bool else -999)
        self.out.fillBranch('mWV_HF_typ2',mass_WV(info['1'][1],info['1'][2],info['1'][3])  if sel_bool else -999)

        self.out.fillBranch('theta_typ0',theta_lep_neu(leptons[0].eta,neu.Eta(),leptons[0].pdgId) if sel_bool else -999)
        self.out.fillBranch('theta_typ2',theta_lep_neu(leptons[0].eta,neu1.Eta(),leptons[0].pdgId) if sel_bool else -999)
        self.out.fillBranch('theta_HF_typ0',theta_lep_neu(info['0'][1].Eta(),info['0'][2].Eta(),leptons[0].pdgId) if sel_bool else -999)
        self.out.fillBranch('theta_HF_typ2',theta_lep_neu(info['1'][1].Eta(),info['1'][2].Eta(),leptons[0].pdgId) if sel_bool else -999)

        for var in 'pt,eta,phi,pdgId,hasTauAnc'.split(','):
            self.out.fillBranch('SeldLep1_%s'%(var),getattr(leptons[0],var) if sel_bool else -999 )
        self.out.fillBranch('SeldLep1_pt_HF_typ0',  info['0'][1].Pt() if sel_bool else -999)
        self.out.fillBranch('SeldLep1_eta_HF_typ0', info['0'][1].Eta() if sel_bool else -999)
        self.out.fillBranch('SeldLep1_phi_HF_typ0', phicorrection(info['0'][1].Phi(),leptons[0].pdgId) if sel_bool else -999 )
        self.out.fillBranch('SeldLep1_pt_HF_typ2',  info['1'][1].Pt() if sel_bool else -999)
        self.out.fillBranch('SeldLep1_eta_HF_typ2', info['1'][1].Eta() if sel_bool else -999)
        self.out.fillBranch('SeldLep1_phi_HF_typ2', phicorrection(info['1'][1].Phi(),leptons[0].pdgId) if sel_bool else -999 )
        
        for j in range(self.nfjets):
            for var in 'pt,eta,phi,mass,hadronFlavour,partonFlavour'.split(','):
                self.out.fillBranch('SelGak8Jet%d_%s'%(j+1,var),getattr(fatJets[j],var) if sel_bool else -999)
            #print "done filling jet branches in the loop"
        self.out.fillBranch('SelGak8Jet1_pt_HF_typ2'  ,info['1'][3].Pt() if sel_bool else -999)
        self.out.fillBranch('SelGak8Jet1_eta_HF_typ2' ,info['1'][3].Eta() if sel_bool else -999)
        self.out.fillBranch('SelGak8Jet1_mass_HF_typ2',info['1'][3].M() if sel_bool else -999)
        self.out.fillBranch('SelGak8Jet1_phi_HF_typ2' ,phicorrection(info['1'][3].Phi(),fatJets[0].partonFlavour) if sel_bool else -999)        
        self.out.fillBranch('SelGak8Jet1_pt_HF_typ0'  ,info['0'][3].Pt() if sel_bool else -999)
        self.out.fillBranch('SelGak8Jet1_eta_HF_typ0' ,info['0'][3].Eta() if sel_bool else -999)
        self.out.fillBranch('SelGak8Jet1_mass_HF_typ0',info['0'][3].M() if sel_bool else -999)
        self.out.fillBranch('SelGak8Jet1_phi_HF_typ0' ,phicorrection(info['0'][3].Phi(),fatJets[0].partonFlavour) if sel_bool else -999)
        
            #        if sel_bool:        #print "check this",info['1'][2].Pt() ," typ 0 =",info['0'][2].Pt()
       

        self.out.fillBranch('neutrino_pt_typ2' ,neu1.Pt() if sel_bool else -999)
        self.out.fillBranch('neutrino_eta_typ2',neu1.Eta() if sel_bool else -999)
        self.out.fillBranch('neutrino_pt_typ0' ,neu.Pt() if sel_bool else -999)
        self.out.fillBranch('neutrino_eta_typ0',neu.Eta() if sel_bool else -999)
        self.out.fillBranch('neutrino_pt_HF_typ2' ,info['1'][2].Pt() if sel_bool else -999)
        self.out.fillBranch('neutrino_eta_HF_typ2',info['1'][2].Eta() if sel_bool else -999)
        self.out.fillBranch('neutrino_pt_HF_typ0' ,info['0'][2].Pt() if sel_bool else -999)
        self.out.fillBranch('neutrino_eta_HF_typ0',info['0'][2].Eta() if sel_bool else -999)
        self.out.fillBranch('neutrino_phi_typ2',phicorrection(neu1.Phi(),neupdgId) if sel_bool else -999)
        self.out.fillBranch('neutrino_phi_typ0' ,phicorrection(neu.Phi(),neupdgId) if sel_bool else -999)
        self.out.fillBranch('neutrino_phi_HF_typ2',phicorrection(info['1'][2].Phi(),neupdgId) if sel_bool else -999)
        self.out.fillBranch('neutrino_phi_HF_typ0' ,phicorrection(info['0'][2].Phi(),neupdgId) if sel_bool else -999)
        #print"event filled"

        return True
