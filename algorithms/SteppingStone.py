import numpy as np
from itertools import product
from typing import Any, Dict, List, Optional, Set, Tuple

class SteppingStone:
    """
    Stepping Stone optimization method for transportation problems.
    Supports explicit basic variables, verbose tracing, and robust cycle search.
    """

    def optimize(
        self,
        init_allocation: np.ndarray,
        transportation_costs: np.ndarray,
        basic_cells: Optional[Set[Tuple[int, int]]] = None,
        verbose: bool = False,
    ) -> Tuple[np.ndarray, List[Dict[str, Any]]]:
        """
        Optimize a feasible transportation solution using
        the Stepping Stone method.

        Returns:
            (x_optima, history)
        """
        total_rows, total_columns = transportation_costs.shape
        x = init_allocation.copy().astype(float)

        if basic_cells is None:
            basic_cells = set(zip(*np.where(x > 0)))

        history: List[Dict[str, Any]] = []

        if verbose:
            print("\n" + "=" * 60)
            print("   ALGORITMO STEPPING STONE — OPTIMIZACIÓN")
            print("=" * 60)

        for iteration_number in range(1, 100):
            current_total_cost = self._total_cost(x, transportation_costs)
            reduced_costs = self.compute_reduced_costs(
                x,
                transportation_costs,
                basic_cells,
            )

            history.append({
                "iteration": iteration_number,
                "cost": current_total_cost,
                "allocation": x.copy(),
            })

            if verbose:
                print(f"\n--- Iteración {iteration_number} | Costo actual: {current_total_cost:.2f} ---")
                print("Costos reducidos (celdas no básicas):")
                for (row, col), value in sorted(reduced_costs.items()):
                    marca = "✓" if value >= 0 else "↓ "
                    print(f"  Δc({row+1},{col+1}) = {value:+.4f}  {marca}")

            improving_moves = {
                cell: value
                for cell, value in reduced_costs.items()
                if value < -1e-9
            }

            if not improving_moves:
                if verbose:
                    print("\n✔ SOLUCIÓN ÓPTIMA ALCANZADA — todos los Δc ≥ 0")
                break

            entering_cell = min(improving_moves, key=improving_moves.get)
            if verbose:
                print(f"\nCelda entrante: ({entering_cell[0]+1},{entering_cell[1]+1})  "
                      f"Δc = {improving_moves[entering_cell]:+.4f}")

            cycle = self.find_cycle(
                basic_cells,
                entering_cell,
                total_rows,
                total_columns,
            )

            if cycle is None:
                if verbose:
                    print("No se encontró ciclo para la celda entrante.")
                break

            cycle_nodes = cycle[:-1]
            subtracting_cells = [
                cycle_nodes[index]
                for index in range(1, len(cycle_nodes), 2)
            ]

            theta = min(x[row, col] for row, col in subtracting_cells)

            if verbose:
                print(f"Ciclo: {[(row+1, col+1) for row, col in cycle_nodes]}")
                print(f"θ = {theta:.2f}")

            for cycle_index, (row, col) in enumerate(cycle_nodes):
                if cycle_index % 2 == 0:
                    x[row, col] += theta
                else:
                    x[row, col] -= theta
                    if x[row, col] < 1e-9:
                        x[row, col] = 0.0

            basic_cells.add(entering_cell)
            for row, col in subtracting_cells:
                if abs(x[row, col]) < 1e-9 and (row, col) != entering_cell:
                    basic_cells.remove((row, col))
                    break

        return x, history

    def _total_cost(self, allocation: np.ndarray, costs: np.ndarray) -> float:
        return float((allocation * costs).sum())

    def compute_reduced_costs(
        self,
        allocation_matrix: np.ndarray,
        transportation_costs: np.ndarray,
        basic_cells: Set[Tuple[int, int]],
    ) -> Dict[Tuple[int, int], float]:
        """
        Compute reduced costs for all non-basic cells.
        """
        total_rows, total_columns = transportation_costs.shape

        reduced_costs: Dict[Tuple[int, int], float] = {}

        for row_index, column_index in product(range(total_rows), range(total_columns)):
            current_cell = (row_index, column_index)
            if current_cell in basic_cells:
                continue

            cycle = self.find_cycle(
                basic_cells,
                current_cell,
                total_rows,
                total_columns,
            )
            if cycle is None:
                continue

            cycle_nodes = cycle[:-1]
            reduced_cost = 0.0
            for cycle_index, (cycle_row, cycle_column) in enumerate(cycle_nodes):
                if cycle_index % 2 == 0:
                    reduced_cost += transportation_costs[cycle_row, cycle_column]
                else:
                    reduced_cost -= transportation_costs[cycle_row, cycle_column]

            reduced_costs[current_cell] = round(reduced_cost, 8)

        return reduced_costs

    def find_cycle(
        self,
        basic_cells: Set[Tuple[int, int]],
        start_cell: Tuple[int, int],
        total_rows: int,
        total_columns: int,
    ) -> Optional[List[Tuple[int, int]]]:
        """
        Find a valid Stepping Stone cycle.
        """
        working_basic_cells = basic_cells.copy()
        working_basic_cells.add(start_cell)

        def dfs(
            current_path: List[Tuple[int, int]],
            search_horizontally: bool,
        ) -> Optional[List[Tuple[int, int]]]:
            current_row, current_column = current_path[-1]

            if search_horizontally:
                for next_column in range(total_columns):
                    if next_column == current_column:
                        continue

                    candidate_cell = (current_row, next_column)
                    if candidate_cell == start_cell and len(current_path) >= 4:
                        return current_path + [start_cell]
                    if candidate_cell in working_basic_cells and candidate_cell not in current_path:
                        result = dfs(current_path + [candidate_cell], False)
                        if result is not None:
                            return result
            else:
                for next_row in range(total_rows):
                    if next_row == current_row:
                        continue
                    candidate_cell = (next_row, current_column)
                    if candidate_cell == start_cell and len(current_path) >= 4:
                        return current_path + [start_cell]
                    if candidate_cell in working_basic_cells and candidate_cell not in current_path:
                        result = dfs(current_path + [candidate_cell], True)
                        if result is not None:
                            return result
            return None

        return dfs([start_cell], True) or dfs([start_cell], False)
