#from CMGTools.TTHAnalysis.treeReAnalyzer import *
from PhysicsTools.NanoAODTools.postprocessing.framework.eventloop import Module 
from PhysicsTools.NanoAODTools.postprocessing.framework.datamodel import Collection as Collection 
from CMGTools.DPSWW.tools.nanoAOD.friendVariableProducerTools import writeOutput
from CMGTools.DPSWW.tools.mvaTool import *
            
    

class BDT_DPSWW(Module):
    def __init__(self,year,usecpt,shift=''):
        self._MVAs = {}
        self.year=year
        self.usecpt=usecpt
        self.pff='_withcpt' if usecpt else '_withpt'
        print year
        self.shift=shift
        self.allvars=['jesBBEC1_year','jesFlavorQCD','jesEC2','jesAbsolute_year','jesHF','jesJECTotal','jesHF_year','jesRelativeSample_year','jesRelativeBal','jesBBEC1','jesEC2_year','jesAbsolute','unclustEn','jerbarrel','jerendcap1','jerendcap2highpt','jerendcap2lowpt','jerforwardhighpt','jerforwardlowpt','HEM'] if len(shift) > 0 else ['']
        self.svars=['HEM'] if len(shift) > 0 else ['']
        #self.svars=['jesJECTotal'] if len(shift) > 0 else ['']
        #self.var=variation
        #print variation
        baseDir='/afs/cern.ch/work/a/anmehta/public/dpsww_runII/CMSSW_10_2_16_UL/src/CMGTools/DPSWW/python/plotter/BDTtraining/files/'
        #pff='_withcpt' if usecpt else '_withpt'

        
        wts_wz_amcG  = baseDir+'dataset_ultramax_{mvaWP}{yr}_wz_amc{here}/weights/TMVAClassification_BDTG.weights.xml' .format(here=self.pff,yr=self.year,mvaWP='muWP90_elWP70_' if self.year == 2017 else '')
        wts_TLCRG    = baseDir+'dataset_ultramax_{mvaWP}{yr}_TL{here}/weights/TMVAClassification_BDTG.weights.xml'     .format(here=self.pff,yr=self.year,mvaWP='muWP90_elWP70_' if self.year == 2017 else '')


        for src in self.svars:
            name='_'+src+self.shift if len(src) > 0 else ''         
            inputvarsUp = [
                MVAVar("Lep1_conept" if usecpt else "Lep1_pt", func = lambda ev : ev.Lep1_conept if usecpt else ev.Lep1_pt),
                MVAVar("Lep2_conept" if usecpt else "Lep2_pt", func = lambda ev : ev.Lep2_conept if usecpt else ev.Lep2_pt),
                MVAVar("met",                                  func = lambda ev : getattr(ev,'met%s'%name)),
                MVAVar("mt2",       func = lambda ev : getattr(ev,'mt2%s'%name)),
                MVAVar("mtll",      func = lambda ev : ev.mtll), 
                MVAVar("mtl1met",   func = lambda ev : getattr(ev,'mtl1met%s'%name)),
                MVAVar("dphill",    func = lambda ev : ev.dphill),
                MVAVar("dphil2met", func = lambda ev : getattr(ev,'dphil2met%s'%name)), 
                MVAVar("dphilll2",  func = lambda ev : ev.dphilll2), 
                MVAVar("Lep1_eta*Lep2_eta",   func = lambda ev : ev.Lep1_eta*ev.Lep2_eta),
                MVAVar("abs(Lep1_eta+Lep2_eta)",    func = lambda ev : abs(ev.Lep1_eta+ev.Lep2_eta))
            ]

            self._MVAs['BDTG_DPS_WZ_amc%s%s'%(self.pff,name)] = MVATool('BDTG_method', wts_wz_amcG,  inputvarsUp, rarity=True)
            self._MVAs['BDTG_DPS_TLCR%s%s'%(self.pff,name)]   = MVATool('BDTG_method', wts_TLCRG ,   inputvarsUp, rarity=True)
            self._MVAs['BDTG_DPS_WZ_amc_raw%s%s'%(self.pff,name)]= MVATool('BDTG_method',wts_wz_amcG,inputvarsUp, rarity=False)
            self._MVAs['BDTG_DPS_TLCR_raw%s%s'%(self.pff,name)]   = MVATool('BDTG_method', wts_TLCRG,inputvarsUp, rarity=False)

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


        for src in self.svars:
            name='_'+src+self.shift if len(src) > 0 else ''
            
            self.out.branch('BDTG_DPS_WZ_amc{here}'     .format(here=self.pff+name)  , "F")
            self.out.branch('BDTG_DPS_TLCR{here}'       .format(here=self.pff+name)  , "F")
            self.out.branch('BDTG_DPS_WZ_amc_raw{here}' .format(here=self.pff+name)  , "F")
            self.out.branch('BDTG_DPS_TLCR_raw{here}'   .format(here=self.pff+name)  , "F")
            

##        self.out.branch('BDT_DPS_multiC', "F")
##        self.out.branch('BDT_WZ_multiC', "F")
##        self.out.branch('BDT_TL_multiC', "F")
        pass
    def endFile(self, inputFile, outputFile, inputTree, wrappedOutputTree):
        pass
    def analyze(self, event):
        
        mvadict = dict([ (name, mva(event)) for name, mva in self._MVAs.iteritems()])

        for src in self.svars:
            name='_'+src+self.shift if len(src) > 0 else ''
            self.out.fillBranch('BDTG_DPS_WZ_amc%s%s'%(self.pff,name)    , mvadict['BDTG_DPS_WZ_amc%s%s' %(self.pff,name)])
            self.out.fillBranch('BDTG_DPS_TLCR%s%s'%(self.pff,name)      , mvadict['BDTG_DPS_TLCR%s%s'   %(self.pff,name)])
            self.out.fillBranch('BDTG_DPS_WZ_amc_raw%s%s'%(self.pff,name), mvadict['BDTG_DPS_WZ_amc_raw%s%s'%(self.pff,name)])
            self.out.fillBranch('BDTG_DPS_TLCR_raw%s%s'%(self.pff,name)  , mvadict['BDTG_DPS_TLCR_raw%s%s'%(self.pff,name)])
        

##        self.out.fillBranch('BDT_DPS_multiC'   , mvadict['BDT_DPS_multiC'])
##        self.out.fillBranch('BDT_WZ_multiC'    , mvadict['BDT_WZ_multiC'])
##        self.out.fillBranch('BDT_TL_multiC'    , mvadict['BDT_TL_multiC'])

        return True


