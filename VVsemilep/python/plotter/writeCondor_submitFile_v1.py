import os,string,sys
from plots_VVsemilep import *

allvars= aTGC_chk #bTag_eff #mWV #topCR #theWVultimateset #+moreak8jetvars MConly+#newVars+lepvars+WVvars+eventvars 
doWhat=sys.argv[1] #cards or plots
fName='submitFile_%s.condor'%doWhat
tmp_condor = open('jobs/%s'%fName, 'w')
tmp_condor.write('''Executable = dummy_{dW}.sh
use_x509userproxy = true
getenv      = True                                                                                                              
environment = "LS_SUBCWD={here}"
Log        = jobs/{dW}_$(ProcId).log
Output     = jobs/{dW}_$(ProcId).out
Error      = jobs/{dW}_$(ProcId).error
requirements = (OpSysAndVer =?= "CentOS7")
+JobFlavour = "workday"
\n\n'''.format(dW=doWhat,here=os.environ['PWD']))
pf="V2"

lepsel={'topCR' : ["onelep"],
        'SR'    : ["mu","el"],
        'sig'   : ["mu","el"],
        'sb_lo' : ["mu","el"],
        'sb_hi' : ["mu","el"]}

     
for sel in ["sig","topCR","sig","sb_lo","sb_hi"]: #"wjCR"]:
        for cat in ["boosted"]: #,"resolved"]: 
            for yr in ["2018"]: #2016,2017,2018".split(","):
                for lep in lepsel[sel]:
                    if "top" in sel:
                        tmp_condor.write('arguments  = {cmssw} {yr} {cat} {sel} {lf} {op} {pf} \n'.format(cmssw=os.environ['PWD'],cat=cat,yr=yr,op='',sel=sel,lf=lep,pf=pf ) )
                        tmp_condor.write('queue 1\n\n')
                    else:
                        for op in ['cwww']:
                            tmp_condor.write('arguments  = {cmssw} {yr} {cat} {sel} {lf} {op} {pf} \n'.format(cmssw=os.environ['PWD'],cat=cat,yr=yr,op=op,sel=sel,lf=lep,pf=pf ) )
                            tmp_condor.write('queue 1\n\n')

tmp_condor.close()

print 'condor_submit jobs/%s'%fName
os.system('condor_submit jobs/%s'%fName)


#python plots_VVsemilep.py --results --sel plots --year ${2} --nLep ${3} --finalState ${4} --pv ${5} --pf ${6}
