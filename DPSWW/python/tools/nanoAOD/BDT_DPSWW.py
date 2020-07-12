#from CMGTools.TTHAnalysis.treeReAnalyzer import *
from PhysicsTools.NanoAODTools.postprocessing.framework.eventloop import Module 
from PhysicsTools.NanoAODTools.postprocessing.framework.datamodel import Collection as Collection 
from CMGTools.TTHAnalysis.tools.nanoAOD.friendVariableProducerTools import writeOutput
from CMGTools.TTHAnalysis.tools.mvaTool import *
            
    

class BDT_DPSWW(Module):
    def __init__(self):
        self._MVAs = {}
        self._vars = [

            MVAVar("Lep1_conept",       func = lambda ev : ev.Lep1_conept ),
            MVAVar("Lep2_conept",       func = lambda ev : ev.Lep2_conept ),
            MVAVar("MET_pt",       func = lambda ev : ev.MET_pt),
            MVAVar("mt2",       func = lambda ev : ev.mt2),
            MVAVar("mtll",      func = lambda ev : ev.mtll), 
            MVAVar("mtl1met",   func = lambda ev : ev.mtl1met), 
            MVAVar("dphill",    func = lambda ev : ev.dphill),
            MVAVar("dphil2met", func = lambda ev : ev.dphil2met), 
            MVAVar("dphilll2",  func = lambda ev : ev.dphilll2), 
            MVAVar("Lep1_eta*Lep2_eta",   func = lambda ev : ev.Lep1_eta*ev.Lep2_eta),
            MVAVar("abs(Lep1_eta+Lep2_eta)",    func = lambda ev : abs(ev.Lep1_eta+ev.Lep2_eta))
        ]


        wts_wz    = '/afs/cern.ch/work/a/anmehta/public/dpsww_runII/CMSSW_10_4_0/src/CMGTools/DPSWW/python/plotter/BDTtraining/dataset_wz/weights/TMVAClassification_BDTG.weights.xml'
        wts_fakes = '/afs/cern.ch/work/a/anmehta/public/dpsww_runII/CMSSW_10_4_0/src/CMGTools/DPSWW/python/plotter/BDTtraining/dataset_fakes/weights/TMVAClassification_BDTG.weights.xml'
        self._MVAs['BDT_DPS_WZ']    = MVATool('BDTG_method', wts_wz   , self._vars, rarity=True)
        self._MVAs['BDT_DPS_fakes'] = MVATool('BDTG_method', wts_fakes, self._vars, rarity=True)
    def beginJob(self):
        pass
    def endJob(self):
        pass
    def beginFile(self, inputFile, outputFile, inputTree, wrappedOutputTree):
        #self.initReaders(inputTree) # initReaders must be called in beginFile
        self.out = wrappedOutputTree
        self.out.branch('BDT_DPS_WZ', "F")
        self.out.branch('BDT_DPS_fakes', "F")
        pass
    def endFile(self, inputFile, outputFile, inputTree, wrappedOutputTree):
        pass
    def analyze(self, event):
        
        mvadict = dict([ (name, mva(event)) for name, mva in self._MVAs.iteritems()])
        self.out.fillBranch('BDT_DPS_WZ'   , mvadict['BDT_DPS_WZ'])
        self.out.fillBranch('BDT_DPS_fakes', mvadict['BDT_DPS_fakes'])
        return True


