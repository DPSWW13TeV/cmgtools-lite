import ROOT
import os
import json

path="/eos/cms/store/cmst3/group/dpsww/vvsemilep/"
for year in ["2018"]: #'2016,2017,2018'.split(','):
        thepath=path+year+'/'
        for PD in ["DoubleMuon","MuonEG","SingleMuon","EGamma", "SingleElectron"]:#,"DoubleEG"                                                                                             
                inputFiles = []
                for f in os.listdir(thepath):
                        if "root" in f and PD in f:
                                inputFiles.append(thepath + f)

                runs = {}


                for f in inputFiles:
                        print f
                        ff    = ROOT.TFile(f, "READ")
                        lumis = ff.Get("LuminosityBlocks")
                        for ev in lumis:
                                if ev.run in runs.keys(): runs[ev.run].append(ev.luminosityBlock)
                                else: runs[ev.run] = [ev.luminosityBlock]

                #Now build it JSON like                                                                                                                                                      
                forjson = {}
                for key in runs.keys():
                        forjson[str(key)] = []
                        templist = runs[key]
                        templist.sort()
                        saving = False
                        start  = 0
                        end    = 0
                        for t in templist:
                                if not saving:
                                        saving = True
                                        start = t
                                        end = t
                                elif t == end +1:
                                        end = t
                                else:
                                        forjson[str(key)].append([start, end])
                                        start = t
                                        end = t
                        forjson[str(key)].append([start,end])

                json.dump(forjson, open("JSON_complete_%s_%s.json"%(year,PD),"w"), sort_keys=True)
