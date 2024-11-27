import mysql.connector
from datetime import datetime

def get_db_connection():
    return mysql.connector.connect(
        host="localhost",
        user="root",
        password="200804",
        database="pruebas5"
    )

class Usuario:
    def __init__(self, nombre_usuario=None, correo_electronico=None, contrasenia=None, plataforma=None):
        self.nombre_usuario = nombre_usuario
        self.correo_electronico = correo_electronico
        self.contrasenia = contrasenia
        self.plataforma = plataforma

    def crear_usuario(self):
        conexion = get_db_connection()
        cursor = conexion.cursor()
        cursor.execute(
            "INSERT INTO usuarios (nombre_usuario, correo_electronico, contrasenia, plataforma) VALUES (%s, %s, %s, %s)",
            (self.nombre_usuario, self.correo_electronico, self.contrasenia, self.plataforma)
        )
        conexion.commit()
        conexion.close()

    @staticmethod
    def obtener_usuarios():
        conexion = get_db_connection()
        cursor = conexion.cursor()
        cursor.execute("SELECT * FROM usuarios")
        usuarios = cursor.fetchall()
        conexion.close()
        return usuarios

    @staticmethod
    def obtener_usuario_por_credenciales(correo_electronico, contrasenia):
        conexion = get_db_connection()
        cursor = conexion.cursor(dictionary=True)
        cursor.execute(
            "SELECT * FROM usuarios WHERE correo_electronico = %s AND contrasenia = %s",
            (correo_electronico, contrasenia)
        )
        usuario = cursor.fetchone()
        conexion.close()
        return usuario

    def editar_usuario(self, id_usuario):
        conexion = get_db_connection()
        cursor = conexion.cursor()
        cursor.execute(
            "UPDATE usuarios SET nombre_usuario = %s, correo_electronico = %s, contrasenia = %s, plataforma = %s WHERE id_usuario = %s",
            (self.nombre_usuario, self.correo_electronico, self.contrasenia, self.plataforma, id_usuario)
        )
        conexion.commit()
        conexion.close()

    @staticmethod
    def eliminar_usuario(id_usuario):
        conexion = get_db_connection()
        cursor = conexion.cursor()
        cursor.execute("DELETE FROM usuarios WHERE id_usuario = %s", (id_usuario,))
        conexion.commit()
        conexion.close()
    
    @staticmethod
    def ver_perfil(id_usuario):
        conexion = get_db_connection()
        cursor = conexion.cursor(dictionary=True)
        query = """
        SELECT u.nombre_usuario, u.correo_electronico, u.plataforma,
               COUNT(p.id_partida) AS partidas_jugadas,
               IFNULL(AVG(e.kd_ratio), 0) AS kd_promedio,
               (SELECT COUNT(*) FROM resenas WHERE id_usuario = %s) AS resenas_publicadas
        FROM usuarios u
        LEFT JOIN partidas p ON u.id_usuario = p.id_usuario
        LEFT JOIN estadisticas e ON p.id_partida = e.id_partida
        WHERE u.id_usuario = %s
        GROUP BY u.id_usuario;
        """
        cursor.execute(query, (id_usuario, id_usuario))
        perfil = cursor.fetchone()
        conexion.close()
        return perfil


class Estadistica:
    def __init__(self, id_partida, kd_ratio, puntuacion, modo_juego):
        self.id_partida = id_partida
        self.kd_ratio = kd_ratio
        self.puntuacion = puntuacion
        self.modo_juego = modo_juego

    def crear_estadistica(self):
        conexion = get_db_connection()
        cursor = conexion.cursor()
        cursor.execute(
            "INSERT INTO estadisticas (id_partida, kd_ratio, puntuacion, modo_juego) VALUES (%s, %s, %s, %s)",
            (self.id_partida, self.kd_ratio, self.puntuacion, self.modo_juego)
        )
        conexion.commit()
        conexion.close()

    @staticmethod
    def obtener_estadisticas():
        conexion = get_db_connection()
        cursor = conexion.cursor()
        cursor.execute("SELECT * FROM estadisticas")
        estadisticas = cursor.fetchall()
        conexion.close()
        return estadisticas

    def editar_estadistica(self, id_estadistica):
        conexion = get_db_connection()
        cursor = conexion.cursor()
        cursor.execute(
            "UPDATE estadisticas SET id_partida = %s, kd_ratio = %s, puntuacion = %s, modo_juego = %s WHERE id_estadistica = %s",
            (self.id_partida, self.kd_ratio, self.puntuacion, self.modo_juego, id_estadistica)
        )
        conexion.commit()
        conexion.close()

    @staticmethod
    def eliminar_estadistica(id_estadistica):
        conexion = get_db_connection()
        cursor = conexion.cursor()
        cursor.execute("DELETE FROM estadisticas WHERE id_estadistica = %s", (id_estadistica,))
        conexion.commit()
        conexion.close()
    
    @staticmethod
    def ver_estadisticas(id_usuario):
        conexion = get_db_connection()
        cursor = conexion.cursor(dictionary=True)
        query = """
        SELECT e.id_partida, e.kd_ratio, e.puntuacion, e.modo_juego
        FROM estadisticas e
        INNER JOIN partidas p ON e.id_partida = p.id_partida
        WHERE p.id_usuario = %s
        ORDER BY e.id_estadistica;
        """
        cursor.execute(query, (id_usuario,))
        estadisticas = cursor.fetchall()
        conexion.close()
        return estadisticas


class Resena:
    def __init__(self, id_usuario, id_modo_juego, contenido, calificacion):
        self.id_usuario = id_usuario
        self.id_modo_juego = id_modo_juego
        self.contenido = contenido
        self.calificacion = calificacion

    def crear_resena(self):
        if len(self.contenido) > 500:
            print("La reseña supera el límite de 500 caracteres.")
            return
        conexion = get_db_connection()
        cursor = conexion.cursor()
        cursor.execute(
            "INSERT INTO resenas (id_usuario, id_modo_juego, contenido, calificacion, fecha_publicacion) VALUES (%s, %s, %s, %s, %s)",
            (self.id_usuario, self.id_modo_juego, self.contenido, self.calificacion, datetime.now())
        )
        conexion.commit()
        conexion.close()

    @staticmethod
    def obtener_resenas():
        conexion = get_db_connection()
        cursor = conexion.cursor()
        cursor.execute("SELECT * FROM resenas")
        resenas = cursor.fetchall()
        conexion.close()
        return resenas

    def editar_resena(self, id_resena):
        conexion = get_db_connection()
        cursor = conexion.cursor()
        cursor.execute(
            "UPDATE resenas SET contenido = %s, calificacion = %s WHERE id_resena = %s",
            (self.contenido, self.calificacion, id_resena)
        )
        conexion.commit()
        conexion.close()

    @staticmethod
    def eliminar_resena(id_resena):
        conexion = get_db_connection()
        cursor = conexion.cursor()
        cursor.execute("DELETE FROM resenas WHERE id_resena = %s", (id_resena,))
        conexion.commit()
        conexion.close()
    
    @staticmethod
    def ver_resenas(id_usuario):
        conexion = get_db_connection()
        cursor = conexion.cursor(dictionary=True)
        query = """
        SELECT r.id_modo_juego, r.contenido, r.calificacion, r.fecha_publicacion
        FROM resenas r
        WHERE r.id_usuario = %s
        ORDER BY r.fecha_publicacion DESC;
        """
        cursor.execute(query, (id_usuario,))
        resenas = cursor.fetchall()
        conexion.close()
        return resenas

class Partida:

    def __init__(self, id_usuario, fecha_partida):
        self.id_usuario = id_usuario
        self.fecha_partida = fecha_partida
    
    def crear_partida_nueva(self):
        conexion = get_db_connection()
        cursor = conexion.cursor()
        cursor.execute(
            "INSERT INTO partidas (id_usuario, fecha_partida) VALUES (%s, %s)",
            (self.id_usuario, self.fecha_partida)
        )
        conexion.commit()
        conexion.close()
        

class Menu:
    def __init__(self):
        self.usuario_actual = None

    def menu_inicio(self):
        while True:
            print("\nBienvenido a la plataforma")
            print("1. Iniciar sesión")
            print("2. Registrarse")
            print("3. Salir")
            opcion = input("Seleccione una opción: ")

            if opcion == "1":
                self.iniciar_sesion()
            elif opcion == "2":
                self.registrar_usuario()
            elif opcion == "3":
                print("Gracias por usar la plataforma. ¡Adiós!")
                break
            else:
                print("Opción inválida. Intente nuevamente.")

    def iniciar_sesion(self):
        print("\nIniciar sesión")
        correo = input("Correo electrónico: ")
        contrasenia = input("Contraseña: ")
        usuario_encontrado = Usuario.obtener_usuario_por_credenciales(correo, contrasenia)
        if usuario_encontrado:
            self.usuario_actual = usuario_encontrado
            print(f"Bienvenido, {usuario_encontrado['nombre_usuario']}!")
            self.menu_principal()
        else:
            print("Credenciales incorrectas. Intente nuevamente.")

    def registrar_usuario(self):
        print("\nRegistro de usuario")
        nombre = input("Nombre de usuario: ")
        correo = input("Correo electrónico: ")
        contrasenia = input("Contraseña: ")
        plataforma = input("Plataforma (PC/Xbox/PlayStation): ")
        usuario = Usuario(nombre, correo, contrasenia, plataforma)
        usuario.crear_usuario()
        print("Usuario registrado exitosamente.")

    def menu_principal(self):
        while True:
            print("\nMenú Principal")
            print("1. Ver perfil")
            print("2. Administrar estadísticas")
            print("3. Administrar reseñas")
            print("4. Administrar Perfil")
            print("5. Cerrar sesión")
            print("6. Crear Partida")
            opcion = input("Seleccione una opción: ")

            if opcion == "1":
                self.ver_perfil()
            elif opcion == "2":
                self.menu_estadisticas()
            elif opcion == "3":
                self.menu_resenas()
            elif opcion == "4":
                self.administrar_perfil()
            elif opcion == "5":
                self.usuario_actual = None
                print("Sesión cerrada exitosamente.")
                break
            elif opcion == "6":
                self.crear_partida()
            else:
                print("Opción inválida. Intente nuevamente.")
            
    def crear_partida(self):
        print("\nCreando Partida")
        fecha_partida = datetime.now()
        partida = Partida(self.usuario_actual["id_usuario"], fecha_partida)
        partida.crear_partida_nueva()
        print("Partida creada exitosamente.")


    def ver_perfil(self):
        perfil = Usuario.ver_perfil(self.usuario_actual["id_usuario"])
        if perfil:
            print(f"\nPerfil de {perfil['nombre_usuario']}")
            print(f"Correo electrónico: {perfil['correo_electronico']}")
            print(f"Plataforma: {perfil['plataforma']}")
            print(f"Partidas jugadas: {perfil['partidas_jugadas']}")
            print(f"K/D promedio: {perfil['kd_promedio']:.2f}")
            print(f"Reseñas publicadas: {perfil['resenas_publicadas']}")
        else:
            print("No se pudo cargar el perfil.")

    def administrar_perfil(self):
        while True:
            print("\nMenú de Perfil")
            print("1. Editar perfil")
            print("2. Eliminar perfil")
            print("3. Regresar al menú principal")
            opcion = input("Seleccione una opción: ")

            if opcion == "1":
                self.editar_perfil()
            elif opcion == "2":
                self.eliminar_perfil()
            elif opcion == "3":
                break
            else:
                print("Opción inválida. Intente nuevamente.")

    def editar_perfil(self):
        print("\nEditar Perfil")
        nombre = input("Nuevo nombre de usuario: ")
        correo = input("Nuevo correo electrónico: ")
        contrasenia = input("Nueva contraseña: ")
        plataforma = input("Nueva plataforma: ")
        usuario = Usuario(nombre, correo, contrasenia, plataforma)
        usuario.editar_usuario(self.usuario_actual["id_usuario"])
        print("Perfil editado exitosamente.")

    def eliminar_perfil(self):
        print("\nEliminar Perfil")
        confirmacion = input("¿Está seguro de que desea eliminar su perfil? (s/n): ")
        if confirmacion.lower() == "s":
            Usuario.eliminar_usuario(self.usuario_actual["id_usuario"])
            print("Perfil eliminado exitosamente.")
            self.usuario_actual = None
            self.menu_inicio()
        else:
            print("Operación cancelada.")
            
    


    def menu_estadisticas(self):
        while True:
            print("\nMenú de Estadísticas")
            print("1. Ver estadísticas")
            print("2. Agregar estadísticas")
            print("3. Editar estadísticas")
            print("4. Eliminar estadísticas")
            print("5. Regresar al menú principal")
            opcion = input("Seleccione una opción: ")

            if opcion == "1":
                self.ver_estadisticas()
            elif opcion == "2":
                self.agregar_estadistica()
            elif opcion == "3":
                self.editar_estadistica()
            elif opcion == "4":
                self.eliminar_estadistica()
            elif opcion == "5":
                break
            else:
                print("Opción inválida. Intente nuevamente.")

    def ver_estadisticas(self):
        estadisticas = Estadistica.ver_estadisticas(self.usuario_actual["id_usuario"])
        if estadisticas:
            print("\nEstadísticas:")
            for estadistica in estadisticas:
                print(f"Partida: {estadistica['id_partida']}, K/D Ratio: {estadistica['kd_ratio']}, "
                      f"Puntuación: {estadistica['puntuacion']}, Modo de Juego: {estadistica['modo_juego']}")
        else:
            print("No hay estadísticas disponibles.")

    def agregar_estadistica(self):
        print("\nAgregar Estadística")
        id_partida = input("ID de la partida: ")
        kd_ratio = float(input("K/D Ratio: "))
        puntuacion = int(input("Puntuación: "))
        modo_juego = input("Modo de Juego (rápido/clasificatoria): ")
        estadistica = Estadistica(id_partida, kd_ratio, puntuacion, modo_juego)
        estadistica.crear_estadistica()
        print("Estadística agregada exitosamente.")

    def editar_estadistica(self):
        print("\nEditar Estadística")
        id_estadistica = input("ID de la estadística a editar: ")
        id_partida = input("ID de la partida: ")
        kd_ratio = float(input("Nuevo K/D Ratio: "))
        puntuacion = int(input("Nueva Puntuación: "))
        modo_juego = input("Nuevo Modo de Juego: ")
        estadistica = Estadistica(id_partida, kd_ratio, puntuacion, modo_juego)
        estadistica.editar_estadistica(id_estadistica)
        print("Estadística editada exitosamente.")

    def eliminar_estadistica(self):
        print("\nEliminar Estadística")
        id_estadistica = input("ID de la estadística a eliminar: ")
        Estadistica.eliminar_estadistica(id_estadistica)
        print("Estadística eliminada exitosamente.")

    def menu_resenas(self):
        while True:
            print("\nMenú de Reseñas")
            print("1. Ver reseñas")
            print("2. Agregar reseña")
            print("3. Editar reseña")
            print("4. Eliminar reseña")
            print("5. Regresar al menú principal")
            opcion = input("Seleccione una opción: ")

            if opcion == "1":
                self.ver_resenas()
            elif opcion == "2":
                self.agregar_resena()
            elif opcion == "3":
                self.editar_resena()
            elif opcion == "4":
                self.eliminar_resena()
            elif opcion == "5":
                break
            else:
                print("Opción inválida. Intente nuevamente.")

    def ver_resenas(self):
        resenas = Resena.ver_resenas(self.usuario_actual["id_usuario"])
        if resenas:
            print("\nReseñas:")
            for resena in resenas:
                print(f"Modo de Juego: {resena['id_modo_juego']}, "
                      f"Contenido: {resena['contenido']}, "
                      f"Calificación: {resena['calificacion']}, "
                      f"Fecha de Publicación: {resena['fecha_publicacion']}")
        else:
            print("No hay reseñas disponibles.")

    def agregar_resena(self):
        print("\nAgregar Reseña")
        id_modo_juego = input("ID del Modo de Juego: ")
        contenido = input("Contenido de la reseña (máximo 500 caracteres): ")
        calificacion = int(input("Calificación (1-5): "))
        resena = Resena(self.usuario_actual["id_usuario"], id_modo_juego, contenido, calificacion)
        resena.crear_resena()
        print("Reseña agregada exitosamente.")

    def editar_resena(self):

        print("\nEditar Reseña")
        id_resena = input("ID de la reseña a editar: ")
        contenido = input("Nuevo contenido de la reseña (máximo 500 caracteres): ")
        calificacion = int(input("Nueva calificación (1-5): "))
        resena = Resena(None, None, contenido, calificacion)
        resena.editar_resena(id_resena)
        print("Reseña editada exitosamente.")

    def eliminar_resena(self):
        print("\nEliminar Reseña")
        id_resena = input("ID de la reseña a eliminar: ")
        Resena.eliminar_resena(id_resena)
        print("Reseña eliminada exitosamente.")


if __name__ == "__main__":
    menu = Menu()
    menu.menu_inicio()