# mesa.py
from typing import List, Tuple, Dict, Set
from pieza import generar_orientaciones, PIECES_BASE

Coord = Tuple[int, int]

class Mesa:
    def __init__(self, filas: int = 20, columnas: int = 20):
        self.filas = filas
        self.columnas = columnas
        self.grid = [["." for _ in range(columnas)] for _ in range(filas)]
        # Estado por jugador (símbolo -> jugó algo ya?)
        self.jugadores_colocaron: Dict[str, bool] = {}
        # Esquinas por jugador (A,B,C,D) en un tablero 20x20
        self.corners_por_jugador = {
            "A": (0, 0),
            "B": (0, columnas - 1),
            "C": (filas - 1, columnas - 1),
            "D": (filas - 1, 0),
        }

    # ---------- utilidades de impresión ----------
    def mostrar(self) -> None:
        print("\n   " + " ".join([f"{c:02d}" for c in range(self.columnas)]))
        for r in range(self.filas):
            print(f"{r:02d} " + " ".join(self.grid[r]))
        print()

    # ---------- validaciones de reglas ----------
    def _dentro(self, r: int, c: int) -> bool:
        return 0 <= r < self.filas and 0 <= c < self.columnas

    def _vecinos_lado(self, r: int, c: int) -> List[Coord]:
        return [(r-1, c), (r+1, c), (r, c-1), (r, c+1)]

    def _vecinos_diagonal(self, r: int, c: int) -> List[Coord]:
        return [(r-1, c-1), (r-1, c+1), (r+1, c-1), (r+1, c+1)]

    def _celdas_orientadas(self, pieza_id: str, orient_idx: int, ref: Coord) -> List[Coord]:
        """
        Toma la orientación 'orient_idx' de la pieza y la traslada para que la
        celda (0,0) caiga en 'ref' (fila, col).
        """
        o = generar_orientaciones(pieza_id)
        if orient_idx < 0 or orient_idx >= len(o):
            raise ValueError(f"Orientación inválida para {pieza_id}: {orient_idx}")
        rr, cc = ref
        return [(rr + r, cc + c) for r, c in o[orient_idx]]

    def _toca_esquina_propia(self, celdas: List[Coord], simbolo: str) -> bool:
        for r, c in celdas:
            for dr, dc in self._vecinos_diagonal(r, c):
                if self._dentro(dr, dc) and self.grid[dr][dc] == simbolo:
                    return True
        return False

    def _toca_lado_propio(self, celdas: List[Coord], simbolo: str) -> bool:
        for r, c in celdas:
            for lr, lc in self._vecinos_lado(r, c):
                if self._dentro(lr, lc) and self.grid[lr][lc] == simbolo:
                    return True
        return False

    def _ocupa_esquina_inicial(self, celdas: List[Coord], simbolo: str) -> bool:
        if simbolo not in self.corners_por_jugador:
            # Si no está mapeado, no exigimos esquina (útil para más de 4)
            return True
        return self.corners_por_jugador[simbolo] in celdas

    # ---------- API pública ----------
    def validar_colocacion(
        self,
        simbolo: str,
        pieza_id: str,
        orient_idx: int,
        ref: Coord
    ) -> Tuple[bool, List[Coord], str]:
        """
        Reglas de Blokus:
          - dentro del tablero
          - sin solaparse con nada
          - si es la primera del jugador: DEBE cubrir su esquina inicial
          - si NO es la primera: DEBE tocar por ESQUINA alguna propia
          - NUNCA tocar por LADO una propia
        """
        if pieza_id not in PIECES_BASE:
            return False, [], f"Pieza no reconocida: {pieza_id}"

        celdas = self._celdas_orientadas(pieza_id, orient_idx, ref)

        # 1) dentro
        for r, c in celdas:
            if not self._dentro(r, c):
                return False, [], "La pieza se sale del tablero."

        # 2) libre/ no solape
        for r, c in celdas:
            if self.grid[r][c] != ".":
                return False, [], "La pieza se superpone con otra."

        # 3) contacto con propias (lado prohibido, esquina depende)
        primera = not self.jugadores_colocaron.get(simbolo, False)

        # no tocar por lado
        if self._toca_lado_propio(celdas, simbolo):
            return False, [], "No puede tocar por lado otra pieza propia."

        if primera:
            # primera debe ocupar la esquina asignada
            if not self._ocupa_esquina_inicial(celdas, simbolo):
                return False, [], "La primera pieza debe cubrir tu esquina inicial."
        else:
            # jugadas posteriores deben tocar por esquina al menos una
            if not self._toca_esquina_propia(celdas, simbolo):
                return False, [], "Debes tocar por esquina alguna pieza tuya."

        return True, celdas, "OK"

    def colocar(
        self,
        simbolo: str,
        pieza_id: str,
        orient_idx: int,
        ref: Coord
    ) -> bool:
        ok, celdas, _ = self.validar_colocacion(simbolo, pieza_id, orient_idx, ref)
        if not ok:
            return False
        for r, c in celdas:
            self.grid[r][c] = simbolo
        # marcar que ya jugó al menos una
        self.jugadores_colocaron[simbolo] = True
        return True
