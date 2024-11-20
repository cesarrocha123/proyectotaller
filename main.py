from funciones import (
    crear_cuenta, iniciar_sesion, ver_cuenta, registrar_estadistica, agregar_resena,
    editar_cuenta, editar_estadistica, eliminar_cuenta
)

def menu():
    usuario_id = None

    while True:
        if not usuario_id:
            print("\n=== BIENVENIDO ===")
            print("1. Iniciar sesión")
            print("2. Registrarse")
            print("3. Salir")
            opcion = input("Seleccione una opción: ")

            if opcion == "1":
                usuario_id = iniciar_sesion()
            elif opcion == "2":
                crear_cuenta()
            elif opcion == "3":
                print("Saliendo...")
                break
            else:
                print("Opción inválida.")
        else:
            print("\n=== MENÚ PRINCIPAL ===")
            print("1. Ver cuenta")
            print("2. Registrar estadística")
            print("3. Agregar reseña")
            print("4. Editar cuenta")
            print("5. Editar estadística")
            print("6. Eliminar cuenta")
            print("7. Cerrar sesión")
            opcion = input("Seleccione una opción: ")

            if opcion == "1":
                ver_cuenta()
            elif opcion == "2":
                registrar_estadistica(usuario_id)
            elif opcion == "3":
                agregar_resena(usuario_id)
            elif opcion == "4":
                editar_cuenta(usuario_id)
            elif opcion == "5":
                editar_estadistica()
            elif opcion == "6":
                eliminar_cuenta(usuario_id)
                usuario_id = None
            elif opcion == "7":
                print("Cerrando sesión...")
                usuario_id = None
            else:
                print("Opción inválida.")

if __name__ == "__main__":
    menu()
