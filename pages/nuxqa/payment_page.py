"""
payment_page.py - Page Object para la página de pago (Payment)

Este archivo representa la página PAYMENT usando el patrón Page Object Model (POM).
Contiene todos los selectores y acciones para llenar datos de tarjeta y facturación.

Caso 1: Llenar datos de tarjeta FAKE y datos de facturación, confirmar pago
"""

# ==================== IMPORTS ====================
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.keys import Keys
import logging
import time

# ==================== LOGGER ====================
logger = logging.getLogger(__name__)

# ==================== CLASE ====================
class PaymentPage:
    """
    Page Object de la página de pago (Payment).

    Responsabilidades:
    - Esperar a que cargue la página Payment
    - Llenar datos de tarjeta de crédito (FAKE)
    - Llenar datos de facturación
    - Aceptar términos y condiciones
    - Confirmar pago
    """

    # ==================== LOCATORS ====================

    # Datos de Tarjeta
    CARD_HOLDER_INPUT = (By.ID, "Holder")
    CARD_NUMBER_INPUT = (By.ID, "Data")
    CARD_MONTH_BUTTON = (By.ID, "expirationMonth_ExpirationDate")
    CARD_YEAR_BUTTON = (By.ID, "expirationYear_ExpirationDate")
    CARD_CVV_INPUT = (By.ID, "Cvv")

    # Datos de Facturación
    BILLING_EMAIL_INPUT = (By.ID, "email")
    BILLING_ADDRESS_INPUT = (By.ID, "address")
    BILLING_CITY_INPUT = (By.ID, "city")
    BILLING_COUNTRY_BUTTON = (By.ID, "country")

    # Términos
    TERMS_CHECKBOX = (By.ID, "terms")

    # Botón Final
    CONFIRM_PAYMENT_BUTTON = (By.XPATH, "//button[contains(@class, 'save-user-consent-confirmation')]")

    # ==================== CONSTRUCTOR ====================
    def __init__(self, driver):
        """
        Constructor de la clase.

        Args:
            driver: Instancia de Selenium WebDriver
        """
        self.driver = driver
        self.wait = WebDriverWait(driver, 25)
        logger.info("PaymentPage object initialized")

    # ==================== MÉTODOS ====================

    def wait_for_page_load(self):
        """
        Espera a que la página de Payment cargue completamente.
        Verifica que aparezca el formulario de tarjeta.

        IMPORTANTE: También detecta y acepta el modal de cookies si aparece.

        Returns:
            bool: True si la página cargó correctamente
        """
        logger.info("Waiting for Payment page to load...")

        try:
            # Esperar a que cambie la URL (reducido - página carga rápido)
            logger.info("Waiting 2 seconds for page navigation...")
            time.sleep(2)

            current_url = self.driver.current_url
            logger.info(f"Current URL: {current_url}")

            # Verificar si la URL contiene 'payment' o 'pay'
            if 'payment' not in current_url.lower() and 'pay' not in current_url.lower():
                logger.warning(f"URL doesn't seem to be a payment page: {current_url}")
                logger.info("Waiting extra time for navigation...")
                time.sleep(2)
                current_url = self.driver.current_url
                logger.info(f"URL after extra wait: {current_url}")

            # CRÍTICO: CAMBIO DE FLUJO - Aceptar cookies PRIMERO (aparecen inmediatamente)
            # ANTES: Esperábamos 13s → cookies → 8s
            # AHORA: cookies inmediato → esperar iframe
            # CRÍTICO: Detectar y aceptar modal de cookies si aparece
            # IMPORTANTE: El modal de OneTrust puede estar en un IFRAME separado o en el DOM principal
            logger.info("Checking for cookies consent modal (may be in iframe or main DOM)...")

            # 📸 Se CAPTURA (SELENIUM): Screenshot y HTML antes de manejar cookies
            try:
                debug_screenshot = f"reports/debug_payment_before_cookies_{int(time.time())}.png"
                self.driver.save_screenshot(debug_screenshot)
                logger.info(f"📸 Screenshot saved BEFORE cookies handling: {debug_screenshot}")

                # Guardar HTML completo para análisis
                html_source = self.driver.page_source
                with open(f"reports/debug_payment_html_{int(time.time())}.html", "w", encoding="utf-8") as f:
                    f.write(html_source)
                logger.info("📄 Page HTML saved for debugging")
            except:
                pass

            try:
                # ESTRATEGIA 1: Intentar buscar el botón directamente en el DOM principal
                logger.info("Strategy 1: Looking for cookies button in main DOM...")
                logger.info("  Waiting up to 10 seconds for button to be clickable...")
                try:
                    # ⏳ Se ESPERA (SELENIUM): Botón de cookies sea clickeable (max 10 segundos)
                    cookies_accept_button = WebDriverWait(self.driver, 10).until(
                        EC.element_to_be_clickable((By.ID, "onetrust-accept-btn-handler"))
                    )
                    logger.info("✓ Cookies button found in main DOM")

                    # 🖱️ Se PRESIONA (SELENIUM): Botón "Aceptar cookies" en modal OneTrust
                    self.driver.execute_script("arguments[0].scrollIntoView({behavior: 'auto', block: 'center'});", cookies_accept_button)
                    time.sleep(1)
                    cookies_accept_button.click()
                    # ⏳ Se ESPERA (SELENIUM): Modal de cookies se cierre
                    time.sleep(2)
                    logger.info("✓ Cookies accepted successfully (main DOM)")

                except Exception as e:
                    logger.info(f"Button not found in main DOM: {e}")

                    # ESTRATEGIA 2: Buscar en IFRAME de OneTrust
                    logger.info("Strategy 2: Looking for OneTrust iframe...")

                    # Posibles selectores de iframe de OneTrust
                    iframe_selectors = [
                        "//iframe[contains(@id, 'onetrust')]",
                        "//iframe[contains(@title, 'cookie')]",
                        "//iframe[contains(@title, 'Cookie')]",
                        "//iframe[contains(@name, 'onetrust')]",
                        "//iframe[contains(@class, 'onetrust')]",
                    ]

                    iframe_found = False
                    for iframe_selector in iframe_selectors:
                        try:
                            logger.info(f"  Trying iframe selector: {iframe_selector[:50]}...")
                            iframe = self.driver.find_element(By.XPATH, iframe_selector)

                            # Cambiar al contexto del iframe
                            self.driver.switch_to.frame(iframe)
                            logger.info(f"  ✓ Switched to iframe: {iframe_selector[:50]}")

                            # Buscar el botón DENTRO del iframe
                            logger.info("  Looking for cookies button inside iframe...")
                            cookies_accept_button = WebDriverWait(self.driver, 5).until(
                                EC.element_to_be_clickable((By.ID, "onetrust-accept-btn-handler"))
                            )
                            logger.info("  ✓ Cookies button found inside iframe")

                            # Click en el botón
                            cookies_accept_button.click()
                            time.sleep(2)
                            logger.info("  ✓ Cookies button clicked inside iframe")

                            # CRÍTICO: Volver al contexto principal
                            self.driver.switch_to.default_content()
                            logger.info("  ✓ Switched back to main content")

                            time.sleep(3)  # Esperar a que el modal desaparezca
                            logger.info("✓ Cookies accepted successfully (iframe)")
                            iframe_found = True
                            break

                        except Exception as iframe_error:
                            # Si falla, volver al contexto principal y seguir intentando
                            try:
                                self.driver.switch_to.default_content()
                            except:
                                pass
                            logger.debug(f"  Iframe selector failed: {str(iframe_error)[:80]}")
                            continue

                    if not iframe_found:
                        logger.warning("No iframe with cookies modal found")

            except Exception as e:
                # Si no hay modal de cookies, continuar normalmente
                logger.info(f"No cookies modal detected (or already accepted): {e}")
                # Asegurar que estamos en el contexto principal
                try:
                    self.driver.switch_to.default_content()
                except:
                    pass

            # CRÍTICO: Después de aceptar cookies, esperar a que Angular inyecte el iframe de payment
            # OPTIMIZACIÓN V2: Reducido de 10s → 6s (ahorro adicional de 4 segundos)
            # Total ahorro desde original: 13s+8s=21s → 6s = 15 segundos ahorrados
            # Razón: Ya aceptamos cookies inmediatamente, ahora Angular puede cargar el iframe
            logger.info("Waiting 6 seconds for Angular to inject payment iframe after cookies...")
            time.sleep(6)

            # CRÍTICO: Los campos de tarjeta (Holder, Data, CVV, etc.) están dentro de un IFRAME externo
            # de payment gateway (api-pay.avtest.ink). Necesitamos cambiar al contexto del iframe.
            logger.info("CRÍTICO: Card form fields are inside an external payment iframe")
            logger.info("Looking for payment iframe (class='payment-forms-layout_iframe')...")

            try:
                # Buscar el iframe de payment
                payment_iframe = WebDriverWait(self.driver, 30).until(
                    EC.presence_of_element_located((By.CLASS_NAME, "payment-forms-layout_iframe"))
                )
                logger.info("✓ Payment iframe found")

                # Cambiar al contexto del iframe
                self.driver.switch_to.frame(payment_iframe)
                logger.info("✓ Switched to payment iframe context")

                # Ahora buscar el input #Holder DENTRO del iframe
                logger.info("Looking for input #Holder inside payment iframe...")
                holder_wait = WebDriverWait(self.driver, 30)
                holder_wait.until(EC.visibility_of_element_located(self.CARD_HOLDER_INPUT))
                logger.info("✓ Input #Holder found inside payment iframe")

                # Verificar que sea interactable
                holder_input = self.driver.find_element(*self.CARD_HOLDER_INPUT)
                if holder_input.is_displayed() and holder_input.is_enabled():
                    logger.info("✓ Input #Holder is visible and enabled inside iframe")
                else:
                    logger.warning("Input #Holder found but may not be interactable")

            except Exception as iframe_error:
                logger.error(f"✗ Error finding payment iframe or card holder input: {iframe_error}")
                # Volver al contexto principal antes de fallar
                try:
                    self.driver.switch_to.default_content()
                except:
                    pass
                # Tomar screenshot de debugging
                try:
                    error_screenshot = f"reports/debug_iframe_not_found_{int(time.time())}.png"
                    self.driver.save_screenshot(error_screenshot)
                    logger.error(f"📸 Error screenshot saved: {error_screenshot}")
                except:
                    pass
                raise

            time.sleep(1)

            logger.info("✓ Payment page loaded successfully")
            return True

        except Exception as e:
            logger.error(f"✗ Error waiting for Payment page: {e}")
            logger.error(f"Final URL: {self.driver.current_url}")
            logger.error(f"Page title: {self.driver.title}")
            import traceback
            traceback.print_exc()
            return False

    def fill_credit_card_info(self, holder_name, card_number="4111111111111111", exp_month="12", exp_year="28", cvv="123"):
        """
        Llena los datos de la tarjeta de crédito DENTRO del iframe de payment.

        IMPORTANTE: Este método asume que YA estamos en el contexto del iframe de payment.
        El método wait_for_page_load() ya cambió al contexto del iframe.

        Args:
            holder_name (str): Nombre del titular (del adulto)
            card_number (str): Número de tarjeta (default: Visa de testing)
            exp_month (str): Mes de expiración (default: 12)
            exp_year (str): Año de expiración (default: 28)
            cvv (str): Código CVV (default: 123)

        Returns:
            bool: True si se llenó correctamente
        """
        logger.info("Filling credit card information INSIDE payment iframe...")

        try:
            # PASO 1: Nombre del titular
            logger.info(f"  1. Card Holder: {holder_name}...")
            # 🔍 Se BUSCA (SELENIUM): Campo de nombre del titular de tarjeta
            holder_input = self.wait.until(EC.presence_of_element_located(self.CARD_HOLDER_INPUT))
            holder_input.clear()
            # ⌨️ Se INGRESA (SELENIUM): Nombre del titular de la tarjeta
            holder_input.send_keys(holder_name)
            logger.info(f"  ✓ Card holder filled: {holder_name}")

            # PASO 2: Número de tarjeta
            logger.info(f"  2. Card Number: {card_number}...")
            # 🔍 Se BUSCA (SELENIUM): Campo de número de tarjeta
            card_input = self.driver.find_element(*self.CARD_NUMBER_INPUT)
            card_input.clear()
            # ⌨️ Se INGRESA (SELENIUM): Número de tarjeta de prueba
            card_input.send_keys(card_number)
            logger.info(f"  ✓ Card number filled: {card_number}")

            # PASO 3: Mes de expiración
            logger.info(f"  3. Expiration Month: {exp_month}...")
            # 🖱️ Se PRESIONA (SELENIUM): Botón para abrir dropdown de mes de expiración
            month_button = self.driver.find_element(*self.CARD_MONTH_BUTTON)
            self.driver.execute_script("arguments[0].click();", month_button)
            time.sleep(0.3)

            # 🖱️ Se PRESIONA (SELENIUM): Mes de expiración específico
            month_option_id = f"expirationMonth_ExpirationDate-{exp_month}"
            month_option = self.driver.find_element(By.ID, month_option_id)
            self.driver.execute_script("arguments[0].click();", month_option)
            logger.info(f"  ✓ Expiration month selected: {exp_month}")

            # PASO 4: Año de expiración
            logger.info(f"  4. Expiration Year: {exp_year}...")
            # 🖱️ Se PRESIONA (SELENIUM): Botón para abrir dropdown de año de expiración
            year_button = self.driver.find_element(*self.CARD_YEAR_BUTTON)
            self.driver.execute_script("arguments[0].click();", year_button)
            time.sleep(0.3)

            # 🖱️ Se PRESIONA (SELENIUM): Año de expiración específico
            year_option_id = f"expirationYear_ExpirationDate-{exp_year}"
            year_option = self.driver.find_element(By.ID, year_option_id)
            self.driver.execute_script("arguments[0].click();", year_option)
            logger.info(f"  ✓ Expiration year selected: {exp_year}")

            # PASO 5: CVV
            logger.info(f"  5. CVV: {cvv}...")
            cvv_input = self.driver.find_element(*self.CARD_CVV_INPUT)
            cvv_input.clear()
            cvv_input.send_keys(cvv)
            logger.info(f"  ✓ CVV filled: {cvv}")

            logger.info("✓ Credit card information filled successfully (inside iframe)")

            # CRÍTICO: Volver al contexto principal del DOM
            # Los campos de facturación (email, address, city, country) están en el DOM principal, NO en el iframe
            self.driver.switch_to.default_content()
            logger.info("✓ Switched back to main DOM context (out of payment iframe)")

            time.sleep(0.5)
            return True

        except Exception as e:
            logger.error(f"✗ Error filling credit card info: {e}")
            import traceback
            traceback.print_exc()
            return False

    def fill_billing_info(self, email, address="Calle Fake 123", city="Bogotá", country_text="colo"):
        """
        Llena los datos de facturación EN EL DOM PRINCIPAL (no en iframe).

        IMPORTANTE: Este método asume que ya salimos del iframe de payment y estamos en el contexto principal.
        Los campos email, address, city, country están en el DOM principal de Payment page.

        Args:
            email (str): Email del titular (del Reservation Holder)
            address (str): Dirección de residencia (default: fake)
            city (str): Ciudad (default: Bogotá)
            country_text (str): Texto para buscar país (default: "colo" para Colombia)

        Returns:
            bool: True si se llenó correctamente
        """
        logger.info("Filling billing information IN MAIN DOM (outside payment iframe)...")

        try:
            # Scroll hacia abajo para ver formulario de facturación
            self.driver.execute_script("window.scrollTo(0, document.body.scrollHeight * 0.7);")
            time.sleep(0.3)

            # PASO 1: Email
            logger.info(f"  1. Email: {email}...")
            email_input = self.wait.until(EC.presence_of_element_located(self.BILLING_EMAIL_INPUT))
            email_input.clear()
            email_input.send_keys(email)
            logger.info(f"  ✓ Email filled: {email}")

            # PASO 2: Address
            logger.info(f"  2. Address: {address}...")
            address_input = self.driver.find_element(*self.BILLING_ADDRESS_INPUT)
            address_input.clear()
            address_input.send_keys(address)
            logger.info(f"  ✓ Address filled: {address}")

            # PASO 3: City
            logger.info(f"  3. City: {city}...")
            city_input = self.driver.find_element(*self.BILLING_CITY_INPUT)
            city_input.clear()
            city_input.send_keys(city)
            logger.info(f"  ✓ City filled: {city}")

            # PASO 4: Country (Colombia)
            logger.info(f"  4. Country: Colombia (searching with '{country_text}')...")
            country_button = self.driver.find_element(*self.BILLING_COUNTRY_BUTTON)
            self.driver.execute_script("arguments[0].click();", country_button)
            time.sleep(0.3)

            # Escribir "colo" para buscar Colombia
            country_button.send_keys(country_text)
            time.sleep(0.5)

            # Seleccionar Colombia (aparece como opción filtrada)
            # XPath: //button[@role='option' and contains(., 'Colombia')]
            colombia_option = self.wait.until(
                EC.presence_of_element_located((By.XPATH, "//button[@role='option' and contains(., 'Colombia')]"))
            )
            self.driver.execute_script("arguments[0].click();", colombia_option)
            logger.info("  ✓ Country selected: Colombia")

            logger.info("✓ Billing information filled successfully")
            time.sleep(0.5)
            return True

        except Exception as e:
            logger.error(f"✗ Error filling billing info: {e}")
            import traceback
            traceback.print_exc()
            return False

    def accept_terms(self):
        """
        Marca el checkbox de términos y condiciones.

        Returns:
            bool: True si se marcó correctamente
        """
        logger.info("Accepting terms and conditions...")

        try:
            # Scroll hacia abajo para ver el checkbox
            self.driver.execute_script("window.scrollTo(0, document.body.scrollHeight * 0.9);")
            time.sleep(0.3)

            terms_checkbox = self.wait.until(EC.presence_of_element_located(self.TERMS_CHECKBOX))

            # Verificar si ya está seleccionado
            if not terms_checkbox.is_selected():
                self.driver.execute_script("arguments[0].click();", terms_checkbox)
                logger.info("✓ Terms and conditions accepted")
            else:
                logger.info("✓ Terms already accepted")

            time.sleep(0.5)
            return True

        except Exception as e:
            logger.error(f"✗ Error accepting terms: {e}")
            return False

    def click_confirm_payment(self):
        """
        Hace click en el botón "Confirmar y pagar".
        Este es el paso FINAL del test Case 1.

        Returns:
            bool: True si se hizo click correctamente
        """
        logger.info("Clicking 'Confirmar y pagar' button...")

        try:
            # Scroll hacia abajo para ver el botón
            self.driver.execute_script("window.scrollTo(0, document.body.scrollHeight);")
            time.sleep(0.5)

            confirm_btn = self.wait.until(EC.presence_of_element_located(self.CONFIRM_PAYMENT_BUTTON))

            # Click usando JavaScript
            self.driver.execute_script("arguments[0].click();", confirm_btn)
            logger.info("✓ 'Confirmar y pagar' button clicked successfully")

            time.sleep(2)  # Esperar a que se procese el pago (reducido de 3s a 2s)
            return True

        except Exception as e:
            logger.error(f"✗ Error clicking 'Confirmar y pagar': {e}")
            return False

    def complete_payment_flow(self, card_holder_name, email):
        """
        Completa todo el flujo de pago en un solo método.

        Flujo:
        1. Llenar datos de tarjeta (FAKE)
        2. Llenar datos de facturación
        3. Aceptar términos
        4. Confirmar pago

        Args:
            card_holder_name (str): Nombre del titular (adulto)
            email (str): Email del Reservation Holder

        Returns:
            bool: True si se completó todo correctamente
        """
        logger.info("Starting complete payment flow...")

        try:
            # Paso 1: Tarjeta
            card_filled = self.fill_credit_card_info(card_holder_name)
            if not card_filled:
                logger.error("Failed to fill credit card info")
                return False

            # Paso 2: Facturación
            billing_filled = self.fill_billing_info(email)
            if not billing_filled:
                logger.error("Failed to fill billing info")
                return False

            # Paso 3: Términos
            terms_accepted = self.accept_terms()
            if not terms_accepted:
                logger.error("Failed to accept terms")
                return False

            # Paso 4: Confirmar pago
            payment_confirmed = self.click_confirm_payment()
            if not payment_confirmed:
                logger.error("Failed to confirm payment")
                return False

            logger.info("✓ Payment flow completed successfully")
            return True

        except Exception as e:
            logger.error(f"✗ Error in payment flow: {e}")
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
