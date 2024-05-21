import os,sys, re, ROOT,optparse
from array import array
from glob import glob
#from  printnEvt import printnEvt
year=sys.argv[1]
frnds=sys.argv[2] #"wjest_skim" #0_wjest_v2_copy" #0_wjest_newCuts_v1/"
eospath="/eos/cms/store/cmst3/group/dpsww/NanoTrees_v9_vvsemilep_06012023/"
#files=[]
outname=frnds+"_addOns" 
outdir=os.path.join(eospath,year,outname)

if not os.path.isdir(outdir):
     os.system("mkdir -p "+outdir)


more=["WWTo1L1Nu2Q","WZTo1L1Nu2Q"]#"WZToLNuQQ01j_5f_amcatnloFxFx",
top=['TTSemi_pow']
#top=['TTSemi_pow_part0','TTSemi_pow_part2','TTSemi_pow_part4','TTSemi_pow_part6','TTSemi_pow_part8','TTSemi_pow_part1','TTSemi_pow_part3','TTSemi_pow_part5','TTSemi_pow_part7','TTSemi_pow_part9']#'TT_mtt1ktoinf','TT_mttp7kto1k']

stop=['T_sch','T_tWch_incldecays','Tbar_tWch_noFullyHad','T_tch','Tbar_tch','T_tWch_noFullyHad'] #['T_sch','T_tWch_incldecays','T_tWch_noFullyHad','T_tch']
wjets=['WJetsToLNu_HT100to200','WJetsToLNu_HT200to400','WJetsToLNu_HT400to600','WJetsToLNu_HT70to100','WJetsToLNu_HT1200to2500','WJetsToLNu_HT2500toInf','WJetsToLNu_HT600to800','WJetsToLNu_HT800to1200']#,'WJetsToLNu_LO']
ww_atgc=['WpWmToLpNujj_01j_aTGC_4f_NLO_FXFX_4f','WmWpToLmNujj_01j_aTGC_4f_NLO_FXFX_4f','WpWmToLpNujj_01j_aTGC_pTW_150toInf_mWV_150to600',
'WpWmToLpNujj_01j_aTGC_pTW_150toInf_mWV_600to800','WpWmToLpNujj_01j_aTGC_pTW_150toInf_mWV_800toInf','WmWpToLmNujj_01j_aTGC_pTW_150toInf_mWV_150to600',
'WmWpToLmNujj_01j_aTGC_pTW_150toInf_mWV_600to800','WmWpToLmNujj_01j_aTGC_pTW_150toInf_mWV_800toInf']
wz_atgc=['WpZToLpNujj_01j_aTGC_pTZ_150toInf_mWV_150to600_4f','WpZToLpNujj_01j_aTGC_pTZ_150toInf_mWV_600to800_4f','WpZToLpNujj_01j_aTGC_pTZ_150toInf_mWV_800toInf_4f',
'WmZToLmNujj_01j_aTGC_pTZ_150toInf_mWV_150to600_4f','WmZToLmNujj_01j_aTGC_pTZ_150toInf_mWV_600to800_4f','WmZToLmNujj_01j_aTGC_pTZ_150toInf_mWV_800toInf_4f']

atgc=[
'WmZToLmNujj_01j_aTGC_pTZ_150toInf_mWV_150to600_v1',
'WpZToLpNujj_01j_aTGC_pTZ_150toInf_mWV_150to600_v1',
'WmZToLmNujj_01j_aTGC_pTZ_150toInf_mWV_600to800_v1',
'WpZToLpNujj_01j_aTGC_pTZ_150toInf_mWV_600to800_v1',
'WmZToLmNujj_01j_aTGC_pTZ_150toInf_mWV_800toInf_v2',
'WpZToLpNujj_01j_aTGC_pTZ_150toInf_mWV_800toInf_v2',
'WpWmToLpNujj_01j_aTGC_pTW_150toInf_mWV_150to600_v1',
'WmWpToLmNujj_01j_aTGC_pTW_150toInf_mWV_150to600_v1',
'WpWmToLpNujj_01j_aTGC_pTW_150toInf_mWV_600to800_v2',
'WmWpToLmNujj_01j_aTGC_pTW_150toInf_mWV_600to800_v2',
'WmWpToLmNujj_01j_aTGC_pTW_150toInf_mWV_800toInf_v2',
'WpWmToLpNujj_01j_aTGC_pTW_150toInf_mWV_800toInf_v2',
]


samples=top + atgc +stop +wjets+more

def printnEvt(fN,yr):
    files=[] 
    sumw=0
    basepath="/eos/cms/store/cmst3/group/dpsww/NanoTrees_v9_vvsemilep_06012023/"+yr+"/"
    for x in glob(basepath+"/*.root"):
        proc=os.path.basename(x)[:-len(".root")]
        #print x
        if re.match(fN+".*", proc):
             print "for this",proc,"considering this files for wts calc",x
             files.append(x)
        else : continue
    for sf in files:
        print sf
        fIn=ROOT.TFile.Open(sf)
        ttree=fIn.Get('Runs')
        for ev in ttree:
            sumw+=ev.genEventSumw
            #print fN,int(sumw)
        fIn.Close()
    print "sample and number of events",fN,int(sumw)
    return int(sumw)



for proc in samples:
    weight=printnEvt(fN=proc,yr=year)
    #now clone friends tree and add a new branch to it
    fbase=os.path.join(eospath,year,frnds)
    fIn=ROOT.TFile.Open(fbase+"/"+proc+"_Friend.root")
    ttree=fIn.Get('Friends')
    fOut=ROOT.TFile(outdir+"/"+proc+"_Friend.root","RECREATE")
    newtree = ROOT.TTree("Friends","new friends tree");
    sumw=array('d',[0.0])
    newtree.Branch("sumw",sumw,"sumw/D")
    for ev in ttree: 
        #print weight
        sumw[0]=weight
        newtree.Fill();

    fOut.Write()
    fOut.Close()




#hadd /eos/cms/store/cmst3/group/dpsww//NanoTrees_v9_vvsemilep_06012023//2018//0_wjest/TTSemi_pow_Friend.root /eos/cms/store/cmst3/group/dpsww//NanoTrees_v9_vvsemilep_06012023//2018//0_wjest/TTSemi_pow_part*root
#mv /eos/cms/store/cmst3/group/dpsww//NanoTrees_v9_vvsemilep_06012023//2018//0_wjest/TTSemi_pow_part* /eos/cms/store/cmst3/group/dpsww//NanoTrees_v9_vvsemilep_06012023//2018//0_wjest/chunks/
# hadd /eos/cms/store/cmst3/group/dpsww/NanoTrees_v9_vvsemilep_06012023/2018/1_wjest_newCuts_v1/WmWpToLmNujj_01j_aTGC_pTW_150toInf_mWV_800toInf_comb.root   /eos/cms/store/cmst3/group/dpsww/NanoTrees_v9_vvsemilep_06012023/2018/1_wjest_newCuts_v1/WmWpToLmNujj_01j_aTGC_pTW_150toInf_mWV_800toInf_part0_v2_Friend.root /eos/cms/store/cmst3/group/dpsww/NanoTrees_v9_vvsemilep_06012023/2018/1_wjest_newCuts_v1/WmWpToLmNujj_01j_aTGC_pTW_150toInf_mWV_800toInf_v2_Friend.root
#[lxplus723 | 05:37 AM] WJets_est $ : mv /eos/cms/store/cmst3/group/dpsww/NanoTrees_v9_vvsemilep_06012023/2018/1_wjest_newCuts_v1/WmWpToLmNujj_01j_aTGC_pTW_150toInf_mWV_800toInf_part0_v2_Friend.root /eos/cms/store/cmst3/group/dpsww/NanoTrees_v9_vvsemilep_06012023/2018/1_wjest_newCuts_v1/chunks/
#[lxplus723 | 05:38 AM] WJets_est $ : mv /eos/cms/store/cmst3/group/dpsww/NanoTrees_v9_vvsemilep_06012023/2018/1_wjest_newCuts_v1/WmWpToLmNujj_01j_aTGC_pTW_150toInf_mWV_800toInf_v2_Friend.root /eos/cms/store/cmst3/group/dpsww/NanoTrees_v9_vvsemilep_06012023/2018/1_wjest_newCuts_v1/chunks/
#[lxplus723 | 05:38 AM] WJets_est $ : hadd /eos/cms/store/cmst3/group/dpsww/NanoTrees_v9_vvsemilep_06012023/2018/1_wjest_newCuts_v1/WpWmToLpNujj_01j_aTGC_pTW_150toInf_mWV_800toInf_comb_v2_Friend.root /eos/cms/store/cmst3/group/dpsww/NanoTrees_v9_vvsemilep_06012023/2018/1_wjest_newCuts_v1/WpWmToLpNujj_01j_aTGC_pTW_150toInf_mWV_800toInf_v2_Friend.root /eos/cms/store/cmst3/group/dpsww/NanoTrees_v9_vvsemilep_06012023/2018/1_wjest_newCuts_v1/WpWmToLpNujj_01j_aTGC_pTW_150toInf_mWV_800toInf_part0_v2_Friend.root
#[lxplus723 | 05:39 AM] WJets_est $ : mv /eos/cms/store/cmst3/group/dpsww/NanoTrees_v9_vvsemilep_06012023/2018/1_wjest_newCuts_v1/WmWpToLmNujj_01j_aTGC_pTW_150toInf_mWV_800toInf_comb.root /eos/cms/store/cmst3/group/dpsww/NanoTrees_v9_vvsemilep_06012023/2018/1_wjest_newCuts_v1/WmWpToLmNujj_01j_aTGC_pTW_150toInf_mWV_800toInf_comb_v2_Friend.root
#[lxplus723 | 05:39 AM] WJets_est $ : mv /eos/cms/store/cmst3/group/dpsww/NanoTrees_v9_vvsemilep_06012023/2018/1_wjest_newCuts_v1/WpWmToLpNujj_01j_aTGC_pTW_150toInf_mWV_800toInf_v2_Friend.root /eos/cms/store/cmst3/group/dpsww/NanoTrees_v9_vvsemilep_06012023/2018/1_wjest_newCuts_v1/chunks/
#[lxplus723 | 05:40 AM] WJets_est $ : mv /eos/cms/store/cmst3/group/dpsww/NanoTrees_v9_vvsemilep_06012023/2018/1_wjest_newCuts_v1/WpWmToLpNujj_01j_aTGC_pTW_150toInf_mWV_800toInf_part0_v2_Friend.root /eos/cms/store/cmst3/group/dpsww/NanoTrees_v9_vvsemilep_06012023/2018/1_wjest_newCuts_v1/chunks/
