import ROOT, re, os, subprocess, sys, optparse, datetime
ROOT.gROOT.SetBatch();    ROOT.gStyle.SetOptFit(0);ROOT.gStyle.SetOptStat(0);

SAFE_COLOR_LIST=[ROOT.kRed+2,ROOT.kOrange+7, ROOT.kAzure+1,ROOT.kMagenta+1,ROOT.kGreen+2, ROOT.kBlue, ROOT.kViolet+5, ROOT.kSpring+5, ROOT.kPink+7, ROOT.kYellow, ROOT.kGray, ROOT.kMagenta+3, ROOT.kBlack]
#legend.AddEntry('NULL','BDTG','');

#years={'2016':[ROOT.kOrange+7,ROOT.kGreen+2],'2017':[ROOT.kAzure+1,ROOT.kPink+7],'2018':[ROOT.kSpring+5,ROOT.kMagenta+1]}
years={'2016':[ROOT.kOrange+7,ROOT.kGreen+2],'2017':[ROOT.kOrange+7,ROOT.kGreen+2],'2018':[ROOT.kOrange+7,ROOT.kGreen+2]}
bkgs=['wz_amc','TL']
templates=['_basic','']
for bkg in bkgs:
    #graphs={};   
    graphs=[] 
    for yr,col in years.iteritems():
        c1 = ROOT.TCanvas("c1%s%s"%(bkg,yr),"",200,45,650,500);ROOT.SetOwnership(c1,False);
        c1.Range(-0.128266,-0.1538462,1.059382,1.128205);
        c1.SetBorderSize(2);    c1.SetGridx();c1.SetGridy();c1.SetTickx(1);c1.SetTicky(1);
        c1.SetRightMargin(0.05);c1.SetBottomMargin(0.12);c1.SetFrameBorderMode(0);
        c1.cd();
        legend = ROOT.TLegend(0.15,0.15,0.35,0.55);
        legend.SetFillColor(0);legend.SetFillStyle(0);legend.SetShadowColor(0);legend.SetLineColor(0);
        legend.SetTextFont(42);legend.SetBorderSize(0); legend.SetTextSize(0.045);
        #legend.SetNColumns(2);
        #mg = ROOT.TMultiGraph("mg%s%s"%(bkg,yr),"")
        dummy = ROOT.TH2F("dummy%s%s"%(bkg,yr),"",1000,0,1.0,1000,0,1.0);
        dummy.SetLineWidth(2);dummy.SetMarkerStyle(21);dummy.SetMarkerSize(0.3);
        dummy.GetXaxis().SetTitle("Signal Efficiency");dummy.GetXaxis().SetLabelOffset(0.012);
        dummy.GetXaxis().SetTitleSize(0.045);dummy.GetXaxis().SetTitleOffset(1.2);
        dummy.GetYaxis().SetTitle("Background Rejection (1 - eff)");
        dummy.GetYaxis().SetLabelOffset(0.012);dummy.GetYaxis().SetTitleSize(0.045);dummy.GetYaxis().SetTitleOffset(1.08);
        dummy.Draw();
        fName="dnn_nospec_dpsvs_%s_%s_withpt"%(bkg,yr)
        fIn = ROOT.TFile.Open("/afs/cern.ch/user/a/anmehta/public/dnn/"+fName+".root")
        roc_bdt = fIn.Get("dataset_%s/Method_BDT/BDTG/MVA_BDTG_trainingRejBvsS"%fName);
        roc_dnn = fIn.Get("dataset_%s/Method_PyKeras/PyKeras/MVA_PyKeras_trainingRejBvsS"%fName);

        graphs.append(roc_bdt); ROOT.SetOwnership(roc_bdt,False);        graphs.append(roc_dnn); ROOT.SetOwnership(roc_dnn,False);
        roc_bdt.SetDirectory(0);roc_dnn.SetDirectory(0);
        fIn.Close()
        fName1="dnn_noee_dpsvs_%s_%s_withpt"%(bkg,yr)
        fIn1 = ROOT.TFile.Open("/afs/cern.ch/user/a/anmehta/public/dnn/"+fName1+".root")
        roc1_bdt = fIn1.Get("dataset_%s/Method_BDT/BDTG/MVA_BDTG_trainingRejBvsS"%fName1);
        roc1_dnn = fIn1.Get("dataset_%s/Method_PyKeras/PyKeras/MVA_PyKeras_trainingRejBvsS"%fName1);
        graphs.append(roc1_bdt); ROOT.SetOwnership(roc1_bdt,False);        graphs.append(roc1_dnn); ROOT.SetOwnership(roc1_dnn,False);
        print roc1_bdt.ClassName(),roc1_dnn.ClassName()
        roc1_bdt.SetDirectory(0);roc1_dnn.SetDirectory(0);
        fIn1.Close()

        fName2="dnn_nospec_dpsvs_chkAll_%s_2018_withpt"%bkg
        fIn2 = ROOT.TFile.Open("/afs/cern.ch/user/a/anmehta/public/dnn/"+fName2+".root")
        roc2_bdt = fIn2.Get("dataset_%s/Method_BDT/BDTG/MVA_BDTG_trainingRejBvsS"%fName2);
        roc2_dnn = fIn2.Get("dataset_%s/Method_PyKeras/PyKeras/MVA_PyKeras_trainingRejBvsS"%fName2);
        graphs.append(roc2_bdt); ROOT.SetOwnership(roc2_bdt,False);        graphs.append(roc2_dnn); ROOT.SetOwnership(roc2_dnn,False);
        print roc2_bdt.ClassName(),roc2_dnn.ClassName()
        roc2_bdt.SetDirectory(0);roc2_dnn.SetDirectory(0);
        fIn2.Close()

        legend.AddEntry('NULL',bkg+' : '+yr,'')
        legend.AddEntry(roc_bdt,'bdtg','l')
        legend.AddEntry(roc_dnn,'dnn','l')
        legend.AddEntry(roc2_bdt,'bdtg'+'_run2','l')
        legend.AddEntry(roc2_dnn,'dnn'+'_run2','l')
        legend.AddEntry(roc1_bdt,'bdtg'+'_noee','l')
        legend.AddEntry(roc1_dnn,'dnn'+'_noee','l')

        roc1_bdt.SetLineColor(col[0]);        roc1_dnn.SetLineColor(col[1]);        roc_bdt.SetLineColor(col[0]);        roc_dnn.SetLineColor(col[1]);       
        roc1_dnn.SetLineStyle(2);         roc1_bdt.SetLineStyle(2); roc_bdt.SetLineStyle(1);        roc_dnn.SetLineStyle(1);
        roc1_bdt.SetLineWidth(2);        roc1_dnn.SetLineWidth(2);        roc_bdt.SetLineWidth(2);        roc_dnn.SetLineWidth(2);
        roc2_bdt.SetLineWidth(2);        roc2_dnn.SetLineWidth(2);     roc2_dnn.SetLineStyle(3);         roc2_bdt.SetLineStyle(3);
        #roc2_bdt.SetLineColor(col[0]);        roc2_dnn.SetLineColor(col[1]);
        roc2_bdt.SetLineColor(ROOT.kBlue);        roc2_dnn.SetLineColor(ROOT.kRed);
        roc1_bdt.Draw('histsame'); roc1_dnn.Draw('histsame');
        roc2_bdt.Draw('histsame'); roc2_dnn.Draw('histsame');
        roc_bdt.Draw('histsame'); roc_dnn.Draw('histsame');
        legend.Draw("same"); 
        c1.SaveAs("/eos/user/a/anmehta/www/DPSWW_v2/DNN//ROC_{here}_dnnVsbdtg.png".format(here=bkg+yr));
        c1.SaveAs("/eos/user/a/anmehta/www/DPSWW_v2/DNN//ROC_{here}_dnnVsbdtg.pdf".format(here=bkg+yr));


            ##        gr_id=bkg+yr+tr
            #graphs[gr_id]=[roc_bdt,roc_dnn,col[templates.index(tr)]]

##am        for ig,iset in graphs.iteritems():
##am            gr_noee_bdt=graphs[bkg+yr+'noee'][0]
##am            gr_noee_dnn=graphs[bkg+yr+'noee'][1]
##am            graph_noee_dnn.SetLineColor(graphs[bkg+yr+'noee'][0][2])
##am            graph_noee_dnn.SetLineStyle(1)
##am            graph_noee_bdt.SetLineColor(graphs[bkg+yr+'noee'][0][2])
##am            graph_noee_bdt.SetLineStyle(1)
##am
##am            else:
##am                #graph.SetLineStyle((variables.index(ip) % 2) +7)
##am                graph.SetLineColor(SAFE_COLOR_LIST[variables.index(ip)]); 
##am                #graph.SetLineStyle((variables.index(ip) % 2) +7)
##am                graph.SetLineStyle(iDS[1])
##am            graph.SetName("gr"+iD+cat+ip);   
        

#c1.cd();

##amgraphs[0].Draw("P");
##am
##amfor i in range(1,len(graphs)):
##am    if "TH1" in graphs[i].ClassName():
##am        graphs[i].Draw("histsame")
##am    else:
##am        mg.Add(graphs[i])
##am    legend.AddEntry(graphs[i],text4legend[i],'l')
##ammg.Draw('L')


