import os,string
from plots_VVsemilep import *

allvars= aTGC_chk #bTag_eff #mWV #topCR #theWVultimateset #+moreak8jetvars MConly+#newVars+lepvars+WVvars+eventvars 

tmp_condor = open('jobs/submitFile.condor', 'w')
tmp_condor.write('''Executable = dummy_plots.sh
use_x509userproxy = true
getenv      = True                                                                                                              
environment = "LS_SUBCWD={here}"
Log        = jobs/log_$(ProcId).log
Output     = jobs/log_$(ProcId).out
Error      = jobs/log_$(ProcId).error
+JobFlavour = "tomorrow"
\n\n'''.format(here=os.environ['PWD']))
pf="prelimit"
for dW in ["SR"]: #,"topCR","wjCR"]: #"SR","topCR","wjCR"]:#"wjCR","SR","topCR"]: #topCR","wjCR","SR"]: #," inclB"]: #,"topCR"]: #,"SR"]:
    for nl in ["1"]: #"1,2".split(","):
        for cat in ["boosted"]: #,"resolved"]: #.split(","):
            for yr in ["2018"]: #2016,2017,2018".split(","):
                for lep in ["el","mu","onelep"]:#"el","mu"]: #,"onelep"]:
                    for iVar in allvars:
                        tmp_condor.write('arguments  = {cmssw} {yr} {nl} {cat} {iVar} {dW} {lf} {pf} \n'.format(cmssw=os.environ['PWD'],cat=cat,yr=yr,nl=nl,iVar=iVar,dW=dW,lf=lep,pf=pf ) )
                        tmp_condor.write('queue 1\n\n')

tmp_condor.close()

print 'condor_submit jobs/submitFile.condor'
os.system('condor_submit jobs/submitFile.condor')


#python plots_VVsemilep.py --results --dW plots --year ${2} --nLep ${3} --finalState ${4} --pv ${5} --pf ${6}
