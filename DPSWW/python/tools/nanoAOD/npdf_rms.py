from PhysicsTools.NanoAODTools.postprocessing.framework.eventloop import Module
from PhysicsTools.NanoAODTools.postprocessing.framework.datamodel import Collection , Object
from copy import deepcopy
import ROOT
import os, math 

class npdf_rms(Module):
    def __init__(self):
        pass
    def beginFile(self, inputFile, outputFile, inputTree, wrappedOutputTree):
        self.out = wrappedOutputTree
        self.out.branch('nnpdf_rms','F')


    def analyze(self, event):
        vals=[];rms_val=0
        if not hasattr(event,"nLHEPdfWeight"):
            nvars=0; 
        else:
            nvars=getattr(event,"nLHEPdfWeight")
            if nvars > 0:
                for i in xrange(nvars):
                    ival=event.LHEPdfWeight[i]
                    vals.append((ival-1.0)**2)
                rms_val=1.0+math.sqrt(sum(vals)/len(vals))
            #print rms_val

        self.out.fillBranch('nnpdf_rms', rms_val)

        return True
