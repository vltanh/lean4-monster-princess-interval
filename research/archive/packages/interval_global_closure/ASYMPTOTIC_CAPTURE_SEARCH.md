# Exact limiting capture search with objective-only pruning

## Scope

This adapter wraps the unchanged finite path capture-order oracle over
\(\mathbb Q(\epsilon)\). It certifies the limiting unrestricted monster response
to one supplied finite rational-germ princess law only when the search completes.
It is not a certificate for the full interval game.

All geometry remains exact: first contacts, strict and closed rank records,
event order, arrival times, speed feasibility, and Pareto dominance use the
original ordered field comparisons. The only changed branch is objective
lower-bound pruning.

## The pruning rule

Let \(B(\epsilon)\) be the cost of the current legal monster witness, and let
\(L_N(\epsilon)\) be the original oracle's valid lower bound for every
continuation of a search node \(N\). The adapter may discard that node when

\[
\lim_{\epsilon\downarrow0}L_N(\epsilon)
\ge
\lim_{\epsilon\downarrow0}B(\epsilon).
\]

It retains the full rational function \(L_N\), not only its limit. The incumbent
is still improved using the original exact germ comparison. No arrival-time or
geometric comparison is replaced by its limit.

## Completed-search certificate

Let \(B_*\) be the final witness cost and let \(L_1,\dots,L_m\) be every retained
bound from objective-pruned nodes. Define

\[
L_*(\epsilon)=\min\{B_*(\epsilon),L_1(\epsilon),\dots,L_m(\epsilon)\}.
\]

For all sufficiently small positive \(\epsilon\),

\[
L_*(\epsilon)
\le \inf_{\text{all legal monsters}} C_\epsilon
\le B_*(\epsilon).
\]

The right inequality is the explicit witness. For the left inequality, the
original finite capture-order theorem covers every monster by the search tree.
Completed leaves are no cheaper than \(B_*\); exact dominated states are covered
by their dominating states; every other discarded subtree has one retained
lower bound. The completed finite tree requires only finitely many polynomial
sign comparisons. Their recorded minimum radius therefore makes this entire
argument uniform in \(\epsilon\).

The limiting costs of incumbents never increase. At its pruning time each
\(L_j\) had limit at least that of the then incumbent, hence at least that of
\(B_*\). Consequently

\[
\lim L_*=\lim B_*=
\lim_{\epsilon\downarrow0}\inf_{\text{all legal monsters}}C_\epsilon.
\]

The certificate does not assert \(L_*=B_*\) as rational functions. The output
sets 'exact_germ_optimum' to true only if those two functions are identical.
The finite list of retained normalized bounds is exported by 'proofBounds()'.

A node-limited search or a search stopped at an attack target supplies only its
explicit legal witness. It is not a completed limiting-response certificate.

## Interface and implementation audit

'createAsymptoticSearch(G)' accepts the validated germ oracle factory result.
It returns a subclass of 'G.CaptureSearch' with the same inputs and methods.

The adapter checks the original method text and replaces exactly one known
objective-bound gate. The replacement is rejected if that gate is absent or
nonunique. The original and patched method texts are available in the class's
'audit' object. Every other instruction in the search step is unchanged.

Source dependencies:

- Finite capture-order core:
  51dbac43b59c3041abf831837dc58fde2a9294b2.
- Rational-germ adapter:
  b7e9accdfa1471a6dc4b348e582abbcc9059172b.
- Six regression fixtures:
  771b51772f4138a5dc45403e7c5746dee42f13f0.

## Independent regression

All six existing fixtures were checked in both raw and implicit quantile-sorted
modes against a completed unpruned exact-germ search. The lower and upper
functions bracketed the exact optimum and had the same limiting constant in
all twelve cases.

An additional three-stationary-path fixture was checked in both modes. It
deliberately yields

\[
L_*=\tfrac12-\tfrac13\epsilon,\qquad
B_*=\tfrac12+\tfrac13\epsilon.
\]

The exact germ optimum is \(L_*\), while the limiting optimum is \(1/2\).
The adapter correctly distinguishes these statements. The fourteen checks used
a common recorded radius \(1/96\). A separate two-path avoided-center fixture
also reproduced the exact symbolic response \(3/4+\epsilon/4\).
