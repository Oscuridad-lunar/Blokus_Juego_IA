# mock_tablero.py (solo para pruebas)
from typing import List, Tuple
from tablero_api import TableroAPI, Coord
from jugador import Jugador, PieceId

class MockTablero(TableroAPI):
    def validar_colocacion(
        self, jugador: Jugador, pieza_id: PieceId, orientacion: int, posicion_referencia: Coord
    ) -> Tuple[bool, List[Coord]]:
        # Simula que toda colocación es válida ocupando 3 celdas
        r, c = posicion_referencia
        return True, [(r, c), (r, c+1), (r+1, c)]

    def colocar_pieza(self, jugador: Jugador, pieza_id: PieceId, celdas: List[Coord]) -> None:
        # No hace nada real (solo imprime)
        print(f"Colocada {pieza_id} de {jugador.nombre} en {celdas}")
