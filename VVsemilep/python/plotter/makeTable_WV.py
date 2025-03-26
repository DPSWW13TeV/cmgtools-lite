import ROOT, os
procs={0:['WJets','\Wj'],1:['tt',"\\ttbar"],
       2:['singletop','single t'],3:['WW_sm','\WW'],4:['WZ_sm','\WZ'],5:['Others','Others'],6:['background','Tot. bkg.'],
       7:['data','data']}
nice_names={'wjCR_incl':'\\WJ control region', 'topCR_incl' :'\\ttbar control region', 'sig_incl': 'signal region', 'el': 'electron','mu':'muon'}

finalState=['mu','el']#,'ll_noee']
classifier='mWV' 
years=['2016APV','2016','2017','2018','fullRun2']
dateStamp="2025-03-07"
info={}
pf="_all_eft"

txtfilename = "{od}/table.txt".format(od=os.getcwd())
txtfile = open(txtfilename,'w')
fmtstring = "%-25s & %15s & %15s & %15s & %15s  & %15s \\\\"

for reg in ["wjCR_incl","topCR_incl","sig_incl"]: #
    for lep in finalState:
        for yr in years:
            baseDir="/eos/user/a/anmehta/www/VVsemilep/{yr}/{reg}/{dateStamp}_boosted_{lep}_{breg}{pf}/".format(pf=pf,yr=yr,lep=lep,breg=reg,reg=reg.split("_")[0],dateStamp=dateStamp)
            fstr="%s.root"%classifier
            print(baseDir+fstr)
            fOpen=ROOT.TFile.Open(baseDir+fstr,"read")
            for proc,pName in procs.items():
                if ("sig" in reg  and pName[0] == "data" ):
                    row=""
                else:
                    hist=classifier+"_"+pName[0]
                    
                    h1=fOpen.Get(hist)
                    if not h1: 
                        hist=classifier+"_logy_"+pName[0]
                        h1=fOpen.Get(hist)
                    print(h1.GetName())
                    h1_err = ROOT.Double(0.)
                    h1_int = h1.IntegralAndError(0, h1.GetNbinsX() + 1, h1_err)
                    row = "$%.2f\pm%.2f$" % (h1_int,h1_err)

                info.update({pName[0]+"-"+lep+"-"+yr:row})

        txtfile.write("\\begin{table}[ht!] \n \\begin{tabular}{llllll}\n \\hline\\hline\n\n")
        txtfile.write("\multicolumn{1}{c}{\multirow{2}{*}{Process}} & \multicolumn{5}{c}{Event yields}    \\\\ \\cline{2-6} \n")
        txtfile.write("\\multicolumn{1}{c}{}                         & 2016APV & 2016 & 2017 & 2018 & Run2 \\\\ \\hline \n")

        for proc,pName in procs.items():
            yld_2016APV=info[pName[0]+"-"+lep+"-2016APV"]
            yld_2016=info[pName[0]+"-"+lep+"-2016"]
            yld_2017=info[pName[0]+"-"+lep+"-2017"]
            yld_2018=info[pName[0]+"-"+lep+"-2018"]
            yld_Run2=info[pName[0]+"-"+lep+"-fullRun2"]
            if ("sig" in reg  and pName[0] == "data" ):                 continue;

            txtfile.write(fmtstring % (pName[1],yld_2016APV,yld_2016,yld_2017,yld_2018,yld_Run2))
            txtfile.write(" \\hline \n")

        txtfile.write(" \\hline\n\end{tabular} \n")
        txtfile.write(" \\caption{Event yields in the %s for the %s channel}\\label{tab:%s_%s}"%(nice_names[reg],nice_names[lep],reg,lep))
        txtfile.write(" \n \end{table}\n")
txtfile.close()

##am
##am\begin{tabular}{ccccccc}
##am\hline\\
##am              & \multicolumn{2}{c}{2016}            & \multicolumn{2}{c}{2017}           & \multicolumn{2}{c}{2018}  \\
##am              & \emu        & \mumu            & \emu         & \mumu            & \emu         & \mumu \\ \hline \hline \\
##amDPS \WpmWpm  & 51.69$\pm$2.50   & 54.47$\pm$2.24   & 69.63$\pm$4.28    & 62.46$\pm$4.01   & 76.95$\pm$3.77   & 79.30$\pm$3.51\\
##amcharge misid.& 24.17$\pm$4.05   & --               & 13.55$\pm$2.50    &  --              & 11.64$\pm$2.45   & --\\
##amRares        & 32.83$\pm$14.11  & 30.00$\pm$12.85  & 43.85$\pm$18.88   & 34.69$\pm$14.97  & 65.24$\pm$28.03  & 55.35$\pm$23.74\\
##am\ZZ          & 35.04$\pm$7.61   & 43.78$\pm$9.40   & 36.89$\pm$6.26    & 41.68$\pm$7.09  & 54.03$\pm$9.04   & 63.35$\pm$10.51\\
##am\WGs         & 69.45$\pm$29.79  & 65.83$\pm1$28.17 & 86.43$\pm$37.06   & 68.23$\pm$29.27  & 114.54$\pm$49.12 & 103.54$\pm$44.34\\
##am\WZ          & 510.92$\pm$76.18 & 471.84$\pm$68.91 & 635.03$\pm$94.69  & 530.81$\pm$79.39 & 915.15$\pm$136.05 & 811.42$\pm$119.23\\
##am\WZg         & 232.31$\pm$63.78 & --               & 184.96$\pm$52.10  & --               & 265.74$\pm$74.22 & --\\
##amnon-prompt  & 259.60$\pm$78.29 & 233.97$\pm$86.61  & 309.50$\pm$101.02 & 207.67$\pm$70.28 & 640.18$\pm$205.31 & 312.80$\pm$111.62\\\hline\\
##amtot. bkg. & 1163.32$\pm$135.25 & 845.42$\pm$116.25 & 1310.21$\pm$158.21 & 883.08$\pm$113.06 & 2066.51$\pm$267.97 & 1346.47$\pm$173.18\\\\\hline
##am\end{tabular}
##am}
