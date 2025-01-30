import ROOT, os, optparse, copy, re
from ROOT import TCanvas, TFile, TColor, TH1F, TH2F
from ROOT import gROOT, gBenchmark, gRandom, gSystem
import numpy as np
from array import array 
import math
ROOT.gROOT.SetBatch()
ROOT.gStyle.SetOptStat(0)


lumis = {
    '2016APV'     : '19.5', #with HIPM /pre-vfp
    '2016'        : '16.8', #without HIPM
    '2017'        : '41.5',
    '2018'        : '59.8',
    'all'         : '19.5,16.8,41.5,59.8',
    'fullRun2'    : '19.5,16.8,41.5,59.8',
}
def drawSLatex(xpos,ypos,text,size):
    latex = ROOT.TLatex()
    latex.SetNDC()
    latex.SetTextAlign(12)
    latex.SetTextSize(size)
    latex.SetTextFont(42)
    latex.DrawLatex(xpos,ypos,text)


processes={
    'Others':[ROOT.TColor.GetColor("\#964a8b"),"Others"],
    'WJets':[ROOT.TColor.GetColor("\#5790fc"),"WJets"],
    'WW_sm':[ROOT.TColor.GetColor("\#ffa90e"),"WW"],
    'WZ_sm':[ROOT.TColor.GetColor("\#e42536"),"WZ"],
    'singletop':[ROOT.TColor.GetColor("\#9c9ca1"),"S-top"],
    'tt':[ROOT.TColor.GetColor("\#7a21dd"),"tt"],
    'data':[ROOT.kBlack,"Data"],
    'total':[ROOT.kBlue,"total"],
    'total_signal':[ROOT.kRed+1,"tot sig"],
    'total_background':[ROOT.kBlue,"tot bkg"]
}
nice_names={'wj_cr_hi':'m_{SD}^{jet} > 105','wj_cr_lo':'m_{SD}^{jet} < 65','top_cr':'t#bar{t}','wjCR':'W+jets'}

fit="fit_b" #prefit" #fit_b #fit_s

channels={'2016':'ch1','2016APV':'ch2','2017':'ch3','2018':'ch4'}

binning=[950,1050,1150,1250,1350,1450,1550,1650,1750,1900,2100,2300,2500,2700,3000,3300,4550]

def makePlot(CR,FS,yr,logy):
    chan=channels[yr]
    temp=[]
    fstr=''
    if 'top' in CR: 
        fstr='topCR'
    else: fstr='wjCR'
    filetoread = ROOT.TFile.Open('fitDiagnosticsTest_SM_dc_2025-01-21_onelep_%s_%s.root'%(yr,fstr))
    temp.append(filetoread)
    histInfo={};
    #hist = filetoread.Get("shapes_{fit}/{FS}_{CR}_{yr}/WJets".format(FS=FS,CR=CR,yr=yr,fit=fit)); hist.Reset();
    for proc in processes.keys():
        print('looking for',proc,CR,FS,yr,"shapes_{fit}/{FS}_{CR}_{yr}/{p}".format(FS=FS,CR=CR,yr=yr,fit=fit,p=proc))
        if proc == "data":           
            hist = filetoread.Get("shapes_{fit}/{chan}_{FS}_{CR}_{yr}/WJets".format(FS=FS,CR=CR,yr=yr,fit=fit,chan=chan)); hist.Reset();           
            hist.Sumw2()        
        hist_el_temp = filetoread.Get("shapes_{fit}/{chan}_{FS}_{CR}_{yr}/{p}".format(FS=FS,CR=CR,yr=yr,fit=fit,p=proc,chan=chan));   

        if proc != "data":  
            hist=hist_el_temp.Clone(proc);

        yvals=[];yerrs=[];
        for i in range(1,hist.GetNbinsX()+1):
            if not (hist_el_temp.InheritsFrom(ROOT.TH1.Class())):
                x = ROOT.Double(0.);   y1 = ROOT.Double(0.) 
                hist_el_temp.GetPoint(i-1,x,y1);
                yvals.append(y1);yerrs.append(math.sqrt(y1))
            else:
                yvals.append(hist_el_temp.GetBinContent(i)); yerrs.append(hist_el_temp.GetBinError(i));

        for i in range(len(yvals)):
            hist.SetBinContent(i+1,yvals[i]);                   hist.SetBinError(i+1,yerrs[i])
        hist.SetName(proc);hist.SetDirectory(0)
        if proc !="data": 
            #print(proc,hist.Integral(),'color',processes[proc][0])
            hist.SetFillColor(processes[proc][0]); 
            hist.SetLineColor(ROOT.kBlack);hist.SetLineWidth(1);
        else:
            hist.SetFillStyle(0);
            hist.SetMarkerColor(1);
            hist.SetMarkerStyle(20);
        hist.SetDirectory(0);           
        histInfo[proc]=hist
    for ip,ih in histInfo.iteritems():
        errAll=[];
        for i in range(1,hist.GetNbinsX()+1):            
            errAll.append(histInfo[ip].GetBinError(i))
        #print '%-15s   %.3f +/- %.2f'%(ip,histInfo[ip].Integral(),sum(errAll))

    ROOT.gROOT.SetBatch()
    ROOT.gStyle.SetOptStat(0)
    Canv = ROOT.TCanvas("Canv_{yr}_{CR}_{FS}".format(yr=yr,FS=FS,CR=CR),"",800,600)
    Canv.Range(0,0,1,1);   Canv.SetFillColor(0);   Canv.SetBorderMode(0);  
    Canv.SetTickx(1);   Canv.SetTicky(1);   Canv.SetLeftMargin(0.12);   Canv.SetRightMargin(0.05);
    Canv.SetBottomMargin(0.13);   Canv.SetFrameFillStyle(0);   Canv.SetFrameBorderMode(0);        
    Canv.SetTopMargin(0.1);
    
    legend = ROOT.TLegend(0.25,0.625,0.85,0.88);
    legend.SetNColumns(3);legend.SetFillColor(0);legend.SetFillStyle(0); legend.SetShadowColor(0);   legend.SetLineColor(0);
    legend.SetTextFont(42);  legend.SetBorderSize(0);   legend.SetTextSize(0.06);
    hs=ROOT.THStack("hs_{yr}_{CR}_{FS}".format(yr=yr,CR=CR,FS=FS),""); 
    histtotbkg=histInfo['total'] 
    histdata=histInfo['data']
    histdata.SetMarkerSize(0.7);  
    histdata.SetMarkerStyle(20);histdata.SetMarkerColor(1);
    histdata.SetLineColor(1);  histdata.SetLineWidth(1);

    hs.Add(histInfo['Others']);
    #hs.Add(histInfo['singletop']);
    hs.Add(histInfo['WW_sm']);
    hs.Add(histInfo['WZ_sm']);
    if "wj" in CR: 
        hs.Add(histInfo['singletop']);
        hs.Add(histInfo['tt']);
        hs.Add(histInfo['WJets']);
    else:
        hs.Add(histInfo['WJets']);
        hs.Add(histInfo['singletop']);
        hs.Add(histInfo['tt']);
    
    legend.AddEntry(histInfo['data'],processes['data'][1],"elp");
    legend.AddEntry(histInfo['WJets'],processes['WJets'][1],"f");
    legend.AddEntry(histInfo['tt'],processes['tt'][1],"f");
    legend.AddEntry(histInfo['singletop'],processes['singletop'][1],"f");
    legend.AddEntry(histInfo['WZ_sm'],processes['WZ_sm'][1],"f");
    legend.AddEntry(histInfo['WW_sm'],processes['WW_sm'][1],"f");
    legend.AddEntry(histInfo['Others'],processes['Others'][1],"f");
    ## ratio plot
    errorData=[]
    
    hist_ratio=histdata.Clone("hist_ratio_{yr}_{CR}_{FS}".format(yr=yr,CR=CR,FS=FS));
    hist_ratio.Sumw2();
    hist_num=histInfo['total'].Clone("hist_num_{yr}_{CR}_{FS}".format(yr=yr,CR=CR,FS=FS))
    hist_ratio.Divide(hist_num);
    
    #print("now canv time over 1 ")
    c1_1 = ROOT.TPad("c1_1_{yr}_{CR}_{FS}".format(yr=yr,CR=CR,FS=FS),"",0.01,0.01,0.99,0.33);    c1_1.Draw(); 
    c1_1.cd(); 
    #    c1_1.SetLogy(True);
    
    c1_1.SetTopMargin(0.041); c1_1.SetBottomMargin(0.3);   c1_1.SetRightMargin(0.05);c1_1.SetBorderMode(0);c1_1.SetTicky(1);
    c1_1.SetBorderSize(2); c1_1.SetFillStyle(0);c1_1.SetFrameBorderMode(0);c1_1.SetFrameLineWidth(2);c1_1.SetFrameBorderMode(0); 
    
    #print("now canv time over 2 ")
    
    line1 = ROOT.TLine(0,1.0,histdata.GetNbinsX(),1.0);    line1.SetLineColor(58);   line1.SetLineWidth(2);   line1.SetLineStyle(1);
    #print("now canv time over 3 ")
    #shaded uncert band around the ratio plot
    band=histdata.Clone("band_{yr}_{CR}_{FS}".format(yr=yr,CR=CR,FS=FS)); band.Reset();
    band.SetFillColor(ROOT.kCyan);   band.SetMarkerSize(0); 
    band.SetFillStyle(1001);        
    #print("now canv time over 4")
    band.Divide(histtotbkg,histtotbkg,1,1,"b");
    

    for ibin in range(1,histdata.GetNbinsX()+1):
        band.GetXaxis().SetBinLabel(ibin,str(binning[ibin]))
        #band.GetXaxis().SetBinLabel(ibin,str(outbins_labels[ibin-1]))
        if (histInfo['total'].GetBinError(ibin) == 0 or histInfo['total'].GetBinContent(ibin) == 0):
            band.SetBinError(ibin, 1)
            
        else:
            ##print("errors",histInfo['total'].GetBinError(ibin),histInfo['total'].GetBinContent(ibin))
            band.SetBinError(ibin,histInfo['total'].GetBinError(ibin)/histInfo['total'].GetBinContent(ibin) )
    #print("now canv time over 5")
    band.GetXaxis().SetTitleFont(42);    band.GetXaxis().SetLabelSize(0.15);    band.GetXaxis().SetTitleSize(0.15);
    band.GetXaxis().SetTitleOffset(0.95);band.GetYaxis().SetTitle("Data/bkg.");    #    band.GetXaxis().SetMaxDigits(1);
    band.GetYaxis().SetLabelSize(0.135);    band.GetYaxis().SetTitleSize(0.15);    band.GetYaxis().SetTitleOffset(0.31);
    band.GetYaxis().SetRangeUser(0.5,2.0 if fit == "fit_s" else 2.5);      band.GetYaxis().SetNdivisions(607);    ROOT.gStyle.SetErrorX(0.5);     band.GetXaxis().SetTitle("m_{WV} (GeV)");
    hist_ratio.SetMarkerStyle(20);   hist_ratio.SetMarkerColor(1);   hist_ratio.SetMarkerSize(0.7);    hist_ratio.SetLineColor(1);  hist_ratio.SetLineWidth(1);
    #print("now canv time over 6")
    band.Draw("E2SAME");
    line1.Draw("LSAMES");
    hist_ratio.Draw("Ex0SAME"); 

    c1_1.Update();
    #print("now canv time over 7")    
    legend2 = ROOT.TLegend(0.55,0.82,0.7,0.92); #,NULL,"brNDC");
    legend2.SetTextFont(42);
    legend2.SetTextSize(0.12);
    legend2.SetFillColor(0);
    legend2.SetLineColor(0);
    legend2.SetFillStyle(0);
    legend2.SetShadowColor(0)
    legend2.SetNColumns(1);
    legend2.AddEntry(band,"Total background unc.","f");
    legend2.Draw("same");
    
    Canv.cd();
    c1_2 = ROOT.TPad("c1_2_{yr}_{CR}_{FS}".format(yr=yr,CR=CR,FS=FS), "",0.01,0.33,0.99,0.99);
    temp.append(c1_2)
    #print("now canv time over 8")
    c1_2.Draw();        c1_2.cd(); 
    if logy:
        c1_2.SetLogy();
    #print("now canv time over 8x")
    c1_2.SetTopMargin(0.1);  c1_2.SetBottomMargin(0.04);  c1_2.SetRightMargin(0.05);        c1_2.SetFillStyle(0);
    c1_2.SetBorderMode(0);        c1_2.SetBorderSize(2);c1_2.SetFrameBorderMode(0);c1_2.SetFrameLineWidth(2);
    c1_2.SetFrameBorderMode(0);   c1_2.SetTicky(1);
    #print("now canv time over 8xy")

    hs.Draw("HIST");
    max2 = hs.GetHistogram().GetMaximum()*(10 if logy else 1.0)
    hs.GetHistogram().GetYaxis().SetRangeUser(0,max2)

    #print("now canv time over 8z")
    hs.GetXaxis().SetTitle("m_{WV} (GeV)"); 
    hs.GetYaxis().SetTitle("Events");
    hs.GetYaxis().SetLabelSize(0.06);    hs.GetYaxis().SetTitleSize(0.075);    hs.GetYaxis().SetTitleOffset(0.65);    hs.GetXaxis().SetLabelSize(0.0000001);   
    hs.GetXaxis().SetTitleSize(0.0000001);   hs.GetXaxis().SetTitleOffset(999);
    hs.GetXaxis().SetTitleFont(42);    hs.GetYaxis().SetTitleFont(42);    hs.SetMaximum(hs.GetHistogram().GetMaximum()*1.5);
    #print("now canv time over 9")
    h_err = histInfo['total'].Clone()
    h_err.SetMarkerStyle(0)
    h_err.SetFillStyle(3344);
    h_err.SetFillColor(ROOT.kGray+2)    #h_err.SetLineColor(1)#ROOT.kGray+1)

    h_err.Draw("PE2 SAME")    
    histdata.Draw("E SAME");

    #print("now canv time over 10")

    legend.AddEntry(h_err,"Total unc.","f");
    legend.Draw("same");
    
    #t2a = drawSLatex(0.1,0.94,"#bf{CMS}",0.085); 
    t2a = drawSLatex(0.1,0.94,"#bf{CMS} #it{Preliminary}",0.085);
    t3a = drawSLatex(0.66,0.94,"%s fb^{#minus1} (13 TeV)"%lumis[yr],0.085);
    t4a = drawSLatex(0.65,0.6,nice_names[CR],0.085);
    t4a = drawSLatex(0.65,0.5,FS+' channel',0.085);
    #print("now canv time over 11")
        
    Canv.Update();
    
    Canv.Print("/eos/user/a/anmehta/www/VVsemilep/postfitplots/postfit_{CR}_{yr}_{FS}_{fit}{log}.pdf".format(yr=yr,fit=fit,CR=CR,FS=FS,log='_log' if logy else ''))
    Canv.Print("/eos/user/a/anmehta/www/VVsemilep/postfitplots/postfit_{CR}_{yr}_{FS}_{fit}{log}.png".format(yr=yr,fit=fit,CR=CR,FS=FS,log='_log' if logy else ''))
    Canv.Close();
    filetoread.Close();

    return True


for FS in ["el","mu"]:
    for CR in ['wj_cr_hi','wj_cr_lo','top_cr']:
        for yr in ["2016","2016APV","2017","2018"]: #,"fullRun2"]:
                makePlot(CR,FS,yr,False)
