"""
database.py - Archivo para gestionar la base de datos SQLite de resultados

SQLite - Base de datos ligera que:
- Se almacena en un solo archivo (.db)
- No requiere instalar servidor (como MySQL o PostgreSQL)
- Perfecta para almacenar datos locales de tests
"""

# ==================== IMPORTS ====================
import sqlite3  # Librería estándar de Python para trabajar con SQLite
from datetime import datetime  # Para manejar fechas y horas
import os  # Para operaciones del sistema operativo (rutas, archivos, etc.)


# ==================== CLASE DE BASE DE DATOS ====================
class TestDatabase:
    """
    Clase que encapsula todas las operaciones con la BD de resultados.

    Responsabilidades:
    - Crear la base de datos y tabla si no existen
    - Guardar resultados de cada test ejecutado
    - Consultar resultados históricos

    Patrón: Una sola instancia para toda la sesión de tests (singleton implícito)
    """

    def __init__(self, db_name="test_results.db"):
        """
        Constructor: Inicializa la conexión a la base de datos.

        Parámetros:
        - db_name: Nombre del archivo de BD (por defecto: "test_results.db")

        Flujo:
        1. Guarda el nombre del archivo .db
        2. Inicializa la variable de conexión
        3. Llama a create_tables() para asegurar que existe la estructura
        """
        self.db_name = db_name  # Nombre del archivo .db
        self.connection = None  # Almacenará el objeto de conexión sqlite3
        self.create_tables()  # Crea tabla si no existe (método definido abajo)

    def create_tables(self):
        """
        Crea la tabla test_executions si no existe.

        IF NOT EXISTS:
        - La primera vez: crea la tabla
        - Siguientes veces: no hace nada (preserva datos existentes)

        Estructura de la tabla:
        - id: Identificador único autoincremental
        - test_name: Nombre del test (ej: "test_cambiar_idioma")
        - status: Resultado ("PASSED", "FAILED", "SKIPPED")
        - execution_time: Duración en segundos
        - error_message: Mensaje de error si falló
        - timestamp: Fecha/hora de ejecución (se asigna automáticamente)
        - browser: Navegador usado (chrome, firefox, edge)
        - url: URL del sitio probado
        """
        # Crea o abre conexión al archivo de base de datos
        self.connection = sqlite3.connect(self.db_name)

        # Cursor: Objeto que ejecuta comandos SQL en la BD
        cursor = self.connection.cursor()

        # Ejecuta SQL para crear la tabla
        cursor.execute("""
            CREATE TABLE IF NOT EXISTS test_executions (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                test_name TEXT NOT NULL,
                status TEXT NOT NULL,
                execution_time REAL,
                error_message TEXT,
                timestamp DATETIME DEFAULT CURRENT_TIMESTAMP,
                browser TEXT,
                url TEXT
            )
        """)

        # commit() guarda los cambios en el archivo .db del disco
        # IMPORTANTE: Sin commit(), los cambios quedan solo en memoria y se pierden
        self.connection.commit()

    def save_test_result(self, test_name, status, execution_time=None,
                        error_message=None, browser="chrome", url=None):
        """
        Inserta un nuevo registro con el resultado de un test ejecutado.

        Parámetros:
        - test_name (str): Nombre del test ejecutado (obligatorio)
        - status (str): "PASSED", "FAILED", o "SKIPPED" (obligatorio)
        - execution_time (float): Segundos que tardó el test (opcional)
        - error_message (str): Mensaje de error si falló (opcional)
        - browser (str): Navegador usado (por defecto: "chrome")
        - url (str): URL probada (opcional)

        Uso de ? en SQL:
        - Los ? son placeholders (marcadores de posición)
        - Previenen SQL injection (inyección de código malicioso)
        - sqlite3 reemplaza cada ? con los valores de la tupla en orden
        """
        cursor = self.connection.cursor()  # Obtiene el cursor

        # INSERT: Agrega nuevo registro a la tabla
        # Los ? se reemplazan con los valores de la tupla en el segundo argumento
        cursor.execute("""
            INSERT INTO test_executions
            (test_name, status, execution_time, error_message, browser, url)
            VALUES (?, ?, ?, ?, ?, ?)
        """, (test_name, status, execution_time, error_message, browser, url))

        self.connection.commit()  # Guarda cambios en disco

    def get_all_results(self):
        """
        Obtiene TODOS los resultados de tests almacenados.

        Retorna:
        - Lista de tuplas, cada tupla es un registro completo
        - Ordenados por timestamp descendente (más reciente primero)

        Ejemplo de retorno:
        [
            (1, "test_login", "PASSED", 2.5, None, "2024-01-01 10:00:00", "chrome", "https://..."),
            (2, "test_logout", "FAILED", 1.2, "Element not found", "2024-01-01 10:05:00", "chrome", "https://...")
        ]
        """
        cursor = self.connection.cursor()

        # SELECT: Consulta los datos
        # ORDER BY timestamp DESC: Más recientes primero
        cursor.execute("SELECT * FROM test_executions ORDER BY timestamp DESC")

        # fetchall(): Trae TODOS los registros y los retorna como lista de tuplas
        return cursor.fetchall()

    def get_latest_results(self, limit=10):
        """
        Obtiene los últimos N resultados (más recientes).

        Parámetros:
        - limit (int): Cantidad de resultados a retornar (por defecto: 10)

        Diferencia con get_all_results():
        - get_all_results() trae TODO (puede ser miles de registros)
        - Este método limita la cantidad con LIMIT

        Nota sobre (limit,) con coma:
        - Python requiere una tupla para los parámetros
        - (limit,) con coma = tupla de 1 elemento
        - (limit) sin coma = solo un número entre paréntesis (NO es tupla)
        """
        cursor = self.connection.cursor()

        cursor.execute(
            "SELECT * FROM test_executions ORDER BY timestamp DESC LIMIT ?",
            (limit,)  # Tupla con el parámetro limit
        )

        # fetchall() retorna solo los registros limitados
        return cursor.fetchall()

    def close(self):
        """
        Cierra la conexión a la base de datos.

        Importante:
        - Libera recursos del sistema
        - Asegura que los últimos cambios se escriban al disco
        - Buena práctica: siempre cerrar conexiones al terminar

        ¿Por qué if self.connection?
        - Valida que exista la conexión antes de cerrarla
        - Previene errores si close() se llama múltiples veces
        """
        if self.connection:  # Solo si hay una conexión activa
            self.connection.close()  # Cierra la conexión
