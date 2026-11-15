# Exact pursuit pruning for the normalized grid oracle

This note proves the additional lower bound in `normalized_record_pricing.cjs`. It applies only after the input's radial nodal field has passed all exact Qout checks: range, interval-containment order, nonincreasing endpoint trace, and outward-after-two identities. Input metadata alone never enables it.

Use integer time and position coordinates with step `1/(2n)`. Write `R=2n` for an endpoint coordinate and `C=4n` for time 2. Costs below are the integer clock costs before division by `4nD`, where `D` is the field denominator.

At a prefix state `(j,k)`, let `s` be the cost already charged and let `m_-`, `m_+` be the two running minimum prices, before updating them at the current node. Before the first endpoint both clocks are active. At a first endpoint, the clock ending there is inactive and the same formulas give it zero future cost.

## 1. Separate direct pursuits bound both clock costs

For the minus clock, consider the fastest direct route from `k` to `-R`; for the plus clock use its reflected route. At each subsequent time, the direct route is at least as far toward that clock's endpoint as any legal continuation. The nodal transport inequalities imply that the direct clock price is no larger than the corresponding actual price at that same time. They also imply that the direct prices are nonincreasing in time along this route.

Consequently, at every scoring tick, the direct current price is no larger than every actual price seen since the prefix state. Taking its minimum with the entry record bounds the actual running record from below. The direct route reaches its endpoint as early as possible, so assigning zero cost thereafter also gives a lower bound. These statements hold separately for each clock on every actual continuation. Their sum is therefore valid even though the two optimizing direct routes cannot both be followed by one Monster.

For an oriented minus-clock starting position `x` and entry record `m`, let

\[
 L=C-j,\qquad q=\min(L,x+R).
\]

Its prefix lower cost is

\[
 A(j,x,m)=\sum_{i=0}^{q-1}\min\{m,p_-(j+i,x-i)\}.
\]

An initially empty record is interpreted as infinity. The code precomputes the diagonal suffix sums of `p_-`, stopping at time `C` or position `-R`. Since the price sequence is nonincreasing, a binary search locates the initial terms exceeding `m`. The rest is one suffix sum. Every sum and comparison is exact integer arithmetic. The code also checks the required diagonal monotonicity directly.

## 2. Terminal records and center-compatible positions

If `x+R <= L`, the direct endpoint is reachable by time 2; use the terminal rate lower bound `a=0`. Otherwise use

\[
 a=\min\{m,p_-(C,x-L)\}.
\]

This includes the time-2 node, which is not charged in the prefix sum. For an endpoint already visited the same formula gives zero. Applying the construction to `(x,m)=(k,m_-)` and `(-k,m_+)` gives lower rates `a,b` for the minus and plus clocks.

If the center has already been visited, the reachable time-2 positions lie in

\[
 [y_-,y_+]=[\max(-R,k-L),\min(R,k+L)].
\]

If it has not been visited, a legal continuation must travel through zero by time 2. There is no such continuation when `L<|k|`. Otherwise the exact reachable interval is

\[
 [y_-,y_+]=[\max(-R,-L+|k|),\min(R,L-|k|)].
\]

The endpoints have the required grid parity. Allowing every point of these intervals would also be a safe relaxation.

## 3. The remaining two-tour lower bound

For Qout, each surviving clock's running record is constant after time 2. This is the fixed-profile result in `NORMALIZED_GRID_BANK_PRICING.md`; its premise includes updating the time-2 node first. Endpoint clocks have rate zero. With terminal position `y` and nonnegative rates `a,b`, the two possible endpoint orders cost

\[
 (R+y)a+(3R+y)b,
 \qquad
 (3R-y)a+(R-y)b.
\]

The first expression is nondecreasing in `y`; the second is nonincreasing. Minimizing over the reachable interval therefore gives

\[
 T=\min\{(R+y_-)a+(3R+y_-)b,
           (3R-y_+)a+(R-y_+)b\}.
\]

Both expressions are nondecreasing in the rates. Replacing the actual terminal records by their lower bounds thus remains valid, including cases where a clock has become inactive. The final state lower bound is

\[
 s+A(j,k,m_-)+A(j,-k,m_+)+T.
\]

This argument bounds every legal continuation. It does not assume that the separately minimizing pursuits, terminal rates, position, and endpoint order can be attained together.

## 4. Safe target-bound verification

To certify a proposed integer lower bound `K`, remove a state only when the proved expression above is at least `K`, or when it cannot visit the center by the deadline. Enumerate every remaining normalized continuation with the ordinary exact record dynamic program. Reject if any completed route has cost below `K`.

If the enumeration finishes without rejection, every route either passed through a state with a proved cost lower bound at least `K`, was removed by exact record-state dominance, or was explicitly evaluated and met the bound. Hence the exact all-path minimum is at least `K`. No feasible route of value `K` and no numerical optimizer assumption are needed.

In exact-minimum mode, the cutoff instead comes from an already evaluated route. This retains an attaining route and proves equality. Both modes use the same physical bank normalization and the same common-quantization theorem to infer the unrestricted game-value bound.
