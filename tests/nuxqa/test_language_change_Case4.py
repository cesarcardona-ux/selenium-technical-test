"""
test_language_change_Case4.py - Test Case 4: Verificar cambio de idioma

Este test verifica que el cambio de idioma funcione correctamente en nuxqa.
Se ejecuta para los 4 idiomas disponibles y en ambos ambientes (QA4 y QA5).
"""

# ==================== IMPORTS ====================
import pytest
import allure
from pages.nuxqa.home_page import HomePage
import logging
from datetime import datetime

# ==================== LOGGER ====================
logger = logging.getLogger(__name__)

# ==================== CONSTANTES ====================
# Diccionario con textos esperados según idioma
EXPECTED_TEXTS = {
    "Español": "Ofertas y destinos",
    "English": "Offers and destinations",
    "Français": "Offres et destinations",
    "Português": "Ofertas e destinos"
}

# ==================== TESTS ====================
@allure.feature("Language Change")
@allure.severity(allure.severity_level.NORMAL)
def test_language_change(driver, base_url, db, language, browser, screenshots_mode):
    """
    Test Case 4: Verificar cambio de idioma.

    Parametrización dinámica basada en opciones CLI:
    - language: Controlado por --language (default: all)
    - browser: Controlado por --browser (default: all)
    - base_url: Controlado por --env (default: all)
    - screenshots_mode: Controlado por --screenshots (default: on-failure)

    Total de ejecuciones:
    - Por defecto: 4 idiomas × 2 envs × 3 navegadores = 24 tests
    - Ejemplo: --browser=chrome --language=Español --env=qa4 → 1 test

    Args:
        driver: Fixture del navegador (Chrome, Edge o Firefox según parámetro)
        base_url: URL parametrizada (QA4 o QA5)
        db: Fixture de base de datos (scope=session)
        language: Idioma (viene de pytest_generate_tests)
        browser: Navegador (viene de pytest_generate_tests)
        screenshots_mode: Modo de captura de screenshots (none, on-failure, all)
    """
    # PASO 0: Configurar metadata de Allure para organización visual
    env = base_url.split('//')[1].split('.')[0].upper()  # Extrae "NUXQA4" o "NUXQA5"
    case_number = "4"  # Número del caso de prueba

    # Título descriptivo para el reporte
    allure.dynamic.title(f"Language: {language} | Browser: {browser.capitalize()} | Env: {env}")

    # Story por navegador (agrupa tests del mismo navegador)
    allure.dynamic.story(f"{browser.capitalize()} Browser")

    # Label específico para número de caso (formato estándar de Allure)
    allure.dynamic.label("case", case_number)

    # Tags para filtrado en Allure (crea gráficos organizados)
    allure.dynamic.tag(browser)           # Tag por navegador: chrome, edge, firefox
    allure.dynamic.tag(language)          # Tag por idioma: Español, English, etc.
    allure.dynamic.tag(env)               # Tag por ambiente: NUXQA4, NUXQA5
    allure.dynamic.tag("Case4")           # Tag general del caso

    # Descripción detallada
    allure.dynamic.description(
        f"Verifica que al seleccionar el idioma '{language}' en el sitio {env}, "
        f"el texto de navegación cambie correctamente. "
        f"Ejecutado en navegador {browser.capitalize()}."
    )

    # PASO 1: Log de inicio del test
    logger.info(f"========== Starting test: Language change to '{language}' on {base_url} ==========")

    # PASO 2: Crear instancia del Page Object
    home = HomePage(driver)
    logger.info("HomePage instance created")

    # PASO 3: Abrir la página
    with allure.step(f"Navigate to {env}"):
        home.open(base_url)
        logger.info(f"Navigated to {base_url}")
        # Capturar screenshot solo si modo es "all"
        if screenshots_mode == "all":
            allure.attach(driver.get_screenshot_as_png(), name="01_Page_Loaded", attachment_type=allure.attachment_type.PNG)

    # PASO 4: Seleccionar idioma (select_language abre el dropdown automáticamente)
    with allure.step(f"Select language: {language}"):
        home.select_language(language)
        logger.info(f"Language '{language}' selected")
        # Capturar screenshot solo si modo es "all"
        if screenshots_mode == "all":
            allure.attach(driver.get_screenshot_as_png(), name=f"02_Language_{language}_Selected", attachment_type=allure.attachment_type.PNG)

    # PASO 5: Obtener texto de validación
    with allure.step(f"Verify language change to {language}"):
        actual_text = home.get_offers_text()
        expected_text = EXPECTED_TEXTS[language]
        logger.info(f"Expected text: '{expected_text}' | Actual text: '{actual_text}'")

        # PASO 6: Validación con assert (requisito del PDF)
        assert expected_text in actual_text, f"Expected '{expected_text}' but got '{actual_text}'"
        logger.info("✓ Assertion passed: Language changed successfully")
        # Capturar screenshot solo si modo es "all"
        if screenshots_mode == "all":
            allure.attach(driver.get_screenshot_as_png(), name="03_Validation_Success", attachment_type=allure.attachment_type.PNG)

    # PASO 7: Guardar resultado en base de datos (requisito del PDF)
    test_name = f"Case4_{language}_{env}_{browser}"
    db.save_test_result(
        test_name=test_name,
        status="PASSED",
        execution_time=0,
        browser=browser,
        url=base_url,
        language=language,
        case_number=case_number
    )
    logger.info(f"Test result saved to database: {test_name}")

    logger.info(f"========== Test completed successfully ==========")
