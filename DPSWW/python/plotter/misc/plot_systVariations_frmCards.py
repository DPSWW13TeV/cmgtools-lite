import ROOT, os, optparse, copy, re, sys, datetime

date = datetime.date.today().isoformat() #"2021-11-29" #
import numpy as np
import array
from array import array
import math
ROOT.gROOT.SetBatch();ROOT.gStyle.SetOptStat(0);    ROOT.gStyle.SetOptTitle(0)

def hStyle(hist,color,xtitle,ytitle="Events",xloff=0.007,xtoff=1.02,ytoff=0.88,tsize=0.04,lsize=0.035,lstyle=1,lwidth=1,mstyle='',msize=0.85,fStyle=0):
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
def getAllhists(fName):
    filetoread = ROOT.TFile(fName,'read')
    allhists={};
    for key in list(filetoread.GetListOfKeys()):
        cl = ROOT.gROOT.GetClass(key.GetClassName())
        if(cl.InheritsFrom(ROOT.TH1.Class())):
            objectName = key.GetName()
            if objectName not in allhists:
                histogram=filetoread.Get(objectName)
                allhists[objectName]=histogram
                histogram.SetDirectory(0)
                #print objectName,histogram.Integral()
                #print type(objectName),objectName,type(filetoread.Get(objectName))
    filetoread.Close();
    return allhists

def gethists(aH,proc):
    hists=[];
    for hN,ihist in aH.iteritems():
        if proc in hN:
            np=hN.split('x_%s_'%proc)[-1].split('Up')[0].split('Down')[0]
            hists.append(np)
    return hists #first is the nominal and then we have name of the NPs


def getCanv(cw=600,ch=600,nlegcol=3):
          canv=ROOT.TCanvas("canv","",cw,ch); 
          canv.Range(0,0,1,1);  canv.SetLeftMargin(0.16); canv.SetRightMargin(0.08);  canv.SetBottomMargin(0.13);
          c1_1 = ROOT.TPad("c1_1","newpad",0.01,0.33,0.99,0.99); c1_1.Draw();canv.cd()
          c1_2 = ROOT.TPad("c1_2","ratioplot",0.01,0.01,0.99,0.33);  c1_2.Draw();c1_1.cd();
          c1_1.SetTopMargin(0.13);c1_1.SetBottomMargin(0.02);
          c1_1.SetRightMargin(0.1); c1_1.SetFillStyle(0);
          c1_2.SetTopMargin(0.055); c1_2.SetBottomMargin(0.3); c1_2.SetRightMargin(0.1);
          leg = ROOT.TLegend(0.15,0.75,0.75,0.86);   leg.SetLineColor(0);
          leg.SetTextFont(42);leg.SetFillColor(0);leg.SetFillStyle(0);leg.SetTextSize(0.045); leg.SetNColumns(nlegcol);
          return canv,c1_1,c1_2,leg

def getRatiobbb(hNom,hUp,hDn):
    for ibin in range(1,hNom.GetNbinsX()+1):
        nom_content=hNom.GetBinContent(ibin);
        nom_error=hNom.GetBinError(ibin);
        up_content=hUp.GetBinContent(ibin);
        up_error  =hUp.GetBinError(ibin);
        dn_content=hDn.GetBinContent(ibin);
        dn_error  =hDn.GetBinError(ibin);
        h_ratioU = h_nom.Clone(); h_ratioD = h_nom.Clone();
        h_ratioU.Reset("ICES"); h_ratioD.Reset("ICES");
        #if(ibin == hNom.GetNbinsX()): print nom_content,nom_error,up_content,up_error,dn_content,dn_error
        if( dn_content > 0 and nom_content >0):
            ratio=(nom_content/dn_content)
            error=ratio*math.sqrt( ( (dn_error/dn_content)**2) + ((nom_error/nom_content)**2));
            h_ratioD.SetBinContent(ibin,ratio);
            h_ratioD.SetBinError(ibin,error);
        if( up_content > 0 and nom_content >0):
            ratio=(up_content/nom_content)
            error=ratio*math.sqrt( ( (up_error/up_content)**2) + ((nom_error/nom_content)**2));
            h_ratioU.SetBinContent(ibin,ratio);
            h_ratioU.SetBinError(ibin,error);
        return h_ratioU,h_ratioD

if __name__ == '__main__':
    parser = optparse.OptionParser(usage='usage: %prog [opts] ', version='%prog 1.0')
    parser.add_option('-p','--proc', dest='proc', type='string' , default="DPSWW,ZZ",help='plots for this proc')
    parser.add_option('-u','--uncert', dest='uncert', type='string' ,default="pileup",help='comma separated uncert srcs')
    parser.add_option('-y','--year', dest='year', type='string' , default="2016,2017,2018", help='plots for this year')
    parser.add_option('-f','--fs', dest='fs', type='string' , default="elmu,mumu", help='elmu/mumu/cr3l/cr4l')
    parser.add_option('--splitcharge',dest='splitcharge', action='store_true' , default=False , help='2lss with chargesplit')
    #parser.add_option("-u", "--uncert",    type=str, default=".*pileup.*", help="Comma separated list of regular expressions to select uncertainties to plot ratios for")
    (opts,args) = parser.parse_args()
    ROOT.gROOT.SetBatch();ROOT.gStyle.SetOptStat(0);    ROOT.gStyle.SetOptTitle(0)
    ROOT.PyConfig.IgnoreCommandLineOptions

    eosDir="/eos/user/a/anmehta/www/DPSWW_v2/"

    processes = opts.proc.split(',') 
    years = opts.year.split(',')
    finalStates=opts.fs.split(',')
    uncerts=opts.uncert.split(',')
    
    #regexp_unc = re.compile(opts.uncert.replace(',','|'))
    charges= ['minusminus', 'plusplus'] if opts.splitcharge else ['']
    #['DPSWW']#,'WZ','ZG','WG','Rares','Wgstar','ZZ','VVV','data_fakes','data_flips']
    binningScheme={'cr3l':'m3l',
                   'cr4l':'m3l',
                   'mumu':'SoBord_sqV3',
                   'elmu':'SoBord_sqV3',
                   ''    :'SoBord_sqV3'}
    for yr in years:
        for FS in finalStates:
            for cc in charges:
                for proc in processes:
                    if FS == "mumu" and  proc in ["data_flips","ZG","WG","Convs"]: continue
                    outdir='{Here}/cards_{bs}'.format(Here=eosDir,bs=binningScheme[FS])
                    createOutdir(outdir)
                    cardstr=binningScheme[FS]+'_{fs}_{y}/{fs}{y}{chg}'.format(y=yr,fs=FS,chg=cc)
                    fName="Cards/cards_{when}-{cstr}.root".format(cstr=cardstr,when=date)
                    allhists=getAllhists(fName)
                    histograms=[];
                    hists=gethists(allhists,proc)
                    h_nom=allhists["x_%s"%proc]
                    histograms.append(h_nom)
                    for np in uncerts:
                        if FS == "mumu" and  np in ["CMS_eff_etight","CMS_eff_eloose"]: continue
                        canv,c1_1,c1_2,leg=getCanv()
                        h_up=allhists["x_%s_%sUp"%(proc,np)];       h_dn=allhists["x_%s_%sDown"%(proc,np)]
                        histograms.append(h_up);histograms.append(h_dn);
                        h_ratioU = h_up.Clone();h_ratioD = h_dn.Clone();
                        print h_ratioU.GetBinContent(1),h_ratioD.GetBinContent(1),h_nom.GetBinContent(1),h_ratioU.GetBinError(1),h_ratioD.GetBinError(1),h_nom.GetBinError(1)
                        h_ratioU.Divide(h_nom); h_ratioD.Divide(h_nom);
                        
                        ymax=max(list(i.GetMaximum() for i in histograms));      
                        ymin=min(list(i.GetMinimum() for i in histograms))
                        h_nom=hStyle(h_nom,ROOT.kBlue,xtitle="#bin",xloff=99999);
                        h_nom.Draw('hist'); 
                        h_up=hStyle(h_up,ROOT.kGreen+2,xtitle="#bin",xloff=99999);
                        h_dn=hStyle(h_dn,ROOT.kRed,xtitle="#bin",xloff=99999);
                        h_up.Draw('histsame');h_dn.Draw('histsame');
                        leg.AddEntry(h_nom,'nom','l');    leg.AddEntry(h_up,'up','l');    leg.AddEntry(h_dn,'dn','l')
                        leg.Draw('same')
                        canv.cd();      c1_2.cd();
                        line1=getLine(h_nom)
                        h_ratioD=hStyle(h_ratioD,ROOT.kRed,xtitle="#bin",ytitle="var/nom",xtoff=0.8,ytoff=0.5,tsize=0.085,lsize=0.08,lwidth=2,mstyle=20,msize=0.5)
                        h_ratioU=hStyle(h_ratioU,ROOT.kGreen+2,xtitle="#bin",ytitle="var/nom",xtoff=0.8,ytoff=0.5,tsize=0.085,lsize=0.08,lwidth=2,mstyle=20,msize=0.5)
                        
                        h_ratioU.Draw("p");    h_ratioD.Draw("psame");     line1.Draw("E2SAME");
                        
                        canv.SaveAs('{od}/{wz}_{mww}_{fs}{y}{chg}_{when}.pdf'.format(when=date,od=outdir,wz=proc,y=yr,fs=FS,chg=cc,mww=np))
                        canv.SaveAs('{od}/{wz}_{mww}_{fs}{y}{chg}_{when}.png'.format(when=date,od=outdir,wz=proc,y=yr,fs=FS,chg=cc,mww=np))



#if ROOT.gROOT.GetListOfCanvases().FindObject("canv"): ROOT.gROOT.GetListOfCanvases().FindObject("canv").Delete()
#if ROOT.gROOT.FindObject("h_nom"): ROOT.gROOT.FindObject("h_nom").Delete()
#if ROOT.gROOT.FindObject("h_up"): ROOT.gROOT.FindObject("h_up").Delete()   
#if ROOT.gROOT.FindObject("h_dn"): ROOT.gROOT.FindObject("h_dn").Delete()

#python plot_systVariations_frmCards.py --splitcharge -p ZZ,DPSWW,Rares,VVV,Convs -u leptonid_etight,pileup -y 2017 -f elmu
