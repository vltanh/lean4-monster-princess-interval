# Off-grid response experiments: recovered mathematical record

Historical recovery note, 2026-11-13.

This note preserves the mathematical conclusions and exact numbers from
two computations completed before the execution environment became
unavailable. The original 95-node field arrays, standalone Fraction
verifier, and generated JSON replay were not uploaded before the outage
and have not been recovered. This file is therefore **not an executable
certificate and not a replacement for the missing field data**.

Two agents independently ran the original exact verifier before the
outage. The results below describe those historical checks. They should
not be cited as a newly replayed or independently reconstructible
certificate from this note alone.

## 1. Original fixture class and exact oracle

Both original fields used a characteristic mesh with light-coordinate
step \(1/2\), 95 signed-CDF vertices, and 160 triangles. The fields were
symmetric and legal, had sticky endpoint traces, moved their common
radial quantiles maximally outward after time \(2\), and were absorbed
at the endpoints by time \(3\).

The original verifier used standard-library Fraction arithmetic. It
reconstructed the characteristic geometry, checked the nodal reflection
and transport inequalities, checked the sticky and outward-after-two
conditions, and integrated strict capture records across field and
record crossings, including the endpoint jumps.

Its chronological lattice dynamic program considered every unit-speed
coordinate-axis lattice walk. Its state retained the physical lattice
vertex and both captured-rank records. Once the first endpoint was
reached, it used the direct sweep to the opposite endpoint. After
Princess absorption, the endpoint tour supplied the exact completion.
No beam cutoff or floating tolerance was used.

The scope was a restriction to unit-speed lattice walks. The dynamic
program did not include arbitrary waiting legs or arbitrary nonunit
constant-field legs.

## 2. Free initial-position example

The first field had nodal CDF values in tenths. The historical exact
lattice minimum was

\[
 \frac{83}{80},
\]

with a lattice response

\[
 (0,1/2)\longrightarrow(3/2,-1)\longrightarrow(7/2,1).
\]

A legal off-grid response was

\[
 (0,-5/9)\longrightarrow(14/9,1)\longrightarrow(32/9,-1),
\]

with exact payoff

\[
 \frac{373}{360}.
\]

The strict improvement was

\[
 \frac{83}{80}-\frac{373}{360}=\frac1{720}.
\]

Thus that fixture refuted a universal restriction of the free initial
position to the characteristic mesh. The historical lattice replay
reported 889 distinct states and 1,516 edge relaxations.

## 3. Fixed center start and a genuinely later off-grid turn

The second field had nodal values in
\(\{0,1/8,1/2,7/8,1\}\). The Monster start was fixed at zero.
The historical exact unit-speed lattice minimum was

\[
 \frac{29}{16},
\]

attained by

\[
 (0,0)\longrightarrow(3/4,3/4)
 \longrightarrow(5/2,-1)\longrightarrow(9/2,1).
\]

The off-grid response

\[
 (0,0)\longrightarrow(5/6,-5/6)
 \longrightarrow(8/3,1)\longrightarrow(14/3,-1)
\]

had exact payoff

\[
 \frac{173}{96},
\]

giving the strict gap

\[
 \frac{29}{16}-\frac{173}{96}=\frac1{96}.
\]

The first turn has light coordinates \((U,W)=(0,5/3)\). Its nonzero
coordinate is not a mesh coordinate, even after adding the fixed
initial light coordinates and integer endpoint translations.
This fixture therefore concerned a later turn, not merely an
off-grid free start.

For the family

\[
 (0,0)\longrightarrow(h,-h)
 \longrightarrow(1+2h,1)\longrightarrow(3+2h,-1),
 \qquad 3/4\le h\le1,
\]

the exact integration recorded the three successive contributions

\[
 \begin{split}
 I_1(h)&=h-\frac{h^2}{4}+\frac3{32},\\
 I_2(h)&=\frac74-\frac{5h}{2}+\frac{7h^2}{4},\\
 I_3(h)&=1-h.
 \end{split}
\]

Their sum is

\[
 J(h)=\frac32h^2-\frac52h+\frac{91}{32}
     =\frac32\left(h-\frac56\right)^2+\frac{173}{96}.
\]

This is a strictly convex quadratic with its minimum at the interior
off-grid parameter \(h=5/6\). The historical exact verifier checked
49 independent rational samples of this identity. Its lattice replay
reported 239 states and 394 edge relaxations.

Without the original field array, the displayed integration formulas
cannot currently be independently tied back to a complete legal CDF.
They are preserved as the exact historical result, not asserted here
as a self-contained counterexample.

## 4. Consequences and recovery boundary

The original checked fixtures showed why the fixed-field finite
quadratic-program response theorem does not imply that all optimal
turns occur at mesh vertices. They did not contradict the fixed-field
finite-piece theorem. They also did not obstruct an approximation by
common quantization: the latter theorem changes the whole law and its
causal clock together and includes an explicit buffer error.

The following original files were not recovered:

* OFFGRID_RESPONSE_COUNTEREXAMPLES.md;
* offgrid_response_counterexamples.json;
* verify_offgrid_response.py;
* offgrid_response_replay_report.json.

The first fixture's exact field array, the second fixture's exact
field array, and the source code would need to be recovered or
reconstructed and replayed before restoring a complete executable
certificate. No missing arrays or check results have been fabricated
in this recovery note.
