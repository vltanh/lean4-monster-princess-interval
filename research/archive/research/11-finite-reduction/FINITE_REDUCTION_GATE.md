# Finite-reduction gate: exact obstruction and finite certificate verification

Date: 2026-11-11.

**The requested full minimax finite reduction is NOT established. G5 remains open.**

The user has directed the work to find the finite reduction first, using computer assistance, rather than refine the value interval or continue endpoint fitting. This checkpoint performs no numerical interval refinement and does not construct an equilibrium.

A finite minimax reduction and a finite certificate-verification reduction are different claims. The former needs a fixed, sufficient strategy or phase class for the game's value. The latter certifies a supplied finitely described strategy against all opponent paths. The results below prove an obstruction to a proposed route to the former, and implement a version of the latter. They must not be reported as closure of G5.

## 1. Endpoint absorption does not supply a universal turn bound

### Theorem 1

For every k>=1 there is a symmetric, ordered princess law whose paths remain in their initial half-interval and reach an endpoint by time two, such that every optimal monster response has at least k interior direction reversals. The same obstruction can be realized with an atomless initial distribution and a continuous piecewise-affine interior space-time CDF.

These are specified-law response examples, not optimal hiding laws for the full game. The theorem does not exclude an equilibrium-specific finite reduction.

### Explicit atomic construction

Put

    B = 16*k*k+1,
    W = B^k+2*sum_{i=1}^k B^(k-i),
    delta = 1/(4W).

Place unnormalized mass B^(k-|i|) at x_i=delta*i/k, -k<=i<=k. Each path stays there until time one, then runs to the endpoint of its sign and remains there. Split the central mass equally between its two reflected outgoing paths. Normalize by W.

The smallest positive physical-path mass is 1/W. A monster leaving any initial site uncaptured until time one has expected cost at least 1/W. Starting at -delta and sweeping directly to +delta captures everything by time 2delta=1/(2W)<1. Its cost is less than 1/W, and it uses no reversal before capture completion. Therefore both unrestricted and turn-capped response optima occur entirely in the stationary prefix.

For stationary sites, delete empty excursions, shift the start to the first captured site, and run directly between new captures. No capture is delayed and no reversal is added. The captured sites expand a contiguous interval. There are exactly 2^(2k)=4^k complete expansion orders; every canonical order completes by 4k*delta=k/W<1. Enumeration is therefore exact for the continuous-time response problem, not a sampled-path approximation.

In integer spatial units delta/k let G_0=T(0) and G_i=T(i)+T(-i). Canonical times are integers and G_i<=8k^2. If two orders first differ at index j, the leading weighted improvement is at least B^(k-j), whereas the possible later loss is less than

    8k^2*sum_{i=j+1}^k B^(k-i)
      < B^(k-j)*8k^2/(B-1) = B^(k-j)/2.

Thus objective minimization is lexicographic in the shell capture-time sums. G_0 forces the initial position to be zero. Each successive shell must be visited by continuing to its nearer point, reversing, then crossing directly to its other point. The other order has a strictly greater shell sum. This forces one reversal per shell, up to the initial reflection. All these reversals are inside the arena, including those at the compressed outer sites +/-delta.

The final capture time is delta*(k+2), and the exact integer weighted cost is

    2*sum_{i=1}^k B^(k-i)*i*(i+1).

The normalized gap to any order with at most k-1 reversals is at least

    Delta_k >= delta/(kW) > 0.                       (1)

### Atomless version

Let n=2k+1. Replace each initial atom by a uniform interval of half-width

    eta = delta/(100*n*k*W).

The intervals are disjoint. Every initial point waits until time one and then runs to its own signed endpoint. The central interval splits symmetrically at zero. The resulting interior CDF is continuous and piecewise affine: before time one it is the initial CDF; afterwards it consists of its two translates, a central gap, and endpoint masses. Its finite cell count grows with k.

Independently sample one site in each interval. For every sampled tuple a direct sweep finishes before time one and costs less than its smallest atomic weight, so its turn-capped optimum is again a stationary capture-order optimum. Moving each site by at most eta changes any fixed order's mean cost by at most 2(n-1)eta and preserves its direction word. Averaging over sampled tuples gives

    V_K(smoothed) >= V_K(atomic)-2(n-1)eta.           (2)

Conversely, follow an optimal atomic route, scanning each small interval before continuing. Each scan adds at most 4eta; every capture is delayed by at most 4n eta and still occurs before time one. Hence

    V_*(smoothed) <= V_*(atomic)+4n eta.              (3)

For K=k-1, equations (1)-(3) give

    V_{k-1}(smoothed)-V_*(smoothed)
      >= delta/(kW)-(6n-2)eta > 0.                   (4)

A cap on interior reversals alone has the same consequence. Between two sampled site captures before time one, a trip to an arena endpoint and back takes at least 2(1-delta-eta)>1. Endpoint reversals therefore cannot replace a required interior capture-order reversal. Reversals before the first capture disappear when the start is shifted.

Thus neither bounded endpoint-absorption time, removal of interior atoms, nor piecewise-affine CDF regularity justifies a universal turn cutoff. A strategy-complexity bound would have to use additional equilibrium-specific structure.

### Exact executed search

The new standard-library script enumerated every complete order for k=1,...,9, using B above, plus a compact k=4, B=8 fixture: **349,780 orders total**. The first nine cases have exactly two optimal capture orders and require k turns. The analytic cost and late-capture separation are checked explicitly.

In the compact fixture W=5266 and delta=1/21064. The unrestricted response is 381/55461512; the best three-turn response is 763/110923024, a strict gap of 1/110923024. These numbers are response-example values, not game bounds.

## 2. A finite arithmetic verifier for an all-monster lower certificate

This specializes the global captured-rank Bellman method in `research/10-turn-density/GLOBAL_CDF_BELLMAN.md`. It makes all local and boundary checks finite for supplied polynomial data. It does not establish that an optimal finite certificate exists.

### Supplied data and legality

Supply a normalized ordered princess law with a continuous piecewise-affine interior CDF F(t,x), 0<=t<=H, on a finite rational polyhedral partition. Its endpoint interior traces b_-(t), b_+(t) are continuous, b_- is nondecreasing, b_+ is nonincreasing, and

    0<=F<=1,             F_x>=|F_t|.                 (5)

At -1 the strict/closed CDF traces are (0,b_-); at +1 they are (b_+,1). At H the interior CDF is constant, so all paths are endpoint-absorbed. These are finite checks on the affine cells and interfaces. The speed-cone inequalities imply that the ordered quantile coupling is 1-Lipschitz. Alternatively supply legal ordered paths and prove these CDF properties directly.

Supply a continuous piecewise-quadratic remaining-duration potential W(t,x,l,h) on a finite rational polyhedral partition of

    0<=l<=F(t,x)<=h<=1.

Include one-sided endpoint states before reset. Continuity on shared faces is a polynomial identity condition, not just equality at vertices. The records l,h are the lowest strict and highest closed CDF ranks visited by the monster; surviving mass is S=l+1-h.

### Four record cases and three critical speeds

On an affine CDF cell put F_t=b, F_x=a. At monster speed v,

    d=b+a*v,
    ldot=min(d,0) if l=F, otherwise 0,
    hdot=max(d,0) if h=F, otherwise 0.

Require

    W_t+v*W_x+W_l*ldot+W_h*hdot+S >= 0.              (6)

The four record cases are l<F<h, l=F<h, l<F=h, and l=h=F. In each case the residual is piecewise affine in v. Its only possible interior breakpoint is v_track=-b/a when a>0. Thus v=-1, +1, and v_track cover every speed in [-1,1]. If a=0 then b=0 and the unit speeds suffice.

No record monotonicity or concavity of W is assumed in this three-speed version. If W_l>=0 and W_h<=0 are separately imposed, the residual is concave in v and the tracking-speed check is redundant. Without those conditions an endpoint-only control check can fail: the residual |v|-1/10 is positive at both unit speeds but negative at zero.

For each fixed record case and critical speed, (6) is AFFINE in the four state variables: the derivatives of W are affine and the CDF slopes are constant. Checking vertices of the corresponding bounded rational polytope is sufficient. Case closures can be imposed as sufficient conditions; empty cases are discarded.

### Boundary cases

The following are also required:

- First contact at +1 resets (l,h) to (l,1); at -1 it resets to (0,h). Require W_before<=W_after. These are zero-time resets, with no duration charge.
- Endpoint waiting is a separate tangency check with speed zero and the surviving boundary record updated using b_+' or b_-'. Checking only inward legs is insufficient.
- At H, W must not exceed either endpoint-only completion cost:

      E_left = l*(1+x)+(1-h)*(3+x),
      E_right = (1-h)*(1-x)+l*(3-x).

- At interior initial positions require W(0,x,F(0,x),F(0,x))>=c. Endpoint starts use their already-reset strict/closed records.

After refining pre/post potential pieces, reset, terminal and initial differences are rational quadratics on finitely many rational polytopes. Quadratic inequalities cannot in general be checked only at vertices.

### Exhaustive finite quadratic minimization

For q(z)=q0+g.z+z^T Qz on a bounded rational polytope Az<=b, enumerate independent subsets of at most dim(z) active constraints. Restrict q to each affine face and solve its linear stationarity equations. If singular, retain the entire stationary affine solution space and test its intersection with the face inequalities by exact rational vertex enumeration. The quadratic is constant on that stationary affine space, so one feasible witness gives its value.

This is exhaustive: a global minimum exists and lies in the relative interior of some face, where every tangent derivative vanishes. Zero-dimensional faces include vertices. The method needs no positive-definiteness assumption and includes singular and indefinite quadratics.

### Theorem 2: unrestricted-path validity

If these finite obligations hold, the supplied law guarantees c against every 1-Lipschitz monster, including slower motion, waiting, and infinitely many turns.

Away from first endpoint resets, the records are running extrema of a Lipschitz CDF composed with an absolutely continuous path. Their derivatives have the displayed form almost everywhere. A continuous piecewise-quadratic W is locally Lipschitz on the finite feasible partition. At interfaces, continuity identifies tangential derivatives, and checking every incident piece is sufficient. The three-control test proves (6) at the actual monster speed almost everywhere; endpoint tangency checks cover waiting.

Integrate to obtain

    W(initial) <= integral_0^H S(t)dt + W(H,state).

The first visits to the two endpoints contribute at most two zero-time resets, whose inequalities preserve this estimate. Endpoint ranks remain there, so later visits introduce no further reset of that side. Every actual continuation costs at least min(E_left,E_right). The survival integral is expected elapsed capture time up to H. The initial and terminal inequalities prove the claim.

This proof does not replace unrestricted paths by a fixed-turn family or rely on favorable convergence of first-capture times.

### Implemented scope and executed checks

`packages/interval_finite_reduction_audit/` is a standard-library reference prototype, not an automatic solver or parser for arbitrary repository fields. It contains rational polytope vertices, face-stationary quadratic minimization, local derivative checks, and complete executable fixtures. A field/potential partition and its exhaustive interface list remain explicit inputs.

Executed: 5,280 exact derivative identities against finite-time record evolution; 5,280 critical-speed comparisons; seven exact quadratic-minimum fixtures; and five complete certificates for specified endpoint-supported laws, including free starts, waiting, resets, and terminal costs. Their exact response values are independently attained by starting at the heavier endpoint. They are not unrestricted game values.

## 3. What remains missing

This supplies finite verification for fixed finite data, not a fixed finite description of an unrestricted equilibrium. In particular, finite local control cases do not imply finitely many optimal phases, and a finite partition for each supplied law does not imply a uniform partition bound at the game's value.

The next required theorem is an equilibrium-specific bounded certificate/phase-complexity result, or one explicit finite certificate pair directly attaining the unrestricted value. A hierarchy whose complexity grows with accuracy is not the requested terminating reduction. Neither missing result has been established here; G5 remains open.

No Lean compilation, CI, independent external review, or matching saddle certificate is claimed.
