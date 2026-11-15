# An attained endpoint-sweep value from center memory

This gives a concrete continuation value for the curved ordered princess
laws, rather than another unspecified Bellman potential. It can remove
every later center excursion even when paths leave the center slowly and
can still be caught in the interior. The costs before the resulting
barrier and a matching unrestricted equilibrium remain open.

## 1. Two radial records

Use an ordered nonnegative princess law, with independent fair reflection.
All paths are 1-Lipschitz and fixed at their signed endpoints from time two
onward. Earlier endpoint visits followed by departure are allowed. Let

    R(U,V)=Pr(p_q((U+V)/2)<=(U-V)/2),
    Z(t)=R(t,t),
    H(t)=sup_{0<=v<=t} Z(v).

The closed interior CDF is used, including exact characteristic contacts.
Define the entire future interior frontier by

    Y_tail(t)=sup {R(U,V): V>=t, V<=U<V+2}.              (1)

Under endpoint absorption by two, the nonzero part has V<=1. Equivalently,
take the fixed-V limits as U increases to V+2 and then their supremum over
V>=t. This is not, in general, the strict spatial CDF at the actual endpoint
at time V+1: an outgoing characteristic atom can be met in the interior and
then reach that endpoint exactly. A single endpoint-row limit at V=t is
also insufficient if some paths leave an earlier endpoint before time two.

The definition makes Y_tail nonincreasing. Every future interior point
reachable from center at time t has V>=t, so every rank caught there is at
most Y_tail(t).

**Center-memory lemma.** At any center visit t, the two captured radial
frontiers r_+,r_- satisfy

    max(r_+,r_-) >= H(t).                               (2)

For any q<H(t), there is a v<=t with p_q(v)=0. If m(v)>=0, the difference
m-p_q is nonnegative at v and nonpositive at t, so the positive copy was
caught by t. If m(v)<=0, the same argument with m+p_q catches the negative
copy. At a center visit each sign's captured labels form a prefix. Thus
at least one prefix reaches every q<H(t), proving (2). This argument is
independent of the initial monster position and all earlier turns.

## 2. The explicit continuation value

Write

    beta_q(t)=inf{s>=t:s-p_q(s)>=t}.

A direct outward run from center at t catches q at beta_q(t), with
t<=beta_q(t)<=t+1. Define the two direct endpoint-tour costs by

    S_+(t,r,n)=1/2 integral_r^1 beta_q(t)dq
               +(t+3)/2*(1-n),
    S_-(t,r,n)=S_+(t,n,r),
    S(t,r,n)=min(S_+,S_-).                              (3)

These are absolute contributions of the still-uncaught paths. The second
endpoint is reached after time three, when all surviving paths are fixed
there. For r<=n,

    2(S_+-S_-)=-integral_r^n (t+3-beta_q(t))dq <=0.       (4)

Hence the endpoint tour starts toward the less-captured sign.

**Sweep theorem.** If

    max(r,n)>=Y_tail(t),                                (5)

then S(t,r,n) is the exact unrestricted continuation value. In particular,
if H(t)>=Y_tail(t), (3) applies to every reachable center state at t and at
every later center return.

Here is a direct Bellman proof. Suppose r=M>=n and M>=Y_tail(t); the
lagging sign is negative. Every interior capture reachable in the future
has radial rank at most M. For a center triangle ending at e:

* If it goes into the lagging sign, its new frontier n' is still at most
  M. The outward capture times are exactly beta_q(t) for the newly caught
  ranks. Following the triangle by the lagging-side sweep delays all other
  negative captures from beta_q(t) to beta_q(e), and delays the remaining
  positive endpoint captures from t+3 to e+3. Both changes are nonnegative.
* If it goes into the M sign, it catches no new path on its outward leg.
  Only negative ranks reached at center can be new. The direct lagging
  sweep from t catches each such rank no later than that center contact.
  Its other negative captures and positive endpoint visit are again no
  later than those after the triangle.

The same comparison handles a center wait, using the first center-contact
time of each new rank. The larger frontier never decreases, while Y_tail
does not increase, so (5) persists at every subsequent state. A triangle
whose turn is an actual endpoint is a direct endpoint tour; (4) handles
the choice of its sign.

These are the exact Bellman inequalities for the explicit function S.
The maximal-tent reduction and finite-quantile transfer in
`GENERAL_CENTER_BELLMAN.md` therefore apply to arbitrary speeds, waits,
and arbitrarily many turns. The direct lagging-side tour attains S, giving
equality, rather than merely a continuation lower bound.

Notice what the proof does not require. It does not require Z(e)=Y_tail(e)
at every later return, and it does not say there are no later interior
captures. Curved low-rank paths may still be uncaught on the lagging sign.
The larger captured prefix makes every further return excursion unnecessary.

## 3. A finite, linear barrier condition for a field

For a continuous triangular affine CDF field, the center trace and the
saved endpoint-interior trace are piecewise affine. Their maxima occur at
their vertices, with interpolation where a proposed barrier cuts an edge.
Thus H(s0)>=Y_tail(s0) is a finite exact boundary calculation.

A convenient sufficient construction fixes a center-peak rank Q and adds

    R(s0,s0)=Q,
    R(V+2-,V)<=Q  for every V>=s0.                      (6)

On a fixed affine mesh these are linear nodal conditions. They allow
nonconstant curved trajectories after s0, arbitrary earlier endpoint
contacts, and a sharply concentrated incoming layer near U=1. They do
not impose a turn bound on arbitrary princess laws.

`packages/interval_turn_sheet/center_memory.py` checks this boundary
criterion in exact rational arithmetic for the decimal data supplied.
The field's transport admissibility and earlier monster costs must be
checked separately. A floating LP field satisfying (6) within tolerance
is not an exact game-value certificate.

## 4. Independent exact checks

`verify_center_memory.py` uses direct Fraction intersections of polygonal
paths and monster legs. Its fixtures include a center peak followed by
slow outward motion, characteristic capture atoms, stationary endpoint
mass, and a path that leaves an earlier endpoint. It checks the memory
bound for initial prefixes and the attained sweep inequalities for both
triangle signs, center waits, and completed continuations.

The endpoint-departure fixture explicitly distinguishes a single outgoing
row from the full future interior cone. Another fixture distinguishes the
fixed-characteristic interior limit from the strict CDF at actual endpoint
contact. These distinctions are essential at atoms.
