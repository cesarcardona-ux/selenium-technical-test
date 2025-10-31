"""
network_capture.py - Utilidad para capturar tráfico de red usando Chrome DevTools Protocol

Este módulo proporciona funcionalidad para capturar eventos de red durante la ejecución de tests.
Utiliza el Chrome DevTools Protocol (CDP) disponible en Selenium 4.

Caso 3: Captura del evento "Session" durante el proceso de login.

Conceptos clave:
- CDP (Chrome DevTools Protocol): API para controlar Chrome a bajo nivel
- Network Domain: Área del CDP que maneja eventos de red
- Request/Response: Eventos que se disparan en cada petición HTTP
"""

# ==================== IMPORTS ====================
import logging
import json
from selenium.webdriver.common.log import Log
from selenium.common.exceptions import WebDriverException

# ==================== LOGGER ====================
logger = logging.getLogger(__name__)

# ==================== CLASE ====================
class NetworkCapture:
    """
    Clase para capturar tráfico de red usando CDP.

    Responsabilidades:
    - Habilitar el Network Domain del CDP
    - Capturar todos los eventos de red (requests/responses)
    - Filtrar eventos específicos (como "Session")
    - Almacenar los datos capturados para análisis
    """

    def __init__(self, driver):
        """
        Constructor: Inicializa el capturador de red.

        Args:
            driver: Instancia de Selenium WebDriver (debe ser Chrome)

        Nota: CDP solo funciona con Chrome/Edge (navegadores Chromium)
        """
        self.driver = driver
        self.network_events = []  # Lista para almacenar todos los eventos capturados
        self.session_events = []  # Lista específica para eventos "Session"
        self.session_response_bodies = {}  # Dict para guardar response bodies de session events (key: requestId, value: body)
        self.enabled = False
        logger.info("NetworkCapture object initialized")

    def enable_network_tracking(self):
        """
        Habilita el rastreo de red usando CDP.

        Proceso:
        1. Ejecuta comando CDP para habilitar Network domain
        2. Marca como habilitado para futuras operaciones

        Importante:
        - Debe llamarse ANTES de navegar a la página
        - Solo funciona con Chrome/Edge
        """
        try:
            # Ejecuta comando CDP: Network.enable
            # Esto activa el monitoreo de todas las peticiones de red
            self.driver.execute_cdp_cmd('Network.enable', {})
            self.enabled = True
            logger.info("Network tracking enabled via CDP")
        except WebDriverException as e:
            logger.error(f"Failed to enable network tracking: {str(e)}")
            logger.error("CDP may not be supported by this browser (use Chrome or Edge)")
            raise

    def disable_network_tracking(self):
        """
        Deshabilita el rastreo de red.

        Debe llamarse al finalizar la captura para liberar recursos.
        """
        try:
            if self.enabled:
                self.driver.execute_cdp_cmd('Network.disable', {})
                self.enabled = False
                logger.info("Network tracking disabled")
        except WebDriverException as e:
            logger.warning(f"Error disabling network tracking: {str(e)}")

    def get_network_logs(self):
        """
        Obtiene todos los logs de red del navegador.

        Returns:
            list: Lista de eventos de red capturados

        Proceso:
        - Lee los logs del tipo 'performance' que contienen eventos de red
        - Filtra solo eventos relacionados con Network
        """
        try:
            # Obtiene logs de performance (contiene eventos de red)
            logs = self.driver.get_log('performance')

            for log_entry in logs:
                try:
                    # Parsea el mensaje JSON del log
                    log_message = json.loads(log_entry['message'])

                    # Solo nos interesan eventos de Network
                    if 'message' in log_message:
                        message = log_message['message']
                        if 'method' in message and message['method'].startswith('Network'):
                            self.network_events.append(message)

                            # Si el evento es relevante para "Session", lo guardamos aparte
                            if self._is_session_event(message):
                                self.session_events.append(message)
                                logger.info(f"Session event captured: {message['method']}")

                                # Si es una respuesta JSON, intentar capturar el body INMEDIATAMENTE
                                if message['method'] == 'Network.responseReceived':
                                    request_id = message.get('params', {}).get('requestId')
                                    response = message.get('params', {}).get('response', {})
                                    mime_type = response.get('mimeType', '')

                                    # Solo intentar con respuestas JSON
                                    if request_id and 'application/json' in mime_type:
                                        try:
                                            response_body = self.driver.execute_cdp_cmd('Network.getResponseBody', {'requestId': request_id})
                                            body_content = response_body.get('body', '')
                                            if body_content:
                                                self.session_response_bodies[request_id] = body_content
                                                logger.info(f"✓ Response body captured for requestId: {request_id}")
                                        except Exception as e:
                                            logger.warning(f"Could not capture body for requestId {request_id}: {str(e)[:100]}")

                except json.JSONDecodeError:
                    continue  # Ignora logs que no sean JSON válido

            logger.info(f"Total network events captured: {len(self.network_events)}")
            logger.info(f"Total session events captured: {len(self.session_events)}")

            return self.network_events

        except Exception as e:
            logger.error(f"Error getting network logs: {str(e)}")
            return []

    def _is_session_event(self, event):
        """
        Determina si un evento de red está relacionado con "Session".

        Args:
            event: Diccionario con datos del evento de red

        Returns:
            bool: True si es un evento de sesión

        Criterios:
        - URL contiene la palabra "session"
        - MimeType es application/json (para respuestas de API)
        - NO es un archivo JavaScript (.js)
        - Request/Response contiene datos de sesión
        - Headers contienen tokens de sesión
        """
        try:
            # Verifica el método del evento
            method = event.get('method', '')

            # Busca en diferentes tipos de eventos de red
            if method == 'Network.responseReceived':
                # Analiza la respuesta HTTP
                response = event.get('params', {}).get('response', {})
                url = response.get('url', '').lower()
                mime_type = response.get('mimeType', '').lower()

                # EXCLUSIÓN: NO incluir archivos JavaScript
                if url.endswith('.js'):
                    return False

                # Verifica si la URL contiene "session" Y es JSON
                if 'session' in url and 'application/json' in mime_type:
                    return True

                # Verifica headers que puedan contener sesión (solo para JSON)
                if 'application/json' in mime_type:
                    headers = response.get('headers', {})
                    for header_name, header_value in headers.items():
                        if 'session' in header_name.lower() or 'session' in str(header_value).lower():
                            return True

            elif method == 'Network.requestWillBeSent':
                # Analiza la petición HTTP
                request = event.get('params', {}).get('request', {})
                url = request.get('url', '').lower()

                # EXCLUSIÓN: NO incluir archivos JavaScript
                if url.endswith('.js'):
                    return False

                # Verifica si la URL contiene "session"
                if 'session' in url:
                    return True

            return False

        except Exception as e:
            logger.warning(f"Error checking session event: {str(e)}")
            return False

    def get_session_events(self):
        """
        Obtiene solo los eventos relacionados con Session.

        Returns:
            list: Lista de eventos de sesión capturados
        """
        # Asegura que tenemos los logs más recientes
        self.get_network_logs()
        return self.session_events

    def find_session_event_details(self):
        """
        Extrae detalles específicos del primer evento de Session encontrado.

        Returns:
            dict: Diccionario con detalles del evento de sesión o None

        Información extraída:
        - URL del evento
        - Método HTTP (GET, POST, etc.)
        - Status code
        - Headers relevantes
        - Request/Response body si está disponible
        """
        session_events = self.get_session_events()

        if not session_events:
            logger.warning("No session events found")
            return None

        # Toma el primer evento de sesión
        first_event = session_events[0]

        details = {
            'method': first_event.get('method'),
            'params': first_event.get('params', {})
        }

        # Extrae información según el tipo de evento
        if details['method'] == 'Network.responseReceived':
            response = details['params'].get('response', {})
            details['url'] = response.get('url')
            details['status'] = response.get('status')
            details['statusText'] = response.get('statusText')
            details['headers'] = response.get('headers', {})
            details['mimeType'] = response.get('mimeType')

        elif details['method'] == 'Network.requestWillBeSent':
            request = details['params'].get('request', {})
            details['url'] = request.get('url')
            details['httpMethod'] = request.get('method')
            details['headers'] = request.get('headers', {})
            details['postData'] = request.get('postData')

        logger.info(f"Session event details: {details}")
        return details

    def save_network_logs_to_file(self, filename="network_logs.json"):
        """
        Guarda todos los eventos de red en un archivo JSON.

        Args:
            filename: Nombre del archivo de salida

        Útil para:
        - Análisis posterior de todos los eventos
        - Debugging de problemas de red
        - Documentación de evidencia
        """
        try:
            with open(filename, 'w', encoding='utf-8') as f:
                json.dump(self.network_events, f, indent=2, ensure_ascii=False)
            logger.info(f"Network logs saved to {filename}")
            logger.info(f"Total events saved: {len(self.network_events)}")
        except Exception as e:
            logger.error(f"Error saving network logs: {str(e)}")

    def get_network_summary(self):
        """
        Genera un resumen de la actividad de red capturada.

        Returns:
            dict: Resumen con estadísticas de red

        Información incluida:
        - Total de eventos
        - Total de requests
        - Total de responses
        - Eventos de sesión
        """
        total_events = len(self.network_events)
        requests = sum(1 for e in self.network_events if e.get('method') == 'Network.requestWillBeSent')
        responses = sum(1 for e in self.network_events if e.get('method') == 'Network.responseReceived')
        session_count = len(self.session_events)

        summary = {
            'total_events': total_events,
            'total_requests': requests,
            'total_responses': responses,
            'session_events': session_count,
            'has_session_data': session_count > 0
        }

        logger.info(f"Network summary: {summary}")
        return summary

    def extract_session_fields(self):
        """
        Extrae los 4 campos específicos del JSON del evento Session.

        Returns:
            dict: Diccionario con los campos extraídos o None si no se encuentran

        Campos extraídos:
        1. closingCheckInDate
        2. fares[].paxCode y fares[].id (primer elemento)
        3. openingCheckInDate
        4. segments[].etd, segments[].status, segments[].std (todos los segmentos)
        """
        session_events = self.get_session_events()

        if not session_events:
            logger.warning("No session events found for field extraction")
            return None

        # Buscar eventos de respuesta (Network.responseReceived) que contengan datos de sesión
        response_events = [e for e in session_events if e.get('method') == 'Network.responseReceived']

        if not response_events:
            logger.warning("No responseReceived events found in session events")
            return None

        # Intentar con cada evento de respuesta hasta encontrar uno con body capturado
        for event in response_events:
            try:
                # Obtener el requestId del evento
                request_id = event.get('params', {}).get('requestId')
                if not request_id:
                    continue

                # Buscar el body en el diccionario de bodies capturados
                body_content = self.session_response_bodies.get(request_id)

                if not body_content:
                    logger.info(f"No captured body for requestId: {request_id}")
                    continue

                logger.info(f"Using captured response body for requestId: {request_id}")

                # Parsear el JSON
                response_json = json.loads(body_content)

                # Muchas APIs envuelven los datos en un campo 'result' o 'data'
                # Verificar si hay un campo 'result' que contenga los datos
                session_data = response_json
                if 'result' in response_json:
                    session_data = response_json['result']
                    if isinstance(session_data, dict):
                        # Si 'result' contiene 'data', usar ese campo
                        if 'data' in session_data and isinstance(session_data['data'], dict):
                            session_data = session_data['data']

                # Los campos están dentro de 'journeys' array
                journeys = session_data.get('journeys', [])

                if not journeys:
                    logger.info(f"Body for requestId {request_id} does not contain 'journeys' array, trying next...")
                    continue

                logger.info(f"✓ Found body with journeys array ({len(journeys)} journeys) for requestId: {request_id}")

                # Si solo hay 1 journey y hay más response bodies, intentar con el siguiente
                # (el primer body puede tener solo el vuelo de ida, el segundo ambos vuelos)
                if len(journeys) == 1:
                    logger.info(f"Only 1 journey found, will try next response body if available...")

                # Extraer los 4 campos específicos de TODOS los journeys
                extracted_fields = {
                    'journeys': [],
                    'requestId': request_id
                }

                for journey_idx, journey in enumerate(journeys):
                    journey_data = {
                        'journey_index': journey_idx,
                        'origin': journey.get('origin'),
                        'destination': journey.get('destination'),
                        'std': journey.get('std'),
                        'closingCheckInDate': journey.get('closingCheckInDate'),
                        'openingCheckInDate': journey.get('openingCheckInDate'),
                        'fares': [],
                        'segments': []
                    }

                    # Extraer fares (paxCode, id, productClass)
                    fares_array = journey.get('fares', [])
                    for fare in fares_array:
                        journey_data['fares'].append({
                            'paxCode': fare.get('paxCode'),
                            'id': fare.get('id'),
                            'productClass': fare.get('productClass')
                        })

                    # Extraer segments (etd, status, std)
                    segments_array = journey.get('segments', [])
                    for segment in segments_array:
                        journey_data['segments'].append({
                            'etd': segment.get('etd'),
                            'status': segment.get('status'),
                            'std': segment.get('std')
                        })

                    extracted_fields['journeys'].append(journey_data)

                logger.info(f"✓ Session fields extracted successfully")
                logger.info(f"  - Total journeys: {len(extracted_fields['journeys'])}")
                for idx, journey in enumerate(extracted_fields['journeys']):
                    logger.info(f"  - Journey [{idx}]: {journey['origin']} → {journey['destination']}")
                    logger.info(f"    - closingCheckInDate: {journey['closingCheckInDate']}")
                    logger.info(f"    - openingCheckInDate: {journey['openingCheckInDate']}")
                    logger.info(f"    - std: {journey['std']}")
                    logger.info(f"    - fares count: {len(journey['fares'])}")
                    logger.info(f"    - segments count: {len(journey['segments'])}")

                # Si solo hay 1 journey, continuar buscando uno con 2 journeys
                if len(extracted_fields['journeys']) == 1:
                    logger.info("Only 1 journey extracted, continuing to search for complete session with 2 journeys...")
                    continue

                # Si llegamos aquí, tenemos 2+ journeys (ida y vuelta completos)
                return extracted_fields

            except json.JSONDecodeError as e:
                logger.warning(f"Failed to parse JSON for requestId {request_id}: {e}")
                continue
            except Exception as e:
                logger.warning(f"Error extracting fields for requestId {request_id}: {e}")
                continue

        logger.error("Could not extract session fields from any response event")
        return None

    def clear_events(self):
        """
        Limpia todos los eventos capturados.

        Útil para:
        - Iniciar captura limpia para un nuevo test
        - Evitar mezclar eventos de diferentes acciones
        """
        self.network_events.clear()
        self.session_events.clear()
        self.session_response_bodies.clear()
        logger.info("All captured events cleared")
