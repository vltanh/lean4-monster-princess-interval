# Compensated curvature and a finite free-start cusp response

A positive inverse-curvature term in the exact three-leg exchange can be
absorbed by the transition derivative. This replaces horizontal CDF convexity
by a weaker invariant condition. It proves that the atom-free front-one
power cusp has an attained finite-turn global response, even though its
centered optimum requires infinitely many initial turns.

The broadened condition still cannot cover a competitive whole inner
region through front two: it forces inward Princess motion there and an
endpoint-sweep upper of at most five-fourths. These are supplied-field
results and a concrete-law corollary, not an equilibrium phase-existence
theorem.

## 1. Field-side condition

Use light coordinates U=t+x, W=t-x. On the phase write

\[
 A=F_U>0,\qquad B=-F_W\ge0.
\]

The sufficient conditions are

\[
 A_W\ge0,\qquad (\log A)_{UW}\le0,\qquad
 \boxed{B A_U+A A_W\ge0.}                         \tag{1}
\]

The last condition replaces horizontal convexity A_U>=0. Where B>0
it says (A/B)_U>=0. It includes horizontal convexity when A_W>=0,
but also permits A_U<0. Assume the field is \(C^3\) on the phase
interior, with continuous traces,
and use the coordinate-box and actual endpoint conventions of
[the curved exchange](CURVED_INITIAL_PHASE_RESPONSE.md) and
[the positive-prefront theorem](POSITIVE_PREFRONT_RESPONSE_AND_MODULUS.md).
The local comparison keeps the physical entry and exit states and times,
and attaches an increasing concave function of the two survivor records.
Every fixed bounded physical continuation supplies such a function.
Singular boundary derivatives are handled by continuous limits inside the
physical arena; actual endpoint capture uses its separate reset.

## 2. Cancellation in the exact RLR objective

For a rectangle [U0,U1] times [W0,W1], set

\[
 s=F(u,W_0),\quad u=\chi(s),\quad G(s)=F(u,W_1).
\]

Let ell,h be valid incoming lower and upper records, so
`0<=ell<=F(U0,W0)<=h<=1`. On the productive
interval, s>h and G<ell; in particular ell<=s. The transition maps
H_W(s)=F(chi(s),W) are increasing concave and have H_W'>=1, by the
first two conditions in (1). Therefore

\[
 C(s)=\int_{W_0}^{W_1}\min\{\ell,H_W(s)\}\,dW
\]

is concave, and G''<=0, G'>=1.

At fixed U let lambda(W)=A_U/A. The logarithmic condition makes
lambda nonincreasing in W. The boxed condition gives

\[
 A_W\ge-B\lambda(W)\ge-B\lambda(W_0).
\]

Integrate from W0 to W1, using integral B=s-G and A(U,W0)>0:

\[
 G'-1\ge -\frac{A_U(U,W_0)}{A(U,W_0)^2}(s-G)
              =(s-G)\frac{\chi''}{\chi'}.             \tag{2}
\]

If chi''>0, ell<=s implies
(ell-G)chi''<=chi'(G'-1). If chi''<=0, the left side is already
nonpositive whereas the right side is nonnegative. Thus this same
bound holds in both cases.

After removal of the constant twice-duration term, the exact twice-cost
formula from the curved exchange has derivative

\[
 S'=(\ell-G)\chi'+C'+(U_1-\chi)(G'-1)
                         +U_1-(W_1-W_0)-v(s),
\]

where v(s) is the clipped inverse of the final horizontal field edge.
Transport makes v nondecreasing. Differentiating gives

\[
 \begin{aligned}
 S''={}&(\ell-G)\chi''+C''+(U_1-\chi)G''
                              +\chi'(1-2G')-v'\\
 \le{}&-\chi'G'-v'\le0.                             \tag{3}
 \end{aligned}
\]

The final survivor records are (G(s),1-max(s,F_exit)); both are
concave in s. Every fixed bounded physical future is increasing and
concave in those two records. Therefore the complete objective still
has a minimizing productive-interval endpoint. The already proved
unproductive endpoint moves and physical clipping apply unchanged.
This removes RLR and leaves at most LRL in one phase. The same
first-RLR argument applies to a whole positive prefront first-exit
problem; it does not require an abstract outer certificate itself
to be concave when the actual physical suffix is retained during
the exchange.

The reflected-complement version retains

\[
 -F_W>0,\quad F_{UW}\le0,\quad
 (\log(-F_W))_{UW}\le0,
 \quad -F_U F_{WW}+F_W F_{UW}\ge0,                    \tag{4}
\]

and removes LRL instead. In particular (4) includes an outward-saturated
field F=K(W) wherever K is strictly decreasing, without requiring K
to be concave. Flat portions have no productive record update and
are handled directly: the middle right leg changes no field value.
Thus an arbitrary monotone outward trace has the same direct reduction,
without an inverse on its flat portions.

## 3. Stationary log-convex densities and the power cusp

For F(t,x)=psi(x) on a positive stationary phase, let rho=psi'>0.
If rho is nonincreasing and log-convex, then A=B=rho/2,
A_W=-rho'/4>=0, (log A)_UW=-(log rho)''/4<=0, and the last
condition in (1) holds with equality. Thus this genuinely enlarges
the earlier horizontal-convex class.

For psi(x)=1/2+x^p/2, 0<p<1, the cancellation can also be seen
explicitly. Put d=(W1-W0)/2, x=(u-W0)/2, r=(x-d)/x on a physical
productive interval. Then

\[
 G'=r^{p-1},\qquad
 (s-G)\frac{\chi''}{\chi'}
       =\frac{1-p}{p}(1-r^p)\le r^{p-1}-1.
\]

The inequality follows by integrating v^(p-1)<=v^(p-2) from r to 1.
All transition maps are concave even though chi is convex. Physical
center limits use the continuous field and lower semicontinuity,
not an assumed finite derivative at zero.

Apply this to the atom-free front-one law in Section 6 of
[the free-start comparison](GLOBAL_FREE_START_ZENO_COUNTEREXAMPLE.md):
choose a fair sign and initial radius with CDF r^p; each radius stays
stationary until t+r=1, then moves outward at unit speed and sticks
at its endpoint. Its positive prefront field is exactly this stationary
power profile, so any positive-start
response has a prefix of at most three unit runs to its first center,
endpoint, or incoming front. The reflected case treats negative starts.

That note proves S_p<Q_p, so a globally attaining free-start response
does not start at the center. Compact attainment uses the already
proved common completion horizon four. If its nonzero initial
radius is a, its first-center upper survivor record is at most
(1-a^p)/2, regardless of the prefix exchange. The positive-gap
center theorem therefore supplies a finite optimal continuation.
In fact every productive balanced return has height at least a,
because Princess radii are nondecreasing. The other first-exit
branches have the exact finite incoming-front or endpoint terminal.

Consequently this particular atom-free cusp has an attained finite-
turn global free-start optimum, although its centered optimum has
infinitely many initial turns. No equilibrium or general continuous-
law finite-response statement follows from this example.

## 4. The enlarged whole-inner criterion is still excluded at front two

In this section F is the globally legal signed CDF of a symmetric ordered
Princess law, with continuous interior traces and the actual endpoint
capture convention. In particular reflection gives F(U,W)=1-F(W,U).
Suppose (1) holds throughout 0<=W<U<=C, 1<C<=2, with strict A>0
in the interior and continuous center trace F(W,W)=1/2. No front
completion assumption is used in this section.

For an interior rank s>1/2, invert U=chi(s,W). Then

\[
 \chi_W=B/A,\qquad
 \partial_s\chi_W=-\frac{B A_U+A A_W}{A^3}\le0.
\]

On a small W interval where that rank is available, compare its
derivative with every lower rank s0>1/2 and integrate. As s0 decreases
to 1/2, continuous strict horizontal increase gives chi(s0,W)->W.
Hence chi(s,W1)-chi(s,W0)<=W1-W0. It follows that chi_W<=1,
or A>=B, equivalently F_t>=0 throughout the inner region. This
argument does not assume a common finite derivative trace at the
center. Central vacuum or other degenerate phase boundaries must
be treated separately; they are not silently included in the strict
horizontal-increase hypothesis.

Put d=C-1, a=1-d, and k=F(1,a)>=1/2. For a<=w<=1 the equal-radius
points (U,W)=(1,w) and (2-w,1) are joined by an increasing-time
segment wholly inside the inner region. Thus
F(2-w,1)>=F(1,w). Transport also gives F(U,1)>=k for U>=C.

Split the fast endpoint sweep
E=(1/2)integral[-1,3]F(1,W)dW into its initial interval [-1,0],
the unpaired positive interval [0,a], the paired intervals [a,1]
and [1,C], and its negative tail [C,3]. Reflection and the preceding
comparison give

\[
 E\le1+\frac{(2-d)(1-k)}2
       \le\frac32-\frac{C-1}{4}.                       \tag{5}
\]

In particular C=2 gives E<=5/4. For any certified game lower L,
a whole-inner application is excluded whenever
C>1+4(3/2-L). At C=21/16 the upper is 91/64=1.421875,
strictly below the [certified unrestricted lower](NORMALIZED_GLOBAL_BOUND_CERTIFICATES.md)
1.4222581340234375. Thus a competitive field cannot retain these
whole-inner hypotheses through U=21/16. The broadened curvature
removes the old horizontal-convexity requirement, but does not yield
a competitive whole-front-two phase.

## 5. Precise phase-attachment limits

With physical Princess velocity v=-F_t/F_x, the boxed condition in
(1) is (partial_t+partial_x)v<=0; its reflected counterpart is
(partial_t-partial_x)v>=0. These are velocity conditions along the
two Monster characteristics, rather than convexity of the CDF itself.

If a reflected phase adjoins a lower-W interface on which F_U=0,
its condition F_UW<=0 and transport force F_U to remain zero for
higher W inside that same phase. It cannot create a genuinely active
inner phase from a fully outward-saturated lower-W interface. On the
other hand, a field already of the form K(W) satisfies the reflected
reduction regardless of its convex endpoint trace, with flat portions
handled as above. Thus the earlier endpoint-trace
concavity obstruction applied only to the stronger reflected
condition, not to (4).

These conditions do not supply an equilibrium-sufficient finite phase
cover or justify replacing an arbitrary field by this class. A proposed
interface must separately control re-entry and preserve the physical
continuation with both records. The finite global cusp corollary above
uses its actual single stationary prefront phase, the exact incoming-front
terminal, and the proved positive-gap center continuation; it makes no
unverified interface assumption.
