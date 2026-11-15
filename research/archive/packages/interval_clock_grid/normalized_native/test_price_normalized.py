#!/usr/bin/env python3
"""Independent exact regression of the native normalized physical-path oracle.

Small grids use exhaustive Fraction path enumeration with no dominance, record
merging, or cost pruning. Known grid certificates additionally use independent
integer record DP merging only identical position/record/center states.
The physical-bank normalization theorem is outside this regression's scope.
"""
from __future__ import annotations

import argparse
from fractions import Fraction as Q
import hashlib
import json
from pathlib import Path
import random
import struct
import subprocess
import tempfile


def require(ok, message):
    if not ok:
        raise AssertionError(message)


def legal_nodes(n):
    R, H = 2 * n, 12 * n
    return [(j, k) for j in range(H + 1) for k in range(j % 2, R + 1, 2)]


def order_profile(n, D, seeds):
    R, H = 2 * n, 12 * n
    field = [[0] * (R + 1) for _ in range(H + 1)]
    for j, k in legal_nodes(n):
        field[j][k] = max((v for t, r, v in seeds
                           if r + abs(j - t) <= k), default=0)
    validate_profile(n, D, field)
    return field


def validate_profile(n, D, field):
    nodes = legal_nodes(n)
    for j, k in nodes:
        a = field[j][k]
        require(0 <= a <= D and (k or a == 0), "profile range/center")
        for t, r in nodes:
            if k + abs(j - t) <= r:
                require(a <= field[t][r], "global radial interval order")


def binary_input(path, n, D, field):
    with path.open("wb") as f:
        f.write(struct.pack("<IIQ", 1, n, D))
        for row in field:
            f.write(struct.pack("<" + "Q" * len(row), *row))


def fraction_reference(n, D, field):
    R, C, H = 2 * n, 4 * n, 12 * n
    best = None
    stats = {"normalized_paths": 0, "late_center_rejected": 0,
             "endpoint_start_paths": 0, "tail_record_decreases": 0,
             "prefix_edges": 0, "tail_edges": 0}

    def price(j, k):
        return Q(D + (field[j][abs(k)] if k > 0 else -field[j][abs(k)]), 2 * D)

    def step(state, direction, tail):
        j, k, left, right, lm, rm, cost, centered, start_endpoint = state
        require(abs(k + direction) <= R and j < H, "physical step")
        if not left:
            new = price(j, k)
            if tail and lm is not None and new < lm:
                stats["tail_record_decreases"] += 1
            lm = new if lm is None else min(lm, new)
            cost += lm * Q(1, 2 * n)
        if not right:
            new = price(j, -k)
            if tail and rm is not None and new < rm:
                stats["tail_record_decreases"] += 1
            rm = new if rm is None else min(rm, new)
            cost += rm * Q(1, 2 * n)
        k += direction
        j += 1
        centered = centered or (k == 0 and j <= C)
        stats["tail_edges" if tail else "prefix_edges"] += 1
        return j, k, left or k == -R, right or k == R, lm, rm, cost, centered, start_endpoint

    def walk(state, target):
        direction = 1 if target > state[1] else -1
        while state[1] != target:
            state = step(state, direction, True)
        return state

    def accept(state):
        nonlocal best
        j, k, left, right, lm, rm, cost, centered, start_endpoint = state
        require(left and right and j <= H, "completed normalized tour")
        if not centered:
            stats["late_center_rejected"] += 1
            return
        stats["normalized_paths"] += 1
        stats["endpoint_start_paths"] += start_endpoint
        best = cost if best is None else min(best, cost)

    def visit(state):
        j, k, left, right, lm, rm, cost, centered, start_endpoint = state
        if left or right:
            accept(walk(state, R if left else -R))
        elif j == C:
            if not centered:
                stats["late_center_rejected"] += 1
                return
            for first in (-R, R):
                accept(walk(walk(state, first), -first))
        else:
            # Deliberately enumerate prefixes even after a future center
            # deadline has become impossible. Only completed leaves reject.
            visit(step(state, -1, False))
            visit(step(state, 1, False))

    for k in range(-R, R + 1, 2):
        visit((0, k, k == -R, k == R, None, None, Q(0), k == 0, abs(k) == R))
    require(best is not None, "nonempty normalized bank")
    units = best * (4 * n * D)
    require(units.denominator == 1, "atomic cost scale")
    stats["minimum_units"] = units.numerator
    stats["minimum"] = str(best)
    return stats


def replay_route(n, D, field, route):
    R, C, H = 2 * n, 4 * n, 12 * n
    k, j = route["start_grid"], 0
    require(-R <= k <= R and k % 2 == 0, "legal route start")
    left, right, centered = k == -R, k == R, k == 0
    lm = rm = None
    cost = Q(0)
    first_endpoint = 0 if left or right else None
    positions = [k]
    for direction in route["moves"]:
        require(direction in (-1, 1) and not (left and right), "legal active route move")
        if not left:
            value = Q(D + (field[j][abs(k)] if k > 0 else -field[j][abs(k)]), 2 * D)
            lm = value if lm is None else min(lm, value)
            cost += lm * Q(1, 2 * n)
        if not right:
            value = Q(D + (field[j][abs(k)] if k < 0 else -field[j][abs(k)]), 2 * D)
            rm = value if rm is None else min(rm, value)
            cost += rm * Q(1, 2 * n)
        k += direction
        j += 1
        require(abs(k) <= R and j <= H, "route arena/horizon")
        positions.append(k)
        centered = centered or (k == 0 and j <= C)
        left, right = left or k == -R, right or k == R
        if first_endpoint is None and abs(k) == R:
            first_endpoint = j
    require(left and right and centered, "route completes and meets center deadline")
    require(first_endpoint is not None, "route first endpoint")
    tail = route["moves"][first_endpoint:]
    require(not tail or len(set(tail)) == 1, "opposite sweep after first endpoint")
    if first_endpoint > C:
        before = route["moves"][C:first_endpoint]
        require(not before or len(set(before)) == 1, "straight first leg of time-2 tour")
    require(cost * (4 * n * D) == int(route["units"]), "exact emitted route price")
    return str(cost)


def independent_record_dp(n, D, field):
    """No Pareto dominance: merge only exactly identical surviving records."""
    R, C = 2 * n, 4 * n
    states = {(k, 2 * D, 2 * D, k == 0): 0 for k in range(-R, R + 1, 2)}
    best, total_states, maximum_layer = None, 0, 0

    def charge(j, k):
        return D + (field[j][abs(k)] if k > 0 else -field[j][abs(k)])

    def tail(j, k, lm, rm, centered, first):
        left, right = k == -R, k == R
        cost = 0
        targets = [R] if left else [-R] if right else [first, -first]
        for target in targets:
            direction = 1 if target > k else -1
            while k != target:
                if not left:
                    lm = min(lm, charge(j, k))
                    cost += lm
                if not right:
                    rm = min(rm, charge(j, -k))
                    cost += rm
                k += direction
                j += 1
                centered = centered or (k == 0 and j <= C)
                left, right = left or k == -R, right or k == R
        return cost if centered else None

    for j in range(C + 1):
        total_states += len(states)
        maximum_layer = max(maximum_layer, len(states))
        nxt = {}
        for (k, lm, rm, centered), cost in states.items():
            if abs(k) == R or j == C:
                for first in (-R, R) if abs(k) != R else (0,):
                    extra = tail(j, k, lm, rm, centered, first)
                    if extra is not None:
                        value = cost + extra
                        best = value if best is None else min(best, value)
                continue
            lm, rm = min(lm, charge(j, k)), min(rm, charge(j, -k))
            newcost = cost + lm + rm
            for direction in (-1, 1):
                x = k + direction
                key = (x, lm, rm, centered or x == 0)
                if key not in nxt or newcost < nxt[key]:
                    nxt[key] = newcost
        states = nxt
    return {"minimum_units": best, "states": total_states, "maximum_layer": maximum_layer}


def certificate_profile(path):
    certificate = json.loads(path.read_text())
    n, source_D = certificate["n"], int(certificate["discount_denominator"])
    D = source_D if source_D <= 10 ** 12 else 10 ** 9 + 7
    seeds = []
    for j, k, discount in certificate["discounts"]:
        if k > 0:
            source_value = max(0, min(source_D, source_D - int(discount)))
            seeds.append((j, k, source_value * D // source_D))
    field = order_profile(n, D, seeds)
    return n, D, field, certificate["exact_value"], D == source_D


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--source", type=Path,
                        default=Path(__file__).with_name("price_normalized.cpp"))
    parser.add_argument("--output", type=Path,
                        default=Path(__file__).with_name("native_oracle_replay.json"))
    parser.add_argument("--compiler", default="g++")
    args = parser.parse_args()
    source_bytes = args.source.read_bytes()
    report = {
        "scope": "Exact regression of normalized-bank integer pricing; the bank-normalization theorem is separate.",
        "source_sha256": hashlib.sha256(source_bytes).hexdigest(),
        "small_fixtures": [], "known_certificates": [], "rejections": [],
    }
    rng = random.Random(602713)
    with tempfile.TemporaryDirectory(prefix="normalized-oracle-regression-") as tmp:
        directory = Path(tmp)
        snapshot = directory / "price_normalized.cpp"
        snapshot.write_bytes(source_bytes)
        executable = directory / "price_normalized"
        build = subprocess.run([args.compiler, "-std=c++17", "-O2", "-Wall", "-Wextra",
                                str(snapshot), "-o", str(executable)],
                               text=True, capture_output=True, timeout=120)
        require(build.returncode == 0, "native compilation\n" + build.stderr)
        report["compiler_diagnostics"] = build.stderr

        def run_case(name, n, D, field, reference):
            input_path = directory / (name + ".bin")
            binary_input(input_path, n, D, field)
            got = subprocess.run([str(executable), str(input_path), "17"],
                                 text=True, capture_output=True, timeout=60)
            require(got.returncode == 0, name + ": native failure " + got.stderr)
            output = json.loads(got.stdout)
            require(int(output["minimum_units"]) == reference["minimum_units"],
                    "{}: native {} != independent {}".format(
                        name, output["minimum_units"], reference["minimum_units"]))
            require(int(output["objective_denominator"]) == 4 * n * D,
                    name + ": objective normalization")
            route_values = [replay_route(n, D, field, route) for route in output["paths"]]
            require(route_values and min(map(Q, route_values)) ==
                    Q(reference["minimum_units"], 4 * n * D), name + ": minimum route replay")
            value_only_checked = name in {"random_n1_0", "random_n2_11", "qout_n2_7", "known_n6"}
            if value_only_checked:
                value_run = subprocess.run([str(executable), str(input_path), "0"],
                                           text=True, capture_output=True, timeout=60)
                require(value_run.returncode == 0, name + ": value-only mode failed")
                value_output = json.loads(value_run.stdout)
                require(value_output["paths"] == [], name + ": value-only mode kept routes")
                require(int(value_output["minimum_units"]) == reference["minimum_units"],
                        name + ": value-only minimum differs")
            return {"name": name, "n": n, "D": str(D), "reference": reference,
                    "routes_replayed": len(route_values),
                    "value_only_checked": value_only_checked,
                    "native": {key: output[key] for key in (
                        "minimum_units", "retained_states", "generated_transitions",
                        "dominance_pruned", "maximum_layer", "terminal_tours",
                        "independent_pursuit_pruned", "late_center_pruned")}}

        for n in (1, 2):
            for trial in range(28):
                D = (1, 17, 101, 10 ** 12)[trial % 4]
                nodes = [(j, k) for j, k in legal_nodes(n) if k]
                if trial == 0:
                    seeds = []
                elif trial == 1:
                    seeds = [(j, k, D) for j, k in nodes]
                else:
                    seeds = [(j, k, rng.randrange(D + 1))
                             for j, k in rng.sample(nodes, min(len(nodes), 6 + trial))]
                field = order_profile(n, D, seeds)
                reference = fraction_reference(n, D, field)
                dp = independent_record_dp(n, D, field)
                require(dp["minimum_units"] == reference["minimum_units"],
                        "independent DP agrees with exhaustive Fraction search")
                item = run_case("random_n{}_{}".format(n, trial), n, D, field, reference)
                report["small_fixtures"].append(item)
        # Independently construct sticky/outward2 fields so the stronger
        # pursuit-prefix plus weighted time2-tail bound is exercised.
        for n in (1,2):
            R,C,H=2*n,4*n,12*n
            nodes=[(j,k) for j,k in legal_nodes(n) if k and j<=C]
            for trial in range(8):
                D=101
                seeds=[(j,k,rng.randrange(D+1)) for j,k in rng.sample(nodes,min(7+trial,len(nodes)))]
                field=order_profile(n,D,seeds)
                for j in range(C-2,-1,-2):
                    field[j][R]=max(field[j][R],field[j+2][R])
                for j in range(C+1,H+1):
                    for k in range(j%2,R+1,2):
                        foot=k-j+C
                        field[j][k]=0 if foot<=0 else field[C][foot]
                validate_profile(n,D,field)
                reference=fraction_reference(n,D,field)
                dp=independent_record_dp(n,D,field)
                require(dp['minimum_units']==reference['minimum_units'],
                        'independent outward2 references disagree')
                item=run_case('qout_n{}_{}'.format(n,trial),n,D,field,reference)
                report['small_fixtures'].append(item)
        require(sum(x["reference"]["late_center_rejected"] for x in report["small_fixtures"]) > 0,
                "late-center rejection not exercised")
        require(sum(x["reference"]["tail_record_decreases"] for x in report["small_fixtures"]) > 0,
                "tail record changes not exercised")
        for path in sorted(args.source.parent.parent.glob("grid_n*_certificate.json")):
            n, D, field, value, unquantized = certificate_profile(path)
            reference = independent_record_dp(n, D, field)
            item = run_case("known_n{}".format(n), n, D, field, reference)
            priced = Q(reference["minimum_units"], 4 * n * D)
            if unquantized:
                require(priced == Q(value), "known exact atomic certificate value")
            else:
                require(abs(priced - Q(value)) <= Q(6, D),
                        "known quantized profile exceeds conservative total price error")
            item.update({"certificate": path.name, "certificate_value": value,
                         "unquantized": unquantized,
                         "priced_value": str(priced),
                         "difference_from_certificate": str(priced - Q(value))})
            report["known_certificates"].append(item)
        n, D = 2, 17
        field = order_profile(n, D, [])
        for name, mutate in (
            ("invalid_center", lambda f: f[0].__setitem__(0, 1)),
            ("invalid_range", lambda f: f[0].__setitem__(2, D + 1)),
            ("invalid_order", lambda f: f[2].__setitem__(2, D)),
        ):
            bad = [row[:] for row in field]
            mutate(bad)
            path = directory / (name + ".bin")
            binary_input(path, n, D, bad)
            result = subprocess.run([str(executable), str(path)], text=True,
                                    capture_output=True, timeout=10)
            require(result.returncode != 0 and not result.stdout,
                    name + ": invalid profile accepted")
            report["rejections"].append({"name": name, "message": result.stderr.strip()})
    report["status"] = "passed"
    report["total_exhaustive_paths"] = sum(
        item["reference"]["normalized_paths"] for item in report["small_fixtures"])
    report["total_routes_replayed"] = sum(
        item["routes_replayed"] for item in report["small_fixtures"] + report["known_certificates"])
    args.output.write_text(json.dumps(report, indent=2, sort_keys=True) + "\n")
    print(json.dumps({key: report[key] for key in (
        "status", "total_exhaustive_paths", "total_routes_replayed")}))
    print(json.dumps({"known_values": [
        {"n": x["n"], "priced_value": x["priced_value"],
         "certificate_value": x["certificate_value"], "unquantized": x["unquantized"]}
        for x in report["known_certificates"]]}, indent=2))


if __name__ == "__main__":
    main()

