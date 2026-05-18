import numpy as np

class EsquinaNoroeste:
    """Northwest Corner Method for initial solution."""
    @staticmethod
    def resolver(costos: np.ndarray, oferta: np.ndarray, demanda: np.ndarray) -> np.ndarray:
        m, n = costos.shape
        x = np.zeros((m, n))
        o = oferta.copy()
        d = demanda.copy()
        i, j = 0, 0

        while i < m and j < n:
            asig = min(o[i], d[j])
            x[i, j] = asig
            o[i] -= asig
            d[j] -= asig
            if np.isclose(o[i], 0) and np.isclose(d[j], 0):
                if i + 1 < m:
                    i += 1
                else:
                    j += 1
            elif np.isclose(o[i], 0):
                i += 1
            else:
                j += 1
        return x

class CostoMinimo:
    """Minimum Cost Method for initial solution."""
    @staticmethod
    def resolver(costos: np.ndarray, oferta: np.ndarray, demanda: np.ndarray) -> np.ndarray:
        m, n = costos.shape
        x = np.zeros((m, n))
        o = oferta.copy()
        d = demanda.copy()
        c = costos.copy()

        while o.sum() > 1e-9 and d.sum() > 1e-9:
            mascara = c < np.inf
            if not mascara.any():
                break
            idx = np.unravel_index(np.where(mascara, c, np.inf).argmin(), c.shape)
            i, j = idx
            asig = min(o[i], d[j])
            x[i, j] = asig
            o[i] -= asig
            d[j] -= asig
            if np.isclose(o[i], 0):
                c[i, :] = np.inf
            if np.isclose(d[j], 0):
                c[:, j] = np.inf
        return x

class Vogel:
    """Vogel's approximation method for initial solution."""
    @staticmethod
    def resolver(costos: np.ndarray, oferta: np.ndarray, demanda: np.ndarray) -> np.ndarray:
        m, n = costos.shape
        x = np.zeros((m, n))
        o = oferta.copy()
        d = demanda.copy()
        c = costos.copy()
        fila_activa = [True] * m
        col_activa = [True] * n

        def pen_fila(i):
            vals = sorted(c[i, j] for j in range(n) if col_activa[j])
            return (vals[1] - vals[0]) if len(vals) >= 2 else 0

        def pen_col(j):
            vals = sorted(c[i, j] for i in range(m) if fila_activa[i])
            return (vals[1] - vals[0]) if len(vals) >= 2 else 0

        for _ in range(m + n - 1):
            if o.sum() < 1e-9 or d.sum() < 1e-9:
                break
            pf = [(pen_fila(i), i, 'f') for i in range(m) if fila_activa[i]]
            pc = [(pen_col(j),  j, 'c') for j in range(n) if col_activa[j]]
            todas = sorted(pf + pc, reverse=True)
            if not todas:
                break
            _, sel, tipo = todas[0]
            if tipo == 'f':
                i_sel = sel
                j_sel = min((j for j in range(n) if col_activa[j]),  key=lambda j: c[i_sel, j])
            else:
                j_sel = sel
                i_sel = min((i for i in range(m) if fila_activa[i]), key=lambda i: c[i, j_sel])
            asig = min(o[i_sel], d[j_sel])
            x[i_sel, j_sel] = asig
            o[i_sel] -= asig
            d[j_sel] -= asig
            if np.isclose(o[i_sel], 0):
                fila_activa[i_sel] = False
                c[i_sel, :]        = np.inf
            if np.isclose(d[j_sel], 0):
                col_activa[j_sel] = False
                c[:, j_sel]       = np.inf
        return x