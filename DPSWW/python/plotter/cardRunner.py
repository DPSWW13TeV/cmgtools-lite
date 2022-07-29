#!/usr/bin/env python
import optparse, subprocess, datetime, math, array, copy, os, re, sys

year=sys.argv[1]
#bS=sys.argv[2]
date=datetime.date.today().isoformat() #"2021-12-02" #
csplit=True
extra="" #_bb17c50f50" #_VGN50"
bS2lss="SoBord_sqV3"+extra #sys.argv[2]+extra #
bS3l="m3l"+extra
bS4l="m4l"+extra
baseDir=os.getcwd()
combdir='Cards/combination/'
outdir=os.path.join(baseDir,combdir)
print outdir
##amoutext=${year}${ppf}.txt
##amext=${year}.txt
##ampf="2021-11-03-SoBord_sqV3"

#txtfilename = "{od}/expsig{nameIt}".format(od=outdir,nameIt=date+"-"+bS2lss+bS3l+bS4l)
#txtfile = open(txtfilename,'w')


fitopts={
'expsig': "-M Significance -t -1 --expectSignal=1",
'obs':   "-M Significance",
'fit_and_pulls': " -M FitDiagnostics --saveShapes --saveNormalizations --saveWithUncertainties"
}


def makeCards(yr,chrgsplt=True,opt='expsig'):
    pf=str(date+"-"+bS2lss)
    pfwz=str(date+"-"+bS3l)
    pfzz=str(date+"-"+bS4l)
    cspf='_cs' if chrgsplt else ''
    finalDC='dc_{pf}_ll_noee_{yr}{cg}_combined.txt'.format(pf=str(date+"-"+bS2lss+bS3l+bS4l),yr=yr,cg=cspf)
    if chrgsplt:
        cmd1 = 'combineCards.py elmu_mm_{year}=Cards/cards_{pf}_elmu_{year}/elmu{year}minusminus.txt elmu_pp_{year}=Cards/cards_{pf}_elmu_{year}/elmu{year}plusplus.txt mumu_mm_{year}=Cards/cards_{pf}_mumu_{year}/mumu{year}minusminus.txt mumu_pp_{year}=Cards/cards_{pf}_mumu_{year}/mumu{year}plusplus.txt wz_cr_{year}=Cards/cards_{pfwz}_cr3l_{year}/cr3l{year}.txt zz_cr_{year}=Cards/cards_{pfzz}_cr4l_{year}/cr4l{year}.txt > {dc}'.format(year=yr,dc=finalDC,pf=pf,pfwz=pfwz,pfzz=pfzz)
        os.system(cmd1)
    else:
        cmd1='combineCards.py elmu_{year}=Cards/cards_{pf}_elmu_{year}/elmu{year}.txt mumu_{year}=Cards/cards_{pf}_mumu_{year}/mumu{year}.txt wz_cr_{year}=Cards/cards_{pfwz}_cr3l_{year}/cr3l{year}.txt zz_cr_{year}=Cards/cards_{pfzz}_cr4l_{year}/cr4l{year}.txt > {dc}'.format(year=yr,dc=finalDC,pf=pf,pfwz=pfwz,pfzz=pfzz)
        os.system(cmd1)
    dC = open(finalDC, 'a')
    dC.write('''norm_WZ       rateParam *{yr}  WZ 1 [0,5]
norm_ZZ       rateParam *{yr}  ZZ 1 [0,5]'''.format(yr=yr))
    dC.close()
    #txtfile.write('running emu  combined %s'%yr)
    #txtfile.write('\n')
    runCombine='combine -M Significance  {finalDC}  -t -1 --expectSignal=1 '.format(finalDC=finalDC)#,txt=txtfilename)
    print '=============================================='
    print 'running for emu+mumu combined %s'%yr
    os.system(runCombine)
    print '=============================================='
    #txtfile.write('-----------------------------------------------\n')    
    for fs in ["elmu","mumu"]:
        FSdc='dc_%s_%s%s%s_combined.txt'%(pf,fs,yr,cspf)
        if chrgsplt:
            cmdfs= 'combineCards.py {fs}_mm_{year}=Cards/cards_{pf}_{fs}_{year}/{fs}{year}minusminus.txt {fs}_pp_{year}=Cards/cards_{pf}_{fs}_{year}/{fs}{year}plusplus.txt wz_cr_{year}=Cards/cards_{pfwz}_cr3l_{year}/cr3l{year}.txt zz_cr_{year}=Cards/cards_{pfzz}_cr4l_{year}/cr4l{year}.txt > {dc}'.format(year=yr,fs=fs,dc=FSdc,pf=pf,pfwz=pfwz,pfzz=pfzz)
            os.system(cmdfs)
        else:
            cmdfs= 'combineCards.py {fs}_{year}=Cards/cards_{pf}_{fs}_{year}/{fs}{year}.txt wz_cr_{year}=Cards/cards_{pfwz}_cr3l_{year}/cr3l{year}.txt zz_cr_{year}=Cards/cards_{pfzz}_cr4l_{year}/cr4l{year}.txt > {dc}'.format(year=yr,fs=fs,dc=FSdc,pf=pf,pfwz=pfwz,pfzz=pfzz)
            os.system(cmdfs)
        fscard= open(FSdc, 'a')
        fscard.write('''norm_WZ       rateParam *{yr}  WZ 1 [0,5]
norm_ZZ       rateParam *{yr}  ZZ 1 [0,5]'''.format(yr=yr))
        fscard.close()
        runCombine='combine -M Significance  {finalDC}  -t -1 --expectSignal=1'.format(finalDC=FSdc)
        print 'running for %s  %s'%(fs,yr)
        print '=============================================='
        os.system(runCombine)
        print '=============================================='
    return finalDC



if year == "all":
    dC16=makeCards("2016",csplit)
    dC17=makeCards("2017",csplit)
    dC18=makeCards("2018",csplit)
    cspf='_cs' if csplit else ''
   
    superdC='dc_{pf}_ll_noee_FR2{cspf}_combined.txt'.format(cspf=cspf,pf=str(date+"-"+bS2lss+bS3l+bS4l))
    cmd='combineCards.py {yr1} {yr2} {yr3} > {dc}'.format(dc=superdC,yr1=dC16,yr2=dC17,yr3=dC18)
    os.system(cmd)
    runCombine='combine -M Significance  {finalDC}  -t -1 --expectSignal=1'.format(finalDC=superdC)
    os.system(runCombine)
    os.system('mv dc*txt {od}/'.format(od=outdir))
    
else:
     dataCard=makeCards(year,csplit)
     os.system('mv dc*txt {od}/'.format(od=outdir))

    #txtfile.close()

##am    mv ${emuCombDC} ${combDir}/
##am    mv ${finalDC} ${combDir}/

#combineCards.py Cards/cards_2021-11-23-SoBord_sqV3_mumu_2016/mumu2016plusplus.txt Cards/cards_2021-11-23-SoBord_sqV3_mumu_2016/mumu2016minusminus.txt Cards/cards_2021-11-23-m3l_cr3l_2016/cr20163l.txt  Cards/cards_2021-11-23-m4l_cr4l_2016/cr20164l.txt > dc_2021-11-23-SoBord_sqV3m3lm4l_mumu_2016.txt
#norm_WZ       rateParam *  WZ 1 [0,5]
#norm_ZZ       rateParam *  ZZ 1 [0,5]

