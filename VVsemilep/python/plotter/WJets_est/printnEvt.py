import os,sys, re, ROOT,optparse

from glob import glob

#fN=sys.argv[1]
#year=sys.argv[2]
files=[]


def printnEvt(fN,yr):
    sumw=0
    basepath="/eos/cms/store/cmst3/group/dpsww/NanoTrees_v9_vvsemilep_06012023/"+yr+"/"
    for x in glob(basepath+"/*.root"):
        proc=os.path.basename(x)[:-len(".root")]
        if re.match(fN+".*", proc):
            files.append(x)
    for sf in files:
        print sf
        fIn=ROOT.TFile.Open(sf)
        ttree=fIn.Get('Runs')
        for ev in ttree:
            sumw+=ev.genEventSumw
    #print fN,int(sumw)
    fIn.Close()
    print fN,int(sumw)
    return int(sumw)
#if __name__ == '__main__':
##    parser = optparse.OptionParser(usage='usage: %prog [opts] ', version='%prog 1.0')
##    parser.add_option('--drawScans', action='store_true', dest='drawScans'        , default=True, help='overlay shapes for VBS ssWW')
##    global opts
##    (opts, args) = parser.parse_args()
##
#    printnEvt(fN,year)

#print fname,int(sumw)
