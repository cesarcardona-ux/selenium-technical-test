"""
seatmap_page.py - Page Object para la página de selección de asientos

Este archivo representa la página SEATMAP usando el patrón Page Object Model (POM).
Contiene todos los selectores y acciones para seleccionar asientos por pasajero.

Caso 1: Seleccionar asientos Economy para los 3 pasajeros (Adulto, Joven, Niño)
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
    Page Object de la página de selección de asientos (Seatmap).

    Responsabilidades:
    - Esperar a que cargue la página Seatmap
    - Seleccionar pasajero por tipo (Adulto, Joven, Niño)
    - Seleccionar asiento Economy disponible
    - Continuar al siguiente paso (Payment)
    """

    # ==================== LOCATORS ====================

    # Botón "Ir a pagar" (después de seleccionar asientos)
    GO_TO_PAYMENT_BUTTON = (By.XPATH, "//button[contains(@class, 'amount-summary_button')]//span[contains(text(), 'Ir a pagar')]")

    # Contenedor de lista de pasajeros
    PASSENGER_LIST = (By.XPATH, "//div[@class='pax-selector_list']")

    # Lista de TODOS los asientos Economy del vuelo
    # Filas Economy: 4, 11, 15-32
    # Cada fila tiene 6 asientos: A, B, C, D, E, K
    # Generar lista completa de IDs de asientos Economy
    def _generate_economy_seat_ids():
        """
        Genera todos los IDs de asientos Economy.

        Returns:
            list: Lista de IDs de asientos Economy
        """
        seat_letters = ['A', 'B', 'C', 'D', 'E', 'K']
        economy_rows = [4, 11] + list(range(15, 33))  # Filas 4, 11, 15-32

        seat_ids = []
        for row in economy_rows:
            for letter in seat_letters:
                seat_ids.append(f"{row}{letter}_ECONOMY")

        return seat_ids

    ECONOMY_SEAT_IDS = _generate_economy_seat_ids()

    # ==================== CONSTRUCTOR ====================
    def __init__(self, driver):
        """
        Constructor de la clase.

        Args:
            driver: Instancia de Selenium WebDriver
        """
        self.driver = driver
        self.wait = WebDriverWait(driver, 25)  # Wait más largo para carga de mapa de asientos
        logger.info("SeatmapPage object initialized")

    # ==================== MÉTODOS ====================

    def wait_for_page_load(self):
        """
        Espera a que la página de Seatmap cargue completamente.
        Verifica que:
        1. La URL contenga indicadores de seatmap
        2. Haya lista de pasajeros visible
        3. Angular haya inicializado completamente (evitar ConfigurationErrorsException)

        Returns:
            bool: True si la página cargó correctamente
        """
        logger.info("Waiting for Seatmap page to load...")

        try:
            # Esperar a que cambie la URL
            time.sleep(3)

            current_url = self.driver.current_url
            logger.info(f"Current URL: {current_url}")

            # Esperar a que aparezca la lista de pasajeros
            self.wait.until(EC.presence_of_element_located(self.PASSENGER_LIST))
            logger.info("Passenger list found")

            # Esperar a que aparezcan asientos Economy
            time.sleep(3)

            # CRÍTICO: Esperar más tiempo para que Angular complete la inicialización del estado interno
            # Sin esto, obtenemos "ConfigurationErrorsException" al hacer click en asientos
            # El problema: Angular necesita tiempo para inicializar el estado de la reserva (PNR),
            # pasajeros, y configuración del seatmap ANTES de procesar clicks
            logger.info("Waiting additional 10 seconds for Angular to fully initialize internal state...")
            logger.info("(This prevents ConfigurationErrorsException modal)")
            time.sleep(10)

            logger.info("✓ Seatmap page loaded successfully")
            return True

        except Exception as e:
            logger.error(f"✗ Error waiting for Seatmap page: {e}")
            return False

    def show_seat_info(self, seat_id, seat_classes, action="CHECKING"):
        """
        Muestra información del asiento en pantalla durante el test (TEMPORAL - debugging).
        Crea un overlay visual en la esquina superior derecha.

        Args:
            seat_id (str): ID del asiento
            seat_classes (str): Clases CSS del asiento
            action (str): Acción actual (CHECKING, CLICKING, SELECTED, ERROR)
        """
        try:
            # Colores según acción
            color_map = {
                "CHECKING": "#FFA500",  # Orange
                "CLICKING": "#00FF00",   # Green
                "SELECTED": "#0080FF",   # Blue
                "ERROR": "#FF0000"       # Red
            }
            color = color_map.get(action, "#FFFFFF")

            # Crear mensaje HTML
            message = f"""
            <div style='margin-bottom: 10px; border-bottom: 1px solid #444; padding-bottom: 8px;'>
                <strong style='color: {color};'>{action}</strong>
            </div>
            <div><strong>Seat ID:</strong> {seat_id}</div>
            <div><strong>Classes:</strong> {seat_classes}</div>
            <div style='margin-top: 8px; font-size: 12px; color: #888;'>
                {time.strftime('%H:%M:%S')}
            </div>
            """

            # JavaScript para crear/actualizar el overlay
            js_code = f"""
            let overlay = document.getElementById('selenium-seat-debug');
            if (!overlay) {{
                overlay = document.createElement('div');
                overlay.id = 'selenium-seat-debug';
                overlay.style.cssText = `
                    position: fixed;
                    top: 20px;
                    right: 20px;
                    background: rgba(0, 0, 0, 0.95);
                    color: #00ff00;
                    padding: 15px 20px;
                    border-radius: 8px;
                    font-family: 'Courier New', monospace;
                    font-size: 14px;
                    z-index: 999999;
                    box-shadow: 0 4px 12px rgba(0,255,0,0.3);
                    border: 2px solid #00ff00;
                    min-width: 300px;
                `;
                document.body.appendChild(overlay);
            }}

            overlay.innerHTML = `{message}`;
            overlay.style.display = 'block';
            """

            self.driver.execute_script(js_code)
        except Exception as e:
            logger.warning(f"Could not display seat info overlay: {e}")

    def hide_seat_info(self):
        """
        Oculta el overlay de información de asientos.
        """
        try:
            js_code = """
            let overlay = document.getElementById('selenium-seat-debug');
            if (overlay) {
                overlay.style.display = 'none';
            }
            """
            self.driver.execute_script(js_code)
        except:
            pass

    def select_passenger_by_text(self, passenger_text):
        """
        Selecciona un pasajero por el texto de su tipo.

        Args:
            passenger_text (str): Texto del tipo de pasajero (ej: "Adulto 1", "Joven 1", "Niño 1")

        Returns:
            bool: True si se seleccionó correctamente
        """
        logger.info(f"Selecting passenger: {passenger_text}...")

        try:
            # Buscar botón de pasajero por texto
            # XPath: //button[.//span[contains(@class, 'pax-selector_pax-type') and contains(text(), 'Adulto 1')]]
            passenger_xpath = f"//button[.//span[contains(@class, 'pax-selector_pax-type') and contains(text(), '{passenger_text}')]]"

            passenger_button = self.wait.until(
                EC.presence_of_element_located((By.XPATH, passenger_xpath))
            )

            # Scroll al elemento
            self.driver.execute_script("arguments[0].scrollIntoView(true);", passenger_button)
            time.sleep(0.5)

            # Click usando JavaScript
            self.driver.execute_script("arguments[0].click();", passenger_button)
            logger.info(f"✓ Passenger '{passenger_text}' selected")

            time.sleep(1)  # Esperar a que se actualice el mapa de asientos
            return True

        except Exception as e:
            logger.error(f"✗ Error selecting passenger '{passenger_text}': {e}")
            return False

    def select_first_available_economy_seat(self):
        """
        Selecciona el primer asiento Economy disponible de la lista de 6 asientos exactos.
        Itera por los IDs específicos (4A_ECONOMY, 4B_ECONOMY, 4C_ECONOMY, 4D_ECONOMY, 4E_ECONOMY, 4K_ECONOMY).
        Verifica que NO tenga la clase "selected" ni "unavailable".
        Después del click, espera a que el asiento se marque como "selected".

        Returns:
            tuple: (bool, str) - (Éxito, ID del asiento seleccionado)
        """
        logger.info("Selecting first available Economy seat from pre-loaded seat directory...")

        try:
            # PASO 1: Pre-cargar TODOS los elementos de asientos Economy de UNA SOLA VEZ
            # Esto evita hacer find_element() repetidamente, lo cual interrumpe Angular
            logger.info("  STEP 1: Loading all Economy seat elements into directory (one-time batch query)...")

            seat_directory = {}  # Dictionary: {seat_id: WebElement}

            for seat_id in self.ECONOMY_SEAT_IDS:
                try:
                    seat_element = self.driver.find_element(By.ID, seat_id)
                    seat_directory[seat_id] = seat_element
                except:
                    # Si un asiento no existe en el DOM, simplemente no lo agregamos
                    pass

            logger.info(f"  ✓ Loaded {len(seat_directory)} Economy seat elements into directory")

            # PASO 2: Iterar por el directorio pre-cargado (SIN más búsquedas dinámicas)
            logger.info("  STEP 2: Iterating through pre-loaded seat directory...")

            attempts = 0
            for seat_id, seat in seat_directory.items():
                attempts += 1
                try:
                    seat_classes = seat.get_attribute("class")

                    # VISUAL DEBUG: Mostrar información del asiento en pantalla
                    self.show_seat_info(seat_id, seat_classes, "CHECKING")

                    logger.info(f"  Checking seat {seat_id}: classes = '{seat_classes}'")

                    # IMPORTANTE: Verificar que es clase Economy (NO tiene "upfront" ni "xlarge")
                    # Premium seats: class="seat upfront ng-star-inserted"
                    # Plus seats: class="seat xlarge ng-star-inserted"
                    # Economy seats: class="seat ng-star-inserted" (solo "seat", sin palabras extra)
                    if "upfront" in seat_classes or "xlarge" in seat_classes:
                        logger.info(f"  ✗ Seat {seat_id} is NOT Economy (has upfront/xlarge class)")
                        continue

                    # Verificar si está disponible (tiene "seat" pero NO tiene "selected" ni "unavailable")
                    if "seat" in seat_classes and "selected" not in seat_classes and "unavailable" not in seat_classes:
                        logger.info(f"  ✓ Seat {seat_id} is available, attempting to select...")

                        # Scroll al asiento
                        self.driver.execute_script("arguments[0].scrollIntoView({behavior: 'auto', block: 'center'});", seat)
                        time.sleep(1)

                        # Esperar a que el asiento sea clickeable
                        try:
                            clickable_seat = self.wait.until(
                                EC.element_to_be_clickable((By.ID, seat_id))
                            )
                        except:
                            logger.warning(f"  ⚠ Seat {seat_id} not clickable, skipping...")
                            continue

                        # VISUAL DEBUG: Mostrar que estamos haciendo click
                        self.show_seat_info(seat_id, seat_classes, "CLICKING")

                        # CAMBIO CRÍTICO: Usar click NORMAL de Selenium (no JavaScript click)
                        # El JavaScript click no dispara los event listeners correctos
                        clickable_seat.click()
                        logger.info(f"  Clicked on seat: {seat_id}")

                        # Esperar 2 segundos para ver si aparece un modal
                        time.sleep(2)

                        # IMPORTANTE: Verificar si apareció un modal de error/advertencia
                        try:
                            modal = self.driver.find_element(By.CSS_SELECTOR, "ngb-modal-window.modal-alert")

                            # VISUAL DEBUG: Mostrar que se detectó un modal (ERROR)
                            self.show_seat_info(seat_id, seat_classes, "ERROR")

                            logger.error(f"⚠⚠⚠ MODAL DETECTED! This should NOT happen in manual testing!")

                            # TOMAR SCREENSHOT DEL MODAL ANTES DE CERRARLO
                            try:
                                screenshot_path = f"reports/modal_error_{seat_id}.png"
                                self.driver.save_screenshot(screenshot_path)
                                logger.error(f"⚠⚠⚠ MODAL SCREENSHOT SAVED: {screenshot_path}")
                            except Exception as e:
                                logger.error(f"Failed to save modal screenshot: {e}")

                            # Intentar capturar el texto del modal
                            try:
                                modal_body = modal.find_element(By.CSS_SELECTOR, ".modal-body, .modal-content, .alert-warning, div")
                                modal_text = modal_body.text if modal_body else modal.text
                                logger.error(f"⚠⚠⚠ MODAL TEXT: {modal_text}")
                            except Exception as e:
                                logger.error(f"Failed to get modal text: {e}")

                            # NO CERRAR EL MODAL - Dejar que el usuario lo vea en el screenshot
                            # Esperar 5 segundos para que quede bien visible en el screenshot
                            logger.error(f"Stopping execution for screenshot inspection...")
                            time.sleep(5)

                            # Ahora buscar botón de cierre del modal (X, Cerrar, Aceptar, OK, etc.)
                            close_selectors = [
                                "button[aria-label='Close']",
                                "button.close",
                                "button.btn-close",
                                "//button[contains(text(), 'Aceptar')]",
                                "//button[contains(text(), 'OK')]",
                                "//button[contains(text(), 'Cerrar')]",
                                "//button[contains(@class, 'close')]"
                            ]

                            modal_closed = False
                            for selector in close_selectors:
                                try:
                                    if selector.startswith("//"):
                                        close_btn = self.driver.find_element(By.XPATH, selector)
                                    else:
                                        close_btn = self.driver.find_element(By.CSS_SELECTOR, selector)
                                    close_btn.click()
                                    logger.info(f"  ✓ Modal closed using selector: {selector[:30]}...")
                                    modal_closed = True
                                    break
                                except:
                                    continue

                            if not modal_closed:
                                logger.warning(f"  ⚠ Could not close modal, continuing anyway...")

                            time.sleep(1)
                        except:
                            # No hay modal, perfecto
                            pass

                        # Esperar 8 segundos más (total 10 seg) para que el asiento cambie a 'selected'
                        logger.info(f"  Waiting 8 more seconds for seat to change to 'selected'...")
                        time.sleep(8)

                        # Verificar UNA SOLA VEZ si se marcó como selected
                        try:
                            updated_seat = self.driver.find_element(By.ID, seat_id)
                            updated_classes = updated_seat.get_attribute("class")
                            logger.info(f"  After 5s, seat classes: '{updated_classes}'")

                            if "selected" in updated_classes:
                                # VISUAL DEBUG: Mostrar que el asiento fue seleccionado exitosamente
                                self.show_seat_info(seat_id, updated_classes, "SELECTED")

                                logger.info(f"✓ Economy seat selected successfully: {seat_id}")
                                time.sleep(2)  # Esperar un poco más para que se vea el mensaje SELECTED
                                return True, seat_id
                            else:
                                logger.warning(f"⚠ Seat {seat_id} still not marked as 'selected' after 5 seconds")
                                # Continuar probando el siguiente asiento
                                continue
                        except Exception as e:
                            logger.warning(f"⚠ Error checking seat status: {e}")
                            continue
                    else:
                        logger.info(f"  ✗ Seat {seat_id} is NOT available (selected or unavailable)")

                except Exception as e:
                    logger.warning(f"  ✗ Could not find or check seat {seat_id}: {e}")
                    continue

            # Si llegamos aquí, ningún asiento estuvo disponible o pudo ser seleccionado
            logger.error(f"✗ No available Economy seats found after checking {attempts} seats")
            return False, None

        except Exception as e:
            logger.error(f"✗ Error selecting Economy seat: {e}")
            import traceback
            traceback.print_exc()
            return False, None

    def assign_seats_to_passengers(self, passenger_count=3):
        """
        Asigna asientos Economy a todos los pasajeros en orden.

        FLUJO CORRECTO (según comportamiento real de nuxqa):
        1. El primer pasajero YA está seleccionado automáticamente
        2. Solo hacer click en el asiento → la página se RECARGA automáticamente
        3. El siguiente pasajero queda seleccionado automáticamente
        4. Repetir: click en asiento → recarga → siguiente pasajero

        NO SE DEBE HACER CLICK EN LOS PASAJEROS MANUALMENTE.

        Args:
            passenger_count (int): Número de pasajeros (default 3)

        Returns:
            dict: Diccionario con pasajeros y sus asientos asignados
        """
        logger.info(f"Assigning Economy seats to {passenger_count} passengers...")
        logger.info("NOTE: Passengers are auto-selected after each seat click. NO manual passenger selection needed.")

        passenger_types = [
            "Adulto 1",
            "Joven 1",
            "Niño 1"
        ][:passenger_count]  # Solo para tracking/logging

        seat_assignments = {}

        try:
            for i, passenger_type in enumerate(passenger_types):
                logger.info(f"")
                logger.info(f"========== Passenger {i+1}/3: {passenger_type} ==========")
                logger.info(f"  (Passenger is ALREADY auto-selected by the page)")

                # Solo seleccionar el asiento (NO seleccionar pasajero manualmente)
                logger.info(f"  Selecting Economy seat for passenger {i+1}...")
                seat_selected, seat_id = self.select_first_available_economy_seat()

                if not seat_selected:
                    logger.error(f"  ✗ Failed to select seat for passenger {i+1}")
                    continue

                seat_assignments[passenger_type] = seat_id
                logger.info(f"✓ Passenger {i+1} ({passenger_type}) → Seat {seat_id}")

                # Esperar a que la página se recargue y seleccione el siguiente pasajero
                # Solo si no es el último pasajero
                if i < passenger_count - 1:
                    logger.info(f"  Waiting for page reload and auto-selection of next passenger...")
                    time.sleep(3)

            logger.info(f"✓ All {len(seat_assignments)} passengers assigned seats successfully")

            # CRÍTICO: Esperar tiempo adicional para que la página actualice el botón correctamente
            logger.info("Waiting 5 additional seconds for page to finalize seat selection state...")
            time.sleep(5)

            return seat_assignments

        except Exception as e:
            logger.error(f"✗ Error assigning seats: {e}")
            return seat_assignments

    def click_go_to_payment(self):
        """
        Hace click en el botón "Ir a pagar" para ir a la página de Payment.

        IMPORTANTE: Debe buscar específicamente el botón "Ir a pagar" y NO el botón "Continuar".
        Si clickea "Continuar" en lugar de "Ir a pagar", va a Services en lugar de Payment.

        Returns:
            bool: True si se hizo click correctamente
        """
        logger.info("Clicking 'Ir a pagar' button...")

        try:
            # Scroll hacia abajo para ver el botón
            self.driver.execute_script("window.scrollTo(0, document.body.scrollHeight);")
            time.sleep(2)

            # DEBUGGING: Tomar screenshot ANTES de hacer click
            try:
                debug_screenshot = f"reports/debug_before_payment_button_{int(time.time())}.png"
                self.driver.save_screenshot(debug_screenshot)
                logger.info(f"📸 Screenshot saved before clicking button: {debug_screenshot}")
            except:
                pass

            # Buscar botón "Ir a pagar" usando el HTML exacto proporcionado por el usuario
            # HTML: <ds-button class="amount-summary_button--skipstep"><button aria-labelledby="Ir a pagar"><span class="button_label"> Ir a pagar </span></button></ds-button>

            # Selectores SÚPER ESPECÍFICOS basados en el HTML real:
            go_to_payment_selectors = [
                # Selector 1: ÓPTIMO - Por aria-labelledby (atributo único del botón "Ir a pagar")
                "//button[@aria-labelledby='Ir a pagar']",
                # Selector 2: Por clase específica amount-summary_button--skipstep
                "//ds-button[contains(@class, 'amount-summary_button--skipstep')]//button",
                # Selector 3: Por span con texto exacto (incluyendo espacios)
                "//span[@class='button_label' and contains(text(), 'Ir a pagar')]",
                # Selector 4: Fallback - ds-button con clase amount-summary_button
                "//ds-button[contains(@class, 'amount-summary_button')]//button",
            ]

            go_to_payment_btn = None
            used_selector = None
            for selector in go_to_payment_selectors:
                try:
                    # Si el selector busca span, obtenemos el botón padre
                    if selector.startswith("//span"):
                        span_elem = self.driver.find_element(By.XPATH, selector)
                        go_to_payment_btn = span_elem.find_element(By.XPATH, "./ancestor::button")
                        logger.info(f"✓ 'Ir a pagar' button found via span, selector: {selector[:60]}...")
                    else:
                        go_to_payment_btn = self.driver.find_element(By.XPATH, selector)
                        logger.info(f"✓ 'Ir a pagar' button found directly, selector: {selector[:60]}...")

                    used_selector = selector
                    logger.info(f"✓ Button found successfully with selector: {selector}")
                    break
                except Exception as e:
                    logger.debug(f"Selector '{selector[:40]}...' failed: {e}")
                    continue

            if not go_to_payment_btn:
                logger.error("'Ir a pagar' button not found with any selector")
                return False

            # Loggear información del botón antes de hacer click
            logger.info(f"Button to click: text='{go_to_payment_btn.text}', class='{go_to_payment_btn.get_attribute('class')}'")

            # Scroll al botón
            self.driver.execute_script("arguments[0].scrollIntoView(true);", go_to_payment_btn)
            time.sleep(1)

            # Click usando JavaScript
            self.driver.execute_script("arguments[0].click();", go_to_payment_btn)
            logger.info("✓ 'Ir a pagar' button clicked successfully")

            time.sleep(5)  # Esperar más tiempo a que cargue la página de Payment
            return True

        except Exception as e:
            logger.error(f"✗ Error clicking 'Ir a pagar' button: {e}")
            import traceback
            traceback.print_exc()
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
