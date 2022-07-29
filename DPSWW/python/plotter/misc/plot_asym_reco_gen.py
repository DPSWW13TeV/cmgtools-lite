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
    Canv.SetLeftMargin(0.1);Canv.SetRightMargin(0.05);Canv.SetTopMargin(0.05);
    Canv.SetBottomMargin(0.1);   Canv.SetFrameFillStyle(0);   Canv.SetFrameBorderMode(0); ROOT.SetOwnership(Canv,False);
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

def getGraph(n,x,y,color,mstyle,msize=1.5):
    graph = ROOT.TGraph(n, array('d',x), array('d',y))
    graph.SetMarkerStyle(mstyle); graph.SetMarkerColor(color); graph.SetMarkerSize(msize)
    graph.SetLineColor(color); graph.SetLineWidth(2)
    #print n,x,y
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

def getAsym_v1(hist,color,mstyle=ROOT.kFullCircle):
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
    gr=getGraph(len(xvals),xvals,yvals,color,mstyle)
    return gr,tot_asym

#leps=['','_genlep','_dressedlep']
regions={'SR':['',''],'SR+FR':['','_SRFR'],'bare_FR':['_genlep','_genlep'],'drsd_FR':['_dressedlep','_dressedlep']}
eosDir="/eos/user/a/anmehta/www/DPSWW_v2/fullRun2/2021-12-29_2lss_asym/"
graphs=[];
canv=ROOT.TCanvas("canv","",800,600);canv=canvStyle(canv);canv.cd()
dummy = ROOT.TH2F("dummy","",5,0,2.5,42,-0.002,0.12)
dummy =histStyle(dummy,'#left|#eta_{min.}#right|','#alpha_{#etal}',0.92,1.1,0.045,0.035);

mg = ROOT.TMultiGraph("mg",""); 
leg = ROOT.TLegend(0.125,0.725,0.875,0.895);
leg=legendStyle(leg,0.03,[],3)
for iR,iS in regions.iteritems():
    procs={'DPSWW':'py','DPSWW_newsim':'dSh','DPSWW_hw':'hw'} if 'SR' in iR else {'DPSWW_gen':'py','DPSWW_gen_newsim':'dSh','DPSWW_gen_hw':'hw'}
    fIn= ROOT.TFile.Open(eosDir+"etaprod_absetamin{here}_ll_noee.root".format(here=iS[1]))
    #print eosDir+"etaprod_absetamin{here}_ll_noee.root".format(here=iS[1])
    for proc,pN in procs.iteritems():
        htmp=fIn.Get("etaprod_absetamin{ltype}_ll_noee_{sample}".format(ltype=iS[0],sample=proc))
        gr_hw,val=getAsym_v1(htmp,SAFE_COLOR_LIST[procs.keys().index(proc)],24+regions.keys().index(iR))
        graphs.append(gr_hw)
        mg.Add(gr_hw);
        sample=proc.split
        leg.AddEntry(gr_hw,pN+'-'+iR+' [{a:.2f}]'.format(a=val),'p')
    fIn.Close();
dummy.Draw(); mg.Draw('P'); leg.Draw('same');
canv.Print("/eos/user/a/anmehta/www/DPSWW_v2/asym.pdf")
canv.Print("/eos/user/a/anmehta/www/DPSWW_v2/asym.png")



#FR+SR region root file needs to be renamed etaprod_absetamin_SRFR_ll_noee.root
