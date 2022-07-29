import os,re,optparse,sys

processes={
    'DPSWW':'\dps',
    'Rares':'Rares',
    'ZZ':'\ZZ',
    'WZ':'\WZ',
    'Convs':'\WZg',
    'data_fakes':'nonprompt',
    'Wgstar':'\WGs',
    'data_flips':'charge-misid.',
    'VVV':'VVV',
    'total_background':'tot. bkg.',
    'data':'data'
    
}

yields={};
fit=sys.argv[1]
#fIn=open("see_%sfit_ylds.txt"%fit,"r");
fIn=open("%sfit_ylds_feb10.txt"%fit,"r");

FS=["mumu_pp","mumu_mm","elmu_pp","elmu_mm"]
yrs=['2016','2017','2018']
for p in processes.keys():
    yields[p]={}
    for fs in FS:
        yields[p][fs]=(0.0,0.0)

for line in fIn:
    #print line.split()[3]
    FS=line.split()[0];proc=line.split()[1];yld=line.split()[2];err=line.split()[3];
    if proc in processes.keys():
        row= "$%.2f\pm%.2f$" % (float(yld),float(err))
        yields[proc][FS]=row
    else: continue


print yields

txtfilename = "{od}/table_{fit}fit.txt".format(fit=fit,od=os.getcwd())
txtfile = open(txtfilename,'w')
fmtstring = "%-20s & %15s & %15s & %15s & %15s  \\\\"

txtfile.write( "\\begin{table}[ht!] \n \\begin{tabular}{ l c c c c c} \\hline \n")
txtfile.write("& $\Pep\Pgmp$      & $\Pem\Pgmm$       & $\Pgmp\Pgmp$     & $\Pgmm\Pgmm$     \\\\ \\hline \n")


for proc in processes.keys():

#for proc,pName in yields.iteritems():
    mumu_pp= yields[proc]['mumu_pp']
    mumu_mm= yields[proc]['mumu_mm']
    emu_pp= yields[proc]['elmu_pp']
    emu_mm= yields[proc]['elmu_mm']

    txtfile.write( fmtstring % (processes[proc],emu_pp,emu_mm,mumu_pp,mumu_mm))
    txtfile.write(" \\hline \n")
txtfile.write(" \\hline\n\end{tabular}\n")
txtfile.close()
