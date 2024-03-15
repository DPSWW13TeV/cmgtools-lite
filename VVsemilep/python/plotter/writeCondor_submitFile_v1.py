import os,string,sys
from plots_VVsemilep import *

allvars= theWVultimateset #HEM + #bTag_eff #mWV #topCR #theWVultimateset #+moreak8jetvars MConly+#newVars+lepvars+WVvars+eventvars 
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
pf=""

lepsel={'topCR' : ["onelep"],
        'inclB' : ["mu","el"],
        'SR'    : ["mu","el"],
        'sig'   : ["mu","el"],
        'sb_lo' : ["mu","el"],
        'sb_hi' : ["mu","el"],
        'SB'    : ["mu","el"],

}

ops=['c3w','ccw','cb','']
for sel in ["SB","sig"]: #"inclB","sig"]: #,"sb_lo","sb_hi"]:  #"wjCR","topCR",]:
   for cat in ["boosted"]: #,"resolved"]: 
       for yr in ["2018"]: #2016,2017,2018".split(","):
           for lep in lepsel[sel]:
              if 'plots' in  doWhat:
                 for iVar in allvars:
                    tmp_condor.write('arguments  = {cmssw} {yr} {cat} {sel} {lf} {iVar} {pf} \n'.format(iVar=iVar,cmssw=os.environ['PWD'],cat=cat,yr=yr,sel=sel,lf=lep,pf=pf ) )
                    tmp_condor.write('queue 1\n\n')
              else:
                 if "top" in sel:
                    tmp_condor.write('arguments  = {cmssw} {yr} {cat} {sel} {lf} {pf} \n'.format(cmssw=os.environ['PWD'],cat=cat,yr=yr,sel=sel,lf=lep,pf=pf ) )
                    tmp_condor.write('queue 1\n\n')
                    for op in ops: #still needs to be validated
                       tmp_condor.write('arguments  = {cmssw} {yr} {cat} {sel} {lf} {op} {pf} \n'.format(cmssw=os.environ['PWD'],cat=cat,yr=yr,op=op,sel=sel,lf=lep,pf=pf ) )
                       tmp_condor.write('queue 1\n\n')

          
tmp_condor.close()

print 'condor_submit jobs/%s'%fName
os.system('condor_submit jobs/%s'%fName)


#python plots_VVsemilep.py --results --sel plots --year ${2} --nLep ${3} --finalState ${4} --pv ${5} --pf ${6}
##fixme suboptimal for the case with pf and ops
#python plots_VVsemilep.py --results --finalState boosted --nLep 1 --sel SR --pv mWV1_typ0_pmet_boosted  --lf mu --lf el --year 2018 --dW plots --applylepSFs --WC cwww --WC ccw --WC cb
## python plots_VVsemilep.py --results --dW cards --year 2016 --finalState elmu --finalState mumu --applylepSFs 
