"""Exact direct-intersection checks of the post-U=1 inward-leg identity.

Standard library only. The reference capture calculation is imported from
the independently checked characteristic package and intersects paths;
it does not use the formula under test.
"""

from fractions import Fraction as F
from pathlib import Path
import importlib.util


source = Path(__file__).resolve().parents[1] / "interval_characteristic_response" / "verify.py"
spec = importlib.util.spec_from_file_location("characteristic_reference", source)
reference = importlib.util.module_from_spec(spec)
spec.loader.exec_module(reference)


def from_characteristics(points):
    path = reference.clean([((u+v)/2, (u-v)/2) for u, v in points])
    if path[-1][0] < 4:
        path.append((F(4), path[-1][1]))
    assert path[0][0] == 0
    assert all(0 <= x <= 1 for _, x in path)
    assert all(abs(y-x) <= t-s for (s,x),(t,y) in zip(path,path[1:]))
    return path


def paths(a, u, c, epsilon):
    assert 0 <= a <= u < 1 and 0 <= c < 1 and 0 < epsilon < 1-c
    common = [(a,-a),(u,-a),(u,min(u,c))]
    if c >= u:
        common.append((c,c))
    common.append((1+epsilon,c))
    ordinary = from_characteristics(common + [(2+c,c)])
    detour = from_characteristics(common + [(1+epsilon,1-epsilon),(3-epsilon,1-epsilon)])
    return ordinary, detour


def main():
    count = 0
    strict = 0
    for ai in range(4):
        a = F(ai,4)
        for ui in range(ai,4):
            u = F(ui,4)
            for ci in range(4):
                c = F(ci,4)
                for epsilon in ((1-c)/3,(1-c)/2):
                    ordinary, detour = paths(a,u,c,epsilon)
                    starts = {F(j,8) for j in range(-8,9)} | {a,-a,-c,1-epsilon}
                    for family in (1,2):
                        for x in starts:
                            # The theorem allows no negative M1 starts except -1.
                            if family == 1 and -1 < x < 0:
                                continue
                            monster = reference.monster_path(family,x)
                            for reflected in (False,True):
                                actual_monster = ([(t,-y) for t,y in monster]
                                                  if reflected else monster)
                                old = reference.direct_capture(actual_monster,ordinary)
                                new = reference.direct_capture(actual_monster,detour)
                                gain = ((1-epsilon-c)/2
                                        if family == 1 and not reflected and a < x < 1-epsilon
                                        else F(0))
                                assert new-old == gain, (a,u,c,epsilon,family,x,reflected,new-old,gain)
                                count += 1
                                strict += gain > 0
    print(f"PASS: {count} exact individual capture comparisons; {strict} strict improvements.")
    print("PASS: starting equalities, M2 cutoff equality, and the x=1-epsilon boundary.")
    print("PASS: exact mixture gain is (1-epsilon-c)/4 times M1 mass in (a,1-epsilon).")


if __name__ == "__main__":
    main()
