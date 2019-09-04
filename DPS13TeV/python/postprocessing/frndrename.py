#!/usr/bin/env python                                                                                                                           
import os, sys
import ROOT
eospath = 'Friends_BDT_with_tight_MVA_2016/'
outputdir='Friends_BDT_with_tight_MVA_2016_renamed/'
list1=( list( i for i in os.listdir(eospath) ) ) 

for name in list1:
    name1=name.split('_treeProducerSusyMultilepton_')[-1] 
    cmd='cp {indir}{infile} {outdir}{outfile}'.format(indir=eospath,outdir=outputdir,infile=name,outfile=name1)
    print cmd
    os.system(cmd)
    
