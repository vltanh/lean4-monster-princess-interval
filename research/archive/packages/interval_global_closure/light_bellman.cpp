// Integer Bellman lower certificate on a directed light-coordinate cell graph.
#include <algorithm>
#include <cassert>
#include <cstdint>
#include <fstream>
#include <iostream>
#include <limits>
#include <string>
#include <vector>
using U=uint64_t; using W=unsigned __int128;
struct Cell {
  int right,up; U time,a,b; bool terminal,initial;
  U la,lb,ra,rb;
  unsigned na,nb;
  std::vector<U> values;
};
struct Graph {
  unsigned count,bins; U den,time_den,quantum; std::vector<Cell> cells;
  explicit Graph(std::istream &in) {
    in>>count>>bins>>den>>time_den;assert(bins&&den%bins==0);quantum=den/bins;
    cells.resize(count);
    U maximum_time=time_den;
    for(unsigned i=0;i<count;i++) {
      auto &c=cells[i];
      in>>c.right>>c.up>>c.time>>c.a>>c.b>>c.terminal>>c.initial>>c.la>>c.lb>>c.ra>>c.rb;
      assert(c.a+c.b<=den);
      assert(c.right<0||unsigned(c.right)>i);assert(c.up<0||unsigned(c.up)>i);
      assert(c.terminal||c.right>=0||c.up>=0);
      maximum_time=std::max({maximum_time,c.time,c.la,c.lb,c.ra,c.rb});
      c.na=unsigned((c.a+quantum-1)/quantum)+1;c.nb=unsigned((c.b+quantum-1)/quantum)+1;
    }
    assert(in.good());
    assert(W(den)*maximum_time<std::numeric_limits<U>::max());
    assert(W(den)*time_den<std::numeric_limits<U>::max());
  }
  U coordinate(unsigned i,U end) const{return std::min(U(i)*quantum,end);}
  static U lerp(U x,U x0,U x1,U v0,U v1) {
    assert(x0<=x&&x<=x1);
    if(x==x0||x0==x1)return v0;if(x==x1)return v1;
    return U((W(x1-x)*v0+W(x-x0)*v1)/(x1-x0));
  }
  U lookup(const Cell &c,U a,U b) const {
    assert(a<=c.a&&b<=c.b);
    unsigned i=std::min(unsigned(a/quantum),c.na-1),j=std::min(unsigned(b/quantum),c.nb-1);
    unsigned k=std::min(i+1,c.na-1),l=std::min(j+1,c.nb-1);
    U a0=coordinate(i,c.a),a1=coordinate(k,c.a),b0=coordinate(j,c.b),b1=coordinate(l,c.b);
    U left=lerp(b,b0,b1,c.values[size_t(i)*c.nb+j],c.values[size_t(i)*c.nb+l]);
    U right=lerp(b,b0,b1,c.values[size_t(k)*c.nb+j],c.values[size_t(k)*c.nb+l]);
    return lerp(a,a0,a1,left,right);
  }
  std::pair<U,int> best(const Cell &c,U a,U b) const {
    U value=std::numeric_limits<U>::max();int chosen=-1;
    if(c.terminal)value=std::min(a*c.la+b*c.lb,a*c.ra+b*c.rb);
    for(int j:{c.right,c.up})if(j>=0) {
      const auto &d=cells[j];assert(d.time>=c.time);
      U aa=std::min(a,d.a),bb=std::min(b,d.b);
      U candidate=d.time*((a-aa)+(b-bb))+lookup(d,aa,bb);
      if(candidate<value){value=candidate;chosen=j;}
    }
    return {value,chosen};
  }
};
int main(int argc,char **argv) {
  if(argc<3){std::cerr<<"usage: light_bellman input output\n";return 2;}
  std::ifstream in(argv[1]);Graph g(in);U states=0;
  for(unsigned kk=g.count;kk>0;kk--) {
    auto &c=g.cells[kk-1];c.values.resize(size_t(c.na)*c.nb);states+=c.values.size();
    for(unsigned i=0;i<c.na;i++)for(unsigned j=0;j<c.nb;j++)
      c.values[size_t(i)*c.nb+j]=g.best(c,g.coordinate(i,c.a),g.coordinate(j,c.b)).first;
  }
  U best=std::numeric_limits<U>::max();int start=-1;
  for(unsigned i=0;i<g.count;i++)if(g.cells[i].initial) {
    const auto &c=g.cells[i];U v=g.lookup(c,c.a,c.b);
    if(v<best){best=v;start=int(i);}
  }
  assert(start>=0);
  std::ofstream out(argv[2]);
  out<<"{\"cells\":"<<g.count<<",\"rank_bins\":"<<g.bins
     <<",\"probability_denominator\":"<<g.den<<",\"time_denominator\":"<<g.time_den
     <<",\"bound_numerator\":"<<best<<",\"bound_denominator\":"<<g.den*g.time_den
     <<",\"evaluated_states\":"<<states<<",\"cell_route\":["<<start;
  U a=g.cells[start].a,b=g.cells[start].b;
  for(int i=start;;) {
    int j=g.best(g.cells[i],a,b).second;if(j<0)break;
    out<<','<<j;a=std::min(a,g.cells[j].a);b=std::min(b,g.cells[j].b);i=j;
  }
  out<<"]}\n";
  std::cerr<<"cells "<<g.count<<" states "<<states<<" bound "<<double(best)/double(g.den*g.time_den)<<"\n";
}
