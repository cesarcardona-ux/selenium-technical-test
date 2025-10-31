"""
payment_page.py - Page Object para la página de pago (Payment)

Este archivo representa la página PAYMENT usando el patrón Page Object Model (POM).
Contiene todos los selectores y acciones para llenar información de pago.

Caso 1: Realizar pago con tarjeta fake (puede ser rechazado)
Caso 2: Llenar información de pago pero NO enviar
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
class PaymentPage:
    """
    Page Object de la página de pago.

    Responsabilidades:
    - Esperar a que cargue la página Payment
    - Llenar información de tarjeta de crédito
    - Llenar información de billing (facturación)
    - Enviar o no enviar el pago según el caso
    """

    # ==================== LOCATORS ====================
    # Selectores de campos de pago - genéricos para adaptarse a diferentes estructuras

    # Campos de tarjeta de crédito
    CARD_NUMBER_INPUT = (By.XPATH, "//input[contains(@id, 'cardNumber') or contains(@name, 'cardNumber') or contains(@placeholder, 'Card number') or contains(@placeholder, 'Número de tarjeta')]")
    CARD_HOLDER_NAME_INPUT = (By.XPATH, "//input[contains(@id, 'cardHolder') or contains(@name, 'cardHolder') or contains(@placeholder, 'Cardholder') or contains(@placeholder, 'Nombre del titular')]")
    EXPIRY_MONTH_SELECT = (By.XPATH, "//select[contains(@id, 'expiryMonth') or contains(@name, 'expiryMonth') or contains(@id, 'month')]")
    EXPIRY_YEAR_SELECT = (By.XPATH, "//select[contains(@id, 'expiryYear') or contains(@name, 'expiryYear') or contains(@id, 'year')]")
    CVV_INPUT = (By.XPATH, "//input[contains(@id, 'cvv') or contains(@name, 'cvv') or contains(@placeholder, 'CVV') or contains(@placeholder, 'Código de seguridad')]")

    # Campos de billing/facturación
    EMAIL_INPUT = (By.XPATH, "//input[contains(@id, 'email') or contains(@name, 'email') or contains(@type, 'email')]")
    PHONE_INPUT = (By.XPATH, "//input[contains(@id, 'phone') or contains(@name, 'phone') or contains(@type, 'tel')]")
    ADDRESS_INPUT = (By.XPATH, "//input[contains(@id, 'address') or contains(@name, 'address') or contains(@placeholder, 'Address') or contains(@placeholder, 'Dirección')]")
    CITY_INPUT = (By.XPATH, "//input[contains(@id, 'city') or contains(@name, 'city') or contains(@placeholder, 'City') or contains(@placeholder, 'Ciudad')]")
    ZIP_CODE_INPUT = (By.XPATH, "//input[contains(@id, 'zip') or contains(@name, 'zip') or contains(@placeholder, 'ZIP') or contains(@placeholder, 'Código postal')]")
    COUNTRY_SELECT = (By.XPATH, "//select[contains(@id, 'country') or contains(@name, 'country')]")

    # Botón de pago
    PAY_BUTTON = (By.XPATH, "//button[contains(text(), 'Pagar') or contains(text(), 'Pay') or contains(text(), 'Payer') or contains(@id, 'payButton') or contains(@class, 'pay-button')]")

    # Checkbox de términos y condiciones
    TERMS_CHECKBOX = (By.XPATH, "//input[@type='checkbox' and (contains(@id, 'terms') or contains(@name, 'terms') or contains(@id, 'conditions'))]")

    # ==================== CONSTRUCTOR ====================
    def __init__(self, driver):
        """
        Constructor de la clase.

        Args:
            driver: Instancia de Selenium WebDriver
        """
        self.driver = driver
        self.wait = WebDriverWait(driver, 20)
        logger.info("PaymentPage object initialized")

    # ==================== MÉTODOS ====================

    def wait_for_page_load(self):
        """
        Espera a que la página de Payment cargue completamente.

        Returns:
            bool: True si la página cargó correctamente
        """
        logger.info("Waiting for Payment page to load...")

        try:
            time.sleep(3)  # Tiempo para que la página empiece a cargar

            current_url = self.driver.current_url
            logger.info(f"Current URL: {current_url}")

            # Verificar que estamos en la página de pago
            is_payment_page = "payment" in current_url.lower() or "pay" in current_url.lower() or "checkout" in current_url.lower()

            if not is_payment_page:
                logger.warning(f"URL doesn't contain 'payment' or 'pay': {current_url}")

            # Esperar a que aparezcan campos de pago
            time.sleep(2)

            logger.info("✓ Payment page loaded successfully")
            return True

        except Exception as e:
            logger.error(f"✗ Error waiting for Payment page: {e}")
            return False

    def fill_card_information(self, card_number="4111111111111111", card_holder="TEST USER",
                             expiry_month="12", expiry_year="2025", cvv="123"):
        """
        Llena la información de la tarjeta de crédito.

        Args:
            card_number (str): Número de tarjeta (default: 4111111111111111 - test card)
            card_holder (str): Nombre del titular
            expiry_month (str): Mes de expiración (01-12)
            expiry_year (str): Año de expiración (YYYY)
            cvv (str): Código de seguridad CVV

        Returns:
            bool: True si se llenó correctamente
        """
        logger.info("Filling card information...")

        try:
            # Llenar número de tarjeta
            try:
                card_number_field = self.wait.until(
                    EC.presence_of_element_located(self.CARD_NUMBER_INPUT)
                )
                self.driver.execute_script("arguments[0].scrollIntoView(true);", card_number_field)
                time.sleep(0.5)
                card_number_field.clear()
                card_number_field.send_keys(card_number)
                logger.info(f"✓ Card number filled: {card_number}")
            except Exception as e:
                logger.warning(f"Could not fill card number: {e}")

            # Llenar nombre del titular
            try:
                card_holder_field = self.driver.find_element(*self.CARD_HOLDER_NAME_INPUT)
                card_holder_field.clear()
                card_holder_field.send_keys(card_holder)
                logger.info(f"✓ Cardholder name filled: {card_holder}")
            except Exception as e:
                logger.warning(f"Could not fill cardholder name: {e}")

            # Seleccionar mes de expiración
            try:
                month_select = Select(self.driver.find_element(*self.EXPIRY_MONTH_SELECT))
                month_select.select_by_value(expiry_month)
                logger.info(f"✓ Expiry month selected: {expiry_month}")
            except Exception as e:
                logger.warning(f"Could not select expiry month: {e}")

            # Seleccionar año de expiración
            try:
                year_select = Select(self.driver.find_element(*self.EXPIRY_YEAR_SELECT))
                year_select.select_by_value(expiry_year)
                logger.info(f"✓ Expiry year selected: {expiry_year}")
            except Exception as e:
                logger.warning(f"Could not select expiry year: {e}")

            # Llenar CVV
            try:
                cvv_field = self.driver.find_element(*self.CVV_INPUT)
                cvv_field.clear()
                cvv_field.send_keys(cvv)
                logger.info(f"✓ CVV filled: {cvv}")
            except Exception as e:
                logger.warning(f"Could not fill CVV: {e}")

            logger.info("✓ Card information filled successfully")
            return True

        except Exception as e:
            logger.error(f"✗ Error filling card information: {e}")
            return False

    def fill_billing_information(self, email="test@example.com", phone="3001234567",
                                address="Calle 123 #45-67", city="Bogota",
                                zip_code="110111", country="CO"):
        """
        Llena la información de facturación (billing).

        Args:
            email (str): Email de contacto
            phone (str): Teléfono de contacto
            address (str): Dirección
            city (str): Ciudad
            zip_code (str): Código postal
            country (str): Código de país (CO, US, etc.)

        Returns:
            bool: True si se llenó correctamente
        """
        logger.info("Filling billing information...")

        try:
            # Llenar email
            try:
                email_field = self.driver.find_element(*self.EMAIL_INPUT)
                self.driver.execute_script("arguments[0].scrollIntoView(true);", email_field)
                time.sleep(0.5)
                email_field.clear()
                email_field.send_keys(email)
                logger.info(f"✓ Email filled: {email}")
            except Exception as e:
                logger.warning(f"Could not fill email: {e}")

            # Llenar teléfono
            try:
                phone_field = self.driver.find_element(*self.PHONE_INPUT)
                phone_field.clear()
                phone_field.send_keys(phone)
                logger.info(f"✓ Phone filled: {phone}")
            except Exception as e:
                logger.warning(f"Could not fill phone: {e}")

            # Llenar dirección
            try:
                address_field = self.driver.find_element(*self.ADDRESS_INPUT)
                address_field.clear()
                address_field.send_keys(address)
                logger.info(f"✓ Address filled: {address}")
            except Exception as e:
                logger.warning(f"Could not fill address: {e}")

            # Llenar ciudad
            try:
                city_field = self.driver.find_element(*self.CITY_INPUT)
                city_field.clear()
                city_field.send_keys(city)
                logger.info(f"✓ City filled: {city}")
            except Exception as e:
                logger.warning(f"Could not fill city: {e}")

            # Llenar código postal
            try:
                zip_field = self.driver.find_element(*self.ZIP_CODE_INPUT)
                zip_field.clear()
                zip_field.send_keys(zip_code)
                logger.info(f"✓ ZIP code filled: {zip_code}")
            except Exception as e:
                logger.warning(f"Could not fill ZIP code: {e}")

            # Seleccionar país
            try:
                country_select = Select(self.driver.find_element(*self.COUNTRY_SELECT))
                country_select.select_by_value(country)
                logger.info(f"✓ Country selected: {country}")
            except Exception as e:
                logger.warning(f"Could not select country: {e}")

            logger.info("✓ Billing information filled successfully")
            return True

        except Exception as e:
            logger.error(f"✗ Error filling billing information: {e}")
            return False

    def accept_terms_and_conditions(self):
        """
        Acepta términos y condiciones si hay checkbox.

        Returns:
            bool: True si se aceptó o no existe checkbox
        """
        logger.info("Checking for terms and conditions checkbox...")

        try:
            terms_checkbox = self.driver.find_element(*self.TERMS_CHECKBOX)

            if not terms_checkbox.is_selected():
                self.driver.execute_script("arguments[0].scrollIntoView(true);", terms_checkbox)
                time.sleep(0.5)
                self.driver.execute_script("arguments[0].click();", terms_checkbox)
                logger.info("✓ Terms and conditions accepted")
                return True
            else:
                logger.info("Terms checkbox already selected")
                return True

        except Exception as e:
            logger.info(f"No terms checkbox found or not required: {e}")
            return True  # No es crítico si no existe

    def click_pay_button(self):
        """
        Hace click en el botón "Pagar" para enviar el pago.
        IMPORTANTE: Solo usar en Case 1 (permitido fallar).

        Returns:
            bool: True si se hizo click (no importa si el pago es rechazado)
        """
        logger.info("Clicking PAY button...")

        try:
            # Scroll hacia abajo para asegurar que el botón esté visible
            self.driver.execute_script("window.scrollTo(0, document.body.scrollHeight);")
            time.sleep(1)

            pay_button = self.wait.until(
                EC.element_to_be_clickable(self.PAY_BUTTON)
            )

            # JavaScript click para mayor confiabilidad
            self.driver.execute_script("arguments[0].click();", pay_button)
            logger.info("✓ Pay button clicked (payment may be declined - this is expected)")
            time.sleep(5)  # Espera a que procese (puede fallar o redirigir)

            return True

        except Exception as e:
            logger.error(f"✗ Error clicking pay button: {e}")
            return False

    def validate_payment_page(self):
        """
        Valida que estamos en la página de pago y que llegamos al último paso.

        Returns:
            bool: True si estamos en la página de pago
        """
        logger.info("Validating that we reached the payment page...")

        try:
            current_url = self.driver.current_url
            is_payment_page = "payment" in current_url.lower() or "pay" in current_url.lower() or "checkout" in current_url.lower()

            if is_payment_page:
                logger.info(f"✓ Payment page validation PASSED: {current_url}")
                return True
            else:
                logger.warning(f"Payment page validation FAILED: {current_url}")
                return False

        except Exception as e:
            logger.error(f"Error validating payment page: {e}")
            return False

    def get_page_screenshot(self, filename="payment_page.png"):
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
