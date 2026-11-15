# Exact high-start Bellman gate for delayed turns at or after U = 1

## Status and scope

The verifier `verify_record_bellman_post_gate.cjs` closes the genuinely delayed
one-I continuation branch with second characteristic \(s\geq1\), for the
specified saved field and the high-start state domain below. It regenerates
the complete triangle and inverse-rank arrangement. It does not infer a
continuum result from a sampled route list.

This is **not** an all-monster lower certificate or a game-value claim.
The genuinely delayed branch \(U<s<1\) remains open. Existing pure-monster
cost dips in the saved field also remain. Direct-inward and
immediate-outward boundary plans have a separate, elementary finite-prepending
argument in the full one-I envelope; they are not being declared to have
nonnegative standalone derivatives.

The exact input is
`snapshots/endpoint_joint_i1_field.json`, Git blob
`5c45d042ee9948faebc03354c3e1e2ee3cbec1a5`.
The embedded exact field reader is the independently checked source whose
blob is `5714f57ada458f38ef8b46adb32be2472a009622`.
There are 3,571 nodes and 6,936 affine triangles. Decimal nodal values are
read as exact rationals, with the existing coordinate recovery convention.
The field is continuous in the positive spatial interior and is at the
endpoints by time two. Its \(V=1\) interior trace is zero. The verifier
explicitly checks all 68 saved nodes on that trace.

## 1. State domain and retained history

Write \(U=t+m,\ V=t-m\). Before its first center visit a positive monster
has captured a positive-rank interval \([L,M]\), and has captured no
negative reflected copy. All records from the preceding history are retained.

Put
\[
 a_0=\frac{255}{256},\qquad
 m_0=A(a_0)=\frac{17670484999841}{19531250000000}.
\]
The nonautomatic current-state domain is
\[
 a_0\le U<1,\qquad -U\le V<w<U,\qquad
 M=R(U,V)\ge m_0,\qquad l=R(U,w)<L\le M.
\]
The future plan goes inward to \(V=w\), outward to \(U=s\), then to the
negative and positive endpoints, with
\[
 1\le s\le2+w,\qquad R_{\rm closed}(s,w)>M.
\]
The current-triangle cover automatically has \(V<0\) for this field.
States with no new upper record, or first inward legs which capture no new
lower rank, are handled by the ordinary automatic/comparator cases in
`PREONE_RECORD_BELLMAN.md`.

The initial-start information gives the stronger reachable lower-record
bound
\[
 L\ge B_0(V):=R_<(\max(a_0,-V),V).                         \tag{1}
\]
Indeed, for an actual initial position \(a\ge a_0\), every previous light
coordinate satisfies \(U'\ge a\) and \(V'\le V\).
Transport therefore gives
\(R_<(U',V')\ge R_<(a,V)\).
Taking the running minimum proves (1). If \(V<-a_0\), the comparison point
is the initial diagonal and the right side is \(A_<(-V)\).
For the saved field these interior traces are continuous. This proof
uses the actual entire prefix; it does not reset the records at \(U=1\).

## 2. The exact outward derivative and its simpler lower bound

Let \(\alpha_q(u)\) and \(\beta_q(v)\) be the actual first capture inverses.
Let \(a=R_U(U,V)\), \(a_1=R_U(U,w)\). The fixed-plan outward residual is
\[
\begin{aligned}
G(L)={}&\frac12\left[L-l+
 \int_{-U}^{w}{\bf1}_{R(U,z)<L}R_U(U,z)\,dz\right]\\
 &+\left[\alpha_{l+}(s)-\frac{U+w}{2}\right]a_1
 -\left[\beta_{M+}(w)-\frac{U+V}{2}\right]a.              \tag{2}
\end{aligned}
\]
The strict indicator and right-rank inverses include the moving-rank
flux correctly. In particular the first line is nonnegative.
At \(L=l\) that line is zero, because \(R(U,z)\ge R(U,w)\) for \(z\le w\).

The proof below often drops this nonnegative first line. This is
conservative, not a claim that the first line vanishes for an arbitrary
history. Separate exact point diagnostics show that it can be large.

For \(s\ge1\), speed and the endpoint bound give
\[
 \alpha_{l+}(s)\ge\alpha_{l+}(1)+(s-1)/2,\qquad
 \beta_{M+}(w)\le w+1.
\]
Consequently
\[
 Q=a_1\left[\alpha_{l+}(1)-\frac{U+w}{2}\right]
    -a\left[w+1-\frac{U+V}{2}\right]\le G(L).            \tag{3}
\]
On a fixed current triangle, first-turn triangle and nonflat row-one
inverse piece, \(Q\) is affine in \((U,V,w)\).
All adjacent inverse pieces are retained on rank boundaries.
Only triangle pieces valid for the actual right-\(U\) derivative are
used; outgoing faces of such pieces are treated by the adjacent
right-hand piece.

A useful independent regression is
\[
 \alpha_q(s)=\frac{s+V_{\rm root}}2,
 \qquad p_q(\alpha_q(s))=\frac{s-V_{\rm root}}2.          \tag{4}
\]
The sign in (4) matters. For the three-leg rank with initial
\(9/20\), incoming characteristic \(13/20\), and outgoing
characteristic \(1/2\), the first \(s=4/5\) contact is at time
\(13/20\), radius \(3/20\). The verifier checks this physical
coordinate identity.

## 3. Competitive-plan cap

Compare a delayed plan to direct inward motion from the current \(U\).
Write \(B=\max(M,R_{\rm closed}(s,w))\), \(\Delta=s-U\) and
\(W=U+6-w\). First-inverse speed bounds and the complete reflected-copy
delay imply
\[
 4(C_{\rm delayed}-C_{\rm inward})
 \ge \Delta(4+l-2B)-W(B-M)
 \ge \Delta(2+l)-W(1-M).                                \tag{5}
\]
Thus any competitive plan in this branch must satisfy
\[
 s\le U+\frac{(U+6-w)(1-M)}{2+l}\le U+4(1-M).            \tag{6}
\]
Only strict violation of (6) gives strict domination. Equality is
retained in all geometric covers.

The ratio \((U+6-w)/(2+l)\) is linear-fractional with a positive
denominator on each first-turn polygon. Its maximum is attained at
a vertex: the value at any convex combination is a
denominator-weighted average of the vertex values. This supplies the
verified per-cell constant \(K\) used in the sharper affine cap
\(s\le U+K(1-M)\).

Using \(\beta_{M+}(w)\le(s+w)/2\) on a useful upper-capture branch,
put \(c=2\alpha_{l+}(1)-1\). Then
\[
 2G(L)\ge a_1(c-w)-a(w-V)+(a_1-a)(s-U).                  \tag{7}
\]
If \(a_1\ge a\), set \(s=1\) in the lower bound.
If \(a_1<a\), use the upper cap in (6). These are affine lower
bounds after the per-polygon ratio maximum is fixed.

## 4. Wide first turns are excluded

The exact endpoint-interior row crosses \(m_0\) at
\[
 w_0=-\frac{31876647474353}{45229875167500}.
\]
All later endpoint-interior traces are at most \(m_0\). Hence, for
\(w\ge w_0\), no interior second turn can capture a new upper rank.
A useful second turn there must be the closed endpoint \(s=2+w\).

For \(w_0\le w\le-5/8\), transport gives
\(l\ge R(a_0,-5/8)=787953762109/10^{12}\).
Substituting this and \(M\ge m_0,\ U\le1\) into (5) proves a four-cost
advantage of at least
\[
 \frac{2517209183656877666974201311}
 {28268671979687500000000000000}>0
\]
for direct inward motion. For \(w\ge-5/8\), the bound \(l\ge0\)
gives the positive four-cost margin
\[
 \frac{3680834990301}{156250000000000}.
\]
Thus only \(w<w_0\) enters the remaining arrangement.

## 5. Interior second turns after one are strictly worse than turn one

The history bound (1), rather than the weaker \(A(-w)\), is decisive.
For every negative-\(V\), post-one triangle, the verifier proves
\[
 4+B_0(V)-2R(U,V)-(U+6-V)R_U(U,V)
 \ge \frac{91472232581}{10^{12}}>0.                      \tag{8}
\]
This is an exact vertex test on 1,156 affine triangles (3,468 vertex
checks). The floor is affine on each tested triangle; the verifier
checks that no floor breakpoint lies in its \(V\) interval.

For a delayed plan, after its first inward leg the remaining lower
record is at least \(B_0(w)\). If its outward leg catches new upper
ranks, (8) bounds its second-turn cost derivative from below; the
additional first-inverse moment derivative is nonnegative.
If its outward leg catches no new upper ranks, increasing the turn
is already nonbeneficial. First-inverse jumps are upward, so they do
not reverse this conclusion.

Therefore an interior \(s>1\) is strictly worse than \(s=1\).
The closed endpoint \(s=2+w\) can have a capture jump and is explicitly
excluded from this argument. It is checked separately next.

## 6. Endpoint comparator

For the delayed endpoint \(s=2+w\), the immediate-outward comparator
stops at \(\bar s=2+V\). Use the notation \(H,K(L)\) from
`PREONE_RECORD_BELLMAN.md`, so that twice their cost difference is
\(H-K(L)\), with \(K\) increasing in \(L\).

Since \(\alpha_{\bar s}\le\bar s\), \(\alpha_U\ge0\), and inverse
speed gives \(\alpha_s-\alpha_{\bar s}\ge(w-V)/2\),
\[
 K(M)\le(2+V)(M-l)-\frac l2(w-V).
\]
The uncaught negative copy alone gives \(H\ge w-V\).
Hence every prior lower record is strictly dominated whenever
\[
 P_E:=(1+l/2)(w-V)-(2+V)(M-l)>0.                         \tag{9}
\]

After the affine cover reductions, exactly 290 endpoint regions
remain. On the closed part of each region where its derivative
lower bounds are nonpositive, the verifier proves
\[
 P_E\ge (w-V)/1000.                                     \tag{10}
\]
A genuine first inward capture has \(w>V\), so (10) is strict enough
to remove every remaining endpoint candidate. Equality faces are
not dropped.

## 7. Fixed-one comparator

Put \(B_V=R(1,V)\), \(B_w=R(1,w)>M\), and \(\delta=w-V\).
For upper ranks \(M<q\le B_w\), replacing the immediate outward leg
by the delayed one postpones \(\beta\) by at least \(\delta/2\).
For \(B_w<q\le B_V\), it postpones capture from at most
\((1+V)/2\) to time four. Therefore
\[
 2H\ge\delta(B_w-M)+(7-V)(B_V-B_w).
\]
For \(l<q\le M\), \(\alpha_U(q)\ge(U+V)/2\) and
\(\alpha_1(q)\le1\), giving
\[
 2K(M)\le(2-U-V)(M-l).
\]
It is sufficient that
\[
 P_1:=\delta(B_w-M)+(7-V)(B_V-B_w)
       -(2-U-V)(M-l)>0.                                 \tag{11}
\]

Of the 273 residual interior cases, 29 have a nonnegative fixed-one
affine derivative bound. The remaining 244 satisfy, on the closed
region where that bound is nonpositive,
\[
 P_1\ge(w-V)/10^6.                                      \tag{12}
\]
Thus all their prior lower records are strictly dominated too.

## 8. Exact quadratic certificates

The domains in (10) and (12) are bounded rational polytopes in
\((U,V,w)\). They are defined by current/first triangles, the
one-sided derivative faces, useful-capture and cap conditions,
and the affine derivative lower bounds.

The verifier enumerates all vertices by exact linear algebra.
For a quadratic \(P\), let \(b_{ii}=P(v_i)\) and
\[
 b_{ij}=2P((v_i+v_j)/2)-\frac{P(v_i)+P(v_j)}2.
\]
If every \(b_{ij}\ge0\), then for any convex combination
\(x=\sum_i\lambda_i v_i\),
\[
 P(x)=\sum_i\lambda_i^2b_{ii}
      +2\sum_{i<j}\lambda_i\lambda_jb_{ij}\ge0.
\]
This is a whole-polytope certificate. No vertex-only assertion about
a general quadratic is being made.

The completed run checked 9,321 endpoint Bernstein pairs and
8,419 fixed-one Bernstein pairs. Degenerate and shared faces are
retained. A branch is discarded as wrong-sided only when its
strict derivative/history conditions cannot hold anywhere.
Because all these strict affine forms are nonnegative on the
closed domain, testing that each has a positive maximum is an
exact feasibility criterion (average their individual witnesses).

## 9. Reproduced coverage

The regenerated arrangement has 156 current triangles and 1,052
first-turn/inverse-rank variants after the wide-turn exclusion.
The initial active-case split checks 45,092 cases: 9,160 are empty,
16,835 have only invalid/degenerate strict traces, 18,282 pass an
affine derivative bound, and 815 require the sharper cap.
The ratio cap proves 168 more and removes 84 empty cases.
The remaining 563 consist of the 290 endpoint cases above and
273 interior cases reduced to \(s=1\).

The full clean replay independently reproduced these counts,
all 50 cross-checks between two affine-vertex routines, the exact
post-turn margin, and zero unresolved endpoint/fixed-one cases.
It ran in pure V8 rational arithmetic during the executor outage.
There was no native Python, Lean, or CI run.

Commands:
```text
node packages/interval_cdf_discovery/verify_record_bellman_post_gate.cjs \
  packages/interval_cdf_discovery/snapshots/endpoint_joint_i1_field.json \
  packages/interval_cdf_discovery/snapshots/record_bellman_post_gate.json
```
The command checks the input Git blob hash before rebuilding the proof.

## 10. What remains for a full pre-center certificate

For the full one-I envelope, direct inward motion at a future state
is handled by finite prepending: an initial outward increment
followed by direct inward motion is itself an immediate-outward
one-I plan from the current state. The same merge handles a future
plan whose first inward leg has zero length. No derivative sign
for those standalone boundary plans is required.

The open branch is a genuinely delayed plan with
\[
 V<w<U<s<1.
\]
The fixed-one comparator has the exact analogue
\[
 P_s=(w-V)(R(s,w)-M)
 +(s+6-V)(R(s,V)-R(s,w))
 -(2s-U-V)(M-l).
\]
If \(P_s>0\), that plan is strictly dominated by immediate outward
motion. In particular, if
\(R(s,V)-R(s,w)\ge M-l\), the positive coefficient margin is
\(6+U-s>0\). Establishing this or the full derivative/comparator
condition on the remaining early-turn domain is the next obligation.

A center continuation and the record-aware \(U=1\) boundary
continuation must also be included when applying the complete
Bellman theorem. The result here does not silently replace either
boundary by an initially reset one-turn response.
