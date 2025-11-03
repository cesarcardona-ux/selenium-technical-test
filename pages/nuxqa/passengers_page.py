"""
passengers_page.py - Page Object para la página de información de pasajeros

Este archivo representa la página PASSENGERS usando el patrón Page Object Model (POM).
Contiene todos los selectores y acciones para llenar información de pasajeros.

Caso 1 y 2: Ingresar información de pasajeros (datos fake permitidos)

OPTIMIZACIÓN V3: Uso de prefijos fijos + índice + búsquedas directas por CSS Selector
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
    - Llenar formularios de pasajeros usando prefijos fijos + índice (OPTIMIZADO V3)
    - Validar que se complete correctamente
    - Continuar al siguiente paso
    """

    # ==================== CONSTRUCTOR ====================
    def __init__(self, driver):
        """
        Constructor de la clase.

        Args:
            driver: Instancia de Selenium WebDriver
        """
        self.driver = driver
        self.wait = WebDriverWait(driver, 25)
        logger.info("PassengersPage object initialized (OPTIMIZED V3 - Prefix + Index)")

    # ==================== MÉTODOS ====================

    def wait_for_page_load(self):
        """
        Espera a que la página de Passengers cargue completamente.

        Returns:
            bool: True si la página cargó correctamente
        """
        logger.info("Waiting for Passengers page to load...")

        try:
            time.sleep(3)

            current_url = self.driver.current_url
            logger.info(f"Current URL: {current_url}")

            # Esperar a que aparezcan los campos de nombre usando CSS Selector con prefijo
            try:
                logger.info("Waiting for passenger form fields...")
                wait_extended = WebDriverWait(self.driver, 30)
                first_name_inputs = wait_extended.until(
                    EC.presence_of_all_elements_located((By.CSS_SELECTOR, "input[id^='IdFirstName']"))
                )
                logger.info(f"✓ Found {len(first_name_inputs)} passenger forms")

                if len(first_name_inputs) == 0:
                    logger.error("No passenger forms found")
                    self.driver.save_screenshot("reports/debug_no_forms.png")
                    return False

            except Exception as e:
                logger.error(f"Could not find passenger forms: {e}")
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
        Llena la información de un pasajero usando prefijos fijos + índice (OPTIMIZADO V3).

        Args:
            passenger_index (int): Índice del pasajero (0-3)
            passenger_type (str): Tipo ("Adult", "Teen", "Child", "Infant")
            first_name (str): Nombre
            last_name (str): Apellido
            birth_date (str): Fecha (YYYY-MM-DD)
            gender (str): "M" o "F"
            nationality (str): Nacionalidad

        Returns:
            bool: True si se llenó correctamente
        """
        logger.info(f"Filling passenger {passenger_index + 1} ({passenger_type}): {first_name} {last_name}")

        try:
            # ==================== PASO 1: NOMBRE ====================
            logger.info(f"  1. Filling first name: {first_name}")
            first_name_inputs = self.driver.find_elements(By.CSS_SELECTOR, "input[id^='IdFirstName']")

            if len(first_name_inputs) <= passenger_index:
                logger.error(f"Passenger form {passenger_index + 1} not found")
                return False

            first_name_field = first_name_inputs[passenger_index]
            self.driver.execute_script("arguments[0].scrollIntoView(true);", first_name_field)
            time.sleep(0.2)
            first_name_field.clear()
            first_name_field.send_keys(first_name)
            logger.info(f"  ✓ First name filled: {first_name}")

            # ==================== PASO 2: APELLIDO ====================
            logger.info(f"  2. Filling last name: {last_name}")
            last_name_inputs = self.driver.find_elements(By.CSS_SELECTOR, "input[id^='IdLastName']")
            if len(last_name_inputs) > passenger_index:
                last_name_field = last_name_inputs[passenger_index]
                last_name_field.clear()
                last_name_field.send_keys(last_name)
                logger.info(f"  ✓ Last name filled: {last_name}")

            # ==================== PASO 3: GÉNERO ====================
            logger.info(f"  3. Selecting gender: {gender}")
            try:
                gender_buttons = self.driver.find_elements(By.CSS_SELECTOR, "button[id^='IdPaxGender_']")
                if len(gender_buttons) > passenger_index:
                    gender_button = gender_buttons[passenger_index]
                    self.driver.execute_script("arguments[0].scrollIntoView(true);", gender_button)
                    time.sleep(0.2)
                    self.driver.execute_script("arguments[0].click();", gender_button)
                    time.sleep(0.3)

                    # Obtener el ID del botón para construir el ID de la opción
                    gender_button_id = gender_button.get_attribute("id")
                    gender_suffix = "-0" if gender == "M" else "-1"
                    gender_option_id = f"{gender_button_id}{gender_suffix}"

                    try:
                        # Intentar encontrar la opción por ID directo
                        gender_option = self.driver.find_element(By.ID, gender_option_id)
                        self.driver.execute_script("arguments[0].click();", gender_option)
                        gender_text = "Masculino" if gender == "M" else "Femenino"
                        logger.info(f"  ✓ Gender selected: {gender_text}")
                    except:
                        logger.warning(f"  Could not find gender option with ID {gender_option_id}")

                    time.sleep(0.2)
            except Exception as e:
                logger.warning(f"  Could not select gender: {e}")

            # ==================== PASO 4: FECHA DE NACIMIENTO ====================
            logger.info(f"  4. Filling birth date: {birth_date} (Year → Month → Day)")
            try:
                year, month, day = birth_date.split("-")
                year, month, day = int(year), int(month), int(day)

                month_names = ["Enero", "Febrero", "Marzo", "Abril", "Mayo", "Junio",
                             "Julio", "Agosto", "Septiembre", "Octubre", "Noviembre", "Diciembre"]

                # A) AÑO
                logger.info(f"  → Selecting YEAR: {year}")
                year_buttons = self.driver.find_elements(By.CSS_SELECTOR, "button[id^='dateYearId_IdDateOfBirthHidden_']")
                if len(year_buttons) > passenger_index:
                    year_button = year_buttons[passenger_index]
                    year_button_id = year_button.get_attribute("id")

                    self.driver.execute_script("arguments[0].scrollIntoView(true);", year_button)
                    time.sleep(0.2)
                    self.driver.execute_script("arguments[0].click();", year_button)
                    time.sleep(0.3)

                    # Buscar año por CSS Selector (prefijo del ID + sufijo calculado)
                    # Intentar calcular sufijo basado en año
                    year_bases = {"Adult": 2010, "Infant": 2025, "Teen": 2013, "Child": 2023}
                    year_base = year_bases.get(passenger_type, 2010)
                    year_suffix = -(year_base - year)
                    year_option_id = f"{year_button_id}{year_suffix}"

                    try:
                        year_option = self.driver.find_element(By.ID, year_option_id)
                        self.driver.execute_script("arguments[0].click();", year_option)
                        logger.info(f"  ✓ Year selected: {year} (ID: {year_option_id})")
                    except:
                        logger.warning(f"  ✗ Year {year} not found with ID {year_option_id}")

                    time.sleep(0.2)

                # B) MES
                logger.info(f"  → Selecting MONTH: {month_names[month-1]}")
                month_buttons = self.driver.find_elements(By.CSS_SELECTOR, "button[id^='dateMonthId_IdDateOfBirthHidden_']")
                if len(month_buttons) > passenger_index:
                    month_button = month_buttons[passenger_index]
                    month_button_id = month_button.get_attribute("id")

                    self.driver.execute_script("arguments[0].scrollIntoView(true);", month_button)
                    time.sleep(0.2)
                    self.driver.execute_script("arguments[0].click();", month_button)
                    time.sleep(0.3)

                    # Calcular sufijo: -(mes - 1), pero forzar formato con guión
                    month_value = month - 1
                    month_option_id = f"{month_button_id}-{month_value}"

                    try:
                        month_option = self.driver.find_element(By.ID, month_option_id)
                        self.driver.execute_script("arguments[0].click();", month_option)
                        logger.info(f"  ✓ Month selected: {month_names[month-1]} (ID: {month_option_id})")
                    except:
                        logger.warning(f"  ✗ Month {month_names[month-1]} not found with ID {month_option_id}")

                    time.sleep(0.2)

                # C) DÍA
                logger.info(f"  → Selecting DAY: {day}")
                day_buttons = self.driver.find_elements(By.CSS_SELECTOR, "button[id^='dateDayId_IdDateOfBirthHidden_']")
                if len(day_buttons) > passenger_index:
                    day_button = day_buttons[passenger_index]
                    day_button_id = day_button.get_attribute("id")

                    self.driver.execute_script("arguments[0].scrollIntoView(true);", day_button)
                    time.sleep(0.2)
                    self.driver.execute_script("arguments[0].click();", day_button)
                    time.sleep(0.3)

                    day_suffix = -(day - 1)
                    day_option_id = f"{day_button_id}{day_suffix}"

                    try:
                        day_option = self.driver.find_element(By.ID, day_option_id)
                        self.driver.execute_script("arguments[0].click();", day_option)
                        logger.info(f"  ✓ Day selected: {day} (ID: {day_option_id})")
                    except:
                        logger.warning(f"  ✗ Day {day} not found with ID {day_option_id}")

                    time.sleep(0.2)

            except Exception as e:
                logger.warning(f"  Could not fill birth date: {e}")
                import traceback
                traceback.print_exc()

            # ==================== PASO 5: NACIONALIDAD ====================
            logger.info(f"  5. Selecting nationality: {nationality}")
            try:
                nationality_buttons = self.driver.find_elements(By.CSS_SELECTOR, "button[id^='IdDocNationality_']")
                if len(nationality_buttons) > passenger_index:
                    nationality_button = nationality_buttons[passenger_index]
                    nationality_button_id = nationality_button.get_attribute("id")

                    self.driver.execute_script("arguments[0].scrollIntoView(true);", nationality_button)
                    time.sleep(0.2)
                    self.driver.execute_script("arguments[0].click();", nationality_button)
                    time.sleep(0.3)

                    # Colombia siempre es -0
                    nationality_option_id = f"{nationality_button_id}-0"

                    try:
                        nationality_option = self.driver.find_element(By.ID, nationality_option_id)
                        self.driver.execute_script("arguments[0].click();", nationality_option)
                        logger.info(f"  ✓ Nationality selected: {nationality}")
                    except:
                        logger.warning(f"  ✗ Nationality not found with ID {nationality_option_id}")

                    time.sleep(0.2)
            except Exception as e:
                logger.warning(f"  Could not select nationality: {e}")

            logger.info(f"✓ Passenger {passenger_index + 1} ({passenger_type}) filled successfully")

            # Screenshot
            screenshot_name = f"reports/debug_passenger_{passenger_index+1}_{passenger_type}.png"
            self.driver.save_screenshot(screenshot_name)
            logger.info(f"📸 Screenshot: {screenshot_name}")

            return True

        except Exception as e:
            logger.error(f"✗ Error filling passenger {passenger_index + 1}: {e}")
            import traceback
            traceback.print_exc()

            error_screenshot = f"reports/ERROR_passenger_{passenger_index+1}_{passenger_type}.png"
            self.driver.save_screenshot(error_screenshot)
            logger.error(f"📸 Error screenshot: {error_screenshot}")

            return False

    def fill_all_passengers(self, passengers_data):
        """
        Llena la información de todos los pasajeros.

        Args:
            passengers_data (list): Lista de diccionarios con datos

        Returns:
            bool: True si se llenaron todos
        """
        logger.info(f"Filling {len(passengers_data)} passengers...")

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

            # Esperar más tiempo entre pasajeros para evitar browser crashes
            # Con 4 pasajeros y tantas operaciones DOM, el browser necesita tiempo para estabilizarse
            time.sleep(2)

        if all_success:
            logger.info("✓ All passengers filled successfully")
        else:
            logger.warning("Some passengers could not be filled")

        return all_success

    def fill_reservation_holder(self, email, phone):
        """
        Llena la información del Titular de la Reserva (Reservation Holder).

        Este contenedor aparece al final del formulario y contiene:
        - Selección de pasajero adulto (ya preseleccionado)
        - Prefijo de teléfono (Colombia +57)
        - Número de teléfono
        - Email
        - Confirmación de email
        - Checkbox de términos y condiciones

        Args:
            email (str): Email del titular
            phone (str): Teléfono del titular (10 dígitos)

        Returns:
            bool: True si se llenó correctamente
        """
        logger.info("Filling Reservation Holder information...")

        try:
            # Scroll hacia abajo para ver el contenedor
            self.driver.execute_script("window.scrollTo(0, document.body.scrollHeight * 0.9);")
            time.sleep(0.5)

            # PASO 1: SELECCIONAR PASAJERO (usualmente ya está preseleccionado el adulto)
            logger.info("  1. Checking passenger selection (Adult should be pre-selected)...")
            try:
                passenger_dropdown = self.driver.find_element(By.ID, "passengerId")
                logger.info("  ✓ Passenger dropdown found (Adult pre-selected)")
                # No necesitamos hacer nada, ya está seleccionado
            except:
                logger.warning("  ⚠ Passenger dropdown not found (may not be required)")

            # PASO 2: PREFIJO DE TELÉFONO (Colombia +57)
            logger.info("  2. Selecting phone prefix: Colombia (+57)...")
            try:
                phone_prefix_button = self.driver.find_element(By.ID, "phone_prefixPhoneId")
                self.driver.execute_script("arguments[0].scrollIntoView(true);", phone_prefix_button)
                time.sleep(0.2)
                self.driver.execute_script("arguments[0].click();", phone_prefix_button)
                time.sleep(0.3)

                # Seleccionar Colombia (primer item: -0)
                phone_prefix_option = self.driver.find_element(By.ID, "phone_prefixPhoneId-0")
                self.driver.execute_script("arguments[0].click();", phone_prefix_option)
                logger.info("  ✓ Phone prefix selected: Colombia (+57)")
                time.sleep(0.2)
            except Exception as e:
                logger.warning(f"  Could not select phone prefix: {e}")

            # PASO 3: NÚMERO DE TELÉFONO
            logger.info(f"  3. Filling phone number: {phone}...")
            try:
                phone_input = self.driver.find_element(By.ID, "phone_phoneNumberId")
                self.driver.execute_script("arguments[0].scrollIntoView(true);", phone_input)
                time.sleep(0.2)
                phone_input.clear()
                phone_input.send_keys(phone)
                logger.info(f"  ✓ Phone number filled: {phone}")
            except Exception as e:
                logger.warning(f"  Could not fill phone number: {e}")

            # PASO 4: EMAIL
            logger.info(f"  4. Filling email: {email}...")
            try:
                email_input = self.driver.find_element(By.ID, "email")
                self.driver.execute_script("arguments[0].scrollIntoView(true);", email_input)
                time.sleep(0.2)
                email_input.clear()
                email_input.send_keys(email)
                logger.info(f"  ✓ Email filled: {email}")
            except Exception as e:
                logger.warning(f"  Could not fill email: {e}")

            # PASO 5: CONFIRMAR EMAIL
            logger.info(f"  5. Confirming email: {email}...")
            try:
                confirm_email_input = self.driver.find_element(By.ID, "confirmEmail")
                self.driver.execute_script("arguments[0].scrollIntoView(true);", confirm_email_input)
                time.sleep(0.2)
                confirm_email_input.clear()
                confirm_email_input.send_keys(email)
                logger.info(f"  ✓ Email confirmed: {email}")
            except Exception as e:
                logger.warning(f"  Could not confirm email: {e}")

            # PASO 6: CHECKBOX DE TÉRMINOS
            logger.info("  6. Accepting terms and conditions...")
            try:
                checkbox = self.driver.find_element(By.ID, "sendNewsLetter")
                self.driver.execute_script("arguments[0].scrollIntoView(true);", checkbox)
                time.sleep(0.2)

                # Verificar si ya está seleccionado
                if not checkbox.is_selected():
                    self.driver.execute_script("arguments[0].click();", checkbox)
                    logger.info("  ✓ Terms and conditions accepted")
                else:
                    logger.info("  ✓ Terms already accepted")
            except Exception as e:
                logger.warning(f"  Could not accept terms: {e}")

            logger.info("✓ Reservation Holder information filled successfully")

            # Screenshot final
            screenshot_name = "reports/debug_reservation_holder.png"
            self.driver.save_screenshot(screenshot_name)
            logger.info(f"📸 Screenshot: {screenshot_name}")

            return True

        except Exception as e:
            logger.error(f"✗ Error filling Reservation Holder: {e}")
            import traceback
            traceback.print_exc()

            error_screenshot = "reports/ERROR_reservation_holder.png"
            self.driver.save_screenshot(error_screenshot)
            logger.error(f"📸 Error screenshot: {error_screenshot}")

            return False

    def click_continue(self):
        """
        Click en botón "Continuar".

        Returns:
            bool: True si exitoso
        """
        logger.info("Clicking continue button...")

        try:
            self.driver.execute_script("window.scrollTo(0, document.body.scrollHeight);")
            time.sleep(2)

            continue_selectors = [
                "//button[contains(@class, 'btn-next')]",
                "//button//span[contains(text(), 'Continuar')]",
                "//button//span[contains(text(), 'Continue')]",
                "//button[contains(text(), 'Continuar')]",
                "//button[contains(@class, 'button-booking')]",
            ]

            for selector in continue_selectors:
                try:
                    if "//span" in selector:
                        span_elem = self.driver.find_element(By.XPATH, selector)
                        continue_btn = span_elem.find_element(By.XPATH, "..")
                    else:
                        continue_btn = self.driver.find_element(By.XPATH, selector)

                    self.driver.execute_script("arguments[0].scrollIntoView(true);", continue_btn)
                    time.sleep(0.5)
                    self.driver.execute_script("arguments[0].click();", continue_btn)
                    logger.info("✓ Continue button clicked")
                    time.sleep(3)
                    return True
                except:
                    continue

            logger.warning("Continue button not found")
            return False

        except Exception as e:
            logger.error(f"✗ Error clicking continue: {e}")
            return False

    def get_page_screenshot(self, filename="passengers_page.png"):
        """
        Screenshot de la página.

        Args:
            filename: Nombre del archivo

        Returns:
            str: Path del screenshot
        """
        try:
            screenshot_path = f"reports/{filename}"
            self.driver.save_screenshot(screenshot_path)
            logger.info(f"Screenshot saved: {screenshot_path}")
            return screenshot_path
        except Exception as e:
            logger.error(f"Error taking screenshot: {e}")
            return None
