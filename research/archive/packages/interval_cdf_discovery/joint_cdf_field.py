"""One fixed triangular CDF mesh and exact affine-record cost derivatives.

The nodal field is the continuous interior radial CDF trace.  Endpoint
contact uses its closed jump to one; center contact has strict trace zero.
This module does not assume ordinary prefix maps or any post-wave profile.
"""
from pathlib import Path
from dataclasses import dataclass
import json
from collections import deque
from math import lcm
import numpy as np


@dataclass(frozen=True)
class Form:
    constant: float
    terms: tuple

    def value(self, values):
        return self.constant + sum(weight*values[index] for index, weight in self.terms)

    def negative(self):
        return Form(-self.constant, tuple((i, -w) for i, w in self.terms))

    def add_gradient(self, gradient, scale):
        for index, weight in self.terms:
            gradient[index] += scale*weight


def combination(parts, constant=0.):
    terms = {}
    for scale, form in parts:
        constant += scale*form.constant
        for index, weight in form.terms:
            terms[index] = terms.get(index, 0.)+scale*weight
    return Form(constant, tuple((index, weight) for index, weight in terms.items() if abs(weight) > 1e-15))


class FieldMesh:
    def __init__(self, base=None):
        if base is None:
            base = sorted(set(np.linspace(0, 1, 17))
                          | {.45, .525, .55, .575}
                          | {1-2.**(-k) for k in range(5, 19)})
        self.base = np.asarray(base, float)
        self.ugrid = np.unique(np.r_[self.base, 2-self.base, 2+self.base])
        self.vgrid = np.unique(np.r_[-self.base, self.base])
        self.nodes = []
        self.index = {}
        for i, u in enumerate(self.ugrid):
            for j, v in enumerate(self.vgrid):
                if u+1e-12 >= abs(v) and u-v <= 2+1e-12 and v <= 1:
                    self.index[i, j] = len(self.nodes)
                    self.nodes.append((u, v))
        self.nodes = np.asarray(self.nodes)
        self.triangles = []
        self.cells = {}
        for i in range(len(self.ugrid)-1):
            for j in range(len(self.vgrid)-1):
                corners = [(i, j), (i+1, j), (i+1, j+1), (i, j+1)]
                inside = [corner for corner in corners if corner in self.index]
                if len(inside) < 3:
                    continue
                if len(inside) == 4:
                    triangles = [tuple(self.index[corners[k]] for k in ids)
                                 for ids in [(0, 1, 2), (0, 2, 3)]]
                else:
                    triangles = [tuple(self.index[corner] for corner in inside)]
                self.cells[i, j] = triangles
                self.triangles.extend(triangles)
        self.triangles = np.asarray(self.triangles, dtype=int)
        self.inverses = {}
        for triangle in self.triangles:
            xyz = np.c_[self.nodes[triangle], np.ones(3)]
            self.inverses[tuple(triangle)] = np.linalg.inv(xyz.T)
        self.transport = []
        for (i, j), left in self.index.items():
            if (i+1, j) in self.index:
                self.transport.append((left, self.index[i+1, j], 'U'))
            if (i, j+1) in self.index:
                self.transport.append((self.index[i, j+1], left, '-V'))
        self.bounds = [(0., 1.) for _ in self.nodes]
        for index, (u, v) in enumerate(self.nodes):
            if abs(v-1) < 1e-12 or abs(u)+abs(v) < 1e-12:
                self.bounds[index] = (0., 0.)
            if abs(u-1)+abs(v+1) < 1e-12:
                self.bounds[index] = (1., 1.)

    def weights(self, u, v):
        if v >= 1-1e-13:
            return ()
        if u < abs(v)-2e-10 or u-v > 2+2e-10:
            raise ValueError(('outside field', u, v))
        ii = np.searchsorted(self.ugrid, u, side='right')-1
        jj = np.searchsorted(self.vgrid, v, side='right')-1
        ii = max(0, min(len(self.ugrid)-2, ii))
        jj = max(0, min(len(self.vgrid)-2, jj))
        for i, j in [(ii, jj), (ii-1, jj), (ii, jj-1), (ii-1, jj-1)]:
            for triangle in self.cells.get((i, j), []):
                weights = self.inverses[triangle] @ np.array([u, v, 1.])
                if np.min(weights) >= -1e-8:
                    weights[np.abs(weights) < 1e-10] = 0
                    weights = np.maximum(weights, 0)
                    weights /= weights.sum()
                    return tuple((index, float(weight)) for index, weight in zip(triangle, weights)
                                 if weight)
        raise ValueError(('missing cell', u, v, ii, jj))

    def radial_form(self, t, r):
        if t-r >= 1-1e-13:
            return Form(0., ())
        return Form(0., self.weights(t+r, t-r))

    def sides(self, t, x, kind=None):
        if kind is None:
            if abs(x) < 2e-12:
                kind = 'center'
            elif abs(x-1) < 2e-12:
                kind = 'right_endpoint'
            elif abs(x+1) < 2e-12:
                kind = 'left_endpoint'
            else:
                kind = 'positive' if x > 0 else 'negative'
        radial = self.radial_form(t, min(1., abs(x)))
        positive = Form(.5, tuple((i, w/2) for i, w in radial.terms))
        negative = Form(.5, tuple((i, -w/2) for i, w in radial.terms))
        if kind == 'center':
            return negative, positive
        if kind == 'right_endpoint':
            return positive, Form(1., ())
        if kind == 'left_endpoint':
            return Form(0., ()), negative
        if kind == 'positive':
            return positive, positive
        return negative, negative

    def route_cells(self, route):
        result = []
        for (t0, x0), (t1, x1) in zip(route, route[1:]):
            if t1 <= t0+1e-14:
                continue
            speed = (x1-x0)/(t1-t0)
            assert abs(speed) <= 1+1e-8, (t0, x0, t1, x1)
            intercept = x0-speed*t0
            cuts = [t0, t1]
            if abs(speed) > 1e-14:
                crossing = -intercept/speed
                if t0 < crossing < t1:
                    cuts.append(crossing)
            pieces = sorted(cuts)
            for left, right in zip(pieces, pieces[1:]):
                midpoint = (left+right)/2
                xpos = speed*midpoint+intercept
                sign = 1 if xpos >= 0 else -1
                us, ui = 1+sign*speed, sign*intercept
                vs, vi = 1-sign*speed, -sign*intercept
                boundaries = [left, right]
                for grid, slope, constant in [(self.ugrid, us, ui), (self.vgrid, vs, vi)]:
                    if abs(slope) > 1e-14:
                        times = (grid-constant)/slope
                        boundaries.extend(times[(times > left+1e-12) & (times < right-1e-12)])
                boundaries = sorted(set(boundaries))
                detailed = list(boundaries)
                for lo, hi in zip(boundaries, boundaries[1:]):
                    middle = (lo+hi)/2
                    u, v = us*middle+ui, vs*middle+vi
                    if v >= 1 or u-v > 2+1e-9:
                        continue
                    i = max(0, min(len(self.ugrid)-2,
                                   np.searchsorted(self.ugrid, u, side='right')-1))
                    j = max(0, min(len(self.vgrid)-2,
                                   np.searchsorted(self.vgrid, v, side='right')-1))
                    if len(self.cells.get((i, j), [])) != 2:
                        continue
                    du, dv = self.ugrid[i+1]-self.ugrid[i], self.vgrid[j+1]-self.vgrid[j]
                    slope = us/du-vs/dv
                    constant = (ui-self.ugrid[i])/du-(vi-self.vgrid[j])/dv
                    if abs(slope) > 1e-14:
                        crossing = -constant/slope
                        if lo+1e-12 < crossing < hi-1e-12:
                            detailed.append(crossing)
                detailed = sorted(set(detailed))
                for lo, hi in zip(detailed, detailed[1:]):
                    midx = speed*(lo+hi)/2+intercept
                    if abs(midx) < 1e-12:
                        kind = 'center'
                    elif abs(midx-1) < 1e-12:
                        kind = 'right_endpoint'
                    elif abs(midx+1) < 1e-12:
                        kind = 'left_endpoint'
                    else:
                        kind = 'positive' if midx > 0 else 'negative'
                    xl, xr = speed*lo+intercept, speed*hi+intercept
                    at_left = self.sides(lo, xl)
                    line_left = self.sides(lo, xl, kind)
                    line_right = self.sides(hi, xr, kind)
                    result.append((hi-lo, at_left, line_left, line_right))
        return result

    def seed(self):
        # Quantiles p_q(t)=min(1,max(q-t,q/2,t+q-1)).
        values = np.maximum(0, np.minimum(1, self.nodes[:, 0])
                            - np.maximum(0, self.nodes[:, 1]))
        for i, (lo, hi) in enumerate(self.bounds):
            if lo == hi:
                values[i] = lo
        return values

    def repair_values(self, values, scale=10**12):
        """An integer isotonic majorant, preserving the fixed physical faces."""
        integers = np.rint(np.clip(values, 0., 1.)*scale).astype(np.int64)
        cone = getattr(self, 'constant_early_cone', None)
        if cone is not None:
            # Preserve the exact affine cone even in the exported rational
            # field.  Its nodes have no external incoming order edge, so
            # subsequent monotone-majorant propagation cannot alter them.
            quantum = lcm(*(ratio.denominator for _, ratio in cone['ratios']))
            assert scale % quantum == 0, ('cone lattice scale', scale, quantum)
            anchor = int(integers[cone['anchor']])
            anchor = min(scale, ((anchor+quantum-1)//quantum)*quantum)
            for index, ratio in cone['ratios']:
                integers[index] = anchor*ratio.numerator//ratio.denominator
        outgoing = [[] for _ in integers]
        edges = [(lo, hi) for lo, hi, _ in self.transport]
        edges += getattr(self, 'additional_order_edges', [])
        for lo, hi in edges:
            outgoing[lo].append(hi)
        queue = deque(map(int, np.argsort(self.nodes[:, 0]-self.nodes[:, 1], kind='stable')))
        queued = np.ones(len(integers), dtype=bool)
        while queue:
            index = queue.popleft()
            queued[index] = False
            for target in outgoing[index]:
                if integers[target] < integers[index]:
                    integers[target] = integers[index]
                    if not queued[target]:
                        queue.append(target)
                        queued[target] = True
        for index, (lo, hi) in enumerate(self.bounds):
            if lo == hi:
                assert integers[index] == int(lo*scale), ('fixed face repair', index)
        if cone is not None:
            anchor = int(integers[cone['anchor']])
            for index, ratio in cone['ratios']:
                assert integers[index]*ratio.denominator == anchor*ratio.numerator, ('cone repair', index)
        repaired = integers.astype(float)/scale
        return repaired, float(np.max(np.abs(repaired-values)))

    def late_rows(self, negative_v=False):
        """Sufficient late-turn inequalities, with every row labelled.

        The negative-V option drops Jplus and is exact only for the intended
        high-rank patch. Its separate duals must not be mistaken for monster
        probabilities or for an established global equilibrium condition.
        """
        coordinate_index = {tuple(np.round(point, 13)): i for i, point in enumerate(self.nodes)}
        rows = []
        for triangle in self.triangles:
            points = self.nodes[triangle]
            if points[:, 0].min() < 1-1e-12:
                continue
            positive = points[:, 1].min() >= -1e-12
            negative = points[:, 1].max() <= 1e-12
            if not positive and not (negative_v and negative):
                continue
            derivative = self.inverses[tuple(triangle)][:, 0]
            for index, (u, v) in zip(triangle, points):
                aindex = coordinate_index[tuple(np.round([abs(v), -abs(v)], 13))]
                coefficients = {}
                for j, slope in zip(triangle, derivative):
                    coefficients[int(j)] = coefficients.get(int(j), 0.)+(6+u-v)*slope
                coefficients[int(index)] = coefficients.get(int(index), 0.)+2
                coefficients[aindex] = coefficients.get(aindex, 0.)+(2 if positive else -1)
                rows.append((coefficients, 4., dict(kind='late_positive_v' if positive else 'late_negative_v',
                                                     u=float(u), v=float(v), triangle=list(map(int, triangle)))))
        return rows

    def save(self, path, values, compact=False, **extra):
        payload = dict(scope='Complete triangular ordered radial CDF; floating discovery, no bound certificate',
                       nodes=self.nodes.tolist(), triangles=self.triangles.tolist(), values=list(map(float, values)),
                       terminal_time=2, ugrid=self.ugrid.tolist(), vgrid=self.vgrid.tolist(),
                       base=self.base.tolist(), trace='continuous interior; closed endpoint=1, strict center=0')
        payload.update(extra)
        Path(path).write_text(json.dumps(payload, indent=None if compact else 2)+'\n')


class RouteFunctional:
    def __init__(self, mesh, route, label=None):
        self.mesh, self.route = mesh, [tuple(map(float, point)) for point in route]
        self.label = label or {}
        self.cells = mesh.route_cells(self.route)
        self.initial = mesh.sides(*self.route[0])
        self.final = mesh.sides(*self.route[-1])

    @staticmethod
    def _maximum(old, left, right, duration, values, gradient):
        ov, lv, rv = old.value(values), left.value(values), right.value(values)
        if abs(lv-rv) <= 1e-12 and lv >= ov-1e-12:
            # At a flat record face, the current affine trace is also an
            # exact supporting selection. Retain its latest form instead of
            # carrying a stale earlier record through an entire cone face.
            left.add_gradient(gradient, duration/2)
            right.add_gradient(gradient, duration/2)
            return duration*(lv+rv)/2, right
        start = old if ov >= lv else left
        sv = max(ov, lv)
        if rv <= sv or rv <= lv:
            start.add_gradient(gradient, duration)
            return duration*sv, start
        alpha = max(0., min(1., (sv-lv)/(rv-lv)))
        weights = [alpha, (1-alpha)**2/2, (1-alpha*alpha)/2]
        for form, weight in zip([start, left, right], weights):
            form.add_gradient(gradient, duration*weight)
        area = duration*(weights[0]*sv+weights[1]*lv+weights[2]*rv)
        return area, right

    def value_gradient(self, values):
        gradient = np.zeros(len(values))
        lower, upper = self.initial
        negative_lower = lower.negative()
        cost = self.route[-1][0]-self.route[0][0]
        for duration, point, left, right in self.cells:
            pmin, pmax = point
            if pmax.value(values) > upper.value(values):
                upper = pmax
            if -pmin.value(values) > negative_lower.value(values):
                negative_lower = pmin.negative()
            area, upper = self._maximum(upper, left[1], right[1], duration, values, gradient)
            cost -= area
            area, negative_lower = self._maximum(negative_lower, left[0].negative(),
                                                  right[0].negative(), duration, values, gradient)
            cost -= area
        gradient *= -1
        lower, upper_final = self.final
        final_survival = 1-max(upper.value(values), upper_final.value(values))
        final_survival -= max(negative_lower.value(values), -lower.value(values))
        assert abs(final_survival) < 1e-7, ('incomplete route', final_survival, self.route)
        return float(cost), gradient


class RadialLine:
    def __init__(self, mesh, fixed, lo, hi, horizontal):
        if not hasattr(mesh, '_line_cache'):
            mesh._line_cache = {}
        key = (float(fixed), float(lo), float(hi), bool(horizontal))
        if key in mesh._line_cache:
            self.cells, self.integral = mesh._line_cache[key]
            return
        self.cells = []
        if hi <= lo+1e-14:
            self.integral = Form(0., ())
            mesh._line_cache[key] = (self.cells, self.integral)
            return
        if horizontal:
            route = [((fixed+lo)/2, (fixed-lo)/2), ((fixed+hi)/2, (fixed-hi)/2)]
        else:
            route = [((fixed+lo)/2, (lo-fixed)/2), ((fixed+hi)/2, (hi-fixed)/2)]
        parts = []
        for duration, point, left, right in mesh.route_cells(route):
            # Interior positive spatial CDF is (1+R)/2, including its limits.
            rl = combination([(2., left[1])], constant=-1.)
            rr = combination([(2., right[1])], constant=-1.)
            width = 2*duration
            self.cells.append((width, rl, rr))
            parts.extend([(width/2, rl), (width/2, rr)])
        self.integral = combination(parts)
        mesh._line_cache[key] = (self.cells, self.integral)

    def hinge(self, values, threshold, sign=1):
        """Integral of (sign*(R-threshold))_+, with its exact subgradient."""
        value = 0.
        gradient = np.zeros(len(values))
        for width, left, right in self.cells:
            lf = combination([(sign, left), (-sign, threshold)])
            rf = combination([(sign, right), (-sign, threshold)])
            lv, rv = lf.value(values), rf.value(values)
            if abs(lv)+abs(rv) < 1e-13:
                lf.add_gradient(gradient, width/4)
                rf.add_gradient(gradient, width/4)
            elif lv >= 0 and rv >= 0:
                value += width*(lv+rv)/2
                lf.add_gradient(gradient, width/2)
                rf.add_gradient(gradient, width/2)
            elif lv <= 0 and rv <= 0:
                continue
            else:
                crossing = -lv/(rv-lv)
                if rv > lv:
                    wl, wr = (1-crossing)**2/2, (1-crossing*crossing)/2
                else:
                    wl, wr = crossing-crossing*crossing/2, crossing*crossing/2
                value += width*(wl*lv+wr*rv)
                lf.add_gradient(gradient, width*wl)
                rf.add_gradient(gradient, width*wr)
        return value, gradient


class TemplateFunctional(RouteFunctional):
    """Full-CDF formulas remove artificial record ties on legal cone faces."""
    def __init__(self, mesh, route, label):
        self.mesh, self.route, self.label = mesh, [tuple(map(float, point)) for point in route], label
        x = label['start']
        self.z = z = abs(x)
        s = label.get('turn', 2-x)
        a = mesh.radial_form(0., z)
        if z == 1:
            a = Form(1., ())  # no initial endpoint atom in this mesh class
        self.a = a
        if x >= 0:
            b = (Form(1., ()) if abs(s-(2-x)) < 1e-12
                 else mesh.radial_form((s-z)/2, (s+z)/2))
            column = RadialLine(mesh, -z, z, s, False).integral
            outgoing = RadialLine(mesh, s, s, s+2, False).integral
            self.linear = combination([(2*s, a), (-(6+s+z), b),
                                       (-1, column), (-1, outgoing)], constant=4*s+8)
            self.hinge_line = RadialLine(mesh, s, -z, s, True)
            self.hinge_sign = -1
        else:
            b = (Form(1., ()) if abs(s-(2+z)) < 1e-12
                 else mesh.radial_form((s+z)/2, (s-z)/2))
            nbar = RadialLine(mesh, z, -z, z, True).integral
            column = RadialLine(mesh, z, z, s, False).integral
            self.linear = combination([(1, nbar), (-2*(s+1), a),
                                       (-(6+s-z), b), (-1, column)], constant=4*s+8)
            self.hinge_line = RadialLine(mesh, s, s, s+2, False)
            self.hinge_sign = 1

    def value_gradient(self, values):
        value = self.linear.value(values)
        gradient = np.zeros(len(values))
        self.linear.add_gradient(gradient, 1.)
        hinge_value, hinge_gradient = self.hinge_line.hinge(values, self.a, self.hinge_sign)
        return (value-hinge_value)/4, (gradient-hinge_gradient)/4


class TwoInteriorFunctional(RouteFunctional):
    """Exact CDF formula for positive/negative starts and two interior turns."""
    def __init__(self, mesh, route, label):
        self.mesh, self.route, self.label = mesh, [tuple(map(float, point)) for point in route], label
        x, s, t = label['start'], label['first_turn'], label['second_turn']
        z = abs(x)
        a = mesh.radial_form(0., z)
        if z == 1:
            a = Form(1., ())
        b = (Form(1., ()) if abs(s-(2-x)) < 1e-12
             else mesh.radial_form((s-x)/2, (s+x)/2))
        d = (Form(1., ()) if abs(t-(s+2)) < 1e-12
             else mesh.radial_form((s+t)/2, (t-s)/2))
        self.hinges = [(RadialLine(mesh, t, t, t+2, False), b, 1)]
        self.point_hinge = None
        if x >= 0:
            column = RadialLine(mesh, -z, z, s, False).integral
            across = RadialLine(mesh, s, s, t, False).integral
            self.linear = combination([(2*s, a), (-(2*t+2+z-s), b),
                                       (-(t+6-s), d), (-1, column), (-1, across)],
                                      constant=4*t+8)
            self.hinges.append((RadialLine(mesh, s, -z, s, True), a, -1))
        else:
            nbar = RadialLine(mesh, z, -z, z, True).integral
            column = RadialLine(mesh, z, z, s, False).integral
            self.linear = combination([(1, nbar), (-2*(t+3), a),
                                       ((s+z-2*t-2), b), (-1, column)], constant=4*t+8)
            self.hinges.append((RadialLine(mesh, s, s, t, False), a, 1))
            self.point_hinge = (t+6-s, combination([(1, d), (-1, a)]))

    def value_gradient(self, values):
        value = self.linear.value(values)
        gradient = np.zeros(len(values))
        self.linear.add_gradient(gradient, 1.)
        for line, threshold, sign in self.hinges:
            hinge, g = line.hinge(values, threshold, sign)
            value -= hinge
            gradient -= g
        if self.point_hinge is not None:
            scale, form = self.point_hinge
            point = form.value(values)
            value -= scale*max(0., point)
            if point > 1e-13:
                form.add_gradient(gradient, -scale)
            elif point >= -1e-13:
                form.add_gradient(gradient, -scale/2)
        return value/4, gradient/4


class WaitTwoTriangleFunctional(RouteFunctional):
    """Wait in a constant-density cone, two triangles, then an endpoint tour.

    Requires R(U,V)=lambda*U for 0<=V<=U<=wait and final return e>=1.
    This mesh excludes a center atom at time one.  Transport makes the
    first triangle's captured rank at least the wait rank, so its integral
    is linear; only the second triangle needs clipped inverse integrals.
    """
    def __init__(self, mesh, route, label):
        self.mesh, self.route, self.label = mesh, [tuple(map(float, point)) for point in route], label
        s, t, e = label['wait'], label['first_return'], label['second_return']
        assert 0 <= s <= t <= e and e >= 1 and e-t < 2
        self.q = mesh.radial_form(s, 0.)
        b = mesh.radial_form((s+t)/2, (t-s)/2)
        d = mesh.radial_form((t+e)/2, (e-t)/2)
        first = label['endpoint_first']
        assert first in [-1, 1]
        alpha = 2*e+(2 if first == -1 else 6)-s-t
        beta = e+(6 if first == -1 else 2)-t
        gamma = 2*e+(6 if first == -1 else 2)
        integral = RadialLine(mesh, s, s, t, False).integral
        self.linear = combination([(-alpha, b), (-gamma, self.q), (-1, integral)],
                                  constant=4*e+8)
        self.point_hinge = (beta, combination([(1, d), (-1, self.q)]))
        self.hinge_line = RadialLine(mesh, t, t, e, False)

    def value_gradient(self, values):
        value = self.linear.value(values)
        gradient = np.zeros(len(values))
        self.linear.add_gradient(gradient, 1.)
        scale, point = self.point_hinge
        p = point.value(values)
        value -= scale*max(0., p)
        point.add_gradient(gradient, -scale*(1. if p > 1e-13 else .5 if p >= -1e-13 else 0.))
        hinge, g = self.hinge_line.hinge(values, self.q, 1)
        return (value-hinge)/4, (gradient-g)/4


class InitialInwardFunctional(RouteFunctional):
    """Initial inward turn before center, then outward and endpoint tour."""
    def __init__(self, mesh, route, label):
        self.mesh, self.route, self.label = mesh, [tuple(map(float, point)) for point in route], label
        a,v,s=label['start'],label['first_v'],label['second_u']
        assert 0<a<=1 and -a-1e-12<=v<a and a-1e-12<=s<=v+2+1e-12
        initial=Form(1.,()) if a==1 else mesh.radial_form(0.,a)
        low=mesh.radial_form((a+v)/2,(a-v)/2)
        high=(Form(1.,()) if abs(s-v-2)<1e-12
              else mesh.radial_form((s+v)/2,(s-v)/2))
        n_part=RadialLine(mesh,a,-a,v,True).integral
        outgoing=RadialLine(mesh,s,s,s+2,False).integral
        self.linear=combination([(1,n_part),(2*s-a-v,low),(-(2*s+6),initial),
                                 (-1,outgoing)],constant=4*s+8)
        self.point_hinge=(s+6-v,combination([(1,high),(-1,initial)]))
        self.hinges=[(RadialLine(mesh,s,v,s,True),low,-1),
                     (RadialLine(mesh,v,a,s,False),initial,1)]

    def value_gradient(self,values):
        value=self.linear.value(values)
        gradient=np.zeros(len(values));self.linear.add_gradient(gradient,1.)
        scale,point=self.point_hinge;p=point.value(values)
        value-=scale*max(0.,p)
        point.add_gradient(gradient,-scale*(1. if p>1e-13 else .5 if p>=-1e-13 else 0.))
        for line,threshold,sign in self.hinges:
            hinge,g=line.hinge(values,threshold,sign);value-=hinge;gradient-=g
        return value/4,gradient/4


def m1(start):
    return [(0., start), (1-start, 1.), (3-start, -1.)]


def m2(start, turn):
    return [(0., start), ((turn-start)/2, (turn+start)/2),
            (turn+1, -1.), (turn+3, 1.)]


def m3(start, first, second):
    return [(0., start), ((first-start)/2, (first+start)/2),
            ((first+second)/2, (first-second)/2),
            (second+1, 1.), (second+3, -1.)]


def wait_two_triangles(wait, first_return, second_return=1., endpoint_first=-1):
    s, t, e = wait, first_return, second_return
    return [(0., 0.), (s, 0.), ((s+t)/2, (s-t)/2), (t, 0.),
            ((t+e)/2, (e-t)/2), (e, 0.),
            (e+1, float(endpoint_first)), (e+3, float(-endpoint_first))]


def initial_inward_route(a,v,s):
    return [(0.,a),((a+v)/2,(a-v)/2),((s+v)/2,(s-v)/2),
            (s+1,-1.),(s+3,1.)]


def initial_inward_pool(mesh):
    """Full legal first-V/second-U family on the existing coordinate mesh."""
    pool=[]
    for a in mesh.base:
        if a<=0:continue
        for v in mesh.vgrid:
            if v < -a-1e-12 or v >= a-1e-12:continue
            for s in mesh.ugrid:
                if s < a-1e-12 or s > v+2+1e-12:continue
                label=dict(kind='initial_inward',start=float(a),first_v=float(v),second_u=float(s))
                pool.append(InitialInwardFunctional(mesh,initial_inward_route(a,v,s),label))
    return pool


def wait_two_triangle_pool(mesh, cutoff):
    pool = []
    for s in mesh.base:
        if s > cutoff+1e-12:
            continue
        for t in mesh.base:
            if t < s-1e-12:
                continue
            for first in [-1, 1]:
                label = dict(kind='wait_two_triangles', wait=float(s), first_return=float(t),
                             second_return=1., endpoint_first=first)
                pool.append(WaitTwoTriangleFunctional(mesh, wait_two_triangles(s, t, 1., first), label))
    return pool


def two_interior_pool(mesh):
    """Every signed M3 start/turn triple on the existing pre-one mesh.

    The first implementation used five first-turn coordinates and omitted
    second turns below .875.  Independent separation found a decisive route
    at the already-present first coordinate 11/16, so the structural family
    is now covered without selecting a few preferred first-turn cells.
    """
    pool = []
    for first in mesh.base:
        for second in mesh.base:
            if second < first-1e-12:
                continue
            for z in mesh.base:
                if z > first+1e-12:
                    continue
                for sign in ([1] if z == 0 else [-1, 1]):
                    x = sign*z
                    label = dict(kind='M3', start=float(x), first_turn=float(first), second_turn=float(second))
                    pool.append(TwoInteriorFunctional(mesh, m3(float(x), float(first), float(second)), label))
    return pool


def route_pool(mesh):
    starts = list(mesh.base)
    pool = []
    for z in starts:
        for sign in ([1] if z == 0 else [-1, 1]):
            x = sign*z
            pool.append(TemplateFunctional(mesh, m1(x), dict(kind='M1', start=x)))
            if z >= 1:
                continue
            turns = sorted(set([1., 1+1/64, 1+1/32, 1+1/16, 1+1/8])
                           | set(mesh.base))
            for s in turns:
                if s > 0 and s >= abs(x)-1e-12 and s < 2-x-1e-10:
                    pool.append(TemplateFunctional(mesh, m2(x, s), dict(kind='M2', start=x, turn=s)))
            if sign < 0:
                for fraction in [.25, .5, .75]:
                    s = z*(2*fraction-1)
                    pool.append(RouteFunctional(mesh, m2(x, s),
                                                dict(kind='M2_negative_first_turn', start=x, turn=s)))
    # A previously decisive first turn on the negative half, retained exactly.
    route = [(0., .8221139321), (.9108307204, -.0887167883),
             (1.9995475087, 1.), (3.9995475087, -1.)]
    pool.append(RouteFunctional(mesh, route, dict(kind='known_negative_first_turn')))
    return pool


if __name__ == '__main__':
    mesh = FieldMesh()
    values = mesh.seed()
    pool = route_pool(mesh)
    print('MESH', len(mesh.nodes), len(mesh.triangles), len(mesh.transport), 'ROUTES', len(pool))
    data = [(functional.value_gradient(values)[0], functional.label) for functional in pool]
    print('SEED_MIN', min(data, key=lambda pair: pair[0]))
    mesh.save(Path(__file__).with_name('joint_cdf_seed.json'), values, routes=[f.route for f in pool])
