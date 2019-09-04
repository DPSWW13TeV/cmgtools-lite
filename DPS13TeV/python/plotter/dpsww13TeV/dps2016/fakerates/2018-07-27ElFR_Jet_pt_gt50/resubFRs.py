import os, optparse

parser = optparse.OptionParser(usage='usage: %prog [opts] ', version='%prog 1.0')
parser.add_option('-s'        , '--submit'    , dest='submit'      , action='store_true' , default=False , help='actually submit the jobs')
(opts, args) = parser.parse_args()


frfiles   = 0
nofrfiles = 0

resubcommands = []

p = os.path.abspath('.')

for d in os.listdir(p):
    if not os.path.isdir(os.path.join(p,d)): continue
    hasFRfile = False
    for f in os.listdir(os.path.join(p,d)):
        if 'fr_mu_{d}.pdf'.format(d=d) in f:
            hasFRfile = True
    if hasFRfile:
        frfiles += 1
        print 'directory {d} has a FR file'.format(d=d)
    else:
        for f in os.listdir(os.path.join(p,d,'jobs')): #'./'+d+'/jobs/'):
            if '.sh' in f:
                shfile = os.path.join(p,d,'jobs',f) #'./'+d+'/jobs/'+f
        tmp_cmd = 'bsub -q 1nd -o {log} {sh}'.format(log=shfile.replace('.sh', '_resub.log'), sh=shfile)
        resubcommands.append(tmp_cmd)
        nofrfiles += 1
        print 'directory {d} DOES NOT HAVEA FR FILE'.format(d=d)

print 'frfiles', frfiles
print 'nofrfiles', nofrfiles
print '=============================='
print resubcommands

if opts.submit:
    for cmd in resubcommands:
        os.system(cmd)
