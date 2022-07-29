from PhysicsTools.NanoAODTools.postprocessing.framework.eventloop import Module 
from PhysicsTools.NanoAODTools.postprocessing.framework.datamodel import Collection as Collection 
from CMGTools.DPSWW.tools.nanoAOD.friendVariableProducerTools import writeOutput
from CMGTools.DPSWW.tools.mvaTool import *

def promptLep(statusFlags,chkbit):
    bits = '{a:15b}'.format(a=statusFlags)
    return (bits[chkbit] == '1')
    
class genInfo_py8_fur_taus(Module):
    def __init__(self):
        self.label = "_sel" # "" if (label in ["",None]) else ("_"+label)
        self.vars = ("pt","eta","phi","mass","pdgId","status","genPartIdxMother","statusFlags")

        pass
    def beginJob(self):
        pass
    def endJob(self):
        pass

    def beginFile(self, inputFile, outputFile, inputTree, wrappedOutputTree):
        self.out = wrappedOutputTree
        self.out.branch("nGenleps"+self.label,"I")
        self.out.branch("nGenleps_unmatched"+self.label,"I")
        for V in self.vars:
            self.out.branch("Genleps"+self.label+"_"+V, "F", lenVar="nGenleps"+self.label)
            self.out.branch("Genleps_unmatched"+self.label+"_"+V, "F", lenVar="nGenleps_unmatched"+self.label)

    def endFile(self, inputFile, outputFile, inputTree, wrappedOutputTree):
        pass
    def gensel(self,gP):
       return True #(gP.pt > 20.0 and abs(gP.eta) < 2.5)

    def analyze(self, event):
        """process event, return True (go to next module) or False (fail, go to next event)"""
 
        genparticles=Collection(event,"GenPart")
        leptons=[]; leptons_unmatched=[];        ret={};        ret_unm={};

        for iGen in genparticles:
            if ( ( abs(iGen.pdgId) in [11,13] and (iGen.statusFlags&(1<<0))==1 and iGen.status == 1 and (iGen.statusFlags&(1<<8))==256 ) or ( abs(iGen.pdgId) == 15 and iGen.status == 2 and (iGen.statusFlags&(1<<0))==1 and (iGen.statusFlags&(1<<8))==256)):
                #      gp_m = gp[((abs(gp.pdgId)==13)&(gp.status==1)&((iGen.statusFlags&(1<<0))==1)&(iGen.statusFlags&(1<<8)==256))]
##am                if iGen.genPartIdxMother > -1 :
##am                    for m,iMa in enumerate(genparticles):
##am                        if m == iGen.genPartIdxMother and (abs(iMa.pdgId) in [24]): #,abs(iGen.pdgId)]):
                leptons.append(iGen)
                #else: 
                #    leptons_unmatched.append(iGen)
            else: continue


        leptons.sort(key=lambda x: x.pt, reverse=True)
        leptons_unmatched.sort(key=lambda x: x.pt, reverse=True)



        self.out.fillBranch('nGenleps'+self.label,len(leptons))
        self.out.fillBranch('nGenleps_unmatched'+self.label,len(leptons_unmatched))

        for V in self.vars:
            ret["Genleps"+self.label+"_"+V] = [getattr(j,V) for j in leptons]

        for V in self.vars:
            self.out.fillBranch("Genleps"+self.label+"_"+V, [ ret["Genleps"+self.label+"_"+V][j] for j in range (len(leptons))])

        for V in self.vars:
            ret_unm["Genleps_unmatched"+self.label+"_"+V] = [getattr(j,V) for j in leptons_unmatched]

        for V in self.vars:
            self.out.fillBranch("Genleps_unmatched"+self.label+"_"+V, [ ret_unm["Genleps_unmatched"+self.label+"_"+V][j] for j in range (len(leptons_unmatched))])




        return True
#genleptons = lambda : genInfo_py8_fur_taus()


        #isPrompt = bits[-1] == '1'
        #isDecayedLeptonHadron = bits[-2] == '1'
        #isTauDecayProduct=bits[-3] == '1' 
        #isPromptTauDecayProduct=bits[-4] == '1'
        #isDirectTauDecayProduct=bits[-5] == '1'
        #isDirectPromptTauDecayProduct=bits[-6] == '1'
        #isDirectHadronDecayProduct=bits[-7] == '1'
        #isHardProcess=bits[7] == '1'
        #fromHardProcess=bits[8] == '1'
        #isHardProcessTauDecayProduct=bits[5] == '1'
        #isDirectHardProcessTauDecayProduct=bits[4] == '1'
        #fromHardProcessBeforeFSR=bits[3] == '1'
        #isFirstCopy=bits[2] == '1'
        #isLastCopy=bits[1] == '1'
        #isLastCopyBeforeFSR=bits[0] == '1'
        #fromHardProcessFinalState = (1 << 0) | (1 << 8) | (1 << 9) | (1 << 5)
        #fromHardProcessDecayed = (1 << 14)
        #lastBeforeFSR = (1 << 14)
#Events->Draw("Sum$(GenPart_status == 2 && (GenPart_statusFlags & 1) && (GenPart_statusFlags & 256) && abs(GenPart_pdgId) == 15) + Sum$(GenPart_status == 1 && (GenPart_statusFlags & 1) && (GenPart_statusFlags & 256) && abs(GenPart_pdgId) == 13) + Sum$(GenPart_status == 1 && (GenPart_statusFlags & 1) && (GenPart_statusFlags & 256) && abs(GenPart_pdgId) == 11)")


