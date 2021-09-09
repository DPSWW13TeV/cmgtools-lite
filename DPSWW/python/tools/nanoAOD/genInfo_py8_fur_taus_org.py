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
        self.jetvars= ("pt","eta","phi","mass","partonFlavour","hadronFlavour")
        pass
    def beginJob(self):
        pass
    def endJob(self):
        pass

    def beginFile(self, inputFile, outputFile, inputTree, wrappedOutputTree):
        self.out = wrappedOutputTree
        self.out.branch("nGenleps"+self.label,"I")
        self.out.branch("nWdaughters"+self.label,"I")
        self.out.branch("nGenJet"+self.label,"I")
        self.out.branch("nGentaus"+self.label,"I")
        self.out.branch("nGentaus_had"+self.label,"I")
        for V in self.vars:
            self.out.branch("Genleps"+self.label+"_"+V, "F", lenVar="nGenleps"+self.label)
            #self.out.branch("Gentaus"+self.label+"_"+V, "F", lenVar="nGentaus"+self.label
        for WV in self.vars:
            self.out.branch("Wdaughters"+self.label+"_"+WV, "F", lenVar="nWdaughters"+self.label)
        for JV in self.jetvars:
            self.out.branch("GenJet"+self.label+"_"+JV, "F", lenVar="nGenJet"+self.label)

    def endFile(self, inputFile, outputFile, inputTree, wrappedOutputTree):
        pass
    def gensel(self,gP):
       return True #(gP.pt > 20.0 and abs(gP.eta) < 2.5)

    def analyze(self, event):
        """process event, return True (go to next module) or False (fail, go to next event)"""
 
        genparticles=Collection(event,"GenPart")
        tausH=Collection(event,"GenVisTau")
        #genjets=Collection(event,"GenJet")
        
        #jetindex=[]
        #retJ={}
        leptons=[]; taus=[]
        ret={}; taus_had=[];
        Wkids=[];WVret={};
        #for JV in self.jetvars:
        #    retJ["GenJet"+self.label+"_"+JV] = [getattr(jj,JV) for jj in genjets]

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
        nleps_M=0
        #print 'starting the event'
        for tH in tausH:
            #if tH.status == 15:    continue
            if tH.genPartIdxMother > -1 :
                for h,iht in enumerate(genparticles):
                    if h == tH.genPartIdxMother and (abs(iht.pdgId) == 24):
                        taus_had.append(tH)
            else: continue

        #        print 'lets start the fun'
        for ig,iGen in enumerate(genparticles):
            if (abs(iGen.pdgId) == 24 and iGen.status == 62):
                #print 'status of W', iGen.status
                for it,itM in enumerate(genparticles):
                    if itM.genPartIdxMother > -1 and itM.genPartIdxMother == ig and abs(itM.pdgId) not in [12,14,16] :
                        #print " this is the W's daugther index: ",ig,itM.pdgId,itM.status,itM.pt
                        Wkids.append(itM)
            elif ( abs(iGen.pdgId) in [11,13]  and iGen.status == 1 and promptLep(iGen.statusFlags,-1) and promptLep(iGen.statusFlags,6) ):
                if iGen.genPartIdxMother > -1 :
                    for m,iMa in enumerate(genparticles):
                        if m == iGen.genPartIdxMother and (abs(iMa.pdgId) in [24]): #,abs(iGen.pdgId)]):
                            leptons.append(iGen)
                else:   nleps_M+=1
            elif ( abs(iGen.pdgId) in [15]  and promptLep(iGen.statusFlags,-1)  and iGen.status == 2  ):
                if iGen.genPartIdxMother > -1 :
                    for t,iTa in enumerate(genparticles):
                        if t == iGen.genPartIdxMother and abs(iTa.pdgId) in [24]:
                            #print 'tau pt ', iGen.pt
                            taus.append(iGen)
                        
            else:continue
        #print 'total',len(leptons)+len(taus)+len(taus_had)
        leptons.sort(key=lambda x: x.pt, reverse=True)
        taus.sort(key=lambda x: x.pt, reverse=True)
        taus_had.sort(key=lambda x: x.pt, reverse=True)
        Wkids.sort(key=lambda x: x.pt, reverse=True)

        self.out.fillBranch('nGenleps'+self.label,len(leptons))
        self.out.fillBranch('nWdaughters'+self.label,len(Wkids))
        self.out.fillBranch('nGentaus'+self.label,len(taus))
        self.out.fillBranch('nGentaus_had'+self.label,len(taus_had))
        #print taus_had
##am
##am        if len(leptons) > 0 and len(taus) > 0:
##am            print 'lep-tau final state: leps saved ',len(leptons),' and taus saved ',len(taus)
##am            if len(taus_had) >0 or nleps_M > 0 :
##am                print "orphaned leps ",nleps_M, " had taus ",len(taus_had)
##am        else:
##am            print 'no. of leptons ',len(leptons),len(taus) if len(taus) > 0 else ''
##am            if len(taus_had) >0 or nleps_M > 0 :
##am                "orphaned leps ",nleps_M, " had taus ",len(taus_had)
        for V in self.vars:
            ret["Genleps"+self.label+"_"+V] = [getattr(j,V) for j in leptons]
        for WV in self.vars:
            WVret["Wdaughters"+self.label+"_"+WV] = [getattr(j,WV) for j in Wkids]
        for V in self.vars:
            self.out.fillBranch("Genleps"+self.label+"_"+V, [ ret["Genleps"+self.label+"_"+V][j] for j in range (len(leptons))])
        for WV in self.vars:
            self.out.fillBranch("Wdaughters"+self.label+"_"+WV, [ WVret["Wdaughters"+self.label+"_"+WV][j] for j in range (len(Wkids))])


        #for JV in self.jetvars:
        #    self.out.fillBranch("GenJet"+self.label+"_"+JV, [ retJ["GenJet"+self.label+"_"+JV][j] for j in range(len(genjets))])

        return True
#genleptons = lambda : genInfo_py8_fur_taus()

