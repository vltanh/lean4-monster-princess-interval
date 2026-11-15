# Exact normalized grid bank and finite tail pricing

Date: 2026-11-13.

Let \({\cal B}_n\) be the finite physical grid bank: unit-speed grid
paths of physical step \(\Delta=1/(2n)\), started at positions in
\(n^{-1}\mathbb Z\cap[-1,1]\), visiting zero by time \(2\), and
completing both endpoints by time \(8\). Use fair reflected pairs as
the Monster rows.

By LEFT_FLOOR_CLOCK_ATOMIZATION.md, the vertex-clock LP value \(U_n\)
is the true unrestricted Princess-response minimax value on this bank.

Define the normalized subbank \({\cal N}_n\) as follows. A path may
choose arbitrary grid moves only until its first endpoint visit or
time \(2\), whichever occurs first.

* If the first endpoint is reached at or before time \(2\), continue
  directly to the opposite endpoint.
* If neither endpoint has been reached by time \(2\), choose one of
  the two endpoint orders and perform the direct two-endpoint tour.

All these paths complete by time \(6\). Then

\[
 \boxed{
 \min_{\nu\text{ on }{\cal B}_n}\sup_p\mathbb E_\nu T(M,p)
 =
 \min_{\nu\text{ on }{\cal N}_n}\sup_p\mathbb E_\nu T(M,p)
 =U_n.}                                                   \tag{1}
\]

There is also an exact optional restriction of the nodal matching
dual to sticky endpoint traces and outward-after-two characteristic
identities. With that restriction, record prices are constant after
time \(2\) until their own endpoint is reached, giving a weighted
two-tour terminal formula.

These are finite-bank statements. They do not assert that \(U_n=V\).

## 1. Princess normalization on the entire bank

For every symmetric Monster law on \({\cal B}_n\), symmetrizing the
Princess law preserves its payoff. The established common-quantile
ordering reduction then permits a fair signed family of ordered
nonnegative radial paths.

Stop every radial path at its first endpoint contact. This weakly
increases capture time against every Monster. Indeed, before that
contact the paths agree. If the Monster subsequently meets the stopped
path at the endpoint, continuity forces it to have met the original
path no later. Stopping preserves rank order.

Now force each radius maximally outward after time \(2\):

\[
 r^{\rm out}(t)=\min(1,r(2)+t-2),\qquad t\ge2.
\]

For a Monster that has visited zero by time \(2\), every surviving
positive Princess is to its right and every surviving negative
Princess to its left. The outward replacement stays at least as far
outward as the old path, by the speed-one bound. It therefore cannot
make a survivor be caught earlier.

Every row in \({\cal B}_n\) has the required center visit.
Consequently, for every symmetric law \(\nu\) on this bank,

\[
 \sup_{\mu\text{ legal}}J(\nu,\mu)
 =
 \sup_{\mu\text{ symmetric, ordered, sticky, outward after }2}
       J(\nu,\mu).                                        \tag{2}
\]

This equality holds separately for each law \(\nu\); no optimal
Princess strategy is assumed to exist.

## 2. A physical normalization independent of the Princess

Let \(m\in{\cal B}_n\), and let \(\sigma\) be its first endpoint time.

If \(\sigma\le2\), retain the path through \(\sigma\), then sweep
directly to the opposite endpoint. Starting from \(+1\), the direct
left sweep is pointwise no farther right than any other legal
continuation. If any other continuation meets a Princess, continuity
forces the direct sweep to meet her no later. The reflected assertion
holds from \(-1\). Thus this replacement dominates against every
Princess path, without any outward assumption.

The opposite endpoint is reached at \(\sigma+2\), no later than in
the original path. Any center visit after \(\sigma\) also occurs no
later. Hence the center-by-two condition is preserved.

If \(\sigma>2\), retain the path through time \(2\). From its position
\(x=m(2)\), visit the endpoints in the same order as the original
path's first and second endpoint visits, using direct unit-speed
legs. The first new endpoint arrival is no later than \(\sigma\);
the second is no later than the original second endpoint arrival.
The new completion time is at most \(2+4=6\).

For a sticky outward-after-two Princess, every survivor at time \(2\)
can thereafter be caught only at her own endpoint. She reaches it
before the Monster's direct earliest arrival there: for a positive
survivor, \(r(2)>x\), so

\[
 2+1-r(2)<2+1-x,
\]

and the negative-side inequality is the reflection. Therefore the
new endpoint tour captures each survivor no later than the original
path. The argument is simultaneous for every Princess in the class
on the right of (2).

The resulting map \(m\mapsto Nm\) depends only on the physical path
and its endpoint order. It is reflection-equivariant. It preserves
the grid because time \(2\), the current position, and both endpoint
distances are integral multiples of \(\Delta\). It maps
\({\cal B}_n\) into \({\cal N}_n\).

For any symmetric law \(\nu\), (2) and this simultaneous domination
give

\[
 \sup_{\mu\text{ legal}}J(N_\#\nu,\mu)
 \le \sup_{\mu\text{ legal}}J(\nu,\mu).
\]

Since \({\cal N}_n\subseteq{\cal B}_n\), both inequalities in (1)
follow. This proof uses neither a minimax exchange nor Princess
attainment.

## 3. Exact pricing with arbitrary nodal dual prices

The normalized bank can be priced even when the candidate nodal
prices have not been constrained to be outward after time \(2\).

For one active clock, a fixed path with endpoint step \(K\) has
minimum vertex-clock price

\[
 \sum_{j=0}^{K-1}\min_{0\le i\le j}p_i,
\]

up to the common physical scaling \(\Delta/2\). Here \(p_i\) is
the selected node's scaled price, and a node at the clock's own
endpoint is excluded.

Maintain the two running records along a physical prefix. Branch
over left and right moves only while time is below \(2\) and no
endpoint has been visited. When the prefix stops:

* at a first endpoint, scan its unique direct opposite sweep;
* at time \(2\), scan each of the two direct endpoint tours and
  take the smaller complete price.

During a scan, update each alive record with its current node price,
charge that scoring interval, then perform the physical move and
deactivate a clock if its endpoint is reached. This is exact for
arbitrary nodal prices. It does not assume that the records stay
constant on the tail.

There are \(O(n)\) nodes in either deterministic suffix. The tail
can also be precomputed as a function of the entry records. For a
fixed suffix and one active clock, let \(a_\ell\) be the running
minimum of the suffix's own node prices through step \(\ell\).
Its contribution for entry record \(r\) is

\[
 \frac{\Delta}{2}\sum_{\ell<K}\min(r,a_\ell).                \tag{3}
\]

The two clocks add independently, conditional on the same physical
suffix. Sorting the distinct levels \(a_\ell\) and storing their
counts and partial sums gives an exact piecewise-linear tail
function, or logarithmic-time evaluation at an entry record.

Thus the equality of bank values alone justifies a branch-until-two
pricing oracle with exact deterministic scans. No additional CDF
normalization constraints are needed for this safe version.

## 4. A value-preserving closed nodal dual restriction

There is a separate argument permitting stronger constraints on an
optimal nodal dual.

Write a radial grid node as \((j,k)\), with physical
\(t=j\Delta,r=k\Delta\), \(0\le k\le2n\), and \(j\equiv k\pmod2\).
Let \(g_{j,k}\in[0,1]\) be the radial isotone profile, with
\(g_{j,0}=0\). Its signed interior-trace prices are

\[
 p_-(j,k)=1+\operatorname{sgn}(k)g_{j,|k|},\qquad
 p_+(j,k)=p_-(j,-k),
\]

and the center price is one.

In addition to the usual interval-containment isotonicity, impose:

\[
 g_{j+2,\,2n}\le g_{j,\,2n}
 \quad\text{for the available even endpoint times},         \tag{4}
\]

and, for \(j\ge4n\),

\[
 g_{j,k}=
 \begin{cases}
 0,&k\le j-4n,\\
 g_{4n,\,k-j+4n},&k>j-4n.
 \end{cases}                                               \tag{5}
\]

The index on the right is nonnegative, at most \(2n\), and even,
because \(j\) and \(k\) have the same parity. It is therefore an
actual radial node at time \(2\). Formula (5) implies \(g=0\)
at and after time \(3\), including the endpoint interior trace.

Let \(Q_{\rm out}\) be this finite closed rational polytope. Then
restricting the nodal dual to \(Q_{\rm out}\) does not change its
optimum \(U_n\).

### Proof of the restriction

The bank has finitely many Monster rows and capture times bounded
by \(8\). Finite-row minimax therefore supplies, for every
\(\epsilon>0\), a Princess mixture securing \(U_n-\epsilon\)
against every fair row. Attainment is not needed; one may use the
compact closure of its bounded payoff vectors.

Apply the ordering, stopping, and outward normalization from
Section 1. Then use stopped outward radial dithering and common
quantile reordering to obtain continuous interior CDFs with no
center atom and continuous endpoint traces, still sticky and
outward after time \(2\), whose finite-row security approaches
the normalized law's security. The convergence follows from
pathwise convergence of the stopped dither and lower
semicontinuity of bounded capture time; a minimum over finitely
many rows preserves the lower-limit inequality.

Sample such a regular field at the grid nodes. Its nodal profile
belongs to \(Q_{\rm out}\): stopping gives (4), maximal outward
motion gives (5), and legality gives interval-containment
isotonicity.

Every fixed atomic clock plane is an upper plane for actual
capture. Hence a field with security at least \(U_n-\epsilon\)
against each row has nodal plane at least \(U_n-\epsilon\)
against every bank law with every admissible atomic clock.
The maximum dual value over \(Q_{\rm out}\) is therefore at least
\(U_n-\epsilon\) for every \(\epsilon>0\).

The finite clock polytope is bounded, so its minimum nodal plane
is a continuous function of the nodal values. Compactness of
\(Q_{\rm out}\) gives a maximizing profile with value at least
\(U_n\). The reverse inequality follows from
\(Q_{\rm out}\subseteq Q_{\rm all}\) and exact finite-bank
clock duality. Thus the optimum is exactly \(U_n\).

This proof does not identify an arbitrary nodal optimizer with an
actual CDF, nor assert a nonexistent Princess best-response
attainment. It uses regular realizable profiles only as an
approximating sequence inside a finite closed polytope.

### A fixed-law upper certificate from the restricted order graph

The restriction also supplies a useful direct upper certificate.
Fix a symmetric physical law \(\nu\) on the center-by-two bank and
any admissible atomic clocks with aggregate measure \(\alpha\).
Then

\[
 \boxed{\sup_{\mu\text{ legal}}J(\nu,\mu)
 \le \max_{g\in Q_{\rm out}}R(\alpha,g).}                   \tag{7}
\]

For each Princess law, first use the law-specific normalization in
Section 1. Approximate the resulting law by regular normalized
fields as in the preceding proof. Every approximating field has
a nodal profile in \(Q_{\rm out}\), and its actual payoff is at
most the fixed clock plane \(R(\alpha,g)\). Lower
semicontinuity of capture in the approximation gives (7) for the
original law as well.

Thus a restricted-\(Q_{\rm out}\) clock-plane bound is already a
physical all-Princess upper certificate. Recovering a separate
unrestricted-pressure matching is unnecessary. This assertion
uses symmetry and the center-by-two condition on the physical law;
it is not an upper bound for an arbitrary noncentered law.

For fixed rational clock masses, the right side of (7) is an exact
finite maximum-weight closure problem. Identify the outward-equal
node classes, impose the zero classes, and retain all containment
and endpoint-time order arcs. The remaining variables lie in
\([0,1]\), with only order inequalities. An integer-capacity
min-cut after denominator scaling gives an exact replay.

Minimizing (7) over all admissible atomic clocks on a fixed grid
law is exact: physical validity bounds that infimum below by the
law's true response value, while \(Q_{\rm out}\subseteq Q_{\rm all}\)
and left-floor fixed-law duality bound it above by the same value.

## 5. Constant records and the weighted two-tour terminal formula

For a profile satisfying (5), include the node at time \(2\) before
evaluating its future cost. A center-by-two path has then seen the
center price one in both still-alive histories, so its entry
records satisfy \(0\le r_-,r_+\le1\).

Neither record can decrease after time \(2\) until its own endpoint.

For the negative-endpoint clock, let \(x=m(2)\). At a later
nonnegative Monster position, its price is at least one. At a
negative position \(m(t)\), the outward footpoint radius is

\[
 a=-m(t)-(t-2)\le -x.
\]

If \(a\le0\), the price is again one. If \(a>0\), necessarily
\(x<0\), and same-time radial monotonicity gives

\[
 1-g(2,a)\ge1-g(2,-x)=p_-(2,x)\ge r_-.
\]

Thus every future alive node price is at least the existing record.
The other clock is the reflected argument. Reaching its own
endpoint deactivates the clock; the endpoint's interior trace is
not an additional selected event.

At time \(2\), write \(x=k\Delta\). The exact future price is

\[
 \frac{\Delta}{2}\min\left\{
 (2n-k)r_+ +(6n-k)r_-,
 \ (2n+k)r_- +(6n+k)r_+
 \right\}.                                                \tag{6}
\]

The first branch visits \(+1\) first; the second visits \(-1\)
first. Set an already inactive record to zero. If a first endpoint
was reached before time \(2\), price its deterministic opposite
sweep through time \(2\) by the exact scan of Section 3, then use
the constant remaining record for its residual distance.

The center-at-exactly-two case requires the stated node update.
Using a pre-update record greater than one in (6) would be wrong.

For \(g\in Q_{\rm out}\), this also proves that normalized-bank and
full-bank atomic pricing agree for that particular profile:
after time \(2\) every continuation has the same two fixed record
rates until its endpoints, and a direct tour minimizes their
weighted endpoint times.

The earlier first-endpoint normalization also holds directly for
nodal prices, without assuming that the profile is a realized CDF.
After a first \(+1\) visit, only the negative-endpoint record remains.
Along the direct left sweep its current nodal price is nonincreasing
by transport isotonicity, and at any common later time it is no
larger than the original continuation's nodal price. It is therefore
no larger than every earlier price on that continuation after the
endpoint visit, so its running record and total price cannot be
larger. The first-\(-1\) case is the reflection.

## 6. Compatibility with constructive Princess extraction

A \(Q_{\rm out}\) profile priced on the normalized bank to value
\(c\) also prices the full bank to \(c\), by Section 5. It therefore
meets the nodal lower inequality required by
CONSTRUCTIVE_PRINCESS_GRID_DUAL.md. For every rational
\(0<\varepsilon\le1/2\), the extracted Princess law secures

\[
 c-\frac1{2n}-\frac{\varepsilon}{2n}.
\]

In fact the common odd, period-two interpolation already preserves
the two normalizations. Its endpoint image time
\(1+T(t-1)\) is nondecreasing, so a nonincreasing nodal endpoint
trace remains nonincreasing after averaging.

For \(t\ge2\), \(0\le r\le1\), put \(L=t-r\). Since the common
map preserves the time-two plane, an image point remains after
time two. If \(L\ge2\), monotonicity gives \(T(L)\ge2\), and both
outward radial CDF values are zero. Otherwise \(1\le L<2\);
the original time-two footpoint radius \(2-L\) and its rounded
radius \(2-T(L)\) belong to \([0,1]\). At this valid time-two
footpoint, oddness and period two give

\[
 T(4-L)=4-T(L).
\]

Thus averaging the nodal identity (5) gives the continuous
outward-after-two identity. The endpoint stopping and outward
operations in the extraction theorem are therefore redundant
for such a profile, though harmless if performed again.

For an arbitrary dual profile priced only on the normalized bank,
the exact bank-value certificate remains valid. One should not
silently infer the full-bank nodal inequality needed by a particular
strategy-extraction routine. Section 5 supplies it when the optional
\(Q_{\rm out}\) conditions are imposed.

## 7. Resulting finite computation and scope

An exact normalized dual computation may use either:

* arbitrary isotone nodal prices, with deterministic suffix scans;
* \(Q_{\rm out}\) prices, with the weighted time-two formula (6).

Both give the same optimum \(U_n\). The second can remove all
post-two field variables through (5), and it can terminate
branching at first endpoint or time two.

This is a reduction of the *true finite physical-bank value*.
Together with common quantization it retains

\[
 U_n-\frac1{2n}\le V\le U_n.
\]

It does not turn that enclosure into an exact full-game equality.
A zero-gap global result still requires a continuous lower
certificate matching a physical upper certificate.

