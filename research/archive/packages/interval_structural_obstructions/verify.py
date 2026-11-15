"""Exact nine-point response certificate, checked by two cost formulations.

Run with Python's standard library. No numerical optimizer is used.
Positions and elapsed times are in quarter-units; all costs are integers
until the final division by four times total probability weight.
"""

from fractions import Fraction
from functools import lru_cache


POSITIONS = tuple(range(-4, 5))
WEIGHTS = tuple(8 ** (4 - abs(x)) for x in POSITIONS)
TOTAL_WEIGHT = sum(WEIGHTS)
EXPECTED_COSTS = (6016, 3236, 3052, 3048)


def enumerate_capture_orders():
    """Accumulate each target's own weight times its first-capture time."""
    records = []

    def visit(left, right, current, time, cost, direction, inner_turns, route):
        if left == 0 and right == len(POSITIONS) - 1:
            records.append((cost, inner_turns, route))
            return
        for nxt in (left - 1, right + 1):
            if not 0 <= nxt < len(POSITIONS):
                continue
            new_direction = 1 if nxt > current else -1
            new_time = time + abs(POSITIONS[nxt] - POSITIONS[current])
            new_turn = (direction != 0 and direction != new_direction
                        and abs(POSITIONS[current]) < 4)
            visit(min(left, nxt), max(right, nxt), nxt, new_time,
                  cost + WEIGHTS[nxt] * new_time, new_direction,
                  inner_turns + int(new_turn),
                  route + ((new_time, POSITIONS[nxt]),))

    for start in range(len(POSITIONS)):
        visit(start, start, start, 0, 0, 0, 0, ((0, POSITIONS[start]),))
    return records


def bellman_cost(maximum_inner_turns):
    """Independently integrate the mass still uncaptured over travel time.

    The state has no elapsed-time or accumulated-cost coordinate. Advancing
    by distance d before the next new capture costs d times remaining mass.
    """
    n = len(POSITIONS)

    @lru_cache(None)
    def remaining(left, right, current, direction, turns_left):
        if left == 0 and right == n - 1:
            return 0
        mass = sum(WEIGHTS[:left]) + sum(WEIGHTS[right + 1:])
        candidates = []
        for nxt in (left - 1, right + 1):
            if not 0 <= nxt < n:
                continue
            new_direction = 1 if nxt > current else -1
            turn = int(direction != 0 and direction != new_direction
                       and abs(POSITIONS[current]) < 4)
            if turn > turns_left:
                continue
            continuation = remaining(min(left, nxt), max(right, nxt), nxt,
                                     new_direction, turns_left - turn)
            if continuation is not None:
                candidates.append(mass * abs(POSITIONS[nxt] - POSITIONS[current])
                                  + continuation)
        return min(candidates) if candidates else None

    values = [remaining(i, i, i, 0, maximum_inner_turns) for i in range(n)]
    return min(value for value in values if value is not None)


def main():
    assert TOTAL_WEIGHT == 5266
    records = enumerate_capture_orders()
    assert len(records) == 256
    minima = tuple(min(cost for cost, turns, _ in records if turns <= cap)
                   for cap in range(4))
    assert minima == EXPECTED_COSTS
    assert tuple(bellman_cost(cap) for cap in range(4)) == EXPECTED_COSTS
    assert bellman_cost(8) == EXPECTED_COSTS[-1]
    best = min(cost for cost, _, _ in records)
    optimizers = [route for cost, _, route in records if cost == best]
    assert len(optimizers) == 2
    assert optimizers[0] == tuple((t, -x) for t, x in optimizers[1])
    assert {route[-1][0] for route in optimizers} == {24}
    for cap, cost in enumerate(minima):
        print(f"Interior-turn cap {cap}: {Fraction(cost, 4 * TOTAL_WEIGHT)}")
    gap = Fraction(minima[2] - best, 4 * TOTAL_WEIGHT)
    assert gap == Fraction(1, 5266)
    print("PASS: 256 capture orders and independent Bellman recurrence agree.")
    print("PASS: exactly two reflected minimizers; final capture at time 6.")
    print(f"PASS: restricting to two interior turns loses exactly {gap}.")


if __name__ == "__main__":
    main()
