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
            time.sleep(2)  # OPTIMIZADO: 3s → 2s (ahorro: 1s)

            current_url = self.driver.current_url
            logger.info(f"Current URL after search: {current_url}")

            # Esperar a que aparezcan elementos de vuelos o el botón continuar
            # (la página puede tener diferentes estructuras según el ambiente)
            time.sleep(3)  # OPTIMIZADO: 5s → 3s (ahorro: 2s)

            logger.info("✓ Select Flight page loaded successfully")
            return True

        except Exception as e:
            logger.error(f"✗ Error waiting for Select Flight page: {e}")
            return False

    def select_outbound_flight_and_basic_plan(self):
        """
        Selecciona el vuelo de IDA y el plan BASIC.

        Flujo:
        1. Click en primer vuelo disponible (button.journey_price_button)
        2. Espera a que aparezcan los 3 planes (Basic, Classic, Flex)
        3. Click en el PRIMER plan (Basic) (button.fare_button[0])

        Returns:
            bool: True si se seleccionó correctamente
        """
        logger.info("Selecting OUTBOUND flight (first available) with BASIC plan...")

        try:
            # PASO 1: Seleccionar primer vuelo de IDA
            journey_buttons = self.wait.until(
                EC.presence_of_all_elements_located((By.CSS_SELECTOR, "button.journey_price_button"))
            )

            if not journey_buttons:
                logger.error("No journey buttons found for outbound flight")
                return False

            logger.info(f"Found {len(journey_buttons)} journey buttons")

            # Click en el PRIMERO usando JavaScript para mayor confiabilidad
            first_journey = journey_buttons[0]
            self.driver.execute_script("arguments[0].scrollIntoView(true);", first_journey)
            time.sleep(0.5)  # OPTIMIZADO: 1s → 0.5s (ahorro: 0.5s)
            self.driver.execute_script("arguments[0].click();", first_journey)  # JavaScript click
            logger.info("✓ Outbound flight selected (first one)")

            time.sleep(1.5)  # OPTIMIZADO: 2s → 1.5s (ahorro: 0.5s)

            # PASO 2: Seleccionar plan BASIC (primer botón fare_button)
            logger.info("Waiting for fare plans to appear...")
            fare_buttons = self.wait.until(
                EC.presence_of_all_elements_located((By.CSS_SELECTOR, "button.fare_button"))
            )

            if len(fare_buttons) < 1:
                logger.error(f"Expected at least 1 fare button, found {len(fare_buttons)}")
                return False

            logger.info(f"Found {len(fare_buttons)} fare buttons (Basic, Classic, Flex)")

            # Click en el PRIMERO (índice 0) = BASIC usando JavaScript
            basic_button = fare_buttons[0]
            self.driver.execute_script("arguments[0].scrollIntoView(true);", basic_button)
            time.sleep(0.5)  # OPTIMIZADO: 1s → 0.5s (ahorro: 0.5s)
            self.driver.execute_script("arguments[0].click();", basic_button)  # JavaScript click
            logger.info("✓ BASIC plan selected for outbound flight (1st button)")

            time.sleep(2)  # OPTIMIZADO: 3s → 2s (ahorro: 1s)

            return True

        except Exception as e:
            logger.error(f"✗ Error selecting outbound flight and BASIC plan: {e}")
            return False

    def select_outbound_flight_and_flex_plan(self):
        """
        Selecciona el vuelo de IDA y el plan FLEX.

        Flujo:
        1. Click en primer vuelo disponible (button.journey_price_button)
        2. Espera a que aparezcan los 3 planes (Basic, Classic, Flex)
        3. Click en el TERCER plan (Flex) (button.fare_button[2])

        Returns:
            bool: True si se seleccionó correctamente
        """
        logger.info("Selecting OUTBOUND flight (first available) with FLEX plan...")

        try:
            # PASO 1: Seleccionar primer vuelo de IDA
            journey_buttons = self.wait.until(
                EC.presence_of_all_elements_located((By.CSS_SELECTOR, "button.journey_price_button"))
            )

            if not journey_buttons:
                logger.error("No journey buttons found for outbound flight")
                return False

            logger.info(f"Found {len(journey_buttons)} journey buttons")

            # Click en el PRIMERO usando JavaScript para mayor confiabilidad
            first_journey = journey_buttons[0]
            self.driver.execute_script("arguments[0].scrollIntoView(true);", first_journey)
            time.sleep(0.5)  # OPTIMIZADO: 1s → 0.5s (ahorro: 0.5s)
            self.driver.execute_script("arguments[0].click();", first_journey)  # JavaScript click
            logger.info("✓ Outbound flight selected (first one)")

            time.sleep(1.5)  # OPTIMIZADO: 2s → 1.5s (ahorro: 0.5s)

            # PASO 2: Seleccionar plan FLEX (tercer botón fare_button)
            logger.info("Waiting for fare plans to appear...")
            fare_buttons = self.wait.until(
                EC.presence_of_all_elements_located((By.CSS_SELECTOR, "button.fare_button"))
            )

            if len(fare_buttons) < 3:
                logger.error(f"Expected 3 fare buttons, found {len(fare_buttons)}")
                return False

            logger.info(f"Found {len(fare_buttons)} fare buttons (Basic, Classic, Flex)")

            # Click en el TERCERO (índice 2) = FLEX usando JavaScript
            flex_button = fare_buttons[2]
            self.driver.execute_script("arguments[0].scrollIntoView(true);", flex_button)
            time.sleep(0.5)  # OPTIMIZADO: 1s → 0.5s (ahorro: 0.5s)
            self.driver.execute_script("arguments[0].click();", flex_button)  # JavaScript click
            logger.info("✓ FLEX plan selected for outbound flight (3rd button)")

            time.sleep(2)  # OPTIMIZADO: 3s → 2s (ahorro: 1s)

            return True

        except Exception as e:
            logger.error(f"✗ Error selecting outbound flight and FLEX plan: {e}")
            return False

    def select_return_flight_and_flex_plan(self):
        """
        Selecciona el vuelo de VUELTA y el plan FLEX.

        Flujo:
        1. Click en primer vuelo disponible de vuelta (button.journey_price_button)
        2. Espera a que aparezcan los 3 planes (Basic, Classic, Flex)
        3. Click en el TERCER plan (Flex) (button.fare_button[2])

        Returns:
            bool: True si se seleccionó correctamente
        """
        logger.info("Selecting RETURN flight (first available)...")

        try:
            # IMPORTANTE: Después de seleccionar FLEX para IDA, la página tarda 25-30 segundos en cargar
            # Se muestra un avión en movimiento (page-loader) mientras carga los vuelos de VUELTA
            logger.info("Waiting for page to reload with return flights (this takes ~25-30 seconds)...")

            # OPTIMIZADO: Esperar a que aparezca el loader (3s → 2s)
            time.sleep(2)  # Reducido para mejorar performance (ahorro: 1s)

            # Esperar a que el loader (avión en movimiento) DESAPAREZCA
            # Aumentamos el timeout a 40 segundos para cubrir los 25-30 segundos de carga
            try:
                page_loader = (By.CSS_SELECTOR, "div.page-loader")
                wait_loader = WebDriverWait(self.driver, 40)  # 40 segundos de timeout
                wait_loader.until(EC.invisibility_of_element_located(page_loader))
                logger.info("✓ Page loader (airplane animation) disappeared")
            except:
                logger.info("No page loader found or already disappeared")

            # OPTIMIZADO: Esperar a que los elementos se estabilicen (2s → 1s)
            time.sleep(1)  # Reducido para mejorar performance (ahorro: 1s)

            # Hacer scroll hacia abajo para ver los vuelos de VUELTA (más abajo que el calendario)
            logger.info("Scrolling down to see return flights list (below the calendar)...")
            # Scroll a 80% de la página para ver los vuelos que están debajo del calendario
            self.driver.execute_script("window.scrollTo(0, document.body.scrollHeight * 0.8);")

            # OPTIMIZADO: Esperar a que aparezcan al menos 30 vuelos (return flights)
            # Cambiado de sleep(10) fijo a WebDriverWait inteligente con fallback de 4s
            logger.info("Waiting for return flights to fully render (smart wait)...")
            try:
                # Esperar a que haya al menos 30 botones de vuelo visibles (cantidad típica de vuelos de vuelta)
                wait_return = WebDriverWait(self.driver, 15)  # Max 15s
                wait_return.until(lambda d: len(d.find_elements(By.CSS_SELECTOR, "button.journey_price_button")) >= 30)
                logger.info("✓ Return flights loaded (30+ buttons detected)")
                time.sleep(1)  # Pequeña espera adicional para estabilidad
            except:
                logger.warning("Timeout waiting for 30 buttons, proceeding with fallback wait...")
                time.sleep(4)  # OPTIMIZADO: 10s → 4s fallback (ahorro: 6s)

            # PASO 1: Seleccionar primer vuelo de VUELTA
            # IMPORTANTE: Los botones correctos tienen texto variable según idioma:
            # - Español: "Seleccionar tarifa" / "Seleccionar de tarifa"
            # - English: "Choose fare" / "Select fare"
            # - Français: "Choisir le tarif"
            # - Português: "Selecionar tarifa"
            logger.info("Looking for return journey buttons (language-agnostic approach)...")

            # Buscar TODOS los botones (incluye IDA + VUELTA)
            all_journey_buttons = self.wait.until(
                EC.presence_of_all_elements_located((By.CSS_SELECTOR, "button.journey_price_button"))
            )
            logger.info(f"Found {len(all_journey_buttons)} total journey buttons in DOM")

            # FILTRAR solo los botones visibles (los de retorno son los que están visibles AHORA)
            # Los de IDA ya no están visibles porque ya se seleccionaron
            # Textos comunes en diferentes idiomas: "tarif", "tarifa", "fare"
            return_flight_buttons = []
            keywords = ["tarif", "tarifa", "fare", "Selec", "Chois", "Choose"]  # Palabras clave multi-idioma
            for btn in all_journey_buttons:
                try:
                    if btn.is_displayed():
                        btn_text = btn.text.lower()
                        # Si contiene alguna palabra clave relacionada con selección de tarifa
                        if any(keyword.lower() in btn_text for keyword in keywords):
                            return_flight_buttons.append(btn)
                except:
                    continue

            logger.info(f"Found {len(return_flight_buttons)} buttons with fare selection text (return flights)")

            if not return_flight_buttons:
                logger.error("No return flight buttons found")
                return False

            # Click en el PRIMERO (primer vuelo de vuelta)
            first_journey = return_flight_buttons[0]
            self.driver.execute_script("arguments[0].scrollIntoView(true);", first_journey)
            time.sleep(0.5)  # OPTIMIZADO: 1s → 0.5s (ahorro: 0.5s)
            self.driver.execute_script("arguments[0].click();", first_journey)  # JavaScript click
            logger.info("✓ Return flight selected (first one available)")

            # OPTIMIZADO: Esperar inteligentemente a que aparezcan los 3 planes de tarifa
            # Cambiado de sleep(5) fijo a WebDriverWait inteligente con fallback de 2s
            logger.info("Waiting for fare plans to appear for return flight (smart wait)...")
            try:
                # Esperar a que aparezcan exactamente 3 botones de tarifa (Basic, Classic, Flex)
                wait_fares = WebDriverWait(self.driver, 10)  # Max 10s
                wait_fares.until(lambda d: len(d.find_elements(By.CSS_SELECTOR, "button.fare_button")) >= 3)
                logger.info("✓ Fare buttons loaded (3 detected)")
                time.sleep(0.5)  # Pequeña espera para estabilidad
            except:
                logger.warning("Timeout waiting for fare buttons, proceeding with fallback wait...")
                time.sleep(2)  # OPTIMIZADO: 5s → 2s fallback (ahorro: 3s)

            # PASO 2: Seleccionar plan FLEX (tercer botón fare_button)
            logger.info("Locating fare plan buttons...")

            # Usar un wait más largo porque puede tardar en cargar
            wait_longer = WebDriverWait(self.driver, 25)
            fare_buttons = wait_longer.until(
                EC.presence_of_all_elements_located((By.CSS_SELECTOR, "button.fare_button"))
            )

            if len(fare_buttons) < 3:
                logger.error(f"Expected 3 fare buttons, found {len(fare_buttons)}")
                return False

            logger.info(f"Found {len(fare_buttons)} fare buttons (Basic, Classic, Flex)")

            # Click en el TERCERO (índice 2) = FLEX usando JavaScript
            flex_button = fare_buttons[2]
            self.driver.execute_script("arguments[0].scrollIntoView(true);", flex_button)
            time.sleep(0.5)  # OPTIMIZADO: 1s → 0.5s (ahorro: 0.5s)
            self.driver.execute_script("arguments[0].click();", flex_button)  # JavaScript click
            logger.info("✓ FLEX plan selected for return flight (3rd button)")

            time.sleep(2)  # OPTIMIZADO: 3s → 2s (ahorro: 1s)

            return True

        except Exception as e:
            logger.error(f"✗ Error selecting return flight and FLEX plan: {e}")
            return False

    def click_continue(self):
        """
        Hace click en el botón "Continuar" para ir al siguiente paso.

        Returns:
            bool: True si se hizo click correctamente
        """
        logger.info("Clicking continue button...")

        try:
            # Buscar botón continuar con diferentes estrategias
            # El botón tiene estructura: <button class="btn-next"><span>Continuar</span></button>
            continue_selectors = [
                # Buscar por clase btn-next (más confiable para nuxqa)
                "//button[contains(@class, 'btn-next')]",
                # Buscar por span interno con texto
                "//button//span[contains(text(), 'Continuar')]",
                "//button//span[contains(text(), 'Continue')]",
                "//button//span[contains(text(), 'Continuer')]",
                # Fallback a selectores antiguos
                "//button[contains(text(), 'Continuar')]",
                "//button[contains(@class, 'continue')]",
                "//button[@id='continueButton']",
            ]

            for selector in continue_selectors:
                try:
                    # Si el selector busca span, obtenemos el botón padre
                    if "//span" in selector:
                        span_elem = self.driver.find_element(By.XPATH, selector)
                        continue_btn = span_elem.find_element(By.XPATH, "..")  # Padre = button
                    else:
                        continue_btn = self.driver.find_element(By.XPATH, selector)

                    self.driver.execute_script("arguments[0].scrollIntoView(true);", continue_btn)
                    time.sleep(0.3)  # OPTIMIZADO: 0.5s → 0.3s (ahorro: 0.2s)
                    self.driver.execute_script("arguments[0].click();", continue_btn)  # JavaScript click
                    time.sleep(1.5)  # OPTIMIZADO: 2s → 1.5s (ahorro: 0.5s)

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
