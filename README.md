# Short recipe for CMGTools 

For the general recipe, [follow these instructions](https://twiki.cern.ch/twiki/bin/view/CMS/CMGToolsReleasesExperimental).

--------------

#### Set up CMSSW and the base git

```
cmsrel CMSSW_10_6_29
cd CMSSW_10_6_29/src
cmsenv
git cms-init
```

#### Add the central cmg-cmssw repository to get the Heppy 80X branch

```
git remote add cmgtools_vvsemilep https://github.com/DPSWW13TeV/cmgtools-lite.git -f  -t cmgtools_10XUL
```

#### Configure the sparse checkout, and get the base heppy packages

```
git checkout -b cmgtools_10XUL cmgtools_vvsemilep/104X_dev_nano_UL_ankita
```

#### Add your mirror, and push the 80X branch to it

```
git remote add origin git@github.com:YOUR_GITHUB_REPOSITORY/cmg-cmssw.git
git push -u origin cmgtools_10XUL
```

#### Now get the CMGTools subsystem from the cmgtools-lite repository

```
git clone -o cmg-central https://github.com/CERN-PH-CMG/cmgtools-lite.git -b 80X CMGTools
cd CMGTools
```

#### Add your fork, and push the 80X branch to it

```
git remote add origin  git@github.com:YOUR_GITHUB_REPOSITORY/cmgtools-lite.git
git push -u cmgtools_10XUL
```

#### Compile

```
cd $CMSSW_BASE/src
scram b -j 8
```
git clone --branch postproc_UL git@github.com:sscruz/nanoAOD-tools.git PhysicsTools/NanoAODTools

#https://cms-analysis.github.io/HiggsAnalysis-CombinedLimit/