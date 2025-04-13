import ROOT, os, optparse, copy, re, sys, datetime

date = datetime.date.today().isoformat() #"2021-11-29" #
import numpy as np
import array
from array import array
import math
ROOT.gROOT.SetBatch();ROOT.gStyle.SetOptStat(0);    ROOT.gStyle.SetOptTitle(0)
varname='mWV'
def hStyle(hist,color,xtitle,ytitle="Events",xtoff=1.02,lstyle=1,xloff=0.007,ytoff=0.88,tsize=0.04,lsize=0.035, mstyle=22,msize=0.85,fStyle=0,lwidth=2):

    hist.GetXaxis().SetTitleOffset(xtoff);             hist.GetYaxis().SetTitleOffset(ytoff)
    hist.GetXaxis().SetTitle(xtitle);                  hist.GetYaxis().SetTitle(ytitle);
    hist.GetXaxis().SetLabelSize(lsize);              hist.GetYaxis().SetLabelSize(lsize);
    hist.GetXaxis().SetTitleSize(tsize);              hist.GetYaxis().SetTitleSize(tsize);
    hist.GetXaxis().SetTitleFont(42);            hist.GetYaxis().SetTitleFont(42);
    hist.GetXaxis().SetLabelFont(42);            hist.GetYaxis().SetLabelFont(42);
    hist.SetLineColor(color);hist.SetLineWidth(lwidth);
    hist.GetXaxis().SetLabelOffset(xloff); hist.SetFillStyle(fStyle);
    if mstyle != '':
        hist.SetMarkerStyle(mstyle); hist.SetMarkerColor(color); hist.SetMarkerSize(msize);
    return hist

def createOutdir(outDir):
    if outDir and not os.path.exists(outDir):
        os.makedirs(outDir)
        os.system('cp /afs/cern.ch/user/a/anmehta/public/index.php {od}'.format(od=outDir))

def get1DBinning(hist):
    xaxis=hist.GetXaxis();nbinsX=hist.GetNbinsX();
    xbinlow=xaxis.GetBinLowEdge(1);xbinhigh=xaxis.GetBinLowEdge(nbinsX+1);    
    return nbinsX,xbinlow,xbinhigh

def getLine(hist):
    nbinsX,xbinlow,xbinhigh=get1DBinning(hist)
    line1 = ROOT.TLine(xbinlow,1.0,xbinhigh,1.0);
    line1.SetLineColor(58);   line1.SetLineWidth(2);   line1.SetLineStyle(1);
    return line1

def getRatiobbb(hNom,hUp,hDn):
    for ibin in range(1,hNom.GetNbinsX()+1):
        nom_content=hNom.GetBinContent(ibin);
        nom_error=hNom.GetBinError(ibin);
        up_content=hUp.GetBinContent(ibin);
        up_error  =hUp.GetBinError(ibin);
        dn_content=hDn.GetBinContent(ibin);
        dn_error  =hDn.GetBinError(ibin);
        h_ratioU = hNom.Clone(); h_ratioD = hNom.Clone();
        h_ratioU.Reset(); h_ratioD.Reset();
        #if(ibin == hNom.GetNbinsX()): print nom_content,nom_error,up_content,up_error,dn_content,dn_error
        if( dn_content > 0 and nom_content >0):
            ratio=(dn_content/nom_content)
            error=ratio*math.sqrt( ( (dn_error/dn_content)**2) + ((nom_error/nom_content)**2));
            print('dn',nom_content,dn_content,ratio,error)
            h_ratioD.SetBinContent(ibin,ratio);
            h_ratioD.SetBinError(ibin,error);
        if( up_content > 0 and nom_content >0):
            ratio=(up_content/nom_content)
            error=ratio*math.sqrt( ( (up_error/up_content)**2) + ((nom_error/nom_content)**2));
            print('up',ratio,error)
            h_ratioU.SetBinContent(ibin,ratio);
            h_ratioU.SetBinError(ibin,error);
        return h_ratioU,h_ratioD

def getPlots(fName,proc,odir):
    filetoread = ROOT.TFile(fName,'read')
    allhists={};NPs=[]
    for key in list(filetoread.GetListOfKeys()):
        cl = ROOT.gROOT.GetClass(key.GetClassName())
        if(cl.InheritsFrom(ROOT.TH1.Class())):
            objectName = key.GetName()
            if objectName.startswith(varname+'_'+proc):
                if 'Up' in objectName or 'Down' in objectName:
                    variation='Up' if 'Up' in objectName else 'Down'
                    #mWV_logy_WW_sm_CMS_pNettag_eff_2018Up
                    NP=objectName.split(varname+'_'+proc)[-1].split(variation)[0]
                    if NP not in NPs and len(NP)>0:
                        #print('this is the NP',NP,'from',objectName)
                        NPs.append(NP)
                        
    allhists[proc]=NPs
    filetoread.Close();
    gethists(fName,NPs,proc,odir)
    return True


def gethists(fName,NPs,proc,odir):
    hists=[];
    filetoread = ROOT.TFile(fName,'read')
    for np in NPs:
        #print(proc,np)
        h_nom=filetoread.Get('%s_%s'%(varname,proc));h_nom.SetDirectory(0)
        h_up=filetoread.Get('%s_%s%sUp'%(varname,proc,np));h_up.SetDirectory(0)
        h_dn=filetoread.Get('%s_%s%sDown'%(varname,proc,np)); h_dn.SetDirectory(0)
        makeCanvas(h_nom,h_up,h_dn,odir,proc,np)
    filetoread.Close();
    return True


def makeCanvas(h_nom,h_up,h_dn,odir,proc,np,nlegcol=3):
    cw=600;ch=600
    canv=ROOT.TCanvas("canv{proc}{np}".format(proc=proc,np=np),"",cw,ch);  
    canv.Range(0,0,1,1);  canv.SetLeftMargin(0.16); canv.SetRightMargin(0.08);  canv.SetBottomMargin(0.13);
    c1_1 = ROOT.TPad("c1_1{proc}{np}".format(proc=proc,np=np),"newpad",0.01,0.33,0.99,0.99); c1_1.Draw();canv.cd();
    c1_2 = ROOT.TPad("c1_2{proc}{np}".format(proc=proc,np=np),"ratioplot",0.01,0.01,0.99,0.33);  c1_2.Draw();c1_1.cd();
    c1_1.SetTopMargin(0.13);c1_1.SetBottomMargin(0.02);
    c1_1.SetRightMargin(0.1); c1_1.SetFillStyle(0);
    c1_2.SetTopMargin(0.055); c1_2.SetBottomMargin(0.3); c1_2.SetRightMargin(0.1);
    leg = ROOT.TLegend(0.15,0.75,0.75,0.86);   leg.SetLineColor(0);
    leg.SetTextFont(42);leg.SetFillColor(0);leg.SetFillStyle(0);leg.SetTextSize(0.045); leg.SetNColumns(nlegcol);

    histograms=[]
    histograms.append(h_up);histograms.append(h_dn);
    h_ratioU = h_up.Clone(); 
    h_ratioD = h_dn.Clone();

    
    #print(h_ratioU.GetBinContent(1),h_ratioD.GetBinContent(1),h_nom.GetBinContent(1),h_ratioU.GetBinError(1),h_ratioD.GetBinError(1),h_nom.GetBinError(1))
    h_ratioU.Divide(h_nom); h_ratioD.Divide(h_nom);
    #h_rup,h_rdn=getRatiobbb(h_nom,h_up,h_dn)
    #for ibin in range(1,h_nom.GetNbinsX()+1):
    #    h_ratioD.SetBinContent(ibin,h_rdn.GetBinContent(ibin));
    #    h_ratioD.SetBinError(ibin,h_rdn.GetBinError(ibin));
    #    h_ratioU.SetBinContent(ibin,h_rup.GetBinContent(ibin));
    #    h_ratioU.SetBinError(ibin,h_rup.GetBinError(ibin));

    ymax=max(list(i.GetMaximum() for i in histograms));      
    ymin=min(list(i.GetMinimum() for i in histograms))
    h_nom=hStyle(h_nom,ROOT.kBlue,xtitle="m_{WV} (GeV)",xloff=99999);
    h_nom.Draw('hist'); h_nom.GetYaxis().SetRangeUser(0,ymax*1.5)
    h_up=hStyle(h_up,ROOT.kGreen+2,xtitle="m_{WV} (GeV) ",xloff=99999,lstyle=3);
    h_dn=hStyle(h_dn,ROOT.kRed,xtitle="m_{WV} (GeV)",xloff=99999,lstyle=5);
    h_up.Draw('histsame');h_dn.Draw('histsame');
    leg.AddEntry(h_nom,'nom','l');    leg.AddEntry(h_up,'up','l');    leg.AddEntry(h_dn,'dn','l')
    leg.Draw('same')
    canv.cd();      c1_2.cd();
    line1=getLine(h_nom)
    h_ratioD=hStyle(h_ratioD,ROOT.kRed,xtitle="m_{WV} (GeV)",ytitle="var/nom",xtoff=0.8,ytoff=0.5,tsize=0.085,lsize=0.08,lwidth=2,mstyle=20,msize=0.5)
    h_ratioU=hStyle(h_ratioU,ROOT.kGreen+2,xtitle="m_{WV} (GeV)",ytitle="var/nom",xtoff=0.8,ytoff=0.5,tsize=0.085,lsize=0.08,lwidth=2,mstyle=20,msize=0.5)
    h_ratioU.GetYaxis().SetRangeUser(0.8,1.2)
    h_ratioU.Draw("p");    h_ratioD.Draw("psame");     line1.Draw("E2SAME");

    canv.SaveAs('{od}/{wz}{mww}_{fs}.pdf'.format(od=outdir,wz=proc,fs=FS,mww=np))
    canv.SaveAs('{od}/{wz}{mww}_{fs}.png'.format(od=outdir,wz=proc,fs=FS,mww=np))
    canv.Close();
    return True

if __name__ == '__main__':
    parser = optparse.OptionParser(usage='usage: %prog [opts] ', version='%prog 1.0')
    parser.add_option('-p','--proc', dest='proc', type='string' , default="WW_sm,WZ_sm,Others,tt,singletop,WJets",help='plots for this proc')
    parser.add_option('-u','--uncert', dest='uncert', type='string' ,default="pileup",help='comma separated uncert srcs')
    parser.add_option('-y','--year', dest='year', type='string' , default="2016,2016APV,2017,2018", help='plots for this year')
    parser.add_option('-f','--fs', dest='fs', type='string' , default="el,mu", help='el/mu')
    parser.add_option('-c','--cr',   dest='cr', type='string' , default="topCR_incl")##,topCR,sig_incl", help='phase space region')
    (opts,args) = parser.parse_args()
    ROOT.gROOT.SetBatch();ROOT.gStyle.SetOptStat(0);    ROOT.gStyle.SetOptTitle(0)

    eosDir="/eos/user/a/anmehta/www/VVsemilep/"
    odir=os.path.join(eosDir,"syst_variations")
    processes = opts.proc.split(',') 
    years = opts.year.split(',')
    finalStates=opts.fs.split(',')
    regions=opts.cr.split(',')
    uncerts=opts.uncert.split(',')

    #regexp_unc = re.compile(opts.uncert.replace(',','|'))
    for yr in years:
        for FS in finalStates:
            for cr in regions:
                for proc in processes:
                    in_file="{eosDir}/{yr}/{crd}/2025-02-04_boosted_{FS}_{cr}_all_eft/{vname}.root".format(eosDir=eosDir,vname=varname,crd=cr.split('_')[0],cr=cr,FS=FS,yr=yr)
                    outdir='{Here}/{yr}/{cr}_{FS}'.format(Here=odir,cr=cr,FS=FS,yr=yr)
                    createOutdir(outdir)
                    getPlots(in_file,proc,outdir)


#/eos/user/a/anmehta/www/VVsemilep/2018/wjCR/2025-02-04_boosted_mu_wjCR_incl_all_eft_withoutTagger
