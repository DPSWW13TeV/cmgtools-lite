#from CMGTools.TTHAnalysis.treeReAnalyzer import *
from PhysicsTools.NanoAODTools.postprocessing.framework.eventloop import Module 
from PhysicsTools.NanoAODTools.postprocessing.framework.datamodel import Collection as Collection 
from CMGTools.DPSWW.tools.nanoAOD.friendVariableProducerTools import writeOutput
from CMGTools.DPSWW.tools.mvaTool import *
            
    

class BDT_DPSWW(Module):
    def __init__(self,year,usecpt,svars=[''],shift=['']):
        self._MVAs = {}
        self.year=year
        self.usecpt=usecpt
        self.pff='_withcpt' if usecpt else '_withpt'

        self.allvars=['jesBBEC1_year','jesFlavorQCD','jesEC2','jesAbsolute_year','jesHF','jesJECTotal','jesHF_year','jesRelativeSample_year','jesRelativeBal','jesBBEC1','jesEC2_year','jesAbsolute','unclustEn','jerbarrel','jerendcap1','jerendcap2highpt','jerendcap2lowpt','jerforwardhighpt','jerforwardlowpt','HEM']
        self.svars=self.allvars if 'all' in svars else svars # #[x  if x != 'all' else self.allvars for x in svars]
        self.shift=shift #if len(svars) > 0 else ['']
        print self.svars,self.shift
        #self.svars=['HEM'] if len(shift) > 0 else [''], ['unclustEn'],['jesJECTotal']

        cmg='/afs/cern.ch/work/a/anmehta/public/dpsww_runII/CMSSW_10_2_16_UL/src/CMGTools/DPSWW/python/plotter/BDTtraining/' #files/'
        baseDir='/afs/cern.ch/user/a/anmehta/public/dnn/'
        pff='_withcpt' if usecpt else '_withpt'

        wts_wz_powG  = cmg+'dataset_Sep2021_dpsWW_wz_pow_%s%s/weights/TMVAClassification_BDTG.weights.xml'%(self.year,self.pff)
        wts_wz_amcG  = baseDir+'dataset_dnn_nospec_dpsvs_wz_amc_%s%s/weights/TMVAClassification_BDTG.weights.xml'%(self.year,self.pff)
        wts_TLCRG    = baseDir+'dataset_dnn_nospec_dpsvs_TL_%s%s/weights/TMVAClassification_BDTG.weights.xml'%(self.year,self.pff)
        Awts_wz_amcG  = baseDir+'dataset_testAll_wz_amc_2018_withpt/weights/TMVAClassification_BDTG.weights.xml'
        Awts_TLCRG    = baseDir+'dataset_testAll_TL_2018_withpt/weights/TMVAClassification_BDTG.weights.xml'
        

        wts_py_wz_pow  = cmg+'dataset_Oct2021_dpsWW_py_wz_pow_%s_withpt/weights/TMVAClassification_BDTG.weights.xml'%(self.year)
        wts_py_wz_amc  = cmg+'dataset_Oct2021_dpsWW_py_wz_amc_%s_withpt/weights/TMVAClassification_BDTG.weights.xml'%(self.year)
        wts_py_TL      = cmg+'dataset_Oct2021_dpsWW_py_TL_%s_withpt/weights/TMVAClassification_BDTG.weights.xml'%(self.year)

        wts_hw_wz_pow  = cmg+'dataset_Oct2021_dpsWW_hw_wz_pow_%s_withpt/weights/TMVAClassification_BDTG.weights.xml'%(self.year)
        wts_hw_wz_amc  = cmg+'dataset_Oct2021_dpsWW_hw_wz_amc_%s_withpt/weights/TMVAClassification_BDTG.weights.xml'%(self.year)
        wts_hw_TL      = cmg+'dataset_Oct2021_dpsWW_hw_TL_%s_withpt/weights/TMVAClassification_BDTG.weights.xml'%(self.year)

        wts_ns_wz_pow  = cmg+'dataset_Oct2021_dpsWW_ns_wz_pow_%s_withpt/weights/TMVAClassification_BDTG.weights.xml'%(self.year)
        wts_ns_wz_amc  = cmg+'dataset_Oct2021_dpsWW_ns_wz_amc_%s_withpt/weights/TMVAClassification_BDTG.weights.xml'%(self.year)
        wts_ns_TL      = cmg+'dataset_Oct2021_dpsWW_ns_TL_%s_withpt/weights/TMVAClassification_BDTG.weights.xml'%(self.year)


        for src in self.svars:
            for sh in self.shift:
                name='_'+src+sh if len(src) > 0 else ''
                print 'this is what m running on', name
                inputvars = [
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

                self._MVAs['BDTG_DPS_WZ_amc_raw%s%s'%(self.pff,name)]= MVATool('BDTG_method',wts_py_wz_amc,inputvars)
                self._MVAs['BDTG_DPS_WZ_pow_raw%s%s'%(self.pff,name)]= MVATool('BDTG_method',wts_py_wz_pow,inputvars)
                self._MVAs['BDTG_DPS_TLCR_raw%s%s'%(self.pff,name)]   = MVATool('BDTG_method', wts_py_TL,inputvars)

                self._MVAs['BDTG_DPS_hw_WZ_amc_raw%s%s'%(self.pff,name)]= MVATool('BDTG_method',wts_hw_wz_amc,inputvars)
                self._MVAs['BDTG_DPS_hw_WZ_pow_raw%s%s'%(self.pff,name)]= MVATool('BDTG_method',wts_hw_wz_pow,inputvars)
                self._MVAs['BDTG_DPS_hw_TLCR_raw%s%s'%(self.pff,name)]   = MVATool('BDTG_method', wts_hw_TL,inputvars)

                self._MVAs['BDTG_DPS_ns_WZ_amc_raw%s%s'%(self.pff,name)]= MVATool('BDTG_method',wts_ns_wz_amc,inputvars)
                self._MVAs['BDTG_DPS_ns_WZ_pow_raw%s%s'%(self.pff,name)]= MVATool('BDTG_method',wts_ns_wz_pow,inputvars)
                self._MVAs['BDTG_DPS_ns_TLCR_raw%s%s'%(self.pff,name)]   = MVATool('BDTG_method', wts_ns_TL,inputvars)


    def beginJob(self):
        pass
    def endJob(self):
        pass
    def beginFile(self, inputFile, outputFile, inputTree, wrappedOutputTree):

        self.out = wrappedOutputTree


        for src in self.svars:
            for sh in self.shift:
                #                name='_'+src+sh
                name='_'+src+sh if len(src) > 0 else ''
            
                self.out.branch('BDTG_DPS_WZ_amc_raw{here}' .format(here=self.pff+name)  , "F")
                self.out.branch('BDTG_DPS_WZ_pow_raw{here}' .format(here=self.pff+name)  , "F")
                self.out.branch('BDTG_DPS_TLCR_raw{here}'   .format(here=self.pff+name)  , "F")
                self.out.branch('BDTG_DPS_hw_WZ_amc_raw{here}' .format(here=self.pff+name)  , "F")
                self.out.branch('BDTG_DPS_hw_WZ_pow_raw{here}' .format(here=self.pff+name)  , "F")
                self.out.branch('BDTG_DPS_hw_TLCR_raw{here}'   .format(here=self.pff+name)  , "F")
                self.out.branch('BDTG_DPS_ns_WZ_amc_raw{here}' .format(here=self.pff+name)  , "F")
                self.out.branch('BDTG_DPS_ns_WZ_pow_raw{here}' .format(here=self.pff+name)  , "F")
                self.out.branch('BDTG_DPS_ns_TLCR_raw{here}'   .format(here=self.pff+name)  , "F")

            

##        self.out.branch('BDT_DPS_multiC', "F")
##        self.out.branch('BDT_WZ_multiC', "F")
##        self.out.branch('BDT_TL_multiC', "F")
        pass
    def endFile(self, inputFile, outputFile, inputTree, wrappedOutputTree):
        pass
    def analyze(self, event):
        
        mvadict = dict([ (name, mva(event)) for name, mva in self._MVAs.iteritems()])

        for src in self.svars:
            for sh in self.shift:
                #name='_'+src+sh
                name='_'+src+sh if len(src) > 0else ''
                
                #            name='_'+src+self.shift if len(src) > 0 else ''
                self.out.fillBranch('BDTG_DPS_WZ_amc_raw%s%s'%(self.pff,name), mvadict['BDTG_DPS_WZ_amc_raw%s%s'%(self.pff,name)])
                self.out.fillBranch('BDTG_DPS_WZ_pow_raw%s%s'%(self.pff,name), mvadict['BDTG_DPS_WZ_pow_raw%s%s'%(self.pff,name)])
                self.out.fillBranch('BDTG_DPS_TLCR_raw%s%s'%(self.pff,name)  , mvadict['BDTG_DPS_TLCR_raw%s%s'%(self.pff,name)])
        
                self.out.fillBranch('BDTG_DPS_hw_WZ_amc_raw%s%s'%(self.pff,name), mvadict['BDTG_DPS_hw_WZ_amc_raw%s%s'%(self.pff,name)])
                self.out.fillBranch('BDTG_DPS_hw_WZ_pow_raw%s%s'%(self.pff,name), mvadict['BDTG_DPS_hw_WZ_pow_raw%s%s'%(self.pff,name)])
                self.out.fillBranch('BDTG_DPS_hw_TLCR_raw%s%s'%(self.pff,name)  , mvadict['BDTG_DPS_hw_TLCR_raw%s%s'%(self.pff,name)])
        
                self.out.fillBranch('BDTG_DPS_ns_WZ_amc_raw%s%s'%(self.pff,name), mvadict['BDTG_DPS_ns_WZ_amc_raw%s%s'%(self.pff,name)])
                self.out.fillBranch('BDTG_DPS_ns_WZ_pow_raw%s%s'%(self.pff,name), mvadict['BDTG_DPS_ns_WZ_pow_raw%s%s'%(self.pff,name)])
                self.out.fillBranch('BDTG_DPS_ns_TLCR_raw%s%s'%(self.pff,name)  , mvadict['BDTG_DPS_ns_TLCR_raw%s%s'%(self.pff,name)])
        

##        self.out.fillBranch('BDT_DPS_multiC'   , mvadict['BDT_DPS_multiC'])
##        self.out.fillBranch('BDT_WZ_multiC'    , mvadict['BDT_WZ_multiC'])
##        self.out.fillBranch('BDT_TL_multiC'    , mvadict['BDT_TL_multiC'])

        return True


