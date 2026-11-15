# Global localization of unmatched pressure after the first endpoint

Global theorem, independently reviewed, 2026-11-13.

**Theorem:** For any symmetric physical Monster law of finite active mass,
and any causal-clock/pressure-matching certificate, the clocks and matching
can be replaced, on the same physical law, without increasing deficiency,
so every unmatched positive unit comes from a scoring time after that
path's first endpoint visit. Retiming just those unmatched units to their
current scoring positions then puts all residual positive pressure on
the chronological positive part of the post-endpoint continuation.

For a law with the universally dominant immediate opposite-endpoint
sweep after its first endpoint, the residual first lies on the family of
descending fronts \(t+u=1+\sigma\), where \(\sigma\) is that path's
first-endpoint time. A second retiming of only the unmatched resources
puts all residual on the single initial front \(t+u=1\).

This is a global theorem for arbitrary laws and clocks, including
continuous supports and atoms. The final front measure can have atoms
at any strictly positive front time. It need not be bounded by the
chronological density of the endpoint-start sweep component.

## 1. Scoring resources and the reflected partner

Let \(\nu\) be a symmetric law of continuous legal Monster paths with

\[
 M=\mathbb E_\nu\tau_-<\infty,\qquad
 \tau_\pm(m)=\inf\{t:m(t)=\pm1\},\quad
 \sigma(m)=\min(\tau_-(m),\tau_+(m)).
\]

Symmetry also gives \(\mathbb E\tau_+<\infty\), so both endpoints
are eventually visited almost surely.

Use the finite scoring-resource measure

\[
 R=\{(m,t):0\le t<\tau_-(m)\},\qquad
 \lambda(dm,dt)=\nu(dm)\,dt.
\]

The paired resource region is

\[
 R_{\mathrm{pair}}=\{(m,t):t<\sigma(m)\}.
\]

On this region, \(J(m,t)=(-m,t)\) is a measure-preserving involution.
Every resource outside \(R_{\mathrm{pair}}\) belongs to a path whose
first endpoint is \(+1\); its reflected resource has already been killed
at its first \(-1\) visit.

Take an existing deterministic causal clock \(s(r)\le t(r)\).
Such clocks suffice by the monotone-clock compression theorem.
Write

\[
 x(r)=m_r(s(r)),\qquad
 P=\{r:x(r)>0\},\quad N=\{r:x(r)<0\},\quad Z=\{r:x(r)=0\}.
\]

The selected positive and negative radial locations are respectively

\[
 f_+(r)=(s(r),x(r)),\quad r\in P,
 \qquad
 f_-(r)=(s(r),-x(r)),\quad r\in N.
\]

If the given clock is a kernel, it may first be determinized by the
existing compression theorem. Alternatively add an auxiliary unit
interval to each scoring resource and let \(J\) preserve that auxiliary
coordinate. All arguments below are unchanged.

## 2. Lift the matching to the scoring resources

Disintegrate \(\lambda|_P\) and \(\lambda|_N\) over \(f_+\) and
\(f_-\). Lifting a pressure matching through these conditional laws gives
a resource coupling

\[
 \Pi\ge0,\qquad
 \Pi_1\le\lambda|_P,\qquad
 \Pi_2\le\lambda|_N,
\]

supported on

\[
 f_+(p)\preceq f_-(n).
\]

This lift retains the matching's total mass exactly. Its unmatched
positive resource measure is

\[
 u=\lambda|_P-\Pi_1.
\]

The matching deficiency represented by this certificate is \(u(R)\).
The matching need not initially be maximal.

## 3. A harmless clock-swap preprocessing

Consider a reflected paired resource pair \(r,Jr\) whose two selected
positions are both nonnegative. Swap their selected history times:

\[
 s_{\mathrm{new}}(r)=s(Jr),\qquad
 s_{\mathrm{new}}(Jr)=s(r).
\]

The two scoring times coincide, so both new choices remain causal.
Since the physical paths are reflections, the new selected positions are

\[
 x_{\mathrm{new}}(r)=-x(Jr)\le0,\qquad
 x_{\mathrm{new}}(Jr)=-x(r)\le0.
\]

Thus every positive source in these pairs disappears, and no old negative
selected resource is changed. Remove the original matching edges
incident to the disappearing positive sources. Their former negative
partners merely become unused; every surviving positive source keeps
all of its old partners. Deficiency cannot increase.

Perform this swap on the reflection-invariant measurable set of all
such pairs simultaneously. Both-center pairs do nothing.
After this preprocessing,

\[
 \boxed{
 p\in P\cap R_{\mathrm{pair}}\quad\Longrightarrow\quad Jp\in N.}
\]

Rename the resulting clock, sign regions, and lifted matching
\(s,P,N,\Pi\). The key property now eliminates collisions between
positive sources and the negative resources that will be retimed.

## 4. A sub-Markov kernel for simultaneous alternating rerouting

Disintegrate the matching with respect to the entire negative resource
measure:

\[
 \Pi(dp,dn)=k(n,dp)\,\lambda|_N(dn),
 \qquad k(n,P)\le1.
\]

The missing kernel mass represents unused negative capacity.
Let \(P_{\mathrm{pair}}=P\cap R_{\mathrm{pair}}\), and define

\[
 K(p,A)=
 \begin{cases}
 k(Jp,A),&p\in P_{\mathrm{pair}},\\
 0,&p\in P\setminus R_{\mathrm{pair}}.
 \end{cases}
\]

For a measure \(\eta\) on \(P\), write
\(K_*\eta(A)=\int K(p,A)\,\eta(dp)\).
Reflection invariance gives, for every measurable \(A\subset P\),

\[
 K_*(\lambda|_P)(A)
 =\int_{J(P_{\mathrm{pair}})}k(n,A)\,\lambda|_N(dn)
 \le\Pi_1(A).
\]

Since \(u=\lambda|_P-\Pi_1\),

\[
 \boxed{u+K_*(\lambda|_P)\le\lambda|_P.}
\]

Consequently the increasing partial sums

\[
 \xi_n=\sum_{j=0}^{n}K_*^j u
\]

are all bounded above by \(\lambda|_P\).
Their monotone limit

\[
 \xi=\sum_{j=0}^{\infty}K_*^j u\le\lambda|_P
\]

is a finite measure and satisfies

\[
 \boxed{\xi=u+K_*\xi.}
\]

This is the finite-measure replacement for an alternating-path
termination argument. It directly handles partially matched resources
and branching transport kernels; no unproved purification to a pointwise
bijection is needed. In particular,
\(\sum_j|K_*^ju|\le\lambda(P)<\infty\), so the mass of paths still
continuing after \(j\) reroutings tends to zero.

## 5. The exact new clocks and matching

Split \(\xi=\xi_{\mathrm{pair}}+\xi_{\mathrm{tail}}\) according to
paired versus unpaired positive resources. Define the negative resource
submeasure

\[
 \zeta=J_*\xi_{\mathrm{pair}}\le\lambda|_N,
 \qquad a(n)=\frac{d\zeta}{d(\lambda|_N)}(n)\in[0,1].
\]

At a negative resource \(n\), retain the old selected time with
probability \(1-a(n)\). With probability \(a(n)\), select the old
history time of its positive reflected mate \(Jn\).
This new time is at most the same scoring time, so the new kernel is
causal. Its new selected position is the negative of the old selected
positive position of \(Jn\).

Remove from the old matching the target fraction \(a(n)\):

\[
 \Pi_{\mathrm{remove}}(dp,dn)=a(n)\Pi(dp,dn).
\]

Its first marginal is exactly

\[
 (\Pi_{\mathrm{remove}})_1=K_*\xi=\xi-u.
\]

The retained matching has first marginal

\[
 \Pi_1-(\xi-u)=\lambda|_P-\xi,
\]

and second marginal at most
\((1-a)\lambda|_N\), so it fits the unchanged fraction of each old
negative selected resource.

Now add the internal matching that sends each positive resource
\(p\), with mass \(\xi_{\mathrm{pair}}(dp)\), to its retimed negative
mate \(Jp\). Their selected radial spacetime points coincide exactly,
so every new edge satisfies the causal order on equality.

The resulting positive matching marginal is

\[
 (\lambda|_P-\xi)+\xi_{\mathrm{pair}}
 =\lambda|_P-\xi_{\mathrm{tail}}.
\]

Thus precisely \(\xi_{\mathrm{tail}}\) remains unmatched.
Its mass is no greater than the old deficiency:

\[
 |\xi_{\mathrm{tail}}|
 =|u|+|K_*\xi|-|\xi_{\mathrm{pair}}|
 \le |u|,
\]

because \(K\) vanishes off \(P_{\mathrm{pair}}\) and is substochastic.

No chronological resource has been added or deleted. The physical
Monster law and active mass \(M\) are unchanged. All modifications are
causal history selections on existing paths.

## 6. Move only the unmatched units to current time

The remaining unmatched resource measure is supported on scoring times
after the first endpoint. Its density is at most one with respect to
the original scoring measure.

For just those unmatched units, replace their selected history time
by their current scoring time \(t\). This is causal. No existing matched
source or partner is changed, because these source units were uncovered.
If \(m(t)>0\), leave the new positive source unmatched. If \(m(t)=0\)
or \(m(t)<0\), the old positive source disappears and no new positive
source is created, so deficiency decreases.

There is no claim that this retiming is downward in the cone order.
No such claim is needed: it applies only to uncovered positive sources,
whose contribution to the certificate is their mass.

If deterministic nondecreasing clocks are desired, perform conditional
quantile compression after these changes. It preserves each path's
selected-history measure and therefore preserves the pressure measure
and its matching.

## 7. Consequence for globally optimal laws

Endpoint-tail dominance permits a symmetric global Monster optimum to
be chosen with an immediate unit sweep to the opposite endpoint after
the first endpoint. Apply the exact fixed-law clock dual and a maximal
pressure matching, then the preceding construction.

Any decrease in \(M+d\) would contradict global optimality.
Hence a global optimal certificate exists whose residual positive
pressure admits a path/scoring-time lift \(\rho\) satisfying

\[
 \rho(dm,dt)\le
 \mathbf1_{\{\tau_+(m)=\sigma(m),\,
                 \sigma(m)\le t<\sigma(m)+1\}}
 \,\nu(dm)\,dt,
\]

and whose pressure location is

\[
 \boxed{(t,u)=(t,1+\sigma(m)-t).}
\]

All residual therefore lies on descending characteristic fronts
\(t+u=1+\sigma(m)\). For endpoint-start sweeps, \(\sigma=0\), and
this is the initial fast-sweep front used by the explicit continuum
completion theorem.

The preceding statement records a useful path/scoring-time lift and
will be used below. The delayed fronts themselves need not be retained.

## 8. A second retiming puts every residual on the initial front

For a path whose first endpoint is \(+1\), define

\[
 h(m)=\inf\{s\ge0:s+m(s)\ge1\}.
\]

The function \(s\mapsto s+m(s)\) is continuous and nondecreasing.
It starts at \(m(0)\le1\), and at the first endpoint time \(\sigma\)
it is \(1+\sigma\). Consequently \(h\le\sigma\), and

\[
 m(h)=1-h.
\]

Retiming an unmatched resource with scoring time \(t\ge\sigma\)
to \(h\) is therefore causal. If \(h<1\), its new positive location is

\[
 z_h=(h,1-h),
\]

on the initial front. If \(h\ge1\), its old positive source becomes
center or negative pressure and disappears from the residual.
Existing matches are unaffected: only previously uncovered source
units have been retimed.

For \(0<m(0)+1<2\), continuity gives \(h>0\).
For any interior-start path with \(\sigma>0\), continuity and
\(\sigma+m(\sigma)>1\) also give \(h<\sigma\).

Endpoint-start pairs are handled separately. Normalize their physical
paths to the immediate unit sweep, and choose their active clocks to
be current time before the localization construction. On the descending
sweep, current time minimizes the selected value for every legal
Princess CDF; equivalently positive sources move downward and negative
partners move upward in the pressure order. Thus this canonicalization
does not increase deficiency. The construction in Sections 3--5 retimes
negative resources only in the paired region, which is empty on an
endpoint-start sweep. Its current clock is therefore preserved.

In the final front retiming, leave the uncovered sweep resources at
their current times. Their pressure is already on \(z_t\), \(0<t<1\).
Do not move these resources back to their first crossing \(h=0\).
Their scoring measure is Lebesgue measure, so they have no atom at zero.

It follows that every finite-mass certificate can be replaced, without
increasing its bound, by one whose residual is a finite measure
\(\rho\) on the front indexed by \(0<t<1\). It has no atom at zero.
The physical path measure and baseline remain unchanged.

Let \(q\) denote the total probability of the fair fast-sweep pair.
The residual decomposes as

\[
 \rho=\rho_{\mathrm{sweep}}+\rho_{\mathrm{int}},
 \qquad
 \rho_{\mathrm{sweep}}\le\frac q2\,dt,
 \qquad
 d_{\mathrm{sweep}}\le\frac q2.
\]

The interior part has a physical pair/scoring-time lift. If the pair
representative \(m\) is chosen to hit \(+1\) first, its residual arises
only from scoring times \(\sigma\le t<\sigma+1\), and is then selected
at \(h(m)\). Therefore, if \(\mu\) is the probability law of such pair
representatives, there is a measurable \(r(m)\in[0,1/2]\) with

\[
 \rho_{\mathrm{int}}
   =\int_{\{|m(0)|<1,\ h(m)<1\}}
         r(m)\,\delta_{h(m)}\,\mu(dm),
 \qquad
 d_{\mathrm{int}}=\int r(m)\,\mu(dm).
\]

Here the factor \(1/2\) is the probability of the orientation whose
active lifetime continues after the first endpoint. This lift, and not
an assumed density of \(\rho_{\mathrm{int}}\), is what the later
physical boundary-turn construction uses.

All resource-level operations precede any final clock compression.
Conditional monotone-clock compression then preserves each physical
path's selected-history measure, and hence all pressure and matching
identities above.

## 9. What has and has not been proved

The initial-front localization is unconditional for finite active mass.
It does not assert that the residual is supplied by the fast sweep,
or that \(\rho\le q\,dt/2\). Interior starting paths can contribute
arbitrary atoms on the same front.

The companion note [GLOBAL_ZERO_DEFICIENCY_REDUCTION.md](GLOBAL_ZERO_DEFICIENCY_REDUCTION.md) proves a
completion for arbitrary front measures when \(q\ge d/2\), then removes
that inequality whenever \(q>0\) by an explicit physical boundary-turn
modification. As a consequence it proves the unconditional identity
\(V=\inf_{D=0}M\), while distinguishing this infimum statement from
attainment of a zero-deficiency global optimizer.

The [subsequent protected-tail limit](GLOBAL_ZERO_DEFICIENCY_ATTAINMENT.md)
closes the attainment distinction: an optimal fully matched law exists
with center time at most 3 and endpoint completion at most 9. Its proof
retains labeled causal kernels until the limiting matching is constructed.
