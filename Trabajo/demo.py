# demo.py
from mesa import Mesa
from pieza import generar_orientaciones

def main():
    mesa = Mesa(20, 20)

    # Jugadores (símbolos) mapeados en mesa.corners_por_jugador:
    # A -> (0,0), B -> (0,19), C -> (19,19), D -> (19,0)
    # Primera jugada de A (debe cubrir (0,0))
    pieza = "L3"
    # Mira cuántas orientaciones tiene:
    o = generar_orientaciones(pieza)
    print(f"Pieza {pieza} tiene {len(o)} orientaciones.")

    mesa.mostrar()

    # Intentamos colocar L3 para A en su esquina:
    ok = mesa.colocar("A", pieza_id=pieza, orient_idx=0, ref=(0, 0))
    print("A coloca L3 en (0,0) orient 0:", ok)
    mesa.mostrar()

    # Ahora B debe cubrir su esquina (0,19). Probemos con I3 orientada en vertical.
    # Buscamos una orientación que caiga dentro y cubra la esquina:
    # Truco: ponemos ref para que una celda sea (0,19). Probemos orient_idx=1 (según salga).
    ok = False
    for idx in range(len(generar_orientaciones("I3"))):
        if mesa.colocar("B", "I3", idx, (0, 17)):  # ajusta ref si no cae exacto a la esquina
            ok = True
            print(f"B coloca I3 con orient {idx} en ref (0,17)")
            break
    print("Resultado B:", ok)
    mesa.mostrar()

    # Jugada posterior de A: debe tocar por esquina, nunca por lado.
    # Intentemos T4 cerca de su forma previa.
    puesto = mesa.colocar("A", "T4", 0, (2, 2))
    print("A coloca T4 en (2,2):", puesto)
    mesa.mostrar()

if __name__ == "__main__":
    main()
