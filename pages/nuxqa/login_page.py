"""
login_page.py - Page Object para la página de login de nuxqa

Este archivo representa la página de LOGIN usando el patrón Page Object Model (POM).
Contiene todos los selectores (locators) y acciones relacionadas con el proceso de login.

Caso 3: Login y captura de Network (Session event)
- Ambiente: UAT1 (nuxqa.avtest.ink)
- Credenciales: Username: 21734198706, Password: Lifemiles1
- Configuración: Idioma Francés, POS France

HERENCIA: Esta clase hereda de HomePage para reutilizar métodos ya probados
de configuración de idioma y POS.
"""

# ==================== IMPORTS ====================
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import logging
import time
from pages.nuxqa.home_page import HomePage  # Importar HomePage para heredar

# ==================== LOGGER ====================
# Requisito técnico del PDF: logs detallados
logger = logging.getLogger(__name__)  # __name__ = 'pages.nuxqa.login_page'

# ==================== CLASE ====================
class LoginPage(HomePage):
    """
    Page Object de la página de login de nuxqa.

    HEREDA de HomePage para reutilizar métodos de:
    - Configuración de idioma (select_language)
    - Configuración de POS (select_pos_by_name)
    - Navegación (open)

    Responsabilidades ADICIONALES:
    - Almacenar locators del formulario de login
    - Proveer métodos para iniciar sesión
    - Validar estado de login
    - Registrar logs de cada acción (requisito del PDF)
    """

    # ==================== LOCATORS (Selectores XPath) ====================
    # Se definen como constantes en MAYÚSCULAS (convención Python)
    # Formato: tupla (By.XPATH, "xpath_string") o (By.ID, "id_string")

    # NOTA: Los locators de idioma y POS se heredan de HomePage

    # ==================== SEARCH FORM LOCATORS (Case 3) ====================
    # Tipo de viaje
    TRIP_TYPE_ROUND_TRIP = (By.XPATH, "//span[@class='label_text' and contains(text(), 'Aller-retour')]")
    TRIP_TYPE_ONE_WAY = (By.XPATH, "//span[@class='label_text' and contains(text(), 'Aller simple')]")

    # Origen (aeropuerto de salida)
    ORIGIN_BUTTON = (By.ID, "originBtn")
    ORIGIN_INPUT = (By.ID, "departureStationInputId")

    # Destino (aeropuerto de llegada)
    DESTINATION_BUTTON = (By.XPATH, "//input[@id='arrivalStationInputId']")
    DESTINATION_INPUT = (By.ID, "arrivalStationInputId")

    # Lista de aeropuertos (autocomplete)
    # El ID es dinámico: BOG, MAD, etc.
    # Se construirá dinámicamente en el método

    # Fechas (calendar)
    # Se construirán dinámicamente basados en el día

    # Pasajeros
    PASSENGERS_BUTTON = (By.XPATH, "//button[@class='control_field_button' and contains(@aria-label, 'Passagers')]")
    PASSENGERS_CONFIRM_BUTTON = (By.XPATH, "//button[contains(@class, 'control_options_selector_action_button')]//span[contains(text(), 'Confirmer')]")

    # Botones "+" y "-" para pasajeros (por posición en el modal)
    # Nota: El modal de pasajeros se carga dinámicamente, por lo que usamos los IDs de los inputs
    # y buscamos los botones relativos a ellos
    PASSENGER_INPUT_ADT = (By.ID, "inputPax_ADT")
    PASSENGER_INPUT_TNG = (By.ID, "inputPax_TNG")
    PASSENGER_INPUT_CHD = (By.ID, "inputPax_CHD")
    PASSENGER_INPUT_INF = (By.ID, "inputPax_INF")

    # Botón Buscar
    SEARCH_BUTTON = (By.ID, "searchButton")

    # ==================== CONSTRUCTOR ====================
    def __init__(self, driver):
        """
        Constructor de la clase.

        Args:
            driver: Instancia de Selenium WebDriver (recibida desde el test)

        NOTA: Llama al constructor de HomePage para heredar su inicialización
        """
        super().__init__(driver)  # Llama al constructor de HomePage
        self.wait = WebDriverWait(driver, 10)  # Wait de 10 segundos para elementos del login
        logger.info("LoginPage object initialized (inherits from HomePage)")

    # ==================== MÉTODOS ESPECÍFICOS DE LOGIN ====================
    # Los métodos de idioma y POS se heredan de HomePage:
    # - open(url)
    # - select_language(language_name)
    # - click_pos_button() - abre el modal de POS
    # - select_pos(pos_name) - selecciona el POS (requiere modal abierto)

    def configure_pos(self, pos_name):
        """
        Método completo para configurar POS que abre el modal primero.

        Args:
            pos_name: Nombre del POS (ej: "France", "Chile", "España")

        Este método es un wrapper que:
        1. Abre el modal de POS usando click_pos_button() (heredado)
        2. Selecciona el POS usando select_pos() (heredado)

        Diferencia con select_pos():
        - select_pos() solo busca el elemento (asume que el modal ya está abierto)
        - configure_pos() abre el modal primero y luego selecciona
        """
        logger.info(f"Configuring POS: {pos_name}")
        self.click_pos_button()  # Abre el modal (método heredado de HomePage)
        time.sleep(1)  # Espera a que se abra completamente el modal
        self.select_pos(pos_name)  # Selecciona el POS (método heredado de HomePage)
        logger.info(f"POS '{pos_name}' configured successfully")

    def select_trip_type(self, trip_type="one-way"):
        """
        Selecciona el tipo de viaje (One-way o Round-trip).

        IMPORTANTE: Este método es OPCIONAL. Si no se llama, el comportamiento por defecto
        de la página web se mantendrá (generalmente Round-trip está seleccionado).

        Args:
            trip_type (str): Tipo de viaje - "one-way" o "round-trip" (default: "one-way")

        Returns:
            bool: True si se seleccionó correctamente

        Nota:
        - Este método funciona con CUALQUIER idioma usando selectores por posición
        - NO afecta tests existentes si no se llama explícitamente
        - Es seguro llamarlo múltiples veces
        """
        logger.info(f"Selecting trip type: {trip_type}")

        try:
            # Selectores por ID exactos de nuxqa4/nuxqa5 (obtenidos de DevTools)
            # Estructura HTML:
            # - Round-trip: <input id="journeytypeId_0" name="journeyTypeSelector" type="radio">
            # - One-way: <input id="journeytypeId_1" name="journeyTypeSelector" type="radio">

            if trip_type.lower() == "one-way":
                # Selector por ID específico: journeytypeId_1 = Solo ida
                one_way_radio = self.wait.until(
                    EC.presence_of_element_located((By.ID, "journeytypeId_1"))
                )
                # Hacer click usando JavaScript para mayor confiabilidad
                self.driver.execute_script("arguments[0].click();", one_way_radio)
                logger.info("✓ One-way trip type selected (journeytypeId_1)")
                time.sleep(1)
                return True

            elif trip_type.lower() == "round-trip":
                # Selector por ID específico: journeytypeId_0 = Ida y vuelta
                round_trip_radio = self.wait.until(
                    EC.presence_of_element_located((By.ID, "journeytypeId_0"))
                )
                self.driver.execute_script("arguments[0].click();", round_trip_radio)
                logger.info("✓ Round-trip trip type selected (journeytypeId_0)")
                time.sleep(1)
                return True

            else:
                logger.error(f"Invalid trip type: {trip_type}. Must be 'one-way' or 'round-trip'")
                return False

        except Exception as e:
            logger.error(f"✗ Error selecting trip type '{trip_type}': {e}")
            # NO lanzar excepción - esto es opcional y no debe romper tests existentes
            return False

    def select_origin(self, city_code, search_text):
        """
        Selecciona el aeropuerto de origen.

        Args:
            city_code: Código IATA del aeropuerto (ej: "BOG")
            search_text: Texto a escribir para buscar (ej: "Bogo")
        """
        logger.info(f"Selecting origin: {city_code} by searching '{search_text}'")

        # Esperar pequeño delay para que el formulario se cargue completamente después de cambiar POS
        time.sleep(2)

        # Scroll al top
        self.driver.execute_script("window.scrollTo(0, 0);")
        time.sleep(1)  # Espera después del scroll

        # Encontrar el botón de origen (puede no estar visible pero sí presente)
        origin_btn = self.wait.until(EC.presence_of_element_located(self.ORIGIN_BUTTON))

        # Hacer el botón visible y clickeable con JavaScript (bypassing CSS display issues)
        self.driver.execute_script("arguments[0].style.display='block'; arguments[0].style.visibility='visible';", origin_btn)
        time.sleep(0.5)

        # Hacer click con JavaScript (más confiable)
        self.driver.execute_script("arguments[0].click();", origin_btn)
        time.sleep(1)  # Espera después del click

        # Escribir en el input y esperar opciones
        origin_input = self.wait.until(EC.visibility_of_element_located(self.ORIGIN_INPUT))
        origin_input.clear()
        origin_input.send_keys(search_text)
        time.sleep(2)  # Espera para que aparezcan las opciones del autocomplete

        # Esperar a que la opción específica esté clickeable
        airport_option = self.wait.until(
            EC.element_to_be_clickable((By.ID, city_code))
        )
        airport_option.click()
        time.sleep(1)  # Espera después de seleccionar

        logger.info(f"Origin '{city_code}' selected successfully")

    def select_destination(self, city_code, search_text):
        """
        Selecciona el aeropuerto de destino.

        Args:
            city_code: Código IATA del aeropuerto (ej: "MAD")
            search_text: Texto a escribir para buscar (ej: "Madri")
        """
        logger.info(f"Selecting destination: {city_code} by searching '{search_text}'")

        # El input de destino se activa automáticamente después de seleccionar origen
        dest_input = self.wait.until(EC.visibility_of_element_located(self.DESTINATION_INPUT))
        dest_input.clear()
        dest_input.send_keys(search_text)
        time.sleep(2)  # Espera para que aparezcan las opciones del autocomplete

        # Esperar a que la opción específica esté clickeable
        airport_option = self.wait.until(
            EC.element_to_be_clickable((By.ID, city_code))
        )
        airport_option.click()
        time.sleep(1)  # Espera después de seleccionar

        logger.info(f"Destination '{city_code}' selected successfully")

    def select_dates(self, departure_days_from_today=4, return_days_from_today=5):
        """
        Selecciona las fechas de viaje de forma dinámica, relativas a HOY.

        Args:
            departure_days_from_today: Días desde HOY para la salida (default: 4 días)
            return_days_from_today: Días desde HOY para el regreso (default: 5 días), None si es solo ida

        Ejemplo:
            Si HOY es 31 de octubre:
            - departure_days_from_today=4 → 4 de noviembre
            - return_days_from_today=5 → 5 de noviembre
        """
        from datetime import datetime, timedelta

        today = datetime.now()
        departure_date = today + timedelta(days=departure_days_from_today)

        logger.info(f"Selecting dates: {departure_days_from_today} days from today = {departure_date.strftime('%Y-%m-%d')}")

        # Seleccionar día de salida
        departure_day = departure_date.day
        departure_xpath = f"//div[contains(@class, 'ngb-dp-day')]//span[@class='custom-day_day' and contains(text(), ' {departure_day} ')]"
        departure_element = self.wait.until(
            EC.element_to_be_clickable((By.XPATH, departure_xpath))
        )
        departure_element.click()
        time.sleep(1)
        logger.info(f"Departure date selected: {departure_date.strftime('%Y-%m-%d')} (day {departure_day})")

        # Seleccionar día de regreso si se proporciona
        if return_days_from_today:
            return_date = today + timedelta(days=return_days_from_today)
            return_day = return_date.day

            logger.info(f"Selecting return: {return_days_from_today} days from today = {return_date.strftime('%Y-%m-%d')}")

            return_xpath = f"//div[contains(@class, 'ngb-dp-day')]//span[@class='custom-day_day' and contains(text(), ' {return_day} ')]"
            return_element = self.wait.until(
                EC.element_to_be_clickable((By.XPATH, return_xpath))
            )
            return_element.click()
            time.sleep(1)
            logger.info(f"Return date selected: {return_date.strftime('%Y-%m-%d')} (day {return_day})")

    def select_passengers(self, adults=3, teens=3, children=3, infants=3):
        """
        Selecciona la cantidad de pasajeros por categoría.

        Args:
            adults: Cantidad de adultos (default: 3 según PDF)
            teens: Cantidad de jóvenes (default: 3 según PDF)
            children: Cantidad de niños (default: 3 según PDF)
            infants: Cantidad de bebés (default: 3 según PDF)

        Nota:
        - El sitio inicia con 1 adulto por defecto
        - Límite total: 9 pasajeros (adultos + jóvenes + niños)
        - Bebés NO cuentan para el límite (van con adulto)

        Estrategia:
        - El modal se carga dinámicamente (Angular)
        - Usamos los IDs de los inputs para localizar el contexto
        - Navegamos desde el input hasta el botón + en el mismo contenedor
        """
        logger.info(f"Selecting passengers: Adults={adults}, Teens={teens}, Children={children}, Infants={infants}")

        # IMPORTANTE: El modal de pasajeros se abre AUTOMÁTICAMENTE después de seleccionar fechas
        # NO hacer click en el botón de pasajeros, ya que eso lo CERRARÍA
        logger.info("Waiting for passengers modal to open automatically after date selection...")
        time.sleep(3)  # Esperar a que se abra automáticamente

        # Esperar a que los botones + estén presentes
        # Selector correcto: <button _ngcontent-gjl-c21="" class="ui-num-ud_button plus"></button>
        plus_button_selector = "//button[contains(@class, 'ui-num-ud_button') and contains(@class, 'plus')]"

        try:
            self.wait.until(
                EC.presence_of_all_elements_located((By.XPATH, plus_button_selector))
            )
            logger.info("✓ Passenger modal opened and plus buttons found")
        except:
            logger.error("✗ Could not find plus buttons - modal may not have opened")
            raise

        time.sleep(1)  # Extra time for rendering

        # Función para hacer click en el botón + por índice
        def click_plus_by_index(index, times, passenger_type):
            """
            Hace click en un botón + específico por su índice N veces.

            Args:
                index: Índice del botón (0=Adults, 1=Teens, 2=Children, 3=Infants)
                times: Número de veces a clickear
                passenger_type: Nombre para logs
            """
            if times <= 0:
                logger.info(f"✓ {passenger_type} - no clicks needed")
                return

            logger.info(f"Clicking + button for {passenger_type} (index {index}) {times} times")

            for i in range(times):
                try:
                    # Re-buscar todos los botones + en cada iteración (el DOM se actualiza)
                    all_plus_buttons = self.driver.find_elements(By.XPATH, plus_button_selector)

                    if len(all_plus_buttons) <= index:
                        raise Exception(f"Not enough plus buttons found. Total: {len(all_plus_buttons)}, needed index: {index}")

                    plus_btn = all_plus_buttons[index]

                    # Scroll al botón para visibilidad
                    self.driver.execute_script("arguments[0].scrollIntoView({block: 'center'});", plus_btn)
                    time.sleep(0.2)

                    # Click con JavaScript
                    self.driver.execute_script("arguments[0].click();", plus_btn)
                    time.sleep(0.6)  # Tiempo para que se actualice el contador

                    logger.info(f"  ✓ {passenger_type} click {i+1}/{times} successful")

                except Exception as e:
                    logger.error(f"  ✗ {passenger_type} click {i+1}/{times} failed: {str(e)}")
                    raise

            logger.info(f"✓ {passenger_type} configured successfully")

        # ADULTOS (índice 0): Inicia en 1, queremos 3 → 2 clicks
        click_plus_by_index(0, adults - 1, "Adults")

        # JÓVENES (índice 1): Inicia en 0, queremos 3 → 3 clicks
        click_plus_by_index(1, teens, "Teens")

        # NIÑOS (índice 2): Inicia en 0, queremos 3 → 3 clicks
        click_plus_by_index(2, children, "Children")

        # BEBÉS (índice 3): Inicia en 0, queremos 3 → 3 clicks
        click_plus_by_index(3, infants, "Infants")

        # Esperar un momento antes de confirmar
        time.sleep(1)

        # Confirmar selección de pasajeros
        logger.info("Confirming passenger selection...")
        confirm_btn = self.wait.until(EC.element_to_be_clickable(self.PASSENGERS_CONFIRM_BUTTON))
        confirm_btn.click()
        time.sleep(2)  # Espera a que se cierre el modal
        logger.info("✓ Passengers selection confirmed and modal closed")
        logger.info(f"TOTAL: {adults} adults + {teens} teens + {children} children + {infants} infants = {adults+teens+children} passengers + {infants} infants")

    def click_search_button(self):
        """
        Hace click en el botón "Rechercher" para buscar vuelos.
        """
        logger.info("Clicking search button")
        search_btn = self.wait.until(EC.presence_of_element_located(self.SEARCH_BUTTON))

        # Scroll al botón y usar JavaScript click para evitar interceptación
        self.driver.execute_script("arguments[0].scrollIntoView({block: 'center'});", search_btn)
        time.sleep(0.5)
        self.driver.execute_script("arguments[0].click();", search_btn)

        time.sleep(3)  # Espera a que cargue la página de selección de vuelos
        logger.info("Search button clicked, waiting for Select Flight page to load")
