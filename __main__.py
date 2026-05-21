import numpy as np
import pandas as pd
from transport_methods import (
    ingresar_problema,
    NorthWestCorner,
    MinimumCostMethod,
    VogelApproximation,
    costo_total,
    mostrar_tabla,
    mostrar_resumen,
    graficar_historial,
    graficar_comparacion,
)
from algorithms.SteppingStone import SteppingStone
from algorithms.floyd_warshall import floyd_warshall
from algorithms.MST_Algorithm import kruskal_mst

def separador(titulo: str = "") -> None:
    ancho = 60
    print("\n" + "=" * ancho)
    if titulo:
        print(f"   {titulo}")
        print("=" * ancho)

def pedir_opcion(opciones, prompt: str = "Elige una opción") -> int:
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


def pedir_entero(prompt, minimo=0, maximo=None):
    while True:
        try:
            valor = int(input(f"{prompt}: "))
            if valor < minimo or (maximo is not None and valor > maximo):
                if maximo is not None:
                    print(f"  Ingresa un valor entre {minimo} y {maximo}.")
                else:
                    print(f"  Ingresa un valor mayor o igual a {minimo}.")
                continue
            return valor
        except ValueError:
            print("  Entrada invalida, intenta de nuevo.")


def pedir_flotante(prompt):
    while True:
        try:
            return float(input(f"{prompt}: "))
        except ValueError:
            print("  Entrada invalida, intenta de nuevo.")


METODOS_INICIALES = {
    "Esquina Noroeste": NorthWestCorner,
    "Costo Mínimo": MinimumCostMethod,
    "Vogel": VogelApproximation,
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

    solver = SteppingStone()
    x_opt, historial = solver.optimize(x_inicial, costos, verbose=verbose)

    mostrar_tabla(x_opt, costos, "\nAsignación Optima Final")

    ahorro = costo_total(x_inicial, costos) - costo_total(x_opt, costos)
    pct = ahorro / costo_total(x_inicial, costos) * 100
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

def menu_transporte():
    costos, oferta, demanda = cargar_problema()
    nombre_inicial = None
    x_inicial = None
    x_opt = None
    historial = []

    opciones = [
        "Calcular solucion inicial",
        "Optimizar con Stepping Stone",
        "Ver graficas",
        "Resumen comparativo (los 3 metodos + optimo)",
        "Volver",
    ]

    while True:
        separador("MENÚ TRANSPORTE")
        idx = pedir_opcion(opciones)

        if idx == 0:
            nombre_inicial, x_inicial = menu_solucion_inicial(costos, oferta, demanda)
        elif idx == 1:
            if x_inicial is None:
                print("\n  Primero debes calcular una solución inicial (opcion 1).")
                continue
            x_opt, historial = menu_optimizar(costos, nombre_inicial, x_inicial)
        elif idx == 2:
            if x_opt is None:
                print("\n  Primero optimiza la solución (opcion 2).")
                continue
            menu_graficas(costos, oferta, demanda, x_inicial, nombre_inicial, x_opt, historial)
        elif idx == 3:
            separador("RESUMEN COMPLETO")
            resultados = {}
            for nombre, Clase in METODOS_INICIALES.items():
                x = Clase.resolver(costos, oferta, demanda)
                resultados[nombre] = costo_total(x, costos)
            if x_opt is not None:
                resultados["Stepping Stone (óptimo)"] = costo_total(x_opt, costos)
            mostrar_resumen(resultados)
        else:
            break


def menu_mst():
    separador("MST — KRUSKAL")
    opciones = ["Ejemplo por defecto", "Ingresar grafo manual", "Volver"]
    idx = pedir_opcion(opciones)

    if idx == 2:
        return

    if idx == 0:
        num_nodes = 4
        edges = [
            (10, 0, 1),
            (6, 0, 2),
            (5, 0, 3),
            (15, 1, 3),
            (4, 2, 3),
        ]
    else:
        num_nodes = pedir_entero("Número de nodos", minimo=2)
        num_edges = pedir_entero("Número de aristas", minimo=1)
        edges = []
        for i in range(num_edges):
            print(f"\nArista {i+1}")
            u = pedir_entero("  Nodo origen", minimo=0, maximo=num_nodes-1)
            v = pedir_entero("  Nodo destino", minimo=0, maximo=num_nodes-1)
            weight = pedir_flotante("  Peso")
            edges.append((weight, u, v))

    mst_edges, total_cost = kruskal_mst(num_nodes, edges)
    separador("RESULTADO MST")
    print("Aristas del MST:")
    for u, v, weight in mst_edges:
        print(f"  ({u} - {v}) = {weight}")
    print(f"Costo total: {total_cost}")


def menu_floyd():
    separador("FLOYD-WARSHALL")
    opciones = ["Ejemplo por defecto", "Ingresar grafo manual", "Volver"]
    idx = pedir_opcion(opciones)

    if idx == 2:
        return

    if idx == 0:
        number_of_nodes = 4
        weighted_edges = [
            (0, 1, 3),
            (0, 2, 8),
            (1, 2, 2),
            (1, 3, 5),
            (2, 3, 1),
            (3, 0, 2),
        ]
    else:
        number_of_nodes = pedir_entero("Número de nodos", minimo=2)
        num_edges = pedir_entero("Número de aristas", minimo=1)
        weighted_edges = []
        for i in range(num_edges):
            print(f"\nArista {i+1}")
            u = pedir_entero("  Nodo origen", minimo=0, maximo=number_of_nodes-1)
            v = pedir_entero("  Nodo destino", minimo=0, maximo=number_of_nodes-1)
            weight = pedir_flotante("  Peso")
            weighted_edges.append((u, v, weight))

    distance_matrix = floyd_warshall(number_of_nodes, weighted_edges)
    separador("RESULTADO FLOYD-WARSHALL")
    df = pd.DataFrame(
        np.array(distance_matrix),
        index=[f"N{i}" for i in range(number_of_nodes)],
        columns=[f"N{j}" for j in range(number_of_nodes)],
    )
    print(df.replace(np.inf, "INF").to_string())


def main():
    print("\n" + "=" * 60)
    print("   INVESTIGACION DE OPERACIONES — SELECCIÓN DE ALGORITMO")
    print("=" * 60)

    opciones = [
        "Transporte — Stepping Stone",
        "MST — Kruskal",
        "Floyd-Warshall",
        "Salir",
    ]

    while True:
        separador("MENÚ PRINCIPAL")
        opcion = pedir_opcion(opciones)

        if opcion == 0:
            menu_transporte()
        elif opcion == 1:
            menu_mst()
        elif opcion == 2:
            menu_floyd()
        else:
            print("\nLeaving\n")
            break


if __name__ == "__main__":
    main()