import os,sys, re, ROOT,optparse
from array import array
from glob import glob


year=sys.argv[1]
frnds_dir=sys.argv[2]
#frnds_dir="3_ak8Vtagged_sdm45"
eospath="/eos/cms/store/cmst3/group/dpsww/NanoTrees_v9_vvsemilep_skimmed" #06012023" #_skimmed"

basepath=os.path.join(eospath,year) 
faultyfrnds=[]

for x in glob(basepath+"/*.root"):
    #proc=os.path.basename(x)[:-len("_Friend.root")]
    proc=os.path.basename(x)[:-len(".root")]
    fIn=ROOT.TFile.Open(x)
    #print(x)
    n_p=fIn.Get("Events").GetEntries();
    frndpath=os.path.join(basepath,frnds_dir) 
    frnd_file=frndpath+"/"+proc+"_Friend.root"
    print frnd_file
    if "Run20" in proc and frnds_dir not in ['1_recl','3_ak8_sdm45','0_wjest_v5']: continue
    if os.path.isfile(frnd_file):
        fIn=ROOT.TFile.Open(frnd_file)
        n_f=fIn.Get("Friends").GetEntries();
        fIn.Close()
        if n_p != n_f:
            print("Np",n_p,"Nf",n_f,"frnd file",frnd_file)
            faultyfrnds.append(proc)
        else: continue
    else:
        print('could not find frnds tree for',proc)
        faultyfrnds.append(proc)
print("faultyfrnds for year %s and type %s are\n"%(year,frnds_dir))
print(faultyfrnds)
