import ROOT, re, os, subprocess, sys, optparse, datetime
ROOT.gROOT.SetBatch();    ROOT.gStyle.SetOptFit(0);ROOT.gStyle.SetOptStat(0);

SAFE_COLOR_LIST=[ROOT.kRed+2,ROOT.kOrange+7, ROOT.kAzure+1,ROOT.kMagenta+1,ROOT.kGreen+2, ROOT.kBlue, ROOT.kViolet+5, ROOT.kSpring+5, ROOT.kPink+7, ROOT.kYellow, ROOT.kGray, ROOT.kMagenta+3, ROOT.kBlack]
#legend.AddEntry('NULL','BDTG','');
indir={'basic':['/eos/cms/store/cmst3/group/dpsww/BDT_optimization/',1]}#,'cpt':['/eos/cms/store/cmst3/group/dpsww/BDT_optimization_cptll/',10]}
outdir='/eos/user/a/anmehta/www/BDT/'
variables=['','mt2','mtll','mtl1','pt1','pt2','dphil2met','dphill','dphilll2','etaprod','etasum','met','dR']
templates=['classification']

bkg='wz_amc' #wz_amc' #'fakes'
c1 = ROOT.TCanvas("c1","",200,45,650,500);ROOT.SetOwnership(c1,False);
c1.Range(-0.128266,-0.1538462,1.059382,1.128205);
c1.SetBorderSize(2);
c1.SetGridx();c1.SetGridy();
c1.SetTickx(1);c1.SetTicky(1);
c1.SetRightMargin(0.05);c1.SetBottomMargin(0.12);c1.SetFrameBorderMode(0);
c1.cd();

legend = ROOT.TLegend(0.15,0.15,0.45,0.35);
legend.SetFillColor(0);legend.SetFillStyle(0);legend.SetShadowColor(0);legend.SetLineColor(0);
legend.SetTextFont(42);legend.SetBorderSize(0); legend.SetTextSize(0.025);
legend.SetNColumns(2);

mg = ROOT.TMultiGraph("mg","")

graphs=[];text4legend=[];

for cat in templates:
    for iD,iDS in indir.items():
        for ip in variables:
            commonstr='_ultramax_dpsvs_'+bkg
            pf='2016_withpt'
            if len(ip) == 0:
                fName='{category}{cs}_allvars{pf}'.format(category=cat,cs=commonstr,pf=pf)
            else:
                fName='{category}{cs}_allbut_{here}{pf}'.format(cs=commonstr,pf=pf,category=cat,here=ip)

            file1= ROOT.TFile((iDS[0]+fName+".root"),"read");
            ROOT.gDirectory.cd("dataset_{here}/Method_BDTG/BDTG".format(here=fName))
            graph = ROOT.gDirectory.Get("MVA_BDTG_Test_rejBvsS_Signal");

            if graph == None:
                graph = ROOT.gDirectory.Get("MVA_BDTG_rejBvsS");
            graphs.append(graph); ROOT.SetOwnership(graph,False);
            if "TH1" in graph.ClassName(): graph.SetDirectory(0)
            print 'AUC for %s is %f'%(ip,graph.Integral())
            #text4legend.append('{cat} - {what}{VV} '.format(cat=cat,what='allvars' if len(ip) == 0 else 'allbut-',VV=ip))
            text4legend.append('{what}{VV}{here} '.format(here=iD,what='allvars' if len(ip) == 0 else 'allbut-',VV=ip))
            if len(ip) == 0:
                graph.SetMarkerStyle(29)
                graph.SetMarkerColor(ROOT.kRed)
                graph.SetLineStyle(iDS[1])
            else:
                #graph.SetLineStyle((variables.index(ip) % 2) +7)
                graph.SetLineColor(SAFE_COLOR_LIST[variables.index(ip)]); 
                #graph.SetLineStyle((variables.index(ip) % 2) +7)
                graph.SetLineStyle(iDS[1])
            graph.SetName("gr"+iD+cat+ip);   
        

#c1.cd();
dummy = ROOT.TH2F("dummy","",1000,0,1.0,1000,0,1.0);
dummy.SetLineWidth(2);dummy.SetMarkerStyle(21);dummy.SetMarkerSize(0.3);
dummy.GetXaxis().SetTitle("Signal Efficiency");dummy.GetXaxis().SetLabelOffset(0.012);
dummy.GetXaxis().SetTitleSize(0.045);dummy.GetXaxis().SetTitleOffset(1.2);
dummy.GetYaxis().SetTitle("Background Rejection (1 - eff)");
dummy.GetYaxis().SetLabelOffset(0.012);dummy.GetYaxis().SetTitleSize(0.045);dummy.GetYaxis().SetTitleOffset(1.08);
dummy.Draw();

graphs[0].Draw("P");
legend.AddEntry(graphs[0],text4legend[0],'P')
for i in range(1,len(graphs)):
    if "TH1" in graphs[i].ClassName():
        graphs[i].Draw("histsame")
    else:
        mg.Add(graphs[i])
    legend.AddEntry(graphs[i],text4legend[i],'l')
mg.Draw('L')
legend.Draw("same"); 

c1.SaveAs("/eos/user/a/anmehta/www/ROC_{here}_superComp.png".format(here=bkg));
c1.SaveAs("/eos/user/a/anmehta/www/ROC_{here}_superComp.pdf".format(here=bkg));

