import ROOT, os, optparse, copy


#datacards = {}


#datacards['topCR']   = 'dc_2025-02-11_onelep_fullRun2_topCR.txt' 
#datacards['wjCR' ] = 'dc_2025-02-11_onelep_fullRun2_wjCR.txt'

#datacards['2017' ] = 'dc_2021-12-23-SoBord_sqV3m3lm4l_ll_noee_2017_cs_combined.txt'
#datacards['2018' ] = 'dc_2021-12-23-SoBord_sqV3m3lm4l_ll_noee_2018_cs_combined.txt'


def makeAllToys(periods, crs,algos):

    for period in periods:
        for cr in crs:
            dc='dc_2025-02-11_onelep_{period}_{cr}.txt'.format(period=period,cr=cr)
            outdir = 'toystudies_'+cr+"_"+period
            os.system('mkdir -p {od}'.format(od=outdir))
    
            for algo in algos:
        
                rr = range(1,options.njobs+1)
        
                ## run separately to circumvent the memory leak problem
                for i in rr:
                    cmd = 'combine -M GoodnessOfFit {dc} --algo={algo} -t {n} -s {i}'.format(algo=algo, i=i, n=options.nperj, dc=dc)
                    if algo == 'saturated':
                        cmd+= ' --toysFreq '
                    os.system(cmd)
        
                allfiles = ' '.join(['higgs*.mH120.'+str(ns)+'.root' for ns in rr])
                print 'this is allfiles', allfiles
                haddcmd = 'hadd {od}/oldcombine_GOF_1000toys_{algo}.root {fs}'.format(algo=algo, fs = allfiles, od=outdir)
                os.system(haddcmd)
            
                os.system('mkdir -p {od}/toys_{algo}'.format(algo=algo,od=outdir))
    
                ## move all the single files with toys in a subdir
                for i in allfiles.split():
                    os.system('mv {i} {od}/toys_{algo}/'.format(i=i, algo=algo, od=outdir))
        
            
                ## run the fit on data to get the reference
                cmd = 'combine -M GoodnessOfFit {dc} --algo={algo} '.format(algo=algo, dc=dc)
                os.system(cmd)
                os.system('mv higgsCombineTest.GoodnessOfFit.mH120.root {od}/oldcombine_GOF_data_{algo}.root'.format(algo=algo, od=outdir))

def makePlots(periods, crs,algos):

    ROOT.gROOT.SetBatch()
    ROOT.gStyle.SetOptStat(0)

    arrow = ROOT.TArrow(); arrow.SetLineWidth(2); arrow.SetLineColor(ROOT.kBlack)
    latex = ROOT.TLatex(); latex.SetTextFont(42); latex.SetTextSize(0.05)

    canv = ROOT.TCanvas()
    for ip,period in enumerate(periods):
        for ic,cr in enumerate(crs):
            for ia,algo in enumerate(algos):
                ftoys = ROOT.TFile('toystudies_{cr}_{p}/oldcombine_GOF_1000toys_{algo}.root'.format(cr=cr,p=period,algo=algo),'read')
                fdata = ROOT.TFile('toystudies_{cr}_{p}/oldcombine_GOF_data_{algo}.root'    .format(cr=cr,p=period,algo=algo),'read')
                ttoys = ftoys.Get('limit'); tdata = fdata.Get('limit')

                minval, maxval = 1e12, -1
                for ev in tdata:
                    val_data = ev.limit
                for ev in ttoys:
                    if ev.limit < minval:
                        minval = ev.limit
                    if ev.limit > maxval:
                        maxval = ev.limit

                h_tmp = ROOT.TH1F('h_'+algo+'_'+cr+'_'+period, algo+' '+(period if '201' in period else 'FR2'), 50, 0.9*min(minval,val_data), 1.1*max(maxval,val_data))
                h_tmp.GetXaxis().SetTitle(algo+' values')
                h_tmp.GetYaxis().SetTitle('frequency of toys')
                ttoys.Draw('limit>>{hn}'.format(hn=h_tmp.GetName()))
                h_tmp.Scale(1./h_tmp.Integral())
                h_tmp.Draw()
                mean = h_tmp.GetMean()
                rms  = h_tmp.GetRMS()
                #print val_data,h_tmp.GetXaxis().FindBin(val_data)
                pval=h_tmp.Integral(h_tmp.GetXaxis().FindBin(val_data),h_tmp.GetNbinsX()+1)
                print pval
                pvalue = ROOT.TPaveText(0.68, 0.83, 0.80, 0.87, "NDC")
                pvalue.SetBorderSize(   0 )
                pvalue.SetFillStyle (   0 )
                pvalue.SetTextAlign (  32 )
                pvalue.SetTextSize  (0.04 )
                pvalue.SetTextColor (   1 )
                pvalue.SetTextFont  (  62 )
                pvalue.AddText("p-value = %0.3f"%pval)
                pvalue.Draw()
                arrow.SetLineStyle(1); arrow.SetLineColor(ROOT.kBlack)
                latex.SetTextColor(ROOT.kBlack)
                arrow.DrawArrow(val_data, 0.03 , val_data, 0, 0.04, '|->')
                latex.DrawLatex(val_data, 0.035, 'data')

                arrow.SetLineColor(ROOT.kGreen-2)
                arrow.DrawArrow(mean, 0.03, mean, 0, 0.04, '|->')
                latex.SetTextColor(ROOT.kGreen-2)
                latex.DrawLatex(mean*0.9, 0.031, 'mean')
                arrow.SetLineStyle(2)
                #arrow.SetLineColor(ROOT.kBlue)
                #arrow.DrawArrow(mean+rms, 0.03, mean+rms, 0, 0.04, '-')
                #arrow.DrawArrow(mean-rms, 0.03, mean-rms, 0, 0.04, '-')
                outdir="/eos/user/a/anmehta/www/VVsemilep/GOFs/" #/eos/user/a/anmehta/www/datacard_review/unblinding/gofTests/
                canv.SaveAs('{od}/gofTest{n}_{cr}_{p}_{a}.png'.format(cr=cr,p=period,a=algo,n=name,od=outdir)) 
                canv.SaveAs('{od}/gofTest{n}_{cr}_{p}_{a}.pdf'.format(cr=cr,p=period,a=algo,n=name,od=outdir)) 


                #                os.system('cp ~/public/index.php {od}'.format(od=outdir))
            


if __name__ == '__main__':
    parser = optparse.OptionParser(usage='usage: %prog [opts] ', version='%prog 1.0')
    parser.add_option('--doToys' , action='store_true' , default=False , help='remake all the toys')
    parser.add_option('--doPlots', action='store_true' , default=False , help='make all the plots')
    parser.add_option('--period' , type=str, default='all', help='specify a certain period, either 2016,2017,super,all. default %default')
    parser.add_option('--postfix', type=str, default=''   , help='postfix for the name of the output file. default %default')
    parser.add_option('--algo'   , type=str, default='saturated', help='specify an algorithm. comma separated list. default %all')
    parser.add_option('--njobs'  , type=int, default=20   , help='number of jobs, default %default')
    parser.add_option('--nperj'  , type=int, default=50   , help='number of toys per job. default %default')
    parser.add_option('--cr' ,     type=str, default='all', help='specify a control region either wj/top/all. default %default')
    ##parser.add_option('--outdir' , type=str, default='all', help='specify a certain period, either 2016,2017,super,all. default %default')
    (options, args) = parser.parse_args()

    global name
    name = '' if not options.postfix else '_'+options.postfix


    if options.period == 'all': 
        periods = ['fullRun2', '2017', '2016','2018']
    else:
        periods = options.period.split(',')
    if options.cr == 'all': 
        crs = ['topCR','wjCR'] 
    else:
        crs = options.cr.split(',')

    if options.algo == 'all':
        algos = ['saturated', 'KS', 'AD']
    else:
        algos = options.algo.split(',')

    if options.doToys:
        makeAllToys(periods, crs,algos)
    
    if options.doPlots:
        makePlots(periods, crs,algos)
