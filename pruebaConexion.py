import mysql.connector

def connect_to_database(host, username, password, database):
    try:
        # Establecer la conexión a la base de datos
        con = mysql.connector.connect(
            host=host,
            user=username,
            password=password,
            database=database
        )
        print("¡Conexión exitosa a la base de datos!")
        return con
    except mysql.connector.Error as e:
        print("Error al conectarse a la base de datos:", e)
        return None

# Configuración de la conexión
host = '149.50.138.155'  # Dirección IP del servidor de la base de datos
username = 'marcelo1234'  # Usuario de la base de datos
password = '1234'  # Contraseña de la base de datos
database = 'clientes'  # Nombre de la base de datos

# Intentar conectar a la base de datos
conexion = connect_to_database(host, username, password, database)

# Si la conexión fue exitosa, puedes ejecutar consultas SQL, etc.
if conexion:
    # Por ejemplo, crear un cursor para ejecutar consultas
    cursor = conexion.cursor()
    # Ejecutar una consulta
    cursor.execute("SELECT * FROM producto")
    # Obtener los resultados
    resultados = cursor.fetchall()
    # Hacer algo con los resultados
    print(resultados)
    # Cerrar la conexión cuando hayas terminado
    conexion.close()
