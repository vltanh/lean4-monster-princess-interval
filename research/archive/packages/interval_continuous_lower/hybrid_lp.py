#!/usr/bin/env python3
"""Calendar separation with selectively promoted discrete/continuous records.

Continuous secant charges are conservative known-route scores. This model
is discovery machinery, never a complete response or game-value certificate.
"""
from fractions import Fraction as Q
from types import SimpleNamespace
import time

import numpy as np
from scipy.sparse import coo_matrix

import event_lp
from record_lp import RecordLP, path_records
from front_model import coefficients
from score_continuous_attack import basis, leg_intervals
from cached_path_pricing import normalize_path
from master import plan_column


def geometry(n):
    return SimpleNamespace(n=n, C=4*n, orientation=lambda i: i % (2*n) < n)


class HybridLP(RecordLP):
    """Persistent sparse LP with one coordinate map for fields and auxiliaries.

    Cheap calendar rows cover the large cache. Only explicitly promoted
    discrete paths receive all-calendar records. Specified continuous routes
    receive the conservative perspective-secant model. Both kinds of records
    retain endpoint interior traces until actual capture.
    """
    def __init__(self, master, floor, seconds=180., level_fraction=.5,
                 front=False, secants=16, route_batch=2):
        if type(secants) is not int or secants < 1:
            raise ValueError('secants must be a positive integer')
        if type(route_batch) is not int or route_batch < 1:
            raise ValueError('continuous route batch must be positive')
        super().__init__(master, floor, seconds, level_fraction, front)
        # A specified inefficient route can cost more than the old search's
        # objective cap of three. Its score must not be clipped to that cap.
        for lp in (self.main, self.prox):
            event_lp._check(lp.highs.changeColBounds(0, 0., np.inf), 'unclip specified-route score')
        self.secants = secants
        self.route_batch = route_batch
        self.pending = []
        self.auxiliary_count = 0
        self.aux_main = []
        self.aux_prox = []
        self.continuous_routes = []
        self.route_seen = set()
        self.promoted_paths = []
        self.promoted_seen = set()
        self.violations = {}

    def select_routes(self, reports):
        # All reports still contribute their supporting planes. Promote only
        # the lowest-scoring physical routes at this screening step; a route
        # becoming active on a later trial can then acquire its full model.
        return sum(self.add_route(p['route'])
                   for p in sorted(reports, key=lambda p: Q(p['value']))[:self.route_batch])

    def checkpoint(self):
        return dict(schema=2, secants=self.secants, front=self.front, route_batch=self.route_batch,
                    continuous_routes=[[[str(t), str(x)] for t, x in r] for r in self.continuous_routes],
                    promoted_paths=self.promoted_paths,
                    violations=[dict(start_grid=start, moves=list(moves), count=count)
                                for (start, moves), count in sorted(self.violations.items())])

    def restore(self, state):
        if (state['schema'], state['secants'], state['front'], state.get('route_batch')) != (2, self.secants, self.front, self.route_batch):
            raise ValueError('hybrid checkpoint model parameters changed')
        for route in state['continuous_routes']:
            self.add_route(route)
        for path in state['promoted_paths']:
            self.promote(path)
        for item in state['violations']:
            path = normalize_path(self.master.n, item)
            count = item['count']
            if type(count) is not int or count < 1:
                raise ValueError('invalid retained violation count')
            key = path['start_grid'], tuple(path['moves'])
            self.violations[key] = count

    def _aux(self):
        key = ('a', self.auxiliary_count)
        self.auxiliary_count += 1
        return key

    def _row(self, terms, bound=0):
        combined = {}
        for key, value in terms:
            combined[key] = combined.get(key, Q(0)) + value
        self.pending.append(({k: v for k, v in combined.items() if v}, Q(bound)))

    def _field(self, point):
        return ('g', *point)

    def _price(self, point, side):
        coef = basis(geometry(self.master.n), *point)
        if self.front:
            coef = coefficients(self.master.n, coef)
        sign = 1 if side == 0 else -1
        return Q(1, 2), {self._field(p): sign*v for p, v in coef.items()}

    def promote(self, path):
        path, records = path_records(self.master.n, path, self.front)
        key = path['start_grid'], tuple(path['moves'])
        if key in self.promoted_seen:
            return False
        self.promoted_seen.add(key)
        self.promoted_paths.append(path)
        variables = []
        for record in records:
            variable = self._aux()
            variables.append(variable)
            if record['previous'] is not None:
                self._row([(variable, 1), (variables[record['previous']], -1)])
            terms = [(variable, 1)]
            if record['point'] is not None:
                terms.append((self._field(record['point']), -record['coefficient']))
            self._row(terms, 1)
        self._row([(v, -Q(r['weight'], 4*self.master.n))
                   for v, r in zip(variables, records)], -self.floor)
        return True

    def note_violation(self, path, threshold=3):
        if type(threshold) is not int or threshold < 1:
            raise ValueError('promotion threshold must be positive')
        path = normalize_path(self.master.n, path)
        key = path['start_grid'], tuple(path['moves'])
        self.violations[key] = self.violations.get(key, 0)+1
        return self.violations[key] >= threshold and self.promote(path)

    def add_route(self, route):
        route = tuple(tuple(map(Q, p)) for p in route)
        # Validate the WHOLE route before mutating the model. Routes can pass
        # an endpoint inside a leg only by leaving the arena, already excluded.
        if not route or route[0][0] != 0 or abs(route[0][1]) > 1:
            raise ValueError('continuous route must start in the arena at time zero')
        if not {-Q(1), Q(1)} <= {x for _, x in route}:
            raise ValueError('continuous route must visit both endpoints')
        for (ta, xa), (tb, xb) in zip(route, route[1:]):
            if tb <= ta or abs(xb-xa) != tb-ta or max(abs(xa), abs(xb)) > 1:
                raise ValueError('continuous record model requires unit-speed legs')
        if route in self.route_seen:
            return False
        self.route_seen.add(route)
        self.continuous_routes.append(route)
        previous = [None, None]
        previous_end = [None, None]
        holding = [False, False]
        stopped = [route[0][1] == -1, route[0][1] == 1]
        charges = []
        for first, last in zip(route, route[1:]):
            direction = 1 if last[1] > first[1] else -1
            for a, b in leg_intervals(geometry(self.master.n), *first, *last):
                duration = b[0]-a[0]
                for side in (0, 1):
                    if stopped[side]:
                        continue
                    c0, q0 = self._price(a, side)
                    c1, q1 = self._price(b, side)
                    decreasing = direction < 0 if side == 0 else direction > 0
                    constant = q0 == q1
                    if holding[side] and (not decreasing or constant):
                        # The entering record was already capped at the start
                        # of this monotone stretch. A nondecreasing price adds
                        # no new cap, and a structurally constant price adds
                        # no perspective. This includes outward endpoint tails.
                        charges.append((previous[side], -duration))
                        previous_end[side] = c1, q1
                        continue
                    record = self._aux()
                    self._row([(record, 1)]+[(k, -v) for k, v in q0.items()], c0)
                    if previous[side] is not None:
                        self._row([(record, 1), (previous[side], -1)])
                        ce, qe = previous_end[side]
                        self._row([(record, 1)]+[(k, -v) for k, v in qe.items()], ce)
                    charges.append((record, -duration))
                    if decreasing and not constant:
                        u, v = self._aux(), self._aux()
                        # u >= record-q1, u <= q0-q1; v >= each secant.
                        self._row([(record, 1), (u, -1)]+[(k, -w) for k, w in q1.items()], c1)
                        drop = dict(q0)
                        for k, w in q1.items():
                            drop[k] = drop.get(k, Q(0))-w
                        self._row([(u, 1)]+[(k, -w) for k, w in drop.items()], c0-c1)
                        for j in range(self.secants):
                            alpha = Q(2*j+1, self.secants)
                            beta = Q(j*(j+1), self.secants**2)
                            self._row([(u, alpha), (v, -1)]+
                                      [(k, -beta*w) for k, w in drop.items()], beta*(c0-c1))
                        charges.append((v, duration/2))
                    previous[side] = record
                    previous_end[side] = c1, q1
                    holding[side] = not decreasing or constant
            if last[1] == -1:
                stopped[0] = True
            if last[1] == 1:
                stopped[1] = True
        self._row([(('z',), 1)]+charges)
        return True

    def _sync(self):
        began = time.monotonic()
        # Calendar coefficients are reconstructed independently of any global
        # front-model installation, then explicitly projected if requested.
        for column in self.master.columns[self.bank_count:]:
            mass, coef = plan_column(self.master.n, column['plan'])
            if self.front:
                coef = coefficients(self.master.n, coef)
            self._row([(self._field(p), -Q(v, 4*self.master.n)) for p, v in coef.items()],
                      Q(mass, 4*self.master.n)-self.floor)
        for plane in self.attacks[self.attack_count:]:
            self._row([(('z',), 1)]+[(self._field(p), -v) for p, v in plane['coeff'].items()], plane['constant'])
        new = sorted({key[1:] for terms, _ in self.pending for key in terms
                      if key[0] == 'g' and key[1:] not in self.index})
        count = len(new)
        if count:
            ms = self.main.highs.getNumCol()
            ps = self.prox.highs.getNumCol()
            self._add_columns(self.main, np.zeros(count), np.ones(count))
            self._add_columns(self.prox, np.tile([0., 1., 0.], count), np.tile([1., np.inf, 1.], count))
            prox_rows = []
            for offset, point in enumerate(new):
                self.index[point] = len(self.nodes)
                self.nodes.append(point)
                self.main_events.append(ms+offset)
                g, u, a = ps+3*offset, ps+3*offset+1, ps+3*offset+2
                self.prox_events.append(g)
                self.prox_anchors.append(a)
                prox_rows.extend([({g: 1, u: -1, a: -1}, 0), ({g: -1, u: -1, a: 1}, 0)])
            self._append(self.prox, prox_rows)
            edges = [e for e in event_lp.projected_order(self.master.n, self.nodes) if e not in self.edges]
            for a, b in edges:
                self._row([(self._field(self.nodes[a]), 1), (self._field(self.nodes[b]), -1)])
            self.edges.update(edges)
        new_aux = self.auxiliary_count-len(self.aux_main)
        for lp, indices in ((self.main, self.aux_main), (self.prox, self.aux_prox)):
            start = lp.highs.getNumCol()
            if new_aux:
                self._add_columns(lp, np.zeros(new_aux), 2*np.ones(new_aux))
                indices.extend(range(start, start+new_aux))
            def column(key):
                if key[0] == 'z':
                    return 0
                if key[0] == 'a':
                    return indices[key[1]]
                i = self.index[key[1:]]
                return (self.main_events if lp is self.main else self.prox_events)[i]
            self._append(lp, [({column(k): v for k, v in terms.items()}, rhs)
                              for terms, rhs in self.pending])
        self.pending.clear()
        self.bank_count = len(self.master.columns)
        self.attack_count = len(self.attacks)
        self.record_variables = self.auxiliary_count
        return time.monotonic()-began

    @staticmethod
    def _add_columns(lp, costs, upper):
        count = len(costs)
        event_lp._check(lp.highs.addCols(count, costs, np.zeros(count), upper, 0,
                         np.zeros(count+1, dtype=np.int32), np.zeros(0, dtype=np.int32), np.zeros(0)),
                        'append hybrid columns')

    @staticmethod
    def _append(lp, rows):
        rr, cc, vv, rhs = [], [], [], []
        for terms, bound in rows:
            row = len(rhs)
            rhs.append(float(bound))
            for col, value in terms.items():
                rr.append(row)
                cc.append(col)
                vv.append(float(value))
        lp.add_rows(coo_matrix((vv, (rr, cc)), shape=(len(rhs), lp.highs.getNumCol())), rhs)

    def solve(self, seed, screen, radius):
        table, upper, level, stats = super().solve(seed, screen, radius)
        stats.update(bank_model='calendar cuts with selective record promotion',
                     physical_path_rows=len(self.promoted_paths),
                     promoted_physical_paths=len(self.promoted_paths),
                     continuous_record_routes=len(self.continuous_routes),
                     continuous_route_batch=self.route_batch,
                     continuous_secants=self.secants)
        # With conservative secants this is an inner model optimum, not an
        # upper on the corresponding exact continuous-route optimization.
        stats['restricted_secant_model_value'] = stats.pop('continuous_restricted_upper')
        return table, upper, level, stats
