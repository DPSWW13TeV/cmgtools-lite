import ROOT
from ROOT import TFile, TH1D, TH2D
import os, sys, getopt, glob
from array import array

ROOT.gROOT.SetBatch() 
ROOT.gStyle.SetOptStat(0); ROOT.gStyle.SetTextFont(42)
if __name__ == "__main__":
    path = "fillhisto_puAnalysis"
    year = 2018
    output = "anaZ"

    fileBTV = TFile.Open("/eos/user/a/anmehta/www/VVsemilep/2018/SR/2023-09-21_onelepboosted_withoutSFs_cutflow/Jet_eta_pt.root");
    dir_deno="cut_11_mWVtyp0pmet/"
    dir_L="cut_13_Loosebtag/"
    dir_M="cut_14_Medbtag/"
    histName="Jet_eta_pt_tt"
    fileBTV.cd();
    hist_deno=fileBTV.Get(str(dir_deno+histName));
    hist_T=fileBTV.Get(histName);
    hist_L=fileBTV.Get(str(dir_L+histName));
    hist_M=fileBTV.Get(str(dir_M+histName));
    WPs=['loose','medium','tight']
    numberOfSel = 3

    histoBtagDenSelEtaPt = hist_deno.Clone()
    histoBtagNumSelEtaPt = [hist_deno.Clone().Reset(),hist_deno.Clone().Reset(),hist_deno.Clone().Reset()]
    histoBtagEffSelEtaPt = [hist_deno.Clone(),hist_deno.Clone(),hist_deno.Clone()]
    fileLepEffName = "histoBtagEffSelEtaPt.root"
    basedir="/eos/user/a/anmehta/www/VVsemilep/"
    outFileLepEff = TFile("/eos/user/a/anmehta/www/VVsemilep/btag_eff2018.root","recreate")
    outFileLepEff.cd()

    
    histoBtagNumSelEtaPt[0] = hist_L.Clone()
    histoBtagNumSelEtaPt[1] = hist_M.Clone()
    histoBtagNumSelEtaPt[2] = hist_T.Clone()

    for theNumSel in range(0,numberOfSel):
        canv=ROOT.TCanvas("canv%d"%theNumSel,"",800,700);
        canv.Range(0,0,1,1);   canv.SetFillColor(0);   canv.SetBorderMode(0);   canv.SetBorderSize(2);
        canv.SetTickx(1);   canv.SetTicky(1);   canv.SetLeftMargin(0.1);   canv.SetRightMargin(0.15);
        canv.SetBottomMargin(0.13);   canv.SetFrameFillStyle(0);   canv.SetFrameBorderMode(0);
        for i in range(histoBtagDenSelEtaPt.GetNbinsX()):
            for j in range(histoBtagDenSelEtaPt.GetNbinsY()):
                den0 = histoBtagDenSelEtaPt.GetBinContent(i+1,j+1)
                num0 = histoBtagNumSelEtaPt[theNumSel].GetBinContent(i+1,j+1)
                eff0 = 1.0;                unc0 = 0.0
                if(den0 > 0 and num0 > 0 and num0 <= den0):
                    eff0 = num0 / den0
                    unc0 = pow(eff0*(1-eff0)/den0,0.5)
                    #print num0,den0,eff0,unc0
                elif(den0 > 0):
                    eff0 = 0.0
                    unc0 = min(pow(1.0/den0,0.5),0.999)
                print type(histoBtagEffSelEtaPt[theNumSel])
                histoBtagEffSelEtaPt[theNumSel].SetBinContent(i+1,j+1,eff0)
                histoBtagEffSelEtaPt[theNumSel].SetBinError  (i+1,j+1,unc0)
                print("({0:2d},{1:2d}): ({2:.3f} +/- {3:.3f})".format(i+1,j+1,eff0,unc0))
    
        histoBtagEffSelEtaPt[theNumSel].SetNameTitle("histoBtagEffSelEtaPt_{0}".format(WPs[theNumSel]),"histoBtagEffSelEtaPt_{0}".format(WPs[theNumSel]))
        histoBtagEffSelEtaPt[theNumSel].GetXaxis().SetTitle('|#eta|')
        histoBtagEffSelEtaPt[theNumSel].GetYaxis().SetTitle('p_{T}')
        histoBtagEffSelEtaPt[theNumSel].GetZaxis().SetTitle('eff')
        histoBtagEffSelEtaPt[theNumSel].GetYaxis().SetTitleOffset(1.08)
        histoBtagEffSelEtaPt[theNumSel].GetZaxis().SetTitleOffset(0.9)
        histoBtagEffSelEtaPt[theNumSel].GetXaxis().SetTitleSize(0.04)
        histoBtagEffSelEtaPt[theNumSel].GetYaxis().SetTitleSize(0.04)
        histoBtagEffSelEtaPt[theNumSel].GetZaxis().SetTitleSize(0.04)
        histoBtagEffSelEtaPt[theNumSel].Draw("colz")

        #histoBtagEffSelEtaPt[theNumSel].Write()
        canv.SaveAs('{od}/histoBtagEffSelEtaPt_{wp}.pdf'.format(wp=WPs[theNumSel],od=basedir));
        canv.SaveAs('{od}/histoBtagEffSelEtaPt_{wp}.png'.format(wp=WPs[theNumSel],od=basedir));
    
    outFileLepEff.Write();
    outFileLepEff.Close();
