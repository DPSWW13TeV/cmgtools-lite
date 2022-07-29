import ROOT, os, optparse, copy, re
from ROOT import TCanvas, TFile, TColor, TH1F, TH2F
from ROOT import gROOT, gBenchmark, gRandom, gSystem
import numpy as np
import math
ROOT.gROOT.SetBatch()
ROOT.gStyle.SetOptStat(0)


def drawSLatex(xpos,ypos,text,size):
    latex = ROOT.TLatex()
    latex.SetNDC()
    latex.SetTextAlign(12)
    latex.SetTextSize(size)
    latex.SetTextFont(42)
    latex.DrawLatex(xpos,ypos,text)


processes={
    'DPSWW':[ROOT.kRed+1,"DPS W^{#pm}W^{#pm}"],
    #'Rare':[ROOT.kPink+6,"t#bar{t}W/Z, SPS W^{#pm}W^{#pm}"],
    'Rares':[ROOT.kPink+6,"Rare"],
    'ZZ':[ROOT.kOrange+7,"ZZ"],
    'WZ':[ROOT.kAzure+1,"WZ"],
    'data_fakes':[ROOT.kGray,"Nonprompt"],
    'Wgstar':[ROOT.kViolet+7,"W#gamma*"],
    'data_flips':[ROOT.kCyan-7,"Charge misid."],
    'Convs':[ROOT.kGreen-3,"V#gamma"],
    'VVV':[5,"VVV"],
    'data':[ROOT.kBlack,"Data"],
    'total':[ROOT.kBlue,"total"],
    'total_signal':[ROOT.kRed+1,"tot sig"],
    'total_background':[ROOT.kBlue,"tot bkg"]
}  



xbinlow=0
xbinhigh=13#
nbinsx=xbinhigh-xbinlow
fit="fit_s" #prefit" #fit_b #fit_s
#data->tgraphasym

FS=["elmu_pp","elmu_mm","mumu_pp","mumu_mm"]
#FS=["elmu_pp","elmu_mm"]
histInfo={};
filetoread = ROOT.TFile('fitDiagnostics_data_withoutConvsNorm.root','read')
#dc_2022-02-07_FR2_fitDiagnosticsTest.root','read') 


#chname='ch{year}_{fs}_{yr}'.format(year=yr-2015,yr=yr)
for proc in processes.keys():
    hist=ROOT.TH1D("%s"%proc,"",nbinsx*4,xbinlow,xbinhigh*4); 
    for xval,fs in enumerate(FS):
        if "mumu" in fs and (proc == "data_flips" or proc == "Convs"): continue            
        if proc == "data":hist.Sumw2()        
        
        hist2016=filetoread.Get("shapes_{fit}/ch1_{fs}_2016/{p}".format(fit=fit,fs=fs,p=proc))
        hist2017=filetoread.Get("shapes_{fit}/ch2_{fs}_2017/{p}".format(fit=fit,fs=fs,p=proc))
        hist2018=filetoread.Get("shapes_{fit}/ch3_{fs}_2018/{p}".format(fit=fit,fs=fs,p=proc))
        
        for i in range(1,nbinsx+1):
            if (hist2016.InheritsFrom(ROOT.TH1.Class())):
                yval=0.0;yerr=0.0;
                yval=hist2016.GetBinContent(i)+hist2017.GetBinContent(i)+hist2018.GetBinContent(i)
                yerr=hist2016.GetBinError(i)+hist2017.GetBinError(i)+hist2018.GetBinError(i)
                hist.SetBinContent(i+(xval*nbinsx),yval);                hist.SetBinError(i+(xval*nbinsx),yerr);
            else:
                #print proc
                x = ROOT.Double(0.);   y1 = ROOT.Double(0.);y2 = ROOT.Double(0.);y3 = ROOT.Double(0.)
                hist2016.GetPoint(i-1,x,y1);hist2017.GetPoint(i-1,x,y2);   hist2018.GetPoint(i-1,x,y3)
                hist.SetBinContent(i+(xval*nbinsx),(y1+y2+y3));     hist.SetBinError(i+(xval*nbinsx),math.sqrt(y1+y2+y3));
        
        #print fs, proc,hist.Integral(1+(xval*nbinsx),14+13*xval),sum([hist.GetBinError(x) for x in range(1+(xval*nbinsx),14+13*xval)])
    hist.SetName(proc);
    if proc !="data": 
        hist.SetFillColor(processes[proc][0]); hist.SetLineColor(ROOT.kBlack);hist.SetLineWidth(1);
        if 'fakes' in proc: 
            hist.SetFillStyle(3005);
    else:
        hist.SetFillStyle(0);hist.SetMarkerColor(1);hist.SetMarkerStyle(20);

    hist.SetDirectory(0)
    histInfo[proc]=hist

    
for ip,ih in histInfo.iteritems():
    errAll=[];
    if ip == "total" or ip == "total_signal" : continue
    for i in range(1,histInfo[ip].GetNbinsX()+1):
        errAll.append(histInfo[ip].GetBinError(i))
    print '%-15s   %.3f +/- %.2f'%(ip,histInfo[ip].Integral(),sum(errAll))



Canv = ROOT.TCanvas("Canv","",800,600)
Canv.Range(0,0,1,1);   Canv.SetFillColor(0);   Canv.SetBorderMode(0);  
Canv.SetTickx(1);   Canv.SetTicky(1);   Canv.SetLeftMargin(0.12);   Canv.SetRightMargin(0.05);
Canv.SetBottomMargin(0.13);   Canv.SetFrameFillStyle(0);   Canv.SetFrameBorderMode(0);        
Canv.SetTopMargin(0.1);

legend = ROOT.TLegend(0.3,0.625,0.8,0.88);
legend.SetNColumns(3);legend.SetFillColor(0);legend.SetFillStyle(0); legend.SetShadowColor(0);   legend.SetLineColor(0);
legend.SetTextFont(42);  legend.SetBorderSize(0);   legend.SetTextSize(0.045);
hs=ROOT.THStack("hs",""); 

#print 'this is what i got',histInfo.keys() #all processes for three years added





histtotbkg=histInfo['total_background'] #histtotbkg=histInfo['bkg']
histdata=histInfo['data']##histInfo['obs'] 

histdata.SetMarkerSize(0.7);  
histdata.SetMarkerStyle(20);histdata.SetMarkerColor(1);
histdata.SetLineColor(1);  histdata.SetLineWidth(1);

#hist_rares=ROOT.TH1D("hist_rares","",nbinsx*4,xbinlow,xbinhigh*4);
hist_rares=histInfo['Rares'].Clone("hist_rares");
hist_rares.Add(histInfo['VVV'])

hs.Add(histInfo['data_fakes']);#fakes
hs.Add(histInfo['Convs']);
hs.Add(histInfo['WZ']);#WZ
hs.Add(histInfo['Wgstar']);#Wg*
hs.Add(histInfo['ZZ']);#ZZ
hs.Add(histInfo['data_flips']);
hs.Add(hist_rares)
#hs.Add(histInfo['VVV']);#VVV

#hs.Add(histInfo['Rares']);#rares
hs.Add(histInfo['DPSWW']);#DPS


legend.AddEntry(histInfo['data'],processes['data'][1],"elp");
legend.AddEntry(histInfo['data_fakes'],processes['data_fakes'][1],"f");
legend.AddEntry(histInfo['data_flips'],processes['data_flips'][1],"f");

legend.AddEntry(histInfo['WZ'],processes['WZ'][1],"f");
legend.AddEntry(histInfo['Wgstar'],processes['Wgstar'][1],"f");
legend.AddEntry(histInfo['Convs'],processes['Convs'][1],"f");
legend.AddEntry(histInfo['ZZ'],processes['ZZ'][1],"f");
#legend.AddEntry(histInfo['VVV'],processes['VVV'][1],"f");            
legend.AddEntry(hist_rares,processes['Rares'][1],"f");            
#legend.AddEntry(histInfo['Rares'],processes['Rares'][1],"f");
## ratio plot
errorData=[]

hist_ratio=histdata.Clone("hist_ratio");hist_ratio.Sumw2();
hist_num=histInfo['total_background'].Clone("hist_num")
#hist_num=histInfo['total'].Clone("hist_num")
hist_ratio.Divide(hist_num);

 
c1_1 = ROOT.TPad("c1_1","ratioplot",0.01,0.01,0.99,0.33);    c1_1.Draw();    c1_1.cd(); #c1_1.SetLogy();
c1_1.SetTopMargin(0.041); c1_1.SetBottomMargin(0.3);   c1_1.SetRightMargin(0.05);c1_1.SetBorderMode(0);c1_1.SetTicky(1);
c1_1.SetBorderSize(2); c1_1.SetFillStyle(0);c1_1.SetFrameBorderMode(0);c1_1.SetFrameLineWidth(2);c1_1.SetFrameBorderMode(0); 
 


line1 = ROOT.TLine(xbinlow,1.0,xbinhigh*4,1.0);    line1.SetLineColor(58);   line1.SetLineWidth(2);   line1.SetLineStyle(1);
 
#shaded uncert band around the ratio plot 
band=ROOT.TH1D("band","",nbinsx*4,xbinlow,xbinhigh*4);    band.SetFillColor(ROOT.kCyan);   band.SetMarkerSize(0); 
band.SetFillStyle(1001);        band.Divide(histtotbkg,histtotbkg,1,1,"b");
signal =histInfo['DPSWW'].Clone();    signal.SetFillColor(0);   signal.SetFillStyle(0);  
signal.SetLineColor(ROOT.kRed+1);   signal.SetLineWidth(2);  


for ibin in range(1,(xbinhigh*4)+1):
    band.SetBinError(ibin,histInfo['total_background'].GetBinError(ibin)/histInfo['total_background'].GetBinContent(ibin) )
    #histtotbkg.GetBinError(ibin)/histtotbkg.GetBinContent(ibin))  
    #signal histogram on the bottom pad

    putit=signal.GetBinContent(ibin)/histtotbkg.GetBinContent(ibin);
    signal.SetBinContent(ibin,1+putit);
#print check
 
band.GetXaxis().SetTitleFont(42);    band.GetXaxis().SetLabelSize(0.11);    band.GetXaxis().SetTitleSize(0.12);
band.GetXaxis().SetTitleOffset(0.95);       band.GetYaxis().SetTitle("Data/bkg.");
band.GetYaxis().SetLabelSize(0.11);    band.GetYaxis().SetTitleSize(0.12);    band.GetYaxis().SetTitleOffset(0.44);
band.GetYaxis().SetRangeUser(0.5,3.0 if fit == "fit_s" else 3.5);     band.GetYaxis().SetNdivisions(607);    ROOT.gStyle.SetErrorX(0.5); 
band.GetXaxis().SetTitle("Bin number");
hist_ratio.SetMarkerStyle(20);   hist_ratio.SetMarkerColor(1);   hist_ratio.SetMarkerSize(0.7);
hist_ratio.SetLineColor(1);  hist_ratio.SetLineWidth(1);



band.Draw("E2SAME");
line1.Draw("LSAMES");
signal.Draw("AHIST][SAME");

hist_ratio.Draw("Ex0SAME"); 

c1_1.Update();
legend1 = ROOT.TLegend(0.32,0.82,0.47,0.93); #,NULL,"brNDC");
legend1.SetTextFont(42);
legend1.SetTextSize(0.09);
legend1.SetFillColor(0);
legend1.SetLineColor(0);
legend1.SetFillStyle(0);
legend1.SetShadowColor(0)
legend1.SetNColumns(1);
legend1.AddEntry(signal,"DPS W^{#pm}W^{#pm}","l");
legend1.Draw("same");
legend2 = ROOT.TLegend(0.55,0.82,0.7,0.93); #,NULL,"brNDC");
legend2.SetTextFont(42);
legend2.SetTextSize(0.09);
legend2.SetFillColor(0);
legend2.SetLineColor(0);
legend2.SetFillStyle(0);
legend2.SetShadowColor(0)
legend2.SetNColumns(1);
legend2.AddEntry(band,"Total background unc.","f");
legend2.Draw("same");
##
Canv.cd();

c1_2 = ROOT.TPad("c1_2", "newpad",0.01,0.33,0.99,0.99);
c1_2.Draw();        c1_2.cd(); #c1_2.SetLogy();
c1_2.SetTopMargin(0.1);  c1_2.SetBottomMargin(0.04);  c1_2.SetRightMargin(0.05);        c1_2.SetFillStyle(0);
c1_2.SetBorderMode(0);        c1_2.SetBorderSize(2);c1_2.SetFrameBorderMode(0);c1_2.SetFrameLineWidth(2);
c1_2.SetFrameBorderMode(0);   c1_2.SetTicky(1);
hs.Draw("HIST");

hs.GetXaxis().SetTitle("Bin Number"); 
hs.GetYaxis().SetTitle("Events");
hs.GetYaxis().SetLabelSize(0.05);    hs.GetYaxis().SetTitleSize(0.055);    hs.GetYaxis().SetTitleOffset(0.98);
#hs.GetXaxis().SetLabelSize(0.045);    hs.GetXaxis().SetTitleSize(0.045);   hs.GetXaxis().SetTitleOffset(0.91);
hs.GetXaxis().SetLabelSize(0.0000001);    hs.GetXaxis().SetTitleSize(0.0000001);   hs.GetXaxis().SetTitleOffset(999);
hs.GetXaxis().SetTitleFont(42);    hs.GetYaxis().SetTitleFont(42);    hs.SetMaximum(600);
#print histdata.Integral()

h_err = histInfo['total'].Clone()
#h_err.SetFillColorAlpha(12, 0.3)  # Set grey colour (12) and alpha (0.3)
#h_err.SetMarkerSize(0)
h_err.SetMarkerStyle(0)
h_err.SetFillStyle(3344);
h_err.SetFillColor(ROOT.kGray+2)
#h_err.SetLineColor(1)#ROOT.kGray+1)

h_err.Draw("PE2 SAME")

histdata.Draw("E SAME");

legend.AddEntry(histInfo['DPSWW'],processes['DPSWW'][1],"f");
legend.AddEntry(h_err,"Total unc.","f");
legend.Draw("same");

line2 = ROOT.TLine(nbinsx,0,nbinsx,400);        line2.SetLineColor(1);   line2.SetLineWidth(1);   line2.SetLineStyle(2);
line3 = ROOT.TLine(nbinsx*2,0,nbinsx*2,400);    line3.SetLineColor(1);   line3.SetLineWidth(1);   line3.SetLineStyle(2);
line4 = ROOT.TLine(nbinsx*3,0,nbinsx*3,400);    line4.SetLineColor(1);   line4.SetLineWidth(1);   line4.SetLineStyle(2);

line2.Draw("lsame")
line3.Draw("lsame");
line4.Draw("lsame");

t2a = drawSLatex(0.1,0.93,"#bf{CMS}",0.045); 
#t2a = drawSLatex(0.1,0.93,"#bf{CMS} #it{Preliminary}",0.05);
t3a = drawSLatex(0.79,0.93,"138 fb^{#minus1} (13 TeV)",0.045);

t4a = drawSLatex(0.6,0.50,"#mu^{#plus}#mu^{#plus}",0.05);
t5a = drawSLatex(0.8,0.50,"#mu^{#minus}#mu^{#minus}",0.05);
t6a = drawSLatex(0.2,0.50,"e^{#plus}#mu^{#plus}",0.05);
t7a = drawSLatex(0.4,0.50,"e^{#minus}#mu^{#minus}",0.05);


Canv.Update();
    
Canv.Print("/afs/cern.ch/work/a/anmehta/public/run2_dpsww_AN/paper_run2/SMP-21-013/Figure_002.pdf")
Canv.Print("/afs/cern.ch/work/a/anmehta/public/run2_dpsww_AN/paper_run2/SMP-21-013/Figure_002.png")

#Canv.Print("/afs/cern.ch/work/a/anmehta/public/run2_dpsww_AN/PAS/SMP-21-013/Figure_002.pdf") 
#Canv.Print("/afs/cern.ch/work/a/anmehta/public/run2_dpsww_AN/PAS/SMP-21-013/Figure_002.png") 
#Canv.Print("/eos/user/a/anmehta/www/DPSWW_v2/10feb/superplot_%s_withratio"%fit + '.pdf')
#Canv.Print("/eos/user/a/anmehta/www/DPSWW_v2/10feb/superplot_%s_withratio"%fit + '.png')

        
