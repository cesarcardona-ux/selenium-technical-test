"""
passengers_page.py - Page Object para la página de información de pasajeros

Este archivo representa la página PASSENGERS usando el patrón Page Object Model (POM).
Contiene todos los selectores y acciones para llenar información de pasajeros.

Caso 1 y 2: Ingresar información de pasajeros (datos fake permitidos)

SELECTORES BASADOS EN DEVTOOLS HTML DE NUXQA4/NUXQA5
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
class PassengersPage:
    """
    Page Object de la página de información de pasajeros.

    Responsabilidades:
    - Esperar a que cargue la página Passengers
    - Llenar formularios de pasajeros usando IDs dinámicos de nuxqa
    - Validar que se complete correctamente
    - Continuar al siguiente paso
    """

    # ==================== LOCATORS (basados en DevTools HTML) ====================
    # Los IDs tienen hashes dinámicos pero prefijos consistentes

    # Botón continuar
    CONTINUE_BUTTON = (By.XPATH, "//button[contains(text(), 'Continuar') or contains(text(), 'Continue') or contains(text(), 'Contin') or contains(@class, 'button-booking')]")

    # ==================== CONSTRUCTOR ====================
    def __init__(self, driver):
        """
        Constructor de la clase.

        Args:
            driver: Instancia de Selenium WebDriver
        """
        self.driver = driver
        self.wait = WebDriverWait(driver, 25)  # Timeout más largo para formularios
        logger.info("PassengersPage object initialized")

    # ==================== MÉTODOS ====================

    def wait_for_page_load(self):
        """
        Espera a que la página de Passengers cargue completamente.

        Returns:
            bool: True si la página cargó correctamente
        """
        logger.info("Waiting for Passengers page to load...")

        try:
            # Esperar más tiempo a que la página Angular se estabilice
            # La página puede tardar en cargar después de validaciones de Services
            time.sleep(10)  # Aumentado de 5 a 10 segundos

            current_url = self.driver.current_url
            logger.info(f"Current URL: {current_url}")

            # Esperar a que aparezcan los campos de nombre (primero que se carga)
            # Aumentar el timeout para dar más tiempo
            try:
                logger.info("Waiting for passenger form fields to appear (timeout: 30s)...")
                wait_extended = WebDriverWait(self.driver, 30)  # 30 segundos de espera
                first_name_inputs = wait_extended.until(
                    EC.presence_of_all_elements_located((By.CSS_SELECTOR, "input[id^='IdFirstName']"))
                )
                logger.info(f"✓ Found {len(first_name_inputs)} passenger forms")

                if len(first_name_inputs) == 0:
                    logger.error("No passenger forms found after waiting 30 seconds")
                    # Tomar screenshot para debug
                    self.driver.save_screenshot("reports/debug_no_forms.png")
                    return False

            except Exception as e:
                logger.error(f"Could not find passenger forms: {e}")
                # Tomar screenshot para debug
                self.driver.save_screenshot("reports/debug_forms_timeout.png")
                raise

            logger.info("✓ Passengers page loaded successfully")
            return True

        except Exception as e:
            logger.error(f"✗ Error waiting for Passengers page: {e}")
            return False

    def fill_passenger_info(self, passenger_index, passenger_type, first_name, last_name,
                           birth_date, gender="M", nationality="Colombia"):
        """
        Llena la información de un pasajero específico usando los IDs exactos de nuxqa.

        Args:
            passenger_index (int): Índice del pasajero (0 = primero, 1 = segundo, etc.)
            passenger_type (str): Tipo de pasajero ("Adult", "Teen", "Child", "Infant")
            first_name (str): Primer nombre
            last_name (str): Apellido
            birth_date (str): Fecha de nacimiento (formato YYYY-MM-DD)
            gender (str): Género ("M" o "F")
            nationality (str): Nacionalidad del documento

        Returns:
            bool: True si se llenó correctamente
        """
        logger.info(f"Filling passenger {passenger_index + 1} info ({passenger_type}): {first_name} {last_name}")

        try:
            # PASO 1: Llenar NOMBRE
            logger.info(f"  1. Filling first name: {first_name}")
            first_name_inputs = self.driver.find_elements(By.CSS_SELECTOR, "input[id^='IdFirstName']")

            if len(first_name_inputs) <= passenger_index:
                logger.error(f"Passenger form {passenger_index + 1} not found (only {len(first_name_inputs)} forms)")
                return False

            first_name_field = first_name_inputs[passenger_index]
            self.driver.execute_script("arguments[0].scrollIntoView(true);", first_name_field)
            time.sleep(0.5)
            first_name_field.clear()
            first_name_field.send_keys(first_name)
            logger.info(f"  ✓ First name filled: {first_name}")

            # PASO 2: Llenar APELLIDO
            logger.info(f"  2. Filling last name: {last_name}")
            last_name_inputs = self.driver.find_elements(By.CSS_SELECTOR, "input[id^='IdLastName']")
            if len(last_name_inputs) > passenger_index:
                last_name_field = last_name_inputs[passenger_index]
                last_name_field.clear()
                last_name_field.send_keys(last_name)
                logger.info(f"  ✓ Last name filled: {last_name}")

            # PASO 3: Seleccionar GÉNERO (Dropdown)
            logger.info(f"  3. Selecting gender: {gender}")
            try:
                gender_buttons = self.driver.find_elements(By.CSS_SELECTOR, "button[id^='IdPaxGender_']")
                if len(gender_buttons) > passenger_index:
                    gender_button = gender_buttons[passenger_index]
                    self.driver.execute_script("arguments[0].scrollIntoView(true);", gender_button)
                    time.sleep(0.5)
                    self.driver.execute_script("arguments[0].click();", gender_button)
                    time.sleep(1)

                    # IMPORTANTE: Buscar la opción en el dropdown abierto más cercano
                    # Usar un selector que busque spans visibles (del dropdown abierto actual)
                    gender_text = "Masculino" if gender == "M" else "Femenino"

                    # Buscar todas las opciones visibles y seleccionar la primera (del dropdown actual)
                    all_gender_options = self.driver.find_elements(By.XPATH, f"//span[text()='{gender_text}' and ancestor::div[contains(@class, 'ng-dropdown-panel') and contains(@style, 'display') and not(contains(@style, 'none'))]]")

                    if not all_gender_options:
                        # Fallback: buscar sin restricción de visibilidad
                        all_gender_options = self.driver.find_elements(By.XPATH, f"//span[text()='{gender_text}']")

                    if all_gender_options:
                        gender_option = all_gender_options[0]  # Primera opción visible (del dropdown abierto)
                        self.driver.execute_script("arguments[0].click();", gender_option)
                        logger.info(f"  ✓ Gender selected: {gender_text}")
                        time.sleep(0.5)
                    else:
                        logger.warning(f"  Could not find gender option: {gender_text}")
            except Exception as e:
                logger.warning(f"  Could not select gender: {e}")

            # PASO 4: Seleccionar FECHA DE NACIMIENTO (3 dropdowns: AÑO primero, luego MES, luego DÍA)
            # IMPORTANTE: El orden es crítico porque el sistema valida en tiempo real
            # Si seleccionamos Día→Mes→Año, podría crear una fecha inválida temporalmente
            # Al seleccionar Año→Mes→Día, el sistema filtra dinámicamente las opciones válidas
            logger.info(f"  4. Filling birth date: {birth_date} (Order: Year → Month → Day)")
            try:
                # Parsear fecha YYYY-MM-DD
                year, month, day = birth_date.split("-")
                year = int(year)
                month = int(month)
                day = int(day)

                # Nombres de meses en español
                month_names = ["Enero", "Febrero", "Marzo", "Abril", "Mayo", "Junio",
                             "Julio", "Agosto", "Septiembre", "Octubre", "Noviembre", "Diciembre"]
                month_name = month_names[month - 1]

                # A) Seleccionar AÑO PRIMERO (más importante para validación)
                year_buttons = self.driver.find_elements(By.CSS_SELECTOR, "button[id^='dateYearId_IdDateOfBirthHidden_']")
                if len(year_buttons) > passenger_index:
                    year_button = year_buttons[passenger_index]
                    self.driver.execute_script("arguments[0].scrollIntoView(true);", year_button)
                    time.sleep(1)

                    # Click en el botón para abrir dropdown
                    self.driver.execute_script("arguments[0].click();", year_button)
                    logger.info(f"  → Year dropdown opened")
                    time.sleep(2)  # Esperar a que el dropdown se abra completamente

                    # IMPORTANT FIX: Search within visible dropdown panel only
                    # Buscar opciones solo en el panel visible (no en toda la página)
                    all_year_options = self.driver.find_elements(By.XPATH,
                        f"//span[text()='{year}' and ancestor::div[contains(@class, 'ng-dropdown-panel') and contains(@style, 'display') and not(contains(@style, 'none'))]]")

                    if not all_year_options:
                        # Fallback: buscar sin restricción de visibilidad
                        all_year_options = self.driver.find_elements(By.XPATH, f"//span[text()='{year}']")

                    if all_year_options:
                        year_option = all_year_options[0]  # First visible option (from current dropdown)
                        self.driver.execute_script("arguments[0].click();", year_option)
                        logger.info(f"  ✓ Year selected FIRST: {year}")
                    else:
                        logger.warning(f"  ✗ Year {year} not found in dropdown")

                    time.sleep(2)  # IMPORTANTE: Esperar más tiempo para que el sistema filtre meses válidos

                # B) Seleccionar MES SEGUNDO (filtrado según año)
                month_buttons = self.driver.find_elements(By.CSS_SELECTOR, "button[id^='dateMonthId_IdDateOfBirthHidden_']")
                if len(month_buttons) > passenger_index:
                    month_button = month_buttons[passenger_index]
                    self.driver.execute_script("arguments[0].scrollIntoView(true);", month_button)
                    time.sleep(1)

                    # Click en el botón para abrir dropdown
                    self.driver.execute_script("arguments[0].click();", month_button)
                    logger.info(f"  → Month dropdown opened")
                    time.sleep(2)  # Esperar a que el dropdown se abra completamente

                    # IMPORTANT FIX: Search within visible dropdown panel only
                    # Buscar opciones solo en el panel visible (no en toda la página)
                    all_month_options = self.driver.find_elements(By.XPATH,
                        f"//span[text()='{month_name}' and ancestor::div[contains(@class, 'ng-dropdown-panel') and contains(@style, 'display') and not(contains(@style, 'none'))]]")

                    if not all_month_options:
                        # Fallback: buscar sin restricción de visibilidad
                        all_month_options = self.driver.find_elements(By.XPATH, f"//span[text()='{month_name}']")

                    if all_month_options:
                        month_option = all_month_options[0]  # First visible option (from current dropdown)
                        self.driver.execute_script("arguments[0].click();", month_option)
                        logger.info(f"  ✓ Month selected SECOND: {month_name}")
                    else:
                        logger.warning(f"  ✗ Month {month_name} not found in dropdown")

                    time.sleep(2)  # IMPORTANTE: Esperar más tiempo para que el sistema filtre días válidos

                # C) Seleccionar DÍA TERCERO (filtrado según año+mes)
                day_buttons = self.driver.find_elements(By.CSS_SELECTOR, "button[id^='dateDayId_IdDateOfBirthHidden_']")
                if len(day_buttons) > passenger_index:
                    day_button = day_buttons[passenger_index]
                    self.driver.execute_script("arguments[0].scrollIntoView(true);", day_button)
                    time.sleep(1)

                    # Click en el botón para abrir dropdown
                    self.driver.execute_script("arguments[0].click();", day_button)
                    logger.info(f"  → Day dropdown opened")
                    time.sleep(2)  # Esperar a que el dropdown se abra completamente

                    # IMPORTANT FIX: Search within visible dropdown panel only
                    # Buscar opciones solo en el panel visible (no en toda la página)
                    all_day_options = self.driver.find_elements(By.XPATH,
                        f"//span[text()='{day}' and ancestor::div[contains(@class, 'ng-dropdown-panel') and contains(@style, 'display') and not(contains(@style, 'none'))]]")

                    if not all_day_options:
                        # Fallback: buscar sin restricción de visibilidad
                        all_day_options = self.driver.find_elements(By.XPATH, f"//span[text()='{day}']")

                    if all_day_options:
                        day_option = all_day_options[0]  # First visible option (from current dropdown)
                        self.driver.execute_script("arguments[0].click();", day_option)
                        logger.info(f"  ✓ Day selected THIRD: {day}")
                    else:
                        logger.warning(f"  ✗ Day {day} not found in dropdown")

                    time.sleep(1)

            except Exception as e:
                logger.warning(f"  Could not fill birth date: {e}")

            # PASO 5: Seleccionar NACIONALIDAD (Dropdown)
            logger.info(f"  5. Selecting nationality: {nationality}")
            try:
                nationality_buttons = self.driver.find_elements(By.CSS_SELECTOR, "button[id^='IdDocNationality_']")
                if len(nationality_buttons) > passenger_index:
                    nationality_button = nationality_buttons[passenger_index]
                    self.driver.execute_script("arguments[0].scrollIntoView(true);", nationality_button)
                    time.sleep(0.5)
                    self.driver.execute_script("arguments[0].click();", nationality_button)
                    logger.info(f"  → Nationality dropdown opened")
                    time.sleep(1)

                    # IMPORTANT FIX: Search within visible dropdown panel only
                    # Buscar opciones solo en el panel visible (no en toda la página)
                    all_nationality_options = self.driver.find_elements(By.XPATH,
                        f"//span[text()='{nationality}' and ancestor::div[contains(@class, 'ng-dropdown-panel') and contains(@style, 'display') and not(contains(@style, 'none'))]]")

                    if not all_nationality_options:
                        # Fallback: buscar sin restricción de visibilidad
                        all_nationality_options = self.driver.find_elements(By.XPATH, f"//span[text()='{nationality}']")

                    if all_nationality_options:
                        nationality_option = all_nationality_options[0]  # First visible option (from current dropdown)
                        self.driver.execute_script("arguments[0].click();", nationality_option)
                        logger.info(f"  ✓ Nationality selected: {nationality}")
                    else:
                        logger.warning(f"  ✗ Nationality {nationality} not found in dropdown")

                    time.sleep(0.5)
            except Exception as e:
                logger.warning(f"  Could not select nationality: {e}")

            logger.info(f"✓ Passenger {passenger_index + 1} ({passenger_type}) filled successfully")

            # PAUSA PARA VALIDACIÓN MANUAL - Con Screenshot
            logger.info(f"\n{'='*80}")
            logger.info(f"VALIDACIÓN MANUAL: Pasajero {passenger_index + 1} ({passenger_type})")
            logger.info(f"{'='*80}")
            logger.info(f"Por favor revisa el formulario del pasajero {passenger_index + 1} en la página.")
            logger.info(f"Datos esperados:")
            logger.info(f"  - Nombre: {first_name}")
            logger.info(f"  - Apellido: {last_name}")
            logger.info(f"  - Género: {gender}")
            logger.info(f"  - Fecha de nacimiento: {birth_date}")
            logger.info(f"  - Nacionalidad: {nationality}")

            # Tomar screenshot
            screenshot_name = f"reports/debug_passenger_{passenger_index+1}_{passenger_type}.png"
            self.driver.save_screenshot(screenshot_name)
            logger.info(f"📸 Screenshot guardado: {screenshot_name}")

            # Pausa larga para que el usuario pueda revisar
            # COMENTADO TEMPORALMENTE para pruebas rápidas
            # logger.info(f"⏸️  PAUSANDO 15 SEGUNDOS para revisión manual...")
            # time.sleep(15)
            logger.info(f"✓ Continuando con siguiente pasajero...")

            return True

        except Exception as e:
            logger.error(f"✗ Error filling passenger {passenger_index + 1}: {e}")
            import traceback
            traceback.print_exc()

            # PAUSA Y SCREENSHOT EN CASO DE ERROR
            logger.error(f"\n{'='*80}")
            logger.error(f"ERROR AL LLENAR PASAJERO {passenger_index + 1} ({passenger_type})")
            logger.error(f"{'='*80}")
            logger.error(f"Error: {e}")

            # Tomar screenshot del error
            error_screenshot = f"reports/ERROR_passenger_{passenger_index+1}_{passenger_type}.png"
            self.driver.save_screenshot(error_screenshot)
            logger.error(f"📸 Screenshot del error: {error_screenshot}")

            logger.error(f"⏸️  PAUSANDO 10 SEGUNDOS para revisar error...")
            time.sleep(10)

            return False

    def fill_all_passengers(self, passengers_data):
        """
        Llena la información de todos los pasajeros.

        Args:
            passengers_data (list): Lista de diccionarios con datos de pasajeros
                Cada diccionario debe contener: type, first_name, last_name, birth_date, gender, nationality

        Returns:
            bool: True si se llenaron todos correctamente
        """
        logger.info(f"Filling information for {len(passengers_data)} passengers...")

        all_success = True
        for index, passenger in enumerate(passengers_data):
            success = self.fill_passenger_info(
                passenger_index=index,
                passenger_type=passenger["type"],
                first_name=passenger["first_name"],
                last_name=passenger["last_name"],
                birth_date=passenger["birth_date"],
                gender=passenger.get("gender", "M"),
                nationality=passenger.get("nationality", "Colombia")
            )

            if not success:
                logger.warning(f"Failed to fill passenger {index + 1}")
                all_success = False

            time.sleep(1)  # Pausa entre pasajeros

        if all_success:
            logger.info("✓ All passengers filled successfully")
        else:
            logger.warning("Some passengers could not be filled")

        return all_success

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
            time.sleep(2)

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
                "//button[contains(@class, 'button-booking')]",
                "//button[contains(@class, 'btn-primary')]",
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
                    time.sleep(0.5)
                    self.driver.execute_script("arguments[0].click();", continue_btn)  # JavaScript click
                    logger.info("✓ Continue button clicked successfully")
                    time.sleep(3)
                    return True
                except:
                    continue

            logger.warning("Continue button not found with any selector")
            return False

        except Exception as e:
            logger.error(f"✗ Error clicking continue button: {e}")
            return False

    def get_page_screenshot(self, filename="passengers_page.png"):
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
