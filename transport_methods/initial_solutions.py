import numpy as np

class NorthWestCorner:
    """Northwest Corner Method for initial solution."""
    @staticmethod
    def resolver(costos: np.ndarray, oferta: np.ndarray, demanda: np.ndarray) -> np.ndarray:
        rows, cols = costos.shape
        allocation = np.zeros((rows, cols))
        supply = oferta.copy()
        demand = demanda.copy()
        costs = costos.copy()
        row, column = 0, 0

        # Traverse the matrix starting from the upper-left corner
        while row < rows and column < cols:
            assigned = min(supply[row], demand[column])
            allocation[row, column] = assigned

            # Reduce supply and demand
            supply[row] -= assigned
            demand[column] -= assigned

            # Move according to which value is exhausted
            if np.isclose(supply[row], 0) and np.isclose(demand[column], 0):
                if row + 1 < rows:
                    row += 1
                else:
                    column += 1
            elif np.isclose(supply[row], 0):
                row += 1
            else:
                column += 1
        return allocation

class MinimumCostMethod:
    """Minimum Cost Method for initial solution."""
    @staticmethod
    def resolver(costos: np.ndarray, oferta: np.ndarray, demanda: np.ndarray) -> np.ndarray:
        rows, cols = costos.shape
        allocation = np.zeros((rows, cols))
        supply = oferta.copy()
        demand = demanda.copy()
        costs = costos.copy()

        # Continue while there is remaining supply and demand
        while supply.sum() > 1e-9 and demand.sum() > 1e-9:
            # Select the available cell with the minimum cost
            mask = (costs < np.inf)

            if not mask.any():
                break
            row, column = np.unravel_index(np.where(mask, costs, np.inf).argmin(), costs.shape)
            assigned = min(supply[row], demand[column])
            allocation[row, column] = assigned

            # Reduce supply and demand
            supply[row] -= assigned
            demand[column] -= assigned

            # Block row if supply is exhausted
            if np.isclose(supply[row], 0):
                costs[row, :] = np.inf

            # Block column if demand is exhausted
            if np.isclose(demand[column], 0):
                costs[:, column] = np.inf
        return allocation

class VogelApproximation:
    """VogelApproximation's approximation method for initial solution."""
    @staticmethod
    def resolver(costos: np.ndarray, oferta: np.ndarray, demanda: np.ndarray) -> np.ndarray:
        rows, cols = costos.shape
        allocation = np.zeros((rows, cols))
        supply = oferta.copy()
        demand = demanda.copy()
        costs = costos.copy()
        active_rows = [True] * rows
        active_cols  = [True] * cols

        # Functions to compute row and column penalties
        def row_penalty(row):
            """
            Calculate row penalties.
            """
            vals = sorted(costs[row, c] for c in range(cols) if active_cols[c])
            return (vals[1] - vals[0]) if len(vals) >= 2 else 0

        def col_penalty(col):
            """
            Calculate column penalties.
            """
            vals = sorted(costs[r, col] for r in range(rows) if active_rows[r])
            return (vals[1] - vals[0]) if len(vals) >= 2 else 0

        # # Iterate until supply and demand are exhausted
        for _ in range(rows + cols - 1):
            if supply.sum() < 1e-9 or demand.sum() < 1e-9:
                break
            penalties = (
                [(row_penalty(r), r, 'row') for r in range(rows) if active_rows[r]] +
                [(col_penalty(c), c, 'col') for c in range(cols) if active_cols[c]]
            )
            if not penalties:
                break

            # Select the highest penalty
            _, selected, kind = max(penalties, key=lambda x: x[0])
            
            if kind == 'row':
                row = selected
                column = min((c for c in range(cols) if active_cols[c]), key=lambda c: costs[row, c])
            else:
                column = selected
                row = min((r for r in range(rows) if active_rows[r]), key=lambda r: costs[r, column])

            assigned = min(supply[row], demand[column])
            allocation[row, column] = assigned

            # Reduce supply and demand
            supply[row] -= assigned
            demand[column] -= assigned

            # Deactivate exhausted row or column
            if np.isclose(supply[row], 0):
                active_rows[row] = False
                costs[row, :] = np.inf

            if np.isclose(demand[column], 0):
                active_cols[column] = False
                costs[:, column] = np.inf
        return allocation