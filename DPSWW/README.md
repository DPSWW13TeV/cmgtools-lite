## analysis steps

1. postprocess nanoAOD samples:
   1. this is done by running run_ttH_fromNanoAOD_cfg.py configuration in CMGTools/DPSWW/cfg. Things to configure : list of the samples to run on (data/MC or both), year, initial skim settings. 
      1. command to run in local (for samll jobs): nanopy.py  <outdir>   <config to run>
      1. running on condor: nanopy_batch.py  <config to run>  -B -b 'run_condor_simple.sh -t 1440 ./batchScript.sh' -r <outdir> -o <jobsDir> 
         (here the <jobsDir> should be in afs area as condor does not support eos submissions. <outdir> will contain the output root files and could be anywhere on the earth. 
   1. once your jobs finish, next thing is to *hadd chunks* (samples are divided into smaller chunks for efficient processing): python Production/python/hadd.py  <jobsDir> <outdir>
      this will add your output root files to <outdir>. This step actually runs haddnano script and it takes a while to run.  

1. Once you get the flat nTuples, next step is to *run lepton-jet recleaner friends*. This can be done by choosing the appropriate settings in runFriends.sh script which is placed under CMGTools/DPSWW/macros. *Object selections used in this steps defined in tth_modules.py and any change made in there needs a compilation.* Once you run this step and you need to run a hadd script using: python ~anmehta/public/haddFriends_v2.py <indir>. This script will warn you about faulty files and missing chunks. Fix the errors and re-run the script to get your friend trees.

1. After recleaner friends, we run the friends which hold *bdt input variables* needed to train BDTs. Follow the previous step with appropriate options and you are all set. 
1. At this point we run BDT reader to compute bdt score for data and MC samples again using runFriends.sh with appropriate option. We use different trainings for 2016 and 2017 and this step you would need to choose the year for that too. 
1. now we are all set to run 2lss/3l skimming, this helps to speed up the plot/card making steps as we reduce the sample size significantly. this step is run in local. 
  1. commands to run skimming are here: DPSWW/python/plotter/runSkimming.sh. You must specify a skim selection, a year to run on, and also the samples you want to run on are provided in the mca files. This will skim the parent trees and recleaner friends also.
 
1. post-skimming, it's time to use runFriends.sh again with post-skimming friend options. you will need to run it atleast twice. In first step you can run  friends with tauCount, lepSFs and jme vars in parallel and then second time you run on recl_allvars step. 

1. once you get all ingredients in place, execute DPSWW/python/plotter/runDPS.py with options depending on what you are trying to do. 