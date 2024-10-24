###tight selection and pT cut on leptons
from PhysicsTools.NanoAODTools.postprocessing.framework.eventloop import Module 
from PhysicsTools.NanoAODTools.postprocessing.framework.datamodel import Collection 
import ROOT 
import math
from math import sqrt, cos, sin
from array import array
from PhysicsTools.NanoAODTools.postprocessing.tools import deltaR, deltaPhi
from CMGTools.VVsemilep.tools.nanoAOD.vvsemilep_TreeForWJestimation import calcmassWV, pNetSFMD_WvsQCD, HEM
#_rootLeafType2rootBranchType = { 'UChar_t':'b', 'Char_t':'B', 'UInt_t':'i', 'Int_t':'I', 'Float_t':'F', 'Double_t':'D', 'ULong64_t':'l', 'Long64_t':'L', 'Bool_t':'O'}

from copy import deepcopy

def if3(cond, iftrue, iffalse):
    return iftrue if cond else iffalse

class input_WJestimation(Module):
    def __init__(self, isMC,lepMultiplicity, fjetMultiplicity, selection,massVar='sD',jecs=[]):
        self.lepMultiplicity=lepMultiplicity
        self.fjetMultiplicity=fjetMultiplicity
        self.selection=selection
        self.mvar=massVar
        self.isMC=isMC
        self.jecs=jecs
        self.pmet_vars=['pt','phi']
        self.shift=["Up","Down"]
        self.vars=['pt','eta','phi','mass','particleNetMD_Xqq','msoftdrop','particleNetMD_Xbb','particleNetMD_Xcc','particleNetMD_QCD','pNetWtagscore','pNetWtagSF']
        if self.isMC: 
            self.vars+=["pt_"+jec+sh for jec in self.jecs for sh in self.shift]
            self.vars+=["msoftdrop_"+jec+sh for jec in self.jecs for sh in self.shift]
        self.pmet_uncert=['JES','JER','Unclustered']
        if self.isMC:self.pmet_vars+=[pmetV+uncert+sh for pmetV in self.pmet_vars for uncert in self.pmet_uncert for sh in self.shift]
        pass
    def beginFile(self, inputFile, outputFile, inputTree, wrappedOutputTree):
        self.out = wrappedOutputTree
        for var in 'pt,eta,phi,pdgId,tightId'.split(','):
            for l in range(self.lepMultiplicity):
                self.out.branch('Lep%d_%s'%(l+1,var),'F')


        for var in self.vars: #'pt,eta,phi,mass,particleNetMD_Xqq,msoftdrop,particleNetMD_Xbb,particleNetMD_Xcc,particleNetMD_QCD,pNetWtagscore,pNetWtagSF'.split(','): 
            for j in range(self.fjetMultiplicity):
                self.out.branch('Selak8Jet%d_%s'%(j+1,var), 'F')
        for var in self.pmet_vars:
            self.out.branch('pmet_%s'%(var), 'F')
        self.out.branch('nFj','I')
        #for jec in self.jecs:
        #    for sh in self.shift:
        #         self.out.branch('nFj_%s%s'%(jec,sh),'I')
        #         self.out.branch('nBJetMedium30_%s%s'%(jec,sh),'I')
        self.out.branch('event', 'L')
        self.out.branch('nLep','I')
        self.out.branch('nLepFO','I')
        self.out.branch('nLepTight','I')
        self.out.branch("Top_pTrw","F")
        self.out.branch('event_presel', 'L')
        self.out.branch('nBJetMedium30', 'I')
        self.out.branch('pmet'       ,'F')
        #self.out.branch('pmet_phi'   ,'F')
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
    
    def analyze(self, event):
        isData = (event.run > 1) or not hasattr(event,"GenDressedLepton_pt")
        self.out.fillBranch('event',event.event)
        all_leps = [l for l in Collection(event,"LepGood")]
        nFO = getattr(event,"nLepFO_Recl")
        chosen = getattr(event,"iLepFO_Recl")
        leps = [all_leps[chosen[i]] for i in xrange(nFO)]
        jets = [j for j in Collection(event,"ak8%sMgt45"%self.mvar)]
        self.out.fillBranch('event_presel',event.event)        
        tot_sel=False;sel_i=False
        for isel in self.selection:
            if eval(isel):
                sel_i=True
            else: 
                sel_i=False;
                break;
        tot_sel= sel_i and len(leps) == self.lepMultiplicity  and  len(jets) > 0
        self.out.fillBranch('event_sel',tot_sel)        
        self.out.fillBranch('nFj',event.nFatJetSel_Recl if tot_sel else 0)
        
        #for jec in self.jecs:
        #    for sh in self.shift:
        #        self.out.fillBranch('nFj_%s%s'%(jec,sh),getattr(event,'nFatJet_%s%s_Recl'%(jec,sh))  if tot_sel else 0)
        #        self.out.fillBranch('nBJetMedium30_%s%s'%(jec,sh),getattr(event,'nBJetMedium30_%s%s_Recl'%(jec,sh))  if tot_sel else 999)

        self.out.fillBranch('nLep',len(leps) if tot_sel else 0)
        self.out.fillBranch('nLepFO',event.nLepFO_Recl  if tot_sel else 0)
        self.out.fillBranch('nLepTight',event.nLepTight_Recl  if tot_sel else 0)
        #if tot_sel: print "finally ",tot_sel,event.event
        for lep in range(self.lepMultiplicity):
            for var in 'pt,eta,phi,pdgId'.split(','):
                self.out.fillBranch('Lep%d_%s'%(lep+1,var), getattr(leps[lep],var) if tot_sel else -999.0)
            self.out.fillBranch('Lep%d_tightId'%(lep+1), getattr(leps[lep],"isLepTight_Recl") if tot_sel else 0)
        for jet in range(self.fjetMultiplicity): 
            for var in self.vars: #'pt,eta,phi,mass,msoftdrop,particleNetMD_Xqq,particleNetMD_Xbb,particleNetMD_Xcc,particleNetMD_QCD,pNetWtagscore'.split(','): 
                if "pNetWtagSF" in var: 
                    continue
                else:
                    self.out.fillBranch('Selak8Jet%d_%s'%(jet+1,var), getattr(jets[jet],var) if tot_sel else -999.0)
            #if tot_sel:print event.event,getattr(jets[jet],"pt"),getattr(jets[jet],"eta"),getattr(jets[jet],"msoftdrop")
            pnetsf=1.0;
            if tot_sel:
                pnetsf=pNetSFMD_WvsQCD(getattr(jets[jet],'pt'),event.year,event.suberaId) if not isData else 1.0
            #print "event \t",event.event,"\t pNetWscore \t",pNetWscore
            self.out.fillBranch('Selak8Jet%d_pNetWtagSF'%(jet+1),pnetsf)
        for i in self.pmet_vars:
            self.out.fillBranch('pmet_%s'%i,getattr(event,'PuppiMET_%s'%i) if tot_sel else -999.0)
        self.out.fillBranch('mWV',calcmassWV(leps[0],jets[0],event.PuppiMET_pt,event.PuppiMET_phi) if tot_sel else -999.0)
        self.out.fillBranch('pmet',event.PuppiMET_pt if tot_sel else -999.0)
        #       self.out.fillBranch('pmet_phi',event.PuppiMET_phi if tot_sel else -999.0)
        self.out.fillBranch('trigger1e',event.Trigger_1e if tot_sel else 0)
        self.out.fillBranch('trigger1m',event.Trigger_1m if tot_sel else 0)
        self.out.fillBranch('nBJetMedium30',event.nBJetMedium30_Recl if tot_sel else -999)
                
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
        hemwt=HEM(event.year,leps[0],jets[0],event.run,isData) if tot_sel else 0.0
        #print hemwt, tot_sel
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




