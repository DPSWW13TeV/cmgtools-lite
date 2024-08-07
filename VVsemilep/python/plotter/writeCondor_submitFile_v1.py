import os,string,sys
from plots_VVsemilep import *

allvars=  theWVultimateset #theWVfullset
doWhat=sys.argv[1] #cards or plots
fName='submitFile_%s.condor'%doWhat
tmp_condor = open('jobs/%s'%fName, 'w')
tmp_condor.write('''Executable = dummy.sh
use_x509userproxy = true
getenv      = True                                                                                                              
Log        = jobs/{dW}_$(Cluster)_$(ProcId).log
Output     = jobs/{dW}_$(Cluster)_$(ProcId).out
Error      = jobs/{dW}_$(Cluster)_$(ProcId).error
#requirements = (OpSysAndVer =?= "CentOS7")
+JobFlavour = "tomorrow"
arguments  = $(info) 
request_cpus  = 16
on_exit_remove = (ExitBySignal == False) && (ExitCode == 0)
max_retries    = 3
requirements   = Machine =!= LastRemoteHost
MY.SingularityImage = "/cvmfs/unpacked.cern.ch/gitlab-registry.cern.ch/cms-cat/cmssw-lxplus/cmssw-el7-lxplus:latest/"\n'''.format(dW=doWhat))
if os.environ['USER'] in ['anmehta', 'vmilosev']:
   tmp_condor.write('+AccountingGroup = "group_u_CMST3.all"\n')
tmp_condor.write('queue info from ( \n')
pf="latest"
lepsel={'topCR' : ["onelep"],
        'topCR_incl' : ["onelep"],
        'topCR_twob' : ["onelep"],
        'topCR_oneb' : ["onelep"],
        'inclB' : ["mu","el"],
        'SR'    : ["mu","el"],
        'sig'   : ["mu","el"],
        'sb_lo' : ["mu","el"],
        'sb_hi' : ["mu","el"],
        'SB'    : ["mu","el"],
        'wjCR_incl': ["onelep"], #"mu","el",
        'wjCR_lo'  : ["onelep"], #"mu","el",
        'wjCR_hi'  : ["onelep"] #"mu","el",


}
ops=['c3w']#,'cw','cb','']
for sel in ["wjCR_lo","wjCR_hi","topCR_oneb","sig","sb_lo","sb_hi"]:#"topCR_twob"]: #"wjCR_incl","topCR","sig","sb_lo","sb_hi"]: #"SB","SR"]
   for cat in ["boosted"]: 
       for yr in ["2018"]: #2016,2017,2018".split(","):
           for lep in lepsel[sel]: 
              if 'plots' in  doWhat:
                 for iVar in allvars:
                    tmp_condor.write('{cmssw} {doWhat} {yr} {cat} {sel} {lf}  {iVar} {pf} \n'.format(iVar=iVar,cat=cat,yr=yr,sel=sel,lf=lep,pf=pf,doWhat=doWhat,cmssw=os.environ['PWD']))
              else:
                 if 'wj' in sel or 'top' in sel: 
                    tmp_condor.write('{cmssw} {doWhat} {yr} {cat} {sel} {lf} {pf} \n'.format(doWhat=doWhat,cat=cat,yr=yr,sel=sel,lf=lep,pf=pf,cmssw=os.environ['PWD'] ) )
                 else:
                    for op in ops: #still needs to be validated
                       tmp_condor.write('{cmssw} {doWhat} {yr} {cat} {sel} {lf} {op} {pf} \n'.format(cmssw=os.environ['PWD'],cat=cat,yr=yr,sel=sel,lf=lep,pf=pf,doWhat=doWhat,op=op ) )


tmp_condor.write(') \n')
tmp_condor.close()

print 'condor_submit jobs/%s'%fName
os.system('condor_submit jobs/%s'%fName)


#python plots_VVsemilep.py --results --sel plots --year ${2} --nLep ${3} --finalState ${4} --pv ${5} --pf ${6}
##fixme suboptimal for the case with pf and ops
#python plots_VVsemilep.py --results --finalState boosted --nLep 1 --sel SR --pv mWV1_typ0_pmet_boosted  --lf mu --lf el --year 2018 --dW plots --applylepSFs --WC cwww --WC ccw --WC cb
## python plots_VVsemilep.py --results --dW cards --year 2016 --finalState elmu --finalState mumu --applylepSFs 
