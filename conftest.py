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
from selenium.webdriver.chrome.options import Options as ChromeOptions  # Para configurar opciones de Chrome
from selenium.webdriver.edge.options import Options as EdgeOptions  # Para configurar opciones de Edge
from selenium.webdriver.firefox.options import Options as FirefoxOptions  # Para configurar opciones de Firefox
from datetime import datetime  # Para trabajar con fechas y horas
from utils.database import TestDatabase  # Clase personalizada de base de datos
import allure  # Para adjuntar evidencias a los reportes
import cv2  # OpenCV para grabación de video
import numpy as np  # Para manejo de arrays en video
from PIL import ImageGrab  # Para capturar screenshots en Windows
import os  # Para operaciones con archivos
import threading  # Para captura de frames en background
import time  # Para delays en captura de frames
import re  # Para sanitizar nombres de archivos
import traceback  # Para logging detallado de errores

# ==================== CONSTANTES GLOBALES ====================
# URLs de los ambientes de prueba (definidas en el PDF de la prueba técnica)
BASE_URL_QA4 = "https://nuxqa4.avtest.ink/"  # Ambiente QA4
BASE_URL_QA5 = "https://nuxqa5.avtest.ink/"  # Ambiente QA5

# ==================== FUNCIÓN AUXILIAR ====================
def sanitize_filename(filename):
    """
    Sanitiza un nombre de archivo removiendo caracteres inválidos para Windows.

    Caracteres prohibidos en Windows: < > : " / \\ | ? *
    También remueve brackets [] que causan problemas.

    Args:
        filename: Nombre original del archivo

    Returns:
        Nombre sanitizado con guiones bajos en lugar de caracteres inválidos
    """
    # Reemplazar caracteres inválidos con guiones bajos
    invalid_chars = r'[<>:"/\\|?*\[\]]'
    sanitized = re.sub(invalid_chars, '_', filename)
    # Limpiar guiones bajos múltiples consecutivos
    sanitized = re.sub(r'_+', '_', sanitized)
    return sanitized


# ==================== CLASE PARA GRABACIÓN DE VIDEO ====================
class VideoRecorder:
    """
    Clase para grabar video de las ejecuciones de tests.

    Captura frame por frame la ventana del navegador y genera un archivo MP4.
    """

    def __init__(self, driver, filename="test_video.mp4", fps=10):
        """
        Inicializa el grabador de video.

        Args:
            driver: WebDriver de Selenium
            filename: Nombre del archivo de salida
            fps: Frames por segundo (menor = menos pesado)
        """
        self.driver = driver
        self.filename = filename
        self.fps = fps
        self.frames = []
        self.is_recording = False

    def start(self):
        """Inicia la grabación en un thread separado."""
        self.is_recording = True
        self.frames = []
        # Iniciar thread que captura frames automáticamente
        self.recording_thread = threading.Thread(target=self._capture_loop, daemon=True)
        self.recording_thread.start()

    def _capture_loop(self):
        """Loop que captura frames continuamente mientras graba."""
        frame_count = 0
        while self.is_recording:
            try:
                # Capturar screenshot como PNG bytes
                screenshot = self.driver.get_screenshot_as_png()
                # Convertir a numpy array para OpenCV
                import io
                from PIL import Image
                img = Image.open(io.BytesIO(screenshot))
                frame = cv2.cvtColor(np.array(img), cv2.COLOR_RGB2BGR)
                self.frames.append(frame)
                frame_count += 1
            except Exception as e:
                # Ignorar errores silenciosamente (ej: ventana cerrada)
                pass
            # Esperar antes del siguiente frame (con FPS=2, sleep=0.5 segundos)
            time.sleep(1.0 / self.fps)

    def stop(self):
        """Detiene la grabación y guarda el video."""
        self.is_recording = False

        # Esperar a que el thread termine
        if hasattr(self, 'recording_thread'):
            self.recording_thread.join(timeout=2.0)

        if not self.frames:
            print("[VIDEO ERROR] No frames captured, skipping video creation")
            return None

        try:
            # Obtener dimensiones del primer frame
            height, width, _ = self.frames[0].shape
            print(f"[VIDEO DEBUG] Video dimensions: {width}x{height}")
            print(f"[VIDEO DEBUG] Total frames to write: {len(self.frames)}")
            print(f"[VIDEO DEBUG] Output file: {self.filename}")

            # Crear video writer
            fourcc = cv2.VideoWriter_fourcc(*'mp4v')
            video_writer = cv2.VideoWriter(self.filename, fourcc, self.fps, (width, height))

            # Verificar que el video writer se creó correctamente
            if not video_writer.isOpened():
                print(f"[VIDEO ERROR] VideoWriter failed to open file: {self.filename}")
                return None

            # Escribir todos los frames
            for i, frame in enumerate(self.frames):
                video_writer.write(frame)
                if i % 5 == 0:  # Log cada 5 frames
                    print(f"[VIDEO DEBUG] Written frame {i+1}/{len(self.frames)}")

            video_writer.release()
            print(f"[VIDEO DEBUG] VideoWriter released successfully")

            # Verificar que el archivo se creó
            if os.path.exists(self.filename):
                file_size = os.path.getsize(self.filename)
                print(f"[VIDEO DEBUG] File created: {self.filename} ({file_size} bytes)")
                return self.filename
            else:
                print(f"[VIDEO ERROR] File not found after creation: {self.filename}")
                return None

        except Exception as e:
            print(f"[VIDEO ERROR] Exception creating video: {e}")
            print(f"[VIDEO ERROR] Full traceback:")
            traceback.print_exc()
            return None

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
        "--pos",
        action="store",
        default="all",
        help="POS to test: Chile, España, Otros países, or all (default: all)"
    )
    parser.addoption(
        "--header-link",
        action="store",
        default="all",
        help="Header link to test: hoteles, credits, equipaje, or all (default: all)"
    )
    parser.addoption(
        "--footer-link",
        action="store",
        default="all",
        help="Footer link to test: vuelos, trabajos, aviancadirect, articulos, or all (default: all)"
    )
    parser.addoption(
        "--env",
        action="store",
        default="all",
        help="Environment to test: qa4, qa5, or all (default: all)"
    )
    parser.addoption(
        "--screenshots",
        action="store",
        default="on-failure",
        help="Screenshot capture mode: none, on-failure, or all (default: on-failure)"
    )
    parser.addoption(
        "--video",
        action="store",
        default="none",
        help="Video recording mode: none or enabled (default: none)"
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
    pos_option = metafunc.config.getoption("pos")
    header_link_option = metafunc.config.getoption("header_link")  # pytest convierte guiones a guiones bajos
    footer_link_option = metafunc.config.getoption("footer_link")  # pytest convierte guiones a guiones bajos
    env_option = metafunc.config.getoption("env")

    # Definir todos los navegadores disponibles
    all_browsers = ["chrome", "edge", "firefox"]

    # Definir todos los idiomas disponibles
    all_languages = ["Español", "English", "Français", "Português"]

    # Definir todos los POS disponibles
    all_pos = ["Chile", "España", "Otros países"]

    # Definir todos los header links disponibles
    all_header_links = ["hoteles", "credits", "equipaje"]

    # Definir todos los footer links disponibles
    all_footer_links = ["vuelos", "trabajos", "aviancadirect", "articulos"]

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

    # Filtrar POS según opción
    if "pos" in metafunc.fixturenames:
        if pos_option == "all":
            pos_list = all_pos
        else:
            pos_list = [pos_option] if pos_option in all_pos else all_pos
        metafunc.parametrize("pos", pos_list, scope="function")

    # Filtrar header links según opción
    if "header_link" in metafunc.fixturenames:
        if header_link_option == "all":
            header_links = all_header_links
        else:
            header_links = [header_link_option] if header_link_option in all_header_links else all_header_links
        metafunc.parametrize("header_link", header_links, scope="function")

    # Filtrar footer links según opción
    if "footer_link" in metafunc.fixturenames:
        if footer_link_option == "all":
            footer_links = all_footer_links
        else:
            footer_links = [footer_link_option] if footer_link_option in all_footer_links else all_footer_links
        metafunc.parametrize("footer_link", footer_links, scope="function")

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
    - browser: Parámetro que indica qué navegador usar (chrome, edge o firefox)
                Viene de pytest_generate_tests según opción CLI

    Navegadores soportados:
    - chrome: Google Chrome
    - edge: Microsoft Edge
    - firefox: Mozilla Firefox

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

        # Usar Selenium Manager (integrado en Selenium 4.x)
        # No requiere webdriver-manager, descarga el driver automáticamente
        driver = webdriver.Chrome(options=chrome_options)

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

        # Usar Selenium Manager (integrado en Selenium 4.x)
        # No requiere webdriver-manager, descarga el driver automáticamente
        driver = webdriver.Firefox(options=firefox_options)

    else:
        raise ValueError(f"Browser '{browser}' not supported. Use 'chrome', 'edge', or 'firefox'.")

    # PASO 3: Configurar esperas implícitas (para todos los navegadores)
    driver.implicitly_wait(10)

    # PASO 3.5: Iniciar grabación de video si está habilitado
    video_mode = request.config.getoption("--video")
    video_recorder = None

    if video_mode == "enabled":
        # Crear nombre único para el video (sanitizar para evitar caracteres inválidos)
        test_name = request.node.name
        sanitized_test_name = sanitize_filename(test_name)
        video_filename = f"reports/{sanitized_test_name}.mp4"

        # Crear directorio si no existe
        os.makedirs("reports", exist_ok=True)

        # Crear y iniciar el recorder (FPS bajo = 2 para no saturar Selenium)
        video_recorder = VideoRecorder(driver, filename=video_filename, fps=2)
        video_recorder.start()
        print(f"\n[VIDEO] Recording started: {video_filename}")
        print(f"[VIDEO] Original test name: {test_name}")
        print(f"[VIDEO] Sanitized filename: {sanitized_test_name}")

    # PASO 4: YIELD - Entrega el driver al test
    yield driver

    # PASO 5: TEARDOWN - Detener video y adjuntar a Allure si está habilitado
    if video_recorder:
        print(f"[VIDEO] Stopping recording...")
        video_file = video_recorder.stop()

        if video_file and os.path.exists(video_file):
            print(f"[VIDEO] Video created successfully: {video_file}")
            print(f"[VIDEO] File size: {os.path.getsize(video_file) / (1024*1024):.2f} MB")
            print(f"[VIDEO] Total frames captured: {len(video_recorder.frames)}")

            # Adjuntar video a Allure
            try:
                with open(video_file, 'rb') as f:
                    allure.attach(
                        f.read(),
                        name="Test Execution Video",
                        attachment_type=allure.attachment_type.MP4
                    )
                print(f"[VIDEO] Video attached to Allure successfully")
            except Exception as e:
                print(f"[VIDEO] Error attaching to Allure: {e}")

            # Eliminar archivo temporal
            try:
                os.remove(video_file)
                print(f"[VIDEO] Temporary file removed")
            except Exception as e:
                print(f"[VIDEO] Error removing file: {e}")
        else:
            print(f"[VIDEO] No video file created or file doesn't exist")
            print(f"[VIDEO] Frames captured: {len(video_recorder.frames) if video_recorder.frames else 0}")

    # PASO 6: Cierra el navegador después del test
    driver.quit()


# ==================== FIXTURE: SCREENSHOTS MODE ====================
@pytest.fixture(scope="session")
def screenshots_mode(request):
    """
    Fixture que devuelve el modo de captura de screenshots según opción CLI.

    Valores posibles:
    - "none": Sin screenshots
    - "on-failure": Solo cuando falla (default)
    - "all": Screenshots en todos los pasos

    scope="session": Se evalúa una sola vez para toda la sesión
    """
    return request.config.getoption("--screenshots")


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


# ==================== FUNCIONES HELPER PARA EVIDENCIAS ====================
def take_screenshot(driver, name="screenshot"):
    """
    Captura un screenshot del navegador y lo adjunta a Allure.

    Parámetros:
    - driver: Instancia del WebDriver
    - name: Nombre descriptivo del screenshot
    """
    try:
        # Capturar screenshot como bytes
        screenshot_bytes = driver.get_screenshot_as_png()

        # Adjuntar a Allure con nombre descriptivo
        allure.attach(
            screenshot_bytes,
            name=name,
            attachment_type=allure.attachment_type.PNG
        )
    except Exception as e:
        print(f"Error capturing screenshot: {e}")


# ==================== HOOK: CAPTURA DE SCREENSHOTS EN FALLOS ====================
@pytest.hookimpl(tryfirst=True, hookwrapper=True)
def pytest_runtest_makereport(item, call):
    """
    Hook de pytest: captura screenshots automáticamente cuando un test falla.

    Funcionamiento:
    1. pytest ejecuta este hook después de cada fase del test
    2. Si el test falla (call.excinfo != None), captura screenshot
    3. El screenshot se adjunta automáticamente al reporte de Allure

    Parámetros:
    - item: Objeto del test que se ejecutó
    - call: Información de la ejecución (resultado, excepción)
    """
    # Ejecutar el hook normalmente
    outcome = yield
    report = outcome.get_result()

    # Obtener el modo de screenshots de la configuración CLI
    screenshots_mode = item.config.getoption("--screenshots")

    # Solo capturar screenshot si:
    # 1. El test falló en la fase "call"
    # 2. El modo de screenshots es "on-failure" o "all"
    if report.when == "call" and report.failed and screenshots_mode in ["on-failure", "all"]:
        # Obtener el driver del test
        driver = item.funcargs.get('driver', None)

        if driver:
            # Capturar screenshot con nombre descriptivo
            test_name = item.name
            take_screenshot(driver, name=f"FAILURE - {test_name}")
