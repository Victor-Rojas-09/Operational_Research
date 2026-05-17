import numpy as np

def ingresar_problema():
    """
    Define la matriz de costos, oferta y demanda del problema de transporte.
    Si el problema no está balanceado, agrega fila/columna ficticia automáticamente.
    Retorna: (costos, oferta, demanda)
    """
    costos = np.array([
        [5, 2, 7, 3],
        [3, 6, 6, 1],
        [6, 1, 2, 4],
        [4, 3, 6, 6],
    ], dtype=float)

    oferta  = np.array([80, 30, 60, 45], dtype=float)
    demanda = np.array([70, 40, 70, 35], dtype=float)

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