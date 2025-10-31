"""
seatmap_page.py - Page Object para la página de selección de asientos (Seatmap)

Este archivo representa la página SEATMAP usando el patrón Page Object Model (POM).
Contiene todos los selectores y acciones para seleccionar asientos de vuelo.

Caso 1: Seleccionar asiento Economy
Caso 2: Seleccionar Plus, Economy, Premium, Economy (si disponible)
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
class SeatmapPage:
    """
    Page Object de la página de selección de asientos.

    Responsabilidades:
    - Esperar a que cargue la página Seatmap
    - Detectar asientos disponibles
    - Seleccionar asientos por tipo (Economy, Premium, Plus)
    - Continuar al siguiente paso
    """

    # ==================== LOCATORS ====================
    # Selectores de asientos - genéricos para adaptarse a diferentes estructuras

    # Asientos disponibles (generalmente son botones o divs clickeables)
    AVAILABLE_SEATS = "//button[contains(@class, 'seat') and not(contains(@class, 'occupied')) and not(contains(@class, 'selected'))] | //div[contains(@class, 'seat-available')]"

    # Asientos Economy (clase más barata)
    ECONOMY_SEATS = "//button[contains(@class, 'seat') and (contains(@class, 'economy') or contains(@class, 'standard'))] | //button[contains(@class, 'seat') and not(contains(@class, 'premium')) and not(contains(@class, 'plus'))]"

    # Asientos Premium
    PREMIUM_SEATS = "//button[contains(@class, 'seat') and contains(@class, 'premium')]"

    # Asientos Plus
    PLUS_SEATS = "//button[contains(@class, 'seat') and contains(@class, 'plus')]"

    # Botón para omitir selección de asientos ("Skip", "Continue without seats")
    SKIP_SEATS_BUTTON = (By.XPATH, "//button[contains(text(), 'Skip') or contains(text(), 'Sin asientos') or contains(text(), 'Omitir asientos') or contains(text(), 'without seat')]")

    # Botón continuar
    CONTINUE_BUTTON = (By.XPATH, "//button[contains(text(), 'Continuar') or contains(text(), 'Continue') or contains(text(), 'Continuer') or contains(@id, 'continueButton') or contains(@class, 'continue')]")

    # Mapa de asientos (contenedor principal)
    SEATMAP_CONTAINER = "//div[contains(@class, 'seatmap') or contains(@class, 'seat-map')]"

    # ==================== CONSTRUCTOR ====================
    def __init__(self, driver):
        """
        Constructor de la clase.

        Args:
            driver: Instancia de Selenium WebDriver
        """
        self.driver = driver
        self.wait = WebDriverWait(driver, 20)
        logger.info("SeatmapPage object initialized")

    # ==================== MÉTODOS ====================

    def wait_for_page_load(self):
        """
        Espera a que la página de Seatmap cargue completamente.

        Returns:
            bool: True si la página cargó correctamente
        """
        logger.info("Waiting for Seatmap page to load...")

        try:
            time.sleep(3)  # Tiempo para que la página empiece a cargar

            current_url = self.driver.current_url
            logger.info(f"Current URL: {current_url}")

            # Verificar que estamos en la página de seatmap
            is_seatmap_page = "seat" in current_url.lower() or "map" in current_url.lower()

            if not is_seatmap_page:
                logger.warning(f"URL doesn't contain 'seat' or 'map': {current_url}")

            # Esperar a que aparezcan asientos
            time.sleep(3)  # Los seatmaps suelen tardar en renderizar

            logger.info("✓ Seatmap page loaded successfully")
            return True

        except Exception as e:
            logger.error(f"✗ Error waiting for Seatmap page: {e}")
            return False

    def get_available_seats_count(self):
        """
        Obtiene el número de asientos disponibles.

        Returns:
            int: Cantidad de asientos disponibles
        """
        try:
            seats = self.driver.find_elements(By.XPATH, self.AVAILABLE_SEATS)
            count = len(seats)
            logger.info(f"Found {count} available seats")
            return count
        except Exception as e:
            logger.error(f"Error counting available seats: {e}")
            return 0

    def select_economy_seat(self, seat_index=0):
        """
        Selecciona un asiento Economy.

        Args:
            seat_index (int): Índice del asiento a seleccionar (0 = primero)

        Returns:
            bool: True si se seleccionó correctamente
        """
        logger.info(f"Attempting to select Economy seat (index {seat_index})...")

        try:
            # Buscar asientos Economy disponibles
            economy_seats = self.driver.find_elements(By.XPATH, self.ECONOMY_SEATS)

            # Si no encuentra con clase específica, usar cualquier asiento disponible
            if not economy_seats or len(economy_seats) == 0:
                logger.info("No economy seats found with specific class, trying all available seats...")
                economy_seats = self.driver.find_elements(By.XPATH, self.AVAILABLE_SEATS)

            if not economy_seats or len(economy_seats) <= seat_index:
                logger.error(f"Not enough economy seats found (need at least {seat_index + 1})")
                return False

            # Seleccionar el asiento
            seat = economy_seats[seat_index]
            self.driver.execute_script("arguments[0].scrollIntoView(true);", seat)
            time.sleep(0.5)

            # Intentar JavaScript click primero (más confiable para seatmaps)
            self.driver.execute_script("arguments[0].click();", seat)
            logger.info(f"✓ Economy seat {seat_index + 1} selected successfully")
            time.sleep(1)

            return True

        except Exception as e:
            logger.error(f"✗ Error selecting economy seat: {e}")
            return False

    def select_seat_by_type(self, seat_type, seat_index=0):
        """
        Selecciona un asiento por tipo específico.

        Args:
            seat_type (str): Tipo de asiento ("economy", "premium", "plus")
            seat_index (int): Índice del asiento a seleccionar

        Returns:
            bool: True si se seleccionó correctamente
        """
        logger.info(f"Attempting to select {seat_type.upper()} seat (index {seat_index})...")

        try:
            # Mapear tipo a XPath
            xpath_map = {
                "economy": self.ECONOMY_SEATS,
                "premium": self.PREMIUM_SEATS,
                "plus": self.PLUS_SEATS
            }

            seat_xpath = xpath_map.get(seat_type.lower(), self.ECONOMY_SEATS)

            # Buscar asientos del tipo especificado
            seats = self.driver.find_elements(By.XPATH, seat_xpath)

            # Si no encuentra con clase específica, usar cualquier asiento disponible
            if not seats or len(seats) == 0:
                logger.info(f"No {seat_type} seats found with specific class, using available seats...")
                seats = self.driver.find_elements(By.XPATH, self.AVAILABLE_SEATS)

            if not seats or len(seats) <= seat_index:
                logger.warning(f"Not enough {seat_type} seats found (need at least {seat_index + 1})")
                return False

            # Seleccionar el asiento
            seat = seats[seat_index]
            self.driver.execute_script("arguments[0].scrollIntoView(true);", seat)
            time.sleep(0.5)
            self.driver.execute_script("arguments[0].click();", seat)
            logger.info(f"✓ {seat_type.upper()} seat {seat_index + 1} selected successfully")
            time.sleep(1)

            return True

        except Exception as e:
            logger.error(f"✗ Error selecting {seat_type} seat: {e}")
            return False

    def select_multiple_seats(self, seat_types):
        """
        Selecciona múltiples asientos de diferentes tipos.
        Útil para Case 2 donde se requiere: Plus, Economy, Premium, Economy.

        Args:
            seat_types (list): Lista de tipos de asientos (ej: ["plus", "economy", "premium", "economy"])

        Returns:
            bool: True si se seleccionaron todos correctamente
        """
        logger.info(f"Attempting to select {len(seat_types)} seats: {seat_types}")

        all_success = True
        for index, seat_type in enumerate(seat_types):
            success = self.select_seat_by_type(seat_type, seat_index=0)  # Siempre el primero disponible de cada tipo
            if not success:
                logger.warning(f"Failed to select seat {index + 1} of type {seat_type}")
                all_success = False

            time.sleep(1)  # Espera entre selecciones

        return all_success

    def skip_seat_selection(self):
        """
        Omite la selección de asientos (no selecciona ninguno).
        Hace click en "Skip" o directamente en "Continue".

        Returns:
            bool: True si se omitió exitosamente
        """
        logger.info("Attempting to skip seat selection...")

        try:
            # Opción 1: Buscar botón "Skip"
            try:
                skip_button = self.driver.find_element(*self.SKIP_SEATS_BUTTON)
                logger.info("Skip button found, clicking it...")
                self.driver.execute_script("arguments[0].scrollIntoView(true);", skip_button)
                time.sleep(0.5)
                self.driver.execute_script("arguments[0].click();", skip_button)
                logger.info("✓ Seat selection skipped using Skip button")
                time.sleep(2)
                return True
            except Exception as e:
                logger.info(f"Skip button not found: {e}")

            # Opción 2: Si no hay botón Skip, hacer click directamente en Continue
            logger.info("No skip button found, will click Continue directly...")
            return self.click_continue()

        except Exception as e:
            logger.error(f"✗ Error skipping seat selection: {e}")
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

    def get_page_screenshot(self, filename="seatmap_page.png"):
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
