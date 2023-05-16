import os,string

indir="/eos/cms/store/group/phys_smp/anmehta/Zh_had_chiral/"
files=[x for x in os.listdir(indir) if os.path.isfile(os.path.join(indir, x))]
outdir="/pnfs/desy.de/cms/tier2/store/user/anmehta/ZH_had_2016/"
tmp_condor = open('logs/submitFile.condor', 'w')
tmp_condor.write('''Executable = dummy_copy_eos_dCache.sh
use_x509userproxy = true
Log        = logs/log_running_$(ProcId).log                                                                                     
Error      = logs/log_running_$(ProcId).error                                                                                   
+JobFlavour = "microcentury"
\n\n''')
for fIn in files:
    tmp_condor.write('arguments = {indir} {fName} {outdir} \n'.format(indir=indir,outdir=outdir,fName=fIn ) )
    tmp_condor.write('queue 1\n\n')

tmp_condor.close()

print 'condor_submit logs/submitFile.condor'
#os.system('condor_submit logs/submitFile.condor')



