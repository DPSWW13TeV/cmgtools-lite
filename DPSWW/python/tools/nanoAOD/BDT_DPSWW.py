#from CMGTools.TTHAnalysis.treeReAnalyzer import *
from PhysicsTools.NanoAODTools.postprocessing.framework.eventloop import Module 
from PhysicsTools.NanoAODTools.postprocessing.framework.datamodel import Collection as Collection 
from CMGTools.DPSWW.tools.nanoAOD.friendVariableProducerTools import writeOutput
from CMGTools.DPSWW.tools.mvaTool import *
            
    

class BDT_DPSWW(Module):
    def __init__(self,year,usecpt):
        self._MVAs = {}
        self.year=year
        self.usecpt=usecpt
        self.pff='_withcpt' if usecpt else '_withpt'
        print year
        self._vars = [
            #MVAVar("Lep1_conept",       func = lambda ev : ev.Lep1_conept ),
            #MVAVar("Lep2_conept",       func = lambda ev : ev.Lep2_conept ),
            MVAVar("Lep1_conept" if usecpt else "Lep1_pt",       func = lambda ev : ev.Lep1_conept if usecpt else ev.Lep1_pt),
            MVAVar("Lep2_conept" if usecpt else "Lep2_pt",       func = lambda ev : ev.Lep2_conept if usecpt else ev.Lep2_pt),
            MVAVar("met",                                        func = lambda ev : ev.met),
            MVAVar("mt2",       func = lambda ev : ev.mt2),
            MVAVar("mtll",      func = lambda ev : ev.mtll), 
            MVAVar("mtl1met",   func = lambda ev : ev.mtl1met), 
            MVAVar("dphill",    func = lambda ev : ev.dphill),
            MVAVar("dphil2met", func = lambda ev : ev.dphil2met), 
            MVAVar("dphilll2",  func = lambda ev : ev.dphilll2), 
            MVAVar("Lep1_eta*Lep2_eta",   func = lambda ev : ev.Lep1_eta*ev.Lep2_eta),
            MVAVar("abs(Lep1_eta+Lep2_eta)",    func = lambda ev : abs(ev.Lep1_eta+ev.Lep2_eta))
        ]
        baseDir='/afs/cern.ch/work/a/anmehta/public/dpsww_runII/CMSSW_10_2_16_UL/src/CMGTools/DPSWW/python/plotter/BDTtraining/files/'
        #pff='_withcpt' if usecpt else '_withpt'
        if self.year == 2016:
            #print 'using wts for 2016'
            wts_wz_amc    = baseDir+'dataset_2016_wz_amc{here}/weights/TMVAClassification_BDT.weights.xml'.format(here=self.pff)
            wts_wz_pow    = baseDir+'dataset_2016_wz_pow{here}/weights/TMVAClassification_BDT.weights.xml'.format(here=self.pff)
            wts_TLCR      = baseDir+'dataset_2016_TL{here}/weights/TMVAClassification_BDT.weights.xml'    .format(here=self.pff)
            wts_wz_amcG   = baseDir+'dataset_2016_wz_amc{here}/weights/TMVAClassification_BDTG.weights.xml'.format(here=self.pff)
            wts_wz_powG   = baseDir+'dataset_2016_wz_pow{here}/weights/TMVAClassification_BDTG.weights.xml'.format(here=self.pff)
            wts_TLCRG     = baseDir+'dataset_2016_TL{here}/weights/TMVAClassification_BDTG.weights.xml'    .format(here=self.pff)

        else:
            #print 'using training wts for 2017/2018' 
            wts_wz_amc    = baseDir+'dataset_muWP90_elWP70_2017_wz_amc{here}/weights/TMVAClassification_BDT.weights.xml'.format(here=self.pff)
            wts_wz_pow    = baseDir+'dataset_muWP90_elWP70_2017_wz_pow{here}/weights/TMVAClassification_BDT.weights.xml'.format(here=self.pff)
            wts_TLCR      = baseDir+'dataset_muWP90_elWP70_2017_TL{here}/weights/TMVAClassification_BDT.weights.xml'    .format(here=self.pff)

            wts_wz_amcG   = baseDir+'dataset_muWP90_elWP70_2017_wz_amc{here}/weights/TMVAClassification_BDTG.weights.xml'.format(here=self.pff)
            wts_wz_powG   = baseDir+'dataset_muWP90_elWP70_2017_wz_pow{here}/weights/TMVAClassification_BDTG.weights.xml'.format(here=self.pff)
            wts_TLCRG     = baseDir+'dataset_muWP90_elWP70_2017_TL{here}/weights/TMVAClassification_BDTG.weights.xml'    .format(here=self.pff)

            #        wts_multiC  = baseDir+'BDTtraining/dataset_multiclass/weights/TMVAMutliClass_BDTG.weights.xml'
            #wts_fakes    = baseDir+'dataset_muWP90_elWP70_2017_fakes_usingFRs{here}/weights/TMVAClassification_BDTG.weights.xml'.format(here=self.pff)
            #wts_TL       = baseDir+'dataset_muWP90_elWP70_2017_TL_usingFRs{here}/weights/TMVAClassification_BDTG.weights.xml'.format(here=self.pff)
            #wts_fakesCR  = baseDir+'dataset_muWP90_elWP70_2017_fakes{here}/weights/TMVAClassification_BDTG.weights.xml'.format(here=self.pff)
            
        self._MVAs['BDT_DPS_WZ_amc{here}' .format(here=self.pff)]      = MVATool('BDT_method',  wts_wz_amc    ,  self._vars, rarity=True)
        self._MVAs['BDT_DPS_WZ_pow{here}' .format(here=self.pff)]      = MVATool('BDT_method',  wts_wz_pow    ,  self._vars, rarity=True)
        self._MVAs['BDT_DPS_TLCR{here}'   .format(here=self.pff)]      = MVATool('BDT_method',  wts_TLCR      ,  self._vars, rarity=True)
        self._MVAs['BDTG_DPS_WZ_amc{here}'.format(here=self.pff)]      = MVATool('BDTG_method', wts_wz_amcG   ,  self._vars, rarity=True)
        self._MVAs['BDTG_DPS_WZ_pow{here}'.format(here=self.pff)]      = MVATool('BDTG_method', wts_wz_powG   ,  self._vars, rarity=True)
        self._MVAs['BDTG_DPS_TLCR{here}'  .format(here=self.pff)]      = MVATool('BDTG_method', wts_TLCRG     ,  self._vars, rarity=True)

##am        self._MVAs['BDT_DPS_fakes']     = MVATool('BDTG_method', wts_fakes    , self._vars, rarity=True)
##am        self._MVAs['BDT_DPS_TL']        = MVATool('BDTG_method', wts_TL       , self._vars, rarity=True)
##am        self._MVAs['BDT_DPS_fakesCR']   = MVATool('BDTG_method', wts_fakesCR  , self._vars, rarity=True)

##        self._MVAs['BDT_DPS_multiC']    = MVATool('BDTG_method', wts_multiC   , self._vars, rarity=False,nClasses=2)
##        self._MVAs['BDT_WZ_multiC']     = MVATool('BDTG_method', wts_multiC   , self._vars, rarity=False,nClasses=3)
##        self._MVAs['BDT_TL_multiC']     = MVATool('BDTG_method', wts_multiC   , self._vars, rarity=False,nClasses=4)
    def beginJob(self):
        pass
    def endJob(self):
        pass
    def beginFile(self, inputFile, outputFile, inputTree, wrappedOutputTree):
        #self.initReaders(inputTree) # initReaders must be called in beginFile
        #pff='_withcpt' if self.usecpt else '_withpt'

        self.out = wrappedOutputTree
        self.out.branch('BDT_DPS_WZ_amc{here}' .format(here=self.pff)  , "F")
        self.out.branch('BDT_DPS_WZ_pow{here}' .format(here=self.pff)  , "F")
        self.out.branch('BDT_DPS_TLCR{here}'   .format(here=self.pff)  , "F")
        self.out.branch('BDTG_DPS_WZ_amc{here}'.format(here=self.pff)  , "F")
        self.out.branch('BDTG_DPS_WZ_pow{here}'.format(here=self.pff)  , "F")
        self.out.branch('BDTG_DPS_TLCR{here}'  .format(here=self.pff)  , "F")

##        self.out.branch('BDT_DPS_multiC', "F")
##        self.out.branch('BDT_WZ_multiC', "F")
##        self.out.branch('BDT_TL_multiC', "F")
##am        self.out.branch('BDT_DPS_fakes'  , "F")
##am        self.out.branch('BDT_DPS_TL'     , "F")
##am        self.out.branch('BDT_DPS_fakesCR', "F")
        pass
    def endFile(self, inputFile, outputFile, inputTree, wrappedOutputTree):
        pass
    def analyze(self, event):
        
        mvadict = dict([ (name, mva(event)) for name, mva in self._MVAs.iteritems()])
        self.out.fillBranch('BDT_DPS_WZ_amc{here}' .format(here=self.pff)      , mvadict['BDT_DPS_WZ_amc{here}'.format(here=self.pff)])
        self.out.fillBranch('BDT_DPS_WZ_pow{here}' .format(here=self.pff)      , mvadict['BDT_DPS_WZ_pow{here}'.format(here=self.pff)])
        self.out.fillBranch('BDT_DPS_TLCR{here}'   .format(here=self.pff)      , mvadict['BDT_DPS_TLCR{here}'  .format(here=self.pff)])
        self.out.fillBranch('BDTG_DPS_WZ_amc{here}'.format(here=self.pff)      , mvadict['BDTG_DPS_WZ_amc{here}'.format(here=self.pff)])
        self.out.fillBranch('BDTG_DPS_WZ_pow{here}'.format(here=self.pff)      , mvadict['BDTG_DPS_WZ_pow{here}'.format(here=self.pff)])
        self.out.fillBranch('BDTG_DPS_TLCR{here}'  .format(here=self.pff)      , mvadict['BDTG_DPS_TLCR{here}'  .format(here=self.pff)])

##        self.out.fillBranch('BDT_DPS_multiC'   , mvadict['BDT_DPS_multiC'])
##        self.out.fillBranch('BDT_WZ_multiC'    , mvadict['BDT_WZ_multiC'])
##        self.out.fillBranch('BDT_TL_multiC'    , mvadict['BDT_TL_multiC'])
##am        self.out.fillBranch('BDT_DPS_fakes'      , mvadict['BDT_DPS_fakes'])
##am        self.out.fillBranch('BDT_DPS_TL'         , mvadict['BDT_DPS_TL'])
##am        self.out.fillBranch('BDT_DPS_fakesCR'    , mvadict['BDT_DPS_fakesCR'])

        return True


