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
        - case_number: Número del caso de prueba (4, 5, 6, 7)
        - test_name: Nombre del test (ej: "test_cambiar_idioma")
        - status: Resultado ("PASSED", "FAILED", "SKIPPED")
        - execution_time: Duración en segundos
        - error_message: Mensaje de error si falló
        - timestamp: Fecha/hora de ejecución (se asigna automáticamente)
        - browser: Navegador usado (chrome, firefox, edge)
        - url: URL final después de la acción
        - language: Idioma usado en el test

        NUEVOS CAMPOS GENERALES:
        - environment: Ambiente de prueba (qa4, qa5)
        - screenshots_mode: Modo de captura (none, on-failure, all)
        - video_enabled: Si el video estaba habilitado (enabled, none)
        - expected_value: Valor esperado en validación
        - actual_value: Valor obtenido en validación
        - validation_result: Resultado de la validación (PASSED, FAILED)
        - initial_url: URL antes de la acción

        CAMPOS ESPECÍFICOS POR CASO:
        - pos: Case 5 - POS seleccionado (Chile, España, Otros países)
        - header_link: Case 6 - Link del header probado
        - footer_link: Case 7 - Link del footer probado
        - link_name: Cases 6&7 - Nombre descriptivo del link
        - language_mode: Cases 6&7 - Modo de idioma (Random, Specific, All Languages)
        - validation_message: Mensaje detallado de validación
        """
        # Crea o abre conexión al archivo de base de datos
        self.connection = sqlite3.connect(self.db_name)

        # Cursor: Objeto que ejecuta comandos SQL en la BD
        cursor = self.connection.cursor()

        # Ejecuta SQL para crear la tabla
        cursor.execute("""
            CREATE TABLE IF NOT EXISTS test_executions (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                case_number TEXT,
                test_name TEXT NOT NULL,
                status TEXT NOT NULL,
                execution_time REAL,
                error_message TEXT,
                timestamp DATETIME DEFAULT CURRENT_TIMESTAMP,
                browser TEXT,
                url TEXT,
                language TEXT,
                environment TEXT,
                screenshots_mode TEXT,
                video_enabled TEXT,
                expected_value TEXT,
                actual_value TEXT,
                validation_result TEXT,
                initial_url TEXT,
                pos TEXT,
                header_link TEXT,
                footer_link TEXT,
                link_name TEXT,
                language_mode TEXT,
                validation_message TEXT
            )
        """)

        # commit() guarda los cambios en el archivo .db del disco
        # IMPORTANTE: Sin commit(), los cambios quedan solo en memoria y se pierden
        self.connection.commit()

    def save_test_result(self, test_name, status, execution_time=None,
                        error_message=None, browser="chrome", url=None, language=None, case_number=None,
                        environment=None, screenshots_mode=None, video_enabled=None,
                        expected_value=None, actual_value=None, validation_result=None,
                        initial_url=None, pos=None, header_link=None, footer_link=None,
                        link_name=None, language_mode=None, validation_message=None):
        """
        Inserta un nuevo registro con el resultado de un test ejecutado.

        PARÁMETROS OBLIGATORIOS:
        - test_name (str): Nombre del test ejecutado
        - status (str): "PASSED", "FAILED", o "SKIPPED"

        PARÁMETROS GENERALES:
        - execution_time (float): Segundos que tardó el test
        - error_message (str): Mensaje de error si falló
        - browser (str): Navegador usado (chrome, firefox, edge)
        - url (str): URL final después de la acción
        - language (str): Idioma del test (Español, English, Français, Português)
        - case_number (str): Número del caso de prueba ("4", "5", "6", "7")
        - environment (str): Ambiente de prueba (qa4, qa5)
        - screenshots_mode (str): Modo de captura (none, on-failure, all)
        - video_enabled (str): Si el video estaba habilitado (enabled, none)
        - expected_value (str): Valor esperado en validación
        - actual_value (str): Valor obtenido en validación
        - validation_result (str): Resultado de la validación (PASSED, FAILED)
        - initial_url (str): URL antes de la acción

        PARÁMETROS ESPECÍFICOS POR CASO:
        - pos (str): Case 5 - POS seleccionado (Chile, España, Otros países)
        - header_link (str): Case 6 - Link del header probado (ofertas-vuelos, credits, etc.)
        - footer_link (str): Case 7 - Link del footer probado (vuelos, noticias, etc.)
        - link_name (str): Cases 6&7 - Nombre descriptivo del link
        - language_mode (str): Cases 6&7 - Modo de idioma (Random, Specific, All Languages)
        - validation_message (str): Mensaje detallado de validación

        Uso de ? en SQL:
        - Los ? son placeholders (marcadores de posición)
        - Previenen SQL injection (inyección de código malicioso)
        - sqlite3 reemplaza cada ? con los valores de la tupla en orden
        """
        cursor = self.connection.cursor()  # Obtiene el cursor

        # INSERT: Agrega nuevo registro a la tabla con TODOS los campos
        cursor.execute("""
            INSERT INTO test_executions
            (case_number, test_name, status, execution_time, error_message, browser, url, language,
             environment, screenshots_mode, video_enabled, expected_value, actual_value,
             validation_result, initial_url, pos, header_link, footer_link, link_name,
             language_mode, validation_message)
            VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
        """, (case_number, test_name, status, execution_time, error_message, browser, url, language,
              environment, screenshots_mode, video_enabled, expected_value, actual_value,
              validation_result, initial_url, pos, header_link, footer_link, link_name,
              language_mode, validation_message))

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
