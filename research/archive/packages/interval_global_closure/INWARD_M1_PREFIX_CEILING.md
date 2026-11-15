# The complete inward-M1 constraint and a fixed-prefix rejection

## A constraint for every continuous start

Let \(X(t)\in[-1,1]\) be any hidden 1-Lipschitz princess path, and write
\(F(t,x)=\Pr(X(t)\le x)\). A monster starts at \(a\in[-1,1]\), moves left
at speed one to \(-1\), then right to \(+1\). Put

\[
T=1+a,\qquad M(a)=F(0,a),\qquad
N(a)=\int_0^T F(t,(a-t)-)\,dt.
\]

The strict trace in the integrand and closed trace in \(M\) are intentional.
Initial coincidence is capture at time zero.

On the first leg, \(X(t)-(a-t)\) is nondecreasing. Thus exactly the initial
mass \(M(a)\) is captured by \(T\), and its first-capture moment is exactly
\(N(a)\). This statement is independent of the temporal coupling of the
marginals.

For the second leg define

\[
J(a)=\int_T^{T+2}
 \bigl[F(t,t-a-2)-M(a)\bigr]_+\,dt.
\]

The cost of the fixed monster obeys

\[
\boxed{\quad
C_{M1}(a)\le N(a)+(3+a)(1-M(a))-J(a).
\quad}
\]

Equality holds for the comonotone, or quantile-ordered, princess law with
these marginals. Therefore a lower strategy guaranteeing \(v\) must satisfy,
for EVERY \(a\in[-1,1]\),

\[
N(a)+(3+a)(1-M(a))-J(a)\ge v.
\]

This is a complete continuous-start M1 constraint for an ordered law; checking
only starts already present in a finite upper support is insufficient.

### Proof of the second-leg term

A survivor of the first leg has \(X(0)>a\). On the second leg,
\(X(t)-(t-a-2)\) is nonincreasing. Survival through time \(t\) is therefore
the intersection of the events \(X(0)>a\) and \(X(t)>t-a-2\). Its probability
is at most

\[
\min\{1-M(a),1-F(t,t-a-2)\}.
\]

For a comonotone law both events are upper rank intervals, so this bound is
an equality. Integrating the survival probability, together with the
first-leg contribution \(N(a)+T(1-M(a))\), gives the displayed formula.
This proof retains endpoint atoms and closed contact at the final endpoint.

## The sharp ceiling when the prefix is held fixed

Since \(J(a)\ge0\),

\[
C_{M1}(a)\le K(a):=N(a)+(3+a)(1-M(a)).
\]

No alteration after \(T\) can exceed this ceiling if the earlier law remains
unchanged. The ceiling is sharp for that one fixed attacking route: send
every survivor toward \(+1\) at speed one and then keep it there. Each stays
strictly ahead of the monster's rightward leg until the final endpoint at
\(T+2\). Sharpness for this route is not simultaneous optimality against
other monsters.

For a symmetric nonnegative radial-pair law and \(a\ge0\), let
\(A(a)=\Pr(p(0)\le a)\). Then

\[
M(a)=\frac{1+A(a)}2,\qquad
N(a)=\frac12\left[
 \mathbb E\,\beta_p(a)
 +\mathbb E\bigl(1_{\{p(0)\le a\}}\alpha_p(a)\bigr)
\right].
\]

Here \(\alpha_p(a)\) and \(\beta_p(a)\) are the first inverse times of
\(t+p(t)=a\) and \(t-p(t)=a\). Exact equality contacts are retained.
Equivalently, in light-coordinate radial CDF notation,

\[
4N(a)=2(a+1)
 +\int_{-a}^{a}R^<(a,V)\,dV
 -\int_a^{a+2}R^\le(U,a)\,dU.
\]

The remaining hinge is

\[
4J(a)=\int_{a+2}^{a+4}
 \bigl[R^\le(U,a+2)-A(a)\bigr]_+\,dU.
\]

If every positive radial path is absorbed at \(+1\) by time two, \(J(a)=0\).
No such absorption assumption is used in the general constraint.

Under ordinary density regularity, the ceiling derivative is

\[
K'(a)=\int_0^{1+a} f_t(a-t)\,dt
      +1-F(0,a)-(3+a)f_0(a).
\]

An active exact-cost phase satisfies \(K'(a)=J'(a)\); it reduces to
\(K'(a)=0\) only when the hinge vanishes. At atoms or characteristic
discontinuities, the exact trace constraint above must be used instead
of this differential shorthand.

## The retained159-control candidate

The input is the actual full-bank dual in
6cac47a4b2227fa1469bb463d35ed37ffb3af1b6, not the earlier36-row common-warp
subproblem dual. Its159 positive controls are paired with their reflections;
the recorded decimal weights are interpreted as exact rationals and normalized.

Three microscopic constructions were checked:

- the avoided-isolated-bounce graph with affine shrink;
- the same graph clipped into \([\epsilon^6,1-\epsilon^6]\);
- the raw avoided graph, without shrink or clipping.

These are distinct legal laws. They give the same limiting cost against the
following simple fixed monster:

\[
(0,7/8),\quad (15/8,-1),\quad (31/8,1).
\]

Its exact ordered-law limiting cost is

\[
\frac{18339429312017578045788928988179}
     {13483358399999999905072033187808}
 \simeq 1.3601529209531047.
\]

Neither this physical route nor its reflected orientation occurs among the
1086 supplied monster atoms. The bank does contain the outward M1 at this
absolute start, several negative-M2 turns, and initial-inward rows. Those do
not replace the omitted inward-first M1 constraint.

The first leg captures mass

\[
M=
\frac{83411087490828341574781}{99999999999999999295962}
 \simeq .8341108749082835,
\]

with limiting first moment

\[
N_0=
\frac{324941879154404974282113567935}
     {421354949999999997033501037119}
 \simeq .7711832485993223.
\]

Therefore EVERY tail modification retaining this prefix has limiting cost at
most

\[
N_0+\frac{31}{8}(1-M)
=
\frac{9532758715001446584439524288449}
     {6741679199999999952536016593904}
 \simeq 1.414003608329724.
\]

This is already below the retained finite-bank master level. The failure
cannot be repaired solely by changing the microscopic isolated-bounce
connector or the later endpoint excursions. Initial/ray moments or the
mixture weights and earlier controls must change.

The large capture group whose LIMIT time is \(15/8\) was checked with the
full germ order: its actual affine/clipped capture time is
\(15/8-\epsilon^6\), and its raw capture is exactly \(15/8\).
Thus the first-leg classification does not replace arrival comparisons by
their limits.

## Verification and scope

The fixed-prefix moment was replayed independently by direct physical
segment intersections, without the inverse-hit or rank-record scorer.
It checked all318 signed paths, found229 captured component paths, and
matched the exact rational-germ moment and captured mass. Shared geometry
caches were used only after checking every distinct physical vertex and edge.

The full fixed attack was evaluated on the ordered marginal law using exact
strict/closed capture records. Its equality across the three microscopic
variants is a candidate-specific rejection. It is not an upper bound for the
full game, a completed adaptive-monster search, or an exclusion of all
approaching multi-wave laws.
