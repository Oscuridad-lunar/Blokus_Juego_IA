
# main.py
from juego import Juego

def mostrar_menu():
    print("========================================")
    print("         🧱 BLOKUS – Consola v1.0")
    print("========================================")
    print("1) Nuevo juego")
    print("2) Ver reglas del juego")
    print("3) Créditos")
    print("4) Salir")
    print("----------------------------------------")

def mostrar_reglas():
    print("\n📜 REGLAS BÁSICAS DE BLOKUS:")
    print("1. Cada jugador empieza en su esquina asignada del tablero.")
    print("2. La primera pieza debe cubrir esa esquina.")
    print("3. Las piezas del mismo jugador NO pueden tocarse por lado,")
    print("   pero deben tocarse por al menos una esquina.")
    print("4. Puedes tocar piezas de otros jugadores sin problema.")
    print("5. Gana quien coloque más cuadros (o menos piezas restantes).")
    print("6. Si no puedes jugar, pasa tu turno.")
    print("----------------------------------------\n")

def mostrar_creditos():
    print("\n👥 CRÉDITOS DEL PROYECTO")
    print("Desarrollado por:")
    print(" - Geison Medina")
    print(" - Luis .......")
    print(" - Nayardo .......")    
    
    print("Instituto Tecnológico de las Américas (ITLA)")
    print("Materia: Inteligencia Artificial")
    print("----------------------------------------\n")

def main():
    while True:
        mostrar_menu()
        opcion = input("Elige una opción (1-4): ").strip()

        if opcion == "1":
            try:
                n = int(input("Número de jugadores (2-4): ").strip())
                if 2 <= n <= 4:
                    juego = Juego(num_jugadores=n)
                    juego.iniciar()
                else:
                    print("⚠️  El número debe estar entre 2 y 4.")
            except ValueError:
                print("⚠️  Debes escribir un número válido.")
        elif opcion == "2":
            mostrar_reglas()
        elif opcion == "3":
            mostrar_creditos()
        elif opcion == "4":
            print("Saliendo del programa... 👋")
            break
        else:
            print("❌ Opción inválida. Intenta de nuevo.\n")

if __name__ == "__main__":
    main()
