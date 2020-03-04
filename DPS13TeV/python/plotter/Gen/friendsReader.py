import ROOT, os, optparse, copy, datetime
from ROOT import TLorentzVector, TVector2, std
ROOT.gROOT.SetBatch(True)
date = datetime.date.today().isoformat()
import time, re
import multiprocessing 
from optparse import OptionParser
from array import array
from ROOT import TLorentzVector


tName = 'Friends'
basedir='/eos/cms/store/cmst3/group/dpsww/genfriends_03022020/'
def if3(cond, iftrue, iffalse):
    return iftrue if cond else iffalse

def dilepVars(pt1,eta1,phi1,pt2,eta2,phi2,variable='M'):
    lep1 = ROOT.TLorentzVector(0,0,0,0)
    lep2 = ROOT.TLorentzVector(0,0,0,0)
    lep1.SetPtEtaPhiM(pt1,eta1,phi1,0.0)
    lep2.SetPtEtaPhiM(pt2,eta2,phi2,0.0)
    dilep = lep1+lep2
    if variable == "M":
        return dilep.M()
    elif variable == "dphi":
        return  abs(lep1.DeltaPhi(lep2))
    elif variable == "pt":
        return dilep.Pt()
    elif variable == "deta":
        return abs(lep1.Eta()-lep2.Eta())
    else :
        return abs(lep1.DeltaR(lep2))

def fourlepVars(pt1,eta1,phi1,pt2,eta2,phi2,pt3,eta3,phi3,pt4,eta4,phi4,variable='M'):
    lep1 = ROOT.TLorentzVector(0,0,0,0)
    lep2 = ROOT.TLorentzVector(0,0,0,0)
    lep3 = ROOT.TLorentzVector(0,0,0,0)
    lep4 = ROOT.TLorentzVector(0,0,0,0)
    lep1.SetPtEtaPhiM(pt1,eta1,phi1,0.0)
    lep2.SetPtEtaPhiM(pt2,eta2,phi2,0.0)
    lep3.SetPtEtaPhiM(pt3,eta3,phi3,0.0)
    lep4.SetPtEtaPhiM(pt4,eta4,phi4,0.0)
    fourlep = lep1+lep2+lep3+lep4
    if variable == "M":
        return fourlep.M()
    else:
        return fourlep.Pt()


def fillmllHist(fName,outdir):
    
    f_ex0 = ROOT.TFile('{basedir}{fileName}.root'.format(basedir=basedir,fileName=fName), 'READ');
    outfile=fName+'_gen'
    t_ex0 = f_ex0.Get(tName)
    fout = ROOT.TFile('{HERE}/{OUTPUT}.root'.format(HERE=outdir,OUTPUT=outfile), 'RECREATE');
    outTree = ROOT.TTree('tree',"subset of Events ")
    mll    =array('f',[0.])
    etal1  =array('f',[0.])
    ptl1   =array('f',[0.])
    phil1  =array('f',[0.])
    etal2  =array('f',[0.])
    phil2  =array('f',[0.])
    ptl2   =array('f',[0.])
    detall =array('f',[0.])
    dphill =array('f',[0.])
    dRll=array('f',[0.])
    pdgIdl1 =array('f',[0.])
    pdgIdl2 =array('f',[0.])
    ptel   =array('f',[0.])
    etael  =array('f',[0.])
    ptmu  =array('f',[0.])
    etamu  =array('f',[0.])
    ptnn  =array('f',[0.])
    nleps=array('f',[0.])
    mW1=array('f',[0.])
    mW2=array('f',[0.])
    outTree.Branch("mW1",mW1,"mW1/F")
    outTree.Branch("mW2",mW2,"mW2/F")
    outTree.Branch("nleps ",nleps,"nleps/F")
    outTree.Branch("ptel ",ptel,"ptel/F")
    outTree.Branch("etael ",etael,"etael/F")
    outTree.Branch("etamu",etamu,"etamu/F")
    outTree.Branch("ptmu ",ptmu,"ptmu/F")


    outTree.Branch("mll",mll,"mll/F")
    outTree.Branch("etal1",etal1,"etal1/F")
    outTree.Branch("ptl1 ",ptl1,"ptl1/F")
    outTree.Branch("phil1 ",phil1,"phil1/F")
    outTree.Branch("etal2",etal2,"etal2/F")
    outTree.Branch("ptl2 ",ptl2,"ptl2/F")
    outTree.Branch("phil2 ",phil2,"phil2/F")
    outTree.Branch("detall",detall,"detall/F")
    outTree.Branch("dphill",dphill,"dphill/F")

    outTree.Branch("ptnn",ptnn,"ptnn/F")
    outTree.Branch("pdgIdl1",pdgIdl1,"pdgIdl1/F")
    outTree.Branch("pdgIdl2",pdgIdl2,"pdgIdl2/F")
    outTree.Branch("dRll",dRll,"dRll/F")


    evt=0.0; passed=0.0;
    for ev in t_ex0:
        leptons=[];sorted_leptons=[];   sorted_nuel=[];  nuel=[]; numu=[]; sorted_numu=[];
        evt+=1
        if(evt%200000 == 0):            print 'processed %f out of %f events' %(evt,t_ex0.GetEntries())
        for i in range(ev.nGenPart_sel):
            if (abs(ev.GenPart_sel_pdgId[i]) in [11,13]):
                info={'pdgId':ev.GenPart_sel_pdgId[i],'pt':ev.GenPart_sel_pt[i],'eta':ev.GenPart_sel_eta[i],'phi':ev.GenPart_sel_phi[i],'mass':ev.GenPart_sel_mass[i]}
                leptons.append(info)
                #print info
            if (abs(ev.GenPart_sel_pdgId[i]) == 12):
                info={'pdgId':ev.GenPart_sel_pdgId[i],'pt':ev.GenPart_sel_pt[i],'eta':ev.GenPart_sel_eta[i],'phi':ev.GenPart_sel_phi[i],'mass':ev.GenPart_sel_mass[i]}
                #print info
                nuel.append(info)
            if (abs(ev.GenPart_sel_pdgId[i]) == 14):
                info={'pdgId':ev.GenPart_sel_pdgId[i],'pt':ev.GenPart_sel_pt[i],'eta':ev.GenPart_sel_eta[i],'phi':ev.GenPart_sel_phi[i],'mass':ev.GenPart_sel_mass[i]}
                #print info
                numu.append(info)


            
        sorted_leptons= sorted(leptons, key = lambda i: i['pt'],reverse=True)
        sorted_nuel= sorted(nuel, key = lambda i: i['pt'],reverse=True)
        sorted_numu= sorted(numu, key = lambda i: i['pt'],reverse=True)

        basesel= len(leptons) > 1 and len(sorted_nuel) > 0 and  len(sorted_numu) > 0 
        if not basesel : continue
        #print sorted_leptons,sorted_quarks,neutrinos
        DRll=dilepVars(sorted_leptons[0]['pt'],sorted_leptons[0]['eta'],sorted_leptons[0]['phi'],sorted_leptons[1]['pt'],sorted_leptons[1]['eta'],sorted_leptons[1]['phi'],'dR')
        MET=dilepVars(sorted_nuel[0]['pt'],sorted_nuel[0]['eta'],sorted_nuel[0]['phi'],sorted_numu[0]['pt'],sorted_numu[0]['eta'],sorted_numu[0]['phi'],'pt')

        passed+=1
        dRll[0]=DRll
        mll[0]    = dilepVars(sorted_leptons[0]['pt'],sorted_leptons[0]['eta'],sorted_leptons[0]['phi'],sorted_leptons[1]['pt'],sorted_leptons[1]['eta'],sorted_leptons[1]['phi'],'M')

        if(abs(sorted_leptons[0]['pdgId']) == 11):
                    etael[0]=sorted_leptons[0]['eta']
                    ptel[0]=sorted_leptons[0]['pt']
                    mW1[0]= dilepVars(sorted_leptons[0]['pt'],sorted_leptons[0]['eta'],sorted_leptons[0]['phi'],sorted_nuel[0]['pt'],sorted_nuel[0]['eta'],sorted_nuel[0]['phi'],'M')
        else:
                    etamu[0]=sorted_leptons[0]['eta']
                    ptmu[0]=sorted_leptons[0]['pt']
                    mW1[0]= dilepVars(sorted_leptons[0]['pt'],sorted_leptons[0]['eta'],sorted_leptons[0]['phi'],sorted_numu[0]['pt'],sorted_numu[0]['eta'],sorted_numu[0]['phi'],'M')

        if(abs(sorted_leptons[1]['pdgId']) == 11):
                    etael[0]=sorted_leptons[1]['eta']
                    ptel[0]=sorted_leptons[1]['pt']
                    mW2[0]= dilepVars(sorted_leptons[1]['pt'],sorted_leptons[1]['eta'],sorted_leptons[1]['phi'],sorted_nuel[0]['pt'],sorted_nuel[0]['eta'],sorted_nuel[0]['phi'],'M')
        else:
                    etamu[0]=sorted_leptons[1]['eta']
                    ptmu[0]=sorted_leptons[1]['pt']
                    mW2[0]= dilepVars(sorted_leptons[1]['pt'],sorted_leptons[1]['eta'],sorted_leptons[1]['phi'],sorted_numu[0]['pt'],sorted_numu[0]['eta'],sorted_numu[0]['phi'],'M')

        nleps[0]=len(sorted_leptons)
        etal1[0]=sorted_leptons[0]['eta']
        ptl1[0]=sorted_leptons[0]['pt']
        pdgIdl1[0]=sorted_leptons[0]['pdgId']
        etal2[0]=sorted_leptons[1]['eta']
        pdgIdl2[0]=sorted_leptons[1]['pdgId']
        ptl2[0]=sorted_leptons[1]['pt']
        detall[0]=dilepVars(sorted_leptons[0]['pt'],sorted_leptons[0]['eta'],sorted_leptons[0]['phi'],sorted_leptons[1]['pt'],sorted_leptons[1]['eta'],sorted_leptons[1]['phi'],'deta')
        dphill[0]=dilepVars(sorted_leptons[0]['pt'],sorted_leptons[0]['eta'],sorted_leptons[0]['phi'],sorted_leptons[1]['pt'],sorted_leptons[1]['eta'],sorted_leptons[1]['phi'],'dphi')
        ptnn[0] = MET
        outTree.Fill()

    print 'passed{%f} out of {%f} events' %(passed,t_ex0.GetEntries())
    outTree.Write()
    fout.Write()
    fout.Close()
    return 1

    
if __name__ == '__main__':
    parser = OptionParser(usage="usage: %prog [options] in.root  \nrun with --help to get list of options")
    parser.add_option('-i', '--infile'  , dest='infile'     , default=''        , type='string', help='file with tree')
    parser.add_option('-o', '--outdir'  , dest='outdir'     , default=''        , type='string', help='file with tree')
    (options, args) = parser.parse_args()
    #infile = options.infile
    starttime = time.time()
    if options.outdir not in os.listdir(os.getcwd()):
        os.system('mkdir {HERE}'.format(HERE=options.outdir))

    fillmllHist(options.infile,options.outdir)                
    print('That took {} seconds'.format(time.time() - starttime))
