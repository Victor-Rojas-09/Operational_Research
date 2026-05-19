import pandas as pd
from transport_methods import (
    ingresar_problema,
    NorthWestCorner,
    MinimumCostMethod,
    VogelApproximation,
    SteppingStoneSolver,
    costo_total,
    mostrar_tabla,
    mostrar_resumen,
    graficar_historial,
    graficar_comparacion,
)

def separador(titulo: str = "") -> None:
    ancho = 60
    print("\n" + "=" * ancho)
    if titulo:
        print(f"   {titulo}")
        print("=" * ancho)

def pedir_opcion(opciones: list[str], prompt: str = "Elige una opción") -> int:
    """Shows a numbered menu and returns the chosen (0-based) index."""
    for idx, op in enumerate(opciones, 1):
        print(f"  [{idx}] {op}")
    while True:
        try:
            val = int(input(f"\n{prompt} (1-{len(opciones)}): "))
            if 1 <= val <= len(opciones):
                return val - 1
            print(f"  Ingresa un numero entre 1 y {len(opciones)}.")
        except ValueError:
            print("  Entrada invalida, intenta de nuevo.")

METODOS_INICIALES = {
    "NorthWestCorner": NorthWestCorner,
    "Costo Mínimo":     MinimumCostMethod,
    "VogelApproximation":            VogelApproximation,
}


def cargar_problema():
    separador("DATOS DEL PROBLEMA")
    costos, oferta, demanda = ingresar_problema()
    m, n = costos.shape
    print(f"\nMatriz de costos ({m}×{n}):")
    print(pd.DataFrame(
        costos.astype(int),
        index=[f"O{i+1}" for i in range(m)],
        columns=[f"D{j+1}" for j in range(n)],
    ).to_string())
    print(f"\nOferta : {oferta.astype(int).tolist()}")
    print(f"Demanda: {demanda.astype(int).tolist()}")
    return costos, oferta, demanda


def menu_solucion_inicial(costos, oferta, demanda):
    """Calcula y muestra la solucion inicial con el metodo elegido."""
    separador("SOLUCION INICIAL")
    nombres  = list(METODOS_INICIALES.keys())
    opciones = nombres + ["Mostrar los tres metodos"]
    idx      = pedir_opcion(opciones, "Selecciona el metodo de solucion inicial")

    if idx < len(nombres):                          # un solo método
        nombre = nombres[idx]
        x = METODOS_INICIALES[nombre].resolver(costos, oferta, demanda)
        mostrar_tabla(x, costos, f"Asignacion — {nombre}")
        return nombre, x
    else:                                           # los tres
        resultados = {}
        ultima_x   = None
        for nombre, Clase in METODOS_INICIALES.items():
            separador(nombre.upper())
            x = Clase.resolver(costos, oferta, demanda)
            mostrar_tabla(x, costos, f"Asignacion — {nombre}")
            resultados[nombre] = costo_total(x, costos)
            ultima_x = (nombre, x)
        mostrar_resumen(resultados)
        return ultima_x          # devuelve el último calculado


def menu_optimizar(costos, nombre_inicial, x_inicial):
    """Corre Stepping Stone desde la solución inicial dada."""
    separador(f"OPTIMIZACIÓN — STEPPING STONE (desde {nombre_inicial})")
    verbose_idx = pedir_opcion(
        ["Mostrar detalle de cada iteracion", "Solo mostrar resultado final"],
        "Nivel de detalle"
    )
    verbose = verbose_idx == 0

    solver        = SteppingStoneSolver(costos, verbose=verbose)
    x_opt, historial = solver.resolver(x_inicial)

    mostrar_tabla(x_opt, costos, "\nAsignación Optima Final")

    ahorro = costo_total(x_inicial, costos) - costo_total(x_opt, costos)
    pct    = ahorro / costo_total(x_inicial, costos) * 100
    print(f"\n  Ahorro vs solución inicial: {ahorro:.2f}  ({pct:.1f}%)")

    return x_opt, historial


def menu_graficas(costos, oferta, demanda, x_inicial, nombre_inicial, x_opt, historial):
    separador("VISUALIZACIONES")
    opciones = [
        "Convergencia del Stepping Stone",
        "Comparación solución inicial vs óptima",
        "Ambas gráficas",
        "Volver al menú principal",
    ]
    idx = pedir_opcion(opciones, "¿Qué quieres graficar?")

    if idx == 0:
        graficar_historial(historial)
    elif idx == 1:
        graficar_comparacion(x_inicial, x_opt, costos, label_ini=f"Inicial ({nombre_inicial})")
    elif idx == 2:
        graficar_historial(historial)
        graficar_comparacion(x_inicial, x_opt, costos, label_ini=f"Inicial ({nombre_inicial})")

def main():
    print("\n" + "=" * 60)
    print("   INVESTIGACION DE OPERACIONES — METODOS DE TRANSPORTE")
    print("=" * 60)

    # Cargar el problema una sola vez
    costos, oferta, demanda = cargar_problema()

    nombre_inicial = None
    x_inicial      = None
    x_opt          = None
    historial      = []

    MENU_PRINCIPAL = [
        "Calcular solucion inicial",
        "Optimizar con Stepping Stone",
        "Ver graficas",
        "Resumen comparativo (los 3 metodos + optimo)",
        "Salir",
    ]

    while True:
        separador("MENÚ PRINCIPAL")
        idx = pedir_opcion(MENU_PRINCIPAL)

        # ── Initial solution ──────────────────────────────────────
        if idx == 0:
            nombre_inicial, x_inicial = menu_solucion_inicial(costos, oferta, demanda)

        # ── Optimizate ─────────────────────────────────────────────
        elif idx == 1:
            if x_inicial is None:
                print("\n  Primero debes calcular una solución inicial (opcion 1).")
                continue
            x_opt, historial = menu_optimizar(costos, nombre_inicial, x_inicial)

        # ── Graphs──────────────────────────────────────────────
        elif idx == 2:
            if x_opt is None:
                print("\n  Primero optimiza la solución (opcion 2).")
                continue
            menu_graficas(costos, oferta, demanda, x_inicial, nombre_inicial, x_opt, historial)

        # ── Complete summary ──────────────────────────────────────
        elif idx == 3:
            separador("RESUMEN COMPLETO")
            resultados = {}
            for nombre, Clase in METODOS_INICIALES.items():
                x = Clase.resolver(costos, oferta, demanda)
                resultados[nombre] = costo_total(x, costos)

            if x_opt is not None:
                resultados["Stepping Stone (óptimo)"] = costo_total(x_opt, costos)

            mostrar_resumen(resultados)

        # ── Exit ─────────────────────────────────────────────────
        elif idx == 4:
            print("\n  Hasta luego!\n")
            break
        
if __name__ == "__main__":
    main()