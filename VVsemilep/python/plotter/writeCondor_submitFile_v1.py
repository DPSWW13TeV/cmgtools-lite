import os,string,sys
from plots_VVsemilep import *
allvars= theWVultimateset_log + theWVultimateset #['FatJet1_pNetMD_Wtagscore']##theWVultimateset_log + theWVultimateset ##++leptons fitCR #mWVs #missing #fitCR #+
doWhat=sys.argv[1] #cards or plots
#allvars=[
#"FatJet1_sDrop_mass_logy",
#"FatJet1_pt_logy",
#"FatJet1_pNetMD_Wtagscore",
#"mWV_logy",
#"pmet_phi",
#"pmet_logy",
#"nVert",
#"mtWlep",
#"ptWlep",
#"dRfjlep",
#"dphifjpmet",
#"dphifjlep",
#"nBJetMedium30_Recl"
#]

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
        'Old_wjCR_incl'   : [ll,fitvar_bkg],

}

ops_smeft=["clj3","cjj18","cW","cWtil","cHWB","cHWBtil","cHl3","cHd","cHu","cHj1","cHj3","cll1","cjj38","cju1","clu","cjj11","cjd1","clj1","cld","cjj31"] #,"cju8","cjd8"]
ops_smeft_All=['cll1','cG','cHd','cHDD','cHj3','cjj38','cHWtil','cHj1','cju1','cuu8','cdd8','cuu1','cdd1','cHG','cHe','cHl1', 'cHWB', 'cHl3', 'cju8', 'cjd1', 'clu',  'cWtil','clj3', 'cjj11','cHu',  'ceu','cHWBtil','ced','clj1','cjj18','cGtil','cW','cld','cje', 'cjd8','cud8','cud1','cjj31','cHGtil']
ops_eft=['cw']#,'Odd_cw','Odd_c3w','c3w','cb']





#Mops_eft=[i+'M'+j for i in ops_eft for j in ops_eft if i != j]
#Mops_smeft=[i+'M'+j for i in ops_smeft for j in ops_smeft if i != j]
#Mops_eft=['Odd_cwMOdd_c3w','c3wMcw','c3wMcb','cwMcb']




nT=False
smeft=False
basis="smeft" if smeft else 'eft'

keepIt=[]
fIn="/afs/cern.ch/work/a/anmehta/public/cmgtools_WVsemilep/CMSSW_10_6_29/src/CMGTools/VVsemilep/python/plotter/vvsemilep/fullRun2/mca-includes/mca-{here}.txt".format( here="wv-smeft" if smeft else "eft")
with open(fIn)  as fin:
   for x in fin:
      keepIt.append(x.split(":")[0].rstrip())

#print(keepIt)
Mops_smeft=[i+'M'+j for i in ops_smeft for j in ops_smeft  if "WV_sm_lin_quad_mixed_"+i+'_'+j in keepIt]
Mops_smeft+=[j+'M'+i for i in ops_smeft for j in ops_smeft  if "WV_sm_lin_quad_mixed_"+j+'_'+i in keepIt ]
Mops_eft=[i+'M'+j for i in ops_eft for j in ops_eft if  "WW_sm_lin_quad_mixed_"+i+'_'+j+'+' in keepIt]


#print(Mops_eft)
list_ops={'smeft':Mops_smeft,'eft':Mops_eft}

#logsDir='jobs_%s'%basis
logsDir='jobs' 

fName='submitFile_%s%s%s.condor'%(doWhat,basis,'nT' if nT else '')
tmp_condor = open('%s/%s'%(logsDir,fName), 'w')
tmp_condor.write('''Executable = dummy{here}.sh
use_x509userproxy = true
getenv      = True                                                                                                              
Log        = {logsDir}/{dW}{tag}{basis}_$(Cluster)_$(ProcId).log
Output     = {logsDir}/{dW}{tag}{basis}_$(Cluster)_$(ProcId).out
Error      = {logsDir}/{dW}{tag}{basis}_$(Cluster)_$(ProcId).error
+JobFlavour = "testmatch"
arguments  = $(info) 
on_exit_remove = (ExitBySignal == False) && (ExitCode == 0)
max_retries    = 3
requirements   = Machine =!= LastRemoteHost
MY.SingularityImage = "/cvmfs/unpacked.cern.ch/gitlab-registry.cern.ch/cms-cat/cmssw-lxplus/cmssw-el7-lxplus:latest/"\n'''.format(dW=doWhat,logsDir=logsDir,here='_2' if nT else '_wv',basis=basis,tag='_nT' if nT else ''))
if os.environ['USER'] in ['anmehta', 'vmilosev']:
   tmp_condor.write('+AccountingGroup = "group_u_CMST3.all"\n')
if 'plots' in doWhat :
   tmp_condor.write('request_memory = 10GB\n')
tmp_condor.write('queue info from ( \n')

configs=[]

ops=list_ops['smeft'] if smeft else list_ops['eft']
if "plots" in doWhat and not nT:
   ops=['all']
   configs=['sig_incl',"topCR_incl","wjCR_incl"]
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

print 'condor_submit %s/%s'%(logsDir,fName)
os.system('condor_submit %s/%s'%(logsDir,fName))


#python plots_VVsemilep.py --results --sel plots --year ${2} --nLep ${3} --finalState ${4} --pv ${5} --pf ${6}
##fixme suboptimal for the case with pf and ops
#python plots_VVsemilep.py --results --finalState boosted --nLep 1 --sel SR --pv mWV1_typ0_pmet_boosted  --lf mu --lf el --year 2018 --dW plots --applylepSFs --WC cwww --WC ccw --WC cb
## python plots_VVsemilep.py --results --dW cards --year 2016 --finalState elmu --finalState mumu --applylepSFs 
