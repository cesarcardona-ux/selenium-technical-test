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

    # Header Navigation selectors (Case 6)
    # Botones del navbar con clase específica (basado en inspección del sitio)
    NAVBAR_OFFERS = (By.XPATH, "//button[contains(@class, 'main-header_nav-primary_item_link')]//span[contains(text(), 'Ofertas y destinos')]")
    NAVBAR_YOUR_RESERVATION = (By.XPATH, "//button[contains(@class, 'main-header_nav-primary_item_link')]//span[contains(text(), 'Tu reserva')]")
    NAVBAR_INFO_AND_HELP = (By.XPATH, "//button[contains(@class, 'main-header_nav-primary_item_link')]//span[contains(text(), 'Información y ayuda')]")

    # Links de submenú (dentro del dropdown que aparece al hacer click en navbar)
    # Buscar por span con clase link_label
    SUBMENU_HOTEL_RESERVATION = (By.XPATH, "//span[@class='link_label' and contains(text(), 'Reserva de hoteles')]")
    SUBMENU_AVIANCA_CREDITS = (By.XPATH, "//span[@class='link_label' and contains(text(), 'avianca credits')]")
    SUBMENU_LUGGAGE = (By.XPATH, "//span[@class='link_label' and contains(text(), 'Equipaje')]")

    # Footer Navigation selectors (Case 7)
    # Links del footer con clase link-label (basado en inspección del sitio)
    FOOTER_VUELOS_BARATOS = (By.XPATH, "//span[@class='link-label' and contains(text(), 'Vuelos baratos')]")
    FOOTER_TRABAJA_CON_NOSOTROS = (By.XPATH, "//span[@class='link-label' and contains(text(), 'Trabaja con nosotros')]")
    FOOTER_AVIANCADIRECT = (By.XPATH, "//span[@class='link-label' and contains(text(), 'aviancadirect')]")
    FOOTER_ARTICULOS_RESTRINGIDOS = (By.XPATH, "//span[@class='link-label' and contains(text(), 'Artículos restringidos')]")

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

    # ==================== MÉTODOS HEADER NAVIGATION (Case 6) ====================

    def click_header_link_and_submenu(self, header_link_name):
        """
        Hace click en un link del navbar y luego en la opción del submenú.
        Maneja la apertura de nueva pestaña si es necesario.

        Args:
            header_link_name: Nombre del link a probar ("hoteles", "credits", "equipaje")

        Returns:
            tuple: (success: bool, new_url: str, message: str)
        """
        from selenium.webdriver.common.action_chains import ActionChains
        from selenium.webdriver.support.ui import WebDriverWait
        from selenium.webdriver.support import expected_conditions as EC

        # Mapear nombre corto a selectores y URLs esperadas
        # expected_url_parts: Lista de strings que DEBEN estar en la URL final (validación multi-parte)
        navigation_map = {
            "hoteles": {
                "navbar": self.NAVBAR_OFFERS,
                "submenu": self.SUBMENU_HOTEL_RESERVATION,
                "expected_url_parts": ["booking.com", "/dealspage"]  # Debe contener dominio + path
            },
            "credits": {
                "navbar": self.NAVBAR_YOUR_RESERVATION,
                "submenu": self.SUBMENU_AVIANCA_CREDITS,
                "expected_url_parts": ["avianca-credits"]  # URL interna, solo una parte necesaria
            },
            "equipaje": {
                "navbar": self.NAVBAR_INFO_AND_HELP,
                "submenu": self.SUBMENU_LUGGAGE,
                "expected_url_parts": ["informacion-y-ayuda", "equipaje"]  # Debe contener ambas partes del path
            }
        }

        if header_link_name not in navigation_map:
            logger.error(f"Invalid header link name: {header_link_name}")
            return False, None, f"Invalid header link: {header_link_name}"

        nav_data = navigation_map[header_link_name]

        try:
            # Guardar URL inicial
            initial_url = self.driver.current_url
            initial_window = self.driver.current_window_handle
            logger.info(f"Initial URL: {initial_url}")

            # Paso 1: Hacer CLICK en el navbar button para abrir el menú dropdown
            logger.info(f"Looking for navbar button for '{header_link_name}'")
            navbar_element = self.driver.find_element(*nav_data["navbar"])
            logger.info(f"Navbar button found, clicking it to open dropdown")

            # Click en el botón del navbar
            navbar_element.click()
            logger.info("Navbar button clicked, dropdown should open")
            time.sleep(2)  # Espera para que se abra el menú

            # Paso 2: Esperar explícitamente a que el elemento del submenú sea visible
            logger.info(f"Waiting for submenu option to be visible for '{header_link_name}'")
            wait = WebDriverWait(self.driver, 10)
            submenu_element = wait.until(
                EC.visibility_of_element_located(nav_data["submenu"])
            )
            logger.info(f"Submenu element is now visible")

            # Paso 3: Click en la opción del submenú usando JavaScript (más confiable para links con target="_blank")
            logger.info(f"Clicking submenu option for '{header_link_name}'")
            self.driver.execute_script("arguments[0].click();", submenu_element)
            logger.info(f"Submenu clicked via JavaScript")
            time.sleep(3)  # Espera a que cargue la página/nueva pestaña

            # Paso 4: Verificar si se abrió en nueva pestaña
            all_windows = self.driver.window_handles
            if len(all_windows) > 1:
                # Se abrió nueva pestaña - cambiar a ella
                logger.info("New tab detected, switching to new tab")
                new_window = [w for w in all_windows if w != initial_window][0]
                self.driver.switch_to.window(new_window)
                time.sleep(2)

            # Paso 5: Obtener URL final
            final_url = self.driver.current_url
            logger.info(f"Final URL: {final_url}")

            # Paso 6: Validar que la URL cambió
            if final_url == initial_url:
                logger.warning(f"URL did not change after clicking '{header_link_name}'")
                return False, final_url, "URL did not change"

            # Paso 7: Validar que la URL contiene TODAS las partes esperadas (validación multi-parte)
            expected_parts = nav_data["expected_url_parts"]
            for expected_part in expected_parts:
                if expected_part not in final_url:
                    logger.error(f"URL validation failed: expected '{expected_part}' in URL but got '{final_url}'")
                    return False, final_url, f"URL doesn't contain expected part: '{expected_part}'"
                else:
                    logger.info(f"✓ URL validation passed: contains '{expected_part}'")

            logger.info(f"✓ Redirection successful to: {final_url}")
            logger.info(f"✓ All URL validations passed: {expected_parts}")
            return True, final_url, "Redirection successful"

        except Exception as e:
            logger.error(f"Error during header navigation for '{header_link_name}': {str(e)}")
            return False, None, f"Error: {str(e)}"

    def close_extra_tabs_and_return_to_main(self):
        """
        Cierra todas las pestañas extras y regresa a la pestaña principal.
        Útil para limpiar después de abrir links que abren nuevas pestañas.
        """
        try:
            main_window = self.driver.window_handles[0]
            # Cerrar todas las pestañas excepto la primera
            for window in self.driver.window_handles[1:]:
                self.driver.switch_to.window(window)
                self.driver.close()
                logger.info(f"Closed extra tab: {window}")
            # Regresar a la pestaña principal
            self.driver.switch_to.window(main_window)
            logger.info("Returned to main tab")
        except Exception as e:
            logger.warning(f"Error closing extra tabs: {str(e)}")

    # ==================== MÉTODOS FOOTER NAVIGATION (Case 7) ====================

    def click_footer_link_and_validate(self, footer_link_name):
        """
        Hace click en un link del footer y valida la URL de destino.
        Maneja la apertura de nueva pestaña si es necesario.

        Args:
            footer_link_name: Nombre del link a probar ("vuelos", "trabajos", "aviancadirect", "articulos")

        Returns:
            tuple: (success: bool, new_url: str, message: str)
        """
        from selenium.webdriver.support.ui import WebDriverWait
        from selenium.webdriver.support import expected_conditions as EC

        # Mapear nombre corto a selectores y URLs esperadas
        # expected_url_parts: Lista de strings que DEBEN estar en la URL final (validación multi-parte)
        navigation_map = {
            "vuelos": {
                "selector": self.FOOTER_VUELOS_BARATOS,
                "expected_url_parts": ["ofertas-destinos", "ofertas-de-vuelos"]
            },
            "trabajos": {
                "selector": self.FOOTER_TRABAJA_CON_NOSOTROS,
                "expected_url_parts": ["jobs.avianca.com"]
            },
            "aviancadirect": {
                "selector": self.FOOTER_AVIANCADIRECT,
                "expected_url_parts": ["portales-aliados", "aviancadirect-ndc"]
            },
            "articulos": {
                "selector": self.FOOTER_ARTICULOS_RESTRINGIDOS,
                "expected_url_parts": ["ayuda.avianca.com", "/hc/"]
            }
        }

        if footer_link_name not in navigation_map:
            logger.error(f"Invalid footer link name: {footer_link_name}")
            return False, None, f"Invalid footer link: {footer_link_name}"

        nav_data = navigation_map[footer_link_name]

        try:
            # Guardar URL inicial
            initial_url = self.driver.current_url
            initial_window = self.driver.current_window_handle
            logger.info(f"Initial URL: {initial_url}")

            # Paso 1: Scroll hacia el footer para que sea visible
            logger.info(f"Scrolling to footer to make link visible")
            self.driver.execute_script("window.scrollTo(0, document.body.scrollHeight);")
            time.sleep(2)  # Espera para que el scroll complete

            # Paso 2: Esperar explícitamente a que el elemento del footer sea visible
            logger.info(f"Waiting for footer link '{footer_link_name}' to be visible")
            wait = WebDriverWait(self.driver, 10)
            footer_element = wait.until(
                EC.visibility_of_element_located(nav_data["selector"])
            )
            logger.info(f"Footer link is now visible")

            # Paso 3: Click en el link del footer usando JavaScript (más confiable)
            logger.info(f"Clicking footer link '{footer_link_name}'")
            self.driver.execute_script("arguments[0].click();", footer_element)
            logger.info(f"Footer link clicked via JavaScript")
            time.sleep(3)  # Espera a que cargue la página/nueva pestaña

            # Paso 4: Verificar si se abrió en nueva pestaña
            all_windows = self.driver.window_handles
            if len(all_windows) > 1:
                # Se abrió nueva pestaña - cambiar a ella
                logger.info("New tab detected, switching to new tab")
                new_window = [w for w in all_windows if w != initial_window][0]
                self.driver.switch_to.window(new_window)
                time.sleep(2)

            # Paso 5: Obtener URL final
            final_url = self.driver.current_url
            logger.info(f"Final URL: {final_url}")

            # Paso 6: Validar que la URL cambió
            if final_url == initial_url:
                logger.warning(f"URL did not change after clicking '{footer_link_name}'")
                return False, final_url, "URL did not change"

            # Paso 7: Validar que la URL contiene TODAS las partes esperadas (validación multi-parte)
            expected_parts = nav_data["expected_url_parts"]
            for expected_part in expected_parts:
                if expected_part not in final_url:
                    logger.error(f"URL validation failed: expected '{expected_part}' in URL but got '{final_url}'")
                    return False, final_url, f"URL doesn't contain expected part: '{expected_part}'"
                else:
                    logger.info(f"✓ URL validation passed: contains '{expected_part}'")

            logger.info(f"✓ Redirection successful to: {final_url}")
            logger.info(f"✓ All URL validations passed: {expected_parts}")
            return True, final_url, "Redirection successful"

        except Exception as e:
            logger.error(f"Error during footer navigation for '{footer_link_name}': {str(e)}")
            return False, None, f"Error: {str(e)}"
