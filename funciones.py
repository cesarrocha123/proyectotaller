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

# === READ ===
def ver_cuenta():
    conexion = conectar()
    if not conexion:
        return

    id_cuenta = input("Ingrese el ID de la cuenta que desea ver: ")

    try:
        cursor = conexion.cursor()
        query = """
        SELECT nombre_usuario, correo, plataforma, 
        (SELECT COUNT(*) FROM estadisticas WHERE id_cuenta = cuentas.id) AS partidas,
        (SELECT IFNULL(AVG(kd_ratio), 0) FROM estadisticas WHERE id_cuenta = cuentas.id) AS kd_promedio,
        (SELECT COUNT(*) FROM resenas WHERE id_cuenta = cuentas.id) AS resenas
        FROM cuentas
        WHERE id = %s
        """
        cursor.execute(query, (id_cuenta,))
        cuenta = cursor.fetchone()

        if cuenta:
            print(f"Nombre: {cuenta[0]}, Correo: {cuenta[1]}, Plataforma: {cuenta[2]}, "
                  f"Partidas: {cuenta[3]}, K/D Ratio promedio: {cuenta[4]:.2f}, Reseñas: {cuenta[5]}")
        else:
            print("Cuenta no encontrada.")
    except mysql.connector.Error as err:
        print(f"Error al obtener cuenta: {err}")
    finally:
        conexion.close()

def registrar_estadistica(usuario_id):
    conexion = conectar()
    if not conexion:
        return

    id_partida = input("ID de la partida: ")
    kd_ratio = float(input("K/D Ratio: "))
    puntuacion = int(input("Puntuación: "))
    modo_juego = input("Modo de juego: ")

    try:
        cursor = conexion.cursor()
        query = "INSERT INTO estadisticas (id_cuenta, id_partida, kd_ratio, puntuacion, modo_juego) VALUES (%s, %s, %s, %s, %s)"
        cursor.execute(query, (usuario_id, id_partida, kd_ratio, puntuacion, modo_juego))
        conexion.commit()
        print("Estadística registrada exitosamente.")
    except mysql.connector.Error as err:
        print(f"Error al registrar estadística: {err}")
    finally:
        conexion.close()

def agregar_resena(usuario_id):
    conexion = conectar()
    if not conexion:
        return

    id_mapa_modo = input("ID del mapa o modo de juego: ")
    contenido = input("Reseña (máx 500 caracteres): ")

    while True:
        try:
            calificacion = int(input("Calificación (1-5): "))
            if 1 <= calificacion <= 5:
                break
            else:
                print("La calificación debe estar entre 1 y 5.")
        except ValueError:
            print("Debe ingresar un número entero entre 1 y 5.")

    try:
        cursor = conexion.cursor()
        query = "INSERT INTO resenas (id_cuenta, id_mapa_modo, contenido, calificacion) VALUES (%s, %s, %s, %s)"
        cursor.execute(query, (usuario_id, id_mapa_modo, contenido, calificacion))
        conexion.commit()
        print("Reseña agregada exitosamente.")
    except mysql.connector.Error as err:
        print(f"Error al agregar reseña: {err}")
    finally:
        conexion.close()

# === UPDATE ===
def editar_cuenta(usuario_id):
    conexion = conectar()
    if not conexion:
        return

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
        valores.append(usuario_id)

        cursor.execute(query, valores)
        conexion.commit()

        if cursor.rowcount > 0:
            print("Cuenta actualizada exitosamente.")
        else:
            print("No se realizaron cambios.")
    except mysql.connector.Error as err:
        print(f"Error al editar cuenta: {err}")
    finally:
        conexion.close()

def editar_estadistica():
    conexion = conectar()
    if not conexion:
        return

    id_estadistica = input("ID de la estadística a editar: ")
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
            print("No se realizaron cambios.")
    except mysql.connector.Error as err:
        print(f"Error al editar estadística: {err}")
    finally:
        conexion.close()

# === DELETE ===
def eliminar_cuenta(usuario_id):
    conexion = conectar()
    if not conexion:
        return

    try:
        cursor = conexion.cursor()
        query = "DELETE FROM cuentas WHERE id = %s"
        cursor.execute(query, (usuario_id,))
        conexion.commit()
        if cursor.rowcount > 0:
            print("Cuenta eliminada exitosamente.")
        else:
            print("No se encontró la cuenta.")
    except mysql.connector.Error as err:
        print(f"Error al eliminar cuenta: {err}")
    finally:
        conexion.close()
# cosas agregar los cambios 

def visualizar_informacion(cursor, usuario_id):
    cursor.execute("SELECT nombre_usuario, correo, plataforma_id, partidas_jugadas FROM usuarios WHERE id = %s", (usuario_id,))

    usuario = cursor.fetchone()
    
    if usuario:
        print("Nombre de usuario:", usuario['nombre_usuario'])
        print("Correo electrónico:", usuario['correo'])
        print("Plataforma:", usuario['plataforma_id'])
        print("Número de partidas jugadas:", usuario['partidas_jugadas'])
        print("K/D Ratio promedio:", usuario['kd_ratio_promedio'])
        print("Número de reseñas publicadas:", usuario['reseñas_publicadas'])
    else:
        print("No se encontró el usuario con ese ID.")

def actualizar_informacion(cursor, conexion, usuario_id):
    nuevo_nombre = input("Nuevo nombre de usuario (deja vacío si no deseas cambiarlo): ")
    nuevo_correo = input("Nuevo correo electrónico (deja vacío si no deseas cambiarlo): ")
    nueva_plataforma = input("Nueva plataforma (deja vacío si no deseas cambiarla): ")

    # Construir la consulta de actualización
    query = "UPDATE usuarios SET "
    values = []
    
    if nuevo_nombre:
        query += "nombre_usuario = %s, "
        values.append(nuevo_nombre)
    if nuevo_correo:
        query += "correo = %s, "
        values.append(nuevo_correo)
    if nueva_plataforma:
        query += "plataforma_id = %s, "
        values.append(nueva_plataforma)

    # Eliminar la última coma si hubo alguna actualización
    if query.endswith(", "):
        query = query[:-2]

    query += " WHERE id = %s"
    values.append(usuario_id)

    cursor.execute(query, tuple(values))
    conexion.commit()

    print("Información actualizada correctamente.")
