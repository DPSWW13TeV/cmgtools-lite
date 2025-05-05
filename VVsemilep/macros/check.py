import os, sys
year=sys.argv[1] 

eosDir="/eos/cms/store/cmst3/group/dpsww/SMEFT_samples/%s/"%(year)
for sample in [x[0] for x in os.walk(eosDir)]: # ["WZToLNuJJ_01j_LO_EWdim6NLO","WWToLNuJJ_01j_LO_EWdim6NLO","WWToLNujj_01j_SMEFT_LO","WZToLNujj_01j_SMEFT_LO"]:
    print("sample ",sample)
    os.system("ls -lrtch  %s/*root | wc -l "%(sample))


#lt /eos/cms/store/cmst3/group/dpsww/SMEFT_samples/2018/WZToLNuJJ_01j_LO_EWdim6NLO/*root | wc -l
#lt /eos/cms/store/cmst3/group/dpsww/SMEFT_samples/2018/WWToLNuJJ_01j_LO_EWdim6NLO/*root | wc -l
#lt /eos/cms/store/cmst3/group/dpsww/SMEFT_samples/2018/WWToLNujj_01j_SMEFT_LO/*root | wc -l
#lt /eos/cms/store/cmst3/group/dpsww/SMEFT_samples/2018/WZToLNujj_01j_SMEFT_LO/*root | wc -l
