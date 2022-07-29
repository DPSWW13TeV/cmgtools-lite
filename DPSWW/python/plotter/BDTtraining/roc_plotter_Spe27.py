import ROOT, re, os, subprocess, sys, optparse, datetime
ROOT.gROOT.SetBatch();    ROOT.gStyle.SetOptFit(0);ROOT.gStyle.SetOptStat(0);

SAFE_COLOR_LIST=[ROOT.kRed+2,ROOT.kOrange+7, ROOT.kAzure+1,ROOT.kMagenta+1,ROOT.kGreen+2, ROOT.kBlue, ROOT.kViolet+5, ROOT.kSpring+5, ROOT.kPink+7, ROOT.kYellow, ROOT.kGray, ROOT.kMagenta+3, ROOT.kBlack]
#legend.AddEntry('NULL','BDTG','');
indir='/eos/cms/store/cmst3/group/dpsww/BDT_optimization/IPvars/'#/eos/cms/store/cmst3/group/dpsww/BDT_optimization/'
outdir='/eos/user/a/anmehta/www/BDT/'
variables=['','dxy']#,'dz']#'mt2','mtll','mtl1','pt1','pt2','dphil2met','dphill','dphilll2','etaprod','etasum','met',
templates={'wz':['wz_amc',ROOT.kAzure+1],'TL':['fakes',ROOT.kOrange+7]}
years=[2016,2017,2018]
for bkg,iset in templates.iteritems():

    c1 = ROOT.TCanvas("c1","",200,45,650,500);ROOT.SetOwnership(c1,False);
    c1.Range(-0.128266,-0.1538462,1.059382,1.128205);
    c1.SetBorderSize(2);c1.SetGridx();c1.SetGridy();c1.SetTickx(1);c1.SetTicky(1);
    c1.SetRightMargin(0.05);c1.SetBottomMargin(0.12);c1.SetFrameBorderMode(0);
    c1.cd();
    
    legend = ROOT.TLegend(0.15,0.15,0.25,0.55);
    legend.SetFillColor(0);legend.SetFillStyle(0);legend.SetShadowColor(0);legend.SetLineColor(0);
    legend.SetTextFont(42);legend.SetBorderSize(0); legend.SetTextSize(0.025);
    #legend.SetNColumns(2);
    
    mg = ROOT.TMultiGraph("mg","")
    
    graphs=[];text4legend=[];
    
    for yr in years:
        for ip in variables:
            commonstr='Sep2021_dpsWW_'+iset[0]
            pf='%s_withpt'%(str(yr))
            if len(ip) == 0:
                fName='{cs}_allvars{pf}'.format(cs=commonstr,pf=pf)
            else:
                fName='{cs}_allbut_{here}{pf}'.format(pf=pf,cs=commonstr,here=ip)

            file1= ROOT.TFile((indir+fName+".root"),"read");
            ROOT.gDirectory.cd("dataset_{here}/Method_BDTG/BDTG".format(here=fName))
            graph = ROOT.gDirectory.Get("MVA_BDTG_Test_rejBvsS_Signal");
            if graph == None:
                graph = ROOT.gDirectory.Get("MVA_BDTG_rejBvsS");
                graphs.append(graph); ROOT.SetOwnership(graph,False);
            if "TH1" in graph.ClassName(): graph.SetDirectory(0)
            print 'AUC for %s is %f'%(ip,graph.Integral())
            text4legend.append('{what}{VV}--{when}--{bkg}'.format(bkg=bkg,when=str(yr),what='allvars' if len(ip) == 0 else 'allbut-',VV=ip))
            #if len(ip) == 0 :
            #    graph.SetLineStyle(1);
            #else :
            graph.SetLineStyle(variables.index(ip)+1);
                                
            #graph.SetLineColor(iset[1]); 
            graph.SetName("gr"+fName);   
            graph.SetLineColor(SAFE_COLOR_LIST[years.index(yr)]); 


    dummy = ROOT.TH2F("dummy","",1000,0,1.0,1000,0,1.0);
    dummy.SetLineWidth(2);dummy.SetMarkerStyle(21);dummy.SetMarkerSize(0.3);
    dummy.GetXaxis().SetTitle("Signal Efficiency");dummy.GetXaxis().SetLabelOffset(0.012);
    dummy.GetXaxis().SetTitleSize(0.045);dummy.GetXaxis().SetTitleOffset(1.2);
    dummy.GetYaxis().SetTitle("Background Rejection (1 - eff)");
    dummy.GetYaxis().SetLabelOffset(0.012);dummy.GetYaxis().SetTitleSize(0.045);dummy.GetYaxis().SetTitleOffset(1.08);
    dummy.Draw();

    graphs[0].Draw("hist");
    legend.AddEntry(graphs[0],text4legend[0],'l')
    for i in range(1,len(graphs)):
        if "TH1" in graphs[i].ClassName():
            graphs[i].Draw("histsame")
        else:
            mg.Add(graphs[i])
        legend.AddEntry(graphs[i],text4legend[i],'l')
    mg.Draw('L')
    legend.Draw("same"); 


    c1.SaveAs("{od}/ROC_{here}_IPvars.png".format(od=outdir,here=bkg));
    c1.SaveAs("{od}/ROC_{here}_IPvars.pdf".format(od=outdir,here=bkg));

