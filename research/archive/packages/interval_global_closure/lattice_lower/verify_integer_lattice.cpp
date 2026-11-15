// Exact exhaustive lattice game-value lower verifier, 2026-11-13.
// The separate quantization theorem transfers its minimum to the unrestricted
// game. Cost precision is independent of the CDF denominator; no beam is used.
#include <algorithm>
#include <cstdint>
#include <cstdlib>
#include <fstream>
#include <iostream>
#include <limits>
#include <vector>
using namespace std;
using U=uint64_t;using Wide=__uint128_t;
const U INF=numeric_limits<U>::max();
struct State {U cost;uint32_t l,r;bool center;};
int main(int argc,char**argv){
  if(argc<3||argc>5){cerr<<"usage: verify_integer_lattice input.bin output.json [cost_precision [outward_cutoff]]\n";return 2;}
  U precision=1;
  if(argc>=4){
    char* end=nullptr;precision=strtoull(argv[3],&end,10);
    if(!end||*end||!precision||precision>=(U(1)<<32))return 2;
  }
  uint32_t cutoff=2;
  if(argc==5){
    if(string(argv[4])!="1"&&string(argv[4])!="2")return 2;
    cutoff=uint32_t(argv[4][0]-'0');
  }
  ifstream in(argv[1],ios::binary);uint32_t B,NT,NX,version;U D;
  in.read((char*)&version,4);in.read((char*)&B,4);in.read((char*)&NT,4);in.read((char*)&NX,4);in.read((char*)&D,8);
  if(version!=1||B==0||B>(1U<<20)||B%2||NX!=2*B+1||NT!=6*B+1||!D||D%2||Wide(32)*D*B*precision>Wide(INF)/2)return 3;
  const uint32_t N=cutoff*B;const U C=2*D*B*precision,budget=12*U(B);
  vector<U> f(size_t(NT)*NX);in.read((char*)f.data(),f.size()*8);if(!in)return 4;
  auto idx=[&](uint32_t n,uint32_t j){return size_t(n)*NX+j;};
  for(uint32_t n=0;n<NT;++n)for(uint32_t j=0;j<NX;++j){
    U a=f[idx(n,j)];if(a>D||a+f[idx(n,2*B-j)]!=D)return 5;
    if(n>=(cutoff+1)*B && a!=D/2)return 10;
    if(n>=cutoff*B && n+1<NT){
      if(j>=B && j+1<NX && f[idx(n+1,j+1)]!=a)return 11;
      if(j<=B && j>0 && f[idx(n+1,j-1)]!=a)return 12;
    }
    if(n+1<NT){
      if(j&&f[idx(n+1,j-1)]>a)return 6;
      if(j+1<NX&&f[idx(n+1,j+1)]<a)return 7;
    }
  }
  // Small-denominator certificates use the CDF numerator itself as a rank.
  // This changes no order comparison and avoids two full-table rank arrays.
  const bool direct_records=D<=(U(1)<<20);
  vector<U> values;
  vector<uint32_t> rank,other;
  if(direct_records){
    values.resize(D+1);
    for(U a=0;a<=D;++a)values[a]=a;
  }else{
    values.reserve(f.size()*2+3);values={0,D/2,D};
    for(U a:f){values.push_back(a);values.push_back(D-a);}
    sort(values.begin(),values.end());values.erase(unique(values.begin(),values.end()),values.end());
    if(values.size()>=(U(1)<<31))return 8;
    rank.resize(f.size());other.resize(f.size());
    for(size_t i=0;i<f.size();++i){rank[i]=lower_bound(values.begin(),values.end(),f[i])-values.begin();other[i]=lower_bound(values.begin(),values.end(),D-f[i])-values.begin();}
  }
  auto left_rank=[&](size_t i)->uint32_t{return direct_records?uint32_t(f[i]):rank[i];};
  auto right_rank=[&](size_t i)->uint32_t{return direct_records?uint32_t(D-f[i]):other[i];};
  vector<U> sl(f.size()),sr(f.size());
  for(int n=int(NT)-2;n>=0;--n)for(uint32_t j=0;j<NX;++j){
    if(j)sl[idx(n,j)]=(f[idx(n,j)]+f[idx(n+1,j-1)])*precision+sl[idx(n+1,j-1)];
    if(j+1<NX)sr[idx(n,j)]=(2*D-f[idx(n,j)]-f[idx(n+1,j+1)])*precision+sr[idx(n+1,j+1)];
  }
  // Ranks below the future minimum endpoint trace stay at that endpoint.
  // Include the preceding row: an odd-time boundary point lies between the
  // two neighboring even-time characteristic-lattice vertices.
  vector<U> endpoint_floor(NT);
  U endpoint_min=D;
  for(int n=int(NT)-1;n>=0;--n){
    endpoint_min=min(endpoint_min,f[idx(n,0)]);
    endpoint_floor[n]=n?min(endpoint_min,f[idx(n-1,0)]):endpoint_min;
  }
  auto edge=[&](U record,U a,U b)->U{
    record=min(record,a);
    if(b>=record)return 2*record*precision;
    if(a<=record)return (a+b)*precision;
    U d=record-b,den=a-b;U ceiling=U((Wide(precision)*d*d+den-1)/den);
    return 2*record*precision-ceiling;
  };
  auto pursuit=[&](uint32_t n,uint32_t j,U record,int dir)->U{
    if(!record)return 0;
    uint32_t dist=dir<0?j:2*B-j;if(!dist)return 0;
    auto at=[&](uint32_t k)->U{U a=f[idx(n+k,uint32_t(int(j)+dir*int(k)))];return dir<0?a:D-a;};
    auto suffix=[&](uint32_t k)->U{return(dir<0?sl:sr)[idx(n+k,uint32_t(int(j)+dir*int(k)))];};
    if(at(0)<=record)return suffix(0);
    if(at(dist)>=record)return 2*record*dist*precision;
    uint32_t low=0,high=dist;
    while(high-low>1){uint32_t mid=(low+high)/2;if(at(mid)>record)low=mid;else high=mid;}
    return 2*record*low*precision+edge(record,at(low),at(high))+suffix(high);
  };
  vector<vector<State>> front(NX),next(NX);
  uint32_t zero=lower_bound(values.begin(),values.end(),U(0))-values.begin();
  uint32_t half=lower_bound(values.begin(),values.end(),D/2)-values.begin();
  U best=pursuit(0,2*B,f[idx(0,2*B)],-1);
  auto rollout=[&](uint32_t n,uint32_t j,const State&s){
    U l=values[s.l],r=values[s.r];
    U left=s.cost+pursuit(n,j,l,-1)+2*r*j*precision+pursuit(n+j,0,r,1);
    best=min(best,left);
    if(s.center||n<=j-B){
      U right=s.cost+pursuit(n,j,r,1)+2*l*(2*B-j)*precision+pursuit(n+2*B-j,2*B,l,-1);
      best=min(best,right);
    }
  };
  for(uint32_t j=B;j<=2*B;j+=2){
    State s={0,left_rank(idx(0,j)),j==2*B?zero:right_rank(idx(0,j)),j==B};
    front[j].push_back(s);rollout(0,j,s);
  }
  vector<U> allbit(values.size()+1),centerbit(values.size()+1);
  vector<U> astamp(values.size()+1),cstamp(values.size()+1);U epoch=0;
  uint64_t generated=0,dominated=0,bounded=0,deadline=0,accepted=0,maxlive=0,maxnode=0;
  vector<uint64_t> layers;
  for(uint32_t n=0;n<N;++n){
    for(auto&v:next)v.clear();
    for(uint32_t j=1;j<2*B;++j)for(const State&s:front[j])for(int dir:{-1,1}){
      uint32_t k=uint32_t(int(j)+dir),nn=n+1;bool centered=s.center||k==B;
      ++generated;
      if(!centered&&(k<B||nn+k-B>2*B)){++deadline;continue;}
      size_t i0=idx(n,j),i1=idx(nn,k);
      U cost=s.cost+edge(values[s.l],f[i0],f[i1])+edge(values[s.r],D-f[i0],D-f[i1]);
      uint32_t l=k==0?zero:min(s.l,left_rank(i1));uint32_t r=k==2*B?zero:min(s.r,right_rank(i1));
      if(cost>=best){++bounded;continue;}
      if(k==0||k==2*B){
        U total=cost+pursuit(nn,k,values[k==0?r:l],k==0?1:-1);
        best=min(best,total);continue;
      }
      if(nn==N){
        if(cutoff==1&&!centered){
          if(l<half||r>half||k<=B)return 9;
          rollout(nn,k,{cost,l,r,false});
          continue;
        }
        if(!centered||l>half||r>half)return 9;
        U ll=values[l],rr=values[r];
        U terminal=min(2*(ll+rr)*(2*B-k)+4*B*ll,2*(ll+rr)*k+4*B*rr)*precision;
        best=min(best,cost+terminal);continue;
      }
      U independent=pursuit(nn,k,values[l],-1)+pursuit(nn,k,values[r],1);
      U fixed_left=min(values[l],endpoint_floor[nn]);
      U fixed_right=min(values[r],endpoint_floor[nn]);
      independent+=min(4*fixed_right*k,4*fixed_left*(2*B-k))*precision;
      U lower=independent>budget?independent-budget:0;
      if(cost+lower>=best){++bounded;continue;}
      next[k].push_back({cost,l,r,centered});
    }
    uint64_t live=0;
    for(uint32_t j=1;j<2*B;++j){
      auto&v=next[j];if(v.empty())continue;
      sort(v.begin(),v.end(),[](const State&a,const State&b){
        if(a.l!=b.l)return a.l<b.l;
        if(a.r!=b.r)return a.r<b.r;
        if(a.cost!=b.cost)return a.cost<b.cost;
        return a.center>b.center;
      });
      ++epoch;size_t out=0;
      for(const State&s:v){
        U low=INF;auto&bit=s.center?centerbit:allbit;auto&stamp=s.center?cstamp:astamp;
        for(uint32_t k=s.r+1;k;k-=k&-k)if(stamp[k]==epoch)low=min(low,bit[k]);
        if(low<=s.cost){++dominated;continue;}
        for(uint32_t k=s.r+1;k<allbit.size();k+=k&-k){
          if(astamp[k]!=epoch){astamp[k]=epoch;allbit[k]=s.cost;}else allbit[k]=min(allbit[k],s.cost);
          if(s.center){if(cstamp[k]!=epoch){cstamp[k]=epoch;centerbit[k]=s.cost;}else centerbit[k]=min(centerbit[k],s.cost);}
        }
        v[out++]=s;
      }
      v.resize(out);maxnode=max<uint64_t>(maxnode,v.size());
      for(const State&s:v)rollout(n+1,j,s);
      live+=v.size();accepted+=v.size();
    }
    front.swap(next);maxlive=max(maxlive,live);layers.push_back(live);
    if(n%32==31||n+1==N)cerr<<"{\"step\":"<<n+1<<",\"rounded_units\":"<<best<<",\"live\":"<<live<<",\"accepted\":"<<accepted<<"}\n";
  }
  ofstream out(argv[2]);out<<"{\"format_version\":1,\"arithmetic\":\"uint64 records and costs; uint128 square and ceiling division; no floating arithmetic\",\"B\":"<<B<<",\"n\":"<<B/2<<",\"cdf_denominator\":"<<D<<",\"cost_precision\":"<<precision<<",\"outward_cutoff\":"<<cutoff<<",\"cost_scale\":"<<C<<",\"rounded_minimum_units\":"<<best<<",\"rounding_budget_units\":"<<budget<<",\"beam_truncations\":0,\"generated\":"<<generated<<",\"dominated\":"<<dominated<<",\"bounded\":"<<bounded<<",\"deadline_pruned\":"<<deadline<<",\"accepted\":"<<accepted<<",\"maximum_live_layer\":"<<maxlive<<",\"maximum_node_frontier\":"<<maxnode<<",\"layer_states\":[";
  for(size_t i=0;i<layers.size();++i){if(i)out<<",";out<<layers[i];}out<<"]}\n";
}
