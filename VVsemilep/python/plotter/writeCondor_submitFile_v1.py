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

list_ops={'smeft':
          ['cHDD', 'cW', 'cHWB', 'cHWBtil', 'cHWtil', 'cHd', 'cHe', 'cHj1', 'cHj3', 'cHl1', 'cHl3', 'cHu', 'cWtil', 'ced', 'ceu', 'cje', 'cld', 'clj1', 'clj3', 'cll1', 'clu','cWtilMcHWtil','cWtilMcHWBtil','cHWBtilMcHWtil','cWMcHDD', 'cHDDMcHWB', 'cHDDMcHd', 'cHDDMcHe', 'cHDDMcHj1', 'cHDDMcHj3', 'cHDDMcHl1', 'cHDDMcHl3', 'cHDDMcHu', 'cHDDMced', 'cHDDMceu', 'cHDDMcje', 'cHDDMcld', 'cHDDMclj1', 'cHDDMclj3', 'cHDDMcll1', 'cHDDMclu', 'cWMcHDD', 'cWMcHWB', 'cWMcHd', 'cWMcHe', 'cWMcHj1', 'cWMcHj3', 'cWMcHl1', 'cWMcHl3', 'cWMcHu', 'cWMced', 'cWMceu', 'cWMcje', 'cWMcld', 'cWMclj1', 'cWMclj3', 'cWMcll1', 'cWMclu', 'cHWBMcHDD', 'cHWBMcW', 'cHWBMcHd', 'cHWBMcHe', 'cHWBMcHj1', 'cHWBMcHj3', 'cHWBMcHl1', 'cHWBMcHl3', 'cHWBMcHu', 'cHWBMced', 'cHWBMceu', 'cHWBMcje', 'cHWBMcld', 'cHWBMclj1', 'cHWBMclj3', 'cHWBMcll1', 'cHWBMclu'],
'eft':['Odd_cw','Odd_c3w','cw','c3w','cb']} #,'c3wMcw','c3wMcb','cwMcb']} 
#'cHdMcHDD', 'cHdMcW', 'cHdMcHWB', 'cHdMcHe', 'cHdMcHj1', 'cHdMcHj3', 'cHdMcHl1', 'cHdMcHl3', 'cHdMcHu', 'cHdMced', 'cHdMceu', 'cHdMcje', 'cHdMcld', 'cHdMclj1', 'cHdMclj3', 'cHdMcll1', 'cHdMclu', 'cHeMcHDD', 'cHeMcW', 'cHeMcHWB', 'cHeMcHd', 'cHeMcHj1', 'cHeMcHj3', 'cHeMcHl1', 'cHeMcHl3', 'cHeMcHu', 'cHeMced', 'cHeMceu', 'cHeMcje', 'cHeMcld', 'cHeMclj1', 'cHeMclj3', 'cHeMcll1', 'cHeMclu', 'cHj1McHDD', 'cHj1McW', 'cHj1McHWB', 'cHj1McHd', 'cHj1McHe', 'cHj1McHj3', 'cHj1McHl1', 'cHj1McHl3', 'cHj1McHu', 'cHj1Mced', 'cHj1Mceu', 'cHj1Mcje', 'cHj1Mcld', 'cHj1Mclj1', 'cHj1Mclj3', 'cHj1Mcll1', 'cHj1Mclu', 'cHj3McHDD', 'cHj3McW', 'cHj3McHWB', 'cHj3McHd', 'cHj3McHe', 'cHj3McHj1', 'cHj3McHl1', 'cHj3McHl3', 'cHj3McHu', 'cHj3Mced', 'cHj3Mceu', 'cHj3Mcje', 'cHj3Mcld', 'cHj3Mclj1', 'cHj3Mclj3', 'cHj3Mcll1', 'cHj3Mclu', 'cHl1McHDD', 'cHl1McW', 'cHl1McHWB', 'cHl1McHd', 'cHl1McHe', 'cHl1McHj1', 'cHl1McHj3', 'cHl1McHl3', 'cHl1McHu', 'cHl1Mced', 'cHl1Mceu', 'cHl1Mcje', 'cHl1Mcld', 'cHl1Mclj1', 'cHl1Mclj3', 'cHl1Mcll1', 'cHl1Mclu', 'cHl3McHDD', 'cHl3McW', 'cHl3McHWB', 'cHl3McHd', 'cHl3McHe', 'cHl3McHj1', 'cHl3McHj3', 'cHl3McHl1', 'cHl3McHu', 'cHl3Mced', 'cHl3Mceu', 'cHl3Mcje', 'cHl3Mcld', 'cHl3Mclj1', 'cHl3Mclj3', 'cHl3Mcll1', 'cHl3Mclu', 'cHuMcHDD', 'cHuMcW', 'cHuMcHWB', 'cHuMcHd', 'cHuMcHe', 'cHuMcHj1', 'cHuMcHj3', 'cHuMcHl1', 'cHuMcHl3', 'cHuMced', 'cHuMceu', 'cHuMcje', 'cHuMcld', 'cHuMclj1', 'cHuMclj3', 'cHuMcll1', 'cHuMclu', 'cedMcHDD', 'cedMcW', 'cedMcHWB', 'cedMcHd', 'cedMcHe', 'cedMcHj1', 'cedMcHj3', 'cedMcHl1', 'cedMcHl3', 'cedMcHu', 'cedMceu', 'cedMcje', 'cedMcld', 'cedMclj1', 'cedMclj3', 'cedMcll1', 'cedMclu', 'ceuMcHDD', 'ceuMcW', 'ceuMcHWB', 'ceuMcHd', 'ceuMcHe', 'ceuMcHj1', 'ceuMcHj3', 'ceuMcHl1', 'ceuMcHl3', 'ceuMcHu', 'ceuMced', 'ceuMcje', 'ceuMcld', 'ceuMclj1', 'ceuMclj3', 'ceuMcll1', 'ceuMclu', 'cjeMcHDD', 'cjeMcW', 'cjeMcHWB', 'cjeMcHd', 'cjeMcHe', 'cjeMcHj1', 'cjeMcHj3', 'cjeMcHl1', 'cjeMcHl3', 'cjeMcHu', 'cjeMced', 'cjeMceu', 'cjeMcld', 'cjeMclj1', 'cjeMclj3', 'cjeMcll1', 'cjeMclu', 'cldMcHDD', 'cldMcW', 'cldMcHWB', 'cldMcHd', 'cldMcHe', 'cldMcHj1', 'cldMcHj3', 'cldMcHl1', 'cldMcHl3', 'cldMcHu', 'cldMced', 'cldMceu', 'cldMcje', 'cldMclj1', 'cldMclj3', 'cldMcll1', 'cldMclu', 'clj1McHDD', 'clj1McW', 'clj1McHWB', 'clj1McHd', 'clj1McHe', 'clj1McHj1', 'clj1McHj3', 'clj1McHl1', 'clj1McHl3', 'clj1McHu', 'clj1Mced', 'clj1Mceu', 'clj1Mcje', 'clj1Mcld', 'clj1Mclj3', 'clj1Mcll1', 'clj1Mclu', 'clj3McHDD', 'clj3McW', 'clj3McHWB', 'clj3McHd', 'clj3McHe', 'clj3McHj1', 'clj3McHj3', 'clj3McHl1', 'clj3McHl3', 'clj3McHu', 'clj3Mced', 'clj3Mceu', 'clj3Mcje', 'clj3Mcld', 'clj3Mclj1', 'clj3Mcll1', 'clj3Mclu', 'cll1McHDD', 'cll1McW', 'cll1McHWB', 'cll1McHd', 'cll1McHe', 'cll1McHj1', 'cll1McHj3', 'cll1McHl1', 'cll1McHl3', 'cll1McHu', 'cll1Mced', 'cll1Mceu', 'cll1Mcje', 'cll1Mcld', 'cll1Mclj1', 'cll1Mclj3', 'cll1Mclu', 'cluMcHDD', 'cluMcW', 'cluMcHWB', 'cluMcHd', 'cluMcHe', 'cluMcHj1', 'cluMcHj3', 'cluMcHl1', 'cluMcHl3', 'cluMcHu', 'cluMced', 'cluMceu', 'cluMcje', 'cluMcld', 'cluMclj1', 'cluMclj3', 'cluMcll1'

#ops=['all'] #'cnb','c3wMcnb','cwMcnb'] #'cW','clu','cw','c3w','cb','c3wMcw','c3wMcb','cwMcb','']#,'']#,'']#'cw','c3w','cb']#,'cb','cHDD','clu','cW']'all']#


nT=False

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
#os.system('condor_submit jobs/%s'%fName)


#python plots_VVsemilep.py --results --sel plots --year ${2} --nLep ${3} --finalState ${4} --pv ${5} --pf ${6}
##fixme suboptimal for the case with pf and ops
#python plots_VVsemilep.py --results --finalState boosted --nLep 1 --sel SR --pv mWV1_typ0_pmet_boosted  --lf mu --lf el --year 2018 --dW plots --applylepSFs --WC cwww --WC ccw --WC cb
## python plots_VVsemilep.py --results --dW cards --year 2016 --finalState elmu --finalState mumu --applylepSFs 
