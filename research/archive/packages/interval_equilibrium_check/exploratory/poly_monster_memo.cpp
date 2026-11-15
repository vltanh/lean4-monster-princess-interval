#include <boost/multiprecision/cpp_int.hpp>
#include <iostream>
#include <vector>
#include <algorithm>
#include <iomanip>
#include <cmath>
#include <unordered_map>
#include <cstdint>
using namespace std;using boost::multiprecision::cpp_int;
cpp_int SCALE;long double SF;
struct P{vector<cpp_int> c;P():c(1){} P(vector<cpp_int> v):c(move(v)){trim();} void trim(){while(c.size()>1&&c.back()==0)c.pop_back();} long double val() const{return c[0].convert_to<long double>()/SF;}};
int cmp(P const&a,P const&b){for(size_t i=0;i<max(a.c.size(),b.c.size());++i){cpp_int x=i<a.c.size()?a.c[i]:cpp_int(0),y=i<b.c.size()?b.c[i]:cpp_int(0);if(x<y)return -1;if(x>y)return 1;}return 0;}
bool operator<(P const&a,P const&b){return cmp(a,b)<0;}bool operator==(P const&a,P const&b){return cmp(a,b)==0;}
P operator+(P const&a,P const&b){vector<cpp_int> c(max(a.c.size(),b.c.size()));for(size_t i=0;i<c.size();++i)c[i]=(i<a.c.size()?a.c[i]:cpp_int(0))+(i<b.c.size()?b.c[i]:cpp_int(0));return P(c);}
P operator-(P const&a){vector<cpp_int>c=a.c;for(auto&x:c)x=-x;return P(c);}P operator-(P const&a,P const&b){return a+(-b);}
P mul(P const&a,int n){vector<cpp_int>c=a.c;for(auto&x:c)x*=n;return P(c);}P divp(P const&a,int n){vector<cpp_int>c=a.c;for(auto&x:c){if(x%n!=0){cerr<<"SCALE EXHAUSTED\n";exit(3);}x/=n;}return P(c);}
struct Path{vector<P>t,x,seq[2];vector<int>slope;long double w;};vector<Path> hs;vector<char>capt;vector<pair<P,P>>route,bestpath;long double best=1e50L;long long nodes=0,leaves=0,prunes=0,limit;
P pos(Path const&h,P const&t){auto it=upper_bound(h.t.begin(),h.t.end(),t);int k=int(it-h.t.begin())-1;if(k+1>=int(h.t.size()))return h.x.back();return h.x[k]+mul(t-h.t[k],h.slope[k]);}
P hit(Path const&h,P const&t,P const&x,int d){P q=t-mul(x,d);auto const&seq=h.seq[(d+1)/2];int k=lower_bound(seq.begin(),seq.end(),q)-seq.begin();P a;if(k==int(seq.size()))a=h.t.back()+q-seq.back();else if(k==0)a=t;else a=h.t[k-1]+divp(q-seq[k-1],1-d*h.slope[k-1]);if(a<t){cerr<<"BACKWARD HIT\n";exit(4);}return a;}

struct Key {uint64_t lo,hi;int a;bool operator==(Key const&b) const{return lo==b.lo&&hi==b.hi&&a==b.a;}};
struct Hash {size_t operator()(Key const&k) const{return k.lo ^ (k.hi*0x9e3779b97f4a7c15ULL) ^ (uint64_t(k.a)*0x517cc1b727220a95ULL);}};
struct State{P t;long double c;};
unordered_map<Key,vector<State>,Hash> memo;
uint64_t masklo=0,maskhi=0;
void walk(P const&t,P const&x,long double cost){int anchor=-1;if(++nodes>limit)return;vector<int>added;long double lb=cost;P next[2];bool has[2]={false,false};int left=0;
for(int j=0;j<int(hs.size());++j){if(capt[j])continue;P y=pos(hs[j],t);int rel=cmp(y,x);if(!rel){capt[j]=1;added.push_back(j);anchor=j;if(j<64)masklo|=1ULL<<j;else if(j<128)maskhi|=1ULL<<(j-64);cost+=hs[j].w*t.val();lb+=hs[j].w*t.val();}else{++left;int d=rel>0?1:-1,k=(d+1)/2;P a=hit(hs[j],t,x,d);lb+=hs[j].w*a.val();if(!has[k]||a<next[k]){next[k]=a;has[k]=true;}}}
bool dom=false;
if(left&&anchor>=0&&hs.size()<=128){auto&v=memo[{masklo,maskhi,anchor}];for(auto&z:v)if(cmp(z.t,t)<=0&&z.c<=cost+1e-13L){dom=true;break;}if(!dom){v.erase(remove_if(v.begin(),v.end(),[&](State const&z){return cmp(t,z.t)<=0&&cost<=z.c+1e-13L;}),v.end());v.push_back({t,cost});}}
if(dom){++prunes;}
else if(left==0){++leaves;if(cost<best){best=cost;bestpath=route;}}
else if(lb<best-1e-12L){int first=has[0]&&(!has[1]||next[0]<next[1])?0:1;for(int kk=0;kk<2;++kk){int k=kk?1-first:first;if(!has[k])continue;P y=x+mul(next[k]-t,2*k-1);route.push_back({next[k],y});walk(next[k],y,cost);route.pop_back();if(nodes>limit)break;}}
else ++prunes;for(int j:added){capt[j]=0;if(j<64)masklo&=~(1ULL<<j);else if(j<128)maskhi&=~(1ULL<<(j-64));}}
P readp(){int n;cin>>n;vector<cpp_int>c(n);for(auto&x:c)cin>>x;return P(c);}void writep(P const&a){cout<<a.c.size();for(auto const&x:a.c)cout<<" "<<x;cout<<"\n";}
int main(){int n;cin>>n>>limit>>SCALE;SF=SCALE.convert_to<long double>();hs.resize(n);capt.assign(n,0);for(auto&h:hs){int k;cin>>k>>h.w;for(int i=0;i<k;++i){h.t.push_back(readp());h.x.push_back(readp());}for(int i=0;i<k-1;++i){P dt=h.t[i+1]-h.t[i],dx=h.x[i+1]-h.x[i];if(dx==P())h.slope.push_back(0);else if(dx==dt)h.slope.push_back(1);else if(dx==-dt)h.slope.push_back(-1);else{cerr<<"BAD SLOPE\n";return 2;}}for(int i=0;i<k;++i){h.seq[0].push_back(h.t[i]+h.x[i]);h.seq[1].push_back(h.t[i]-h.x[i]);}}
vector<P>starts;for(auto const&h:hs)starts.push_back(h.x[0]);sort(starts.begin(),starts.end());starts.erase(unique(starts.begin(),starts.end()),starts.end());for(P const&x:starts){route={{P(),x}};walk(P(),x,0);if(nodes>limit)break;}
cout<<setprecision(20)<<best<<" "<<nodes<<" "<<leaves<<" "<<prunes<<" "<<(nodes<=limit)<<" "<<bestpath.size()<<"\n";for(auto const&v:bestpath){writep(v.first);writep(v.second);} }
