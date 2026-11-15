# Isolated center avoidance in the frozen upper response face

This note concerns only the exact 280-pair law in `upper_warp_exact.json`. It does not construct a lower strategy or prove that this upper law is minimax optimal. It identifies a genuine first-contact discontinuity in its maximizing response face.

The exact unrestricted response is
\[
57045189772271291487410009/40000000000000000000000000.
\]
The integer flow certificate supplies the complete finite maximum-cut face. The complete atomic response theorem also supplies its componentwise capture envelope: after fixing a finite capture chamber, filling unpriced inverse intervals and expressing the remaining controls in the order-polytope vertices bounds every oriented monster capture time by the corresponding convex combination of limiting vertex capture times. The face statement below uses that componentwise form, not just equality of one scalar objective.

## A single positive-weight witness

Use reference light coordinates U=t+p, V=t-p and write P(V)=U for a strictly increasing regularized inverse. Set b=5/8 and c=11/16. Under the frozen common map,
\[
 B=\psi(b)=624999999999997/1000000000000000,\qquad
 C=\psi(c)=343748638961819/500000000000000.
\]
In particular B<C<1.

Atom 30 is the reflected pair with reference path
\[
 (-b,b)\longrightarrow(1,b)\longrightarrow(1,3)\longrightarrow(5,3).
\]
Its pair probability is
\[
 w=30789495/10000000000>0.
\]
The actual light coordinates are obtained by applying psi to both coordinates.

The unreflected first leg is V=B and travels through the center at time B. Its reflection has initial left-moving leg U=B and also passes through the center at time B. Both first legs extend far enough to include the contact coordinates below.

The minimum and maximum residual cuts agree at the relevant query thresholds:

| Reference query | Minimum label | Maximum label |
|---|---|---|
| Last query before b, namely 5033165/8388608 | (b, minus) | (b, minus) |
| Query b | (c, minus) | (c, minus) |

Here “minus” is the strict lower-side lexicographic state. The extremal initial positions lie between psi(15/32) and psi(1/2), both below B. Thus the initial side of both witness legs is fixed throughout the maximum face.

Direct first-contact evaluation on both extremal cuts gives
\[
 \alpha(B)=B,\qquad
 \beta(B)=\frac{B+C}{2}
 =262499455584727/400000000000000>B.
\]
Every maximum cut has the same two contact coordinates. For the reflected initial leg, all earlier query states are below U=B and the first threshold crossing occurs at V=B. For the unreflected leg, the query at V=B has the common limiting value U=C. The monotonicity of the corresponding first inverses and the extremal-cut bounds make these statements valid throughout the face.

## Why a literal path cannot attain the face

For any actual nonnegative continuous princess path,
\[
 \alpha(B)=B\quad\Longrightarrow\quad
 B+p(B)=B\quad\Longrightarrow\quad p(B)=0.
\]
Since V(t)=t-p(t) is nondecreasing, satisfies V(t)<=t, and equals B at t=B, this forces
\[
 \beta(B)=B.
\]
It is therefore impossible for a literal path to have the two contact times required by the maximum face.

This also excludes an attained maximum hidden outside the canonical filling convention. Suppose an actual path attained the exact upper response. Strictly positive paths with speed strictly below one approximate it uniformly. First-capture lower semicontinuity and the finite uniform capture horizon imply that their total payoffs tend to the same maximum; along a subsequence each positive-weight oriented capture time tends to its value for the alleged maximizer. Their componentwise finite capture envelopes have the same limiting total payoff. Consequently all positive mass in the finite vertex decompositions concentrates on maximum vertices, and every positive-weight component has zero limiting envelope loss. The two witness contact times must then converge to the two fixed face values above. They cannot both be the actual contact times of the alleged maximizer. By the symmetric folding theorem, allowing signed princess paths does not repair this contradiction.

The upper response is a supremum approached by legal paths. Nonattainment of this particular upper response is not a proof that the upper law itself is or is not optimal in the full game.

For a literal center-touching realization under the same face envelope, the witness pair alone loses at least
\[
 \frac{w(C-B)}4
 =384851925228710990259/8000000000000000000000000
 \approx 0.000048106490653588874
\]
relative to the limiting face value. This comparison is scoped to that face envelope; it is not a uniform gap for arbitrary nearby probability laws.

## The seven bounces are priced, not late filling artifacts

The same exact trace pattern occurs at
\[
 b\in\{5/8,11/16,3/4,13/16,7/8,15/16,2047/2048\}.
\]
Before each query, both extremal labels are (b, minus). At the query they jump to the next listed return characteristic. At the final query the common base is b+2; its two extremal side states are minus and zero.

Each bounce has a positive-weight initial-left witness U=b and a center-crossing outgoing witness V=b. In the first five cases an ordinary negative-start M2 pair with turn U=1 already supplies both witnesses. These witnesses prevent a macroscopic advance of the outgoing crossing while keeping the same optimal envelope: advancing the first U=b crossing by a V-distance delta lowers its reflected first-capture contribution by its positive probability times delta/2.

The limiting pre-one geometry has isolated center zeros, with a unit incoming leg followed by a unit outgoing leg. It has no positive-duration pre-one center wait. The narrow positive-radius regularizations avoid exact center contact and converge to those corners. This is different from replacing a positive-duration center wait by a small constant displacement; no such claim is made here.

Canonical reconstructions also contain many late excursions close to the endpoint, and even later center waits. Those are not being promoted to necessary phases. A separately checked positive regularization with the absorbing tail p(t)=1 for t>=2 has all 560 oriented captures complete and approaches the same exact response within 1.43722e-16 at epsilon=2^-48.

## A uniform attack on this exact face

There is also an obstruction to recovering a matching law solely inside this exact face, independently of the center-contact issue. Set
\[
 A=\psi(15/32),\qquad X=\psi(1/2),\qquad T=\psi(5/8).
\]
The extremal priced traces give
\[
 P(-X)\le X,\qquad P(-A)\ge X,\qquad P(X)\le T.
\]
The first bound follows from the maximum label \((1/2,\mathrm{minus})\) at the reference query \(-1/2\). At \(-15/32\), both labels have base \(4823449/8388608>1/2\). At \(1/2\), both labels have base \(5/8\), with the lower-side state. These inequalities survive every extension of the unpriced inverse intervals; they do not rely on either canonical fill.

Thus the initial radius is at most \(X\), and
\[
 \alpha(X)\le\frac{X-A}{2},\qquad
 \beta(X)\le\frac{X+T}{2}.
\]
A straight-left monster starting at \(+X\), continuing to \(-1\), then to \(+1\), captures the positive and negative copies at these two first inverses. Its expected cost against any reflected law confined to these face traces is at most
\[
 \frac{2X+T-A}{4}
 =\frac{578124999999997}{2000000000000000}
 \approx0.2890625.
\]
For realizing epsilon controls the same bound has a vanishing perturbation error. In particular, the exact face's two extremal controls cannot be promoted to a useful lower mixture merely by assigning weights or changing unpriced fills. Broad near-optimal response phases at other initial positions are required. This is a diagnostic about the frozen, rounded law, not an exclusion of general multi-wave approaching strategies.

## Reproducible data and remaining obligation

`upper_warp_face_geometry.json` records both limiting profiles through time two, every critical query side state, the witnessing physical atoms, and the absorbing physical epsilon path. No lower mixture weights have been assigned. The initial range of this exact face is narrow, so the face alone is not a candidate matching lower law.

The open constructive question is whether a joint probability law can use moving versions of these isolated center-avoidance fronts, with a uniform all-monster guarantee. A common coordinate warp preserves exact center contacts and cannot by itself create the positive-radius layer. The finite face and this nonattainment lemma identify that missing layer without asserting its existence.
