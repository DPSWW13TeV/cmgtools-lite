import ROOT,os,datetime,optparse
date = datetime.date.today().isoformat()
path = '/eos/cms/store/cmst3/group/dpsww/'
_allfiles=[]


samples=['WJetsToLNu_LO','WWDoubleTo2L']
paths=['forWWmixing/2016/','NanoTrees_v7_dpsww_04092020/2016/']
friends=['dpsbdt_neu_ssnoeebkg_afacdps']
def histStyle_v1(hist,xtitle,ytitle,xtoff,ytoff,tsize,lsize,color,lstyle=1,lwidth=1,mstyle='',msize=1.0):
    hist.GetXaxis().SetTitleOffset(xtoff);             hist.GetYaxis().SetTitleOffset(ytoff)
    hist.GetXaxis().SetTitle(xtitle);                  hist.GetYaxis().SetTitle(ytitle);
    hist.GetXaxis().SetLabelSize(lsize);              hist.GetYaxis().SetLabelSize(lsize);
    hist.GetXaxis().SetTitleSize(tsize);              hist.GetYaxis().SetTitleSize(tsize);
    hist.GetXaxis().SetTitleFont(42);            hist.GetYaxis().SetTitleFont(42);
    hist.GetXaxis().SetLabelFont(42);            hist.GetYaxis().SetLabelFont(42);
    hist.SetLineColor(color);hist.SetLineWidth(lwidth);
    if mstyle != '':
        hist.SetMarkerStyle(mstyle); hist.SetMarkerColor(color); hist.SetMarkerSize(msize);
    return hist
def getAll(bdir,fname):
    fileloc = os.path.join(path,bdir,'bdt_input_vars_toInfnBeynd/%s_Friend.root' %fname)
    infile = ROOT.TFile.Open(fileloc)
    _allfiles.append(infile)
    tree = infile.Get('Friends')
    for friend in friends:
        friendloc = os.path.join(path,bdir,friend,'%s_Friend.root' % fname)
        tree.AddFriend('Friends', friendloc)
    return tree
def histStyle(hist,xtitle,color,lstyle=1,xsec=1):
    markerstyle = 20; lsize=0.045;tsize=0.055
    hist.SetLineColor(color)
    hist.SetLineWidth(2)
    hist.SetLineStyle(lstyle)
    hist.GetXaxis().SetTitle(xtitle)
    hist.GetYaxis().SetTitle('a.u.')
    hist.GetYaxis().SetNdivisions(505)
    hist.GetXaxis().SetNdivisions(510)
    hist.GetYaxis().SetTitleOffset(1.0)
    hist.GetXaxis().SetTitleFont(42);            hist.GetYaxis().SetTitleFont(42);
    hist.GetXaxis().SetLabelFont(42);            hist.GetYaxis().SetLabelFont(42);
    hist.GetXaxis().SetLabelSize(lsize);              hist.GetYaxis().SetLabelSize(lsize);
    hist.GetXaxis().SetTitleSize(tsize);              hist.GetYaxis().SetTitleSize(tsize);

    hist.Scale(xsec)
    hist.Scale(1.0/hist.Integral())
    return hist

def gethist(tree,selcuts,vname,xtitle,nXbins,xmin,xmax, color = 1):
    hist1   = ROOT.TH1F("hist1" ,'',nXbins,xmin,xmax)
    if vname.startswith('d'):
        tree.Draw('abs({here})>>hist1'.format(here=vname), selcuts, 'goff')
    else :
        tree.Draw('{here}>>hist1'.format(here=vname), selcuts, 'goff')
    #tree.Draw('{here}>>hist1'.format(here=abs(vname) if vname.startswith('d') else vname),selcuts, 'goff')
    #tree.Draw('{here}>>hist1'.format(here=vname), '', 'goff')
    hist1 = histStyle(hist1,xtitle,color)

    hist1.SetDirectory(0)
    return hist1

#def overlayshapes():
if __name__ == '__main__':
    basedir='/eos/user/a/anmehta/www/DPSWW_v2/'
    outdir='{Here}{when}_signal_vs_randomMix'.format(Here=basedir,when=date)
    if outdir not in os.listdir(basedir):
        os.system('mkdir -p {od}'.format(od=outdir))
        os.system('cp /afs/cern.ch/user/a/anmehta/index.php {od}'.format(od=outdir))

pdraw={'Lep1_conept':[10,0,100,'p_{T}^{l_{1}}'],
       'Lep2_conept':[10,0,100,'p_{T}^{l_{2}}'],
       'mt2':[10,0,100,'m_{T2}^{ll}'],
       'mtll':[10,0,100,'m_{T2}^{ll}'],
       'mtl1met':[10,0,100,'mtl1met'],
       'dphill':[10,0,3.2,'dphill'],
       'met':[10,0,100,'met'],
       'dphil2met':[10,0,3.2,'dphil2met'],
       'dphilll2':[10,0,3.2,'dphilll2'],
       'cptll':[10,0,100,'ptll'],
       'mll':[10,0,100,'mll'],
       #'deltadz':[40,0,0.004],
       #'deltadxy':[40,0,0.004],
       'BDTG_DPS_WZ_amc_raw_withpt':[20,-1.0,1.0,'BDT-WZ']}

sel = 'Lep1_pt > 25 && Lep2_pt > 20 && (Lep2_pdgId*Lep1_pdgId) >0 && met > 15 && mll >12 && Lep1_isLepTight &&  Lep2_isLepTight && ((abs(Lep1_pdgId) == 13 && abs(Lep2_pdgId) == 13) || cptll > 20) && (abs(Lep1_pdgId)!=11 || ( Lep1_tightCharge>=2)) && (abs(Lep2_pdgId)!=11 || (Lep2_tightCharge>=2)) && (abs(Lep1_pdgId)!=13 || Lep1_tightCharge>=1) && (abs(Lep2_pdgId)!=13 || Lep2_tightCharge>=1)'
for ikey,ival in pdraw.iteritems():
    print ikey
    ROOT.gROOT.SetBatch()
    ROOT.gStyle.SetOptStat(0)
    canv = ROOT.TCanvas('{here}'.format(here=ikey), 'bar', 600, 600)
    canv.Range(0,0,1,1);   canv.SetFillColor(0);   canv.SetBorderMode(0);   canv.SetBorderSize(2);
    canv.SetTickx(1);   canv.SetTicky(1);   canv.SetLeftMargin(0.16);   canv.SetRightMargin(0.08);
    canv.SetBottomMargin(0.13);   canv.SetFrameFillStyle(0);   canv.SetFrameBorderMode(0);
    c1_1 = ROOT.TPad("c1_1", "newpad",0.01,0.33,0.99,0.99);
    c1_1.Draw();        c1_1.cd();
    c1_1.SetTopMargin(0.13);  c1_1.SetBottomMargin(0.04);  c1_1.SetRightMargin(0.1);        c1_1.SetFillStyle(0);
    c1_1.SetBorderMode(0);        c1_1.SetBorderSize(2);c1_1.SetFrameBorderMode(0);c1_1.SetFrameLineWidth(2);
    c1_1.SetFrameBorderMode(0);   c1_1.SetTicky(1);


    tr_WW=getAll(paths[0],samples[0])
    tr_sig=getAll(paths[1],samples[1])
    h_ex0 = gethist(tr_WW,sel,ikey,ival[3],ival[0],ival[1],ival[2],ROOT.kOrange+10)
    
    h_ex1 = gethist(tr_sig,sel,ikey,ival[3],ival[0],ival[1],ival[2],ROOT.kAzure+4)
    ymax=max(h_ex0.GetMaximum(),h_ex1.GetMaximum())
    h_ex0.GetYaxis().SetRangeUser(0.,ymax+ymax/2.0)
    h_ratio=h_ex0.Clone();    h_ratio.Sumw2();
    h_ratio.Divide(h_ex1);



    
    h_ex0.GetXaxis().SetLabelOffset(9999999);
    h_ex0.Draw('hist')
    h_ex1.Draw('histsame')

    leg = ROOT.TLegend(0.6, 0.65, 0.8, 0.875)
    leg.SetTextSize(0.045); leg.SetShadowColor(0);        leg.SetFillStyle(0);    leg.SetTextFont(42);   leg.SetBorderSize(0);

    leg.AddEntry('NULL', 'W^{#pm}W^{#pm}'  , '')
    leg.AddEntry(h_ex0, 'randomly mixed WW'  , 'l')
    leg.AddEntry(h_ex1, 'DPSWW'  , 'l')
    leg.SetLineColor(ROOT.kWhite);    leg.SetFillColor(ROOT.kWhite)
    leg.Draw('same')

    canv.cd();

    c1_2 = ROOT.TPad("c1_2","ratioplot",0.01,0.01,0.99,0.33);    c1_2.Draw();    c1_2.cd();
    c1_2.SetTopMargin(0.041); c1_2.SetBottomMargin(0.3);   c1_2.SetRightMargin(0.1);c1_2.SetBorderMode(0);c1_2.SetTicky(1);
    c1_2.SetBorderSize(2); c1_2.SetFillStyle(0);c1_2.SetFrameBorderMode(0);c1_2.SetFrameLineWidth(2);c1_2.SetFrameBorderMode(0); 


    line1 = ROOT.TLine(ival[1],1.0,ival[2],1.0);
    line1.SetLineColor(58);   line1.SetLineWidth(2);   line1.SetLineStyle(1);
    #h_ratio.SetLineColor(ROOT.kRed);h_ratio.SetMarkerColor(ROOT.kRed);h_ratio.SetMarkerStyle(21); h_ratio.GetYaxis().SetTitle("random/sig");
    h_ratio=histStyle_v1(h_ratio,ival[3],"random/sig",xtoff=0.8,ytoff=0.35,tsize=0.15,lsize=0.1,color=ROOT.kRed,lstyle=1,lwidth=2,mstyle=20,msize=1.0)
    #histStyle_v1(hist,xtitle,ytitle,xtoff,ytoff,tsize,lsize,color,lstyle=1,lwidth=1,mstyle='',msize=0.85):
    
    h_ratio.GetYaxis().SetRangeUser(0.02,3.0)
    h_ratio.Draw("E1X0");
    line1.Draw("E2SAME");

    canv.SaveAs('{od}/{mww}.pdf'.format(od=outdir,mww=ikey))
    canv.SaveAs('{od}/{mww}.png'.format(od=outdir,mww=ikey))
    
    
##if __name__ == '__main__':
##    parser = optparse.OptionParser(usage='usage: %prog [opts] ', version='%prog 1.0')
##    parser.add_option('--overlayshapes', action='store_true', dest='overlayshapes'        , default=True, help='blah blah ')
##    global opts
##    (opts, args) = parser.parse_args()
##
##
##    if opts.overlayshapes:
##        overlayshapes()
