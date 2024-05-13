#import ROOT
#from array import array
#from optparse import OptionParser
#from ConfigParser import SafeConfigParser
#import math as math
#import random
#import os
##import datetime
##date = "2024-05-03" #datetime.date.today().isoformat()
#import CMS_lumi, tdrstyle
#ROOT.gSystem.Load("PDFs/PdfDiagonalizer_cc.so")
#ROOT.gSystem.Load("PDFs/Util_cxx.so")
#ROOT.gStyle.SetOptStat(0)
#ROOT.gStyle.SetOptTitle(0)
#ROOT.gROOT.SetBatch(True)
#ROOT.gStyle.SetTextFont(42)

from prepare_bkg_oneCat_AM import *
vetoPlots=['cwww_WW_lin','cwww_WZ_lin','cb_WZ_lin','cb_WZ_quad']



from ROOT import TGaxis, TPaveText, TLatex, TString, TFile,TLine, TLegend, TCanvas,  TMath, TText, TPad, RooFit, RooArgSet, RooArgList,  RooAddition, RooProduct, RooConstraintSum, RooCustomizer, RooMinuit,  RooAbsData, RooAbsPdf, RooAbsReal, RooAddPdf, RooWorkspace, RooExtendPdf,RooGaussian, RooDataSet, RooExponential, RooRealVar,RooFormulaVar, RooDataHist, RooHist,RooCategory, RooSimultaneous, RooGenericPdf, RooProdPdf, kTRUE, kFALSE, kGray, kRed, kDashed, kGreen,kAzure, kOrange, kBlack,kBlue,kYellow,kCyan, kMagenta, kWhite,kDot,kDashDotted,kDotted, RooErfExpPdf, RooErfPowExpPdf, RooErfPowPdf, RooErfPow2Pdf, RooExpNPdf, RooAlpha4ExpNPdf, RooExpTailPdf, RooAlpha4ExpTailPdf, Roo2ExpPdf,RooWorkspace,TH1F

ROOT.RooMsgService.instance().setGlobalKillBelow(RooFit.FATAL)

parser        = OptionParser()

parser.add_option('-p', '--plots', action='store_false', dest='Make_plots', default=True, help='make plots')
parser.add_option('-v', action='store_true', dest='verbose', default=False, help='print model outputs etc.')
parser.add_option('-c', '--ch', dest='chan', default='elmu', help='channel, el, mu or elmu')
parser.add_option('-y', '--yr', dest='year', default='2018', help='year to run on, 2016, 2016APV, 2017 or 2018')
parser.add_option('--pf', dest='pf', default='', help='pf to be used with (root) inputs and (root) outputs ')
parser.add_option('--printatgc', action='store_true', default=False, help='print atgc-interference contribution')
parser.add_option('--uS', action='store_true', dest='useSkim', default=False, help='use skimmed trees or friends')
parser.add_option('--hi', action='store', dest='mlvj_hi', type='float', default=4550, help='dont change atm!')
parser.add_option('--lo', action='store', dest='mlvj_lo', type='float', default=950, help='set lower cut on MWV, mat cause problems')
parser.add_option('--inPath', action="store",type="string",dest="inPath",default="/eos/cms/store/cmst3/group/dpsww//NanoTrees_v9_vvsemilep_06012023/")
(options,args) = parser.parse_args()



usepNM=False
useWts=True

def mkplotDir(dname):
    if not os.path.isdir(dname): os.system("mkdir %s"%eos)
    if "www" in dname:
        os.system("cp /afs/cern.ch/user/a/anmehta/public/index.php "+dname)    
    return True

def if3(cond, iftrue, iffalse):
    return iftrue if cond else iffalse

def drawSLatex(xpos,ypos,text,size):
    latex = ROOT.TLatex()
    latex.SetNDC()
    latex.SetTextAlign(12)
    latex.SetTextSize(size)
    latex.SetTextFont(42)
    latex.DrawLatex(xpos,ypos,text)
    return latex


WW_aTGC=[]
WZ_aTGC=[]
basepath="/eos/cms/store/cmst3/group/dpsww//NanoTrees_v9_vvsemilep_06012023/"
final_cardsdir_name="%s/src/CMGTools/VVsemilep/python/plotter/Cards/" %(os.environ['CMSSW_BASE']); #for future perhaps add year as sub dir 
if not os.path.isdir(final_cardsdir_name):  os.system("mkdir -p %s"%final_cardsdir_name)

class Prepare_workspace_4limit:

        def __init__(self,year,ch): #,mlvj_lo,mlvj_hi,pf=""):
            
            self.POI                    = ['cwww','cw','cb']
            self.PAR_TITLES             = {'cwww' : '#frac{c_{WWW}}{#Lambda^{2}}', 'cw' : '#frac{c_{W}}{#Lambda^{2}}', 'cb' : '#frac{c_{B}}{#Lambda^{2}}'}#latex titles 
            self.PAR_MAX                = {'cwww' : 3.6, 'cw' : 4.5, 'cb' : 20}#atgc points
            self.ch                     = ch
            self.mlvj_lo                = options.mlvj_lo                #lower bound on invariant mass
            self.mlvj_hi                = options.mlvj_hi                #upper bound
            self.year                   = options.year
            self.pf                     = "_"+options.pf if len(options.pf) >0 else ""
            self.pf+="_withSkim" if options.useSkim else ""
            self.channel                = self.ch
            self.nbins                  = (self.mlvj_hi-self.mlvj_lo)/100
            self.file_Directory         = os.path.join(self.year,trees_b)
            self.file1_Directory        = os.path.join(self.year,trees_r)

            self.WS                     = RooWorkspace("w","w_%s_%s"%(self.ch,self.year))        #final workspace
            self.wtmp                   = RooWorkspace('wtmp',"wtmp_%s_%s"%(self.ch,self.year))
            
            self.fitresults             = []
            ##nuisance parameter to change all slope parameters by certain percentage (bigger for cb in WZ-cateogry)
            self.eps                    = RooRealVar('slope_nuis','slope_nuis',2,0,4)
            self.eps.setConstant(kTRUE)
            self.eps4cbWZ               = RooFormulaVar('rel_slope_nuis4cbWZ','rel_slope_nuis4cbWZ','1+3.0*(@0-1)',RooArgList(self.eps))
            self.eps4cbWW               = RooFormulaVar('rel_slope_nuis4cbWW','rel_slope_nuis4cbWW','1+3.0*(@0-1)',RooArgList(self.eps))
            self.PNSWP={'WPL':0.64,'WPM':0.85,'WPT':0.91,'WPU':0.5,'WPD':-1}
            self.wtagger_label        = 'WPM' 
            self.PNS = self.PNSWP[self.wtagger_label]
            eos='/eos/user/a/anmehta/www/VVsemilep/WJest/%s/%s_%s'%(self.year,'pNM' if usepNM else 'sDM',date)
            if not os.path.isdir(eos): os.system("mkdir %s"%eos)
            if os.path.exists("/afs/cern.ch"): os.system("cp /afs/cern.ch/user/a/anmehta/public/index.php "+eos)
            extra_str="%s%s"%("weighted" if useWts else "unweighted",self.pf)
            self.plotsDir = eos+'/plots_aTGC_%s_%s_%s_%s_%s' %(self.channel,self.wtagger_label,self.mlvj_lo,int(self.mlvj_hi),extra_str)
            if not os.path.isdir(self.plotsDir): os.system("mkdir %s"%self.plotsDir)
            os.system("cp /afs/cern.ch/user/a/anmehta/public/index.php "+self.plotsDir)
            os.system("cp make_PDF_input_oneCat_AM.py "+self.plotsDir)
            self.rlt_DIR_name="Cards/%s/cards_%s_%s_%s_%s_%s_%s/"%(date,'pNM' if usepNM else 'sDM',extra_str,self.channel,self.wtagger_label,options.mlvj_lo,int(options.mlvj_hi))##date

            ##read workspace containing background pdfs
            fileInWs                    = TFile.Open(self.rlt_DIR_name+'/wwlvj_%s_%s_%s_%s_workspace.root'%(self.ch,self.wtagger_label,950,int(self.mlvj_hi)))
            w                           = fileInWs.Get('workspace4limit_')
            self.rrv_mass_lvj           = w.var('rrv_mass_lvj')
            self.rrv_mass_lvj.SetTitle('m_{WV}')
            self.rrv_mass_lvj.setRange(self.mlvj_lo,self.mlvj_hi)
            self.rrv_mass_j             = w.var('rrv_mass_j')

            #names of bkg contributions and regions
            self.bkgs        = ['WJets','TTbar','WW','WZ','STop']
            self.regions     = ['sig','sb_lo','sb_hi']
            self.samples={
                    'WW':[ww_atgc],
                    'WZ':[wz_atgc]}#stop 24011170135.9
            self.file_WW_aTGC_mc              = "WW_aTGC"
            self.file_WZ_aTGC_mc              = "WZ_aTGC"

        #read trees containing aTGC WW and WZ events and fill them into histograms
        def Read_ATGCtree(self,ch='mu'):
            print ('######### Making histograms for aTGC working points #########')
            hists4scale        = {}
            for WV in ['WW','WZ']:
                #create 3 histograms for each aTGC parameter (positive, negative and positive-negative working point)
                for para in self.POI:
                    hists4scale['c_pos_%s_hist_%s'%(WV,para)] = TH1F('c_pos_%s_hist_%s'%(WV,para),'c_pos_%s_hist_%s'%(WV,para),self.nbins,self.mlvj_lo,self.mlvj_hi);
                    hists4scale['c_neg_%s_hist_%s'%(WV,para)] = TH1F('c_neg_%s_hist_%s'%(WV,para),'c_neg_%s_hist_%s'%(WV,para),self.nbins,self.mlvj_lo,self.mlvj_hi);
                    hists4scale['c_sm_lin_quad_%s_hist_%s'%(WV,para)] = TH1F('c_sm_lin_quad_%s_hist_%s'%(WV,para),'c_sm_lin_quad_%s_hist_%s'%(WV,para),self.nbins,self.mlvj_lo,self.mlvj_hi);
                    hists4scale['c_pos_%s_hist_%s'%(WV,para)].Sumw2(kTRUE)
                    hists4scale['c_neg_%s_hist_%s'%(WV,para)].Sumw2(kTRUE)
                    hists4scale['c_sm_lin_quad_%s_hist_%s'%(WV,para)].Sumw2(kTRUE)
                    hists4scale['c_quad_%s_hist_%s'%(WV,para)]=TH1F('c_quad_%s_hist_%s'%(WV,para),'c_quad_%s_hist_%s'%(WV,para),self.nbins,self.mlvj_lo,self.mlvj_hi); hists4scale['c_quad_%s_hist_%s'%(WV,para)].Sumw2(kTRUE)

                #add histograms for SM and all aTGC parameters unequal to zero
                hists4scale['c_sm_%s_hist'%WV]                  = TH1F('c_sm_%s_hist'%WV,'c_sm_%s_hist'%WV,self.nbins,self.mlvj_lo,self.mlvj_hi);                
                hists4scale['c_%s_histall3'%WV]                 = TH1F('c_%s_histall3'%WV,'c_%s_histall3'%WV,self.nbins,self.mlvj_lo,self.mlvj_hi);
                hists4scale['c_sm_%s_hist'%WV].Sumw2(kTRUE)
                hists4scale['c_%s_histall3'%WV].Sumw2(kTRUE)

		# Add histograms for two aTGC parameters positive
		hists4scale['c_cwww_cw_%s_hist'%WV]=TH1F('c_cwww_cw_%s_hist'%WV,'c_cwww_cw_%s_hist'%WV,self.nbins,self.mlvj_lo,self.mlvj_hi);
		hists4scale['c_cw_cb_%s_hist'%WV]=TH1F('c_cw_cb_%s_hist'%WV,'c_cw_cb_%s_hist'%WV,self.nbins,self.mlvj_lo,self.mlvj_hi);
		hists4scale['c_cwww_cw_%s_hist'%WV].Sumw2(kTRUE)
		hists4scale['c_cw_cb_%s_hist'%WV].Sumw2(kTRUE)

		# Add histograms for aTGC-aTGC interference terms
		hists4scale['c_int_cwww_cw_%s_hist'%WV]=TH1F('c_int_cwww_cw_%s_hist'%WV,'c_int_cwww_cw_%s_hist'%WV,self.nbins,self.mlvj_lo,self.mlvj_hi);
		hists4scale['c_int_cw_cb_%s_hist'%WV]=TH1F('c_int_cw_cb_%s_hist'%WV,'c_int_cw_cb_%s_hist'%WV,self.nbins,self.mlvj_lo,self.mlvj_hi);
		hists4scale['c_int_cwww_cw_%s_hist'%WV].Sumw2(kTRUE)
		hists4scale['c_int_cw_cb_%s_hist'%WV].Sumw2(kTRUE)



                #print 'reading for %s sample in  %s channel'%(WV,self.ch)
                treeIn  = ROOT.TChain('Friends')
                treeIn1 = ROOT.TChain('Friends')                
                for i in self.samples[WV][0]:
                    fileIn_name = str(options.inPath+"/"+self.file_Directory+"/"+i+"_Friend.root");
                    treeIn.Add(fileIn_name)
                    fileIn1_name = str(options.inPath+"/"+self.file1_Directory+"/"+i+"_Friend.root");
                    treeIn1.Add(fileIn1_name)
                treeIn.AddFriend(treeIn1)
                lumi_tmp         = lumis[self.year]
                for i in range(treeIn.GetEntries()):
                    if i%50000==0:                            print (str(i) + '/' + str(treeIn.GetEntries()))
                    treeIn.GetEntry(i)
                    MWW                = treeIn.mWV
                    #apply cuts
                    #using whole mj-range (sideband and signal region)
                    #tmp_jet_mass=treeIn.Selak8Jet1_particleNet_mass if usepNM else treeIn.Selak8Jet1_msoftdrop
                    #tmp_jet_pNetscore=treeIn.Selak8Jet1_pNetWtagscore

                    tmp_jet_mass=treeIn.Selak8Jet1_particleNet_mass if usepNM else treeIn.Selak8Jet1_msoftdrop
                    tmp_jet_pNetscore=treeIn.Selak8Jet1_pNetWtagscore
                    dRfjlep=treeIn.dR_fjlep > 1.6 
                    dphifjlep=treeIn.dphi_fjlep > 2.0 
                    dphifjmet=treeIn.dphi_fjmet > 2.0 
                    ptWlep=treeIn.pTWlep > 200
                    boosted_sel=dRfjlep and dphifjlep and dphifjmet and ptWlep and tmp_jet_pNetscore > self.PNS and tmp_jet_mass < 150 and tmp_jet_mass > 45 and  MWW>self.mlvj_lo
                    lep_flav= (abs(treeIn.Lep1_pdgId) == 13 and treeIn.trigger1m) if self.ch == "mu" else (abs(treeIn.Lep1_pdgId) == 11 and treeIn.trigger1e )
                    if lep_flav and  boosted_sel and lep_sel:
                        #                    if (abs(treeIn.Lep1_pdgId) == 13 and treeIn.trigger1m if self.channel == "mu" else  abs(treeIn.Lep1_pdgId) == 11 and treeIn.trigger1e )  and treeIn.Lep1_pt > 50  and  boosted_sel and treeIn.pmet > 110 and treeIn.nBJetMedium30 == 0:
			#weight_part =1000*treeIn.xsec*treeIn.genwt*treeIn.evt_wt*treeIn.lepSF*treeIn.Selak8Jet1_pNetWtagSF*lumis[self.year]/treeIn.sumw 
			weight_part =1000*treeIn.xsec*treeIn.genwt*treeIn.evt_wt*treeIn.lepSF*treeIn.Selak8Jet1_pNetWtagSF*lumis[self.year]/treeIn.sumw 
			aTGC        = treeIn.aGC_wt 
			#all3hists4scale['c_%s_histall3'%WV].Fill(MWW,aTGC[123] * weight_part)
			hists4scale['c_%s_histall3'%WV].Fill(MWW,aTGC[124]*weight_part) #all ops set to non zero, same as starting point on the grid
			#SM
			hists4scale['c_sm_%s_hist'%WV].Fill(MWW,aTGC[62] * weight_part) #SM point
			#cwww 
			hists4scale['c_pos_%s_hist_cwww'%WV].Fill(MWW,aTGC[12] * weight_part) #cwww3p6
			hists4scale['c_neg_%s_hist_cwww'%WV].Fill(MWW,aTGC[112] * weight_part) #cwww-3p6
			#cw
			hists4scale['c_pos_%s_hist_cw'%WV].Fill(MWW,aTGC[72] * weight_part) #cw4p50
			hists4scale['c_neg_%s_hist_cw'%WV].Fill(MWW,aTGC[52] * weight_part) #cw-4p50
			#cb
			hists4scale['c_pos_%s_hist_cb'%WV].Fill(MWW,aTGC[64] * weight_part) #cb20
			hists4scale['c_neg_%s_hist_cb'%WV].Fill(MWW,aTGC[60] * weight_part) #cbm20
			#cw-SM interference
			hists4scale['c_sm_lin_quad_%s_hist_cw'%WV].Fill(MWW,0.5*(aTGC[72]-aTGC[52]) * weight_part)
			#cb-SM interference
			hists4scale['c_sm_lin_quad_%s_hist_cb'%WV].Fill(MWW,0.5*(aTGC[64]-aTGC[60]) * weight_part)
			#cwww-SM interference
			hists4scale['c_sm_lin_quad_%s_hist_cwww'%WV].Fill(MWW,0.5*(aTGC[112]-aTGC[12]) * weight_part)
			#cwww+cw
			hists4scale['c_cwww_cw_%s_hist'%WV].Fill(MWW,aTGC[122] * weight_part)
			#cw+cb
			hists4scale['c_cw_cb_%s_hist'%WV].Fill(MWW,aTGC[74] * weight_part)
			#cwww-cw interference
			hists4scale['c_int_cwww_cw_%s_hist'%WV].Fill(MWW, ((aTGC[122]-aTGC[23])-(aTGC[12]-aTGC[112])) * weight_part)
			#cw-cb interference
			hists4scale['c_int_cw_cb_%s_hist'%WV].Fill(MWW, ((aTGC[74]-aTGC[54])-(aTGC[72]-aTGC[52])) * weight_part)
                        hists4scale['c_quad_%s_hist_cb'%WV].Fill(MWW,0.5*(aTGC[64]+aTGC[60]-2*aTGC[62]) * weight_part)
                        hists4scale['c_quad_%s_hist_cw'%WV].Fill(MWW,0.5*(aTGC[72]+aTGC[52]-2*aTGC[62]) * weight_part)
                        hists4scale['c_quad_%s_hist_cwww'%WV].Fill(MWW,0.5*(aTGC[112]+aTGC[12]-2*aTGC[62]) * weight_part)



		# Fit exponential to the aTGC-aTGC interference histograms (This is to avoid doing this via gen-level files)
		hists4scale['c_int_cwww_cw_%s_hist'%WV].Fit("expo")
		a5_val=hists4scale['c_int_cwww_cw_%s_hist'%WV].GetFunction("expo").GetParameter(1)
		hists4scale['c_int_cw_cb_%s_hist'%WV].Fit("expo")
		a7_val=hists4scale['c_int_cw_cb_%s_hist'%WV].GetFunction("expo").GetParameter(1)
		
		# Write the slopes to workspace
		a5=RooRealVar('a5_%s'%WV,'a5_%s'%WV,-0.0001,-0.01,0.01)
		a7=RooRealVar('a7_%s'%WV,'a7_%s'%WV,-0.001,-0.01,0.01)
		a5.setVal(a5_val)
		a7.setVal(a7_val)
		a5.setConstant(ROOT.kTRUE)
		a7.setConstant(ROOT.kTRUE)
		self.Import_to_ws(self.wtmp, [a5,a7])
		
		# Write normalizations to workspace
		# Not used now (histograms are retrieved later, RooDataHists are created and sumEntries is used on them); although can be done via this too, the results are identical
		N3645=RooRealVar('N_cwww_cw_36_45_%s'%WV,'N_cwww_cw_36_45_%s'%WV,hists4scale['c_cwww_cw_%s_hist'%WV].Integral())
		N4520=RooRealVar('N_cw_cb_45_20_%s'%WV,'N_cw_cb_45_20_%s'%WV,hists4scale['c_cw_cb_%s_hist'%WV].Integral())
		N36  =RooRealVar('N_cwww_36_%s'%WV,'N_cwww_36_%s'%WV,hists4scale['c_pos_%s_hist_cwww'%WV].Integral())
		N36_ =RooRealVar('N_cwww__36_%s'%WV,'N_cwww__36_%s'%WV,hists4scale['c_neg_%s_hist_cwww'%WV].Integral())
		N45  =RooRealVar('N_cw_45_%s'%WV,'N_cw_45_%s'%WV,hists4scale['c_pos_%s_hist_cw'%WV].Integral())
                N45_ =RooRealVar('N_cw__45_%s'%WV,'N_cw__45_%s'%WV,hists4scale['c_neg_%s_hist_cw'%WV].Integral())
		N20  =RooRealVar('N_cb_20_%s'%WV,'N_cb_20_%s'%WV,hists4scale['c_pos_%s_hist_cb'%WV].Integral())
                N20_ =RooRealVar('N_cb__20_%s'%WV,'N_cb__20_%s'%WV,hists4scale['c_neg_%s_hist_cb'%WV].Integral())
                N_sm_lin_quad_cb    = RooRealVar('N_sm_lin_quad_cb_%s'%WV,'N_sm_lin_quad_cb_%s'%WV,hists4scale['c_sm_lin_quad_%s_hist_cb'%WV].Integral())
                N_sm_lin_quad_cwww  = RooRealVar('N_sm_lin_quad_cwww_%s'%WV,'N_sm_lin_quad_cwww_%s'%WV,hists4scale['c_sm_lin_quad_%s_hist_cwww'%WV].Integral())
                N_sm_lin_quad_cw    = RooRealVar('N_sm_lin_quad_cw_%s'%WV,'N_sm_lin_quad_cw_%s'%WV,hists4scale['c_sm_lin_quad_%s_hist_cw'%WV].Integral())
                N_quad_cb           = RooRealVar('N_quad_cb_%s'%WV,'N_quad_cb_%s'%WV,hists4scale['c_quad_%s_hist_cb'%WV].Integral())
                N_quad_cwww         = RooRealVar('N_quad_cwww_%s'%WV,'N_quad_cwww_%s'%WV,hists4scale['c_quad_%s_hist_cwww'%WV].Integral())
                N_quad_cw           = RooRealVar('N_quad_cw_%s'%WV,'N_quad_cw_%s'%WV,hists4scale['c_quad_%s_hist_cw'%WV].Integral())

		self.Import_to_ws(self.wtmp, [N3645,N4520,N36,N36_,N45,N45_,N20,N20_,N_sm_lin_quad_cb,N_sm_lin_quad_cwww,N_sm_lin_quad_cw,N_quad_cb,N_quad_cwww,N_quad_cw])

            #write histograms to file
            fileOut        = TFile.Open(self.rlt_DIR_name+'/hists4scale_%s_WV_aTGC-%s_%s.root'%(self.ch,self.mlvj_lo,self.mlvj_hi),'recreate')
            for key in hists4scale:
                hists4scale[key].Write()
            print ('--------> Written to file ' + fileOut.GetName())
            fileOut.Close()

        def Make_plots(self,rrv_x,cat,fitres):
            can     = [];can2    = [];      plots   = [];     plots2  = []; pads    = [];
            channel = self.ch+'_'+cat
            for i in range(3):
                rrv_x.setRange(self.mlvj_lo,self.mlvj_hi)
                p       = rrv_x.frame(self.mlvj_lo,self.mlvj_hi)
                p2      = rrv_x.frame(self.mlvj_lo,self.mlvj_hi)
                c       = TCanvas(cat+'_'+self.POI[i]+'-',self.POI[i]+'-',600,600)
                c.cd()
                CMS_lumi.lumi_13TeV = "%s fb^{-1}" %str(lumis[self.year])
                CMS_lumi.writeExtraText = True;                       CMS_lumi.extraText = "Preliminary"
                H_ref = 600;        W_ref = 600;        W = W_ref;       H  = H_ref
                T = 0.12*H_ref;       B = 0.12*H_ref;       L = 0.12*W_ref;       R = 0.01*W_ref
                
                pad1        = TPad(cat+'pad1_%s'%self.POI[i],cat+'pad1_%s'%self.POI[i],0.,0.3,1.,1.)  
                pad2        = TPad(cat+'pad2_%s'%self.POI[i],cat+'pad2_%s'%self.POI[i],0.,0.02,1.,0.3)
                c2          = TCanvas(cat+self.POI[i]+'+',self.POI[i]+'+',600,600)
                c2.cd()
                pad3        = TPad(cat+'pad3_%s'%self.POI[i],cat+'pad3_%s'%self.POI[i],0.,0.3,1.,1.)
                pad4        = TPad(cat+'pad4_%s'%self.POI[i],cat+'pad4_%s'%self.POI[i],0.,0.02,1.,0.3)
                p2pads      = [pad1,pad2,pad3,pad4]
                can.append(c); can2.append(c2);  plots.append(p);        plots2.append(p2);                pads.append(p2pads)

            for i in range(3):
                can[i].cd();
                #CMS_lumi.CMS_lumi(pads[i][0], 4, 11,0.075);
                pads[i][0].Update()
                pads[i][0].Draw();                pads[i][1].Draw()
                pads[i][0].SetLeftMargin(0.1);    pads[i][1].SetLeftMargin(0.1)
                norm = self.wtmp.function('normfactor_3d_%s'%channel)

                for j in range(3):
                    self.wtmp.var(self.POI[j]).setVal(0)
                self.wtmp.data('SMdatahist_%s'%cat).plotOn(plots[i],RooFit.MarkerColor(kBlack),RooFit.LineColor(kBlack),RooFit.LineStyle(kDashed),RooFit.DataError(RooAbsData.SumW2),RooFit.DrawOption('E0'),RooFit.Name('SMdata'))
                normvalSM        = norm.getVal() * self.wtmp.data('SMdatahist_%s'%cat).sumEntries()
                self.wtmp.pdf('aTGC_model_%s'%channel).plotOn(plots[i],RooFit.LineColor(kBlack),RooFit.Normalization(normvalSM, RooAbsReal.NumEvent),RooFit.Name('SMmodel'))
                #self.wtmp.data('neg_datahist_%s_%s'%(cat,self.POI[i])).plotOn(plots[i],RooFit.MarkerColor(kBlue),RooFit.LineColor(kBlue),RooFit.DataError(RooAbsData.SumW2),RooFit.DrawOption('E0'),RooFit.Name('atgcdata'))
                self.wtmp.var(self.POI[i]).setVal(-self.PAR_MAX[self.POI[i]])
                normvalneg = norm.getVal() * self.wtmp.data('SMdatahist_%s'%cat).sumEntries()
                #self.wtmp.pdf('aTGC_model_%s'%channel).plotOn(plots[i],RooFit.LineColor(kBlue),RooFit.Normalization(normvalneg, RooAbsReal.NumEvent),RooFit.Name('atgcmodel'))
                #                    print "this info we nned: category \t",cat,"\t poi\t",self.POI[i],"\t channel \t",channel,"\t ch\t",self.ch


                pullhist_q=None;pullhist_l=None
                
                linStr=self.POI[i]+'_'+cat+'_lin'
                quadStr=self.POI[i]+'_'+cat+'_quad'
                if linStr not in vetoPlots:
                    lin_Norm=self.wtmp.var('norm_sm_lin_quad_%s_%s'%(self.POI[i],channel))
                    print "linear term \t", self.POI[i],"\t", channel,"\t",lin_Norm.getVal(),"\t",self.wtmp.data('SMdatahist_%s'%cat).sumEntries()
                    self.wtmp.data('sm_lin_quad_datahist_%s_%s'%(cat,self.POI[i])).plotOn(plots[i],RooFit.MarkerColor(ROOT.kAzure+10),RooFit.MarkerSize(0.75),RooFit.LineColor(ROOT.kAzure+10),RooFit.DataError(RooAbsData.SumW2),RooFit.DrawOption('P0E1'),RooFit.Name('linData'))
                    self.wtmp.pdf('%s_sm_lin_quad_%s_%s'%(cat,self.POI[i],self.ch)).plotOn(plots[i],RooFit.LineColor(ROOT.kAzure+7),RooFit.LineStyle(kDotted),RooFit.Normalization(lin_Norm.getVal()*self.wtmp.data('SMdatahist_%s'%cat).sumEntries(), RooAbsReal.NumEvent),RooFit.Name('linModel'))
                    pullhist_l= plots[i].pullHist('linData','linModel')
                if quadStr not in vetoPlots:
                    quad_Norm=self.wtmp.var('norm_quad_%s_%s'%(self.POI[i],channel))
                    print "quad term \t", self.POI[i],"\t", channel,"\t",quad_Norm.getVal(),"\t",self.wtmp.data('SMdatahist_%s'%cat).sumEntries()
                    self.wtmp.pdf('%s_quad_%s_%s'%(cat,self.POI[i],self.ch)).plotOn(plots[i],RooFit.LineColor(ROOT.kPink-2),RooFit.LineStyle(kDashed),RooFit.Normalization(quad_Norm.getVal()*self.wtmp.data('SMdatahist_%s'%cat).sumEntries(), RooAbsReal.NumEvent),RooFit.Name('quadModel'))
                    self.wtmp.data('quad_datahist_%s_%s'%(cat,self.POI[i])).plotOn(plots[i],RooFit.MarkerColor(ROOT.kPink-7),RooFit.MarkerSize(0.75),RooFit.LineColor(ROOT.kPink-7),RooFit.DataError(RooAbsData.SumW2),RooFit.DrawOption('P0E1'),RooFit.Name('quadData'))

                    pullhist_q= plots[i].pullHist('quadData','quadModel')

                #pullhist = plots[i].pullHist('atgcdata','atgcmodel')

                plotmax        = 1e6; plotmin = 1e-3
                plots[i].GetYaxis().SetRangeUser(plotmin,plotmax)
                pads[i][0].cd();pads[i][0].SetBottomMargin(0.03);pads[i][0].SetTopMargin(0.1);
                pads[i][0].SetLogy()
                plots[i].SetTitle('')
                plots[i].GetYaxis().SetTitle('Events')
                plots[i].GetYaxis().SetTitleSize(0.04);plots[i].GetYaxis().SetLabelSize(0.035);
                plots[i].GetXaxis().SetLabelOffset(99999)
                txt = ROOT.TText(2, 100, "Signal")
                txt.SetTextSize(0.04)
                txt.SetTextColor(ROOT.kRed)
                #t2a = drawSLatex(0.1,0.90,"#bf{CMS} Preliminary",0.05);
                #t3a = drawSLatex(0.665,0.90,"%f fb^{#minus1} (13 TeV)"%(lumis[self.year]),0.05);
                #t2a.Draw();t3a.Draw();
                plots[i].addObject(txt)
                plots[i].Draw()
                ndof        = (self.mlvj_hi-self.mlvj_lo)/100 - 4
                plots[i].Print()
                
                parlatex        = ['#frac{c_{WWW}}{#Lambda^{2}}','#frac{c_{W}}{#Lambda^{2}}','#frac{c_{B}}{#Lambda^{2}}']
                leg        = TLegend(0.11,0.5,0.85,0.85)
                leg.SetFillStyle(0);leg.SetTextFont(42);                leg.SetBorderSize(0);leg.SetNColumns(2);
                leg.SetFillStyle(0); leg.SetTextSize(0.035);
                leg.AddEntry(plots[i].findObject('SMdata'),'SM (MC)','le')
                leg.AddEntry(plots[i].findObject('SMmodel'),'SM (exp)','l')
                #leg.AddEntry(plots[i].findObject('atgcdata'),'MC '+parlatex[i]+'='+str(-self.PAR_MAX[self.POI[i]])+' TeV^{-2}','le')
                #leg.AddEntry(plots[i].findObject('atgcmodel'),'signal model '+parlatex[i]+'='+str(-self.PAR_MAX[self.POI[i]])+' TeV^{-2}','l')
                if quadStr not in vetoPlots:  
                    leg.AddEntry(plots[i].findObject('quadData'),'quad. MC '+parlatex[i]+'='+str(-self.PAR_MAX[self.POI[i]])+' TeV^{-2}','le')
                    leg.AddEntry(plots[i].findObject('quadModel'),'quad. model '+parlatex[i]+'='+str(-self.PAR_MAX[self.POI[i]])+' TeV^{-2}','l')
                if linStr not in vetoPlots:
                    leg.AddEntry(plots[i].findObject('linData'),'lin. MC '+parlatex[i]+'='+str(-self.PAR_MAX[self.POI[i]])+' TeV^{-2}','le')
                    leg.AddEntry(plots[i].findObject('linModel'),'lin. model '+parlatex[i]+'='+str(-self.PAR_MAX[self.POI[i]])+' TeV^{-2}','l')


                leg.Draw()
                leg.Print()

                pads[i][1].cd();                pads[i][1].SetTopMargin(0.03);  pads[i][1].SetBottomMargin(0.3)##HERE
                ratio_style = ROOT.TH1D('ratio_style','ratio_style',(self.mlvj_hi-self.mlvj_lo)/100,self.mlvj_lo,self.mlvj_hi)
                ratio_style.SetMarkerStyle(21)
                ratio_style.SetLineColor(kBlack);ratio_style.SetLineWidth(1);
                ratio_style.SetMaximum(3)
                ratio_style.SetMinimum(-3)
                ratio_style.GetYaxis().SetNdivisions(7)
                ratio_style.GetYaxis().SetTitle('#frac{MC-Fit}{error}')
                ratio_style.GetYaxis().SetLabelSize(0.095)
                ratio_style.GetYaxis().SetTitleSize(0.1)
                ratio_style.GetYaxis().SetTitleOffset(0.425)
                #ratio_style.GetXaxis().SetLabelOffset(0.425)
                #ratio_style.GetYaxis().SetLabelOffset(0.425)
                ratio_style.GetXaxis().SetLabelSize(0.095)
                ratio_style.GetXaxis().SetTitleSize(0.1)
                ratio_style.GetXaxis().SetTitle("m_{WV} (GeV)");
                ratio_style.Draw("")
                #pullhist.SetLineColor(kBlue);pullhist.SetLineWidth(1);
                #pullhist.Draw("SAME E1")
                if (pullhist_q) is not None: 
                    pullhist_q.Draw("SAME P0E1");  
                    pullhist_q.SetLineColor(ROOT.kPink-2);pullhist_q.SetLineWidth(1);
                    pullhist_q.SetMarkerColor(ROOT.kPink-2);
                if (pullhist_l) is not None: 
                    pullhist_l.SetLineColor(ROOT.kAzure+10);pullhist_l.SetLineWidth(1);pullhist_l.SetMarkerColor(ROOT.kAzure+10);
                    pullhist_l.Draw("SAME P0E1")
                can[i].Update()
                can[i].SaveAs(self.plotsDir+'/%s_neg_%s.pdf'%(self.POI[i],channel))
                can[i].SaveAs(self.plotsDir+'/%s_neg_%s.png'%(self.POI[i],channel))
                

                for j in range(3):
                        self.wtmp.var(self.POI[j]).setVal(0)
                self.wtmp.data('SMdatahist_%s'%cat).plotOn(plots2[i],RooFit.MarkerColor(kBlack),RooFit.LineColor(kBlack),RooFit.DataError(RooAbsData.SumW2),RooFit.DrawOption('E0'))
                self.wtmp.data('pos_datahist_%s_%s'%(cat,self.POI[i])).plotOn(plots2[i],RooFit.MarkerColor(kBlue),RooFit.LineColor(kBlue),RooFit.DataError(RooAbsData.SumW2),RooFit.DrawOption('E0'))

                self.wtmp.pdf('aTGC_model_%s'%channel).plotOn(plots2[i],RooFit.LineColor(kBlack),RooFit.Normalization(normvalSM, RooAbsReal.NumEvent))
                self.wtmp.var(self.POI[i]).setVal(self.PAR_MAX[self.POI[i]])
                normvalpos = norm.getVal() * self.wtmp.data('SMdatahist_%s'%cat).sumEntries()

                self.wtmp.pdf('aTGC_model_%s'%channel).plotOn(plots2[i],RooFit.LineColor(kBlue),RooFit.Normalization(normvalpos, RooAbsReal.NumEvent))
                
                self.wtmp.data('pos_datahist_%s_%s'%(cat,self.POI[i])).plotOn(plots2[i],RooFit.MarkerColor(kBlue),RooFit.LineColor(kBlue),RooFit.DataError(RooAbsData.SumW2),RooFit.DrawOption('E'))

                plots2[i].GetYaxis().SetRangeUser(plotmin,plotmax);
                plots2[i].GetYaxis().SetTitle('Events')
                plots2[i].GetXaxis().SetLabelOffset(99); plots2[i].GetXaxis().SetTitleOffset(999);plots2[i].GetXaxis().SetLabelSize(0.0001);plots2[i].GetXaxis().SetTitleSize(0.0001);
                can2[i].cd()
                pads[i][2].Draw()
                pads[i][3].Draw()
                pads[i][2].SetLeftMargin(0.1)
                pads[i][3].SetLeftMargin(0.1)
                plots2[i].SetTitle('')
                pads[i][2].SetLogy()
                pads[i][2].cd()
                plots2[i].Draw()
		leg2        = TLegend(0.11,0.2,0.4,0.6)
                leg2.SetFillStyle(0)
                leg2.SetBorderSize(0)
                leg2.AddEntry(plots[i].findObject('SMdata'),'MC '+parlatex[i]+'=0 TeV^{-2}','le')
                leg2.AddEntry(plots[i].findObject('SMmodel'),'signal model '+parlatex[i]+'=0 TeV^{-2}','l')
                leg2.AddEntry(plots[i].findObject('atgcdata'),'MC '+parlatex[i]+'='+str(+self.PAR_MAX[self.POI[i]])+' TeV^{-2}','le')
                leg2.AddEntry(plots[i].findObject('atgcmodel'),'signal model '+parlatex[i]+'='+str(+self.PAR_MAX[self.POI[i]])+' TeV^{-2}','l')
		leg2.Draw()
		leg2.Print()
                pullhist2 = plots2[i].pullHist('h_pos_datahist_%s_%s'%(cat,self.POI[i]),'aTGC_model_%s_Norm[rrv_mass_lvj]'%channel)
                pads[i][3].cd()
                pads[i][3].SetTopMargin(0.0005);pads[i][3].SetBottomMargin(0.3);
                ratio_style.Draw("")
                ratio_style.GetXaxis().SetTitle("m_{WV} (GeV)");
                pullhist2.SetLineColor(kBlue);  pullhist2.SetLineWidth(1);
                pullhist2.Draw("E1")

                can2[i].Update()
                can2[i].SaveAs(self.plotsDir+'/%s_pos_%s.pdf'%(self.POI[i],channel))
                can2[i].SaveAs(self.plotsDir+'/%s_pos_%s.png'%(self.POI[i],channel))
                    


            
        #function to import multiple items from a list into a workspace
        def Import_to_ws(self,workspace,items,recycle=0):
            for item in items:
                if recycle:
                    getattr(workspace,'import')(item,RooFit.RecycleConflictNodes())
                else:
                    getattr(workspace,'import')(item)

        def Make_signal_pdf(self,rrv_x,sample):
            channel        = self.ch+'_'+sample                #needed for variables that differ for WW and WZ
            cwww     = RooRealVar('cwww','cwww',0,-36,36);
            cw       = RooRealVar('cw','cw',0,-45,45);
            cb       = RooRealVar('cb','cb',0,-200,200);
            cwww.setConstant(kTRUE);
            cw.setConstant(kTRUE);
            cb.setConstant(kTRUE);
   
            #get SM and other histograms and make RooDataHists
            fileInHist      = TFile.Open(self.rlt_DIR_name+'/hists4scale_%s_WV_aTGC-%s_%s.root'%(self.ch,self.mlvj_lo,self.mlvj_hi))
            rrv_x.setRange(self.mlvj_lo,self.mlvj_hi)
            SMdatahist       = RooDataHist('SMdatahist_%s'     %sample,'SMdatahist_%s'     %sample,RooArgList(rrv_x),fileInHist.Get('c_sm_%s_hist'%sample))
	    cwwwPosDataHist  = RooDataHist('cwwwPosDataHist_%s'%sample,'cwwwPosDataHist_%s'%sample,RooArgList(rrv_x),fileInHist.Get('c_pos_%s_hist_cwww'%sample))
	    cwwwNegDataHist  = RooDataHist('cwwwNegDataHist_%s'%sample,'cwwwNegDataHist_%s'%sample,RooArgList(rrv_x),fileInHist.Get('c_neg_%s_hist_cwww'%sample))
	    cwPosDataHist    = RooDataHist('cwPosDataHist_%s'  %sample,'cwPosDataHist_%s'  %sample,RooArgList(rrv_x),fileInHist.Get('c_pos_%s_hist_cw'%sample))
	    cwNegDataHist    = RooDataHist('cwNegDataHist_%s'  %sample,'cwNegDataHist_%s'  %sample,RooArgList(rrv_x),fileInHist.Get('c_neg_%s_hist_cw'%sample))
	    cbPosDataHist    = RooDataHist('cbPosDataHist_%s'  %sample,'cbPosDataHist_%s'  %sample,RooArgList(rrv_x),fileInHist.Get('c_pos_%s_hist_cb'%sample))
	    cbNegDataHist    = RooDataHist('cbNegDataHist_%s'  %sample,'cbNegDataHist_%s'  %sample,RooArgList(rrv_x),fileInHist.Get('c_neg_%s_hist_cb'%sample))
	    cwwwcwDataHist   = RooDataHist('cwwwcwDataHist_%s' %sample,'cwwwcwDataHist_%s' %sample,RooArgList(rrv_x),fileInHist.Get('c_cwww_cw_%s_hist'%sample))
	    cwcbDataHist     = RooDataHist('cwcbDataHist_%s'   %sample,'cwcbDataHist_%s'   %sample,RooArgList(rrv_x),fileInHist.Get('c_cw_cb_%s_hist'%sample))
            
            
            sm_lin_quad_cb_DataHist         = RooDataHist('sm_lin_quad_cb_DataHist_%s'   %sample,'sm_lin_quad_cb_DataHist_%s'   %sample,RooArgList(rrv_x),fileInHist.Get('c_sm_lin_quad_%s_hist_cb'  %sample))
            sm_lin_quad_cw_DataHist         = RooDataHist('sm_lin_quad_cw_DataHist_%s'   %sample,'sm_lin_quad_cw_DataHist_%s'   %sample,RooArgList(rrv_x),fileInHist.Get('c_sm_lin_quad_%s_hist_cw'  %sample))
            sm_lin_quad_cwww_DataHist       = RooDataHist('sm_lin_quad_cwww_DataHist_%s' %sample,'sm_lin_quad_cwww_DataHist_%s' %sample,RooArgList(rrv_x),fileInHist.Get('c_sm_lin_quad_%s_hist_cwww'%sample))
            quad_cb_DataHist                = RooDataHist('quad_cb_DataHist_%s'          %sample,'quad_cb_DataHist_%s'          %sample,RooArgList(rrv_x),fileInHist.Get('c_quad_%s_hist_cb'  %sample))
            quad_cw_DataHist                = RooDataHist('quad_cw_DataHist_%s'          %sample,'quad_cw_DataHist_%s'          %sample,RooArgList(rrv_x),fileInHist.Get('c_quad_%s_hist_cw'  %sample))
            quad_cwww_DataHist              = RooDataHist('quad_cwww_DataHist_%s'        %sample,'quad_cwww_DataHist_%s'        %sample,RooArgList(rrv_x),fileInHist.Get('c_quad_%s_hist_cwww'%sample))

            fileInHist.Close()

            #make SM pdf, simple exponential
            a1_4fit         = RooRealVar('a_SM_4fit_%s'%channel,'a_SM_4fit_%s'%channel,-0.005,-0.05,0)
            a1              = RooFormulaVar('a_SM_%s'%channel,'a_SM_%s'%channel,'@0*@1',RooArgList(a1_4fit,self.eps))
            SMPdf           = RooExponential('SMPdf_%s'%channel,'SMPdf_%s'%channel,rrv_x,a1)
            ##actual fit to determine SM shape parameter a1_4fit
            fitresSM        = SMPdf.fitTo(SMdatahist, RooFit.SumW2Error(kTRUE), RooFit.Save(kTRUE))
            self.fitresults.append(fitresSM)
            a1_4fit.setConstant(kTRUE)
            #coefficient for SM term and other terms in final signal function
            N_SM                 = RooRealVar('N_SM_%s'%channel,'N_SM_%s'%channel,SMdatahist.sumEntries())
	    N_3645               = RooRealVar('N_3645_%s'%channel,'N_3645_%s'%channel,cwwwcwDataHist.sumEntries())
	    N_4520               = RooRealVar('N_4520_%s'%channel,'N_4520_%s'%channel,cwcbDataHist.sumEntries())
            N_36                 = RooRealVar('N_36_%s'%channel,'N_36_%s'%channel,cwwwPosDataHist.sumEntries())
            N__36                = RooRealVar('N__36_%s'%channel,'N__36_%s'%channel,cwwwNegDataHist.sumEntries())
            N_45                 = RooRealVar('N_45_%s'%channel,'N_45%s'%channel,cwPosDataHist.sumEntries())
            N__45                = RooRealVar('N__45%s'%channel,'N__45%s'%channel,cwNegDataHist.sumEntries())
            N_20                 = RooRealVar('N_20%s'%channel,'N_20%s'%channel,cbPosDataHist.sumEntries())
            N__20                = RooRealVar('N__20%s'%channel,'N__20%s'%channel,cbNegDataHist.sumEntries())
            N_sm_lin_quad_cb     = RooRealVar('N_sm_lin_quad_cb%s'  %channel,'N_sm_lin_quad_cb%s'%channel,sm_lin_quad_cb_DataHist.sumEntries())
            N_sm_lin_quad_cw     = RooRealVar('N_sm_lin_quad_cw%s'  %channel,'N_sm_lin_quad_cw%s'%channel,sm_lin_quad_cw_DataHist.sumEntries())
            N_sm_lin_quad_cwww   = RooRealVar('N_sm_lin_quad_cwww%s'%channel,'N_sm_lin_quad_cwww%s'%channel,sm_lin_quad_cwww_DataHist.sumEntries())
            N_quad_cb            = RooRealVar('N_quad_cb%s'  %channel,'N_quad_cb%s'%channel,  quad_cb_DataHist.sumEntries())
            N_quad_cw            = RooRealVar('N_quad_cw%s'  %channel,'N_quad_cw%s'%channel,  quad_cw_DataHist.sumEntries())
            N_quad_cwww          = RooRealVar('N_quad_cwww%s'%channel,'N_quad_cwww%s'%channel,quad_cwww_DataHist.sumEntries())


            self.Import_to_ws(self.wtmp,[cwww,cw,cb,self.eps4cbWZ,self.eps4cbWW,SMdatahist,SMdatahist,N_SM,N_sm_lin_quad_cb,N_sm_lin_quad_cw,N_sm_lin_quad_cwww,N_quad_cb,N_quad_cw,N_quad_cwww]) ###only the fitted SM is imported
            
            #define parameter ranges for error function

            if self.ch=='mu':
                Erf_width_cwww      = RooRealVar('Erf_width_cwww_%s'%channel,'Erf_width_cwww_%s'%channel,1000.,500.,1500.)
                Erf_width_cw        = RooRealVar('Erf_width_cw_%s'%channel,'Erf_width_cw_%s'%channel,1500.,1000.,2000.)
                Erf_width_cb        = RooRealVar('Erf_width_cb_%s'%channel,'Erf_width_cb_%s'%channel,1500.,1000.,2000.)
            elif self.ch=='el':
                Erf_width_cwww      = RooRealVar('Erf_width_cwww_%s'%channel,'Erf_width_cwww_%s'%channel,1000.,500.,7500.)
                Erf_width_cw        = RooRealVar('Erf_width_cw_%s'%channel,'Erf_width_cw_%s'%channel,1500.,500.,2000.)
                Erf_width_cb        = RooRealVar('Erf_width_cb_%s'%channel,'Erf_width_cb_%s'%channel,1500.,500.,2000.)

            Erf_offset_cwww         = RooRealVar('Erf_offset_cwww_%s'%channel,'Erf_offset_cwww_%s'%channel,1000.,500.,1500.)
            Erf_offset_cw           = RooRealVar('Erf_offset_cw_%s'%channel,'Erf_offset_cw_%s'%channel,1500.,500.,2500.)
            Erf_offset_cb           = RooRealVar('Erf_offset_cb_%s'%channel,'Erf_offset_cb_%s'%channel,1000.,500.,1500.)

            Erf_offset_cwww.setConstant(kTRUE);Erf_width_cwww.setConstant(kTRUE);Erf_offset_cw.setConstant(kTRUE);Erf_width_cw.setConstant(kTRUE);            Erf_offset_cb.setConstant(kTRUE);            Erf_width_cb.setConstant(kTRUE)
            self.Import_to_ws(self.wtmp,[Erf_width_cwww,Erf_offset_cwww,Erf_width_cw,Erf_offset_cw,Erf_offset_cb,Erf_width_cb])
                
            for i in range(len(self.POI)):
                s_name          = self.POI[i] + '_' + channel #added to parameter names
                fileInHist      = TFile.Open(self.rlt_DIR_name+'/hists4scale_%s_WV_aTGC-%s_%s.root'%(self.ch,self.mlvj_lo,self.mlvj_hi))
                rrv_x.setRange(self.mlvj_lo,self.mlvj_hi)                
                pos_datahist            = RooDataHist('pos_datahist_%s_%s'%(sample,self.POI[i]),'pos_datahist_%s_%s'%(sample,self.POI[i]),RooArgList(rrv_x),fileInHist.Get('c_pos_%s_hist_%s'%(sample,self.POI[i])))
                neg_datahist            = RooDataHist('neg_datahist_%s_%s'%(sample,self.POI[i]),'neg_datahist_%s_%s'%(sample,self.POI[i]),RooArgList(rrv_x),fileInHist.Get('c_neg_%s_hist_%s'%(sample,self.POI[i])))
                sm_lin_quad_datahist    = RooDataHist('sm_lin_quad_datahist_%s_%s'%(sample,self.POI[i]),'sm_lin_quad_datahist_%s_%s'%(sample,self.POI[i]),RooArgList(rrv_x),fileInHist.Get('c_sm_lin_quad_%s_hist_%s'%(sample,self.POI[i])))
                quad_datahist           = RooDataHist('quad_datahist_%s_%s'%(sample,self.POI[i]),'quad_datahist_%s_%s'%(sample,self.POI[i]),RooArgList(rrv_x),fileInHist.Get('c_quad_%s_hist_%s'%(sample,self.POI[i])))

                SMWW             = RooDataHist('SMWW_4scale','SMWW_4scale',RooArgList(rrv_x),fileInHist.Get('c_sm_WW_hist'))
                posWW            = RooDataHist('posWW_4scale_%s'%self.POI[i],'posWW_4scale_%s'%self.POI[i],RooArgList(rrv_x),fileInHist.Get('c_pos_WW_hist_%s'%self.POI[i]))
                negWW            = RooDataHist('negWW_4scale_%s'%self.POI[i],'negWW_4scale_%s'%self.POI[i],RooArgList(rrv_x),fileInHist.Get('c_neg_WW_hist_%s'%self.POI[i]))
                SMWZ             = RooDataHist('SMWZ_4scale','SMWZ_4scale',RooArgList(rrv_x),fileInHist.Get('c_sm_WZ_hist'))
                posWZ            = RooDataHist('posWZ_4scale_%s'%self.POI[i],'posWZ_4scale_%s'%self.POI[i],RooArgList(rrv_x),fileInHist.Get('c_pos_WZ_hist_%s'%self.POI[i]))
                negWZ            = RooDataHist('negWZ_4scale_%s'%self.POI[i],'negWZ_4scale_%s'%self.POI[i],RooArgList(rrv_x),fileInHist.Get('c_neg_WZ_hist_%s'%self.POI[i]))                
                sm_lin_quadWW    = RooDataHist('sm_lin_quadWW_4scale_%s'%self.POI[i],'sm_lin_quadWW_4scale_%s'%self.POI[i],RooArgList(rrv_x),fileInHist.Get('c_sm_lin_quad_WW_hist_%s'%self.POI[i]))
                quadWW           = RooDataHist('quadWW_4scale_%s'%self.POI[i],'quadWW_4scale_%s'%self.POI[i],RooArgList(rrv_x),fileInHist.Get('c_quad_WW_hist_%s'%self.POI[i]))
                sm_lin_quadWZ    = RooDataHist('sm_lin_quadWZ_4scale_%s'%self.POI[i],'sm_lin_quadWZ_4scale_%s'%self.POI[i],RooArgList(rrv_x),fileInHist.Get('c_sm_lin_quad_WZ_hist_%s'%self.POI[i]))
                quadWZ           = RooDataHist('quadWZ_4scale_%s'%self.POI[i],'quadWZ_4scale_%s'%self.POI[i],RooArgList(rrv_x),fileInHist.Get('c_quad_WZ_hist_%s'%self.POI[i]))

                fileInHist.Close()

                #import datasets to wtmp and final workspace WS
                self.Import_to_ws(self.wtmp,[pos_datahist,neg_datahist,sm_lin_quad_datahist,quad_datahist])
                self.Import_to_ws(self.WS,[pos_datahist,neg_datahist,sm_lin_quad_datahist,quad_datahist])
                #get scaling parabel from yields
                #FIXME scaling to the sum of WW and WZ leads to over-estimating WW and under-estimating WZ
                #FIXME scaling to WW and WZ separately leads to a really high scaling factor for WZ
                hist4scale = TH1F('hist4scale_%s'%self.POI[i],'hist4scale_%s'%self.POI[i],3,-1.5*self.PAR_MAX[self.POI[i]],1.5*self.PAR_MAX[self.POI[i]])
                hist4scale.SetBinContent(2,1)
                factor=1.0; #if3(self.POI[i] == "cwww",3.6, if3(self.POI[i] == "cb",20,4.5))

		if sample=='WW':
		    hist4scale.SetBinContent(1,(negWW.sumEntries())/(SMWW.sumEntries()))
                    hist4scale.SetBinContent(3,(posWW.sumEntries())/(SMWW.sumEntries()))
                
                    nevt_posWW=posWW.sumEntries()/factor;
                    nevt_negWW=negWW.sumEntries()/factor;
                    norm_lin   = RooRealVar('norm_sm_lin_quad_%s'%s_name,'norm_sm_lin_quad_%s'%s_name,0.5*(nevt_posWW-nevt_negWW)/SMWW.sumEntries())
                    norm_quad  = RooRealVar('norm_quad_%s'%s_name,'norm_quad_%s'%s_name,(0.5*(nevt_posWW+nevt_negWW)-SMWW.sumEntries())/SMWW.sumEntries() )
		else:
		    hist4scale.SetBinContent(1,(negWZ.sumEntries())/(SMWZ.sumEntries()))
                    hist4scale.SetBinContent(3,(posWZ.sumEntries())/(SMWZ.sumEntries()))
                    nevt_posWZ=posWZ.sumEntries()/factor;
                    nevt_negWZ=negWZ.sumEntries()/factor;
                    norm_lin   = RooRealVar('norm_sm_lin_quad_%s'%s_name,'norm_sm_lin_quad_%s'%s_name,0.5*(nevt_posWZ-nevt_negWZ)/SMWZ.sumEntries())
                    norm_quad  = RooRealVar('norm_quad_%s'%s_name,'norm_quad_%s'%s_name,(0.5*(nevt_posWZ+nevt_negWZ)-SMWZ.sumEntries())/SMWZ.sumEntries() )

                #fit parabel
                hist4scale.Fit('pol2','0')
                fitfunc     = hist4scale.GetFunction('pol2')
                par1        = RooRealVar('par1_%s'%s_name,'par1_%s'%s_name,fitfunc.GetParameter(1));
                par1.setConstant(kTRUE);
                par2        = RooRealVar('par2_%s'%s_name,'par2_%s'%s_name,fitfunc.GetParameter(2));
                par2.setConstant(kTRUE);

                N_pos_tmp         = pos_datahist.sumEntries()
                N_neg_tmp         = neg_datahist.sumEntries()
                N_quad            = RooRealVar('N_quad_%s'%s_name,'N_quad_%s'%s_name, ((N_pos_tmp+N_neg_tmp)/2)-N_SM.getVal())# if  not (self.POI[i]=='cb'  and sample=='WZ') else 0)
                N_lin             = RooRealVar('N_sm_lin_quad_%s'%s_name,'N_sm_lin_quad_%s'%s_name,((N_pos_tmp+N_neg_tmp)/2)-N_SM.getVal()) 
                #scaleshape is the relative change to SM
                print "$$$$$$$$$$$$$$$$$thats the sname",s_name
                scaleshape       = RooFormulaVar('scaleshape_%s'%s_name,'scaleshape_%s'%s_name, '(@0*@2+@1*@2**2)', RooArgList(par1,par2,self.wtmp.var(self.POI[i])))
                #FIXME only very few atgc events for cb in WZ sample, fit doesn't work yet -> different parametrization, starting values+ranges or leave out completely
                if  self.POI[i]=='cb': #  and sample=='WZ': #so cb for WW is also modeled using exponential
                    #N_lin       = RooRealVar('N_sm_lin_quad_%s'%s_name,'N_sm_lin_quad_%s'%s_name,(N_pos_tmp-N_neg_tmp)/2) ##0 
                    a2_4fit     = RooRealVar('a_quad_4fit_%s'%s_name,'a_quad_4fit_%s'%s_name,-0.1,-2,0.)
                    a2          = RooFormulaVar('a_quad_nuis_%s'%s_name,'a_quad_nuis_%s'%s_name,'@0*@1',RooArgList(a2_4fit,self.eps4cbWZ if sample=='WZ' else self.eps4cbWW))
                    a3_4fit     = RooRealVar('a_lin_4fit_%s'%s_name,'a_lin_4fit_%s'%s_name,-0.0001,-0.1,0.)
                    a3          = RooFormulaVar('a_lin_nuis_%s'%s_name,'a_lin_nuis_%s'%s_name,'@0*@1',RooArgList(a3_4fit,self.eps4cbWZ if sample=='WZ' else self.eps4cbWW))
                    cPdf_quad   = RooExponential('%s_quad_%s_%s'%(sample,self.POI[i],self.ch),'%s_quad_%s_%s'%(sample,self.POI[i],self.ch),rrv_x,a2)

                else:
		    #N_lin      = RooRealVar('N_lin_%s'%s_name,'N_lin_%s'%s_name, 0 )
                    #N_lin       = RooRealVar('N_sm_lin_quad_%s'%s_name,'N_sm_lin_quad_%s'%s_name,(N_pos_tmp-N_neg_tmp)/2)
                    a2_4fit     = RooRealVar('a_quad_4fit_%s'%s_name,'a_quad_4fit_%s'%s_name,-0.001,-0.01,0.1)
                    a2          = RooFormulaVar('a_quad_nuis_%s'%s_name,'a_quad_nuis_%s'%s_name,'@0*@1',RooArgList(a2_4fit,self.eps))
                    a3_4fit     = RooRealVar('a_lin_4fit_%s'%s_name,'a_lin_4fit_%s'%s_name,-0.001,-0.01,0.1)
                    a3          = RooFormulaVar('a_lin_nuis_%s'%s_name,'a_lin_nuis_%s'%s_name,'@0*@1',RooArgList(a3_4fit,self.eps))
                    cPdf_quad   = RooErfExpPdf('%s_quad_%s_%s'%(sample,self.POI[i],self.ch),'%s_quad_%s_%s'%(sample,self.POI[i],self.ch),rrv_x,a2,self.wtmp.var('Erf_offset_%s'%s_name),self.wtmp.var('Erf_width_%s'%s_name))
                

                a2_4fit.setConstant(kTRUE)
                a3_4fit.setConstant(kTRUE)
                #PDF for SM interference
                #cPdf_lin        = RooExponential('Pdf_lin_%s'%s_name,'Pdf_lin_%s'%s_name,rrv_x,a3)
                cPdf_lin        = RooExponential('%s_sm_lin_quad_%s_%s'%(sample,self.POI[i],self.ch),'%s_sm_lin_quad_%s_%s'%(sample,self.POI[i],self.ch),rrv_x,a3)
                self.Import_to_ws(self.wtmp,[cPdf_quad,cPdf_lin],1)
                self.Import_to_ws(self.wtmp,[N_quad,N_lin,scaleshape,norm_lin,norm_quad])
                
            ###make model
            #list of all coefficients
            paralist    = RooArgList(N_SM)

            # Include aTGC-interference
            # Get parameter values of aTGC-interference from tmp workspace where they are saved in the start 
            a5_tmp      = RooRealVar('a_cwww_cw_%s'%channel,'a_cwww_cw_%s'%channel, self.wtmp.var('a5_%s'%sample).getVal())
            a7_tmp      = RooRealVar('a_cw_cb_%s'%channel,'a_cw_cb_%s'%channel, self.wtmp.var('a7_%s'%sample).getVal())
            a5_tmp.setConstant(kTRUE)
            a7_tmp.setConstant(kTRUE)
            #apply uncertainty parameter, bigger uncertainty for c_B in WZ
            a5          = RooFormulaVar('a_cwww_cw_nuis_%s'%channel,'a_cwww_cw_nuis_%s'%channel,'@0*@1',RooArgList(a5_tmp,self.eps))
            a7          = RooFormulaVar('a_cw_cb_nuis_%s'%channel,'a_cw_cb_nuis_%s'%channel,'@0*@1',RooArgList(a7_tmp,self.eps4cbWZ if sample=='WZ' else self.eps4cbWW))
            
            Pdf_cwww_cw    = RooExponential('Pdf_cwww_cw_%s'%channel,'Pdf_cwww_cw_%s'%channel,rrv_x,a5)
            Pdf_cw_cb      = RooExponential('Pdf_cw_cb_%s'%channel,'Pdf_cw_cb_%s'%channel,rrv_x,a7)


            # Get other coefficients
            NSM         = N_SM.getVal()
            N3645       = N_3645.getVal()
            N4520       = N_4520.getVal()
            N36         = N_36.getVal()
            N36_        = N__36.getVal()
            N45         = N_45.getVal()
            N45_        = N__45.getVal()
            N20         = N_20.getVal()
            N20_        = N__20.getVal()
            N__sm_lin_quad_cb    = N_sm_lin_quad_cb.getVal()   
            N__sm_lin_quad_cw    = N_sm_lin_quad_cw.getVal()   
            N__sm_lin_quad_cwww  = N_sm_lin_quad_cwww.getVal() 
            N__quad_cb           = N_quad_cb.getVal()          
            N__quad_cw           = N_quad_cw.getVal()          
            N__quad_cwww         = N_quad_cwww.getVal()        

            print "ylds\t",channel,"\t SM\t",NSM,"\tc3W(I)",N__sm_lin_quad_cwww,"\tc3W(Q)\t",N__quad_cwww,"\tcw(I)",N__sm_lin_quad_cw,"\tcW(Q)\t",N__quad_cw,"\tcb(Q)\t",N__quad_cb,"\t cb(I)\t",N__sm_lin_quad_cb
 
            N_cwww_cw      = RooRealVar('N_cwww_cw_%s'%channel,'N_cwww_cw_%s'%channel,\
                                            ((N3645+NSM)-(N36+N45)))
            N_cw_cb        = RooRealVar('N_cw_cb_%s'%channel,'N_cw_cb_%s'%channel,\
                                            ((N4520+NSM)-(N45+N20)))
            #self.wtmp.function('N_lin_%s_%s'%(self.POI[1],channel)),
            paralist.add(RooArgList(self.wtmp.function('N_quad_%s_%s'%(self.POI[0],channel)),self.wtmp.var('cwww'),\
                                    self.wtmp.function('N_quad_%s_%s'%(self.POI[1],channel)),self.wtmp.function('N_sm_lin_quad_%s_%s'%(self.POI[1],channel)),self.wtmp.var('cw'),\
                                    self.wtmp.function('N_quad_%s_%s'%(self.POI[2],channel)),self.wtmp.function('N_sm_lin_quad_%s_%s'%(self.POI[2],channel)),self.wtmp.var('cb')))
            paralist.add(RooArgList(N_cwww_cw,N_cw_cb))
            
            #parts of final signal model formula
            cwww_s      = '+@1*(@2/3.6)**2' #SM-BSM interference is negligible for both WW and WZ 
            ccw_s       = '+@3*(@5/4.5)**2+@4*(@5/4.5)'
            cb_s        = '+@6*(@8/20)**2+@7*(@8/20)'
            cwww_ccw_s  = '+@9*(@2/3.6)*(@5/4.5)'
            ccw_cb_s    = '+@10*(@5/4.5)*(@8/20)'
            Pdf_norm    = RooFormulaVar('Pdf_norm_%s'%channel, 'Pdf_norm_%s'%channel, '@0'+cwww_s+ccw_s+cb_s+cwww_ccw_s+ccw_cb_s, paralist)

            paralistN   = RooArgList()
    
            for i in range(11):
                paralistN.add(RooArgList(paralist.at(i)))
            paralistN.add(RooArgList(Pdf_norm))

            N1                = RooFormulaVar( 'N1_%s'%channel, 'N1_%s'%channel, '@0/@11', paralistN )
            N2                = RooFormulaVar( 'N2_%s'%channel, 'N2_%s'%channel, '(@1*(@2/3.6)**2)/@11', paralistN )
            #N3 ->no SM-interference for c_WWW
            N4                = RooFormulaVar( 'N4_%s'%channel, 'N4_%s'%channel, '(@3*(@5/4.5)**2)/@11', paralistN )
            N5                = RooFormulaVar( 'N5_%s'%channel, 'N5_%s'%channel, '(@4*(@5/4.5))/@11', paralistN )
            N6                = RooFormulaVar( 'N6_%s'%channel, 'N6_%s'%channel, '(@6*(@8/20)**2)/@11', paralistN )
            N7                = RooFormulaVar( 'N7_%s'%channel, 'N7_%s'%channel, '(@7*(@8/20))/@11', paralistN )
            N8                = RooFormulaVar( 'N8_%s'%channel, 'N8_%s'%channel, '(@9*(@2/3.6)*(@5/4.5))/@11', paralistN )
            #N9 ->no aTGC-interference for c_WWW/c_B #FIXME should be added for WZ
            N10               = RooFormulaVar( 'N10_%s'%channel,'N10_%s'%channel,'(@10*(@5/4.5)*(@8/20))/@11', paralistN )

            N_list        = RooArgList(N1,N2,N4,N5,N6,N7)
            N_list.add(RooArgList(N8,N10))
            Pdf_list        = RooArgList(SMPdf)
            ##AMin the following add interference terrm for cwww #self.wtmp.pdf('Pdf_lin_cwww_%s'%channel),\
            ##amPdf_list.add(RooArgList(self.wtmp.pdf('Pdf_quad_cwww_%s'%channel),\
            ##am                        self.wtmp.pdf('Pdf_quad_cw_%s'%channel),self.wtmp.pdf('Pdf_lin_cw_%s'%channel),\
            ##am                        self.wtmp.pdf('Pdf_quad_cb_%s'%channel),self.wtmp.pdf('Pdf_lin_cb_%s'%channel)))
            Pdf_list.add(RooArgList(self.wtmp.pdf('%s_quad_cwww_%s'%(sample,self.ch)),\
                                    self.wtmp.pdf('%s_quad_cw_%s'%(sample,self.ch)),self.wtmp.pdf('%s_sm_lin_quad_cw_%s'%(sample,self.ch)),\
                                    self.wtmp.pdf('%s_quad_cb_%s'%(sample,self.ch)),self.wtmp.pdf('%s_sm_lin_quad_cb_%s'%(sample,self.ch))))
            Pdf_list.add(RooArgList(Pdf_cwww_cw,Pdf_cw_cb))
            model             = RooAddPdf('aTGC_model_%s'%channel,'aTGC_model_%s'%channel, Pdf_list, N_list)
            if options.verbose: print model
            scale_list        = RooArgList(self.wtmp.function('scaleshape_cwww_%s'%channel), self.wtmp.function('scaleshape_cw_%s'%channel), self.wtmp.function('scaleshape_cb_%s'%channel))
            normfactor_3d     = RooFormulaVar('normfactor_3d_%s'%channel,'normfactor_3d_%s'%channel,'1+@0+@1+@2',scale_list)

            if options.verbose: self.wtmp.Print()

            #fit 3 pdfs for 3 atgc parameters
            for i in range(3):
                s_name        = self.POI[i] + '_' + channel
                for j in range(3):
                    self.wtmp.var(self.POI[j]).setVal(0)
                self.wtmp.var(self.POI[i]).setVal(self.PAR_MAX[self.POI[i]])

                #fit SM-interference first
                ##no SM-interference for cwww; not enough aTGC events for cb in WZ sample
                if not self.POI[i] == 'cwww' and not (sample=='WZ' and self.POI[i]=='cb'):
                    #set SM and quadratical terms to zero so only the linear term is fitted
                    N_SM_tmp = N_SM.getVal()
                    N_quad_tmp = self.wtmp.var('N_quad_%s'%s_name).getVal()
                    N_SM.setVal(0)
                    self.wtmp.var('N_quad_%s'%s_name).setVal(0)
                    
                    self.wtmp.var('a_lin_4fit_%s'%s_name).setConstant(kFALSE)
                    fitres1                = model.fitTo(self.wtmp.data('sm_lin_quad_datahist_%s_%s'%(sample,self.POI[i])),RooFit.Save(kTRUE), RooFit.SumW2Error(kTRUE), RooFit.Minimizer('Minuit2'))
                    self.wtmp.var('a_lin_4fit_%s'%s_name).setConstant(kTRUE)
                    self.fitresults.append(fitres1)
                    
                    N_SM.setVal(N_SM_tmp)
                    self.wtmp.var('N_quad_%s'%s_name).setVal(N_quad_tmp)

                #fit quadratic term
                self.wtmp.var('a_quad_4fit_%s'%s_name).setConstant(kFALSE)
                if self.POI[i]!='cb' and sample=='WZ':
                    self.wtmp.var('Erf_offset_%s'%s_name).setConstant(kFALSE)
                    self.wtmp.var('Erf_width_%s'%s_name).setConstant(kFALSE)
                fitres2         = model.fitTo(self.wtmp.data('pos_datahist_%s_%s'%(sample,self.POI[i])), RooFit.Save(kTRUE), RooFit.SumW2Error(kTRUE))
                fitres2         = model.fitTo(self.wtmp.data('pos_datahist_%s_%s'%(sample,self.POI[i])), RooFit.Save(kTRUE), RooFit.SumW2Error(kTRUE), RooFit.Minimizer('Minuit2'))
                self.wtmp.var('a_quad_4fit_%s'%s_name).setConstant(kTRUE)
                if self.POI[i]!='cb' and sample=='WZ':
                    self.wtmp.var('Erf_offset_%s'%s_name).setConstant(kTRUE)
                    self.wtmp.var('Erf_width_%s'%s_name).setConstant(kTRUE)
                self.fitresults.append(fitres2)
                
            for i in range(3):
                self.wtmp.var(self.POI[i]).setVal(0)

            if options.verbose: model.Print()
            self.Import_to_ws(self.wtmp,[normfactor_3d,model])
            self.Import_to_ws(self.WS,[normfactor_3d,model])

            #print coefficients to see contribution for all atgc-parameter positive
            for i in range(3):
                self.wtmp.var(self.POI[i]).setVal(self.PAR_MAX[self.POI[i]])
            for i in range(11):
                print paralist.at(i).GetName() + ' : ' + str(paralist.at(i).getVal())

            #print self.fitresults
            for i in range(8):
                print N_list.at(i).GetName() + ' : ' + str(N_list.at(i).getVal())


        def Write_datacard(self,w,region):
            ### make the card for this channel and plane ID
            ##amcodename    = 'WWWZ_' + region + '_' + self.ch
            dirName = os.path.join("../WJets_est",self.rlt_DIR_name)#"since we move everyhting one dir up"
            pbkgs  = ['WJets','TTbar','STop']
            dbbkgs = ['WW_sm','WZ_sm']
            terms  = ['_sm_lin_quad_','_quad_']
            moreprocs=[p+q for p in ['WZ','WW'] for q in terms]               
            EFTprocs=[p+q for p in moreprocs for q in self.POI]
            allprocs=EFTprocs+pbkgs+dbbkgs
            binname = '{region}_{ch}'.format(ch=self.ch,region=region)
            codename='WWWZ_{region}_{ch}_{year}'.format(ch=self.ch,region=region,year=self.year)
            cardName_test='aC_%s_%s.txt'%(codename,date)
            print ("this is where i am keeping the card",cardName_test)
            datacard = open(cardName_test,'w')
            datacard.write('##----------------------------------\n')
            datacard.write('bin         %s\n' % binname)            
            klen = max([7, len(binname)]+[len(p) for p in allprocs])

            kpatt = " %%%ds "  % klen
            nuisances=[]
            npatt = "%%-%ds " % max([len('process')]+map(len,nuisances))
            rate_str= "1"
            iproc={}
            for i,s in enumerate(allprocs):
                if s in dbbkgs:
                    iproc[s] = -99+i
                else:
                    iproc[s]=i+1
            datacard.write('\nimax 1  number of channels\njmax *  number of backgrounds\nkmax *  number of nuisance parameters (sources of systematical uncertainties)\n\n')
            for i in pbkgs:
                nr=28-len(i)
                datacard.write( ("shapes %s"%i)+(" "*nr)+binname+(" "*klen)+" {dirName}/WWWZ_{binName}_{year}_ws.root {here} proc_WWWZ_{binName}_{year}:$PROCESS".format(here= (" "*3),year=self.year,binName=binname,dirName=dirName)+"\n")
            for i in EFTprocs:
                nr=28-len(i)
                datacard.write( ("shapes %s"%i)+(" "*nr)+binname+(" "*klen)+" {dirName}/WWWZ_{binName}_{year}_ws.root {here} proc_WWWZ_{binName}_{year}:{proc}".format(here= (" "*3),year=self.year,binName=binname,dirName=dirName,proc=i+"_"+self.ch)+"\n")
            for i in dbbkgs:
                nr=28-len(i)
                datacard.write( ("shapes %s"%i)+(" "*nr)+binname+(" "*klen)+" {dirName}/WWWZ_{binName}_{year}_ws.root {here} proc_WWWZ_{binName}_{year}:".format(binName=binname,here= (" "*3),year=self.year,dirName=dirName)+i.split("_sm")[0]+"\n")
            nr=28-len("data_obs")
            datacard.write("shapes data_obs"+(" "*nr)+binname+(" "*klen)+" {dirName}/WWWZ_{binName}_{year}_ws.root {here}  proc_WWWZ_{binName}_{year}:$PROCESS\n".format(binName=binname,here= (" "*3),year=self.year,dirName=dirName))
            datacard.write('##----------------------------------\n')
            datacard.write('bin         %s\n' % binname)
            datacard.write('observation %s\n' % w.data('dataset_2d_%s_%s'%(region,self.ch)).sumEntries())
            datacard.write((npatt % 'bin    ')+(" "*3)+(" ".join([kpatt % binname  for p in allprocs]))+"\n")
            datacard.write((npatt % 'process')+(" "*3)+(" ".join([kpatt % p        for p in allprocs]))+"\n")
            datacard.write((npatt % 'process')+(" "*3)+(" ".join([kpatt % iproc[p] for p in allprocs]))+"\n")
            datacard.write((npatt % 'rate   ')+(" "*3)+(" ".join([kpatt % rate_str for p in allprocs ]))+"\n")
            datacard.write('##----------------------------------\n')
            datacard.write('''
normvar_WJets_{ch}  flatParam

rrv_c_Exp_WJets0_{ch}  flatParam
rrv_c_Exp_WJets0_sb_{ch}  flatParam
rrv_n_Exp_WJets0_sb_{ch}  flatParam
Deco_WJets0_sim_{ch}_HPV_mlvj_13TeV_eig0 param 0.0 1.4
Deco_WJets0_sim_{ch}_HPV_mlvj_13TeV_eig1 param 0.0 1.4
Deco_WJets0_sim_{ch}_HPV_mlvj_13TeV_eig2 param 0.0 1.4
Deco_WJets0_sim_{ch}_HPV_mlvj_13TeV_eig3 param 0.0 1.4
slope_nuis    param  1.0 0.05'''.format(ch=self.ch)
                       )    
            datacard.close()
            return cardName_test


        ########################
        ######MAIN CODE#########
        ########################
        def Make_input(self):

            #prepare variables, parameters and temporary workspace
            #if options.readtrees:
            self.Read_ATGCtree(self.ch)
            
            #make and fit signal pdf for WW and WZ
            self.Make_signal_pdf(self.rrv_mass_lvj,'WW')
            self.Make_signal_pdf(self.rrv_mass_lvj,'WZ')

            #read, rename and write bkg pdfs and bkg rates
            fileInWs    = TFile.Open(self.rlt_DIR_name+'/wwlvj_%s_%s_%s_%s_workspace.root'%(self.ch,self.wtagger_label,int(self.mlvj_lo),int(self.mlvj_hi)))
            w_bkg       = fileInWs.Get('workspace4limit_') 

            for bkg in ['WJets','TTbar','STop','WW','WZ']:
                if options.verbose: w_bkg.var('norm_%s_%s'%(bkg,self.ch)).Print()
                getattr(self.WS,'import')(w_bkg.var('norm_%s_%s'%(bkg,self.ch)))

            #import m_pruned and define ranges
            getattr(self.WS,'import')(w_bkg.var('rrv_mass_j'))
            self.WS.var('rrv_mass_j').setRange('sb_lo',45,65)
            self.WS.var('rrv_mass_j').setRange('sig',65,105)
            self.WS.var('rrv_mass_j').setRange('sb_hi',105,150)
            self.WS.var('rrv_mass_lvj').setRange(950,4550)
            #bkg-pdfs have the format '[bkg-name]_mlvj_[region]_[ch]' or '[bkg-name]_mj_[region]_[ch]'

            rrv_mass_j   = w_bkg.var("rrv_mass_j")#with correct wts
            rrv_mass_lvj = w_bkg.var("rrv_mass_lvj")#with correct wts

            #create a workspace for each component in each region
            for region in self.regions:
                self.WS2 = self.WS.Clone("w")        #temporary 
                set_mj          = RooArgSet(self.WS2.var('rrv_mass_j'))
                for bkg in self.bkgs:
                    #define global norm for whole mj spectrum
                    norm_var    = RooRealVar('normvar_%s_%s'%(bkg,self.ch),'normvar_%s_%s'%(bkg,self.ch),self.WS2.var("norm_%s_%s"%(bkg,self.ch)).getVal(),0,1e4)
                    norm_var.setConstant(kTRUE)
                    #define integral over region
                    reg_Int     = w_bkg.pdf('mj_%s_%s'%(bkg,self.ch)).createIntegral(set_mj,set_mj, region)
                    if bkg=='WJets':        #norm floating for WJets, integral depends on (floating) shape parameter
                        norm    = RooFormulaVar('%s_%s_%s_norm'%(bkg,region,self.ch),'%s_%s_%s_norm'%(bkg,region,self.ch),'@0*@1',RooArgList(reg_Int,norm_var))
                    else:#norm and integral fixed for rest
                        norm    = RooFormulaVar('%s_%s_%s_norm'%(bkg,region,self.ch),'%s_%s_%s_norm'%(bkg,region,self.ch),'%s*@0'%reg_Int.getVal(),RooArgList(norm_var))
                    if region == 'sig':
                        bkg_MWV = w_bkg.pdf('%s_mlvj_sig_%s'%(bkg,self.ch))
                    else:#pdfs from the sb fit are fitted simultaneously in the lower and upper sb
                        bkg_MWV = w_bkg.pdf('%s_mlvj_sb_%s'%(bkg,self.ch)).clone('%s_mlvj_%s_%s'%(bkg,region,self.ch))
                    bkg_mj      = w_bkg.pdf('%s_mj_%s_%s'%(bkg,region,self.ch))
                    #make 2d pdf
                    bkg_2d_pdf  = RooProdPdf(bkg,bkg,RooArgList(bkg_MWV,bkg_mj))
                    if options.verbose: bkg_MWV.Print();bkg_mj.Print();bkg_2d_pdf.Print();
                    norm.SetName(bkg_2d_pdf.GetName()+'_norm')#the normalization variable must have the corresponding pdf-name + _norm
                    self.Import_to_ws(self.WS2,[bkg_2d_pdf,norm],1)

                #signal function for WW and WZ in signal region and lower/upper sideband
                ##FIXME? signal shape is not explicitly evaluated in the sideband region since its contribution is assumed to be negligible there
                data_obs            = RooDataSet('data_obs','data_obs',w_bkg.data('dataset_2d_%s_%s'%(region,self.ch)),RooArgSet(self.WS2.var('rrv_mass_lvj'),self.WS2.var('mj_%s'%region)))
                getattr(self.WS2,'import')(data_obs)

                for VV in ['WW','WZ']:
                    ##AM HERE define the normalizations for linear and quadratic terms
                    pdf_atgc_mlvj_VV        = self.WS2.pdf('aTGC_model_%s_%s'%(self.ch,VV))
                    pdf_atgc_mj_VV          = w_bkg.pdf('%s_mj_%s_%s'%(VV,region,self.ch))
                    pdf_atgc_VV_2d          = RooProdPdf('aTGC_%s_%s_%s'%(VV,region,self.ch),'aTGC_%s_%s_%s'%(VV,region,self.ch),RooArgList(pdf_atgc_mlvj_VV,pdf_atgc_mj_VV))
                    norm_VV_reg             = self.WS2.function("%s_norm"%VV).Clone("%s_norm_%s_%s"%(VV,region,self.ch))
                    signal_norm_VV          = RooFormulaVar(pdf_atgc_VV_2d.GetName()+'_norm',pdf_atgc_VV_2d.GetName()+'_norm','@0*@1',RooArgList(self.WS2.function('normfactor_3d_%s_%s'%(self.ch,VV)),norm_VV_reg))

                    self.Import_to_ws(self.WS2,[pdf_atgc_VV_2d,signal_norm_VV],1)

                    for ops in ['cwww','cw','cb']:
                        pdf_sm_lin_quad_mlvj_VV = self.wtmp.pdf('%s_sm_lin_quad_%s_%s'%(VV,ops,self.ch)) ##AMNewPdf_lin
                        pdf_quad_mlvj_VV        = self.wtmp.pdf('%s_quad_%s_%s'%(VV,ops,self.ch)) ##AMNewPdf_quad
                        print "defined pdfs",ops,VV,region,self.ch,pdf_sm_lin_quad_mlvj_VV.Print();
                        pdf_sm_lin_quad_VV_2d  = RooProdPdf('%s_sm_lin_quad_%s_%s_%s'%(VV,ops,region,self.ch),'%s_sm_lin_quad_%s_%s_%s'%(VV,ops,region,self.ch),RooArgList(pdf_sm_lin_quad_mlvj_VV,pdf_atgc_mj_VV))
                        print "moving on with the quad pdf",VV,region,self.ch
                        pdf_quad_VV_2d     = RooProdPdf('%s_quad_%s_%s_%s'%(VV,ops,region,self.ch),'%s_quad_%s_%s_%s'%(VV,ops,region,self.ch),RooArgList(pdf_quad_mlvj_VV,pdf_atgc_mj_VV))
                        signal_lin_norm_VV = RooFormulaVar(pdf_sm_lin_quad_VV_2d.GetName()+'_norm',pdf_sm_lin_quad_VV_2d.GetName()+'_norm','@0*@1',RooArgList(self.wtmp.var('norm_sm_lin_quad_%s_%s_%s'%(ops,self.ch,VV)),norm_VV_reg))
                        signal_quad_norm_VV = RooFormulaVar(pdf_quad_VV_2d.GetName()+'_norm',pdf_quad_VV_2d.GetName()+'_norm','@0*@1',RooArgList(self.wtmp.var('norm_quad_%s_%s_%s'%(ops,self.ch,VV)),norm_VV_reg))
                        self.Import_to_ws(self.WS2,[pdf_sm_lin_quad_VV_2d,pdf_quad_VV_2d,signal_lin_norm_VV,signal_quad_norm_VV],1)
                        
                        mplot_tmp_AM = rrv_mass_lvj.frame( RooFit.Bins(rrv_mass_lvj.getBins()));
                        c3_AM=ROOT.TCanvas('c3_%s_%s_%s_%s'%(ops,VV,region,self.ch),'',600,600); #c3_AM.SetLogy();
                        
                        pdf_sm_lin_quad_mlvj_VV.plotOn(mplot_tmp_AM, RooFit.Name("lin"),RooFit.LineStyle(kDashDotted),RooFit.LineColor(ROOT.kOrange));
                        pdf_quad_mlvj_VV.plotOn(mplot_tmp_AM, RooFit.Name("quad"), RooFit.LineStyle(kDotted),RooFit.LineColor(ROOT.kBlue));
                        pdf_atgc_mlvj_VV.plotOn(mplot_tmp_AM, RooFit.Name("aTGC"), RooFit.LineStyle(kDotted),RooFit.LineColor(ROOT.kGreen));
                        legend = ROOT.TLegend(0.26,0.64,0.82,0.86);
                        legend.SetNColumns(3);legend.SetFillColor(0);legend.SetFillStyle(0); legend.SetShadowColor(0);   legend.SetLineColor(0);
                        legend.SetTextFont(42);        legend.SetBorderSize(0);   legend.SetTextSize(0.04);
                        legend.AddEntry(pdf_quad_mlvj_VV,'quad','l')
                        legend.AddEntry(pdf_sm_lin_quad_mlvj_VV,'lin','l')
                        legend.AddEntry(pdf_atgc_mlvj_VV,'aTGC','l')
                        #mplot_tmp_AM.addObject(legend);
                        c3_AM.cd();
                        mplot_tmp_AM.SetYTitle("PDFs"); mplot_tmp_AM.GetYaxis().SetTitleOffset(1.05);
                        mplot_tmp_AM.Draw();     
                        legend.Draw();
                        c3_AM.Draw();
                        c3_AM.SaveAs(self.plotsDir+'pdfs_%s_%s%s_%s.png'%(ops,self.ch,region,VV))
                        c3_AM.SaveAs(self.plotsDir+'pdfs_%s_%s%s_%s.pdf'%(ops,self.ch,region,VV))
                        
                    

                ##define which parameters are floating (also has to be done in the datacard)
                print "this is missing piece of crap==============","rrv_c_Exp_WJets0_%s"%self.ch
                self.WS2.var("rrv_c_ChiSq_WJets0_%s"%self.ch).setConstant(kFALSE) ##am
                #self.WS2.var("rrv_c_Exp_WJets0_%s"%self.ch).setConstant(kFALSE)
                self.WS2.var("normvar_WJets_%s"%self.ch).setConstant(kFALSE)
                if 'sb' in region:
                    self.WS2.var("rrv_c_Exp_WJets0_sb_%s"%self.ch).setConstant(kFALSE)
                    #self.WS2.var("rrv_n_Exp_WJets0_sb_%s"%self.ch).setConstant(kFALSE)
                else:
                    self.WS2.var("Deco_WJets0_sim_%s_%s_mlvj_13TeV_eig0"%(self.ch,self.wtagger_label)).setConstant(kTRUE)
                    self.WS2.var("Deco_WJets0_sim_%s_%s_mlvj_13TeV_eig1"%(self.ch,self.wtagger_label)).setConstant(kTRUE)
                    #self.WS2.var("Deco_WJets0_sim_%s_%s_mlvj_13TeV_eig2"%(self.ch,self.wtagger_label)).setConstant(kTRUE)
                    #self.WS2.var("Deco_WJets0_sim_%s_%s_mlvj_13TeV_eig3"%(self.ch,self.wtagger_label)).setConstant(kTRUE)

                output        = TFile(self.rlt_DIR_name+'/WWWZ_{region}_{ch}_{year}_ws.root'.format(ch=self.ch,region=region,year=self.year),'recreate')
                self.WS2.SetName('proc_WWWZ_%s_%s_%s'%(region,self.ch,self.year))
                self.WS2.Write();
                output.Close()
                print ('Write to file ' + output.GetName())


            ##create the datacards for all regions
            card_sb_lo=self.Write_datacard(w_bkg,"sb_lo")
            card_sig=self.Write_datacard(w_bkg,"sig")
            card_sb_hi=self.Write_datacard(w_bkg,"sb_hi")
            combineCardName="aC_WWWZ_%s_%s.txt"%(self.ch,date)
            cmd = 'combineCards.py {sig} {sb_lo} {sb_hi}  > {dC}'.format(sig=card_sig,sb_lo=card_sb_lo,sb_hi=card_sb_hi,dC=combineCardName)
            #print (cmd)
            #os.system(cmd)
            #os.system('mv *txt %s/'%(self.rlt_DIR_name))
            #os.system('mv %s %s'%(combineCardName,self.rlt_DIR_name))
#            dC=open(combineCardName,'a')
#            dC.write('''            
#normvar_WJets_{ch}  flatParam
#rrv_c_ChiSq_WJets0_{ch}  flatParam
#rrv_n_ExpN_WJets0_sb_{ch}  flatParam
#rrv_c_ExpN_WJets0_sb_{ch}  flatParam
#Deco_WJets0_sim_{ch}_{WP}_mlvj_13TeV_eig0 param 0.0 1.4
#Deco_WJets0_sim_{ch}_{WP}_mlvj_13TeV_eig1 param 0.0 1.4
#Deco_WJets0_sim_{ch}_{WP}_mlvj_13TeV_eig2 param 0.0 1.4
#Deco_WJets0_sim_{ch}_{WP}_mlvj_13TeV_eig3 param 0.0 1.4
#Deco_TTbar_sb_{ch}_{WP}_mlvj_13TeV_eig0 param 0.0 2.0
#Deco_TTbar_sb_{ch}_{WP}_mlvj_13TeV_eig1 param 0.0 2.0
#Deco_TTbar_sig_{ch}_{WP}_mlvj_13TeV_eig0 param 0.0 2.0
#Deco_TTbar_sig_{ch}_{WP}_mlvj_13TeV_eig1 param 0.0 2.0
#slope_nuis    param  1.0 0.05'''.format(ch=self.ch,WP=self.wtagger_label))

            #dC.close()

            #make some plots
            if options.Make_plots:
                self.Make_plots(self.rrv_mass_lvj,'WW',self.fitresults)
                self.Make_plots(self.rrv_mass_lvj,'WZ',self.fitresults)
            if options.verbose:             
                for i in range(len(self.fitresults)):
                    self.fitresults[i].Print()

            if options.printatgc:
                self.wtmp.var('cwww').setVal(3.6)
                self.wtmp.var('cw').setVal(4.5)
                self.wtmp.var('cb').setVal(0)
                print ('cwww and cw positive:')
                for i in range(8):
                    print N_list.at(i).GetName() + ' : ' + str(N_list.at(i).getVal())
                self.wtmp.var('cwww').setVal(3.6)
                self.wtmp.var('cw').setVal(0)
                self.wtmp.var('cb').setVal(20)
                print ('cwww and cb positive:')
                for i in range(8):
                    print (N_list.at(i).GetName() + ' : ' + str(N_list.at(i).getVal()))
                self.wtmp.var('cwww').setVal(0)
                self.wtmp.var('cw').setVal(4.5)
                self.wtmp.var('cb').setVal(20)
                print ('cw and cb positive:')
                for i in range(8):
                    print (N_list.at(i).GetName() + ' : ' + str(N_list.at(i).getVal()))

                #actual yields
                for i in range(3):
                    for j in range(3):
                        self.wtmp.var(self.POI[j]).setVal(0)
                    self.wtmp.var(self.POI[i]).setVal(self.PAR_MAX[self.POI[i]])
                    print (channel + ' ' + self.POI[i] + ' : ' + str(w.var('rate_VV').getVal()*normfactor_3d.getVal()))

                raw_input(channel)

            return combineCardName
###run code###

if __name__ == '__main__':

    if options.chan=='elmu':
        makeWS_el        = Prepare_workspace_4limit(options.year,'el')#,950,4550,options.pf)
        combineCardName_el=makeWS_el.Make_input()
        makeWS_mu        = Prepare_workspace_4limit(options.year,'mu')#,950,4550,options.pf)
        combineCardName_mu=makeWS_mu.Make_input()
        output_card_name='aC_WWWZ_simfit'
        cmd = 'combineCards.py aC_WWWZ_sig_el_{yr}_{dd}.txt aC_WWWZ_sig_mu_{yr}_{dd}.txt aC_WWWZ_sb_lo_el_{yr}_{dd}.txt aC_WWWZ_sb_lo_mu_{yr}_{dd}.txt aC_WWWZ_sb_hi_el_{yr}_{dd}.txt aC_WWWZ_sb_hi_mu_{yr}_{dd}.txt > {dC}_{yr}_{dd}.txt'.format(dC=output_card_name,yr=options.year,dd=date)
        print (cmd)
        os.system(cmd)
        os.system('mv *txt %s/'%(final_cardsdir_name))

        #combine_cards_dir="Cards/%s/"%(date)
        #combineCardName=combine_cards_dir+'/aC_WWWZ_elmu_simfit_%s.txt'%(options.year)
        #cmd='combineCards.py {mu} {el} > {elmu}'.format(mu=combineCardName_mu,el=combineCardName_el,elmu=combineCardName)
        #os.system(cmd)
        #return True 
        
    else:
        
        makeWS        = Prepare_workspace_4limit(options.year,options.chan)
        makeWS.Make_input()
    #combine the created datacards
    #output_card_name = '%s/aC_WWWZ_simfit'%self.combine_cards_dir
    #cmd = 'combineCards.py aC_WWWZ_sig_el.txt aC_WWWZ_sig_mu.txt aC_WWWZ_sb_lo_el.txt aC_WWWZ_sb_lo_mu.txt aC_WWWZ_sb_hi_el.txt aC_WWWZ_sb_hi_mu.txt > %s.txt'%output_card_name
    #cmd = 'combineCards.py Cards/2023-12-12/cards_sDM_weighted_mu_WPM_950_4550/aC_WWWZ_sig_mu.txt Cards/2023-12-12/cards_sDM_weighted_mu_WPM_950_4550/aC_WWWZ_sb_lo_mu.txt Cards/2023-12-12/cards_sDM_weighted_mu_WPM_950_4550/aC_WWWZ_sb_hi_mu.txt > %s.txt'%output_card_name
    #print cmd
    #os.system(cmd)
    #print 'generated Card : %s.txt'%output_card_name
    #print ("all done")
    
