# Exact structural counterexample

Run `python verify.py`. Only Python's standard library is required.

The verifier checks a symmetric stationary princess distribution on nine
positions. Its optimal monster responses require three interior turns and
finish at time six. Restricting to at most two interior turns increases the
minimum expected capture time by exactly `1/5266`.

Two implementations agree: exhaustive first-capture-order enumeration and
a Bellman recurrence integrating uncaptured mass over elapsed travel time.
The latter has no accumulated-time or accumulated-cost state.

The complete hand proof, including a family forcing arbitrarily many
interior turns and arbitrarily large optimal-response horizons, is in
`../../research/07-structural-audit/CAPTURE_ORDER.md`.

This is a counterexample to a universal response-shape reduction. It does
not determine the unrestricted Princess–Monster game value.
