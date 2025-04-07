from PhysicsTools.NanoAODTools.postprocessing.framework.eventloop import Module
from PhysicsTools.NanoAODTools.postprocessing.framework.datamodel import Collection 
from CMGTools.TTHAnalysis.tools.nanoAOD.friendVariableProducerTools import loadHisto
from copy import deepcopy
import ROOT
import os 
import math 

class BSMtoSM_ratio_save(Module):
    def __init__(self):
        self.ratio     = {}

        for year in '2017,2018'.split(','): #2016APV,2016,
            #self.triggerSF['%s'%year]=loadHisto(os.environ['CMSSW_BASE'] + '/src/CMGTools/VVsemilep/data/triggerSF/triggerSF_%s_20200422.root'%year,'EGamma_SF2D')
            self.ratio['WW_eft_%s'%year]=loadHisto(os.environ['CMSSW_BASE'] + '/src/CMGTools/VVsemilep/data/BSMtoSMratios/res_%s_mWV_logy_expo.root'%year,'ratio_mWV_logy_WW_eft_%s'%year)
            self.ratio['WW_smeft_%s'%year]=loadHisto(os.environ['CMSSW_BASE'] + '/src/CMGTools/VVsemilep/data/BSMtoSMratios/res_%s_mWV_logy_expo.root'%year,'ratio_mWV_logy_WW_smeft_%s'%year)
            self.ratio['WZ_eft_%s'%year]=loadHisto(os.environ['CMSSW_BASE'] + '/src/CMGTools/VVsemilep/data/BSMtoSMratios/res_%s_mWV_logy_expo.root'%year,'ratio_mWV_logy_WZ_eft_%s'%year)
            self.ratio['WZ_smeft_%s'%year]=loadHisto(os.environ['CMSSW_BASE'] + '/src/CMGTools/VVsemilep/data/BSMtoSMratios/res_%s_mWV_logy_expo.root'%year,'ratio_mWV_logy_WZ_smeft_%s'%year)


    def beginFile(self, inputFile, outputFile, inputTree, wrappedOutputTree):
        self.out = wrappedOutputTree
        self.out.branch('corr_WW_eft','F')
        self.out.branch('corr_WW_eft_up','F')
        self.out.branch('corr_WW_eft_dn','F')
        self.out.branch('corr_WW_smeft','F')
        self.out.branch('corr_WW_smeft_up','F')
        self.out.branch('corr_WW_smeft_dn','F')
        self.out.branch('corr_WZ_eft','F')
        self.out.branch('corr_WZ_eft_up','F')
        self.out.branch('corr_WZ_eft_dn','F')
        self.out.branch('corr_WZ_smeft','F')
        self.out.branch('corr_WZ_smeft_up','F')
        self.out.branch('corr_WZ_smeft_dn','F')

        
    def getCorr(self, mWV,year):
        for sm in ["WW","WZ"]:
            for bsm in 'eft,smeft'.split(","):
                h1=self.ratio['%s_%s_%s'%(sm,bsm,year)]
                constant=h1.GetFunction("expo").GetParameter(0);
                constant_err=h1.GetFunction("expo").GetParError(0);
                slope=h1.GetFunction("expo").GetParameter(1);
                slope_err=h1.GetFunction("expo").GetParError(1);
                mWV_N=math.exp(constant+slope*mWV)
                mWV_up=math.exp((constant+constant_err) + (slope+slope_err)*mWV)
                mWV_dn=math.exp((constant-constant_err) + (slope-slope_err)*mWV)
                #print(sm,bsm,"\t correction\t",mWV_N,"\t var \t",mWV_up,mWV_dn)
                self.out.fillBranch('corr_%s_%s'%(sm,bsm), mWV_N if mWV !=-999 else -999)
                self.out.fillBranch('corr_%s_%s_up'%(sm,bsm), mWV_up if mWV !=-999 else -999)
                self.out.fillBranch('corr_%s_%s_dn'%(sm,bsm), mWV_dn if mWV !=-999 else -999)
    def analyze(self, event):
        year = event.year
        # leptons

        year=str(event.year)
        if event.suberaId == 0 and year == '2016':
            year='2016APV'
            
        # get correction
        self.getCorr(event.mWV, year)
        return True
