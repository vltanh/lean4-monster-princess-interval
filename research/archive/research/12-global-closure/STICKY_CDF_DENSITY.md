# First-endpoint stopping and density of regular sticky CDFs

Independently reviewed proof, 2026-11-13.

The endpoint-stopping constraint can be added to the value-dense
Princess class used in the finite potential hierarchy. The radial
dither must be stopped as well. Its distance from the original sticky
path need not be bounded by the dither size, but it still converges
uniformly on compact time intervals, path by path.

## 1. Stopping at the first endpoint improves every capture time

For a legal Princess path \(p\), let \(\tau\) be its first visit to
either endpoint, and let \(p^{\rm st}\) agree with \(p\) through \(\tau\)
and remain at that endpoint afterward.

For every Monster path \(m\),

\[
 T(m,p)\le T(m,p^{\rm st}).
\]

If capture occurs by \(\tau\), both paths give the same capture.
Otherwise suppose the visited endpoint is \(+1\). At time \(\tau\)
the Monster is strictly below \(p(\tau)=1\). At the first later time
the Monster meets \(p^{\rm st}=1\), it is weakly above the original
Princess, because \(p\le1\). Continuity forces an original capture
in between. The \(-1\) case is reflected.

Stopping preserves order in an ordered family. If a lower path reaches
\(+1\), every path above it has already reached \(+1\); if an upper
path reaches \(-1\), every path below it has already reached \(-1\).
Thus endpoint stopping is globally value-preserving for the
maximizing Princess.

For a symmetric ordered radial family, write \(F^-(t,x)\) for its
strict signed CDF. At \(0<x<1\), the stopped CDF is

\[
 F_{\rm st}^-(t,x)
 =\min\left\{F^-(t,x),\,\inf_{0\le s\le t}F^-(s,1)\right\}.
\]

Both conditions, being below \(x\) now and never having reached
\(+1\), are initial rank intervals. Their intersection has the smaller
length. Rank-boundary tie choices change no probability mass.
The restriction \(x>0\) matters when the original law has a center
atom: a negative path that returned to zero after an endpoint visit
is negative after stopping, changing the strict CDF at zero.
In particular the positive endpoint trace is nonincreasing in time.

## 2. Stopped outward radial dither

Let \(r\) be an endpoint-sticky radial path: \(r\ge0\), \(r\le1\),
it is \(1\)-Lipschitz, and after its first visit to \(1\) it remains
there. Let \(Z\) be uniform on \([0,1]\), independent of \(r\).
For \(\delta>0\), first form \(\min(1,r+\delta Z)\), and stop it at
its first visit to \(1\). Denote the resulting legal path by
\(R_\delta\).

For fixed \(r,Z\), its stopping time is

\[
 \tau_\delta=\inf\{t:r(t)\ge1-\delta Z\}.
\]

As \(\delta\downarrow0\), these times increase to the original first
endpoint time \(\tau\), with the convention \(\tau=+\infty\).
If a bounded subsequence converged to a time strictly before \(\tau\),
continuity would give \(r=1\) at that earlier limit, a contradiction.

Before \(\tau_\delta\), the dither differs from \(r\) by at most
\(\delta\). Between \(\tau_\delta\) and a finite \(\tau\), the stopped
dither equals \(1\), and

\[
 0\le1-r(t)\le\tau-t\le\tau-\tau_\delta.
\]

After \(\tau\), both paths equal \(1\). If \(\tau\) is infinite, then
on every fixed compact time interval the maximum of \(r\) is strictly
less than \(1\), so no sufficiently small dither stops there.
Consequently

\[
 R_\delta\longrightarrow r
 \quad\hbox{uniformly on every compact time interval}.
\]

This is a pathwise convergence statement, not the generally false
uniform estimate \(\|R_\delta-r\|_\infty\le\delta\).
If every original path is absorbed by \(H\), then every dither is
also absorbed by \(H\), since \(\tau_\delta\le\tau\).

## 3. Exact regularity and the boundary monotonicity

Set

\[
 M_r(t)=\max_{0\le s\le t}r(s).
\]

For \(0\le x<1\), conditional on \(r\),

\[
 \Pr(R_\delta(t)<x\mid r)
 =
 \left[
 \min\left\{
  1,\frac{x-r(t)}{\delta},\frac{1-M_r(t)}{\delta}
 \right\}
 \right]_+.
\]

The first nonconstant bound says the unstopped dither is below \(x\)
now. The second says it has not already hit the endpoint. Uniformity
of \(Z\) gives the formula.

Both \(r\) and its running maximum \(M_r\) are \(1\)-Lipschitz.
The conditional CDF, and hence its average over \(r\), is continuous
and satisfies

\[
 |G_\delta(t,x)-G_\delta(s,y)|
 \le \frac{|t-s|+|x-y|}{\delta}.
\]

Its positive endpoint trace is exactly

\[
 G_\delta(t,1-)
 =\mathbb E\left[
    \min\left\{1,\frac{1-M_r(t)}{\delta}\right\}
   \right],
\]

which is nonincreasing and \(1/\delta\)-Lipschitz in time.
The radial law has no atom at zero. After adding a fair sign, the
signed interior CDF is continuous, symmetric, has density at most
\(1/(2\delta)\), and has the corresponding time-Lipschitz endpoint
traces. Its actual endpoint atoms are allowed.

These marginal CDFs obey the transport inequalities because they come
from legal paths. Common quantile reordering therefore gives a legal
ordered family with these same marginals. Its endpoint trace is
nonincreasing, so its law is concentrated on endpoint-sticky paths.
Possible quantile tie exceptions at endpoint-trace plateau ranks form
a null rank set and can be assigned sticky representatives. The existing
ordered-law dominance theorem says this reordering cannot decrease
the Princess security.

## 4. Preservation of the security value

The coupling in Section 2 gives weak convergence of the raw stopped
dither path laws to the original sticky law. Capture time on the
compact normalized Monster/Princess path product is bounded and lower
semicontinuous.

For completeness, if \(\mu_\delta\to\mu\) are these Princess laws,
choose nearly minimizing normalized Monster paths \(m_\delta\).
Pass to a subsequence \(m_\delta\to m\). Then the product laws
\(\delta_{m_\delta}\otimes\mu_\delta\) converge to
\(\delta_m\otimes\mu\), and the lower-semicontinuity inequality gives

\[
 \liminf_{\delta\downarrow0}S(\mu_\delta)
 \ge \int T(m,p)\,\mu(dp)
 \ge S(\mu).
\]

The normalized compact Monster class is sufficient for every law
absorbed by the fixed horizon. Quantile reordering only improves this
lower bound.

Thus regular, ordered, endpoint-sticky CDFs, absorbed by the same
horizon, are value-dense in the endpoint-sticky class. Endpoint
stopping from Section 1 shows this class has the unrestricted value.

## 5. Characteristic interpolation

Use a characteristic mesh aligned with reflection, the absorption
time, and the two physical boundaries. Sampling a continuous legal
CDF gives the usual nodal transport inequalities. Along the \(+1\)
boundary, the sampled values are also nonincreasing in time.
Their piecewise affine trace remains nonincreasing.

The symmetric monotone rational quantizer used in the hierarchy
preserves this additional order constraint. Consequently the finite
rational CDF meshes can impose a nonincreasing positive endpoint
trace without losing their global value-density.

## 6. Compatibility with the sharp outward cutoff

If the original sticky radius is forced outward at time T, the stopped
dither is also forced outward at T. A dither already stopped at T remains
at 1. Otherwise it equals r(T)+delta Z at T and subsequently increases
at unit speed until it reaches 1. Thus the regularization preserves
both outward time 2 and endpoint absorption time 3. The extra sticky
constraint and the sharp outward normalization can be imposed together.
