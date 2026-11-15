# Exact continuous-response cells for a common coordinate warp

This is a finite construction for specified monster families against one
fixed ordered field. It is not an unrestricted lower bound or an
equilibrium certificate. The underlying field is the complete original
field, Git blob 5c45d042ee9948faebc03354c3e1e2ee3cbec1a5; its initial trace is
continuous, its V=1 interior trace is zero, and all paths are at endpoints
by time 2. A strict common warp preserves these hypotheses.

## Fixed reference geometry

Write psi for an increasing odd map with psi(x+2)=psi(x)+2. Its knot
increments d are nonnegative and sum to1; positive increments give a
physical bijection. All original U/V grid coordinates, after folding
modulo 2, are among the 34 reference knot intervals.

For fixed reference monster parameters, every first-capture rank and
capture-coordinate branch is independent of d. The payoff is linear in d.
On a fixed reference arrangement cell, trace ranks are affine in the route
parameters. Rank inverse cutoffs and geometric intersections are affine
as well. Integrating an affine CDF against dpsi on an interval whose
endpoints are affine gives a quadratic polynomial. Capture jumps have
the same degree: an affine time multiplied by an affine captured mass.

These degree assertions are consequences of the branch geometry, not
inferences from finitely many polynomial checks. The exact checks below
audit their implementation.

The positive-M1 arrangement splits when A(a)=R(2-a,V) crosses a triangle
edge. The positive fixed-U1 M2 arrangement splits when A(a) crosses a rank
on the U=1 row. Negative families need only the initial/geometric knots.
Because ranks and triangle incidence are unchanged by the common warp,
these reference-start arrangements are independent of d.

There are 34 negative-M1, 148 positive-M1, 34 negative fixed-U1 M2 and 85
positive fixed-U1 M2 cells: 301 in total.

## Whole continuous late-negative M2 family

For reference start -a and first turn U=s>=1, the exact four-cost is

    N(a)+4s+8-2(s+1)A(a)-(s+6-a)R(s,a)-integral_a^s R(U,a)dU.

On every affine post-one triangle, with a fixed,

    4 C_ss = -3 R_U <= 0.

Therefore a minimum on the fixed-a fiber is at a fiber endpoint. These
endpoints lie on the vertical or diagonal triangle edges. A horizontal
edge has fixed a and reduces to its vertices by the same concavity.
The full two-parameter family consequently reduces to 3,502 retained
edges from 3,468 triangles. No claim about the sign of the full Hessian is
needed.

At the physical endpoint s=a+2 use the CLOSED rank B=1, not the interior
radial trace. There are 34 separately evaluated endpoint edges. The
capture jump can only lower the endpoint payoff, so omitting the larger
interior endpoint limit cannot miss a smaller value.

Under a common warp, write

    N_d(a) = integral_-a^a R(a,V) dpsi(V),
    I_d(s,a) = integral_a^s R(U,a) dpsi(U).

For B=R(s,a), or B=1 on the endpoint face, the warped four-cost is

    N_d + (4-2A-B) psi(s) + B psi(a)
        + (8-2A-6B) - I_d.

This is linear in d. Its restriction to each reference edge is quadratic.
Weighted column primitives at only 103 distinct a coordinates compile all
3,502 exact coefficient triples efficiently. The same fiber argument
holds in the physical warped coordinates, since each common-knot right
triangle is mapped affinely.

## Exact conic form and separator

Each cell uses a normalized reference parameter t in[0,1] and stores
three vectors c,b,a such that

    C_d(t) = dot(c,d) + dot(b,d)t + dot(a,d)t^2.

For target v set

    A=dot(c,d)-v,
    B=dot(c+b/2,d)-v,
    C=dot(c+b+a,d)-v.

The whole interval inequality is exactly

    A>=0, C>=0, B+sqrt(A C)>=0.

Indeed this is nonnegativity of
A(1-t)^2+2B t(1-t)+C t^2. Equivalently introduce q>=0,q>=-B and require
the second-order cone A+C>=sqrt((A-C)^2+4q^2).

The portable separator needs no conic solver: evaluate the endpoints and,
when the quadratic coefficient is positive, its interior stationary
point. All arithmetic is rational. A newly minimizing reference route
has its exact warp feature obtained from the same three stored vectors.

## Exact verification and scope

The 301-cell compiler passed 907 independent identity-payoff checks and
10,234 basiswise quarter-point identities. The 3,502-edge compiler passed
119,068 basiswise quarter-point identities. Twenty-two independent
first-capture feature evaluations additionally verified748 exact basis
coefficients, including closed endpoint edges and the physical minima of
three distinct strict warps.

The strict first finite-bank solution failed an omitted positive fixed-U1
M2 at reference start 1/8: cost about 1.42013860114 versus its finite-bank
minimum about 1.42318232099. After the four complete start families were
added, the late-negative family still attacked at reference(a,s)=
(9/20,1025/1024), cost about 1.42294529024. Thus none of these numerical
warp states is an unrestricted lower certificate.

## Phase interpretation

At a smooth interior late turn, differentiation with respect to the
REFERENCE s gives

    4 partial_s C_N^psi
      = 2 psi'(s) [2-A(a)-R(s,a)]
        - [6+psi(s)-psi(a)] R_U(s,a).

At an active fixed-turn boundary s=1, its right derivative must be
nonnegative. At a slack fixed-turn route that derivative may be negative
without contradiction. Oddness and 2-periodicity imply
psi'(2-s)=psi'(s) at regular points, so the post-one incoming price is
directly coupled to compression just below one.

For the finite master 8168d3aaf410d21ae6613e01909226490c5e456e, the terminal
warp slope was 1/32. One nearly active negative fixed-U1 route has exact
R_U=12583936/48828125 and four-cost derivative about -1.59279412918 at
U=1+2^-20. This identifies the missed phase: near-one compression makes
a later turn cheaper. A joint solution must alter that slope or move the
active monster support away from U=1. The full edge constraints permit
both possibilities; a global monotonicity restriction is unnecessary.

The associated floating finite-master dual has equal capture-coordinate
moments on its 26 positive free increments, but deficits up to about .03435
on the eight identity-floor intervals. This is a numerical diagnostic of
the constrained finite master, not an exact saddle law. At an attained
unrestricted saddle all odd-periodic capture-coordinate moments must
vanish, as proved in COMMON_LIGHT_COORDINATE_WARP.md.

## Portable replay

The CommonJS modules are:
warp_exact_field_core.cjs, warp_capture_features.cjs,
warp_family_audit.cjs, warp_compile_families.cjs,
warp_compile_late_edges.cjs and warp_quadratic_separator.cjs.

Run:

    node verify_warp_quadratics.mjs FIELD FOUR_TENSOR LATE_TENSOR SOLUTION REPORT --rebuild

This recompiles both complete tensors from the field, checks all stored
coefficient bytes, separates the supplied strict warp exactly, and
independently captures each minimizing physical route. Omitting --rebuild
evaluates the stored tensors and verifies their minimizing captures; it
does not rebuild their complete coefficient tables. The computational
bodies were executed in portable V8. Native CLI replay was unavailable
during this checkpoint.
