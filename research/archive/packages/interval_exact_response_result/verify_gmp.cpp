// Exact finite-hider response search. All payoff and geometric arithmetic is rational.
// Compile: g++ -O3 -std=c++17 monster_exact.cpp -lgmpxx -lgmp -o monster_exact
#include <gmpxx.h>
#include <boost/multiprecision/cpp_int.hpp>
#include <algorithm>
#include <cstdint>
#include <fstream>
#include <iostream>
#include <stdexcept>
#include <unordered_map>
#include <vector>
#include <chrono>
using namespace std;
using Q=mpq_class;using Mask=boost::multiprecision::uint512_t;
struct Path{Q w;vector<Q> t,x,up,dn;
 Q pos(Q const&s)const{auto it=upper_bound(t.begin(),t.end(),s);int i=int(it-t.begin())-1;if(i<0)throw runtime_error("negative time");if(i+1==(int)t.size())return x.back();return x[i]+(s-t[i])*(x[i+1]-x[i])/(t[i+1]-t[i]);}
 Q hit(Q const&s,Q const&y,int dir)const{
  Q z=pos(s);if(z==y)return s;if((z-y)*dir<0)throw runtime_error("target behind ray");
  auto&a=(dir==1?dn:up);Q q=s-dir*y;auto it=lower_bound(a.begin(),a.end(),q);int k=int(it-a.begin());Q h;
  if(k==(int)a.size())h=t.back()+(q-a.back());
  else if(k==0)h=t[0];
  else if(a[k]==a[k-1])h=t[k-1];
  else h=t[k-1]+(t[k]-t[k-1])*(q-a[k-1])/(a[k]-a[k-1]);
  if(h<s)h=s;return h;
 }};
struct Key{Mask mask;unsigned anchor;bool operator==(Key const&o)const{return mask==o.mask&&anchor==o.anchor;}};
struct Hash{size_t operator()(Key const&k)const{uint64_t h=k.anchor+1;for(int i=0;i<8;i++)h=(h*0x9e3779b97f4a7c15ULL)^uint64_t(k.mask>>(64*i));return h;}};
vector<Path> ps;vector<pair<Q,Q>> route,bestpath;vector<Q> captures,bestcaps;
unordered_map<Key,vector<pair<Q,Q>>,Hash> memo;Mask full;
uint64_t nodes=0,leaves=0,prunes=0,dominated=0;bool havebest=false;Q best;
auto begun=chrono::steady_clock::now();
void walk(Mask mask,Q const&t,Q const&x,Q cost,unsigned anchor){
 nodes++;
 for(unsigned j=0;j<ps.size();j++)if(!bool((mask>>j)&1)&&ps[j].pos(t)==x){mask|=Mask(1)<<j;cost+=ps[j].w*t;captures[j]=t;anchor=j;}
 if(mask==full){leaves++;if(!havebest||cost<best){havebest=true;best=cost;bestpath=route;bestcaps=captures;}return;}
 Q lb=cost,hits[2];int js[2]={-1,-1};
 for(unsigned j=0;j<ps.size();j++)if(!bool((mask>>j)&1)){
  int dir=ps[j].pos(t)>x?1:-1;Q h=ps[j].hit(t,x,dir);lb+=ps[j].w*h;int k=dir==1?1:0;
  if(js[k]<0||h<hits[k]){hits[k]=h;js[k]=j;}
 }
 if(havebest&&lb>=best){prunes++;return;}
 auto &v=memo[Key{mask,anchor}];
 for(auto const&z:v)if(z.first<=t&&z.second<=cost){dominated++;return;}
 v.erase(remove_if(v.begin(),v.end(),[&](auto const&z){return t<=z.first&&cost<=z.second;}),v.end());v.emplace_back(t,cost);
 int first=js[0]<0?1:js[1]<0?0:hits[0]<hits[1]?0:1;
 for(int a=0;a<2;a++){int k=a==0?first:1-first;if(js[k]<0)continue;Q s=hits[k];int dir=k==0?-1:1;Q y=x+dir*(s-t);
  if(s<=t||y< -1||y>1)throw runtime_error("invalid capture step");
  auto old=captures;route.emplace_back(s,y);walk(mask,s,y,cost,js[k]);route.pop_back();captures=old;
 }
}
int main(int argc,char**argv){try{
 if(argc!=2)throw runtime_error("usage: monster_exact hiders.txt");ifstream in(argv[1]);int n;in>>n;if(n<1||n>511)throw runtime_error("invalid number of hiders");ps.resize(n);captures.resize(n);full=(Mask(1)<<n)-1;Q sum=0;
 for(auto&p:ps){string w;int k;in>>w>>k;p.w=Q(w);p.w.canonicalize();if(p.w<=0)throw runtime_error("nonpositive weight");sum+=p.w;p.t.resize(k);p.x.resize(k);
  for(int i=0;i<k;i++){string st,sx;in>>st>>sx;p.t[i]=Q(st);p.x[i]=Q(sx);p.t[i].canonicalize();p.x[i].canonicalize();if(p.x[i]< -1||p.x[i]>1||(i==0&&p.t[i]!=0)||(i>0&&(p.t[i]<=p.t[i-1]||abs(p.x[i]-p.x[i-1])>p.t[i]-p.t[i-1])))throw runtime_error("inadmissible hider");p.up.push_back(p.t[i]+p.x[i]);p.dn.push_back(p.t[i]-p.x[i]);}
 }
 if(sum!=1)throw runtime_error("weights do not sum to one");
 vector<Q> starts;for(auto&p:ps)starts.push_back(p.x[0]);sort(starts.begin(),starts.end());starts.erase(unique(starts.begin(),starts.end()),starts.end());
 for(auto const&x:starts){route={{Q(0),x}};fill(captures.begin(),captures.end(),Q(-1));walk(Mask(0),Q(0),x,Q(0),0);}
 cout<<"{\"value\":\""<<best<<"\",\"nodes\":"<<nodes<<",\"leaves\":"<<leaves<<",\"lower_bound_prunes\":"<<prunes<<",\"dominance_prunes\":"<<dominated<<",\"states\":"<<memo.size()<<",\"initial_positions\":"<<starts.size()<<",\"seconds\":"<<chrono::duration<double>(chrono::steady_clock::now()-begun).count()<<",\"path\":[";
 for(unsigned i=0;i<bestpath.size();i++){if(i)cout<<",";cout<<"[\""<<bestpath[i].first<<"\",\""<<bestpath[i].second<<"\"]";}cout<<"],\"captures\":[";
 for(unsigned i=0;i<bestcaps.size();i++){if(i)cout<<",";cout<<"\""<<bestcaps[i]<<"\"";}cout<<"]}"<<endl;
 }catch(exception const&e){cerr<<e.what()<<endl;return 1;}}
