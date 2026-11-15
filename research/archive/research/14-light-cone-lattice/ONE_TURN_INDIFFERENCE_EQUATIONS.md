# Indifference equations of the one-turn game in the continuum

Date: 2026-11-14. Status: **derivation for a stated support, checked against numerical optima.
Not a proof that the support is the right one, and not a solution of the one-turn game.** The
equations below reproduce the densities found by the lattice and continuum linear programs of
[packages/interval_lightcone](../../packages/interval_lightcone/README.md) to within a few per
cent, which is the accuracy of those densities. They do not yet cover the layer next to the
center at time 1.

Notation and the capture-time table are those of
[LIGHT_CONE_LATTICE_GAME.md](LIGHT_CONE_LATTICE_GAME.md): \(U=t+x\), \(W=t-x\); a radial Princess
is a monotone curve below the diagonal starting at \((r_0,-r_0)\).

## 1. The strategies

**Monster.** Every path is used with its mirror image, each with probability one half. The
"pair masses" are

| Symbol | Path | Support seen numerically |
| --- | --- | --- |
| \(e\) | endpoint sweep | atom, about 0.63 to 0.65 |
| \(p(a)\) | \(P_1(a)\), \(a>0\): right to the line \(U=1\), then left to \(-1\), then right | \((a_1,1)\), \(a_1\approx0.19\) |
| \(s(a)\) | \(S(a)\), \(a>0\): right to \(+1\), then left to \(-1\) | \((a_s,1)\), \(a_s\approx0.53\) |
| \(\rho(c)\) | \(P_1(-c)\), \(c>0\) | \((a_1,c_2)\), \(c_2\approx0.9\) |
| \(\alpha(c)\) | \(S(-c)\), \(c>0\): right through the center to \(+1\), then left | \((c_2,1)\) |

Write \(P^+(u)=\int_0^u p\), \(S^+(u)=\int_0^u s\), \(R(u)=\int_0^u\rho\),
\(A(u)=\int_0^u\alpha\).

**Princess.** Three families of radial paths, each with a fair sign:

| Symbol | Path |
| --- | --- |
| \(\pi(u)\) | center-waiter \(C(u)\): start at radius \(u\), run inward at once, wait at the center, leave just before time 1 |
| \(\eta(\omega)\) | highway path \(H(\omega)\): start next to the endpoint, run inward just ahead of the sweep line \(U=1\), turn back at height \(W=\omega\), return to the endpoint and stay |
| \(\varsigma\) | atom on \(H(-1)\): stay at the endpoint |

Write \(\Pi_{<u}\), \(\Pi_{>u}\) for the mass of center-waiters below and above \(u\),
\(\Pi_C\) for their total, and \(H_{<\omega}\), \(H_{>\omega}\) for the highway mass.

## 2. Comparing two Princess paths

For a fixed start \(r_0\) let \(\nu_V(U)\,dU\) be the mass of Monster legs on vertical lines that
would be her first meeting, and \(\nu_H(W)\,dW\) the same for horizontal lines. Crossing a
vertical line at height \(W\) costs her the capture time \((U+W)/2\), so along her curve

\[
 2\,\mathbb E T=\text{const}+\int_\Gamma\bigl(W\,\nu_V(U)\,dU+U\,\nu_H(W)\,dW\bigr).
\]

By Green's theorem, two monotone curves with the same end points, one going right and then up
and the other up and then right, differ by

\[
 \iint\bigl(\nu_H(W)-\nu_V(U)\bigr)\,dU\,dW
\]

over the rectangle between them, in favour of right-then-up when the integral is positive. She
runs outward first where horizontal legs are denser and inward first where vertical legs are
denser, and she is indifferent among all monotone curves exactly where the two densities are
equal constants. This is why the numerical optima contain arbitrary wiggles in some regions:
there \(\rho\) is flat and every path through the region has the same payoff.

## 3. Pair sums

For a Monster path \(m\) and a radial Princess path \(q\), let
\(\Sigma(m,q)=T(m,q)+T(\bar m,q)\) with \(\bar m\) the mirror image, so that
\(\mathbb E T=\tfrac12\int\Sigma\,d(\text{pair mass})\).

| \(m\) | \(\Sigma(m,C(u))\) | \(\Sigma(m,H(\omega))\) |
| --- | --- | --- |
| sweep | \(3\) | \(\tfrac{1+\omega}2+2\) |
| \(P_1(a)\) | \(3\) if \(a>u\); \(\tfrac{u-a}2+2\) if \(a<u\) | \(\tfrac{1-a}2+2\) if \(-a<\omega\); \(6\) if \(-a>\omega\) |
| \(S(a)\) | \(\tfrac32(3-a)\) if \(a>u\); \(\tfrac{u-a}2+3-a\) if \(a<u\) | \(\tfrac{1-a}2+3-a\) if \(-a<\omega\); \(4-2a\) if \(-a>\omega\) |
| \(P_1(-c)\) | \(2c\) if \(c>u\); \(\tfrac{u+c}2+2\) if \(c<u\) | \(\tfrac{1+c}2+2\) if \(c<\omega\); \(6\) if \(c>\omega\) |
| \(S(-c)\) | \(2c\) if \(c>u\); \(\tfrac{u+c}2+3+c\) if \(c<u\) | \(\tfrac{1+c}2+3+c\) if \(c<\omega\); \(4+2c\) if \(c>\omega\) |

Each entry is read off the capture-time table. For example a center-waiter with \(u<c\) is at the
center when \(P_1(-c)\) and its mirror image pass through it at time \(c\), which gives \(2c\);
a highway path that has turned back below height \(-a\) is beyond the turning point of \(P_1(a)\)
and is met only on its last leg at time 4, while the mirror image meets her at her endpoint at
time 2.

## 4. The Princess's conditions determine the Monster's densities

Differentiating \(\int\Sigma\,d\mu\) in the parameter of each Princess family, with the jumps at
\(a=u\), \(c=u\), \(-a=\omega\), \(c=\omega\), gives on the support of that family:

\[
 (7+a)\,p(a)+(1-a)\,s(a)=e\qquad(\text{highway turn at }\omega=-a<0), \tag{R1}
\]
\[
 (7-c)\,\rho(c)+(1+c)\,\alpha(c)=e\qquad(\text{highway turn at }\omega=c>0), \tag{R2}
\]
\[
 (2-u)\rho(u)+3\alpha(u)+\tfrac12\bigl[R+A+P^++S^+\bigr](u)=p(u)+\tfrac12(3-u)\,s(u)
 \qquad(\text{center-waiter }u). \tag{R3}
\]

Off the support the same expressions are inequalities. With \(\alpha=0\) below \(c_2\), (R2) is
\(\rho(c)=e/(7-c)\); with \(\rho=0\) above \(c_2\) it is \(\alpha(c)=e/(1+c)\). On \((a_1,a_s)\),
where \(s=0\), (R3) is a first-order linear equation for \(P^+\); on \((a_s,1)\), (R1) and (R3)
give \(p\) and \(s\). Eliminating \(p\),

\[
 s(u)\,\frac{19-2u-u^2}{2(7+u)}
 =(2-u)\rho(u)+3\alpha(u)+\tfrac12\bigl[R+A+P^++S^+\bigr](u)-\frac e{7+u}.
\]

Because \(3\alpha\approx1\) while \((2-u)\rho\approx0.1\), the density \(s\) rises by about a
factor ten where \(\alpha\) replaces \(\rho\): this is the dense group of "delayed sweeps" seen
next to \(a=1\).

## 5. The Monster's conditions determine the Princess's densities

In the same way, differentiating the cost of each Monster family in its start gives

\[
 \pi(a)=\tfrac12\bigl[\Pi_{>a}+H_{>-a}\bigr]+\tfrac12(7+a)\,\eta(-a)\qquad(P_1(a)), \tag{M1}
\]
\[
 \tfrac12(3-a)\,\pi(a)-\tfrac12(1-a)\,\eta(-a)=\tfrac32\bigl(\Pi_C+H_{>-a}\bigr)+2\bigl(H_{<-a}+\varsigma\bigr)
 \qquad(S(a)), \tag{M2}
\]
\[
 (2-c)\,\pi(c)=2\,\Pi_{<c}+\tfrac12\bigl[\Pi_{>c}+H_{>c}\bigr]+\tfrac12(7-c)\,\eta(c)\qquad(P_1(-c)), \tag{M3}
\]
\[
 3\,\pi(c)=2\,\Pi_{<c}+\tfrac32\,\Pi_{>c}+\tfrac12(1+c)\,\eta(c)+\tfrac32H_{>c}+2\bigl(H_{<c}+\varsigma\bigr)
 \qquad(S(-c)). \tag{M4}
\]

On \((a_1,a_s)\) there is no highway turn at \(\omega=-a\), so (M1) is
\(\pi=\tfrac12(\Pi_{>a}+H_{>-a})\) and \(\pi\) decays like \(e^{-a/2}\). On \((a_s,1)\), (M1) and
(M2) give \(\pi(a)\) and \(\eta(-a)\); eliminating \(\pi\),

\[
 \eta(-a)\,\frac{19-2a-a^2}{4}
 =\tfrac32\bigl(\Pi_C+H_{>-a}\bigr)+2\bigl(H_{<-a}+\varsigma\bigr)-\tfrac14(3-a)\bigl(\Pi_{>a}+H_{>-a}\bigr),
\]

with the same quadratic \(19-2a-a^2\) as on the Monster's side. The term
\(\tfrac12(7+a)\eta(-a)\approx1.2\) in (M1) is the jump of the center-waiter density at \(a_s\).
(M3) then gives the density \(\eta(c)\) of highway turns at positive heights.

## 6. Numerical checks

Monster side, one-turn lattice optimum at \(n=32\) (\(e=0.6479\)) and the continuum optimum with
16 bins (\(e=0.6281\)):

| Relation | Where | Left side divided by right side |
| --- | --- | --- |
| (R1) | \(a\ge27/32\), \(n=32\) | 1.0000 |
| (R1) | \(a\in[9/16,13/16]\), \(n=32\) | 1.003 to 1.017 (inequality side) |
| (R1) | \(a\in[9/16,7/8]\), continuum | 0.999 to 1.001 |
| (R2), \(\rho(7-c)/e\) | six starts in \([7/32,5/8]\), \(n=32\) | 1.0000 |
| (R2), \(\rho(7-c)/e\) | \([7/32,21/32]\), \(n=32\) | 0.981 to 1.019 |
| (R2), \(\rho(7-c)/e\) | \([11/16,7/8]\), \(n=32\) | 1.077 to 1.081 (no highway turn there) |
| (R2), \(\alpha(1+c)/e\) | \(c=15/16,31/32\), \(n=32\) | 1.023, 1.044 |
| (R3) | \(u=0.354\), \(n=24\) | residual \(1.5\cdot10^{-4}\) on terms of size 0.19 |
| (R3) | \(u=0.646\), \(n=24\) | residual \(5\cdot10^{-4}\) on terms of size 0.20 |

Princess side, continuum optimum with 16 bins (its dual solution is a vertex and is noisy):

| Relation | Prediction | Seen |
| --- | --- | --- |
| (M1) on \((a_1,a_s)\) | \(\pi\approx0.335\) at \(a=0.3\) | 0.33 to 0.39 |
| (M1) on \((a_s,1)\) | \(\pi\approx1.41\) at \(a=0.65\) | 1.32 to 1.41 |
| (M1)+(M2) | \(\eta(-a)\approx0.31\) at \(a=0.65\) | 0.29 to 0.36 |
| (M3) | \(\eta(c)\approx0.34\) at \(c=0.6\), \(\approx0.01\) at \(c=0.3\) | about 0.3; about 0.02 |

## 7. What is missing

1. **The layer before time 1.** Above \(c_2\) the Monster uses \(S(-c)\) and paths \(P_b(a)\)
   with \(c_2<b<1\) that join those sweeps, and for \(c\) between about 0.69 and 0.875 a few
   \(P_b(-c)\) with \(b\) just above 1. The Princess's center-waiters leave the center at about
   \(c_2\), run out to the sweep line and ride it back in. Removing the levels \(b\ne1\) costs
   \(7.7\cdot10^{-4}\) at \(n=16\). The equations of this layer are not written here.
2. **Thresholds.** \(e\), \(a_1\), \(a_s\), \(c_2\) are fixed by the equality of the payoffs of the
   families, for instance by the condition that the highway payoff, which falls on
   \((-a_s,-a_1)\) and rises on \((-a_1,a_1)\), returns to its level:
   \(\int_{a_1}^{a_s}\bigl[(7+a)p(a)-e\bigr]da=2e\,a_1\). These conditions have not been solved.
3. **Uniqueness.** Where (R2) is an inequality the optimal law is not unique; the linear programs
   return a flat \(\rho\) there, with matching wiggles in the Princess's paths.
4. **The unrestricted game.** Two-turn paths that join a one-turn trajectory lower the value by
   about \(2\cdot10^{-4}\) on the lattice. The Princess's answer is a short outward run before
   each inward run, which changes \(\pi\) and the relation between start radius and \(u\).
