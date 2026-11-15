# A whole-law test of diffuse deadline corridors

Date: 2026-11-11.

**The unrestricted game is not solved.** This note constructs and then
excludes one natural continuum lower candidate in its entirety. It does not
add another local turn case or change the rigorous game interval. In
particular, it does not prove that every deadline-corridor construction or
every finite monster support fails.

## 1. The candidate and the conclusion

The exact coarse fixed-bank minimax certificate has value

    c_bank = 219625051/152700512 = 1.4382731801187412...

and nine positive-side response components. The single extreme path used
to realize each component concentrates initial mass and fails the exact
epsilon-germ response test in `GERM_RESPONSE.md`. The natural global repair
tested here spreads each component over its whole available deadline
corridor. It uses a uniform parameter lambda in (0,1), followed by the
usual independent reflection with probability one half.

This removes the initial atoms. The starting intervals of the nine
components, in their saved order, are

    (3/4,1), (3/4,1), (3/4,1), (3/4,1),
    (1/2,3/4), (1/2,3/4), (1/4,1/2), (1/4,1/2), (0,1/4).

Nevertheless, the single legal monster which starts at -15/16, runs right
to +1, and then runs left to -1 defeats the entire approaching family.
More strongly, it defeats **every legal coupling of the same time
marginals**, including the ordered quantile coupling:

    limsup_(delta -> 0+) E T
       <= 34192713983279/29347816802304
       = 1.165085437653224... < 7/6 < c_bank.                 (1)

The quantifier over couplings in (1) is uniform: the coupling may depend on
delta. Thus quantile uncrossing cannot repair this particular family.

This is not a new upper bound for the game. It is an upper bound on the
payoff of the specified proposed lower family against one attacking
monster. The failure does not establish which broader support geometry an
equilibrium requires. In particular, initial diffusion alone is not enough
for this candidate; no universal later-coalescence obstruction is asserted.

## 2. Constructing the continuum law

Use only the positive-weight monster pairs in
`packages/interval_global_closure/global_minimax_grid4_exact.json`.
For each response profile, its lexicographic query values determine a
limiting capture deadline r_i and whether monster i starts below or above
the princess. All these data are rational. A row with r_i=0 imposes no
positive capture requirement and is omitted from the envelope constraints.

For delta>0, put e_i=max(0,r_i-delta). A below-monster has downward
continuation

    l_i(t) = m_i(t)                         for t<=e_i,
             m_i(e_i)-(t-e_i)              for t>=e_i.

An above-monster has the corresponding upward continuation u_i(t).
Set

    L_delta(t)=max(0,max_i l_i(t)),
    U_delta(t)=min(1,min_j u_j(t)).

The lower wall is zero because these profiles have positive-half
representatives. The exact construction checks L_delta<U_delta on the
complete finite envelope arrangement; each difference is affine between
arrangement vertices. The strict corridor property therefore holds for
every time, not only at sampled vertices.

For a uniform random lambda in (0,1), define

    p_(delta,lambda)(t)
      = (1-lambda)L_delta(t)+lambda U_delta(t).               (2)

Both envelopes are 1-Lipschitz, so (2) is a legal 1-Lipschitz path in the
positive half interval. After the supplied common horizon it remains
constant. The active monsters have already completed both endpoint visits
by that horizon. No endpoint-absorption property of (2) is assumed.

Every path in (2) stays strictly on its assigned side of monster i until
e_i. Therefore

    T(m_i,p_(delta,lambda)) >= r_i-delta                      (3)

for every lambda in (0,1). This is the same envelope argument proved in
`research/02-exact-response-reduction/REDUCTION.md`; allowing all lambda
simultaneously gives a continuum of witnesses.

The nine mixing weights are the exact rational weights in the fixed-bank
certificate. The verifier checks the exact weighted deadline equality c_bank
for every positive-weight upper atom. Thus the diffuse law retains a
guarantee c_bank-delta against every atom of that active support. For
delta=1/4096 this lower threshold is

    28107234637/19545665536 = 1.4380290394937412...

The numerical minimum of the analytically integrated active-atom payoffs
is approximately 1.438126. These facts explain why checking only the
active bank would fail to detect the attack in (1).

## 3. Exact integration against a supplied monster

For one noncollapsed corridor, its time-t CDF is

    F_delta(t,x)
       = clamp((x-L_delta(t))/(U_delta(t)-L_delta(t)),0,1).

Along a piecewise-linear supplied monster, subdivide at the union of its
vertices and the envelope vertices. On each resulting time interval the
unclamped CDF is fractional linear:

    (A t+B)/(C t+D),

with rational coefficients. Its derivative has constant sign. The first
capture set in lambda is an interval, so expected capture time is the
integral of

    1 - max_(s<=t) F_delta(s,m(s))
      + min_(s<=t) F_delta(s,m(s)).

Split at the exact crossings of the previous rank records and of zero
and one. Integrating the remaining fractional-linear pieces uses

    integral_a^b (A t+B)/(C t+D) dt
      = A(b-a)/C
        + (BC-AD)/C^2 log((Cb+D)/(Ca+D)),                    (4)

when C is nonzero; the constant-denominator case is an ordinary quadratic
primitive. Every accepted denominator is strictly positive on its
integration interval.

There is a second, independent implementation. Subdivide lambda at every
contact with a vertex of the common time arrangement. On each open rank
interval, the first capture segment is fixed and its capture time is a
fractional-linear function of lambda. Integrating that function gives the
same rational-plus-log form. Contact at a vertex for a whole rank interval
is retained as a constant capture-time contribution. This second method
also handles collapsed delta=0 corridors directly.

The code sums the expected times of the physical mixture of corridors.
It does not incorrectly substitute the CDF of that mixture into a single
running-record formula. Components can cross; their ordered quantile
coupling is a distinct law. Section 5 below controls that coupling as well.

## 4. Exact attack arithmetic

Write m for the monster starting at -15/16 and going right first. Its
first endpoint time is H=31/16 and its opposite endpoint time is 63/16.

For delta=1/4096, direct integration of the physical mixture gives

    E T(m,P_delta) = 1.0253772853717871456...

The decimal is discovery output. The exclusion itself uses only rational
inequalities. For every r>0,

    1-1/r <= log(r) <= r-1.

Apply the appropriate bound according to the sign of each coefficient
in the exact expression (4). This proves

    E T(m,P_delta)
      <= 38988395686171360146464288935247
         /37526228444123945289355351818240
      = 1.0389638741400449... .                              (5)

For the actual limiting-envelope law P_0, the corresponding exact
rational-plus-log expression has decimal value

    E T(m,P_0) = 1.0254466061388931454...

and the same elementary logarithm inequalities prove

    E T(m,P_0) <= 30459425896751/29347816802304.              (6)

The complete rational coefficients and logarithm arguments for (5) and
(6) are in `uniform_corridor_exclusion.json`. There is no reliance on
floating-point signs in either rational bound.

**We do not identify E T(m,P_0) with lim E T(m,P_delta).** First-capture
time can jump at collapsed limiting corridors. The argument below needs
only convergence of the first-sweep CDF integral and uses (6) as an upper
bound on that integral.

## 5. One global bound covers every coupling

Let F_delta now denote the aggregate signed time-marginal CDF of the
nine-component symmetric law. Its initial CDF at a=-15/16 is independent
of sufficiently small positive delta and equals

    f_0 = 1214049/19087564 = 0.0636041875223051... .          (7)

The initial marginal is atomless. During the unit-right first leg,
every legal princess's displacement relative to the monster is
nonincreasing. A princess initially below a cannot catch the monster
from behind. Consequently, for every legal coupling with those marginals,
the captured mass by time t<=H is

    F_delta(t,a+t)-f_0.

The expected elapsed capture time through H is therefore the same for
all couplings:

    B_delta = integral_0^H [1-F_delta(t,a+t)+f_0] dt.          (8)

At +1, the surviving mass is f_0. The direct return sweep captures all
of it within two more time units. Hence every such coupling satisfies

    E T <= B_delta+2 f_0.                                  (9)

For the physical mixture, its total expected capture time is at least
B_delta. Thus (5) and (7) already prove, at delta=1/4096, the exact
all-couplings bound

    E T <= 43762046228101197987961147886927
           /37526228444123945289355351818240 < 7/6.          (10)

### Passing to the whole approaching family

The unit speed bound gives

    ||L_delta-L_0||_infinity <= 2 delta,
    ||U_delta-U_0||_infinity <= 2 delta.

At a time where the limiting corridor has positive width, its CDF at the
monster converges immediately. At a collapsed limiting corridor, the CDF
still converges whenever the monster is not at its collapsed position.
There are finitely many linear pieces. It is enough to exclude a
positive-length coincidence between the first monster leg and a collapsed
limiting envelope, for both reflection choices.

The verifier enumerates all **74 collapsed envelope segments** meeting
the first-sweep time range and checks that neither reflected monster
coincides with one on an interval. The remaining possible coincidence
times form a finite set. Thus the aggregate CDF converges almost everywhere
on [0,H]. It is bounded between zero and one, so dominated convergence
in (8) gives B_delta -> B_0.

The actual physical limiting law has total expected capture time at
least B_0. Combining (6), (7), and (9) therefore proves

    limsup E T
      <= E T(m,P_0)+2 f_0
      <= 34192713983279/29347816802304 < 7/6,

which is (1). This proof neither assumes continuity of the full capture
functional nor takes a limit of the second-leg capture times.

## 6. Reproduction and stopping decision

Run

```sh
python packages/interval_global_closure/verify_corridor_law.py
```

The verifier checks the exact active deadline equalities, the rational
logarithm upper bounds, the initial mass (7), the 74 limiting collapsed
segments, and the all-couplings bounds. Two independent integration
implementations agree to 45 decimal places; a separate nontrivial
fractional-linear fixture has the known value
`1/4+(3/2)log(3/2)`. A further 1,152 exact physical midpoint captures
satisfy the uniform quantile-discrepancy error bound. Those numerical
cross-checks validate the implementation; the final exclusion uses the
displayed rational inequalities.

This branch is stopped. Adjusting a small set of initial atoms, using a
fixed positive epsilon, or simply replacing each extreme response by a
uniform envelope blend does not produce the matching lower strategy.
An optimal-face query profile is not a certificate that its chosen
physical realization is an equilibrium. The unrestricted value,
equilibrium-specific finite reduction, and matching certificate remain
open.
