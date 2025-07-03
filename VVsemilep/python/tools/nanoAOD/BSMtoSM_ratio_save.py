from PhysicsTools.NanoAODTools.postprocessing.framework.eventloop import Module
from PhysicsTools.NanoAODTools.postprocessing.framework.datamodel import Collection 
from CMGTools.TTHAnalysis.tools.nanoAOD.friendVariableProducerTools import loadHisto
from copy import deepcopy
import ROOT
import os 
import math 
from math import sqrt, cos, sin
#from array import array
#from PhysicsTools.NanoAODTools.postprocessing.tools import deltaR, deltaPhi

def calcmassWV(l1,fjet,metpt,metphi):
    from ROOT.heppy import METzCalculator
        
    NeutrinoPz = METzCalculator()
    met=ROOT.TLorentzVector(0.0,0.0,0.0,0.0);
    metV=ROOT.TLorentzVector(0.0,0.0,0.0,0.0);
    lepton1=ROOT.TLorentzVector(0.0,0.0,0.0,0.0);
    fatjet1=ROOT.TLorentzVector(0.0,0.0,0.0,0.0);
    mWV=ROOT.TLorentzVector(0.0,0.0,0.0,0.0);
    met.SetPtEtaPhiM(metpt,0.,metphi,0.);
    lepton1.SetPtEtaPhiM(l1.pt,l1.eta,l1.phi,0);
    fatjet1.SetPtEtaPhiM(fjet.pt,fjet.eta,fjet.phi,fjet.mass); #particleNet_mass);
    NeutrinoPz.SetMET(met);
    NeutrinoPz.SetLepton(lepton1);
    NeutrinoPz.SetLeptonType(abs(l1.pdgId));
    nu_pz=NeutrinoPz.Calculate(0)
    metV.SetPxPyPzE(metpt*cos(metphi), metpt*sin(metphi),nu_pz,sqrt(metpt*metpt+nu_pz*nu_pz));
    mWV=lepton1+fatjet1+metV;
    massWV=mWV.M();
    return massWV


class BSMtoSM_ratio_save(Module):
    def __init__(self):
        self.ratio     = {}

        for year in '2017,2018,2016APV,2016,fullRun2'.split(','): #
            for procs in ['WW','WZ','WV']:
                self.ratio['%s_eft_%s'%(procs,year)]=loadHisto(os.environ['CMSSW_BASE'] + '/src/CMGTools/VVsemilep/data/BSMtoSMratios/res_%s_mWV_logy_pol1.root'%year,'ratio_mWV_logy_%s_eft_HTbinned_%s'%(procs,year))
                self.ratio['%s_smeft_%s'%(procs,year)]=loadHisto(os.environ['CMSSW_BASE'] + '/src/CMGTools/VVsemilep/data/BSMtoSMratios/res_%s_mWV_logy_pol1.root'%year,'ratio_mWV_logy_%s_smeftprod_%s'%(procs,year))
                self.ratio['gen_%s_eft_%s'%(procs,year)]=loadHisto(os.environ['CMSSW_BASE'] + '/src/CMGTools/VVsemilep/data/BSMtoSMratios/res_%s_GenmWV_typ0_pmet_boosted_pol1_gen.root'%year,'ratio_GenmWV_typ0_pmet_boosted_%s_eft_HTbinned_%s'%(procs,year))
                self.ratio['gen_%s_smeft_%s'%(procs,year)]=loadHisto(os.environ['CMSSW_BASE'] + '/src/CMGTools/VVsemilep/data/BSMtoSMratios/res_%s_GenmWV_typ0_pmet_boosted_pol1_gen.root'%year,'ratio_GenmWV_typ0_pmet_boosted_%s_smeftprod_%s'%(procs,year))




    def beginFile(self, inputFile, outputFile, inputTree, wrappedOutputTree):
        self.out = wrappedOutputTree

        for bsm in ['eft','smeft']:
            for sm in ['WW','WZ','gen_WW','gen_WZ','gen_WV','WV']:
                 for var in ['']: #'_up','_dn','']:
                    for yr in ['','_FR2']:
                        self.out.branch('corr_%s_%s%s%s'%(sm,bsm,yr,var),'F')
                        self.out.branch('pol1_corr_%s_%s%s%s'%(sm,bsm,yr,var),'F')
#                        if len(var) > 0:
#                            self.out.branch('pol1_corr_%s_%s%s_param1%s'%(sm,bsm,yr,var),'F')
#                            self.out.branch('pol1_corr_%s_%s%s_param2%s'%(sm,bsm,yr,var),'F')



        
    def getCorr(self, mWV,mWV_gen,year,pf):

        for sm in ['WW','WZ','gen_WW','gen_WZ','WV','gen_WV']:
            for bsm in 'eft,smeft'.split(","):
                
                h1=self.ratio['%s_%s_%s'%(sm,bsm,year)]
                ff="pol1" #if  bsm=="smeft" else "pol1"
                constant=h1.GetFunction(ff).GetParameter(0);
                constant_err=h1.GetFunction(ff).GetParError(0);
                slope=h1.GetFunction(ff).GetParameter(1);
                slope_err=h1.GetFunction(ff).GetParError(1);
                mWV_N=1.0;
                mWV_up=1.0; mWV_dn=1.0; mWV_1up=1.0; mWV_1dn=1.0; mWV_2up=1.0; mWV_2dn=1.0;

                if "gen" in sm:
                    MassWV=mWV_gen
                else:
                    MassWV=mWV
                mWV_N=constant + slope*MassWV #p[0] + p[1]*x 

                ratio=h1.GetBinContent(h1.FindFixBin(mWV));
                #ratio_error=h1.GetBinError(h1.FindFixBin(mWV));
                #ratio_up=ratio+ratio_error
                #ratio_dn=ratio-ratio_error

 #               mWV_up=(constant+constant_err)+ ((slope+slope_err)*MassWV)
 #               mWV_dn=(constant+constant_err)+ ((slope-slope_err)*MassWV)
 #               mWV_1up=(constant+constant_err)+(slope*MassWV)
 #               mWV_1dn=(constant-constant_err)+(slope*MassWV)
 #               mWV_2up=constant+((slope+slope_err)*MassWV)
 #               mWV_2dn=constant+((slope-slope_err)*MassWV)
                
                #print(sm,bsm,"\t correction\t",mWV_N,"\t var \t",mWV_up,mWV_dn)
#                self.out.fillBranch('corr_%s_%s%s_up'%(sm,bsm,pf), ratio_up if mWV !=-999 else -999)
 #               self.out.fillBranch('corr_%s_%s%s_dn'%(sm,bsm,pf), ratio_dn if mWV !=-999 else -999)

                self.out.fillBranch('corr_%s_%s%s'%(sm,bsm,pf), ratio if mWV !=-999 else -999)
                self.out.fillBranch('%s_corr_%s_%s%s'%(ff,sm,bsm,pf), mWV_N if mWV !=-999 else -999)
#                self.out.fillBranch('%s_corr_%s_%s%s_up'%(ff,sm,bsm,pf), mWV_up if mWV !=-999 else -999)
#                self.out.fillBranch('%s_corr_%s_%s%s_dn'%(ff,sm,bsm,pf), mWV_dn if mWV !=-999 else -999)
#                self.out.fillBranch('%s_corr_%s_%s%s_param1_up'%(ff,sm,bsm,pf), mWV_1up if mWV !=-999 else -999)
#                self.out.fillBranch('%s_corr_%s_%s%s_param1_dn'%(ff,sm,bsm,pf), mWV_1dn if mWV !=-999 else -999)
#                self.out.fillBranch('%s_corr_%s_%s%s_param2_up'%(ff,sm,bsm,pf), mWV_2up if mWV !=-999 else -999)
#                self.out.fillBranch('%s_corr_%s_%s%s_param2_dn'%(ff,sm,bsm,pf), mWV_2dn if mWV !=-999 else -999)

                
    def analyze(self, event):
        year = event.year
        # leptons
        leps=[j for j in Collection(event,"GenDressedLepton")]
        fjets=[j for j in Collection(event,"GenJetAK8")]
        if len(leps) > 0 and len(fjets) > 0:
            mWV_gen=calcmassWV(leps[0],fjets[0],getattr(event,'GenMET_pt'),getattr(event,'GenMET_phi'))
            #print(mWV_gen,event.mWV)
        else: mWV_gen=0.0;
        year=str(event.year)
        if event.suberaId == 0 and year == '2016':
            year='2016APV'
            
        # get correction
        self.getCorr(event.mWV, mWV_gen,year,'')
        self.getCorr(event.mWV, mWV_gen,'fullRun2','_FR2')
        return True

