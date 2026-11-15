#!/usr/bin/env python3
"""Closed-form and rejection regressions for the independent exact replay."""

from contextlib import redirect_stdout
from fractions import Fraction as Q
import io

from replay_certificate import ExactMesh, ExactReplay


def fixture():
    mesh = ExactMesh(Q(1, 2), Q(3))
    queues = (Q(0), Q(1), Q(2), Q(4))
    potential = [
        2 - abs(mesh.vertices[v][1]) - (qp + qm) / 2
        for v in mesh.potential_vertices
        for qp in queues
        for qm in queues
    ]
    return {
        "step": "1/2",
        "mesh_kind": "light",
        "center_aligned": True,
        "queue_knots": list(map(str, queues)),
        "lower": "1",
        "coefficients": list(map(str, potential + [Q(1, 2)] * len(mesh.vertices) + [Q(1)])),
    }


def main():
    data = fixture()
    replay = ExactReplay(data)
    # A static fair endpoint Princess has exact security one. This potential
    # supplies its independent analytic fixture across all stopping faces.
    with redirect_stdout(io.StringIO()):
        result = replay.run()
    assert result["status"] == "PASS"

    integral_checks = 0
    for t in (Q(0), Q(3, 2), Q(3)):
        for x in (Q(-1), Q(-1, 2), Q(0), Q(1, 2), Q(1)):
            for q in (Q(0), Q(1, 4), Q(1, 2), Q(1), Q(2), Q(4)):
                length = max(Q(0), 1 + x - q)
                assert replay.tail(t + x, t + q) == length / 2
                integral_checks += 1

    # A stationary spatially uniform field is another independent closed
    # antiderivative fixture. It is deliberately not an absorbed-by3 law,
    # so only its integral routine, not the global certificate, is used.
    uniform = fixture()
    offset = len(replay.w)
    for i, (_, x) in enumerate(replay.mesh.vertices):
        uniform["coefficients"][offset + i] = str((1 + x) / 2)
    uniform_replay = ExactReplay(uniform)
    for t in (Q(0), Q(7, 4), Q(3)):
        for x in (Q(-1), Q(-2, 3), Q(0), Q(4, 5), Q(1)):
            for q in (Q(0), Q(1, 3), Q(3, 2), Q(4)):
                length = max(Q(0), 1 + x - q)
                assert uniform_replay.tail(t + x, t + q) == length * length / 4
                integral_checks += 1

    # A constant potential shift preserves every derivative inequality and
    # strengthens its initial lower bound, but violates the genuine endpoint
    # continuation. The independent boundary evaluator must reject it.
    corrupt = fixture()
    for i in range(len(replay.w)):
        corrupt["coefficients"][i] = str(Q(corrupt["coefficients"][i]) + Q(1, 100))
    corrupt_replay = ExactReplay(corrupt)
    corrupt_replay.field_and_controls()
    try:
        corrupt_replay.endpoint_guards()
    except AssertionError as error:
        assert error.args[0]["kind"] == "endpoint_boundary"
        assert Q(error.args[0]["margin"]) < 0
    else:
        raise AssertionError("The corrupted endpoint potential was accepted.")

    print("PASS: static-endpoint full certificate")
    print("PASS:", integral_checks, "exact closed-form tail integrals")
    print("PASS: derivative-preserving endpoint corruption rejected")


if __name__ == "__main__":
    main()
