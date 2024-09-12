import os,string,sys
from plots_VVsemilep import *

allvars=  theWVultimateset_log #+theWVultimateset
doWhat=sys.argv[1] #cards or plots
pf=""

allfavs=["mu","el","onelep"]
ll=["mu","el"]
fitvar_sig=['mWV']#,'mWV_fixedbW']
fitvar_bkg=['mWV']#'fjet_pt']#,'fjet_pt_fixedbW']

lepsel={'topCR' : ["onelep"],
        'topCR_incl' : [ ["onelep"],fitvar_bkg],
        'topCR_twob' : [ ["onelep"],fitvar_bkg],
        'topCR_oneb' : [ ["onelep"],fitvar_bkg],
        'topCR_lo'   : [ ["onelep"],fitvar_bkg],
        'topCR_hi'   : [ ["onelep"],fitvar_bkg],
        'inclB' : [ll,fitvar_bkg],
        'sig'   : [ll,fitvar_sig],
        'sb_lo' : [allfavs,fitvar_sig],
        'sb_hi' : [allfavs,fitvar_sig],
        'wjCR_incl': [ll,fitvar_bkg],
        'wjCR_lo'  : [ll,fitvar_bkg],
        'wjCR_hi'  : [ll,fitvar_bkg],
}
ops=['all'] #,'c3w','cb']#,'cb','cHDD','clu','cW']


fName='submitFile_%s.condor'%doWhat
tmp_condor = open('jobs/%s'%fName, 'w')
tmp_condor.write('''Executable = dummy.sh
use_x509userproxy = true
getenv      = True                                                                                                              
Log        = jobs/{dW}_$(Cluster)_$(ProcId).log
Output     = jobs/{dW}_$(Cluster)_$(ProcId).out
Error      = jobs/{dW}_$(Cluster)_$(ProcId).error
+JobFlavour = "tomorrow"
arguments  = $(info) 
on_exit_remove = (ExitBySignal == False) && (ExitCode == 0)
max_retries    = 3
request_memory = 10GB
requirements   = Machine =!= LastRemoteHost
MY.SingularityImage = "/cvmfs/unpacked.cern.ch/gitlab-registry.cern.ch/cms-cat/cmssw-lxplus/cmssw-el7-lxplus:latest/"\n'''.format(dW=doWhat))
if os.environ['USER'] in ['anmehta', 'vmilosev']:
   tmp_condor.write('+AccountingGroup = "group_u_CMST3.all"\n')
if 'plots' in doWhat :
   tmp_condor.write('request_memory = 10GB\n')
tmp_condor.write('queue info from ( \n')

for sel in ["topCR_incl","wjCR_lo","wjCR_hi","sig"]: #"topCR_lo","topCR_hi","sig",
   for cat in ["boosted"]: 
       for yr in ["2018"]: #2016,2017,2018".split(","):
           for lep in lepsel[sel][0]: 
              if 'plots' in  doWhat:
                 for iVar in allvars:
                    if len(ops) > 0:   
                       for op in ops: 
                          tmp_condor.write('{cmssw} {doWhat} {yr} {cat} {sel} {lf} {iVar} {op} {pf} \n'.format(iVar=iVar,cat=cat,yr=yr,sel=sel,lf=lep,pf=pf,doWhat=doWhat,op=op,cmssw=os.environ['PWD']))
                    else:
                       tmp_condor.write('{cmssw} {doWhat} {yr} {cat} {sel} {lf} {iVar} {pf} \n'.format(iVar=iVar,cat=cat,yr=yr,sel=sel,lf=lep,pf=pf,doWhat=doWhat,cmssw=os.environ['PWD']))
              else:
                 for fv in lepsel[sel][1]:
                    if 'wj' in sel or 'top' in sel: 
                       tmp_condor.write('{cmssw} {doWhat} {yr} {cat} {sel} {lf} {fv} {pf} \n'.format(doWhat=doWhat,cat=cat,yr=yr,sel=sel,lf=lep,pf=pf,cmssw=os.environ['PWD'],fv=fv ) )
                    else:
                       for op in ops: 
                          tmp_condor.write('{cmssw} {doWhat} {yr} {cat} {sel} {lf} {fv} {op} {pf} \n'.format(cmssw=os.environ['PWD'],cat=cat,yr=yr,sel=sel,lf=lep,pf=pf,doWhat=doWhat,op=op,fv=fv ) )


tmp_condor.write(') \n')
tmp_condor.close()

print 'condor_submit jobs/%s'%fName
os.system('condor_submit jobs/%s'%fName)


#python plots_VVsemilep.py --results --sel plots --year ${2} --nLep ${3} --finalState ${4} --pv ${5} --pf ${6}
##fixme suboptimal for the case with pf and ops
#python plots_VVsemilep.py --results --finalState boosted --nLep 1 --sel SR --pv mWV1_typ0_pmet_boosted  --lf mu --lf el --year 2018 --dW plots --applylepSFs --WC cwww --WC ccw --WC cb
## python plots_VVsemilep.py --results --dW cards --year 2016 --finalState elmu --finalState mumu --applylepSFs 
