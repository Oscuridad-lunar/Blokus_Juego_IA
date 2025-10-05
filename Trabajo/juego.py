# juego.py
from typing import List
from mesa import Mesa
from pieza import generar_orientaciones, PIECES_BASE
from jugador import Jugador

class Juego:
    def __init__(self, filas: int = 20, columnas: int = 20, num_jugadores: int = 2):
        if not 2 <= num_jugadores <= 4:
            raise ValueError("El juego soporta entre 2 y 4 jugadores.")

        self.mesa = Mesa(filas, columnas)
        # Símbolos fijos para mapear esquinas: A,B,C,D
        simbolos = ["A", "B", "C", "D"]
        nombres  = ["Azul", "Rojo", "Verde", "Amarillo"]

        self.jugadores: List[Jugador] = []
        for i in range(num_jugadores):
            piezas_iniciales = list(PIECES_BASE.keys())  # copia
            j = Jugador(
                id=i+1,
                nombre=nombres[i],
                simbolo=simbolos[i],
                piezas_disponibles=piezas_iniciales
            )
            self.jugadores.append(j)

        self.turno_idx = 0
        self.pases_consecutivos = 0  # para detectar fin (todos pasaron)

    # ----------------- utilidades de turno -----------------
    def jugador_actual(self) -> Jugador:
        return self.jugadores[self.turno_idx]

    def siguiente_turno(self) -> None:
        self.turno_idx = (self.turno_idx + 1) % len(self.jugadores)

    def quedan_jugadas_posibles(self, jugador: Jugador) -> bool:
        """Heurística simple: intenta validar al menos una orientación/pos en una vecindad.
           Para no hacerlo costoso, probamos unas cuantas posiciones alrededor de todo el tablero.
        """
        # Estrategia rápida: muestreamos celdas cada 2 pasos para acelerar
        for pieza_id in jugador.piezas_disponibles:
            orientaciones = generar_orientaciones(pieza_id)
            for orient_idx in range(len(orientaciones)):
                # muestreo r y c saltando de 2 en 2 para no probar 400 posiciones por orientación
                for r in range(0, self.mesa.filas, 2):
                    for c in range(0, self.mesa.columnas, 2):
                        ok, _, _ = self.mesa.validar_colocacion(jugador.simbolo, pieza_id, orient_idx, (r, c))
                        if ok:
                            return True
        return False

    # ----------------- UI consola -----------------
    def _mostrar_menu_turno(self, jugador: Jugador):
        print("=====================================")
        print(f" Turno de [{jugador.simbolo}] {jugador.nombre}")
        print("=====================================")
        print("Opciones:")
        print("  1) Colocar pieza")
        print("  2) Ver tablero")
        print("  3) Ver mis piezas")
        print("  4) Pasar turno")
        print("  5) Salir del juego")
        print("-------------------------------------")

    def _listar_piezas(self, jugador: Jugador):
        print(f"Piezas disponibles ({len(jugador.piezas_disponibles)}):")
        # mostrar 10 por línea para que sea legible
        fila = []
        for i, pid in enumerate(sorted(jugador.piezas_disponibles)):
            fila.append(pid)
            if (i+1) % 10 == 0:
                print("  " + ", ".join(fila))
                fila = []
        if fila:
            print("  " + ", ".join(fila))
        print()

    def _input_int(self, msg: str, minimo: int = None, maximo: int = None):
        while True:
            txt = input(msg).strip()
            if txt.lower() == "q":
                return None
            if not txt.isdigit():
                print("  > Debe ser un número. (o Q para cancelar)")
                continue
            val = int(txt)
            if minimo is not None and val < minimo:
                print(f"  > Debe ser >= {minimo}")
                continue
            if maximo is not None and val > maximo:
                print(f"  > Debe ser <= {maximo}")
                continue
            return val

    def _accion_colocar(self, jugador: Jugador):
        if not jugador.piezas_disponibles:
            print("No te quedan piezas. Debes pasar.")
            return False

        self._listar_piezas(jugador)
        pieza_id = input("Elige pieza (ej: L3, I3, T4) o Q para cancelar: ").strip().upper()
        if pieza_id == "Q":
            return False

        if pieza_id not in jugador.piezas_disponibles:
            print("Esa pieza no está en tu lista disponible.")
            return False

        orientaciones = generar_orientaciones(pieza_id)
        print(f"La pieza {pieza_id} tiene {len(orientaciones)} orientaciones (0 a {len(orientaciones)-1}).")
        orient_idx = self._input_int("Orientación: ", 0, len(orientaciones)-1)
        if orient_idx is None:
            return False

        r = self._input_int(f"Fila (0..{self.mesa.filas-1}): ", 0, self.mesa.filas-1)
        if r is None:
            return False
        c = self._input_int(f"Columna (0..{self.mesa.columnas-1}): ", 0, self.mesa.columnas-1)
        if c is None:
            return False

        ok, _, motivo = self.mesa.validar_colocacion(jugador.simbolo, pieza_id, orient_idx, (r, c))
        if not ok:
            print(f"❌ Jugada inválida: {motivo}")
            return False

        # Colocar y actualizar estado del jugador
        colocado = self.mesa.colocar(jugador.simbolo, pieza_id, orient_idx, (r, c))
        if colocado:
            jugador.quitar_pieza(pieza_id)
            jugador.ha_pasado = False
            print("✅ Jugada realizada.")
            self.mesa.mostrar()
            return True
        else:
            print("❌ No se pudo colocar (algo salió mal).")
            return False

    # ----------------- bucle principal -----------------
    def iniciar(self):
        print("=========== BLOKUS (Consola) ===========")
        print(f"Jugadores: {', '.join([f'{j.nombre}({j.simbolo})' for j in self.jugadores])}")
        print("Reglas activas: esquina inicial, solo vértice, no lados.")
        print("Escribe 'Q' cuando se te pida un número para cancelar esa acción.\n")
        self.mesa.mostrar()

        # Si un jugador no puede jugar de entrada, igual debe intentar/o pasar.
        while True:
            jugador = self.jugador_actual()

            # Si ningún jugador puede jugar (todos pasaron en la ronda), fin
            if self.pases_consecutivos >= len(self.jugadores):
                print("\n🏁 Todos pasaron. ¡Fin del juego!\n")
                self._imprimir_puntajes()
                break

            # Chequeo rápido: ¿le queda al menos una jugada posible?
            if not jugador.piezas_disponibles or not self.quedan_jugadas_posibles(jugador):
                print(f"[{jugador.simbolo}] {jugador.nombre} no tiene jugadas posibles. Debe pasar.")
                jugador.marcar_paso()
                self.pases_consecutivos += 1
                self.siguiente_turno()
                continue

            self._mostrar_menu_turno(jugador)
            opcion = input("Elige opción (1-5): ").strip()

            if opcion == "1":
                exito = self._accion_colocar(jugador)
                if exito:
                    self.pases_consecutivos = 0
                    # (opcional) sumar puntaje inmediato por celdas colocadas
                # sin importar, avanzamos turno
                self.siguiente_turno()

            elif opcion == "2":
                self.mesa.mostrar()

            elif opcion == "3":
                self._listar_piezas(jugador)

            elif opcion == "4":
                jugador.marcar_paso()
                self.pases_consecutivos += 1
                print(f"[{jugador.simbolo}] {jugador.nombre} pasó el turno.")
                self.siguiente_turno()

            elif opcion == "5":
                print("Saliendo del juego...")
                break

            else:
                print("Opción no válida. Intenta de nuevo.")

        print("Gracias por jugar. 👋")

    # ----------------- puntajes (simple) -----------------
    def _imprimir_puntajes(self):
        # Puntaje simple: celdas colocadas = sumatoria de piezas puestas (tendríamos que
        # contarlas; como no guardamos histórico en Mesa, lo haremos por piezas restantes.)
        # Aproximación: piezas restantes → penaliza por cantidad de celdas que tendría esa pieza.
        # Para exactitud, suma real = (todas celdas colocadas). Aquí: penalización por restantes.
        print("PUNTAJES (aprox. por piezas restantes):")
        tabla = []
        for j in self.jugadores:
            penal = 0
            for pid in j.piezas_disponibles:
                # penalizamos por tamaño de la pieza = # celdas base
                penal += len(PIECES_BASE[pid])
            score = -penal  # menos penalización es mejor
            tabla.append((score, j))
        tabla.sort(reverse=True, key=lambda x: x[0])

        for rank, (score, j) in enumerate(tabla, start=1):
            print(f"{rank}. [{j.simbolo}] {j.nombre}  ->  {score} (piezas sin jugar: {len(j.piezas_disponibles)})")

if __name__ == "__main__":
    # Inicia el juego con 2 jugadores (A y B). Cambia a 3 o 4 si quieres.
    Juego(num_jugadores=2).iniciar()
