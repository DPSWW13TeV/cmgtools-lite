import os,sys, re, ROOT,optparse
from array import array
from glob import glob


year=sys.argv[1]
frnds_dir=sys.argv[2]
#frnds_dir="3_ak8Vtagged_sdm45"
eospath="/eos/cms/store/cmst3/group/dpsww/NanoTrees_v9_vvsemilep_skimmed"

basepath=os.path.join(eospath,year) 
faultyfrnds=[]

for x in glob(basepath+"/*.root"):
    #proc=os.path.basename(x)[:-len("_Friend.root")]
    proc=os.path.basename(x)[:-len(".root")]
    fIn=ROOT.TFile.Open(x)
    print(x)
    n_p=fIn.Get("Events").GetEntries();
    #n_p=fIn.Get("Friends").GetEntries();
    frndpath=os.path.join(basepath,frnds_dir) #"/eos/cms/store/cmst3/group/dpsww/NanoTrees_v9_vvsemilep_06012023/2018/wjest_skim/" #
    frnd_file=frndpath+"/"+proc+"_Friend.root"
    #print frnd_file
    if os.path.isfile(frnd_file):
        fIn=ROOT.TFile.Open(frnd_file)
        n_f=fIn.Get("Friends").GetEntries();
        fIn.Close()
        if n_p != n_f:
            print("Np",n_p,"Nf",n_f,"frnd file",frnd_file)
            faultyfrnds.append(frnd_file)
        else: continue
    else:
        print('could not find frnds tree for',proc)
print "faultyfrnds" , faultyfrnds
