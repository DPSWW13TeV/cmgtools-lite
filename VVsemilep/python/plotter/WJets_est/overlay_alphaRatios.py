import ROOT, os, optparse, copy, datetime
date = datetime.date.today().isoformat()

def histStyle(hist,xtitle,color,lstyle,mstyle):
    markerstyle = 20 
    hist.SetLineColor(color)
    hist.SetLineWidth(2)
    #hist.SetLineStyle(lstyle)
    hist.SetMarkerStyle(mstyle)
    hist.SetMarkerColor(color)
    hist.GetXaxis().SetTitle(xtitle)
    hist.GetYaxis().SetTitle('SR/CR')
    #print 'and here',hist.Integral()
    hist.GetYaxis().SetNdivisions(505)
    hist.GetXaxis().SetNdivisions(510)
    hist.GetYaxis().SetTitleOffset(1.25);    hist.GetXaxis().SetTitleOffset(1.25)
    hist.GetXaxis().SetTitleFont(42);        hist.GetYaxis().SetTitleFont(42);
    hist.GetXaxis().SetLabelFont(42);        hist.GetYaxis().SetLabelFont(42);
    hist.GetXaxis().SetTitleSize(0.035); hist.GetYaxis().SetTitleSize(0.035);
    hist.GetXaxis().SetMaxDigits(3);
    return hist

def gethists(filewithHists):
    histsinfile=[]
    filetoread = ROOT.TFile(filewithHists,'read')
    histsinfile = list(filetoread.GetListOfKeys())
    processes=[]

    for key in histsinfile:
        classname = key.GetClassName()
        cl = ROOT.gROOT.GetClass(classname)
        if(cl.InheritsFrom(ROOT.TH1.Class())):
            objectName = key.GetName()
            if objectName not in processes:
                processes.append(objectName)# if objectName not in processes]
    return processes

def drawhists(fname,color,lstyle,mstyle):
    filetoread = ROOT.TFile(fname,'READ')
    #print fname,pstate,hname,color,xsec
    h_num=filetoread.Get("mWV1_typ0_pmet_boosted_WJetsSR")
    h_deno=filetoread.Get("mWV1_typ0_pmet_boosted_WJetsCR")
    h_num.Scale(1.0/h_num.Integral())
    h_deno.Scale(1.0/h_deno.Integral())
    h_num.Divide(h_deno)
    #print type(histogram1)
    xaxis=h_num.GetXaxis()
    nbinsX=h_num.GetNbinsX();xbinlow=xaxis.GetBinLowEdge(1);xbinhigh=xaxis.GetBinLowEdge(nbinsX+1);
    #print nbinsX,xbinlow,xbinhigh
    histogram = ROOT.TH1F("histogram",'ratio%s'%fname, [890,944,1058., 1118, 1181, 1246, 1313, 1383, 1455, 1530, 1607, 1687, 1770, 1856, 1945, 2037, 2132, 2231, 2332, 2438, 2546, 2659, 2775, 2895, 3019, 3147, 3279, 3416, 3558, 3704, 3854, 4010, 4171, 4337, 4509]); #nbinsX,xbinlow,xbinhigh);
    histogram=h_num.Clone("histogram")
    histogram=histStyle(histogram,"mWV (GeV)",color,lstyle,mstyle)

    #print 'chk here',histogram.Integral()
    histogram.SetDirectory(0)
    #filetoread.Close()
    return histogram

def drawScans():

    basedir='/eos/user/a/anmehta/www/VVsemilep/2018/alphaRatio//'    
    outdir=basedir+'{when}_ratio'.format(when=date)

    if outdir not in os.listdir(basedir):
        os.system('mkdir -p {od}'.format(od=outdir))
        os.system('cp /afs/cern.ch/user/a/anmehta/index.php {od}'.format(od=outdir))

    ROOT.gROOT.SetBatch()
    ROOT.gStyle.SetOptStat(0)
    ROOT.gStyle.SetOptTitle(0)
    fout = ROOT.TFile("{od}/plots.root".format(od=outdir,when=date),"RECREATE")

    PS={'lep':[ROOT.kOrange+10,29],'el':[ROOT.kGreen+2,25],'mu':[ROOT.kBlue+1,24]}


    histograms=[];textforlegend=[];
    for iPS,icol in PS.iteritems():
        #print ihist
        fname= '/eos/user/a/anmehta/www/VVsemilep/2018/alphaRatio/2023-03-14_%sboosted/mWV1_typ0_pmet_boosted.root'%iPS
        histograms.append(drawhists(fname,icol[0],1,icol[1]));
        textforlegend.append(iPS)

    canv = ROOT.TCanvas("canv","",800,600);    canv.SetTickx(1);   canv.SetTicky(1); canv.cd();     canv.Draw();
    leg = ROOT.TLegend(0.5,0.75,0.85,0.85);   leg.SetLineColor(0);
    leg.SetTextFont(42);#leg.SetTextSize(0.045);
    leg.SetFillColor(0);leg.SetFillStyle(0);
    leg.SetTextSize(0.03);        leg.SetFillStyle(0);        leg.SetFillColor(0);       
    leg.SetNColumns(3);        leg.SetLineColor(ROOT.kWhite)
    leg.AddEntry(histograms[0],textforlegend[0],'p')
    ymax=max(list(i.GetMaximum() for i in histograms))
    #print ymax
    histograms[0].SetMaximum(ymax*1.5)
    histograms[0].Draw('Ex0')

    for hist in range(1,len(histograms)):
        histograms[hist].Draw('Ex0SAME')
        leg.AddEntry(histograms[hist],textforlegend[hist],'p')

    leg.Draw('same')
    
    fout.WriteTObject(canv)
    canv.SaveAs('{od}/ratio.pdf'.format(od=outdir))
    canv.SaveAs('{od}/ratio.png'.format(od=outdir))

if __name__ == '__main__':
    parser = optparse.OptionParser(usage='usage: %prog [opts] ', version='%prog 1.0')
    parser.add_option('--drawScans', action='store_true', dest='drawScans'        , default=True, help='overlay shapes for VBS ssWW')
    global opts
    (opts, args) = parser.parse_args()


    if opts.drawScans:
        drawScans()
