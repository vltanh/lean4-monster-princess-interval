#!/usr/bin/env python3
"""Exact checks of the turn-sheet payoff identities and global envelope.

Uses rational constant-f sheets, for which the continuous turn integral
is polynomial and exact. This checks the capture-derived integrand
independently of the flatness differential equation. The accompanying
proof supplies the exhaustive arbitrary-path reduction.
"""

from fractions import Fraction as Q


def primitive_s2(s, z, u):
    # Integral of 2s+6-z-u with respect to the turn characteristic s.
    return s*s+(6-z-u)*s


def direct_sheet_capture_gain(z, u, v, density):
    """Four times pair gain, from literal early/late first captures.

    Relative to late capture s+3, the unreflected early capture is
    (z+u)/2. The reflected capture is unchanged. Integrate in s exactly.
    """
    lower = max(Q(1), u)
    if lower >= v:
        return Q(0)
    # Twice the unreflected capture difference is z+u-2s-6.
    return -density*(primitive_s2(v,z,u)-primitive_s2(lower,z,u))


def gain(a, z, u, v, f, ell):
    density = (f-ell)/(v+6-z)
    positive_m1_gain = f*max(Q(0), 2-a-u)
    negative_m1_gain = -ell*(z+2-u)
    return (positive_m1_gain+negative_m1_gain
            +direct_sheet_capture_gain(z,u,v,density))


def check_one(a, z, v, f, ell):
    assert 0 <= a <= 1 and 0 <= z <= 1
    assert 1 <= v <= 2 and 0 <= ell <= f
    density = (f-ell)/(v+6-z)
    H = density*(v-1)
    M = density*(v-1)**2/2
    gamma = f*(2-v)-ell*(z+2-v)
    price = (1+z)*ell+(7-z)*H+2*M
    assert price == f-gamma
    upper = max(gamma-f*a, Q(0))

    # Cover the relevant interval endpoints and all smooth pieces,
    # including a cutoff L that can fall strictly inside the corridor.
    cuts = sorted(set([Q(1), v, 2-a, z+2]))
    cuts = [u for u in cuts if 1 <= u <= z+2]
    probes = set(cuts)
    for lo, hi in zip(cuts, cuts[1:]):
        probes.update([lo+(hi-lo)*Q(j,7) for j in range(1,7)])
    count = 0
    for u in probes:
        value = gain(a,z,u,v,f,ell)
        assert value <= upper, (a,z,u,v,f,ell,value,upper)
        if u <= min(v,2-a):
            assert value == gamma-f*a
        if u >= 2-a:
            assert value <= 0
        count += 1

    # The global supremum is reached by either an interior corridor
    # inverse or the endpoint inverse; no numerical maximizer is used.
    assert max(gain(a,z,Q(1),v,f,ell),
               gain(a,z,z+2,v,f,ell)) == upper
    return count


def step_integral(knots, heights, lo, hi):
    return sum((max(Q(0),min(hi,b)-max(lo,a))*height
                for a,b,height in zip(knots,knots[1:],heights)),Q(0))


def step_value(knots, heights, x):
    for a,b,height in zip(knots,knots[1:],heights):
        if a <= x < b:
            return height
    assert x == 1
    return heights[-1]


def check_step(a, z, v, knots, heights, ell):
    """Compare finite jump moments with direct piecewise capture integrals."""
    p=step_value(knots,heights,2-v)-ell
    assert p>=0
    jumps=[(2-x,hi-lo) for x,lo,hi in zip(knots[1:-1],heights,heights[1:])
           if 2-x < v]
    H=(v-1)*p/(v+6-z)+sum((d*(r-1)/(r+6-z) for r,d in jumps),Q(0))
    M=(v-1)**2*p/(2*(v+6-z))+sum(
        (d*(r-1)**2/(2*(r+6-z)) for r,d in jumps),Q(0))
    turn_cuts=sorted(set([Q(1),v]+[r for r,d in jumps]))
    pieces=[]
    for lo,hi in zip(turn_cuts,turn_cuts[1:]):
        mid=(lo+hi)/2
        density=p/(v+6-z)+sum((d/(r+6-z) for r,d in jumps if mid<r),Q(0))
        pieces.append((lo,hi,density))
    assert H==sum(((hi-lo)*d for lo,hi,d in pieces),Q(0))
    assert M==sum((((hi-1)**2-(lo-1)**2)*d/2 for lo,hi,d in pieces),Q(0))
    F1=step_integral(knots,heights,Q(0),Q(1))
    Fa=step_integral(knots,heights,Q(0),a)
    gamma=step_integral(knots,heights,Q(0),2-v)-ell*(z+2-v)
    assert (1+z)*ell+(7-z)*H+2*M==F1-gamma
    upper=max(gamma-Fa,Q(0))
    probes=sorted(set([Q(1),v,2-a,z+2]+[2-x for x in knots]))
    probes=[u for u in probes if 1<=u<=z+2]
    probes=sorted(set(probes+[(lo+hi)/2 for lo,hi in zip(probes,probes[1:])]))
    for u in probes:
        capture_gain=Q(0)
        for lo,hi,density in pieces:
            lower=max(lo,u)
            if lower<hi:
                capture_gain-=density*(primitive_s2(hi,z,u)-primitive_s2(lower,z,u))
        R=step_integral(knots,heights,a,max(a,2-u))
        value=R-ell*(z+2-u)+capture_gain
        assert value<=upper,(a,z,v,u,value,upper)
        if u<=min(v,2-a):
            assert value==gamma-Fa,(a,z,v,u,value,gamma-Fa)
    return len(probes)


def main():
    count = 0
    for den in [5,8,11]:
        for ai in range(den+1):
            a=Q(ai,den)
            for zi in range(den+1):
                z=Q(zi,den)
                for v in [Q(1),Q(9,8),Q(3,2),Q(2),1+z/4]:
                    for f,ell in [(Q(1),Q(0)),(Q(1),Q(1,4)),
                                  (Q(2,3),Q(2,3)),(Q(7,5),Q(2,5))]:
                        count += check_one(a,z,v,f,ell)

    # Independent exact moment arithmetic for the explicit example.
    for zi in range(33):
        z=Q(zi,32)
        density=3/(28-3*z)
        width=z/4
        H=density*width
        M=density*width*width/2
        assert H == 3*z/(4*(28-3*z))
        assert M == 3*z*z/(32*(28-3*z))
        assert (1+z)/4+(7-z)*H+2*M == Q(1,4)+7*z/16

    step_count=0
    knots=[Q(0),Q(1,4),Q(1,2),Q(3,4),Q(7,8),Q(1)]
    heights=[Q(1,5),Q(2,5),Q(3,5),Q(4,5),Q(7,5)]
    for ai in range(9):
        for zi in range(9):
            for v in [Q(1),Q(9,8),Q(5,4),Q(4,3),Q(3,2),Q(7,4),Q(2)]:
                for ell in [Q(0),Q(1,10),Q(1,5)]:
                    step_count+=check_step(Q(ai,8),Q(zi,8),v,knots,heights,ell)

    print(f"PASS: {count} exact capture-integral/envelope checks")
    print("PASS: 33 exact sheet moment and effective-price checks")
    print(f"PASS: {step_count} exact step-density capture/moment/envelope checks")
    print("Scope: global upper response theorem in UPPER_EQUALITY_CORRIDOR.md;")
    print("no assertion of a matching lower law or an equilibrium value.")


if __name__ == "__main__":
    main()
