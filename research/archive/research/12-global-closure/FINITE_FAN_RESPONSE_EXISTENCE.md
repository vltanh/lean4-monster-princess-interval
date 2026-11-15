# Finite-piece optimal response for a fixed ordered finite fan

## Scope and conclusion

Fix one finite fan law with ordinary real parameters. Each base path has
finitely many affine pieces, slopes in {-1,0,+1}, and is stationary after a
finite time h. Every translation interval has fixed positive width. Apply
endpoint clipping and fair reflection, then realize the resulting marginal
law by one common ordered signed quantile.

The same result applies to the reflected-outward construction
p_z=1-|1-p-z|, with p in [0,1] and 0<=z<=delta<=1, and to finite sums of the
resulting interval-density pieces. What matters is the marginal geometry:
the signed interior CDF is continuous piecewise affine on a finite
space-time arrangement; its cell edges have speeds -1, 0, or +1; it has a
finite uniform interior density bound; and its final marginal is a static
piecewise constant density with finitely many atoms.

**The unrestricted optimal Monster response is attained by a path with
finitely many affine pieces.** This is an existence assertion for the fixed
law. This note does not supply an effective uniform bound on the number of
pieces before the static tail. It does not prove any proposed equilibrium
or membership in a fixed finite-turn game.

For rational base vertices, weights and nondegenerate translation bounds,
the optimal response value is a real algebraic number, and some optimal
finite-piece response has real algebraic vertex coordinates. The number of
pieces whose optimization yields that value is not supplied by this proof.
This corollary does not imply algebraicity of the full Princess-Monster game
value.

The ordered-law qualification is essential. A raw mixture of translated
paths can cross itself; the captured ranks of that raw realization need not
form one interval. Only the marginal fan and its common-quantile realization
are used here.

## 1. Notation and local hypotheses

Write p_q(t), 0<q<1, for the nondecreasing signed quantile paths. They are
1-Lipschitz. Let F^-(t,x) and F^+(t,x) be the strict and closed signed CDFs.
For a Monster path m, put

\[
 L(t)=\inf_{0\le s\le t}F^-(s,m(s)),\qquad
 M(t)=\sup_{0\le s\le t}F^+(s,m(s)).
\]

The ranks caught by time t are the interval between these two records, up to
irrelevant singleton rank conventions. The uncaught mass is
1+L(t)-M(t). Initial and endpoint atoms are counted by the distinct strict
and closed traces, including isolated endpoint contacts.

On the open physical interval, every fan has a finite constant C with

\[
 0\le F_x\le C,\qquad |F_t|\le F_x.
\]

Consequently, before the first endpoint contact, the continuous trace

\[
 f_m(t)=F(t,m(t))
\]

is 2C-Lipschitz. This follows on every affine cell by the chain rule and then
across the finitely many cell boundaries by continuity; equivalently it is
the Lipschitz transport estimate. It applies to arbitrary 1-Lipschitz
Monster curves, not only polygonal ones.

For clipped fans there can be atoms at -1 or +1. They are explicitly excluded
from this bounded-interior-CDF estimate and are treated in Sections 4 and 5.
Reflected-outward fans have no endpoint atom, but do not need that stronger
property.

### The local interface input

At any interior point (tau,a), take a sufficiently short right-time
neighborhood. A moving edge of speed +1 or -1 through that point lies on the
boundary of its forward light cone. Other moving edges stay outside a
sufficiently small cone. Only stationary edges through a can divide its
interior. The signed CDF in that cone therefore has the form

\[
 F(\tau+t,a+x)-F(\tau,a)=
 \begin{cases}
 \alpha t+\beta_-x,&x\le0,\\
 \alpha t+\beta_+x,&x\ge0,
 \end{cases}
 \qquad \beta_\pm\ge|\alpha|.
\]

Coincident stationary edges are combined. One or both densities may be zero.
The game center is included: fair reflection and absence of a center atom
give F(t,0)=1/2, hence alpha=0 and beta_+=beta_- at a central source.
Its local cone is a single stationary affine-density cone, so the alpha=0
bridge/return argument applies directly. If its density is zero, no capture
source can begin until the next cone on which the density is positive.
Only physical endpoints are excluded and handled separately below.

After reflecting local directions, take alpha>=0. If beta_-=alpha, there is
no productive growth of the opposing record and the one-sign bridge below
suffices. In the nondegenerate case, the local persistence requirement of
the interface theorem can always be met by shortening the window, because
beta_-/(beta_--alpha)+1/2 is a finite fixed number.

The proven local normal form is the following input:

> In a sufficiently small unchanged forward cone, any prefix from its
> source to a prescribed space-time endpoint can be replaced, with the same
> later continuation, by at most five real interface-return tents, three
> productive unit legs in a final partial excursion, one constant-rank hold,
> and one nonproductive connector. Its cost is no greater, and no rank
> already caught by the old prefix is lost at the end of the replacement.

Thus at most fifteen affine pieces suffice locally. An all-wait block is an
alternative to the five-tent return block, not an additional wait beside
five tents. The exact return-block proof includes arbitrary old rank
records; the zero-width case alone is enough for Section 5.

This local input consists of:
- INITIAL_INTERFACE_RETURN_BLOCK.md, including its explicit old-record
  extension;
- AFFINE_HALF_CELL_BRIDGE.md, including the labelled extension;
- the earlier affine-corridor and arbitrary-left-excursion lemmas cited there.

It is not a global atlas count. In particular, a future-hit credit used by
the local normalization must remain inside its specified persistence cone.

## 2. A fixed finite completion horizon and attainment

Let K0 be the number of distinct density-cell endpoints, atom positions and
arena endpoints in the complete static marginal after h. The stationary
tail theorem gives the uniform horizon

\[
 H=h+2(K0+3).
\]

Indeed an ordered history removes one rank interval. At h the survivor
measure is the two outer spatial tails of the static marginal, adding at
most two cut locations. The exact static turning-point reduction then
completes optimally within the displayed time. Its proof retains atoms at
closed contacts and does not assume a direct endpoint tour is optimal from
an arbitrary static interior state.

It follows that restricting to Monster paths which catch almost every rank
by H does not change the unrestricted infimum. This family is nonempty.

The set of 1-Lipschitz paths [0,H]->[-1,1], with arbitrary initial position,
is compact in the uniform norm. For each fixed continuous target path
p_q, its first-contact time is lower semicontinuous in that topology. To
see this, take a convergent sequence and a subsequence along which the
contact times converge to their lower limit. A convergent subsequence of
contact points is still a contact by uniform convergence. The value
+infinity is allowed for no contact.

The subset catching almost every rank by H is closed: for a convergent
sequence, discard the countable union of its null exceptional rank sets and
apply the preceding contact-time inequality at each remaining q. Fatou's
lemma makes the expected first-contact time lower semicontinuous. A minimum
is therefore attained on this compact family.

This establishes an unrestricted bounded-horizon optimal response before
any finite-piece reduction is applied.

## 3. Finite record alternation after positive captured width

Suppose the first endpoint has not yet been reached and

\[
 w_0=M(t_0)-L(t_0)>0.
\]

The nondecreasing record M and nonincreasing record L are continuous.
At a time in the support of positive upper-record growth, the trace equals
M; at a time in the support of lower-record decrease, it equals L.
For any such opposite types of productive times after t0, the two trace
values differ by at least w0. Since the trace is 2C-Lipschitz, they are
separated in time by at least

\[
 \frac{w_0}{2C}.
\]

For C=0 no interior record grows. For C>0, on a bounded horizon there are
only finitely many switches between upper and lower productive record
growth after t0.

This statement concerns supports of the continuous record-variation
measures. It does not assume isolated first-hit times, positive speed, a
finite number of original turns, or attainment of a first productive event
in each interval. A closed interval during which both records are constant
can be assigned to an adjacent episode. We obtain finitely many episodes
with growth of at most one record direction.

The width w0 depends on the particular positive time t0. This argument
deliberately does not produce a law-only effective bound as t0 approaches
an initial zero-width source.

## 4. Pointwise bridges for a one-sign episode and for endpoint completion

Consider an interval [s,e] whose new captures belong only to upper ranks
q>M(s). Keep its two endpoints fixed. Replace the Monster by

\[
 m_{\max}(t)=\min\{1,\ m(s)+t-s,\ m(e)+e-t\}.
\]

This is the pointwise largest legal Lipschitz bridge between those endpoints.
It has at most three affine pieces. Every newly caught upper rank starts
strictly above the Monster at s, up to null rank boundaries. At its old
first-contact time, the new Monster is at least as high as the old one.
The intermediate value theorem therefore gives a new contact no later than
the old contact. There are no old newly caught lower ranks in this episode
to lose. Previously caught ranks remain caught, and the subsequent route
is identical. Extra contacts only help.

For a lower-only episode use

\[
 m_{\min}(t)=\max\{-1,\ m(s)-(t-s),\ m(e)-(e-t)\}.
\]

The reflected proof is identical. If neither record grows, the straight
legal connector has no old new capture to delay. This argument is
pointwise in each relevant quantile path and does not depend on any affine
CDF-cell confinement.

At the first endpoint contact, say m(s)=+1, the direct unit sweep toward -1
dominates every continuation pointwise in all remaining targets. Every
survivor is below +1 at s. At any old future contact before s+2, the new
left-moving ray is no higher than the old Monster; hence it has already
crossed that target. By s+2 it crosses every target. The reverse statement
holds after first contact with -1.

Thus endpoint atoms do not cause an accumulation difficulty: their closed
contact is retained, and from the first endpoint onward one straight sweep
suffices. If its zero-mass arena completion extends beyond H, it may be
truncated at H; all ranks caught by the old path by H are already caught.

## 5. Removing the only possible initial accumulation

Take the bounded-horizon optimizer from Section 2. If its captured width is
positive at the initial time, Section 3 applies immediately. This can occur
at an endpoint atom and is also covered by direct endpoint completion.

Otherwise let tau be the first source of positive captured width: before
tau the width is zero, and either an endpoint jump occurs at tau or
positive width occurs arbitrarily soon after tau. Before tau no target of
positive mass has been caught.

A zero-capture initial gap can be replaced by a straight legal connector
having the same initial and terminal space-time points. This delays no old
capture, and any additional capture can only improve the later response.

If the source is an endpoint jump, use Section 4. If it is interior, the
finite fan arrangement gives the local two-half-cell cone of Section 1.
Choose a positive time T inside its full persistence region such that the
old width at tau+T is positive. If both local density pieces vanish, no
width could begin in that cone, so this case cannot be the source. Apply
the local at-most-fifteen-piece replacement up to tau+T and leave the
remaining route unchanged.

The replacement retains all ranks caught by the old prefix at its endpoint,
so its captured width there is still positive. Section 3 now gives only
finitely many later record-direction episodes. Apply the at-most-three-piece
bridge of Section 4 to each, and apply the endpoint sweep when an endpoint
is first encountered. The resulting entire response has finitely many
affine pieces and no greater cost than the optimizer. It is therefore
also optimal.

This proves the stated finite-piece existence theorem. It does not assert
that every optimizer has finitely many turns. A noncanonical optimizer may
still waste turns or realize an unnecessary accumulation.

## 6. Algebraicity for rational ordinary finite fans

Assume all fan data are rational and all widths are fixed positive rational
numbers. The final time h and the horizon H above may be chosen rational.
The full strict/closed signed CDF has a finite piecewise-affine description
with rational coefficients, including the endpoint-atom traces.

The preceding existence theorem supplies some finite N for an optimal
response. Parameterize all legal paths with at most N affine pieces by their
time-position vertices, padding with zero-duration repeated vertices if
necessary. The inequalities

\[
 0=t_0\le t_1\le\cdots\le t_N=H,\quad -1\le x_i\le1,\quad
 |x_i-x_{i-1}|\le t_i-t_{i-1}
\]

are semialgebraic over the rationals. Zero-duration pieces have equal
positions and are handled as a separate finite branch.

For a fixed nonzero-duration leg, the CDF along it is affine in physical
time. Its coefficients are rational functions of the vertex parameters.
Intersections with the finitely many CDF-cell boundaries are rational
functions of those parameters on each nondegenerate branch. Collinear
legs, ties and zero slopes are retained as separate branches.

The running lower and upper records are obtained by finitely many minima,
maxima and crossings of these affine traces and preceding record values.
Their additional break times are again rational functions on a finite
semialgebraic partition. Isolated endpoint contacts update both strict and
closed records immediately; an isolated zero-duration contact is not
discarded merely because it has zero length.

Consequently the exact capture cost

\[
 \int_0^H[\,1+L(t)-M(t)\,]\,dt
\]

and the full-capture condition L(H)=0, M(H)=1 are semialgebraic over the
rationals. More concretely, the cost is piecewise rational in the vertex
parameters. Only affine-in-time integration is performed, so no logarithmic
term is introduced.

The minimum in this fixed-N class equals the unrestricted value because it
contains the finite-piece optimizer. By real-closed-field definability, an
attained minimum of a rational semialgebraic function over a rational
semialgebraic feasible set is a real algebraic number. One way to express
this directly is to define the singleton of values v for which a feasible
point has cost v and every feasible point has cost at least v. Quantifier
elimination makes that singleton semialgebraic over the rationals; a
one-dimensional rational semialgebraic singleton is algebraic.

The nonempty set of minimizing vertex parameters is semialgebraic over the
real algebraic numbers and therefore contains a tuple of real algebraic
numbers. This gives an algebraic optimal finite-piece response.

No effective N follows. Enumerating fixed-N minima without a stopping
certificate is not made into a terminating response algorithm by this
existence proof. Infinitesimal germs, zero-width limiting fans, and the
infimum over all Princess laws are outside this algebraicity corollary.

## Dependencies and verification scope

- Static tail:
  research/12-global-closure/STATIC_TAIL_BOUNDARY_REDUCTION.md,
  blob e78d8a40669357968709ce9a5c4be8c76237e1fa.
- Local return block and explicit old-record extension:
  INITIAL_INTERFACE_RETURN_BLOCK.md,
  blob d10fa2df15cb767f11fb5cb4b92cf990e3a046ce.
- Local partial bridge and labelled old-record extension:
  AFFINE_HALF_CELL_BRIDGE.md,
  blob a7f977451db98b0b00bdd4e5b3f1f4fd3974cf3a.
- Fixed-law finite center-return theorem:
  FAN_FINITE_CENTER_RETURNS.md,
  blob 9bb8fd646b164ebff57b9de374c13953437222ad.
  Its explicit center count is compatible with, but not used to assert an
  effective full-prefix count here.

The proof of finite existence and algebraicity is analytic. Companion
finite exact fixtures, if supplied, test bridge and record estimates only;
they do not replace compactness, the local source theorem, or
real-closed-field definability. No native execution or new numerical game
bound is claimed by this note.
