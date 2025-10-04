# tablero_api.py
from typing import List, Tuple, Protocol
from jugador import Jugador, PieceId

Coord = Tuple[int, int]

class TableroAPI(Protocol):
    def validar_colocacion(
        self,
        jugador: Jugador,
        pieza_id: PieceId,
        orientacion: int,
        posicion_referencia: Coord,
    ) -> Tuple[bool, List[Coord]]:
        """
        Devuelve (es_valida, celdas_ocupadas_si_se_coloca).
        Debe aplicar reglas de Blokus:
        - La primera pieza de un jugador debe tocar su esquina inicial.
        - Nunca lado a lado con piezas propias (solo contacto por vértice).
        - Debe estar dentro del tablero y sin solaparse.
        """
        ...

    def colocar_pieza(
        self,
        jugador: Jugador,
        pieza_id: PieceId,
        celdas: List[Coord],
    ) -> None:
        """Pinta la pieza en la rejilla interna y registra al jugador inicial si es su primera jugada."""
        ...
