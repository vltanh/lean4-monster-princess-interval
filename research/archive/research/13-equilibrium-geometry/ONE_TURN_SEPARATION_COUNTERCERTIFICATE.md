# One-turn separation test: closed by a physical countercertificate

**2026-11-14 UTC — the target `W_1 > U_*` is false.** A rational physical
Monster law in the canonical one-interior-turn class has a certified upper
against every legal Princess path:

\[
\boxed{
 W_1\le C:=\frac{142472349375511}{100000000000003}
 =1.424723493755067\ldots
 <\frac{57}{40}
 <U_*:=\frac{291849329389899}{204800000000000}.
}                                                               \tag{1}
\]

This proves alternative (M) of the
[separation directive](ONE_TURN_SEPARATION_DIRECTIVE.md), and excludes its
alternative (P). The exact restricted value \(W_1\), the unrestricted value
\(V\), and whether \(W_1=V\) remain open. In particular, (1) does not prove
that one interior turn suffices for an unrestricted optimal Monster law.

## 1. The game and the claim being closed

Both players choose independent hidden 1-Lipschitz paths in \([-1,1]\),
with free initial positions. Capture is the first coincidence, including
time zero. Let \(\mathcal B_1\) consist of Monster paths with unit-speed
straight legs, at most one interior reversal before the first endpoint,
and then a direct unit-speed sweep to the opposite endpoint. The endpoint
reversal is not counted as an interior turn. Define

\[
 W_1=\inf_{\nu\in\mathcal P(\mathcal B_1)}
       \sup_{p\text{ legal}}\mathbb E_{m\sim\nu}T(m,p).
\]

The Princess is unrestricted, including arbitrary turns, waits, endpoint
contacts, center contacts and initial coincidences. We exhibit one legal
\(\nu\) and prove its universal upper \(C\). No completeness or optimality
claim for the chosen Monster support is needed for this direction.

The comparison value \(U_*\) remains the frozen earlier unrestricted upper;
its historical certificate is unchanged. Because the new law is also legal
in the unrestricted game,

\[
 \frac{36409808231}{25600000000}\le V\le W_1\le C.             \tag{2}
\]

The new enclosure width is exactly

\[
 C-\frac{36409808231}{25600000000}
 =\frac{6311320912972370575307}{2560000000000076800000000}
 =0.002465359731629758\ldots.
\]

The inherited lower in (2) is a limiting game-value bound. The saved fixed
positive-width Princess law separately guarantees
\(582556541071/409600000000\); it is not assigned the larger limiting lower.

## 2. An explicit physical Monster distribution

All components below are paired fairly with their spatial reflections.
Let \(E\) be the pair of endpoint-to-endpoint sweeps. The endpoint-first
family and the one-interior-turn family have chronological vertices

\[
 S(a):\quad (0,a),\ (1-a,1),\ (3-a,-1),
\]

\[
 P_b(a):\quad
 (0,a),\ \left(\frac{b-a}{2},\frac{a+b}{2}\right),\
 (b+1,-1),\ (b+3,1).                                      \tag{3}
\]

For \(S\), the start support is \([-1,1]\). For \(P_b\), it is
\(I_b=[-\min(b,1),\min(b,2-b,1)]\). These restrictions make the
turn position nonnegative and at most one. Except for null boundary starts,
(3) is a genuine one-interior-turn route. Degenerate boundary starts may be
assigned their canonical endpoint representatives. Every route visits zero
by time two and completes its endpoint tour by time \(65/16\).

Put \(N=100000000000003\). The exact total component probabilities are:

| Component | Start support | Probability numerator over \(N\) |
| --- | --- | ---: |
| Endpoint sweep pair \(E\) | endpoints | 58529458302223 |
| \(S(a)\) | \([-1,1]\) | 23338621584333 |
| \(P_{15/16}(a)\) | \([-15/16,15/16]\) | 2557066763 |
| \(P_{31/32}(a)\) | \([-31/32,31/32]\) | 210093876391 |
| \(P_1(a)\) | \([-1,1]\) | 16091292591464 |
| \(P_{65/64}(a)\) | \([-1,63/64]\) | 1643036417352 |
| \(P_{33/32}(a)\) | \([-1,31/32]\) | 83345115201 |
| \(P_{17/16}(a)\) | \([-1,15/16]\) | 101595046276 |

These eight numerators sum to \(N\). The seven start distributions have
nonnegative piecewise constant densities on a common signed partition.
Its nonnegative knots are

\[
 \{j/16:0\le j\le15\}
 \cup\{1-2^{-k}:5\le k\le12\}\cup\{1\},                   \tag{4}
\]

together with their negatives. There are 48 signed start bins. For a bin
\([a_j,a_{j+1}]\) with saved integer mass \(m_j\), the density is exactly
\(m_j/[N(a_{j+1}-a_j)]\). Unsupported bins have zero mass. Thus the saved
integers, (3), and (4) specify the complete physical probability law; this
is a continuous start distribution, not a finite selection of start points.

The complete bin masses and certificate values are in
[one_turn_continuum_upper.json.gz](../../packages/interval_one_turn/one_turn_continuum_upper.json.gz).
Its canonical format contains integer numerators and rational geometry,
with no numerical CDF auxiliary columns or optimizer residuals. The exact
replay report also lists every bin probability in readable rational form.

## 3. Why the upper covers every Princess

The full proof and all cost formulas are in
[the continuum potential certificate theorem](ONE_TURN_CONTINUUM_POTENTIAL_CERTIFICATE.md).
Here is the chain from physical capture to the finite inequalities.

Reflection symmetry and ordered-quantile normalization reduce the upper
problem to fair reflected radial Princess paths. For this particular
Monster law, every Monster visits zero by time two. A surviving positive
Princess is then outside the Monster. Replacing her continuation by
\(p(t)=\min(1,p(2)+t-2)\) cannot advance capture. This reduces the response
to a radial path on \([0,2]\) with a specified physical outward completion.
There is no bound on the number of Princess turns before time two.

For strict radial paths, write \(r=p(0)\), \(U=t+p(t)\), and
\(W=t-p(t)\). Direct chronological capture integration gives

\[
 2\mathbb E_\nu T
 =A(r)+\int_0^2 G(r;U(t),W(t))\,dt
   +\sum_{r<b}J_b(W(\tau_b))+K(r,p(2)).                    \tag{5}
\]

Here \(\tau_b\) is the first \(U=b\) crossing. The explicit formulas
include the initial bonus
\(A(r)=\sum_{b\le r}(b+3)M_b\), which is essential for the two levels
below one. They also retain the late \(W=b\) terminal contribution for
levels above one, and the exact endpoint-sweep atom. Both neighboring
initial traces at \(r=b\) and both terminal phase traces are checked.

The domain \(0\le U-W\le2\), \(0\le U+W\le4\) is triangulated with
all density and phase boundaries aligned. On each of 28 phase regions and
at each of 25 radius knots, the certificate supplies continuous quadratic
Lagrange potentials \(V_k\). They satisfy

\[
 2(V_k)_U+G_k\le0,\qquad 2(V_k)_W+G_k\le0,
\]

the appropriate downward jump inequalities, the terminal inequality
\(V_k\ge K_k\), and the initial inequality
\(A(r)+V_{k(r)}(r;r,-r)\le2C\). Because \(U',W'\ge0\) and
\(U'+W'=2\), these inequalities telescope along every strict legal path
to bound (5) by \(2C\).

The finite checks extend to whole cells: the derivative-plus-cost
residual is convex on each triangle, edge residuals are quadratic and
checked in the Bernstein basis, and the initial trace is cubic after
linear interpolation in \(r\). Convexity of the cost and terminal term
in \(r\) proves coverage between radius knots. Consequently this is a
continuous all-path certificate, rather than a test of sampled Princess
positions or trajectories.

Finally, \(p_\epsilon=(1-2\epsilon)p+\epsilon\) makes any radial path
strict on \([0,2]\). With the outward completion, these paths converge
uniformly on the common capture horizon. First coincidence is lower
semicontinuous under uniform convergence, so Fatou's lemma transfers the
same upper to arbitrary radial paths. This restores time-zero ties,
endpoint paths, center contacts and unit-speed characteristic segments.
The normalization then gives the asserted upper for every original
Princess path and every Princess law.

## 4. Exact replay and strict comparison

The frozen file contains 259,738 integer entries: the claimed bound,
337 probability masses, and 259,400 quadratic potential values. A
standard-library Python verifier reconstructs the physical costs, density
supports, common mesh, phase connectivity, gradients and all Bernstein
coefficients from those integers. It checks:

| Inequality family | Exact rational inequalities |
| --- | ---: |
| Interior HJB vertex inequalities | 691200 |
| \(U\)-interface jump inequalities | 19050 |
| \(W\)-interface transition inequalities | 18000 |
| Time-two terminal inequalities | 1800 |
| Initial cubic Bernstein inequalities | 96 |
| **Total** | **730146** |

Every maximum positive residual is exactly zero. The reported upper is
therefore the saved rational \(C\) itself: **no residual repair is needed**.
The floating discovery objective, solver status, auxiliary CDF columns and
floating feasibility tolerances are not inputs to this replay.

The strict comparison can be checked with small rational differences:

\[
 \frac{57}{40}-C
 =\frac{1106024979731}{4000000000000120}>0,
 \qquad
 U_*-\frac{57}{40}
 =\frac{9329389899}{204800000000000}>0.                      \tag{6}
\]

The full improvement over the frozen benchmark is

\[
 U_*-C
 =\frac{6595786886122747988169697}
        {20480000000000614400000000000}
 =0.000322059906548952\ldots.
\]

The compressed input SHA256 is
`c87c7b902382396bce06e4265b6140077b50e336af48de5ff6d2f301af9dc482`;
its uncompressed SHA256 is
`5c76896d0a07983e2a0d27f4f99bd05d5242e56783ea9db2d1783b45c04d2a86`.
Both the initial frozen-file replay and a separate fresh root replay passed
the explicit counterexample gate with the same exact bound and zero repair.

## 5. Reproduction and independent physical audits

From the repository root, with Python's standard library only:

```sh
python3 packages/interval_one_turn/verify_continuum_upper.py \
  packages/interval_one_turn/one_turn_continuum_upper.json.gz \
  --output /tmp/one_turn_continuum_replay.json --require-counterexample
python3 packages/interval_one_turn/verify_continuum_upper.py --self-test
python3 packages/interval_one_turn/verify_continuum_functional.py
python3 packages/interval_one_turn/verify_continuum_physical.py
```

The main replay takes about ten seconds on the execution environment used
for this result. Its full report is retained as
[one_turn_continuum_upper_replay.json](../../packages/interval_one_turn/one_turn_continuum_upper_replay.json).
The analytic endpoint-only control has exact value \(3/2\) and zero repair;
the self-test also checks residual repair and malformed-input rejection.

The functional checker integrates actual chronological captures on complete
one-dimensional start arrangements, including individual density bins.
A separate physical checker, independent of the potential/HJB code,
passes 238 \(P_b\)-bin fixtures, 136 \(S\)-bin fixtures and 34 endpoint
fixtures, including 43 cases with \(r>b\), four with \(r=b\), and 24
late-\(W\) cases. Its report is
[continuum_physical_replay.json](../../packages/interval_one_turn/continuum_physical_replay.json).
These fixtures audit the formulas and implementations; the universal
extension is proved in the manuscript. No new CI run or Lean formalization
is claimed.

## 6. Consequences and remaining scope

Alternative (M) is now proved. By weak duality, no actual Princess law can
have security greater than \(U_*\) against all of \(\mathcal B_1\); a
controlled approaching family with such uniform limiting security is
also excluded. The separation search is therefore closed, not merely
paused at an unsuccessful candidate.

The full-domain theorem, restricted minimax identity, attained Monster
measure, exact finite-Princess pricing and convergent lower hierarchy
remain valid foundations. Earlier atomic and causal-clock certificates
remain reproducible, but their upper bounds are superseded by (1).

The certificate establishes one admissible continuous distribution and its
universal bound. It supplies neither a matching Princess lower at \(C\)
nor an equilibrium-support classification. Questions about the exact
restricted value, a strict gap between \(W_1\) and \(V\), optimal finite
Monster support, and the unrestricted saddle remain open.
