import ROOT, re, os, subprocess, sys, optparse, datetime
ROOT.gROOT.SetBatch();    ROOT.gStyle.SetOptFit(0);ROOT.gStyle.SetOptStat(0);

SAFE_COLOR_LIST=[ROOT.kRed+2,ROOT.kOrange+7, ROOT.kAzure+1,ROOT.kMagenta+1,ROOT.kGreen+2, ROOT.kBlue, ROOT.kViolet+5, ROOT.kSpring+5, ROOT.kPink+7, ROOT.kYellow, ROOT.kGray, ROOT.kMagenta+3, ROOT.kBlack]
#legend.AddEntry('NULL','BDTG','');
indir='/afs/cern.ch/work/a/anmehta/public/dpsww_runII/CMSSW_10_2_16_UL/src/CMGTools/DPSWW/python/plotter/BDTtraining/'
#/eos/cms/store/cmst3/group/dpsww/BDT_optimization/IPvars/'#/eos/cms/store/cmst3/group/dpsww/BDT_optimization/'
outdir='/eos/user/a/anmehta/www/DPSWW_v2/BDT/eta/'
variables=['','etasum','etadiff','etaprod']#,'dz']#'mt2','mtll','mtl1','pt1','pt2','dphil2met','dphill','dphilll2','etaprod','etasum','met',
templates={'wz':['wz_amc',ROOT.kAzure+1],'TL':['fakes',ROOT.kOrange+7]}
signalMC=['py']#'hw','py','ns']  #{'py':['py',ROOT.kAzure+1],'hw':['hw',ROOT.kOrange+7],'ns':['ns',ROOT.kMagenta]} #
years=[2016,2017,2018]



for bkg,iset in templates.iteritems():    
    for yr in years:
        for sig in signalMC:
            c1 = ROOT.TCanvas("c1%s%d%s"%(bkg,yr,sig),"",200,45,650,500);ROOT.SetOwnership(c1,False);
            c1.Range(-0.128266,-0.1538462,1.059382,1.128205);c1.SetBorderSize(2);c1.SetGridx();
            #c1.SetGridy();
            c1.SetTickx(1);c1.SetTicky(1);  c1.SetRightMargin(0.05);c1.SetBottomMargin(0.12);c1.SetFrameBorderMode(0);
            c1.cd();
            leg = ROOT.TLegend(0.15,0.58,0.25,0.7);
            leg.SetFillColor(0);leg.SetFillStyle(0);leg.SetShadowColor(0);leg.SetLineColor(0);leg.SetTextFont(42);leg.SetBorderSize(0); leg.SetTextSize(0.035);leg.SetTextColor(ROOT.kBlue);
            leg.AddEntry('NULL','allvars #rightarrow 11 vars + etadiff','')
            leg.AddEntry('NULL','sig. = {s}; bkg. = {b}; yr = {y}'.format(s=sig,b=bkg,y=str(yr)),'')
            
            legend = ROOT.TLegend(0.15,0.25,0.3,0.55);
            legend.SetFillColor(0);legend.SetFillStyle(0);legend.SetShadowColor(0);legend.SetLineColor(0);legend.SetTextFont(42);legend.SetBorderSize(0); legend.SetTextSize(0.03);


            #legend.SetNColumns(2);

            mg = ROOT.TMultiGraph("mg","");        graphs=[];text4legend=[];
            for ip in variables:
                commonstr='Nov2021_dpsWW_'+sig+"_"+iset[0]
                pf='%s_withpt'%(str(yr))
                if len(ip) == 0:
                    fName='{cs}_allvars{pf}'.format(cs=commonstr,pf=pf)
                else:
                    fName='{cs}_allbut_{here}{pf}'.format(pf=pf,cs=commonstr,here=ip)
                print fName
                file1= ROOT.TFile((indir+fName+".root"),"read");
                ROOT.gDirectory.cd("dataset_{here}/Method_BDTG/BDTG".format(here=fName))
                graph = ROOT.gDirectory.Get("MVA_BDTG_Test_rejBvsS_Signal");#MVA_BDTG_S"); #
                if graph == None:
                    graph = ROOT.gDirectory.Get("MVA_BDTG_rejBvsS");
                graphs.append(graph); ROOT.SetOwnership(graph,False);
                if "TH1" in graph.ClassName(): graph.SetDirectory(0)
                #print 'AUC for %s is %f'%(commonstr,graph.Integral())
                graph.SetLineStyle(variables.index(ip)+1);                
                graph.SetLineColor(iset[1]);                 graph.SetName("gr"+fName);   
                #graph.SetLineColor(SAFE_COLOR_LIST[years.index(yr)]); graph.SetLineWidth(2); 
                #graph.Rebin(2);graph.Scale(1.0/graph.Integral()); 
                auc='%.2f'%(graph.Integral())
                #print auc
                text4legend.append('{what}{VV} [AUC={auc}]'.format(auc=auc,what='allvars' if len(ip) == 0 else 'allbut-',VV=ip))
                #text4legend.append('{sig}_vs_{bkg}_{when}'.format(sig=sig,bkg=bkg,when=str(yr),what='allvars' if len(ip) == 0 else 'allbut-',VV=ip))
        dummy = ROOT.TH2F("dummy%s%d"%(sig,yr),"",100,0,1.0,100,0,1.0); # for roc
        #dummy = ROOT.TH2F("dummy","",100,0,1.0,1000,0,1.5);
        dummy.SetLineWidth(2);dummy.SetMarkerStyle(21);dummy.SetMarkerSize(0.3);
        dummy.GetXaxis().SetTitle("Signal Efficiency");dummy.GetXaxis().SetLabelOffset(0.012);
        dummy.GetXaxis().SetTitleSize(0.045);dummy.GetXaxis().SetTitleOffset(1.2);
        dummy.GetYaxis().SetTitle("Background Rejection (1 - eff)");
        dummy.GetYaxis().SetLabelOffset(0.012);dummy.GetYaxis().SetTitleSize(0.045);dummy.GetYaxis().SetTitleOffset(1.08);
        dummy.Draw();

        graphs[0].Draw("hist");
    
        #graphs[0].GetYaxis().SetRangeUser(0,0.2)
        legend.AddEntry(graphs[0],text4legend[0],'l')
        for i in range(1,len(graphs)):
            if "TH1" in graphs[i].ClassName():
                graphs[i].Draw("histsame")
            else:
                mg.Add(graphs[i])
            legend.AddEntry(graphs[i],text4legend[i],'l')
        mg.Draw('L')
        legend.Draw("same"); 
        leg.Draw("same"); 

        c1.SaveAs("{od}/ROC_varScan_{sig}vs{here}_{yr}.png".format(yr=yr,sig=sig,od=outdir,here=bkg));
        c1.SaveAs("{od}/ROC_varScan_{sig}vs{here}_{yr}.pdf".format(yr=yr,sig=sig,od=outdir,here=bkg));



