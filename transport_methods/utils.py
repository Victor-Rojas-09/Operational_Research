import numpy as np
import pandas as pd


def costo_total(x: np.ndarray, costos: np.ndarray) -> float:
    """Calculate the total transportation cost given an allocation x."""
    return float((x * costos).sum())


def mostrar_tabla(x: np.ndarray, costos: np.ndarray, titulo: str = "Asignación") -> None:
    """Print the allocation table with its total cost."""
    m, n = x.shape
    df = pd.DataFrame(
        x.astype(int),
        index=[f"O{i+1}" for i in range(m)],
        columns=[f"D{j+1}" for j in range(n)],
    )
    print(f"\n{titulo}")
    print(df.to_string())
    print(f"  → Costo total = {costo_total(x, costos):.2f}")


def mostrar_resumen(resultados: dict) -> None:
    """ Print a comparative summary of all methods. results = {"Method name": cost, ...} """
    print("\n" + "=" * 60)
    print("   RESUMEN COMPARATIVO DE METODOS")
    print("=" * 60)
    costos_vals = list(resultados.values())
    minimo      = min(costos_vals)
    for nombre, costo in resultados.items():
        marca = "  OPTIMO" if costo == minimo else ""
        print(f"  {nombre:<30}: {costo:.2f}{marca}")