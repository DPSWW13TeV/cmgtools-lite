#include <cmath>
#include <map>
#include "Math/GenVector/LorentzVector.h"
#include "Math/GenVector/PtEtaPhiM4D.h"
#include "Math/GenVector/PxPyPzM4D.h"
#include "Math/GenVector/Boost.h"
#include "TLorentzVector.h"
#include "TH2Poly.h"
#include "TGraphAsymmErrors.h"
#include "TH1F.h"
#include "TFile.h"
#include "PhysicsTools/Heppy/interface/Davismt2.h"
#include "TSystem.h"

TString CMSSW_BASE = gSystem->ExpandPathName("${CMSSW_BASE}");

//// UTILITY FUNCTIONS NOT IN TFORMULA ALREADY

float myratio(float num, float denom) {
  if(denom==0) return 0;
  return num/denom;
}

float deltaPhi(float phi1, float phi2) {
    float result = phi1 - phi2;
    while (result > float(M_PI)) result -= float(2*M_PI);
    while (result <= -float(M_PI)) result += float(2*M_PI);
    return result;
}

float if3(bool cond, float iftrue, float iffalse) {
    return cond ? iftrue : iffalse;
}

float deltaR2(float eta1, float phi1, float eta2, float phi2) {
    float deta = std::abs(eta1-eta2);
    float dphi = deltaPhi(phi1,phi2);
    return deta*deta + dphi*dphi;
}
float deltaR(float eta1, float phi1, float eta2, float phi2) {
    return std::sqrt(deltaR2(eta1,phi1,eta2,phi2));
}

float pt_2(float pt1, float phi1, float pt2, float phi2) {
    phi2 -= phi1;
    return hypot(pt1 + pt2 * std::cos(phi2), pt2*std::sin(phi2));
}

float mt_2(float pt1, float phi1, float pt2, float phi2) {
    return std::sqrt(2*pt1*pt2*(1-std::cos(phi1-phi2)));
}



float mass_2(float pt1, float eta1, float phi1, float m1, float pt2, float eta2, float phi2, float m2) {
    typedef ROOT::Math::LorentzVector<ROOT::Math::PtEtaPhiM4D<double> > PtEtaPhiMVector;
    PtEtaPhiMVector p41(pt1,eta1,phi1,m1);
    PtEtaPhiMVector p42(pt2,eta2,phi2,m2);
    return (p41+p42).M();
}

float mt2davis(float pt1, float eta1, float phi1, float pt2, float eta2, float phi2, float met, float metphi){
    // NOTE THAT THIS FUNCTION ASSUMES MASSLESS OBJECTS. NOT ADVISED TO USE WITH HEMISPHERES ETC.
    typedef ROOT::Math::LorentzVector<ROOT::Math::PtEtaPhiM4D<double> > PtEtaPhiMVector;
    PtEtaPhiMVector p1(pt1,eta1,phi1,0.);
    PtEtaPhiMVector p2(pt2,eta2,phi2,0.);
    PtEtaPhiMVector mv(met,0.,metphi,0.);
    double a[] = {p1.M(), p1.Px(), p1.Py()};
    double b[] = {p2.M(), p2.Px(), p2.Py()};
    double c[] = {mv.M(), mv.Px(), mv.Py()};

    heppy::Davismt2 mt2obj;
    mt2obj.set_momenta( a, b, c );
    mt2obj.set_mn( 0. );

    float result = (float) mt2obj.get_mt2();
    return result;
}

float phi_2(float pt1, float phi1, float pt2, float phi2) {
    float px1 = pt1 * std::cos(phi1);
    float py1 = pt1 * std::sin(phi1);
    float px2 = pt2 * std::cos(phi2);
    float py2 = pt2 * std::sin(phi2);
    return std::atan2(py1+py2,px1+px2);
}

float phi_3(float pt1, float phi1, float pt2, float phi2, float pt3, float phi3) {
    float px1 = pt1 * std::cos(phi1);
    float py1 = pt1 * std::sin(phi1);
    float px2 = pt2 * std::cos(phi2);
    float py2 = pt2 * std::sin(phi2);
    float px3 = pt3 * std::cos(phi3);
    float py3 = pt3 * std::sin(phi3);
    return std::atan2(py1+py2+py3,px1+px2+px3);
}

float eta_2(float pt1, float eta1, float phi1, float m1, float pt2, float eta2, float phi2, float m2) {
    typedef ROOT::Math::LorentzVector<ROOT::Math::PtEtaPhiM4D<double> > PtEtaPhiMVector;
    PtEtaPhiMVector p41(pt1,eta1,phi1,m1);
    PtEtaPhiMVector p42(pt2,eta2,phi2,m2);
    return (p41+p42).Eta();
}

float ptll(float pt1, float eta1, float phi1, float m1, float pt2, float eta2, float phi2, float m2) {
    typedef ROOT::Math::LorentzVector<ROOT::Math::PtEtaPhiM4D<double> > PtEtaPhiMVector;
    PtEtaPhiMVector p41(pt1,eta1,phi1,m1);
    PtEtaPhiMVector p42(pt2,eta2,phi2,m2);
    return (p41+p42).Pt();
}

float mtww(float ptll, float dphill, float met, float metphi) {
  float dphillmet=deltaPhi(dphill,metphi);
  return (std::sqrt(2*ptll*met*(1-std::cos(dphillmet))));

}


float pt_3(float pt1, float phi1, float pt2, float phi2, float pt3, float phi3) {
    phi2 -= phi1;
    phi3 -= phi1;
    return hypot(pt1 + pt2 * std::cos(phi2) + pt3 * std::cos(phi3), pt2*std::sin(phi2) + pt3*std::sin(phi3));
}


float mass_3(float pt1, float eta1, float phi1, float m1, float pt2, float eta2, float phi2, float m2, float pt3, float eta3, float phi3, float m3) {
    typedef ROOT::Math::LorentzVector<ROOT::Math::PtEtaPhiM4D<double> > PtEtaPhiMVector;
    PtEtaPhiMVector p41(pt1,eta1,phi1,m1);
    PtEtaPhiMVector p42(pt2,eta2,phi2,m2);
    PtEtaPhiMVector p43(pt3,eta3,phi3,m3);
    return (p41+p42+p43).M();
}

float mass_3lep(float pt1, float eta1, float phi1, float pt2, float eta2, float phi2, float pt3, float eta3, float phi3) {
    typedef ROOT::Math::LorentzVector<ROOT::Math::PtEtaPhiM4D<double> > PtEtaPhiMVector;
    PtEtaPhiMVector p41(pt1,eta1,phi1,0);
    PtEtaPhiMVector p42(pt2,eta2,phi2,0);
    PtEtaPhiMVector p43(pt3,eta3,phi3,0);
    return (p41+p42+p43).M();
}


float pt_4(float pt1, float phi1, float pt2, float phi2, float pt3, float phi3, float pt4, float phi4) {
    phi2 -= phi1;
    phi3 -= phi1;
    phi4 -= phi1;
    return hypot(pt1 + pt2 * std::cos(phi2) + pt3 * std::cos(phi3) + pt4 * std::cos(phi4), pt2*std::sin(phi2) + pt3*std::sin(phi3) + pt4*std::sin(phi4));
}
 
float mass_4(float pt1, float eta1, float phi1, float m1, float pt2, float eta2, float phi2, float m2, float pt3, float eta3, float phi3, float m3, float pt4, float eta4, float phi4, float m4) {
    typedef ROOT::Math::LorentzVector<ROOT::Math::PtEtaPhiM4D<double> > PtEtaPhiMVector;
    PtEtaPhiMVector p41(pt1,eta1,phi1,m1);
    PtEtaPhiMVector p42(pt2,eta2,phi2,m2);
    PtEtaPhiMVector p43(pt3,eta3,phi3,m3);
    PtEtaPhiMVector p44(pt4,eta4,phi4,m4);
    return (p41+p42+p43+p44).M();
}

float mt_llv(float ptl1, float phil1, float ptl2, float phil2, float ptv, float phiv) {
    float px = ptl1*std::cos(phil1) + ptl2*std::cos(phil2) + ptv*std::cos(phiv);
    float py = ptl1*std::sin(phil1) + ptl2*std::sin(phil2) + ptv*std::sin(phiv);
    float ht = ptl1+ptl2+ptv;
    return std::sqrt(std::max(0.f, ht*ht - px*px - py*py));
}

float mt_lllv(float ptl1, float phil1, float ptl2, float phil2, float ptl3, float phil3, float ptv, float phiv) {
    float px = ptl1*std::cos(phil1) + ptl2*std::cos(phil2) + ptl3*std::cos(phil3) + ptv*std::cos(phiv);
    float py = ptl1*std::sin(phil1) + ptl2*std::sin(phil2) + ptl3*std::sin(phil3) + ptv*std::sin(phiv);
    float ht = ptl1+ptl2+ptl3+ptv;
    return std::sqrt(std::max(0.f, ht*ht - px*px - py*py));
}


float mtw_wz3l(float pt1, float eta1, float phi1, float m1, float pt2, float eta2, float phi2, float m2, float pt3, float eta3, float phi3, float m3, float mZ1, float met, float metphi) 
{
    if (abs(mZ1 - mass_2(pt1,eta1,phi1,m1,pt2,eta2,phi2,m2)) < 0.01) return mt_2(pt3,phi3,met,metphi);
    if (abs(mZ1 - mass_2(pt1,eta1,phi1,m1,pt3,eta3,phi3,m3)) < 0.01) return mt_2(pt2,phi2,met,metphi);
    if (abs(mZ1 - mass_2(pt2,eta2,phi2,m2,pt3,eta3,phi3,m3)) < 0.01) return mt_2(pt1,phi1,met,metphi);
    return 0;
}

float u1_2(float met_pt, float met_phi, float ref_pt, float ref_phi) 
{
    float met_px = met_pt*std::cos(met_phi), met_py = met_pt*std::sin(met_phi);
    float ref_px = ref_pt*std::cos(ref_phi), ref_py = ref_pt*std::sin(ref_phi);
    float ux = - met_px + ref_px, uy = - met_px + ref_px;
    return (ux*ref_px + uy*ref_py)/ref_pt;
}
float u2_2(float met_pt, float met_phi, float ref_pt, float ref_phi)
{
    float met_px = met_pt*std::cos(met_phi), met_py = met_pt*std::sin(met_phi);
    float ref_px = ref_pt*std::cos(ref_phi), ref_py = ref_pt*std::sin(ref_phi);
    float ux = - met_px + ref_px, uy = - met_px + ref_px;
    return (ux*ref_py - uy*ref_px)/ref_pt;
}

// reconstructs a top from lepton, met, b-jet, applying the W mass constraint and taking the smallest neutrino pZ
float mtop_lvb(float ptl, float etal, float phil, float ml, float met, float metphi, float ptb, float etab, float phib, float mb) 
{
    typedef ROOT::Math::LorentzVector<ROOT::Math::PtEtaPhiM4D<double> > PtEtaPhiMVector;
    typedef ROOT::Math::LorentzVector<ROOT::Math::PxPyPzM4D<double> > PxPyPzMVector;
    PtEtaPhiMVector p4l(ptl,etal,phil,ml);
    PtEtaPhiMVector p4b(ptb,etab,phib,mb);
    double MW=80.4;
    double a = (1 - std::pow(p4l.Z()/p4l.E(), 2));
    double ppe    = met * ptl * std::cos(phil - metphi)/p4l.E();
    double brk    = MW*MW / (2*p4l.E()) + ppe;
    double b      = (p4l.Z()/p4l.E()) * brk;
    double c      = met*met - brk*brk;
    double delta   = b*b - a*c;
    double sqdelta = delta > 0 ? std::sqrt(delta) : 0;
    double pz1 = (b + sqdelta)/a, pz2 = (b - sqdelta)/a;
    double pznu = (abs(pz1) <= abs(pz2) ? pz1 : pz2);
    PxPyPzMVector p4v(met*std::cos(metphi),met*std::sin(metphi),pznu,0);
    return (p4l+p4b+p4v).M();
}

float DPhi_CMLep_Zboost(float l_pt, float l_eta, float l_phi, float l_M, float l_other_pt, float l_other_eta, float l_other_phi, float l_other_M){
  typedef ROOT::Math::LorentzVector<ROOT::Math::PtEtaPhiM4D<double> > PtEtaPhiMVector;
  PtEtaPhiMVector l1(l_pt,l_eta,l_phi,l_M);
  PtEtaPhiMVector l2(l_other_pt,l_other_eta,l_other_phi,l_other_M);
  PtEtaPhiMVector Z = l1+l2;
  ROOT::Math::Boost boost(Z.BoostToCM());
  l1 = boost*l1;
  return deltaPhi(l1.Phi(),Z.Phi());
}


//PU weights

#include <assert.h>
#include "TH2F.h"
#include "TH1F.h"
#include "TFile.h"

// for json up to 276811 (12.9/fb), pu true reweighting
float _puw2016_nTrueInt_13fb[60] = {0.0004627598152210959, 0.014334910915287028, 0.01754727657726197, 0.03181477917631854, 0.046128282569231016, 0.03929080994013006, 0.057066019809589925, 0.19570744862221007, 0.3720256062526554, 0.6440076202772811, 0.9218024454406528, 1.246743510634073, 1.5292543296414058, 1.6670061646418215, 1.7390553377117133, 1.6114721876895595, 1.4177294439817985, 1.420132866045718, 1.3157656415540477, 1.3365188060918483, 1.1191478126677334, 0.9731079434848392, 0.9219564145009487, 0.8811793391804676, 0.7627315352977334, 0.7265186492688713, 0.558602385324645, 0.4805954159733825, 0.34125298049234554, 0.2584848657646724, 0.1819638766151892, 0.12529545619337035, 0.11065705912071645, 0.08587356267495487, 0.09146322371620583, 0.11885517671051576, 0.1952483711863489, 0.23589115679998116, 1.0, 1.0, 1.0, 1.0, 1.0, 1.0, 1.0, 1.0, 1.0, 1.0, 1.0, 1.0, 1.0, 1.0, 1.0, 1.0, 1.0, 1.0, 1.0, 1.0, 1.0, 1.0};
float puw2016_nTrueInt_13fb(int nTrueInt) { if (nTrueInt<60) return _puw2016_nTrueInt_13fb[nTrueInt]; else return 0; }

float _puw2016_nTrueInt_36fb[100] = {0.3505407355600995, 0.8996968628890968, 1.100322319466069, 0.9562526765089195, 1.0366251229154624, 1.0713954619016586, 0.7593488199769544, 0.47490309461978414, 0.7059895997695581, 0.8447022252423783, 0.9169159386164522, 1.0248924033173097, 1.0848877947714115, 1.1350984224561655, 1.1589888429954602, 1.169048420382294, 1.1650383018054549, 1.1507200023444994, 1.1152571438041776, 1.0739529436969637, 1.0458014000030829, 1.032500407707141, 1.0391236062781293, 1.041283620738903, 1.0412963370894526, 1.0558823002770783, 1.073481674823461, 1.0887053272606795, 1.1041701696801014, 1.123218903738397, 1.1157169321377927, 1.1052520327174429, 1.0697489590429388, 1.0144652740600584, 0.9402657069968621, 0.857142825520793, 0.7527112615290031, 0.6420618248685722, 0.5324755829715156, 0.4306470627563325, 0.33289171600176093, 0.24686361729094983, 0.17781595237914027, 0.12404411884835284, 0.08487088505600057, 0.056447805688061216, 0.03540829360547507, 0.022412461576677457, 0.013970541270658443, 0.008587896629717911, 0.004986410514292661, 0.00305102303701641, 0.001832072556146534, 0.0011570757619737708, 0.0008992999249003301, 0.0008241241729452477, 0.0008825716073180279, 0.001187003960081393, 0.0016454104270429153, 0.0022514113879764414, 0.003683196037880878, 0.005456695951503178, 0.006165248770884191, 0.007552675218762607, 0.008525338219226993, 0.008654690499815343, 0.006289068906974821, 0.00652551838513972, 0.005139581024893171, 0.005115751962934923, 0.004182527768384693, 0.004317593022028565, 0.0035749335962533355, 0.003773660372937113, 0.002618732319396435, 1.0, 1.0, 1.0, 1.0, 1.0, 1.0, 1.0, 1.0, 1.0, 1.0, 1.0, 1.0, 1.0, 1.0, 1.0, 1.0, 1.0, 1.0, 1.0, 1.0, 1.0, 1.0, 1.0, 1.0, 1.0};
float puw2016_nTrueInt_36fb(int nTrueInt) { if (nTrueInt<100) return _puw2016_nTrueInt_36fb[nTrueInt]; else return 0; }

float mass_3_cheap(float pt1, float eta1, float pt2, float eta2, float phi2, float pt3, float eta3, float phi3) {
    typedef ROOT::Math::LorentzVector<ROOT::Math::PtEtaPhiM4D<double> > PtEtaPhiMVector;
    PtEtaPhiMVector p41(pt1,eta1,0,   0.0);
    PtEtaPhiMVector p42(pt2,eta2,phi2,0.0);
    PtEtaPhiMVector p43(pt3,eta3,phi3,0.0);
    return (p41+p42+p43).M();
}

float lnN1D_p1(float kappa, float x, float xmin, float xmax) {
    return std::pow(kappa,(x-xmin)/(xmax-xmin));
}

float deepFlavB_WPLoose(int year) {
    float wp[3]  = { 0.0614, 0.0521, 0.0494 };
    return wp[year-2016];
}
float deepFlavB_WPMedium(int year) {
    float wp[3] = { 0.3093, 0.3033, 0.2770 };
    return wp[year-2016];
}
float deepFlavB_WPTight(int year) {
    float wp[3]  = { 0.7221, 0.7489, 0.7264 };
    return wp[year-2016];
}


float deepFlavB_WP(int year, int wp /*0 = loose, 1 = medium, 2=tight*/) {
    switch(wp) {
        case 0: return deepFlavB_WPLoose(year);
        case 1: return deepFlavB_WPMedium(year);
        case 2: return deepFlavB_WPTight(year);
    }
    return -99;
}

float triggerSF_ttH(int pdgid1, float pt1, int pdgid2, float pt2, int year, int nlep = 2, int var=0){
  std::cout<<pdgid1<<"\t"<<pt1<<pdgid2<<"\t"<<pt2<<"\t"<<nlep<<"\t"<<year<<std::endl;
  if (nlep == 2){
    if (abs(pdgid1*pdgid2) == 121){
      if (year == 2016){
	if (pt2 < 25){
	  return 0.98*(1 + var*0.02);
	}
      else return 1.*(1 + var*0.02);
      }
      if (year == 2017){
	if (pt2<40) return 0.98*(1 + var*0.01);
	else return 1*(1 + var*0.01);
      }
      if (year == 2018){
	if (pt2<25){
	return 0.98*(1 + var*0.01);
	}
	else return 1.*(1 + var*0.01);
      }
    }
    
    else if ( abs(pdgid1*pdgid2) == 143){
      if (year == 2016) return 1.*(1 + var*0.01);
      if (year == 2017){
	if (pt2<40) return 0.98*(1 + var*0.01);
	else return 0.99*(1 + var*0.01);
      }
      if (year == 2018){
	if (pt2<25) return 0.98*(1 + var*0.01);
	else        return 1*(1 + var*0.01);
      }
    }
    else{
      if (year == 2016) return 0.99*(1 + var*0.01);
      if (year == 2017){
	if (pt2 < 40) return 0.97*(1 + var*0.02);
	else if (pt2 < 55 && pt2>40) return 0.995*(1 + var*0.02);
	else if (pt2 < 70 && pt2>55) return 0.96*(1 + var*0.02);
	else                         return 0.94*(1 + var*0.02);
      }
      if (year == 2018){
	if (pt1 < 40) return 1.01*(1 + var*0.01);
	if (pt1 < 70) return 0.995*(1 + var*0.01);
	else return 0.98*(1 + var*0.01);
      }
    }
    
  }
  else return 1.;
}

float ttH_2lss_ifflav(int LepGood1_pdgId, int LepGood2_pdgId, float ret_ee, float ret_em, float ret_mm){
  if (abs(LepGood1_pdgId)==11 && abs(LepGood2_pdgId)==11) return ret_ee;
  if ((abs(LepGood1_pdgId) != abs(LepGood2_pdgId)))       return ret_em;
  if (abs(LepGood1_pdgId)==13 && abs(LepGood2_pdgId)==13) return ret_mm;
  std::cerr << "ERROR: invalid input " << abs(LepGood1_pdgId) << ", " << abs(LepGood1_pdgId) << std::endl;
  assert(0);
  return 0; // avoid warning
}

int unroll_2Dbdt_dps_elmu(float BDTx,float BDTy){
  if(BDTx  > 0.1 && BDTx <=0.25 && BDTy >0.1 && BDTy <= 0.35)return 0;
  else if((BDTx > 0.1 && BDTx <=0.3 && BDTy >0.35) || (BDTx  > 0.3 && BDTx <=0.35 && BDTy >0.35 && BDTy <= 0.65))return 1;
  else if((BDTx > 0.25  && BDTx <=0.8 && BDTy <= 0.35) || (BDTx > 0.1 && BDTx <= 0.25 && BDTy <= 0.1) )return 2;
  else if(BDTx  <= 0.1 )return 3;
  else if(BDTx  > 0.65 && BDTx <=0.8 && BDTy >0.35 && BDTy <= 0.65)return 4;
  else if(BDTx  > 0.35 && BDTx <=0.65 && BDTy >0.35 && BDTy <= 0.6)return 5;
  else if((BDTx  > 0.3  && BDTx <= 0.65  && BDTy > 0.65) || (BDTx  > 0.35 && BDTx <=0.65 && BDTy >0.6 ))return 6;
  else if(BDTx  > 0.65 && BDTx <=0.85 && BDTy >0.65 && BDTy <=0.75)return 7;  
  else if(BDTx  > 0.8 && BDTx <=0.9 && BDTy <=0.65)return 8;
  else if((BDTx  > 0.9 && BDTy <=0.75) || (BDTx  > 0.85 && BDTx  <=0.9 && BDTy > 0.65 && BDTy <=0.75) ) return 9;
  else if(BDTx  > 0.95  && BDTy > 0.8 && BDTy <=0.9)return 10;
  else if((BDTx  > 0.95 && BDTy > 0.75 && BDTy <=0.8)||  (BDTx  > 0.85 && BDTx <= 0.95 && BDTy > 0.75 && BDTy <=0.9) )return 11;
  else if((BDTx > 0.65 && BDTx <=0.8 && BDTy >0.75) || (BDTx  > 0.8 && BDTx <=0.85 && BDTy > 0.75 && BDTy <=0.95) )return 12;
  else if((BDTx > 0.8  && BDTx <=0.95 && BDTy > 0.95) || (BDTx > 0.85 && BDTy > 0.90 && BDTy <= 0.95) )return 13;
  else if(BDTx  > 0.95  && BDTy > 0.95)return 14;
  else{
  std::cout << "values of BDT variables are out of bounds, please check" << std::endl;
    exit(EXIT_FAILURE);}

}

int unroll_2Dbdt_dps_mumuN(float BDTx,float BDTy){
  //v13 arranged acc to signal strength(final)
  if(BDTx  <= 0.1 )return 3;
  else if(BDTx  > 0.1 && BDTx <=0.25 && BDTy >0.1 && BDTy <= 0.35)return 3;
  else if((BDTx > 0.1 && BDTx <=0.3 && BDTy >0.35) || (BDTx  > 0.3 && BDTx <=0.35 && BDTy >0.35 && BDTy <= 0.65))return 3; //problematic bin
  else if(BDTx  > 0.35 && BDTx <=0.65 && BDTy >0.45 && BDTy <= 0.6)return 2;
  else if((BDTx > 0.1 && BDTx <= 0.25 && BDTy <= 0.1) || (BDTx > 0.25  && BDTx <=0.35 && BDTy <= 0.35) || (BDTx > 0.35 && BDTx <= 0.65 && BDTy <= 0.45) || (BDTx > 0.65 && BDTx <= 0.8 && BDTy <= 0.35) )return 1;
  else if(BDTx  > 0.65 && BDTx <=0.8 && BDTy >0.35 && BDTy <= 0.65)return 0;
  else if(BDTx  > 0.8 && BDTx <=0.9 && BDTy <=0.65)return 4;
  else if(BDTx  > 0.65 && BDTx <=0.85 && BDTy >0.65 && BDTy <=0.75)return 5;
  else if((BDTx  > 0.3  && BDTx <= 0.65  && BDTy > 0.65) || (BDTx  > 0.35 && BDTx <=0.65 && BDTy >0.6))return 6;
  else if((BDTx  > 0.9 && BDTy <=0.75) || (BDTx  > 0.85 && BDTx  <=0.9 && BDTy > 0.65 && BDTy <=0.75) )return 7;
  else if((BDTx > 0.8  && BDTx <=0.85 && BDTy > 0.95) || (BDTx > 0.85 && BDTx <= 0.95 && BDTy > 0.9) )return 8;
  else if((BDTx > 0.65 && BDTx <=0.8 && BDTy >0.75) || (BDTx  > 0.8 && BDTx <=0.85 && BDTy > 0.75 && BDTy <=0.95) )return 9;
  else if((BDTx  > 0.95 && BDTy > 0.75 && BDTy <=0.85)||  (BDTx  > 0.85 && BDTx <= 0.95 && BDTy > 0.75 && BDTy <=0.9) )return 10;
  else if(BDTx  > 0.95  && BDTy > 0.85 && BDTy <=0.95)return 11;
  else if(BDTx  > 0.95  && BDTy > 0.95)return 12;
  else{
    std::cout << "values of BDT variables are out of bounds, please check" << std::endl;
    exit(EXIT_FAILURE);}
}

int unroll_2Dbdt_dps_elmuN(float BDTx,float BDTy){
  //v13 arranged acc to signal strength(final)
  if(BDTx  <= 0.1 )return 0;
  else if(BDTx  > 0.1 && BDTx <=0.25 && BDTy >0.1 && BDTy <= 0.35)return 0;
  else if((BDTx > 0.1 && BDTx <=0.3 && BDTy >0.35) || (BDTx  > 0.3 && BDTx <=0.35 && BDTy >0.35 && BDTy <= 0.65))return 0;
  else if(BDTx  > 0.35 && BDTx <=0.65 && BDTy >0.45 && BDTy <= 0.6)return 2;
  else if((BDTx > 0.1 && BDTx <= 0.25 && BDTy <= 0.1) || (BDTx > 0.25  && BDTx <=0.35 && BDTy <= 0.35) || (BDTx > 0.35 && BDTx <= 0.65 && BDTy <= 0.45) || (BDTx > 0.65 && BDTx <= 0.8 && BDTy <= 0.35) )return 1;
  else if(BDTx  > 0.65 && BDTx <=0.8 && BDTy >0.35 && BDTy <= 0.65)return 3;
  else if(BDTx  > 0.8 && BDTx <=0.9 && BDTy <=0.65)return 4;
  else if(BDTx  > 0.65 && BDTx <=0.85 && BDTy >0.65 && BDTy <=0.75)return 5;
  else if((BDTx  > 0.3  && BDTx <= 0.65  && BDTy > 0.65) || (BDTx  > 0.35 && BDTx <=0.65 && BDTy >0.6))return 6;
  else if((BDTx  > 0.9 && BDTy <=0.75) || (BDTx  > 0.85 && BDTx  <=0.9 && BDTy > 0.65 && BDTy <=0.75) )return 7;
  else if((BDTx > 0.8  && BDTx <=0.85 && BDTy > 0.95) || (BDTx > 0.85 && BDTx <= 0.95 && BDTy > 0.9) )return 8;
  else if((BDTx > 0.65 && BDTx <=0.8 && BDTy >0.75) || (BDTx  > 0.8 && BDTx <=0.85 && BDTy > 0.75 && BDTy <=0.95) )return 9;
  else if((BDTx  > 0.95 && BDTy > 0.75 && BDTy <=0.85)||  (BDTx  > 0.85 && BDTx <= 0.95 && BDTy > 0.75 && BDTy <=0.9) )return 10;
  else if(BDTx  > 0.95  && BDTy > 0.85 && BDTy <=0.95)return 11;
  else if(BDTx  > 0.95  && BDTy > 0.95)return 12;
  else{
    std::cout << "values of BDT variables are out of bounds, please check" << std::endl;
    exit(EXIT_FAILURE);}
}
int unroll_2Dbdt_dps_mumu(float BDTx,float BDTy){
  //v13 arranged acc to signal strength(final)
  if(BDTx  <= 0.1 )return 0;
  else if(BDTx  > 0.1 && BDTx <=0.25 && BDTy >0.1 && BDTy <= 0.35)return 1;
  else if((BDTx > 0.1 && BDTx <=0.3 && BDTy >0.35) || (BDTx  > 0.3 && BDTx <=0.35 && BDTy >0.35 && BDTy <= 0.65))return 2;
  else if(BDTx  > 0.35 && BDTx <=0.65 && BDTy >0.45 && BDTy <= 0.6)return 3;
  else if((BDTx > 0.1 && BDTx <= 0.25 && BDTy <= 0.1) || (BDTx > 0.25  && BDTx <=0.35 && BDTy <= 0.35) || (BDTx > 0.35 && BDTx <= 0.65 && BDTy <= 0.45) || (BDTx > 0.65 && BDTx <= 0.8 && BDTy <= 0.35) )return 4;
  else if(BDTx  > 0.65 && BDTx <=0.8 && BDTy >0.35 && BDTy <= 0.65)return 5;
  else if(BDTx  > 0.8 && BDTx <=0.9 && BDTy <=0.65)return 6;
  else if(BDTx  > 0.65 && BDTx <=0.85 && BDTy >0.65 && BDTy <=0.75)return 7;
  else if((BDTx  > 0.3  && BDTx <= 0.65  && BDTy > 0.65) || (BDTx  > 0.35 && BDTx <=0.65 && BDTy >0.6))return 8;
  else if((BDTx  > 0.9 && BDTy <=0.75) || (BDTx  > 0.85 && BDTx  <=0.9 && BDTy > 0.65 && BDTy <=0.75) )return 9;
  else if((BDTx > 0.8  && BDTx <=0.85 && BDTy > 0.95) || (BDTx > 0.85 && BDTx <= 0.95 && BDTy > 0.9) )return 10;
  else if((BDTx > 0.65 && BDTx <=0.8 && BDTy >0.75) || (BDTx  > 0.8 && BDTx <=0.85 && BDTy > 0.75 && BDTy <=0.95) )return 11;
  else if((BDTx  > 0.95 && BDTy > 0.75 && BDTy <=0.85)||  (BDTx  > 0.85 && BDTx <= 0.95 && BDTy > 0.75 && BDTy <=0.9) )return 12;
  else if(BDTx  > 0.95  && BDTy > 0.85 && BDTy <=0.95)return 13;
  else if(BDTx  > 0.95  && BDTy > 0.95)return 14;
  else{
    std::cout << "values of BDT variables are out of bounds, please check" << std::endl;
    exit(EXIT_FAILURE);}
}






float smoothBFlav(float jetpt, float ptmin, float ptmax, int year, float scale_loose=1.0) {
    float wploose[3]  = { 0.0614, 0.0521, 0.0494 };
    float wpmedium[3] = { 0.3093, 0.3033, 0.2770 };
    float x = std::min(std::max(0.f, jetpt - ptmin)/(ptmax-ptmin), 1.f); 
    return x*wploose[year-2016]*scale_loose + (1-x)*wpmedium[year-2016];
}





int unroll_2Dbdt_dps_simple(float BDTx,float BDTy){
  if(BDTx  <= 0.35 )return 1;
  else if(BDTx  > 0.35 && BDTx <= 0.45)return 1;
  else if(BDTx  > 0.45 && BDTx <= 0.5)return 2;
  else if(BDTx  > 0.5  && BDTx <= 0.55)return 3;
  else if(BDTx  > 0.55 && BDTx <= 0.65)return 4;
  else if(BDTx  > 0.65 && BDTx <= 0.7)return 5;
  else if(BDTx  > 0.7  && BDTx <= 0.8)return 6;
  else if(BDTx  > 0.8  && BDTx <= 0.85)return 7;
  else if(BDTx  > 0.85 && BDTx <= 0.9)return 8;
  else if(BDTx  > 0.9  && BDTx <= 0.95 && BDTy <= 0.7)return 9;
  else if(BDTx  > 0.9  && BDTx <= 0.95 && BDTy > 0.7)return 10;
  else if(BDTx  > 0.95 && BDTy <= 0.7)return 11;
  else if(BDTx  > 0.95 && BDTy > 0.7)return 12;
  else{
    std::cout << "values of BDT variables are out of bounds, please check" << std::endl;
    exit(EXIT_FAILURE);}
}






int unroll_2Dbdt_dps_SoBord_sq(float BDTx,float BDTy){
 
  if(BDTx  > 0.8 && BDTy > 0.8 )return 0;
  else if( (BDTx >   0.6 && BDTx <= 0.8 && BDTy >  0.6) || (BDTx > 0.8 && BDTy >  0.6 && BDTy <= 0.8)) return 1;
  else if( (BDTx >   0.4 && BDTx <= 0.6 && BDTy >  0.4) || (BDTx > 0.6 && BDTy >  0.4 && BDTy <= 0.6)) return 2;
  else if( (BDTx >   0.2 && BDTx <= 0.4 && BDTy >  0.2) || (BDTx > 0.4 && BDTy >  0.2 && BDTy <= 0.4)) return 3;
  else if( (BDTx >   0.0 && BDTx <= 0.2 && BDTy >  0.0) || (BDTx > 0.2 && BDTy >  0.0 && BDTy <= 0.2)) return 4;
  else if( (BDTx >  -0.2 && BDTx <= 0.0 && BDTy > -0.2) || (BDTx > 0.0 && BDTy > -0.2 && BDTy <= 0.0)) return 5;
		    				  				 
  else if( (BDTx >  -0.4 && BDTx <=-0.2 && BDTy > -0.4) || (BDTx >-0.2 && BDTy > -0.4 && BDTy <=-0.2)) return 6;
  else if( (BDTx >  -0.6 && BDTx <=-0.4 && BDTy > -0.6) || (BDTx >-0.4 && BDTy > -0.6 && BDTy <=-0.4)) return 7;
  else if( (BDTx >  -0.8 && BDTx <=-0.6 && BDTy > -0.8) || (BDTx >-0.6 && BDTy > -0.8 && BDTy <=-0.6)) return 8;
  else if( (BDTx >= -1.0 && BDTx <=-0.8 && BDTy >=-1.0) || (BDTx >-0.8 && BDTy >=-1.0 && BDTy <=-0.8)) return 9;

  else{
    std::cout << "values of BDT variables are out of bounds, please check\t" <<BDTx<<"\t"<<BDTy<<std::endl;
    exit(EXIT_FAILURE);}
} 



int unroll_2Dbdt_dps_SoBord_sqV1(float BDTx,float BDTy){
 
  if(BDTx  > 0.8 && BDTy > 0.8 )return 0;
  //else if( (BDTx >   0.8 && BDTx <= 0.9 && BDTy >  0.8) || (BDTx > 0.9 && BDTy >  0.8 && BDTy <= 0.9)) return 1;
  else if( (BDTx >   0.6 && BDTx <= 0.8 && BDTy >  0.6) || (BDTx > 0.8 && BDTy >  0.6 && BDTy <= 0.8)) return 1;
  else if( (BDTx >   0.4 && BDTx <= 0.6 && BDTy >  0.4) || (BDTx > 0.6 && BDTy >  0.4 && BDTy <= 0.6)) return 2;
  else if( (BDTx >   0.2 && BDTx <= 0.4 && BDTy >  0.2) || (BDTx > 0.4 && BDTy >  0.2 && BDTy <= 0.4)) return 3;
  else if( (BDTx >   0.0 && BDTx <= 0.2 && BDTy >  0.0) || (BDTx > 0.2 && BDTy >  0.0 && BDTy <= 0.2)) return 4;
  else if( (BDTx >  -0.2 && BDTx <= 0.0 && BDTy > -0.2) || (BDTx > 0.0 && BDTy > -0.2 && BDTy <= 0.0)) return 5;	 
  else if( (BDTx >  -0.4 && BDTx <=-0.2 && BDTy > -0.4) || (BDTx >-0.2 && BDTy > -0.4 && BDTy <=-0.2)) return 6;
  else if( (BDTx >  -0.6 && BDTx <=-0.4 && BDTy > -0.6) || (BDTx >-0.4 && BDTy > -0.6 && BDTy <=-0.4)) return 7;
  else if( (BDTx >  -0.8 && BDTx <=-0.6 && BDTy > -0.8) || (BDTx >-0.6 && BDTy > -0.8 && BDTy <=-0.6)) return 8;
  else if( BDTx  >= -1.0 && BDTx <=-0.8 && BDTy <= -0.6)return 9;
  else if( BDTx  >= -1.0 && BDTx <=-0.8 && BDTy > -0.6)return 10;
  else if( BDTx  >  -0.8 && BDTy <=-0.8) return 11;

  else{
    std::cout << "values of BDT variables are out of bounds, please check\t" <<BDTx<<"\t"<<BDTy<<std::endl;
    exit(EXIT_FAILURE);}
} 


int unroll_2Dbdt_dps_SoBord_sqV2(float BDTx,float BDTy){
 
  if(BDTx  > 0.75 && BDTy > 0.75 )return 0;
  else if( (BDTx >   0.6 && BDTx <= 0.75 && BDTy >  0.6) || (BDTx > 0.75 && BDTy >  0.6 && BDTy <= 0.75)) return 1;
  else if( (BDTx >   0.4 && BDTx <= 0.6 && BDTy >  0.4) || (BDTx > 0.6 && BDTy >  0.4 && BDTy <= 0.6)) return 2;
  else if( (BDTx >   0.2 && BDTx <= 0.4 && BDTy >  0.2) || (BDTx > 0.4 && BDTy >  0.2 && BDTy <= 0.4)) return 3;
  else if( (BDTx >   0.0 && BDTx <= 0.2 && BDTy >  0.0) || (BDTx > 0.2 && BDTy >  0.0 && BDTy <= 0.2)) return 4;
  else if( (BDTx >  -0.2 && BDTx <= 0.0 && BDTy > -0.2) || (BDTx > 0.0 && BDTy > -0.2 && BDTy <= 0.0)) return 5;	 
  else if( (BDTx >  -0.4 && BDTx <=-0.2 && BDTy > -0.4) || (BDTx >-0.2 && BDTy > -0.4 && BDTy <=-0.2)) return 6;
  else if( (BDTx >  -0.6 && BDTx <=-0.4 && BDTy > -0.6) || (BDTx >-0.4 && BDTy > -0.6 && BDTy <=-0.4)) return 7;

  else if( BDTx  >  -0.8 && BDTx <=-0.6 && BDTy > -0.6) return 8;
  else if( BDTx  >  -0.8 && BDTy > -0.8 && BDTy <=-0.6) return 9;

  else if( BDTx  >= -1.0 && BDTx <=-0.8 && BDTy <= -0.8)return 10;
  else if( BDTx  >= -1.0 && BDTx <=-0.8 && BDTy > -0.8) return 11;
  else if( BDTx  >  -0.8 && BDTy <=-0.8) return 12;

  else{
    std::cout << "values of BDT variables are out of bounds, please check\t" <<BDTx<<"\t"<<BDTy<<std::endl;
    exit(EXIT_FAILURE);}
} 

int unroll_2Dbdt_dps_SoBord_sqV3(float BDTx,float BDTy){
 
  if(BDTx  > 0.8 && BDTy > 0.8 )return 0;
  else if( (BDTx >   0.6 && BDTx <= 0.8 && BDTy >  0.6) || (BDTx > 0.8 && BDTy >  0.6 && BDTy <= 0.8)) return 1;
  else if( (BDTx >   0.4 && BDTx <= 0.6 && BDTy >  0.4) || (BDTx > 0.6 && BDTy >  0.4 && BDTy <= 0.6)) return 2;
  else if( (BDTx >   0.2 && BDTx <= 0.4 && BDTy >  0.2) || (BDTx > 0.4 && BDTy >  0.2 && BDTy <= 0.4)) return 3;
  else if( (BDTx >   0.0 && BDTx <= 0.2 && BDTy >  0.0) || (BDTx > 0.2 && BDTy >  0.0 && BDTy <= 0.2)) return 4;
  else if( (BDTx >  -0.2 && BDTx <= 0.0 && BDTy > -0.2) || (BDTx > 0.0 && BDTy > -0.2 && BDTy <= 0.0)) return 5;	 
  else if( (BDTx >  -0.4 && BDTx <=-0.2 && BDTy > -0.4) || (BDTx >-0.2 && BDTy > -0.4 && BDTy <=-0.2)) return 6;
  else if( (BDTx >  -0.6 && BDTx <=-0.4 && BDTy > -0.6) || (BDTx >-0.4 && BDTy > -0.6 && BDTy <=-0.4)) return 7;

  else if( BDTx  >  -0.8 && BDTx <=-0.6 && BDTy > -0.6) return 8;
  else if( BDTx  >  -0.8 && BDTy > -0.8 && BDTy <=-0.6) return 9;

  else if( BDTx  >= -1.0 && BDTx <=-0.8 && BDTy <= -0.8)return 10;
  else if( BDTx  >= -1.0 && BDTx <=-0.8 && BDTy > -0.8) return 11;
  else if( BDTx  >  -0.8 && BDTy <=-0.8) return 12;

  else{
    std::cout << "values of BDT variables are out of bounds, please check\t" <<BDTx<<"\t"<<BDTy<<std::endl;
    exit(EXIT_FAILURE);}
} 
 
int unroll_2Dbdt_dps_SoBord_diag(float BDTx,float BDTy){

  float x1[]={-0.8,-0.4,-0.2,0,0.2,0.4,0.6,0.8,1,1};//,1};
  float y1[]={-1,-1,-0.8,-0.6,-0.4,-0.2,0,0.2,0.4,0.6};//,0.8};
  float x2[]={-1,-1,-0.8,-0.6,-0.4,-0.2,0,0.2,0.4,0.6};//,0.8};
  float y2[]={-0.8,-0.4,-0.2,0,0.2,0.4,0.6,0.8,1,1};//,1};
  float bigx1[]={-0.4,-1};
  float bigy1[]={-1.0,-0.4};
  float bigx2[]={1,0.4};
  float bigy2[]={0.4,1};
//am  float bigx1[]={-0.4,-1};
//am  float bigy1[]={-1.0,-0.4};
//am  float bigx2[]={1,0.4};
//am  float bigy2[]={0.4,1};


  int bin;  int nbins=10;
  float m0 = (y2[0]-y1[0])/(x2[0]-x1[0]);
  float f0 = y1[0] - m0*x1[0];
  float mtop = (y2[9]-y1[9])/(x2[9]-x1[9]);
  float ftop = y1[9] - mtop*x1[9];
  float mbig1 = (bigy2[0]-bigy1[0])/(bigx2[0]-bigx1[0]);
  float mbig2 = (bigy2[1]-bigy1[1])/(bigx2[1]-bigx1[1]);
  float fbig1 = bigy1[0] - mbig1*bigx1[0];
  float fbig2 = bigy1[1] - mbig2*bigx1[1];
  if( (BDTx-m0*BDTy - f0) <0 ) bin=0;
  else if( (BDTx-mtop*BDTy - ftop) >=0 ) bin=10;
  else if( (BDTx-mbig1*BDTy - fbig1) <0 ) bin=11;
  else if( (BDTx-mbig2*BDTy - fbig2) >=0 ) bin=12;
  else {
    //    std::cout<<"in here"<<std::endl;
    for (int i = 1; i < nbins; i++){ 
      float slope1=(y2[i-1]-y1[i-1])/(x2[i-1]-x1[i-1]);
      float line1 = y1[i-1] - slope1*x1[i-1]; 
      float slope2=(y2[i]-y1[i])/(x2[i]-x1[i]);
      float line2 = y1[i] - slope2*x1[i];
      float fprime1 = BDTy - slope1*BDTx;
      float fprime2 = BDTy - slope2*BDTx;
      float lowerBound = fprime1-line1;
      float upperBound = fprime2-line2;
      if( lowerBound >=0 && upperBound < 0){
	bin=i;
      }
      else{	continue;}
    }

  }
  //std::cout<<"for  BDTx = \t"<<BDTx<<"\t and BDTy = \t"<<BDTy<<"\t i get bin number \t"<<bin<<std::endl;}

  return bin;
  
}

int unroll_2Dbdt_dps_SoBord_diag_pc(float BDTx,float BDTy){
  //pchang's suggestion
  float x1[]={-0.4,-0.2,0,0.2,0.4,0.6,0.8,1,1};//,1};
  float y1[]={-1,-0.8,-0.6,-0.4,-0.2,0,0.2,0.4,0.6};//,0.8};
  float x2[]={-1,-0.8,-0.6,-0.4,-0.2,0,0.2,0.4,0.6};//,0.8};
  float y2[]={-0.4,-0.2,0,0.2,0.4,0.6,0.8,1,1};//,1};
  float bigx1[]={-0.4,-1};
  float bigy1[]={-1.0,-0.4};
  float bigx2[]={1,0.4};
  float bigy2[]={0.4,1};
//am  float bigx1[]={-0.4,-1};
//am  float bigy1[]={-1.0,-0.4};
//am  float bigx2[]={1,0.4};
//am  float bigy2[]={0.4,1};


  int bin;  int nbins=9;
  float m0 = (y2[0]-y1[0])/(x2[0]-x1[0]);
  float f0 = y1[0] - m0*x1[0];
  float mtop = (y2[8]-y1[8])/(x2[8]-x1[8]);
  float ftop = y1[8] - mtop*x1[8];
  float mbig1 = (bigy2[0]-bigy1[0])/(bigx2[0]-bigx1[0]);
  float mbig2 = (bigy2[1]-bigy1[1])/(bigx2[1]-bigx1[1]);
  float fbig1 = bigy1[0] - mbig1*bigx1[0];
  float fbig2 = bigy1[1] - mbig2*bigx1[1];
  if( (BDTx-m0*BDTy - f0) <0 ) bin=0;
  else if( (BDTx-mtop*BDTy - ftop) >=0 ) bin=9;
  else if( (BDTx-mbig1*BDTy - fbig1) <0 ) bin=10;
  else if( (BDTx-mbig2*BDTy - fbig2) >=0 ) bin=10;
  else {
    //    std::cout<<"in here"<<std::endl;
    for (int i = 1; i < nbins; i++){ 
      float slope1=(y2[i-1]-y1[i-1])/(x2[i-1]-x1[i-1]);
      float line1 = y1[i-1] - slope1*x1[i-1]; 
      float slope2=(y2[i]-y1[i])/(x2[i]-x1[i]);
      float line2 = y1[i] - slope2*x1[i];
      float fprime1 = BDTy - slope1*BDTx;
      float fprime2 = BDTy - slope2*BDTx;
      float lowerBound = fprime1-line1;
      float upperBound = fprime2-line2;
      if( lowerBound >=0 && upperBound < 0){
	bin=i;
      }
      else{	continue;}
    }

  }
  //std::cout<<"for  BDTx = \t"<<BDTx<<"\t and BDTy = \t"<<BDTy<<"\t i get bin number \t"<<bin<<std::endl;}

  return bin;
  
}


int unroll_2Ddnn_dps_SoBord_diag(float DNNx,float DNNy){
  float x1[]={0.1,0.2,0.3,0.42,0.5,0.6,0.68,0.78,0.88,1.0};
  float y1[]={0,0,0,0.1,0.22,0.32,0.41,0.51,0.62,0.75};
  float x2[]={0,0,0,0.1,0.22,0.32,0.4,0.5,0.62,0.75};
  float y2[]={0.1,0.2,0.3,0.4,0.5,0.58,0.68,0.76,0.87,1};
  //points are like (x1[0],y1[0]) and so on 
  float bigx1[]={0.3,0}; 
  float bigy1[]={0,0.3};
  float bigx2[]={1,0.75};
  float bigy2[]={0.75,1};

  int bin;  int nbins=10;
  float m0 = (y2[0]-y1[0])/(x2[0]-x1[0]);
  float f0 = y1[0] - m0*x1[0];
  float mtop = (y2[9]-y1[9])/(x2[9]-x1[9]);
  float ftop = y1[9] - mtop*x1[9];
  float mbig1 = (bigy2[0]-bigy1[0])/(bigx2[0]-bigx1[0]);
  float mbig2 = (bigy2[1]-bigy1[1])/(bigx2[1]-bigx1[1]);
  float fbig1 = bigy1[0] - mbig1*bigx1[0];
  float fbig2 = bigy1[1] - mbig2*bigx1[1];
  if( (DNNx-m0*DNNy - f0) <0 ) bin=0;
  else if( (DNNx-mtop*DNNy - ftop) >=0 ) bin=10;
  else if( (DNNx-mbig1*DNNy - fbig1) <0 ) bin=11;
  else if( (DNNx-mbig2*DNNy - fbig2) >=0 ) bin=12;
  else {
    //    std::cout<<"in here"<<std::endl;
    for (int i = 1; i < nbins; i++){ 
      float slope1=(y2[i-1]-y1[i-1])/(x2[i-1]-x1[i-1]);
      float line1 = y1[i-1] - slope1*x1[i-1]; 
      float slope2=(y2[i]-y1[i])/(x2[i]-x1[i]);
      float line2 = y1[i] - slope2*x1[i];
      float fprime1 = DNNy - slope1*DNNx;
      float fprime2 = DNNy - slope2*DNNx;
      float lowerBound = fprime1-line1;
      float upperBound = fprime2-line2;
      if( lowerBound >=0 && upperBound < 0){
	bin=i;
      }
      else{	continue;}
    }

  }
  //std::cout<<"for  DNNx = \t"<<DNNx<<"\t and DNNy = \t"<<DNNy<<"\t i get bin number \t"<<bin<<std::endl;}

  return bin;
  
}




void functions() {}




