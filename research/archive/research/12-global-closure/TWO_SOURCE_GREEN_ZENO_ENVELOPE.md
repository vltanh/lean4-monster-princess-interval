# Exact all-count terminal-center envelope on the long-horizon strip

Date: 2026-11-12. **This closes the prescribed-terminal, no-initial-wait productive center-return optimization for a nontrivial full time strip. It does not solve the unrestricted Princess–Monster game or construct equilibrium CDFs.**

## 1. Exact result

Use the saved affine terminal wedge and its already-audited physical inverse
gates from LOW_SURPLUS_ALL_HINGES_EXCLUSION.md:
\[
R(U,V)=kU-\ell V+c,\qquad
k=\frac{655898601421}{62500000000},\quad
\ell=\frac{820954217}{12500000000},\quad
d=k-\ell,\quad b=\frac{15}{16}.
\]
A balanced center state at \(t=b-H\) has captured rank
\(n=Z(t)+y\), \(Z(t)=dt+c\). Its *productive fixed-terminal*
policies consist of alternating maximal center tents of positive
durations summing to \(H\), returning last at \(b\), followed by the
prescribed balanced terminal endpoint tour. **No initial wait, earlier
front reset, alternative exterior exit, or other prefix is allowed
within the optimized component.** Let \(E_y\) be the genuine excess
energy relative to the same chain-independent baseline, as in
INFINITE_TURN_RENEWAL.md.

Put
\[
 r=\ell/k,\quad
 \theta=\frac{1-\sqrt{1-8r}}{1+\sqrt{1-8r}},\quad
 A=k/8-\ell/2,\quad
 E_\infty(y)=-\frac{9\ell\theta}{4}
             -\frac{\theta y^2}{4\ell}-\frac{y^2}{8k}.
\]
Let the **actual one-return energy**, including its potential initial
short hinge, be
\[
 E_1(H,y)=AH^2-\frac{3\ell H}{2}-\frac{yH}{2}
          -\frac{y^2}{8k}-\frac{(y-dH)_+^2}{8k}.
\]

**Theorem (all finite productive turn counts).** For every
\[
  \boxed{\frac1{20}\le H\le\frac1{16},\qquad 0\le y<kH,}
\]
the exact infimum over all productive fixed-\(b\) finite-center-return
policies, with no preceding center wait, is
\[
\boxed{
 \inf_{\text{all finite counts}} E_y
 =\begin{cases}
   \min\{E_1(H,y),E_\infty(y)\},&0\le y\le 2H/5,\\
   E_1(H,y),&2H/5\le y<kH.
  \end{cases}
}                                                           \tag{1}
\]
For \(0\le y\le2H/5\), **every finite multi-return policy is strictly
above** \(E_\infty(y)\), and an explicitly constructed family of finite,
productive, no-hinge policies approaches \(E_\infty(y)\). Therefore the
formula is an exact **infimum**, not a finite-turn cutoff or an
assertion that a particular finite-count optimum attains it.

There is exactly one transition
\(0<y_*(H)<2H/5\) satisfying \(E_1(H,y_*)=E_\infty(y_*)\).
The many-turn limit is better for \(0\le y<y_*(H)\);
one return is better for \(y>y_*(H)\) within this sector.
For orientation, \(y_*(1/20)\simeq0.00685411\) and
\(y_*(1/16)\simeq0.02449564\), *not* asserted as game values.

## 2. Uniform lower bound on all low-surplus multi-return chains

By the previously proved all-short-hinge deletion, every finite
productive chain can be improved to a no-hinge chain or one return.
For a no-hinge \(m\ge2\) chain the exact energy is
\[
 E_y(h)=A\sum_jh_j^2-\frac\ell2\sum_{j<m}h_jh_{j+1}
        -\frac{3\ell}2h_m-\frac y2h_1-\frac{y^2}{8k},
\]
with \(dh_1\ge y,\ dh_j\ge\ell h_{j-1}\), and \(\sum h_j=H\).

Set \(C_0=\ell/(4\theta),\ \alpha=\theta y/\ell,\ \gamma=3\theta\).
The h-dependent energy is exactly
\[
 C_0(h^\mathsf TK_mh-2\alpha h_1-2\gamma h_m),
\]
with \(K_m\) tridiagonal, diagonal \(1+\theta^2\), adjacent
entries \(-\theta\). Its inverse boundary entries are
\[
 u_m=\frac{1-\theta^{2m}}{1-\theta^{2m+2}},\quad
 v_m=\frac{\theta^{m-1}(1-\theta^2)}
            {1-\theta^{2m+2}},
\]
and
\[
 c_m=\frac{1-\theta^m}{(1-\theta)(1+\theta^{m+1})},
 \qquad P_m=\frac{m-2\theta c_m}{(1-\theta)^2}.
\]

Completing the square **with the actual fixed-duration equality** (but
dropping the positivity and no-hinge inequalities, which can only
decrease the minimum) yields
\[
\begin{split}
 E_y(h)\ge{}&
 -C_0\{(\alpha^2+\gamma^2)u_m+2\alpha\gamma v_m\}\\
 &+C_0\,\frac{[H-(\alpha+\gamma)c_m]^2}{P_m}
 -\frac{y^2}{8k}.                                     \tag{2}
\end{split}
\]
The factor \(P_m=\mathbf1^\mathsf TK_m^{-1}\mathbf1>0\).

Let
\[
 H_{\rm free}=\frac{\alpha+\gamma}{1-\theta},\qquad
 \Delta=H-H_{\rm free}.
\]
For \(\Delta>0\), use \(u_m<1,\ v_m<\theta^{m-1}\),
\(c_m<(1-\theta)^{-1}\), and
\(P_m<m/(1-\theta)^2\). Hence (2) implies
\[
 E_y(h)-E_\infty(y)>
 C_0\left\{\frac{\Delta^2(1-\theta)^2}{m}
                 -2\alpha\gamma\theta^{m-1}\right\}.
                                                               \tag{3}
\]
Since \(\theta<2/3\), the sequence \(m\theta^{m-1}\), \(m\ge2\),
is decreasing, bounded by \(2\theta\). Thus a single **count-uniform**
strict condition suffices:
\[
 \boxed{\Delta^2(1-\theta)^2>4\alpha\gamma\theta
                =12\theta^3y/\ell.}                  \tag{4}
\]

Verify (4) on the entire rectangle
\(H\in[1/20,1/16]\), \(0\le y\le1/40\), which contains the desired
low-surplus band \(0\le y\le2H/5\).
The exact identity \(r=\theta/[2(1+\theta)^2]\) and monotonicity
of this function imply
\[
 0<\theta<T:=321/25000.
\]
Consequently
\[
 \Delta\ge\Delta_{\min}:=
 \frac1{20}-\frac{T(3+(1/40)/\ell)}{1-T}
 =\frac{2442500901923}{405206582426860}>0 .
\]
An **exact rational** comparison gives
\[
 \boxed{
   \Delta_{\min}^2 >
   \frac{12T^3(1/40)}{\ell(1-T)^2}.                    \tag{5}
 }
\]
Its rational numerator difference and every defining inequality
are checked by the standalone Fraction verifier. This proves
\(E_y(h)>E_\infty(y)\) for every hinge-free finite \(m\ge2\)
in the entire stated band. After short-hinge deletion, every other
multi-return chain is beaten by either such a chain or the one-return
policy. No optimization over turn counts is left.

## 3. An explicit approaching family of legal finite policies

For every integer \(N\ge2\) define
\[
 \begin{split}
 w_N&=\frac{H-(\alpha+\gamma)(1-\theta^N)/(1-\theta)}N,\\
 h_j^{(N)}&=\alpha\theta^{j-1}
          +\gamma\theta^{N-j}+w_N,\quad 1\le j\le N.
 \end{split}                                           \tag{6}
\]
The verified \(\Delta>0\) implies \(w_N>0\), and direct geometric
summation gives \(\sum_jh_j^{(N)}=H\).
These are **genuine productive no-hinge** tents: the rational
parameter identity gives
\[
 \frac{d\theta}{\ell}
 =2(1+\theta)^2-\theta=2+3\theta+2\theta^2>1,
\]
so \(dh_1^{(N)}>y\), and for every \(j\ge2\), each of the three
nonnegative terms in (6) separately satisfies
\(d h_j\ge\ell h_{j-1}\):
\[
 d\theta>\ell,\quad d/\theta>\ell,\quad d>\ell.
\]
The entire positive duration word lies in the saved wedge because
\(H\le1/16\), every return lies between \(b-H\ge7/8\) and \(b\),
and the endpoint/inverse inequalities for these no-hinge returns
are already certified for that wedge.

To compute its limiting cost, split (6) into the two geometric source
columns and the uniform term \(w_N=O(N^{-1})\). The two sources solve
their respective infinite tridiagonal Green equations:
\(K(\alpha,\alpha\theta,\ldots)^\mathsf T=\alpha e_1\)
and its reverse counterpart
\(K(\ldots,\gamma\theta,\gamma)^\mathsf T=\gamma e_N\),
up to endpoint errors \(O(\theta^N)\).
Their mutual interaction is \(O(N\theta^{N-1})\).
The constant term contributes \(O(Nw_N^2)+O(w_N)\to0\).
It follows by direct substitution into the exact no-hinge energy that
\[
 \boxed{\lim_{N\to\infty}E_y(h^{(N)})=
 -C_0(\alpha^2+\gamma^2)-\frac{y^2}{8k}
 =E_\infty(y).}                                         \tag{7}
\]
Thus (2)-(7) give an **exact infimum over actual legal finite routes**.
No unjustified continuity of first-hitting times for a limiting
Zeno path is invoked. In particular, this theorem does not claim
that an infinitely turning physical path attains the infimum.

## 4. The unique exact phase boundary and the high-surplus extension

For \(0\le y\le2H/5\), \(y<dH\), and
\[
 E_1(H,y)-E_\infty(y)
 =C(H)-\frac H2y+\frac{\theta}{4\ell}y^2,\quad
 C(H):=AH^2-\frac{3\ell H}{2}+\frac{9\ell\theta}{4}.     \tag{8}
\]
Its derivative in y is strictly negative on the band, since
\(\theta(2/5)/\ell<1\).

Exact rational lower and upper enclosures for theta show
\(C(H)>0\) for \(H\in[1/20,1/16]\); it is increasing there.
The previous uniform one-return theorem's four-corner certificate
gives \(E_1(H,2H/5)-E_\infty(2H/5)<0\) on the same interval
(direct rational verification is also included).
Consequently (8) has one and only one zero
\(y_*(H)\in(0,2H/5)\).
Explicitly, it is the **smaller root**
\[
 y_*(H)=\frac{\ell}{\theta}
 \left(H-\sqrt{H^2-\frac{4\theta}{\ell}C(H)}\right).     \tag{9}
\]

For \(2H/5\le y<kH\), the separate all-count theorem
LOW_SURPLUS_UNIFORM_SINGLE_RETURN.md proves that a single return
strictly beats every multi-return policy, including the initial-hinge
case \(y>dH\). Combining this with (2)-(9) proves (1).
Terminal Zeno chains that accumulate at b without an earlier reset
cannot lower the infimum: replacing the shrinking last tail by one
productive tent gives a finite chain with the same limit, by the
previously proved captured-rank-band estimate.

## 5. Meaning and remaining obligations

This result **completely optimizes all finite productive center-return
counts**, plus no-reset terminal-Zeno limits, in a continuous
\(H\in[1/20,1/16]\) time strip with the specified terminal row,
terminal tour, and **no initial waiting**. The optimal object in
the low-surplus phase is an explicit *approaching* family with an
early decreasing geometric source, a vanishing-width center-return
middle region, and a late increasing geometric source. It is not an
arbitrarily imposed M3/M4 cutoff.

Still open: all earlier horizon values \(H<1/20\) at low surplus;
productive initial waits and intermediate front resets; exterior exits
before/after b; attaching the resulting full center Bellman value to
every initial Monster start; and finding a complete Princess CDF and
Monster mixed law with matching **unrestricted** saddle inequalities.
Neither player's global optimal CDF or the full game value is
established here.

## Reproduction

Run \`python packages/interval_turn_sheet/verify_two_source_outer_envelope.py\`.
The exact verifier checks (5), both theta enclosures, the root-crossing
signs, all polynomial convexity coefficients and required positivity
with standard-library Fraction arithmetic; the universal all-m
inequalities are proved analytically above. No Lean or CI run is claimed.
