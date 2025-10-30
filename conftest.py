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
from selenium.webdriver.chrome.service import Service as ChromeService  # Gestiona el driver de Chrome
from selenium.webdriver.chrome.options import Options as ChromeOptions  # Para configurar opciones de Chrome
from selenium.webdriver.edge.service import Service as EdgeService  # Gestiona el driver de Edge
from selenium.webdriver.edge.options import Options as EdgeOptions  # Para configurar opciones de Edge
from selenium.webdriver.firefox.service import Service as FirefoxService  # Gestiona el driver de Firefox
from selenium.webdriver.firefox.options import Options as FirefoxOptions  # Para configurar opciones de Firefox
from webdriver_manager.chrome import ChromeDriverManager  # Descarga automática del driver Chrome
from webdriver_manager.microsoft import EdgeChromiumDriverManager  # Descarga automática del driver Edge
from webdriver_manager.firefox import GeckoDriverManager  # Descarga automática del driver Firefox
from datetime import datetime  # Para trabajar con fechas y horas
from utils.database import TestDatabase  # Clase personalizada de base de datos

# ==================== CONSTANTES GLOBALES ====================
# URLs de los ambientes de prueba (definidas en el PDF de la prueba técnica)
BASE_URL_QA4 = "https://nuxqa4.avtest.ink/"  # Ambiente QA4
BASE_URL_QA5 = "https://nuxqa5.avtest.ink/"  # Ambiente QA5

# ==================== OPCIONES PERSONALIZADAS CLI ====================
def pytest_addoption(parser):
    """
    Hook que agrega opciones personalizadas a la línea de comandos de pytest.

    Opciones agregadas:
    - --browser: Selecciona navegador(es) para ejecutar tests
    - --language: Selecciona idioma(s) para ejecutar tests

    Uso:
    pytest --browser=chrome --language=Español
    pytest --browser=all --language=all
    """
    parser.addoption(
        "--browser",
        action="store",
        default="all",
        help="Browser to run tests on: chrome, edge, firefox, or all (default: all)"
    )
    parser.addoption(
        "--language",
        action="store",
        default="all",
        help="Language to test: Español, English, Français, Português, or all (default: all)"
    )
    parser.addoption(
        "--env",
        action="store",
        default="all",
        help="Environment to test: qa4, qa5, or all (default: all)"
    )

def pytest_generate_tests(metafunc):
    """
    Hook que genera parametrizaciones dinámicas basadas en opciones CLI.

    metafunc: Objeto con información sobre la función de test.

    Funcionamiento:
    1. Lee las opciones --browser, --language, --env
    2. Filtra los valores según lo especificado
    3. Parametriza automáticamente los tests
    """
    # Obtener valores de las opciones CLI
    browser_option = metafunc.config.getoption("browser")
    language_option = metafunc.config.getoption("language")
    env_option = metafunc.config.getoption("env")

    # Definir todos los navegadores disponibles
    all_browsers = ["chrome", "edge", "firefox"]

    # Definir todos los idiomas disponibles
    all_languages = ["Español", "English", "Français", "Português"]

    # Definir todos los ambientes disponibles
    all_envs = {
        "qa4": BASE_URL_QA4,
        "qa5": BASE_URL_QA5
    }

    # Filtrar navegadores según opción
    if "browser" in metafunc.fixturenames:
        if browser_option == "all":
            browsers = all_browsers
        else:
            browsers = [browser_option] if browser_option in all_browsers else all_browsers
        metafunc.parametrize("browser", browsers, scope="function")

    # Filtrar idiomas según opción
    if "language" in metafunc.fixturenames:
        if language_option == "all":
            languages = all_languages
        else:
            languages = [language_option] if language_option in all_languages else all_languages
        metafunc.parametrize("language", languages, scope="function")

    # Filtrar ambientes según opción
    if "base_url" in metafunc.fixturenames:
        if env_option == "all":
            envs = list(all_envs.values())
        else:
            envs = [all_envs[env_option]] if env_option in all_envs else list(all_envs.values())
        metafunc.parametrize("base_url", envs, scope="function")

# ==================== FIXTURE: DRIVER DEL NAVEGADOR ====================
@pytest.fixture(scope="function")
def driver(request, browser):
    """
    Fixture principal: crea, configura y destruye el navegador para cada test.

    Parámetros:
    - request: Objeto de pytest con información del test
    - browser: Parámetro que indica qué navegador usar (chrome o edge)
                Viene de pytest_generate_tests según opción CLI

    Navegadores soportados:
    - chrome: Google Chrome
    - edge: Microsoft Edge

    scope="function": Crea un navegador NUEVO para cada test individual
    """

    # PASO 1: Configurar opciones comunes para todos los navegadores
    common_args = [
        "--start-maximized",  # Ventana maximizada
        "--disable-notifications",  # Bloquea notificaciones
        "--disable-popup-blocking",  # Permite popups
        "--disable-blink-features=AutomationControlled"  # Oculta detección de Selenium
    ]

    # PASO 2: Crear navegador según parámetro
    if browser == "chrome":
        # Configurar Chrome
        chrome_options = ChromeOptions()
        for arg in common_args:
            chrome_options.add_argument(arg)
        # chrome_options.add_argument("--headless")  # Descomentar para modo invisible

        service = ChromeService(ChromeDriverManager().install())
        driver = webdriver.Chrome(service=service, options=chrome_options)

    elif browser == "edge":
        # Configurar Edge
        edge_options = EdgeOptions()
        for arg in common_args:
            edge_options.add_argument(arg)
        # edge_options.add_argument("--headless")  # Descomentar para modo invisible

        # Usar Selenium Manager (no requiere webdriver-manager)
        driver = webdriver.Edge(options=edge_options)

    elif browser == "firefox":
        # Configurar Firefox
        firefox_options = FirefoxOptions()
        # Firefox usa diferentes nombres para algunas opciones
        # firefox_options.add_argument("--headless")  # Descomentar para modo invisible

        service = FirefoxService(GeckoDriverManager().install())
        driver = webdriver.Firefox(service=service, options=firefox_options)

    else:
        raise ValueError(f"Browser '{browser}' not supported. Use 'chrome', 'edge', or 'firefox'.")

    # PASO 3: Configurar esperas implícitas (para todos los navegadores)
    driver.implicitly_wait(10)

    # PASO 4: YIELD - Entrega el driver al test
    yield driver

    # PASO 5: TEARDOWN - Cierra el navegador después del test
    driver.quit()


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
