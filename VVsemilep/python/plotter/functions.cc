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
#include "PhysicsTools/Heppy/interface/METzCalculator_Run2.h"
#include "PhysicsTools/Heppy/interface/METzCalculator.h"
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
  float dR=std::sqrt(deltaR2(eta1,phi1,eta2,phi2));
  if (dR < 0.8){
    std::cout<<dR<<"\t inputs \t"<<eta1<<"\t"<<phi1<<"\t"<<eta2<<"\t"<<phi2<<std::endl;}
  return std::sqrt(deltaR2(eta1,phi1,eta2,phi2));
}

float pt_2(float pt1, float phi1, float pt2, float phi2) {
    phi2 -= phi1;
    return hypot(pt1 + pt2 * std::cos(phi2), pt2*std::sin(phi2));
}

float mt_2(float pt1, float phi1, float pt2, float phi2) {
    return std::sqrt(2*pt1*pt2*(1-std::cos(phi1-phi2)));
}

float mass_2(float pt1, float eta1, float phi1, int pdgId1, float pt2, float eta2, float phi2, int pdgId2) {
    typedef ROOT::Math::LorentzVector<ROOT::Math::PtEtaPhiM4D<double> > PtEtaPhiMVector;
    float m1= abs(pdgId1) == 13 ? 0.106 : 0.512e-3;
    float m2= abs(pdgId2) == 13 ? 0.106 : 0.512e-3;
    PtEtaPhiMVector p41(pt1,eta1,phi1,m1);
    PtEtaPhiMVector p42(pt2,eta2,phi2,m2);
    return (p41+p42).M();
}

float Mass_2(float pt1, float eta1, float phi1, float m1, float pt2, float eta2, float phi2, float m2) {
    typedef ROOT::Math::LorentzVector<ROOT::Math::PtEtaPhiM4D<double> > PtEtaPhiMVector;
    PtEtaPhiMVector p41(pt1,eta1,phi1,m1);
    PtEtaPhiMVector p42(pt2,eta2,phi2,m2);    
    return (p41+p42).M();
}

float ptll(float pt1, float eta1, float phi1, int pdgId1, float pt2, float eta2, float phi2, int pdgId2) {
    typedef ROOT::Math::LorentzVector<ROOT::Math::PtEtaPhiM4D<double> > PtEtaPhiMVector;
    float m1= abs(pdgId1) == 13 ? 0.106 : 0.512e-3;
    float m2= abs(pdgId2) == 13 ? 0.106 : 0.512e-3;
    PtEtaPhiMVector p41(pt1,eta1,phi1,m1);
    PtEtaPhiMVector p42(pt2,eta2,phi2,m2);
    return (p41+p42).Pt();
}


float ptWV(float pt1, float eta1, float phi1, int pdgId, float pt2, float eta2, float phi2, float mass, float met, float metphi) {
    typedef ROOT::Math::LorentzVector<ROOT::Math::PtEtaPhiM4D<double> > PtEtaPhiMVector;
    float m1= abs(pdgId) == 13 ? 0.106 : 0.512e-3;
    PtEtaPhiMVector p41(pt1,eta1,phi1,m1);
    PtEtaPhiMVector p42(pt2,eta2,phi2,mass);
    PtEtaPhiMVector mv(met,0.,metphi,0.);
    return (p41+p42+mv).Pt();
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

double METz_calc_run2(float pt1, float eta1, float phi1,int pdgId1,float met, float metphi,int type=0){
  //  typedef ROOT::Math::LorentzVector<ROOT::Math::PtEtaPhiM4D<double> > PtEtaPhiMVector;
  //  PtEtaPhiMVector lep(pt1,eta1,phi1,0.0);
  //  PtEtaPhiMVector mv(met,0.,metphi,0.);

    TLorentzVector p4l(0.,0.,0.,0);
    p4l.SetPtEtaPhiM(pt1,eta1,phi1,0.0);
    TLorentzVector mv(0.,0.,0.,0.);
    mv.SetPtEtaPhiM(met,0.,metphi,0.0);
    heppy::METzCalculator_Run2 NeutrinoPz_run2;
    //std::cout<<"check this lepton pt\t"<<p41.Pt()<<"\t"<<p41.E()<<"\t here"<<std::endl;
    //std::cout<<"check this MET   "<<mv.Pt()<<std::endl;
    NeutrinoPz_run2.SetMET(mv);
    NeutrinoPz_run2.SetLepton(p4l);
    NeutrinoPz_run2.SetLeptonType(pdgId1);
    double pz1_type0 = NeutrinoPz_run2.Calculate();
    //    std::cout<<"and the result is"<<pz1_type0<<std::endl;
    return pz1_type0;
}

double METz_calc(float pt1, float eta1, float phi1,int pdgId1,float met, float metphi,int type=0){
  //complex roots-> pick the real part
  //if real roots
  //type 0,1,2,3
  // type0: pick the one closest to pz of muon  unless pznu is > 300 then pick the most central root 
  //typ1: pick the one closest to pz of muon 
  //typ2: pick the most central root
  //typ3:pick the largest value of the cosine
    float m1= abs(pdgId1) == 13 ? 0.106 : 0.512e-3;
    TLorentzVector p4l(0.,0.,0.,0);
    p4l.SetPtEtaPhiM(pt1,eta1,phi1,m1);
    TLorentzVector mv(0.,0.,0.,0.);
    mv.SetPtEtaPhiM(met,0.,metphi,0.0);
    heppy::METzCalculator_Run2 NeutrinoPz_run2_M;
    //std::cout<<"check this lepton pt\t"<<p41.Pt()<<"\t"<<p41.E()<<"\t here"<<std::endl;
    //std::cout<<"check this MET   "<<mv.Pt()<<std::endl;
    NeutrinoPz_run2_M.SetMET(mv);
    NeutrinoPz_run2_M.SetLepton(p4l);
    NeutrinoPz_run2_M.SetLeptonType(pdgId1);
    double pz1_type0 = NeutrinoPz_run2_M.Calculate(type);
    //    std::cout<<"and the result is"<<pz1_type0<<std::endl;
    return pz1_type0;
}

double mass_WV_el(float jpt,float jeta,float jphi, float jm,float lpt,float leta,float lphi,float met,float metphi, int type){
  //FIXME: compute neupz first and pass it as an argument ->get rid of pdgId and type args
  float massWV=-999.0;
  TLorentzVector lep(0.,0.,0.,0);
  TLorentzVector jet(0.,0.,0.,0);
  TLorentzVector metV(0.,0.,0.,0);
  TLorentzVector mWV(0.,0.,0.,0);
  //float lmass= abs(lpdgId) == 13 ? 0.106 : 0.512e-3;
  lep.SetPtEtaPhiM(lpt,leta,lphi,0.512e-3);
  jet.SetPtEtaPhiM(jpt,jeta,jphi,jm);
  
  float pz1=METz_calc(lpt,leta, lphi,11,met,metphi,type);
  metV.SetPxPyPzE(met*TMath::Cos(metphi), met*TMath::Sin(metphi),pz1,sqrt(met*met+pz1*pz1));
  mWV=lep+jet+metV;
  massWV=mWV.M();
  return massWV;
}

double mass_WV_mu(float jpt,float jeta,float jphi, float jm,float lpt,float leta,float lphi,float met,float metphi, int type){
  //FIXME: compute neupz first and pass it as an argument ->get rid of pdgId and type args
  float massWV=-999.0;
  TLorentzVector lep(0.,0.,0.,0);
  TLorentzVector jet(0.,0.,0.,0);
  TLorentzVector metV(0.,0.,0.,0);
  TLorentzVector mWV(0.,0.,0.,0);
  //float lmass= abs(lpdgId) == 13 ? 0.106 : 0.512e-3;
  
  lep.SetPtEtaPhiM(lpt,leta,lphi,0.106);
  jet.SetPtEtaPhiM(jpt,jeta,jphi,jm);
  
  float pz1=METz_calc(lpt,leta, lphi,13,met,metphi,type);
  metV.SetPxPyPzE(met*TMath::Cos(metphi), met*TMath::Sin(metphi),pz1,sqrt(met*met+pz1*pz1));
  mWV=lep+jet+metV;
  massWV=mWV.M();
  return massWV;
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

float HEMhandle(int year, float phi1, float eta1, float phi2, float eta2, int pdgId, int run, bool isData){
  //  bool isData=false;
  float HEM_eta_min =  -3.2; float HEM_eta_max = -1.3;
  float HEM_phi_min= -1.57; float HEM_phi_max= -0.87;
  float weight=1.0;  bool vetoHEM=false; bool vetofj=false; bool vetoel=false;
  //  isData=run>319077 ? true : false; //assuming for MC run=1 always!!
  
  vetofj = (year>2017 && eta1 < HEM_eta_max && eta1 > HEM_eta_min && phi1 < HEM_phi_max && phi1 > HEM_phi_min) ? true : false;
  vetoel = (abs(pdgId) == 11 && year>2017 && eta2 > -2.5 && eta2 < -1.479 && phi2 < HEM_phi_max && phi2 > HEM_phi_min) ? true : false;
  vetoHEM = vetofj||vetoel;
  if (vetoHEM){
    if (isData) {
      if(run > 319077){ 	weight=0;      }
      else{	weight=1.0;}    }//isdata
    else{      weight=0.35;    }//for MC
  }//veto HEM
  else{	weight=1.0;    }//if outside HEM
  //std::cout<<"isdata\t"<<isData<<"\t run\t"<<run<<"\t vetoHEM \t"<<vetoHEM<<"\t wt\t"<<weight<<endl;
  return weight;
  
}



float triggerSF_ttH(int pdgid1, float pt1, int pdgid2, float pt2, int nlep, int year, int suberaid, int var=0){

  TString yearString= TString::Format("%d",year) + (( year == 2016 && suberaid == 0) ? "APV" : "");

  if (nlep == 2){
    if (abs(pdgid1*pdgid2) == 121){

      if (yearString == "2016APV"){
        if (pt2 < 20){
          return 0.96*(1 + var*0.02);
        }
        else if (pt2 > 20 && pt2 < 55){
          return 0.99*(1 + var*0.01);
        }
        else return 1.*(1 + var*0.01);
      }

      if (yearString == "2016"){
        if (pt2 < 40){
          return 0.98*(1 + var*0.02);
        }
        else return 0.99*(1 + var*0.01);
      }

      if (yearString == "2017"){
        if (pt2<25) return 0.96*(1 + var*0.02);
	else return 0.985*(1 + var*0.01);
      }

      if (yearString == "2018"){
        if (pt2<20){
	  return 0.98*(1 + var*0.01);
        }
        else if (pt2 > 20 && pt2 < 70){
          return 1.*(1 + var*0.01);
        }
        else return 1.01*(1 + var*0.005);
      }
    }

    else if ( abs(pdgid1*pdgid2) == 143){

      if (yearString == "2016APV"){
        if (pt2 < 25){
          return 0.98*(1 + var*0.01);
        }
        else if (pt2 > 25 && pt2 < 70){
          return 0.99*(1 + var*0.005);
        }
        else return 1.*(1 + var*0.005);
      }

      if (yearString == "2016"){
        if (pt2 < 20){
          return 0.98*(1 + var*0.02);
        }
        else return 0.99*(1 + var*0.01);
      }

      if (yearString == "2017"){
	if (pt2<20) return 0.99*(1 + var*0.01);
        else if (pt2 > 20 && pt2 < 40){
          return 0.98*(1 + var*0.01);
        }
        else return 0.995*(1 + var*0.005);
      }

      if (yearString == "2018"){
        if (pt2<20) return 0.98*(1 + var*0.01);
        else if (pt2 > 20 && pt2 < 55){
          return 0.99*(1 + var*0.005);
        }
        else  return 1.*(1 + var*0.005);
      }
    }
  
    else{
      if (yearString == "2016APV"){
        if (pt2 < 25){
          return 0.98*(1 + var*0.01);
        }
        else return 0.99*(1 + var*0.01);
      }

      if (yearString == "2016"){
        if (pt2 < 20){
          return 0.97*(1 + var*0.01);
        }
        else return 0.99*(1 + var*0.01);
      }

      if (yearString == "2017"){
        if (pt2 < 25){
          return 0.97*(1 + var*0.01);
        }
        else return 0.99*(1 + var*0.01);
      }

      if (yearString == "2018"){
        return 0.99*(1 + var*0.01);
      }
    }

  }
  else {
    
    if (yearString == "2016APV" || yearString == "2016"){
      return 1.*(1 + var*0.02);
    }
    if (yearString == "2017" || yearString == "2018"){
      return 1.*(1 + var*0.01);
    }

  }

}



//##########################################
float pNetSFMD_WvsQCD(float pt, int year, int suberaid, float WP=1.0,int var=0){
  //WP 0.5/1.0/2.5% of mistag rate
  TString yearString= TString::Format("%d",year) + (( year == 2016 && suberaid == 0) ? "APV" : "");
  if (yearString == "2018"){

    if(pt >= 200 && pt < 300){
      if(WP == 0.5){
	return 0.81*(1 + var*0.03);
      }
      else if(WP == 1.0){
	return 0.87*(1 + var*0.02);
      }
      else{
	if (var > 0){
	  return 0.92*(1 + var*0.03);}
	else {return 0.92*(1 + var*0.02);}
      }
    }
    
    else if(pt >= 300 && pt < 400){
      if(WP == 0.5){
	return 0.81*(1 + var*0.02);
      }
      else if(WP == 1.0){
	return 0.86*(1 + var*0.02);
      }
      else{
	  return 0.92*(1 + var*0.02);}
    }

    else {
      if(WP == 0.5){
	return 0.77*(1 + var*0.04);
      }
      else if(WP == 1.0){
	return 0.82*(1 + var*0.04);
      }
      else{
	  return 0.87*(1 + var*0.04);}
    }

  }//2018





  if (yearString == "2017"){
    if(pt >= 200 && pt < 300){
      if(WP == 0.5){
	return 0.85*(1 + var*0.03);
      }
      else if(WP == 1.0){
	return 0.91*(1 + var*0.02);
      }
      else{
	return 0.96*(1 + var*0.03);}
    
    }
    
    else if(pt >= 300 && pt < 400){
      if(WP == 0.5){
	return 0.85*(1 + var*0.03);
      }
      else if(WP == 1.0){
	return 0.90*(1 + var*0.02);
      }
      else{
	if(var > 0){return 0.95*(1 + var*0.03);}
	else{return 0.95*(1 + var*0.02);}
      }
    }

    else{
      if(WP == 0.5){
	return 0.86*(1 + var*0.05);
      }
      else if(WP == 1.0){
	if(var > 0){return 0.89*(1 + var*0.05);}
	else{return 0.89*(1 + var*0.04);}
      }
      else{
	  return 0.98*(1 + var*0.05);}
    }

  }//2017




  if (yearString == "2016APV"){

    if(pt >= 200 && pt < 300){
      if(WP == 0.5){
	return 0.85*(1 + var*0.03);
      }
      else if(WP == 1.0){
	return 0.90*(1 + var*0.03);
      }
      else{	  return 0.90*(1 + var*0.02);
      }
    }
    
    else if(pt >= 300 && pt < 400){
      if(WP == 0.5){
	return 0.86*(1 + var*0.04);
      }
      else if(WP == 1.0){
	return 0.87*(1 + var*0.04);
      }
      else{
	  return 0.94*(1 + var*0.04);}
    }

    else {
      if(WP == 0.5){
	return 0.86*(1 + var*0.08);
      }
      else if(WP == 1.0){
	if(var > 0){return 0.92*(1 + var*0.08);}
	else{	return 0.92*(1 + var*0.07);}
      }
      else{
	  return 0.94*(1 + var*0.07);}
    }

  }//2016APV



  if (yearString == "2016"){

    if(pt >= 200 && pt < 300){
      if(WP == 0.5){
	return 0.85*(1 + var*0.04);
      }
      else if(WP == 1.0){
	if(var > 0){return 0.89*(1 + var*0.04);}
	else{	return 0.89*(1 + var*0.03);}
      }
      else{
	  return 0.95*(1 + var*0.04);}

    }
    
    else if(pt >= 300 && pt < 400){
      if(WP == 0.5){
	return 0.83*(1 + var*0.04);
      }
      else if(WP == 1.0){
	return 0.86*(1 + var*0.04);
      }
      else{
	  return 0.91*(1 + var*0.04);}
    }

    else {
      if(WP == 0.5){
	if(var > 0){return 0.69*(1 + var*0.07);}
	else{	return 0.69*(1 + var*0.06);}
      }
      else if(WP == 1.0){
	return 0.73*(1 + var*0.07);
      }
      else{
	  return 0.84*(1 + var*0.07);}
    }
  
  }//2016




  //need to implement 2016 


}//pNet


//###########################################


float ttH_2lss_ifflav(int LepGood1_pdgId, int LepGood2_pdgId, float ret_ee, float ret_em, float ret_mm){
  if (abs(LepGood1_pdgId)==11 && abs(LepGood2_pdgId)==11) return ret_ee;
  if ((abs(LepGood1_pdgId) != abs(LepGood2_pdgId)))       return ret_em;
  if (abs(LepGood1_pdgId)==13 && abs(LepGood2_pdgId)==13) return ret_mm;
  std::cerr << "ERROR: invalid input " << abs(LepGood1_pdgId) << ", " << abs(LepGood1_pdgId) << std::endl;
  assert(0);
  return 0;
}

void functions() {}




