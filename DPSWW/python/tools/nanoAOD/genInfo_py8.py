from PhysicsTools.NanoAODTools.postprocessing.framework.eventloop import Module 
from PhysicsTools.NanoAODTools.postprocessing.framework.datamodel import Collection as Collection 
from CMGTools.DPSWW.tools.nanoAOD.friendVariableProducerTools import writeOutput
from CMGTools.DPSWW.tools.mvaTool import *

def promptLep(statusFlags,chkbit):
    bits = '{a:15b}'.format(a=statusFlags)
    return (bits[chkbit] == '1')
    
class genInfo_py8(Module):
    def __init__(self):
        self.label = "_sel" # "" if (label in ["",None]) else ("_"+label)
        self.vars = ("pt","eta","phi","mass","pdgId","status","genPartIdxMother","statusFlags")
        self.jetvars= ("pt","eta","phi","mass","partonFlavour","hadronFlavour")
        pass
    def beginJob(self):
        pass
    def endJob(self):
        pass

    def beginFile(self, inputFile, outputFile, inputTree, wrappedOutputTree):
        self.out = wrappedOutputTree
        self.out.branch("nGenPart"+self.label,"I")
        self.out.branch("nGenJet"+self.label,"I")

        for V in self.vars:
            self.out.branch("GenPart"+self.label+"_"+V, "F", lenVar="nGenPart"+self.label)
        for JV in self.jetvars:
            self.out.branch("GenJet"+self.label+"_"+JV, "F", lenVar="nGenJet"+self.label)

    def endFile(self, inputFile, outputFile, inputTree, wrappedOutputTree):
        pass
    def gensel(self,gP):
       return True #(gP.pt > 20.0 and abs(gP.eta) < 2.5)

    def analyze(self, event):
        """process event, return True (go to next module) or False (fail, go to next event)"""
 
        genparticles=Collection(event,"GenPart")
        genjets=Collection(event,"GenJet")
        
        jetindex=[]
        retJ={}
        leptons=[]
        ret={}

        for JV in self.jetvars:
            retJ["GenJet"+self.label+"_"+JV] = [getattr(jj,JV) for jj in genjets]

        #isPrompt = bits[-1] == '1'
        #isDecayedLeptonHadron = bits[-2] == '1'
        #isTauDecayProduct=bits[-3] == '1' 
        #isPromptTauDecayProduct=bits[-4] == '1'
        #isDirectTauDecayProduct=bits[-5] == '1'
        #isDirectPromptTauDecayProduct=bits[-6] == '1'
        #isDirectHadronDecayProduct=bits[-7] == '1'
        #isHardProcess=bits[7] == '1'
        #fromHardProcess=bits[6] == '1'
        #isHardProcessTauDecayProduct=bits[5] == '1'
        #isDirectHardProcessTauDecayProduct=bits[4] == '1'
        #fromHardProcessBeforeFSR=bits[3] == '1'
        #isFirstCopy=bits[2] == '1'
        #isLastCopy=bits[1] == '1'
        #isLastCopyBeforeFSR=bits[0] == '1'
        #fromHardProcessFinalState = (1 << 0) | (1 << 8) | (1 << 9) | (1 << 5)
        #fromHardProcessDecayed = (1 << 14)
        #lastBeforeFSR = (1 << 14)

        for iGen in genparticles:
            ##            if ( ( ( (abs(iGen.pdgId) in [11,13] and iGen.status == 1) or  (abs(iGen.pdgId) ==15 and iGen.status ==  2) ) and promptLep(iGen.statusFlags,-1) and promptLep(iGen.statusFlags,6)  ) or ( abs(iGen.pdgId) in [12,14,16] and iGen.status == 1)       ):
            if ( ( ( (abs(iGen.pdgId) in [11,13] and iGen.status == 1) or  (abs(iGen.pdgId) ==15 and iGen.status ==  2) ) and promptLep(iGen.statusFlags,-1) and promptLep(iGen.statusFlags,6)  )        ):    
                    leptons.append(iGen)
            else:
                continue

        leptons.sort(key=lambda x: x.pt, reverse=True)
        self.out.fillBranch('nGenPart'+self.label,len(leptons))
        self.out.fillBranch('nGenJet'+self.label,len(genjets))


        for V in self.vars:
            ret["GenPart"+self.label+"_"+V] = [getattr(j,V) for j in leptons]

        for V in self.vars:
            self.out.fillBranch("GenPart"+self.label+"_"+V, [ ret["GenPart"+self.label+"_"+V][j] for j in range (len(leptons))])

        for JV in self.jetvars:
            self.out.fillBranch("GenJet"+self.label+"_"+JV, [ retJ["GenJet"+self.label+"_"+JV][j] for j in range(len(genjets))])

        return True
#genleptons = lambda : genInfo_py8()

