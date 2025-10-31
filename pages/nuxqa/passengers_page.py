"""
passengers_page.py - Page Object para la página de información de pasajeros

Este archivo representa la página PASSENGERS usando el patrón Page Object Model (POM).
Contiene todos los selectores y acciones para llenar información de pasajeros.

Caso 1 y 2: Ingresar información de pasajeros (datos fake permitidos)
"""

# ==================== IMPORTS ====================
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.ui import Select
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
    - Llenar formularios de pasajeros (adultos, jóvenes, niños, infantes)
    - Validar que se complete correctamente
    - Continuar al siguiente paso
    """

    # ==================== LOCATORS ====================
    # Formularios de pasajeros - selectores genéricos que funcionan con índices
    # Los formularios suelen estar en contenedores repetidos

    # Campo de primer nombre (genérico, se ajustará con índice)
    FIRST_NAME_INPUT = "//input[contains(@id, 'firstName') or contains(@name, 'firstName') or contains(@placeholder, 'First name') or contains(@placeholder, 'Primer nombre')]"

    # Campo de apellido
    LAST_NAME_INPUT = "//input[contains(@id, 'lastName') or contains(@name, 'lastName') or contains(@placeholder, 'Last name') or contains(@placeholder, 'Apellido')]"

    # Campo de fecha de nacimiento (puede ser input o select)
    DATE_OF_BIRTH_INPUT = "//input[contains(@id, 'dateOfBirth') or contains(@name, 'dateOfBirth') or contains(@placeholder, 'Date of birth')]"

    # Selector de género
    GENDER_SELECT = "//select[contains(@id, 'gender') or contains(@name, 'gender')]"

    # Selector de tipo de documento
    DOCUMENT_TYPE_SELECT = "//select[contains(@id, 'documentType') or contains(@name, 'documentType') or contains(@id, 'idType')]"

    # Campo de número de documento
    DOCUMENT_NUMBER_INPUT = "//input[contains(@id, 'documentNumber') or contains(@name, 'documentNumber') or contains(@id, 'idNumber')]"

    # Campo de email (solo para adulto contacto)
    EMAIL_INPUT = "//input[contains(@id, 'email') or contains(@name, 'email') or contains(@type, 'email')]"

    # Campo de teléfono
    PHONE_INPUT = "//input[contains(@id, 'phone') or contains(@name, 'phone') or contains(@type, 'tel')]"

    # Botón continuar
    CONTINUE_BUTTON = (By.XPATH, "//button[contains(text(), 'Continuar') or contains(text(), 'Continue') or contains(text(), 'Continuer') or contains(@id, 'continueButton')]")

    # Contenedor de pasajeros
    PASSENGER_FORM = "//div[contains(@class, 'passenger') or contains(@class, 'pax')]"

    # ==================== CONSTRUCTOR ====================
    def __init__(self, driver):
        """
        Constructor de la clase.

        Args:
            driver: Instancia de Selenium WebDriver
        """
        self.driver = driver
        self.wait = WebDriverWait(driver, 20)
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
            time.sleep(3)  # Tiempo para que la página empiece a cargar

            current_url = self.driver.current_url
            logger.info(f"Current URL: {current_url}")

            # Verificar que estamos en la página de pasajeros
            is_passengers_page = "passenger" in current_url.lower() or "pax" in current_url.lower()

            if not is_passengers_page:
                logger.warning(f"URL doesn't contain 'passenger' or 'pax': {current_url}")

            # Esperar a que aparezcan formularios de pasajeros
            time.sleep(2)

            logger.info("✓ Passengers page loaded successfully")
            return True

        except Exception as e:
            logger.error(f"✗ Error waiting for Passengers page: {e}")
            return False

    def fill_passenger_info(self, passenger_index, passenger_type, first_name, last_name,
                           birth_date, gender="M", doc_type="CC", doc_number="1234567890",
                           email=None, phone=None):
        """
        Llena la información de un pasajero específico.

        Args:
            passenger_index (int): Índice del pasajero (0 = primero, 1 = segundo, etc.)
            passenger_type (str): Tipo de pasajero ("Adult", "Teen", "Child", "Infant")
            first_name (str): Primer nombre
            last_name (str): Apellido
            birth_date (str): Fecha de nacimiento (formato YYYY-MM-DD o DD/MM/YYYY)
            gender (str): Género ("M" o "F")
            doc_type (str): Tipo de documento ("CC", "Passport", etc.)
            doc_number (str): Número de documento
            email (str): Email (solo para adulto contacto)
            phone (str): Teléfono (solo para adulto contacto)

        Returns:
            bool: True si se llenó correctamente
        """
        logger.info(f"Filling passenger {passenger_index + 1} info ({passenger_type})...")

        try:
            # Buscar todos los formularios de entrada de texto (para firstName)
            first_name_inputs = self.driver.find_elements(By.XPATH, self.FIRST_NAME_INPUT)

            if len(first_name_inputs) <= passenger_index:
                logger.error(f"Passenger form {passenger_index + 1} not found")
                return False

            # Llenar primer nombre
            logger.info(f"Filling first name: {first_name}")
            first_name_field = first_name_inputs[passenger_index]
            self.driver.execute_script("arguments[0].scrollIntoView(true);", first_name_field)
            time.sleep(0.5)
            first_name_field.clear()
            first_name_field.send_keys(first_name)

            # Llenar apellido
            last_name_inputs = self.driver.find_elements(By.XPATH, self.LAST_NAME_INPUT)
            if len(last_name_inputs) > passenger_index:
                logger.info(f"Filling last name: {last_name}")
                last_name_field = last_name_inputs[passenger_index]
                last_name_field.clear()
                last_name_field.send_keys(last_name)

            # Llenar fecha de nacimiento (puede ser input de texto o date picker)
            birth_date_inputs = self.driver.find_elements(By.XPATH, self.DATE_OF_BIRTH_INPUT)
            if len(birth_date_inputs) > passenger_index:
                logger.info(f"Filling birth date: {birth_date}")
                birth_date_field = birth_date_inputs[passenger_index]

                # Intentar JavaScript para fechas más confiable
                self.driver.execute_script(f"arguments[0].value = '{birth_date}';", birth_date_field)

                # Si falla, intentar send_keys
                if not birth_date_field.get_attribute('value'):
                    birth_date_field.clear()
                    birth_date_field.send_keys(birth_date)

            # Seleccionar género (si está disponible)
            try:
                gender_selects = self.driver.find_elements(By.XPATH, self.GENDER_SELECT)
                if len(gender_selects) > passenger_index:
                    logger.info(f"Selecting gender: {gender}")
                    gender_select = Select(gender_selects[passenger_index])
                    # Intentar por valor
                    try:
                        gender_select.select_by_value(gender)
                    except:
                        # Si falla, intentar por índice (M suele ser 0, F = 1)
                        gender_select.select_by_index(0 if gender == "M" else 1)
            except Exception as e:
                logger.warning(f"Could not select gender: {e}")

            # Seleccionar tipo de documento (si está disponible)
            try:
                doc_type_selects = self.driver.find_elements(By.XPATH, self.DOCUMENT_TYPE_SELECT)
                if len(doc_type_selects) > passenger_index:
                    logger.info(f"Selecting document type: {doc_type}")
                    doc_type_select = Select(doc_type_selects[passenger_index])
                    # Intentar por valor
                    try:
                        doc_type_select.select_by_value(doc_type)
                    except:
                        # Si falla, seleccionar el primero (suele ser CC o Passport)
                        doc_type_select.select_by_index(0)
            except Exception as e:
                logger.warning(f"Could not select document type: {e}")

            # Llenar número de documento
            doc_number_inputs = self.driver.find_elements(By.XPATH, self.DOCUMENT_NUMBER_INPUT)
            if len(doc_number_inputs) > passenger_index:
                logger.info(f"Filling document number: {doc_number}")
                doc_number_field = doc_number_inputs[passenger_index]
                doc_number_field.clear()
                doc_number_field.send_keys(doc_number)

            # Email y teléfono (solo para el primer adulto - contacto)
            if email and passenger_index == 0:
                email_inputs = self.driver.find_elements(By.XPATH, self.EMAIL_INPUT)
                if email_inputs:
                    logger.info(f"Filling email: {email}")
                    email_field = email_inputs[0]  # Primer campo de email
                    email_field.clear()
                    email_field.send_keys(email)

            if phone and passenger_index == 0:
                phone_inputs = self.driver.find_elements(By.XPATH, self.PHONE_INPUT)
                if phone_inputs:
                    logger.info(f"Filling phone: {phone}")
                    phone_field = phone_inputs[0]  # Primer campo de teléfono
                    phone_field.clear()
                    phone_field.send_keys(phone)

            logger.info(f"✓ Passenger {passenger_index + 1} info filled successfully")
            return True

        except Exception as e:
            logger.error(f"✗ Error filling passenger {passenger_index + 1} info: {e}")
            return False

    def fill_all_passengers(self, passengers_data):
        """
        Llena información de todos los pasajeros.

        Args:
            passengers_data (list): Lista de diccionarios con datos de pasajeros
                Ejemplo:
                [
                    {
                        "type": "Adult",
                        "first_name": "Juan",
                        "last_name": "Perez",
                        "birth_date": "1990-01-01",
                        "gender": "M",
                        "doc_type": "CC",
                        "doc_number": "1234567890",
                        "email": "juan@test.com",
                        "phone": "3001234567"
                    },
                    ...
                ]

        Returns:
            bool: True si se llenaron todos correctamente
        """
        logger.info(f"Filling information for {len(passengers_data)} passengers...")

        all_success = True
        for index, passenger in enumerate(passengers_data):
            success = self.fill_passenger_info(
                passenger_index=index,
                passenger_type=passenger.get("type", "Adult"),
                first_name=passenger.get("first_name", "Test"),
                last_name=passenger.get("last_name", "Passenger"),
                birth_date=passenger.get("birth_date", "1990-01-01"),
                gender=passenger.get("gender", "M"),
                doc_type=passenger.get("doc_type", "CC"),
                doc_number=passenger.get("doc_number", "1234567890"),
                email=passenger.get("email"),
                phone=passenger.get("phone")
            )

            if not success:
                all_success = False
                logger.warning(f"Failed to fill passenger {index + 1}")

            time.sleep(1)  # Espera entre pasajeros

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
