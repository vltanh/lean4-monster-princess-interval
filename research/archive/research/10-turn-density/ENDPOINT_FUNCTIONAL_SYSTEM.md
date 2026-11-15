# The endpoint layer: exact integral equations and conditional asymptotics

## 1. Scope and conventions

This note studies a possible endpoint attachment of the separated-sheet
candidate. It does **not** establish an equilibrium, a new game bound, or
existence of a solution of the complete boundary system.

The ordinary/no-late identities below must not be used unchanged after
adding a negative-characteristic post-incoming sheet. The exact correction
to `Cf-Cg`, the two flux contributions to the leading tail coefficient,
and the additional smallness assumptions on the curved-prefix correction
are given in [`POSITIVE_TURN_SHEET.md`](POSITIVE_TURN_SHEET.md), Sections
3 and 7. That note also records why the saved fixed-parameter outer
attachment fails.

Use the ordinary ordered positive princess paths

    p_q(t)=min(1,max(min(a(q)+t,u(q)-t),t-c(q),0))

and their fair reflections. The initial and incoming parameters increase
with rank q; c decreases. Assume a<=u<=1, -a<=c<=1, no initial endpoint
atom, u<1 almost everywhere, and no outgoing atom at c=1. Every path is absorbed at its endpoint
by time two. Write A for the initial CDF and I for the incoming CDF.

The terminal branch has c(a)<0 and u(a)>a. The positive M1 and M2 pair
costs are Cf and Cg, and the negative M1 cost is Cell, using the definitions
in `../09-equilibrium-structure/SIGNED_M1_FUNCTIONAL.md`.

For an initial-coordinate deficit e=1-a, set

    r(e)=1-A(1-e),  d(e)=1+c(1-e),  h(e)=1-u(1-e),
    tau(e)=d^{-1}(e),  P(e)=integral_0^e r(t)dt,
    L(e)=integral_0^e h(t)dr(t).

These lower-law functions are unrelated to the upper-law primitives used
in Section 6. All inverse expressions below are restricted to a strictly
monotone terminal branch. Integral statements also admit their usual
Stieltjes versions.

## 2. A central atom cannot replace an approaching outgoing front

Suppose instead that B=Pr(c=1)>0, retaining no initial endpoint atom and
u<1 almost everywhere. For such
paths, the monster with positive M1 parameter z approaching one from
below has pair cost tending to 3/2. The negative M1 pair reaches their
central waiting segment, and its cost tends to 1. For every path with
c<1 the two limits agree. Dominated convergence therefore gives

    4 Cf(1-)=5+integral c(q)dq,
    4 Cell(1-)=5+integral c(q)dq-2B.                 (1)

At the exact endpoint start the sweep also makes the earlier contact.
Consequently common Cf=Cell activity arbitrarily near one forces B=0.
A numerical collection of paths with c very close to one cannot be
replaced by a literal atom at one. This is a first-capture trace issue,
independent of the numerical precision of a fit.

If the condition u<1 almost everywhere is removed, first contact on the
incoming U=1 plateau contributes one more nonnegative term:

    4 Cf(1-)-4 Cell(1-)
      =2 Pr(c=1)+integral_(u=1) [a(q)+c(q)]dq.       (1a)

Here a+c>=0. Common tail activity therefore also excludes a nondegenerate
incoming atom at U=1. A branch with u=1 and c=-a has no actual inward leg
and is a redundant parameterization of outward motion.

## 3. Exact terminal cost residuals

Let

    V4=5+integral c(q)dq.

Under the assumptions of Section 1 this is four times the endpoint-sweep
cost. Direct partitioning of captures gives, for z=1-e,

    4 Cf(z)-V4
      =3e-integral_0^e [d(t)+h(t)]dr(t)
          +e r(tau(e))+L(tau(e)),                  (2)

and

    4[Cg(z)-Cf(z)]
      =-e[3-r(e)]+(8-2e)r(tau(e)).                 (3)

These are identities for an arbitrary supplied ordinary wave. They do not
assume either monster cost is constant. For example, in rank coordinates
the positive M1 correction for c<-z is exactly

    integral_(c<-z) [2-z-u(q)]dq,

which accounts for the last two terms in (2). Treating this set as an
endpoint-start component would give a different, incorrect equation.

If Cf=Cg=V4/4 on the branch, equations (2)-(3) become

    integral_0^e [d+h]dr = 3e+e r(tau)+L(tau),      (4)
    r(tau(e)) = e[3-r(e)]/(8-2e).                 (5)

Equivalently, eliminating tau gives the advanced relation

    r(e)=d(e)[3-r(d(e))]/[8-2d(e)].                (6)

It is important that d(e) is larger than e near zero. A terminal interval
does not determine (6) without its outer attachment data.

Assume in addition that C(z)=Pr(c>=z)=0 on the relevant high-z interval.
Define

    H(v)=(8-2v)r(v)+P(v)-3v.

Then the negative M1 cost has the exact residual identity

    4 Cell(u(a))-V4
      =H(h(e))-integral_0^e [d(t)-t]dr(t).          (7)

One way to verify (7) is to differentiate its two sides. At z=u(a),
the exact negative-M1 derivative is

    4 Cell'(z)=3+r(1-z)+(a+c(a)) I'(z)
                  -(6+2z) A'(z),

and I'(u(a))=A'(a)/u'(a). Both sides of (7) vanish at e=0.
Direct capture integration is an independent verification.

Combining (4) with Cell=V4/4 yields a derivative-free pair:

    H(h(e))=3e+e r(tau)+L(tau)-L(e)-e r(e)+P(e),  (8)
    r(tau(e))=e[3-r(e)]/(8-2e).                  (9)

Equations (4), (8), and (9) avoid differentiating interpolated delayed
fronts. They still have to be solved with transport, support, and outer
matching conditions. Small local residuals do not prove those conditions.

The positive outgoing front can be included without differentiating it.
For C(z)<I(z), with e_z=1-u^{-1}(z), the exact generalization of (7) is

    4 Cell(z)-V4
      =H(1-z)-integral_0^e_z [d(t)-t]dr(t)
                    -2C(z)-integral_z^1 C(s)ds.    (9a)

The correction follows by separating the ranks still waiting at the center
at threshold z. Thus ell indifference requires, with v=1-z,

    2 Ctilde(v)+integral_0^v Ctilde(s)ds=R(v),
    R(v)=H(v)-integral_0^e_(1-v) [d(t)-t]dr(t).

For continuous R with R(0)=0 its unique continuous solution is

    Ctilde(v)=R(v)/2
      -(1/4)integral_0^v exp(-(v-s)/2)R(s)ds.       (9b)

This is an explicit ordinary-wave attachment equation. Its solution still
must be a nonnegative nondecreasing function of v and must agree with the
actual outgoing quantiles. It does not grant those properties automatically.

`packages/interval_turn_sheet/verify_terminal_integrals.py` checks 328
exact rational cost-residual identities against the independent continuous
capture-record engine. It uses initial and incoming parameters that differ,
moving negative outgoing fronts, positive outgoing-front corrections, and center-waiting pieces. The checks
verify identities, not existence of a law making every residual zero. It
also checks 60 exact endpoint traces, including the extra incoming-atom
term in (1a), by direct segment intersections.

### A curved low-rank prefix can contribute before C becomes positive

The ordinary-wave correction (9a) has a useful extension. Suppose a low
rank follows an arbitrary nonnegative Lipschitz prefix, starts at a<z0,
and joins its final unit outward leg at (U,V)=(b,c), where 0<=c<1 and
b<1. Let alpha_q and B_q be its exact first inverses of t+p and t-p.
For z>=z0 define

    V_first,q(z)=2 alpha_q(z)-z,
    phi_first,q(z)=2 B_q(z)-z,
    Omega_q(z)=[c-V_first,q(z)]_+
                 +1_(z<=c)[z+2-phi_first,q(z)].     (9c)

Direct first captures give

    4 Cell,q(z)=3z+2+c-Omega_q(z),
    4 Cf,q(z)=8-3z+c,   4 Cg,q(z)=5+c.             (9d)

Consequently replacing low ordinary prefixes by these curved prefixes
does not change (2)-(3), provided their initial/outgoing parameters and
the high ordinary branch are retained. For the combined law, let Omega
be the integral of (9c) over the low ranks only. Then

    4 Cell(z)-V4
      =H(1-z)-integral_(ordinary high:u>=z)(a+c)dq
                   -Omega(z).                    (9e)

In the continuous high branch the middle integral is the Stieltjes term
in (9a). It already accounts for the high incoming ranks and must not be
counted again in Omega. The first-contact endpoint u=z uses the displayed
closed trace. Initial-position atoms require their separate capture rule;
the continuous high initial CDF used here has no such atom.

For low paths that have already reached the center, Omega reduces to
2C+integral_z^1 C. A curved prefix may instead have V_first(z)<c even
with c<z. Thus the first attachment interface is controlled by its final
incoming U-coordinate b, not just its outgoing coordinate c. The exact
checker `packages/interval_turn_density/verify_curved_outgoing_layer.py`
passes 570 rational segment-capture comparisons, including characteristic
plateaus and equality at the outgoing cutoff.

## 4. The conditional leading endpoint balance

In the no-late-motion branch, the leading regular balance of (4)-(9) is

    r(e) ~ (3/2) sqrt(e),
    d(e) ~ 4 sqrt(e),
    h(e) ~ e^2/16.                                (10)

Thus the incoming characteristic approaches one substantially faster than
the initial position. Identifying u with a loses this branch.

The sub-half relative corrections have exponents

    eta_n=(1-2^(-n))/2,  n>=1,

and coefficients D_0=1,

    D_n=-16^eta_n D_(n-1)/[4(1+eta_n)],
    K_n=-(1+2eta_n)D_n.                            (11)

Their ratios tend in absolute value to 2/3. The corresponding series
converge absolutely; on compact positive intervals they may be
differentiated termwise. The first terms are

    D_1=-2/5, K_1=3/5,
    D_2=8 sqrt(2)/55, K_2=-14 sqrt(2)/55.

The next particular coefficients are

    D_*=23/250, K_*=22/125,

giving the conditional asymptotic history

    r(e)=(3/2)sqrt(e)[1+sum D_n e^eta_n+D_*sqrt(e)+o(sqrt(e))],
    d(e)=4sqrt(e)[1+sum K_n e^eta_n+K_*sqrt(e)+o(sqrt(e))],
    h(e)=(e^2/16)[1+sqrt(e)/15+o(sqrt(e))].        (12)

For (11), the positive-M1 equation gives
K_n+(1+2eta_n)D_n=0. The quantile relation (6) gives
D_n-K_n=-(16^eta_n/2)D_(n-1). Cross products first appear
at relative exponent 1/2. At that order the two equations are

    3D_*-K_*=1/10,   K_*+2D_*=9/25.

For the last coefficient in (12), write h=(e^2/16)(1+n sqrt(e)).
The numerator of its differentiated ell equation is
3-(3/4)sqrt(e)+o(sqrt(e)); the denominator is
(24/e)[1-(n/2+3/10)sqrt(e)+o(sqrt(e))]. Comparing derivatives
gives 5n/4=n/2+1/20, hence n=1/15.

These are necessary balances within the stated branch and regularity
ansatz. The convergent coefficient series is not, by itself, a proof that
an exact nonlinear solution with expansion (12) exists.

## 5. Why the endpoint history does not select a unique outer branch

Linearizing the leading advanced relation around (10)-(11), at the first
unresolved scale, permits normalized perturbations of the form

    delta r(e)=(3/2)e K(x),  x=log(16/e),

where the leading homogeneous equation is

    K'(x)=(3/2)K(x)+K(x/2).                        (13)

Its algebraic mode exponents obey

    2^(-theta)=-3/2,
    Re(theta)=log(2/3)/log 2.

They are oscillatory in log(x). For each such exponent the convergent
inverse-power correction has coefficients b_0=1 and

    b_n=-2(theta-n+1)b_(n-1)/[3(2^n-1)].            (14)

These modes are smaller than the particular e term, but larger than an
arbitrary fixed higher power of e. Consequently leading powers, even with
the particular corrections in (12), cannot justify uniqueness of a
continuation. Equations (13)-(14) describe the linearized equation, not a
claimed family of exact solutions of the nonlinear system. Outer matching
must determine any admissible mode amplitudes.

## 6. An exact linear upper-tail reduction

Now fix supplied lower front maps d,h and let tau=d^{-1}. Use a different
notation for the upper-law densities:

    p(t)=f(1-t)+g(1-t),
    P_up(t)=integral_0^t p(s)ds,
    Lambda(t)=integral_0^t ell(1-s)ds.

Assume there are no negative-M2 starts in this terminal interval. The
negative outgoing branch has y=c. The upper c and a stationarity equations
give exactly

    g(1-t)=[w0+P_up(tau(t))+Lambda(h(tau(t)))
                 -(t+h(tau(t)))p(t)]/(8-2t),       (15)

    ell(1-t)=[(d(t)+h(t))p(t)-t g(1-t)
                  +Lambda(t)-Lambda(h(t))]/(8-2t). (16)

After integrating (16), these are one affine Volterra equation for Lambda.
For fixed integrable source and 0<=h(t),tau(t)<t<=T, the dependence on
Lambda has sup-norm contraction bound

    2T/(8-2T)+T^2/[2(8-2T)^2] < 1   for T<=1.      (17)

Thus (15)-(16) uniquely determine a continuous primitive Lambda for the
supplied p,w0,d,h. This does not automatically give nonnegative densities.
The remaining upper incoming-turn equation is

    P_up(d(t))-P_up(t)=(d(t)-t)ell(1-h(t)).          (18)

For fixed fronts it is linear in p and w0, so it can be studied without
adding another nonlinear density state.

The leading powers f(1-t) proportional to t^(-2/3) and ell(1-t)
proportional to (1/2)t^(-1/6) need a logarithmic modulation. Put

    gamma=log(3/2)/log 4,  x=log(16/t),
    H_up(x)=x^gamma sum_(n>=0) b_n x^(-n),
    b_0=1, b_n=-12(gamma-n+1)b_(n-1)/(4^n-1).

This convergent series solves

    12 H_up'(x)=H_up(x)-(3/2)H_up(x/4).            (19)

It supplies one useful nonoscillatory tail basis. It is not a uniqueness
statement for all positive tails. With d=4sqrt(t), h=t^2/16 it makes the
dominant part of (18) exact; the omitted full terms and the corrected
fronts still need to be solved. `endpoint_tail.py` and
`fit_endpoint_tail.py` in the turning-density package implement these
primitives and a local residual fit. That fit is discovery, not an exact
upper certificate.

## 7. Obligations still needed for closure

The terminal equations must be attached to a legal ordered law and a
normalized nonnegative monster law at a common value. Their support
boundaries and global inequalities remain unresolved. In particular,
ordinary waves need not realize all the equality freedom of the separated
early and late sheets, and arbitrary multi-turn monsters must still be
controlled. No exact game value is claimed here.
