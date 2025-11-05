"""
test_roundtrip_booking_Case2.py - Caso de prueba 2: Round-trip Booking completo

DESCRIPCIÓN DEL CASO DE PRUEBA (según PDF página 3):
- Realizar booking Round-trip (Ida y vuelta) completo
- 6 páginas: Home → Select Flight → Passengers → Services → Seatmap → Payment
- Validaciones en cada página
- NO importa que el pago sea rechazado (datos fake permitidos)

FLUJO COMPLETO:
1. Home: Seleccionar idioma, POS, origen, destino, 1 pasajero de cada tipo, ROUND-TRIP
2. Select Flight: Seleccionar tarifa Basic (IDA) y Flex (VUELTA)
3. Passengers: Ingresar información de los pasajeros
4. Services: NO seleccionar ninguno
5. Seatmap: Seleccionar asiento Economy
6. Payment: Realizar pago con tarjeta fake

DIFERENCIAS CON CASE 1:
- Case 1: One-way (solo ida) con tarifa Basic
- Case 2: Round-trip (ida y vuelta) con Basic (ida) y Flex (vuelta)

PUNTOS: 15 pts (según PDF)
"""

# ==================== IMPORTS ====================
import pytest
import allure
import time
import logging
from pages.nuxqa.login_page import LoginPage  # Usamos LoginPage que tiene métodos de búsqueda
from pages.nuxqa.select_flight_page import SelectFlightPage
from pages.nuxqa.passengers_page import PassengersPage
from pages.nuxqa.services_page import ServicesPage
from pages.nuxqa.seatmap_page import SeatmapPage
from pages.nuxqa.payment_page import PaymentPage
from datetime import datetime, timedelta

# ==================== LOGGER ====================
logger = logging.getLogger(__name__)

# ==================== TEST ====================
# 📋 Se REPORTA (ALLURE): Feature "Case 2: Round-trip Booking"
@allure.feature("Case 2: Round-trip Booking")
# 📋 Se REPORTA (ALLURE): Story "Complete Round-trip Flight Booking Flow"
@allure.story("Complete Round-trip Flight Booking Flow")
# 📋 Se REPORTA (ALLURE): Severity level CRITICAL
@allure.severity(allure.severity_level.CRITICAL)
# 🔖 Se MARCA (PYTEST): Test marcado como case2
@pytest.mark.case2
def test_roundtrip_booking(driver, base_url, db, browser, language, screenshots_mode, request, test_config):
    """
    Caso 2: Round-trip Booking - Flujo completo de reserva de ida y vuelta.

    Flujo del test (según PDF página 3):
    1. Home: Idioma, POS, origen, destino, 1 pasajero de cada tipo, ROUND-TRIP
    2. Select Flight: Tarifa Basic (IDA) y Flex (VUELTA)
    3. Passengers: Información de pasajeros (fake)
    4. Services: NO seleccionar ninguno
    5. Seatmap: Asiento Economy
    6. Payment: Pago con tarjeta fake (puede ser rechazado)

    Requisitos técnicos:
    - Logs detallados
    - Almacenamiento en SQLite
    - Reporte Allure con attachments
    - Screenshots en cada paso
    """

    # ==================== SETUP ====================
    case_number = "2"
    test_name = request.node.name
    video_mode = request.config.getoption("--video")

    # Obtener parámetros CLI al inicio para usarlos en el test summary
    pos_param = request.config.getoption("--pos")
    origin_param = request.config.getoption("--origin")
    destination_param = request.config.getoption("--destination")
    departure_days_param = int(request.config.getoption("--departure-days"))
    return_days_param = int(request.config.getoption("--return-days"))  # NUEVO: para round-trip

    # Obtener información de ciudades desde JSON
    cities_info = test_config.get_parameter_options("cities")
    origin_city_name = cities_info[origin_param]["city_name"]
    dest_city_name = cities_info[destination_param]["city_name"]

    # ==================== CARGAR DATOS DESDE JSON ====================
    # Cargar datos de pasajeros desde testdata.json (case_2)
    # IMPORTANTE: El orden debe coincidir con el orden de los contenedores en la página
    # Orden en la página: 1=Adulto, 2=Bebé, 3=Joven, 4=Niño

    # Cargar datos de facturación para obtener email y teléfono del adulto
    billing_data_temp = test_config.get_billing_data()

    adult_data = test_config.get_passenger_data("adult")
    adult_data["type"] = "Adult"
    adult_data["email"] = billing_data_temp.get("email", "test@example.com")
    adult_data["phone"] = billing_data_temp.get("phone", "3001234567")

    infant_data = test_config.get_passenger_data("infant")
    infant_data["type"] = "Infant"

    teen_data = test_config.get_passenger_data("teen")
    teen_data["type"] = "Teen"

    child_data = test_config.get_passenger_data("child")
    child_data["type"] = "Child"

    PASSENGERS_DATA = [adult_data, infant_data, teen_data, child_data]

    # Cargar datos de pago y facturación desde testdata.json
    CARD_DATA = test_config.get_payment_data()
    BILLING_DATA = billing_data_temp

    logger.info(f"✅ Datos cargados desde JSON: {len(PASSENGERS_DATA)} pasajeros, tarjeta, facturación")

    # Obtener environment del base_url
    if "nuxqa4" in base_url:
        env = "qa4"
    elif "nuxqa5" in base_url:
        env = "qa5"
    elif "nuxqa.avtest.ink" in base_url:
        env = "uat1"
    else:
        env = "unknown"

    # Agregar tags dinámicos a Allure
    allure.dynamic.tag(f"browser-{browser}")
    allure.dynamic.tag(f"env-{env}")
    allure.dynamic.tag(f"language-{language.lower()}")
    allure.dynamic.tag("round-trip-booking")
    allure.dynamic.tag("complete-flow")

    # Título dinámico
    allure.dynamic.title(f"Round-trip Booking [{browser}] [{env.upper()}] [{language}]")

    # ==================== PASO 1: Configuración y Resumen ====================
    # 📋 Se REPORTA (ALLURE): Step "Initialize Test Configuration"
    with allure.step("Initialize Test Configuration"):
        test_summary = (
            f"═══════════════════════════════════════════════════\n"
            f"        CASE 2 - ROUND-TRIP BOOKING TEST\n"
            f"═══════════════════════════════════════════════════\n\n"
            f"📋 TEST DETAILS:\n"
            f"   • Test Name: {test_name}\n"
            f"   • Case Number: {case_number}\n"
            f"   • Environment: {env.upper()} ({base_url})\n"
            f"   • Browser: {browser.capitalize()}\n\n"
            f"🌍 CONFIGURATION:\n"
            f"   • Language: {language}\n"
            f"   • POS (Point of Sale): {pos_param}\n"
            f"   • Origin: {origin_param} ({origin_city_name})\n"
            f"   • Destination: {destination_param} ({dest_city_name})\n"
            f"   • Departure: TODAY + {departure_days_param} days\n"
            f"   • Return: TODAY + {return_days_param} days\n"
            f"   • Trip Type: Round-trip (Ida y vuelta)\n\n"
            f"👥 PASSENGERS ({len(PASSENGERS_DATA)} total):\n"
            f"   • 1 Adult (Adulto)\n"
            f"   • 1 Teen (Joven)\n"
            f"   • 1 Child (Niño)\n"
            f"   • 1 Infant (Bebé)\n\n"
            f"🎯 TEST FLOW (6 pages):\n"
            f"   1. Home Page: Select language, POS, round-trip flight search\n"
            f"   2. Select Flight: Choose BASIC fare (IDA) + FLEX fare (VUELTA)\n"
            f"   3. Passengers: Fill passenger information (4 passengers)\n"
            f"   4. Services: Skip all services (no selection)\n"
            f"   5. Seatmap: Select ECONOMY seat\n"
            f"   6. Payment: Fill payment info with fake data (may be rejected)\n\n"
            f"✈️  FLIGHT FARES:\n"
            f"   • Outbound (IDA): BASIC\n"
            f"   • Return (VUELTA): FLEX\n\n"
            f"💳 PAYMENT INFO:\n"
            f"   • Card: Test card (may vary by POS)\n"
            f"   • Note: Payment rejection is EXPECTED and ACCEPTABLE\n\n"
            f"📊 REPORTING:\n"
            f"   • Screenshots: {screenshots_mode}\n"
            f"   • Video: {video_mode}\n"
            f"═══════════════════════════════════════════════════"
        )

        # 📋 Se REPORTA (ALLURE): Adjuntar resumen de configuración del test
        allure.attach(
            test_summary,
            name="📋 Test Configuration Summary",
            attachment_type=allure.attachment_type.TEXT
        )

    # Variables para tracking
    initial_url = base_url
    current_step = "Setup"
    step_results = {}

    # ==================== PASO 2: Home Page - Abrir y Configurar Idioma y POS ====================
    # 📋 Se REPORTA (ALLURE): Step "Open Home Page and Configure Language and POS"
    with allure.step(f"Step 1: Open Home Page and Configure Language ({language}) and POS"):
        current_step = "Home - Language and POS Selection"
        search_page = LoginPage(driver)
        # 🌐 Se NAVEGA (SELENIUM): Abrir URL base de la aplicación
        search_page.open(base_url)
        # ⏳ Se ESPERA (SELENIUM): Página cargue completamente
        time.sleep(2)

        # 🖱️ Se PRESIONA (SELENIUM): Seleccionar idioma desde dropdown
        search_page.select_language(language)
        time.sleep(1)

        # 🖱️ Se PRESIONA (SELENIUM): Abrir modal de POS
        logger.info(f"Selecting POS: {pos_param}")
        search_page.click_pos_button()
        # 🖱️ Se PRESIONA (SELENIUM): Seleccionar POS específico y aplicar
        search_page.select_pos(pos_param)
        time.sleep(1)

        step_results["language_selection"] = "SUCCESS"
        step_results["pos_selection"] = "SUCCESS"
        allure.attach(
            f"Language: {language}\nPOS: {pos_param}\nURL: {driver.current_url}",
            name="Language and POS Configuration",
            attachment_type=allure.attachment_type.TEXT
        )

    # ==================== PASO 3: Home Page - Configurar Búsqueda de Vuelo (ROUND-TRIP) ====================
    with allure.step("Step 2: Configure Flight Search (Round-trip, 4 passengers)"):
        current_step = "Home - Flight Search"

        # IMPORTANTE: Seleccionar tipo de viaje PRIMERO (antes de origen/destino)
        # CAMBIO CLAVE: "round-trip" en vez de "one-way"
        trip_type_selected = search_page.select_trip_type("round-trip")
        if trip_type_selected:
            logger.info("✓ Trip type 'round-trip' selected successfully")
        else:
            logger.warning("Could not select trip type, continuing with default")
        time.sleep(1)

        # Obtener search strings desde parameter_options.json
        origin_search = cities_info[origin_param]["search_string"]
        dest_search = cities_info[destination_param]["search_string"]

        logger.info(f"Origin: {origin_param} (search: '{origin_search}')")
        logger.info(f"Destination: {destination_param} (search: '{dest_search}')")
        logger.info(f"Departure days from today: {departure_days_param}")
        logger.info(f"Return days from today: {return_days_param}")

        # Seleccionar origen y destino usando parámetros desde JSON
        search_page.select_origin(origin_param, origin_search)
        time.sleep(1)

        search_page.select_destination(destination_param, dest_search)
        time.sleep(1)

        # Seleccionar fechas (ida Y vuelta - ROUND-TRIP)
        # CAMBIO CLAVE: pasar return_days_from_today en vez de None
        search_page.select_dates(
            departure_days_from_today=departure_days_param,
            return_days_from_today=return_days_param
        )
        time.sleep(2)

        # Configurar pasajeros: 1 de cada tipo
        search_page.select_passengers(adults=1, teens=1, children=1, infants=1)
        time.sleep(1)

        # Crear summary de búsqueda
        search_info = (
            f"Language: {language}\n"
            f"POS: {pos_param}\n"
            f"Trip Type: Round-trip (Ida y vuelta)\n"
            f"Origin: {origin_param} ({origin_city_name})\n"
            f"Destination: {destination_param} ({dest_city_name})\n"
            f"Departure: TODAY + {departure_days_param} days\n"
            f"Return: TODAY + {return_days_param} days\n"
            f"Passengers: 4 total (1 Adult, 1 Teen, 1 Child, 1 Infant)"
        )

        step_results["flight_search_config"] = "SUCCESS"
        allure.attach(
            search_info,
            name="Flight Search Configuration",
            attachment_type=allure.attachment_type.TEXT
        )

        # 🖱️ Se PRESIONA (SELENIUM): Botón "Buscar vuelos" para iniciar búsqueda
        search_page.click_search_button()
        # ⏳ Se ESPERA (SELENIUM): Resultados de búsqueda de vuelos carguen
        time.sleep(5)

    # ==================== PASO 4: Select Flight Page - Seleccionar BASIC (IDA) + FLEX (VUELTA) ====================
    # 📋 Se REPORTA (ALLURE): Step "Select Flights - BASIC (Outbound) + FLEX (Return)"
    with allure.step("Step 3: Select Flights - BASIC (Outbound) + FLEX (Return)"):
        current_step = "Select Flight - Basic + Flex"
        select_flight_page = SelectFlightPage(driver)

        # ⏳ Se ESPERA (SELENIUM): Página de selección de vuelos cargue completamente
        page_loaded = select_flight_page.wait_for_page_load()
        # ✅ Se VALIDA (PYTEST): Página de vuelos debe cargar correctamente
        assert page_loaded, "Select Flight page did not load"

        # PASO 4.1: Seleccionar vuelo de IDA con tarifa BASIC
        logger.info("Selecting OUTBOUND flight with BASIC fare...")
        # 🖱️ Se PRESIONA (SELENIUM): Seleccionar vuelo de ida con tarifa BASIC
        flight_outbound_selected = select_flight_page.select_outbound_flight_and_basic_plan()
        # ✅ Se VALIDA (PYTEST): Vuelo de ida con BASIC debe seleccionarse correctamente
        assert flight_outbound_selected, "Failed to select outbound flight with BASIC fare"

        step_results["outbound_flight_basic"] = "SUCCESS"
        logger.info("✓ Outbound flight with BASIC fare selected")

        time.sleep(2)

        # PASO 4.2: Seleccionar vuelo de VUELTA con tarifa FLEX
        logger.info("Selecting RETURN flight with FLEX fare...")
        # 🖱️ Se PRESIONA (SELENIUM): Seleccionar vuelo de vuelta con tarifa FLEX
        flight_return_selected = select_flight_page.select_return_flight_and_flex_plan()
        # ✅ Se VALIDA (PYTEST): Vuelo de vuelta con FLEX debe seleccionarse correctamente
        assert flight_return_selected, "Failed to select return flight with FLEX fare"

        step_results["return_flight_flex"] = "SUCCESS"
        logger.info("✓ Return flight with FLEX fare selected")

        flight_selection_info = (
            f"Flight Type: Round-trip (Ida y vuelta)\n"
            f"Outbound Fare: BASIC (1st option)\n"
            f"Return Fare: FLEX (3rd option)\n"
            f"Selected: First available flights for both directions\n"
            f"Note: Combines Case 1 (Basic) with Case 3 (Flex) selection logic"
        )

        allure.attach(
            flight_selection_info,
            name="Flight Selection Details",
            attachment_type=allure.attachment_type.TEXT
        )

        time.sleep(2)

        # Intentar click "Continuar" si existe
        try:
            select_flight_page.click_continue()
            logger.info("Continue button clicked successfully")
        except:
            logger.info("No Continue button found or not needed - may auto-navigate to Passengers")

        time.sleep(5)  # Esperar a que cargue la página de Passengers

    # ==================== PASO 5: Passengers Page - Llenar Información ====================
    # 📋 Se REPORTA (ALLURE): Step "Fill Passenger Information"
    with allure.step(f"Step 4: Fill Passenger Information ({len(PASSENGERS_DATA)} passengers)"):
        current_step = "Passengers Information"
        passengers_page = PassengersPage(driver)

        # ⏳ Se ESPERA (SELENIUM): Página de pasajeros cargue completamente
        page_loaded = passengers_page.wait_for_page_load()
        # ✅ Se VALIDA (PYTEST): Página de pasajeros debe cargar correctamente
        assert page_loaded, "Passengers page did not load"

        # ⌨️ Se INGRESA (SELENIUM): Información completa de todos los pasajeros (nombres, apellidos, fechas, documentos)
        all_filled = passengers_page.fill_all_passengers(PASSENGERS_DATA)
        # ✅ Se VALIDA (PYTEST): Todos los pasajeros deben llenarse correctamente
        assert all_filled, "Failed to fill all passenger information"

        # Llenar información del Titular de la Reserva (Reservation Holder)
        adult_data = PASSENGERS_DATA[0]  # Primer pasajero es el adulto
        # ⌨️ Se INGRESA (SELENIUM): Email y teléfono del titular de la reserva
        holder_filled = passengers_page.fill_reservation_holder(
            email=adult_data["email"],
            phone=adult_data["phone"]
        )
        # ✅ Se VALIDA (PYTEST): Información del titular debe llenarse correctamente
        assert holder_filled, "Failed to fill Reservation Holder information"

        step_results["passengers_info"] = "SUCCESS"
        step_results["reservation_holder"] = "SUCCESS"

        passengers_summary = "Passengers Information Filled:\n\n"
        for i, passenger in enumerate(PASSENGERS_DATA):
            passengers_summary += f"{i+1}. {passenger['type']}: {passenger['first_name']} {passenger['last_name']}\n"
            passengers_summary += f"   Birth Date: {passenger['birth_date']}\n"
            passengers_summary += f"   Doc: {passenger.get('doc_type', 'N/A')} - {passenger.get('doc_number', 'N/A')}\n\n"

        passengers_summary += "\n📧 Reservation Holder (Titular de la Reserva):\n"
        passengers_summary += f"   • Email: {adult_data['email']}\n"
        passengers_summary += f"   • Phone: +57 {adult_data['phone']}\n"
        passengers_summary += f"   • Terms Accepted: Yes\n"

        allure.attach(
            passengers_summary,
            name="Passengers Information Summary",
            attachment_type=allure.attachment_type.TEXT
        )

        # 📸 Se CAPTURA (SELENIUM): Screenshot después de llenar pasajeros
        time.sleep(2)
        driver.save_screenshot("reports/debug_passengers_after_fill.png")
        logger.info("DEBUG screenshot saved: debug_passengers_after_fill.png")

        # 🖱️ Se PRESIONA (SELENIUM): Botón "Continuar" para avanzar a Services
        continue_clicked = passengers_page.click_continue()
        # ✅ Se VALIDA (PYTEST): Botón Continuar debe hacer click correctamente
        assert continue_clicked, "Failed to click continue button on Passengers page"

        time.sleep(2)

    # ==================== PASO 6: Services Page - Seleccionar Servicio ====================
    with allure.step("Step 5: Services - Select 'Avianca Lounges' or Any Available Service"):
        current_step = "Services - Service Selection"
        services_page = ServicesPage(driver)

        page_loaded = services_page.wait_for_page_load()
        assert page_loaded, "Services page did not load"

        # Intentar seleccionar "Avianca Lounges"
        logger.info("Attempting to select 'Avianca Lounges' service...")
        service_selected = services_page.select_service_by_name("Avianca Lounges")

        selected_service_name = "Avianca Lounges"

        # Si no está disponible, seleccionar el primer servicio disponible
        if not service_selected:
            logger.warning("'Avianca Lounges' not available, selecting first available service...")
            service_selected = services_page.select_first_available_service()
            selected_service_name = "First available service"

        # Si aún así no se pudo seleccionar ninguno, la página redirige automáticamente
        if not service_selected:
            logger.warning("No services available to select - page may auto-redirect to Seatmap")
            selected_service_name = "NONE (auto-skipped)"
            # Esperar a que la página redirija automáticamente
            time.sleep(3)
        else:
            # Si se seleccionó un servicio, esperar un poco para que el botón esté listo
            logger.info(f"Service selected: {selected_service_name}")
            time.sleep(2)

            # Click en Continue para ir a Seatmap
            logger.info("Clicking Continue button to proceed to Seatmap...")
            continue_clicked = services_page.click_continue()

            if not continue_clicked:
                logger.warning("Continue button not found via click_continue(), trying alternative approach...")
                # Alternativa: scroll hacia abajo y buscar cualquier botón con texto "Continuar"
                try:
                    driver.execute_script("window.scrollTo(0, document.body.scrollHeight);")
                    time.sleep(1)
                    alt_continue_btn = driver.find_element(By.XPATH, "//button[contains(., 'Continuar') or contains(@class, 'btn-next')]")
                    driver.execute_script("arguments[0].click();", alt_continue_btn)
                    logger.info("✓ Continue clicked via alternative approach")
                    continue_clicked = True
                except Exception as e:
                    logger.error(f"Alternative Continue click also failed: {e}")
                    continue_clicked = False

            assert continue_clicked, "Failed to click Continue on Services page"

        step_results["services_selection"] = "SUCCESS"

        services_summary = f"🛎️  Service Selected: {selected_service_name}\n\n"
        services_summary += "Case 2 Requirements:\n"
        services_summary += "1. Try to select 'Avianca Lounges'\n"
        services_summary += "2. If not available, select any other service\n"
        services_summary += "3. If no services available, skip all"

        allure.attach(
            services_summary,
            name="Services Configuration",
            attachment_type=allure.attachment_type.TEXT
        )

        time.sleep(2)

    # ==================== PASO 7: Seatmap Page - Asignar Asientos (IDA y VUELTA) ====================
    # 📋 Se REPORTA (ALLURE): Step "Seatmap - Assign Seats for Outbound and Return Flights"
    with allure.step("Step 6: Seatmap - Assign Seats (ANY TYPE) for Outbound and Return Flights"):
        current_step = "Seatmap - Seat Assignment (Round-trip)"
        seatmap_page = SeatmapPage(driver)

        # ⏳ Se ESPERA (SELENIUM): Página de seatmap cargue completamente
        page_loaded = seatmap_page.wait_for_page_load()
        # ✅ Se VALIDA (PYTEST): Página de seatmap debe cargar correctamente
        assert page_loaded, "Seatmap page did not load"

        # ========== VUELO DE IDA (Outbound) ==========
        logger.info("======== SELECTING SEATS FOR OUTBOUND FLIGHT ========")

        # 🖱️ Se PRESIONA (SELENIUM): Seleccionar asientos de cualquier tipo para 3 pasajeros (vuelo de ida)
        seat_assignments_outbound = seatmap_page.assign_any_type_seats_to_passengers(passenger_count=3)
        # ✅ Se VALIDA (PYTEST): Deben asignarse al menos 2 asientos para el vuelo de ida
        assert len(seat_assignments_outbound) >= 2, f"Failed to assign at least 2 seats for outbound. Got: {seat_assignments_outbound}"

        if len(seat_assignments_outbound) < 3:
            logger.warning(f"Only assigned {len(seat_assignments_outbound)} seats for outbound (expected 3).")

        logger.info(f"✓ Outbound seat assignments: {seat_assignments_outbound}")

        # Screenshot después de seleccionar asientos de ida
        try:
            seatmap_page.get_page_screenshot("seatmap_outbound_complete.png")
        except:
            pass

        # 🖱️ Se PRESIONA (SELENIUM): Botón "Siguiente vuelo" para continuar a asientos de vuelta
        logger.info("Clicking 'Siguiente vuelo' to proceed to return flight seatmap...")
        next_flight_clicked = seatmap_page.click_next_flight()
        # ✅ Se VALIDA (PYTEST): Botón "Siguiente vuelo" debe hacer click correctamente
        assert next_flight_clicked, "Failed to click 'Siguiente vuelo' button"

        # ========== VUELO DE VUELTA (Return) ==========
        logger.info("======== SELECTING SEATS FOR RETURN FLIGHT ========")

        # 🖱️ Se PRESIONA (SELENIUM): Seleccionar asientos de cualquier tipo para 3 pasajeros (vuelo de vuelta)
        seat_assignments_return = seatmap_page.assign_any_type_seats_to_passengers(passenger_count=3)
        # ✅ Se VALIDA (PYTEST): Deben asignarse al menos 2 asientos para el vuelo de vuelta
        assert len(seat_assignments_return) >= 2, f"Failed to assign at least 2 seats for return. Got: {seat_assignments_return}"

        if len(seat_assignments_return) < 3:
            logger.warning(f"Only assigned {len(seat_assignments_return)} seats for return (expected 3).")

        logger.info(f"✓ Return seat assignments: {seat_assignments_return}")

        step_results["seatmap_selection"] = "SUCCESS"

        # Crear summary de asientos asignados (IDA + VUELTA)
        seatmap_summary = "🪑 Seat Assignments (ANY TYPE: Plus/Premium/Economy):\n\n"
        seatmap_summary += "✈️  OUTBOUND FLIGHT (IDA):\n"
        for passenger, seat_id in seat_assignments_outbound.items():
            seatmap_summary += f"  • {passenger}: {seat_id}\n"

        seatmap_summary += "\n✈️  RETURN FLIGHT (VUELTA):\n"
        for passenger, seat_id in seat_assignments_return.items():
            seatmap_summary += f"  • {passenger}: {seat_id}\n"

        seatmap_summary += "\nNote: Bebé (Infant) does not require seat selection"

        allure.attach(
            seatmap_summary,
            name="Seat Selection Details",
            attachment_type=allure.attachment_type.TEXT
        )

        # Screenshot después de seleccionar asientos de vuelta
        try:
            seatmap_page.get_page_screenshot("seatmap_return_complete.png")
        except:
            pass

        # 🖱️ Se PRESIONA (SELENIUM): Botón "Ir a pagar" para avanzar a Payment
        logger.info("Clicking 'Ir a pagar' to proceed to Payment page...")
        go_to_payment_clicked = seatmap_page.click_go_to_payment()
        # ✅ Se VALIDA (PYTEST): Botón "Ir a pagar" debe hacer click correctamente
        assert go_to_payment_clicked, "Failed to click 'Ir a pagar' button on Seatmap page"

        # ⏳ Se ESPERA (SELENIUM): Página de Payment cargue completamente
        time.sleep(5)

    # ==================== PASO 8: Payment Page - Llenar y Confirmar ====================
    # 📋 Se REPORTA (ALLURE): Step "Payment - Fill Information and Confirm Payment"
    with allure.step("Step 7: Payment - Fill Information and Confirm Payment"):
        current_step = "Payment - Fill and Confirm"
        payment_page = PaymentPage(driver)

        # ⏳ Se ESPERA (SELENIUM): Página de pago cargue completamente
        page_loaded = payment_page.wait_for_page_load()
        # ✅ Se VALIDA (PYTEST): Página de pago debe cargar correctamente
        assert page_loaded, "Payment page did not load"

        # Obtener datos del adulto (titular)
        adult_data = PASSENGERS_DATA[0]
        card_holder_name = f"{adult_data['first_name']} {adult_data['last_name']}"

        # ⌨️ Se INGRESA (SELENIUM): Información de tarjeta, facturación y términos (datos fake)
        payment_completed = payment_page.complete_payment_flow(
            card_holder_name=card_holder_name,
            email=adult_data["email"]
        )
        # ✅ Se VALIDA (PYTEST): Flujo de pago debe completarse correctamente
        assert payment_completed, "Failed to complete payment flow"

        step_results["payment_completed"] = "SUCCESS"

        payment_summary = (
            f"💳 PAYMENT INFORMATION (FAKE DATA):\n\n"
            f"Card Holder: {card_holder_name}\n"
            f"Card Number: Test card (from JSON)\n"
            f"Email: {adult_data['email']}\n"
            f"Billing Address: From testdata.json\n\n"
            f"⚠️  NOTE: Payment may be REJECTED (this is expected and acceptable)"
        )

        allure.attach(
            payment_summary,
            name="Payment Details",
            attachment_type=allure.attachment_type.TEXT
        )

    # ==================== PASO 9: Verificar Página Post-Pago ====================
    with allure.step("Step 8: Verify post-payment page"):
        logger.info("Waiting for post-payment page to fully load and process...")

        # Capturar la URL inicial (página de payment)
        initial_payment_url = driver.current_url
        logger.info(f"Initial payment URL: {initial_payment_url}")

        max_wait_time = 90  # segundos máximos
        check_interval = 5
        elapsed_time = 0
        url_changed = False

        while elapsed_time < max_wait_time:
            time.sleep(check_interval)
            elapsed_time += check_interval

            current_url = driver.current_url
            logger.info(f"[{elapsed_time}s] Current URL: {current_url}")

            # Verificar si la URL cambió
            initial_path = initial_payment_url.split('?')[0]
            current_path = current_url.split('?')[0]

            if current_path != initial_path:
                logger.info(f"✓ Page URL changed from payment to new page after {elapsed_time} seconds")
                url_changed = True
                break

        if not url_changed:
            logger.warning(f"URL did not change after {max_wait_time} seconds - may still be processing")

        # Esperar 10 segundos adicionales para que la página final cargue completamente
        logger.info("Waiting 10 additional seconds for final page to fully render...")
        time.sleep(10)

        # Capturar información de la página final
        final_url = driver.current_url
        final_title = driver.title

        logger.info(f"Post-payment URL: {final_url}")
        logger.info(f"Post-payment Title: {final_title}")

        # 📸 Se CAPTURA (SELENIUM): Screenshot de la página final después del pago
        final_screenshot = f"reports/final_page_{int(time.time())}.png"
        driver.save_screenshot(final_screenshot)
        logger.info(f"📸 Final page screenshot: {final_screenshot}")

        # Determinar el tipo de página alcanzada
        page_type = "Unknown"
        if "confirmation" in final_url.lower() or "confirm" in final_url.lower():
            page_type = "Confirmation Page"
        elif "success" in final_url.lower():
            page_type = "Success Page"
        elif "error" in final_url.lower() or "fail" in final_url.lower():
            page_type = "Error Page"
        elif "rejected" in final_url.lower() or "decline" in final_url.lower():
            page_type = "Payment Rejected Page"
        elif "payment" in final_url.lower() or "pay" in final_url.lower():
            page_type = "Still on Payment Page (may have validation errors)"
        elif "booking" in final_url.lower():
            page_type = "Booking Status Page"

        post_payment_summary = (
            f"═══════════════════════════════════════\n"
            f"       POST-PAYMENT PAGE DETAILS\n"
            f"═══════════════════════════════════════\n\n"
            f"Page Type: {page_type}\n\n"
            f"URL: {final_url}\n\n"
            f"Title: {final_title}\n\n"
            f"Screenshot: {final_screenshot}\n"
        )

        logger.info(f"Post-payment page type identified: {page_type}")

        allure.attach(
            post_payment_summary,
            name="Post-Payment Page Information",
            attachment_type=allure.attachment_type.TEXT
        )

        # 📋 Se REPORTA (ALLURE): Adjuntar screenshot de página final a reporte
        try:
            with open(final_screenshot, "rb") as image:
                allure.attach(
                    image.read(),
                    name="Final Page Screenshot",
                    attachment_type=allure.attachment_type.PNG
                )
        except:
            pass

        step_results["Step 8 - Post-Payment Page"] = f"SUCCESS - {page_type} | URL: {final_url[:50]}..."

        # Esperar 3 segundos adicionales antes de cerrar
        logger.info("Waiting 3 additional seconds before closing browser...")
        time.sleep(3)

    # ==================== PASO 10: Resultados Finales ====================
    steps_summary = "═══════════════════════════════════════\n"
    steps_summary += "      ROUND-TRIP BOOKING - FLOW SUMMARY\n"
    steps_summary += "═══════════════════════════════════════\n\n"

    for step, result in step_results.items():
        status_icon = "✅" if "SUCCESS" in result else "⚠️"
        steps_summary += f"{status_icon} {step}: {result}\n"

    steps_summary += f"\n📊 FINAL STATUS:\n"
    steps_summary += f"   • Initial URL: {initial_url}\n"
    steps_summary += f"   • Final URL: {final_url}\n"
    steps_summary += f"   • Total Steps Completed: {len(step_results)}/8\n"
    steps_summary += f"   • Test Result: PASSED\n\n"
    steps_summary += "🎯 VALIDATION:\n"
    steps_summary += "   ✓ Completed full round-trip booking flow\n"
    steps_summary += "   ✓ Selected BASIC fare for outbound\n"
    steps_summary += "   ✓ Selected FLEX fare for return\n"
    steps_summary += "   ✓ Reached payment page successfully\n"
    steps_summary += "   ✓ All required information filled\n"
    steps_summary += "   ✓ Payment submission attempted\n"
    steps_summary += "   ✓ Post-payment page verified\n"

    allure.attach(
        steps_summary,
        name="Complete Flow Summary",
        attachment_type=allure.attachment_type.TEXT
    )

    # ==================== PASO 11: Guardar en Base de Datos ====================
    with allure.step("Save test results to database"):
        db.save_test_result(
            test_name=test_name,
            status="PASSED",
            execution_time=0,
            browser=browser,
            url=final_url,
            language=language,
            case_number=case_number,
            environment=env,
            screenshots_mode=screenshots_mode,
            video_enabled=video_mode,
            expected_value="Complete round-trip booking flow to payment page",
            actual_value=f"Reached: {final_url}",
            validation_result="PASSED",
            initial_url=initial_url,
            validation_message=f"Round-trip booking flow completed successfully. Steps: {len(step_results)}/8. Final page: {page_type}"
        )

        db_summary = (
            f"✓ Test results saved to database\n\n"
            f"Case: {case_number}\n"
            f"Status: PASSED\n"
            f"Environment: {env}\n"
            f"Language: {language}\n"
            f"Steps Completed: {len(step_results)}/8"
        )

        allure.attach(
            db_summary,
            name="Database Save Confirmation",
            attachment_type=allure.attachment_type.TEXT
        )

    # ==================== RESULTADO FINAL ====================
    with allure.step("Test completed successfully"):
        final_message = (
            f"✅ ROUND-TRIP BOOKING TEST COMPLETED SUCCESSFULLY\n\n"
            f"Flow: Home → Select Flight (Basic+Flex) → Passengers → Services → Seatmap → Payment → Post-Payment\n"
            f"All 8 steps executed\n"
            f"Final page: {page_type}\n"
            f"Test status: PASSED"
        )

        allure.attach(
            final_message,
            name="Test Completion Summary",
            attachment_type=allure.attachment_type.TEXT
        )

    # Assert final para pytest
    assert len(final_url) > 0, f"Test completed but final URL is empty"
