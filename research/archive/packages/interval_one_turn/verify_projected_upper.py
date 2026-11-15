#!/usr/bin/env python3
"""Independently replay an exact projected one-turn Monster upper certificate.

Only the Python standard library is used.  The physical rational paths and
integer probabilities determine the geometry, threshold bounds, reward
clauses, and capacities.  Supplied geometry/defs/units/labels and floating-point
scores are not used.  Projected old_nodes select threshold indices; every
supplied threshold edge must be a sound order implication.  Missing edges
only weaken the resulting upper bound.

The mathematical basis is the finite-event radial inverse-curve upper
theorem.  A formal optimal-label row is not an actual finite-epsilon Princess
witness and is not needed by this verifier.

Usage:
  python3 packages/interval_one_turn/verify_projected_upper.py result.json
  python3 packages/interval_one_turn/verify_projected_upper.py --self-test
"""
from __future__ import annotations

import argparse
from bisect import bisect_left
from dataclasses import dataclass
from fractions import Fraction
import gzip
import hashlib
import json
from math import isfinite, lcm
from pathlib import Path


FROZEN_BENCHMARK = Fraction(291849329389899, 204800000000000)


class VerificationError(ValueError):
    pass


def require(condition, message):
    if not condition:
        raise VerificationError(message)


def integer(value, what):
    require(not isinstance(value, bool), f"{what}: Boolean is not an integer")
    if isinstance(value, int):
        return value
    require(isinstance(value, str), f"{what}: expected an integer or integer string")
    try:
        result = int(value)
    except ValueError as exc:
        raise VerificationError(f"{what}: malformed integer") from exc
    require(str(result) == value or value == "+"+str(result),
            f"{what}: noncanonical integer string")
    return result


def rational(value, what):
    require(not isinstance(value, bool), f"{what}: Boolean is not rational data")
    require(isinstance(value, (int, float, str)), f"{what}: malformed rational")
    if isinstance(value, float):
        require(isfinite(value), f"{what}: nonfinite coordinate")
    try:
        return Fraction(value)
    except (ValueError, ZeroDivisionError) as exc:
        raise VerificationError(f"{what}: malformed rational") from exc


@dataclass
class Geometry:
    scale: int
    denominator: int
    weights: list[int]
    routes: list[list[list[tuple[int, int]]]]
    queries: list[int]
    bases: list[int]
    bounds: list[tuple[int, int]]
    offsets: list[int]
    node_query: list[int]
    node_threshold: list[int]
    physical_report: dict

    def ge(self, value):
        i = bisect_left(self.bases, value)
        return 3*i + int(i < len(self.bases) and self.bases[i] == value)

    def gt(self, value):
        i = bisect_left(self.bases, value)
        return 3*i + 2*int(i < len(self.bases) and self.bases[i] == value)

    def node(self, row, threshold):
        lo, hi = self.bounds[row]
        require(lo < threshold <= hi, "internal unforced-node error")
        return self.offsets[row]+threshold-lo-1


def reconstruct_geometry(atoms, denominator):
    """Validate every route, then construct all coordinates independently.

    After a completed direct endpoint-to-opposite-endpoint sweep, every legal
    Princess has already been captured.  Any later supplied unit-speed arena
    continuation is explicitly ignored for B1 membership, but retained when
    reconstructing the supplied response graph.  Its capture payoff equals
    that of the canonical prefix stopped at the second endpoint.
    """
    require(isinstance(atoms, list) and atoms, "empty or malformed physical law")
    require(denominator > 0, "probability denominator must be positive")
    rational_routes, weights = [], []
    scale = 1
    classes = {"endpoint_start": 0, "interior_endpoint_first": 0,
               "one_interior_reversal": 0}
    class_mass = dict.fromkeys(classes, 0)
    max_completion = Fraction(0)
    truncated_rows = truncated_legs = 0
    for atom_index, atom in enumerate(atoms):
        require(isinstance(atom, dict), "malformed physical atom")
        weight = integer(atom.get("weight_numerator"), f"weight {atom_index}")
        require(weight >= 0, "negative probability weight")
        weights.append(weight)
        supplied = atom.get("exact_light")
        require(isinstance(supplied, list) and len(supplied) >= 2,
                "a physical route needs at least two vertices")
        route = []
        directions = []
        for vertex_index, pair in enumerate(supplied):
            require(isinstance(pair, list) and len(pair) == 2,
                    "malformed light-coordinate vertex")
            u, v = (rational(x, f"atom {atom_index}, vertex {vertex_index}")
                    for x in pair)
            require(u+v >= 0 and abs(u-v) <= 2,
                    "Monster vertex is outside the physical arena/time domain")
            if route:
                du, dv = u-route[-1][0], v-route[-1][1]
                require((du > 0 and dv == 0) or (dv > 0 and du == 0),
                        "Monster leg is not a positive-duration unit-speed light leg")
                directions.append(1 if du > 0 else -1)
            route.append((u, v))
            scale = lcm(scale, u.denominator, v.denominator)
        require(sum(route[0]) == 0, "Monster does not start at time zero")
        endpoints = [(i, 1 if u-v == 2 else -1)
                     for i, (u, v) in enumerate(route) if abs(u-v) == 2]
        require(endpoints, "Monster never visits an endpoint")
        first, first_sign = endpoints[0]
        second = next((i for i, sign in endpoints if sign == -first_sign), None)
        require(second is not None, "Monster does not visit both endpoints")
        turns = sum(directions[i-1] != directions[i] for i in range(1, first))
        require(turns <= 1, "Monster has more than one interior reversal before its first endpoint")
        require(all(direction == -first_sign for direction in directions[first:second]),
                "Monster does not sweep directly to the opposite endpoint")
        first_time = sum(route[first])/2
        completion = sum(route[second])/2
        require(completion-first_time == 2,
                "opposite endpoint sweep has incorrect duration")
        require(completion <= 6, "canonical B1 completion exceeds six")
        max_completion = max(max_completion, completion)
        if second < len(route)-1:
            truncated_rows += 1
            truncated_legs += len(route)-1-second
        kind = ("endpoint_start" if first == 0 else
                "one_interior_reversal" if turns else "interior_endpoint_first")
        classes[kind] += 1
        class_mass[kind] += weight
        rational_routes.append(route)
    require(sum(weights) == denominator, "probability weights do not sum to denominator")

    routes, query_set, base_set = [], {-scale}, {0}
    for route in rational_routes:
        integer_route = [(int(u*scale), int(v*scale)) for u, v in route]
        pair = [integer_route, [(v, u) for u, v in integer_route]]
        routes.append(pair)
        for oriented in pair:
            for u, v in oriented:
                query_set.add(v)
                if u >= 0:
                    base_set.add(u)
    queries = sorted(query_set)
    require(queries[0] == -scale, "invalid first virtual radial query")
    for v in queries:
        base_set.update((max(v, 0), v+2*scale))
    bases = sorted(base_set)

    def ge(value):
        i = bisect_left(bases, value)
        return 3*i+int(i < len(bases) and bases[i] == value)

    bounds = [(ge(max(v, 0)), ge(v+2*scale)) for v in queries]
    bounds[0] = (ge(0), ge(0))
    last = ge(queries[-1]+2*scale)
    bounds[-1] = (last, last)
    offsets, node_query, node_threshold = [], [], []
    for row, (lo, hi) in enumerate(bounds):
        require(lo <= hi, "empty physical threshold interval")
        offsets.append(len(node_query))
        node_query.extend([row]*(hi-lo))
        node_threshold.extend(range(lo+1, hi+1))
    return Geometry(
        scale, denominator, weights, routes, queries, bases, bounds, offsets,
        node_query, node_threshold,
        {"reflected_pairs": len(atoms), "positive_weight_pairs": sum(w > 0 for w in weights),
         "class_counts": classes,
         "class_probability": {k: str(Fraction(w, denominator)) for k, w in class_mass.items()},
         "maximum_canonical_completion": str(max_completion),
         "rows_with_irrelevant_postcapture_continuation": truncated_rows,
         "irrelevant_postcapture_legs": truncated_legs})


def reconstruct_rewards(geometry):
    """Compile exact survival lengths, in integer light-coordinate units.

    A positive clause requires all its ordered thresholds to be true.  A
    negative clause requires all of them to be false.  The two orientations
    and dt=d(light)/2 account for the final factor four, outside this compiler.
    """
    g = geometry
    query_index = {v: i for i, v in enumerate(g.queries)}
    definitions, rewards, ids = [], [], {}

    def normalize(positive, literals):
        by_row = {}
        for row, threshold in literals:
            lo, hi = g.bounds[row]
            if positive:
                if threshold <= lo:
                    continue
                if threshold > hi:
                    return None
                by_row[row] = max(threshold, by_row.get(row, threshold))
            else:
                if threshold <= lo:
                    return None
                if threshold > hi:
                    continue
                by_row[row] = min(threshold, by_row.get(row, threshold))
        ordered = sorted(by_row.items())
        retained = []
        if positive:
            high = -1
            for row, threshold in ordered:
                if threshold > high:
                    retained.append(g.node(row, threshold))
                    high = threshold
        else:
            low = 3*len(g.bases)+1
            for row, threshold in reversed(ordered):
                if threshold < low:
                    retained.append(g.node(row, threshold))
                    low = threshold
            retained.reverse()
        return tuple(retained)

    def add(positive, literals, length, weight):
        require(length >= 0, "negative physical survival length")
        if length == 0:
            return
        bits = normalize(positive, literals)
        if bits is None:
            return
        key = (positive, bits)
        index = ids.get(key)
        if index is None:
            index = len(definitions)
            ids[key] = index
            definitions.append(key)
            rewards.append(0)
        rewards[index] += weight*length

    for weight, pair in zip(g.weights, g.routes):
        for route in pair:
            u0, v0 = route[0]
            above = [(query_index[v0], g.gt(u0))]
            below = [(query_index[v0], g.ge(u0))]
            for u1, v1 in route[1:]:
                if u1 > u0:
                    row = query_index[v0]
                    old = max(0, min(g.bases[0], u1)-u0)
                    add(True, above, old, weight)
                    for level in range(1, len(g.bases)):
                        new = max(0, min(g.bases[level], u1)-u0)
                        if new > old:
                            add(True, above+[(row, 3*level)], new-old, weight)
                        old = new
                    add(False, below, u1-u0, weight)
                else:
                    add(True, above, v1-v0, weight)
                    left, right = query_index[v0], query_index[v1]
                    threshold = g.ge(u0)
                    for row in range(left, right):
                        length = max(0, min(g.queries[row+1], u0)-g.queries[row])
                        add(False, below+[(row, threshold)], length, weight)
                above.append((query_index[v1], g.gt(u1)))
                below.append((query_index[v1], g.ge(u1)))
                u0, v0 = u1, v1
    return definitions, rewards


def reconstruct_network(g, definitions, rewards, projection):
    require(isinstance(projection, dict), "missing threshold projection")
    selection = projection.get("projection")
    require(isinstance(selection, dict), "missing projected index selection")
    supplied = selection.get("old_nodes")
    require(isinstance(supplied, list), "malformed projected old_nodes")
    old_nodes = [integer(x, "projected old node") for x in supplied]
    require(len(set(old_nodes)) == len(old_nodes), "duplicate projected threshold node")
    require(all(0 <= node < len(g.node_query) for node in old_nodes),
            "projected threshold index outside independently reconstructed geometry")
    require(integer(projection.get("N"), "projected N") == len(old_nodes),
            "projected node count mismatch")
    index = {old: i for i, old in enumerate(old_nodes)}
    for _, bits in definitions:
        require(all(bit in index for bit in bits), "projection omitted a physical reward threshold")
    edges = projection.get("threshold_hard")
    require(isinstance(edges, list), "malformed projected threshold edges")
    hard = []
    for edge in edges:
        require(isinstance(edge, list) and len(edge) == 2, "malformed implication edge")
        source, target = (integer(x, "implication node") for x in edge)
        require(0 <= source < len(old_nodes) and 0 <= target < len(old_nodes)
                and source != target, "invalid projected implication node")
        u, v = old_nodes[source], old_nodes[target]
        require(g.node_query[u] <= g.node_query[v]
                and g.node_threshold[u] >= g.node_threshold[v],
                "unsound projected threshold implication")
        hard.append((source, target))
    linear = [0]*len(old_nodes)
    constant = 0
    for (positive, original_bits), reward in zip(definitions, rewards):
        require(reward >= 0, "negative aggregate reward")
        if reward == 0:
            continue
        bits = [index[old] for old in original_bits]
        if not bits:
            constant += reward
        elif len(bits) == 1:
            linear[bits[0]] += reward if positive else -reward
            if not positive:
                constant += reward
        else:
            auxiliary = len(linear)
            linear.append(reward if positive else -reward)
            if not positive:
                constant += reward
            hard.extend((auxiliary, bit) if positive else (bit, auxiliary) for bit in bits)
    source, sink = len(linear), len(linear)+1
    positive = sum(value for value in linear if value > 0)
    infinite = 1+sum(abs(value) for value in linear)
    return {"linear": linear, "hard": hard, "constant": constant,
            "positive": positive, "infinite": infinite, "source": source, "sink": sink,
            "projected_nodes": len(old_nodes), "threshold_edges": len(edges)}


def expected_arcs(network):
    source, sink = network["source"], network["sink"]
    for node, value in enumerate(network["linear"]):
        if value > 0:
            yield source, node, value
        elif value < 0:
            yield node, sink, -value
    for u, v in network["hard"]:
        yield u, v, network["infinite"]


def replay_flow(g, network, supplied_graph, supplied_flow):
    require(isinstance(supplied_graph, dict) and isinstance(supplied_flow, dict),
            "missing graph or flow certificate")
    source, sink = network["source"], network["sink"]
    nodes = sink+1
    for key, expected in (("nodes", nodes), ("source", source), ("sink", sink),
                          ("constant", network["constant"]), ("positive", network["positive"]),
                          ("scale", g.scale)):
        require(integer(supplied_graph.get(key), f"graph {key}") == expected,
                f"independently reconstructed graph {key} mismatch")
    arcs = supplied_graph.get("arcs")
    require(isinstance(arcs, list), "malformed supplied arc list")
    expected_count = sum(value != 0 for value in network["linear"])+len(network["hard"])
    require(len(arcs) == expected_count, "independently reconstructed arc count mismatch")
    declared_flow = integer(supplied_flow.get("value"), "flow value")
    require(0 <= declared_flow <= network["positive"], "invalid total flow value")
    flows = [None]*expected_count
    entries = supplied_flow.get("entries")
    require(isinstance(entries, list), "malformed positive flow entries")
    for entry in entries:
        require(isinstance(entry, list) and len(entry) == 2, "malformed positive flow entry")
        edge, amount = integer(entry[0], "flow arc index"), integer(entry[1], "arc flow")
        require(0 <= edge < expected_count and flows[edge] is None and amount > 0,
                "invalid, repeated, or nonpositive flow entry")
        flows[edge] = amount
    side = bytearray(nodes)
    source_side = supplied_flow.get("source_side")
    require(isinstance(source_side, list), "malformed cut side")
    for value in source_side:
        node = integer(value, "cut node")
        require(0 <= node < nodes and not side[node], "invalid or repeated cut node")
        side[node] = 1
    require(side[source] and not side[sink], "cut does not separate the terminals")
    balances = [0]*nodes
    cut = 0
    for edge_index, ((u, v, capacity), supplied) in enumerate(zip(expected_arcs(network), arcs)):
        require(isinstance(supplied, list) and len(supplied) == 3, "malformed supplied arc")
        actual = tuple(integer(value, "supplied arc field") for value in supplied)
        require(actual == (u, v, capacity),
                f"independent physical capacity/arc reconstruction mismatch at arc {edge_index}")
        amount = flows[edge_index] or 0
        require(amount <= capacity, "flow exceeds independently reconstructed capacity")
        balances[u] -= amount
        balances[v] += amount
        if side[u] and not side[v]:
            cut += capacity
    for node, balance in enumerate(balances):
        expected = -declared_flow if node == source else declared_flow if node == sink else 0
        require(balance == expected, f"integer flow conservation failure at node {node}")
    require(cut == declared_flow, "integer flow and cut capacity disagree")
    score = network["constant"]+network["positive"]-declared_flow
    upper = Fraction(score, 4*g.scale*g.denominator)
    return upper, {"nodes": nodes, "arcs": expected_count,
                   "positive_flow_entries": len(entries), "source_side_nodes": len(source_side),
                   "constant_units": str(network["constant"]),
                   "positive_units": str(network["positive"]),
                   "flow_equals_cut_units": str(declared_flow), "score_units": str(score)}


def verify_certificate(data, *, require_counterexample=False):
    require(isinstance(data, dict), "certificate must be an object")
    denominator = integer(data.get("weights_denominator"), "probability denominator")
    geometry = reconstruct_geometry(data.get("atoms"), denominator)
    definitions, rewards = reconstruct_rewards(geometry)
    network = reconstruct_network(geometry, definitions, rewards, data.get("projection"))
    upper, flow_report = replay_flow(geometry, network, data.get("graph"), data.get("flow"))
    require(upper == rational(data.get("exact_value"), "claimed exact upper"),
            "claimed exact upper differs from independently reconstructed certificate")
    gap = upper-FROZEN_BENCHMARK
    if require_counterexample:
        require(gap <= 0,
                f"counterexample gate rejected: exact upper {upper} exceeds "
                f"frozen benchmark {FROZEN_BENCHMARK} by exactly {gap}")
    return {
        "status": "PASS",
        "scope": "all-Princess upper for the supplied fair-reflected canonical B1 Monster law",
        "exact_upper": str(upper), "upper_decimal": float(upper),
        "frozen_benchmark": str(FROZEN_BENCHMARK),
        "exact_upper_minus_frozen_benchmark": str(gap),
        "upper_at_most_frozen_benchmark": gap <= 0,
        "counterexample_gate_required": require_counterexample,
        "weights_denominator": str(denominator), "coordinate_scale": str(geometry.scale),
        "physical": geometry.physical_report,
        "reconstructed": {
            "query_rows": len(geometry.queries), "base_levels": len(geometry.bases),
            "full_threshold_nodes": len(geometry.node_query), "reward_clauses": len(definitions),
            "projected_threshold_nodes": network["projected_nodes"],
            "sound_supplied_threshold_edges": network["threshold_edges"],
            "auxiliary_nodes": len(network["linear"])-network["projected_nodes"],
        },
        "integer_certificate": flow_report,
        "supplied_geometry_defs_units_labels_and_float_scores_used": False,
        "projection_completeness_required": False,
        "formal_label_row_claimed_as_physical_witness": False,
    }


def self_test():
    # These small certificates were produced by the separate JavaScript
    # construction.  Their capacities and flow are fixed test data here.
    endpoint = json.loads('''{"exact_value":"3/2","weights_denominator":"1",
      "atoms":[{"weight_numerator":"1","exact_light":[["-1","1"],["3","1"]]}],
      "projection":{"N":1,"threshold_hard":[],"projection":{"old_nodes":[1]}},
      "graph":{"nodes":3,"arcs":[[1,0,"2"]],"source":1,"sink":2,
               "constant":"4","positive":"2","scale":"1"},
      "flow":{"value":"0","entries":[],"source_side":[0,1]}}''')
    turning = json.loads('''{"exact_value":"5/2","weights_denominator":"1",
      "atoms":[{"weight_numerator":"1","exact_light":[["-1/2","1/2"],
        ["1/2","1/2"],["1/2","5/2"],["9/2","5/2"]]}],
      "projection":{"N":7,"threshold_hard":[[1,0],[5,4],[4,3],[1,2],[3,2]],
        "projection":{"old_nodes":[2,3,9,10,13,16,19]}},
      "graph":{"nodes":13,"arcs":[[0,12,"2"],[11,1,"2"],[11,2,"8"],
        [11,7,"4"],[11,8,"1"],[11,9,"1"],[11,10,"2"],[1,0,"21"],
        [5,4,"21"],[4,3,"21"],[1,2,"21"],[3,2,"21"],[7,2,"21"],
        [7,6,"21"],[8,1,"21"],[8,3,"21"],[9,1,"21"],[9,4,"21"],
        [10,1,"21"],[10,5,"21"]],"source":11,"sink":12,
        "constant":"4","positive":"18","scale":"2"},
      "flow":{"value":"2","entries":[[0,"2"],[1,"2"],[7,"2"]],
        "source_side":[0,1,2,3,4,5,6,7,8,9,10,11]}}''')
    require(verify_certificate(endpoint)["exact_upper"] == "3/2", "endpoint test")
    require(verify_certificate(turning)["exact_upper"] == "5/2", "turning test")
    nondyadic = json.loads('''{"exact_value":"41/15","weights_denominator":"1",
      "atoms":[{"weight_numerator":"1","exact_light":[["1/3","-1/3"],
        ["11/15","-1/3"],["11/15","41/15"],["71/15","41/15"]]}],
      "projection":{"N":9,"threshold_hard":[[2,1],[1,0],[2,3],[7,6],[6,5],[5,4]],
        "projection":{"old_nodes":[2,4,6,14,25,28,31,34,37]}},
      "graph":{"nodes":13,"arcs":[[0,12,"16"],[11,1,"6"],[11,2,"76"],
        [11,4,"4"],[11,5,"10"],[11,6,"10"],[11,7,"6"],[9,12,"6"],
        [11,10,"30"],[2,1,"165"],[1,0,"165"],[2,3,"165"],[7,6,"165"],
        [6,5,"165"],[5,4,"165"],[0,9,"165"],[3,9,"165"],[10,2,"165"],
        [10,8,"165"]],"source":11,"sink":12,"constant":"44",
        "positive":"142","scale":"15"},
      "flow":{"value":"22","entries":[[0,"16"],[1,"6"],[2,"16"],
        [7,"6"],[9,"10"],[10,"16"],[11,"6"],[16,"6"]],
        "source_side":[0,1,2,3,4,5,6,7,8,9,10,11]}}''')
    require(verify_certificate(nondyadic)["exact_upper"] == "41/15",
            "nondyadic coordinates and negative-clause auxiliary test")
    clone = lambda value: json.loads(json.dumps(value))
    rejected = []

    def reject(name, mutate, fixture=turning):
        data = clone(fixture)
        mutate(data)
        try:
            verify_certificate(data)
        except VerificationError:
            rejected.append(name)
        else:
            raise VerificationError(f"corrupted certificate accepted: {name}")

    reject("negative weight", lambda d: d["atoms"][0].update(weight_numerator="-1"))
    reject("wrong mass", lambda d: d.update(weights_denominator="2"))
    reject("nonzero starting time", lambda d: d["atoms"][0]["exact_light"].__setitem__(0, ["0", "1/2"]))
    reject("nonunit leg", lambda d: d["atoms"][0]["exact_light"].__setitem__(1, ["1/2", "3/4"]))
    reject("missing second endpoint", lambda d: d["atoms"][0]["exact_light"].pop())
    reject("missing reward bit", lambda d: d["projection"]["projection"]["old_nodes"].__setitem__(0, 0))
    reject("duplicate projected node", lambda d: d["projection"]["projection"]["old_nodes"].__setitem__(0, 3))
    reject("unsound threshold edge", lambda d: d["projection"]["threshold_hard"].__setitem__(0, [0, 1]))
    reject("wrong physical capacity", lambda d: d["graph"]["arcs"][0].__setitem__(2, "3"))
    reject("flow exceeds capacity", lambda d: d["flow"]["entries"][0].__setitem__(1, "3"))
    reject("flow conservation", lambda d: d["flow"]["entries"].pop())
    reject("duplicate flow entry", lambda d: d["flow"]["entries"].append([0, "2"]))
    reject("wrong cut", lambda d: d["flow"]["source_side"].remove(0))
    reject("wrong exact value", lambda d: d.update(exact_value="2"))
    # Completeness of the supplied projection edges is intentionally not used.
    fewer = clone(turning)
    fewer["projection"]["threshold_hard"].pop(1)
    fewer["graph"]["arcs"].pop(8)  # no positive flow uses this removed edge
    require(verify_certificate(fewer)["exact_upper"] == "5/2", "missing sound edge test")
    ignored = clone(turning)
    ignored.update(geometry={"N": -100}, labels=["not a physical path"], value=-1000)
    ignored["projection"].update(defs=["untrusted"], units=["untrusted"])
    require(verify_certificate(ignored)["exact_upper"] == "5/2", "untrusted fields test")

    def light(vertices):
        return [[str(Fraction(t)+Fraction(x)), str(Fraction(t)-Fraction(x))] for t, x in vertices]

    bad_routes = [
        [(0, 0), ("1/2", "1/2"), ("3/2", "-1/2"),
         ("11/4", "3/4"), ("9/2", -1), ("13/2", 1)],
        [(0, 0), (1, 1), (2, 0), ("5/2", "1/2"), (4, -1)],
        [(0, -1), (1, 0), (2, -1), (4, 1)],
    ]
    for i, vertices in enumerate(bad_routes):
        reject(f"noncanonical topology {i}",
               lambda d, vertices=vertices: d["atoms"][0].update(exact_light=light(vertices)))
    extended = clone(endpoint)
    extended["atoms"][0]["exact_light"].append(["3", "5"])
    extended_report = verify_certificate(extended)
    physical = extended_report["physical"]
    require(physical["irrelevant_postcapture_legs"] == 1
            and physical["maximum_canonical_completion"] == "2",
            "postcapture continuation was not explicitly truncated")
    zero_weight = clone(endpoint)
    zero_weight["atoms"].append(clone(endpoint["atoms"][0]))
    zero_weight["atoms"][1]["weight_numerator"] = "0"
    require(verify_certificate(zero_weight)["exact_upper"] == "3/2", "zero weight test")
    try:
        verify_certificate(endpoint, require_counterexample=True)
    except VerificationError as exc:
        require("counterexample gate rejected" in str(exc), "wrong gate rejection")
    else:
        raise VerificationError("counterexample gate accepted an upper above the benchmark")
    return {"status": "PASS", "known_exact_uppers": ["3/2", "5/2", "41/15"],
            "corrupted_certificates_rejected": rejected,
            "missing_sound_projection_edge_accepted": True,
            "untrusted_geometry_defs_units_labels_ignored": True,
            "nondyadic_geometry_and_negative_auxiliary_checked": True,
            "zero_probability_atom_checked": True,
            "counterexample_gate_rejects_nonqualifying_upper": True,
            "irrelevant_continuation_explicitly_checked": True}


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("certificate", nargs="?", type=Path)
    parser.add_argument("--self-test", action="store_true")
    parser.add_argument("--require-counterexample", action="store_true",
                        help="reject unless the independently verified upper is at most the frozen U*")
    parser.add_argument("--output", type=Path)
    args = parser.parse_args()
    require(args.self_test or args.certificate is not None, "supply a certificate or --self-test")
    require(not (args.self_test and args.require_counterexample),
            "--require-counterexample requires an actual certificate, not --self-test")
    if args.self_test:
        report = self_test()
    else:
        raw = args.certificate.read_bytes()
        body = gzip.decompress(raw) if args.certificate.suffix == ".gz" else raw
        report = verify_certificate(json.loads(body), require_counterexample=args.require_counterexample)
        report["input_sha256"] = hashlib.sha256(raw).hexdigest()
    text = json.dumps(report, indent=2, sort_keys=True)+"\n"
    if args.output:
        args.output.write_text(text)
    print(text, end="")


if __name__ == "__main__":
    main()
