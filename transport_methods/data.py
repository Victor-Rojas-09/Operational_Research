import numpy as np

def _balancear(costos, oferta, demanda):
    total_oferta  = oferta.sum()
    total_demanda = demanda.sum()
    print(f"Oferta total  : {total_oferta}")
    print(f"Demanda total : {total_demanda}")

    if not np.isclose(total_oferta, total_demanda):
        print("Problema NO balanceado — se agrega variable ficticia.")
        if total_oferta > total_demanda:
            diff    = total_oferta - total_demanda
            demanda = np.append(demanda, diff)
            costos  = np.hstack([costos, np.zeros((costos.shape[0], 1))])
        else:
            diff   = total_demanda - total_oferta
            oferta = np.append(oferta, diff)
            costos = np.vstack([costos, np.zeros((1, costos.shape[1]))])
        print("Problema balanceado con variable ficticia.")
    else:
        print("Problema balanceado.")
    return costos, oferta, demanda


def _problema_default():
    costos = np.array([
        [5, 2, 7, 3],
        [3, 6, 6, 1],
        [6, 1, 2, 4],
        [4, 3, 6, 6],
    ], dtype=float)
    oferta  = np.array([80, 30, 60, 45], dtype=float)
    demanda = np.array([70, 40, 70, 35], dtype=float)
    return costos, oferta, demanda


def _problema_manual():
    from __main__ import pedir_entero, pedir_flotante  

    print("\n  Ingresa las dimensiones de la matriz de costos.")
    m = pedir_entero("  Número de orígenes (filas) ", minimo=1)
    n = pedir_entero("  Número de destinos (columnas)", minimo=1)

    print(f"\n  Ingresa la matriz de costos ({m}×{n}) fila por fila.")
    costos = np.zeros((m, n), dtype=float)
    for i in range(m):
        while True:
            raw = input(f"    Fila O{i+1} ({n} valores separados por espacio): ")
            valores = raw.strip().split()
            if len(valores) != n:
                print(f"    Se esperan exactamente {n} valores, intenta de nuevo.")
                continue
            try:
                costos[i] = [float(v) for v in valores]
                break
            except ValueError:
                print("    Algún valor no es numérico, intenta de nuevo.")

    print(f"\n  Ingresa la oferta de cada origen ({m} valores).")
    oferta = np.zeros(m, dtype=float)
    for i in range(m):
        oferta[i] = pedir_flotante(f"    Oferta O{i+1}")

    print(f"\n  Ingresa la demanda de cada destino ({n} valores).")
    demanda = np.zeros(n, dtype=float)
    for j in range(n):
        demanda[j] = pedir_flotante(f"    Demanda D{j+1}")

    return costos, oferta, demanda


def ingresar_problema(manual: bool = False):
    """
    Returns (costs, supply, demand) — balanced automatically if needed.
    manual=True  → interactive console input
    manual=False → hardcoded default problem
    """
    if manual:
        costos, oferta, demanda = _problema_manual()
    else:
        costos, oferta, demanda = _problema_default()

    return _balancear(costos, oferta, demanda)