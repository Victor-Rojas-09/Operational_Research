import numpy as np
import matplotlib.pyplot as plt
from ui.utils import costo_total

def graficar_historial(historial: list) -> None:
    """Graph the convergence of the cost over the iterations."""
    iters  = [h["iteracion"] for h in historial]
    costos = [h["costo"]     for h in historial]

    plt.figure(figsize=(8, 4))
    plt.plot(iters, costos, marker="o", color="steelblue", linewidth=2.5, markersize=9)
    for i, c in zip(iters, costos):
        plt.annotate(
            f"{c:.0f}", (i, c),
            textcoords="offset points", xytext=(0, 10),
            ha="center", fontsize=9, fontweight="bold",
        )
    plt.xlabel("Iteración", fontsize=12)
    plt.ylabel("Costo Total", fontsize=12)
    plt.title("Convergencia del Algoritmo Stepping Stone", fontsize=14, fontweight="bold")
    plt.xticks(iters)
    plt.grid(alpha=0.35)
    plt.tight_layout()
    plt.show()

def graficar_comparacion(
        x_inicial:  np.ndarray,
        x_optima:   np.ndarray,
        costos:     np.ndarray,
        label_ini:  str = "Solución Inicial",
    ) -> None:
    """Show heatmaps side by side: initial solution vs optimal solution."""
    m, n = costos.shape
    fig, axes = plt.subplots(1, 2, figsize=(14, 5))

    titulos = [
        f"{label_ini}\nCosto = {costo_total(x_inicial, costos):.0f}",
        f"Solucion Optima (Stepping Stone)\nCosto = {costo_total(x_optima, costos):.0f}",
    ]

    for ax, x, titulo in zip(axes, [x_inicial, x_optima], titulos):
        ax.imshow(x, cmap="Blues", aspect="auto", vmin=0)
        ax.set_title(titulo, fontsize=11, fontweight="bold", pad=12)
        ax.set_xticks(range(n))
        ax.set_xticklabels([f"D{j+1}" for j in range(n)], fontsize=10)
        ax.set_yticks(range(m))
        ax.set_yticklabels([f"O{i+1}" for i in range(m)], fontsize=10)

        for i in range(m):
            for j in range(n):
                val = int(x[i, j])
                txt = f"{val}\n(c={int(costos[i, j])})"
                clr = "white" if val > 60 else "black"
                fw = "bold"  if val > 0  else "normal"
                ax.text(j, i, txt, ha="center", va="center",
                        fontsize=9, color=clr, fontweight=fw)
    plt.tight_layout()
    plt.show()