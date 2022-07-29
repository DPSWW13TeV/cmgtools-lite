import ROOT, math
from array import array

ROOT.gROOT.SetBatch();ROOT.gStyle.SetOptStat(0);    ROOT.gStyle.SetOptTitle(0)
SAFE_COLOR_LIST=[ROOT.kOrange+7, ROOT.kAzure+1,ROOT.kMagenta+1, ROOT.kCyan+1,ROOT.kRed, ROOT.kGreen+2, ROOT.kBlue , ROOT.kGray+2, ROOT.kViolet+5, ROOT.kSpring+5, ROOT.kPink+7, ROOT.kOrange+3, ROOT.kBlue+3, ROOT.kMagenta+3, ROOT.kRed+2]
def histStyle(hist,xtitle,ytitle,xoffset,yoffset,titlesize,labelsize):

    hist.GetXaxis().SetTitle(xtitle);        hist.GetYaxis().SetTitle(ytitle);
    hist.GetXaxis().SetTitleSize(titlesize); hist.GetYaxis().SetTitleSize(titlesize); 
    hist.GetXaxis().SetTitleFont(42);        hist.GetYaxis().SetTitleFont(42);
    hist.GetXaxis().SetTitleOffset(xoffset); hist.GetYaxis().SetTitleOffset(yoffset);
    hist.GetXaxis().SetLabelSize(labelsize); hist.GetYaxis().SetLabelSize(labelsize);
    hist.GetXaxis().SetLabelFont(42);        hist.GetYaxis().SetLabelFont(42);

    if "TH2" in hist.ClassName():
        hist.GetZaxis().SetLabelFont(42);    hist.GetZaxis().SetLabelSize(labelsize);    hist.GetZaxis().SetTitleSize(titlesize);    hist.GetZaxis().SetTitleFont(42);

    hist.SetDirectory(0)
    return hist

def canvStyle(Canv,grids=False):
    Canv.Range(0,0,1,1);Canv.SetFillColor(0);Canv.SetBorderMode(0);Canv.SetBorderSize(2);Canv.SetTickx(1);Canv.SetTicky(1);
    Canv.SetLeftMargin(0.15);Canv.SetRightMargin(0.15)
    Canv.SetBottomMargin(0.13);   Canv.SetFrameFillStyle(0);   Canv.SetFrameBorderMode(0); ROOT.SetOwnership(Canv,False);
    if (grids): Canv.SetGridx(); Canv.SetGridy();
    return Canv

def legendStyle(legend,textSize,dummyEntry,ncol):
    if(ncol > 0):        legend.SetNColumns(ncol);
    legend.SetFillColor(0);legend.SetFillStyle(0);legend.SetShadowColor(0);legend.SetLineColor(0);legend.SetTextFont(42);legend.SetBorderSize(0);legend.SetTextSize(textSize);
    for entry in dummyEntry:
        if entry.strip():      
            legend.AddEntry('NULL',entry,'');
        else: 
            continue

    return legend

def getGraph(n,x,y,color,mstyle=ROOT.kFullCircle,msize=1.0):
    graph = ROOT.TGraph(n, array('d',x), array('d',y))
    graph.SetMarkerStyle(mstyle); graph.SetMarkerColor(color); graph.SetMarkerSize(msize)
    graph.SetLineColor(color); graph.SetLineWidth(2)
    print n,x,y
    return graph


def getAsym(hist,color):
    hist.Scale(1.0/hist.Integral())
    yvals=[];xvals=[]
    for i in range(1,hist.GetNbinsX()+1):
        asym_bbb=[];
        for j in range(1,hist.GetNbinsY()+1):
            #print hist.GetYaxis().GetBinLowEdge(j),hist.GetYaxis().GetBinUpEdge(j)
            sign=hist.GetYaxis().GetBinCenter(j)/abs(hist.GetYaxis().GetBinCenter(j))
            asym_bbb.append(hist.GetBinContent(i,j)*sign)
        #print abs(sum(asym_bbb))
        yvals.append(abs(sum(asym_bbb)));
        xvals.append(hist.GetXaxis().GetBinCenter(i))
    gr=getGraph(len(xvals),xvals,yvals,color)
    return gr

def getAsym_v1(hist,color):
    yvals=[];xvals=[];tot_pos = 0.;tot_neg  = 0.
    for x in range(1,hist.GetNbinsX()+1):
        pos = hist.Integral(x,x,6,10)
        neg = hist.Integral(x,x,1, 5)
        asym = (neg - pos) / (pos + neg)
        tot_pos += pos
        tot_neg += neg
        yvals.append(asym)
        xvals.append(hist.GetXaxis().GetBinCenter(x))
    tot_asym=(tot_neg-tot_pos)/(tot_neg+tot_pos)
    gr=getGraph(len(xvals),xvals,yvals,color)
    return gr,tot_asym

procs=['DPSWW','DPSWW_newsim','DPSWW_hw']
leps=['','_genlep','_dressedlep']
fIn= ROOT.TFile.Open("/eos/user/a/anmehta/www/DPSWW_v2/fullRun2/2021-12-10_2lss_asym_fid_v1//etaprod_absetamin_genlep_ll_noee_AND_etaprod_absetamin_dressedlep_ll_noee_AND_etaprod_absetamin_ll_noee.root")
#/eos/user/a/anmehta/www/DPSWW_v2/fullRun2/2021-12-10_2lss_asym/etaprod_absetamin_genlep_ll_noee_AND_etaprod_absetamin_dressedlep_ll_noee_AND_etaprod_absetamin_ll_noee.root") 
#/eos/user/a/anmehta/www/DPSWW_v2/fullRun2/2021-12-10_2lss_asym_reco_n_fid/etaprod_absetamin_genlep_ll_noee_AND_etaprod_absetamin_dressedlep_ll_noee_AND_etaprod_absetamin_ll_noee.root")
#/eos/user/a/anmehta/www/DPSWW_v2/fullRun2/2021-12-10_2lss_asym_fid
graphs=[];

for lep in leps:
    canv=ROOT.TCanvas("canv%s"%lep,"",800,600);canv=canvStyle(canv)
    dummy=fIn.Get("etaprod_absetamin_ll_noee_signal");
    xaxis=dummy.GetXaxis();nbinsX=dummy.GetNbinsX();
    xbinlow=xaxis.GetBinLowEdge(1);xbinhigh=xaxis.GetBinLowEdge(nbinsX+1);    
    mg = ROOT.TMultiGraph("mg%s"%lep,""); 
    hist = ROOT.TH2F("hist%s"%lep,"",nbinsX,xbinlow,xbinhigh,36,-0.002,0.16)
    hist =histStyle(hist,'|#eta_{min.}|','#alpha_{#etal}',1.07,1.5,0.045,0.035);
    hist.SetStats(0);hist.GetXaxis().SetTitleOffset(0.94);
    leg = ROOT.TLegend(0.185,0.7,0.9,0.865);
    leg=legendStyle(leg,0.03,[],1)
    for proc in procs:
        htmp=fIn.Get("etaprod_absetamin%s_ll_noee_%s"%(lep,proc));
        print "etaprod_absetamin%s_ll_noee_%s"%(lep,proc),htmp.Integral()
        gr_hw,val=getAsym_v1(htmp,SAFE_COLOR_LIST[procs.index(proc)])
        graphs.append(gr_hw)
        mg.Add(gr_hw);
        leg.AddEntry(gr_hw,proc+': {a:.3f}'.format(a=val),'p')
    hist.Draw(); mg.Draw('P'); leg.Draw('same');
    canv.Print("/eos/user/a/anmehta/www/DPSWW_v2/asym/asym_fidcuts_v1%s"%lep  + '.pdf')
    canv.Print("/eos/user/a/anmehta/www/DPSWW_v2/asym/asym_fidcuts_v1%s"%lep  + '.png')
fIn.Close();

