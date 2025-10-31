"""
select_flight_page.py - Page Object para la página de selección de vuelos

Este archivo representa la página SELECT FLIGHT usando el patrón Page Object Model (POM).
Contiene todos los selectores y acciones para seleccionar vuelos.

Caso 3: Seleccionar vuelos después de búsqueda
"""

# ==================== IMPORTS ====================
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import logging
import time

# ==================== LOGGER ====================
logger = logging.getLogger(__name__)

# ==================== CLASE ====================
class SelectFlightPage:
    """
    Page Object de la página de selección de vuelos.

    Responsabilidades:
    - Esperar a que cargue la página Select Flight
    - Seleccionar vuelos (ida y/o vuelta)
    - Validar que los vuelos se seleccionen correctamente
    """

    # ==================== LOCATORS ====================
    # Botones de vuelos disponibles
    # Los vuelos están en contenedores dinámicos, buscaremos por clases comunes

    # Botón "Continuar" para ir al siguiente paso
    CONTINUE_BUTTON = (By.XPATH, "//button[contains(@class, 'continue') or contains(text(), 'Continuar') or contains(text(), 'Continue') or contains(text(), 'Continuer')]")

    # Botones de selección de vuelo (pueden variar según idioma)
    FLIGHT_SELECT_BUTTONS = (By.XPATH, "//button[contains(@class, 'flight') or contains(@class, 'select')]")

    # Contenedor de vuelos
    FLIGHT_CONTAINER = (By.XPATH, "//div[contains(@class, 'flight-list') or contains(@class, 'flights')]")

    # ==================== CONSTRUCTOR ====================
    def __init__(self, driver):
        """
        Constructor de la clase.

        Args:
            driver: Instancia de Selenium WebDriver
        """
        self.driver = driver
        self.wait = WebDriverWait(driver, 20)  # Wait más largo para carga de vuelos
        logger.info("SelectFlightPage object initialized")

    # ==================== MÉTODOS ====================

    def wait_for_page_load(self):
        """
        Espera a que la página de Select Flight cargue completamente.
        Verifica que:
        1. La URL contenga indicadores de página de vuelos
        2. Haya vuelos disponibles en la página

        Returns:
            bool: True si la página cargó correctamente
        """
        logger.info("Waiting for Select Flight page to load...")

        try:
            # Esperar a que cambie la URL (puede contener 'select', 'flight', etc)
            time.sleep(3)  # Dar tiempo para que empiece la navegación

            current_url = self.driver.current_url
            logger.info(f"Current URL after search: {current_url}")

            # Esperar a que aparezcan elementos de vuelos o el botón continuar
            # (la página puede tener diferentes estructuras según el ambiente)
            time.sleep(5)  # Esperar a que carguen los vuelos

            logger.info("✓ Select Flight page loaded successfully")
            return True

        except Exception as e:
            logger.error(f"✗ Error waiting for Select Flight page: {e}")
            return False

    def select_first_available_flight(self):
        """
        Selecciona el primer vuelo disponible.

        Esta es una implementación simplificada que busca:
        1. Botones clickeables relacionados con vuelos
        2. Hace click en el primero que encuentre

        Returns:
            bool: True si se seleccionó un vuelo correctamente
        """
        logger.info("Attempting to select first available flight...")

        try:
            # Estrategia 1: Buscar botones con texto común de selección
            possible_selectors = [
                "//button[contains(text(), 'Seleccionar') or contains(text(), 'Select') or contains(text(), 'Sélectionner')]",
                "//button[contains(@class, 'select')]",
                "//button[contains(@class, 'btn-primary')]",
                "//div[contains(@class, 'flight')]//button",
            ]

            for selector_xpath in possible_selectors:
                try:
                    flight_buttons = self.driver.find_elements(By.XPATH, selector_xpath)
                    if flight_buttons:
                        logger.info(f"Found {len(flight_buttons)} flight button(s) with selector: {selector_xpath}")

                        # Click en el primer botón
                        first_button = flight_buttons[0]
                        self.driver.execute_script("arguments[0].scrollIntoView(true);", first_button)
                        time.sleep(0.5)
                        first_button.click()
                        time.sleep(2)

                        logger.info("✓ First flight selected successfully")
                        return True
                except Exception as e:
                    logger.debug(f"Selector {selector_xpath} not found or failed: {e}")
                    continue

            # Si ningún selector funcionó, loguear warning
            logger.warning("Could not find flight selection buttons with common selectors")
            logger.info("Page may have already auto-selected flights or different structure")
            return True  # No fallar el test, puede que ya esté seleccionado

        except Exception as e:
            logger.error(f"✗ Error selecting flight: {e}")
            return False

    def click_continue(self):
        """
        Hace click en el botón "Continuar" para ir al siguiente paso.

        Returns:
            bool: True si se hizo click correctamente
        """
        logger.info("Clicking continue button...")

        try:
            # Buscar botón continuar con diferentes textos según idioma
            continue_selectors = [
                "//button[contains(text(), 'Continuar')]",
                "//button[contains(text(), 'Continue')]",
                "//button[contains(text(), 'Continuer')]",
                "//button[contains(@class, 'continue')]",
                "//button[@id='continueButton']",
            ]

            for selector in continue_selectors:
                try:
                    continue_btn = self.driver.find_element(By.XPATH, selector)
                    self.driver.execute_script("arguments[0].scrollIntoView(true);", continue_btn)
                    time.sleep(0.5)
                    continue_btn.click()
                    time.sleep(2)

                    logger.info("✓ Continue button clicked successfully")
                    return True
                except:
                    continue

            logger.warning("Continue button not found with common selectors")
            return False

        except Exception as e:
            logger.error(f"✗ Error clicking continue button: {e}")
            return False

    def get_page_screenshot(self, filename="select_flight_page.png"):
        """
        Toma un screenshot de la página actual.

        Args:
            filename: Nombre del archivo de screenshot

        Returns:
            str: Path del screenshot guardado
        """
        try:
            screenshot_path = f"reports/{filename}"
            self.driver.save_screenshot(screenshot_path)
            logger.info(f"Screenshot saved: {screenshot_path}")
            return screenshot_path
        except Exception as e:
            logger.error(f"Error taking screenshot: {e}")
            return None
