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

    # Language selectors (Case 4)
    LANGUAGE_BUTTON = (By.XPATH, "//button[contains(@class, 'dropdown_trigger')]")
    OFFERS_TEXT = (By.XPATH, "//button[contains(@class, 'main-header_nav-primary_item_link')]//span[@class='button_label']")

    # POS (Point of Sale) selectors (Case 5)
    POS_BUTTON = (By.ID, "pointOfSaleSelectorId")  # Usar ID es más confiable que XPath
    POS_SELECTED_TEXT = (By.XPATH, "//button[@id='pointOfSaleSelectorId']//span[@class='button_label']")  # Texto del POS seleccionado
    POS_APPLY_BUTTON = (By.XPATH, "//button[contains(@class, 'points-of-sale_footer_action_button')]")  # Botón "Aplicar" por clase

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

    # ==================== MÉTODOS POS (Case 5) ====================

    def click_pos_button(self):
        """
        Hace click en el botón de selección de POS (Point of Sale).
        Abre el dropdown con las opciones de países/regiones.
        """
        logger.info("Clicking POS button")
        element = self.driver.find_element(*self.POS_BUTTON)
        element.click()
        time.sleep(1)  # Espera a que se abra el dropdown
        logger.info("POS dropdown opened")

    def select_pos(self, pos_name):
        """
        Selecciona un POS (Point of Sale) del dropdown y aplica el cambio.

        Args:
            pos_name: Nombre del POS (ej: "Chile", "España", "Otros países")
        """
        logger.info(f"Selecting POS: {pos_name}")
        # XPath dinámico: busca por texto visible en el label
        xpath = f"//span[@class='points-of-sale_list_item_label' and contains(text(), '{pos_name}')]"
        element = self.driver.find_element(By.XPATH, xpath)
        element.click()
        time.sleep(1)  # Espera a que se resalte la opción
        logger.info(f"POS '{pos_name}' clicked")

        # Click en el botón "Aplicar" para confirmar el cambio
        logger.info("Clicking 'Aplicar' button to confirm POS change")
        apply_button = self.driver.find_element(*self.POS_APPLY_BUTTON)
        apply_button.click()
        time.sleep(3)  # Espera a que se recargue la página (más tiempo porque recarga)
        logger.info(f"POS '{pos_name}' applied successfully")

    def get_pos_text(self):
        """
        Obtiene el texto del POS actualmente seleccionado para validación.

        Returns:
            str: Texto del POS seleccionado (ej: "Chile", "Colombia", "España")
        """
        logger.info("Getting POS text for validation")
        element = self.driver.find_element(*self.POS_SELECTED_TEXT)
        text = element.text.strip()  # .strip() remueve espacios en blanco
        logger.info(f"POS text retrieved: '{text}'")
        return text
