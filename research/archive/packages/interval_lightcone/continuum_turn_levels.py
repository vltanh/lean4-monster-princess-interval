"""
Continuum game with piecewise-constant Monster densities and exact integration: one-turn paths with a
spread of turn levels around b = 1, and two-turn paths that join a one-turn trajectory.

Variables (pair masses; each pair is a path and its mirror image, probability 1/2 each):
  e            sweep pair
  Pp[i]        P_1(a),  a in bin i  (turn level b = 1 exactly)
  Sp[i]        S(a),    a in bin i  (b = 2 - a)
  Pm[i]        P_1(-c), c in bin i
  Sm[i]        S(-c),   c in bin i  (b = 2 + c)
  Qp[i, jb]    P_b(a),  a in bin i, b uniform in level bin jb
  Qm[i, jb]    P_b(-c), c in bin i, b uniform in level bin jb
  Tp[i, j]     T2(c, U1),  c in bin i (c > 0), U1 uniform in bin j > i
  Tm[i, j]     T2(-c, U1), c in bin i,         U1 uniform in bin j > i
Level bins are the mesh columns next to U = 1: jb < nb below 1, jb >= nb above 1, both in increasing b.

T2(c, U1) starts at c, runs right until t + x = U1, runs left through the center until t - x = 1 (the line
of the sweep from -1), and then follows that sweep to +1 and back.  It is the mirror image of P_1(-U1)
with the first part of its run replaced by a run from c.

The Princess's response is a dynamic program over (start radius; U, W) on the mesh refined r times.  Rewards
are in units of 2*T(path) + 2*T(mirror) per unit pair mass, i.e. 4*E[T].  A Princess who has passed the
turning point of T2 is credited with the largest time that path can still give (capture at +1 at time 2),
so the response value is an upper estimate of her true payoff.

Numerical tool: floating-point LP (HiGHS), no certificate.  The response is exact only for staircases with
corners on the refined mesh; on a mesh refined further the value rises by about 1.5e-5 at 16 bins.
"""
import numpy as np, sys, time, pickle
from scipy.optimize import linprog


class Continuum:
    def __init__(self, g, nb, nc=0):
        self.g = g = np.asarray(g, dtype=float); n = self.n = len(g) - 1; self.nb = nb
        self.mid = 0.5 * (g[:-1] + g[1:]); self.dg = np.diff(g)
        self.Uc = np.concatenate([g[:n], [1.0, 1.0], 2 - g[n - 1::-1]]); self.NU = 2 * n + 2
        self.Wc = np.concatenate([-g[::-1], g[1:n], [1.0, 1.0], 2 - g[n - 1::-1]]); self.NW = len(self.Wc)
        # b-bins
        self.blo = np.zeros(2 * nb); self.bhi = np.zeros(2 * nb); self.lo_node = np.zeros(2 * nb, dtype=int)
        self.col_of_b = {}            # U-column index (iu of its left node) -> jb
        for jb in range(nb):          # below 1: column jc = n - nb + jb
            jc = n - nb + jb
            self.blo[jb] = g[jc]; self.bhi[jb] = g[jc + 1]; self.lo_node[jb] = jc
        for jb in range(nb, 2 * nb):  # above 1: m = n - 1 - (jb - nb), U in (2-g_{m+1}, 2-g_m)
            m = n - 1 - (jb - nb)
            self.blo[jb] = 2 - g[m + 1]; self.bhi[jb] = 2 - g[m]; self.lo_node[jb] = 2 * n - m
        self.bmid = 0.5 * (self.blo + self.bhi)
        # validity masks: need |a| <= b on the whole rectangle and b <= 2 - a
        self.okp = np.zeros((n, 2 * nb), dtype=bool); self.okm = np.zeros((n, 2 * nb), dtype=bool)
        for i in range(n):
            for jb in range(2 * nb):
                self.okp[i, jb] = (self.blo[jb] >= g[i + 1] - 1e-15) and (self.bhi[jb] <= 2 - g[i + 1] + 1e-15)
                self.okm[i, jb] = (self.blo[jb] >= g[i + 1] - 1e-15)
        # variable layout
        self.o = dict(e=0, Pp=1, Sp=1 + n, Pm=1 + 2 * n, Sm=1 + 3 * n, Qp=1 + 4 * n, Qm=1 + 4 * n + 2 * n * nb)
        self.nc = nc
        self.o['Tp'] = 1 + 4 * n + 4 * n * nb; self.o['Tm'] = self.o['Tp'] + nc * n
        self.nvar = 1 + 4 * n + 4 * n * nb + 2 * nc * n
        ub = np.full(self.nvar, np.inf)
        ub[self.o['Qp']:self.o['Qp'] + 2 * n * nb][~self.okp.ravel()] = 0.0
        ub[self.o['Qm']:self.o['Qm'] + 2 * n * nb][~self.okm.ravel()] = 0.0
        okt = np.zeros((nc, n), dtype=bool)
        for i in range(nc):
            okt[i, i + 1:] = True
        self.okt = okt
        if nc:
            ub[self.o['Tp']:self.o['Tp'] + nc * n][~okt.ravel()] = 0.0
            ub[self.o['Tm']:self.o['Tm'] + nc * n][~okt.ravel()] = 0.0
        self.ub = ub

    def unpack(self, mu):
        n = self.n; nb = self.nb; o = self.o
        return (mu[0], mu[o['Pp']:o['Pp'] + n], mu[o['Sp']:o['Sp'] + n], mu[o['Pm']:o['Pm'] + n], mu[o['Sm']:o['Sm'] + n],
                mu[o['Qp']:o['Qp'] + 2 * n * nb].reshape(n, 2 * nb), mu[o['Qm']:o['Qm'] + 2 * n * nb].reshape(n, 2 * nb))

    def unpackT(self, mu):
        n = self.n; nc = self.nc; o = self.o
        return mu[o['Tp']:o['Tp'] + nc * n].reshape(nc, n), mu[o['Tm']:o['Tm'] + nc * n].reshape(nc, n)

    # ---- geometry ----------------------------------------------------------
    def bound_iu(self, jw):
        n = self.n
        if jw <= n:
            i = n - jw
            return n + 1 if i == n else 2 * n + 1 - i
        return 2 * n + 1
    def min_iu(self, jw):
        n = self.n
        if jw <= n: return 0
        if jw <= 2 * n - 1: return jw - n
        if jw == 2 * n: return n
        if jw == 2 * n + 1: return n + 1
        return 2 * n + 1 - (3 * n + 1 - jw)

    def jb_of_cbin(self, i):          # c-bin / U-column i in (0,1) as a b-bin (below 1), or -1
        jb = i - (self.n - self.nb)
        return jb if 0 <= jb < self.nb else -1
    def jb_of_mbin(self, m):          # column/row (2-g_{m+1}, 2-g_m) as a b-bin above 1, or -1
        jb = self.nb + (self.n - 1 - m)
        return jb if self.nb <= jb < 2 * self.nb else -1

    # ---- rewards -----------------------------------------------------------
    def prepare(self, mu):
        n = self.n; nb = self.nb; g = self.g; mid = self.mid
        e, Pp, Sp, Pm, Sm, Qp, Qm = self.unpack(mu)
        K = n + 1; ks = np.arange(K)
        P = type('R', (), {})()
        P.e, P.Pp, P.Sp, P.Pm, P.Sm, P.Qp, P.Qm = e, Pp, Sp, Pm, Sm, Qp, Qm
        P.E1 = e + np.concatenate([np.cumsum(Pp[::-1])[::-1], [0]])
        P.E2 = e + Pp.sum() + np.concatenate([[0], np.cumsum(Pm)])
        NU = self.NU
        iu = np.arange(NU)
        caught = self.lo_node[None, :] >= iu[:, None]                    # (NU, 2nb)
        esc_val = 2 * (self.bmid + 3)
        P.CQp = Qp @ caught.T.astype(float)                              # (n, NU)
        P.EQp = (Qp * esc_val[None, :]) @ (~caught).T.astype(float)
        P.CQm = Qm @ caught.T.astype(float)
        P.EQm = (Qm * esc_val[None, :]) @ (~caught).T.astype(float)
        P.QpB = Qp.sum(axis=0)                                           # (2nb,)
        P.QmA = Qm.sum(axis=1)                                           # (n,)
        P.QpAllEsc = (Qp * esc_val[None, :]).sum(axis=1)                 # (n,)
        P.QmAllEsc = (Qm * esc_val[None, :]).sum(axis=1)
        P.cumQmB = np.vstack([np.zeros((1, 2 * nb)), np.cumsum(Qm, axis=0)])        # [k, jb] = sum_{i<k}
        P.sufQpB = np.vstack([np.cumsum(Qp[::-1], axis=0)[::-1], np.zeros((1, 2 * nb))])  # [k, jb] = sum_{i>=k}
        P.ks = ks
        nc = self.nc
        Tp, Tm = self.unpackT(mu)
        P.Tp, P.Tm = Tp, Tm
        # caught tables for H-legs capped at U1-bin j (caught iff iu <= j)
        cm = (np.arange(n)[None, :] >= np.arange(NU)[:, None]).astype(float)      # (NU, n): j >= iu
        P.CTp = Tp @ cm.T if nc else np.zeros((0, NU)); P.ETp = 4.0 * (Tp @ (1 - cm).T) if nc else np.zeros((0, NU))
        P.CTm = Tm @ cm.T if nc else np.zeros((0, NU)); P.ETm = 4.0 * (Tm @ (1 - cm).T) if nc else np.zeros((0, NU))
        P.TpA = Tp.sum(axis=1) if nc else np.zeros(0); P.TmA = Tm.sum(axis=1) if nc else np.zeros(0)
        P.TpB = Tp.sum(axis=0) if nc else np.zeros(n)                              # by U1-bin
        suf = np.zeros((K, n)); cum = np.zeros((K, n))
        for kk in range(K):
            if nc:
                suf[kk] = Tp[min(kk, nc):].sum(axis=0)                             # starts c-bin i' >= k
                cum[kk] = Tm[:min(kk, nc)].sum(axis=0)                             # c'-bins i' < k
        P.sufTpJ = suf; P.cumTmJ = cum
        return P

    def tail(self, P):
        n = self.n; mid = self.mid; K = n + 1
        R = np.zeros((K, self.NW + 1))
        beyond = np.concatenate([[0], np.cumsum(P.Sm * (2 * (2 + mid) + 2))])
        R[:, 3 * n + 1] = beyond
        for jw in range(3 * n, n - 1, -1):
            if jw >= 2 * n + 1:
                m = 3 * n - jw
                rew = P.Sp[m] * (2 * (2 - mid[m]) + 2) * np.ones(K)
                jb = self.jb_of_mbin(m)
                if jb >= 0: rew = rew + (2 * (2 - mid[m]) + 2) * (P.QpB[jb] + P.cumQmB[:, jb])
            elif jw == 2 * n:
                rew = 4 * P.E2
            else:
                i = jw - n
                rew = (P.Pm[i] * 8 + P.Sm[i] * (2 * mid[i] + 2) + P.QmAllEsc[i]) * np.ones(K)
                jb = self.jb_of_cbin(i)
                if jb >= 0: rew = rew + (2 * mid[i] + 2) * (P.QpB[jb] + P.cumQmB[:, jb])
                rew = rew + 8.0 * P.TpB[i] + 8.0 * P.cumTmJ[:, i]
                if i < self.nc: rew = rew + 4.0 * P.TmA[i]
            R[:, jw] = R[:, jw + 1] + rew
        return R

    def r_right(self, P, iu, w):
        n = self.n; mid = self.mid; ks = P.ks
        if iu <= n - 1:
            i = iu
            rew = (P.Pm[i] + P.Sm[i] + P.QmA[i]) * (mid[i] + w) * (ks <= i)
            jb = self.jb_of_cbin(i)
            if jb >= 0: rew = rew + (mid[i] + w) * P.sufQpB[:, jb]
            rew = rew + (mid[i] + w) * P.sufTpJ[:, i]
            if i < self.nc: rew = rew + (mid[i] + w) * P.TmA[i] * (ks <= i)
            return rew
        if iu == n:
            return P.E1 * (1 + w)
        m = 2 * n - iu
        rew = P.Sp[m] * ((2 - mid[m]) + w) * (ks <= m)
        jb = self.jb_of_mbin(m)
        if jb >= 0: rew = rew + ((2 - mid[m]) + w) * P.sufQpB[:, jb]
        return rew

    def r_up(self, P, jw, iu, x):
        n = self.n; mid = self.mid; ks = P.ks; K = n + 1
        if jw <= n - 1:
            i = n - 1 - jw; m = -mid[i]
            base = P.Pp[i] * ((m + x) if iu <= n else 8.0) + P.Sp[i] * (m + x) + (m + x) * P.CQp[i, iu] + P.EQp[i, iu]
            if i < self.nc: base = base + (m + x) * P.CTp[i, iu] + P.ETp[i, iu]
            return base * (ks > i)
        if jw <= 2 * n - 1:
            i = jw - n
            base = P.Pm[i] * ((mid[i] + x) if iu <= n else 8.0) + P.Sm[i] * (mid[i] + x) + (mid[i] + x) * P.CQm[i, iu] + P.EQm[i, iu]
            rew = base * np.ones(K)
            jb = self.jb_of_cbin(i)
            if jb >= 0: rew = rew + (mid[i] + x) * (P.QpB[jb] + P.cumQmB[:, jb])
            capv = (mid[i] + x) if iu <= n else 8.0
            rew = rew + capv * (P.TpB[i] + P.cumTmJ[:, i])
            if i < self.nc: rew = rew + (mid[i] + x) * P.CTm[i, iu] + P.ETm[i, iu]
            return rew
        if jw == 2 * n:
            return P.E2 * (1 + x)
        m = 3 * n - jw
        rew = P.Sp[m] * ((2 - mid[m]) + x) * np.ones(K)
        jb = self.jb_of_mbin(m)
        if jb >= 0: rew = rew + ((2 - mid[m]) + x) * (P.QpB[jb] + P.cumQmB[:, jb])
        return rew

    def r_diag(self, P, jw):
        n = self.n; mid = self.mid; ks = P.ks
        i = n - 1 - jw
        inside = (P.Pp[i] * 8.0 + P.Sp[i] * (2 * (-mid[i]) + 2) + P.QpAllEsc[i] + (4.0 * P.TpA[i] if i < self.nc else 0.0)) * (ks > i)
        outside = P.Sp[i] * (2 * (2 - mid[i]) - 2) * (ks <= i)
        jb = self.jb_of_mbin(i)
        if jb >= 0: outside = outside + (2 * (2 - mid[i]) - 2) * P.sufQpB[:, jb]
        return inside + outside

    def dp(self, mu, want_paths=True):
        n = self.n; K = n + 1; NU = self.NU; NW = self.NW
        P = self.prepare(mu); Rt = self.tail(P)
        NEG = -1e18
        Phi = np.full((K, NU, NW), NEG)
        dec = np.zeros((K, NU, NW), dtype=np.int8) if want_paths else None
        Uc = self.Uc; Wc = self.Wc
        for jw in range(NW - 1, -1, -1):
            w = Wc[jw]; imax = self.bound_iu(jw); imin = self.min_iu(jw)
            up_ok_row = jw + 1 < NW
            if up_ok_row: lo2 = self.min_iu(jw + 1); hi2 = self.bound_iu(jw + 1)
            for iu in range(imax, imin - 1, -1):
                x = Uc[iu]
                if iu == 2 * n + 1 and jw >= n:
                    Phi[:, iu, jw] = Rt[:, jw]; continue
                best = np.full(K, NEG); bd = np.zeros(K, dtype=np.int8)
                if iu + 1 <= imax:
                    best = Phi[:, iu + 1, jw] + self.r_right(P, iu, w); bd[:] = 1
                if up_ok_row and lo2 <= iu <= hi2:
                    v = Phi[:, iu, jw + 1] + self.r_up(P, jw, iu, x)
                    upd = v > best; best = np.where(upd, v, best); bd = np.where(upd, 2, bd)
                if jw <= n - 1 and iu == imax:
                    v = Phi[:, self.bound_iu(jw + 1), jw + 1] + self.r_diag(P, jw)
                    upd = v > best; best = np.where(upd, v, best); bd = np.where(upd, 3, bd)
                Phi[:, iu, jw] = best
                if want_paths: dec[:, iu, jw] = bd
        vals = np.array([Phi[k, k if k < n else n, n - k] for k in range(K)])
        self._dec = dec
        return vals, Phi

    # ---- coefficient rows --------------------------------------------------
    def row(self, k):
        n = self.n; nb = self.nb; mid = self.mid; dec = self._dec; o = self.o
        c = np.zeros(self.nvar)
        Qp = c[o['Qp']:o['Qp'] + 2 * n * nb].reshape(n, 2 * nb)      # views
        Qm = c[o['Qm']:o['Qm'] + 2 * n * nb].reshape(n, 2 * nb)
        Pp = c[o['Pp']:o['Pp'] + n]; Sp = c[o['Sp']:o['Sp'] + n]; Pm = c[o['Pm']:o['Pm'] + n]; Sm = c[o['Sm']:o['Sm'] + n]
        esc_val = 2 * (self.bmid + 3)
        nc = self.nc
        Tp = c[o['Tp']:o['Tp'] + nc * n].reshape(nc, n); Tm = c[o['Tm']:o['Tm'] + nc * n].reshape(nc, n)
        kc = min(k, nc)
        def mirror_b(jb, val):       # mirrors with b in bin jb and a > -r0
            Qp[:, jb] += val; Qm[:k, jb] += val
        iu, jw = (k if k < n else n), n - k
        Uc = self.Uc; Wc = self.Wc
        path = [(iu, jw)]
        while True:
            if iu == 2 * n + 1 and jw >= n:
                for j in range(jw, 3 * n + 1):
                    if j >= 2 * n + 1:
                        m = 3 * n - j; val = 2 * (2 - mid[m]) + 2
                        Sp[m] += val
                        jb = self.jb_of_mbin(m)
                        if jb >= 0: mirror_b(jb, val)
                    elif j == 2 * n:
                        c[0] += 4; Pp += 4; Pm[:k] += 4
                    else:
                        i = j - n
                        Pm[i] += 8; Sm[i] += 2 * mid[i] + 2; Qm[i, :] += esc_val
                        jb = self.jb_of_cbin(i)
                        if jb >= 0: mirror_b(jb, 2 * mid[i] + 2)
                        if nc:
                            Tp[:, i] += 8.0; Tm[:kc, i] += 8.0
                            if i < nc: Tm[i, :] += 4.0
                Sm[:k] += 2 * (2 + mid[:k]) + 2
                break
            d = dec[k, iu, jw]; x = Uc[iu]; w = Wc[jw]
            if d == 1:
                if iu <= n - 1:
                    i = iu
                    if k <= i:
                        Pm[i] += mid[i] + w; Sm[i] += mid[i] + w; Qm[i, :] += mid[i] + w
                        if i < nc: Tm[i, :] += mid[i] + w
                    jb = self.jb_of_cbin(i)
                    if jb >= 0: Qp[k:, jb] += mid[i] + w
                    if nc: Tp[kc:, i] += mid[i] + w
                elif iu == n:
                    c[0] += 1 + w; Pp[k:] += 1 + w
                else:
                    m = 2 * n - iu
                    if k <= m: Sp[m] += (2 - mid[m]) + w
                    jb = self.jb_of_mbin(m)
                    if jb >= 0: Qp[k:, jb] += (2 - mid[m]) + w
                iu += 1
            elif d == 2:
                if jw <= n - 1:
                    i = n - 1 - jw; m = -mid[i]
                    if k > i:
                        Pp[i] += (m + x) if iu <= n else 8.0
                        Sp[i] += m + x
                        cau = self.lo_node >= iu
                        Qp[i, :] += np.where(cau, m + x, esc_val)
                        if i < nc: Tp[i, :] += np.where(np.arange(n) >= iu, m + x, 4.0)
                elif jw <= 2 * n - 1:
                    i = jw - n
                    Pm[i] += (mid[i] + x) if iu <= n else 8.0
                    Sm[i] += mid[i] + x
                    cau = self.lo_node >= iu
                    Qm[i, :] += np.where(cau, mid[i] + x, esc_val)
                    jb = self.jb_of_cbin(i)
                    if jb >= 0: mirror_b(jb, mid[i] + x)
                    if nc:
                        capv = (mid[i] + x) if iu <= n else 8.0
                        Tp[:, i] += capv; Tm[:kc, i] += capv
                        if i < nc: Tm[i, :] += np.where(np.arange(n) >= iu, mid[i] + x, 4.0)
                elif jw == 2 * n:
                    c[0] += 1 + x; Pp += 1 + x; Pm[:k] += 1 + x
                else:
                    m = 3 * n - jw
                    Sp[m] += (2 - mid[m]) + x
                    jb = self.jb_of_mbin(m)
                    if jb >= 0: mirror_b(jb, (2 - mid[m]) + x)
                jw += 1
            elif d == 3:
                i = n - 1 - jw
                if k > i:
                    Pp[i] += 8.0; Sp[i] += 2 * (-mid[i]) + 2; Qp[i, :] += esc_val
                    if i < nc: Tp[i, :] += 4.0
                else:
                    Sp[i] += 2 * (2 - mid[i]) - 2
                jb = self.jb_of_mbin(i)
                if jb >= 0: Qp[k:, jb] += 2 * (2 - mid[i]) - 2
                iu = self.bound_iu(jw + 1); jw += 1
            else:
                raise RuntimeError("dead end at %s" % ((k, iu, jw),))
            path.append((iu, jw))
        return c, path


from scipy.sparse import coo_matrix

def refinement_matrix(pc, pcf, r):
    n, nb, nc = pc.n, pc.nb, pc.nc; nf, nbf, ncf = pcf.n, pcf.nb, pcf.nc
    rows = []; cols = []; vals = []
    def add(fi, ci, v): rows.append(fi); cols.append(ci); vals.append(v)
    add(0, 0, 1.0)
    for name in ('Pp', 'Sp', 'Pm', 'Sm'):
        for i in range(n):
            for q in range(r): add(pcf.o[name] + i * r + q, pc.o[name] + i, 1.0 / r)
    for name in ('Qp', 'Qm'):
        for i in range(n):
            for jb in range(2 * nb):
                ci = pc.o[name] + i * 2 * nb + jb
                for q in range(r):
                    for s in range(r):
                        add(pcf.o[name] + (i * r + q) * 2 * nbf + (jb * r + s), ci, 1.0 / (r * r))
    for name in ('Tp', 'Tm'):
        for i in range(nc):
            for j in range(n):
                ci = pc.o[name] + i * n + j
                for q in range(r):
                    for s in range(r):
                        add(pcf.o[name] + (i * r + q) * nf + (j * r + s), ci, 1.0 / (r * r))
    return coo_matrix((vals, (rows, cols)), shape=(pcf.nvar, pc.nvar)).tocsr()

def solve(g, nb, nc, r=2, iters=4000, tol=5e-7, verbose=True):
    g = np.asarray(g, float); n = len(g) - 1
    pc = Continuum(g, nb, nc)
    gf = np.concatenate([np.linspace(g[i], g[i + 1], r + 1)[:-1] for i in range(n)] + [[1.0]])
    pcf = Continuum(gf, nb * r, nc * r)
    A = refinement_matrix(pc, pcf, r)
    mu = np.zeros(pc.nvar); mu[0] = 1.0
    rows = []; v = -np.inf; duals = None; paths = []
    bounds = [(0, None if np.isinf(u) else 0.0) for u in pc.ub] + [(None, None)]
    for it in range(iters):
        muf = A @ mu
        vals, _ = pcf.dp(muf)
        ub = vals.max() / 4
        if verbose: print(f"it {it:3d} rows {len(rows):5d} LP {v:.9f} BR {ub:.9f} gap {ub - v:.2e}", flush=True)
        if ub - v < tol: break
        for k in np.argsort(-vals):
            if vals[k] / 4 > v + tol * 0.5:
                cf, p = pcf.row(k)
                c = A.T @ cf
                if abs(c @ mu - vals[k]) > 1e-8: print("row mismatch", k, c @ mu, vals[k])
                rows.append(c / 4); paths.append((k, p))
        Am = np.array(rows)
        cobj = np.zeros(pc.nvar + 1); cobj[-1] = 1
        A_ub = np.hstack([Am, -np.ones((len(rows), 1))])
        A_eq = np.zeros((1, pc.nvar + 1)); A_eq[0, :pc.nvar] = 1
        res = linprog(cobj, A_ub=A_ub, b_ub=np.zeros(len(rows)), A_eq=A_eq, b_eq=[1.0], bounds=bounds, method="highs")
        if res.status != 0: raise RuntimeError(res.message)
        mu = res.x[:pc.nvar]; v = res.x[-1]; duals = -res.ineqlin.marginals
    return pc, pcf, A, mu, v, ub, rows, paths, duals

if __name__ == "__main__":
    import argparse
    ap = argparse.ArgumentParser(description="Continuum LP: one-turn paths with turn levels near 1, optional two-turn paths.")
    ap.add_argument("n", type=int, help="uniform bins on [0,1]")
    ap.add_argument("nb", type=int, help="level bins on each side of b = 1")
    ap.add_argument("nc", type=int, help="start bins |c| < nc/n of the two-turn family (0 = one-turn only)")
    ap.add_argument("--refine", type=int, default=2, help="refinement of the Princess mesh")
    ap.add_argument("--check", type=int, nargs="*", default=[4], help="also evaluate the response on these finer meshes")
    ap.add_argument("--verbose", action="store_true")
    a = ap.parse_args()
    g = np.linspace(0, 1, a.n + 1)
    t0 = time.time()
    pc, pcf, A, mu, v, ub, rows, paths, duals = solve(g, a.nb, a.nc, a.refine, verbose=a.verbose)
    print("bins", a.n, "level bins", a.nb, "two-turn start bins", a.nc, "refine", a.refine,
          "LP value", v, "response", ub, "time", round(time.time() - t0, 1), flush=True)
    e, Pp, Sp, Pm, Sm, Qp, Qm = pc.unpack(mu); Tp, Tm = pc.unpackT(mu)
    print("sweep %.5f  P_1(a>0) %.5f  S(a>0) %.5f  P_1(a<0) %.5f  S(a<0) %.5f  other levels %.5f  two-turn %.5f"
          % (e, Pp.sum(), Sp.sum(), Pm.sum(), Sm.sum(), Qp.sum() + Qm.sum(), Tp.sum() + Tm.sum()))
    for r in a.check:
        gf = np.concatenate([np.linspace(g[i], g[i + 1], r + 1)[:-1] for i in range(a.n)] + [[1.0]])
        fine = Continuum(gf, a.nb * r, a.nc * r)
        vals, _ = fine.dp(refinement_matrix(pc, fine, r) @ mu, want_paths=False)
        print("  response on the mesh refined %d times: %.10f" % (r, vals.max() / 4), flush=True)
