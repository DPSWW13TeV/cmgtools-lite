import ROOT, os, subprocess, sys, optparse,numpy
ROOT.gROOT.SetBatch()
ROOT.gStyle.SetOptTitle(0)
ROOT.gStyle.SetOptStat(0);
ROOT.gStyle.SetOptStat(0)
from array import array
#ROOT.gStyle.SetOptFit(1111)
#ROOT.gStyle.SetErrorY(0)
def graphStyle(graph,color,mstyle,lstyle):
    graph.SetMarkerColor(color);  graph.SetMarkerSize(1);  graph.SetMarkerStyle(mstyle);
    graph.SetLineColor(color);    graph.SetLineWidth(1);   graph.SetLineStyle(lstyle);
    return graph
def histStyle(hist,xtitle,ytitle,xoffset,yoffset,titlesize,labelsize):

    hist.GetXaxis().SetTitle(xtitle);        hist.GetYaxis().SetTitle(ytitle);
    hist.GetXaxis().SetTitleSize(titlesize); hist.GetYaxis().SetTitleSize(titlesize); 
    hist.GetXaxis().SetTitleFont(42);        hist.GetYaxis().SetTitleFont(42);
    hist.GetXaxis().SetTitleOffset(xoffset); hist.GetYaxis().SetTitleOffset(yoffset);
    hist.GetXaxis().SetLabelSize(labelsize); hist.GetYaxis().SetLabelSize(labelsize);
    hist.GetXaxis().SetLabelFont(42);        hist.GetYaxis().SetLabelFont(42);

    if "TH2" in hist.ClassName():
        hist.GetZaxis().SetLabelFont(42);    hist.GetZaxis().SetLabelSize(labelsize);    hist.GetZaxis().SetTitleSize(titlesize);    hist.GetZaxis().SetTitleFont(42);

    hist.SetDirectory(0)
    return hist

def makePlot(vname,yr,ff):
    outFile=ROOT.TFile("/eos/user/a/anmehta/www/VVsemilep/res_%s_%s_%s_uncert.root"%(yr,vname,ff),"recreate")
    inFile=ROOT.TFile.Open("/eos/user/a/anmehta/www/VVsemilep/%s/boosted/2025-05-06_WV_smeft_sanitychk//mWV_logy_AND_FatJet1_pt_logy_AND_FatJet1_sDrop_mass_logy.root"%(yr))
    for bsm in ["smeft"]:
        for sm in ["WZ","WW"]:
            outFile.cd();
            canv=ROOT.TCanvas("canv", "%s_%s_%s"%(vname,sm,bsm),600,600);
            h_sm=inFile.Get("%s_SM_%s"%(vname,sm))
            h_sm_up=inFile.Get("%s_SM_%s_CMS_qcdscales_%s_ACCEPTUp"%(vname,sm,sm))
            h_sm_dn=inFile.Get("%s_SM_%s_CMS_qcdscales_%s_ACCEPTDown"%(vname,sm,sm))
            h_eft=inFile.Get("%s_%s_%s_sm"%(vname,sm,bsm))
            print(type(h_eft))
            h_eft_up=inFile.Get("%s_%s_%s_sm_CMS_qcdscales_%s_ACCEPTUp"%(vname,sm,bsm,sm)) 
            h_eft_dn=inFile.Get("%s_%s_%s_sm_CMS_qcdscales_%s_ACCEPTDown"%(vname,sm,bsm,sm)) 

            print("integrals",h_sm.Integral(),"\t ",bsm,"\t",h_eft.Integral())
            ratio_sm=h_sm.Clone("ratio_sm")
            ratio_sm_up=h_sm_up.Clone("ratio_sm_up")
            ratio_sm_dn=h_sm_dn.Clone("ratio_sm_dn")
            ratio_eft=h_eft.Clone("ratio_eft")
            ratio_eft_up=h_eft_up.Clone("ratio_eft_up")
            ratio_eft_dn=h_eft_dn.Clone("ratio_eft_dn")
            
            #h_sm.SetLineColor(ROOT.kGreen+2);
            #h_eft.SetLineColor(ROOT.kBlue);
            ratio_sm_dn.Divide(h_sm);ratio_sm_dn.SetLineColor(ROOT.kOrange-3); ratio_sm_dn.SetMarkerColor(ROOT.kOrange-3);  ratio_sm_dn.SetLineStyle(8);ratio_sm_dn.SetMarkerStyle(23); 
            ratio_eft_dn.Divide(h_eft);ratio_eft_dn.SetLineColor(ROOT.kAzure+1); ratio_eft_dn.SetMarkerColor(ROOT.kAzure+1);  ratio_eft_dn.SetLineStyle(8);ratio_eft_dn.SetMarkerStyle(23);
            ratio_sm_up.Divide(h_sm);ratio_sm_up.SetLineColor(ROOT.kViolet+5); ratio_sm_up.SetMarkerColor(ROOT.kViolet+5);  ratio_sm_up.SetLineStyle(8);ratio_sm_up.SetMarkerStyle(22);
            ratio_eft_up.Divide(h_eft);ratio_eft_up.SetLineColor(ROOT.kMagenta+1); ratio_eft_up.SetMarkerColor(ROOT.kMagenta+1);  ratio_eft_up.SetLineStyle(8);ratio_eft_up.SetMarkerStyle(22);
            
            ratio_sm_d=[];            ratio_sm_u=[];            ratio_eft_d=[];            ratio_eft_u=[];            x=[];
            gr_eft_d       = ROOT.TGraphAsymmErrors(ratio_sm_dn.GetNbinsX()+1);
            gr_eft_u       = ROOT.TGraphAsymmErrors(ratio_sm_dn.GetNbinsX()+1);
            gr_sm_d        = ROOT.TGraphAsymmErrors(ratio_sm_dn.GetNbinsX()+1);
            gr_sm_u        = ROOT.TGraphAsymmErrors(ratio_sm_dn.GetNbinsX()+1);

            for i in range (ratio_sm_dn.GetNbinsX()+1 ):
#                print(i+1,ratio_sm_dn.GetXaxis().GetBinLowEdge(i+1))
                x.append(ratio_sm_dn.GetXaxis().GetBinLowEdge(i+1))

                gr_eft_d.SetPoint(i+1,ratio_sm_dn.GetXaxis().GetBinLowEdge(i+1),ratio_eft_dn.GetBinContent(i+1));
                gr_eft_u.SetPoint(i+1,ratio_sm_dn.GetXaxis().GetBinLowEdge(i+1),ratio_eft_up.GetBinContent(i+1));
                gr_sm_d.SetPoint(i+1,ratio_sm_dn.GetXaxis().GetBinLowEdge(i+1),ratio_sm_dn.GetBinContent(i+1));
                gr_sm_u.SetPoint(i+1,ratio_sm_dn.GetXaxis().GetBinLowEdge(i+1),ratio_sm_up.GetBinContent(i+1));
                gr_eft_d.SetPointError(i+1,0,0,0,0);
                gr_eft_u.SetPointError(i+1,0,0,0,0);
                gr_sm_d.SetPointError(i+1,0,0,0,0);
                gr_sm_u.SetPointError(i+1,0,0,0,0);
                
            mgraphX = ROOT.TMultiGraph("mgraphX{HERE}".format(HERE=sm),""); 
            gr_sm_u        = graphStyle(gr_sm_u,ROOT.kOrange-3,22,8)
            gr_sm_d        = graphStyle(gr_sm_d,ROOT.kMagenta+1,23,8)
            gr_eft_d       = graphStyle(gr_eft_d,ROOT.kViolet+5,23,8)
            gr_eft_u       = graphStyle(gr_eft_u,ROOT.kAzure+1,22,8)
            step=0.005
            #y= numpy.arange(0.98, 1.04, step,)
            #print(array('d',x),array('d',y))
            y=[0.8,0.98, 0.985, 0.99, 0.995, 1.0, 1.005, 1.01, 1.015, 1.02, 1.025, 1.03, 1.035, 1.04,1.045,1.05,1.1,1.2,1.4]
            histX = ROOT.TH2D("histX{he}".format(he=sm),"",len(x),x[0]-100,x[-1]+50,len(y),y[0],y[-1])
            histX =histStyle(histX,"mWV (GeV)","{proc} var./nom.".format(proc=sm),0.9,0.95,0.045,0.035);
            
            histX.SetStats(0);#histX.GetXaxis().SetTitleOffset(0.8);
            legend = ROOT.TLegend(0.25,0.75,0.85,0.88);
            legend.SetNColumns(3);legend.SetFillColor(0);legend.SetFillStyle(0); legend.SetShadowColor(0);   legend.SetLineColor(0);
            legend.SetTextFont(42);  legend.SetBorderSize(0);   legend.SetTextSize(0.025);
            legend.SetNColumns(2);
            legend.AddEntry(gr_sm_d,"SM Down/Nom.","P");
            legend.AddEntry(gr_sm_u,"SM Up/Nom.","P");
            legend.AddEntry(gr_eft_d,"SMEFT Down/Nom.","P");
            legend.AddEntry(gr_eft_u,"SMEFT Up/Nom.","P");
            histX.Draw();


            mgraphX.Add(gr_sm_u);
            mgraphX.Add(gr_sm_d);
            mgraphX.Add(gr_eft_u);
            mgraphX.Add(gr_eft_d);
            mgraphX.Draw('P'); 
            #gr_sm_u.Draw("ACP");
            #gr_sm_d.Draw("CP same");
            #gr_eft_u.Draw("CP same");
            #gr_eft_d.Draw("CP same");
            legend.Draw('same');

            #rtrp1 = ROOT.TRatioPlot(h1);
            #rp1.Draw();
            #rp1.GetLowerRefYaxis().SetTitle("sm/eft");
            #rp1.GetUpperRefYaxis().SetTitle("sm/eft");
            canv.Update();
            canv.Print('/eos/user/a/anmehta/www/VVsemilep/SMratios/%s_%s_%s_qcd_scaleuncert.pdf'%(vname,yr,sm))
            canv.Print('/eos/user/a/anmehta/www/VVsemilep/SMratios/%s_%s_%s_qcd_scaleuncert.png'%(vname,yr,sm))
            canv.Close()
            #            h1.Write()
    outFile.Write();
    outFile.Close();

if __name__ == '__main__':
    parser = optparse.OptionParser(usage='usage: %prog [opts] ', version='%prog 1.0')
    parser.add_option('--yr',  dest='yr',type="string", default="fullRun2", help='make plots for this yr')
    #parser.add_option('--sm',  dest='sm',type="string", default="WW", help='make plots for this FS')
    #parser.add_option('--bsm',  dest='bsm',type="string", default="SMEFT_WW", help='make plots for this FS')
    parser.add_option('--vname',  dest='vname',type="string", default="mWV_logy", help='make plots for this FS')
    parser.add_option('--ff',  dest='ff',type="string", default="expo", help='fit fxm')

    global opts
    (opts, args) = parser.parse_args()


    makePlot(opts.vname,opts.yr,opts.ff)
