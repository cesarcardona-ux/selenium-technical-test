"""
home_page.py - Page Object para la página principal de nuxqa

Este archivo representa la página HOME usando el patrón Page Object Model (POM).
Contiene todos los selectores (locators) y acciones que se pueden hacer en esta página.
"""

# ==================== IMPORTS ====================
from selenium.webdriver.common.by import By
import logging
import time

# ==================== LOGGER ====================
# Requisito técnico del PDF: logs detallados
logger = logging.getLogger(__name__)  # __name__ = 'pages.nuxqa.home_page'

# ==================== CLASE ====================
class HomePage:
    """
    Page Object de la página principal de nuxqa.

    Responsabilidades:
    - Almacenar locators (selectores XPath)
    - Proveer métodos para interactuar con elementos
    - Registrar logs de cada acción (requisito del PDF)
    """

    # ==================== LOCATORS (Selectores XPath) ====================
    # Se definen como constantes en MAYÚSCULAS (convención Python)
    # Formato: tupla (By.XPATH, "xpath_string")

    LANGUAGE_BUTTON = (By.XPATH, "//button[contains(@class, 'dropdown_trigger')]")
    OFFERS_TEXT = (By.XPATH, "//button[contains(@class, 'main-header_nav-primary_item_link')]//span[@class='button_label']")

    # ==================== CONSTRUCTOR ====================
    def __init__(self, driver):
        """
        Constructor de la clase.

        Args:
            driver: Instancia de Selenium WebDriver (recibida desde el test)
        """
        self.driver = driver
        logger.info("HomePage object initialized")

    # ==================== MÉTODOS ====================

    def open(self, url):
        """
        Abre la página en la URL especificada.

        Args:
            url: URL completa a abrir (ej: https://nuxqa4.avtest.ink/)
        """
        logger.info(f"Opening URL: {url}")
        self.driver.get(url)
        time.sleep(2)  # Espera 2 segundos para que cargue completamente
        logger.info("Page loaded successfully")

    def click_language_button(self):
        """
        Hace click en el botón de selección de idioma.
        Abre el dropdown con las opciones de idioma.
        """
        logger.info("Clicking language button")
        element = self.driver.find_element(*self.LANGUAGE_BUTTON)
        element.click()
        time.sleep(1)  # Espera a que se abra el dropdown
        logger.info("Language dropdown opened")

    def select_language(self, language_name):
        """
        Selecciona un idioma del dropdown.

        Args:
            language_name: Nombre del idioma (ej: "English", "Español", "Français", "Português")
        """
        logger.info(f"Selecting language: {language_name}")
        # XPath dinámico: busca por texto visible
        xpath = f"//span[contains(text(), '{language_name}')]"
        element = self.driver.find_element(By.XPATH, xpath)
        element.click()
        time.sleep(2)  # Espera a que se recargue la página
        logger.info(f"Language '{language_name}' selected successfully")

    def get_offers_text(self):
        """
        Obtiene el texto del elemento "Ofertas y destinos" para validación.

        Returns:
            str: Texto del elemento (ej: "Ofertas y destinos", "Offers and destinations")
        """
        logger.info("Getting offers text for validation")
        element = self.driver.find_element(*self.OFFERS_TEXT)
        text = element.text
        logger.info(f"Offers text retrieved: '{text}'")
        return text
