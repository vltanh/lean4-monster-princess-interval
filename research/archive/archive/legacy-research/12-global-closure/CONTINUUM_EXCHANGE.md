# Whole-CDF synthesis with global physical-route separation

This work constructs complete legal Princess laws and searches for their
Monster responses. It does not establish an unrestricted saddle point.
The exchange loop uses every free CDF value at once and a search over
physical routes with no prescribed number of turns.

## A complete strategy representation

Write `U=t+r`, `V=t-r` for radius `0≤r≤1`. A radial CDF `R(U,V)` is
represented by its values on an entire triangular mesh. The imposed
conditions are

\[
0\le R\le1,\qquad R_U\ge0,\qquad R_V\le0,
\qquad R(0,0)=0,\qquad R(1,-1)=1.
\]

The declared terminal face is `R(U,Vmax)=0`. The corresponding law has
endpoint absorption by time `Vmax+1`. The original class has `Vmax=1`;
the extended class has `Vmax=2`, allowing center mass after time one and
absorption as late as time three. Neither class is asserted to contain an
unrestricted optimum. No constant center cone, endpoint tail formula,
late derivative restriction, or local matching condition is imposed.

At an interior point `x>0`, the signed CDF is `(1+R(t+x,t-x))/2`; at
`x<0` it is `(1-R(t-x,t+x))/2`. At the center the strict and closed CDFs
are `(1-R(t,t))/2` and `(1+R(t,t))/2`. At the two endpoints the appropriate
closed or strict trace is `0` or `1`. These traces retain actual contact
atoms.

The two characteristic inequalities give the speed-one light-cone
inequalities for these distributions. Consequently their ordered
quantiles are speed-one paths. A uniform rank, held fixed for the whole
path, therefore specifies an actual legal Princess law. The exported
field contains the entire CDF, not only values along selected routes.

`continuum_field.py` extends the original mesh and exact scorer. Alternate
unit strips reflect the nonuniform base grid so both physical diagonal
faces meet mesh vertices. A naive translation of every strip leaves
uncovered boundary slivers and is not used. The default extended mesh has
5,917 vertices and 11,560 triangles. Its total characteristic-plane area
is exactly the expected `1+2 Vmax=5` numerically to machine precision.

The values saved after isotonic repair lie on a decimal rational lattice.
`ExtendedExactField` checks every triangle's two transport derivatives in
exact rational arithmetic. The verification fixture has

\[
R(U,V)=\max(0,\min(U,1,2-V)),
\]

so it genuinely exercises late center mass: the center mass at time
`3/2` is `1/2`. Specialized route formulas agree with the generic
running-CDF integral on 116 routes; three independent exact unit-route
costs are `3/2`, `25/18`, and `7/4`.

## Global concavity and the master problem

For a continuous Monster path `m`, let

\[
L(t)=\inf_{0\le s\le t}F^-(s,m(s)),\qquad
H(t)=\sup_{0\le s\le t}F(s,m(s)).
\]

For the ordered quantile law, the captured ranks form the interval from
`L(t)` to `H(t)`, up to null rank endpoints. Thus its expected capture time
is

\[
J_m(F)=\int_0^\infty[1-H(t)+L(t)]\,dt.
\]

For a fixed complete physical route, this is a concave function of all
CDF values: a negative maximum and a minimum of linear forms are
concave. `RouteFunctional` integrates the running records exactly within
each affine cell, subject only to floating arithmetic. The independent
rational scorer evaluates unit-leg routes using first moments and checks
strict/closed contact semantics.

`continuum_master.py` maximizes the minimum over its current route bank.
It adds global supporting hyperplanes of each concave route payoff.
Every configured route is rescored after every solve. A secondary LP may
select the nearest field on the almost-optimal master face; this selects
an iterate without constraining the candidate class geometrically.

The LP objective is an upper bound on the optimum of this *fixed CDF
class against this finite bank*. It is not an upper bound on the original
game. Its route multipliers do give a concrete candidate Monster law,
which must be tested by the unrestricted Princess oracle separately.

## Physical response search in every exchange iteration

The exchange loop freezes each CDF iterate and invokes
`continuous_response_grid.py`. That search uses the native characteristic
nodes and quantized capture records. It has no turn-count cap. Its
decoded routes and all returned prefix endpoint completions are added to
the master, after scoring the complete continuum field. A previously
selected best field is rescored against every new route before it can
remain the incumbent.

The static bank also includes every legal signed M2 start and signed
first-turn characteristic on the native mesh. Turns on the negative half
use the generic record integral; the efficient M2 formula is used only
where its hypotheses hold. This closes the whole declared grid rather
than choosing a few offsets above `U=1`.

`continuum_inward_scan.py` evaluates all 54,145 native-grid initial-inward
routes by vectorized characteristic integrals. It takes about 0.2 seconds
to evaluate a field after geometry setup in the measured run. The master
adds the worst 512 routes, without constructing 54,145 dense gradients.
Only 486 were below 1.42355 in the measured early H3 iterate. This gives a
complete scan of that declared parameter grid in every iteration, while
the physical DP continues to search more general controls and center
waits. It is not a continuous-parameter or all-Monster certificate.

Record quantization is a discovery device in this loop. A decoded legal
route is a valid attack after exact rescoring regardless of the DP's
record approximation. The minimum over the returned routes does not
certify a lower bound against all Monsters. An unrestricted lower bound
requires the separate rigorous Bellman relaxation or another complete
response theorem.

Typical invocation:

```sh
python packages/interval_global_closure/continuum_master.py \
  --resume packages/interval_global_closure/continuum_free_candidate_12.json \
  --vmax 2 --initial-all --proximal --dp-bins 64 --dp-routes 8 \
  --tag continuum_exchange
```

## Why the automatic response loop matters

The first whole-CDF run converged against its 17,862 configured routes:

| Quantity | Value |
|---|---:|
| Minimum configured-route payoff | 1.423555001740737 |
| Supporting-cut master value | 1.423555046396745 |
| Difference | 0.000000044656008 |

The complete law is frozen in `continuum_free_candidate_12.json`, SHA256
`515cc2541dad42983b76fb411986ff69adcec7a08f0990235f455c6fb05aaa89`.
Its 6,936 triangle transport inequalities pass exact rational checking.
The route bank used for that result is preserved as
`continuum_h2_attack_routes.json`.

Nevertheless the global physical search found a stronger response. Its
simple two-interior-turn version is the legal unit-speed path

\[
\begin{aligned}
(0,9/16)&\longrightarrow(3/160,87/160)\\
&\longrightarrow(622597/2621440,1998853/2621440)\\
&\longrightarrow(524289/262144,-1)\\
&\longrightarrow(1048577/262144,1).
\end{aligned}
\]

Its exact-rescored payoff is approximately `1.41399400062525`, well below
the finite-bank minimum. The initial inward characteristic is `V=-21/40`
and the outward turn has `U=1+2^-18`. This attack is included in the new
exchange bank; it is not repaired by imposing a local condition at this
particular turn.

An independently rationalized unit-route law derived from the old CDF
dual has unrestricted Princess response approximately
`1.434887088574663`. Exact legal rational Princess paths realizing that
response are exported in `efficient_h2.princess_paths.json`. This tests
that *constructed rounded law*. Independently rounding turning positions
can break shared contact characteristics and change the global response
discontinuously, so the test does not reject an exactly aligned version
of the intended dual. Exact geometry must be reconstructed from native
characteristic labels and original rational source routes before a
dual-law comparison is conclusive.

## Continuing an interrupted solve

`continuum_hotstart.py` reuses the persistent HiGHS helpers from
`efficient_hotstart.py`: the first solve uses IPM with crossover, and
subsequent rows retain the simplex basis. The model checkpoint keeps all
physical constraints, every supporting cut, route metadata, current and
incumbent values, and the basis. `--resume-checkpoint PATH` restores that
state. It does not discard old cuts and restart from only a field.

For earlier cold runs without model checkpoints, `--replay-run TAG`
reconstructs supporting inequalities from their frozen CDF iterates and
route snapshots. The initial full bank is retained, and later replay
includes every route at or below the corresponding old master level, a
superset of the old violated batches. Historical worst-route payoffs are
checked before the replayed model is solved.

HiGHS ignores coefficients below its minimum supported matrix threshold.
The wrapper removes such terms explicitly and adjusts each right-hand
side by the removed term's minimum over the variable bounds. This keeps
every originally feasible point feasible; the unmodified coefficients
remain in the checkpoint. These LP calculations are still numerical
discovery, not exact game certificates.

The ongoing exchange artifacts carry their own route counts, DP record
resolution, input hashes, field-class horizon, and measured payoffs.
None of these discovery outputs changes the open unrestricted proof
gate by itself.
