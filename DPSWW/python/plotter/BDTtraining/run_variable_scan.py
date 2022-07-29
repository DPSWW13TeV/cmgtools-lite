import ROOT, re, os, subprocess, sys, string
allFiles=[]

variables={
'allvars':'',
#'dz': 'deltadz',
#'dxy': 'deltadxy',
##am'pt1':'pt1',
##am'pt2':'pt2',
##am'met':'met := met',
##am'mt2':'mt2',
##am'mtll':'mtll',
##am'mtl1':'mtl1met',
##am'dphill':'dphill',
##am'dphil2met':'dphil2met',
##am'dphilll2':'dphilll2',
'etaprod':'etaprod',
'etasum':'etasum',
'etadiff':'etadiff',
    
##am'dR':'deltaR(Lep1_eta,Lep1_phi,Lep2_eta,Lep2_phi)'
#'cptll':'cptll',
#'mll':'mll :=mll',
#'deltaz':'deltaz := abs(LepGood_dz[iLepFO_Recl[0]]-LepGood_dz[iLepFO_Recl[1]])',
#'deltaxy':'deltaxy := abs(LepGood_dxy[iLepFO_Recl[0]]-LepGood_dxy[iLepFO_Recl[1]])'
}

odir='/eos/cms/store/cmst3/group/dpsww/BDT_optimization/'
templates=['classification']
for iv,ivar in variables.iteritems():
    for cat in templates: 
        #fIn = open("tmvaProducer_{here}_withptll.py".format(here=cat),"r")
        fIn = open("test_all.py","r")
        if len(ivar) > 0:
            py_str = 'logs/tmvaProducer_{HERE}_allbut_{here}.py'.format(HERE=cat,here=iv) 
        else:
            py_str = 'logs/tmvaProducer_{HERE}_allvars.py'.format(HERE=cat)
        pyfile = open(py_str,'w')
        for line in fIn.readlines():
            if ivar in line and len(ivar) > 0:
                line=line.replace('AddVariable','AddSpectator');
            pyfile.write(line)
        pyfile.close()
        allFiles.append(py_str)
        #    cmd='python {pyfile} {od}allvars_but_{vN}'.format(pyfile=py_str,vN=iv,od=outdir)
#    print cmd
tmp_condor = open('logs/submitFile.condor', 'w')
tmp_condor.write('''Executable = dummy_scan.sh                                                                       
use_x509userproxy = true                                                                                                        
getenv      = True                                                                                                              
Log        = logs/log_running_$(ProcId).log                                                                               
Output     = logs/log_running_$(ProcId).out                                                                               
Error      = logs/log_running_$(ProcId).error                                   
environment = "LS_SUBCWD={here}"
+MaxRuntime = 14500 \n\n'''.format(here=os.environ['PWD']))
for bkg in ['wz_amc','fakes']:
    for yr in ['2016','2017','2018']:
        for ifile in allFiles:
            fOut = str(ifile.split('tmvaProducer_classification_')[-1].replace('.py',''))
            tmp_condor.write('arguments = {where} {pyfile} {yr} {bkg} {spltxt} {outdir} \n'.format(where=os.environ['PWD'],pyfile=os.environ['PWD']+'/'+ifile,outdir=odir,spltxt=fOut,yr=yr,bkg=bkg) )
            tmp_condor.write('queue 1\n\n')

tmp_condor.close()

print 'condor_submit logs/submitFile.condor'
