# Independent audit of the history-selector physical realization

This note audits the linear marginal functional compiled from causal
history selectors and the query/fill representation proposed for its
supremum. It is not a claim that one fixed selector equals the original
record functional for every Princess law.

## 1. Selector signs and exact contact traces

On a right-moving unit Monster leg of duration d, choose a causal old lower
point L, a causal old upper point H, and a cut after time d0. The selector
plane is

\[
 d[1+F^-(L)]-d_0F^+(H)-\int_{\mathrm{cut}}^{\mathrm{end}}F^+(\mathrm{current})\,dt.
\]

For a left-moving unit leg it is

\[
 d[1-F^+(H)]+d_0F^-(L)+\int_{\mathrm{cut}}^{\mathrm{end}}F^-(\mathrm{current})\,dt.
\]

Each chosen point is an available operand of the running minimum or maximum,
so these are majorants of the exact survival integral. Choosing the actual
record points and switch makes the appropriate plane tight. Nonnegative
mixture weights preserve the point-term form

\[
 -aF^++bF^-,\qquad a,b\ge0.
\]

For a fair radial pair +/-p, exact contact cannot improve this point reward
over either adjacent noncontact value. At x>0, the three rewards for
p<x, p=x and p>x are

\[
 -a+b,\quad -a+b/2,\quad(-a+b)/2.
\]

At x<0 they are

\[
 0,\quad-a/2,\quad(-a+b)/2.
\]

At x=0 the contact value is -a, whereas p>0 gives (-a+b)/2.
At an arena endpoint only the inward perturbation is available, and the
same inequality holds. Thus endpoint and center contacts do not hide a
larger selector supremum. This is the relevant sign fact; arbitrary
unary jumps would not justify dropping exact contact labels.

Folding a signed Princess path to its absolute value preserves its fair
reflected one-time marginal. Since the selector plane is linear in that
marginal, its supremum over laws reduces to the supremum over one legal
deterministic radial pair.

## 2. Inverse coordinates and all factors

For a nonnegative path put U=t+p(t), V=t-p(t). A continuous nondecreasing
inverse graph U=P(V) lies in

\[
 \max(V,0)\le P(V)\le V+2.
\]

A virtual initial point (V,P)=(-1,0) is harmless. Trim the resulting graph
at its unique crossing of t=(P+V)/2=0. Thereafter
p=(P-V)/2 is in [0,1] and has speed at most one. Extend its final radial
position constantly if additional query times remain.

For a noncontact point (t,x), with u=t+|x| and v=t-|x|,

\[
 A=1_{\{P(v)>u\}},\qquad
 F(t,x)=
 \begin{cases}
 1-A/2,&x\ge0,\\
 A/2,&x<0.
 \end{cases}
\]

Hence a point coefficient c gives unary Above coefficient
-sign(x)c/2, plus its constant term. A unit Monster ray is split at the
center. A radial-outward piece fixes V and has dU=2dt; a radial-inward
piece fixes U and has dV=2dt. Both therefore give Above coefficient
-sign(x)c/4 in the corresponding horizontal or vertical integral.

At x=0 either sign convention produces 1/2 for a noncontact radial pair.
Contact is handled by Section 1 rather than silently choosing a half-mass
value.

## 3. Arbitrary-sign interval fills

Make V cuts at every point/horizontal query and vertical interval endpoint;
make U cuts at every point/vertical threshold and horizontal endpoint.
Close the finite bounded grids under U=V, U=V+2 and their inverse shifts.
Include V=-1 and U=0. Finite closure follows because only shifts by 2 are
introduced within bounded ranges.

For consecutive V cuts a<b, there is no priced U strictly inside either
(a,b) or (a+2,b+2). The vertical objective on that open cell is

\[
 \int_a^b g(P(V))\,dV,
 \qquad
 g(z)=\sum_j w_j1_{\{z>U_j\}},
\]

with completely arbitrary signed weights w_j.

Given valid ordered query levels q_a<=q_b, any admissible P is bounded
between them. Choose a feasible threshold pattern attaining the maximum
of g on that range. It can be represented by a scalar c between q_a and
q_b and maintained throughout the open interval by

\[
 P_c(V)=\min(V+2,\max(V,0,c)).
\]

The moving lower and upper clips cross no priced threshold in the open
cell, so g(P_c(V)) is constant at the chosen best value almost everywhere.
The clipped profile stays between the endpoint query levels:
V+2>=a+2>=q_a and max(V,0)<=max(b,0)<=q_b. This proves the one-fill-scalar
reduction without any sign or concavity restriction on g.

The scalar fill's relaxed physical bounds are
max(a,0)<c<b+2, interpreted by the appropriate endpoint sides.
They are deliberately wider than either query row's bounds.

Horizontal integrals are clipped ramps of the query level. On each open
U-label cell the query objective is affine. With scalar order constraints,
one must push an entire equal-level order block, or use the vertices of
the corresponding order polytope; independent coordinate pushing is not
a valid explanation when neighboring variables are tied. Every vertex
uses U-cell endpoints. Together with both one-sided point values, this
gives the common ordered labels U_j- and U_j+.

The exact label backend accepts arbitrary signed unary tables. Its
within-row threshold chains and adjacent-row implications are precisely
the scalar-order constraints after bound propagation. This audit does
not replace its independent maximum-closure proof.

## 4. Ordinary rational physical realization

For a finite label assignment choose a positive rational delta smaller
than both one quarter and one quarter of the minimum grid gap. Realize
U_j- and U_j+ by U_j-delta and U_j+delta. The virtual initial row alone
uses the exact label P(-1)=0.

Put eta=delta^2. On [a+eta,b-eta] use the clipped constant fill, and join
its endpoints linearly to the prescribed query values at a and b.
These bridges are nondecreasing and stay in the convex physical cone.
All query values are off the priced U thresholds.

A constant bridge cannot create a priced vertical tie because its query
endpoint is off-threshold. A diagonal boundary piece meets a fixed priced
U only at an isolated V. Thus the required point bits are realized exactly,
horizontal ramp errors are bounded by

\[
 \delta\sum|\hbox{horizontal coefficients}|,
\]

and vertical bridge errors by

\[
 2\eta\sum_{\rm cells}\sum_{\rm active\ thresholds}|w_j|.
\]

After trimming the negative-time prefix, the result is an ordinary legal
radial polygonal path. No strict-speed mixture is required. The errors
tend to zero, so the label value is the actual supremum of the selector
functional.

This is a supremum statement. An unsmoothed jump of P may run along a
priced horizontal characteristic; its exact contact payoff can be lower
than the approaching rewards. The continuous bridge realizes the chosen
query level inside such a would-be jump and avoids that mistaken
attainment claim.

## 5. Independent exact checks

verify_selector_realization_audit.cjs uses rational BigInt arithmetic and
does not invoke the compiler or the ordered-label optimizer. It builds
84 legal alternating query/fill assignments on a closed half-integer
grid, realizes each by the preceding bridges, trims it to physical time,
and evaluates its radial path directly.

It checks:

- 112 exact-contact versus adjacent-side inequalities;
- 3,693 physical cone and speed inequalities;
- 4,872 signed physical point identities;
- 14,112 clipped-fill and signed vertical-error inequalities;
- 4,704 horizontal-ramp error inequalities;
- direct integration over 4,503 physical vertical-ray pieces and
  5,011 physical horizontal-ray pieces.

For both ray orientations the independent integrator evaluates
p(t)-|x(t)| from the physical path; it does not re-use inverse-graph
threshold values. The deterministic perturbations are delta=1/128 and
eta=1/16384. These finite fixtures test the stated ingredients; the
arbitrary-field claim rests on the preceding grid, order-polytope and
realization arguments. The complete physical selector compiler is checked separately in Section 6.

Independent backend inspected:
signed_label_closure source blob
198116dd73d64d23fdbdbdf76760c50de2b86cf1 and proof note
734722a5b40ec2626fdb1e6f81ca3170cf31f58f.

## 6. Independent compiler replay

The draft compiler audited here is blob
8a6926549004f5739b207e41ddd9167f6784584f.
verify_selector_compiler_independent.cjs accepts that source as an argument:

\[
 \mathrm{Function(auditSource)().verify(compilerSource)}.
\]

Its rational arithmetic, label optimization and physical scoring are
independent of the compiler's scorer and the maximum-closure engine.
The label optimizer uses the exact recurrence

\[
 D_i(k)=f_i(k)+\max_{j\le k}D_{i-1}(j)
\]

with the stated row bounds. A prefix maximum computes it in linear time
per row; arbitrary unary signs are allowed.

Eight weighted selector mixtures, with cuts at leg starts, thirds,
midpoints and ends, pass all of the following:

- literal original route-plane evaluation equals the compiled source terms;
- direct physical CDF integration equals the compiler's realized score;
- every selector plane majorizes actual chronological pair first capture;
- the realized score lies between the exact label supremum minus its
  proved error and the supremum itself.

The replay checks 89 source points and 133 physical ray pieces. For each
of the eight realized Princess paths, it additionally constructs tight
selectors for five completed Monster routes. All 40 selector values equal
the independent chronological first-capture averages exactly.

A final adversarial fixture cancels all off-contact point and ray terms by
pairing positive strict coefficients with negative closed coefficients.
The compiler must retain that geometry: at an exact contact the unmerged
functional would still be adverse. The realized path avoids the four
distinct retained point queries and all priced characteristic ties. Its
label value, physical score and error bound are all exactly zero.

These tests confirm the present compiler integration. The theorem remains
a supremum of a fixed linear causal-selector plane. A selector is tight
only for fields whose actual records it represents; maximizing one plane
is not, on its own, an unrestricted response theorem for a whole Monster
mixture.
