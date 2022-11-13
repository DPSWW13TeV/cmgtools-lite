import os,string
from plots_VVsemilep import *

allvars=lepvars #ak8jetvars#ak4jetvars+lepvars+eventvars

tmp_condor = open('jobs/submitFile.condor', 'w')
tmp_condor.write('''Executable = dummy_plots.sh 
use_x509userproxy = true
getenv      = True                                                                                                              
Log        = jobs/log_running_$(ProcId).log                                                                                     
Error      = jobs/log_running_$(ProcId).error                                                                                   
environment = "LS_SUBCWD={here}"
+JobFlavour = "workday"
\n\n'''.format(here=os.environ['PWD']))
pf="testfatty"
for nl in ["1"]: #"1,2".split(","):
    for cat in ["boosted"]: #,resolved".split(","):
        for yr in ["2018"]: #2016,2017,2018".split(","): 
            for iVar in allvars:
                tmp_condor.write('arguments = {cmssw} {yr} {nl} {cat} {iVar} {pf} \n'.format(cmssw=os.environ['PWD'],cat=cat,yr=yr,nl=nl,iVar=iVar,pf=pf  ) )
                tmp_condor.write('queue 1\n\n')

tmp_condor.close()

print 'condor_submit jobs/submitFile.condor'
#os.system('condor_submit jobs/submitFile.condor')


#python plots_VVsemilep.py --results --dW plots --year ${2} --nLep ${3} --finalState ${4} --pv ${5} --pf ${6}
