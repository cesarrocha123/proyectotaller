import mysql.connector

def conectar():
    try:
        conexion = mysql.connector.connect(
            host="localhost",        # Cambia si tu servidor es diferente
            user="root",             # Tu usuario de MySQL
            password="",             # Tu contraseña de MySQL (déjala vacía si no configuraste una)
            database="videojuego"    # Nombre de la base de datos que creaste
        )
        if conexion.is_connected():
            print("Conexión exitosa a la base de datos.")
            return conexion
    except mysql.connector.Error as err:
        print(f"Error al conectar: {err}")
        return None

conexion = conectar()
if conexion:
    print("Conexión probada exitosamente.")
    conexion.close()
