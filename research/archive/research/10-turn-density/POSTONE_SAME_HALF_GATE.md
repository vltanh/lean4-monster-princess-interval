# Continuous same-half continuation after U=1

This theorem removes every additional same-half return after a specified
positive-half prefix reaches U=1. It applies to arbitrary continuous
monster motion with speed at most one; there is no bound on its turn
count. Its hypotheses are explicit CDF gates and a center-continuation
condition. It does not assume the prefix or a one-I response is active.

## 1. Prefix records and the two gates

Let an ordered reflected princess law have continuous radial paths of
speed at most one, absorbed at their signed endpoints by time two.
Consider a monster prefix which has stayed strictly positive and ends
at the positive point

    U=1, V=v, time=(1+v)/2, position=(1-v)/2.

Let L and M be its lower and upper captured radial records. Thus its
surviving positive ranks are `[0,L)` and `(M,1]`, with inclusive first
contact incorporated in the records. Put

    d=1-L,       m=1-M.

For the initial-inward prefix `+a -> V=v -> U=1`, the records are

    L=R_strict(a,v),
    M=max(Pr(p(0)<=a), R_closed(1,v)).                (1)

No ordinary initial or incoming path geometry is assumed. If m=0,
immediate inward continuation already dominates any additional
same-half excursion; suppose below that m>0.

Assume there is ystar in `[1+v,2]` such that

    ystar>4m,                                       (2)

    1-R_strict(1,-1+y)<=d
        for every 1+v<=y<ystar,                     (3)

    R_closed(1+4m,-1+ystar)<=M.                      (4)

The point in (4) is physical: (2) puts it strictly inside the spatial
endpoint edge, and ystar<=2 keeps it above the initial-time edge.
Condition (3) says when a new lower rank can first become available.
Condition (4) rules out a later upper capture during a sufficiently
short continuation. Strict and closed traces in these two statements
are intentionally different.

We also require the following separate continuation fact: after the
first center contact at time S>=1, the monster can continue directly to
the negative endpoint and then the positive endpoint without increasing
its expected capture time. This may be supplied by a center-memory
certificate. Section 4 gives a simple sufficient condition valid for
the current continuous-field representation.

## 2. Continuous branch reduction

Under these assumptions, every continuation of the specified prefix is
no better than one of the following:

* immediate inward continuation along U=1, then the negative/positive
  endpoint tour;
* one outward continuation along the current V=v to some
  `1<=U*<=2+v`, followed by inward motion along U*
  and the same endpoint tour.

In the second item U*=2+v is the positive-endpoint turn. For prefix (1), these are precisely
the actual free-second-turn responses `I(a,v,U*)`. Their costs must be
checked as a family. The theorem does not assert that U*=1, the endpoint,
or any prescribed interior turn is always best.

Consequently, if every such free one-I response has cost at least V,
then every arbitrary continuation of prefix (1) has cost at least V.
For an arbitrary earlier prefix, the same statement holds with that
prefix retained. Additional turns before its first U=1 contact are not
removed by this theorem.

### Proof

Write the continuation as m(t). Its light coordinates

    U(t)=t+m(t),       V(t)=t-m(t)

are continuous and nondecreasing. If it never reaches the center, the
reflected half of the princess law is never captured, so its expected
capture time is infinite. Otherwise let S be the first center-contact
time. Then S=U(S)>=1. Use the assumed center-continuation certificate to
replace the later history by the negative/positive endpoint tour.

If S>=1+4m, the delay bound in `POSTONE_SAME_HALF_DELAY.md` gives

    2(Ccontinuation-Cimmediate)>=S-1-4m>=0.           (5)

Equality S=1+4m is included. That proof did not use finitely many turns:
all still-lower positive ranks are delayed, only the upper mass m can
gain by at most four per rank, and every reflected capture is delayed
by at least S-1. Thus it applies to this arbitrary continuous curve.

It remains to consider S<1+4m. Let ell(t) be its running lower captured
record, and let

    tau=inf{t after the shared prefix : ell(t)<L}.

If this set is empty, no new lower positive rank is captured before the
center. Merge all outward U-growth into the first outward block at V=v,
then continue inward. This catches every captured upper rank no later
and delays no lower capture. Stop that merged outward block at the
positive endpoint if it would otherwise leave the interval.

If the set is nonempty, put U*=U(tau), with its continuous limit when
the record first begins to decrease only after tau. Every new lower
capture at a positive point (U,V) has

    1-R_strict(U,V)>d.

Transport gives `R_strict(U,V)>=R_strict(1,V)` for U>=1, so (3)
forces `V>=-1+ystar`. Every later point before the center has

    U<=S<1+4m,       V>=-1+ystar.

By (4) and transport its closed radial CDF is at most M. Hence no new
upper rank can be captured after the first new lower capture. The same
conclusion holds at a simultaneous first contact, because (4) uses the
closed trace.

Move all outward growth before tau to the initial V=v block, ending at
U*. An upper rank caught before tau is then caught no later: its first
inverse beta(v) is no later than its original contact beta(V(t)), and
its light coordinate at that earlier contact is at most U(t)<=U*.
There were no new lower captures to delay before tau.

After this merged block, continue inward along U*. Every lower rank
caught later in the original history had incoming coordinate at least
U*, so its first inverse alpha(U*) is no later. No upper capture after
tau is lost, since there was none. Remaining upper ranks and all
reflected ranks are captured no later on the earlier endpoint tour.
If U*>2+v, instead stop at the positive endpoint U=2+v and start the
inward sweep there; all upper ranks have then already been captured,
and the incoming coordinate is still no larger than U*.

When tau is an unattained infimum, the statements apply directly to each
rank with an actual first capture after tau. Its coordinate is at least
the continuous limit U(tau). Equivalently, one may take first-record
times decreasing to tau and use continuity of the competing paths and
inclusive first contact. No positive-mass band is discarded by this
limit. This proves the branch reduction.

## 3. A convenient continuous-field sufficient test

For a field with no spatial atoms in the interior, let

    e(y)=1-R(1,-1+y),
    eend(y)=1-R_interior(1+y,-1+y),    0<=y<=2.

The latter is the deficit immediately before the positive-endpoint
capture jump. Suppose

    e(y)<=y/2,       eend(y)>=e(y)/2                 (6)

throughout the relevant outgoing range, and the given prefix satisfies

    d>=2m.                                          (7)

A new lower capture requires e(y)>d>=2m, hence y>4m.
Every later interior upper trace has deficit at least eend(y), which is
greater than m; a new upper capture then requires the endpoint. Such an
endpoint has incoming coordinate 1+y>1+4m and is excluded by (5) in the
short-continuation case. At y>2 the interior radial CDF is zero by
endpoint absorption, so no upper capture is possible there either.
This proves the same reduction without having
to solve separately for ystar.

More generally, choose positive constants C, kappa, gamma and a cut
Yout<=2 such that

    e(y)<=C*y on [0,Yout],
    eend(y)>=kappa*e(y) on [0,2],
    d>=gamma*m,       d<e(Yout),
    gamma>4C,         kappa*gamma>=1.                (9)

Continuity and monotonicity of e give a ystar with e(ystar)=d, and

    ystar>=d/C>=gamma*m/C>4m.

The endpoint trace at that row, and every subsequent interior trace,
has deficit at least kappa*d>=m. Thus (9) implies the exact gates
(2)--(4). These sufficient tests can fail even when the more precise
gates hold. With interior atoms, use the original strict/closed gates
instead of identifying the two traces in (6) or (9).

## 4. The center-continuation condition

Endpoint absorption by time two implies

    p_q(t)>=t-1 for t<=2.

From a center start at S>1, even the fastest outward monster has radius
at most t-S<t-1 before time two. Thus it cannot capture any princess in
the interior. Equivalently, its outgoing first inverse is
`beta_q(S)=S+1`, the endpoint contact. At S=1 the only exception is a
path reaching the outgoing characteristic V=1 before time two.

Therefore a sufficient extra condition is

    beta_q(1)=2 for almost every radial rank q.       (8)

Under (8), a center start at any S>=1 has only endpoint captures. Before
the first center contact a positive-half monster has captured no
reflected path, while it may have captured positive paths. The negative
endpoint consequently has at least as much remaining mass, so visiting
it first is optimal. This proves the required continuation condition.

Condition (8) is used only for this simple center-continuation argument;
it is not needed for the delay estimate (5). An alternative center-memory
certificate may permit outgoing V=1 atoms. The saved discovery fields
set the entire V=1 interior trace to zero and therefore satisfy (8).

## 5. Whole-cell audit of the supplied terminal field

The diagnostic `endpoint_joint_i1_field.json` satisfies (9) on its entire
terminal prefix domain

    0<=x=1-a<=y=1+v<=1/128

with the rational constants

    C=9/20,       kappa=19/20,       gamma=19/10,
    Yout=1/2.

In particular gamma-4C=1/10 and kappa*gamma-1=161/200.
This is a continuous-domain statement, not a nodal sample. The auditor
checks e and the endpoint interior trace on every affine boundary
segment. In each terminal triangle it splits at the affine line
`r(x)=e(y)` and checks all resulting vertices of
`D(x,y)-gamma*min(r(x),e(y))`. Therefore every point in each cell is
covered. Exact rational transport is checked separately by `ExactField`.

Reproduce the certificate with

```sh
python -B packages/interval_cdf_discovery/audit_postone_branch_gates.py \
  packages/interval_cdf_discovery/snapshots/endpoint_joint_i1_field.json \
  --output packages/interval_cdf_discovery/snapshots/endpoint_joint_i1_return_gates.json
```

The output includes each rational boundary witness and each split-cell
witness, along with the input field path and the explicit theorem
scope. It does not assert the required free-I cost inequalities. The
same certificate is unaffected by a subsequent rank-band warp if that
warp leaves this terminal initial triangle and the relevant U>=1
postfield unchanged; that preservation must be checked for the chosen
rank band.

## 6. Exact capture fixtures and scope

Run

```sh
python -B packages/interval_turn_density/verify_postone_same_half_gate.py
```

The verifier checks the strict first-lower gate on whole characteristic
intervals, verifies the short-case merge pointwise for both reflected
copies, and exercises the endpoint truncation. It includes legal
princess paths with a genuine post-U=1 wave. All 3,620 checks pass,
including 1,440 short-return pointwise comparisons and 320 long-return
delay comparisons. The continuous-time argument in Section 2 supplies
the absence of a turn-count restriction; the finite fixtures are
independent checks of its capture partition.

This is a usable branch certificate for a supplied field. A complete
all-monster lower certificate must additionally establish its free
one-I inequalities, handle the histories preceding U=1, and cover the
center states outside Section 4. Those obligations are not replaced by
a numerical pass of the gates.
