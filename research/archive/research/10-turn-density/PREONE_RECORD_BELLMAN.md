# A record Bellman certificate before the first center return

**Recovery status.** This text was reconstructed from the retained proof notes during the executor outage on 2026-11-11. The mathematical checks and diagnostic counts below were completed before the outage. The reconstruction itself is not a new Python run.

## Scope

This is a sufficient response certificate for a supplied ordered, reflected princess law. It does not assert that the saved discovery field satisfies every gate, and it does not assert a game value. The remaining obligation is an outward Bellman inequality over a continuous geometric domain. Incoming and outgoing rank records from the whole previous monster history must be retained. They must not be reset when \(U\) reaches one.

Let \(p_q\) be the nonnegative ordered quantile paths, \(q\in[0,1]\), each legal and at its endpoint by time two. Write \(R(U,V)\) for their radial CDF in light coordinates \(U=t+x,V=t-x\). Use the strict spatial CDF for a lower captured frontier and the closed CDF for an upper frontier. Let \(\alpha_q(U)\) and \(\beta_q(V)\) be the actual first inverses of \(t+p_q(t)\) and \(t-p_q(t)\), with first-contact conventions. At thresholds below the initial characteristic their inverse is zero. All equations below use these first inverses, not a later intersection of a repeated characteristic.

The derivative calculations apply on continuous piecewise-affine interior field regions, with one-sided traces at regime boundaries. A field with spatial atoms must satisfy the finite-increment inequalities with its actual strict/closed traces; a pointwise derivative calculation alone is insufficient there.

## 1. State and continuation moment

Before the first center visit the monster remains positive and no reflected negative copy has been captured. At its current point \((U,V)\), put \(t=(U+V)/2\). Its positive captured ranks form one interval \([L,M]\), up to null rank endpoints. A valid state satisfies
\[
0\le L\le R_{<}(U,V)\le R_{\le}(U,V)\le M\le1.
\]
The surviving probability is
\[
\sigma=(2+L-M)/2.
\]
The two records \(L,M\) contain the entire prefix history.

Consider a future plan that goes inward to \(V=w\), outward to \(U=s\), and then visits the negative and positive endpoints. Its parameters satisfy
\[
V\le w<U,\qquad U\le s\le2+w.
\]
Include the limiting direct-inward and immediate-outward plans, and truncate a plan when it first reaches an endpoint. Define
\[
l=\min(L,R_{<}(U,w)),\qquad m=\max(M,R_{\le}(s,w)).
\]
Twice the unresolved absolute capture moment is exactly
\[
\begin{aligned}
2F={}&\int_l^L\alpha_q(U)\,dq+\int_0^l\alpha_q(s)\,dq
+\int_M^m\beta_q(w)\,dq\\
&+(s+3)(1-m)+\int_0^1\beta_q(s)\,dq. \tag{1}
\end{aligned}
\]
The first term captures newly reached lower positive ranks on the first inward leg. The second captures the remaining lower positive ranks on the later inward sweep. The third captures new upper positive ranks on the outward leg. The fourth is their remaining endpoint tail: \(s\ge0\) and endpoint absorption by time two make its first contact exactly \(s+3\). The last term is the complete reflected-copy first-inverse moment. In particular, \(\beta_q(s)\) must not be replaced by \(s+1\) when \(s<1\) without a separate outgoing-trace theorem.

Define the remaining-time envelope
\[
B(U,V,L,M)=\inf_{w,s}F(U,V,L,M;w,s)-t\sigma. \tag{2}
\]
This is the infimum over the stated continuation family. It becomes a lower certificate only after the Bellman inequalities and boundary continuation obligations below have been proved.

## 2. Finite Bellman inequalities

For an outward unit leg, \(M(u)=\max(M,R_{\le}(u,V))\), while \(L\) is unchanged. Require, for every legal increment \(h\),
\[
B(U,V,L,M)\le
\frac14\int_U^{U+h}[2+L-M(u)]\,du
+B(U+h,V,L,M(U+h)). \tag{3}
\]
For an inward unit leg, \(L(v)=\min(L,R_{<}(U,v))\), while \(M\) is unchanged. Require
\[
B(U,V,L,M)\le
\frac14\int_V^{V+h}[2+L(v)-M]\,dv
+B(U,V+h,L(V+h),M). \tag{4}
\]

Equation (4) is automatic for the envelope: prepend the inward increment to a future one-I plan and merge its first inward leg. Equation (3) is substantive, because prepending an outward increment can create an additional return.

At every exit from the region being certified, \(B\) must be no larger than the true optimal remaining cost. This includes a center visit, an endpoint, and any artificial boundary such as \(U=1\). A center-memory theorem can supply the center boundary. A post-one return theorem can supply \(U=1\) only for record states satisfying its hypotheses. Neither obligation is implied merely by having proved all initial one-I inequalities.

If (3)-(4), valid boundary continuations, and
\[
B(a,-a,A(a),A(a))\ge v
\]
hold for every initial \(a\) under consideration, every monster starting at such an \(a\) has expected capture time at least \(v\). For an initial atom replace the two equal records by the strict and closed initial frontiers.

## 3. Arbitrary speeds and turn counts

The finite inequalities telescope along any finite unit-leg path, with its actual record updates. They extend to arbitrary legal continuous monster curves; no finite-turn hypothesis is needed.

A finite-contact argument avoids an unjustified continuity assertion at first-contact atoms. Sample \(N\) equally spaced positive quantiles and their reflections. For any monster curve, the captured ranks of each orientation form an interval. Hence the empirical captured mass differs from the continuum captured mass by at most \(2/N\), uniformly in time. On a finite horizon, retain the sampled first-contact points and join consecutive points at the same times by legal unit-leg zigzags. Before a positive-half exit these can remain in that half; spare time can be filled by sufficiently small interior out-and-back pieces. Sampled first captures do not become later. The already valid boundary continuation handles the first exit, even if the interpolant reaches it earlier.

Append an endpoint tour to truncate a finite-cost curve. On a horizon \(H\), the two empirical/continuum comparisons cost at most \(4H/N\). Let \(N\) tend to infinity, then let the truncation horizon increase. The extra endpoint-tour cost is at most four times the remaining mass and tends to zero for a finite-cost curve. Infinite-cost curves need no further argument. This proves the all-speed, unrestricted-turn extension under the stated boundary obligations, including exact contact atoms.

## 4. The only nonautomatic derivative case

Fix a nondegenerate potentially active plan with
\[
l=R(U,w)<L,\qquad m=R(s,w)>M.
\]
If \(M>R(U,V)\), an infinitesimal initial outward move captures no new upper rank. The fixed-plan contribution from delaying lower captures is nonnegative. The difficult case is \(M=R(U,V)\).

On strictly invertible smooth pieces the outward Bellman residual can be written
\[
\begin{aligned}
G(L)={}&\int_l^L\partial_U\alpha_q(U)\,dq\\
&+\left[\alpha_l(s)-\frac{U+w}{2}\right]R_U(U,w)
-\left[\beta_M(w)-\frac{U+V}{2}\right]R_U(U,V). \tag{5}
\end{aligned}
\]
On a fixed active branch, including the current \(M\) update,
\[
B_U+\sigma/2=G/2.
\]
Thus nonnegative \(G\) for every active plan proves the local outward inequality.

However, (5) cannot be interpreted as an integral of pointwise inverse derivatives across a moving incoming-rank jump. The next section gives the correct direct-moment version.

## 5. Direct first-turn flux, including flat rows

The exact first-turn identity is
\[
2\int_l^L\alpha_q(U)\,dq
=(U+w)(L-l)-\int_{-U}^{w}(L-R(U,z))_+\,dz. \tag{6}
\]
Its right-\(U\) derivative, together with the moving lower-rank contribution at the later turn, gives
\[
\begin{aligned}
G(L)={}&\frac12\left[
L-l+\int_{-U}^{w}{\bf1}_{\{R(U,z)<L\}}R_U(U,z)\,dz
\right]\\
&+\left[\alpha_{l+}(s)-\frac{U+w}{2}\right]R_U(U,w)
-\left[\beta_{M+}(w)-\frac{U+V}{2}\right]R_U(U,V). \tag{7}
\end{aligned}
\]
Use the right-rank limits in the last two terms and the strict indicator for the right-\(U\) flux. The flux integral stops at \(w\). Replacing it by a whole-row flux, or subtracting two fixed-\(q\) derivatives at a flat rank, can include the wrong portion of the incoming plateau.

For a fixed geometric regime, \(G\) is nondecreasing in \(L\). Between upward jumps its slope is at least \(1/2\). A jump occurs when the strict integration set acquires a flat incoming interval. Such a jump may make the first nonnegative threshold a rank boundary rather than a literal zero of \(G\).

A continuum witness in verify_record_bellman_flux.py takes
\[
a(q)=\frac15+\frac q2,\quad u(q)=\frac25+\frac q2,\quad
c(q)=\frac34-\frac q2,
\]
and
\[
U=\frac35,\quad V=-\frac{11}{20},\quad w=-\frac3{10},
\quad s=\frac45,\quad L=\frac35,\quad M=\frac7{10}.
\]
Direct physical first-inverse integration gives \(2F=2311/800\) and derivative \(5/4\). Formula (7) gives the same \(5/4\). Integrating pointwise inverse derivatives in (5) without the jump flux gives only \(23/20\), missing \(1/10\). This is an exact continuum calculation, not a finite-rank test.

## 6. Eliminate the record L before checking geometry

Let
\[
P_s(q)=\int_0^q\alpha_r(s)\,dr,\qquad
T_v(q)=\int_0^q\beta_r(v)\,dr,
\]
and put
\[
\operatorname{Upper}(M;v,s)=T_v(b)-T_v(M)+(s+3)(1-b),
\quad b=\max(M,R_{\le}(s,v)).
\]
Compare the delayed plan \((w,s)\) to an immediate-outward plan with the same intended second \(U\). The immediate plan must stop at
\[
\bar s=\min(s,2+V),
\]
because it may reach the positive endpoint first. Let \(l_0=R(U,w)\), and define
\[
\begin{aligned}
H={}&\operatorname{Upper}(M;w,s)
-\operatorname{Upper}(M;V,\bar s)+T_s(1)-T_{\bar s}(1),\\
K(L)={}&P_{\bar s}(L)-P_U(L)+P_U(l_0)-P_s(l_0). \tag{8}
\end{aligned}
\]
Twice delayed-plan cost minus comparator cost is \(H-K(L)\). Direct first-capture comparison gives \(H\ge0\), and
\[
K'(L)=\alpha_L(\bar s)-\alpha_L(U)\ge0.
\]
Consequently a minimizing delayed plan must satisfy \(K(L)\ge H\). If \(K(M)<H\), it is excluded for every possible \(L\). Otherwise set
\[
L_{\rm crit}=\inf\{L\in[l_0,M]:K(L)\ge H\}.
\]
It suffices to prove \(G(L_{\rm crit})\ge0\). This reduces the record variable to a monotone scalar threshold rather than sampling arbitrary \(L\).

An equivalent exact branch test uses the first nonnegative \(G\) threshold \(L_0\). If \(G(l_0)\ge0\), all records are safe. Otherwise:

- If the actual trace has \(G(L_0)\ge0\), it is enough that \(K(L_0)\le H\).
- If \(G(L_0)<0<G(L_0+)\), require \(K(L_0)<H\), or separately prove the equality face harmless. Nonstrict equality alone leaves a potentially active bad state at the lower trace.
- If \(G(M)<0\), exclude the plan using the strict inequality \(K(M)<H\). Equality is again insufficient.

These strictness requirements matter at flat-row flux jumps and terminal record faces.

## 7. Exact affine-region certificate format

For a rational continuous piecewise-affine field, fix the triangles containing \((U,V)\), \((U,w)\), the inverse point defining \(\alpha_l(s)\), and the inverse point defining \(\beta_M(w)\), together with all row-integral regimes. Their membership inequalities and capture-rank branch conditions are affine in the geometric parameters. On each such region, \(G\) is piecewise affine in \(L\) and the geometric parameters, with positive slope in \(L\) between upward jumps. A zero threshold is affine; a jump threshold is an affine row-rank boundary. The difference \(H-K\) at that threshold is a rational quadratic on a rational polytope.

This is a finite quadratic certificate problem: check the appropriate quadratic on the polytope, with strict faces treated as described above. The finite rational-polytope face theorem in research/09-equilibrium-structure/FINITE_QUADRATIC_CERTIFICATE.md supplies a verification format. A numerical minimizer or a check only at vertices is not a certificate for an arbitrary quadratic.

There is an automatic same-region case. If one affine patch
\[
R=kU-lV+c,\qquad k,l>0,
\]
contains all relevant inverse points, then
\[
G(l_0)=\frac{k+l}{2l}\,[k(s-U)-l(w-V)]. \tag{9}
\]
The bracket is positive whenever \(R(s,w)>R(U,V)\), the useful new-upper-capture condition. Thus only cross-regime plans require the heavier geometric check.

A stronger record-free exclusion is also available region by region: on the bad halfspace \(G(l_0)<0\), prove \(H-K(M)>0\). It eliminates every \(L\) without solving for \(L_{\rm crit}\). This is sufficient, not necessary.

## 8. Evidence and open obligation

The prior physical moment verifier completed 13,092 exact checks: 2,916 arbitrary-prefix continuation moments, 2,916 endpoint-truncated comparison identities, and 2,916 fixed-plan concavity checks, including 996 endpoint truncations, 2,052 waits, and 1,296 repeated-prefix changes. The separate flux witness above checks the missing moving-rank contribution exactly.

On the frozen endpoint_joint_i1 field, a floating diagnostic checked 41,602 plans formed from all existing second-turn coordinates in the high-start region. Of these, 359 survived the comparator screen \(K(M)\ge H\), including 15 off-initial-diagonal plans. Every surviving sampled plan already had \(G(l_0)>0\); the smallest displayed \(G(l_0)\) was about 0.00099829. This is a diagnostic only. It does not verify the continuous geometric regions, trace equality faces, or arbitrary record states.

The desired next certificate is therefore a whole-region proof of \(G(l_0)\ge0\) or \(H-K(M)>0\), with the threshold test used where these simpler alternatives do not separate the region. The exact outer and post-one boundary obligations remain explicit. No unrestricted lower bound or matching equilibrium is claimed by this note.
