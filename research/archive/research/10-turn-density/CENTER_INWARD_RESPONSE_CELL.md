# Center-first inward response: the exact boundary trace

This note closes the missing first-center-contact boundary of the
initial-inward response formula. It is a response identity and a finite
geometric constraint format, not an all-monster certificate or an
instantiated equilibrium.

## Route and traces

The monster starts at +z, moves inward to the center at time z, moves
outward until U=s, then visits the left and right endpoints:
0<=z<=1 and z<=s<=z+2.

Use A=P(p(0)<=z), Z=P(p(z)=0), and the CLOSED radial frontier B at
the outward turn. Thus B=1 at the endpoint s=z+2. Let

N(z)=integral[-z,z] R_strict(z,V)dV.

The N row uses the strict incoming trace; an incoming U=z atom has
already been caught at its first contact and must not be counted as
delayed until center. Every fixed-V beta integral below uses CLOSED R.
An outgoing characteristic atom can occupy a whole fixed-V row, so
strict and closed traces are not interchangeable there.

The repository's continuous interior affine field implements these
conventions automatically, with explicit closed endpoint capture.

## Direct rank partition

Against the positive princess copy:

* Ranks q<=A are caught on the first inward leg at alpha_q(z).
* Ranks A<q<=B, when B>A, are caught on the outward leg at beta_q(z).
* Ranks q>max(A,B) are caught on the final right sweep at s+3.

Against the negative copy, ranks q<=Z are caught at center at time z;
the others are caught at beta_q(s). This partition handles incoming
atoms without obtaining the formula from an interior v<z limit.

The inverse moments are

2 integral[0,A] alpha_q(z)dq = N(z),

2 integral[Z,1] beta_q(s)dq
 =2(s+1)(1-Z)-integral[s,s+2](R(U,s)-Z)_+dU,

2 integral[A,B] beta_q(z)dq
 =(s+z)(B-A)-integral[z,s](R(U,z)-A)_+dU   when B>A.

Consequently the reflected-pair expected cost C satisfies

4C=N+4s+8-(2s+2-2z)Z-(2s+6)A
   -(s+6-z)(B-A)_+
   -integral[z,s](R(U,z)-A)_+dU
   -integral[s,s+2](R(U,s)-Z)_+dU.                  (1)

At s=z, monotonicity gives
integral[z,z+2](R-Z)_+=integral[z,z+2]R-2Z,
and (1) reduces exactly to the direct inward M1 cost. At s=z+2, B=1
is required; the interior endpoint trace is insufficient.

## Lift and dimensions

Each positive-part integral is a maximum over a tail cutoff. Thus
(1) is the minimum, for z<=b<=s, s<=d<=s+2 and j in{0,1}, of

N+4s+8+(2z-s-d)Z-(s+b+6)A
 -j(s+6-z)(B-A)
 -integral[b,s]R(U,z)dU-integral[d,s+2]R(U,s)dU.     (2)

This has four continuous parameters (z,s,b,d). A geometric simplex
has a 5-by-5 copositive matrix; PSD plus entrywise nonnegative is a
sufficient condition, not an equivalent representation in this order.

For s>1, endpoint absorption by time2 forces the final row R(U,s)=0.
The same holds at s=1 if there is no outgoing V=1 atom. Then d=s+2
minimizes (2), leaving three parameters and exact order-four
copositivity/SDP constraints.

At fixed s=1, the lifted formula becomes

N+12+(2z-4)Z-(7+b)A
 -j(7-z)(R(1,z)-A)-integral[b,1]R(U,z)dU.           (3)

The domain0<=z<=b<=1 is partitioned by the existing positive pre-one
triangles in coordinates(b,z). Every term is quadratic on such a
triangle with coefficients linear in the field values. There are
n^2 triangles for n shared-grid intervals:1156 for the current n=34
field. Each is an exact order-three copositive constraint.

Branch0 is redundant once all reflected negative-M1 constraints hold.
If B>A, branch1 is smaller. If B<=A, the outward detour captures no
positive rank above the initial frontier; continuing inward directly
captures every relevant rank no later. Closed B and atom-inclusive A
are essential to this deletion argument.

## Verification and implementation

The parent independently verified (1) against35 exact full-path
first-capture calculations: z=0,1/8,1/4,9/16,13/16,15/16,1 and
s=z,z+1/2,z+1,z+3/2,z+2. These include zero legs, pre/post-one turns,
initial center, and the closed endpoint branch.

GeometryForms.center_i_four implements (2).
response_cells.center_i_one_cells supplies the n^2 fixed-s1 cells.
The Python additions were reconstructed during the executor outage
and have not themselves run; the formula's independent exact capture
checks are a separate validation. No unrestricted payoff claim follows.
