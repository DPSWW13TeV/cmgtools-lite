import ROOT, os, subprocess, sys, optparse
ROOT.gROOT.SetBatch()
ROOT.gStyle.SetOptTitle(0)
ROOT.gStyle.SetOptStat(0);
ROOT.gStyle.SetOptStat(0)
ROOT.gStyle.SetOptFit(1111)

def makePlot(vname,yr,ff):
    outFile=ROOT.TFile("/eos/user/a/anmehta/www/VVsemilep/res_%s_%s_%s.root"%(yr,vname,ff),"recreate")
    for bsm in ["eft","smeft"]:
        inFile=ROOT.TFile.Open("/eos/user/a/anmehta/www/VVsemilep/%s/boosted/2025-04-28_WV_%s_sanitychk//mWV_logy_AND_FatJet1_pt_logy_AND_FatJet1_sDrop_mass_logy.root"%(yr,bsm))
        for sm in ["WZ","WW"]:
            outFile.cd();
            canv=ROOT.TCanvas("canv", "%s_%s_%s"%(vname,sm,bsm),600,600);
            print("this is what i m looking for","%s_%s"%(vname,sm))
            h_sm=inFile.Get("%s_SM_%s"%(vname,sm))
            #if bsm == "smeft":
            #    h_eft=inFile.Get("%s_%s_%s"%(vname,sm,bsm))
            #else:
            h_eft=inFile.Get("%s_%s_sm"%(vname,sm)) #eftdim6 are labeled as WW_sm in the files
            print("integrals",h_sm.Integral(),"\t ",bsm,"\t",h_eft.Integral())
            ratio=h_sm.Clone("ratio")
            ratio.Divide(h_eft)
            h1=ratio.Clone("ratio_%s_%s_%s_%s"%(vname,sm,bsm,yr));
            h1.Fit(ff);
            h1.GetXaxis().SetTitle("mWV (GeV)");
            h1.GetYaxis().SetTitleOffset(1.05)
            h1.GetYaxis().SetTitle("{proc} sm/{eft}#rightarrow sm".format(proc=sm,eft=bsm));
            h1.GetYaxis().SetTitleSize(0.04)
            h1.GetXaxis().SetTitleSize(0.04)
            h1.GetYaxis().SetLabelSize(0.03)
            h1.GetXaxis().SetLabelSize(0.03)

            

            #rtrp1 = ROOT.TRatioPlot(h1);
            #rp1.Draw();
            #rp1.GetLowerRefYaxis().SetTitle("sm/eft");
            #rp1.GetUpperRefYaxis().SetTitle("sm/eft");
            canv.Update();
            canv.Print('/eos/user/a/anmehta/www/VVsemilep/SMratios/res_%s_%s_%s_%s_%s_new.pdf'%(vname,yr,sm,bsm,ff))
            canv.Print('/eos/user/a/anmehta/www/VVsemilep/SMratios/res_%s_%s_%s_%s_%s_new.png'%(vname,yr,sm,bsm,ff))
            canv.Close()
            h1.Write()
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
