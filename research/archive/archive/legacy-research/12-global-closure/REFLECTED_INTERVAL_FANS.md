# Exact endpoint-reflected interval fans

## Physical strategy

Fix a nonnegative legal 1-Lipschitz path p(t) in [0,1], and a fixed interval

    0 <= l < h <= 1,   w=h-l.

Choose z uniformly in [l,h], use

    p_z(t)=1-|1-p(t)-z|,

then fairly reflect. Both the path and the interval are immutable strategy data. Changing either creates a new row.

The map u -> 1-|1-u| is 1-Lipschitz on [0,2], so each p_z is legal and remains in [0,1]. The continuous translation law has no center or endpoint atom: the preimage of either endpoint consists of finitely many z values. Almost every positive-copy path avoids the center at each fixed time, while p=1 produces positions 1-z instead of a clipped endpoint atom.

This is a different physical basis from clipped translation fans. A limiting endpoint contact of the Monster is still evaluated at its actual germ coordinate; the new row's absence of endpoint atoms is not permission to collapse the Monster geometry.

The provider supports rational and QQ(epsilon) inputs. Positive interval width and all legality conditions are checked in the exact ordered field, with a common specialization radius recorded by the arithmetic core.

## Radial and signed CDFs

For 0<=x<=1 the exact radial CDF is

    R(t,x)
      = clip((x-p(t)-l)/w,0,1)
        + clip((x+p(t)+h-2)/w,0,1).

The two terms count p+z<=x and p+z>=2-x. Their sets are disjoint before x=1 and cover the translation interval at x=1.

The signed CDF is

    F(t,x)=(1+R(t,x))/2       when x>=0,
    F(t,x)=(1-R(t,-x))/2      when x<0.

Strict and closed versions agree everywhere, including x=0,+1,-1, because the spatial marginal is atomless. The radial density is bounded by 2/w and the signed density by 1/w.

For two base profiles with uniform distance eta and the same interval, the two clipped terms move in opposite directions as p changes. Consequently the radial CDF changes by at most eta/w, and the signed CDF by at most eta/(2w). A looser bound is also safe when constructing outward-rounded coefficient enclosures.

## An explicit ordered realization of a single fan

For radial quantile q in [0,1], the ordered radial path is

    r_q(t)=min(
      p(t)+l+w*q,
      2-p(t)-h+w*q,
      1-w/2+w*q/2
    ).

This formula follows by inverting the one-density and two-density parts of R. It also proves legality directly: each of its three terms is 1-Lipschitz in time, and the minimum is 1-Lipschitz.

The third term is a positive time plateau depending on q, not a spatial atom. When the moving translation interval straddles the endpoint, upper radial quantiles remain on these plateaus while lower quantiles follow one of the moving edges.

For a mixture of fans, the ordered law is obtained from the quantiles of the summed signed CDF. Sorting each component separately and then mixing is generally different. The provider always sums the component CDFs before updating the captured quantile interval.

## Exact ray integration

For a unit Monster leg, split time at:

- all base-path vertices;
- the Monster's center crossing;
- every crossing of |m(t)| with one of
  p(t)+l, p(t)+h, 2-p(t)-h, 2-p(t)-l.

Between these times every component signed CDF is affine. The weighted CDF is affine as well.

The ordered captured quantiles form [L,H]. A rightward leg contributes

    integral [1-H+L-(F-H)_+] dt,

and a leftward leg contributes

    integral [1-H+L-(L-F)_+] dt.

These hinge areas are integrated exactly on each affine cell. Every endpoint update is evaluated at the actual route vertex. The final captured mass must equal one unless incomplete scoring is explicitly requested.

Component CDF integrals are exact trapezoid integrals over their own affine ray cells. The implementation does not reuse the clipped fan's raw inverse-band formula across the endpoint fold.

## Weight supergradients

For fixed path/window rows and normalized constant weights, each CDF value is affine in the weights. At a supplied law, select actual past ranks that realize H and L before a leg's activation. After activation, use the current CDF for the record that moves on that leg.

This choice gives an affine upper plane in all mixture weights and equality at the supplied law. Its coefficients are therefore a valid concave supergradient, including at a tie. The implementation checks the exact homogeneous identity

    dot(normalized_weights, gradient) = cost.

It also returns the corresponding history selectors on request, so the coefficient interpretation is independently reviewable.

## Arbitrary causal history selectors

The stronger certificate does not require optimal selector choices. At any time t, choose two actual Monster-history times sigma_H(t),sigma_L(t)<=t. For the ordered law,

    survival(t)
       = 1-max_{s<=t} F_closed(s,m(s))
           +min_{s<=t} F_strict(s,m(s))
       <= 1-F_closed(sigma_H(t),m(sigma_H(t)))
           +F_strict(sigma_L(t),m(sigma_L(t))).

Integrating the right side yields an affine upper plane for every normalized mixture on the fixed fan basis.

The historyPlane API supports a partition into pieces where each selector is either a fixed past time or the current time. It checks partition coverage, causality and legal unit Monster geometry. Both endpoints must be visited, ensuring capture by the supplied horizon for every possible basis weight vector.

A numerically proposed activation can therefore be rounded to any legal point in its leg. The resulting selector plane remains valid even if it no longer touches the actual cost. A separately rationalized positive mixture of such planes gives a basis ceiling when its weighted coefficient is bounded for every basis row. This is a statement about that fixed Princess basis, not an unrestricted game upper bound.

## API

    const R=createReflectedFanTools(G);
    const B=R.prepareBasis([
      {id:"row",path:vertices,lower:0,upper:"1/1024"}
    ]);
    const law=R.law(B,weights);

    const result=law.score(monster,{
      gradient:true,
      selectors:true,
      details:true
    });

    const plane=R.historyPlane(B,monster,result.selectors);

The convenience field delta may replace upper for an interval [0,delta]. The provider also exports prepareInterval, marginal, rowTrace and featureIntegral. A history selector piece has the form

    {
      start:"...",
      end:"...",
      upper:{time:"..."} or {current:true},
      lower:{time:"..."} or {current:true}
    }.

Weights must be constant nonnegative rationals with positive total mass. Base profiles must be nonnegative, translation windows must lie in [0,1], and the supplied Monster legs must have unit speed. Unsupported data are rejected.

This source scores a supplied route. It does not search all Monster paths, certify a turn bound, or automatically adapt the clipped-fan continuous-start separator to the reflected geometry.

## Independent physical verification

The verifier uses three complementary checks.

First, it computes each CDF by explicitly partitioning the z interval and measuring the set of folded positions below the query. It does not call the provider's clipped-term CDF.

Second, for a single fan it constructs actual paths at fixed z and the explicit ordered quantile paths r_q above. It inserts their fold/minimum switches, then uses chronological segment intersections with the Monster. Translation and quantile intervals are split at every possible capture-branch change. Exact midpoint integration is checked again at the quarter and three-quarter points.

Third, for multi-fan ordered mixtures it computes the signed CDF directly and integrates newly captured rank bands against their affine first-hit inverses. This is a first-contact moment evaluation, distinct from the provider's survival-area evaluation.

The completed QQ(epsilon) replay passed:

- 245 physical marginal checks;
- 42 directly captured ordered single-fan scores;
- 42 directly captured raw fan scores;
- 780 chronological segment-capture checks;
- 260 affine capture-branch checks;
- 112 component feature-integral checks;
- 20 independent mixed rank-moment scores;
- 80 weight-superplane inequalities;
- 20 nonactive causal selector-plane inequalities;
- 102 active history coefficient identities;
- 3 rejection checks for invalid path/window/selector data.

Two supplied routes show strict rearrangement improvement, so the ordered and raw implementations are not being conflated. The common comparison radius is 1/18816 and the maximum arithmetic degree is 6.

Replay:

    node packages/interval_global_closure/verify_reflected_fan.mjs REPORT.json

The fixture paths, windows and routes are embedded in the verifier. The packet needs only the established exact rational/germ core. It makes no claim about the optimized 342-profile numerical basis or any unrestricted game value.
