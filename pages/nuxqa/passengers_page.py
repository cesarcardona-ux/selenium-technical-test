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
            time.sleep(5)  # Esperar a que la página Angular se estabilice

            current_url = self.driver.current_url
            logger.info(f"Current URL: {current_url}")

            # Esperar a que aparezcan los campos de nombre (primero que se carga)
            try:
                first_name_inputs = self.wait.until(
                    EC.presence_of_all_elements_located((By.CSS_SELECTOR, "input[id^='IdFirstName']"))
                )
                logger.info(f"✓ Found {len(first_name_inputs)} passenger forms")
            except:
                logger.warning("Could not find passenger forms immediately, will retry later")

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

                    # Seleccionar opción según género
                    gender_text = "Masculino" if gender == "M" else "Femenino"
                    gender_option = self.driver.find_element(By.XPATH, f"//span[text()='{gender_text}']")
                    self.driver.execute_script("arguments[0].click();", gender_option)
                    logger.info(f"  ✓ Gender selected: {gender_text}")
                    time.sleep(0.5)
            except Exception as e:
                logger.warning(f"  Could not select gender: {e}")

            # PASO 4: Seleccionar FECHA DE NACIMIENTO (3 dropdowns: día, mes, año)
            logger.info(f"  4. Filling birth date: {birth_date}")
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

                # A) Seleccionar DÍA
                day_buttons = self.driver.find_elements(By.CSS_SELECTOR, "button[id^='dateDayId_IdDateOfBirthHidden_']")
                if len(day_buttons) > passenger_index:
                    day_button = day_buttons[passenger_index]
                    self.driver.execute_script("arguments[0].scrollIntoView(true);", day_button)
                    time.sleep(0.5)
                    self.driver.execute_script("arguments[0].click();", day_button)
                    time.sleep(1)

                    # Buscar día por texto
                    day_option = self.driver.find_element(By.XPATH, f"//span[text()='{day}']")
                    self.driver.execute_script("arguments[0].click();", day_option)
                    logger.info(f"  ✓ Day selected: {day}")
                    time.sleep(0.5)

                # B) Seleccionar MES
                month_buttons = self.driver.find_elements(By.CSS_SELECTOR, "button[id^='dateMonthId_IdDateOfBirthHidden_']")
                if len(month_buttons) > passenger_index:
                    month_button = month_buttons[passenger_index]
                    self.driver.execute_script("arguments[0].scrollIntoView(true);", month_button)
                    time.sleep(0.5)
                    self.driver.execute_script("arguments[0].click();", month_button)
                    time.sleep(1)

                    # Buscar mes por nombre
                    month_option = self.driver.find_element(By.XPATH, f"//span[text()='{month_name}']")
                    self.driver.execute_script("arguments[0].click();", month_option)
                    logger.info(f"  ✓ Month selected: {month_name}")
                    time.sleep(0.5)

                # C) Seleccionar AÑO
                year_buttons = self.driver.find_elements(By.CSS_SELECTOR, "button[id^='dateYearId_IdDateOfBirthHidden_']")
                if len(year_buttons) > passenger_index:
                    year_button = year_buttons[passenger_index]
                    self.driver.execute_script("arguments[0].scrollIntoView(true);", year_button)
                    time.sleep(0.5)
                    self.driver.execute_script("arguments[0].click();", year_button)
                    time.sleep(1)

                    # Buscar año por texto
                    year_option = self.driver.find_element(By.XPATH, f"//span[text()='{year}']")
                    self.driver.execute_script("arguments[0].click();", year_option)
                    logger.info(f"  ✓ Year selected: {year}")
                    time.sleep(0.5)

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
                    time.sleep(1)

                    # Buscar nacionalidad por texto
                    nationality_option = self.driver.find_element(By.XPATH, f"//span[text()='{nationality}']")
                    self.driver.execute_script("arguments[0].click();", nationality_option)
                    logger.info(f"  ✓ Nationality selected: {nationality}")
                    time.sleep(0.5)
            except Exception as e:
                logger.warning(f"  Could not select nationality: {e}")

            logger.info(f"✓ Passenger {passenger_index + 1} ({passenger_type}) filled successfully")
            return True

        except Exception as e:
            logger.error(f"✗ Error filling passenger {passenger_index + 1}: {e}")
            import traceback
            traceback.print_exc()
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

            # Buscar botón continuar con múltiples estrategias
            continue_selectors = [
                "//button[contains(text(), 'Continuar')]",
                "//button[contains(text(), 'Continue')]",
                "//button[contains(@class, 'button-booking')]",
                "//button[contains(@class, 'btn-primary')]",
            ]

            for selector in continue_selectors:
                try:
                    continue_btn = self.driver.find_element(By.XPATH, selector)
                    if continue_btn.is_displayed():
                        self.driver.execute_script("arguments[0].scrollIntoView(true);", continue_btn)
                        time.sleep(1)
                        self.driver.execute_script("arguments[0].click();", continue_btn)
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
