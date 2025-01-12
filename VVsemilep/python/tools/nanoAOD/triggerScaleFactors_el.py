from PhysicsTools.NanoAODTools.postprocessing.framework.eventloop import Module
from PhysicsTools.NanoAODTools.postprocessing.framework.datamodel import Collection 
from CMGTools.TTHAnalysis.tools.nanoAOD.friendVariableProducerTools import loadHisto
from copy import deepcopy
import ROOT
import os 

class triggerScaleFactors_el(Module):
    def __init__(self):
        self.triggerSF     = {}

        for year in '2016APV,2016,2017,2018'.split(','):
            #self.triggerSF['%s'%year]=loadHisto(os.environ['CMSSW_BASE'] + '/src/CMGTools/VVsemilep/data/triggerSF/triggerSF_%s_20200422.root'%year,'EGamma_SF2D')
            self.triggerSF['%s'%year]=loadHisto(os.environ['CMSSW_BASE'] + '/src/CMGTools/VVsemilep/data/triggerSF/singleElTrigEff_%s.root'%year,'EGamma_SF2D')


    def beginFile(self, inputFile, outputFile, inputTree, wrappedOutputTree):
        self.out = wrappedOutputTree
        for var in ',_up,_dn'.split(','):
            self.out.branch('triggerSF_el%s'%var,'F')

    def getTriggerEff(self, leps, year):
        
        for var in ',_up,_dn'.split(","):
            if len(leps)>0:
                if abs(leps[0].pdgId) == 11:
                    hist_1e=self.triggerSF['%s'%(year)]
                    thebin=hist_1e.FindBin(leps[0].eta, min(500.,leps[0].pt))
                    shift= 0 if var == '' else 1 if 'up' in var else -1 
                    self.out.fillBranch('triggerSF_el%s'%var, hist_1e.GetBinContent(thebin) + shift*hist_1e.GetBinError(thebin))
                else:
                    self.out.fillBranch('triggerSF_el%s'%var, 1)
            else:  self.out.fillBranch('triggerSF_el%s'%var, 1)
    def analyze(self, event):
        year = event.year
        # leptons
        all_leps = [l for l in Collection(event,"LepGood")]
        nFO = getattr(event,"nLepFO_Recl")
        chosen = getattr(event,"iLepFO_Recl")
        leps = [all_leps[chosen[i]] for i in xrange(nFO)]
        

        year=str(event.year)
        if event.suberaId == 0 and year == '2016':
            year='2016APV'
        
        # trigger efficiency
        self.getTriggerEff(leps, year)
        return True
