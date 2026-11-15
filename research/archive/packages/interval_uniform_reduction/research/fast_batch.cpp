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


struct PrefixCache {
 vector<P> q;
 vector<long double> at,aa,bb;
 int n;
 void build(int d){
  n=int(hs.size());
  for(auto const&h:hs)for(auto const&x:h.seq[(d+1)/2])q.push_back(x);
  sort(q.begin(),q.end());q.erase(unique(q.begin(),q.end()),q.end());
  size_t count=q.size()*(n+1);at.assign(count,0);aa.assign(count,0);bb.assign(count,0);
  for(size_t k=0;k<q.size();++k){
   size_t o=k*(n+1);long double z=q[k].val();
   for(int j=0;j<n;++j){
    auto const&h=hs[j];auto const&ss=h.seq[(d+1)/2];
    int b=int(lower_bound(ss.begin(),ss.end(),q[k])-ss.begin());
    long double tm=0;
    if(b==int(ss.size()))tm=h.t.back().val()+z-ss.back().val();
    else if(b>0){int den=1-d*h.slope[b-1];tm=h.t[b-1].val()+(z-ss[b-1].val())/den;}
    at[o+j+1]=at[o+j]+h.w*tm;
    b=int(upper_bound(ss.begin(),ss.end(),q[k])-ss.begin());
    long double a=0,c=0;
    if(b==int(ss.size())){a=1;c=h.t.back().val()-ss.back().val();}
    else if(b>0){int den=1-d*h.slope[b-1];a=1.L/den;c=h.t[b-1].val()-ss[b-1].val()/den;}
    aa[o+j+1]=aa[o+j]+h.w*a;bb[o+j+1]=bb[o+j]+h.w*c;
   }
  }
 }
 long double eval(P const&z,int l,int r)const{
  if(l==r)return 0;
  size_t k=lower_bound(q.begin(),q.end(),z)-q.begin();
  if(k<q.size()&&q[k]==z){size_t o=k*(n+1);return at[o+r]-at[o+l];}
  if(k==0)return 0;
  size_t o=(k-1)*(n+1);return (aa[o+r]-aa[o+l])*z.val()+bb[o+r]-bb[o+l];
 }
};
PrefixCache pc[2];

#include <map>
#include <tuple>
struct State {P t;long double c;};
map<tuple<int,int,int>, vector<State>> memo;
void walk(int l,int r,int anchor,P const&t,P const&x,long double cost){
 if(++nodes>limit)return;
 while(l>0&&pos(hs[l-1],t)==x){--l;cost+=hs[l].w*t.val();}
 while(r+1<int(hs.size())&&pos(hs[r+1],t)==x){++r;cost+=hs[r].w*t.val();}
 if(l==0&&r+1==int(hs.size())){++leaves;if(cost<best){best=cost;bestpath=route;}return;}
 auto key=make_tuple(l,r,anchor);auto&v=memo[key];
 for(auto&z:v)if(cmp(z.t,t)<=0&&z.c<=cost+1e-13L){++prunes;return;}
 v.erase(remove_if(v.begin(),v.end(),[&](State const&z){return cmp(t,z.t)<=0&&cost<=z.c+1e-13L;}),v.end());v.push_back({t,cost});
 long double lb=cost+pc[0].eval(t+x,0,l)+pc[1].eval(t-x,r+1,int(hs.size()));
 if(lb>=best-1e-12L){++prunes;return;}
 P a,b;if(l>0)a=hit(hs[l-1],t,x,-1);if(r+1<int(hs.size()))b=hit(hs[r+1],t,x,1);
 int first=l>0&&(r+1==int(hs.size())||a<b)?0:1;
 for(int k=0;k<2;++k){int d=k?1-first:first,j=d?r+1:l-1;if(j<0||j>=int(hs.size()))continue;P nt=d?b:a;P nx=x+mul(nt-t,2*d-1);route.push_back({nt,nx});walk(min(l,j),max(r,j),j,nt,nx,cost+hs[j].w*nt.val());route.pop_back();if(nodes>limit)return;}
}
P readp(){int n;cin>>n;vector<cpp_int>c(n);for(auto&x:c)cin>>x;return P(c);}void writep(P const&a){cout<<a.c.size();for(auto const&x:a.c)cout<<" "<<x;cout<<"\n";}
int main(){int n;cin>>n>>limit>>SCALE;SF=SCALE.convert_to<long double>();hs.resize(n);capt.assign(n,0);for(auto&h:hs){int k;cin>>k>>h.w;for(int i=0;i<k;++i){h.t.push_back(readp());h.x.push_back(readp());}for(int i=0;i<k-1;++i){P dt=h.t[i+1]-h.t[i],dx=h.x[i+1]-h.x[i];if(dx==P())h.slope.push_back(0);else if(dx==dt)h.slope.push_back(1);else if(dx==-dt)h.slope.push_back(-1);else{cerr<<"BAD SLOPE\n";return 2;}}for(int i=0;i<k;++i){h.seq[0].push_back(h.t[i]+h.x[i]);h.seq[1].push_back(h.t[i]-h.x[i]);}}

for(int i=0;i<n-1;++i){vector<P>ts=hs[i].t;for(auto&t:hs[i+1].t)ts.push_back(t);for(auto&t:ts)if(cmp(pos(hs[i],t),pos(hs[i+1],t))>0){cerr<<"PATHS CROSS\n";return 5;}}
pc[0].build(-1);pc[1].build(1);

vector<long double> values;vector<vector<pair<P,P>>> paths;
for(int i=n/2;i<n;++i){
 if(i>n/2&&hs[i].x[0]==hs[i-1].x[0])continue;
 best=1e50L;bestpath.clear();memo.clear();P x=hs[i].x[0];route={{P(),x}};walk(i,i,i,P(),x,0);
 if(!bestpath.empty()){values.push_back(best);paths.push_back(bestpath);}
 if(nodes>limit)break;
}
cout<<setprecision(20)<<paths.size()<<" "<<nodes<<" "<<(nodes<=limit)<<"\n";
for(size_t k=0;k<paths.size();++k){cout<<values[k]<<" "<<paths[k].size()<<"\n";for(auto const&v:paths[k]){writep(v.first);writep(v.second);}}
}
