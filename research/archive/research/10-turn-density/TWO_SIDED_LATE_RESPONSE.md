# Positive late turns and the negative outgoing layer

This extends the separated early/late upper response construction. It
constructs the positive-turn density and proves its response compression;
it does not assert that a matched lower law has been found.

Let j(z,s) denote positive-M2 pair density with start +z and turn U=s.
Its legal domain is `0<z<1`, `1<s<v(z)<=2-z`. Retain the total positive
M2 start density g, and require `g0(z)=g(z)-integral j(z,s)ds>=0` for the
remaining line density at U=1. The monotonicity assumptions use f+g,
including the sheet mass.

## 1. Explicit density

For nondecreasing integrable f put

    j(z,s)=[f(2-v(z))-f(z)]/[v(z)+6+z]
             +integral_s^v(z) f'(2-r)/(r+6+z)dr.

The derivative integral is a Stieltjes integral for step densities.
Legality gives `2-v>=z`, so every term is nonnegative. Let
`H(z)=integral_1^v j` and `M(z)=integral_1^v(s-1)j`. With L=7+z,

    H=L integral_1^v [f(2-r)-f(z)]/(r+6+z)^2 dr,
    2M=integral_1^v [f(2-r)-f(z)]
                          *[1-L^2/(r+6+z)^2]dr.

In particular `L H+2M=F(1)-F(2-v)-(v-1)f(z)`.

## 2. Global post-prefix comparison

For initial a, the additional alpha price is

    J_a(s)=integral_(z>a) j(z,s)dz.

It is nonnegative, nonincreasing in s, and is supported on `s<=2-a`.
The latter statement uses the legal positive-turn restriction, and is
essential to the response comparison.

At negative V=-z, z<=a, the four-score for a post-U=1 inverse u is

    q(u)=integral_u^(2-a) [f(2-r)+J_a(r)]dr_+
           -f(z)(2-z-u)
           -integral_u^v(2s+6+z-u)j(z,s)ds,

where the final integral is zero above v. For `1<=u<=2-a`, its
derivative is nonpositive: inside the flat part it is `-J_a(u)`;
beyond v it is `f(z)-f(2-u)-J_a(u)<=0`. Above `2-a`, both alpha
sources vanish and q is nonpositive. Therefore its upper envelope is
attained by the U=1 limiting inverse or endpoint completion. The U=1
score is

    F(2-v)-f(z)(2-z-v)-F(a)+integral_a^1 H(x)dx.

The same alpha correction affects positive V. In a negative-start late
sheet's corridor it changes the derivative from zero to `-J_a(u)`.
After that corridor, the derivative is nondecreasing, because f is
nondecreasing and J_a is nonincreasing. The endpoint at `u=2-a` has
nonpositive score. Thus the same two endpoint comparison holds there.
The positive-V score acquires only the common initial-dependent constant
`integral_a^1 H`, preserving its monotonicity in V.

Before the first U=2-a crossing, these comparisons replace the extra
incoming segment by U=1+. After that crossing, every alpha source is
exhausted and endpoint completion is optimal. Consequently one suffix
exit y still suffices. The prefix below U=1 is unchanged: positive-sheet
negative-threshold captures have the same total beta price g, while its
new alpha thresholds lie above one. The negative-prefix Jensen argument
therefore still uses f+g, and the positive-prefix optimizer is unchanged.
The earlier integrable-density and legal epsilon-limit arguments apply.

## 3. Canonical four-scalar feature correction

For the ordinary prefix parameters a,u,c and extra exit y, replacing
the positive line density H by its late sheet changes four times the
response by

    2 integral_0^a M + 3 integral_a^1 M
      +(y-c) integral_a^1 H
      +2 integral_0^min(a,(-y)+) M
      -integral_max(0,-y)^min(a,(-c)+) (7+z)H(z)dz.

Empty integrals are zero. This follows directly from first capture:
the reflected component contributes 2(s-1); an unreflected negative
threshold crossed after U=1 gains the early contact and contributes
`-(7+z)`; thresholds beyond y contribute another 2(s-1). For z>a,
the alpha capture contributes `(s-1)+(y-c)` instead.

This correction is independent of the optimized prefix profile and is
linear in f. `positive_sheet_oracle.py` evaluates it analytically for
fixed constant turn profiles within start bins, and wraps the existing
oracle as `optimal_features_two_late`. The line residual is checked at
each start-bin left endpoint; H decreases within that bin under the
monotonicity assumptions. All profiles must satisfy `v<=2-z`.

`verify_positive_sheet.py` checks 4,284 exact rational envelope identities.
The feature module separately integrates actual segment captures for
five legal epsilon-path families, covering initial positions below,
inside, and above the positive start band, and both signs of y.
