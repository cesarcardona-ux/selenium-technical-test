"""
test_header_redirections_Case6.py - Test Case 6: Verificar redirecciones del Header

Este test verifica que los links del navbar redirigen correctamente a sitios externos/internos.
Se ejecuta para los 3 header links especificados y en ambos ambientes (QA4 y QA5).
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
# Diccionario con nombres descriptivos de cada header link
HEADER_LINK_NAMES = {
    "ofertas-vuelos": "Ofertas de vuelos",
    "credits": "Avianca Credits",
    "equipaje": "Equipaje"
}

# ==================== TESTS ====================
@allure.feature("Header Redirections")
@allure.severity(allure.severity_level.NORMAL)
def test_header_redirections(driver, base_url, db, header_link, browser, screenshots_mode, language):
    """
    Test Case 6: Verificar redirecciones del header (navbar).

    Parametrización dinámica basada en opciones CLI:
    - header_link: Controlado por --header-link (default: all)
    - browser: Controlado por --browser (default: all)
    - base_url: Controlado por --env (default: all)
    - screenshots_mode: Controlado por --screenshots (default: on-failure)
    - language: Controlado por --language (default: None para aleatorio)

    Total de ejecuciones:
    - Por defecto: 3 header links × 2 envs × 3 navegadores × 1 (random) = 18 tests
    - Con --language=all: 3 header links × 2 envs × 3 navegadores × 4 idiomas = 72 tests
    - Ejemplo: --browser=chrome --header-link=hoteles --env=qa4 → 1 test (random language)
    - Ejemplo: --browser=chrome --header-link=hoteles --env=qa4 --language=English → 1 test (English)

    Args:
        driver: Fixture del navegador (Chrome, Edge o Firefox según parámetro)
        base_url: URL parametrizada (QA4 o QA5)
        db: Fixture de base de datos (scope=session)
        header_link: Link del header a probar (viene de pytest_generate_tests)
        browser: Navegador (viene de pytest_generate_tests)
        screenshots_mode: Modo de captura de screenshots (none, on-failure, all)
        language: Idioma a usar (None para aleatorio, o idioma específico)
    """
    # PASO 0: Configurar metadata de Allure para organización visual
    env = base_url.split('//')[1].split('.')[0].upper()  # Extrae "NUXQA4" o "NUXQA5"
    case_number = "6"  # Número del caso de prueba
    link_name = HEADER_LINK_NAMES[header_link]

    # Título descriptivo para el reporte (el idioma se agregará después)
    # El idioma se establece dinámicamente después de la navegación
    allure.dynamic.title(f"Header Link: {link_name} | Browser: {browser.capitalize()} | Env: {env}")

    # Story por navegador (agrupa tests del mismo navegador)
    allure.dynamic.story(f"{browser.capitalize()} Browser")

    # Label específico para número de caso (formato estándar de Allure)
    allure.dynamic.label("case", case_number)

    # Tags para filtrado en Allure (crea gráficos organizados)
    allure.dynamic.tag(browser)           # Tag por navegador: chrome, edge, firefox
    allure.dynamic.tag(header_link)       # Tag por link: hoteles, credits, equipaje
    allure.dynamic.tag(env)               # Tag por ambiente: NUXQA4, NUXQA5
    allure.dynamic.tag("Case6")           # Tag general del caso

    # Descripción detallada
    allure.dynamic.description(
        f"Verifica que al hacer click en el header link '{link_name}' en el sitio {env}, "
        f"se redirija correctamente a la página correspondiente. "
        f"Ejecutado en navegador {browser.capitalize()}."
    )

    # PASO 1: Log de inicio del test
    logger.info(f"========== Starting test: Header redirection to '{link_name}' on {base_url} ==========")

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

    # PASO 4: Click en header link y submenu option (incluye cambio de idioma)
    with allure.step(f"Click on header link: {link_name}"):
        success, final_url, message, selected_language = home.click_header_link_and_submenu(header_link, language)
        logger.info(f"Redirection result: success={success}, url={final_url}, message={message}, language={selected_language}")

        # Capturar screenshot solo si modo es "all"
        if screenshots_mode == "all":
            allure.attach(driver.get_screenshot_as_png(), name=f"02_After_Click_{header_link}", attachment_type=allure.attachment_type.PNG)

    # PASO 5: Validar redirección
    with allure.step(f"Verify redirection to {link_name}"):
        # Determinar modo de idioma para el reporte
        language_mode = "Random" if language is None else ("All Languages" if language == "all" else "Specific")

        # Actualizar título con el idioma usado y modo
        allure.dynamic.title(f"Header Link: {link_name} | Browser: {browser.capitalize()} | Env: {env} | Lang: {selected_language} ({language_mode})")

        # Agregar tag del idioma seleccionado para filtrado en Allure
        if selected_language:
            allure.dynamic.tag(selected_language)

        # Agregar tag del modo de idioma
        allure.dynamic.tag(f"lang-mode-{language_mode.lower().replace(' ', '-')}")

        # Adjuntar información detallada de idioma al reporte de Allure
        allure.attach(
            final_url if final_url else "No URL captured",
            name="Final URL",
            attachment_type=allure.attachment_type.TEXT
        )
        allure.attach(
            selected_language if selected_language else "No language selected",
            name="Selected Language (Used in Test)",
            attachment_type=allure.attachment_type.TEXT
        )
        allure.attach(
            f"CLI Parameter: {language if language else 'None (random)'}\nMode: {language_mode}\nActual Language Used: {selected_language}",
            name="Language Configuration",
            attachment_type=allure.attachment_type.TEXT
        )

        # PASO 6: Validación con assert (requisito del PDF)
        assert success, f"Header redirection to '{link_name}' failed: {message}"
        assert final_url is not None, f"No URL captured after clicking '{link_name}'"
        assert selected_language is not None, f"No language selected"
        logger.info(f"✓ Assertion passed: Redirection to '{link_name}' successful with language '{selected_language}'")

        # Capturar screenshot solo si modo es "all"
        if screenshots_mode == "all":
            allure.attach(driver.get_screenshot_as_png(), name="03_Validation_Success", attachment_type=allure.attachment_type.PNG)

    # PASO 7: Limpiar pestañas extras si se abrieron
    with allure.step("Clean up extra tabs"):
        home.close_extra_tabs_and_return_to_main()
        logger.info("Extra tabs closed, returned to main tab")

    # PASO 8: Guardar resultado en base de datos (requisito del PDF)
    test_name = f"Case6_{header_link}_{env}_{browser}_{selected_language}"
    db.save_test_result(
        test_name=test_name,
        status="PASSED",
        execution_time=0,
        browser=browser,
        url=final_url,
        language=selected_language,  # Idioma usado en el test
        case_number=case_number
    )
    logger.info(f"Test result saved to database: {test_name} with language {selected_language}")

    logger.info(f"========== Test completed successfully ==========")
