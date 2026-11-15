// Exact normalized-bank pricing with proved center phase compression.
// Policies: 0 original moves, 1 triangles/heavier-first, 2 also peak balance,
// 3 jump the deterministic balanced return (minimum only, no witnesses),
// 4 also use the exact incoming-front terminal guard on front-two fields.
// See research/12-global-closure/DISCRETE_CENTER_BALANCE_PRICING.md.
// The physical-bank normalization theorem is a separate mathematical dependency.
// No beam search, floating comparison, or state-count cutoff is used.
// Witnesses use packed current-layer move prefixes: no unbounded ancestor tree.
#include <algorithm>
#include <cstdint>
#include <fstream>
#include <iostream>
#include <limits>
#include <map>
#include <queue>
#include <stdexcept>
#include <string>
#include <tuple>
#include <vector>

using U = std::uint64_t;
static constexpr U INF = std::numeric_limits<U>::max();
struct State { U left, right, cost; std::int64_t trace; bool center, positive; };
struct Candidate { U left, right, cost; std::int64_t parent; bool center, positive; };
struct RecordSum {
  std::vector<U> minimum, suffix;
  void finish() {
    suffix.assign(minimum.size()+1,0);
    for (std::size_t i=minimum.size(); i-->0;) suffix[i]=suffix[i+1]+minimum[i];
  }
  U evaluate(U record) const {
    std::size_t lo=0,hi=minimum.size();
    while(lo<hi){auto mid=(lo+hi)/2;if(minimum[mid]>record)lo=mid+1;else hi=mid;}
    return record*lo+suffix[lo];
  }
};
struct Tail { RecordSum left,right; std::vector<int> moves; };
struct Pursuit { int first; std::vector<U> price,prefix; };
struct Finish {
  U cost; std::int64_t trace; int tail, start, steps;
  std::vector<U> prefix;
  bool operator<(const Finish& b)const{return std::tie(cost,trace,tail)<std::tie(b.cost,b.trace,b.tail);}
};

class Pricing {
  int n,R,C,H,keep,centerPolicy; U D;
  std::vector<U> field;
  std::vector<U> histories;
  std::size_t historyWords=0, peakHistoryBytes=0;
  std::int64_t historyOffset=0, historiesCreated=0;
  std::vector<Tail> tails;
  std::map<std::tuple<int,int,int>,int> tailIndex;
  std::priority_queue<Finish> winners;
  std::vector<Pursuit> pursuits;
  bool outward=false;
  U generated=0,retained=0,dominated=0,terminal=0;
  U boundPruned=0,centerPruned=0;
  U phasePruned=0,heavyPruned=0,balancePruned=0,precenterStates=0,postcenterStates=0;
  U returnJumps=0,jumpedSteps=0;
  U frontTerminals=0;
  std::size_t largest=0;

  U g(int j,int k)const{return field[static_cast<std::size_t>(j)*(R+1)+std::abs(k)];}
  U charge(int j,int k)const {const auto a=g(j,k);return k<0?D-a:D+a;}
  int makeTail(int j,int position,int first) {
    auto key=std::make_tuple(j,position,first);
    if(auto it=tailIndex.find(key);it!=tailIndex.end())return it->second;
    Tail tail;bool left=position==-R,right=position==R;
    U lm=2*D,rm=2*D;
    int k=position,t=j;
    auto advance=[&](int target){
      const int step=target>k?1:-1;
      while(k!=target){
        if(t>=H)throw std::runtime_error("suffix exceeds normalized horizon");
        if(!left){lm=std::min(lm,charge(t,k));tail.left.minimum.push_back(lm);}
        if(!right){rm=std::min(rm,charge(t,-k));tail.right.minimum.push_back(rm);}
        tail.moves.push_back(step);k+=step;++t;
        left=left||k==-R;right=right||k==R;
      }
    };
    if(left)advance(R);
    else if(right)advance(-R);
    else{advance(first*R);advance(-first*R);}
    if(!left||!right)throw std::runtime_error("incomplete suffix");
    tail.left.finish();tail.right.finish();
    const int id=static_cast<int>(tails.size());tails.push_back(std::move(tail));tailIndex[key]=id;
    return id;
  }
  void offerSuffix(int j,int k,const State& s,int first){
    const int id=makeTail(j,k,first);const auto& tail=tails[id];
    const U cost=s.cost+tail.left.evaluate(s.left)+tail.right.evaluate(s.right);
    ++terminal;
    // The serial tie key is identical to the former append-only Trace ID.
    // Only a winning suffix copies its prefix; rejected offers allocate none.
    Finish f{cost,keep?historyOffset+s.trace:-1,id,k,j,{}};
    const bool full=static_cast<int>(winners.size())>=std::max(1,keep);
    if(full && !(f<winners.top()))return;
    if(keep && historyWords){
      const auto first=histories.begin()+s.trace*historyWords;
      f.prefix.assign(first,first+historyWords);
      int positive=0;
      for(const U word:f.prefix)positive+=__builtin_popcountll(word);
      f.start=k-(2*positive-j);
    }
    if(full)winners.pop();
    winners.push(std::move(f));
  }
  void finish(int j,int k,const State& s,int first){
    if(!s.center && (std::abs(k)!=R || j+R>C))return;
    offerSuffix(j,k,s,first);
  }
  void preparePursuits(){
    for(int u=-R;u<=C+R;u+=2){
      Pursuit p;p.first=std::max(0,u-R);p.prefix.push_back(0);
      for(int j=p.first;j<u+R;++j){
        const U value=charge(j,u-j);
        if(!p.price.empty()&&value>p.price.back())throw std::runtime_error("nonmonotone direct pursuit");
        p.price.push_back(value);p.prefix.push_back(p.prefix.back()+value);
      }
      pursuits.push_back(std::move(p));
    }
    outward=true;
    for(int j=C;j<=H&&outward;++j)for(int k=j%2;k<=R;k+=2){
      const int foot=k-j+C;const U expected=foot<=0?0:g(C,foot);
      if(g(j,k)!=expected){outward=false;break;}
    }
  }
  U pursuitCost(int j,int k,U record,int through)const{
    const auto& p=pursuits[(j+k+R)/2];
    const auto begin=static_cast<std::size_t>(j-p.first);
    const auto end=static_cast<std::size_t>(std::min(through,j+k+R)-p.first);
    std::size_t lo=begin,hi=end;
    while(lo<hi){const auto mid=(lo+hi)/2;if(p.price[mid]>record)lo=mid+1;else hi=mid;}
    return record*(lo-begin)+p.prefix[end]-p.prefix[lo];
  }
  U remainingLower(int j,int k,const State& s)const{
    if(!outward)return pursuitCost(j,k,s.left,H)+pursuitCost(j,-k,s.right,H);
    const int duration=C-j;
    const U prefix=pursuitCost(j,k,s.left,C)+pursuitCost(j,-k,s.right,C);
    const U lm=k+R<=duration?0:std::min(s.left,charge(C,k-duration));
    const U rm=R-k<=duration?0:std::min(s.right,charge(C,-k-duration));
    const int reach=duration-std::abs(k);
    const int low=s.center?std::max(-R,k-duration):std::max(-R,-reach);
    const int high=s.center?std::min(R,k+duration):std::min(R,reach);
    U future=INF;
    for(int x:{low,high}){
      future=std::min(future,static_cast<U>(R-x)*rm+static_cast<U>(3*R-x)*lm);
      future=std::min(future,static_cast<U>(R+x)*lm+static_cast<U>(3*R+x)*rm);
    }
    return prefix+future;
  }
  void validate()const{
    if(n<1||n>10000||D==0||D>1000000000000ULL||24ULL*n*D>INF/2)
      throw std::runtime_error("unsafe dimensions or integer scale");
    for(int j=0;j<=H;++j)for(int k=j%2;k<=R;k+=2){
      auto a=g(j,k);if(a>D||(k==0&&a!=0))throw std::runtime_error("invalid radial field range or center");
      if(k<R)for(int sign:{-1,1})if(j+sign>=0&&j+sign<=H)
        if(a>g(j+sign,k+1))throw std::runtime_error("radial interval order violation");
    }
  }
public:
  explicit Pricing(const std::string& input,int keepCount,int policy):keep(keepCount),centerPolicy(policy){
    if(policy<0||policy>4)throw std::runtime_error("invalid center policy");
    if(policy>=3 && keepCount!=0)throw std::runtime_error("jump policy requires zero witness count");
    std::ifstream in(input,std::ios::binary);if(!in)throw std::runtime_error("cannot open input");
    std::uint32_t version,nn;in.read(reinterpret_cast<char*>(&version),4);in.read(reinterpret_cast<char*>(&nn),4);
    in.read(reinterpret_cast<char*>(&D),8);if(!in||version!=1||nn>10000)throw std::runtime_error("bad input header");
    n=static_cast<int>(nn);R=2*n;C=4*n;H=12*n;
    field.resize(static_cast<std::size_t>(H+1)*(R+1));
    in.read(reinterpret_cast<char*>(field.data()),static_cast<std::streamsize>(8*field.size()));
    char extra;if(!in||in.read(&extra,1))throw std::runtime_error("wrong input length");
    validate();if(keep<0||keep>1000)throw std::runtime_error("invalid output count");
    preparePursuits();
    if(centerPolicy && !outward)throw std::runtime_error("center compression requires outward-after-two field");
    if(centerPolicy)for(int j=0;j<C;j+=2)
      if(g(j+2,R)>g(j,R))throw std::runtime_error("center compression requires sticky endpoint trace");
    if(centerPolicy==4)for(int j=0;j<=H;++j)for(int k=j%2;k<=R;k+=2){
      if(j+k<=C)continue;
      const int distance=(j+k-C)/2,foot=k-distance;
      const U expected=foot<=0?0:g(j-distance,foot);
      if(g(j,k)!=expected)throw std::runtime_error("front policy requires exact incoming-front-two identities");
    }
  }
  void run(std::ostream& out){
    const int stride=centerPolicy?4:2;
    std::vector<std::vector<State>> layer(2*R+1);
    std::vector<std::vector<Candidate>> pendingCenter(C+1);
    // Fair reflection gives identical prices and calendar coefficients.
    // Represent each reflected start pair once; later positions stay signed.
    for(int k=0;k<=R;k+=2){
      const auto id=keep?historiesCreated++:-1;
      const State s{2*D,2*D,0,id,k==0,false};layer[k+R].push_back(s);
      // Both direct initial endpoint orders are legal center-by-two paths.
      // At the center the reflected order is redundant.
      offerSuffix(0,k,s,k==R?-1:1);
      if(k>0&&k<R)offerSuffix(0,k,s,-1);
    }
    for(int j=0;j<=C;++j){
      std::vector<std::vector<Candidate>> next(stride*(2*R+1));std::size_t count=0;
      for(int k=-R;k<=R;++k)for(const auto& s:layer[k+R]){
        ++count;if(s.center)++postcenterStates;else ++precenterStates;
        if(std::abs(k)==R){finish(j,k,s,k>0?-1:1);continue;}
        if(j==C || (centerPolicy==4 && s.center && j+std::abs(k)>=C)){
          if(s.center){
            // Each original tail scans this node before integrating its
            // first step, so a new front-contact record is not omitted.
            if(j<C)++frontTerminals;
            finish(j,k,s,-1);finish(j,k,s,1);
          }
          continue;
        }
        if(!s.center&&std::abs(k)>C-j){++centerPruned;continue;}
        if(winners.size()>=static_cast<std::size_t>(std::max(1,keep))&&
           s.cost+remainingLower(j,k,s)>=winners.top().cost){++boundPruned;continue;}
        const U lm=std::min(s.left,charge(j,k)),rm=std::min(s.right,charge(j,-k));
        const U cost=s.cost+lm+rm;
        for(int step:{-1,1}){
          if(j==0 && k==0 && step<0)continue;
          if(centerPolicy && s.center){
            // Include the current center/peak sample in lm/rm before any
            // ordering test. Inward states have a fixed return to center.
            if(k==0){
              const int heavier=lm<=rm?1:-1;
              if(step!=heavier){++heavyPruned;continue;}
            }else{
              const bool inward=k>0?!s.positive:s.positive;
              const int toward=k>0?-1:1;
              if(inward && step!=toward){++phasePruned;continue;}
              if(centerPolicy>=2 && !inward && step==toward &&
                 (k>0?rm>lm:lm>rm)){++balancePruned;continue;}
              if(centerPolicy>=3 && step==toward){
                // Along a unit inward ray both updated records are constant:
                // the attacked sample increases and the opposite record is
                // already at most D after the previous center visit.
                const int duration=std::min(std::abs(k),C-j);
                const int time=j+duration,position=k+duration*toward;
                const U total=s.cost+static_cast<U>(duration)*(lm+rm);
                const State returned{lm,rm,total,-1,true,step>0};
                ++returnJumps;jumpedSteps+=duration;++generated;
                if(time==C){
                  finish(time,position,returned,-1);
                  finish(time,position,returned,1);
                }else if(winners.size()>=static_cast<std::size_t>(std::max(1,keep))&&
                         total+remainingLower(time,0,returned)>=winners.top().cost){
                  ++boundPruned;
                }else{
                  pendingCenter[time].push_back({lm,rm,total,-1,true,step>0});
                }
                continue;
              }
            }
          }
          const int x=k+step;const bool c=s.center||x==0;
          if(!c&&j+1>=C)continue;
          const bool inward=x!=0 && (x>0?step<0:step>0);
          const int group=centerPolicy?(c?2+static_cast<int>(inward):0):static_cast<int>(c);
          next[stride*(x+R)+group].push_back({lm,rm,cost,s.trace,c,step>0});++generated;
        }
      }
      retained+=count;largest=std::max(largest,count);
      if(j==C)break;
      if(centerPolicy>=3 && !pendingCenter[j+1].empty()){
        auto& target=next[stride*R+2];
        auto& pending=pendingCenter[j+1];
        target.insert(target.end(),pending.begin(),pending.end());
        std::vector<Candidate>().swap(pending);
      }
      layer.assign(2*R+1,{});
      std::size_t nextRows=0;
      for(int index=0;index<static_cast<int>(next.size());++index){
        auto& v=next[index];if(v.empty())continue;
        std::sort(v.begin(),v.end(),[](const Candidate& a,const Candidate& b){
          return std::tie(a.left,a.right,a.cost,a.parent)<std::tie(b.left,b.right,b.cost,b.parent);
        });
        std::vector<U> right;right.reserve(v.size());for(const auto& s:v)right.push_back(s.right);
        std::sort(right.begin(),right.end());right.erase(std::unique(right.begin(),right.end()),right.end());
        std::vector<U> fenwick(right.size()+1,INF);
        auto query=[&](std::size_t i){U answer=INF;for(;i;i-=i&-i)answer=std::min(answer,fenwick[i]);return answer;};
        auto put=[&](std::size_t i,U value){for(;i<fenwick.size();i+=i&-i)fenwick[i]=std::min(fenwick[i],value);};
        const int k=index/stride-R;
        for(const auto& s:v){
          const auto rank=static_cast<std::size_t>(std::lower_bound(right.begin(),right.end(),s.right)-right.begin()+1);
          if(query(rank)<=s.cost){++dominated;continue;}
          put(rank,s.cost);
          // Keep the parent row only until this layer's Pareto pass ends.
          // Then one exactly sized contiguous buffer stores retained prefixes.
          layer[k+R].push_back({s.left,s.right,s.cost,s.parent,s.center,s.positive});
          ++nextRows;
        }
      }
      if(keep){
        const std::size_t nextWords=static_cast<std::size_t>((j+1+63)/64);
        if(nextRows>std::numeric_limits<std::size_t>::max()/nextWords)
          throw std::runtime_error("packed witness allocation overflow");
        std::vector<U> nextHistories(nextRows*nextWords,0);
        peakHistoryBytes=std::max(peakHistoryBytes,
          (histories.capacity()+nextHistories.capacity())*sizeof(U));
        std::size_t row=0;
        for(auto& group:layer)for(auto& s:group){
          auto* target=nextHistories.data()+row*nextWords;
          if(historyWords)std::copy_n(histories.data()+s.trace*historyWords,historyWords,target);
          if(s.positive)target[j/64]|=U{1}<<(j%64);
          s.trace=static_cast<std::int64_t>(row++);
        }
        if(row!=nextRows)throw std::runtime_error("packed witness row count");
        historyOffset=historiesCreated;
        if(nextRows>static_cast<std::size_t>(std::numeric_limits<std::int64_t>::max()-historiesCreated))
          throw std::runtime_error("witness serial overflow");
        historiesCreated+=static_cast<std::int64_t>(nextRows);
        histories.swap(nextHistories);historyWords=nextWords;
      }
    }
    if(winners.empty())throw std::runtime_error("no normalized path");
    std::vector<Finish> best;while(!winners.empty()){best.push_back(winners.top());winners.pop();}
    std::sort(best.begin(),best.end());
    out<<"{\"status\":\"PASS\",\"scope\":\"exact integer dual pricing on the normalized physical grid bank\",\"n\":"<<n
       <<",\"field_denominator\":\""<<D<<"\",\"minimum_units\":\""<<best[0].cost
       <<"\",\"objective_denominator\":\""<<4ULL*n*D<<"\",\"retained_states\":"<<retained
       <<",\"center_policy\":"<<centerPolicy<<",\"precenter_states\":"<<precenterStates<<",\"postcenter_states\":"<<postcenterStates
       <<",\"center_phase_pruned_moves\":"<<phasePruned<<",\"heavier_side_pruned_moves\":"<<heavyPruned<<",\"peak_balance_pruned_moves\":"<<balancePruned
       <<",\"deterministic_return_jumps\":"<<returnJumps<<",\"jumped_return_steps\":"<<jumpedSteps
       <<",\"incoming_front_terminal_states\":"<<frontTerminals
       <<",\"generated_transitions\":"<<generated<<",\"dominance_pruned\":"<<dominated
       <<",\"independent_pursuit_pruned\":"<<boundPruned<<",\"late_center_pruned\":"<<centerPruned
       <<",\"maximum_layer\":"<<largest<<",\"terminal_tours\":"<<terminal
       <<",\"witness_storage\":\"packed current-layer prefixes\",\"peak_packed_trace_bytes\":"<<peakHistoryBytes
       <<",\"paths\":[";
    bool comma=false;
    for(const auto& b:best){
      if(!keep)break;
      std::vector<int> moves;
      for(int j=0;j<b.steps;++j)moves.push_back((b.prefix[j/64]>>(j%64))&1?1:-1);
      moves.insert(moves.end(),tails[b.tail].moves.begin(),tails[b.tail].moves.end());
      if(comma)out<<",";
      comma=true;
      out<<"{\"units\":\""<<b.cost<<"\",\"start_grid\":"<<b.start<<",\"moves\":[";
      for(std::size_t i=0;i<moves.size();++i){if(i)out<<",";out<<moves[i];}out<<"]}";
    }
    out<<"]}\n";
  }
};
int main(int argc,char** argv){
  try{
    if(argc<2||argc>4)throw std::runtime_error("usage: price_center input.bin [number_of_paths [policy=2]]");
    Pricing search(argv[1],argc>=3?std::stoi(argv[2]):32,argc==4?std::stoi(argv[3]):2);search.run(std::cout);return 0;
  }catch(const std::exception& error){std::cerr<<error.what()<<"\n";return 1;}
}
