from PhysicsTools.NanoAODTools.postprocessing.framework.eventloop import Module 
from PhysicsTools.NanoAODTools.postprocessing.framework.datamodel import Collection 
import ROOT 

from math import sqrt, cos, sin
from PhysicsTools.NanoAODTools.postprocessing.tools import deltaR, deltaPhi
#_rootLeafType2rootBranchType = { 'UChar_t':'b', 'Char_t':'B', 'UInt_t':'i', 'Int_t':'I', 'Float_t':'F', 'Double_t':'D', 'ULong64_t':'l', 'Long64_t':'L', 'Bool_t':'O'}

from copy import deepcopy

def if3(cond, iftrue, iffalse):
    return iftrue if cond else iffalse

class vvsemilep_TreeForWJestimation(Module):
    def __init__(self, lepMultiplicity, selection,finalstate='onelep'):
        self.lepMultiplicity=lepMultiplicity
        self.selection=selection
        self.finalstate=finalstate
        pass
    def beginFile(self, inputFile, outputFile, inputTree, wrappedOutputTree):
        self.out = wrappedOutputTree
        for var in 'pt,eta,phi,pdgId'.split(','):
            for l in range(self.lepMultiplicity):
                self.out.branch('Lep%d_%s'%(l+1,var),'F')
        
        self.out.branch('nSelak8Jets'  ,'I')
        for var in 'pt,eta,phi,mass,msoftdrop,particleNet_mass,particleNetMD_Xqq,particleNetMD_Xbb,particleNetMD_Xcc,particleNetMD_QCD,pNetWtagscore,pNetZtagscore,pNetWtagSF'.split(','):
            self.out.branch('Selak8Jet_%s'%var, 'F', 10, 'nSelak8Jets')

        self.out.branch('event', 'I')
        self.out.branch('nBJetMedium30', 'I')
        self.out.branch('pmet'       ,'F')
        self.out.branch('pmet_phi'   ,'F')
        self.out.branch('evt_wt'       ,'F') #pu*prefiring*prescale*hem
        self.out.branch('genwt'   ,'F')
        #self.out.branch('genSumw'   ,'F')
        self.out.branch('xsec'   ,'F')
        self.out.branch('lepSF'   ,'F') 
        self.out.branch('mWV',"F")
        self.out.branch('trigger2l','I')
        self.out.branch('trigger1e','I')
        self.out.branch('trigger1m','I')
    
    def beginJob(self):
        pass
    def endJob(self):
        pass
    def endFile(self, inputFile, outputFile, inputTree, wrappedOutputTree):
        pass
    

    def calcmassWV(self,l1,fjet,metpt,metphi):
        from ROOT.heppy import METzCalculator_Run2
        
        NeutrinoPz = METzCalculator_Run2()
        met=ROOT.TLorentzVector(0.0,0.0,0.0,0.0);
        metV=ROOT.TLorentzVector(0.0,0.0,0.0,0.0);
        lepton1=ROOT.TLorentzVector(0.0,0.0,0.0,0.0);
        fatjet1=ROOT.TLorentzVector(0.0,0.0,0.0,0.0);
        mWV=ROOT.TLorentzVector(0.0,0.0,0.0,0.0);
        met.SetPtEtaPhiM(metpt,0.,metphi,0.);
        lepton1.SetPtEtaPhiM(l1.pt,l1.eta,l1.phi,l1.mass);
        fatjet1.SetPtEtaPhiM(fjet.pt,fjet.eta,fjet.phi,fjet.particleNet_mass);
        NeutrinoPz.SetMET(met);
        NeutrinoPz.SetLepton(lepton1);
        NeutrinoPz.SetLeptonType(l1.pdgId);
        nu_pz=NeutrinoPz.Calculate(0)
        metV.SetPxPyPzE(metpt*cos(metphi), metpt*sin(metphi),nu_pz,sqrt(metpt*metpt+nu_pz*nu_pz));
        mWV=lepton1+fatjet1+metV;
        massWV=mWV.M();
        return massWV

    def pNetSFMD_WvsQCD(self,pt,year,suberaid,WP=1.0,var=0):
        yearString= str(year)+if3(year == 2016 and suberaid == 0,"APV","")
        if (yearString == "2018"):
            if(pt >= 200 and pt < 300):
                return if3(WP == 0.5,0.81*(1 + var*0.03),if3(WP == 1.0,0.87*(1 + var*0.02),if3(var > 0,0.92*(1 + var*0.03),0.92*(1 + var*0.02))))
            elif(pt >= 300 and pt < 400):
                return if3(WP == 0.5,0.81*(1 + var*0.02),if3(WP == 1.0,0.86*(1 + var*0.02),0.92*(1 + var*0.02)))
            else:
                return if3(WP == 0.5,0.77*(1 + var*0.04), if3(WP == 1.0,0.82*(1 + var*0.04),0.87*(1 + var*0.04)))
        elif (yearString == "2017"):
            if(pt >= 200 and pt < 300):
                return if3(WP == 0.5,0.85*(1 + var*0.03),if3(WP == 1.0,0.91*(1 + var*0.02),0.96*(1 + var*0.03)))
            elif(pt >= 300 and pt < 400):
                return if3(WP == 0.5,0.85*(1 + var*0.03),if3(WP == 1.0,0.90*(1 + var*0.02),if3(var > 0,0.95*(1 + var*0.03),0.95*(1 + var*0.02))))
            else: return if3(WP == 0.5,0.86*(1 + var*0.05),if3(WP == 1.0,if3(var > 0, 0.89*(1 + var*0.05),0.89*(1 + var*0.04)),0.98*(1 + var*0.05)))
        elif (yearString == "2016APV"):
            if(pt >= 200 and pt < 300):
                return if3(WP == 0.5,0.85*(1 + var*0.03),if3(WP == 1.0,0.90*(1 + var*0.03),0.90*(1 + var*0.02)))
            elif(pt >= 300 and pt < 400):
                return if3(WP == 0.5,0.86*(1 + var*0.04),if3(WP == 1.0,0.87*(1 + var*0.04),0.94*(1 + var*0.04)))
            else:
                return if3(WP == 0.5,0.86*(1 + var*0.08),if3(WP == 1.0,if3(var > 0,0.92*(1 + var*0.08),0.92*(1 + var*0.07)),0.94*(1 + var*0.07)))
        else:
            if(pt >= 200 and pt < 300):
                return if3(WP == 0.5,0.85*(1 + var*0.04),if3(WP == 1.0,if3(var > 0,0.89*(1 + var*0.04),0.89*(1 + var*0.03)),0.95*(1 + var*0.04)))
            elif(pt >= 300 and pt < 400):
                return if3(WP == 0.5,0.83*(1 + var*0.04),if3(WP == 1.0,0.86*(1 + var*0.04),0.91*(1 + var*0.04)))
            else: return if3(WP == 0.5,if3(var > 0,0.69*(1 + var*0.07),0.69*(1 + var*0.06)),if3(WP == 1.0,0.73*(1 + var*0.07),0.84*(1 + var*0.07)))

    def HEM(self,year,lep,jet,run,isData):
        HEM_eta_min =  -3.2;  HEM_eta_max = -1.3;
        HEM_phi_min= -1.57;  HEM_phi_max= -0.87;
        weight=1.0;  
        if year==2018:
            vetoHEM=False;vetofj=False;vetoel=False;
            vetofj = (jet.eta < HEM_eta_max and jet.eta > HEM_eta_min and jet.phi < HEM_phi_max and jet.phi > HEM_phi_min)
            vetoel = (abs(lep.pdgId) == 11 and lep.eta > -2.5 and lep.eta < -1.479 and lep.phi < HEM_phi_max and lep.phi > HEM_phi_min)
            vetoHEM = vetofj or vetoel;
            if (vetoHEM):
                if (isData):
                    if(run > 319077): 	weight=0;    
                    else:	weight=1.0;
                else:      weight=0.35; 
            else:	weight=1.0; 
        else: weight=1.0
        return weight;

    def analyze(self, event):
        isData = (event.run > 1) or not hasattr(event,"GenDressedLepton_pt")
        self.out.fillBranch('event',event.event)
        all_leps = [l for l in Collection(event,"LepGood")]
        nFO = getattr(event,"nLepFO_Recl")
        chosen = getattr(event,"iLepFO_Recl")
        leps = [all_leps[chosen[i]] for i in xrange(nFO)]
        jets = [j for j in Collection(event,"ak8pNMgt40")]
        if len(leps) < self.lepMultiplicity: return False
        if len(jets) < 1: return False
        
        for sel in self.selection: 
            if not eval(sel): return False
        for lep in range(self.lepMultiplicity):
            for var in 'pt,eta,phi,pdgId'.split(','):
                self.out.fillBranch('Lep%d_%s'%(lep+1,var), getattr(leps[lep],var))
        for var in 'pt,eta,phi,mass,msoftdrop,particleNet_mass,particleNetMD_Xqq,particleNetMD_Xbb,particleNetMD_Xcc,particleNetMD_QCD'.split(','): #,pNetWtagscore
            jetVar=[]
            for j in jets:
                jetVar.append(getattr(j,var))

            self.out.fillBranch('Selak8Jet_%s'%var, jetVar)
        pNetZscore=[];        pNetWscore=[];pnetsf=[];
        for j in jets:

            score=(getattr(j,'particleNetMD_Xcc')+getattr(j,'particleNetMD_Xqq'))/(getattr(j,'particleNetMD_Xcc')+getattr(j,'particleNetMD_Xqq')+getattr(j,'particleNetMD_QCD'))
            pNetWscore.append(score)
            score=(getattr(j,'particleNetMD_Xcc')+getattr(j,'particleNetMD_Xbb')+getattr(j,'particleNetMD_Xqq'))/(getattr(j,'particleNetMD_Xcc')+getattr(j,'particleNetMD_Xqq')+getattr(j,'particleNetMD_QCD')+getattr(j,'particleNetMD_Xbb'))
            pNetZscore.append(score)
            pnetsf.append(self.pNetSFMD_WvsQCD(j.pt,event.year,event.suberaId) if not isData else 1.0)

        self.out.fillBranch('Selak8Jet_pNetWtagSF',pnetsf)
        self.out.fillBranch('Selak8Jet_pNetWtagscore', pNetWscore)
        self.out.fillBranch('Selak8Jet_pNetZtagscore', pNetZscore)
        self.out.fillBranch('mWV',self.calcmassWV(leps[0],jets[0],event.PuppiMET_pt,event.PuppiMET_phi))
        self.out.fillBranch('pmet',event.PuppiMET_pt)
        self.out.fillBranch('pmet_phi',event.PuppiMET_phi)
        self.out.fillBranch('trigger2l',event.Trigger_2l)
        self.out.fillBranch('trigger1e',event.Trigger_1e)
        self.out.fillBranch('trigger1m',event.Trigger_1m)
        self.out.fillBranch('nBJetMedium30',event.nBJetMedium30_Recl)
        hemwt=self.HEM(event.year,leps[0],jets[0],event.run,isData)
        #print hemwt,event.prescaleFromSkim,event.L1PreFiringWeight_Nom,event.puWeight
        eventWt=hemwt * (event.prescaleFromSkim if isData else event.L1PreFiringWeight_Nom*event.puWeight*event.prescaleFromSkim)
        self.out.fillBranch('evt_wt',eventWt) #pu*prefiring*prescale*hem
        self.out.fillBranch('genwt',event.genWeight if not isData else 1.0  )
        #self.out.fillBranch('genSumw',event.genEventSumw if not isData else 1.0   )
        self.out.fillBranch('xsec',event.xsec if not isData else 1.0  )
        self.out.fillBranch('lepSF',event.lepsf if not isData else 1.0  ) 
        return True


###to add triggger+met selection based on lep pdgId
##HEM
##bVeto ?
##event weights
##genWeight
##genEventSumw
##xsec
##pu*prefiring*prescale*hemwt
##pnetscore*lepSF
##trigger SF