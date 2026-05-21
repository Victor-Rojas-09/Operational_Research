# Expone la API pública del paquete para importaciones cortas.

from .data               import ingresar_problema
from .initial_solutions  import NorthWestCorner, MinimumCostMethod, VogelApproximation
from ui.utils import costo_total, mostrar_tabla, mostrar_resumen
from ui.visualization import graficar_historial, graficar_comparacion

__all__ = [
    "ingresar_problema",
    "NorthWestCorner",
    "MinimumCostMethod",
    "VogelApproximation",
    "costo_total",
    "mostrar_tabla",
    "mostrar_resumen",
    "graficar_historial",
    "graficar_comparacion",
]