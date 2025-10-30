"""
test_pos_change_Case5.py - Test Case 5: Verificar cambio de POS

Este test verifica que el cambio de POS (Point of Sale) funcione correctamente en nuxqa.
Se ejecuta para los 3 POS especificados y en ambos ambientes (QA4 y QA5).
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
# Diccionario con textos esperados según POS
# El texto que debe aparecer en el botón de POS después de seleccionar
EXPECTED_POS_TEXTS = {
    "Chile": "Chile",
    "España": "España",
    "Otros países": "Otros países"
}

# ==================== TESTS ====================
@allure.feature("POS Change")
@allure.severity(allure.severity_level.NORMAL)
def test_pos_change(driver, base_url, db, pos, browser, screenshots_mode):
    """
    Test Case 5: Verificar cambio de POS (Point of Sale).

    Parametrización dinámica basada en opciones CLI:
    - pos: Controlado por --pos (default: all)
    - browser: Controlado por --browser (default: all)
    - base_url: Controlado por --env (default: all)
    - screenshots_mode: Controlado por --screenshots (default: on-failure)

    Total de ejecuciones:
    - Por defecto: 3 POS × 2 envs × 3 navegadores = 18 tests
    - Ejemplo: --browser=chrome --pos=Chile --env=qa4 → 1 test

    Args:
        driver: Fixture del navegador (Chrome, Edge o Firefox según parámetro)
        base_url: URL parametrizada (QA4 o QA5)
        db: Fixture de base de datos (scope=session)
        pos: POS a probar (viene de pytest_generate_tests)
        browser: Navegador (viene de pytest_generate_tests)
        screenshots_mode: Modo de captura de screenshots (none, on-failure, all)
    """
    # PASO 0: Configurar metadata de Allure para organización visual
    env = base_url.split('//')[1].split('.')[0].upper()  # Extrae "NUXQA4" o "NUXQA5"
    case_number = "5"  # Número del caso de prueba

    # Título descriptivo para el reporte
    allure.dynamic.title(f"POS: {pos} | Browser: {browser.capitalize()} | Env: {env}")

    # Story por navegador (agrupa tests del mismo navegador)
    allure.dynamic.story(f"{browser.capitalize()} Browser")

    # Label específico para número de caso (formato estándar de Allure)
    allure.dynamic.label("case", case_number)

    # Tags para filtrado en Allure (crea gráficos organizados)
    allure.dynamic.tag(browser)           # Tag por navegador: chrome, edge, firefox
    allure.dynamic.tag(pos)               # Tag por POS: Chile, España, Otros países
    allure.dynamic.tag(env)               # Tag por ambiente: NUXQA4, NUXQA5
    allure.dynamic.tag("Case5")           # Tag general del caso

    # Descripción detallada
    allure.dynamic.description(
        f"Verifica que al seleccionar el POS '{pos}' en el sitio {env}, "
        f"el cambio se refleje correctamente en el selector. "
        f"Ejecutado en navegador {browser.capitalize()}."
    )

    # PASO 1: Log de inicio del test
    logger.info(f"========== Starting test: POS change to '{pos}' on {base_url} ==========")

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

    # PASO 4: Click en botón de POS
    with allure.step("Open POS dropdown"):
        home.click_pos_button()
        logger.info("POS dropdown opened")
        # Capturar screenshot solo si modo es "all"
        if screenshots_mode == "all":
            allure.attach(driver.get_screenshot_as_png(), name="02_POS_Dropdown_Opened", attachment_type=allure.attachment_type.PNG)

    # PASO 5: Seleccionar POS
    with allure.step(f"Select POS: {pos}"):
        home.select_pos(pos)
        logger.info(f"POS '{pos}' selected")
        # Capturar screenshot solo si modo es "all"
        if screenshots_mode == "all":
            allure.attach(driver.get_screenshot_as_png(), name=f"03_POS_{pos}_Selected", attachment_type=allure.attachment_type.PNG)

    # PASO 6: Obtener texto de validación
    with allure.step(f"Verify POS change to {pos}"):
        actual_text = home.get_pos_text()
        expected_text = EXPECTED_POS_TEXTS[pos]
        logger.info(f"Expected text: '{expected_text}' | Actual text: '{actual_text}'")

        # Adjuntar información detallada al reporte de Allure
        allure.attach(
            expected_text,
            name="Expected POS Text",
            attachment_type=allure.attachment_type.TEXT
        )
        allure.attach(
            actual_text,
            name="Actual POS Text (Retrieved from Page)",
            attachment_type=allure.attachment_type.TEXT
        )
        allure.attach(
            f"POS: {pos}\nExpected: '{expected_text}'\nActual: '{actual_text}'\nValidation: {'PASSED' if expected_text in actual_text else 'FAILED'}",
            name="Validation Details",
            attachment_type=allure.attachment_type.TEXT
        )

        # PASO 7: Validación con assert (requisito del PDF)
        assert expected_text in actual_text, f"Expected '{expected_text}' but got '{actual_text}'"
        logger.info("✓ Assertion passed: POS changed successfully")
        # Capturar screenshot solo si modo es "all"
        if screenshots_mode == "all":
            allure.attach(driver.get_screenshot_as_png(), name="04_Validation_Success", attachment_type=allure.attachment_type.PNG)

    # PASO 8: Guardar resultado en base de datos (requisito del PDF)
    test_name = f"Case5_{pos}_{env}_{browser}"
    db.save_test_result(
        test_name=test_name,
        status="PASSED",
        execution_time=0,
        browser=browser,
        url=base_url,
        language=None,  # No aplica para este caso
        case_number=case_number
    )
    logger.info(f"Test result saved to database: {test_name}")

    logger.info(f"========== Test completed successfully ==========")
