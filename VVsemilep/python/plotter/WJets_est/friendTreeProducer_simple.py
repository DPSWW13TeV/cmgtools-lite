import os,sys, re, ROOT,optparse
from array import array
from glob import glob
#from  printnEvt import printnEvt
#fN=sys.argv[1]
year=sys.argv[1]
frnds="0_wjest_sDM_all/"
eospath="/eos/cms/store/cmst3/group/dpsww/NanoTrees_v9_vvsemilep_06012023/"
#files=[]
outname="1_wjest_sDM_all"
outdir=os.path.join(eospath,year,outname)

if not os.path.isdir(outdir):
     os.system("mkdir -p "+outdir)


more=["WWTo1L1Nu2Q","WZToLNuQQ01j_5f_amcatnloFxFx"]
top=['TTSemi_pow']
#top=['TTSemi_pow_part0','TTSemi_pow_part2','TTSemi_pow_part4','TTSemi_pow_part6','TTSemi_pow_part8','TTSemi_pow_part1','TTSemi_pow_part3','TTSemi_pow_part5','TTSemi_pow_part7','TTSemi_pow_part9']#'TT_mtt1ktoinf','TT_mttp7kto1k']

stop=['T_sch','T_tWch_incldecays','Tbar_tWch_noFullyHad','T_tch','Tbar_tch'] #['T_sch','T_tWch_incldecays','T_tWch_noFullyHad','T_tch']
wjets=['WJetsToLNu_HT100to200','WJetsToLNu_HT200to400','WJetsToLNu_HT400to600','WJetsToLNu_HT70to100','WJetsToLNu_HT1200to2500','WJetsToLNu_HT2500toInf','WJetsToLNu_HT600to800','WJetsToLNu_HT800to1200','WJetsToLNu_LO']
ww_atgc=['WpWmToLpNujj_01j_aTGC_4f_NLO_FXFX_4f','WmWpToLmNujj_01j_aTGC_4f_NLO_FXFX_4f','WpWmToLpNujj_01j_aTGC_pTW_150toInf_mWV_150to600',
'WpWmToLpNujj_01j_aTGC_pTW_150toInf_mWV_600to800','WpWmToLpNujj_01j_aTGC_pTW_150toInf_mWV_800toInf','WmWpToLmNujj_01j_aTGC_pTW_150toInf_mWV_150to600',
'WmWpToLmNujj_01j_aTGC_pTW_150toInf_mWV_600to800','WmWpToLmNujj_01j_aTGC_pTW_150toInf_mWV_800toInf']
wz_atgc=['WpZToLpNujj_01j_aTGC_pTZ_150toInf_mWV_150to600_4f','WpZToLpNujj_01j_aTGC_pTZ_150toInf_mWV_600to800_4f','WpZToLpNujj_01j_aTGC_pTZ_150toInf_mWV_800toInf_4f',
'WmZToLmNujj_01j_aTGC_pTZ_150toInf_mWV_150to600_4f','WmZToLmNujj_01j_aTGC_pTZ_150toInf_mWV_600to800_4f','WmZToLmNujj_01j_aTGC_pTZ_150toInf_mWV_800toInf_4f']
samples= ww_atgc+wz_atgc #top #stop +wjets+top+stop+more

def printnEvt(fN,yr):
    files=[] 
    sumw=0
    basepath="/eos/cms/store/cmst3/group/dpsww/NanoTrees_v9_vvsemilep_06012023/"+yr+"/"
    for x in glob(basepath+"/*.root"):
        proc=os.path.basename(x)[:-len(".root")]
        if re.match(fN+".*", proc):
             print "for this",proc,x
             files.append(x)
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
    fIn=ROOT.TFile.Open(fbase+proc+"_Friend.root")
    ttree=fIn.Get('Friends')
    fOut=ROOT.TFile(outdir+"/"+proc+"_Friend.root","RECREATE")
    newtree = ROOT.TTree("Friends","new friends tree");
    sumw=array('d',[-9999.0])
    newtree.Branch("sumw",sumw,"sumw/D")
    for ev in ttree: 
        #print weight
        sumw[0]=weight
        newtree.Fill();

    fOut.Write()
    fOut.Close()



#hadd /eos/cms/store/cmst3/group/dpsww//NanoTrees_v9_vvsemilep_06012023//2018//0_wjest/data_Friend.root /eos/cms/store/cmst3/group/dpsww//NanoTrees_v9_vvsemilep_06012023//2018//0_wjest/*UL18_Friend.root
#hadd /eos/cms/store/cmst3/group/dpsww//NanoTrees_v9_vvsemilep_06012023//2018//0_wjest/TTSemi_pow_Friend.root /eos/cms/store/cmst3/group/dpsww//NanoTrees_v9_vvsemilep_06012023//2018//0_wjest/TTSemi_pow_part*root
#mv /eos/cms/store/cmst3/group/dpsww//NanoTrees_v9_vvsemilep_06012023//2018//0_wjest/TTSemi_pow_part* /eos/cms/store/cmst3/group/dpsww//NanoTrees_v9_vvsemilep_06012023//2018//0_wjest/chunks/
