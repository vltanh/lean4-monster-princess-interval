#!/usr/bin/env python3
"""Exact regressions for common quantization and integer clock calendars."""
from fractions import Fraction as Q
from itertools import product
import json


def nearest(z, n):
    y = z * n
    lower = y.numerator // y.denominator
    fraction = y - lower
    if fraction < Q(1, 2):
        integer = lower
    elif fraction > Q(1, 2):
        integer = lower + 1
    else:
        integer = lower if lower % 2 == 0 else lower + 1
    return Q(integer, n)


def position(path, time):
    for (a, x), (b, y) in zip(path, path[1:]):
        if a <= time <= b:
            return x + (y - x) * (time - a) / (b - a)
    raise AssertionError(("time outside path", time))


def first_hit(path, target):
    for (a, x), (b, y) in zip(path, path[1:]):
        if x == target:
            return a
        if x != y and min(x, y) <= target <= max(x, y):
            return a + (target - x) * (b - a) / (y - x)
    if path[-1][1] == target:
        return path[-1][0]
    raise AssertionError(("missing endpoint", target))


def image_node(path, time, n):
    x = position(path, time)
    return nearest(time + x, n), nearest(time - x, n)


def physical(node):
    u, v = node
    return (u + v) / 2, (u - v) / 2


def threshold_times(path, n):
    cuts = {t for t, x in path}
    for (a, x), (b, y) in zip(path, path[1:]):
        speed = (y - x) / (b - a)
        intercept = x - speed * a
        for slope, offset in ((1 + speed, intercept), (1 - speed, -intercept)):
            if not slope:
                continue
            low, high = slope * a + offset, slope * b + offset
            for k in range(int(low * n) - 3, int(high * n) + 4):
                level = Q(2 * k + 1, 2 * n)
                time = (level - offset) / slope
                if a < time < b:
                    cuts.add(time)
    return sorted(cuts)


def quantize(path, n):
    cuts = threshold_times(path, n)
    samples = set(cuts)
    samples.update((a + b) / 2 for a, b in zip(cuts, cuts[1:]))
    chain = []
    for time in sorted(samples):
        node = image_node(path, time, n)
        if not chain or node != chain[-1]:
            chain.append(node)
    h = Q(1, n)
    lattice = [chain[0]]
    mixed = 0
    for a, b in zip(chain, chain[1:]):
        du, dv = (b[0] - a[0]) / h, (b[1] - a[1]) / h
        assert du in (0, 1) and dv in (0, 1) and du + dv > 0
        if du and dv:
            options = [
                corner for corner in ((b[0], a[1]), (a[0], b[1]))
                if abs(corner[0] - corner[1]) <= 2
            ]
            assert options
            # Local legal-fill sets are exchanged exactly by reflection.
            reflected = {(y, x) for x, y in options}
            reverse_options = {
                corner for corner in ((b[1], a[0]), (a[1], b[0]))
                if abs(corner[0] - corner[1]) <= 2
            }
            assert reflected == reverse_options
            lattice.append(options[0])
            mixed += 1
        lattice.append(b)
    assert all(node in lattice for node in chain)
    new = [physical(node) for node in lattice]
    assert new[0][0] == 0
    for a, b in zip(new, new[1:]):
        assert b[0] - a[0] == h / 2
        assert abs(b[1] - a[1]) == h / 2
        assert -1 <= b[1] <= 1
    assert first_hit(new, -1) <= path[-1][0]
    assert first_hit(new, 1) <= path[-1][0]
    if first_hit(path, 0) <= 2:
        assert first_hit(new, 0) <= 2
    for time in samples:
        mapped_time, mapped_x = physical(image_node(path, time, n))
        assert abs(mapped_time - time) <= h / 2
        assert position(new, mapped_time) == mapped_x
    return new, cuts, mixed


def add(measure, time, mass):
    if mass:
        measure[time] = measure.get(time, Q(0)) + mass


def push_clock(path, cuts, n, kind):
    tau = first_hit(path, -1)
    times = sorted({Q(0), tau, *(t for t in cuts if 0 < t < tau)})
    measure = {}
    for a, b in zip(times, times[1:]):
        # Current-time clock is Lebesgue mass on this interval. The atomic
        # variant selects its left endpoint, including exact rounding ties.
        selected = (a + b) / 2 if kind == "current" else a
        new_time, x = physical(image_node(path, selected, n))
        add(measure, new_time, b - a)
    assert sum(measure.values(), Q(0)) == tau
    return measure, tau


def causal_repair(path, n, kind):
    new, cuts, mixed = quantize(path, n)
    pushed, tau = push_clock(path, cuts, n, kind)
    delta = Q(1, 2 * n)
    tau_new = first_hit(new, -1)
    assert tau_new <= tau + delta
    maximum_defect = Q(0)
    for time, x in new:
        if 0 < time <= tau_new:
            before = sum((mass for s, mass in pushed.items() if s < time), Q(0))
            maximum_defect = max(maximum_defect, time - before)
            assert before >= time - delta
    raw = dict(pushed)
    add(raw, Q(0), delta)
    remaining = tau_new
    kept = {}
    for time in sorted(raw):
        part = min(remaining, raw[time])
        add(kept, time, part)
        remaining -= part
    assert remaining == 0
    assert sum(kept.values(), Q(0)) == tau_new
    assert all(time < tau_new for time in kept)
    for time, x in new:
        if 0 < time <= tau_new:
            assert sum((mass for s, mass in kept.items() if s < time), Q(0)) >= time
    assert all(position(new, time) != -1 for time in kept)
    return maximum_defect, tau_new < tau, mixed


def calendars(real):
    k = len(real)
    cumulative = []
    total = Q(0)
    for j, value in enumerate(real):
        total += value
        cumulative.append(total)
        assert total >= j + 1
    assert total == k
    cuts = {Q(0), Q(1)}
    for value in cumulative:
        fractional = value - value.__floor__()
        if fractional:
            cuts.add(1 - fractional)
    cuts = sorted(cuts)
    result = []
    average = [Q(0)] * k
    for a, b in zip(cuts, cuts[1:]):
        z = (a + b) / 2
        rounded = [(value + z).__floor__() for value in cumulative]
        charges = [value - (rounded[j - 1] if j else 0) for j, value in enumerate(rounded)]
        assert all(value >= 0 for value in charges)
        assert sum(charges) == k
        assert all(sum(charges[:j + 1]) >= j + 1 for j in range(k))
        for j, value in enumerate(charges):
            average[j] += (b - a) * value
        result.append((b - a, charges))
    assert average == real
    return result


def check_two_queue_paths():
    minus = [Q(3), Q(0), Q(1, 2), Q(1, 2), Q(1), Q(1)]
    plus = [Q(3, 2), Q(1, 2)]
    count = 0
    # Physical path: center -> +1 at step2 -> -1 at step6.
    for (wm, cm), (wp, cp) in product(calendars(minus), calendars(plus)):
        qm = qp = 0
        dead_m = dead_p = False
        charge_count = 0
        previous_progress = 0
        for j in range(6):
            for side, amount in (("minus", cm[j]), ("plus", cp[j] if j < 2 else 0)):
                for _ in range(amount):
                    assert not (dead_m if side == "minus" else dead_p)
                    if side == "minus":
                        qm += 1
                    else:
                        qp += 1
                    progress = 3 * j + qm + qp
                    assert progress > previous_progress
                    previous_progress = progress
                    assert qm <= 16 - j and qp <= 16 - j
                    charge_count += 1
            if not dead_m:
                assert qm >= 1
                qm -= 1
            if not dead_p:
                assert qp >= 1
                qp -= 1
            if j + 1 == 2:
                assert qp == 0
                dead_p = True
            if j + 1 == 6:
                assert qm == 0
                dead_m = True
            progress = 3 * (j + 1) + qm + qp
            assert progress > previous_progress
            previous_progress = progress
        assert dead_m and dead_p and charge_count == 8
        count += 1
    assert calendars([]) == [(Q(1), [])]
    return count


def phi(radius, x):
    if x > 0:
        return 1 + int(radius < x)
    if x < 0:
        return int(radius > -x)
    return int(radius > 0)


def check_containment():
    count = 0
    collapse = 0
    for n, t, s, x, y in product(
        range(1, 5),
        [Q(0), Q(1, 4), Q(1, 2), Q(1)],
        [Q(0), Q(1, 4), Q(1, 2), Q(1)],
        [Q(1, 8), Q(1, 4), Q(1, 2)],
        [Q(1, 4), Q(1, 2), Q(3, 4), Q(1)],
    ):
        if y < x + abs(s - t):
            continue
        a, b = nearest(t - x, n), nearest(t + x, n)
        c, d = nearest(s - y, n), nearest(s + y, n)
        assert c <= a <= b <= d
        tp, xp = (a + b) / 2, (b - a) / 2
        tn, yn = (c + d) / 2, (d - c) / 2
        assert xp >= 0 and yn >= 0
        if yn == 0:
            assert xp == 0
            collapse += 1
        for initial, speed in product([Q(0), Q(1, 4), Q(1)], [Q(-1), Q(0), Q(1)]):
            rp = min(Q(1), max(Q(0), initial + speed * tp))
            rn = min(Q(1), max(Q(0), initial + speed * tn))
            assert phi(rp, xp) + phi(rn, -yn) <= 2
        count += 1
    return count, collapse


def main():
    quantizer_checks = 0
    for n in range(1, 6):
        points = [Q(k, 4 * n) for k in range(-40 * n, 40 * n + 1)]
        mapped = [nearest(z, n) for z in points]
        assert mapped == sorted(mapped)
        for z, image in zip(points, mapped):
            assert image == -nearest(-z, n)
            assert nearest(z + 2, n) == image + 2
            assert abs(image - z) <= Q(1, 2 * n)
            quantizer_checks += 3
    fixtures = [
        [(Q(0), Q(0)), (Q(1), Q(0)), (Q(2), Q(1)), (Q(4), Q(-1))],
        [(Q(0), Q(1, 4)), (Q(1), Q(1, 4)), (Q(7, 4), Q(1)), (Q(15, 4), Q(-1)), (Q(4), Q(-1))],
        [(Q(0), Q(-7, 8)), (Q(15, 8), Q(1)), (Q(31, 8), Q(-1)), (Q(4), Q(-1))],
        [(Q(0), Q(0)), (Q(9, 10), Q(-9, 10)), (Q(14, 5), Q(1)), (Q(24, 5), Q(-1)), (Q(6), Q(-1))],
    ]
    repaired, early, simultaneous, sharp_buffer = 0, 0, 0, 0
    for path, n, kind in product(fixtures, range(1, 5), ("current", "atomic")):
        defect, shortened, mixed = causal_repair(path, n, kind)
        repaired += 1
        early += int(shortened)
        simultaneous += mixed
        sharp_buffer += int(defect == Q(1, 2 * n))
    assert early and simultaneous and sharp_buffer
    matched, collapsed = check_containment()
    assert collapsed
    calendar_count = check_two_queue_paths()
    for radius, x in product([Q(0), Q(1, 4), Q(1, 2), Q(1)], [Q(0), Q(1, 4), Q(1, 2), Q(1)]):
        assert phi(radius, x) + phi(radius, -x) <= 2
    print(json.dumps({
        "status": "PASS",
        "quantizer_identities": quantizer_checks,
        "physical_clock_repairs": repaired,
        "early_endpoint_cases": early,
        "simultaneous_jump_fills": simultaneous,
        "sharp_delta_buffer_cases": sharp_buffer,
        "matching_containments": matched,
        "collapsed_target_cases": collapsed,
        "two_queue_calendar_paths": calendar_count,
    }, indent=2))


if __name__ == "__main__":
    main()
