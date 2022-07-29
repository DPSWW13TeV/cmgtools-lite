import ROOT, itertools, random


infile = ROOT.TFile('pvz.root', 'read')

h_pvz = infile.Get('htemp')


f_g = h_pvz.GetFunction('gaus')

npumax = 50

nsample = 10000

probs = []

for npu in range(1,npumax):
    _pass = 0

    for n in range(nsample):
    
        tmp_pvz = f_g.GetRandom()

        tmp_dzs = []
        for i in range(npu):
            tmp_dzs.append(abs(tmp_pvz-f_g.GetRandom()))
        dz_other = random.choice(tmp_dzs)
    
        if dz_other < 0.12:
            _pass+=1
    
        #tmp_dzs = []
        #for a, b in itertools.combinations(tmp_zs, 2):
        #    tmp_dzs.append(abs(a-b) < 0.1)
        
        #if any(tmp_dzs):
        #    _pass +=1


    eff = float(_pass)/float(nsample)
    probs.append(eff)

print probs

    
#print tmp_zs
#print tmp_dzs

    
