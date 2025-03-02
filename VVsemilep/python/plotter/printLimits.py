import optparse, subprocess, datetime, math, array, copy, os, re, sys,shutil
lumis = {
    '2016APV': '19.5', #with HIPM
    '2016': '16.8', #without HIPM
    '2017': '41.5',
    '2018': '59.8',
    'run2': '137.6',
    'fullRun2': '137.6',
    '2016combo': '36.3',
}
plots_odir="/eos/user/a/anmehta/www/VVsemilep/EFT_nllscans/"
limit={};
nicename={'cb':'\\cb', 'cw':'\\cw','c3w':'\\cwww'}
ops=['cb','c3w','cw']
yrs=['2016','2017','2018','fullRun2']#,'2016combo']
for op in ops: 
    for yr in yrs: 
        print('op and yr',op,yr)
        cmd="mkEFTScan.py" # higgsCombine.{op}.individual.MultiDimFit.mH125.root  -p k_{op}  -lumi lumis[{yr}] -cms -preliminary -o {plots_odir}/scan_{op}_{yr}" #.png"
        output = subprocess.check_output(cmd, shell=True)
        #        print(output,type(output))
        limit[op+'_'+yr+'_1sig']=str(output).split('more')[0].replace('b\'','')
        limit[op+'_'+yr+'_2sig']=str(output).split('more')[-1].replace('\\n\'','')
        print(str(output).split('more')[0].replace('b\'',''),str(output).split('more')[-1].replace('\\n\'',''))


txtfilename = "{od}/table.txt".format(od=os.getcwd())
txtfile = open(txtfilename,'w')
fmtstring = "%-25s & %15s & %15s & %15s & %15s  & %15s  %15s & %15s & %15s \n \\\\"
txtfile.write("\\begin{table}[ht!] \n \\begin{tabular}{lllllllll}\n \\hline\\hline\n\n \\ \\cline{2-9} \n")
txtfile.write("\multicolumn{1}{l|}{\multirow{2}{*}{Parameter}} & \multicolumn{4}{l|}{Expected limits at 68\% CL} & \multicolumn{4}{l|}{Expected limits at 95\% CL} \\\\ \\cline{2-9} \n")
txtfile.write("\multicolumn{1}{l|}{}                           & 2016       & 2017       & 2018      & Run2      & 2016       & 2017       & 2018      & Run2      \\ \n")

for op in ops:
    txtfile.write(fmtstring %(nicename[op],limit[op+'_2016combo_1sig'],limit[op+'_2017_1sig'],limit[op+'_2018_1sig'],limit[op+'_fullRun2_1sig'],limit[op+'_2016combo_2sig'],limit[op+'_2017_2sig'],limit[op+'_2018_2sig'],limit[op+'_fullRun2_2sig']))
    #txtfile.write(fmtstring %(op,limit[op+'_2016_1sig'],limit[op+'_2017_1sig'],limit[op+'_2018_1sig'],limit[op+'_fullRun2_1sig'],limit[op+'_2016_2sig'],limit[op+'_2017_2sig'],limit[op+'_2018_2sig'],limit[op+'_fullRun2_2sig']))
    txtfile.write(" \n \\hline \n")
txtfile.write(" \\hline\n\end{tabular} \n")
txtfile.write(" \\caption{\caption{Expected limits on the aTGC-parameters at 68\% and 95\% confidence levels.}\\label{tab:limitsEFT}")
txtfile.write(" \n \end{table}\n")
txtfile.close()
