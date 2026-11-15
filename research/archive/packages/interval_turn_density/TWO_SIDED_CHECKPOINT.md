# Two-sided response checkpoint: what is established and what remains

**No actual global matching candidate has been constructed.** The work in
this package supplies response reductions, exact capture identities, a
local analytic endpoint model, and concrete failed attachment tests. None
of the numerical objectives or small local residuals closes the
unrestricted Princess--Monster game.

## Global response assumptions

The two-sided late-sheet response theorem in
`research/10-turn-density/TWO_SIDED_LATE_RESPONSE.md` retains the separated
negative early/late law and adds a positive-M2 late sheet. Its hypotheses
must all be checked on a proposed law:

* f, p=f+g_total, and k have nonnegative nondecreasing versions and finite
  integrals. The endpoint densities may be unbounded, with the compact
  start-support assumptions of Section 9 of `SEPARATED_SHEETS_RESPONSE.md`.
* The negative start bands remain below their early turn band. The early
  density, negative late density, and line residual h0 have the prescribed
  signs; the negative late exit score Gamma has the stated monotonicity.
* The positive sheet has legal cap `1<v_plus(z)<=2-z`, the explicitly
  constructed nonnegative density j, and nonnegative line residual
  `g0=g_total-integral j`.
* Positive M2 mass is included in g_total when applying the prefix
  monotonicity assumption. Its low-initial alpha price J_a must be retained.
  J_a is nonnegative and nonincreasing in turn s, and legality gives its
  support bound `s<=2-a`. Those facts are what preserve the one-exit suffix
  comparison; simply discarding J_a would prove a different statement.
* The law is normalized. Boundary scalar values describe legal epsilon
  limits in the upper response theorem. They do not authorize replacing a
  continuous lower layer by an atom at U=1, c=1, or an initial endpoint.

For fixed a,c,y, the positive-sheet feature correction is independent of
the optimized prefix. Before U=1 its total negative-threshold price is
still g_total. After U=1 the alpha support bound and monotonicity above
give the same endpoint comparison. This explains why the implemented
four-scalar wrapper is valid under these hypotheses.

## Verification completed

`verify_positive_sheet.py` passes **4,284 exact Fraction** corridor and
envelope checks. `positive_sheet_oracle.py` separately checks its feature
correction against actual first segment intersections of five legal
epsilon-path families. They include starts below, inside, and above the
positive sheet band, and both signs of the suffix exit. The largest
extrapolated discrepancy was **5.21e-17**.

`verify_curved_outgoing_layer.py` passes **570 exact Fraction** identities
for genuinely curved low prefixes mixed with ordinary high paths. The
fixtures include exact first-touch U plateaus and exact V cutoffs. For a
low path beginning below z and completing its incoming prefix at U<1 on
the final outgoing V=c>=0 line, its correction is

    Omega_q(z)=[c-V_first,q(z)]_+
                  +1_(z<=c)[z+2-phi_first,q(z)].

Only the designated low paths enter Omega; the ordinary high incoming
mass is already accounted for in the terminal integral identity. An
ordinary center-waiting low layer gives `Omega=2C+integral_z^1 C`.
A curved layer can remain nonzero above c_max because its final prefix
U-value can exceed c. This is a real additional state/frontier to match.

The analytic endpoint H basis and local Volterra model have the separate
verification described in the README. No Lean compilation or CI was run.

## Actual outer-density splice test

`splice_endpoint_tail.py` uses the old outer f,g,k,ell primitives and the
analytic tail, with coefficients separated linearly into leading-amplitude
and endpoint-mass columns. The f/ell matched splice has

    leading amplitude             0.050154988719290375
    ell cutoff deficit            7.423612986603471e-6
    f/g cutoff deficit            0.011208199980463887
    tentative normalization       1.0437809530591726

The f join is continuous, p has an upward join of about 0.000317, and g is
positive on the tail probes. The alternative p-matched splice has a small
downward f join and fails the f monotonicity requirement. These tests do
not certify all recomputed negative-M2 residual densities; they are the
full-primitives stationarity diagnostic requested before a global solve.

At the proposed lower-layer entry

    a=.991696693624, c=-.585131232,

optimizing the incoming parameter gives `1-u=2.927704e-6` and Ku=0, but
the normalized derivatives are

    4Ka=+1.9680537,  4Kc=+0.0568650.

The unchanged outer terminal ell plateau is therefore incompatible with
that active path. The necessary unnormalized ell(a) is about .12 rather
than the seed's .3785. This is an outer matching failure, not a rejection
of the singular endpoint asymptotics.

`suffix_switch_splice.py` evaluates a genuine extra suffix ending at
y=.625. At the supplied collision `a=.99013684913`, `c=-.54648347435`,
the four-score gain is .06730645 in the diagnostic normalization. At the
supplied entry it is .06422444. The exact identity here is

    4Delta=(.625-c) Fbar(a)-integral_0^(-c)(1-x)f(x)dx.

Both the negative sheet start band and the early turn band lie above
the affected thresholds, and ell vanishes below .625. Thus these gains
expose a genuine missing suffix-indifference condition in the attachment.
They are not a new game-value interval.

## Reconstructing outer prices instead of holding ell fixed

`reconstruct_outer_upper.py` solves the exact Ka/Kc Volterra reduction
on the supplied no-C history joined to the first C>0 layer. Its frozen
input is `outer_lower_input.json`; this input is a numerical lower
experiment, not a certified lower strategy.

The resulting ell is positive and increasing on probes. On the high
initial range a=.9901364 to .9916967 it ranges from .118378 to .120946.
The old terminal k value .369145 at .9375 therefore cannot be retained
if k=ell above the old negative-start band.

The remaining Ku condition still fails. At layer entry the reconstructed
ell(u)=.416618, while Ku requires .447513. At layer exit the corresponding
numbers are .168663 and .417390. The unnormalized four-score Ku residual
grows from .01256 to .11035. A positive monotone outer ell can therefore
be reconstructed, but p and the lower geometry must be solved jointly.

## What the two-sided LP smoke run does and does not resolve

`discover_two_sided.py` performed one structural plumbing test, retaining
the existing density bins and adding positive starts [.5,.625] with cap
17/16. Its negative-c/positive-y response-dual path still has

    a=.984374994, c=-.500000001, y=.625,
    response multiplier .00357742.

That path crosses a negative threshold after U=1 only for `z<-c`, so
the test sheet's start band misses its extra segment except a vanishing
boundary sliver. The turn cap additionally needs crossing ranks with
initial a<=15/16; the displayed response does not provide them. Thus the
stored response dual does not supply the required positive-sheet turn
flux. Structural inequality/equality multiplier masses remain about
.00334555 and .01568476. It is not a matching princess law, and its
floating objective is not a certified game bound.

## Remaining coupled conditions

A successful next solve must select the positive-sheet start interval
from the actual negative extra branch, with b below its crossed start
thresholds, and match its full turn support to the responding ranks.
Where low-rank postflux vanishes, the necessary positive-sheet field is

    (s+6+z) R_s(s,-z)+2R(s,-z)=4+A(z).

The upper alpha-reward cap requires the relevant incoming crossings to
occur by U=2-a. The row mass, legal turn cap, initial support, and endpoint
traces must satisfy both restrictions. The earlier missing extra mass
about .0175 cannot simply be placed at the old a≈.984 response: the
inverse-square capacity suggests some earlier initial positions near
.946 or a changed row-mass geometry.

The unknown global p must satisfy Ku together with the already eliminated
Ka/Kc equations, the continuous suffix-switch value condition, and the
low outgoing branch's equations. The f-activation boundary, end of the
ordinary negative branch, and extra branch need not coincide. The
negative-V postfield also changes the positive f/g first-integral match;
using the ordinary no-extra first integral there would be incorrect.

Finally, the reconstructed monster densities must satisfy every residual
and monotonicity condition, and the lower field must pass a global
all-monster verification. Curved high-c prefixes do not automatically
have post-return center saturation. These are unresolved obligations;
the upper response theorem and local attachment computations do not
replace them.
