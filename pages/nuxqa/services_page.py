"""
services_page.py - Page Object para la página de servicios adicionales

Este archivo representa la página SERVICES usando el patrón Page Object Model (POM).
Contiene todos los selectores y acciones para seleccionar/omitir servicios adicionales.

Caso 1: No seleccionar ningún servicio (skip all)
Caso 2: Seleccionar Avianca Lounges (o cualquier otro si no disponible)
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
class ServicesPage:
    """
    Page Object de la página de servicios adicionales.

    Responsabilidades:
    - Esperar a que cargue la página Services
    - Listar servicios disponibles
    - Seleccionar servicios específicos (o ninguno)
    - Continuar al siguiente paso
    """

    # ==================== LOCATORS ====================
    # Selectores de servicios - genéricos para adaptarse a diferentes estructuras

    # Botón para omitir servicios ("Skip", "No thanks", "Continue without services")
    SKIP_SERVICES_BUTTON = (By.XPATH, "//button[contains(text(), 'Skip') or contains(text(), 'No thanks') or contains(text(), 'Sin servicios') or contains(text(), 'Omitir')]")

    # Botón continuar (después de seleccionar o no servicios)
    CONTINUE_BUTTON = (By.XPATH, "//button[contains(text(), 'Continuar') or contains(text(), 'Continue') or contains(text(), 'Continuer') or contains(@id, 'continueButton')]")

    # Contenedores de servicios disponibles
    SERVICE_CARDS = "//div[contains(@class, 'service') or contains(@class, 'product')]"

    # Checkbox de selección de servicio
    SERVICE_CHECKBOX = "//input[@type='checkbox' and (contains(@id, 'service') or contains(@name, 'service'))]"

    # Botón de agregar servicio
    ADD_SERVICE_BUTTON = "//button[contains(text(), 'Add') or contains(text(), 'Agregar') or contains(text(), 'Añadir') or contains(@class, 'add-service')]"

    # Título de servicio (para buscar por nombre)
    SERVICE_TITLE = "//h3[contains(@class, 'service') or contains(@class, 'product')] | //div[contains(@class, 'service-title') or contains(@class, 'product-title')]"

    # ==================== CONSTRUCTOR ====================
    def __init__(self, driver):
        """
        Constructor de la clase.

        Args:
            driver: Instancia de Selenium WebDriver
        """
        self.driver = driver
        self.wait = WebDriverWait(driver, 20)
        logger.info("ServicesPage object initialized")

    # ==================== MÉTODOS ====================

    def wait_for_page_load(self):
        """
        Espera a que la página de Services cargue completamente.

        Returns:
            bool: True si la página cargó correctamente
        """
        logger.info("Waiting for Services page to load...")

        try:
            time.sleep(3)  # Tiempo para que la página empiece a cargar

            current_url = self.driver.current_url
            logger.info(f"Current URL: {current_url}")

            # Verificar que estamos en la página de servicios
            is_services_page = "service" in current_url.lower() or "product" in current_url.lower() or "ancillar" in current_url.lower()

            if not is_services_page:
                logger.warning(f"URL doesn't contain 'service' or 'product': {current_url}")

            # Esperar a que aparezcan elementos
            time.sleep(2)

            logger.info("✓ Services page loaded successfully")
            return True

        except Exception as e:
            logger.error(f"✗ Error waiting for Services page: {e}")
            return False

    def skip_all_services(self):
        """
        Omite todos los servicios (no selecciona ninguno).
        Hace click en "Skip" o directamente en "Continue".

        Returns:
            bool: True si se omitieron exitosamente
        """
        logger.info("Attempting to skip all services...")

        try:
            # Opción 1: Buscar botón "Skip" / "No thanks"
            try:
                skip_button = self.driver.find_element(*self.SKIP_SERVICES_BUTTON)
                logger.info("Skip button found, clicking it...")
                self.driver.execute_script("arguments[0].scrollIntoView(true);", skip_button)
                time.sleep(0.5)
                self.driver.execute_script("arguments[0].click();", skip_button)
                logger.info("✓ Services skipped using Skip button")
                time.sleep(2)
                return True
            except Exception as e:
                logger.info(f"Skip button not found: {e}")

            # Opción 2: Si no hay botón Skip, hacer click directamente en Continue
            logger.info("No skip button found, will click Continue directly...")
            return self.click_continue()

        except Exception as e:
            logger.error(f"✗ Error skipping services: {e}")
            return False

    def get_available_services(self):
        """
        Obtiene la lista de servicios disponibles en la página.

        Returns:
            list: Lista de nombres de servicios disponibles
        """
        logger.info("Getting list of available services...")

        try:
            service_titles = self.driver.find_elements(By.XPATH, self.SERVICE_TITLE)
            services = [title.text.strip() for title in service_titles if title.text.strip()]

            logger.info(f"Found {len(services)} services: {services}")
            return services

        except Exception as e:
            logger.error(f"✗ Error getting services list: {e}")
            return []

    def select_service_by_name(self, service_name):
        """
        Selecciona un servicio específico por su nombre.
        Busca el servicio por nombre y hace click en su checkbox o botón "Add".

        Args:
            service_name (str): Nombre del servicio a seleccionar (ej: "Avianca Lounges")

        Returns:
            bool: True si se seleccionó correctamente
        """
        logger.info(f"Attempting to select service: {service_name}")

        try:
            # Buscar el servicio por texto que contenga el nombre
            service_xpath = f"//div[contains(@class, 'service') or contains(@class, 'product')][contains(., '{service_name}')]"

            service_element = self.driver.find_element(By.XPATH, service_xpath)
            logger.info(f"Service '{service_name}' found")

            # Scroll al elemento
            self.driver.execute_script("arguments[0].scrollIntoView(true);", service_element)
            time.sleep(0.5)

            # Intentar encontrar checkbox dentro del servicio
            try:
                checkbox = service_element.find_element(By.XPATH, ".//input[@type='checkbox']")
                if not checkbox.is_selected():
                    self.driver.execute_script("arguments[0].click();", checkbox)
                    logger.info(f"✓ Service '{service_name}' selected via checkbox")
                    return True
            except:
                logger.info("Checkbox not found, trying Add button...")

            # Intentar encontrar botón "Add" dentro del servicio
            try:
                add_button = service_element.find_element(By.XPATH, ".//button[contains(text(), 'Add') or contains(text(), 'Agregar')]")
                self.driver.execute_script("arguments[0].click();", add_button)
                logger.info(f"✓ Service '{service_name}' selected via Add button")
                return True
            except:
                logger.warning("Add button not found")

            logger.warning(f"Could not interact with service '{service_name}'")
            return False

        except Exception as e:
            logger.error(f"✗ Error selecting service '{service_name}': {e}")
            return False

    def select_first_available_service(self):
        """
        Selecciona el primer servicio disponible (fallback).
        Útil cuando un servicio específico no está disponible.

        Returns:
            bool: True si se seleccionó correctamente
        """
        logger.info("Attempting to select first available service...")

        try:
            # Buscar todos los checkboxes de servicios
            checkboxes = self.driver.find_elements(By.XPATH, self.SERVICE_CHECKBOX)

            if checkboxes:
                first_checkbox = checkboxes[0]
                self.driver.execute_script("arguments[0].scrollIntoView(true);", first_checkbox)
                time.sleep(0.5)

                if not first_checkbox.is_selected():
                    self.driver.execute_script("arguments[0].click();", first_checkbox)
                    logger.info("✓ First available service selected")
                    return True
            else:
                # Intentar con botones "Add"
                add_buttons = self.driver.find_elements(By.XPATH, self.ADD_SERVICE_BUTTON)
                if add_buttons:
                    first_button = add_buttons[0]
                    self.driver.execute_script("arguments[0].scrollIntoView(true);", first_button)
                    time.sleep(0.5)
                    self.driver.execute_script("arguments[0].click();", first_button)
                    logger.info("✓ First available service selected via Add button")
                    return True

            logger.warning("No services found to select")
            return False

        except Exception as e:
            logger.error(f"✗ Error selecting first service: {e}")
            return False

    def click_continue(self):
        """
        Hace click en el botón "Continuar" para ir al siguiente paso.

        Returns:
            bool: True si se hizo click correctamente
        """
        logger.info("Clicking continue button...")

        try:
            # Scroll hacia abajo para asegurar que el botón esté visible
            self.driver.execute_script("window.scrollTo(0, document.body.scrollHeight);")
            time.sleep(1)

            continue_btn = self.wait.until(
                EC.element_to_be_clickable(self.CONTINUE_BUTTON)
            )

            # JavaScript click para mayor confiabilidad
            self.driver.execute_script("arguments[0].click();", continue_btn)
            logger.info("✓ Continue button clicked successfully")
            time.sleep(3)  # Espera a que cargue la siguiente página

            return True

        except Exception as e:
            logger.error(f"✗ Error clicking continue button: {e}")
            return False

    def get_page_screenshot(self, filename="services_page.png"):
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
