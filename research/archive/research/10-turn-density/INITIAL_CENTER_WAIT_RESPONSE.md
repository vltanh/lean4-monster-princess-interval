# Removing an initial center wait from an upper response law

An initial center-wait component can be replaced by an approaching
unit-speed prefix without increasing the unrestricted princess-response
supremum. This is a statement about a monster law's upper guarantee.
The replacement need not capture every particular princess sooner.

## 1. Strictly positive princesses give the same supremum

Let nu be any symmetric Borel monster law. The universal folding
comparison permits restriction to nonnegative princess paths. For such
a path p and `0<epsilon<1`, define

    p_epsilon(t)=(1-epsilon)p(t)+epsilon.

This path lies in `[epsilon,1]`, has speed at most one, and converges
uniformly to p. For any fixed continuous monster path m,

    T(m,p) <= liminf_(epsilon->0) T(m,p_epsilon).    (1)

Indeed, if a subsequence of capture times had a finite limit strictly
before T(m,p), continuity of m and uniform convergence of p_epsilon
would give an earlier exact contact with p. The same argument on each
finite time interval covers T(m,p)=infinity. Thus capture time is lower
semicontinuous in the princess path, with the usual infinite value.

Fatou's lemma, applied to the nonnegative capture times, gives

    E_nu T(m,p) <= liminf E_nu T(m,p_epsilon).

Consequently

    sup_(all princess p) E_nu T
      =sup_(p(t)>0 for every t) E_nu T.             (2)

No uniform upper bound on the route horizon is required for this step.
The approximation can improve a contact discontinuity; convergence of
the payoffs themselves is not asserted.

## 2. A coalescing replacement

Suppose a monster route m stays at zero until time `0<=w<=1` and then
has some specified continuation. Replace its initial part by

    m_new(t)=w-t,        0<=t<=w,
    m_new(t)=m(t),       t>=w.                      (3)

The new route is legal and coalesces with the old route at time w.
When the old first departing leg moves left at unit speed, the new
prefix is simply its backward extension to time zero.

For a strictly positive princess p, neither m nor its reflection
captures her during the center wait. Before time w the new pair may
make additional captures, and after time w it is the same pair. Hence

    T(m_new,p)<=T(m,p),
    T(-m_new,p)<=T(-m,p)                            (4)

for every strictly positive p. The same conclusion holds for a mixture
of such rows, and in the presence of any unchanged symmetric components.
Combining (2) and (4) proves

    sup_p E_(nu_new) T <= sup_p E_nu T.             (5)

Thus this substitution never worsens the law's unrestricted upper
guarantee. It can be made before optimizing the remaining monster law.

## 3. The two-triangle rows become early M3

Consider the saved route which waits at zero until w, makes a negative
excursion returning to center at S, makes a positive excursion returning
to center at one, then visits -1 and +1. Assume `0<=w<=S<=1`.

The approaching replacement starts at +w and moves inward through the
center to the old first negative turn. Reflect the entire route. It is
then exactly the center-reaching early-M3 route with

    initial position x=-w,
    first outward turn U=S,
    second outward characteristic V=1.

The phase condition `|x|=w<=S` holds. Therefore the initial-center-wait
two-triangle rows can be absorbed into the signed early-M3 upper class,
without a larger unrestricted response ceiling. This is a structural
replacement of the upper class, not a new game-value estimate.

## 4. Why this does not delete lower-law attacks

At an exact center-contact path, (4) can fail. For example, if the
princess stays at zero, the old waiting pair captures at time zero,
whereas both approaching routes first capture at time w. This is why
the proof uses the response supremum and the approximation in (2).

In particular, the theorem does not justify ignoring initial waiting
monsters when checking a supplied lower princess law with center atoms.
Nor does it give uniform lower guarantees for p_epsilon against a
monster that may depend on epsilon. Those are separate obligations.

`verify_initial_center_wait_removal.py` checks the two orientations
individually on strictly positive rational polygonal paths, verifies the
exact early-M3 identification, and retains the center-contact
counterexample. The general supremum statement follows from the
lower-semicontinuity proof above, not from those finite fixtures.
