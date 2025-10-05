# repositorio_piezas.py
# Catálogo oficial de piezas de Blokus + cache de orientaciones
from typing import Dict, List, Tuple, Set

Coord = Tuple[int, int]

# --- 21 piezas oficiales ---
PIECES_BASE: Dict[str, List[Coord]] = {
    # Monomino (1)
    "I1": [(0, 0)],

    # Domino (1)
    "I2": [(0, 0), (0, 1)],

    # Trominoes (2)
    "I3": [(0, 0), (0, 1), (0, 2)],
    "L3": [(0, 0), (1, 0), (1, 1)],

    # Tetrominoes (5) — (S se obtiene como reflejo de Z)
    "I4": [(0, 0), (0, 1), (0, 2), (0, 3)],
    "O4": [(0, 0), (0, 1), (1, 0), (1, 1)],
    "L4": [(0, 0), (1, 0), (2, 0), (2, 1)],
    "T4": [(0, 0), (0, 1), (0, 2), (1, 1)],
    "Z4": [(0, 0), (0, 1), (1, 1), (1, 2)],

    # Pentominoes (12)
    "F5": [(0, 0), (0, 1), (1, 1), (1, 2), (2, 1)],               # F
    "I5": [(0, 0), (0, 1), (0, 2), (0, 3), (0, 4)],               # I
    "L5": [(0, 0), (1, 0), (2, 0), (3, 0), (3, 1)],               # L
    "P5": [(0, 0), (0, 1), (1, 0), (1, 1), (2, 0)],               # P
    "N5": [(0, 0), (1, 0), (2, 0), (2, 1), (3, 1)],               # N
    "T5": [(0, 0), (0, 1), (0, 2), (1, 1), (2, 1)],               # T
    "U5": [(0, 0), (0, 2), (1, 0), (1, 1), (1, 2)],               # U
    "V5": [(0, 0), (1, 0), (2, 0), (2, 1), (2, 2)],               # V
    "W5": [(0, 0), (1, 0), (1, 1), (2, 1), (2, 2)],               # W
    "X5": [(1, 1), (0, 1), (1, 0), (1, 2), (2, 1)],               # X (cruz)
    "Y5": [(0, 0), (1, 0), (2, 0), (3, 0), (2, 1)],               # Y
    "Z5": [(0, 0), (0, 1), (1, 1), (2, 1), (2, 2)],               # Z
}

# ---------------- utilidades geométricas ----------------
def _normalize(cells: List[Coord]) -> List[Coord]:
    min_r = min(r for r, _ in cells)
    min_c = min(c for _, c in cells)
    return sorted([(r - min_r, c - min_c) for r, c in cells])

def _rot90(c: Coord) -> Coord:
    r, c = c
    return (c, -r)

def _reflect(c: Coord) -> Coord:
    r, c = c
    return (r, -c)

# ---------------- repositorio con cache ----------------
class RepositorioPiezas:
    def __init__(self, base: Dict[str, List[Coord]] = None):
        self.base = base if base is not None else PIECES_BASE
        self._cache_orient: Dict[str, List[List[Coord]]] = {}

    def ids(self) -> List[str]:
        return list(self.base.keys())

    def tam(self, pieza_id: str) -> int:
        return len(self.base[pieza_id])

    def base_coords(self, pieza_id: str) -> List[Coord]:
        return self.base[pieza_id]

    def orientaciones(self, pieza_id: str) -> List[List[Coord]]:
        """Devuelve todas las orientaciones únicas (rotaciones + reflejos). Usa cache."""
        if pieza_id in self._cache_orient:
            return self._cache_orient[pieza_id]

        base = self.base[pieza_id]
        variantes: Set[Tuple[Coord, ...]] = set()

        shapes = [base, [_reflect(c) for c in base]]
        for shape in shapes:
            cur = shape
            for _ in range(4):
                variantes.add(tuple(_normalize(cur)))
                cur = [_rot90(c) for c in cur]

        orient = [list(v) for v in sorted(list(variantes))]
        self._cache_orient[pieza_id] = orient
        return orient

# Instancia global cómoda
PIEZAS = RepositorioPiezas()
