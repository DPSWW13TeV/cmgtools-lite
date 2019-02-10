// #ifndef FAKERATE_H
// #define FAKERATE_H

#include <TH2.h>
#include <TH2D.h>
#include <TFile.h>
#include <TF1.h>
#include <cmath>
#include <iostream>
#include <string>
#include <map>
#include <cstdlib> //as stdlib.h         
#include <cstdio>
#include <TMath.h>

TH2 * helicityFractions_0 = 0;
TH2 * helicityFractions_L = 0;
TH2 * helicityFractions_R = 0;
TH2 * QF_el = 0;
TH2 * FR_mu = 0;
TH2 * FR_el = 0;
TH2 * FR_el_jptgt40 =0;
TH2 * FR_el_jptgt50 =0;
TH2 * PR_el_jptgt40 =0;
TH2 * PR_el_jptgt50 =0;
TH2 * FR_mu_jptgt40 =0;
TH2 * FR_mu_jptgt50 =0;
TH2 * PR_mu_jptgt40 =0;
TH2 * PR_mu_jptgt50 =0;

TH2 * PR_mu_down =0;
TH2 * FR_mu_down =0;
TH2 * FR_el_up =0;
TH2 * PR_el_up =0;

TH2 * PR_mu_up =0;
TH2 * FR_mu_up =0;
TH2 * FR_el_down =0;
TH2 * PR_el_down =0;

TH2 *FR_mu_2017_up=0;
TH2 *FR_el_2017_up=0;
TH2 *FR_mu_2017=0;
TH2 *FR_el_2017=0;
TH2 *FR_mu_2017_down=0;
TH2 *FR_el_2017_down=0;


TH2 * FRi_mu[30], *FRi_el[30];
//TH2 * FRi_2016_mu[30], *FRi_2016_el[30];
TH2 *PR_mu=0;
TH2 *PR_el = 0;
TH2 * PRi_mu[7] = {0};
// TH2 * FRcorrectionForPFMET = 0;
// TH2 * FRcorrectionForPFMET_i[5];

bool loadFRHisto(const std::string &histoName, const char *file, const char *name) {
  TH2 **histo = 0, **hptr2 = 0;
  TH2 * FR_temp = 0;
  if (histoName == "FR_mu")  { histo = & FR_mu; }
  else if (histoName == "FR_mu_qcdmc")  { histo = & FR_mu; }
  else if (histoName == "FR_el")  { histo = & FR_el;}//   hptr2 = & FRi_2016_el[0];}
    else if (histoName == "PR_mu")  { histo = & PR_mu;  }
    else if (histoName == "PR_el")  { histo = & PR_el;  }
    else if (histoName == "FR_el_2017")  { histo = & FR_el_2017; hptr2 = & FRi_el[0]; }
    else if (histoName == "FR_mu_2017")  { histo = & FR_mu_2017; hptr2 = & FRi_mu[0]; }
    else if (histoName == "FR_el_up")  { histo = & FR_el_up;  }
    else if (histoName == "PR_mu_up")  { histo = & PR_mu_up;  }
    else if (histoName == "FR_mu_up")  { histo = & FR_mu_up;  }
    else if (histoName == "PR_el_up")  { histo = & PR_el_up;  }
    else if (histoName == "FR_el_down")  { histo = & FR_el_down;  }
    else if (histoName == "PR_mu_down")  { histo = & PR_mu_down;  }
    else if (histoName == "FR_mu_down")  { histo = & FR_mu_down;  }
    else if (histoName == "PR_el_down")  { histo = & PR_el_down;  }

    else if (histoName == "FR_el_qcdmc")  { histo = & FR_el;  hptr2 = & FRi_el[0]; }
    else if(histoName == "PR_mu_jptgt50"){ histo = & PR_mu_jptgt50;  }
    else if(histoName == "FR_mu_jptgt50"){ histo = & FR_mu_jptgt50;  }
    else if(histoName == "PR_mu_jptgt40"){ histo = & PR_mu_jptgt40;  }
    else if(histoName == "FR_mu_jptgt40"){ histo = & FR_mu_jptgt40;  }
    else if(histoName == "PR_el_jptgt50"){ histo = & PR_el_jptgt50;  }
    else if(histoName == "FR_el_jptgt50"){ histo = & FR_el_jptgt50;  }
    else if(histoName == "PR_el_jptgt40"){ histo = & PR_el_jptgt40;  }
    else if(histoName == "FR_el_jptgt40"){ histo = & FR_el_jptgt40;  }
    else if(histoName == "FR_mu_2017_up"){histo = &FR_mu_2017_up; hptr2 = &FRi_mu[0];}
    else if(histoName == "FR_el_2017_up"){histo = &FR_el_2017_up; hptr2 = &FRi_el[0]; }
    else if(histoName == "FR_mu_2017_down"){histo = &FR_mu_2017_down; hptr2 = &FRi_mu[0];}
    else if(histoName == "FR_el_2017_down"){histo = &FR_el_2017_down; hptr2 = &FRi_el[0];}


    // else if (histoName == "FR_correction")  { histo = & FRcorrectionForPFMET; hptr2 = & FRcorrectionForPFMET_i[0]; }
    else if (TString(histoName).BeginsWith("FR_mu_i")) {histo = & FR_temp; hptr2 = & FRi_mu[TString(histoName).ReplaceAll("FR_mu_i","").Atoi()];}
    else if (TString(histoName).BeginsWith("FR_el_i")) {histo = & FR_temp; hptr2 = & FRi_el[TString(histoName).ReplaceAll("FR_el_i","").Atoi()];}
    else if (histoName == "QF_el") histo = & QF_el;
    else if (TString(histoName).Contains("helicityFractions_0")) { histo = & helicityFractions_0; }
    else if (TString(histoName).Contains("helicityFractions_L")) { histo = & helicityFractions_L; }
    else if (TString(histoName).Contains("helicityFractions_R")) { histo = & helicityFractions_R; }
    if (histo == 0)  {
        std::cerr << "ERROR: histogram " << histoName << " is not defined in fakeRate.cc." << std::endl;
        return 0;
    }

    TFile *f = TFile::Open(file);
    if (*histo != 0) {
      if (std::string(name) != (*histo)->GetName()) {
        //std::cerr << "WARNING: overwriting histogram " << (*histo)->GetName() << std::endl;
      } else {
          TH2* hnew = (TH2*) f->Get(name);
          if (hnew == 0 || hnew->GetNbinsX() != (*histo)->GetNbinsX() || hnew->GetNbinsY() != (*histo)->GetNbinsY()) {
	    std::cerr << "WARNING: overwriting histogram " << (*histo)->GetName() << hnew->GetNbinsX()<<(*histo)->GetNbinsX()<<hnew->GetNbinsY()<<(*histo)->GetNbinsY()<<std::endl;
          } else {
              bool fail = false;
              for (int ix = 1; ix <= (*histo)->GetNbinsX(); ++ix) {
                  for (int iy = 1; iy <= (*histo)->GetNbinsX(); ++iy) {
                      if ((*histo)->GetBinContent(ix,iy) != hnew->GetBinContent(ix,iy)) {
                          fail = true; break;
                      }
                  }
              }
              if (fail) std::cerr << "overwriting histogram " << (*histo)->GetName() << std::endl;
          }
      }
      delete *histo;
    }
    if (f->Get(name) == 0) {
        std::cerr << "ERROR: could not find " << name << " in " << file << std::endl;
        *histo = 0;
    } else {
        *histo = (TH2*) f->Get(name)->Clone(name);
        (*histo)->SetDirectory(0);
        if (hptr2) *hptr2 = *histo;
    }
    f->Close();
    return histo != 0;
}

float puw2017_herwigg[80] = {0,0,0,2.27008,3.74564,2.25339,2.82139,2.97948,2.47187,2.77325,2.53951,2.33365,2.03668,1.88443,1.77833,1.67443,1.56289,1.3917,1.25253,1.06277,0.976758,0.870936,0.790535,0.713799,0.643822,0.551428,0.516994,0.465398,0.38879,0.349138,0.327546,0.30658,0.240941,0.251968,0.200709,0.181512,0.183967,0.157223,0.151671,0.106266,0.104634,0.0948796,0.0902638,0.0717555,0.0832775,0.0625131,0.0606511,0.0446805,0.036115,0.0295584,0.0344268,0.0403625,0.0211761,0.0270248,0.00522258,0.0136205,0.0214609,0.0390496,0.0286949,0.0197972,0.0425641,0,0.0236467,0.0257964,0,0,0,0.0405372,0,0,0,0,0,0,0,0,0,0,0,0};
float puw2017_CP5[80] = {0,0,0,0.0720495,0.396272,0.368435,1.04472,1.10326,1.26087,2.03283,2.41803,1.9437,1.61881,1.51869,1.59003,1.60409,1.48697,1.55307,1.42429,1.04643,0.977148,0.925688,0.89919,0.696008,0.652616,0.619487,0.529287,0.476657,0.363019,0.380386,0.38475,0.295426,0.227875,0.243373,0.189566,0.184144,0.194828,0.150433,0.177622,0.0854195,0.0947405,0.109906,0.0900619,0.104282,0.0827099,0.0577756,0.068155,0.0438763,0.0360248,0.0237005,0.0300206,0.0309588,0.0250172,0.0200138,0.00428866,0.0180124,0.0150103,0.0204686,0.0142203,0.0225155,0.0600413,0,0.0150103,0.0300206,0,0,0,0.0900619,0,0,0,0,0,0,0,0,0,0,0,0};
 
float puw_2017( int nVert, bool herwMC){
   if(herwMC == true) return puw2017_herwigg[nVert];
   else if (nVert > 80) return 0;
   else if(herwMC == false) return puw2017_CP5[nVert];
   else return 0;
 }

float fakeRateWeight_2lssMVA(float l1pt, float l1eta, int l1pdgId, float l1mva,
                         float l2pt, float l2eta, int l2pdgId, float l2mva, float WP)
{
    int nfail = (l1mva < WP)+(l2mva < WP);
    switch (nfail) {
        case 1: {
            double fpt,feta; int fid;
            if (l1mva < l2mva) { fpt = l1pt; feta = std::abs(l1eta); fid = abs(l1pdgId); }
            else               { fpt = l2pt; feta = std::abs(l2eta); fid = abs(l2pdgId); }
            TH2 *hist = (fid == 11 ? FR_el : FR_mu);
            int ptbin  = std::max(1, std::min(hist->GetNbinsX(), hist->GetXaxis()->FindBin(fpt)));
            int etabin = std::max(1, std::min(hist->GetNbinsY(), hist->GetYaxis()->FindBin(feta)));
            double fr = hist->GetBinContent(ptbin,etabin);
            return fr/(1-fr);
        }
        case 2: {
	    TH2 *hist1 = (abs(l1pdgId) == 11 ? FR_el : FR_mu);
            int ptbin1  = std::max(1, std::min(hist1->GetNbinsX(), hist1->GetXaxis()->FindBin(l1pt)));
            int etabin1 = std::max(1, std::min(hist1->GetNbinsY(), hist1->GetYaxis()->FindBin(std::abs(l1eta))));
            double fr1 = hist1->GetBinContent(ptbin1,etabin1);
            TH2 *hist2 = (abs(l2pdgId) == 11 ? FR_el : FR_mu);
            int ptbin2  = std::max(1, std::min(hist2->GetNbinsX(), hist2->GetXaxis()->FindBin(l2pt)));
            int etabin2 = std::max(1, std::min(hist2->GetNbinsY(), hist2->GetYaxis()->FindBin(std::abs(l2eta))));
            double fr2 = hist2->GetBinContent(ptbin2,etabin2);
            return -fr1*fr2/((1-fr1)*(1-fr2));

        }
        default: return 0;
    }
}
///////////////// muon FRs from AN2018_098_v18

float coneptTTH(float leppt, int leppdgId, bool lepmediumMuonId, float lepmva, float lepjetPtRatiov2){
  if (abs(leppdgId)!=11 && abs(leppdgId)!=13) return leppt;
  else if ((abs(leppdgId)!=13 || lepmediumMuonId>0) && lepmva > 0.90) return leppt;
  else return (0.90 * leppt / lepjetPtRatiov2);

}

float Conept_TTH2017(float lpt, int lpdgId, bool lmediumMuonId, float lmva, float ljetPtRatiov2, float ljetBTagCSV,float lrelIso04){

  float ljetPtRatiov3 = 0.0;
  if(ljetBTagCSV > -98){
    ljetPtRatiov3= ljetPtRatiov2;
  }
  else{
    ljetPtRatiov3= 1.0/(1.0 + lrelIso04);
  }
  if (abs(lpdgId)!=11 && abs(lpdgId)!=13) return lpt;
  else if ((abs(lpdgId)!=13 || lmediumMuonId>0) && lmva > 0.90) return lpt;
  else return (0.90 * lpt / ljetPtRatiov3);
 }


float fakeRateWeight_2lssMVA_smoothed_FR(float l1pt, float l1eta, int l1pdgId, float l1mva,
                         float l2pt, float l2eta, int l2pdgId, float l2mva, float WP)
{
    int nfail = (l1mva < WP)+(l2mva < WP);
    switch (nfail) {
        case 1: {
            double fpt,feta; int fid;
            if (l1mva < l2mva) { fpt = l1pt; feta = std::abs(l1eta); fid = abs(l1pdgId); }
            else               { fpt = l2pt; feta = std::abs(l2eta); fid = abs(l2pdgId); }
            TH2 *hist = (fid == 11 ? FR_el : FR_mu);
	    int etabin = std::max(1, std::min(hist->GetNbinsX(), hist->GetXaxis()->FindBin(feta)));
	    float p0 = hist->GetBinContent(etabin, 1);
	    float p1 = hist->GetBinContent(etabin, 2);	    
	    float fr = (fpt < 60.0 ? p0 + p1*fpt : p0 + p1*60);
            return fr/(1-fr);

        }
        case 2: {
            TH2 *hist1 = (abs(l1pdgId) == 11 ? FR_el : FR_mu);
            int etabin1 = std::max(1, std::min(hist1->GetNbinsY(), hist1->GetYaxis()->FindBin(std::abs(l1eta))));
	    float p0_1 = hist1->GetBinContent(etabin1, 1);
            float p1_1 = hist1->GetBinContent(etabin1, 2);
            float fr1 = (l1pt < 60.0 ? p0_1 + p1_1*l1pt :  p0_1 + p1_1*60);
            TH2 *hist2 = (abs(l2pdgId) == 11 ? FR_el : FR_mu);
            int etabin2 = std::max(1, std::min(hist2->GetNbinsY(), hist2->GetYaxis()->FindBin(std::abs(l2eta))));
	    float p0_2 = hist2->GetBinContent(etabin2, 1);
            float p1_2 = hist2->GetBinContent(etabin2, 2);
            float fr2 = (l1pt < 60.0 ? p0_2 + p1_2*l2pt :  p0_2 + p1_2*60);
         return -fr1*fr2/((1-fr1)*(1-fr2));
        }
        default: return 0;
    }
}


//////////////////////////////////////////////////////////


// float fakeRateWeight_1l_i_smoothed_FRcorr(float lpt, float leta, int lpdgId, bool passWP, int iFR, float pfmet) {
//   if (!passWP) {
//     double fpt = lpt; double feta = std::fabs(leta); int fid = abs(lpdgId);
//     TH2 *hist = (fid == 11 ? FRi_el[iFR] : FRi_mu[iFR]);
//     if (hist == 0) {
//       std::cout << "Error in fakeRateWeight_1l_i_smoothed_FRcorr: hist == 0. Returning 0" << std::endl;	
//       return 0;
//     }
//     int etabin = std::max(1, std::min(hist->GetNbinsX(), hist->GetXaxis()->FindBin(feta)));
//     float p0 = hist->GetBinContent(etabin, 1);
//     float p1 = hist->GetBinContent(etabin, 2);
//     if (iFR==1) p0 += hist->GetBinError(etabin, 1);
//     if (iFR==2) p0 -= hist->GetBinError(etabin, 1);
//     if (iFR==3) p1 += hist->GetBinError(etabin, 2);
//     if (iFR==4) p1 -= hist->GetBinError(etabin, 2);
//     float fr = p0 + p1*lpt;
//     /////////////
//     float FRcorrection = 1;
//     TH2 *hist_FRcorr = 0;
//     if (fid == 11 && pfmet >= 0) {
//       hist_FRcorr = FRcorrectionForPFMET_i[iFR];
//       if (hist_FRcorr == 0) {
// 	std::cout << "Error in fakeRateWeight_1l_i_smoothed_FRcorr: hist_FRcorr == 0. Returning 0" << std::endl;
// 	return 0;
//       } else {
// 	int pfmetbin = std::max(1, std::min(hist_FRcorr->GetNbinsX(), hist_FRcorr->GetXaxis()->FindBin(pfmet))); 
// 	etabin = std::max(1, std::min(hist_FRcorr->GetNbinsY(), hist_FRcorr->GetYaxis()->FindBin(leta))); 
// 	FRcorrection = hist_FRcorr->GetBinContent(pfmetbin,etabin); 
//       }
//     }
//     /////////////
//     return FRcorrection * fr/(1-fr);
//   } else return 0;
// }

// float fakeRateWeight_1l_i_smoothed(float lpt, float leta, int lpdgId, bool passWP, int iFR) {

//   // this function is used for backward compatibility, becasue I added a new argument with respect to original fakeRateWeight_1l_i_smoothed(...)
//   return fakeRateWeight_1l_i_smoothed_FRcorr(lpt, leta, lpdgId, passWP, iFR, -1);

// }

float fakeRateWeight_1l_i_smoothed(float lpt, float leta, int lpdgId, bool passWP, int iFR) {
  if (!passWP) {
    double fpt = lpt; double feta = std::fabs(leta); int fid = abs(lpdgId);
    TH2 *hist = (fid == 11 ? FRi_el[iFR] : FRi_mu[iFR]);
    if (hist == 0) {
      std::cout << "Error in fakeRateWeight_1l_i_smoothed: hist == 0. Returning 0" << std::endl;	
      return 0;
    }
    int etabin = std::max(1, std::min(hist->GetNbinsX(), hist->GetXaxis()->FindBin(feta)));
    float p0 = hist->GetBinContent(etabin, 1);
    float p1 = hist->GetBinContent(etabin, 2);
    if (iFR==1) p0 += hist->GetBinError(etabin, 1);
    if (iFR==2) p0 -= hist->GetBinError(etabin, 1);
    if (iFR==3) p1 += hist->GetBinError(etabin, 2);
    if (iFR==4) p1 -= hist->GetBinError(etabin, 2);
    float fr = p0 + p1*lpt;
    return fr/(1-fr);
  } else return 0;
}

float fakeRateWeight_1l_i(float lpt, float leta, int lpdgId, bool passWP, int iFR) {
  if (!passWP) {
    double fpt = lpt; double feta = std::fabs(leta); int fid = abs(lpdgId);
    TH2 *hist = (fid == 11 ? FRi_el[iFR] : FRi_mu[iFR]);
    if (hist == 0) return 0;
    int ptbin  = std::max(1, std::min(hist->GetNbinsX(), hist->GetXaxis()->FindBin(fpt)));
    int etabin = std::max(1, std::min(hist->GetNbinsY(), hist->GetYaxis()->FindBin(feta)));
    double fr = hist->GetBinContent(ptbin,etabin);
    return fr/(1-fr);
  } else return 0;
}

float fakeRateWeight_1l(float lpt, float leta, int lpdgId, bool passWP)
{
  return fakeRateWeight_1l_i(lpt, leta, lpdgId, passWP, 0);
}

float fetchFR_i(float l1pt, float l1eta, int l1pdgId, int iFR) 
{
    TH2 *hist1 = (abs(l1pdgId) == 11 ? FRi_el[iFR] : FRi_mu[iFR]);
    if (hist1 == 0) { std::cerr << "ERROR, missing FR for pdgId " << l1pdgId << ", iFR " << iFR << std::endl; }
    int ptbin1  = std::max(1, std::min(hist1->GetNbinsX(), hist1->GetXaxis()->FindBin(l1pt)));
    int etabin1 = std::max(1, std::min(hist1->GetNbinsY(), hist1->GetYaxis()->FindBin(std::abs(l1eta))));
    double fr1 = hist1->GetBinContent(ptbin1,etabin1);
    if (fr1 <= 0)  { std::cerr << "WARNING, FR is " << fr1 << " for " << hist1->GetName() << ", pt " << l1pt << " eta " << l1eta << std::endl; }
    return fr1;
}

   
TF1 * helicityFraction_0 = new TF1("helicityFraction_0", "3./4*(TMath::Sqrt(1-x*x))^2", -1., 1.);
TF1 * helicityFraction_L = new TF1("helicityFraction_L", "3./8.*(1-x)^2"              , -1., 1.);
TF1 * helicityFraction_R = new TF1("helicityFraction_R", "3./8.*(1+x)^2"              , -1., 1.);

float helicityWeight(float yw, float ptw, float costheta, int pol)
{

  if (std::abs(costheta) > 1.) {
    //std::cout << " found an event with weird cosTheta = " << costheta << std::endl;
    //std::cout << " setting event weight to 0" << std::endl;
    return 0;
  }

  TH2 *hist_f0 = helicityFractions_0;
  TH2 *hist_fL = helicityFractions_L;
  TH2 *hist_fR = helicityFractions_R;

  // float yval  = std::abs(yw) > hist_f0->GetXaxis()->GetXmax() ? hist_f0->GetXaxis()->GetXmax() : yw;
  // float ptval = ptw > hist_f0->GetYaxis()->GetXmax() ? hist_f0->GetYaxis()->GetXmax() : ptw;

  int ywbin = std::max(1, std::min(hist_f0->GetNbinsX(), hist_f0->GetXaxis()->FindBin(yw )));
  int ptbin = std::max(1, std::min(hist_f0->GetNbinsY(), hist_f0->GetYaxis()->FindBin(ptw)));

  float f0 = hist_f0->GetBinContent(ywbin, ptbin);
  float fL = hist_fL->GetBinContent(ywbin, ptbin);
  float fR = hist_fR->GetBinContent(ywbin, ptbin);

  float f0Term = helicityFraction_0->Eval(costheta);
  float fLTerm = helicityFraction_L->Eval(costheta);
  float fRTerm = helicityFraction_R->Eval(costheta);

  float weight = 0.;
  float max_weight = 4.;

  if      (pol == 0) return std::min( f0*f0Term/(f0*f0Term+fL*fLTerm+fR*fRTerm), max_weight);
  else if (pol == 1) return std::min( fL*fLTerm/(f0*f0Term+fL*fLTerm+fR*fRTerm), max_weight);
  else if (pol == 2) return std::min( fR*fRTerm/(f0*f0Term+fL*fLTerm+fR*fRTerm), max_weight);
        
  std::cout << "something went wrong in the helicity reweighting" << std::endl;
  return -99999.;

}

float weights_TT_and_TL(float iso1, float iso2, float cut, int category){
  int sum = (iso1 > cut) + (iso2 > cut);
  if      (sum == 2 && category == 0) return 1;
  else if (sum == 1 && category == 1) return 1;
  else if (sum == 0 && category == 2) return 1;
  else return 0;
}


float eps_smoothFR(float lpt, float leta, int lpdgId, int variation){
  
  int etabin;
  float p0 =0.0;
  float p1 =0.0;
  if (variation > 6) cout<<"you should enter a number less than 6"<<endl;

  if (variation < 5){
  TH2 *hist = (abs(lpdgId) == 11 ? FR_el : FR_mu);
   etabin = std::max(1, std::min(hist->GetNbinsX(), hist->GetXaxis()->FindBin(abs(leta))));
   p0 = hist->GetBinContent(etabin, 1);
   p1 = hist->GetBinContent(etabin, 2);
  if(variation == 1){
    p0+=hist->GetBinError(etabin, 1);
    p1+=hist->GetBinError(etabin, 2);
  }
  else if (variation == 2){
    p0-=hist->GetBinError(etabin, 1);
    p1-=hist->GetBinError(etabin, 2);
  }
  else if (variation == 3){
    p1-=0.25*p1;
  }
  else if (variation == 4){
    p1+=0.25*p1;
  }  
  else{
    p0+=0;
    p1+=0;
  }  
  }
  else{
    if(variation == 5){ // for jet pt gt 40 
      TH2 *hist = (abs(lpdgId) == 11 ? FR_el_jptgt40 : FR_mu_jptgt40);
      etabin = std::max(1, std::min(hist->GetNbinsX(), hist->GetXaxis()->FindBin(abs(leta))));
       p0 = hist->GetBinContent(etabin, 1);
       p1 = hist->GetBinContent(etabin, 2);
  }
    else if (variation == 6){ // for jet pt gt 50
      TH2 *hist = (abs(lpdgId) == 11 ? FR_el_jptgt50 : FR_mu_jptgt50);
      etabin = std::max(1, std::min(hist->GetNbinsX(), hist->GetXaxis()->FindBin(abs(leta))));
       p0 = hist->GetBinContent(etabin, 1);
       p1 = hist->GetBinContent(etabin, 2);
  }

  }

  float SFR = (lpt < 60.0 ? p0 + p1*lpt : p0 + p1*60);
  return(SFR/(1-SFR));
}

float eta_smoothPR(float lpt, float leta, int lpdgId, int variation){
  int etabin;
  float p0 =0.0;
  float p1 =0.0;
  float p2=0.0;
  if (variation > 6) cout<<"you should enter a number less than 6"<<endl;  
  if (variation == 0){
  TH2 *hist = (abs(lpdgId) == 11 ? PR_el : PR_mu);
   etabin = std::max(1, std::min(hist->GetNbinsX(), hist->GetXaxis()->FindBin(abs(leta))));
   p0 = hist->GetBinContent(etabin,1);
   p1 = hist->GetBinContent(etabin,2);
   p2 = hist->GetBinContent(etabin,3);
  }
  else if (variation == 3){
  TH2 *hist = (abs(lpdgId) == 11 ? PR_el_down : PR_mu_down);
   etabin = std::max(1, std::min(hist->GetNbinsX(), hist->GetXaxis()->FindBin(abs(leta))));
   p0 = hist->GetBinContent(etabin,1);
   p1 = hist->GetBinContent(etabin,2);
   p2 = hist->GetBinContent(etabin,3);
  }
  else if (variation ==4){
  TH2 *hist = (abs(lpdgId) == 11 ? PR_el_up : PR_mu_up);
   etabin = std::max(1, std::min(hist->GetNbinsX(), hist->GetXaxis()->FindBin(abs(leta))));
   p0 = hist->GetBinContent(etabin,1);
   p1 = hist->GetBinContent(etabin,2);
   p2 = hist->GetBinContent(etabin,3);
  }
  else if (variation ==5){
  TH2 *hist = (abs(lpdgId) == 11 ? PR_el_jptgt40 : PR_mu_jptgt40);
   etabin = std::max(1, std::min(hist->GetNbinsX(), hist->GetXaxis()->FindBin(abs(leta))));
   p0 = hist->GetBinContent(etabin,1);
   p1 = hist->GetBinContent(etabin,2);
   p2 = hist->GetBinContent(etabin,3);
  }
  else if (variation ==6){
  TH2 *hist = (abs(lpdgId) == 11 ? PR_el_jptgt50 : PR_mu_jptgt50);
   etabin = std::max(1, std::min(hist->GetNbinsX(), hist->GetXaxis()->FindBin(abs(leta))));
   p0 = hist->GetBinContent(etabin,1);
   p1 = hist->GetBinContent(etabin,2);
   p2 = hist->GetBinContent(etabin,3);
  }
  else{
  TH2 *hist = (abs(lpdgId) == 11 ? PR_el : PR_mu);
   etabin = std::max(1, std::min(hist->GetNbinsX(), hist->GetXaxis()->FindBin(abs(leta))));
   p0 = hist->GetBinContent(etabin,1);
   p1 = hist->GetBinContent(etabin,2);
   p2 = hist->GetBinContent(etabin,3);
  }

  /*
  if(variation == 1){
    p0+=hist->GetBinError(etabin, 1);
    p1+=hist->GetBinError(etabin, 2);
    p2+=hist->GetBinError(etabin, 3);
  }
  else if (variation == 2){
    p0-=hist->GetBinError(etabin, 1);
    p1-=hist->GetBinError(etabin, 2);
    p2-=hist->GetBinError(etabin, 3);
  }
  */


  float SPR = p0*TMath::Erf((lpt-p1)/p2);
  return((1-SPR)/SPR);
}


float fakeRateWeight_2lssMVA_usingPRs_smooth(float l1pt, float l1eta, int l1pdgId, float l1mva,
                                             float l2pt, float l2eta, int l2pdgId, float l2mva,int syst){

  //syst variation = 0 for nominal FRs/PRs, 1 for Up, 2 for Down variation within uncert of fit params.
  //for variation = 3 & 4 slope of FR fit is varried down & up resp. by 25%. 
  float WP=0.9;
  double  wSum =0.0;
  double  qSum =0.0;
  bool l1pass=l1mva > WP;
  bool l2pass=l2mva > WP;
  //  int syst = 0;
  float Eta_l1=eta_smoothPR(l1pt,l1eta,l1pdgId,syst);
  float Eta_l2=eta_smoothPR(l2pt,l2eta,l2pdgId,syst);
  float Eps_l1=eps_smoothFR(l1pt,l1eta,l1pdgId,syst);
  float Eps_l2=eps_smoothFR(l2pt,l2eta,l2pdgId,syst);
  
  double  norm  = 1./((1-Eps_l1*Eta_l1)*(1-Eps_l2*Eta_l2));

  if(l1pass && l2pass){
    wSum = - (Eps_l1*Eta_l1 + Eps_l2*Eta_l2);
    qSum =   Eps_l1*Eta_l1*Eps_l2*Eta_l2;
    //    cout<<"weight is TT \t"<<(wSum+qSum)/norm<<endl;
    return ((wSum+qSum)/norm);
  }
  else if (l1pass && !l2pass){
    wSum     = (Eps_l2 + Eps_l1*Eta_l1*Eps_l2);
    qSum     = -(Eps_l1*Eps_l2*Eta_l1);
    //    cout<<"weight is TL \t"<<(wSum+qSum)/norm<<endl;
    return ((wSum+qSum)/norm);
  }
  else if (!l1pass && l2pass){
    wSum  = (Eps_l1 + Eps_l2*Eta_l2*Eps_l1);
    qSum  = -(Eps_l1*Eps_l2*Eta_l2);
    //cout<<"weight is LT \t"<<(wSum+qSum)/norm<<endl;
    return ((wSum+qSum)/norm);
  }
  else if (!l1pass && !l2pass){
    wSum     = -2*Eps_l1*Eps_l2;
    qSum     = Eps_l1*Eps_l2;
    //cout<<"weight is LL \t"<<(wSum+qSum)/norm<<endl;
    return ((wSum+qSum)/norm);
  }
  else {
    
    cout<<"Unexpected 2l category, returning defaults"<<endl;
    //    cout<<"MVA values"<<l1mva<<"\t"<<l2mva<<endl;
    return 0;
  }
}  


float fakeRateWeight_2lssCB_i(float l1pt, float l1eta, int l1pdgId, float l1relIso,
			      float l2pt, float l2eta, int l2pdgId, float l2relIso, float WP, int iFR) 
{
  int nfail = (l1relIso > WP)+(l2relIso > WP);
  switch (nfail) {
  case 1: {
    double fpt,feta; int fid;
    if (l1relIso > l2relIso) { fpt = l1pt; feta = std::abs(l1eta); fid = abs(l1pdgId); }
    else                     { fpt = l2pt; feta = std::abs(l2eta); fid = abs(l2pdgId); }
    TH2 *hist = (fid == 11 ? FRi_el[iFR] : FRi_mu[iFR]);
    if (hist == 0) { std::cerr << "ERROR, missing FR for pdgId " << fid << ", iFR " << iFR << std::endl; std::abort(); }
    int ptbin  = std::max(1, std::min(hist->GetNbinsX(), hist->GetXaxis()->FindBin(fpt)));
    int etabin = std::max(1, std::min(hist->GetNbinsY(), hist->GetYaxis()->FindBin(feta)));
    double fr = hist->GetBinContent(ptbin,etabin);
    if (fr < 0)  { std::cerr << "WARNING, FR is " << fr << " for " << hist->GetName() << ", pt " << fpt << " eta " << feta << std::endl; if (fr<0) std::abort(); }
    return fr/(1-fr);
  }
  case 2: {
    TH2 *hist1 = (abs(l1pdgId) == 11 ? FRi_el[iFR] : FRi_mu[iFR]);
    if (hist1 == 0) { std::cerr << "ERROR, missing FR for pdgId " << l1pdgId << ", iFR " << iFR << std::endl; std::abort(); }
    int ptbin1  = std::max(1, std::min(hist1->GetNbinsX(), hist1->GetXaxis()->FindBin(l1pt)));
    int etabin1 = std::max(1, std::min(hist1->GetNbinsY(), hist1->GetYaxis()->FindBin(std::abs(l1eta))));
    double fr1 = hist1->GetBinContent(ptbin1,etabin1);
    if (fr1 < 0)  { std::cerr << "WARNING, FR is " << fr1 << " for " << hist1->GetName() << ", pt " << l1pt << " eta " << l1eta << std::endl; if (fr1<0) std::abort(); }
    TH2 *hist2 = (abs(l2pdgId) == 11 ? FRi_el[iFR] : FRi_mu[iFR]);
    if (hist2 == 0) { std::cerr << "ERROR, missing FR for pdgId " << l2pdgId << ", iFR " << iFR << std::endl; std::abort(); }
    int ptbin2  = std::max(1, std::min(hist2->GetNbinsX(), hist2->GetXaxis()->FindBin(l2pt)));
    int etabin2 = std::max(1, std::min(hist2->GetNbinsY(), hist2->GetYaxis()->FindBin(std::abs(l2eta))));
    double fr2 = hist2->GetBinContent(ptbin2,etabin2);
    if (fr2 < 0)  { std::cerr << "WARNING, FR is " << fr2 << " for " << hist2->GetName() << ", pt " << l2pt << " eta " << l2eta << std::endl; if (fr2<0) std::abort(); }
    return -fr1*fr2/((1-fr1)*(1-fr2));
  }
  default: return 0;
  }
}

  // for syst uncertainty on Fake ratios
float fakeRateWeight_2lss(float l1pt, float l1eta, int l1pdgId, float l1pass,
			  float l2pt, float l2eta, int l2pdgId, float l2pass, int varUorD) 
{
  // varUorD == 0 for nominal FRs, {1 for up variation, 2 for down variation as a function of lepton eta}
  if (varUorD == 0) {
  return fakeRateWeight_2lssCB_i(l1pt, l1eta, l1pdgId, -l1pass,
				 l2pt, l2eta, l2pdgId, -l2pass, -0.5, 0);}
  else if (varUorD == 1) {
    float varWeight = 1.05+(fabs(l1eta)+fabs(l2eta))/2.*0.0625;
    return varWeight*fakeRateWeight_2lssCB_i(l1pt, l1eta, l1pdgId, -l1pass,
					     l2pt, l2eta, l2pdgId, -l2pass, -0.5, 0);}

  else if (varUorD == 2) {
    float varWeight = 0.95-(fabs(l1eta)+fabs(l2eta))/2*0.0625;
    return varWeight*fakeRateWeight_2lssCB_i(l1pt, l1eta, l1pdgId, -l1pass,
					     l2pt, l2eta, l2pdgId, -l2pass, -0.5, 0);}
  else if (varUorD == 3) {
    float varWeight = 1.05 + (fabs(l1eta)*0.0625);
    return varWeight*fakeRateWeight_2lssCB_i(l1pt, l1eta, l1pdgId, -l1pass,
					     l2pt, l2eta, l2pdgId, -l2pass, -0.5, 0);}

  else if (varUorD == 4) {
    float varWeight = 0.95 - (fabs(l1eta)*0.0625);
    return varWeight*fakeRateWeight_2lssCB_i(l1pt, l1eta, l1pdgId, -l1pass,
					     l2pt, l2eta, l2pdgId, -l2pass, -0.5, 0);}

  else if (varUorD == 5) {
    float ptwt= 0.0025 * (l1pt < 50 ? l1pt : 50); 
    float varWeight = 1.05 + (fabs(l1eta)*0.0625) + ptwt;
    return varWeight*fakeRateWeight_2lssCB_i(l1pt, l1eta, l1pdgId, -l1pass,
					     l2pt, l2eta, l2pdgId, -l2pass, -0.5, 0);}

  else if (varUorD == 6) {
    float ptwt= 0.0025 * (l1pt < 50 ? l1pt : 50);
    float varWeight = 0.95 - (fabs(l1eta)*0.0625) - ptwt;
    return varWeight*fakeRateWeight_2lssCB_i(l1pt, l1eta, l1pdgId, -l1pass,
					     l2pt, l2eta, l2pdgId, -l2pass, -0.5, 0);}


  
  else {
    return fakeRateWeight_2lssCB_i(l1pt, l1eta, l1pdgId, -l1pass,
				   l2pt, l2eta, l2pdgId, -l2pass, -0.5, 0);}

}


float chargeFlipWeight_2lss(float l1pt, float l1eta, int l1pdgId, int l1charge, 
			    float l2pt, float l2eta, int l2pdgId, int l2charge) 
{
  if (l1pdgId * l2pdgId > 0) return 0.;
  //if (l1charge * l2charge > 0) return 0.;
  double w = 0;
  if (abs(l1pdgId) == 11) {
    int ptbin  = std::max(1, std::min(QF_el->GetNbinsX(), QF_el->GetXaxis()->FindBin(l1pt)));
    int etabin = std::max(1, std::min(QF_el->GetNbinsY(), QF_el->GetYaxis()->FindBin(std::abs(l1eta))));
    w += QF_el->GetBinContent(ptbin,etabin);
  }
  if (abs(l2pdgId) == 11) {
    int ptbin  = std::max(1, std::min(QF_el->GetNbinsX(), QF_el->GetXaxis()->FindBin(l2pt)));
    int etabin = std::max(1, std::min(QF_el->GetNbinsY(), QF_el->GetYaxis()->FindBin(std::abs(l2eta))));
    w += QF_el->GetBinContent(ptbin,etabin);
  }
  return w;
}


//#endif
