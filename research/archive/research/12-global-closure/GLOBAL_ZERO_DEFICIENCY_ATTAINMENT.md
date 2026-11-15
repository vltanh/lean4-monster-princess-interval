# Attained full pressure matching with a uniform horizon

**Sharper horizon corollary (2026-11-13):** the subsequently proved
[sharp outward cutoff](SHARP_OUTWARD_HORIZON_REDUCTION.md) supplies an
optimal input law with center visited by 2 and first endpoint by 4. The
same protected-turn construction below then gives an attained fully
matched optimum with center visited by 2 and both endpoints completed
by 8. The proof below retains its original, valid bounds 3 and 9.


Global theorem, independently reviewed, 2026-11-13.

The global zero-deficiency infimum reduction can be strengthened to an
attained minimum:

\[
 \boxed{
 V=\min\{M(\nu):
    \nu\text{ is symmetric and admits physical causal clocks with a full
    pressure matching},\
    \tau_0\le3,\ \tau_+\le9,\ \tau_-\le9
    \text{ almost surely}\}.}
\]

Here \(M(\nu)=\mathbb E_\nu\tau_-\) is the endpoint baseline.
Consequently some unrestricted optimal Monster law has its stationary
endpoint response active: its worst Princess payoff is exactly \(M=V\).

This is a global structural reduction. It does not determine the
numerical value \(V\), a finite physical support, or a matching optimal
Princess law. The newly proved attainment does not follow from
closedness of an unrestricted endpoint-hitting condition. Its proof
uses a coupling on which every physical path changes at most once.
The construction retains labeled causal kernels throughout iteration;
monotone-clock compression is performed only after the limiting full
matching has been obtained.

## 1. Inputs and the remaining case

[GLOBAL_ZERO_DEFICIENCY_REDUCTION.md](GLOBAL_ZERO_DEFICIENCY_REDUCTION.md) proves the following two physical
constructions.

First, if a normalized finite-mass certificate has positive probability
\(q>0\) on the fastest endpoint-sweep pair, then it can be converted
to full matching without increasing its certified value \(M+d\).
Starting from paths completed by time \(7\), the new law is completed
by time \(9\), and first center visits by time \(3\) are preserved.

Second, when \(q=0\), residual localization gives an interior-start
pair law \(\mu\), with pair representatives \(m\) that hit \(+1\)
first at time \(\sigma\), and measurable residual masses

\[
 0\le r(m)\le\frac12,\qquad
 d=\int r(m)\,\mu(dm).
\]

All these residual units have scoring times in
\([\sigma,\sigma+1)\) and select the first light-coordinate crossing

\[
 h=\inf\{s:s+m(s)\ge1\},
 \qquad 0<h<\min(1,\sigma).
\]

At \(n=2\), define

\[
 \eta=\min\left(\frac12,\frac{\sigma-h}{2}\right),\qquad
 a=\sigma-\eta,\qquad
 \varepsilon=1-m(a),\qquad
 \gamma=r/2.
\]

Then \(0<\varepsilon\le\eta\le1/2\) and \(h<a<\sigma\).
Replace fraction \(\gamma\) of the pair by the fair reflection pair
of the path \(m^a\) that agrees with \(m\) through \(a\), moves directly
to \(-1\), and then moves directly to \(+1\).

Writing

\[
 T=a+2-\varepsilon,
\]

the modified pair's first and second endpoint times are \(T,T+2\).
Its canonical representative, which hits \(+1\) first, is
\(-m^a\). Its first endpoint time increases from \(\sigma\) by

\[
 \Delta=T-\sigma=2-\eta-\varepsilon\in[1,2].
\]

The replacement clocks retain old resources where their pressure
improves. On the reflected orientation they assign the *entire* new
scoring interval

\[
 a\le t<T+2
\]

to the history time \(h\). The selected physical position is

\[
 -m^a(h)=-m(h)=-(1-h)<0.
\]

The accounting in the preceding note gives

\[
 M_{\mathrm{new}}=M+d-A,\qquad
 d_{\mathrm{new}}\le A\le d/2,
\]

after another localization, where
\(A=\int\gamma(\eta+\varepsilon)\,d\mu\).
In particular the total upper certificate does not increase.

## 2. A turned pair is permanently protected

Mark every copy of a turned path pair as protected. Keep this mark
and its original pair label throughout the construction. The mark is
reflection invariant. Conditional on a physical path, keeping such
labels is simply allowing a randomized causal clock; labels can be
forgotten after the final construction.

For the newly turned pair, the first endpoint time is \(T\).
Its only unpaired active orientation is the canonical representative
\(-m^a\), on the interval

\[
 T\le t<T+2.
\]

This whole interval lies inside its frozen negative resource pool
\([a,T+2)\). Every unpaired selected resource of the protected pair
is therefore negative, whether or not that resource is used by the
current matching.

This property is preserved by every operation in
[POST_FIRST_ENDPOINT_PRESSURE_LOCALIZATION.md](POST_FIRST_ENDPOINT_PRESSURE_LOCALIZATION.md):

1. The preliminary clock swaps act only on reflected *paired*
   resources, those with scoring time before the first endpoint.
2. The alternating-kernel rerouting retimes only negative mates of
   paired positive resources. These are again paired resources.
3. Retiming uncovered sources to current time or to the first
   \(U=1\) crossing acts only on positive source fractions.
4. Removing or rerouting matching edges changes no selected position
   on an untouched negative resource.

Thus no operation changes the protected negative unpaired tail.
After localization, every unmatched positive source is unpaired.
It follows that a protected pair carries no residual in every later
iteration.

Changes to other physical pairs can expose previously matched positive
sources on a protected pair. Such sources are necessarily paired;
the alternating resource construction moves any remaining unmatched
mass away from them. It cannot terminate at a protected unpaired
resource because that resource is negative.

Two implementation details are essential:

- Keep the origin and protection labels even if two physical path
  copies happen to coincide. An unprotected copy and a protected copy
  must not have their conditional clocks averaged before the next
  replacement decision.
- Do not apply monotone-clock compression between iterations. It
  preserves the selected-history marginal, but it can redistribute
  selected signs between earlier and later scoring resources. Keep
  causal kernels throughout the iterative construction and compress
  only once, after taking the limit.

The active pressure upper bound holds for these causal kernels:
every selected history time is at most its scoring time. Monotonicity
of the clock is unnecessary for the upper-certificate inequality.

## 3. Iterate only on unprotected original pairs

Start with a normalized certificate of value \(U=M_0+d_0\), with
\(q=0\), first center visits by \(3\), and both endpoints visited by
\(7\). Apply the preceding replacement and localization successively,
always on the labeled unprotected pairs only.

At stage \(k\), every residual-carrying copy is unprotected. Hence the
same accounting applies and yields

\[
 d_{k+1}\le d_k/2,\qquad
 M_{k+1}+d_{k+1}\le M_k+d_k\le U.
\]

In particular \(d_k\le2^{-k}d_0\).

Couple the laws by retaining each sampled pair with probability
\(1-\gamma_k\) and replacing it with probability \(\gamma_k\).
Once replaced, the copy is protected and is never replaced again.
The sign of the representative can be tracked separately so that
the actual oriented physical trajectory agrees with its predecessor
until its turn time.

At fixed \(n=2\), the turn image of an original pair is fixed: its
\(\sigma\), first crossing \(h\), turn time \(a\), and modified path
depend only on that original physical pair. They do not depend on
the iteration number or on the current amount of residual assigned
to that pair.

Therefore every sampled physical path either remains its original
path forever or changes once to one prescribed turn image. In
particular it eventually stabilizes exactly, not merely in the
topology of uniform convergence.

Every original pair has \(\sigma\le5\). Every turned image completes
its second endpoint by

\[
 T+2=\sigma+4-\eta-\varepsilon\le9.
\]

First center visits do not become later. If the original center visit
was before \(a\), it is preserved. Otherwise the new descent reaches
the center at \(a+m(a)\), the earliest possible time from the positive
position \(m(a)\). Reflection has the same center time.

Thus every stage, and its pointwise stabilized limit, satisfies

\[
 \tau_0\le3,\qquad \tau_+\le9,\qquad \tau_-\le9.
\]

The limiting law is carried by the original pairs and their one-turn
images. More precisely, with \(\mu_0\) the original pair law and
\(\mathcal T(m)\) its fixed turn image, it has the pushforward-mixture
representation

\[
 \mu_\infty=(1-\theta)\mu_0+\mathcal T_\#(\theta\mu_0)
 \quad\text{for a measurable }0\le\theta\le1.
\]

Only residual-eligible original pairs need a turn image; set
\(\theta=0\) elsewhere. For an actual finite original bank, this
enlarges the physical pair support by at most a factor of two.
No continuity of \(\mathcal T\), closedness of its image, or finiteness
assumption is needed for the general theorem.

## 4. Total-variation convergence of the active resource bases

Let \(X_k\) be the coupled actual oriented physical path, and \(X_\infty\)
its eventually stabilized limit. Let \(\nu_k,\nu_\infty\) be their
symmetric laws. For bounded measurable test functions \(f\), the active
resource measures are

\[
 \int f\,d\lambda_k
  =\mathbb E\int_0^{\tau_-(X_k)}f(X_k,t)\,dt,
 \qquad
 \int f\,d\lambda_\infty
  =\mathbb E\int_0^{\tau_-(X_\infty)}f(X_\infty,t)\,dt.
\]

On the event \(X_k=X_\infty\), the integrals are identical, including
their endpoint stopping times. On its complement both stopping times
are bounded by \(9\). Therefore

\[
 \|\lambda_k-\lambda_\infty\|_{\mathrm{TV}}
 \le18\,\mathbb P\{X_k\ne X_\infty\}\longrightarrow0.
\]

The harmless convention-dependent factor in total variation has no
effect on the conclusion. This argument never invokes continuity of
the first endpoint hitting-time functional.

The same coupling gives

\[
 M_k=\lambda_k(R)\longrightarrow
 M_\infty=\lambda_\infty(R)\le U.
\]

The limit remains a law of physical paths with the stated horizon and
center properties, and with no endpoint-start mass when \(q=0\).

## 5. The limiting clock is still a physical causal clock

Retain the full selector measure

\[
 \Lambda_k(dm,dt,ds)
 =\lambda_k(dm,dt)\,\kappa_k(ds\mid m,t)
\]

after forgetting the auxiliary labels. Its base marginal is
\(\lambda_k\), and its support obeys \(0\le s\le t\le9\).
The path space is Polish in the topology of uniform convergence on
compact time intervals. Tightness of the base measures, together with
the bounded selector coordinate, makes \(\Lambda_k\) tight.

Pass to a weakly convergent subsequence \(\Lambda_k\Rightarrow\Lambda\).
Its base marginal is exactly \(\lambda_\infty\), by the preceding
total-variation convergence. The causal set \(0\le s\le t\) is closed,
so it still has full measure.

Disintegrating \(\Lambda\) over its base produces a causal kernel on
the actual limiting physical paths. Since the base is

\[
 \nu_\infty(dm)\,\mathbf1_{\{0\le t<\tau_-(m)\}}\,dt,
\]

every selected time satisfies \(s\le t<\tau_-(m)\). In particular

\[
 m(s)\ne-1
\]

almost everywhere. The absence of selected negative-endpoint pressure
is preserved by the exact limiting base, rather than by an invalid
closedness assertion about endpoint avoidance.

The evaluation map
\((m,t,s)\mapsto(s,m(s))\) is continuous. Hence the physical selected
occupation measures converge weakly:

\[
 \alpha_k\Rightarrow
 \alpha=(s,m(s))_\#\Lambda.
\]

Their total mass is \(M_\infty\).

## 6. A limiting matching covers all actual positive pressure

Let \(\mu_{k,+},\mu_{k,-}\) be the positive and negative radial
pressure measures of \(\alpha_k\), and let \(\pi_k\) be the matching
at stage \(k\). Its unmatched positive mass is \(d_k\to0\).

Both matching marginals are dominated by the absolute radial pushforward
of \(\alpha_k\). These pushforwards converge weakly, because
\((s,x)\mapsto(s,|x|)\) is continuous. Thus the matching measures are
tight. Pass to a further subsequence \(\pi_k\Rightarrow\pi\).
The radial containment order is closed, so \(\pi\) is still supported
on

\[
 v\ge u+|s-t|.
\]

Positive and negative pressure splitting is discontinuous at \(x=0\).
Handle that point explicitly. For any continuous compactly supported
test function whose radial support is bounded away from zero, sign
restriction is continuous when pulled back to the signed occupation
space. Since

\[
 \mu_{k,+}-(\pi_k)_1\ge0,\qquad
 |\mu_{k,+}-(\pi_k)_1|=d_k\longrightarrow0,
\]

the first marginal of \(\pi\), restricted to positive source radius,
is exactly the actual positive pressure \(\mu_+\) of \(\alpha\).
The second marginal, restricted to positive target radius, is
dominated by the actual negative pressure \(\mu_-\).

Now restrict \(\pi\) to edges with strictly positive source radius.
The order inequality forces their target radius to be strictly
positive too. The resulting measure \(\pi'\) therefore satisfies

\[
 \boxed{\pi'_1=\mu_+,\qquad \pi'_2\le\mu_-,\qquad
       \operatorname{supp}\pi'\subset\{\text{radial containment}\}.}
\]

It is a full matching of the actual positive pressure. Any extra
zero-radius source or target masses arising in the weak limit are
discarded and have no role in this assertion.

Finally perform conditional monotone-clock compression on
\(\Lambda\). It preserves the selected-history measure on each
physical path, and therefore preserves \(\alpha\) and the full matching.
The resulting law is a genuine zero-deficiency physical certificate
with baseline \(M_\infty\le U\).

## 7. Apply the construction to the unrestricted optimum

The previously proved exact horizon reduction supplies a symmetric
globally optimal law completed by \(7\) with first center visit by \(3\).
Normalize its endpoint tails and take an attaining active-clock dual
certificate and maximal matching. Its value is \(M_0+d_0=V\).

If \(q>0\), the finite positive-sweep construction in
[GLOBAL_ZERO_DEFICIENCY_REDUCTION.md](GLOBAL_ZERO_DEFICIENCY_REDUCTION.md) gives a fully matched law completed
by \(9\), with first center visit by \(3\), and baseline at most \(V\).

If \(q=0\), Sections 2--6 give a fully matched law with the same bounds
and baseline \(M_\infty\le V\).

A full matching makes the worst Princess payoff equal to the endpoint
baseline. No physical law can have worst payoff below the game value.
Thus in either case its baseline equals \(V\), proving the attained
minimum stated at the beginning.

The proof uses earlier attainment of the unrestricted Monster and
active-clock minima. It does not assume that a Princess maximizer
exists, that a finite bank is globally sufficient, or that a bounded
turn count follows from compactness.

## 8. Regression coverage

The accompanying [verify_global_pressure_localization.py](../../packages/interval_global_closure/verify_global_pressure_localization.py) checks the
fractional alternating construction with an explicitly unpaired
negative resource. Its selected clock fraction is unchanged even
though matching edges use that resource.

The physical boundary-turn fixture checks that the entire new
unpaired orientation selects the negative history point and lies
outside the paired region. Together with the resource identities,
these check the protected-tail invariant in the two distinct operations
where it is used. The measure and limiting arguments are proved above.
