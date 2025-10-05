# pieza.py
# Definición de piezas base como lista de celdas (r, c) con origen en (0,0)
# y utilidades para generar rotaciones/reflejos únicas.

from typing import List, Tuple, Set

Coord = Tuple[int, int]

# Piezas ejemplo (agrega más según necesites)
PIECES_BASE = {
    "I1": [(0, 0)],                          # 1 celda
    "I2": [(0, 0), (0, 1)],                  # 2 en línea
    "I3": [(0, 0), (0, 1), (0, 2)],          # 3 en línea
    "L3": [(0, 0), (1, 0), (1, 1)],          # L de 3
    "L5": [(0,0), (1,0), (2,0), (3,0), (3,1)],  # L de 5
    "T4": [(0,0), (0,1), (0,2), (1,1)],      # T de 4
    "Z4": [(0,0), (0,1), (1,1), (1,2)],      # Z de 4
}

def _normalize(cells: List[Coord]) -> List[Coord]:
    """Traslada las celdas para que el mínimo r y c sean 0 (origen normalizado)."""
    min_r = min(r for r, _ in cells)
    min_c = min(c for _, c in cells)
    norm = sorted([(r - min_r, c - min_c) for r, c in cells])
    return norm

def _rot90(c: Coord) -> Coord:
    r, c0 = c
    return (c0, -r)

def _reflect(c: Coord) -> Coord:
    r, c0 = c
    return (r, -c0)

def generar_orientaciones(piece_id: str) -> List[List[Coord]]:
    """
    Genera rotaciones (0,90,180,270) y reflejo de la pieza_id.
    Devuelve listas de celdas únicas (normalizadas) para cada orientación.
    """
    base = PIECES_BASE[piece_id]
    variantes: Set[Tuple[Coord, ...]] = set()

    # Generar: 4 rotaciones de base y de su reflejo
    bases = [base]
    # reflejada horizontal
    reflejada = [_reflect(c) for c in base]
    bases.append(reflejada)

    for shape in bases:
        cur = shape
        for _ in range(4):
            norm = tuple(_normalize(cur))
            variantes.add(norm)
            # rotar 90 para próxima
            cur = [_rot90(c) for c in cur]

    # Ordenamos por tamaño y luego lexicográfico para estabilidad
    orientaciones = [list(o) for o in sorted(list(variantes))]
    return orientaciones
