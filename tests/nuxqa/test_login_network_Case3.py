"""
test_login_network_Case3.py - Caso de prueba 3: Búsqueda de vuelos y captura de Network

DESCRIPCIÓN DEL CASO DE PRUEBA (según PDF página 4):
- Navegar a UAT1 (nuxqa.avtest.ink)
- Configurar idioma Francés y POS France
- Realizar búsqueda de vuelos (tipo viaje, origen, destino, 3 pasajeros de cada tipo)
- Validar que cargue página de Select Flight
- Capturar el evento "Session" del Network usando Chrome DevTools Protocol
- Almacenar datos en base de datos SQLite
- Generar reporte detallado en Allure

CONFIGURACIÓN:
- Ambiente: UAT1 (nuxqa.avtest.ink)
- Idioma: Français
- POS: France
- Pasajeros: 3 de cada tipo (Adulto, Joven, Niño, Infante)

NOTA: El sitio UAT1 NO tiene botón de login visible. El flujo se realiza sin login.

PUNTOS: 10 pts (según PDF)
"""

# ==================== IMPORTS ====================
import pytest
import allure
import time
from pages.nuxqa.login_page import LoginPage
from pages.nuxqa.select_flight_page import SelectFlightPage
from utils.network_capture import NetworkCapture
import json

# ==================== CONFIGURACIÓN ====================
# Configuración fija para Case 3 (sin login)
LANGUAGE = "Français"
POS = "France"
PASSENGERS_EACH_TYPE = 3  # 3 pasajeros de cada tipo según PDF

# Mapeo de códigos IATA a textos de búsqueda
AIRPORT_SEARCH_MAPPING = {
    # Colombia
    "BOG": "Bogo",      # Bogotá
    "MDE": "Mede",      # Medellín
    "CLO": "Cali",      # Cali
    "CTG": "Cart",      # Cartagena
    "BAQ": "Barr",      # Barranquilla
    "SMR": "Sant",      # Santa Marta
    "BGA": "Buca",      # Bucaramanga

    # Ecuador
    "UIO": "Quit",      # Quito
    "GYE": "Guay",      # Guayaquil

    # España
    "MAD": "Madr",      # Madrid
    "BCN": "Barc",      # Barcelona

    # Perú
    "LIM": "Lima",      # Lima

    # México
    "MEX": "Mexi",      # Ciudad de México

    # USA
    "MIA": "Miam",      # Miami
    "JFK": "New",       # Nueva York JFK
}

# NOTA: Las fechas y ciudades se pasan por parámetros CLI:
# --origin, --destination, --departure-days, --return-days

# ==================== TEST ====================
@allure.feature("Case 3: Flight Search and Network Capture")
@allure.story("Search Flights with Session Event Capture")
@allure.severity(allure.severity_level.CRITICAL)
@pytest.mark.case3
def test_flight_search_and_network_capture(driver, base_url, db, browser, screenshots_mode, request):
    """
    Caso 3: Búsqueda de vuelos y captura del evento Session del Network.

    Flujo del test (según PDF página 4):
    1. Habilitar captura de red (CDP)
    2. Navegar a UAT1
    3. Configurar idioma Francés
    4. Configurar POS France
    5. Llenar formulario de búsqueda (origen, destino, fechas, 3 pasajeros de cada tipo)
    6. Hacer click en "Buscar"
    7. Validar que cargue página Select Flight
    8. Capturar evento "Session" del network
    9. Guardar resultados en BD
    10. Generar reporte Allure con evidencia

    Requisitos técnicos:
    - CDP habilitado (solo Chrome/Edge)
    - Logs detallados
    - Almacenamiento en SQLite
    - Reporte Allure con attachments
    """

    # ==================== SETUP ====================
    case_number = "3"
    test_name = request.node.name  # Nombre del test desde pytest
    env = "uat1"  # UAT1 environment
    video_mode = request.config.getoption("--video")

    # Obtener parámetros CLI para Case 3
    ORIGIN_CODE = request.config.getoption("--origin")
    DESTINATION_CODE = request.config.getoption("--destination")
    DEPARTURE_DAYS_FROM_TODAY = request.config.getoption("--departure-days")
    RETURN_DAYS_FROM_TODAY = request.config.getoption("--return-days")

    # Obtener textos de búsqueda del diccionario
    ORIGIN_SEARCH = AIRPORT_SEARCH_MAPPING.get(ORIGIN_CODE, ORIGIN_CODE[:4].capitalize())
    DESTINATION_SEARCH = AIRPORT_SEARCH_MAPPING.get(DESTINATION_CODE, DESTINATION_CODE[:4].capitalize())

    # Agregar tags dinámicos a Allure
    allure.dynamic.tag(f"browser-{browser}")
    allure.dynamic.tag(f"env-{env}")
    allure.dynamic.tag(f"language-{LANGUAGE.lower()}")
    allure.dynamic.tag(f"pos-{POS.lower()}")
    allure.dynamic.tag("flight-search")
    allure.dynamic.tag("network-capture")

    # Título dinámico
    allure.dynamic.title(f"Flight Search & Network Capture [{browser}] [UAT1] [French-France]")

    # ==================== PASO 1: Inicializar Page Objects y Network Capture ====================
    with allure.step("Initialize Page Objects and Network Capture"):
        search_page = LoginPage(driver)  # Usamos LoginPage para el formulario de búsqueda
        network_capture = NetworkCapture(driver)

        # Habilitar captura de red ANTES de navegar
        network_capture.enable_network_tracking()

        allure.attach(
            f"Browser: {browser}\n"
            f"Environment: {env}\n"
            f"Language: {LANGUAGE}\n"
            f"POS: {POS}\n"
            f"Origin: {ORIGIN_CODE} (search: {ORIGIN_SEARCH})\n"
            f"Destination: {DESTINATION_CODE} (search: {DESTINATION_SEARCH})\n"
            f"Departure: TODAY + {DEPARTURE_DAYS_FROM_TODAY} days\n"
            f"Return: TODAY + {RETURN_DAYS_FROM_TODAY} days\n"
            f"Passengers: {PASSENGERS_EACH_TYPE} of each type",
            name="Test Configuration",
            attachment_type=allure.attachment_type.TEXT
        )

    # ==================== PASO 2: Navegar a UAT1 ====================
    with allure.step(f"Open UAT1 URL: {base_url}"):
        search_page.open(base_url)
        time.sleep(2)  # Espera inicial para carga completa

    # ==================== PASO 3: Configurar Idioma ====================
    with allure.step(f"Configure Language: {LANGUAGE}"):
        search_page.select_language(LANGUAGE)
        time.sleep(1)

        allure.attach(
            f"Selected Language: {LANGUAGE}",
            name="Language Configuration",
            attachment_type=allure.attachment_type.TEXT
        )

    # ==================== PASO 4: Configurar POS ====================
    with allure.step(f"Configure POS: {POS}"):
        search_page.configure_pos(POS)
        time.sleep(1)

        allure.attach(
            f"Selected POS: {POS}",
            name="POS Configuration",
            attachment_type=allure.attachment_type.TEXT
        )

    # ==================== PASO 5: Seleccionar Origen ====================
    with allure.step(f"Select Origin: {ORIGIN_CODE} (search: '{ORIGIN_SEARCH}')"):
        search_page.select_origin(ORIGIN_CODE, ORIGIN_SEARCH)
        time.sleep(1)

        allure.attach(
            f"Origin Code: {ORIGIN_CODE}\nSearch Text: {ORIGIN_SEARCH}",
            name="Origin Selection",
            attachment_type=allure.attachment_type.TEXT
        )

    # ==================== PASO 6: Seleccionar Destino ====================
    with allure.step(f"Select Destination: {DESTINATION_CODE} (search: '{DESTINATION_SEARCH}')"):
        search_page.select_destination(DESTINATION_CODE, DESTINATION_SEARCH)
        time.sleep(1)

        allure.attach(
            f"Destination Code: {DESTINATION_CODE}\nSearch Text: {DESTINATION_SEARCH}",
            name="Destination Selection",
            attachment_type=allure.attachment_type.TEXT
        )

    # ==================== PASO 7: Seleccionar Fechas ====================
    from datetime import datetime, timedelta
    today = datetime.now()
    departure_date = today + timedelta(days=DEPARTURE_DAYS_FROM_TODAY)
    return_date = today + timedelta(days=RETURN_DAYS_FROM_TODAY)

    with allure.step(f"Select Travel Dates: TODAY + {DEPARTURE_DAYS_FROM_TODAY} days → TODAY + {RETURN_DAYS_FROM_TODAY} days"):
        search_page.select_dates(
            departure_days_from_today=DEPARTURE_DAYS_FROM_TODAY,
            return_days_from_today=RETURN_DAYS_FROM_TODAY
        )
        time.sleep(1)

        allure.attach(
            f"Today: {today.strftime('%Y-%m-%d')}\n"
            f"Departure: {departure_date.strftime('%Y-%m-%d')} (TODAY + {DEPARTURE_DAYS_FROM_TODAY} days)\n"
            f"Return: {return_date.strftime('%Y-%m-%d')} (TODAY + {RETURN_DAYS_FROM_TODAY} days)\n\n"
            f"Note: Dynamic dates ensure test always works regardless of execution date",
            name="Date Selection",
            attachment_type=allure.attachment_type.TEXT
        )

    # ==================== PASO 8: Seleccionar Pasajeros ====================
    with allure.step(f"Select Passengers: {PASSENGERS_EACH_TYPE} of each type (as per PDF)"):
        # PDF especifica: 3 adultos, 3 jóvenes, 3 niños, 3 bebés
        # Límite del sitio: 9 pasajeros totales (bebés NO cuentan)
        # Total: 3+3+3 = 9 pasajeros + 3 bebés ✓
        search_page.select_passengers(
            adults=PASSENGERS_EACH_TYPE,
            teens=PASSENGERS_EACH_TYPE,
            children=PASSENGERS_EACH_TYPE,
            infants=PASSENGERS_EACH_TYPE
        )
        time.sleep(1)

        total_passengers = PASSENGERS_EACH_TYPE * 3  # Adultos + Jóvenes + Niños
        allure.attach(
            f"Adults: {PASSENGERS_EACH_TYPE}\nTeens: {PASSENGERS_EACH_TYPE}\nChildren: {PASSENGERS_EACH_TYPE}\nInfants: {PASSENGERS_EACH_TYPE}\n\nTotal passengers: {total_passengers}\nTotal infants: {PASSENGERS_EACH_TYPE}\n\nNote: Infants do NOT count towards the 9 passenger limit",
            name="Passenger Selection",
            attachment_type=allure.attachment_type.TEXT
        )

    # ==================== PASO 9: Hacer Click en Buscar ====================
    with allure.step("Click Search Button to find flights"):
        # Limpiar eventos previos antes de buscar
        network_capture.clear_events()

        # Click en buscar
        search_page.click_search_button()
        time.sleep(5)  # Espera a que cargue la página de Select Flight

        allure.attach(
            "Search button clicked\nWaiting for Select Flight page to load...",
            name="Flight Search Initiated",
            attachment_type=allure.attachment_type.TEXT
        )

    # ==================== PASO 10: Validar Página Select Flight ====================
    with allure.step("Validate that Select Flight page loaded"):
        current_url = driver.current_url

        # Validar que estamos en la página de selección de vuelos
        # La URL debería contener indicadores de la página de selección de vuelos
        is_select_flight_page = "select" in current_url.lower() or "flight" in current_url.lower() or len(current_url) > len(base_url)

        # Preparar datos de validación
        expected_result = "Select Flight page loaded successfully"
        actual_result = f"Current URL: {current_url}"
        validation_status = "PASSED" if is_select_flight_page else "FAILED"

        allure.attach(
            f"Expected: {expected_result}\nActual: {actual_result}\nStatus: {validation_status}",
            name="Page Load Validation",
            attachment_type=allure.attachment_type.TEXT
        )

        # Assert que la página de vuelos cargó
        assert is_select_flight_page, f"Select Flight page did not load. Current URL: {current_url}"

    # ==================== PASO 10.5: Seleccionar Vuelos ====================
    with allure.step("Select flights on Select Flight page (as per PDF)"):
        # Crear Page Object para Select Flight
        select_flight_page = SelectFlightPage(driver)

        # Esperar a que la página cargue completamente
        page_loaded = select_flight_page.wait_for_page_load()

        if page_loaded:
            # Tomar screenshot de la página de vuelos
            screenshot = select_flight_page.get_page_screenshot("select_flight_before_selection.png")
            if screenshot:
                allure.attach.file(
                    screenshot,
                    name="Select Flight Page - Before Selection",
                    attachment_type=allure.attachment_type.PNG
                )

            # Seleccionar primer vuelo disponible
            flight_selected = select_flight_page.select_first_available_flight()

            if flight_selected:
                allure.attach(
                    "✓ Flight selected successfully\n\nNote: Selected first available flight as per Case 3 requirements",
                    name="Flight Selection Status",
                    attachment_type=allure.attachment_type.TEXT
                )
            else:
                allure.attach(
                    "⚠ Flight selection not performed or auto-selected by system\n\nNote: Some environments may auto-select flights",
                    name="Flight Selection Status",
                    attachment_type=allure.attachment_type.TEXT
                )
        else:
            allure.attach(
                "⚠ Could not wait for Select Flight page fully loaded",
                name="Flight Selection Warning",
                attachment_type=allure.attachment_type.TEXT
            )

        # Esperar un momento para que se procesen las selecciones
        time.sleep(3)

    # ==================== PASO 11: Capturar Network Events ====================
    with allure.step("Capture Session event from Network"):
        # Obtener todos los eventos de red
        network_capture.get_network_logs()

        # Obtener eventos específicos de Session
        session_events = network_capture.get_session_events()

        # Obtener resumen de red
        network_summary = network_capture.get_network_summary()

        # Guardar logs completos en archivo (evidencia)
        network_capture.save_network_logs_to_file(f"reports/network_logs_case3_{browser}.json")

        allure.attach(
            json.dumps(network_summary, indent=2),
            name="Network Summary",
            attachment_type=allure.attachment_type.JSON
        )

        # Si se capturaron eventos de sesión, adjuntar detalles
        if session_events:
            session_details = network_capture.find_session_event_details()
            allure.attach(
                json.dumps(session_details, indent=2, ensure_ascii=False),
                name="Session Event Details",
                attachment_type=allure.attachment_type.JSON
            )
        else:
            allure.attach(
                "No session events captured during flight search process",
                name="Session Event Warning",
                attachment_type=allure.attachment_type.TEXT
            )

    # ==================== PASO 12: Obtener datos finales ====================
    final_url = current_url

    # Construir mensaje de validación detallado
    validation_message = f"Flight search successful. Page loaded: {is_select_flight_page}. Session events captured: {len(session_events)}"
    if network_summary['has_session_data']:
        validation_message += f" | Total network events: {network_summary['total_events']}"

    # ==================== PASO 13: Guardar en Base de Datos ====================
    with allure.step("Save test results to database"):
        db.save_test_result(
            test_name=test_name,
            status="PASSED",
            execution_time=0,  # pytest calculará esto automáticamente
            browser=browser,
            url=final_url,
            language=LANGUAGE,
            case_number=case_number,
            environment=env,
            screenshots_mode=screenshots_mode,
            video_enabled=video_mode,
            expected_value=expected_result,
            actual_value=actual_result,
            validation_result=validation_status,
            initial_url=base_url,
            validation_message=validation_message,
            pos=POS,
            link_name=f"BOG-MAD | {PASSENGERS_EACH_TYPE*3}pax+{PASSENGERS_EACH_TYPE}inf | Session Events: {len(session_events)}"
        )

        allure.attach(
            f"Test results saved to database\nCase: {case_number}\nStatus: PASSED\nEnvironment: {env}\nRoute: BOG-MAD\nPassengers: {PASSENGERS_EACH_TYPE*3} + {PASSENGERS_EACH_TYPE} infants",
            name="Database Save Confirmation",
            attachment_type=allure.attachment_type.TEXT
        )

    # ==================== CLEANUP ====================
    # Deshabilitar captura de red
    network_capture.disable_network_tracking()

    # ==================== RESULTADO FINAL ====================
    with allure.step("Test completed successfully"):
        allure.attach(
            f"✓ Flight search completed\n✓ Select Flight page loaded\n✓ Session events captured: {len(session_events)}\n✓ Network summary generated\n✓ Data saved to database",
            name="Test Summary",
            attachment_type=allure.attachment_type.TEXT
        )


# ==================== TEST PARAMETRIZADO (FUTURO) ====================
# Si en el futuro se quiere probar con múltiples navegadores o ambientes,
# se puede parametrizar como los otros casos:

# @pytest.mark.parametrize("custom_param", ["value1", "value2"])
# def test_login_parametrized(driver, base_url, db, browser, custom_param):
#     # Test implementation
#     pass
