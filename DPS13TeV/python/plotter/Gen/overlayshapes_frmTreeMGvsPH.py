# make sure you update the reference file from which list of histograms is taken
import ROOT, os, optparse, copy, datetime
date = datetime.date.today().isoformat()

def histStyle(hist,xtitle,color,lstyle,xsec):
    markerstyle = 20 
    hist.SetLineColor(color)
    hist.SetLineWidth(2)
    hist.SetLineStyle(lstyle)
    hist.GetXaxis().SetTitle(xtitle)
    hist.GetYaxis().SetTitle('a.u.')
    #print 'and here',hist.Integral()
    hist.GetYaxis().SetNdivisions(505)
    hist.GetXaxis().SetNdivisions(510)
    hist.GetYaxis().SetTitleOffset(1.5)
    hist.Scale(1.0/hist.Integral())
    ROOT.SetOwnership(hist,False);
    return hist

def gethists(filewithHists):
    histsinfile=[]
    filetoread = ROOT.TFile(filewithHists,'read')
    histsinfile = list(filetoread.GetListOfKeys())
    processes=[]

    for key in histsinfile:
        classname = key.GetClassName()
        cl = ROOT.gROOT.GetClass(classname)
        if(cl.InheritsFrom(ROOT.TH1F.Class())):
            objectName = key.GetName()
            if objectName not in processes:
                processes.append(objectName)# if objectName not in processes]
    return processes

def drawhists(fname,pstate,hname,color,lstyle,xsec):
    filetoread = ROOT.TFile(fname,'READ')
    histogram1=filetoread.Get(hname)
    xaxis=histogram1.GetXaxis()
    nbinsX=histogram1.GetNbinsX();xbinlow=xaxis.GetBinLowEdge(1);xbinhigh=xaxis.GetBinLowEdge(nbinsX+1);
    histogram = ROOT.TH1F('histogram{FS}{PS}{hist}'.format(FS=fname,PS=pstate,hist=hname),'',nbinsX,xbinlow,xbinhigh);
    histogram=histStyle(histogram1,hname,color,lstyle,xsec)
    histogram.SetDirectory(0)
    return histogram

def gethistfrmtree(fname,hname,nXbins,xmin,xmax,xtitle,color,lstyle,xsec):
    fIn =ROOT.TFile('{fname}.root'.format(fname=fname),'read')
    tree=fIn.Get('tree')
    print hname,fname, tree.GetEntries()
    h_dummy   = ROOT.TH1F('h_dummy' ,'',nXbins,xmin,xmax)
    h_dummy.Sumw2()
    sel='pdgIdl1 + pdgIdl2 == -24 && min(ptl1,ptl2) > 20 && abs(etal1) < 2.5 && abs(etal2) < 2.5'
    tree.Draw('{here}>>h_dummy'.format(here=hname),sel, "goff")
    dummy = histStyle(h_dummy,xtitle,color,lstyle,xsec)
    dummy.SetDirectory(0)
    return dummy


def drawScans():
    basedir='/eos/user/a/anmehta/www/DPSWW_v2/'
    genlevel=True
    outdir='{Here}{when}{here}'.format(Here=basedir,when=date,here='gen' if genlevel else '')
    print outdir 
    if outdir not in os.listdir(basedir):
        #print os.listdir(currentpath)
        os.system('mkdir -p {od}'.format(od=outdir))
        os.system('cp /afs/cern.ch/user/a/anmehta/index.php {od}'.format(od=outdir))

    ROOT.gROOT.SetBatch()
    ROOT.gStyle.SetOptStat(0)
    ROOT.gStyle.SetOptTitle(0)
    fout = ROOT.TFile("{od}/plots.root".format(od=outdir),"RECREATE")
    FS={'WpmWpm':1}
    PS={'tree_Friend_DPS2017HWpp_gen':['HW++',ROOT.kOrange+7,1],'tree_Friend_WWTo2L2NuDPSpy8_gen':['P8_CUET',ROOT.kRed,6],'tree_Friend_WWDPSCP5py8_gen':['P8_CP5',ROOT.kAzure+1,9], 'DPS_noShower_genlevel':['new sim without shower',ROOT.kMagenta+1,7],'DPS_withShower_genlevel':['new sim with shower',ROOT.kGreen+2,2]}


    hdraw={
        'mll':['m_{ll}',50,0,200],
        'ptl1':['p_{T}^{l1}',20,0.0,100.0],
        'ptl2':['p_{T}^{l2}',20,0.0,100.0],
        'ptel':['p_{T}^{el}',20,0.0,100.0],
        'ptmu':['p_{T}^{#mu}',20,0.0,100.0],
        'etamu':['#eta^{#mu}',10,-2.5,2.5],
        'etael':['#eta^{el}',10,-2.5,2.5],
        #'ptnn':['p_{T}^({miss}',30,0,300.0],
        'etal2':['#eta^{l2}',10,-2.5,2.5],
        'etal1':['#eta^{l1}',10,-2.5,2.5],
        'detall':['#Delta#eta^{ll}',30,0,5],
        'dphill':['#Delta#phi^{ll}',8,0,3.2],
        'dRll':['#DeltaR_{ll}',25,0,5],
        'nleps':['nleps',4,0,4],
        'etal1*etal2':['#eta^{l1}#eta^{l2}',10,-6.25,6.25],
        'etal1*etal2 > 0':['#eta^{l1}#eta^{l2} > 0',2,0,2],
        'etal1*etal2 < 0':['#eta^{l1}#eta^{l2} < 0',2,0,2],
        'etal1+etal2 ':['#eta^{l1}+#eta^{l2}',10,-5,5],
        'pdgIdl1':['pdgIdl1',30,-15,15],
        'pdgIdl2':['pdgIdl2',30,-15,15]
       }

    for ihist,ival in hdraw.iteritems():
        histograms=[];textforlegend=[];
        for iFS,istyle in FS.iteritems():
            for iPS,icol in PS.iteritems():
                #print ihist
                histograms.append(gethistfrmtree(iPS,ihist,ival[1],ival[2],ival[3],ival[0],icol[1],icol[2],1))
                textforlegend.append('{FS}'.format(FS=icol[0]))

        canv = ROOT.TCanvas("canv{HERE}".format(HERE=ihist),"",800,600);    canv.SetTickx(1);   canv.SetTicky(1); ROOT.SetOwnership(canv,False); canv.cd();    splitpoint = 0.7;
        leg = ROOT.TLegend(0.15,0.8,0.85,0.875);   leg.SetLineColor(0);
        leg.SetTextFont(42);leg.SetTextSize(0.03);
        leg.SetNColumns(3);
        leg.SetFillColor(0);leg.SetFillStyle(0);leg.SetLineColor(ROOT.kWhite)
        leg.AddEntry(histograms[0],textforlegend[0],'l')
        #pad1.cd()
        ymax=max(list(i.GetMaximum() for i in histograms))
        ymin=min(list(i.GetMinimum() for i in histograms))
        #print ymax
        histograms[0].SetMaximum(ymax*1.15)
        histograms[0].SetMinimum(ymin*0.99)
        histograms[0].Draw('ehist')

        for hist in range(1,len(histograms)):
            histograms[hist].Draw('ehistsame')
            leg.AddEntry(histograms[hist],textforlegend[hist],'l')
        leg.Draw('same')
    
        fout.WriteTObject(canv)
        canv.SaveAs('{od}/shapes_{mww}.pdf'.format(od=outdir,mww=ihist))
        canv.SaveAs('{od}/shapes_{mww}.png'.format(od=outdir,mww=ihist))

if __name__ == '__main__':
    parser = optparse.OptionParser(usage='usage: %prog [opts] ', version='%prog 1.0')
    parser.add_option('--drawScans', action='store_true', dest='drawScans', default=True, help='overlay shapes for DPS ssWW')
    global opts
    (opts, args) = parser.parse_args()


    if opts.drawScans:
        drawScans()
