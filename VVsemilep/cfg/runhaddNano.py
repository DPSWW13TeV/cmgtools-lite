import os,sys
import subprocess


eospath="/eos/cms/store/cmst3/group/dpsww/" #/eos/cms/store/group/phys_smp/ec/anmehta/"
indir="aTGC_Apr2024_UL16" #/eos/cms/store/cmst3/group/dpsww/"
odir= "Combined_aTGC_Oct2024_UL16"
samples=[]
sample=sys.argv[1]
samples.append(sample)


for iproc in samples:
    newName=iproc.split('_4f_NLO_FXFX')[0].replace('-','_')
    print "running for process",newName
    basepath_private=os.path.join(eospath,indir,iproc)
    outdir=os.path.join(eospath,odir,newName)#  basepath_private #+"_hadded"
    if not  os.path.exists(outdir):
        os.system("mkdir -p %s"%outdir)
    files=[os.path.join(basepath_private,x) for x in os.listdir(basepath_private) if os.path.isfile(os.path.join(basepath_private, x)) ]
    maxSize=30
    tot_size=0;
    subtasks={};    elements=[];
    print 'tot number of files %d'%len(files)

    for i in files:
        tot_size+=os.path.getsize(i);
        if(tot_size < maxSize*(1024.**3) and len(elements) < 1000):
            elements.append(i)
            if i == files[-1]:
                #ikey=str(outdir+'/'+iproc+'_part'+str(len(subtasks)))
                ikey=str(outdir+'/'+newName+'_part'+str(len(subtasks)))
                subtasks[ikey]=elements;
            else:
                continue
        else:
            ikey=str(outdir+'/'+iproc+'_part'+str(len(subtasks)))
            subtasks[ikey]=elements;
            elements=[i]; tot_size=os.path.getsize(i);
            continue;


    for ikey,ival in subtasks.iteritems():
    
        if len(subtasks) == 1 :
            print "in here"
            oname=ikey.split('_part')[0]
            print ikey,ival
            print(["haddnano.py", oname+".root" ] + ival) 
            subprocess.call(["haddnano.py", oname+".root" ] + ival)
        else:
            #        print ikey,len(ival)
            print(["haddnano.py", ikey+".root" ] + ival)
            subprocess.call(["haddnano.py", ikey+".root" ] + ival)

#WmWpToLmNujj_01j_aTGC_pTW-150toInf_mWV-150to600_4f_NLO_FXFX
