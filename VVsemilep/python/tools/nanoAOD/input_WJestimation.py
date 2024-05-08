###tight selection and pT cut on leptons
from PhysicsTools.NanoAODTools.postprocessing.framework.eventloop import Module 
from PhysicsTools.NanoAODTools.postprocessing.framework.datamodel import Collection 
import ROOT 
import math
from math import sqrt, cos, sin
from array import array
from PhysicsTools.NanoAODTools.postprocessing.tools import deltaR, deltaPhi
#_rootLeafType2rootBranchType = { 'UChar_t':'b', 'Char_t':'B', 'UInt_t':'i', 'Int_t':'I', 'Float_t':'F', 'Double_t':'D', 'ULong64_t':'l', 'Long64_t':'L', 'Bool_t':'O'}

from copy import deepcopy

def if3(cond, iftrue, iffalse):
    return iftrue if cond else iffalse

class input_WJestimation(Module):
    def __init__(self, lepMultiplicity, fjetMultiplicity, selection,mvar='sD'):
        self.lepMultiplicity=lepMultiplicity
        self.fjetMultiplicity=fjetMultiplicity
        self.selection=selection
        self.mvar=mvar
        pass
    def beginFile(self, inputFile, outputFile, inputTree, wrappedOutputTree):
        self.out = wrappedOutputTree
        for var in 'pt,eta,phi,pdgId,tightId'.split(','):
            for l in range(self.lepMultiplicity):
                self.out.branch('Lep%d_%s'%(l+1,var),'F')


        for var in 'pt,eta,phi,mass,particleNetMD_Xqq,msoftdrop,particleNetMD_Xbb,particleNetMD_Xcc,particleNetMD_QCD,pNetWtagscore,pNetWtagSF'.split(','): #msoftdrop,particleNet_mass,
            for j in range(self.fjetMultiplicity):
                self.out.branch('Selak8Jet%d_%s'%(j+1,var), 'F')
        for nsel in self.selection:
            self.out.branch('event_sel%d'%self.selection.index(nsel), 'L')
        self.out.branch('event', 'L')
        self.out.branch('nFj','I')
        self.out.branch('nLep','I')
        self.out.branch('nLepFO','I')
        self.out.branch('nLepTight','I')
        self.out.branch("Top_pTrw","F")
        self.out.branch('event_presel', 'L')
        self.out.branch('nBJetMedium30', 'I')
        self.out.branch('pmet'       ,'F')
        self.out.branch('pmet_phi'   ,'F')
        self.out.branch('evt_wt'       ,'F') #pu*prefiring*prescale*hem
        self.out.branch('pu_wt'       ,'F') #pu
        self.out.branch('prefiring_wt'       ,'F') #prefiring
        self.out.branch('hem_wt'       ,'F') #pu*prefiring*prescale*hem
        self.out.branch('prescale_wt'       ,'F') #pu*prefiring*prescale*hem
        self.out.branch('genwt'   ,'F')
        self.out.branch('event_sel', 'O')
        #self.out.branch('genSumw'   ,'F')
        self.out.branch('xsec'   ,'F')
        self.out.branch('lepSF'   ,'F') 
        self.out.branch('mWV',"F")
        self.out.branch('trigger1e','I')
        self.out.branch('trigger1m','I')

        self.out.branch('dR_fjlep','F')
        self.out.branch('dphi_fjlep','F')
        self.out.branch('dphi_fjmet','F')
        self.out.branch('pTWlep','F');
        self.out.branch('naGC_wt','I')
        self.out.branch('aGC_wt',"F",lenVar="naGC_wt")
    def beginJob(self):
        pass
    def endJob(self):
        pass
    def endFile(self, inputFile, outputFile, inputTree, wrappedOutputTree):
        pass
    

    def calcmassWV(self,l1,fjet,metpt,metphi):
        from ROOT.heppy import METzCalculator
        
        NeutrinoPz = METzCalculator()
        met=ROOT.TLorentzVector(0.0,0.0,0.0,0.0);
        metV=ROOT.TLorentzVector(0.0,0.0,0.0,0.0);
        lepton1=ROOT.TLorentzVector(0.0,0.0,0.0,0.0);
        fatjet1=ROOT.TLorentzVector(0.0,0.0,0.0,0.0);
        mWV=ROOT.TLorentzVector(0.0,0.0,0.0,0.0);
        met.SetPtEtaPhiM(metpt,0.,metphi,0.);
        lepton1.SetPtEtaPhiM(l1.pt,l1.eta,l1.phi,l1.mass);
        fatjet1.SetPtEtaPhiM(fjet.pt,fjet.eta,fjet.phi,fjet.msoftdrop); #particleNet_mass);
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
        if run > 1: isData=True;
        if year==2018:
            vetoHEM=False;vetofj=False;vetoel=False;
            vetofj = (jet.eta < HEM_eta_max and jet.eta > HEM_eta_min and jet.phi < HEM_phi_max and jet.phi > HEM_phi_min)
            vetoel = (abs(lep.pdgId) == 11 and lep.eta > -2.5 and lep.eta < -1.479 and lep.phi < HEM_phi_max and lep.phi > HEM_phi_min)
            vetoHEM = vetofj or vetoel;
            if (vetoHEM):
                if (isData):
                    if(run >= 319077): 	weight=0;    
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
        jets = [j for j in Collection(event,"ak8%sMgt45"%self.mvar)]
        self.out.fillBranch('event_presel',event.event)        
        tot_sel=False;sel=False

        for isel in self.selection:
            if eval(isel):
                sel=True
                #print 'passed %s'%isel
                self.out.fillBranch('event_sel%d'%self.selection.index(isel),1)        
            else: 
                sel=False
                self.out.fillBranch('event_sel%d'%self.selection.index(isel),0)        
                #print 'failed ',isel,event.event
                break;
        tot_sel= sel and len(leps) == 1 and  len(jets) > 0
        self.out.fillBranch('event_sel',tot_sel)        
        self.out.fillBranch('nFj',event.nFatJetSel_Recl)
        self.out.fillBranch('nLep',len(leps))
        self.out.fillBranch('nLepFO',event.nLepFO_Recl)
        self.out.fillBranch('nLepTight',event.nLepTight_Recl)
        #if tot_sel: print "finally ",tot_sel,event.event
        for lep in range(self.lepMultiplicity):
            for var in 'pt,eta,phi,pdgId'.split(','):
                self.out.fillBranch('Lep%d_%s'%(lep+1,var), getattr(leps[lep],var) if tot_sel else -999.0)
            self.out.fillBranch('Lep%d_tightId'%(lep+1), getattr(leps[lep],"isLepTight_Recl") if tot_sel else 0)
        for jet in range(self.fjetMultiplicity): 
            for var in 'pt,eta,phi,mass,msoftdrop,particleNetMD_Xqq,particleNetMD_Xbb,particleNetMD_Xcc,particleNetMD_QCD'.split(','): #,pNetWtagscore#,msoftdrop particleNet_mass,
                self.out.fillBranch('Selak8Jet%d_%s'%(jet+1,var), getattr(jets[jet],var) if tot_sel else -999.0)
            pNetWscore=0.0;pnetsf=1.0;
            if tot_sel:
                pNetWscore=(getattr(jets[jet],'particleNetMD_Xcc')+getattr(jets[jet],'particleNetMD_Xqq'))/(getattr(jets[jet],'particleNetMD_Xcc')+getattr(jets[jet],'particleNetMD_Xqq')+getattr(jets[jet],'particleNetMD_QCD'))
                pnetsf=self.pNetSFMD_WvsQCD(getattr(jets[jet],'pt'),event.year,event.suberaId) if not isData else 1.0
            #print "event \t",event.event,"\t pNetWscore \t",pNetWscore
            self.out.fillBranch('Selak8Jet%d_pNetWtagSF'%(jet+1),pnetsf)
            self.out.fillBranch('Selak8Jet%d_pNetWtagscore'%(jet+1), pNetWscore)
                
        self.out.fillBranch('mWV',self.calcmassWV(leps[0],jets[0],event.PuppiMET_pt,event.PuppiMET_phi) if tot_sel else -999.0)
        self.out.fillBranch('pmet',event.PuppiMET_pt if tot_sel else -999.0)
        self.out.fillBranch('pmet_phi',event.PuppiMET_phi if tot_sel else -999.0)
        self.out.fillBranch('trigger1e',event.Trigger_1e if tot_sel else 0)
        self.out.fillBranch('trigger1m',event.Trigger_1m if tot_sel else 0)
        self.out.fillBranch('nBJetMedium30',event.nBJetMedium30_Recl if tot_sel else 999)
                
        self.out.fillBranch('dR_fjlep',deltaR(leps[0].eta,leps[0].phi,jets[0].eta,jets[0].phi) if tot_sel else 999.0)
        self.out.fillBranch('dphi_fjlep',abs(deltaPhi(leps[0].phi,jets[0].phi)) if tot_sel else -999.0 )
        self.out.fillBranch('dphi_fjmet',abs(deltaPhi(event.PuppiMET_phi,jets[0].phi)) if tot_sel else -999.0 )
        pmet=ROOT.TLorentzVector(0.0,0.0,0.0,0.0);
        lep1=ROOT.TLorentzVector(0.0,0.0,0.0,0.0);
        lmet=ROOT.TLorentzVector(0.0,0.0,0.0,0.0);
        if tot_sel:
            pmet.SetPtEtaPhiM(event.PuppiMET_pt,0.,event.PuppiMET_phi,0.);
            lep1.SetPtEtaPhiM(leps[0].pt,leps[0].eta,leps[0].phi,0.); #leps[0].mass);
        lmet=pmet+lep1
        self.out.fillBranch('pTWlep',lmet.Pt() if tot_sel else -999.0 )
        
        hemwt=self.HEM(event.year,leps[0],jets[0],event.run,isData) if tot_sel else 0.0
        #print hemwt,event.prescaleFromSkim,event.L1PreFiringWeight_Nom,event.puWeight
        eventWt=hemwt * (event.prescaleFromSkim if isData else event.L1PreFiringWeight_Nom*event.puWeight*event.prescaleFromSkim)
        self.out.fillBranch('evt_wt',eventWt if tot_sel else 0 ) #pu*prefiring*prescale*hem
        self.out.fillBranch('hem_wt',hemwt if tot_sel else 0.0 )
        self.out.fillBranch('pu_wt',1.0 if isData else event.puWeight)
        self.out.fillBranch('prefiring_wt', event.L1PreFiringWeight_Nom)
        self.out.fillBranch('prescale_wt',event.prescaleFromSkim)
        self.out.fillBranch('genwt',event.genWeight if not isData else 1.0  )
        #self.out.fillBranch('genSumw',event.genEventSumw if not isData else 1.0   )
        self.out.fillBranch('xsec',event.xsec if not isData else 1.0  )
        self.out.fillBranch('lepSF',event.lepsf if not isData and tot_sel else 1.0  ) 
        max_n=event.nLHEReweightingWeight if hasattr(event,"nLHEReweightingWeight") and tot_sel else 150 
        self.out.fillBranch('naGC_wt', event.nLHEReweightingWeight if hasattr(event,"nLHEReweightingWeight") and tot_sel else max_n)
        tmp=[1.0]*max_n
        if hasattr(event,"nLHEReweightingWeight"):            
            for j in range(max_n):
                #print event.LHEReweightingWeight[j]
                tmp[j]=event.LHEReweightingWeight[j]
        self.out.fillBranch('aGC_wt', tmp)

        topsf=1.0;
        if not isData:
            tops=[];
            genparticles=Collection(event,"GenPart")
            foundt=False;foundtbar=False; tgenPt=0.0; AtopPt=0.0;
            for iGen in genparticles:
                if abs(iGen.pdgId) == 6:
                    lastcopy=ROOT.TMath.Odd(iGen.statusFlags/(1<<13))
                    if iGen.pdgId == 6 and lastcopy:
                        topPt=iGen.pt;foundt=True;tops.append(iGen);
                    if iGen.pdgId == -6 and lastcopy:
                        AtopPt=iGen.pt;foundtbar=True;tops.append(iGen);
                else: continue
                if len(tops)==2 and foundt and foundtbar:
                    topsf=(math.sqrt(math.exp(0.0615 - 0.0005 * topPt) * math.exp(0.0615 - 0.0005 * AtopPt)))
        self.out.fillBranch('Top_pTrw',topsf if tot_sel else -999.0 )    

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
