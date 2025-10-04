from jugador import Jugador
from mock_tablero import MockTablero

def main():
    p1 = Jugador(id=1, nombre="Azul", simbolo="A",
                 piezas_disponibles=["I1", "L5", "T4", "Z4"])
    tab = MockTablero()

    ok = p1.intentar_colocar("L5", orientacion=0, posicion_referencia=(0, 0), tablero_iface=tab)
    print("¿Colocó?", ok)
    print(p1.resumen())

if __name__ == "__main__":
    main()
