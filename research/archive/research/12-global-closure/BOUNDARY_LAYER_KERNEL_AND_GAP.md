# Exact endpoint-layer kernel and the retained n64 fixed-law obstruction

Research note with independently reviewed kernels and structural lemmas,
2026-11-14. Sections 1–6 were reviewed by the root and verification agents;
Sections 7–12 were independently reviewed by both audit and verification
agents, including the corrected direct-inward coefficient in (19).

This note combines the exact boundary-gap diagnostic for the retained n64
Monster certificate with the complete two-parameter initial-inward kernel.
The kernel is a restricted family of Princess tests. It is not an upper
certificate against all Princess paths and does not identify the global
equilibrium value.

## 1. Physical paths and conventions

Use initial deficit `a` and outgoing deficit `z` for the Monster:

\[
                 0\le a\le z<1.
\]

The positive member of the fair reflected pair `I_{a,z}` has vertices

\[
 (0,1-a),\quad
 ((z-a)/2,1-(z+a)/2),\quad
 (z/2,1-z/2),\quad
 (2,-1),\quad(4,1).
 \tag{1}
\]

It initially goes inward, turns outward along `W=-1+z`, and turns inward
again on `U=1`. The case `a=z` is the pure-outward initial M2 route. The
case `a=0` is the direct endpoint sweep, independently of `z`; the middle
outward leg has zero duration.

For the Princess take

\[
                 0\le\varepsilon\le h<1
\]

and the nonnegative radial path

\[
 p_{\varepsilon,h}(t)=
 \begin{cases}
  1-\varepsilon-t,&0\le t\le(h-\varepsilon)/2,\\
  1-h+t,&(h-\varepsilon)/2\le t\le h,\\
  1,&t\ge h.
 \end{cases}
 \tag{2}
\]

Reflect it fairly. For `ε>0` this is an endpoint-stopped legal loop. The
case `ε=h` is immediate outward motion. The actual `ε=0` path starts at
the endpoint and then leaves it if `h>0`; it is included as a legal
boundary case to distinguish an actual endpoint start from the limit
`ε→0+`. It is not an absorbed-at-first-contact Princess path in that case.

The negative target is captured at time two for all parameters in these
domains: the Monster remains positive until time one, whereas that target
has already reached `-1` by time `h<1`.

## 2. Complete capture kernel, including ties

Let `K(a,z;ε,h)` be the fair expected capture time. Away from the two
contact equalities, direct physical intersection gives

\[
\begin{array}{c|c|c}
 &h<z&h>z\\ \hline
 \varepsilon>a
   &1+(h-a)/4&1+h/4\\[2pt]
 \varepsilon<a
   &3&1+(z-\varepsilon)/4.
\end{array}
 \tag{3}
\]

The actual equality values are

\[
 \boxed{\varepsilon=a\quad\Longrightarrow\quad K=1,}
 \tag{4}
\]

because the positive target is captured at time zero, and, when
`ε!=a`,

\[
 \boxed{h=z\quad\Longrightarrow\quad
 K=1+\frac{z-\min(a,\varepsilon)}4.}
 \tag{5}
\]

Initial contact (4) is applied before (5). These formulas include `a=z`,
`ε=h`, and the zero-parameter cases. They do not replace a contact value
by an adjacent one-sided trace.

### Derivation

If `a<ε`, the Monster initially lies to the right of the Princess. When
`h<z`, its first inward leg meets the Princess after her outward turn at
time `(h-a)/2`. When `h>z`, the Monster turns outward too early to meet
her there; its final inward `U=1` leg catches her at time `h/2`.

If `a>ε`, the Monster starts to the left. When `z<h`, its middle outward
leg meets her initial inward leg at time `(z-ε)/2`. When `z>h`, it misses
her before she begins outward motion and cannot meet her again until its
positive endpoint visit at time four.

The reflected target always contributes time two, yielding (3). At `h=z`
the first meeting occurs exactly at a turn, giving (5). At `ε=a`, actual
initial co-location gives (4), regardless of subsequent turns.

For the direct endpoint sweep `E`, the distinction at zero offset is
especially important:

\[
 K_E(\varepsilon,h)=
 \begin{cases}
  1+h/4,&\varepsilon>0,\\
  1,&\varepsilon=0.
 \end{cases}
 \tag{6}
\]

Thus an `ε→0+` calculation cannot substitute the actual `ε=0` path.

## 3. A universal initial-gap test for a fixed Monster law

Let a normalized Monster law have mass `q` on the direct endpoint sweep
pair. Suppose every other supported start satisfies

\[
                    |m(0)|\le1-\delta,
                         \qquad 0<\delta<1.
\]

Write its endpoint-time baseline as

\[
 M=\frac12\mathbb E(\tau_-+\tau_+).
\]

If every path sweeps directly after its first endpoint `σ`, as the retained n64
certificate does, then `M=1+Eσ`.

For `0<ε<=h<δ`, no non-endpoint-start Monster can meet either target of
(2) before the target reaches its own endpoint. On the initial inward
piece, its distance from the positive target is at least
`δ-ε-2t>=δ-h>0`; on the outward piece it is at least `δ-h>0`. Reflection
gives the other sign. These targets are therefore captured exactly at
the Monster's respective endpoint times.

The loop payoff against the entire law is exactly

\[
                         J_\nu(\varepsilon,h)=M+qh/4.
 \tag{7}
\]

Taking `h→δ-` gives the law-specific lower bound

\[
                  \sup_{\text{Princess}}J_\nu
                       \ge M+q\delta/4.
 \tag{8}
\]

This is a lower bound on the worst Princess response to this **fixed
Monster law**, not a lower bound on the unrestricted game value. The
strict approach from below avoids initial-contact atoms at the largest
interior start. A supremum is intended; no limiting-path attainment is
assumed.

## 4. Exact diagnostic for the retained n64 certificate

For `packages/interval_clock_grid/upper_n64_physical.json.gz`, whose exact
input SHA256 is

`2a09355539fa015a0b281843a9db108c4a619243118eb0d57d14144cab20d89a`,

the independent physical replay gives

\[
 q=\frac{630441926044}{10^{12}},\qquad
 \delta=\frac1{64},\qquad
 M=\frac{2276326166273}{1600000000000}.
\]

The stored exact upper certificate is

\[
 U=\frac{364842628535291}{256000000000000}.
\]

Its distance from the explicit boundary-loop lower bound is exactly

\[
 \boxed{U-M-q\delta/4
       =\frac{5567}{256000000000000}
       \approx2.174609375\times10^{-11}.}
 \tag{9}
\]

Thus this physical Monster law is priced to essentially its exact worst
response by the short initial endpoint-layer loops. A materially smaller
upper bound requires changing the physical law, rather than merely
improving its stored clock/matching witness.

The stored upper bound remains supported by its separate exact flow
certificate. The replay accompanying this note checks the physical
geometry and the lower witness (7); it does not duplicate that flow proof.

## 5. Why gap-confined repairs cannot remove this obstruction

Keep the old interior-start law fixed and replace its endpoint-sweep mass
`q` by an arbitrary measure `η` of total mass `q` on the rows (1). Suppose

\[
                  0\le a\le z<\delta
                       \quad\eta\text{-almost surely}.
 \tag{10}
\]

Test the new law on the immediate-outward Princess family `ε=h`, with
`h→δ-`. For every fixed row satisfying (10), eventually `a<=z<h=ε`, so
(3) gives `K=1+h/4`. The kernel is bounded, hence dominated convergence
gives the same limiting payoff as the old endpoint sweep mass:

\[
              M_{\rm old}+q\delta/4.
 \tag{11}
\]

Here `M_old` is the baseline of the old law before the replacement; the
new law's own endpoint-time baseline generally changes. No claim of its
equality with `M_old` is being made.

Therefore arbitrary redistribution into initial-inward rows whose outgoing
deficits remain strictly inside the old gap cannot remove the old bound.
This holds for continuous repair measures as well as finite ones.

The boundary `z=δ` must be kept explicit. An atom there with `a<δ` sees
the approaching immediate-outward tests in the `h<z` regime and can lower
their payoff by `a/4`. The argument above therefore does **not** exclude
boundary-touching repairs. A successful repair must give positive mass
to `z>=δ`, or alter the second front, the old bulk law, or another part of
the construction. Merely reaching this necessary condition does not prove
that a repair controls all Princesses.

For the pure-outward subclass `a=z<=δ`, the same obstruction persists
even if there is mass at `a=z=δ`: that row gives cost three for `h=ε<δ`,
which only increases the limiting worst payoff. This is why flattening a
kernel after taking `ε→0` prematurely does not repair the actual game.

## 6. Exact physical regression and its scope

The single standard-library script
`verify_boundary_layer_kernel.py` uses chronological intersections of
actual rational affine paths. It unions their breakpoint times, checks
initial and endpoint equality, and solves each possible linear crossing
exactly with `fractions.Fraction`. It does not use formula (3) to determine
the first capture time.

Its accompanying `boundary_layer_kernel_replay.json` reports:

* 6,084 exact inward-kernel comparisons, including both contact equalities,
  immediate-outward Princesses, pure-outward Monsters, and all zero-offset
  closure cases;
* 78 direct-sweep comparisons, including the discontinuity in (6);
* all 736 calendar plans of the retained physical n64 certificate replayed
  against six rational loops, with exact agreement with (7);
* 129 exact checks of the law-specific outward-completion cutoff profile
  from `LAW_SPECIFIC_OUTWARD_COMPLETION.md`;
* exact recovery of every quantity in (9).

Run, for example,

```sh
python -B packages/interval_global_closure/verify_boundary_layer_kernel.py \
  --physical-certificate packages/interval_clock_grid/upper_n64_physical.json.gz \
  --report packages/interval_global_closure/boundary_layer_kernel_replay.json
```

from the repository root. The canonical script and report live in
`packages/interval_global_closure/`; this proof note belongs with the other
global-closure research notes.

The exact kernel constrains a boundary-sector design. It leaves the
all-Princess response, attachment to interior contact families, and the
global equilibrium problem open.

## 7. A stronger Princess path: shadowing the principal front

The inward/outward loops in Sections 1–5 are not an exhaustive boundary
response family. Fix `0<eta<epsilon<h<1` and use the radial Princess path

\[
 (0,1-\epsilon),\quad
 ((\epsilon-\eta)/2,1-(\epsilon+\eta)/2),\quad
 ((h-\eta)/2,1-(h+\eta)/2),\quad (h,1).
 \tag{12}
\]

Its velocities are `+1,-1,+1`. During the middle leg it stays on
`U=t+r=1-eta`, strictly below the Monster's principal turning front.
It reaches `U=1` only at time `h/2`, then reaches the endpoint at time `h`.
Call it the shadow path `S_{eta,epsilon,h}`. Both it and the original loop
`L_{epsilon,h}` have fast-sweep score `1+h/4`.

For `I_{a,z}`, the negative Princess is again captured at time two.
The complete fair-pair shadow kernel is the following ordered case table;
the initial-equality row has priority.

| Condition | Shadow score |
|---|---:|
| `a=epsilon` | `1` |
| `z<epsilon` | `1+h/4` |
| `eta<=a<epsilon<=z` | `1+(epsilon-a)/4` |
| `a<eta`, `h<=z` | `1+(h-a)/4` |
| `a<eta`, `z<h` | `1+h/4` |
| `a>epsilon`, `z<=h` | `1+(z-eta)/4` |
| `a>epsilon`, `z>h` | `3` |

In particular, the equalities `a=eta`, `z=epsilon`, and `z=h` cannot be
replaced by arbitrary limiting branches. For example, when
`a<eta` and `z=h`, the original inward Monster leg meets the Princess
at the Monster's first turn, giving `1+(h-a)/4`.

Also write `D_a` for the direct initial-inward route

\[
 (0,1-a),\quad(2-a,-1),\quad(4-a,1),\qquad 0\le a<1.
\]

Its shadow score is `1-a/2` at `a=epsilon`, `3-a` for `a>epsilon`,
`1+epsilon/4-3a/4` for `eta<=a<epsilon`, and
`1+h/4-3a/4` for `a<eta`. The pure-outward route is `P_z=I_{z,z}`.
These formulas follow by intersecting the corresponding affine physical
legs. They use actual first contact, not a limiting CDF trace.

### The exact cost of the missed attack

Suppose a boundary Monster law has a fast-sweep atom, direct-inward density
`X(a) da`, and pure-outward density `Y(z) dz`. Then, for densities with no
atoms on the displayed boundaries,

\[
 4\{C(S_{\eta,\epsilon,h})-C(L_{\epsilon,h})\}
  =(\epsilon-\eta)\int_\epsilon^hY(z)\,dz
       -(h-\epsilon)\int_\eta^\epsilon X(a)\,da.
 \tag{13}
\]

The first term is a delayed positive-side capture by `P_z` for
`epsilon<z<h`. The second is an earlier positive-side capture by `D_a`
for `eta<a<epsilon`. The endpoint atom contributes zero difference.

Thus a law that makes inward/outward loops nearly indifferent can still
have a profitable shadow attack. If `Y` is of constant order and `X` is
of the order of the layer width, (13) can be of quadratic order in that
width. A cubic improvement found using only the original loops does not
control it. Formula (13) is a response comparison, not a global value
bound.

## 8. What an initial-inward sheet contributes

Let the law also have a density `zeta(a,z) da dz` on `0<a<z<1` for the
initial-inward routes `I_{a,z}`. Off boundary atoms, the full exact
shadow-minus-loop comparison is

\[
\begin{aligned}
 4\Delta={}&(\epsilon-\eta)
 \left[\int_\epsilon^hY(z)\,dz
       +\int_{\epsilon<a<z<h}\zeta(a,z)\,da\,dz\right]\\
 &-(h-\epsilon)
 \left[\int_\eta^\epsilon X(a)\,da
       +\int_{\eta<a<\epsilon,\ z>\epsilon}
                      \zeta(a,z)\,da\,dz\right]\\
 &-\int_{\eta<a<\epsilon,\ \epsilon<z<h}
                        a\,\zeta(a,z)\,da\,dz.
\end{aligned}
 \tag{14}
\]

For `eta<a<epsilon` and `epsilon<z<h`, the inward Monster leg catches
the shadow at time `(epsilon-a)/2`, whereas it catches the original loop
only at time `h/2`. This is the extra `a`-weighted term in the last line.
For `z>h` in the same initial band, the improvement is instead
`(h-epsilon)/4`, giving the second line. For `epsilon<a<z<h`, shadowing
delays the outward-leg capture, giving the positive triangular term.

If `X,Y` are continuous at `epsilon`, the initial marginal of `zeta` is
continuous there, and `zeta` has a continuous one-sided trace at the
corner `(epsilon,epsilon)`, then

\[
 \lim_{\substack{\eta\uparrow\epsilon\\ h\downarrow\epsilon}}
 \frac{4\Delta}{(\epsilon-\eta)(h-\epsilon)}
  =Y(\epsilon)-X(\epsilon)
     -\int_\epsilon^1\zeta(\epsilon,z)\,dz
     -\epsilon\zeta(\epsilon,\epsilon).
 \tag{15}
\]

This identifies two ways that inward rows can counter the shadow swap:
their total initial density, and concentration near zero initial-turn
duration. Singular sheets and atoms must be treated using the physical
kernel, rather than by inserting them into (15).

If a proposed contact model requires all these local swaps to be
nonprofitable, its right side in (15) must be nonpositive. This is a
conditional contact requirement. It is not an unconditional equation for
a global saddle: if the compared loop is not an active Princess response,
a positive difference need not exceed its old slack below the value.

## 9. A conditional complete response reduction within one short layer

There is a precise positive result for the law consisting only of
`E,D_a,P_z`. Fix the Princess initial radius `1-epsilon` and first hitting
time `h/2` of `U=1`, where `epsilon<=h<1`. Forcing the Princess maximally
outward after that hit weakly increases her payoff against every one of
these Monster rows. All still-uncaught positive targets can then be
caught only at the prescribed positive endpoint; all negative targets
are caught as late as their corresponding descending sweep permits.

Before that hit, the light coordinates are nondecreasing and traverse

\[
 U:1-\epsilon\longrightarrow1,\qquad
 W:-1+\epsilon\longrightarrow h-1.
\]

Apart from fixed terms, the score is half the sum of the first-visit times
of the `U` levels `1-a`, weighted by `X(a)` for `0<a<epsilon`, and the `W`
levels `z-1`, weighted by `Y(z)` for `epsilon<z<h`.
For each pair of such levels, the cross contribution is

\[
 \frac14\bigl[X(a)1_{\{W_z\text{ first}\}}
              +Y(z)1_{\{U_a\text{ first}\}}\bigr],da\,dz.
 \tag{16}
\]

The portions due to movement in the same coordinate are fixed. This
identity follows directly from `2t=U+W` at a first visit and Fubini.
Consequently, if

\[
       Y(z)\ge X(a)
       \qquad (0<a<\epsilon<z<h),                         \tag{17}
\]

putting every `U` level before every `W` level maximizes the score.
The shadow paths achieve its supremum as `eta` tends to zero from above;
the last `eta` of `U` movement is reserved to keep the first `U=1` hit at
exactly `h/2`. This proves an exact response reduction in this conditional
short-layer problem, not merely a numerical comparison with one new path.

The hypothesis fixes the first principal-front hit before time one-half.
There is no proof here that a Princess against the full bulk law may be
restricted to that cutoff. Adding an initial-inward Monster sheet also
changes the pair-order functional; its extra terms are exactly the issue
exposed by (14).

## 10. A safe attachment to the inner initial band

For any `0<delta<1`, a useful comparison does hold against completely
arbitrary legal Princess paths. Suppose the initial radius satisfies
`r(0)<=1-delta`. Every `D_a` and `P_z` with `a,z<=delta` captures each
signed target no later than the endpoint sweep `E` does.

For `P_z`, the physical path joins `E` at time `z/2`. Before that time,
its positive branch stays outside the initially inner positive target by
the unit-speed bound; the negative target is on the other side. The fast
sweep also cannot reach either target before the joining time. Subsequent
paths agree. Initial equality can only make `P_z` capture earlier.

For `D_a`, both signed targets start at or to the left of `1-a`.
During its first descending leg, `D_a(t)=E(t)-a`. If `E` meets a target
before `D_a` reaches the negative endpoint, continuity forces `D_a` to
have met it already. Otherwise `D_a` has met it by that endpoint.
This proves the pointwise comparison for both reflections.

Therefore replacing any endpoint-sweep mass by an arbitrary mixture of
such `D_a,P_z` rows cannot raise the payoff of any Princess starting in
`[0,1-delta]`. Only the outer initial band needs a new upper estimate.
This lemma permits a macroscopic layer to be considered while retaining
the old bulk law. It does not assert that the old bulk's constant-baseline
formula continues to hold throughout the larger layer.

## 11. Exact shadow regression

The additional standard-library script
`packages/interval_global_closure/verify_boundary_shadow_kernel.py` imports
the already checked chronological affine-intersection evaluator. Its
sibling report `boundary_shadow_kernel_replay.json` records:

* 9,075 exact `I_{a,z}` shadow-kernel cases, including initial and turn ties;
* 1,650 direct-inward cases and 165 endpoint-sweep cases;
* 1,365 direct-inward and 1,365 pure-outward difference comparisons for
  the two terms of (13).

Run it from the repository root with

```sh
python -B packages/interval_global_closure/verify_boundary_shadow_kernel.py
```

The full `I` case table also checks the rowwise ingredients of (14).
These are exact finite regressions of the analytic formulas. They are
not a proof that the boundary family or its short completion horizon is
sufficient for the unrestricted game.

## 12. A monotone contact relation for the shadow trace

The sheet kernel also supplies a compact boundary contact system. Assume
`X,Y,zeta` are smooth densities on their open parameter domains, with
integrable continuous traces where differentiation is used. Keep all
endpoint-start mass in the separate atom `q`. Define the one-sided
shadow payoff

\[
 \mathcal C(e,h)=\lim_{\eta\downarrow0}
                  C(S_{\eta,e,h}),\qquad 0<e<h<1.
\]

This is a limit of legal paths. Substituting `eta=0` into the physical
path itself would make it touch `U=1` earlier, and is not the same
operation.

Put

\[
 A(e)=q+\int_0^eY(z)\,dz
          +\int_{0<a<z<e}\zeta(a,z)\,da\,dz,
 \qquad
 B(e,h)=Y(h)+\int_e^h\zeta(a,h)\,da.
\]

The physical kernel gives the exact front derivative

\[
             4\mathcal C_h(e,h)=A(e)-(8-h)B(e,h).
 \tag{18}
\]

The direct-inward density does not appear: in this limit its positive
captures occur on the first outward leg, while its negative captures
remain at their endpoints, so changing the later shadow duration does
not change them. The coefficient `8-h` is the difference between a
missed positive-side capture and a capture at the principal turn.

The complementary start derivative is

\[
\begin{aligned}
 4\mathcal C_e(e,h)={}&\int_0^eX(a)\,da-(8-2e)X(e)+(h-e)Y(e)\\
 &+\int_{a<e<z}\zeta(a,z)\,da\,dz
   +\int_0^e(h-e+a)\zeta(a,e)\,da\\
 &-\int_e^h z\zeta(e,z)\,dz
       -8\int_h^1\zeta(e,z)\,dz.
\end{aligned}
 \tag{19}
\]

An interior active shadow trace must satisfy both derivatives equal to
zero. Boundary contacts use the corresponding one-sided inequalities.
The formulas can be checked directly by partitioning the sheet into
`z<e`, `a<e<z`, `e<a<z<h`, and `h<z,a>e`; their four costs are respectively
`1+h/4`, `1+(e-a)/4`, `1+z/4`, and `3`.

A useful sign follows without solving those equations:

\[
 4\mathcal C_{eh}(e,h)
    =Y(e)+\int_0^e\zeta(a,e)\,da+(8-h)\zeta(e,h)\ge0.
 \tag{20}
\]

For a fixed positive `eta`, the same calculation gives

\[
 4\,\partial_{eh}C(S_{\eta,e,h})
    =Y(e)+\int_\eta^e\zeta(a,e)\,da
                    +(8-h+\eta)\zeta(e,h)\ge0.
\]

When the mixed derivative is strictly positive across a rectangle, two
maximizing pairs cannot have opposite order in their coordinates. Indeed,
for `e_1<e_2` and `h_1<h_2`, integration of (20) gives

\[
 \mathcal C(e_1,h_1)+\mathcal C(e_2,h_2)
   >\mathcal C(e_1,h_2)+\mathcal C(e_2,h_1).
\]

If the two terms on the right were both global maxima, the left side
could not be larger. For two oppositely ordered feasible pairs, their
cross pairs also lie in `e<=h`, so there is no missing feasibility case.
Thus active shadow contacts form a nondecreasing relation between the
initial deficit and the principal-front time whenever the indicated
strictness holds; they cannot fill an open two-dimensional region.
Vertical or horizontal contact intervals are not excluded.

Equations (18)–(20) give a possible one-dimensional boundary contact curve
and its coupling to the inward sheet. They do not prove that all optimal
Princess paths are shadows, that this sheet is the complete Monster
support, or that the resulting contact system has a global saddle
solution. The earlier finite response theorem and the bulk contact
identities remain necessary for those missing checks.
