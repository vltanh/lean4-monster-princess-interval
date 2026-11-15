// Exact ordered finite-quantile response with a certified unfinished frontier.
// g++ -O3 -std=c++17 continuous_response_search.cpp -lgmpxx -lgmp -o SEARCH
#include <gmpxx.h>
#include <algorithm>
#include <chrono>
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
struct Link {Q t,x;shared_ptr<Link> previous;};
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
  auto offer=[&](Q cost,shared_ptr<Link>route){if(cost<best){best=cost;bestRoute=route;improvements++;}};
  auto completeBoth=[&](shared_ptr<Link>route){
    bool left=false,right=false;for(auto p=route;p;p=p->previous){left|=p->x==-1;right|=p->x==1;}
    if(left&&right)return route;
    int d=left?1:right?-1:route->x<0?-1:1;
    Q end=route->t+1-d*route->x;
    auto first=make_shared<Link>(Link{end,Q(d),route});
    if(left||right)return first;
    return make_shared<Link>(Link{Q(end+2),Q(-d),first});
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
      for(int j=0;j<s.l;j++)cost+=ps[j].w*ps[j].hit(s.t,s.x,d);
      for(int j=s.r+1;j<n;j++)cost+=ps[j].w*ps[j].hit(s.t,s.x,d);
      Q end=s.t+1-d*s.x;auto first=make_shared<Link>(Link{end,Q(d),s.route});
      terminal++;offer(cost,completeBoth(first));return;
    }
    if(s.t>=absorption){
      Q left=prefix[s.l],right=1-prefix[s.r+1];
      Q a=s.cost+left*(s.t+1+s.x)+right*(s.t+3+s.x);
      Q b=s.cost+right*(s.t+1-s.x)+left*(s.t+3-s.x);
      int d=a<b?-1:1;Q end=s.t+1-d*s.x;
      auto first=make_shared<Link>(Link{end,Q(d),s.route});
      auto last=make_shared<Link>(Link{Q(end+2),Q(-d),first});
      terminal++;offer(min(a,b),last);return;
    }
    auto key=(static_cast<unsigned long long>(s.l)*(n+1)+s.r+1)*(n+1)+s.anchor;
    auto&front=memo[key];
    for(auto&entry:front)if(entry.first<=s.t&&entry.second<=s.cost){dominated++;return;}
    front.erase(remove_if(front.begin(),front.end(),[&](auto&entry){return s.t<=entry.first&&s.cost<=entry.second;}),front.end());
    front.emplace_back(s.t,s.cost);
    s.lb=s.cost;
    for(int j=0;j<s.l;j++)s.lb+=ps[j].w*ps[j].hit(s.t,s.x,-1);
    for(int j=s.r+1;j<n;j++)s.lb+=ps[j].w*ps[j].hit(s.t,s.x,1);
    if(s.lb>=best){bounded++;return;}
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
    for(int d:{-1,1}){
      int j=d<0?s.l-1:s.r+1;if(j<0||j>=n)continue;
      Q t=ps[j].hit(s.t,s.x,d),x=s.x+d*(t-s.t);
      if(t<=s.t)throw runtime_error("non-new capture");
      auto route=make_shared<Link>(Link{t,x,s.route});
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
      <<",\"seconds\":"<<chrono::duration<double>(chrono::steady_clock::now()-begin).count()<<",\"route\":[";
  for(size_t i=0;i<route.size();i++){if(i)cout<<",";cout<<"[\""<<route[i].first<<"\",\""<<route[i].second<<"\"]";}
  cout<<"]}"<<endl;
}catch(exception&e){cerr<<e.what()<<endl;return 1;}}
