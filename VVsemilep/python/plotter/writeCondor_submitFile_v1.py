import os,string,sys
from plots_VVsemilep import *
allvars= theWVultimateset_log + theWVultimateset #['FatJet1_pNetMD_Wtagscore']##theWVultimateset_log + theWVultimateset ##++leptons fitCR #mWVs #missing #fitCR #+
doWhat=sys.argv[1] #cards or plots

#year=sys.argv[2]
pf="" #withoutTaggernHEEP"
years=["2018","2017","2016","2016APV"] #,"fullRun2"] #,"all"] 
#years.append(year)

allfavs=["mu","el","onelep"]
ll=["el","mu"]
fitvar_sig=['mWV']#,'mWV_fixedbW']
fitvar_bkg=['mWV']#'fjet_pt']#,'fjet_pt_fixedbW']

lepsel={'topCR' : [allfavs],
        'topCR_incl'  : [ ll,fitvar_bkg],
        'topCR_twob'  : [ ["onelep"],fitvar_bkg],
        'topCR_oneb'  : [ ["onelep"],fitvar_bkg],
        'topCR_lo'    : [ ["onelep"],fitvar_bkg],
        'topCR_hi'    : [ ["onelep"],fitvar_bkg],
        'inclB'       : [ll,fitvar_bkg],
        'sig'         : [ll,fitvar_sig],
        'sig_incl'    : [ll,fitvar_sig],
        'SR'          : [ll,fitvar_sig],
        'sig_lo'      : [ll,fitvar_sig],
        'sig_hi'      : [ll,fitvar_sig],
        'sb_lo'       : [allfavs,fitvar_sig],
        'sb_hi'       : [allfavs,fitvar_sig],
        'wjCR_incl'   : [ll,fitvar_bkg],
        'wjCR_lo'     : [ll,fitvar_bkg],
        'wjCR_hi'     : [ll,fitvar_bkg],
}

list_ops={'smeft':['cW','clu','cWtil','cHWB','cHD','cHj3','cHj1','clj1','cWMclu','cHWBMcHD','cHDMcW','cHWBMcW'],'eft':['cw','c3w','cb','Odd_cw','Odd_c3w','c3wMcw','c3wMcb','cwMcb']} #,'cnb','c3wMcnb','cwMcnb']}

#ops=['all'] #'cnb','c3wMcnb','cwMcnb'] #'cW','clu','cw','c3w','cb','c3wMcw','c3wMcb','cwMcb','']#,'']#,'']#'cw','c3w','cb']#,'cb','cHDD','clu','cW']'all']#


nT=True

smeft=True
basis="smeft" if smeft else ''
fName='submitFile_%s%s%s.condor'%(doWhat,basis,'nT' if nT else '')
tmp_condor = open('jobs/%s'%fName, 'w')
tmp_condor.write('''Executable = dummy{here}.sh
use_x509userproxy = true
getenv      = True                                                                                                              
Log        = jobs/{dW}{tag}{basis}_$(Cluster)_$(ProcId).log
Output     = jobs/{dW}{tag}{basis}_$(Cluster)_$(ProcId).out
Error      = jobs/{dW}{tag}{basis}_$(Cluster)_$(ProcId).error
+JobFlavour = "tomorrow"
arguments  = $(info) 
on_exit_remove = (ExitBySignal == False) && (ExitCode == 0)
max_retries    = 3
requirements   = Machine =!= LastRemoteHost
MY.SingularityImage = "/cvmfs/unpacked.cern.ch/gitlab-registry.cern.ch/cms-cat/cmssw-lxplus/cmssw-el7-lxplus:latest/"\n'''.format(dW=doWhat,here='_2' if nT else '',basis=basis,tag='_nT' if nT else ''))
if os.environ['USER'] in ['anmehta', 'vmilosev']:
   tmp_condor.write('+AccountingGroup = "group_u_CMST3.all"\n')
if 'plots' in doWhat :
   tmp_condor.write('request_memory = 10GB\n')
tmp_condor.write('queue info from ( \n')

configs=[]

ops=list_ops['smeft'] if smeft else list_ops['eft']
if "plots" in doWhat and not nT:
   ops=['all']
   configs=["topCR_incl",'sig_incl',"wjCR_incl"]
elif "plots" in doWhat and nT:
   ops=['all']
   configs=['wjCR_incl']
elif "cards" in doWhat:
   nT=False
   configs=["wjCR_lo","topCR_incl","wjCR_hi","sig_lo","sig_hi"] #] #,"sig_incl"
   if "fullRun2" in years: 
      years.remove('fullRun2');
else: configs=[]
      
for sel in configs:
   for yr in years: #in "2016APV,2016,2017,2018".split(","):
      for lep in lepsel[sel][0]: 
         if 'plots' in  doWhat:
            for iVar in allvars:
               if len(ops) > 0:   
#                  for op in ops:  #ops should be 'all' for plotting or else empty string
                  tmp_condor.write('{cmssw} {doWhat} {yr}  {sel} {lf} {iVar} {op} {basis} \n'.format(iVar=iVar,yr=yr,sel=sel,lf=lep,basis=basis,doWhat=doWhat,op='all',cmssw=os.environ['PWD']))
               else:
                  tmp_condor.write('{cmssw} {doWhat} {yr}  {sel} {lf} {iVar} {basis} \n'.format(iVar=iVar,yr=yr,sel=sel,lf=lep,basis=basis,doWhat=doWhat,cmssw=os.environ['PWD']))
         else:
            for fv in lepsel[sel][1]:
               for op in ops: 
                  if len(op) > 0:
                     tmp_condor.write('{cmssw} {doWhat} {yr}  {sel} {lf} {fv} {op} {basis} \n'.format(cmssw=os.environ['PWD'],yr=yr,sel=sel,lf=lep,basis=basis,doWhat=doWhat,op=op,fv=fv ) )
                  else:
                     tmp_condor.write('{cmssw} {doWhat} {yr}  {sel} {lf} {fv} {basis} \n'.format(doWhat=doWhat,yr=yr,sel=sel,lf=lep,basis=basis,cmssw=os.environ['PWD'],fv=fv ) )

tmp_condor.write(') \n')
tmp_condor.close()

print 'condor_submit jobs/%s'%fName
os.system('condor_submit jobs/%s'%fName)


#python plots_VVsemilep.py --results --sel plots --year ${2} --nLep ${3} --finalState ${4} --pv ${5} --pf ${6}
##fixme suboptimal for the case with pf and ops
#python plots_VVsemilep.py --results --finalState boosted --nLep 1 --sel SR --pv mWV1_typ0_pmet_boosted  --lf mu --lf el --year 2018 --dW plots --applylepSFs --WC cwww --WC ccw --WC cb
## python plots_VVsemilep.py --results --dW cards --year 2016 --finalState elmu --finalState mumu --applylepSFs 
