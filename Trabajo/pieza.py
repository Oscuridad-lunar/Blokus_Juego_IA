# pieza.py
# Módulo para generar orientaciones de las piezas de Blokus
# Usa el repositorio oficial definido en repositorio_piezas.py

from typing import List, Tuple
from repositorio_piezas import PIEZAS  # importamos el repositorio global

Coord = Tuple[int, int]

def generar_orientaciones(pieza_id: str) -> List[List[Coord]]:
    """
    Devuelve todas las orientaciones únicas (rotaciones + reflejos) 
    para una pieza específica.
    Usa el cache del repositorio para que sea rápido.
    """
    return PIEZAS.orientaciones(pieza_id)

def tamano_pieza(pieza_id: str) -> int:
    """
    Devuelve el tamaño (cantidad de cuadros) de la pieza.
    Ejemplo: I1 -> 1, L5 -> 5
    """
    return PIEZAS.tam(pieza_id)

def lista_piezas_disponibles() -> List[str]:
    """
    Devuelve la lista completa de IDs de piezas disponibles en el juego.
    Ejemplo: ["I1", "I2", "I3", "L3", "L4", "L5", ...]
    """
    return PIEZAS.ids()

# Ejemplo de uso rápido
if __name__ == "__main__":
    print("Piezas disponibles:", lista_piezas_disponibles())
    print("Tamaño de L5:", tamano_pieza("L5"))
    print("Cantidad de orientaciones de L5:", len(generar_orientaciones("L5")))
