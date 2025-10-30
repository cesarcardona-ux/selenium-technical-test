"""
test_language_change_Case4.py - Test Case 4: Verificar cambio de idioma

Este test verifica que el cambio de idioma funcione correctamente en nuxqa.
Se ejecuta para los 4 idiomas disponibles y en ambos ambientes (QA4 y QA5).
"""

# ==================== IMPORTS ====================
import pytest
from pages.nuxqa.home_page import HomePage
import logging
from datetime import datetime

# ==================== LOGGER ====================
logger = logging.getLogger(__name__)

# ==================== CONSTANTES ====================
# URLs de los ambientes (importadas desde conftest)
BASE_URL_QA4 = "https://nuxqa4.avtest.ink/"
BASE_URL_QA5 = "https://nuxqa5.avtest.ink/"

# Diccionario con textos esperados según idioma
EXPECTED_TEXTS = {
    "Español": "Ofertas y destinos",
    "English": "Offers and destinations",
    "Français": "Offres et destinations",
    "Português": "Ofertas e destinos"
}

# ==================== TESTS ====================
@pytest.mark.parametrize("base_url", [BASE_URL_QA4, BASE_URL_QA5])
@pytest.mark.parametrize("language", ["Español", "English", "Français", "Português"])
def test_language_change(driver, base_url, db, language):
    """
    Test Case 4: Verificar cambio de idioma.

    Este test se ejecuta 8 veces en total:
    - 4 idiomas × 2 ambientes = 8 ejecuciones

    Args:
        driver: Fixture del navegador (scope=function)
        base_url: URL parametrizada (QA4 o QA5)
        db: Fixture de base de datos (scope=session)
        language: Idioma parametrizado (Español, English, Français, Português)
    """
    # PASO 1: Log de inicio del test
    logger.info(f"========== Starting test: Language change to '{language}' on {base_url} ==========")

    # PASO 2: Crear instancia del Page Object
    home = HomePage(driver)
    logger.info("HomePage instance created")

    # PASO 3: Abrir la página
    home.open(base_url)
    logger.info(f"Navigated to {base_url}")

    # PASO 4: Click en botón de idioma
    home.click_language_button()
    logger.info("Language dropdown opened")

    # PASO 5: Seleccionar idioma
    home.select_language(language)
    logger.info(f"Language '{language}' selected")

    # PASO 6: Obtener texto de validación
    actual_text = home.get_offers_text()
    expected_text = EXPECTED_TEXTS[language]
    logger.info(f"Expected text: '{expected_text}' | Actual text: '{actual_text}'")

    # PASO 7: Validación con assert (requisito del PDF)
    assert expected_text in actual_text, f"Expected '{expected_text}' but got '{actual_text}'"
    logger.info("✓ Assertion passed: Language changed successfully")

    # PASO 8: Guardar resultado en base de datos (requisito del PDF)
    test_name = f"Case4_Language_{language}_{base_url.split('//')[1].split('.')[0]}"
    db.save_test_result(
        test_name=test_name,
        status="PASSED",
        execution_time=0,
        url=base_url
    )
    logger.info(f"Test result saved to database: {test_name}")

    logger.info(f"========== Test completed successfully ==========")
