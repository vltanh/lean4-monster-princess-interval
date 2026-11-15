// Exact ordered finite-quantile response with aggregate inverse-hit sums.
// g++ -O3 -std=c++17 continuous_response_fast_search.cpp -lgmpxx -lgmp -o SEARCH
// Intervals are RIGHT-CLOSED: flat pursuit characteristics have jumps, and
// capture at equality must use the earliest contact, not its right limit.
#include <gmpxx.h>
#include <algorithm>
#include <chrono>
#include <cstdlib>
#include <fstream>
#include <iomanip>
#include <iostream>
#include <memory>
#include <queue>
#include <sstream>
#include <stdexcept>
#include <string>
#include <unordered_map>
#include <vector>
using namespace std;
using Q=mpq_class;

struct Path {
  Q w; vector<Q> t,x,v,up,dn;
  Q at(const Q&s) const {
    int k=int(upper_bound(t.begin(),t.end(),s)-t.begin())-1;
    if(k<0)throw runtime_error("negative time");
    return k+1==int(t.size())?x[k]:Q(x[k]+v[k]*(s-t[k]));
  }
  Q hit(const Q&s,const Q&y,int d) const {
    const auto&z=d==1?dn:up;Q q=s-d*y;
    int k=int(lower_bound(z.begin(),z.end(),q)-z.begin());Q ans;
    if(k==int(z.size()))ans=t.back()+q-z.back();
    else if(k==0)ans=s;
    else {Q denominator=1-d*v[k-1];if(denominator<=0)throw runtime_error("flat inverse");
      ans=t[k-1]+(q-z[k-1])/denominator;}
    if(ans<s||ans>s+1-d*y)throw runtime_error("invalid earliest hit");
    return ans;
  }
};
struct Affine {Q slope,intercept;};
struct InverseSum {
  vector<Q> ends;
  vector<Affine> pieces;
  Q at(const Q&q)const{
    size_t i=lower_bound(ends.begin(),ends.end(),q)-ends.begin();
    return pieces[i].slope*q+pieces[i].intercept;
  }
  static InverseSum leaf(const Path&p,int direction){
    const auto&z=direction==1?p.dn:p.up;
    InverseSum f;f.ends.push_back(z[0]);f.pieces.push_back({0,0});
    for(size_t k=1;k<z.size();k++)if(z[k]>z[k-1]){
      Q slope=p.w/(1-direction*p.v[k-1]);
      f.ends.push_back(z[k]);
      f.pieces.push_back({slope,Q(p.w*p.t[k-1]-slope*z[k-1])});
    }
    f.pieces.push_back({p.w,Q(p.w*(p.t.back()-z.back()))});
    if(f.pieces.size()!=f.ends.size()+1)throw runtime_error("inverse leaf size");
    return f;
  }
  static InverseSum sum(const InverseSum&a,const InverseSum&b){
    if(a.pieces.empty())return b;if(b.pieces.empty())return a;
    InverseSum f;size_t i=0,j=0;
    while(i<a.ends.size()||j<b.ends.size()){
      Q end=j==b.ends.size()||(i<a.ends.size()&&a.ends[i]<b.ends[j])?a.ends[i]:b.ends[j];
      Affine p{Q(a.pieces[i].slope+b.pieces[j].slope),Q(a.pieces[i].intercept+b.pieces[j].intercept)};
      // Coalescing equal adjacent affine pieces preserves both point values
      // and right limits because this breakpoint then has no jump.
      if(!f.pieces.empty()&&f.pieces.back().slope==p.slope&&f.pieces.back().intercept==p.intercept)
        f.ends.back()=end;
      else {f.ends.push_back(end);f.pieces.push_back(move(p));}
      if(i<a.ends.size()&&a.ends[i]==end)i++;
      if(j<b.ends.size()&&b.ends[j]==end)j++;
    }
    f.pieces.push_back({Q(a.pieces[i].slope+b.pieces[j].slope),Q(a.pieces[i].intercept+b.pieces[j].intercept)});
    return f;
  }
};
struct InverseTree {
  int count,base;vector<InverseSum> tree;
  InverseTree(const vector<Path>&ps,int direction):count(ps.size()),base(1){
    while(base<count)base*=2;tree.resize(2*base);
    for(int i=0;i<count;i++)tree[base+i]=InverseSum::leaf(ps[i],direction);
    for(int i=base-1;i>0;i--)tree[i]=InverseSum::sum(tree[2*i],tree[2*i+1]);
  }
  Q range(int l,int r,const Q&q)const{
    Q result=0;for(l+=base,r+=base;l<r;l/=2,r/=2){
      if(l%2)result+=tree[l++].at(q);
      if(r%2)result+=tree[--r].at(q);
    }return result;
  }
  size_t pieces()const{size_t n=0;for(const auto&f:tree)n+=f.pieces.size();return n;}
};
struct Link {Q t,x;shared_ptr<Link> previous;};
shared_ptr<Link> linkAt(Q t,Q x,shared_ptr<Link>previous){
  if(previous&&previous->previous){
    const auto&a=previous->previous;
    if((previous->x-a->x)*(t-previous->t)==(x-previous->x)*(previous->t-a->t))previous=a;
  }
  return make_shared<Link>(Link{move(t),move(x),move(previous)});
}
struct State {int l,r,anchor;Q t,x,cost,lb;shared_ptr<Link> route;};
struct Later {bool operator()(const State&a,const State&b)const{return a.lb>b.lb;}};

int main(int argc,char**argv){try{
  if(argc<2)throw runtime_error("usage: SEARCH hiders.txt [node_limit] [incumbent_route.txt] [--start rational]");
  unsigned long long limit=1000000ULL;string incumbent;bool fixedStart=false;Q start=0;int argument=2;
  if(argument<argc&&string(argv[argument])!="--start")limit=stoull(argv[argument++]);
  if(argument<argc&&string(argv[argument])!="--start")incumbent=argv[argument++];
  if(argument<argc){
    if(string(argv[argument++])!="--start"||argument+1!=argc)throw runtime_error("invalid start argument");
    start=Q(argv[argument]);start.canonicalize();fixedStart=true;
    if(abs(start)>1)throw runtime_error("start outside arena");
  }
  ifstream input(argv[1]);string header;getline(input,header);istringstream line(header);
  int n;string horizon;line>>n;Q absorption=2;if(line>>horizon){absorption=Q(horizon);absorption.canonicalize();}
  if(!input||n<1||absorption<0)throw runtime_error("missing paths or invalid absorption time");
  vector<Path> ps(n);vector<Q> prefix(n+1,0);Q total=0;
  for(int j=0;j<n;j++){
    auto&p=ps[j];string weight;int count;input>>weight>>count;
    p.w=Q(weight);p.w.canonicalize();if(p.w<=0||count<1)throw runtime_error("weight or length");
    for(int k=0;k<count;k++){
      string st,sx;input>>st>>sx;Q t(st),x(sx);t.canonicalize();x.canonicalize();
      if(x< -1||x>1||(k==0&&t!=0)||(k&&t<=p.t.back()))throw runtime_error("vertex");
      if(k){Q v=(x-p.x.back())/(t-p.t.back());if(abs(v)>1)throw runtime_error("speed");p.v.push_back(v);}
      p.t.push_back(t);p.x.push_back(x);p.up.push_back(t+x);p.dn.push_back(t-x);
    }
    if(p.t.back()>absorption||abs(p.x.back())!=1)throw runtime_error("declared endpoint absorption violated");
    total+=p.w;prefix[j+1]=total;
  }
  if(total!=1)throw runtime_error("normalization");
  for(int j=1;j<n;j++)for(const auto*ts:{&ps[j-1].t,&ps[j].t})for(const Q&t:*ts)
    if(ps[j-1].at(t)>ps[j].at(t))throw runtime_error("crossing quantiles");
  for(int j=0;j<n;j++){
    auto&p=ps[j];auto&q=ps[n-1-j];if(p.w!=q.w)throw runtime_error("symmetry weights");
    for(const auto*ts:{&p.t,&q.t})for(const Q&t:*ts)if(p.at(t)!=-q.at(t))throw runtime_error("symmetry paths");
  }
  auto begin=chrono::steady_clock::now();
  InverseTree leftHits(ps,-1),rightHits(ps,1);
  unsigned long long inverseChecks=0;
  // Independent scalar pursuit checks at every exact leaf breakpoint and
  // between them. This explicitly exercises equality at flat characteristics.
  for(int j=0;j<n;j++)for(int d:{-1,1}){
    const auto&z=d==1?ps[j].dn:ps[j].up;
    const auto&tree=d==1?rightHits:leftHits;
    for(size_t k=0;k<z.size();k++)for(int side:{0,1}){
      Q q=z[k];if(side&&k+1<z.size())q=(q+z[k+1])/2;
      if(q<z[0])continue;
      size_t h=0;while(h<z.size()&&z[h]<q)h++;
      Q expected=0;
      if(h==z.size())expected=ps[j].t.back()+q-z.back();
      else if(h)expected=ps[j].t[h-1]+(q-z[h-1])/(1-d*ps[j].v[h-1]);
      expected*=ps[j].w;
      if(tree.range(j,j+1,q)!=expected)throw runtime_error("inverse point/contact check");
      inverseChecks++;
    }
  }
  cerr<<"inverse tables "<<leftHits.pieces()+rightHits.pieces()<<" pieces"<<endl;
  auto routeCost=[&](const vector<pair<Q,Q>>&candidate){
    if(candidate.empty()||candidate[0].first!=0||abs(candidate[0].second)>1)throw runtime_error("incumbent initial point");
    if(fixedStart&&candidate[0].second!=start)throw runtime_error("incumbent has wrong fixed start");
    int count=candidate.size();
    for(int k=1;k<count;k++)if(candidate[k].first<=candidate[k-1].first||
       abs(candidate[k].second)>1||abs(candidate[k].second-candidate[k-1].second)!=candidate[k].first-candidate[k-1].first)
      throw runtime_error("incumbent unit speed");
    Q cost=0;
    for(auto&p:ps){
      bool caught=false;
      for(int k=0;k+1<count;k++){
        auto[t,x]=candidate[k];auto[end,y]=candidate[k+1];int d=y>x?1:-1;
        if((p.at(t)-x)*d<0)continue;
        Q hit=p.hit(t,x,d);if(hit<=end){cost+=p.w*hit;caught=true;break;}
      }
      if(!caught)throw runtime_error("incumbent incomplete");
    }
    return cost;
  };
  vector<pair<Q,Q>> initial=fixedStart?
    vector<pair<Q,Q>>{{0,start},{Q(1+start),-1},{Q(3+start),1}}:
    vector<pair<Q,Q>>{{0,-1},{2,1}};
  if(initial.size()==3&&initial[0]==initial[1])initial.erase(initial.begin());
  Q best=routeCost(initial);shared_ptr<Link> bestRoute=nullptr;
  for(auto[t,x]:initial)bestRoute=make_shared<Link>(Link{t,x,bestRoute});
  if(!incumbent.empty()){
    ifstream saved(incumbent);int count;saved>>count;vector<pair<Q,Q>> candidate;
    for(int k=0;k<count;k++){string t,x;saved>>t>>x;Q a(t),b(x);a.canonicalize();b.canonicalize();candidate.emplace_back(a,b);}
    Q cost=routeCost(candidate);
    if(cost<best){best=cost;bestRoute=nullptr;for(auto[t,x]:candidate)bestRoute=make_shared<Link>(Link{t,x,bestRoute});}
  }
  priority_queue<State,vector<State>,Later> queue;
  unordered_map<unsigned long long,vector<pair<Q,Q>>> memo;
  unsigned long long processed=0,created=0,bounded=0,dominated=0,terminal=0,improvements=0;
  unsigned long long pairChecks=0,pairPruned=0;
  int pairBlocks=8;
  if(const char*setting=getenv("CONTINUOUS_RESPONSE_PAIR_BLOCKS"))pairBlocks=stoi(setting);
  if(pairBlocks<0)throw runtime_error("negative pair-block count");
  auto pairedLower=[&](const State&s){
    int right=n-s.r-1,blocks=min(pairBlocks,min(s.l,right));
    if(!blocks)return s.cost;
    Q value=s.cost;pairChecks++;
    for(int k=0;k<blocks;k++){
      int l0=k*s.l/blocks,l1=(k+1)*s.l/blocks;
      int r0=s.r+1+(blocks-1-k)*right/blocks,r1=s.r+1+(blocks-k)*right/blocks;
      int i=l1-1,j=r0;Q a=prefix[l1]-prefix[l0],b=prefix[r1]-prefix[r0];
      // Every left block is met through its largest ordered rank; every
      // right block through its smallest. All members' capture times are
      // at least that representative's. Each pair may choose its own order,
      // so summing these exact two-target optima is a relaxation.
      Q tl=ps[i].hit(s.t,s.x,-1),tr=ps[j].hit(s.t,s.x,1);
      Q yl=s.x-(tl-s.t),yr=s.x+(tr-s.t);
      Q lr=a*tl+b*ps[j].hit(tl,yl,1);
      Q rl=b*tr+a*ps[i].hit(tr,yr,-1);
      value+=min(lr,rl);
    }
    return value;
  };
  auto offer=[&](Q cost,shared_ptr<Link>route){if(cost<best){best=cost;bestRoute=route;improvements++;}};
  auto completeBoth=[&](shared_ptr<Link>route){
    bool left=false,right=false;for(auto p=route;p;p=p->previous){left|=p->x==-1;right|=p->x==1;}
    if(left&&right)return route;
    int d=left?1:right?-1:route->x<0?-1:1;
    Q end=route->t+1-d*route->x;
      auto first=linkAt(end,Q(d),route);
    if(left||right)return first;
    return linkAt(Q(end+2),Q(-d),first);
  };
  auto prepare=[&](State s){
    created++;
    while(s.l>0&&ps[s.l-1].at(s.t)==s.x){s.l--;s.cost+=ps[s.l].w*s.t;}
    while(s.r+1<n&&ps[s.r+1].at(s.t)==s.x){s.r++;s.cost+=ps[s.r].w*s.t;}
    if(s.l==0&&s.r==n-1){
      // Complete both arena endpoints for the later continuum transfer;
      // the extra motion changes no finite-law capture time.
      terminal++;offer(s.cost,completeBoth(s.route));return;
    }
    if(s.l==0||s.r==n-1){
      // All surviving targets lie on one side. Direct pursuit catches each
      // no later than any continuation, even before an endpoint is reached.
      int d=s.l==0?1:-1;Q cost=s.cost;
      const auto&hits=d<0?leftHits:rightHits;Q q=s.t-d*s.x;
      cost+=hits.range(0,s.l,q)+hits.range(s.r+1,n,q);
      Q end=s.t+1-d*s.x;auto first=linkAt(end,Q(d),s.route);
      terminal++;offer(cost,completeBoth(first));return;
    }
    if(s.t>=absorption){
      Q left=prefix[s.l],right=1-prefix[s.r+1];
      Q a=s.cost+left*(s.t+1+s.x)+right*(s.t+3+s.x);
      Q b=s.cost+right*(s.t+1-s.x)+left*(s.t+3-s.x);
      int d=a<b?-1:1;Q end=s.t+1-d*s.x;
      auto first=linkAt(end,Q(d),s.route);
      auto last=linkAt(Q(end+2),Q(-d),first);
      terminal++;offer(min(a,b),last);return;
    }
    auto key=(static_cast<unsigned long long>(s.l)*(n+1)+s.r+1)*(n+1)+s.anchor;
    auto&front=memo[key];
    for(auto&entry:front)if(entry.first<=s.t&&entry.second<=s.cost){dominated++;return;}
    front.erase(remove_if(front.begin(),front.end(),[&](auto&entry){return s.t<=entry.first&&s.cost<=entry.second;}),front.end());
    front.emplace_back(s.t,s.cost);
    s.lb=s.cost;
    s.lb+=leftHits.range(0,s.l,Q(s.t+s.x))+rightHits.range(s.r+1,n,Q(s.t-s.x));
    if(s.lb>=best){bounded++;return;}
    Q pairBound=pairedLower(s);
    if(pairBound>=best){bounded++;pairPruned++;return;}
    s.lb=max(s.lb,pairBound);
    queue.push(move(s));
  };
  if(fixedStart){
    int j=0;while(j<n&&ps[j].x[0]<start)j++;
    auto route=make_shared<Link>(Link{Q(0),start,nullptr});
    prepare(State{j,j-1,n,Q(0),start,Q(0),Q(0),route});
  }else for(int j=0;j<n;j++)if(ps[j].x[0]>=0&&(!j||ps[j].x[0]!=ps[j-1].x[0])){
    auto route=make_shared<Link>(Link{Q(0),ps[j].x[0],nullptr});
    prepare(State{j,j,j,Q(0),ps[j].x[0],Q(0),Q(0),route});
  }
  while(!queue.empty()&&processed<limit){
    State s=queue.top();queue.pop();processed++;
    if(s.lb>=best){bounded++;continue;}
    auto key=(static_cast<unsigned long long>(s.l)*(n+1)+s.r+1)*(n+1)+s.anchor;
    bool stale=false;for(const auto&entry:memo[key])
      if(entry.first<=s.t&&entry.second<=s.cost&&(entry.first<s.t||entry.second<s.cost)){stale=true;break;}
    if(stale){dominated++;continue;}
    if(processed%100000==0)cerr<<"processed "<<processed<<" pending "<<queue.size()<<" lower "<<s.lb.get_d()<<" best "<<best.get_d()<<endl;
    for(int d:{-1,1}){
      int j=d<0?s.l-1:s.r+1;if(j<0||j>=n)continue;
      Q t=ps[j].hit(s.t,s.x,d),x=s.x+d*(t-s.t);
      if(t<=s.t)throw runtime_error("non-new capture");
      auto route=linkAt(t,x,s.route);
      prepare(State{min(s.l,j),max(s.r,j),j,t,x,Q(s.cost+ps[j].w*t),Q(0),route});
    }
  }
  Q lower=queue.empty()?best:min(best,queue.top().lb);bool complete=queue.empty()||lower==best;
  vector<pair<Q,Q>> raw;for(auto p=bestRoute;p;p=p->previous)raw.emplace_back(p->t,p->x);
  reverse(raw.begin(),raw.end());vector<pair<Q,Q>> route;
  for(auto p:raw){
    if(!route.empty()&&p.first==route.back().first){if(p.second!=route.back().second)throw runtime_error("route duplicate");continue;}
    route.push_back(p);
    while(route.size()>=3){auto a=route[route.size()-3],b=route[route.size()-2],c=route.back();
      if((b.second-a.second)*(c.first-b.first)==(c.second-b.second)*(b.first-a.first))route.erase(route.end()-2);else break;}
  }
  cout<<setprecision(17)<<"{\"scope\":\"Exact specified finite quantile law; transfer to the CDF requires the documented discrepancy theorem\",\"complete\":"<<(complete?"true":"false")
      <<",\"fixed_start\":"<<(fixedStart?string("\"")+start.get_str()+"\"":"null")
      <<",\"absorption_time\":\""<<absorption<<"\",\"paths\":"<<n<<",\"value\":\""<<best<<"\",\"lower_bound\":\""<<lower<<"\",\"decimal\":"<<best.get_d()
      <<",\"processed\":"<<processed<<",\"created\":"<<created<<",\"terminal\":"<<terminal<<",\"bounded\":"<<bounded
      <<",\"dominated\":"<<dominated<<",\"improvements\":"<<improvements<<",\"pending\":"<<queue.size()
      <<",\"inverse_pieces\":"<<leftHits.pieces()+rightHits.pieces()<<",\"inverse_point_checks\":"<<inverseChecks
      <<",\"pair_blocks\":"<<pairBlocks<<",\"pair_bound_checks\":"<<pairChecks<<",\"pair_pruned\":"<<pairPruned
      <<",\"seconds\":"<<chrono::duration<double>(chrono::steady_clock::now()-begin).count()<<",\"route\":[";
  for(size_t i=0;i<route.size();i++){if(i)cout<<",";cout<<"[\""<<route[i].first<<"\",\""<<route[i].second<<"\"]";}
  cout<<"]}"<<endl;
}catch(exception&e){cerr<<e.what()<<endl;return 1;}}
