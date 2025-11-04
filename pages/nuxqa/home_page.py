"""
home_page.py - Page Object para la página principal de nuxqa

Este archivo representa la página HOME usando el patrón Page Object Model (POM).
Contiene todos los selectores (locators) y acciones que se pueden hacer en esta página.
"""

# ==================== IMPORTS ====================
from selenium.webdriver.common.by import By
import logging
import time
import random

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
    # Botones del navbar (independientes del idioma - basados en posición)
    NAVBAR_OFFERS = (By.XPATH, "(//button[contains(@class, 'main-header_nav-primary_item_link')])[1]")
    NAVBAR_YOUR_RESERVATION = (By.XPATH, "(//button[contains(@class, 'main-header_nav-primary_item_link')])[2]")
    NAVBAR_INFO_AND_HELP = (By.XPATH, "(//button[contains(@class, 'main-header_nav-primary_item_link')])[3]")

    # Links de submenú (independientes del idioma - buscar por href parcial que no cambia)
    # Cada submenú tiene URLs con patrones únicos, buscar el elemento <a> directamente
    SUBMENU_FLIGHT_OFFERS = (By.XPATH, "//a[contains(@href, 'ofertas-de') or contains(@href, 'offres-de') or contains(@href, 'flight-offers') or contains(@href, 'voos-promocionais')]")
    SUBMENU_AVIANCA_CREDITS = (By.XPATH, "//a[contains(@href, 'credit')]")
    SUBMENU_CHANGEMENTS_REMBOURSEMENTS = (By.XPATH, "//a[contains(@href, 'changements-et-remboursements')]")  # Caso especial para Français
    SUBMENU_LUGGAGE = (By.XPATH, "//a[contains(@href, 'equipaje') or contains(@href, 'baggage') or contains(@href, 'bagages') or contains(@href, 'bagagem')]")

    # Footer Navigation selectors (Case 7)
    # Links del footer (independientes del idioma - usar la primera opción visible por tipo)
    # Como los slugs cambian con el idioma, buscamos por palabras clave que permanecen
    FOOTER_VUELOS_BARATOS = (By.XPATH, "//footer//a[contains(@href, 'ofertas-') or contains(@href, 'offres-') or contains(@href, 'offers-')]//span[@class='link-label']")
    FOOTER_NOTICIAS_CORPORATIVAS = (By.XPATH, "//footer//a[contains(@href, 'noticias') or contains(@href, 'nouvelles') or contains(@href, 'news') or contains(@href, 'noticias')]//span[@class='link-label']")
    FOOTER_AVIANCADIRECT = (By.XPATH, "//footer//a[contains(@href, 'aviancadirect')]//span[@class='link-label']")
    FOOTER_CONTACTANOS = (By.XPATH, "//footer//a[contains(@href, 'contact') or contains(@href, 'contato')]//span[@class='link-label']")

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
        time.sleep(1)  # OPTIMIZADO: 2s → 1s (ahorro: 1s)
        logger.info("Page loaded successfully")

    def click_language_button(self):
        """
        Hace click en el botón de selección de idioma.
        Abre el dropdown con las opciones de idioma.
        """
        logger.info("Clicking language button")
        element = self.driver.find_element(*self.LANGUAGE_BUTTON)
        element.click()
        time.sleep(0.5)  # OPTIMIZADO: 1s → 0.5s (ahorro: 0.5s)
        logger.info("Language dropdown opened")

    def select_language(self, language_name):
        """
        Selecciona un idioma del dropdown.
        Primero abre el dropdown y luego selecciona el idioma.

        Args:
            language_name: Nombre del idioma (ej: "English", "Español", "Français", "Português")
        """
        logger.info(f"Selecting language: {language_name}")
        # Primero abrir el dropdown de idiomas
        self.click_language_button()
        # XPath dinámico: busca por texto visible
        xpath = f"//span[contains(text(), '{language_name}')]"
        element = self.driver.find_element(By.XPATH, xpath)
        element.click()
        time.sleep(1)  # OPTIMIZADO: 2s → 1s (ahorro: 1s)
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
        time.sleep(0.5)  # OPTIMIZADO: 1s → 0.5s (ahorro: 0.5s)
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
        time.sleep(0.5)  # OPTIMIZADO: 1s → 0.5s (ahorro: 0.5s)
        logger.info(f"POS '{pos_name}' clicked")

        # Click en el botón "Aplicar" para confirmar el cambio
        logger.info("Clicking 'Aplicar' button to confirm POS change")
        apply_button = self.driver.find_element(*self.POS_APPLY_BUTTON)
        apply_button.click()
        time.sleep(2)  # OPTIMIZADO: 3s → 2s (ahorro: 1s)
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

    def click_header_link_and_submenu(self, header_link_name, language=None):
        """
        Hace click en un link del navbar y luego en la opción del submenú.
        Maneja la apertura de nueva pestaña si es necesario.
        Incluye selección de idioma y validación del idioma en la URL.

        Args:
            header_link_name: Nombre del link a probar ("ofertas-vuelos", "credits", "equipaje")
            language: Idioma a seleccionar (Español, English, Français, Português) o None para aleatorio

        Returns:
            tuple: (success: bool, new_url: str, message: str, selected_language: str)
        """
        from selenium.webdriver.common.action_chains import ActionChains
        from selenium.webdriver.support.ui import WebDriverWait
        from selenium.webdriver.support import expected_conditions as EC

        # Mapeo de idiomas a códigos de lenguaje en URL
        language_codes = {
            "Español": "es",
            "English": "en",
            "Français": "fr",
            "Português": "pt"
        }

        # Mapear nombre corto a selectores y URLs esperadas
        # expected_url_parts: Lista de strings que DEBEN estar en la URL final (validación multi-parte)
        navigation_map = {
            "ofertas-vuelos": {
                "navbar": self.NAVBAR_OFFERS,
                "submenu": self.SUBMENU_FLIGHT_OFFERS,
                "expected_url_parts": []  # El slug cambia con idioma, solo validamos que navegó
            },
            "credits": {
                "navbar": self.NAVBAR_YOUR_RESERVATION,
                "submenu": self.SUBMENU_AVIANCA_CREDITS,
                "expected_url_parts": ["credits"]  # "credits" no cambia con el idioma
            },
            "equipaje": {
                "navbar": self.NAVBAR_INFO_AND_HELP,
                "submenu": self.SUBMENU_LUGGAGE,
                "expected_url_parts": []  # El slug "equipaje" cambia con idioma
            }
        }

        if header_link_name not in navigation_map:
            logger.error(f"Invalid header link name: {header_link_name}")
            return False, None, f"Invalid header link: {header_link_name}", None

        nav_data = navigation_map[header_link_name]

        try:
            # PASO NUEVO: Seleccionar idioma (aleatorio o específico)
            if language is None:
                # Sin idioma especificado: selección aleatoria
                available_languages = list(language_codes.keys())
                selected_language = random.choice(available_languages)
                logger.info(f"Randomly selected language: {selected_language}")
            else:
                # Idioma específico proporcionado
                selected_language = language
                logger.info(f"Using specified language: {selected_language}")

            expected_lang_code = language_codes[selected_language]
            logger.info(f"Language code: {expected_lang_code}")

            # PASO NUEVO: Cambiar idioma antes de navegar
            logger.info(f"Changing language to: {selected_language}")
            self.select_language(selected_language)
            time.sleep(2)  # Esperar a que se aplique el cambio de idioma

            # CASO ESPECIAL: Para Français, el link "Avianca Credits" no existe
            # En su lugar, debemos usar "Changements et remboursements"
            if selected_language == "Français" and header_link_name == "credits":
                logger.info("Special case detected: Français language with credits link")
                logger.info("Using 'Changements et remboursements' link instead of 'Avianca Credits'")
                nav_data = {
                    "navbar": self.NAVBAR_YOUR_RESERVATION,
                    "submenu": self.SUBMENU_CHANGEMENTS_REMBOURSEMENTS,
                    "expected_url_parts": ["changements-et-remboursements"]  # URL en francés
                }

            # Guardar URL inicial
            initial_url = self.driver.current_url
            initial_window = self.driver.current_window_handle
            logger.info(f"Initial URL after language change: {initial_url}")

            # Paso 1: Hacer CLICK en el navbar button para abrir el menú dropdown
            logger.info(f"Looking for navbar button for '{header_link_name}'")
            navbar_element = self.driver.find_element(*nav_data["navbar"])
            logger.info(f"Navbar button found, clicking it to open dropdown")

            # Click en el botón del navbar
            navbar_element.click()
            logger.info("Navbar button clicked, dropdown should open")
            time.sleep(3)  # Espera para que se abra el menú (aumentado a 3 segundos)

            # Paso 2: Esperar explícitamente a que el elemento del submenú sea visible
            logger.info(f"Waiting for submenu option to be visible for '{header_link_name}'")
            wait = WebDriverWait(self.driver, 15)
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
                return False, final_url, "URL did not change", selected_language

            # Paso 7: Validar que la URL contiene TODAS las partes esperadas (validación multi-parte)
            expected_parts = nav_data["expected_url_parts"]
            for expected_part in expected_parts:
                if expected_part not in final_url:
                    logger.error(f"URL validation failed: expected '{expected_part}' in URL but got '{final_url}'")
                    return False, final_url, f"URL doesn't contain expected part: '{expected_part}'", selected_language
                else:
                    logger.info(f"✓ URL validation passed: contains '{expected_part}'")

            # PASO NUEVO: Validar que el idioma está en la URL
            if f"/{expected_lang_code}/" in final_url or final_url.endswith(f"/{expected_lang_code}"):
                logger.info(f"✓ Language validation passed: URL contains '/{expected_lang_code}/'")
            else:
                logger.error(f"Language validation failed: expected '/{expected_lang_code}/' in URL but got '{final_url}'")
                return False, final_url, f"URL doesn't contain expected language code: '/{expected_lang_code}/'", selected_language

            logger.info(f"✓ Redirection successful to: {final_url}")
            logger.info(f"✓ All URL validations passed: {expected_parts}")
            logger.info(f"✓ Language validation passed: {selected_language} ({expected_lang_code})")
            return True, final_url, "Redirection successful", selected_language

        except Exception as e:
            logger.error(f"Error during header navigation for '{header_link_name}': {str(e)}")
            return False, None, f"Error: {str(e)}", None

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

    def click_footer_link_and_validate(self, footer_link_name, language=None):
        """
        Hace click en un link del footer y valida la URL de destino.
        Maneja la apertura de nueva pestaña si es necesario.
        Incluye selección de idioma y validación del idioma en la URL.

        Args:
            footer_link_name: Nombre del link a probar ("vuelos", "noticias", "aviancadirect", "contactanos")
            language: Idioma a seleccionar (Español, English, Français, Português) o None para aleatorio

        Returns:
            tuple: (success: bool, new_url: str, message: str, selected_language: str)
        """
        from selenium.webdriver.support.ui import WebDriverWait
        from selenium.webdriver.support import expected_conditions as EC

        # Mapeo de idiomas a códigos de lenguaje en URL
        language_codes = {
            "Español": "es",
            "English": "en",
            "Français": "fr",
            "Português": "pt"
        }

        # Mapear nombre corto a selectores y URLs esperadas
        # expected_url_parts: Lista de strings que DEBEN estar en la URL final (validación multi-parte)
        navigation_map = {
            "vuelos": {
                "selector": self.FOOTER_VUELOS_BARATOS,
                "expected_url_parts": []  # El slug cambia con idioma, solo validamos que navegó
            },
            "noticias": {
                "selector": self.FOOTER_NOTICIAS_CORPORATIVAS,
                "expected_url_parts": []  # El slug cambia con idioma
            },
            "aviancadirect": {
                "selector": self.FOOTER_AVIANCADIRECT,
                "expected_url_parts": ["aviancadirect"]  # Único que no cambia
            },
            "contactanos": {
                "selector": self.FOOTER_CONTACTANOS,
                "expected_url_parts": []  # El slug cambia con idioma
            }
        }

        if footer_link_name not in navigation_map:
            logger.error(f"Invalid footer link name: {footer_link_name}")
            return False, None, f"Invalid footer link: {footer_link_name}", None

        nav_data = navigation_map[footer_link_name]

        try:
            # PASO NUEVO: Seleccionar idioma (aleatorio o específico)
            if language is None:
                # Sin idioma especificado: selección aleatoria
                available_languages = list(language_codes.keys())
                selected_language = random.choice(available_languages)
                logger.info(f"Randomly selected language: {selected_language}")
            else:
                # Idioma específico proporcionado
                selected_language = language
                logger.info(f"Using specified language: {selected_language}")

            expected_lang_code = language_codes[selected_language]
            logger.info(f"Language code: {expected_lang_code}")

            # PASO NUEVO: Cambiar idioma antes de navegar
            logger.info(f"Changing language to: {selected_language}")
            self.select_language(selected_language)
            time.sleep(2)  # Esperar a que se aplique el cambio de idioma

            # Guardar URL inicial
            initial_url = self.driver.current_url
            initial_window = self.driver.current_window_handle
            logger.info(f"Initial URL after language change: {initial_url}")

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
                return False, final_url, "URL did not change", selected_language

            # Paso 7: Validar que la URL contiene TODAS las partes esperadas (validación multi-parte)
            expected_parts = nav_data["expected_url_parts"]
            for expected_part in expected_parts:
                if expected_part not in final_url:
                    logger.error(f"URL validation failed: expected '{expected_part}' in URL but got '{final_url}'")
                    return False, final_url, f"URL doesn't contain expected part: '{expected_part}'", selected_language
                else:
                    logger.info(f"✓ URL validation passed: contains '{expected_part}'")

            # PASO NUEVO: Validar que el idioma está en la URL
            if f"/{expected_lang_code}/" in final_url or final_url.endswith(f"/{expected_lang_code}"):
                logger.info(f"✓ Language validation passed: URL contains '/{expected_lang_code}/'")
            else:
                logger.error(f"Language validation failed: expected '/{expected_lang_code}/' in URL but got '{final_url}'")
                return False, final_url, f"URL doesn't contain expected language code: '/{expected_lang_code}/'", selected_language

            logger.info(f"✓ Redirection successful to: {final_url}")
            logger.info(f"✓ All URL validations passed: {expected_parts}")
            logger.info(f"✓ Language validation passed: {selected_language} ({expected_lang_code})")
            return True, final_url, "Redirection successful", selected_language

        except Exception as e:
            logger.error(f"Error during footer navigation for '{footer_link_name}': {str(e)}")
            return False, None, f"Error: {str(e)}", None
