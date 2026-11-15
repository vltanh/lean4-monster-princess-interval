# A global finite-vertex Bellman certificate

This criterion covers the free monster start, arbitrary initial same-half
motion, center excursions, curved ordered princess paths, and capture
atoms in one verification problem. It does not require a monster turn
bound or an ordinary-wave initial-prefix reduction.

The certificate is not yet instantiated. No princess CDF and verification
potential satisfying its initial lower bound at a matching unrestricted
upper value have been supplied. The theorem below is a sufficient global
verification scheme, not an equilibrium or a new value bound.

## 1. Full signed CDF and capture records

Let q be uniform on (0,1), and let p_q(t) in [-1,1] be ordered
nondecreasingly in q and 1-Lipschitz in time. Assume

    p_q(t) in {-1,+1} for every t>=2, almost surely.       (1)

Positive mass may arrive at its endpoint exactly at time two. Reflection
symmetry is permitted but is not needed in the theorem.

Keep the two CDF traces distinct:

    F^-(t,x)=Pr(p_q(t)<x),
    F^+(t,x)=Pr(p_q(t)<=x).

At a monster state (t,x), let l and h be the lower and upper captured
quantile records. The feasible state domain is

    0<=l<=F^-(t,x)<=F^+(t,x)<=h<=1.                      (2)

Captured ranks form the interval between l and h. The surviving masses
are l below the monster and 1-h above it. For an actual monster path,

    l(t)=inf_{0<=s<=t} F^-(s,m(s)),
    h(t)=sup_{0<=s<=t} F^+(s,m(s)).                     (3)

At time zero, equality is already capture, so the initial records are

    l(0)=F^-(0,x),    h(0)=F^+(0,x).                     (4)

The interval in (4) can have positive mass. Its capture contribution is
zero, not a one-sided limit of a nearby starting position.

## 2. Exact unit-leg actions

For v in {-1,+1}, take a unit-speed leg

    m(s)=x+v(s-t),    t<=s<=e<=2,

remaining inside [-1,1]. Along a rightward leg, both CDF traces are
nondecreasing; along a leftward leg they are nonincreasing. This follows
directly from the princess speed bound. A target strictly behind a
unit-speed ray cannot catch it from behind.

### Rightward leg

Put y=x+e-t. Its updated records and immediate absolute capture
contribution are

    l'=l,    h'=max(h,F^+(e,y)),                         (5)
    G_+(t,x,e;l,h)
      =e*(h'-h)-integral_t^e (F^+(s,x+s-t)-h)_+ ds.       (6)

### Leftward leg

Put y=x-(e-t). Then

    l'=min(l,F^-(e,y)),    h'=h,                         (7)
    G_-(t,x,e;l,h)
      =e*(l-l')-integral_t^e (l-F^-(s,x-s+t))_+ ds.       (8)

These are first-hit layer-cake identities. For example, in (6), the
captured mass by intermediate time s is (F^+(s,m(s))-h)_+. Integrating its
first capture times gives endpoint time times final captured mass minus
the area under that mass process. Formula (8) is the same identity for
the lower ranks.

The traces in (5)-(8) are essential. A rightward leg uses the closed CDF,
and a leftward leg the strict CDF. At +1 the closed trace is one; at -1
the strict trace is zero. A jump at the end of a leg contributes its full
mass times e through the first term. An incoming coincidence interval is
captured at its first equality, not at the end of the interval.

## 3. Exact horizon-two completion

At time two all surviving lower ranks are at -1 and all surviving upper
ranks at +1. For a state (2,x,l,h), define

    E_2(x,l,h)=min(
       l*(3+x)+(1-h)*(5+x),
       (1-h)*(3-x)+l*(5-x)).                            (9)

The first expression visits -1 first; the second visits +1 first. They
are absolute capture-time contributions. Formula (9) applies also when
x is an endpoint, because (2) has already removed the mass captured there
at time two.

For reference, at any later endpoint-only state the corresponding formula
is

    E(t,x,l,h)=min(
       l*(t+x+1)+(1-h)*(t+x+3),
       (1-h)*(t+1-x)+l*(t+3-x)).                         (10)

No no-atom assumption at absorption time two is required here. This is
why the global theorem uses the actual horizon two, even when a
candidate-specific center theorem can terminate at time one.

## 4. Global Bellman theorem

Let Q(t,x,l,h) be a bounded function on (2), for 0<=t<=2. Suppose:

1. For every feasible rightward or leftward unit leg,

       Q(t,x,l,h) <= G_v(t,x,e;l,h)+Q(e,y,l',h').         (B)

2. At the endpoint-absorption horizon,

       Q(2,x,l,h) <= E_2(x,l,h).                         (T)

3. At every free initial position x in [-1,1],

       Q(0,x,F^-(0,x),F^+(0,x)) >= c.                   (I)

**Theorem.** The ordered princess law guarantees c against every
unrestricted 1-Lipschitz monster with a free initial position.

For a finite unit-speed canonical monster, split its last pre-horizon leg
at time two. Sum (B) along the pre-horizon legs. Their G terms are precisely
the contributions of newly captured ranks, with no rank charged twice.
Use (T) for all survivors. Their actual continuation cannot beat (9).
Condition (I) therefore proves the lower bound for every such canonical
monster.

To pass to arbitrary monsters, take n midpoint quantiles of the ordered
law. The capture-order domination theorem supplies a finite canonical
monster whose capture time against each selected path is no greater than
the original monster's time. It moves at unit speed between new captures;
there is no shadowing segment in the constructed path. After time two,
the next new capture is at an endpoint and occurs by time four, and a
direct opposite sweep finishes by time six. If every selected path was
captured earlier, append direct unit-speed visits to both endpoints;
likewise append the opposite endpoint if the last selected capture left
it unvisited. This makes the continuum route complete by six without
delaying any selected capture. Thus its selected capture
times are bounded by the original selected times truncated at six.

For any monster, captured quantile ranks form an interval. Midpoint
quantile discrepancy therefore bounds its truncated payoff error
uniformly by 6/n at horizon six, including atoms and tied captures. Apply
this once to the original monster and once to the canonical one. The
original full payoff is at least c-12/n. Let n tend to infinity.

This proof does not approximate a monster by rapid oscillations and then
assume capture times converge favorably. It uses coordinatewise finite
capture domination and a uniform discrepancy estimate. Center waiting,
slower motion, infinitely many turns, and tangencies are covered by that
argument. The number of canonical legs can grow with n; the certificate
checks each leg through the same inequality (B).

## 5. Joint record concavity

Fix a future monster route from (t,x). Among surviving lower ranks,
first future capture time T_q is nonincreasing in q: a route starting
above two ordered paths cannot meet the lower one without first meeting
the upper one. Among surviving upper ranks, T_q is nondecreasing in q.
Its remaining contribution is therefore

    integral_0^l T_q dq + integral_h^1 T_q dq,

which is jointly concave in (l,h). Its partial slopes satisfy

    partial_l Q >= t,    partial_h Q <= -t.             (11)

The infimum over future routes preserves joint concavity. This suggests
the following sufficient form for a verification potential:

    Q(t,x,l,h)=min_j [a_j(t,x)*l+b_j(t,x)*h+d_j(t,x)],    (12)
    a_j(t,x)>=t,    b_j(t,x)<=-t.

There are finitely many planes on each stated (t,x) region. A complete
certificate must specify their coefficients, region boundaries, and
traces. This note does not assert that a matching potential with finitely
many planes has already been found.

## 6. Finite record vertices suffice

For fixed t,x,e,v, the right side of (B) is jointly concave in the current
records. To see this, take one future affine plane in (12).

On a rightward leg, let f=F^+(e,y). Its h-dependent part, including newly
captured ranks, is

    b*max(h,f)+integral_h^{max(h,f)} kappa_+(q)dq.        (13)

Here kappa_+(q) is the absolute first capture time on that leg. It is
nondecreasing and at most e. Below f, the derivative of (13) is
-kappa_+(h); above f it is b<=-e. Thus the derivative is nonincreasing,
including its downward jump at f. The l part remains affine.

On a leftward leg, let f=F^-(e,y). Its l-dependent part is

    a*min(l,f)+integral_{min(l,f)}^l kappa_-(q)dq.        (14)

Below f its derivative is a>=e; above f it is kappa_-(l)<=e, which is
nonincreasing. This too is concave, with the h part affine. Taking the
minimum over the future affine planes proves joint concavity of the full
right side of (B). The terminal function (9) is already a minimum of two
affine planes with the same slope bounds at time two.

For each fixed (t,x), decompose the feasible record rectangle

    [0,F^-(t,x)] x [F^+(t,x),1]

into the convex polygonal cells where the current Q is affine. It is
enough to check (B) at every vertex of every such cell. On a convex
combination of vertices, the right side is at least the corresponding
combination of its vertex values, while the current Q is exactly that
combination. The same vertex principle applies to (T).

The resulting certificate has finitely many record-vertex families, two
unit directions, and the continuous variables (t,x,e). It does not
quantize the princess law, enumerate capture orders, or guess the number
of initial or later monster turns. Condition (I) is a one-variable exact
initial check. This supplies the global initial-prefix verification that
the center-only potential left open.

### Optional local form

Where the CDF is continuous and differentiable, write F for its common
trace and D_vF=F_t+vF_x. Along a differentiable potential branch, (B) has
the local sufficient form

    Q_t+v Q_x
      +(Q_h+t)*max(D_vF,0)*1_{h=F}
      +(Q_l-t)*min(D_vF,0)*1_{l=F} >= 0,                (15)

for v=-1,+1. All active potential branches and record faces must be
checked, together with their interface conditions. At CDF jumps,
coincidence intervals, or uncertain interface regularity, use the exact
integral actions (5)-(8), rather than replacing first touch by a
derivative limit.

## 7. Phase and trace audit

* **Initial equality:** use the pair (F^-,F^+) in (4). A starting atom
  contributes zero and is removed before any future leg.
* **Rightward capture:** only h advances, and it advances to the closed
  CDF. A new upper atom is captured at its first equality.
* **Leftward capture:** only l retreats, and it retreats to the strict
  CDF. An incoming coincidence plateau is not charged again later.
* **Center atoms:** their full signed CDF interval is retained. No
  assumption that both radial frontiers become equal is made.
* **Endpoint turns:** F^+(t,1)=1 and F^-(t,-1)=0 are used exactly. The
  interior endpoint limit cannot substitute for either value.
* **Slow outward or multiple waves:** they change the line CDF, but not
  its monotonicity under a unit-speed monster. No ordinary-wave phase
  or post-center saturation is invoked.
* **Absorption exactly at time two:** the boundary applies after the
  first-touch update at that time. Positive absorption atoms are allowed.
* **Unrestricted paths:** finite capture-order domination, not a uniform
  turn bound or a favorable singular limit, supplies the transfer.

These points identify what an eventual candidate and potential must
verify. They do not supply missing candidate functions or a matching
constant.

## 8. Exact independent fixtures

Run from the repository root:

```sh
python packages/interval_turn_sheet/verify_signed_bellman.py
```

The verifier performs **1,189 exact Fraction checks**:

| Check | Count |
|---|---:|
| Immediate absolute unit-leg capture contributions | 462 |
| Both signed capture-record updates | 462 |
| Exact endpoint-only completion at time two | 91 |
| Joint record concavity across clipping boundaries | 168 |
| Deliberate atomic first-touch phases | 6 |

Reference payoffs come from the independent continuous running-CDF
capture engine. The fixtures include non-unit-speed continuum waves,
five- and seven-leg laws, stationary endpoint atoms, and entire radial
atoms on incoming coincidence intervals and center waits. A separate
atomic fixture has positive mass absorbed exactly at time two. Strict and
closed traces are computed separately for those atomic paths.

`signed_bellman.py` implements (5)-(10) using exact affine CDF line cells.
The checks audit the action formulas, terminal boundary, and concavity
comparisons. They are Python research checks, not a Lean compilation or
an instantiated proof of the game's value.
