import numpy as np
from itertools import product


class SteppingStoneSolver:
    """Stepping Stone Optimizer. It takes an initial solution and steps it down to the optimum. """

    def __init__(self, costos: np.ndarray, verbose: bool = True):
        self.costos  = costos
        self.verbose = verbose
        self.m, self.n = costos.shape

    def resolver(self, x_inicial: np.ndarray):
        """ Optimizes the initial x_allocation. Returns (optimal x, history) """
        x = x_inicial.copy().astype(float)
        historial = []

        if self.verbose:
            print("\n" + "=" * 60)
            print("   ALGORITMO STEPPING STONE — OPTIMIZACION")
            print("=" * 60)

        for iteracion in range(1, 100):
            costo_actual = self._costo_total(x)
            reducidos = self._calcular_costos_reducidos(x)

            if self.verbose:
                print(f"\n--- Iteracion {iteracion} | Costo actual: {costo_actual:.2f} ---")
                print("Costos reducidos (celdas no basicas):")
                for (i, j), val in sorted(reducidos.items()):
                    marca = "✓" if val >= 0 else "↓ "
                    print(f"  Δc({i+1},{j+1}) = {val:+.4f}  {marca}")

            historial.append({
                "iteracion": iteracion,
                "costo":     costo_actual,
                "x":         x.copy(),
            })

            negativos = {k: v for k, v in reducidos.items() if v < -1e-9}
            if not negativos:
                if self.verbose:
                    print("\n SOLUCION OPTIMA ALCANZADA — todos los Δc ≥ 0")
                break

            entrante = min(negativos, key=negativos.get)
            if self.verbose:
                print(f"\nCelda entrante: ({entrante[0]+1},{entrante[1]+1})  "
                      f"Δc = {negativos[entrante]:+.4f}")

            bas_set = set(zip(*np.where(x > 0)))
            ciclo   = self._encontrar_ciclo(bas_set, entrante[0], entrante[1])

            if ciclo is None:
                print("No se encontró ciclo.")
                break

            if self.verbose:
                print(f"Ciclo: {[(c[0]+1, c[1]+1) for c in ciclo]}")

            posiciones_resta = [ciclo[k] for k in range(1, len(ciclo), 2)]
            theta            = min(x[i][j] for i, j in posiciones_resta)

            if self.verbose:
                print(f"θ = {theta:.2f}")

            for k, (ci, cj) in enumerate(ciclo):
                if k % 2 == 0:
                    x[ci, cj] += theta
                else:
                    x[ci, cj] -= theta
                    if x[ci, cj] < 1e-9:
                        x[ci, cj] = 0.0

        return x, historial

    def _costo_total(self, x: np.ndarray) -> float:
        return float((x * self.costos).sum())

    def _encontrar_ciclo(self, bas_set, i0, j0):
        m, n = self.m, self.n

        def dfs(camino, buscando_fila):
            cur_i, cur_j = camino[-1]
            if buscando_fila:
                for j in range(n):
                    if j == cur_j:
                        continue
                    candidato = (cur_i, j)
                    if len(camino) >= 4 and candidato == (i0, j0):
                        return camino
                    if candidato in bas_set and candidato not in camino:
                        res = dfs(camino + [candidato], False)
                        if res:
                            return res
            else:
                for i in range(m):
                    if i == cur_i:
                        continue
                    candidato = (i, cur_j)
                    if len(camino) >= 4 and candidato == (i0, j0):
                        return camino
                    if candidato in bas_set and candidato not in camino:
                        res = dfs(camino + [candidato], True)
                        if res:
                            return res
            return None

        return dfs([(i0, j0)], True)

    def _calcular_costos_reducidos(self, x: np.ndarray) -> dict:
        bas_set   = set(zip(*np.where(x > 0)))
        reducidos = {}
        for i0, j0 in product(range(self.m), range(self.n)):
            if (i0, j0) in bas_set:
                continue
            ciclo = self._encontrar_ciclo(bas_set, i0, j0)
            if ciclo is None:
                continue
            delta = sum(
                self.costos[ci, cj] * (1 if k % 2 == 0 else -1)
                for k, (ci, cj) in enumerate(ciclo)
            )
            reducidos[(i0, j0)] = round(delta, 8)
        return reducidos