#include <boost/multiprecision/cpp_int.hpp>
#include <iostream>
#include <vector>
#include <algorithm>
#include <iomanip>
#include <cmath>
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
P readp(){int n;cin>>n;vector<cpp_int>c(n);for(auto&x:c)cin>>x;return P(c);}void writep(P const&a){cout<<a.c.size();for(auto const&x:a.c)cout<<" "<<x;cout<<"\n";}

Path readpath(){Path h;int k;cin>>k;for(int i=0;i<k;++i){h.t.push_back(readp());h.x.push_back(readp());}for(int i=0;i<k-1;++i){P dt=h.t[i+1]-h.t[i],dx=h.x[i+1]-h.x[i];if(dx==P())h.slope.push_back(0);else if(dx==dt)h.slope.push_back(1);else if(dx==-dt)h.slope.push_back(-1);else{cerr<<"BAD SLOPE\n";exit(2);}}return h;}
P meeting(Path const&a,Path const&b,int reflect){
 vector<P>ts=a.t;for(auto&t:b.t)ts.push_back(t);sort(ts.begin(),ts.end());ts.erase(unique(ts.begin(),ts.end()),ts.end());
 P prev,dprev;
 for(size_t k=0;k<ts.size();++k){P t=ts[k],d=pos(a,t)-mul(pos(b,t),reflect);int sign=cmp(d,P());if(!sign)return t;if(k&&sign!=cmp(dprev,P())){P dt=t-prev,dv=d-dprev;for(int v:{-2,-1,1,2})if(dv==mul(dt,v))return prev-divp(dprev,v);cerr<<"BAD CROSSING\n";exit(4);}prev=t;dprev=d;}
 cerr<<"NO MEETING\n";exit(5);
}
int main(){int n,m;cin>>n>>m>>SCALE;SF=SCALE.convert_to<long double>();vector<Path>ps(n),ms(m);for(auto&p:ps)p=readpath();for(auto&p:ms)p=readpath();cout<<setprecision(18);for(auto&p:ps){for(auto&m:ms)cout<<(meeting(m,p,1).val()+meeting(m,p,-1).val())/2<<" ";cout<<"\n";} }
