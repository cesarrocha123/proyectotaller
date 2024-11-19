from funciones import (
    crear_cuenta, iniciar_sesion, editar_cuenta, editar_estadistica, editar_resena
)

def menu():
    while True:
        print("\n=== MENÚ PRINCIPAL ===")
        print("1. Crear cuenta")
        print("2. Iniciar sesión")
        print("3. Editar cuenta")
        print("4. Editar estadística")
        print("5. Editar reseña")
        print("6. Salir")

        opcion = input("Seleccione una opción: ")

        if opcion == "1":
            crear_cuenta()
        elif opcion == "2":
            iniciar_sesion()
        elif opcion == "3":
            editar_cuenta()
        elif opcion == "4":
            editar_estadistica()
        elif opcion == "5":
            editar_resena()
        elif opcion == "6":
            print("Saliendo...")
            break
        else:
            print("Opción inválida.")

if __name__ == "__main__":
    menu()
