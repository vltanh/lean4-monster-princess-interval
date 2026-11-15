# Exact continuous-start separation for interval fans

## Scope and input

Fix finitely many legal piecewise affine Princess paths p_i. Each row chooses a translation uniformly in a fixed nonempty interval [l_i,h_i], clips p_i+z to [-1,1], and fairly reflects. Row weights are nonnegative constant rationals, normalized once. The paths, intervals and weights are held fixed while the Monster initial position varies.

The provider germ_translation_fan.cjs computes the exact RAW mixture payoff. The common-quantile ordered law has the same one-time marginals and weakly larger payoff against every Monster, but it is a different coupling. Therefore:

- a nonviolating complete raw family is also nonviolating after ordering;
- a raw violating route must be rescored on the ordered law before it is described as an ordered-law attack.

This packet separates two continuous families exactly: all M1 endpoint tours, and all initial starts compatible with one supplied completed unit tail. It does not bound the number of Monster turns, separate all tails, or claim a game value.

All coordinates may be rational functions in a positive epsilon. Arithmetic decisions are made in QQ(epsilon) and retain a common explicit positive specialization radius. An exact limiting coordinate is never substituted for an actual endpoint contact.

## 1. The inverse-band primitive

For one Princess orientation sigma in {-1,+1}, use the effective translation interval [l,h] for sigma=+1 and [-h,-l] for sigma=-1. A Monster unit leg of direction d has constant c=t-d*m(t). Define

    phi(t)=t-d*sigma*p(t),   q=c+d*z.

The first capture time of translation z is the first inverse of phi at q, capped at the leg end for clipping mass captured at an endpoint. The integral of this inverse over a translation band is a piecewise quadratic primitive: on each nonflat characteristic segment the inverse is affine, and a flat segment has zero q-length. The constant Princess tail supplies the final affine inverse branch.

Captured translations form an interval [L,H]. An outward/right unit leg raises H, an inward/left unit leg lowers L, and an actual endpoint visit forces the corresponding record to the interval boundary. Initial and turn endpoint atoms use closed capture at the physical route, not a limiting interior trace.

The following separation constructions list every change of a clipping, record, inverse or cap branch. Between consecutive listed parameter values, every moment is quadratic.

## 2. Complete M1 starts

By fair reflection it suffices to consider the left-first route

    (0,a), (1+a,-1), (3+a,+1),    -1 <= a <= 1.

Its reflection represents the opposite orientation. Write p0=sigma*p(0), and let [l,h] be the effective translation window. The first-leg inverse is associated with t+sigma*p(t), and its possible q endpoints are

    a-l, a-h, p0.

The second-leg inverse is associated with t-sigma*p(t), and its possible q endpoints are

    a+2+l, a+2+h, 2*a+2-p0.

The arrangement includes:

1. a=-1,+1 and the initial clipping thresholds p0+l,p0+h.
2. Every equality of one of these affine q endpoints with an inverse-characteristic vertex.
3. Every equality 1+a=t_i or 3+a=t_i with a Princess vertex time.
4. Within each resulting Princess phase, every equality of an affine q endpoint with the cap characteristic at the appropriate leg-end time.

For a leg end T=a+k, a Princess phase p(t)=p_i+v_i(t-t_i), and inverse sign nu=d*sigma, the cap characteristic is

    T-nu*p(T)
      = (1-nu*v_i)*a + k-nu*(p_i+v_i*(k-t_i)).

Thus every listed boundary is the solution of a linear equation. Identically equal boundaries do not require an extra cut. Roots outside the relevant phase and start interval are discarded.

No initial-position sampling defines this arrangement. Its cells cover the entire allowed start interval, including microscopic germ intervals.

## 3. One fixed completed unit tail

Orient the first Monster leg to the right. If the physical first direction is d, write b=d*a and reflect all fixed tail positions by d. Let (t2,x2) be the first fixed tail vertex after the variable first turn, and let

    c=t2+x2.

The variable first turn is

    t1=(c-b)/2,   y1=(c+b)/2.

Legality is exactly

    max(-1,c-2*t2) <= b <= min(1,c,2-c).

The supplied fixed tail must contain both endpoint visits; all its nonzero legs must have unit speed. The implementation rejects an incomplete tail or a nonunit tail rather than silently adding or approximating one. At a domain boundary a first or second leg can collapse, and the physical closed route is evaluated there.

For one Princess sign, put

    R0(b)=b-sigma*p(0),
    R1(b)=y1-sigma*p(t1).

On a Princess phase with velocity v_i,

    R1(b)=alpha*b+B,
    alpha=(1+sigma*v_i)/2,
    B=c*(1-sigma*v_i)/2-sigma*p_i+sigma*v_i*t_i.

Insert the phase boundaries b=c-2*t_i. On every phase R0 and R1 are affine. Because the Monster first leg is rightward and the Princess is 1-Lipschitz, R1>=R0 throughout the legal interval. Hence their mutual order does not introduce a missing record branch.

Every later translation record is obtained by taking minima/maxima among:

- R0 and R1;
- the effective interval endpoints;
- the fixed relative positions x_j-sigma*p(t_j).

For a fixed tail leg with direction d_j and characteristic c_j=t_j-d_j*x_j, each inverse-characteristic knot q gives the translation threshold

    z=d_j*(q-c_j).

The fixed relative end position also gives the cap threshold. Pull these constant translation thresholds back through both R0 and each affine piece of R1.

The first outward leg has q=z-b. Its clipped-window endpoints give l-b and h-b; its initial-record endpoint gives the constant -sigma*p(0); its moving-turn endpoint gives R1-b. Insert their equalities with every first-leg inverse-characteristic knot. The comparisons R1=l,h are already among the translation-record cuts.

This list covers the full topology:

- Princess phase changes at the variable turn;
- initial and turn translation clipping;
- running record changes on every fixed later leg;
- every inverse primitive branch;
- the first moving cap and every later fixed cap.

Within each resulting cell every selected translation band endpoint is affine in b, every inverse primitive is quadratic, and every cap remainder is a product of affine quantities. The weighted raw cost is therefore quadratic. The argument allows arbitrary Princess speeds in [-1,1]; the Monster tail is the part restricted to unit legs.

## 4. Exact minimization, including atoms

On an open cell [a,b], use the local parameter u=(start-a)/(b-a). Evaluate the exact cost at u=1/4,1/2,3/4 to reconstruct

    q(u)=q0+q1*u+q2*u^2,

where

    q2=8*(f(1/4)-2*f(1/2)+f(3/4)),
    q1=2*(f(3/4)-f(1/4))-q2,
    q0=f(1/2)-q1/2-q2/4.

The geometry proof above establishes the degree; fitting alone is not the justification. The default runtime additionally checks the identity at u=1/3 and 2/3 and aborts on disagreement.

Every physical closed arrangement endpoint is scored. When q2>0, the stationary point -q1/(2*q2) is also scored if it lies strictly inside the cell. Its physical cost must equal the reconstructed polynomial.

Why do endpoint values suffice even with a jump? The completed Monster path depends continuously on its start in the uniform topology on a common bounded horizon. Closed first-contact time is lower semicontinuous under such path convergence. Fatou's lemma therefore makes the expected payoff lower semicontinuous. A closed endpoint value is no larger than the relevant one-sided liminf. A possible lower open-cell endpoint limit cannot be missed by evaluating the closed route.

In particular a Monster starting on a clipped endpoint atom captures that mass at time zero. The fixture with a stationary endpoint Princess has M1 cost 1 at a=1 and left limit 3. Replacing the closed value by the left polynomial would lose the actual optimum.

The exact result is either a listed arrangement endpoint or a rational stationary point. The germ implementation certifies the same finite branch arrangement for all sufficiently small positive epsilon using its common comparison radius.

## 5. APIs

    const T=createTranslationFan(G);
    const entries=[
      {id:"row",row:T.prepareInterval(path,lo,hi),weight:"1"}
    ];

    const M=createFanM1Separator(G,T,entries);
    const answer=M.separate({keepCells:true});

    const F=createFanFixedTailSeparator(G,T,entries,{
      firstDirection:1,
      tail:[["2","-1"],["4","1"]]
    });
    const answer2=F.separate({keepCells:true});

Both providers expose score, route, geometryCuts and separate. The fixed-tail provider additionally exposes its oriented domain and characteristic. Its result start is the oriented variable b; physical_start=d*b is supplied separately.

The cell limit is a fail-closed resource guard: exceeding maxCells throws an error, not an incomplete certification disguised as a complete result. Constant weights are checked by the QQ(epsilon) constant-weight getter. Zero-weight rows may be omitted because this is separation for the supplied law, not a universal arrangement for every future weight vector.

## 6. Independent verification

verify_fan_m1_separator.mjs checks 7 laws and 55 complete cells:

- 228 independent physical scores;
- 110 independent polynomial checks;
- asymmetric windows, nontrivial motion, germ widths and endpoint atoms;
- common radius 1/56, maximum polynomial arithmetic degree 4.

verify_fan_fixed_tail_separator.mjs checks 19 supplied tail families and 130 complete cells:

- 539 independent physical scores;
- 260 independent polynomial checks;
- 260 closed endpoint checks;
- reflected tails, genuine multiple-turn tails, subunit Princess velocities, asymmetric windows, germ widths and germ turn times;
- common radius 1/80, maximum arithmetic degree 4.

The independent scorer constructs actual translated and clipped Princess paths. It splits the translation interval at all relative values obtained at merged Princess/Monster vertices; on each resulting interval the first hit is affine in the translation, so exact midpoint integration is valid. It uses chronological physical segment intersections, not the provider's inverse-band cache or the separator's reconstructed polynomial.

These particular laws have no interior convex stationary minimizer. The stationary branch is included analytically and checked against the physical scorer whenever present; the reports do not claim a nonexistent stationary fixture.

Replay:

    node packages/interval_global_closure/verify_fan_m1_separator.mjs M1_REPORT.json
    node packages/interval_global_closure/verify_fan_fixed_tail_separator.mjs FIXED_TAIL_REPORT.json

The reports certify the complete stated families for their supplied raw laws. They do not certify the evolving 349-row optimization, an ordered-law attack, or the unrestricted game.
