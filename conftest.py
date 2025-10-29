"""
conftest.py - Archivo de configuración compartida para todos los tests

IMPORTANTE: Este archivo es especial en pytest
- Se ejecuta AUTOMÁTICAMENTE antes de los tests
- No es necesario importarlo en los archivos de test
- pytest lo encuentra y carga automáticamente
- Define "fixtures" (recursos reutilizables) que los tests pueden solicitar como parámetros
"""

# ==================== IMPORTS ====================
import pytest  # Framework de testing
from selenium import webdriver  # Librería principal para controlar el navegador
from selenium.webdriver.chrome.service import Service  # Gestiona el driver de Chrome
from selenium.webdriver.chrome.options import Options  # Para configurar opciones de Chrome
from webdriver_manager.chrome import ChromeDriverManager  # Descarga automática del driver
from datetime import datetime  # Para trabajar con fechas y horas
from utils.database import TestDatabase  # Clase personalizada de base de datos

# ==================== CONSTANTES GLOBALES ====================
# URLs de los ambientes de prueba (definidas en el PDF de la prueba técnica)
BASE_URL_QA4 = "https://nuxqa4.avtest.ink/"  # Ambiente QA4
BASE_URL_QA5 = "https://nuxqa5.avtest.ink/"  # Ambiente QA5

# ==================== FIXTURE: DRIVER DEL NAVEGADOR ====================
@pytest.fixture(scope="function")
def driver(request):
    """
    Fixture principal: crea, configura y destruye el navegador para cada test.

    ¿Qué es una fixture?
    - Función que prepara recursos necesarios para los tests
    - Se ejecuta automáticamente cuando un test la solicita como parámetro
    - Ejemplo: def test_algo(driver): <- pytest detecta "driver" y ejecuta esta fixture

    scope="function":
    - Crea un navegador NUEVO para cada test individual
    - Alternativas: 
        "class"     (uno por clase), 
        "module"    (uno por archivo), 
        "session"   (uno para todos)

    request:
    - Objeto de pytest con información del test que solicita esta fixture
    - Útil para capturar nombre del test, parámetros, etc.
    """

    # PASO 1: Crear objeto de opciones de Chrome
    chrome_options = Options()  # Almacena las configuraciones del navegador

    # PASO 2: Configurar comportamiento del navegador
    # chrome_options.add_argument("--headless")  # Descomentar para modo invisible (sin ventana)
    chrome_options.add_argument("--start-maximized")  # Ventana maximizada desde el inicio
    chrome_options.add_argument("--disable-notifications")  # Bloquea notificaciones
    chrome_options.add_argument("--disable-popup-blocking")  # Permite popups (algunos sitios los usan)
    chrome_options.add_argument("--disable-blink-features=AutomationControlled")  # Oculta detección de Selenium

    # PASO 3: Crear servicio del driver
    # ChromeDriverManager().install() descarga automáticamente el driver compatible con Chrome instalado
    # Service() envuelve el driver para que Selenium pueda usarlo
    service = Service(ChromeDriverManager().install())

    # PASO 4: Crear instancia del navegador Chrome
    driver = webdriver.Chrome(
        service=service,  # Servicio con el driver descargado
        options=chrome_options  # Opciones configuradas arriba
    )

    # PASO 5: Configurar esperas implícitas (MUY IMPORTANTE)
    # Al buscar un elemento, espera hasta 10 segundos antes de fallar
    # Útil cuando los elementos tardan en cargar (animaciones, AJAX, etc.)
    driver.implicitly_wait(10)

    # PASO 6: YIELD - Pausa aquí y entrega el driver al test
    # Todo lo de ARRIBA = SETUP (preparación del navegador)
    # yield = entrega el driver y espera a que termine el test
    # El test se ejecuta con el driver...
    yield driver

    # PASO 7: TEARDOWN - Se ejecuta DESPUÉS de que termina el test
    # quit() cierra el navegador y libera recursos de memoria
    # IMPORTANTE: Se ejecuta SIEMPRE, incluso si el test falló
    driver.quit()


# ==================== FIXTURE: URL BASE ====================
@pytest.fixture(scope="function")
def base_url():
    """
    Fixture de URL base: proporciona la URL del sitio a probar.

    Ventajas de usar fixture en vez de constante directa:
    - Permite cambiarla dinámicamente según parámetros
    - Permite leer de variables de entorno
    - Centraliza la configuración del ambiente

    scope="function":
    - Se ejecuta para cada test (aunque solo retorna un valor)
    """
    return BASE_URL_QA4  # Por defecto retorna QA4, puede cambiarse a QA5 según necesidad


# ==================== FIXTURE: BASE DE DATOS ====================
@pytest.fixture(scope="session")
def db():
    """
    Fixture de base de datos: crea y proporciona conexión a SQLite.

    scope="session":
    - Se crea UNA SOLA VEZ al inicio de la sesión de tests
    - TODOS los tests comparten la misma instancia
    - Se destruye al final cuando todos los tests terminan

    ¿Por qué "session" y no "function"?
    - Crear la BD y tablas muchas veces sería lento e innecesario
    - Los resultados deben acumularse en la misma BD
    """
    database = TestDatabase()  # Crea instancia de la clase de BD
    yield database  # Entrega la conexión a los tests que la soliciten
    database.close()  # Cierra conexión al terminar todos los tests


# ==================== HOOK: CAPTURA DE RESULTADOS ====================
def pytest_runtest_makereport(item, call):
    """
    Hook de pytest: se ejecuta después de cada fase de los tests.

    ¿Qué es un hook?
    - Función con nombre especial que pytest reconoce automáticamente
    - pytest la llama en el momento correcto del ciclo de vida
    - Permite interceptar eventos del ciclo de vida de los tests

    Parámetros:
    - item: Objeto del test que se ejecutó (nombre, ubicación, etc.)
    - call: Información de la ejecución (resultado, excepción, tiempo)

    Fases de un test (call.when):
    - "setup": Preparación (las fixtures se ejecutan)
    - "call": Ejecución del test en sí (código de prueba)
    - "teardown": Limpieza (cierre de navegador, etc.)

    Usos comunes:
    - Capturar screenshots cuando un test falla
    - Guardar logs adicionales
    - Enviar notificaciones
    """
    if call.when == "call":  # Solo interesa la fase de ejecución del test
        if call.excinfo is not None:  # excinfo != None significa que el test falló
            # Aquí se puede agregar en el futuro:
            # driver = item.funcargs.get('driver')  # Obtener el driver del test
            # driver.save_screenshot(f"error_{item.name}.png")  # Guardar screenshot del error
            pass  # Por ahora no hace nada, pero el hook está listo para extenderse
