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
    #'Rares':[ROOT.kPink+6,"t#bar{t}W/Z, SPS W^{#pm}W^{#pm}"],
    'Rares':[ROOT.kPink+6,"Rares"],
    'ZZ':[ROOT.kOrange-3,"ZZ"],
    'WZ':[ROOT.kAzure+1,"WZ"],
    'data_fakes':[ROOT.kGray,"Nonprompt"],
    'Wgstar':[ROOT.kViolet+7,"W#gamma*"],
    'data_flips':[ROOT.kCyan-7,"Charge misid."],
    'Convs':[ROOT.kGreen-3,"W/Z#gamma"],
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

FS=["mumu_pp","mumu_mm","elmu_pp","elmu_mm"]
#FS=["elmu_pp","elmu_mm"]
histInfo={};
filetoread = ROOT.TFile('fitDiagnostics.root','read') #fitDiagnostics_data_withoutConvsNorm.root','read')
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
        hist.SetFillColor(processes[proc][0]); hist.SetLineColor(ROOT.kBlack);
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
    print '%-15s   %.3f pm %.2f'%(ip,histInfo[ip].Integral(),sum(errAll))



Canv = ROOT.TCanvas("Canv","",600,600)
Canv.Range(0,0,1,1);   Canv.SetFillColor(0);   Canv.SetBorderMode(0);  
Canv.SetTickx(1);   Canv.SetTicky(1);   Canv.SetLeftMargin(0.15);   Canv.SetRightMargin(0.1);
Canv.SetBottomMargin(0.13);   Canv.SetFrameFillStyle(0);   Canv.SetFrameBorderMode(0);        

legend = ROOT.TLegend(0.2,0.65,0.86,0.88);
legend.SetNColumns(3);legend.SetFillColor(0);legend.SetFillStyle(0); legend.SetShadowColor(0);   legend.SetLineColor(0);
legend.SetTextFont(42);  legend.SetBorderSize(0);   legend.SetTextSize(0.035);
hs=ROOT.THStack("hs",""); 

#print 'this is what i got',histInfo.keys() #all processes for three years added





histtotbkg=histInfo['total_background'] #histtotbkg=histInfo['bkg']
histdata=histInfo['data']##histInfo['obs'] 

histdata.SetMarkerSize(0.8);  
histdata.SetMarkerStyle(20);histdata.SetMarkerColor(1);
histdata.SetLineColor(1);  histdata.SetLineWidth(1);


hs.Add(histInfo['data_fakes']);#fakes

hs.Add(histInfo['Convs']);
hs.Add(histInfo['WZ']);#WZ
hs.Add(histInfo['Wgstar']);#Wg*
hs.Add(histInfo['ZZ']);#ZZ
hs.Add(histInfo['VVV']);#VVV
hs.Add(histInfo['data_flips']);
hs.Add(histInfo['Rares']);#rares
hs.Add(histInfo['DPSWW']);#DPS


legend.AddEntry(histInfo['data'],processes['data'][1],"elp");
legend.AddEntry(histInfo['data_fakes'],processes['data_fakes'][1],"f");
legend.AddEntry(histInfo['data_flips'],processes['data_flips'][1],"f");

legend.AddEntry(histInfo['WZ'],processes['WZ'][1],"f");
legend.AddEntry(histInfo['Wgstar'],processes['Wgstar'][1],"f");
legend.AddEntry(histInfo['DPSWW'],processes['DPSWW'][1],"f");
legend.AddEntry(histInfo['ZZ'],processes['ZZ'][1],"f");
legend.AddEntry(histInfo['VVV'],processes['VVV'][1],"f");            
legend.AddEntry(histInfo['Rares'],processes['Rares'][1],"f");
## ratio plot
errorData=[]

hist_ratio=histdata.Clone("hist_ratio");hist_ratio.Sumw2();
hist_num=histInfo['total_background'].Clone("hist_num")
hist_ratio.Divide(hist_num);

 
#c1_1 = ROOT.TPad("c1_1","ratioplot",0.01,0.01,0.99,0.33);    c1_1.Draw();    c1_1.cd();
#c1_1.SetTopMargin(0.041); c1_1.SetBottomMargin(0.3);   c1_1.SetRightMargin(0.1);c1_1.SetBorderMode(0);c1_1.SetTicky(1);
#c1_1.SetBorderSize(2); c1_1.SetFillStyle(0);c1_1.SetFrameBorderMode(0);c1_1.SetFrameLineWidth(2);c1_1.SetFrameBorderMode(0); 
 

#line1 = ROOT.TLine(xbinlow,1.0,xbinhigh*4,1.0);    line1.SetLineColor(58);   line1.SetLineWidth(2);   line1.SetLineStyle(1);
line1 = ROOT.TLine(xbinlow,0.0,xbinhigh*4,0.0);    line1.SetLineColor(58);   line1.SetLineWidth(2);   line1.SetLineStyle(1);
 
#shaded uncert band around the ratio plot 
#band=ROOT.TH1D("band","",nbinsx*4,xbinlow,xbinhigh*4);    band.SetFillColor(ROOT.kCyan);   band.SetMarkerSize(0); 
#band.SetFillStyle(1001);        band.Divide(histtotbkg,histtotbkg,1,1,"b");
#signal =histInfo['DPSWW'].Clone();    signal.SetFillColor(0);   signal.SetFillStyle(0);  
#signal.SetLineColor(ROOT.kRed+1);   signal.SetLineWidth(2);  
#pull=ROOT.TH1D("pull","",nbinsx*4,xbinlow,xbinhigh*4);
#pull.SetLineColor(ROOT.kRed+1); pull.SetLineWidth(2); 
#check=0.0
#for ibin in range(1,(xbinhigh*4)+1):
#    band.SetBinError(ibin,histInfo['total'].GetBinError(ibin)/histInfo['total'].GetBinContent(ibin) )
#    #histtotbkg.GetBinError(ibin)/histtotbkg.GetBinContent(ibin))  
#    num=histdata.GetBinContent(ibin)-histInfo['total_background'].GetBinContent(ibin)
#    deno=math.sqrt(histdata.GetBinError(ibin)**2 + histInfo['total_background'].GetBinError(ibin))
#    pull_val=float(num)/float(deno) #,num,deno
#    #print pull_val
#    check+=pull_val
#    #signal histogram on the bottom pad
#    pull.SetBinContent(ibin,pull_val)
#    putit=signal.GetBinContent(ibin)/histtotbkg.GetBinContent(ibin);
#    signal.SetBinContent(ibin,1+putit);
#print check
 
 
 
#pull.GetXaxis().SetTitleFont(42);    pull.GetXaxis().SetLabelSize(0.11);    pull.GetXaxis().SetTitleSize(0.12);
#pull.GetXaxis().SetTitleOffset(0.95);    
#pull.GetYaxis().SetTitle("Pull"); #Data/bkg.");
#pull.GetYaxis().SetLabelSize(0.11);    pull.GetYaxis().SetTitleSize(0.12);    pull.GetYaxis().SetTitleOffset(0.44);
#pull.GetYaxis().SetRangeUser(-3.5,3.5);    pull.GetYaxis().SetNdivisions(607);    ROOT.gStyle.SetErrorX(0.5);
#hist_ratio.SetMarkerStyle(20);   hist_ratio.SetMarkerColor(1);   hist_ratio.SetMarkerSize(1);
#hist_ratio.SetLineColor(1);  hist_ratio.SetLineWidth(1);


#pull.Draw("HIST][SAME");
#band.Draw("E2SAME");
#line1.Draw("LSAMES");
#signal.Draw("AHIST][SAME");

#hist_ratio.Draw("Ex0SAME"); 

#c1_1.Update();
#legend1 = ROOT.TLegend(0.27,0.69,0.42,0.93); #,NULL,"brNDC");
#legend1.SetTextFont(42);
#legend1.SetTextSize(0.09);
#legend1.SetFillColor(0);
#legend1.SetLineColor(0);
#legend1.SetFillStyle(0);
#legend1.AddEntry(band,"Total background uncertainty","f");
#legend1.AddEntry(signal,"DPS W^{#pm}W^{#pm}","l");
#legend1.Draw("same");

##
#Canv.cd();

hs.Draw("HIST");
#pull.GetXaxis().SetTitle("Bin Number"); 
hs.GetXaxis().SetTitle("Bin Number"); 
hs.GetYaxis().SetTitle("Events");
hs.GetYaxis().SetLabelSize(0.04);    hs.GetYaxis().SetTitleSize(0.045);    hs.GetYaxis().SetTitleOffset(1.2);
hs.GetXaxis().SetLabelSize(0.04);    hs.GetXaxis().SetTitleSize(0.045);   hs.GetXaxis().SetTitleOffset(0.91);
#hs.GetXaxis().SetLabelSize(0.0000001);    hs.GetXaxis().SetTitleSize(0.0000001);   hs.GetXaxis().SetTitleOffset(1.03);
hs.GetXaxis().SetTitleFont(42);    hs.GetYaxis().SetTitleFont(42);    hs.SetMaximum(680);
#print histdata.Integral()

h_err = histInfo['total'].Clone()
#h_err.SetFillColorAlpha(12, 0.3)  # Set grey colour (12) and alpha (0.3)
h_err.SetMarkerSize(0)
h_err.SetFillStyle(3244);
h_err.SetFillColor(ROOT.kGray+2)


histdata.Draw("E SAME");
h_err.Draw("PE2 SAME")
legend.AddEntry(histInfo['Convs'],processes['Convs'][1],"f");
legend.AddEntry(h_err,"Total unc.","f");
legend.Draw("same");
#legend3.Draw("same");
line2 = ROOT.TLine(nbinsx,0,nbinsx,450);        line2.SetLineColor(1);   line2.SetLineWidth(1);   line2.SetLineStyle(2);
line3 = ROOT.TLine(nbinsx*2,0,nbinsx*2,450);    line3.SetLineColor(1);   line3.SetLineWidth(1);   line3.SetLineStyle(2);
line4 = ROOT.TLine(nbinsx*3,0,nbinsx*3,450);    line4.SetLineColor(1);   line4.SetLineWidth(1);   line4.SetLineStyle(2);

line2.Draw("lsame")
line3.Draw("lsame");
line4.Draw("lsame");

t2a = drawSLatex(0.16,0.92,"#bf{CMS} #it{Preliminary}",0.045);
t3a = drawSLatex(0.6,0.92,"138 fb^{#minus1} (13 TeV)",0.045);

t4a = drawSLatex(0.2,0.50,"#mu^{#plus}#mu^{#plus}",0.045);
t5a = drawSLatex(0.4,0.50,"#mu^{#minus}#mu^{#minus}",0.045);
t6a = drawSLatex(0.6,0.50,"e^{#plus}#mu^{#plus}",0.045);
t7a = drawSLatex(0.8,0.50,"e^{#minus}#mu^{#minus}",0.045);


Canv.Update();
    
#Canv.Print("/afs/cern.ch/work/a/anmehta/public/run2_dpsww_AN/paper_run2/SMP-21-013/Figure_002.pdf")
#Canv.Print("/afs/cern.ch/work/a/anmehta/public/run2_dpsww_AN/paper_run2/SMP-21-013/Figure_002.png")

    
#Canv.Print("/eos/user/a/anmehta/www/DPSWW_v2/10feb/superplot_%s_ordered"%fit + '.pdf')
#Canv.Print("/eos/user/a/anmehta/www/DPSWW_v2/10feb/superplot_%s_ordered"%fit + '.png')
        
#    FS={
#        #'mpp':[outname,ymaxstack,xlabel,xvalue],
#        'mpp':['mpp',200,"Bin number (#mu^{#plus}#mu^{#plus})",{'2016':39,'2017':145,'2018':251}],
#        'mmm':['mmm',120,"Bin number (#mu^{#minus}#mu^{#minus})",{'2016':26,'2017':132,'2018':238}],
#        'epp':['epp',370,"Bin number (e^{#plus}#mu^{#plus})",{'2016':13,'2017':119,'2018':225}],
#        'emm':['emm',280,"Bin number (e^{#minus}#mu^{#minus})",{'2016':0,'2017':106,'2018':212}]
#        }
#    histsWithFS={}
#    for proc,hist in histInfo.iteritems():
#        for fs,bn in FS.iteritems():
#            yvals=[];yerr=[]
#            for yr,iB in bn[3].iteritems():
#                for i in range(iB,iB+14):
#                    yvals.append(hist.GetBinContent(iB));yerr.append(hist.GetBinError(iB));
#                ikey=proc+"_fs"+fs+"_yr"+yr
#                histsWithFS[ikey]=zip(yvals,yerr)

    #for ikey,iVals in merged_dictionary.items(): 
    #    print ikey
    #    for i in iVals:
    #        print i

#In [41]: for yr,ib in years.iteritems():
#    ...: 
#    ...:     for proc,hist in histInfo.iteritems():
#    ...:         sub={}
#    ...:         yvals=[];yerr=[]
#    ...:         for i in range(ib[0],ib[1]+1):
#    ...:             yvals.append(hist.GetBinContent(i));yerr.append(hist.GetBinError(i));
#    ...:         #sub[proc]=zip(yvals,yerr)
#    ...:         sub={proc:zip(yvals,yerr)}    
#    ...:         #print sub.keys()
#    ...:         info[yr].append(sub)
#    ...:                        
#    ...:     
#years={'2016':(0,52),
#       '2017':(106,158),
#       '2018':(212,264)}

#FS={
#    'mumu_pp':['mpp',500,"Bin number (#mu^{#plus}#mu^{#plus})",{'2016':39,'2017':145,'2018':251}],
#    'mumu_mm':['mmm',300,"Bin number (#mu^{#minus}#mu^{#minus})",{'2016':26,'2017':132,'2018':238}],
#    'elmu_pp':['epp',500,"Bin number (e^{#plus}#mu^{#plus})",{'2016':13,'2017':119,'2018':225}],
#    'elmu_mm':['emm',600,"Bin number (e^{#minus}#mu^{#minus})",{'2016':0,'2017':106,'2018':212}]
#}

