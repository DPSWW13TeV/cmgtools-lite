from prepare_bkg_oneCat_AM import *

vetoPlots=['cwww_WW_lin','cwww_WZ_lin','cb_WZ_lin','cb_WZ_quad']

from ROOT import TH1F 


#date="2024-07-16"
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
parser.add_option('--pD',dest='plotsDir', type='string', default="/eos/user/%s/%s/www/VVsemilep/WJest"%(os.environ['USER'][0],os.environ['USER']),help='save plots here')
parser.add_option('--db', action="store",type="string",dest="DB",default="WWWZ")

(options,args) = parser.parse_args()



usepNM=False
useWts=True

def if3(cond, iftrue, iffalse):
    return iftrue if cond else iffalse




final_cardsdir_name="%s/src/CMGTools/VVsemilep/python/plotter/Cards/" %(os.environ['CMSSW_BASE']); #for future perhaps add year as sub dir 
if not os.path.isdir(final_cardsdir_name):  
    os.system("mkdir -p %s "%final_cardsdir_name)

class Prepare_workspace_4limit:

        def __init__(self,year,ch):
            
            self.POI                    = ['cwww','cw','cb']
            self.PAR_TITLES             = {'cwww' : '#frac{c_{WWW}}{#Lambda^{2}}', 'cw' : '#frac{c_{W}}{#Lambda^{2}}', 'cb' : '#frac{c_{B}}{#Lambda^{2}}'}#latex titles 
            self.PAR_MAX                = {'cwww' : 3.6, 'cw' : 4.5, 'cb' : 20}#atgc points
            self.ch                     = ch
            self.mlvj_lo                = options.mlvj_lo                #lower bound on invariant mass
            self.mlvj_hi                = options.mlvj_hi                #upper bound
            self.year                   = options.year
            self.pf                     = "_"+options.pf if len(options.pf) >0 else ""
            self.pf+= "_withSkim" if options.useSkim else ""
            self.channel                = self.ch
            self.nbins                  = (self.mlvj_hi-self.mlvj_lo)/100
            self.file_Directory         = os.path.join(self.year,trees_b)
            self.file1_Directory        = os.path.join(self.year,trees_r)
            self.WS                     = RooWorkspace("w","w_%s_%s"%(self.ch,self.year))        #final workspace
            self.wtmp                   = RooWorkspace('wtmp',"wtmp_%s_%s"%(self.ch,self.year))
            
            self.fitresults             = []
            ##nuisance parameter to change all slope parameters by certain percentage (bigger for cb in WZ-cateogry)
            self.eps                    =  RooRealVar('slope_nuis','slope_nuis',1,0,2)
            self.eps.setConstant(kTRUE)
            self.eps4cbWZ               = RooFormulaVar('rel_slope_nuis4cbWZ','rel_slope_nuis4cbWZ','1+3.0*(@0-1)',RooArgList(self.eps))
            self.eps4cbWW               = RooFormulaVar('rel_slope_nuis4cbWW','rel_slope_nuis4cbWW','1+3.0*(@0-1)',RooArgList(self.eps))
            self.PNSWP                  = {'WPL':0.64,'WPM':0.85,'WPT':0.91,'WPU':0.5,'WPD':-1}
            self.wtagger_label          = 'WPM' 
            self.PNS                    = self.PNSWP[self.wtagger_label]
            eos=os.path.join(options.plotsDir,'%s/%s_%s'%(self.year,'pNM' if usepNM else 'sDM',date))
            if not os.path.isdir(eos): os.system("mkdir -p %s"%eos)
            if os.path.exists("/afs/cern.ch"): os.system("cp /afs/cern.ch/user/a/anmehta/public/index.php %s/"%eos)
            extra_str="%s%s"%("weighted" if useWts else "unweighted",self.pf)
            self.plotsDir = os.path.join(eos,'plots_aTGC_%s_%s_%s_%s_%s' %(self.channel,self.wtagger_label,self.mlvj_lo,int(self.mlvj_hi),extra_str))
            if not os.path.isdir(self.plotsDir): 
                print "here",self.plotsDir
                os.system("mkdir  %s "%self.plotsDir)
            os.system("cp /afs/cern.ch/user/a/anmehta/public/index.php %s/" %self.plotsDir)
            os.system("cp make_PDF_input_oneCat_AM.py %s/" %self.plotsDir)
            self.rlt_DIR_name="Cards/%s/cards_%s_%s_%s_%s_%s_%s/"%(date,'pNM' if usepNM else 'sDM',extra_str,self.channel,self.wtagger_label,options.mlvj_lo,int(options.mlvj_hi))##date
            if not os.path.isdir(self.rlt_DIR_name): os.system("mkdir -p  %s "%self.rlt_DIR_name)
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
                    'WZ':[wz_atgc]}
            self.aTGCprocs=list(self.samples.keys())
            self.lumi_uncrt={'2016':[('lumi_13TeV_2016','1.022'),('lumi_13TeV_XY','1.009'),('lumi_13TeV_BBD','1.004'),('lumi_13TeV_DB','1.005'),('Lumi_13TeV_GS','1.004')],
                             '2017':[('lumi_13TeV_2017','1.020'),('lumi_13TeV_XY','1.008'),('lumi_13TeV_LS','1.003'),('lumi_13TeV_BBD','1.004'),('lumi_13TeV_DB','1.005'),('lumi_13TeV_BCC','1.003'),('lumi_13TeV_GS','1.001')],
                             '2018':[('lumi_13TeV_2018','1.015'),('lumi_13TeV_XY','1.020'),('lumi_13TeV_LS','1.002'),('lumi_13TeV_BCC','1.002')]}

        #read trees containing aTGC WW and WZ events and fill them into histograms
        ####################
        def get_pull(self, rrv_x, mplot_orig):

            #print "############### draw the pull plot ########################"
            hpull = mplot_orig.pullHist();
            x = ROOT.Double(0.); y = ROOT.Double(0) ;
            for ipoint in range(0,hpull.GetN()):
                hpull.GetPoint(ipoint,x,y);
                #hpull.SetPoint(ipoint,x,1000)
                #print x,y
                if(y == 0):
                    hpull.SetPoint(ipoint,x,10)
            tmpObjName=mplot_orig.GetName()+'_pull'
            if ROOT.gROOT.FindObject(tmpObjName) != None: ROOT.gROOT.FindObject(tmpObjName).Delete()
            self.gt = ROOT.TH1F(mplot_orig.GetName()+'_pull',mplot_orig.GetName()+'_pull',rrv_x.getBins(),rrv_x.getMin(),rrv_x.getMax());
            self.gt.SetMinimum(-3.999);        self.gt.SetMaximum(3.999);
            self.gt.SetDirectory(0);        self.gt.SetStats(0);
            self.gt.SetLineStyle(0);        self.gt.SetMarkerStyle(20);
            self.gt.GetXaxis().SetTitle(rrv_x.GetTitle() + " (GeV)");
            self.gt.GetXaxis().SetLabelFont(42);        self.gt.GetXaxis().SetLabelOffset(0.02);      self.gt.GetXaxis().SetLabelSize(0.10);
            self.gt.GetXaxis().SetTitleSize(0.11);        self.gt.GetXaxis().SetTitleOffset(1.2);     self.gt.GetXaxis().SetTitleFont(42);        self.gt.GetYaxis().SetTitle("#frac{Data-Fit}{#sigma_{Data}}");
            self.gt.GetYaxis().CenterTitle(True);        self.gt.GetYaxis().SetNdivisions(205);        self.gt.GetYaxis().SetLabelFont(42);        self.gt.GetYaxis().SetLabelOffset(0.007);
            self.gt.GetYaxis().SetLabelSize(0.10);        self.gt.GetYaxis().SetTitleSize(0.11);        self.gt.GetYaxis().SetTitleOffset(0.35);        self.gt.GetYaxis().SetTitleFont(42);
            hpull.SetHistogram(self.gt)
            return hpull

    #################################################################################################
    #################################################################################################

    #set uncertainties for data as recommended by the statistics commitee

    ################
        def legend4Plot(self, plot,isFill=1, x_offset_low=0.,y_offset_low=0.,x_offset_high =0., y_offset_high =0., TwoCoulum =1.,firstentry=''):
            #        print "############### draw the legend ########################"
            theLeg = TLegend(0.37+x_offset_low, 0.50+y_offset_low, 0.72+x_offset_high, 0.82+y_offset_high, "", "NDC");            
            #theLeg.SetName("theLegend");
            if TwoCoulum :                theLeg.SetNColumns(2);

            
            theLeg.SetFillColor(0);        theLeg.SetFillStyle(0);        theLeg.SetTextSize(0.04);        theLeg.SetTextFont(42);
            theLeg.SetBorderSize(0);        theLeg.SetLineColor(0);        theLeg.SetLineWidth(0);        theLeg.SetLineStyle(0);
            if firstentry: theLeg.AddEntry('NULL',firstentry.split('_')[-1],'');
            entryCnt = 0;
            objName_before = "";
            objName_signal_graviton = "";
            objNameLeg_signal_graviton = "";        
            legHeader="e#nu" if   self.ch == 'el' else "#mu#nu";
            for obj in range(int(plot.numItems()) ):
                objName = plot.nameOf(obj);
                #if objName.find("TPave") != -1: continue
                if objName == "errorband" : objName = "Uncertainty";
                if not ( ( (plot.getInvisible(objName)) and (not TString(objName).Contains("Uncertainty")) ) or TString(objName).Contains("invisi") or TString(objName).Contains("TLine") or 
objName ==objName_before ):
                    theObj = plot.getObject(obj);
                    objTitle = objName;
                    drawoption= plot.getDrawOptions(objName).Data()
                    if drawoption=="P":drawoption="PE"
                    if TString(objName).Contains("Uncertainty") or TString(objName).Contains("sigma"):  objName_before=objName; continue ;
                    elif TString(objName).Contains("Graph") :  objName_before=objName; continue ;
                    elif TString(objName).Contains("Uncertainty"): theLeg.AddEntry(theObj, objTitle,drawoption);  objName_before=objName;
                    elif TString(objName).Data()=="data" : theLeg.AddEntry(theObj, "Data, W#rightarrow"+legHeader,"PE");  objName_before=objName;                 
                    else: objName_before=objName; continue ;

            entryCnt = 0;
            objName_before = "";

                   
            for obj in range(int(plot.numItems()) ):
                objName = plot.nameOf(obj);
                if objName == "errorband" : objName = "Uncertainty";
                if not ( ( (plot.getInvisible(objName)) and (not TString(objName).Contains("Uncertainty")) ) or TString(objName).Contains("invisi") or TString(objName).Contains("TLine") or 
objName ==objName_before ):
                    theObj = plot.getObject(obj);
                    objTitle = objName;
                    drawoption= plot.getDrawOptions(objName).Data()
                    if drawoption=="P":drawoption="PE"
                    if TString(objName).Contains("Uncertainty") or TString(objName).Contains("sigma"):  objName_before=objName; continue ;
                    elif TString(objName).Contains("Graph") :  objName_before=objName; continue ;
                    elif TString(objName).Data()=="WJets" : objName_before=objName;                 
                    else:  objName_before=objName; continue ;

            entryCnt = 0;
            objName_before = "";
            for obj in range(int(plot.numItems()) ):
                objName = plot.nameOf(obj);
                if objName.find("TPave") != -1: continue
                if objName == "errorband" : objName = "Uncertainty";
                if not ( ( (plot.getInvisible(objName)) and (not TString(objName).Contains("Uncertainty")) ) or TString(objName).Contains("invisi") or TString(objName).Contains("TLine") or 
objName ==objName_before ):
                    theObj = plot.getObject(obj);
                    objTitle = objName;
                    drawoption= plot.getDrawOptions(objName).Data()
                    if drawoption=="P":drawoption="PE"
                    if TString(objName).Contains("Uncertainty") or TString(objName).Contains("sigma"):
                        theLeg.AddEntry(theObj, objName,"F");
                    elif TString(objName).Contains("Graph") :
                        if not (objName_before=="Graph" or objName_before=="Uncertainty"): theLeg.AddEntry(theObj, "Uncertainty","F");
                    else:
                        if TString(objName).Data()=="STop" : theLeg.AddEntry(theObj, "Single top","F");
                        #elif TString(objName).Contains("Uncertainty"): theLeg.AddEntry(theObj, objTitle,drawoption);
                        elif TString(objName).Data()=="TTbar" : theLeg.AddEntry(theObj, "t#bar{t}","F");
                        elif TString(objName).Data()=="VV" : theLeg.AddEntry(theObj, "WW/WZ","F");
                        elif TString(objName).Data()=="data" :  objName_before=objName; entryCnt = entryCnt+1; continue ;
                        elif TString(objName).Data()=="WJets" : theLeg.AddEntry(theObj, "W+jets","F"); entryCnt = entryCnt+1; continue;
                        elif TString(objName).Contains("vbfH"): theLeg.AddEntry(theObj, (TString(objName).ReplaceAll("vbfH","qqH")).Data() ,"L");
                        else : theLeg.AddEntry(theObj, objTitle,drawoption);
                    entryCnt=entryCnt+1;
                    objName_before=objName;

            return theLeg;
##########################
        def Read_ATGCtree(self,ch='mu',procs=['WW','WZ']):
            print ('######### Making histograms for aTGC working points #########')
            hists4scale        = {}
            for WV in self.aTGCprocs: #['WW','WZ']:
                #create 3 histograms for each aTGC parameter (positive, negative and positive-negative working point)
                for para in self.POI:
                    hists4scale['c_pos_%s_hist_%s'%(WV,para)] = TH1F('c_pos_%s_hist_%s'%(WV,para),'c_pos_%s_hist_%s'%(WV,para),self.nbins,self.mlvj_lo,self.mlvj_hi);
                    hists4scale['c_neg_%s_hist_%s'%(WV,para)] = TH1F('c_neg_%s_hist_%s'%(WV,para),'c_neg_%s_hist_%s'%(WV,para),self.nbins,self.mlvj_lo,self.mlvj_hi);
                    hists4scale['c_sm_lin_quad_%s_hist_%s'%(WV,para)] = TH1F('c_sm_lin_quad_%s_hist_%s'%(WV,para),'c_sm_lin_quad_%s_hist_%s'%(WV,para),self.nbins,self.mlvj_lo,self.mlvj_hi);
                    hists4scale['c_pos_%s_hist_%s'%(WV,para)].Sumw2(kTRUE); hists4scale['c_neg_%s_hist_%s'%(WV,para)].Sumw2(kTRUE);hists4scale['c_sm_lin_quad_%s_hist_%s'%(WV,para)].Sumw2(kTRUE)
                    hists4scale['c_quad_%s_hist_%s'%(WV,para)]=TH1F('c_quad_%s_hist_%s'%(WV,para),'c_quad_%s_hist_%s'%(WV,para),self.nbins,self.mlvj_lo,self.mlvj_hi); hists4scale['c_quad_%s_hist_%s'%(WV,para)].Sumw2(kTRUE)

                #add histograms for SM and all aTGC parameters unequal to zero
                hists4scale['c_sm_%s_hist'%WV]                  = TH1F('c_sm_%s_hist'%WV,'c_sm_%s_hist'%WV,self.nbins,self.mlvj_lo,self.mlvj_hi);                


                #print 'reading for %s sample in  %s channel'%(WV,self.ch)
                treeIn  = ROOT.TChain('Friends');                treeIn1 = ROOT.TChain('Friends')                
                for i in self.samples[WV][0]:
                    fileIn_name = str(options.inPath+"/"+self.file_Directory+"/"+i+"_Friend.root");
                    treeIn.Add(fileIn_name)
                    fileIn1_name = str(options.inPath+"/"+self.file1_Directory+"/"+i+"_Friend.root");
                    treeIn1.Add(fileIn1_name)
                treeIn.AddFriend(treeIn1)
                lumi_tmp         = lumis[self.year]
                ##tree.Draw('{here}>>hist1'.format(here=vname), selcuts, 'goff');hist1.SetDirectory(0)
                sel_boosted='dR_fjlep > 1.6 && dphi_fjlep > 2.0 && dphi_fjmet > 2.0 && pTWlep > 200 && Selak8Jet1_pNetWtagscore  > {WP} && {mass_var} > {m_l} && {mass_var} < {m_h} && mWV >{mwv}'.format(mass_var="Selak8Jet1_particleNet_mass" if usepNM else "Selak8Jet1_msoftdrop",WP=self.PNS,m_l=45,m_h=150,mwv=self.mlvj_lo)
                sel_lep=" ( Lep1_pt > 50 && nLepTight == 1 && nLepFO==1 && Lep1_tightId == 1 && ((abs(Lep1_pdgId) == 13 or (abs(Lep1_eta) < 1.442 or abs(Lep1_eta) > 1.556 )))"
                flav_lep="(abs(Lep1_pdgId) == {pdg} && {trig})".format(trig="trigger1m" if self.ch == "mu" else "trigger1e",pdg=13  if self.ch == "mu" else 11) 
                for i in range(treeIn.GetEntries()):
                    if i%500000==0:                            print (str(i) + '/' + str(treeIn.GetEntries()))
                    treeIn.GetEntry(i)
                    MWW                = treeIn.mWV
                    tmp_jet_mass=treeIn.Selak8Jet1_particleNet_mass if usepNM else treeIn.Selak8Jet1_msoftdrop
                    tmp_jet_pNetscore=treeIn.Selak8Jet1_pNetWtagscore
                    dRfjlep=treeIn.dR_fjlep > 1.6; dphifjlep=treeIn.dphi_fjlep > 2.0 ; dphifjmet=treeIn.dphi_fjmet > 2.0; ptWlep=treeIn.pTWlep > 200;
                    boosted_sel=False;                    lep_sel=False;
                    lep_sel= treeIn.Lep1_pt > 50  and treeIn.nLepTight == 1 and treeIn.nLepFO==1 and treeIn.Lep1_tightId == 1 and ( (abs(treeIn.Lep1_pdgId) == 13 or (abs(treeIn.Lep1_eta) < 1.442 or abs(treeIn.Lep1_eta) > 1.556 )) );
                    boosted_sel=dRfjlep and dphifjlep and dphifjmet and ptWlep and tmp_jet_pNetscore > self.PNS and tmp_jet_mass < 150 and tmp_jet_mass > 45 and MWW > self.mlvj_lo
                    lep_flav= (abs(treeIn.Lep1_pdgId) == 13 and treeIn.trigger1m) if self.ch == "mu" else (abs(treeIn.Lep1_pdgId) == 11 and treeIn.trigger1e )
                    if lep_flav and  boosted_sel and lep_sel:
			weight_part =1000*treeIn.xsec*treeIn.genwt*treeIn.evt_wt*treeIn.lepSF*treeIn.Selak8Jet1_pNetWtagSF*lumis[self.year]/treeIn.sumw 
			aTGC        = treeIn.aGC_wt 
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
			hists4scale['c_sm_lin_quad_%s_hist_cw'%WV].Fill(MWW,0.5*(aTGC[72]-aTGC[52]) * weight_part/4.5)
			#cb-SM interference
			hists4scale['c_sm_lin_quad_%s_hist_cb'%WV].Fill(MWW,0.5*(aTGC[64]-aTGC[60]) * weight_part/20)
			hists4scale['c_sm_lin_quad_%s_hist_cwww'%WV].Fill(MWW,0.5*(aTGC[112]-aTGC[12]) * weight_part/3.6)
                        hists4scale['c_quad_%s_hist_cb'%WV].Fill(MWW,0.5*(aTGC[64]+aTGC[60]-2*aTGC[62]) * weight_part/20**2)
                        hists4scale['c_quad_%s_hist_cw'%WV].Fill(MWW,0.5*(aTGC[72]+aTGC[52]-2*aTGC[62]) * weight_part/4.5**2)
                        hists4scale['c_quad_%s_hist_cwww'%WV].Fill(MWW,0.5*(aTGC[112]+aTGC[12]-2*aTGC[62]) * weight_part/3.6**2)


                N_sm_lin_quad_cb    = RooRealVar('N_sm_lin_quad_cb_%s'%WV,'N_sm_lin_quad_cb_%s'%WV,hists4scale['c_sm_lin_quad_%s_hist_cb'%WV].Integral())
                N_sm_lin_quad_cwww  = RooRealVar('N_sm_lin_quad_cwww_%s'%WV,'N_sm_lin_quad_cwww_%s'%WV,hists4scale['c_sm_lin_quad_%s_hist_cwww'%WV].Integral())
                N_sm_lin_quad_cw    = RooRealVar('N_sm_lin_quad_cw_%s'%WV,'N_sm_lin_quad_cw_%s'%WV,hists4scale['c_sm_lin_quad_%s_hist_cw'%WV].Integral())
                N_quad_cb           = RooRealVar('N_quad_cb_%s'%WV,'N_quad_cb_%s'%WV,hists4scale['c_quad_%s_hist_cb'%WV].Integral())
                N_quad_cwww         = RooRealVar('N_quad_cwww_%s'%WV,'N_quad_cwww_%s'%WV,hists4scale['c_quad_%s_hist_cwww'%WV].Integral())
                N_quad_cw           = RooRealVar('N_quad_cw_%s'%WV,'N_quad_cw_%s'%WV,hists4scale['c_quad_%s_hist_cw'%WV].Integral())

		self.Import_to_ws(self.wtmp, [N_sm_lin_quad_cb,N_sm_lin_quad_cwww,N_sm_lin_quad_cw,N_quad_cb,N_quad_cwww,N_quad_cw])
            #write histograms to file
            fileOut        = TFile.Open(self.rlt_DIR_name+'/hists4scale_%s_WV_aTGC-%s_%s.root'%(self.ch,self.mlvj_lo,self.mlvj_hi),'recreate')
            for key in hists4scale:
                hists4scale[key].Write()
            print ('--------> Written to file ' + fileOut.GetName())
            fileOut.Close()
        def drawSLatex(self,xpos,ypos,text,size):
            latex = ROOT.TLatex()
            latex.SetNDC()
            latex.SetTextAlign(12)
            latex.SetTextSize(size)
            latex.SetTextFont(42)
            latex.DrawLatex(xpos,ypos,text)
            return latex
        def get_canvas(self,cname):
            CMS_lumi.lumi_13TeV = "%s fb^{-1}" %str(lumis[self.year])
            CMS_lumi.writeExtraText = True
            CMS_lumi.extraText = "Preliminary"
            iPos = 11
            if( iPos==0 ): CMS_lumi.relPosX = 0.15
            H_ref = 600;        W_ref = 600;        W = W_ref;       H  = H_ref
            T = 0.12*H_ref;       B = 0.12*H_ref;       L = 0.12*W_ref;       R = 0.01*W_ref
            canvas = ROOT.TCanvas(cname,"",W,H)
            canvas.SetFillColor(0);       canvas.SetBorderMode(0);
            canvas.SetFrameFillStyle(0);       canvas.SetFrameBorderMode(0);      canvas.SetLeftMargin(0.15);# L/W );
            canvas.SetRightMargin(0.1);# R/W );
            #canvas.SetTopMargin(T/H);
            canvas.SetBottomMargin(0.1);#B/H);
            canvas.SetTickx();       canvas.SetTicky();
            return canvas

        
        def Make_plots(self,rrv_x,cat,fitres):
            can     = [];can2    = [];      plots   = [];     plots2  = []; pads    = []; dummy_list=[]
            channel = self.ch+'_'+cat
            for i in range(3):
                rrv_x.setRange(self.mlvj_lo,self.mlvj_hi)
                p       = rrv_x.frame(self.mlvj_lo,self.mlvj_hi)
                p2      = rrv_x.frame(self.mlvj_lo,self.mlvj_hi)
                c       = self.get_canvas(cat+'_'+self.POI[i]+'-');#TCanvas(cat+'_'+self.POI[i]+'-',self.POI[i]+'-',600,600)
                c.Draw();                c.cd();
                pad1        = TPad(cat+'pad1_%s'%self.POI[i],cat+'pad1_%s'%self.POI[i],0.,0.3,1.,1.)  
                pad2        = TPad(cat+'pad2_%s'%self.POI[i],cat+'pad2_%s'%self.POI[i],0.,0.02,1.,0.3)
                c2          = TCanvas(cat+self.POI[i]+'+',self.POI[i]+'+',600,600)
                c2.cd()
                pad3        = TPad(cat+'pad3_%s'%self.POI[i],cat+'pad3_%s'%self.POI[i],0.,0.3,1.,1.)
                pad4        = TPad(cat+'pad4_%s'%self.POI[i],cat+'pad4_%s'%self.POI[i],0.,0.02,1.,0.3)
                p2pads      = [pad1,pad2,pad3,pad4]
                can.append(c); can2.append(c2);  plots.append(p);        plots2.append(p2);                pads.append(p2pads)
                dummy_list.append(can);dummy_list.append(can2),dummy_list.append(plots);dummy_list.append(plots2);dummy_list.append(pads);
            for i in range(3):
                can[i].cd();
                #CMS_lumi.CMS_lumi(pads[i][0], 4, 11,0.075);
                pads[i][0].Update()
                pads[i][0].Draw();                pads[i][1].Draw()
                pads[i][0].SetLeftMargin(0.1);    pads[i][1].SetLeftMargin(0.1)


                for j in range(3):
                    self.wtmp.var(self.POI[j]).setVal(0)

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


                plotmax        = 1e4; plotmin = 1e-4
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
                plots[i].addObject(txt)
                plots[i].Draw()
                ndof        = (self.mlvj_hi-self.mlvj_lo)/100 - 4
                #plots[i].Print()
                parlatex        = ['#frac{c_{WWW}}{#Lambda^{2}}','#frac{c_{W}}{#Lambda^{2}}','#frac{c_{B}}{#Lambda^{2}}']
                leg        = TLegend(0.15,0.675,0.875,0.85)
                leg.SetFillStyle(0);leg.SetTextFont(42);                leg.SetBorderSize(0);leg.SetNColumns(2);
                leg.SetFillStyle(0); leg.SetTextSize(0.035);
                if quadStr not in vetoPlots:  
                    leg.AddEntry(plots[i].findObject('quadData'),'quad. MC '+parlatex[i]+'= 1 TeV^{#minus2}','le')
                    leg.AddEntry(plots[i].findObject('quadModel'),'quad. model '+parlatex[i]+'= 1 TeV^{#minus2}','l')
                if linStr not in vetoPlots:
                    leg.AddEntry(plots[i].findObject('linData'),'lin. MC '+parlatex[i]+'= 1 TeV^{#minus2}','le')
                    leg.AddEntry(plots[i].findObject('linModel'),'lin. model '+parlatex[i]+'= 1 TeV^{#minus2}','l')

                leg.Draw()
                #leg.Print()

                pads[i][1].cd();                pads[i][1].SetTopMargin(0.03);  pads[i][1].SetBottomMargin(0.3)##HERE
                if ROOT.gROOT.FindObject("dummy") != None: ROOT.gROOT.FindObject("dummy").Delete()
                ratio_style = ROOT.TH1D('dummy','dummy',(self.mlvj_hi-self.mlvj_lo)/100,self.mlvj_lo,self.mlvj_hi)
                ratio_style.SetMarkerStyle(21)
                ratio_style.SetLineColor(kBlack);ratio_style.SetLineWidth(1);
                ratio_style.SetMaximum(3)
                ratio_style.SetMinimum(-3)
                ratio_style.GetYaxis().SetNdivisions(7)
                ratio_style.GetYaxis().SetTitle('#frac{MC-Fit}{error}')
                ratio_style.GetYaxis().SetLabelSize(0.095)
                ratio_style.GetYaxis().SetTitleSize(0.1)
                ratio_style.GetYaxis().SetTitleOffset(0.425)
                ratio_style.GetXaxis().SetLabelSize(0.095)
                ratio_style.GetXaxis().SetTitleSize(0.1)
                ratio_style.GetXaxis().SetTitle("m_{WV} (GeV)");
                ratio_style.Draw("")
                if (pullhist_q) is not None: 
                    pullhist_q.Draw("SAME P0E1");  
                    pullhist_q.SetLineColor(ROOT.kPink-2);pullhist_q.SetLineWidth(1);pullhist_q.SetMarkerStyle(26);  pullhist_q.SetMarkerColor(ROOT.kPink-2);
                if (pullhist_l) is not None: 
                    pullhist_l.SetLineColor(ROOT.kAzure+10);pullhist_l.SetLineWidth(1);pullhist_l.SetMarkerStyle(25); pullhist_l.SetMarkerColor(ROOT.kAzure+10);
                    pullhist_l.Draw("SAME P0E1")
                    #pullhist_l1.SetLineColor(8);pullhist_l1.SetLineWidth(1);pullhist_l1.SetMarkerStyle(27); pullhist_l1.SetMarkerColor(8);
                    #pullhist_l1.Draw("SAME P0E1")

                can[i].Update()
                can[i].SaveAs(self.plotsDir+'/%s_neg_%s.pdf'%(self.POI[i],channel))
                can[i].SaveAs(self.plotsDir+'/%s_neg_%s.png'%(self.POI[i],channel))
                dummy_list.append(can[i]);dummy_list.append(pullhist_l);dummy_list.append(pullhist_q);

            #    return True 
                
        #function to import multiple items from a list into a workspace
        def Import_to_ws(self,workspace,items,recycle=0):
            for item in items:
                if recycle:
                    getattr(workspace,'import')(item,RooFit.RecycleConflictNodes())
                else:
                    getattr(workspace,'import')(item)
            #return True 

        def Make_signal_pdf(self,rrv_x,sample):
            channel        = self.ch+'_'+sample                #needed for variables that differ for WW and WZ
            cwww     = RooRealVar('cwww','cwww',0,-1,1);#-36,36);
            cw       = RooRealVar('cw','cw',0,-1,1);#-45,45);
            cb       = RooRealVar('cb','cb',0,-1,1);#-200,200);
            cwww.setConstant(kTRUE);
            cw.setConstant(kTRUE);
            cb.setConstant(kTRUE);
   
            #get SM and other histograms and make RooDataHists
            fileInHist      = TFile.Open(self.rlt_DIR_name+'/hists4scale_%s_WV_aTGC-%s_%s.root'%(self.ch,self.mlvj_lo,self.mlvj_hi))
            rrv_x.setRange(self.mlvj_lo,self.mlvj_hi)
            SMdatahist                  = RooDataHist('SMdatahist_%s'     %sample,'SMdatahist_%s'     %sample,RooArgList(rrv_x),fileInHist.Get('c_sm_%s_hist'%sample))
            SM                          = RooDataHist('SM%s_4scale'%sample,'SM%s_4scale'%sample,RooArgList(rrv_x),fileInHist.Get('c_sm_%s_hist'%sample))
            sm_lin_quad_cb_DataHist     = RooDataHist('sm_lin_quad_cb_DataHist_%s'   %sample,'sm_lin_quad_cb_DataHist_%s'   %sample,RooArgList(rrv_x),fileInHist.Get('c_sm_lin_quad_%s_hist_cb'  %sample))
            sm_lin_quad_cw_DataHist     = RooDataHist('sm_lin_quad_cw_DataHist_%s'   %sample,'sm_lin_quad_cw_DataHist_%s'   %sample,RooArgList(rrv_x),fileInHist.Get('c_sm_lin_quad_%s_hist_cw'  %sample))
            sm_lin_quad_cwww_DataHist   = RooDataHist('sm_lin_quad_cwww_DataHist_%s' %sample,'sm_lin_quad_cwww_DataHist_%s' %sample,RooArgList(rrv_x),fileInHist.Get('c_sm_lin_quad_%s_hist_cwww'%sample))
            quad_cb_DataHist            = RooDataHist('quad_cb_DataHist_%s'          %sample,'quad_cb_DataHist_%s'          %sample,RooArgList(rrv_x),fileInHist.Get('c_quad_%s_hist_cb'  %sample))
            quad_cw_DataHist            = RooDataHist('quad_cw_DataHist_%s'          %sample,'quad_cw_DataHist_%s'          %sample,RooArgList(rrv_x),fileInHist.Get('c_quad_%s_hist_cw'  %sample))
            quad_cwww_DataHist          = RooDataHist('quad_cwww_DataHist_%s'        %sample,'quad_cwww_DataHist_%s'        %sample,RooArgList(rrv_x),fileInHist.Get('c_quad_%s_hist_cwww'%sample))

            #make SM pdf, simple exponential
            a1_4fit         = RooRealVar('a_SM_4fit_%s'%channel,'a_SM_4fit_%s'%channel,-0.005,-0.25,0) ##AM
            a1              = RooFormulaVar('a_SM_%s'%channel,'a_SM_%s'%channel,'@0*@1',RooArgList(a1_4fit,self.eps))
            SMPdf           = RooExponential('SMPdf_%s'%channel,'SMPdf_%s'%channel,rrv_x,a1)
            ##actual fit to determine SM shape parameter a1_4fit
            print "fitting the SM part"
            fitresSM        = SMPdf.fitTo(SMdatahist, RooFit.SumW2Error(kTRUE), RooFit.Save(kTRUE))
            c3_AM=ROOT.TCanvas('can_am_%s'%(channel),'',600,600); #c3_AM.SetLogy();
            mplot_tmp_am = rrv_x.frame( RooFit.Bins(rrv_x.getBins()));
            SMdatahist.plotOn( mplot_tmp_am,RooFit.Name("sm"),RooFit.MarkerSize(1), RooFit.DataError(RooAbsData.Poisson), RooFit.XErrorSize(0), RooFit.MarkerColor(1), RooFit.LineColor(1) );
            SMPdf.plotOn(mplot_tmp_am, RooFit.Name("smpdf"),RooFit.LineStyle(kDashDotted),RooFit.LineColor(ROOT.kOrange));
            self.leg_tmp_AM= self.legend4Plot(mplot_tmp_am,0, 0, 0., 0., -0.1,0,channel);
            mplot_tmp_am.addObject(self.leg_tmp_AM);
            mplot_tmp_am.Draw();        c3_AM.Update();        c3_AM.Draw();
            c3_AM.SaveAs(self.plotsDir+'/sm_%s.png'%(channel))
            c3_AM.SaveAs(self.plotsDir+'/sm_%s.pdf'%(channel))            
            self.fitresults.append(fitresSM)
            a1_4fit.setConstant(kTRUE)

            #coefficient for SM term and other terms in final signal function
            N_SM                 = RooRealVar('N_SM_%s'%channel,'N_SM_%s'%channel,SMdatahist.sumEntries())
            N_sm_lin_quad_cb     = RooRealVar('N_sm_lin_quad_cb%s'  %channel,'N_sm_lin_quad_cb%s'%channel,sm_lin_quad_cb_DataHist.sumEntries())
            N_sm_lin_quad_cw     = RooRealVar('N_sm_lin_quad_cw%s'  %channel,'N_sm_lin_quad_cw%s'%channel,sm_lin_quad_cw_DataHist.sumEntries())
            N_sm_lin_quad_cwww   = RooRealVar('N_sm_lin_quad_cwww%s'%channel,'N_sm_lin_quad_cwww%s'%channel,sm_lin_quad_cwww_DataHist.sumEntries())
            N_quad_cb            = RooRealVar('N_quad_cb%s'  %channel,'N_quad_cb%s'%channel,  quad_cb_DataHist.sumEntries())
            N_quad_cw            = RooRealVar('N_quad_cw%s'  %channel,'N_quad_cw%s'%channel,  quad_cw_DataHist.sumEntries())
            N_quad_cwww          = RooRealVar('N_quad_cwww%s'%channel,'N_quad_cwww%s'%channel,quad_cwww_DataHist.sumEntries())
            print "checkpoint 1"
            self.Import_to_ws(self.wtmp,[cwww,cw,cb,self.eps4cbWZ,self.eps4cbWW,SMdatahist,SMdatahist,N_SM,N_sm_lin_quad_cb,N_sm_lin_quad_cw,N_sm_lin_quad_cwww,N_quad_cb,N_quad_cw,N_quad_cwww]) 
            #define parameter ranges for error function
            print "checkpoint 2"
            Erf_width_cwww      = RooRealVar('Erf_width_cwww_%s'%channel,'Erf_width_cwww_%s'%channel,500.,0.,2500.)
            Erf_width_cw        = RooRealVar('Erf_width_cw_%s'%channel,'Erf_width_cw_%s'%channel,1000.,500.,2500.)
            Erf_width_cb        = RooRealVar('Erf_width_cb_%s'%channel,'Erf_width_cb_%s'%channel,500.,0.,2500.)
            Erf_offset_cwww         = RooRealVar('Erf_offset_cwww_%s'%channel,'Erf_offset_cwww_%s'%channel,500.,0.,2500.)
            Erf_offset_cw           = RooRealVar('Erf_offset_cw_%s'%channel,'Erf_offset_cw_%s'%channel,500.,0.,1500.)
            Erf_offset_cb           = RooRealVar('Erf_offset_cb_%s'%channel,'Erf_offset_cb_%s'%channel,500.,0.,2500.)
            self.Import_to_ws(self.wtmp,[Erf_width_cwww,Erf_offset_cwww,Erf_width_cw,Erf_offset_cw,Erf_offset_cb,Erf_width_cb])                
            print "checkpoint 3"
            #fileInHist    = TFile.Open(self.rlt_DIR_name+'/hists4scale_%s_WV_aTGC-%s_%s.root'%(self.ch,self.mlvj_lo,self.mlvj_hi))
            for i in range(len(self.POI)):
                s_name        = self.POI[i] + '_' + channel #added to parameter names
                rrv_x.setRange(self.mlvj_lo,self.mlvj_hi)                
                pos_datahist  = RooDataHist('pos_datahist_%s_%s'%(sample,self.POI[i]),'pos_datahist_%s_%s'%(sample,self.POI[i]),RooArgList(rrv_x),fileInHist.Get('c_pos_%s_hist_%s'%(sample,self.POI[i])))
                neg_datahist  = RooDataHist('neg_datahist_%s_%s'%(sample,self.POI[i]),'neg_datahist_%s_%s'%(sample,self.POI[i]),RooArgList(rrv_x),fileInHist.Get('c_neg_%s_hist_%s'%(sample,self.POI[i])))
                sm_lin_quad_datahist = RooDataHist('sm_lin_quad_datahist_%s_%s'%(sample,self.POI[i]),'sm_lin_quad_datahist_%s_%s'%(sample,self.POI[i]),RooArgList(rrv_x),fileInHist.Get('c_sm_lin_quad_%s_hist_%s'%(sample,self.POI[i])))
                quad_datahist =RooDataHist('quad_datahist_%s_%s'%(sample,self.POI[i]),'quad_datahist_%s_%s'%(sample,self.POI[i]),RooArgList(rrv_x),fileInHist.Get('c_quad_%s_hist_%s'%(sample,self.POI[i])))

                #import datasets to wtmp and final workspace WS
                self.Import_to_ws(self.wtmp,[pos_datahist,neg_datahist,sm_lin_quad_datahist,quad_datahist],RooFit.RecycleConflictNodes())
                self.Import_to_ws(self.WS,[pos_datahist,neg_datahist,sm_lin_quad_datahist,quad_datahist],RooFit.RecycleConflictNodes())
                N_pos_tmp   = pos_datahist.sumEntries()
                N_neg_tmp   = neg_datahist.sumEntries()
                factor     = if3(self.POI[i] == "cwww",3.6, if3(self.POI[i] == "cb",20,4.5))
                norm_lin   = RooRealVar('norm_sm_lin_quad_%s'%s_name,'norm_sm_lin_quad_%s'%s_name,0.5*(N_pos_tmp-N_neg_tmp)/SM.sumEntries()/factor)
                norm_quad  = RooRealVar('norm_quad_%s'%s_name,'norm_quad_%s'%s_name,(0.5*(N_pos_tmp+N_neg_tmp)-SM.sumEntries())/SM.sumEntries()/factor**2 )
                a2_4fit     = RooRealVar('a_quad_4fit_%s'%s_name,'a_quad_4fit_%s'%s_name,-0.00012,-0.01,0.1) #-0.000173527 for cb #-0.0012 to 0.1
                a2          = RooFormulaVar('a_quad_nuis_%s'%s_name,'a_quad_nuis_%s'%s_name,'@0*@1',RooArgList(a2_4fit,self.eps4cbWZ if sample=='WZ' else self.eps4cbWW))
                cPdf_quad   = RooErfExpPdf('%s_quad_%s_%s'%(sample,self.POI[i],self.ch),'%s_quad_%s_%s'%(sample,self.POI[i],self.ch),rrv_x,a2,self.wtmp.var('Erf_offset_%s'%s_name),self.wtmp.var('Erf_width_%s'%s_name))

                a5_lin    = RooRealVar("a5_lin_%s"%s_name,"a5_lin_%s"%s_name,-2e-4,-1e-1,0.1);
                a4_lin    = RooRealVar("a4_lin_%s"%s_name,"a4_lin%s"%s_name,0, -20000, 20000);
                cPdf_lin  = ROOT.RooExpNPdf('%s_sm_lin_quad_%s_%s'%(sample,self.POI[i],self.ch),'%s_sm_lin_quad_%s_%s'%(sample,self.POI[i],self.ch),rrv_x,a5_lin, a4_lin);
                linStr=self.POI[i]+'_'+sample+'_lin'
                quadStr=self.POI[i]+'_'+sample+'_quad'
                if quadStr not in vetoPlots:
                    print "fitting quad term ----------------------------------------********************************$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$"
                    print "check this out for %s"%s_name,cPdf_quad.Print();
                    fitres_quad  = cPdf_quad.fitTo(self.wtmp.data('quad_datahist_%s_%s'%(sample,self.POI[i])),RooFit.Save(kTRUE), RooFit.SumW2Error(kTRUE))
                    fitres_quad  = cPdf_quad.fitTo(self.wtmp.data('quad_datahist_%s_%s'%(sample,self.POI[i])),RooFit.Save(kTRUE), RooFit.SumW2Error(kTRUE), RooFit.Minimizer('Minuit2'))
                    self.fitresults.append(fitres_quad)
                    
                if linStr not in vetoPlots:
                    print "fitting linear term ----------------------------------------********************************$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$"
                    fitres_lin   = cPdf_lin.fitTo(self.wtmp.data('sm_lin_quad_datahist_%s_%s'%(sample,self.POI[i])),RooFit.Save(kTRUE), RooFit.SumW2Error(kTRUE))
                    fitres_lin   = cPdf_lin.fitTo(self.wtmp.data('sm_lin_quad_datahist_%s_%s'%(sample,self.POI[i])),RooFit.Save(kTRUE), RooFit.SumW2Error(kTRUE), RooFit.Minimizer('Minuit2'))
                    self.fitresults.append(fitres_lin) 

                a2_4fit.setConstant(kTRUE)
                #a3_4fit.setConstant(kTRUE)
                Erf_offset_cwww.setConstant(kTRUE);Erf_width_cwww.setConstant(kTRUE);
                Erf_offset_cw.setConstant(kTRUE);Erf_width_cw.setConstant(kTRUE);       
                Erf_offset_cb.setConstant(kTRUE);            Erf_width_cb.setConstant(kTRUE)
                a4_lin.setConstant(kTRUE); a5_lin.setConstant(kTRUE)
                self.Import_to_ws(self.wtmp,[Erf_width_cwww,Erf_offset_cwww,Erf_width_cw,Erf_offset_cw,Erf_offset_cb,Erf_width_cb,a4_lin,a5_lin])                
                #PDF for SM interference
                self.Import_to_ws(self.wtmp,[cPdf_quad,cPdf_lin],1)
                self.Import_to_ws(self.wtmp,[norm_lin,norm_quad])
            for i in range(3):
                self.wtmp.var(self.POI[i]).setVal(0)
            for i in range(3):
                self.wtmp.var(self.POI[i]).setVal(self.PAR_MAX[self.POI[i]])
            fileInHist.Close()
            #return True 
            print ("done with this")

        def Write_datacard(self,w,region):
            ### make the card for this channel and plane ID
            dirName = os.path.join("../WJets_est",self.rlt_DIR_name)#"since we move everyhting one dir up"
            pbkgs  = ['WJets','TTbar','STop']
            dbbkgs = ['WW_sm','WZ_sm']
            terms  = ['_sm_lin_quad_','_quad_']
            moreprocs=[p+q for p in self.aTGCprocs for q in terms]               
            EFTprocs=[p+q for p in moreprocs for q in self.POI]
            veto=['WZ_sm_lin_quad_cb','WZ_quad_cb','WW_sm_lin_quad_cwww','WZ_sm_lin_quad_cwww']
            EFTprocs=[p for p in EFTprocs if p not in veto]
            allprocs=EFTprocs+pbkgs+dbbkgs
            binname = '{region}_{ch}'.format(ch=self.ch,region=region)
            codename='WWWZ_{region}_{ch}_{year}'.format(ch=self.ch,region=region,year=self.year)
            cardName_test='aC_%s_%s.txt'%(codename,date)
            #            print ("this is where i am saving the datacard",cardName_test)
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
rrv_c_Exp_WJets0_sb_{ch}  flatParam
Deco_WJets0_sim_{ch}_WPM_mlvj_13TeV_eig0 param 0.0 1.8
Deco_WJets0_sim_{ch}_WPM_mlvj_13TeV_eig1 param 0.0 1.8
Deco_TTbar_sb_{ch}_WPM_mlvj_13TeV_eig0 param 0.0 2.0
Deco_TTbar_sb_{ch}_WPM_mlvj_13TeV_eig1 param 0.0 2.0
Deco_TTbar_sig_{ch}_WPM_mlvj_13TeV_eig0 param 0.0 2.0
Deco_TTbar_sig_{ch}_WPM_mlvj_13TeV_eig1 param 0.0 2.0
rrv_c_ChiSq_WJets0_{ch}  flatParam
rrv_shift_ChiSq_WJets0_{ch}  flatParam
slope_nuis    param  1.0 0.05'''.format(ch=self.ch)
                       )    
            datacard.close()
            return cardName_test
#rrv_c_ExpN_WJets0_sb_{ch}  flatParam
#rrv_n_ExpN_WJets0_sb_{ch}  flatParam


#Deco_WJets0_sim_{ch}_HPV_mlvj_13TeV_eig2 param 0.0 1.4
#Deco_WJets0_sim_{ch}_HPV_mlvj_13TeV_eig3 param 0.0 1.4


        ########################
        ######MAIN CODE#########
        ########################

        def Make_input(self):

            #prepare variables, parameters and temporary workspace
            self.Read_ATGCtree(self.ch,self.aTGCprocs)
            #make and fit signal pdf for WW and WZ
            for i in self.aTGCprocs:
                self.Make_signal_pdf(self.rrv_mass_lvj,i)
            #            self.Make_signal_pdf(self.rrv_mass_lvj,'WZ')

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

                for VV in self.aTGCprocs: #['WW','WZ']:
                    ##AM HERE define the normalizations for linear and quadratic terms
                    ##AMMpdf_atgc_mlvj_VV        = self.WS2.pdf('aTGC_model_%s_%s'%(self.ch,VV))
                    pdf_atgc_mj_VV          = w_bkg.pdf('%s_mj_%s_%s'%(VV,region,self.ch))
                    norm_VV_reg             = self.WS2.function("%s_norm"%VV).Clone("%s_norm_%s_%s"%(VV,region,self.ch))

                    for ops in ['cwww','cw','cb']:
                        pdf_sm_lin_quad_mlvj_VV = self.wtmp.pdf('%s_sm_lin_quad_%s_%s'%(VV,ops,self.ch)) ##AMNewPdf_lin
                        pdf_quad_mlvj_VV        = self.wtmp.pdf('%s_quad_%s_%s'%(VV,ops,self.ch)) ##AMNewPdf_quad
                        print "defined pdfs",ops,VV,region,self.ch,pdf_sm_lin_quad_mlvj_VV.Print();
                        pdf_sm_lin_quad_VV_2d  = RooProdPdf('%s_sm_lin_quad_%s_%s_%s'%(VV,ops,region,self.ch),'%s_sm_lin_quad_%s_%s_%s'%(VV,ops,region,self.ch),RooArgList(pdf_sm_lin_quad_mlvj_VV,pdf_atgc_mj_VV))


                        print "moving on with the quad pdf",VV,region,self.ch
                        pdf_quad_VV_2d     = RooProdPdf('%s_quad_%s_%s_%s'%(VV,ops,region,self.ch),'%s_quad_%s_%s_%s'%(VV,ops,region,self.ch),RooArgList(pdf_quad_mlvj_VV,pdf_atgc_mj_VV))
                        signal_lin_norm_VV = RooFormulaVar(pdf_sm_lin_quad_VV_2d.GetName()+'_norm',pdf_sm_lin_quad_VV_2d.GetName()+'_norm','@0*@1',RooArgList(self.wtmp.var('norm_sm_lin_quad_%s_%s_%s'%(ops,self.ch,VV)),norm_VV_reg))


                        signal_quad_norm_VV = RooFormulaVar(pdf_quad_VV_2d.GetName()+'_norm',pdf_quad_VV_2d.GetName()+'_norm','@0*@1',RooArgList(self.wtmp.var('norm_quad_%s_%s_%s'%(ops,self.ch,VV)),norm_VV_reg))
                        self.Import_to_ws(self.WS2,[pdf_sm_lin_quad_VV_2d,pdf_quad_VV_2d,signal_lin_norm_VV,signal_quad_norm_VV],1) #,pdf_sm_lin1_quad_VV_2d,signal_lin1_norm_VV
                        
                        c3_AM=ROOT.TCanvas('c3_%s_%s_%s_%s'%(ops,VV,region,self.ch),'',600,600); #c3_AM.SetLogy();                        
                        mplot_tmp_AM = rrv_mass_lvj.frame(RooFit.Bins(rrv_mass_lvj.getBins()));

                        pdf_sm_lin_quad_mlvj_VV.plotOn(mplot_tmp_AM, RooFit.Name("lin"),RooFit.LineStyle(kDashDotted),RooFit.LineColor(ROOT.kOrange+10));
                        pdf_quad_mlvj_VV.plotOn(mplot_tmp_AM, RooFit.Name("quad"),RooFit.LineColor(ROOT.kBlue));
                        self.leg_tmp_am= self.legend4Plot(mplot_tmp_AM,0, 0, 0., 0., -0.1,0,str(self.ch+"-"+ops));
                        mplot_tmp_AM.addObject(self.leg_tmp_am);

                        mplot_tmp_AM.SetYTitle("PDFs"); mplot_tmp_AM.GetYaxis().SetTitleOffset(1.05);
                        mplot_tmp_AM.Draw();        c3_AM.Update();        c3_AM.Draw();
                        c3_AM.SaveAs(self.plotsDir+'/pdfs_%s_%s%s_%s.png'%(ops,self.ch,region,VV))
                        c3_AM.SaveAs(self.plotsDir+'/pdfs_%s_%s%s_%s.pdf'%(ops,self.ch,region,VV))
                        
                    

                ##define which parameters are floating (also has to be done in the datacard)
                #self.WS2.var("rrv_c_ChiSq_WJets0_%s"%self.ch).setConstant(kFALSE) ##am
                self.WS2.var("rrv_c_Exp_WJets0_%s"%self.ch).setConstant(kFALSE)
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

            if options.Make_plots:
                for i in self.aTGCprocs:
                    self.Make_plots(self.rrv_mass_lvj,i,self.fitresults)
                    
                    #self.Make_plots(self.rrv_mass_lvj,'WZ',self.fitresults)
            for i in range(3):
                for j in range(3):
                    self.wtmp.var(self.POI[j]).setVal(0)
                #self.wtmp.var(self.POI[i]).setVal(self.PAR_MAX[self.POI[i])

            #raw_input(self.channel)
            return combineCardName

###run code###

if __name__ == '__main__':
    if options.chan=='elmu':
        makeWS_el        = Prepare_workspace_4limit(options.year,'el')
        combineCardName_el=makeWS_el.Make_input()
        makeWS_mu        = Prepare_workspace_4limit(options.year,'mu')
        combineCardName_mu=makeWS_mu.Make_input()
        output_card_name='aC_%s_simfit'%(options.DB)
        cmd = 'combineCards.py aC_{DB}_sig_el_{yr}_{dd}.txt aC_{DB}_sig_mu_{yr}_{dd}.txt aC_{DB}_sb_lo_el_{yr}_{dd}.txt aC_{DB}_sb_lo_mu_{yr}_{dd}.txt aC_{DB}_sb_hi_el_{yr}_{dd}.txt aC_{DB}_sb_hi_mu_{yr}_{dd}.txt > {dC}_{yr}_{dd}.txt'.format(dC=output_card_name,yr=options.year,dd=date,DB=options.DB)
        print (cmd)
        os.system(cmd)
    else:
        makeWS= Prepare_workspace_4limit(options.year,options.chan)
        combineCardName=makeWS.Make_input()
        output_card_name='aC_%s_%s'%(options.DB,options.chan)
        cmd = 'combineCards.py aC_{DB}_sig_{FS}_{yr}_{dd}.txt  aC_{DB}_sb_lo_{FS}_{yr}_{dd}.txt  aC_{DB}_sb_hi_{FS}_{yr}_{dd}.txt > {dC}_{yr}_{dd}.txt'.format(dC=output_card_name,yr=options.year,dd=date,FS=options.chan,DB=options.DB)
        print (cmd)
        os.system(cmd)

    os.system('mv *txt %s/'%(final_cardsdir_name))

    #    #combine_cards_dir="Cards/%s/"%(date)
    #    #combineCardName=combine_cards_dir+'/aC_WWWZ_elmu_simfit_%s.txt'%(options.year)
    #    #cmd='combineCards.py {mu} {el} > {elmu}'.format(mu=combineCardName_mu,el=combineCardName_el,elmu=combineCardName)
    #    #os.system(cmd)
    #    #return True 
    #    
    #else:
    #    
    #    makeWS        = Prepare_workspace_4limit(options.year,options.chan)
    #    makeWS.Make_input()
    
