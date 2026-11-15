# A globally sufficient incoming-front Princess class

This strengthens the outward-after-time reduction in
SHARP_OUTWARD_HORIZON_REDUCTION.md. The new restriction is global: it
preserves Princess security against unrestricted Monster paths. It is
not inferred merely from improvement against one optimal Monster law.

## 1. Pathwise completion at a characteristic front

Let \(r:[0,\infty)\to[0,1]\) be a legal radial Princess path and let
\(C\ge1\). Put

\[
 T_C(r)=\inf\{t\ge0:t+r(t)\ge C\}.                         \tag{1}
\]

The function \(t+r(t)\) is continuous and nondecreasing. Thus

\[
 C-1\le T_C(r)\le C,\qquad T_C(r)+r(T_C(r))=C.             \tag{2}
\]

The possible time-zero case is \(C=1,r(0)=1\), where (2) still holds.
Define

\[
 (P_Cr)(t)=
 \begin{cases}
 r(t),&t\le T_C(r),\\
 \min\{1,r(T_C(r))+t-T_C(r)\},&t\ge T_C(r).
 \end{cases}                                             \tag{3}
\]

This is legal. It is outward after time \(C\) and is at its endpoint by
time \(C+1\). If the original path stops at its first endpoint, so does
the completed one.

If \(r\le s\) pointwise, then \(T_C(s)\le T_C(r)\). The outer path starts
its maximal outward completion earlier. Before either completion the old
order holds; between the two times its outward completion dominates its
old path; afterward both completions use the same order-preserving
outward evolution. Hence \(P_Cr\le P_Cs\). Applying (3) rank by rank
preserves an ordered Princess law. First-hit times of these continuous
monotone coordinates and the completion maps are Borel, so the transformed
law is well defined. Fair reflection is retained.

## 2. A security inequality against every Monster

Let \(\mu\) be a symmetric ordered Princess law, with security
\[
                         S(\mu)=\inf_m J(m,\mu).
\]
Then
\[
 \boxed{S(P_C\mu)\ge\min\{S(\mu),(C+1)/2\}.}               \tag{4}
\]

Fix an arbitrary legal Monster \(m\) and let \(\tau_0\) be its first
center time, possibly infinite.

### A center visit by C

Suppose \(\tau_0\le C\). Fix one radial target \(r\) and put \(T=T_C(r)\).
If \(|m(0)|\le r(0)\), both uncaught reflected targets are on their
assigned outer sides of the Monster. Maximal outward completion cannot
advance either capture: at a later contact with the completed outer
target, continuity gives an old contact no later.

If \(m(0)>r(0)\), the initially adjacent positive target has already been
caught by \(T\). This is immediate if \(\tau_0\le T\). Otherwise the speed
bound from the known future center visit gives
\[
                m(T)\le\tau_0-T\le C-T=r(T).              \tag{5}
\]
The initial strict order and (5) force a contact by \(T\). Equality is an
actual contact, not an avoided trace. The negative target has remained on
its outer side until any capture. Completion therefore cannot advance
either target's capture. Reflection covers \(m(0)<-r(0)\). Initial
co-location was already capture at time zero.

This proves the pointwise comparison
\[
               J(m,P_C\mu)\ge J(m,\mu)
                          \quad(\tau_0\le C).             \tag{6}
\]

### No center visit by C

If \(\tau_0>C\), the Monster has kept one strict sign throughout \([0,C]\).
The opposite fair half of the Princess law is entirely uncaught. This
includes targets whose radius is zero at time \(C\): the Monster is
strictly on the other side of them.

Every completed path is already moving maximally outward at time \(C\).
The Monster cannot catch an opposite-side target in the interior while
that target continues outward at unit speed. Capture must therefore
occur at the opposite endpoint. Its earliest possible Monster arrival
is \(C+1+|m(C)|\). The other half contributes a nonnegative cost, so
\[
 J(m,P_C\mu)\ge\frac{C+1+|m(C)|}{2}>\frac{C+1}{2}.         \tag{7}
\]

Equations (6) and (7), followed by an infimum over all \(m\), prove (4).
No restriction on the number of Monster or Princess turns, no existence
of an optimal Princess, and no interchange of capture-time limits is used.

## 3. Global consequences

The existing symmetric ordered-law reduction and the certified inequality
\(V<3/2\) imply that \(C=2\) preserves every Princess security. Thus,
without changing the unrestricted game value, every Princess rank may be
required to move maximally outward as soon as it first reaches
\[
                              t+r=2.                     \tag{8}
\]

This is stronger than outward motion only after time two. The whole
region beyond the incoming characteristic in (8) is determined by its
departure distribution.

More generally, if a certified global upper bound is \(1\le U<3/2\), set
\(C=2U-1\). Since \(S(\mu)\le V\le U\), (4) again gives
\(S(P_C\mu)\ge S(\mu)\). The retained n128 upper permits
\[
 C=\frac{94725593551091}{51200000000000}
   =1.85010924904474609375.                               \tag{9}
\]

The subsequently verified n256 upper sharpens the available choice to
\[
 C=\frac{189449329389899}{102400000000000}
   =1.850091107323232421875.                              \tag{9a}
\]
Its retained source and exact independent replay are recorded in
NORMALIZED_GLOBAL_BOUND_CERTIFICATES.md. The older rational choice (9)
and its existing fixtures remain valid.

Using two keeps the front on the usual integer characteristic grid.
Using (9) gives a smaller exact domain. Neither statement supplies an
optimal finite mesh or an exact equilibrium by itself.

## 4. The CDF beyond the front, including atoms

For a radial law, write \(G(U,W)\) for its CDF at
\((t,r)=((U+W)/2,(U-W)/2)\), at interior radii \(0\le r<1\). Define the
random departure coordinate
\[
                         B=2T_C(r)-C\in[C-2,C].
\]
The exact transformed CDF satisfies
\[
 \boxed{G_C(U,W)=\Pr(B\ge W)\quad(U\ge C,\ 0\le r<1).}     \tag{10}
\]

If a rank has not reached the front by the query time, its future
departure has \(B>W\) and it lies below the query point. If it has departed
and has not reached its endpoint, its path is \(r(t)=t-B\), so the CDF
condition is exactly \(B\ge W\). An already-absorbed endpoint rank is above
every interior query; it also has \(B<W\) there. This proves (10).

For \(U<C\) the old CDF is unchanged. A rank that has already crossed the
front has \(t+r(t)\ge C>U\) both before and after completion, so it
contributes to neither CDF at that query.

One must not generally replace (10) by the raw trace \(G(C,W)\). An atomic
rank can linger on the incoming front after its first hit; the original
trace then contains ranks which have already departed under (3).
The correct trace reconstruction, for \(C-2<W\le C\), is
\[
 \Pr(B\ge W)=\lim_{v\uparrow W}\lim_{u\uparrow C}G(u,v).    \tag{11}
\]

Both limits use legal interior query points. The inner incoming trace
at \(v\) lies between \(\Pr(T_C>(C+v)/2)\) and
\(\Pr(T_C\ge(C+v)/2)\). Letting \(v\) increase to \(W\) makes both bounds
converge to \(\Pr(T_C\ge(C+W)/2)\). Thus (11) restores the correct
left-continuous survival representative even at an atom. At \(W=C-2\)
set the survival value to one; at \(W>C\) it is zero. Physical endpoint
CDFs and their interior traces remain distinct.

## 5. Regular fields and a smaller finite synthesis domain

Suppose the source law has no center atom and every interior radial
marginal has density at most \(L\), with a permitted endpoint atom.
For \(C-1\le t<t+h\le C\), the speed bound gives
\[
 \{t<T_C\le t+h\}\subseteq
 \{C-t-2h\le r(t)<C-t\}.
\]
The possible endpoint atom is excluded by the strict upper inequality
when \(t=C-1\). Hence
\[
                  \Pr(t<T_C\le t+h)\le2Lh.                \tag{12}
\]

The departure law has density at most \(L\) on \((C-2,C]\), with only the
possible endpoint atom at \(B=C-2\). In particular there is no interior
front-contact atom. For \(C-2<W<C\), (10) therefore agrees with \(G(C,W)\).
The new field is continuous across the front and has the same interior
spatial density bound: before the front it is unchanged, afterward it
is (10), and the two continuous pieces meet without a jump.

In this regular class the extension is consequently
\[
 G_C(U,W)=
 \begin{cases}
 G(U,W),&U\le C,\\
 G(C,W),&U\ge C,\ C-2<W<C,\\
 0,&W\ge C,
 \end{cases}                                             \tag{13}
\]
with endpoint values interpreted by their prescribed interior traces.
After the front, \(G_U=0\): each nonabsorbed quantile moves outward at unit
speed. Sticky source laws remain sticky.

The established stopped-dithering approximation supplies regular
value-dense Princess laws. For either globally sufficient choice of
\(C\) in Section 3, applying (3) preserves their security by (4) and
preserves the density bound by (12). Thus that regular front class is
also value-dense. This is a global sufficient class, not only a class of
responses to a chosen finite Monster bank.

For a rational P1 source and rational \(C\), the regular extension remains
finite rational P1: cut the source mesh at \(U=C\), retain its part with
\(U\le C\), and extend each affine segment of its boundary trace constantly
in \(U\) until the physical endpoint or center constraints intervene.
All intersections and coefficients remain rational. This reduces the
field domain while retaining the established complete hierarchy; it
does not bound the mesh size needed for exact optimality.

For \(C=2\), this is an additional restriction beyond the existing
outward-after-two nodal polytope. For example, the supplied n1 profile has
radial value zero at \((U,W)=(2,1)\), but interior endpoint trace one at
\((3,1)\). It satisfies the old time-two condition and fails the new
constant-\(U\) extension. The new theorem therefore removes actual
degrees of freedom.

At light-grid nodes, impose equality with the \(U=2\) node having the
same \(W\), and zero for \(W\ge2\). The usual common threshold maps fix
the integer characteristic value two and are monotone. Hence averaging
those maps preserves this nodal extension exactly.

### Direct monotonicity of every nodal record price

There is a stronger discrete statement which does not need an optimal
profile, a minimax passage, or regularization. Give the center radial
value zero and define, on the legal radial node domain,
\[
 (\Gamma_2g)(U,W)=
 \begin{cases}
 g(\min\{U,2\},W),&W<2,\\
 0,&W\ge2.
 \end{cases}                                             \tag{14}
\]

For changed nodes \(U>2\), the projected query is legal when \(W<2\):
the old arena inequality gives \(W\ge U-2>0\), and decreasing \(U\)
decreases the radius. Nodal transport implies \(\Gamma_2g\le g\).
The projection retains both transport orders, the center convention,
and any existing sticky endpoint condition. It also implies the old
outward-after-two identities, so it maps the old normalized nodal
polytope into its front-two subpolytope.

Fix any physical lattice path whose first center visit is at time
\(\tau_0\le2\). A node before that visit satisfies
\[
                     t+|x|\le\tau_0\le2.
\]
Thus every changed node is strictly postcenter. Each still-active
endpoint clock has already seen the center price one, so its running
record is at most one. At a positive spatial node the clock directed
toward the negative endpoint sees price \(1+g\), while the clock directed
toward the positive endpoint sees \(1-g\). Projection decreases the
first price, but it remains at least one and cannot improve its record;
it increases the second price. At a negative spatial node the two
clock roles reverse. Induction along the path therefore gives
\[
 \text{each running record under }\Gamma_2g
 \ \ge\ \text{its record under }g.                       \tag{15}
\]

First visits to the corresponding endpoints deactivate exactly the same
clocks at exactly the same times. Summing the active running records
proves that **every such path's optimal atomic-clock price weakly
increases**. This is about the minimum over causal calendars for each
path; it does not claim that every individually prescribed calendar
plane increases.

Consequently the exact finite-bank optimum is unchanged by restricting
to the front-two nodal subpolytope. One inequality follows from (15),
applied simultaneously to every physical path; the reverse follows from
polytope inclusion. More operationally, any exact all-path price lower
bound already proved for \(g\) remains valid for \(\Gamma_2g\), with the
same scaling. Reusing that lower bound requires checking the exact
projection and binding it to the original certified source. It does not
assert that the old minimum remains attained or attach an old pricing
replay to new field bytes. Existing common-threshold Princess extraction
and global quantization bounds then apply to the projected legal field.

## 6. A sharper height bound in the regular center recurrence

Consider the regular fixed-field center continuation studied in
FINITE_POSTCENTER_RESPONSE.md and CENTER_HEAVIER_FIRST_BALANCE.md,
now for a front-C field with \(1\le C\le2\). From center time \(t<C\), an
outward triangle of height \(h\) has peak light coordinates
\[
                           (U,W)=(t+2h,t).
\]

Once \(h\ge(C-t)/2\), its affected survival record is constant along the
outgoing ray, by (13). If a proper returning triangle exceeds this height,
shorten it to \(h'=(C-t)/2\). The peak record does not change; the two return
times are both at or after \(C\). All ranks are outward after \(C\), so the
remaining center cost at either time is the same two-endpoint-tour cost.
The removed local cost is exactly
\[
                          2(h-h')(l+r'),
\]
where \(l\) is the untouched record and \(r'\) the attained record. It is
nonnegative. Consequently proper returning excursions may be restricted
to
\[
                         0<h\le(C-t)/2.                  \tag{16}
\]

They finish by \(C\), rather than merely having their peaks before the old
outward deadline. The first-endpoint branches and actual contact resets
remain separate, as in the existing exact recurrence. This corollary is
stated for the regular fixed fields covered by that recurrence; no new
universal finite-turn bound for an arbitrary atomic Princess law is
being assumed.

## 7. An exact terminal guard on the postcenter front

Keep the regular-field hypotheses of Section 6. The terminal statement
and its proof work for every \(C\ge1\); they do not use the extra
\(C\le2\) restriction of that section's recurrence discussion.
Consider a state after the Monster has visited the center, at the positive incoming front
\[
              U=C,\qquad t=C-x,\qquad 0\le x\le1,
\]
with surviving negative and positive masses \(l,r\le1/2\), respectively.
The exact remaining cost is
\[
 \boxed{\min\{(3-x)l+(1-x)r,\ (1+x)l+(3+x)r\}.}          \tag{17}
\]
Reflection gives the corresponding negative-front formula.

Until the next center or positive-endpoint visit, \(U\ge C\) and \(W\)
is nondecreasing. The radial field is \(G(C,W)\), which is nonincreasing
in \(W\). Hence the positive-survivor price \(1-F\) cannot improve its
stored record. The negative-survivor price \(F\) remains at least
\(1/2\), so it cannot improve the already registered record \(l\le1/2\)
either. There are no interior captures on this interval.

If the next exit is the positive endpoint, its earliest arrival is after
\(1-x\). The earliest subsequent center time is
\(C+2-2x\ge C\). After time \(C\) all ranks move maximally outward, so
the negative survivors can only be caught at their endpoint. The direct
positive-then-negative endpoint tour therefore has the first cost in
(17), and no continuation taking that exit order can improve it.

If the next exit is the center, its earliest arrival is after \(x\), at
time \(C\). The regular field has no center atom. The records are
unchanged and the remaining center value is
\(\min\{3l+r,l+3r\}\). Returning to the center and then choosing the
positive endpoint first costs \((x+3)l+(x+1)r\); this exceeds the direct
positive-first cost by \(2x(l+r)\). The center-then-negative-first choice
gives the second cost in (17). The two direct endpoint tours attain the
displayed minimum, proving the claim.

This is a postcenter terminal condition. A precenter state need not have
both records at most one-half, and an arbitrary atomic law may have an
uncaught center atom. Neither is covered by (17). For a projected nodal
profile, the same argument applies to the two stored atomic-clock records
in their doubled units, using center price one. Thus exact grid pricing
may terminate when the center flag is true and
\(t+|x|\ge2\), scanning only the two direct endpoint tours. This is an
algorithmic consequence of the proved front identities, not a new
pricing computation claimed here.

## 8. A global Monster decision-front normal form

The preceding regular terminal guard also gives an unrestricted Monster
class reduction. It is not only a best-response statement for one fixed
CDF. For a symmetric Monster law write
\[
                         K(\nu)=\sup_\mu J(\nu,\mu).
\]
Fix \(C\ge1\). There is a measurable reflection-equivariant
normalization \(N_C\) of every Monster law supported on paths with
\(\tau_0\le C\) such that
\[
                         K((N_C)_\#\nu)\le K(\nu).       \tag{18}
\]
Every normalized path branches only until its first endpoint or its
first postcenter hit of \(t+|m(t)|=C\), whichever comes first, and then
takes a direct endpoint tour. Its first endpoint is reached by \(C+1\),
and both endpoints are completed by \(C+3\).

### The normalization is one common physical map

For a path with \(\tau_0\le C\), let \(\sigma\) be its first endpoint
time, allowing infinity, and put
\[
 T=\inf\{t\ge\tau_0:t+|m(t)|\ge C\}.
\]
Since \(t+|m(t)|\) is continuous and nondecreasing,
\[
             \tau_0\le T\le C,\qquad T+|m(T)|=C.          \tag{19}
\]
The restriction \(t\ge\tau_0\) matters when a path approaches its first
center visit along a plateau of the incoming characteristic.

If \(\sigma\le T\), retain the path through that endpoint and sweep
directly to the opposite endpoint. The usual endpoint comparison shows
that this captures every Princess no later, without a front or regularity
assumption. It also preserves center visitation by \(C\): if the center
has not already been visited, the new sweep reaches it at
\(\sigma+1\le\tau_0\le C\).

If \(T<\sigma\), retain the prefix through \(T\), then take the direct
two-endpoint tour in the order of the old path's first endpoint visits.
There are no already-visited endpoints in this branch. If only one old
endpoint is ever visited, put it first; if neither is visited, either
order can be used. A fair coin resolves a completely symmetric tie.
The center visit lies in the unchanged prefix.

All first-hit times here are Borel functions on continuous path space.
For example, the event of hitting a given closed target by a fixed time
is determined by the minimum distance on that compact interval.
More explicitly, if \(\alpha_C\) is the first hit of
\(t+|m(t)|\ge C\), monotonicity gives
\(T=\max\{\tau_0,\alpha_C\}\), including the precenter plateau case.
Comparisons of these extended-real times, evaluation at finite hitting
times, and concatenation with the finitely specified unit-speed legs
are Borel operations. The choices above are equivariant under reflection,
including their tie coin. Thus this is a single measurable kernel on
physical paths and its image of a symmetric law is symmetric; it does
not depend on the Princess law.

### Simultaneous domination on the regular front class

Fix a regular sticky front-C Princess law. In the front branch, the
Monster is postcenter at \(T\). Section 7 shows that every still-uncaught
rank can subsequently be caught only at its endpoint: before the next
center or same-side endpoint no record improves, and any next center
visit occurs at or after \(C\). The absence of a center atom is used
here. The replacement reaches both endpoints no later than any old
continuation with the same endpoint order. Thus
\[
                  J(N_Cm,\mu)\le J(m,\mu)               \tag{20}
\]
simultaneously for every regular sticky front-C law \(\mu\).
The endpoint branch already has this comparison for every Princess.

Actual endpoint arrival is consistent with this record argument. For
\(x=m(T)>0\), every positive survivor is strictly above \(x\) and has
already crossed its own incoming front, so it reaches \(+1\) before the
Monster's earliest arrival there. Every negative survivor is endpoint
absorbed by \(C+1\), no later than any Monster arrival at \(-1\) from
\((T,x)\). Reflection handles \(x<0\). At \(x=0,T=C\), all survivors
are already moving outward. Hence the endpoint-tour comparison is a
comparison of actual captures, not merely formal endpoint times.

### Passing from regular Princesses to all Princesses

Let \(\nu'=(N_C)_\#\nu\), and start with an arbitrary legal Princess
law. Because \(\nu'\) is symmetric, the established symmetrization,
common-quantile ordering and first-endpoint stopping reductions give a
symmetric ordered sticky radial law \(\bar\mu\) whose payoff against
\(\nu'\) is at least the original payoff.

Apply stopped outward radial dithering to \(\bar\mu\). The raw dithered
paths converge uniformly on compact time intervals to the original
sticky paths under their defining coupling. They have no center atom,
interior density at most \(1/\delta\), and the permitted endpoint atom.
Common-quantile reordering gives regular sticky laws \(\mu_\delta\)
and can only increase their payoff against \(\nu'\). Lower
semicontinuity of first capture and Fatou's lemma therefore give
\[
             J(\nu',\bar\mu)
                    \le\liminf_{\delta\downarrow0}
                                      J(\nu',\mu_\delta).\tag{21}
\]
No convergence of the reordered paths is needed: the raw coupled
dithers supply (21), and reordering only increases its right side.

Both \(\nu\) and \(\nu'\) visit the center by \(C\). By the pathwise
front comparison (6), regularity preservation (12), and (20),
\[
 \begin{aligned}
 J(\nu',\mu_\delta)
 &\le J(\nu',P_C\mu_\delta)\\
 &\le J(\nu,P_C\mu_\delta)\\
 &\le K(\nu).
 \end{aligned}                                           \tag{22}
\]
Combining (21) and (22) proves (18). There is no new restricted minimax
interchange, no assumed Princess attainment, and no removal of a positive
late-center set by an unjustified uniform limiting gap. In particular,
(20) is not asserted for an arbitrary center-atomic front law; the
regularization argument is what proves the all-Princess upper statement.

### Timing and optimal-law consequences

In the endpoint branch one has \(\sigma\le C-1\). If the center precedes
the endpoint, monotonicity and \(\sigma\le T\) give
\(\sigma+1\le C\); if the endpoint precedes the center, the distance
one to the center gives \(\sigma+1\le\tau_0\le C\). This branch
therefore completes by \(C+1\).

In the front branch, put \(x=m(T)\). The first endpoint is at distance
at most \(1+|x|\), and a two-endpoint tour has length at most
\(3+|x|\). Equation (19) gives the claimed bounds \(C+1\) and \(C+3\).

Section 3 of SHARP_OUTWARD_HORIZON_REDUCTION.md proves that every globally
optimal Monster law satisfies \(\tau_0\le2V-1\) almost surely, using
near-optimal Princess laws and the opposite-half lower bound. It needs
no optimal Princess. Starting from the previously established optimal
symmetric Monster law, take any \(C\ge\max\{1,2V-1\}\) and apply
(18). The resulting law remains globally optimal and has the decision
front just described. In particular:

* \(C=2\) permits a global optimal law with first endpoint by three and
  completion by five.
* The retained certified n128 upper permits the rational choice (9),
  first endpoint by
  \(145925593551091/51200000000000\), and completion by
  \(248325593551091/51200000000000=4.85010924904474609375\).
* The current n256 upper permits (9a), first endpoint by
  \(291849329389899/102400000000000\), and completion by
  \(496649329389899/102400000000000=4.850091107323232421875\).
* The theoretical choice \(C=2V-1\) gives first endpoint by \(2V\) and
  completion by \(2V+2\). The known certified lower bound \(V>1\)
  ensures that this choice satisfies the required \(C\ge1\).

For a unit light lattice with \(C=2\), the front hitting times and all
new endpoint legs remain on that same lattice. Consequently the exact
finite physical bank may likewise be restricted to this earlier
decision front without changing its minimax value. The original finite
bank is closed under the normalization, and (18) supplies the required
law-by-law comparison. This improves the physical prefix domain as well
as the Princess field domain; it still allows arbitrary legal continuous
prefixes in the unrestricted game and does not prove a finite-dimensional
equilibrium family.

## 9. Exact targeted regression

The standard-library replay uses ten radial paths, including center and
endpoint atoms, an incoming-front plateau, and a slow front approach,
against 32 physical Monster paths. With \(C=1,3/2,2\), it checks 580
early-center signed-pair comparisons, 380 late-center endpoint floors,
and 99 ordered-completion comparisons. It also checks 8,160 exact
departure-distribution queries and both distinct atomic trace pitfalls
in Section 4.

These fixtures test the physical and trace conventions; the universal
claims follow from the proofs above. Run

    python -B packages/interval_global_closure/verify_incoming_front_completion.py \
      --report packages/interval_global_closure/incoming_front_completion_replay.json

The replay imports the existing Fraction chronological-intersection
helpers from verify_boundary_layer_kernel.py beside it.
