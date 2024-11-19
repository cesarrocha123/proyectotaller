from conectar import conectar
import mysql.connector

# === CREATE ===
def crear_cuenta():
    conexion = conectar()
    if not conexion:
        return

    nombre = input("Nombre de usuario: ")
    correo = input("Correo electrónico: ")
    contrasena = input("Contraseña: ")
    plataforma = input("Plataforma (PC, Xbox, PlayStation): ")

    try:
        cursor = conexion.cursor()
        query = "INSERT INTO cuentas (nombre_usuario, correo, contrasena, plataforma) VALUES (%s, %s, %s, %s)"
        cursor.execute(query, (nombre, correo, contrasena, plataforma))
        conexion.commit()
        print("Cuenta creada exitosamente.")
    except mysql.connector.Error as err:
        print(f"Error al crear cuenta: {err}")
    finally:
        conexion.close()

# === READ ===
def iniciar_sesion():
    conexion = conectar()
    if not conexion:
        return None

    print("\n=== INICIO DE SESIÓN ===")
    nombre = input("Nombre de usuario: ")
    contrasena = input("Contraseña: ")

    try:
        cursor = conexion.cursor()
        query = "SELECT id FROM cuentas WHERE nombre_usuario = %s AND contrasena = %s"
        cursor.execute(query, (nombre, contrasena))
        usuario = cursor.fetchone()

        if usuario:
            print(f"Inicio de sesión exitoso. Bienvenido, {nombre}!")
            return usuario[0]
        else:
            print("Usuario o contraseña incorrectos.")
            return None
    except mysql.connector.Error as err:
        print(f"Error al iniciar sesión: {err}")
        return None
    finally:
        conexion.close()

# === UPDATE ===
def editar_cuenta():
    conexion = conectar()
    if not conexion:
        return

    id_cuenta = input("ID de la cuenta que deseas editar: ")

    nuevo_nombre = input("Nuevo nombre de usuario (dejar vacío para no cambiar): ")
    nuevo_correo = input("Nuevo correo electrónico (dejar vacío para no cambiar): ")
    nueva_contrasena = input("Nueva contraseña (dejar vacío para no cambiar): ")
    nueva_plataforma = input("Nueva plataforma (PC, Xbox, PlayStation) (dejar vacío para no cambiar): ")

    try:
        cursor = conexion.cursor()
        query = "UPDATE cuentas SET "
        valores = []

        if nuevo_nombre:
            query += "nombre_usuario = %s, "
            valores.append(nuevo_nombre)
        if nuevo_correo:
            query += "correo = %s, "
            valores.append(nuevo_correo)
        if nueva_contrasena:
            query += "contrasena = %s, "
            valores.append(nueva_contrasena)
        if nueva_plataforma:
            query += "plataforma = %s, "
            valores.append(nueva_plataforma)

        query = query.rstrip(", ") + " WHERE id = %s"
        valores.append(id_cuenta)

        cursor.execute(query, valores)
        conexion.commit()

        if cursor.rowcount > 0:
            print("Cuenta actualizada exitosamente.")
        else:
            print("No se encontró la cuenta o no se realizaron cambios.")
    except mysql.connector.Error as err:
        print(f"Error al editar cuenta: {err}")
    finally:
        conexion.close()

def editar_estadistica():
    conexion = conectar()
    if not conexion:
        return

    id_estadistica = input("ID de la estadística que deseas editar: ")

    nuevo_kd_ratio = input("Nuevo K/D Ratio (dejar vacío para no cambiar): ")
    nueva_puntuacion = input("Nueva puntuación (dejar vacío para no cambiar): ")
    nuevo_modo = input("Nuevo modo de juego (dejar vacío para no cambiar): ")

    try:
        cursor = conexion.cursor()
        query = "UPDATE estadisticas SET "
        valores = []

        if nuevo_kd_ratio:
            query += "kd_ratio = %s, "
            valores.append(float(nuevo_kd_ratio))
        if nueva_puntuacion:
            query += "puntuacion = %s, "
            valores.append(int(nueva_puntuacion))
        if nuevo_modo:
            query += "modo_juego = %s, "
            valores.append(nuevo_modo)

        query = query.rstrip(", ") + " WHERE id = %s"
        valores.append(id_estadistica)

        cursor.execute(query, valores)
        conexion.commit()

        if cursor.rowcount > 0:
            print("Estadística actualizada exitosamente.")
        else:
            print("No se encontró la estadística o no se realizaron cambios.")
    except mysql.connector.Error as err:
        print(f"Error al editar estadística: {err}")
    finally:
        conexion.close()

def editar_resena():
    conexion = conectar()
    if not conexion:
        return

    id_resena = input("ID de la reseña que deseas editar: ")

    nuevo_contenido = input("Nuevo contenido de la reseña (máx 500 caracteres, dejar vacío para no cambiar): ")
    nueva_calificacion = input("Nueva calificación (1-5, dejar vacío para no cambiar): ")

    try:
        cursor = conexion.cursor()
        query = "UPDATE resenas SET "
        valores = []

        if nuevo_contenido:
            query += "contenido = %s, "
            valores.append(nuevo_contenido)
        if nueva_calificacion:
            nueva_calificacion = int(nueva_calificacion)
            if 1 <= nueva_calificacion <= 5:
                query += "calificacion = %s, "
                valores.append(nueva_calificacion)
            else:
                print("La calificación debe estar entre 1 y 5.")
                return

        query = query.rstrip(", ") + " WHERE id = %s"
        valores.append(id_resena)

        cursor.execute(query, valores)
        conexion.commit()

        if cursor.rowcount > 0:
            print("Reseña actualizada exitosamente.")
        else:
            print("No se encontró la reseña o no se realizaron cambios.")
    except mysql.connector.Error as err:
        print(f"Error al editar reseña: {err}")
    finally:
        conexion.close()
