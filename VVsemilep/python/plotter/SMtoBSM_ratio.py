import ROOT, os, subprocess, sys, optparse
ROOT.gROOT.SetBatch()
ROOT.gStyle.SetOptTitle(0)
ROOT.gStyle.SetOptStat(0);
ROOT.gStyle.SetOptStat(0)
ROOT.gStyle.SetOptFit(1111)
plotsdir="/eos/user/a/anmehta/www/VVsemilep/SMratios/newsamples/"
def makePlot(vname,yr,ff):
    outFile=ROOT.TFile("%s/res_%s_%s_%s.root"%(plotsdir,yr,vname,ff),"recreate")
    for bsm in ["smeftprod","eft_HTbinned"]:
        for sm in ["WZ","WW"]:
            bsm1="smeft" if "smeft" in bsm else "eft"
            inFile=ROOT.TFile.Open("/eos/user/a/anmehta/www/VVsemilep/%s/boosted/2025-05-14_%s_%s_sanitychk//mWV_logy_AND_FatJet1_pt_logy_AND_mWV_den_logy.root"%(yr,sm,bsm1))
            outFile.cd();
            canv=ROOT.TCanvas("canv", "%s_%s_%s"%(vname,sm,bsm),600,600);
            print("this is what i m looking for","%s_%s"%(vname,sm),inFile.GetName())
            h_sm=inFile.Get("%s_SM_%s"%(vname,sm))
            #if bsm == "smeft":
            #    h_eft=inFile.Get("%s_%s_%s"%(vname,sm,bsm))
            #else:
            h_eft=inFile.Get("%s_%s_%s_sm"%(vname,sm,bsm)) #eftdim6 are labeled as WW_sm in the files
            print("this is what i m looking for","%s_%s_%s_sm"%(vname,sm,bsm),inFile.GetName())
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
            canv.Print('%s/res_%s_%s_%s_%s_%s_new.pdf'%(plotsdir,vname,yr,sm,bsm,ff))
            canv.Print('%s/res_%s_%s_%s_%s_%s_new.png'%(plotsdir,vname,yr,sm,bsm,ff))
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
