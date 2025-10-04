# jugador.py
from dataclasses import dataclass, field
from typing import List, Optional, Tuple, Dict

Coord = Tuple[int, int]  # (fila, col)
PieceId = str            # p.ej. "L5", "I1", "T4", etc.

@dataclass
class Jugador:
    id: int                      # 1..4
    nombre: str                  # "Azul", "Amarillo", etc.
    simbolo: str                 # p.ej. "A", "B", "C", "D" para imprimir en tablero
    piezas_disponibles: List[PieceId] = field(default_factory=list)
    piezas_colocadas: Dict[PieceId, List[Coord]] = field(default_factory=dict)
    ha_pasado: bool = False      # si pasó el turno
    puntaje: int = 0             # puntaje acumulado (se calcula al final)

    def tiene_pieza(self, pieza: PieceId) -> bool:
        return pieza in self.piezas_disponibles

    def quitar_pieza(self, pieza: PieceId) -> None:
        if pieza not in self.piezas_disponibles:
            raise ValueError(f"La pieza {pieza} no está disponible para {self.nombre}.")
        self.piezas_disponibles.remove(pieza)

    def registrar_colocacion(self, pieza: PieceId, celdas: List[Coord]) -> None:
        """Guarda la jugada en el historial del jugador."""
        self.piezas_colocadas[pieza] = celdas

    def piezas_restantes(self) -> int:
        return len(self.piezas_disponibles)

    def marcar_paso(self) -> None:
        self.ha_pasado = True

    # --- Operación de alto nivel (se integra con el Tablero) ---
    def intentar_colocar(
        self,
        pieza: PieceId,
        orientacion: int,
        posicion_referencia: Coord,
        tablero_iface: "TableroAPI",
    ) -> bool:
        """
        Orquesta la colocación:
        - Verifica que el jugador tenga la pieza.
        - Pregunta al Tablero si la colocación es válida para este jugador.
        - Si es válida: actualiza tablero y estado del jugador.
        Devuelve True si se colocó, False si no.
        """
        if not self.tiene_pieza(pieza):
            return False

        valido, celdas_resultantes = tablero_iface.validar_colocacion(
            jugador=self,
            pieza_id=pieza,
            orientacion=orientacion,
            posicion_referencia=posicion_referencia,
        )
        if not valido:
            return False

        tablero_iface.colocar_pieza(
            jugador=self,
            pieza_id=pieza,
            celdas=celdas_resultantes,
        )
        self.quitar_pieza(pieza)
        self.registrar_colocacion(pieza, celdas_resultantes)
        self.ha_pasado = False
        return True

    # --- Utilidades de impresión/depuración ---
    def resumen(self) -> str:
        return (f"[{self.simbolo}] {self.nombre} | "
                f"Restantes: {self.piezas_restantes()} | "
                f"Puestas: {len(self.piezas_colocadas)} | "
                f"Puntaje: {self.puntaje} | "
                f"Pasó: {self.ha_pasado}")
