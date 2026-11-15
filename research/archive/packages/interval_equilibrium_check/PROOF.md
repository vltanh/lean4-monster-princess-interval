# Exact fixed-support equilibrium check and support exclusion

## Status

**This does not solve the unrestricted interval Princess–Monster game.** It completes the first proposed gate (an exact finite-support minimax LP), and proves that the specific support used in that gate cannot contain an optimal unrestricted monster strategy, regardless of its probabilities.

The exact unrestricted value is not identified. No finite exhaustive classification of unrestricted equilibria is established. The computational search for a matching pair did not close.

The proof below is mathematical prose with exact arithmetic certificates. It is not a Lean formalization or an independently reviewed theorem.

## 1. Rules and the fixed support

Both players independently select hidden 1-Lipschitz paths in [-1,1], including their initial positions. Capture is the first equality, including time zero. The princess maximizes expected capture time and the monster minimizes it.

The initial monster support S has 32 paths: each of the following 16 paths, together with its reflection.

M1(x): vertices (0,x), (1-x,1), (3-x,-1).

M2(x): vertices (0,x), ((1-x)/2,(1+x)/2), (2,-1), (4,1).

The starts are:

* M1: -1, 5/8, 3/4, 7/8.
* M2: -7/8, -3/4, -5/8, -1/2, -3/8, -1/4, 1/4, 3/8, 1/2, 5/8, 3/4, 7/8.

Constant tails are added through H=4 where needed. Every path completes an endpoint-to-endpoint traversal by H. Thus it captures every continuous princess by H.

The restricted minimax quantity is

    U(S) = inf_{nu supported on S} sup_{all admissible p} E_nu T(M,p).

The princess is NOT restricted in this quantity. Only the monster support is fixed. Symmetrizing a monster distribution cannot worsen its upper guarantee, so reflection pairs may be assigned equal probabilities.

## 2. Completed result

The exact value of this fixed-support problem is

    c = 13394119476306831993 / 9350024947551443632.

This is approximately 1.4325223249606884. It is NOT the unrestricted game's value.

`certificate.json` specifies 16 positive pair probabilities w, 16 positive dual probabilities q, 16 feasible capture-deadline vectors r, their initial chambers, and the exact matrix

    A[k,j] = (r[k,2j] + r[k,2j+1])/2.

The verifier checks the exact equalities

    sum_j w_j = sum_k q_k = 1,
    A w = c 1,
    q^T A = c 1^T.

It also checks the geometric feasibility of all deadline vectors and exact integer flow certificates for every initial-position chamber.

## 3. Why the finite certificate is unrestricted on the princess side

Fix an open interval between consecutive monster starting points. Write B for monsters initially below the princess, A for those above. Let d_i be the first arrival at the opposite wall: +1 for B, -1 for A. Let tau_ij be the first meeting of an opposite-side pair.

Every actual capture-time vector obeys

    0 <= r_i <= d_i,
    min(r_i,r_j) <= tau_ij  (i in B, j in A).

Before capture, a monster initially below the princess remains below her, and one initially above remains above her. The opposite-side constraints therefore follow from continuity. The wall constraints follow in the same way.

Conversely, a feasible deadline vector can be approached by unit-speed princess paths. For epsilon>0, put e_i=max(0,r_i-epsilon). Retain each B-path until e_i, then continue it downward at speed one. Retain each A-path until e_i, then continue it upward at speed one. Let L be the maximum of the lower curves and -1; let U be the minimum of the upper curves and +1.

The constraints imply L<U. Before either of an opposite-side pair expires, the curves have not yet met; after the first expires, its continuation moves away at the maximum possible speed. The wall constraints similarly ensure separation from the opposite wall.

Both envelopes are 1-Lipschitz. For any fixed 0<lambda<1, the convex combination

    p_epsilon = (1-lambda)L + lambda U

is admissible and remains on the required side of monster i through e_i. Choosing lambda from the desired initial point gives

    T(m_i,p_epsilon) >= r_i-epsilon.

Consequently, the supremum over princess paths is exactly the maximum weighted feasible deadline objective. The supremum need not be attained by one princess path.

### Finite event reduction and the upper certificate

All deadlines and first pair meetings form a finite event set. Rounding each feasible r_i upward to the next event preserves feasibility and cannot reduce the objective. Survival beyond each event can therefore be represented by binary variables. Survival monotonicity, wall deadlines, and opposite-side meeting constraints are directed implications.

The supplied network has the property that every actual princess yields a cut with capacity

    H - sum_i probability_i * rounded_capture_i.

A feasible flow F consequently gives the upper guarantee H-F. Only weak flow-cut duality is needed; no claim of an optimizer is trusted.

`flows.json.gz` supplies an integer flow for each of the seven nonnegative starting-position chambers. `verify.py` rebuilds the networks, checks every integer capacity and conservation equation, and obtains H-F=c in every chamber. Reflection handles negative starts. At a monster starting point, the coincident monsters capture at time zero, and the neighboring chamber inequalities still apply.

Thus the monster distribution w guarantees at most c against every princess path.

### The dual lower certificate for this support

For every deadline row k, the approaching princess construction gives capture times at least r[k,i]-epsilon against every member i of S. Mix these families using q, and symmetrize. The equality q^T A=c 1^T implies

    E T(m_j,P_epsilon) >= c-epsilon

for every monster path m_j in S, and hence for every mixture on S. Let epsilon decrease to zero. Together with the upper certificate, this proves U(S)=c.

This argument does NOT apply the lower inequality to monsters outside S.

## 4. The initial support is rigorously ruled out for the full game

A separate monster distribution, with 68 paths, is supplied in `exclusion_strategy.json`. Its probabilities have denominator 1,000,000 before dividing by two for reflection. Every path is an M1 or M2 path with a finer set of starting positions.

`exclusion_flows.json.gz` contains exact integer flows covering its 14 nonnegative starting chambers. The same unrestricted upper-bound argument proves that this distribution guarantees at most

    b = 5717477 / 4000000.

The verifier checks

    b < c.

Therefore

    V <= b < U(S).

This rules out EVERY probability distribution on the original 32-path support S as an unrestricted optimal strategy. It is stronger than rejecting one particular reweighting or one chosen dual representative.

The comparison is included as an exclusion certificate, not as a substitute for finding the exact unrestricted value. It does not rule out the continuum of all M1/M2 paths or assert that the 68-path support is optimal.

## 5. A symbolic check of the proposed dual continuation

For transparency, the package also constructs one natural realization of the 16 dual deadline rows: take the midpoint of each starting chamber and use the constant convex blend of the two survival envelopes. Mix these paths and their reflections with probabilities q_k/2.

The geometry is calculated in exact affine arithmetic a+b*epsilon. Every comparison records a positive interval on which its sign is valid. The program checks admissibility and all deadline guarantees symbolically, not only at a sample epsilon.

The omitted monster path

    (0,-15/16), (31/16,1), (63/16,-1)

has expected capture time against this chosen dual family equal to

    27356900849985340679 / 32725087316430052712
      - (84148771486765172 / 240625642032573917) * epsilon,

for 0<epsilon<1/64. Its limit is approximately 0.835961126259561, strictly below c.

This is NOT a bound on the full game. It is a counterexample to this particular proposed extension of the fixed-support dual strategy. Other realizations of the deadline rows need not have the same weakness. Independently, Section 4 proves that no realization can supply a full-game lower guarantee matching c, because c is already above a universal monster upper guarantee.

## 6. What the broader computer-assisted search did

The accompanying research log records fixed-support cutting-plane optimizations and several two-sided response-generation experiments. The search used the princess deadline oracle, LP dual solutions, and capture-order monster searches. Later versions preserved small turns with exact ordered-polynomial geometry rather than erasing them by floating-point simplification.

No run yielded matching unrestricted guarantees. Several large monster searches reached an explicit node cap. Such outputs are exhibited improving responses, not certified minima and not lower bounds on the full game's value. LP weights and objective values in the exploratory runs are floating-point quantities, even when the path geometry is exact.

The exact assertions of this package are limited to Sections 2-5 and the checks performed by `verify.py`. In particular, no convergence or finite termination theorem for the expanding-support search is claimed.

## 7. Reproduction

Run:

    python verify.py

Only Python's standard library is required. The verifier checks the two flow systems, the primal-dual identities, the geometric deadline constraints, the strict support exclusion, and the symbolic counterexample. It does not call a numerical optimizer.

`verification_output.txt` records one successful run, but is not a replacement for running the verifier.

## Sources and attribution

The finite deadline-response theorem used here is the theorem derived in the earlier conversation artifact `REDUCTION.md`; its proof is reproduced above. It is not claimed as externally reviewed.

The unrestricted finite-hider capture-order search used in the exploratory work is based on Proposition 5 of S. Alpern, R. Fokkink, R. Lindelauf and G. J. Olsder, “The ‘Princess and Monster’ Game on an Interval,” SIAM Journal on Control and Optimization 47(3), 1178-1190 (2008), DOI 10.1137/060672054. Propositions 7 and 8 supply uncrossing and the half-interval restriction used in some exploratory optimizations. The exact flow certificate itself does not depend on the capture-order search.
