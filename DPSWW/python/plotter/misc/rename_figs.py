import os, string
#/eos/home-i01/a/anmehta/www/DPSWW_v2/fullRun2/2022-03-08_suppMaterial_scaledtopostfit
#path="/eos/user/a/anmehta/www/DPSWW_v2/fullRun2/2022-03-08_suppMaterial_scaledtopostfit/"
#path="/eos/user/a/anmehta/www/DPSWW_v2/fullRun2/2022-03-09_suppMaterial_scaledtopostfit_FORPAPER/" #
path="/eos/user/a/anmehta/www/DPSWW_v2/fullRun2/2022-03-09_2lss_suppMaterial_shapesForPaper/"

#outdir="/afs/cern.ch/work/a/anmehta/public/run2_dpsww_AN/PAS/SMP-21-013"
outdir="/afs/cern.ch/work/a/anmehta/public/paper_run2_postFR/SMP-21-013/"

figs=[f for f in os.listdir(path) if f.endswith(".pdf") and  not "BDT" in f]



chars=[c for i,c in enumerate(string.ascii_lowercase) if i < len(figs)]
for f in figs:
    #cmd="cp %s/%s %s/Figure-aux_004_%s.pdf"%(path,f,outdir,chars[figs.index(f)])
    cmd="cp %s/%s %s/Figure-aux_001_%s.pdf"%(path,f,outdir,chars[figs.index(f)])
    #print cmd
    os.system(cmd)
