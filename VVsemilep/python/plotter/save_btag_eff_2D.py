import os,ROOT
ROOT.gROOT.SetBatch()
ROOT.gStyle.SetOptStat(0)

outdir="/eos/user/a/anmehta/www/VVsemilep/"
fIn=ROOT.TFile.Open("/afs/cern.ch/work/a/anmehta/public/cmgtools_WVsemilep/CMSSW_12_1_1/src/CMGTools/TTHAnalysis/data/btag/btagEffs_TopEFT_2022_05_16.root");
for yr in ["2016","2017","2018","2016apv"]:
    for flav in ["B","C","L"]:
        canv=ROOT.TCanvas("canv%s%s"%(yr,flav),"",800,700);
        canv.Range(0,0,1,1);   canv.SetFillColor(0);   canv.SetBorderMode(0);   canv.SetBorderSize(2);
        canv.SetTickx(1);   canv.SetTicky(1);   canv.SetLeftMargin(0.1);   canv.SetRightMargin(0.15);
        canv.SetBottomMargin(0.13);   canv.SetFrameFillStyle(0);   canv.SetFrameBorderMode(0);

        hist=fIn.Get("BtagSF{h}_DeepFlavM_{yr}".format(yr=yr,h=flav))
        hist.GetYaxis().SetTitle('|#eta|')
        hist.GetXaxis().SetTitle('p_{T} (GeV)')
        hist.GetZaxis().SetTitle('eff.')
        hist.GetZaxis().SetTitleOffset(1.3)
        hist.GetXaxis().SetTitleSize(0.04)
        hist.GetYaxis().SetTitleSize(0.04)
        hist.GetZaxis().SetTitleSize(0.04)

        hist.Draw("textcolz");
        canv.SaveAs('{od}/histoBtagEff_SF{wp}_{yr}.pdf'.format(yr=yr,wp=flav,od=outdir))
        canv.SaveAs('{od}/histoBtagEff_SF{wp}_{yr}.png'.format(yr=yr,wp=flav,od=outdir))
        canv.Close();
fIn.Close();
