import ROOT, re, os, subprocess, sys, optparse, datetime
ROOT.gROOT.SetBatch();    ROOT.gStyle.SetOptFit(0);ROOT.gStyle.SetOptStat(0);

SAFE_COLOR_LIST=[ROOT.kRed+2,ROOT.kOrange+7, ROOT.kAzure+1,ROOT.kMagenta+1,ROOT.kGreen+2, ROOT.kBlue, ROOT.kViolet+5, ROOT.kSpring+5, ROOT.kPink+7, ROOT.kYellow, ROOT.kGray, ROOT.kMagenta+3, ROOT.kBlack]
#legend.AddEntry('NULL','BDTG','');

#years={'2016':[ROOT.kOrange+7,ROOT.kGreen+2],'2017':[ROOT.kAzure+1,ROOT.kPink+7],'2018':[ROOT.kSpring+5,ROOT.kMagenta+1]}
years={'2016':ROOT.kOrange+7,'2017':ROOT.kGreen+2,'2018':ROOT.kMagenta+1}

bkgs=['wz_amc','TL']
templates=['_basic','']
for bkg in bkgs:
    #graphs={};   
    graphs=[] 
    c1 = ROOT.TCanvas("c1%s"%bkg,"",200,45,650,500);ROOT.SetOwnership(c1,False);
    c1.Range(-0.128266,-0.1538462,1.059382,1.128205);
    c1.SetBorderSize(2);    c1.SetGridx();c1.SetGridy();c1.SetTickx(1);c1.SetTicky(1);
    c1.SetRightMargin(0.05);c1.SetBottomMargin(0.12);c1.SetFrameBorderMode(0);
    c1.cd();
    legend = ROOT.TLegend(0.15,0.15,0.35,0.55);
    legend.SetFillColor(0);legend.SetFillStyle(0);legend.SetShadowColor(0);legend.SetLineColor(0);
    legend.SetTextFont(42);legend.SetBorderSize(0); legend.SetTextSize(0.045);
    legend.AddEntry('NULL',bkg+' : BDTG','')

    #legend.SetNColumns(2);
    #mg = ROOT.TMultiGraph("mg%s"%bkg),"")
    dummy = ROOT.TH2F("dummy%s"%bkg,"",1000,0,1.0,1000,0,1.0);
    dummy.SetLineWidth(2);dummy.SetMarkerStyle(21);dummy.SetMarkerSize(0.3);
    dummy.GetXaxis().SetTitle("Signal Efficiency");dummy.GetXaxis().SetLabelOffset(0.012);
    dummy.GetXaxis().SetTitleSize(0.045);dummy.GetXaxis().SetTitleOffset(1.2);
    dummy.GetYaxis().SetTitle("Background Rejection (1 - eff)");
    dummy.GetYaxis().SetLabelOffset(0.012);dummy.GetYaxis().SetTitleSize(0.045);dummy.GetYaxis().SetTitleOffset(1.08);
    dummy.Draw();
    for yr,col in years.items():
        fName="dnn_nospec_dpsvs_%s_%s_withpt"%(bkg,yr)
        fIn = ROOT.TFile.Open("/eos/cms/store/cmst3/group/dpsww/trainings/"+fName+".root")
        roc_bdt = fIn.Get("dataset_%s/Method_BDT/BDTG/MVA_BDTG_trainingRejBvsS"%fName);
        print roc_bdt.Integral();
        graphs.append(roc_bdt); ROOT.SetOwnership(roc_bdt,False);          roc_bdt.SetDirectory(0);
        roc_bdt.SetLineColor(col);         roc_bdt.SetLineWidth(2); roc_bdt.Draw('histsame')
        fIn.Close()
        legend.AddEntry(roc_bdt,yr,'l')
    fName2="dnn_nospec_dpsvs_chkAll_%s_2018_withpt"%bkg
    fIn2 = ROOT.TFile.Open("/eos/cms/store/cmst3/group/dpsww/trainings/"+fName2+".root")
    roc2_bdt = fIn2.Get("dataset_%s/Method_BDT/BDTG/MVA_BDTG_trainingRejBvsS"%fName2);
    print roc2_bdt.Integral();
    graphs.append(roc2_bdt); ROOT.SetOwnership(roc2_bdt,False);    

    roc2_bdt.SetDirectory(0);
    roc2_bdt.SetLineColor(ROOT.kBlue); roc2_bdt.SetLineWidth(2);
    roc2_bdt.Draw('histsame');
    fIn2.Close()

    legend.AddEntry(roc2_bdt,'run2','l')
    legend.Draw("same"); 
    c1.SaveAs("/eos/user/a/anmehta/www/DPSWW_v2/DNN//ROC_{here}_bdtgTest.png".format(here=bkg));
    c1.SaveAs("/eos/user/a/anmehta/www/DPSWW_v2/DNN//ROC_{here}_bdtgTest.pdf".format(here=bkg));


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


