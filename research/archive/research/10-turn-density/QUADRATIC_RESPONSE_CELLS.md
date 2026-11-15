# Exact continuum response cells on an affine CDF

This is an instantiated response component, not an unrestricted game certificate. It turns a whole three-parameter geometric cell of the attacking early M3 family into two exact 4-by-4 matrix constraints. No response sampling or field-mesh refinement is involved.

## Exact hinge lift

Assume a continuous affine radial CDF on the fixed triangular geometry, no initial center/endpoint atom and no outgoing V=1 atom, with ExactField's closed endpoint and strict center conventions. For negative-start M3, put

A=A(a), N=integral[-a,a] R(a,V)dV, B=R(s,a), D=R(1,s),
I=integral[a,s] R(U,a)dU.

The monster starts at -a, turns at U=s, then V=1, then visits right and left endpoints. Its exact four-cost is

4C = N+12-8A+(s+a-4)B-(7-s)(D-A)_+-I
     -integral[s,1](R(U,s)-A)_+ dU.

Since R(U,s) increases in U, the final integral equals

max_{s<=b<=1} { integral[b,1]R(U,s)dU -(1-b)A }.

Therefore 4C is the minimum over b in [s,1] and j in {0,1} of

F_j(a,s,b)=N+12-8A+(s+a-4)B-I-j(7-s)(D-A)
          -integral[b,1]R(U,s)dU+(1-b)A.

Requiring every actual route cost >= V is equivalent to requiring F_j>=4V for BOTH branches and EVERY cutoff. This does not freeze a rank root from the numerical field.

The corresponding lifted positive-family four-costs are

F_+M2(a,c)=12+(1+c)A-(7+a)R(1,-a)
          -integral[a,1]R(U,-a)dU+integral[c,1]R(1,V)dV;

F_+M1(a,c)=8-4a+(2-a+c)A
          -integral[a,2-a]R(U,-a)dU+integral[c,1]R(2-a,V)dV;

F_+M3(a,s,c)=12+(s+c)A-(4+a-s)R(s,-a)-(7-s)R(1,s)
            -integral[a,s]R(U,-a)dU-integral[s,1]R(U,s)dU
            +integral[c,s]R(s,V)dV.

The first two minimize over -a<=c<=1; the third minimizes over -a<=c<=s, with 0<=a<=s<=1. Negative M1/M2 need no cutoff.

## Geometric quadratic cells

A trace on a fixed field triangle is affine in coordinates and linear in field values. Characteristic integrals have affine geometric intersection coordinates, hence are quadratic in endpoint coordinates and linear in field values.

For negative M3, pair a triangle containing (s,a) and one containing (b,s). Their shared s interval has affine fiber bounds

l<=s<=h, a_-(s)<=a<=a_+(s), b_-(s)<=b<=b_+(s).

Each such rational polytope has at most eight vertices and can be triangulated geometrically. There is no value-dependent cutoff arrangement. Positive M3 pairs (s,-a) and (s,c) triangles. Positive M1 uses the existing post triangle under (a,c)=(2-U,V); positive M2 uses an initial a interval times a V interval at U=1, clipped by c>=-a.

The instantiated attacked cell is the tetrahedron

0<=a<=s-13/16, 13/16<=s<=b<=7/8,

with vertices

(0,13/16,13/16), (1/16,7/8,7/8),
(0,7/8,7/8), (0,13/16,7/8).

A lies on the first initial interval, (s,a) stays on one triangle because s-a>=13/16, and (b,s) stays in the same center triangle. Other integral pieces traverse complete mesh strips. Thus F_j is one quadratic on this entire tetrahedron, independently of the nodal values.

## Exact order-four cone

For simplex vertices v_i and barycentric weights lambda,

F(sum lambda_i v_i)=lambda^T Q lambda.

Q_ii=F(v_i), and
Q_ij=2F((v_i+v_j)/2)-(F(v_i)+F(v_j))/2.

Every entry is affine in the CDF values. Subtract 4V from EVERY matrix entry to encode a target. Nonnegativity on the simplex is equivalent by homogeneity to copositivity.

For order n<=4, the copositive cone is exactly

Q=P+N, P positive semidefinite, N entrywise nonnegative.

Thus the tetrahedral constraint has an exact SDP representation, not a hierarchy relaxation. The equivalence fails in order five. Original source: P. H. Diananda, On non-negative forms in real variables some or all of which are non-negative, Proc. Cambridge Philos. Soc.58(1962),17-25, DOI10.1017/S0305004100036185. The exact order-four statement is also verified in the primary research paper Schweighofer–Vargas, Sum-of-squares certificates for copositivity via test states, p.3:
https://www.math.uni-konstanz.de/~schweigh/publications/copositive.pdf

## Exact final verification

quadratic_simplex.py enumerates every nonempty face S and solves

[2Q_SS, -1; 1^T,0] (lambda,mu)=(0,1).

Every invertible system with nonnegative lambda supplies an exact Fraction candidate. Singular stationary faces can be skipped: a nonzero null pair (d,eta) satisfies 1^T d=0 and 2Qd=eta1, so d^TQd=0. At a stationary point, q(lambda+td)=q(lambda) until the line reaches a proper face. Recursing reaches an invertible face or vertex. No numerical PSD certificate or rationality assumption on an SDP decomposition is needed.

## Instantiated result

Run:
python packages/interval_cdf_discovery/verify_quadratic_response_cell.py

Before executor loss this completed 360 exact checks:112 identities of sparse affine rows (all nodal values simultaneously),224 independent record comparisons,4 optimal cutoff/branch gates,20 other-family identities.

New files saved before executor loss:
- quadratic_response_forms.py
- verify_quadratic_response_cell.py
- snapshots/negative_m3_quadratic_cell.json

The snapshot contains exact sparse four-score matrices, at most138 field coefficients per entry.

For endpoint_joint_i1_field.json, branch1 has its minimum in the tetrahedron interior at

a=.030235785946124943,
s=.8571340323028184,
b=.8582882613709526.

The exact physical first-capture engine agrees:
C=1.4233421829970763,
C-endpoint_reference=-.00011976218070780337.

Branch0 is safely positive. The current field FAILS this cell. This is a concrete whole-cell constraint for a joint field reconstruction, not a successful lower certificate. Other cells, other families and unrestricted paths remain open.
