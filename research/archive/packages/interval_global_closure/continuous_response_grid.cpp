// Physical light-coordinate node routes, with continuum capture costs.
// Floating concave interpolation guides attack discovery; it is not an
// unrestricted-monster lower certificate. Every reported route is rescored
// exactly by continuous_response_grid.py.
#include <algorithm>
#include <cassert>
#include <cmath>
#include <fstream>
#include <iomanip>
#include <iostream>
#include <limits>
#include <sstream>
#include <string>
#include <utility>
#include <vector>

struct Node {
  int right,up,wait=-1; double t,x,a,b; bool initial,terminal; unsigned na,nb;
  std::vector<double> right_cost,left_cost,wait_cost,values;
};
struct Graph {
  unsigned count,bins; double horizon; std::vector<Node> nodes;std::vector<double> knots;
  explicit Graph(std::istream&in){
    std::string header;std::getline(in,header);std::istringstream first(header);int waits=0;
    unsigned knot_count=0;first>>count>>bins>>horizon;first>>waits;first>>knot_count;
    assert(bins>0);nodes.resize(count);
    if(knot_count){knots.resize(knot_count);for(double&x:knots)in>>x;
      assert(knots.front()==0&&knots.back()==1&&std::is_sorted(knots.begin(),knots.end()));}
    for(unsigned i=0;i<count;i++){
      auto&c=nodes[i];
      in>>c.right>>c.up;if(waits)in>>c.wait;
      in>>c.t>>c.x>>c.a>>c.b>>c.initial>>c.terminal>>c.na>>c.nb;
      assert(c.a>=0&&c.b>=0&&c.a+c.b<=1+1e-12);
      assert(c.right<0||unsigned(c.right)>i);assert(c.up<0||unsigned(c.up)>i);
      assert(c.terminal||c.right>=0||c.up>=0);
      c.right_cost.resize(c.nb);c.left_cost.resize(c.na);
      for(double&x:c.right_cost)in>>x;
      for(double&x:c.left_cost)in>>x;
      if(c.wait>=0){assert(unsigned(c.wait)>i&&c.x==0&&c.a==c.b&&c.na==c.nb);
        c.wait_cost.resize(c.na);for(double&x:c.wait_cost)in>>x;}
    }
    assert(in.good());
  }
  double coordinate(unsigned i,double end)const{return std::min(knots.empty()?double(i)/bins:knots[i],end);}
  unsigned index(double x,unsigned size)const{
    unsigned i=knots.empty()?unsigned(x*bins):unsigned(std::upper_bound(knots.begin(),knots.end(),x)-knots.begin()-1);
    return std::min(i,size-1);
  }
  static double lerp(double x,double x0,double x1,double v0,double v1){
    if(x<=x0||x0==x1)return v0;if(x>=x1)return v1;
    return ((x1-x)*v0+(x-x0)*v1)/(x1-x0);
  }
  double scalar(const std::vector<double>&values,double end,double x)const{
    assert(x<=end+1e-12&&x>=-1e-12);x=std::min(end,std::max(0.,x));
    unsigned i=index(x,values.size());
    unsigned j=std::min(i+1,unsigned(values.size()-1));
    return lerp(x,coordinate(i,end),coordinate(j,end),values[i],values[j]);
  }
  double lookup(const Node&c,double a,double b)const{
    assert(a<=c.a+1e-12&&b<=c.b+1e-12);
    a=std::min(a,c.a);b=std::min(b,c.b);
    unsigned i=index(a,c.na),j=index(b,c.nb);
    unsigned k=std::min(i+1,c.na-1),l=std::min(j+1,c.nb-1);
    double aa=coordinate(i,c.a),ab=coordinate(k,c.a),ba=coordinate(j,c.b),bb=coordinate(l,c.b);
    double left=lerp(b,ba,bb,c.values[size_t(i)*c.nb+j],c.values[size_t(i)*c.nb+l]);
    double right=lerp(b,ba,bb,c.values[size_t(k)*c.nb+j],c.values[size_t(k)*c.nb+l]);
    return lerp(a,aa,ab,left,right);
  }
  std::pair<double,int> best(const Node&c,double a,double b)const{
    double value=std::numeric_limits<double>::infinity();int chosen=-1;
    if(c.terminal)value=std::min(a*(horizon+1+c.x)+b*(horizon+3+c.x),
                                 a*(horizon+3-c.x)+b*(horizon+1-c.x));
    if(c.right>=0){
      const auto&d=nodes[c.right];assert(d.a+1e-12>=c.a);
      double candidate=scalar(c.right_cost,c.b,b)+lookup(d,std::min(a,d.a),std::min(b,d.b));
      if(candidate<value){value=candidate;chosen=c.right;}
    }
    if(c.up>=0){
      const auto&d=nodes[c.up];assert(d.b+1e-12>=c.b);
      double candidate=scalar(c.left_cost,c.a,a)+lookup(d,std::min(a,d.a),std::min(b,d.b));
      if(candidate<value){value=candidate;chosen=c.up;}
    }
    if(c.wait>=0){
      const auto&d=nodes[c.wait];assert(d.x==0);
      double candidate=scalar(c.wait_cost,c.a,a)+scalar(c.wait_cost,c.b,b)
                       +lookup(d,std::min(a,d.a),std::min(b,d.b));
      if(candidate<value){value=candidate;chosen=c.wait;}
    }
    return {value,chosen};
  }
};

int main(int argc,char**argv){
  if(argc<3){std::cerr<<"usage: grid input output [route_count]\n";return 2;}
  unsigned requested=argc>3?std::stoul(argv[3]):8;
  std::ifstream input(argv[1]);Graph g(input);size_t states=0;
  for(unsigned k=g.count;k>0;k--){
    auto&c=g.nodes[k-1];c.values.resize(size_t(c.na)*c.nb);states+=c.values.size();
    for(unsigned i=0;i<c.na;i++)for(unsigned j=0;j<c.nb;j++)
      c.values[size_t(i)*c.nb+j]=g.best(c,g.coordinate(i,c.a),g.coordinate(j,c.b)).first;
  }
  std::vector<std::pair<double,int>> starts;
  for(unsigned i=0;i<g.count;i++)if(g.nodes[i].initial&&g.nodes[i].x>=0){
    const auto&c=g.nodes[i];starts.emplace_back(g.lookup(c,c.a,c.b),int(i));
  }
  std::sort(starts.begin(),starts.end());
  std::ofstream out(argv[2]);out<<std::setprecision(17)
    <<"{\"scope\":\"Physical node-route attack discovery with continuous CDF costs; interpolation estimate is not an unrestricted lower certificate\","
    <<"\"nodes\":"<<g.count<<",\"rank_bins\":"<<g.bins<<",\"record_knots\":"<<g.knots.size()
    <<",\"states\":"<<states<<",\"routes\":[";
  for(unsigned k=0;k<std::min(requested,unsigned(starts.size()));k++){
    auto[estimate,start]=starts[k];if(k)out<<',';
    out<<"{\"estimate\":"<<estimate<<",\"node_ids\":["<<start;
    double a=g.nodes[start].a,b=g.nodes[start].b;
    for(int i=start;;){
      int next=g.best(g.nodes[i],a,b).second;if(next<0)break;
      out<<','<<next;a=std::min(a,g.nodes[next].a);b=std::min(b,g.nodes[next].b);i=next;
    }
    out<<"]}";
  }
  out<<"]}\n";
  std::cerr<<"nodes "<<g.count<<" states "<<states<<" best estimate "<<starts.front().first<<"\n";
}
