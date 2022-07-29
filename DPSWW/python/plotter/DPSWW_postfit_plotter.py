import ROOT, os, optparse, copy, re
from ROOT import TCanvas, TFile, TColor, TH1F, TH2F
from ROOT import gROOT, gBenchmark, gRandom, gSystem
import numpy as np
import math
#bdt13bins
#wz_cr24 bins
#zz cr30bins
#tot318bins
#ch1_elmu_mm_2016->0-13
#ch1_elmu_pp_2016->13-26
#ch1_mumu_mm_2016->26-39
#ch1_mumu_pp_2016->39-52
#ch1_wz_cr_2016->52-76
#ch1_zz_cr_2016->76-106
#ch2_elmu_mm_2017->106-119  
#ch2_elmu_pp_2017->119-132  
#ch2_mumu_mm_2017->132-145  
#ch2_mumu_pp_2017->145-158  
#ch2_wz_cr_2017->158-182   
#ch2_zz_cr_2017->182-212    
#ch3_elmu_mm_2018->212-225  
#ch3_elmu_pp_2018->225-238  
#ch3_mumu_mm_2018->238-251  
#ch3_mumu_pp_2018->251-264  
#ch3_wz_cr_2018->264-288
#ch3_zz_cr_2018->288-318


xbinlow=0
xbinhigh=13
nbinsx=xbinhigh-xbinlow
fit="fit_s" #fit_b #fit_s
def unpackHistcontent(xBL):
    histInfo={};allhists={} 
    filetoread = ROOT.TFile('fitresults_bonlyfit.root','read')
    for key in list(filetoread.GetListOfKeys()):
        classname = key.GetClassName()
        cl = ROOT.gROOT.GetClass(classname)
        if(cl.InheritsFrom(ROOT.TH1D.Class())):
            objectName = key.GetName()
            if 'hybrid' in objectName or 'prefit' in objectName: continue
            ikey=objectName.split('_postfit')[0].split('exp')[-1].split('proc_')[-1]
            allhists[ikey]=filetoread.Get(objectName)
    #print allhists.keys()


    for proc,hpost in allhists.iteritems():
        yval2k16=[]; yerr2k16=[]; yval2k18=[]; yerr2k18=[];
        yval2k17=[]; yerr2k17=[];        yval=[]; yerr=[];
       
        for i in range(xBL['2016']+1,xBL['2016']+xbinhigh+1):
            yval2k16.append(hpost.GetBinContent(i));       yerr2k16.append(hpost.GetBinError(i));
        for i in range(xBL['2017']+1,xBL['2017']+xbinhigh+1):
            yval2k17.append(hpost.GetBinContent(i));       yerr2k17.append(hpost.GetBinError(i));
        for i in range(xBL['2018']+1,xBL['2018']+xbinhigh+1):
            yval2k18.append(hpost.GetBinContent(i));       yerr2k18.append(hpost.GetBinError(i));
        yval=[yval2k16[i]+yval2k17[i]+yval2k18[i] for i in range(0,len(yval2k16))]
        yerr=[yerr2k16[i]+yerr2k17[i]+yerr2k18[i] for i in range(0,len(yerr2k16))]
        histFR2 = ROOT.TH1D('histFR2','',nbinsx,xbinlow,xbinhigh)

        for i in xrange(len(yval)):
            histFR2.SetBinContent(i+1,yval[i]);
            if proc != "obs":histFR2.SetBinError(i+1,yerr[i]);
        if proc == "obs":     
            histFR2.Sumw2()
        histFR2.SetDirectory(0);        histFR2.SetName(proc)
        histInfo[proc]= histFR2
    

    return histInfo

#data->tgraphasym
processes=['data',
'data_flips',
#'Convs',
'DPSWW',
'Rares',
'VVV',
'WZ',
'Wgstar',
'ZZ',
'data_fakes',
'total',
'total_signal',
'total_background']

def unpackHistcontent_hc(fs):
    print fs
    histInfo={};allhists={} 
    filetoread = ROOT.TFile('fitDiagnostics.root','read')
    #chname='ch{year}_{fs}_{yr}'.format(year=yr-2015,yr=yr)
    for proc in processes:
        if "mumu" in fs and (proc == "data_flips" or proc == "Convs"): continue
            
        hist=ROOT.TH1D("%s"%proc,"",nbinsx,xbinlow,xbinhigh); 
        if proc == "data":hist.Sumw2()
        hist2016=filetoread.Get("shapes_{fit}/ch1_{fs}_2016/{p}".format(fit=fit,fs=fs,p=proc))
        hist2017=filetoread.Get("shapes_{fit}/ch2_{fs}_2017/{p}".format(fit=fit,fs=fs,p=proc))
        hist2018=filetoread.Get("shapes_{fit}/ch3_{fs}_2018/{p}".format(fit=fit,fs=fs,p=proc))

        for i in range(1,nbinsx+1):
            if (hist2016.InheritsFrom(ROOT.TH1.Class())):
                yval=hist2016.GetBinContent(i)+hist2017.GetBinContent(i)+hist2018.GetBinContent(i)
                yerr=hist2016.GetBinError(i)+hist2017.GetBinError(i)+hist2018.GetBinError(i)
                #print yval,yerr
                hist.SetBinContent(i,yval);                hist.SetBinError(i,yerr);

            else:
                #print proc
                x = ROOT.Double(0.)
                y1 = ROOT.Double(0.);y2 = ROOT.Double(0.);y3 = ROOT.Double(0.)
                hist2016.GetPoint(i-1,x,y1)
                hist2017.GetPoint(i-1,x,y2)
                hist2018.GetPoint(i-1,x,y3)
                #print y1,y2,y3
                hist.SetBinContent(i,(y1+y2+y3))
                hist.SetBinError(i,math.sqrt(y1+y2+y3));
        hist.SetDirectory(0)

        histInfo[proc]=hist
        #print proc,hist.Integral()

    return histInfo

def drawSLatex(xpos,ypos,text,size):
    latex = ROOT.TLatex()
    latex.SetNDC()
    latex.SetTextAlign(12)
    latex.SetTextSize(size)
    latex.SetTextFont(42)
    latex.DrawLatex(xpos,ypos,text)



if __name__ == '__main__':
    
    ROOT.gROOT.SetBatch()
    ROOT.gStyle.SetOptStat(0)

    FS={
        'mumu_pp':['mpp',500,"Bin number (#mu^{#plus}#mu^{#plus})",{'2016':39,'2017':145,'2018':251}],
        'mumu_mm':['mmm',300,"Bin number (#mu^{#minus}#mu^{#minus})",{'2016':26,'2017':132,'2018':238}],
        'elmu_pp':['epp',500,"Bin number (e^{#plus}#mu^{#plus})",{'2016':13,'2017':119,'2018':225}],
        'elmu_mm':['emm',600,"Bin number (e^{#minus}#mu^{#minus})",{'2016':0,'2017':106,'2018':212}]
        }

    #loop on FS
    cosmetics={
        'DPSWW':[ROOT.kRed+1,"DPS W^{#pm}W^{#pm}"],
        'Rares':[ROOT.kPink+6,"Rares"],
        'ZZ':[ROOT.kOrange-3,"ZZ"],
        'WZ':[ROOT.kAzure+1,"WZ"],
        'data_fakes':[ROOT.kGray,"Nonprompt"],
        'Wgstar':[ROOT.kViolet+7,"W#gamma*"],
        'data_flips':[ROOT.kCyan-7,"Charge misid."],
        'Convs':[ROOT.kGreen-3,"W/Z#gamma"],
        'VVV':[5,"VVV"],
        'obs':[ROOT.kBlack,"Data"],
        'data':[ROOT.kBlack,"Data"]
        }  

    for key,val in FS.iteritems(): # loop on all final states
        Canv = ROOT.TCanvas("Canv{FS}".format(FS=key),"",600,600)
        Canv.Range(0,0,1,1);   Canv.SetFillColor(0);   Canv.SetBorderMode(0);   Canv.SetBorderSize(2);
        Canv.SetTickx(1);   Canv.SetTicky(1);   Canv.SetLeftMargin(0.16);   Canv.SetRightMargin(0.08);
        Canv.SetBottomMargin(0.13);   Canv.SetFrameFillStyle(0);   Canv.SetFrameBorderMode(0);
        
        legend = ROOT.TLegend(0.26,0.64,0.82,0.86);
        legend.SetNColumns(3);legend.SetFillColor(0);legend.SetFillStyle(0); legend.SetShadowColor(0);   legend.SetLineColor(0);
        legend.SetTextFont(42);  legend.SetBorderSize(0);   legend.SetTextSize(0.04);
        
        hs=ROOT.THStack("hs{FS}".format(FS=key),""); 

        histFS={}
        histFS=unpackHistcontent_hc(key)
        #histFS = unpackHistcontent(val[3]) # dict with keys as pname & one tuple per bin with xval,yval,yerr for FR2 

        # use histFS  to define histograms for the stack

        #print 'this is what i got',histFS.keys() #all processes for three years added


        for proc,ihist in histFS.iteritems():    
            if proc in cosmetics.keys():
                ihist.SetName(proc); ihist.SetLineColor(ROOT.kBlack)
                if proc !="data":
                    ihist.SetFillColor(cosmetics[proc][0]); 
                if proc == "data" :ihist.SetFillStyle(0);ihist.SetMarkerColor(1);ihist.SetMarkerStyle(20);
                if 'fakes' in proc:                    ihist.SetFillStyle(3005);
        histtotbkg=histFS['total_background'] #histtotbkg=histFS['bkg']
        histdata=histFS['data']##histFS['obs'] 
        #histdata.SetLineColor(ROOT.kBlack); 
        histdata.SetMarkerSize(1);  
        histdata.SetMarkerStyle(20);histdata.SetMarkerColor(1);
        histdata.SetLineColor(1);  histdata.SetLineWidth(1);
        #histdata.SetFillStyle(0)

        #print 'total background %.3f' % histtotbkg.Integral()   
        print 'observed %.3f' % histdata.Integral()   
        errA=ROOT.Double(0.)
        er=histFS['DPSWW'].IntegralAndError(1,histFS['DPSWW'].GetNbinsX(),errA, "");
        print 'signal %.3f pm %.3f'%(er,errA)
        errA=ROOT.Double(0.)
        er=histFS['total_background'].IntegralAndError(1,histFS['total_background'].GetNbinsX(),errA, "");
        #print 'error on sig', er,errA
        print 'total background %.3f pm %.3f'%(er,errA)

        hs.Add(histFS['data_fakes']);#fakes
        #       if "elmu" in key:
 #          hs.Add(histFS['Convs']);
        hs.Add(histFS['WZ']);#WZ
        hs.Add(histFS['Wgstar']);#Wg*
        hs.Add(histFS['ZZ']);#ZZ
        hs.Add(histFS['VVV']);#VVV
        if "elmu" in key:
            hs.Add(histFS['data_flips']);
        hs.Add(histFS['Rares']);#rares
        hs.Add(histFS['DPSWW']);#DPS


 
        legend.AddEntry(histFS['WZ'],cosmetics['WZ'][1],"f");
        legend.AddEntry(histFS['ZZ'],cosmetics['ZZ'][1],"f");
        legend.AddEntry(histFS['VVV'],cosmetics['VVV'][1],"f");
        legend.AddEntry(histFS['Rares'],cosmetics['Rares'][1],"f");
        legend.AddEntry(histFS['DPSWW'],cosmetics['DPSWW'][1],"f");
        legend.AddEntry(histFS['data_fakes'],cosmetics['data_fakes'][1],"f");
        legend.AddEntry(histFS['Wgstar'],cosmetics['Wgstar'][1],"f");
        #legend.AddEntry(histFS['obs'],cosmetics['obs'][1],"elp");
        legend.AddEntry(histFS['data'],cosmetics['data'][1],"elp");
        if(val[0] == "epp" or val[0] == "emm"):
            legend.AddEntry(histFS['data_flips'],cosmetics['data_flips'][1],"f");
            #   legend.AddEntry(histFS['Convs'],cosmetics['Convs'][1],"f");
            
## ratio plot
        errorData=[]
        hist_data= ROOT.TH1D("hist_data{FS}".format(FS=key),"",nbinsx,xbinlow,xbinhigh)
        for ibin in range(xbinlow+1,xbinhigh+1):
            MC_stack_content=histtotbkg.GetBinContent(ibin);
            MC_stack_error=histtotbkg.GetBinError(ibin);
            datacontent=histdata.GetBinContent(ibin);
            dataerror=histdata.GetBinError(ibin);
            #print MC_stack_content, MC_stack_error, datacontent,dataerror
            if((MC_stack_content!=0) and (datacontent !=0)):
                ratiocontent=(datacontent/MC_stack_content);
                error=ratiocontent*math.sqrt( ((dataerror/datacontent)**2) + ((MC_stack_error/MC_stack_content)**2) );
                hist_data.SetBinContent(ibin,ratiocontent);
                hist_data.SetBinError(ibin,error);
                #print error
                errorData.append(error)
        #print len(errorData)
 
        c1_1 = ROOT.TPad("c1_1","ratioplot",0.01,0.01,0.99,0.33);    c1_1.Draw();    c1_1.cd();
        c1_1.SetTopMargin(0.041); c1_1.SetBottomMargin(0.3);   c1_1.SetRightMargin(0.1);c1_1.SetBorderMode(0);c1_1.SetTicky(1);
        c1_1.SetBorderSize(2); c1_1.SetFillStyle(0);c1_1.SetFrameBorderMode(0);c1_1.SetFrameLineWidth(2);c1_1.SetFrameBorderMode(0); 
 
 ##central line on ratio plot 
        line1 = ROOT.TLine(xbinlow,1.0,xbinhigh,1.0);    line1.SetLineColor(58);   line1.SetLineWidth(2);   line1.SetLineStyle(1);
 
    #shaded uncert band around the ratio plot 
 
        band=ROOT.TH1D("band{FS}".format(FS=key),"",nbinsx,xbinlow,xbinhigh);    band.SetFillColor(ROOT.kCyan);   band.SetMarkerSize(0); 
        band.SetFillStyle(1001);        band.Divide(histtotbkg,histtotbkg,1,1,"b");
        for ibin in range(xbinlow+1,xbinhigh+1):
            band.SetBinError(ibin,errorData[ibin-1]);    
  
    #signal histogram on the bottom pad
            signal =histFS['DPSWW'].Clone();    signal.SetFillColor(0);   signal.SetFillStyle(0);  
            signal.SetLineColor(ROOT.kRed+1);   signal.SetLineWidth(2);  
            for w in range(xbinlow+1,xbinhigh+1):
                putit=signal.GetBinContent(w)/histtotbkg.GetBinContent(w);
                signal.SetBinContent(w,1+putit);
        
 
 
 
        band.GetXaxis().SetTitleFont(42);    band.GetXaxis().SetLabelSize(0.11);    band.GetXaxis().SetTitleSize(0.12);
        band.GetXaxis().SetTitleOffset(0.95);       band.GetXaxis().SetRangeUser(xbinlow,xbinhigh);    band.GetYaxis().SetTitle("Data/bkg.");
        band.GetYaxis().SetLabelSize(0.11);    band.GetYaxis().SetTitleSize(0.12);    band.GetYaxis().SetTitleOffset(0.44);
        band.GetYaxis().SetRangeUser(0.2,2.0);     band.GetYaxis().SetNdivisions(607);    ROOT.gStyle.SetErrorX(0.5);
        hist_data.SetMarkerStyle(20);   hist_data.SetMarkerColor(1);   hist_data.SetMarkerSize(1);
        hist_data.SetLineColor(1);  hist_data.SetLineWidth(1);

 
        band.Draw("E2SAME");
        line1.Draw("LSAMES");
        #signal.Draw("AHIST][SAME");
        hist_data.Draw("Ex0SAME"); 

        c1_1.Update();
        legend1 = ROOT.TLegend(0.27,0.69,0.42,0.93); #,NULL,"brNDC");
        legend1.SetTextFont(42);
        legend1.SetTextSize(0.09);
        legend1.SetFillColor(0);
        legend1.SetLineColor(0);
        legend1.SetFillStyle(0);
        legend1.AddEntry(band,"Total background uncertainty","f");
        #legend1.AddEntry(signal,"DPS W^{#pm}W^{#pm}","l");
        legend1.Draw("same");

##
        Canv.cd();

        c1_2 = ROOT.TPad("c1_2", "newpad",0.01,0.33,0.99,0.99);
        c1_2.Draw();        c1_2.cd();
        c1_2.SetTopMargin(0.13);  c1_2.SetBottomMargin(0.04);  c1_2.SetRightMargin(0.1);        c1_2.SetFillStyle(0);
        c1_2.SetBorderMode(0);        c1_2.SetBorderSize(2);c1_2.SetFrameBorderMode(0);c1_2.SetFrameLineWidth(2);
        c1_2.SetFrameBorderMode(0);   c1_2.SetTicky(1);
 
        hs.Draw("HIST");
        band.GetXaxis().SetTitle(val[2]);    hs.GetXaxis().SetTitle(val[2]);    hs.GetYaxis().SetTitle("Events");
        hs.GetYaxis().SetLabelSize(0.05);    hs.GetYaxis().SetTitleSize(0.06);    hs.GetYaxis().SetTitleOffset(0.87);
        hs.GetXaxis().SetLabelSize(0.0000001);    hs.GetXaxis().SetTitleSize(0.0000001);    hs.GetXaxis().SetTitleOffset(1.03);
        hs.GetXaxis().SetTitleFont(42);    hs.GetYaxis().SetTitleFont(42);    hs.SetMaximum(val[1]);
        histdata.Draw("PEX0 SAME");
    
        legend.Draw("same");
        t2a = drawSLatex(0.1,0.90,"#bf{CMS} #it{Preliminary}",0.05);
        t3a = drawSLatex(0.665,0.90,"138 fb^{#minus1} (13 TeV)",0.05);
    
        Canv.Update();
    
    
        Canv.Print("/eos/user/a/anmehta/www/DPSWW_v2/plot/plot_%s_"%fit + val[0] + '.pdf')
        Canv.Print("/eos/user/a/anmehta/www/DPSWW_v2/plot/plot_%s_"%fit + val[0] + '.png')

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
