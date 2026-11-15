# Infinite-turn renewal in the center layer

Date: 2026-11-12. **Structural result only; the unrestricted game remains open.**

This checkpoint attacks the possibility that the equilibrium support has no
finite turn cutoff. The answer is affirmative at the conditional center
level, and the current exact upper law already contains positive mass through
seven direction reversals.

## 1. The finite upper law is already sampling higher-turn behavior

For the certified 280-pair law in
`packages/interval_global_closure/upper_dyadic_exact.json`, grouping positive
weights by direction reversals gives

| reversals | mass |
|---:|---:|
| 0 | 6522690337/10^10 |
| 1 | 817845233/5000000000 |
| 2 | 450161789/2500000000 |
| 3 | 35750697/10^10 |
| 4 | 11299/2500000000 |
| 5 | 2513551/5000000000 |
| 7 | 74523/5000000000 |

The largest five-reversal correction has mass `4960732/10^10` and was
introduced by a `physical_node_attack` from the continuum response search,
not by a prescribed finite-turn template. Seven is therefore not a justified
cutoff.

## 2. Exact all-count renewal energy

In the terminal affine center cell write

    R(U,V)=k U-ell V+c,   d=k-ell,   r=ell/k in (0,1/8),
    theta=(1-sqrt(1-8r))/(1+sqrt(1-8r)).

The existing front theorem already proves an actual Zeno optimum: at the
critical duration

    H_* = 3 theta/(1-theta)

successive center excursions shrink geometrically and infinitely many returns
attain the conditional value.

For a neighboring non-front state let `y=n-z(t)` be the captured-rank gap and
let `h_1,...,h_m` be productive center-return durations ending on the terminal
row. Direct substitution in the exact renewal formula gives

    E_y(h)=Q(h)-y h_1/2-y^2/(8k)
      -(y-d h_1)_+^2/(8k)
      -sum_{j=2}^{m-1}(ell h_{j-1}-d h_j)_+^2/(8k)
      -(ell h_{m-1}-d h_m)_+/2,                         (1)

where

    Q(h)=(k/8-ell/2) sum h_j^2
         -(ell/2) sum h_j h_{j+1}-(3ell/2)h_m.          (2)

Thus all turn counts are governed by one nearest-neighbor piecewise-quadratic
functional; separate M4/M5/... payoff lemmas are unnecessary.

An active quadratic short-return hinge has curvature

    (k/8-ell/2)-d^2/(8k)
      = -ell(2k+ell)/(8k) < 0.                           (3)

Hence a hinge-active minimum is forced onto a productivity, hinge, duration,
or adjacent-status interface. The unresolved hinge problem is therefore a
boundary problem, not an interior continuum of short-return shapes.

## 3. Exact two-source Green bridge at fixed physical duration

On a no-hinge cell put

    C0=ell/(4theta),  alpha=theta y/ell,  gamma=3theta.

Then the h-dependent part is

    C0 [h^T K_m h-2alpha h_1-2gamma h_m],               (4)

where K_m is tridiagonal with diagonal `1+theta^2` and adjacent entries
`-theta`. Its two endpoint Green columns are explicit:

    (K^-1 e_1)_j = theta^(j-1)(1-theta^(2(m+1-j)))
                    /(1-theta^(2m+2)),
    (K^-1 e_m)_j = theta^(m-j)(1-theta^(2j))
                    /(1-theta^(2m+2)).                  (5)

The terminal row fixes the duration; unused time is not a free wait away
from the front. Define

    c_m=(1-theta^m)/((1-theta)(1+theta^(m+1))),
    P_m=(m-2theta c_m)/(1-theta)^2,
    zeta_m=((alpha+gamma)c_m-H_*)/P_m.

The fixed-duration stationary bridge is exactly

    h=K_m^-1(alpha e_1+gamma e_m-zeta_m 1).              (6)

With

    u_m=(1-theta^(2m))/(1-theta^(2m+2)),
    v_m=theta^(m-1)(1-theta^2)/(1-theta^(2m+2)),
    q=alpha/gamma=y/(3ell),   s=1/(1-theta),

the normalized fixed-m value is

    Psi_m(q)=-u_m(1+q^2)-2v_m q
             +((1+q)c_m-s)^2/P_m.                       (7)

At q=0 this is the existing front problem and finite m converges to the
actual Zeno control. For q>0, `Psi_(m+1)=Psi_m` is an explicit quadratic in
q. Its small positive root q_m satisfies

    q_m ~ ((1+theta)/2) theta^(m+1),
    y_m=3ell q_m.                                       (8)

Therefore the finite-turn transition layers accumulate geometrically at the
Zeno front. A regular entry-state density would induce geometrically
diminishing probability of increasingly high turn counts; an atom on the
front gives positive probability to the Zeno pure control itself.

For the saved terminal cell

    k=10.494377622736,
    ell=0.06567633736,
    theta=0.012839966589597487...,
    H_*=0.039020927169949733...,

the first y-transition scales are approximately

    3.33281522262e-5,
    3.18902287962e-7,
    3.63180793080e-9,
    4.36702242568e-11,
    5.37944152964e-13.

## 4. Consequence and remaining gate

The evidence now favors

    finite coarse outer phases
      + an all-count renewal center layer
      + endpoint completion,

rather than `M1+M2+M3` with a finite cutoff. The natural mixed-strategy
variable is an entry-state measure plus a renewal policy; turn-count weights
are induced by that state.

The next local obligation is the **two-source hinge/interface gate**: compare
every boundary configuration of (1) with the Green branch (6) and the already
proved reset/front/terminal renewal pieces, uniformly over the physical
terminal wedge. This is one piecewise-quadratic interface problem, not an
open-ended sequence of turn lemmas.

No global game bound changes here.

## Reproduction

Run

```sh
python packages/interval_turn_sheet/verify_two_source_turn_tail.py
```

The verifier checks the Green/KKT identities, (1), the curvature identity
(3), the saved-cell adjacent-count roots, and the exact turn-count masses of
the certified 280-pair law. The executed output is
`packages/interval_turn_sheet/two_source_turn_tail_report.json`.
