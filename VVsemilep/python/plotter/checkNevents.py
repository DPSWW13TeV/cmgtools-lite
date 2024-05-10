import os,sys, re, ROOT,optparse
from array import array
from glob import glob

#fN=sys.argv[1]
year=sys.argv[1]
frnds_dir=sys.argv[2]
#frnds_dir="3_ak8Vtagged_sdm45"
eospath="/eos/cms/store/cmst3/group/dpsww/NanoTrees_v9_vvsemilep_06012023/"

basepath=os.path.join(eospath,year)
faultyfrnds=[]

for x in glob(basepath+"/*.root"):
    proc=os.path.basename(x)[:-len(".root")]
    #print proc 
    fIn=ROOT.TFile.Open(x)
    #print x
    n_p=fIn.Get("Events").GetEntries();
    frndpath=os.path.join(basepath,frnds_dir)
    frnd_file=frndpath+"/"+proc+"_Friend.root"
    #print frnd_file
    if os.path.isfile(frnd_file):
        fIn=ROOT.TFile.Open(frnd_file)
        n_f=fIn.Get("Friends").GetEntries();
        fIn.Close()
        if n_p != n_f:
            print n_p,n_f,frnd_file
            faultyfrnds.append(frnd_file)
        else: continue

print "faultyfrnds" , faultyfrnds
