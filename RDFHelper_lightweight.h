#include "ROOT/RDataFrame.hxx"
#include "ROOT/RVec.hxx"
#include "TCanvas.h"
#include "TH1D.h"
#include "TLatex.h"
#include "Math/Vector4D.h"
#include "TStyle.h"
#include "TMath.h"
#include <algorithm> 
#include "TVector3.h"

template<typename T>
std::vector<T> Particle_fourvec(T Particle_pt, T Particle_eta, T Particle_phi, T Particle_mass) {

  const ROOT::Math::PtEtaPhiMVector p4(Particle_pt, Particle_eta, Particle_phi, Particle_mass);
  T Particle_E  = p4.E();
  T Particle_px = p4.px();
  T Particle_py = p4.py();
  T Particle_pz = p4.pz();

  std::vector<T> Particle_p = {Particle_E, Particle_px, Particle_py, Particle_pz};
  return Particle_p;
}

template<typename T>
std::vector<ROOT::RVec<T>> ParticleVec_fourvec(ROOT::RVec<T> Particle_pt, ROOT::RVec<T> Particle_eta, ROOT::RVec<T> Particle_phi, ROOT::RVec<T> Particle_mass) {
  size_t nParticle = Particle_mass.size();
  ROOT::RVec<T> Particle_E(nParticle, -1);
  ROOT::RVec<T> Particle_px(nParticle, -1);
  ROOT::RVec<T> Particle_py(nParticle, -1);
  ROOT::RVec<T> Particle_pz(nParticle, -1);


  for(size_t i=0; i<nParticle; ++i){
    const ROOT::Math::PtEtaPhiMVector p4(Particle_pt[i], Particle_eta[i], Particle_phi[i], Particle_mass[i]);
    Particle_E[i]  = p4.E();
    Particle_px[i] = p4.px();
    Particle_py[i] = p4.py();
    Particle_pz[i] = p4.pz();
  }

  std::vector<ROOT::RVec<T>> Particle_p = {Particle_E, Particle_px, Particle_py, Particle_pz};
  return Particle_p;
}