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
import sys  # Para manipular el path de Python
from pathlib import Path  # Para manejo de rutas de archivos

# Agregar la carpeta ide_test al path para importar ConfigManager
sys.path.append(str(Path(__file__).parent / "ide_test"))
from core.config_manager import ConfigManager  # Gestor de configuraciones JSON

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

# ==================== HELPERS PARA CONFIGURACIÓN DINÁMICA ====================
def _get_available_environments():
    """
    Carga la lista de ambientes disponibles desde parameter_options.json

    Returns:
        Lista de environment keys definidos en el archivo JSON de configuración
    """
    try:
        config_mgr = ConfigManager()
        env_options = config_mgr.get_parameter_options("env")
        if env_options:
            # Retornar solo los keys que no sean "all" y tengan base_url
            return [key for key in env_options.keys() if key != "all" and "base_url" in env_options[key]]
        return []
    except Exception:
        return []

def _get_parameter_keys(parameter_name, exclude_all=True):
    """
    Carga las opciones disponibles para cualquier parámetro desde parameter_options.json

    Args:
        parameter_name: Nombre del parámetro en JSON
        exclude_all: Si True, excluye la opción "all" de la lista

    Returns:
        Lista de keys disponibles para el parámetro desde JSON
    """
    try:
        config_mgr = ConfigManager()
        options = config_mgr.get_parameter_options(parameter_name)
        if options:
            keys = list(options.keys())
            if exclude_all and "all" in keys:
                keys.remove("all")
            return keys
        return []
    except Exception:
        return []

def _get_parameter_display_names(parameter_name, exclude_all=True):
    """
    Carga los display_names de los parámetros desde parameter_options.json

    Args:
        parameter_name: Nombre del parámetro en JSON (ej: "language", "pos")
        exclude_all: Si True, excluye la opción "all" de la lista

    Returns:
        Lista de display_names disponibles para el parámetro desde JSON
        Ejemplo para language: ["Español", "English", "Français", "Português"]
    """
    try:
        config_mgr = ConfigManager()
        options = config_mgr.get_parameter_options(parameter_name)
        if options:
            display_names = []
            for key, value in options.items():
                if exclude_all and key == "all":
                    continue
                if isinstance(value, dict) and "display_name" in value:
                    display_names.append(value["display_name"])
            return display_names
        return []
    except Exception:
        return []

def _convert_cli_value_to_display_name(parameter_name, cli_value):
    """
    Convierte un valor CLI (key o command_value) a su display_name correspondiente.

    Args:
        parameter_name: Nombre del parámetro (ej: "language", "pos")
        cli_value: Valor desde CLI (ej: "español", "Español", etc.)

    Returns:
        display_name correspondiente o el valor original si no se encuentra
        Ejemplo: "español" -> "Español", "chile" -> "Chile"
    """
    try:
        config_mgr = ConfigManager()
        options = config_mgr.get_parameter_options(parameter_name)
        if options:
            # Buscar por key (ej: "español")
            if cli_value in options:
                return options[cli_value].get("display_name", cli_value)
            # Buscar por command_value (case-insensitive)
            for key, value in options.items():
                if isinstance(value, dict):
                    command_val = value.get("command_value", "")
                    display_name = value.get("display_name", "")
                    if command_val.lower() == cli_value.lower() or display_name.lower() == cli_value.lower():
                        return display_name
        return cli_value  # Si no se encuentra, devolver el valor original
    except Exception:
        return cli_value

# ==================== OPCIONES PERSONALIZADAS CLI ====================
def pytest_addoption(parser):
    """
    Hook que agrega opciones personalizadas a la línea de comandos de pytest.

    Opciones agregadas:
    - --browser: Selecciona navegador(es) para ejecutar tests
    - --language: Selecciona idioma(s) para ejecutar tests

    Uso:
    pytest --browser=<browser_option> --language=<language_option>
    pytest --browser=all --language=all
    """
    # Cargar todos los parámetros disponibles dinámicamente desde JSON para help texts
    available_envs = _get_available_environments()
    available_browsers = _get_parameter_keys("browser")
    available_languages = _get_parameter_keys("language")
    available_pos = _get_parameter_keys("pos")
    available_header_links = _get_parameter_keys("header-link")
    available_footer_links = _get_parameter_keys("footer-link")

    # Construir strings para help texts
    env_list_str = ", ".join(available_envs) if available_envs else "check parameter_options.json"
    browser_list_str = ", ".join(available_browsers) if available_browsers else "check parameter_options.json"
    language_list_str = ", ".join(available_languages) if available_languages else "check parameter_options.json"
    pos_list_str = ", ".join(available_pos) if available_pos else "check parameter_options.json"
    header_link_list_str = ", ".join(available_header_links) if available_header_links else "check parameter_options.json"
    footer_link_list_str = ", ".join(available_footer_links) if available_footer_links else "check parameter_options.json"

    parser.addoption(
        "--browser",
        action="store",
        default="all",
        help=f"Browser to run tests on: {browser_list_str}, or all (default: all)"
    )
    parser.addoption(
        "--language",
        action="store",
        default=None,
        help=f"Language to test: {language_list_str}, all, or none for random (default: depends on test case)"
    )
    parser.addoption(
        "--pos",
        action="store",
        default="all",
        help=f"POS to test: {pos_list_str}, or all (default: all)"
    )
    parser.addoption(
        "--header-link",
        action="store",
        default="all",
        help=f"Header link to test: {header_link_list_str}, or all (default: all)"
    )
    parser.addoption(
        "--footer-link",
        action="store",
        default="all",
        help=f"Footer link to test: {footer_link_list_str}, or all (default: all)"
    )
    parser.addoption(
        "--env",
        action="store",
        default="all",
        help=f"Environment to test: {env_list_str}, or all (default: all)"
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
    # ==================== CASE 3 SPECIFIC OPTIONS ====================
    parser.addoption(
        "--origin",
        action="store",
        default="BOG",
        help="Origin airport IATA code for Case 3 (default: BOG - Bogotá)"
    )
    parser.addoption(
        "--destination",
        action="store",
        default="MAD",
        help="Destination airport IATA code for Case 3 (default: MAD - Madrid)"
    )
    parser.addoption(
        "--departure-days",
        action="store",
        default="4",
        type=int,
        help="Days from today for departure date in Case 3 (default: 4)"
    )
    parser.addoption(
        "--return-days",
        action="store",
        default="5",
        type=int,
        help="Days from today for return date in Case 3 (default: 5)"
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

    # Cargar todos los parámetros disponibles dinámicamente desde parameter_options.json
    all_browsers = _get_parameter_keys("browser")
    all_languages = _get_parameter_display_names("language")  # Usar display_names: "Español", "English", etc.
    all_pos = _get_parameter_display_names("pos")  # Usar display_names: "Chile", "España", etc.
    all_header_links = _get_parameter_keys("header-link")
    all_footer_links = _get_parameter_keys("footer-link")

    # Cargar todos los ambientes disponibles con sus URLs desde parameter_options.json
    config_mgr = ConfigManager()
    env_options = config_mgr.get_parameter_options("env")
    all_envs = {}
    if env_options:
        for env_key, env_data in env_options.items():
            # Excluir la opción "all" y solo cargar ambientes con base_url definida
            if env_key != "all" and "base_url" in env_data:
                all_envs[env_key] = env_data["base_url"]

    # Filtrar navegadores según opción
    if "browser" in metafunc.fixturenames:
        if browser_option == "all":
            browsers = all_browsers
        else:
            browsers = [browser_option] if browser_option in all_browsers else all_browsers
        metafunc.parametrize("browser", browsers, scope="function")

    # Filtrar idiomas según opción
    if "language" in metafunc.fixturenames:
        # Determinar si es Case 4, Case 6 o Case 7 basado en el módulo del test
        test_module = metafunc.module.__name__
        is_case4 = "test_language_change" in test_module
        is_case6_or_7 = "test_header_redirections" in test_module or "test_footer_redirections" in test_module

        if is_case4:
            # Case 4: Comportamiento original (default=all si no se especifica)
            if language_option is None or language_option == "all":
                languages = all_languages
            else:
                # Convertir el valor CLI al display_name correspondiente
                display_name = _convert_cli_value_to_display_name("language", language_option)
                languages = [display_name] if display_name in all_languages else all_languages
        elif is_case6_or_7:
            # Cases 6 y 7: None = idioma aleatorio, all = todos los idiomas
            if language_option is None:
                # Sin --language: parametrizar con [None] para idioma aleatorio
                languages = [None]
            elif language_option == "all":
                # Con --language=all: parametrizar con todos los idiomas
                languages = all_languages
            else:
                # Con --language=<idioma>: parametrizar con ese idioma específico
                display_name = _convert_cli_value_to_display_name("language", language_option)
                languages = [display_name] if display_name in all_languages else [None]
        else:
            # Otros tests: comportamiento por defecto (similar a Case 4)
            if language_option == "all" or language_option is None:
                languages = all_languages
            else:
                # Convertir el valor CLI al display_name correspondiente
                display_name = _convert_cli_value_to_display_name("language", language_option)
                languages = [display_name] if display_name in all_languages else all_languages

        metafunc.parametrize("language", languages, scope="function")

    # Filtrar POS según opción
    if "pos" in metafunc.fixturenames:
        # Determinar si es Case 5 basado en el módulo del test
        test_module = metafunc.module.__name__
        is_case5 = "test_pos_change" in test_module

        if is_case5:
            # Case 5: Solo usar Chile, España y Otros países
            # Francia y Peru requieren idioma específico primero
            available_pos = ["Chile", "España", "Otros países"]
            if pos_option == "all":
                pos_list = available_pos
            else:
                # Convertir el valor CLI al display_name correspondiente
                display_name = _convert_cli_value_to_display_name("pos", pos_option)
                pos_list = [display_name] if display_name in available_pos else available_pos
        else:
            # Otros tests: usar todos los POS
            if pos_option == "all":
                pos_list = all_pos
            else:
                # Convertir el valor CLI al display_name correspondiente
                display_name = _convert_cli_value_to_display_name("pos", pos_option)
                pos_list = [display_name] if display_name in all_pos else all_pos

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

    # Filtrar ambientes según opción y env_options del caso
    if "base_url" in metafunc.fixturenames:
        # Detectar qué caso se está ejecutando por el nombre del módulo
        test_module = metafunc.module.__name__
        case_id = None
        if "test_oneway_booking_Case1" in test_module:
            case_id = "case_1"
        elif "test_roundtrip_booking_Case2" in test_module:
            case_id = "case_2"
        elif "test_login_network_Case3" in test_module:
            case_id = "case_3"
        elif "test_language_change_Case4" in test_module:
            case_id = "case_4"
        elif "test_pos_change_Case5" in test_module:
            case_id = "case_5"
        elif "test_header_redirections_Case6" in test_module:
            case_id = "case_6"
        elif "test_footer_redirections_Case7" in test_module:
            case_id = "case_7"

        # Obtener los env_options permitidos para este caso desde case_mappings.json
        # Cargar todos los ambientes disponibles dinámicamente como default
        allowed_env_keys = _get_available_environments()
        if case_id:
            try:
                from pathlib import Path
                config_mgr = ConfigManager()
                case_info = config_mgr.get_case_info(case_id)
                if case_info and "env_options" in case_info:
                    # Filtrar "all" de env_options ya que no es un ambiente real
                    allowed_env_keys = [e for e in case_info["env_options"] if e != "all"]
            except Exception:
                # Si falla, usar todos los ambientes disponibles dinámicamente
                allowed_env_keys = _get_available_environments()

        # Filtrar según opción CLI y ambientes permitidos
        if env_option == "all":
            # Usar solo los ambientes permitidos para este caso
            envs = [all_envs[key] for key in allowed_env_keys if key in all_envs]
        else:
            # Verificar que el ambiente solicitado esté permitido
            if env_option in allowed_env_keys and env_option in all_envs:
                envs = [all_envs[env_option]]
            else:
                # Si no está permitido, usar los permitidos
                envs = [all_envs[key] for key in allowed_env_keys if key in all_envs]

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

        # Habilitar performance logging para captura de red (Case 3: CDP Network)
        # Permite acceder a eventos de red mediante driver.get_log('performance')
        chrome_options.set_capability('goog:loggingPrefs', {'performance': 'ALL'})

        # Usar Selenium Manager (integrado en Selenium 4.x)
        # No requiere webdriver-manager, descarga el driver automáticamente
        driver = webdriver.Chrome(options=chrome_options)

    elif browser == "edge":
        # Configurar Edge
        edge_options = EdgeOptions()
        for arg in common_args:
            edge_options.add_argument(arg)
        # edge_options.add_argument("--headless")  # Descomentar para modo invisible

        # Habilitar performance logging para captura de red (Case 3: CDP Network)
        # Edge es Chromium-based, soporta las mismas capacidades que Chrome
        edge_options.set_capability('ms:loggingPrefs', {'performance': 'ALL'})

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


# ==================== FIXTURE: CONFIGURACIONES JSON ====================
@pytest.fixture(scope="session")
def test_config():
    """
    Fixture de configuraciones: proporciona acceso a los JSON de configuración.

    scope="session":
    - Se crea UNA SOLA VEZ al inicio de la sesión de tests
    - TODOS los tests comparten la misma instancia
    - Los tests pueden usar esta fixture para leer datos desde:
      * testdata.json: Pasajeros, pago, facturación
      * parameter_options.json: URLs, ciudades, idiomas, POS, etc.
      * case_mappings.json: Información de cada caso

    Uso en tests:
        def test_example(test_config):
            passengers = test_config.get_passenger_data("adult")
            payment = test_config.get_payment_data()
            cities = test_config.get_parameter_options("cities")
    """
    config_manager = ConfigManager()  # Crea instancia del gestor de configuraciones
    return config_manager  # Entrega a los tests que lo soliciten


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


# ==================== HOOK: AGREGAR TIMESTAMPS A ALLURE ====================
@pytest.hookimpl(tryfirst=True)
def pytest_runtest_setup(item):
    """
    Hook de pytest: ejecuta ANTES de cada test para agregar timestamp a Allure.

    Agrega automáticamente la fecha/hora de inicio como attachment en Allure.
    """
    # Obtener timestamp actual
    start_time = datetime.now().strftime("%Y-%m-%d %H:%M:%S")

    # Adjuntar a Allure
    allure.attach(
        f"Test Started: {start_time}",
        name="⏰ Execution Timestamp",
        attachment_type=allure.attachment_type.TEXT
    )


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

    # Agregar timestamp de finalización si el test terminó
    if report.when == "call":
        end_time = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        allure.attach(
            f"Test Finished: {end_time}",
            name="⏱️ Completion Timestamp",
            attachment_type=allure.attachment_type.TEXT
        )
