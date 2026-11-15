# A free suffix strip excludes the present M1/M2 support class

## 1. Statement

This note proves an exclusion of an entire monster-law class, rather than
of one selected family of princess responses. The proof applies to arbitrary
admissible princess paths. It does not determine the unrestricted game value.

Use the reflected M1 and M2 pairs defined in
`../08-continuum/CHARACTERISTIC_RESPONSE.md`. Consider a symmetric monster
law whose unreflected parameter measures are

    mu_1 = w0 delta_(-1) + nu on [0,1],
    mu_2 = an arbitrary finite nonnegative measure on [-1,1],

with total mass one. Suppose, for some `0 <= beta < 1`,

    nu([0,beta))=0,
    nu((a,1))>0 for every a<1.                            (H)

The first condition is vacuous when beta=0, which is enough for the main
exclusion theorem. No density, monotonicity, or atomlessness assumption
is needed. Countably
many positive M1 atoms accumulating at one are included, as is an
additional atom at one. The second condition requires mass below one in
every top interval, so an isolated top atom does not suffice. The monotone
densities previously proposed in the continuum calculation are a special
case whenever every top density tail has positive mass. A positive support
gap improves the numerical obstruction but is not required for exclusion.

Write M for this law and

    S = sup_p E_M T(M,p).

Every path in the support captures by time four, so S is finite.

**Theorem.** If `S>7/5`, a finite mixture of M and explicit additional
symmetric monster pairs has response ceiling strictly less than S.
Consequently, under (H), M is not an optimal unrestricted monster law
whenever the unrestricted game has a known lower guarantee greater than
`7/5`.

The extra pairs can be drawn from the following two countable families,
with `eta=1/(j+2)`, `j=1,2,...`:

* F_eta is the reflected pair M1(1-eta).
* L_eta is the reflected pair M1(-1+eta).

Thus the strict improvement can be made entirely inside the full M1/M2
family by adding negative interior M1 starts. It is the one-sided M1
support restriction, not the use of two named monster families alone,
that is excluded.

The theorem supplies a strict improvement by a finite mixture. It does not
give a bound on the required number of pairs or compute the improving
weights. Its purpose is to exclude a candidate class that cannot contain
a complete saddle certificate.

## 2. Nonnegative princess paths suffice for all laws used here

For any monster path m and any princess path p, the pairwise comparison

    T(m,p)+T(-m,p) <= T(m,abs(p))+T(-m,abs(p))             (1)

holds. One proof is given in the characteristic-response note. The earlier
capture in each pair is the first radial contact `abs(m)=abs(p)`. After
that contact, continuity forces the other original capture no later than
the other capture of `abs(p)`.

Every monster law in this note is symmetric. Thus replacing p by abs(p)
weakly increases its payoff against all these laws simultaneously. It
suffices to consider paths in `[0,1]`. For such a path put

    a=p(0),  d=p(1),
    U(t)=t+p(t),  V(t)=t-p(t),
    A(z)=inf{t:U(t)>=z},  B(z)=inf{t:V(t)>=z}.

The characteristic coordinates are continuous and nondecreasing. All
inverses below are first inverses, including at plateaus.

## 3. A quantitative free-strip improvement

Choose `0<eta<delta<1`, and suppose

    a <= 1-delta,    d >= delta,
    A(1+eta) >= (1+eta-beta)/2.                           (2)

Define

    kappa(delta,eta)
      = delta/8 * nu((1-delta,1-eta)).                    (3)

**Lemma.** There is an admissible nonnegative princess path q with

    E_M T(M,q) >= E_M T(M,p) + kappa(delta,eta).           (4)

### Construction

Let `u0=1+eta`, `t0=A(u0)`, and `v0=V(t0)`. The last inequality in
(2) gives `v0>=-beta`. Since `U(1)=1+d>=1+delta>u0`,

    t0<=1,    v0<=V(1)=1-d<=1-delta.

Set `r=1-delta/2`, so `v0<r<1`, and let `tr=B(r)`. The preceding
inequality gives `tr>1`. Write `ur=U(tr)`.

Follow p until `(U,V)=(u0,v0)`. Replace its characteristic path up to
`(ur,r)` by

    (u0,v0) -> (u0,r) -> (ur,r),

and then follow p again. These are one inward and one outward unit-speed
leg. The old and new paths have the same entrance and exit times because
`U+V=2t`. Both new legs stay in `0<=U-V<=2`: increasing V from v0
to r cannot violate the upper spatial boundary, and the second leg ends
at an original legal point. Also `r<1<u0`, so neither leg crosses zero.
This defines q.

### Capture comparison

The change occurs strictly after the path has crossed `U=1`. Hence it
preserves the M2 cutoff, all A thresholds at or below one, and all B
thresholds at or above one. The early M2 B thresholds have already been
crossed before this change. The exact characteristic formulas therefore
show that **every M2 capture is unchanged**, including atoms, cutoff
equalities, and plateau cases. The endpoint M1 pair uses A(1) and B(1),
so it is unchanged as well.

Among positive M1 parameters, reflected captures use `B(2-x)` with
threshold at least one and are unchanged. An unreflected M1 with `x<a`
uses `B(-x)`. Such a B inverse can become earlier only when

    v0 < -x <= r.

Since `v0>=-beta`, this requires `x<beta` strictly. The measure nu gives
this set zero mass. An atom at x=beta is unchanged: if v0=-beta, its B
threshold has already been crossed at the entrance to the replacement.
Initial coincidences are unchanged as well.

Every affected M1 A inverse is delayed. In particular, for
`1+eta<z<=1+delta`, its original first-inverse V coordinate is at most
`V(1)<=1-delta`, whereas the new coordinate is r. Therefore its capture
is delayed by at least `delta/4`.

Restricting to positive M1 parameters `1-delta<x<1-eta` ensures x>a
and puts their A thresholds strictly above u0. Integrating their delay and
including the probability one half of choosing the unreflected path gives
the lower bound (3). The open interval correctly excludes both an initial
coincidence at x=a and a first-inverse coincidence at U=u0, even if either
parameter has positive mass. This proves (4).

For each fixed delta, hypothesis (H) implies `kappa(delta,eta)>0` for
all sufficiently small positive eta. This follows by letting eta tend
to zero in the increasing interval `(1-delta,1-eta)` in (3).

## 4. Stability for arbitrary near-best response laws

Let lambda be any probability law on nonnegative princess paths, and put

    epsilon = S - E_lambda E_M T(M,p) >= 0.

Write `lambda^sym` for the law obtained by choosing the sign of a sampled
path fairly. Against every symmetric monster law used here, lambda and
`lambda^sym` have the same payoff.

Let R_delta be the event

    a<=1-delta and d>=delta.

Call a path in R_delta bad if it also satisfies the last inequality in
(2). The lemma implies that its individual deficit from S is at least
kappa. Consequently, whenever `kappa>0`,

    Pr_lambda(bad) <= epsilon/kappa.                     (5)

This conclusion concerns every admissible path, not only the extreme
representatives in the conditional response reduction. It is the step
that prevents unused equality corridors from repairing the old candidate.

## 5. Two explicit attacking inequalities

### The near-endpoint M1 pair

For F_eta, if `a<1-eta`, the exact pair payoff is

    [A(1+eta)+B(1+eta)]/2.

Since `p>=0` and `p<=1`, respectively,

    A(1+eta)<=1+eta,    B(1+eta)<=2+eta.

Thus this payoff is at most `3/2+eta`. If `a>=1-eta`, the
unreflected capture is at most eta, including an initial coincidence,
and the reflected capture is at most `2+eta`. The pair payoff is then
at most `1+eta`.

On a non-bad path in R_delta, with `eta<delta`, the stronger bound from
(2) failing is

    F_eta(p) <= (5-beta+3eta)/4.

Combining these bounds and (5) gives

    E_lambda F_eta
      <= 3/2+eta
         - (1/2) Pr(a>=1-eta)
         - ((1+beta)/4) Pr(R_delta)
         + ((1+beta)/4) epsilon/kappa.                   (6)

The endpoint-start event and R_delta are disjoint because eta<delta.

### The near-endpoint negative M1 pair

Put `z=1-zeta`. The exact pair payoff of L_zeta is

    [B(z)+A(z)]/2         if a<z,
    B(z)/2                if a=z,
    [B(z)+B(2+z)]/2       if a>z.                         (7a)

The middle case retains the reflected initial coincidence. The inverse
bounds give L_zeta<=3 whenever a>=z. If a<z, then A(z)<=z. When
also d<=zeta, one has `V(1)=1-d>=z`, so B(z)<=1 and L_zeta<=1.
Otherwise B(z)<=1+z and L_zeta<=3/2. Hence, writing E_zeta for
`{a>=1-zeta}`,

    L_zeta(p)
      <= 1 + 2 1_E_zeta
           + (1/2) 1_(a<1-zeta and d>zeta).

There is an additional gain on a non-bad path in R_delta when
`zeta<delta`. Here a<1-zeta, and (7a) together with stability gives

    L_zeta(p)
      = [B(1-zeta)+A(1-zeta)]/2
      <= [2-zeta+A(1+eta)]/2
      <= (5-beta+eta-2zeta)/4.

The previous pointwise bound on this event was 3/2. Set
`c_eta=(1+beta-eta)/4>0`. Subtracting at least this improvement and
using (5) gives

    E_lambda L_zeta
      <= 1 + 2 Pr(a>=1-zeta)
           + (1/2) Pr(a<1-zeta and d>zeta)
           - c_eta Pr(R_delta) + c_eta epsilon/kappa.    (7)

The joint event in the positive term must be retained. It excludes the
endpoint-start cluster instead of counting that cluster a second time.

## 6. The 7/5 obstruction, with the limits in the required order

Consider a sequence lambda_n with

    E_lambda_n E_M T -> S.

Pass to a subsequence along which the joint distributions of `(a,d)`
converge weakly on the compact square `[0,1]^2` to a probability measure
rho. Write

    A0 = rho(a=1),
    R0 = rho(a<1 and d>0).

Fix delta, eta, and zeta first, with `zeta<delta` and eta sufficiently
small that `eta<delta` and kappa is positive. In (6) and (7) the deficit terms tend to zero
as n tends to infinity. Portmanteau gives the following bounds without
requiring atom-free thresholds:

    liminf Pr_n(a>=1-eta) >= rho(a>1-eta),
    liminf Pr_n(R_delta) >= rho(a<1-delta and d>delta),
    limsup Pr_n(a>=1-zeta) <= rho(a>=1-zeta),
    limsup Pr_n(a<1-zeta and d>zeta)
      <= rho(a<=1-zeta and d>=zeta).

Use the monster mixture `4/5 F_eta + 1/5 L_zeta`. Equations (6) and
(7), followed by `n->infinity`, give an upper bound for its limiting
payoff. Now let eta and zeta decrease to zero, keeping delta fixed.
Finally let delta decrease to zero. The resulting upper bound is

    7/5 + (1/10) R0 - ((1+beta)/4) R0
      = 7/5 - (3/20+beta/4) R0
      <= 7/5.                                           (8)

In particular,

    limsup_n inf_m E_(lambda_n^sym) T(m,p) <= 7/5.        (9)

For (9), first choose a subsequence realizing its left-hand limsup and
then take the weakly convergent marginal subsequence just used.

The order of limits is essential. The monster parameters eta and zeta
remain fixed while the princess laws converge. Therefore M1(1-eta) lies
inside any endpoint-start cluster sufficiently far along the sequence,
and the negative M1 comparison detects any cluster collapsing to zero
at time one. Only after this comparison are the monster parameters reduced.
Taking either monster parameter to zero before the princess concentration
scale would not establish (8).

The same argument proves a slightly stronger statement useful below:
if eta_j is any fixed positive sequence decreasing to zero, there cannot
be laws lambda_n whose M payoff tends to S and whose payoff against
every fixed F_eta_j and L_eta_j tends to a lower bound greater than 7/5.
The Portmanteau argument does not require choosing eta_j at continuity
points of rho.

## 7. A strict improvement of the candidate monster law

This step does not assume a minimax theorem for the full path game.
Only finite-dimensional zero-sum duality is needed.

For each N consider the finite list of symmetric monster laws

    M, F_eta_1, L_eta_1, ..., F_eta_N, L_eta_N,

and let W_N be the least response ceiling among their mixed strategies.
The pure choice M gives `W_N<=S`.

Suppose for contradiction that `W_N=S` for every N. Finite-row minimax
then provides a finitely supported princess law lambda_N for which every
listed monster payoff is at least `S-1/N`. To see that no compactness
assumption on the princess path set is hidden here, take the closure of
the convex hull of its bounded payoff vectors in a finite-dimensional
Euclidean space. This is a compact convex set. Separation from an upper
orthant gives the finite-row minimax equality, and finite convex
combinations approximate its maximizing payoff vector to arbitrary
accuracy. Inequality (1) lets these princess paths all be nonnegative.

The M deficit of lambda_N tends to zero. Moreover, each fixed F_eta_j
and L_eta_j has payoff at least `S-1/N` for all N>=j. The stronger
conclusion at the end of Section 6 therefore implies `S<=7/5`, contrary
to the hypothesis.

Thus `W_N<S` for some finite N. The weight simplex is compact and its
response ceiling is the supremum of bounded continuous linear functions
of the weights, hence lower semicontinuous. Its minimum is attained.
The attaining finite mixture is a legal monster law with strictly lower
ceiling than M. This proves the theorem.

## 8. Consequences for the present proof search

The existing exact unrestricted lower guarantee in the repository is

    36290299773897097 / 25600000000000000
      = 1.4175898349178553515625 > 7/5.

Accordingly, an M1/M2 law satisfying (H) cannot be the optimal
unrestricted monster law. The conclusion is not restricted to a sampled
dual, to frozen princess weights, or to the four-parameter extreme
response family. It includes arbitrary prefix and suffix equality cases,
because the free-strip improvement was proved for arbitrary paths.

The obstruction comes from the empty beta-threshold strip `[-beta,1)`
after U=1. The old candidate can delay M1 captures at no beta cost by
pushing surviving paths toward the center, and near-endpoint M1 pairs of
both parameter signs exploit the forced response alternatives. A complete candidate must escape at
least one hypothesis of this theorem. Possible changes include a positive
M1 support bounded away from one, additional interior negative M1
parameters, or monster turning characteristics beyond the common line
`U=1`. This note does not assert which change produces an equilibrium.

