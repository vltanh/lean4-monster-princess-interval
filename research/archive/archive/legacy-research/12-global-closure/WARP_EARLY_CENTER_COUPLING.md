# Early prefix and center-potential coupling

The common-warp five-family construction is rejected by the exact positive
M2 with reference start a=1/8 and first turn s=15/16. Its physical cost is

    181988419226356214104426769 / 128000000000000000000000000
    = 1.421784525205908,

below the approximately 1.4231574374 five-family level. This is a genuine
first-capture calculation on the complete warped field. It is not a
quantile approximation. Positive M3 with reference(a,s,t)=(1/8,7/8,1)
also costs only about 1.422379717276559.

At the M2 witness,

    A=10218164907/250000000000,
    B=327949300711/500000000000,
    Z=10184278599/15625000000,

so A<Z<B and the hinge F vanishes. The complete beta-row moment is exactly
H=2Z, both before and after the warp. One-sided derivatives with respect
to the reference start are about (-.06087056,+.02675696), and with respect
to the reference first turn about(-2.53654563,+.02230063). Thus the
existing coordinates form a strict corner minimum. Adding intermediate
turn samples is not the missing mathematical step.

## Exact early-M2 source

Use physical coordinates in this section. Put

    A=A(a), B=R(s,-a), Z=R(s,s),
    I=integral_a^s R(U,-a)dU,
    F=integral_-a^s (A-R(s,V))_+ dV,
    H(s)=integral_s^(s+2) R(U,s)dU.

The exact cost is

    4C_+=4s+8+2sA-(s+6+a)B-I-F-H.

At smooth points define
J_A=integral_-a^s 1{R(s,V)<A} R_U(s,V)dV. Then

    4 partial_s C_+
      =4+A+min(A,Z)-2B-(s+6+a)R_U(s,-a)+J_A-H'(s).

The min(A,Z) term includes the center-diagonal contribution. On A<Z,
F=J_A=0 and the leading term is 4+2A, not 4+A.

For a fixed active start, q=2+A-B and w=s+6+a obey

    (q w^2)' = w H'(s).

This is a forced inverse-square row. A drifting active start requires
its additional derivative terms and cannot be replaced by this integrated
fixed-start formula.

In reference coordinates of a common warp, replace s,a by psi(s),psi(a)
in the time coefficients and use

    H_psi(s)=integral_s^(s+2)R(U,s)dpsi(U),
    J_psi=integral_-a^s1{R<A}R_U(s,V)dpsi(V).

Then

    4 partial_s C_+
      =psi'(s)[4+A+min(A,Z)-2B]
       -[6+psi(s)+psi(a)]R_U(s,-a)+J_psi-H_psi'(s).

The same forced relation is
(q[6+psi(s)+psi(a)]^2)'=[6+psi(s)+psi(a)]H_psi'(s)
on a fixed-start A<Z active branch.

## The general center continuation is the actual coupling variable

Let W(t,n) be the transformed balanced center value from the center
factorization, and let N(a)=integral_-a^a R(a,V)dV. The exact cost of a
negative start -a going directly to its first center, then using an
optimal arbitrary continuation, is

    G_-(a)=N(a)/4+W(a,A(a)).

For a positive start +a, an initial outward turn U=s, direct return to
the first center, and arbitrary optimal continuation,

    G_+(a,s)=W(s,B)+[2sA+(s-a)B-I-F]/4.

Thus early one-M2 is the special case in which the endpoint completion
value is substituted for W. The general W includes arbitrary subsequent
returns. Initial inward reversals before the first center remain a
separate prefix family. More generally, for any positive-side prefix
ending at its first center time s, let M be its largest captured radial
rank and tau_q the positive-copy first hit. Its exact optimized cost is
W(s,M)+(1/2) integral_0^M tau_q dq. The missing initial-history problem is
therefore a one-sided prefix problem with terminal potential W; it can
still contain arbitrary same-half oscillations.

At smooth points let gamma=s if A<=Z; otherwise choose the row root
R(s,gamma)=A. Differentiating gives

    4 G_{+,s}
      =4W_t(s,B)+A+min(A,Z)
       +[s-a+4W_n(s,B)]R_U(s,-a)+J_A,

    4 G_{+,a}
      =A'(a)(s+gamma)-(B-A)
       -[s-a+4W_n(s,B)]R_V(s,-a)
       +integral_a^s R_V(U,-a)dU.

The general first-center identity follows directly from the record
partition. The positive-copy prefix contributes (1/2) integral_0^M tau_q dq.
The negative-copy center contact contributes sZ/2. The remaining value is
J(s,M,Z)=[T_s(M)-T_s(Z)]/2+V(s,M). Since T_s(Z)=sZ, the two center terms
cancel and the remaining sum is W(s,M)+(1/2) integral_0^M tau_q dq.

Trace conventions matter for a general law with atoms. N uses the strict
horizontal radial CDF. G_- uses the closed initial A_le, whereas G_+ uses
the strict initial A_<. Outward first-contact frontiers and vertical beta
integrals use closed traces; horizontal inverse-prefix integrals use
strict traces. All these initial traces coincide on the saved continuous
initial data. The barrier flatness excludes the actual endpoint
U=s0+2, where the closed radial CDF is 1. A path which never reaches the
center leaves an entire reflected half of a symmetric radial law
uncaught and has infinite expected cost.

These are coupled field/potential phase equations. Classical derivatives
are asserted only on smooth branches. At the witnessed knots use the
one-sided cost inequalities instead.

For endpoint completion,
W_n=-(s+3)/2 and 4W_t=4-2B-H', recovering the earlier formulas exactly.
Also H(s)=2[s+1-T_s(1)], where T_s(1)=integral_0^1 beta_q(s)dq.
The early source is therefore the same beta moment already present in
the center renewal boundary, not a new independent functional datum.

## A finite center-barrier closure face

If a candidate retains a fixed barrier s0 with
R(U,s0)=Z0 on s0<=U<s0+2 and the all-future interior rank bound needed
for endpoint completion, then H(s0)=2Z0. For starts with A(a)<Z0 the
active initial-prefix equality is

    (s0+6+a)R(s0,-a)+integral_a^s0 R(U,-a)dU+2Z0
      =4s0+8+2s0A(a)-4V.

For fixed physical start/turn this is affine in the full CDF. On the
existing affine mesh, the complete fixed-s0 start family consists of
one-dimensional quadratic cells with linear field coefficients; it
needs no hinge-root arrangement. It couples the initial trace, negative-V
incoming column and center rank. A common warp freezes their reference
knot ranks, which explains why a geometry-only optimization can fail.

This is one missing closure component, not a proof that all other turn
levels or initial prefixes are redundant. Away from the barrier, the
attached general W must be retained.

## Replay

    node verify_warp_early_phase.mjs FIELD FIVE_FAMILY_SOLUTION REPORT

The exact input field is Git blob 5c45d042ee9948faebc03354c3e1e2ee3cbec1a5,
and the strict five-family warp is e007870c77baf4b13986272333f22e899f6d81ee.
The verifier independently scores all four physical witness routes,
checks the exact warp features and M2 moment identity, verifies F=0 and
H=2Z, and obtains both one-sided derivatives from exact local quadratics.
The portable V8 computational body was run; native execution was
unavailable. The discovery search itself tested 27,437 floating routes or
iterates and is explicitly not a completeness certificate.
