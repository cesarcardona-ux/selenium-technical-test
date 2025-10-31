# Advance Test - Selenium Technical Test

**Test cases implementation log**

> **📚 Concepts and definitions:** See [Glossary and Definitions.md](Glossary and Definitions.md)
> **📖 Step by step guide:** See [Technical Test - Selenium.md](Technical Test - Selenium.md)

-------------------------------

## CASOS IMPLEMENTADOS

### Caso 4: Verificar Cambio de Idioma
**Estado:** ✅ Completado
**Objetivo:** Seleccionar los 4 idiomas y verificar que el cambio se hace correctamente
**Idiomas:** Español, Inglés, Francés, Portugués
**Navegadores:** Chrome, Edge, Firefox
**Ambientes:** QA4, QA5
**Total tests:** 24 (4 idiomas × 2 ambientes × 3 navegadores)

**Archivos implementados:**
- `pages/nuxqa/home_page.py` - Page Object con locators XPath
- `tests/nuxqa/test_language_change_Case4.py` - Test parametrizado dinámicamente

**CLI Options implementadas:**
- `--browser` (chrome | edge | firefox | all)
- `--language` (Español | English | Français | Português | all)
- `--env` (qa4 | qa5 | all)
- `--screenshots` (none | on-failure | all) - Captura de screenshots condicional
- `--video` (none | enabled) - Grabación de video en formato MP4

**Selectores utilizados:**
- `//button[contains(@class, 'dropdown_trigger')]` - Botón de idioma
- `//span[contains(text(), '{language}')]` - Opción de idioma por texto
- `//button[@class='main-header_nav-primary_item_link']//span[@class='button_label']` - Texto "Ofertas"

**Validaciones implementadas:**
- Verificación de texto esperado según idioma seleccionado
- Resultados guardados en SQLite database con campo `case_number`
- Logs detallados de cada paso
- Screenshots automáticos en fallos y opcionales en todos los pasos
- Video recording completo de ejecución (MP4 con OpenCV)

**Características técnicas:**
- Page Object Model (POM)
- Parametrización dinámica vía pytest_generate_tests
- Soporte multi-browser con CLI options
- Selenium Manager para Edge (sin webdriver-manager)
- webdriver-manager para Chrome y Firefox
- Video recording con threading (VideoRecorder class)
  - OpenCV (cv2) para creación de MP4
  - 2 FPS para evitar saturación del connection pool
  - Sanitización de nombres de archivo (Windows-compatible)
- Screenshots condicionales con Allure integration
  - Captura automática en fallos
  - Captura manual en cada paso del test
- Allure decorators avanzados
  - Tags dinámicos (browser, language, environment)
  - Labels personalizados (case_number)
  - Titles dinámicos
  - Features y Stories
- Database SQLite con campo `case_number` para tracking de casos

**Comandos de ejecución:**
```bash
# Ejecución básica (todos los browsers, idiomas y ambientes)
pytest tests/nuxqa/test_language_change_Case4.py --browser=all --language=all --env=all -v

# Con video y screenshots completos para Allure
pytest tests/nuxqa/test_language_change_Case4.py --browser=all --language=all --env=all --video=enabled --screenshots=all --alluredir=reports/allure

# Solo video, sin screenshots
pytest tests/nuxqa/test_language_change_Case4.py --browser=chrome --language=English --env=qa5 --video=enabled --screenshots=none

# Solo screenshots en fallos (default)
pytest tests/nuxqa/test_language_change_Case4.py --browser=all --language=all --env=all --screenshots=on-failure
```

-------------------------------

### Caso 5: Verificar Cambio de POS
**Estado:** ✅ Completado
**Objetivo:** Seleccionar 3 POS y verificar que el cambio se hace correctamente
**POS:** Chile, España, Otros países
**Navegadores:** Chrome, Edge, Firefox
**Ambientes:** QA4, QA5
**Total tests:** 18 (3 POS × 2 ambientes × 3 navegadores)

**Archivos implementados:**
- `pages/nuxqa/home_page.py` - Page Object con locators de POS (actualizado)
- `tests/nuxqa/test_pos_change_Case5.py` - Test parametrizado dinámicamente

**CLI Options utilizadas:**
- `--browser` (chrome | edge | firefox | all)
- `--pos` (Chile | España | Otros países | all)
- `--env` (qa4 | qa5 | all)
- `--screenshots` (none | on-failure | all) - Captura de screenshots condicional
- `--video` (none | enabled) - Grabación de video en formato MP4

**Selectores utilizados:**
- `//button[@id='pointOfSaleSelectorId']` - Botón de POS (usando ID único)
- `//span[@class='points-of-sale_list_item_label' and contains(text(), '{pos}')]` - Opción de POS por texto
- `//button[@id='pointOfSaleSelectorId']//span[@class='button_label ng-star-inserted']` - Texto del POS seleccionado

**Validaciones implementadas:**
- Verificación de POS seleccionado en el botón
- Resultados guardados en SQLite database con campo `case_number`
- Logs detallados de cada paso
- Screenshots automáticos en fallos y opcionales en todos los pasos
- Video recording completo de ejecución (MP4 con OpenCV)

**Características técnicas:**
- Reutiliza infraestructura del Caso 4 (POM, fixtures, CLI options)
- Parametrización dinámica vía pytest_generate_tests
- Soporte multi-browser heredado de conftest.py
- Allure decorators avanzados (tags, labels, dynamic titles)
- Database SQLite con tracking por caso

**Comandos de ejecución:**
```bash
# Ejecución básica (todos los browsers, POS y ambientes)
pytest tests/nuxqa/test_pos_change_Case5.py --browser=all --pos=all --env=all -v

# Con video y screenshots completos para Allure
pytest tests/nuxqa/test_pos_change_Case5.py --browser=all --pos=all --env=all --video=enabled --screenshots=all --alluredir=reports/allure

# Solo un POS específico
pytest tests/nuxqa/test_pos_change_Case5.py --browser=chrome --pos=Chile --env=qa5 --video=enabled --screenshots=all

# Ejecución paralela
pytest tests/nuxqa/test_pos_change_Case5.py --browser=all --pos=all --env=all -n auto
```

-------------------------------

### Caso 6: Redirecciones Header con Validación de Idioma
**Estado:** ✅ Completado
**Objetivo:** Usar opciones del Navbar para acceder a 3 sitios diferentes con validación de idioma
**Header Links:** Ofertas de vuelos, Avianca Credits, Equipaje
**Language Validation:** Selección de idioma (random por defecto, configurable con --language) con verificación del código en URL
**Navegadores:** Chrome, Edge, Firefox
**Ambientes:** QA4, QA5
**Total tests:**
- Por defecto: 18 (3 links × 2 ambientes × 3 navegadores × random language)
- Con --language=all: 72 (3 links × 2 ambientes × 3 navegadores × 4 idiomas)

**Archivos implementados:**
- `pages/nuxqa/home_page.py` - Page Object con locators de navbar y submenús (actualizado)
- `tests/nuxqa/test_header_redirections_Case6.py` - Test parametrizado dinámicamente

**CLI Options utilizadas:**
- `--browser` (chrome | edge | firefox | all)
- `--header-link` (ofertas-vuelos | credits | equipaje | all)
- `--env` (qa4 | qa5 | all)
- `--language` (Español | English | Français | Português | all) - **Default: random per test**
- `--screenshots` (none | on-failure | all) - Captura de screenshots condicional
- `--video` (none | enabled) - Grabación de video en formato MP4

**Selectores utilizados:**
- `//button[contains(@class, 'main-header_nav-primary_item_link')]//span[contains(text(), 'Ofertas y destinos')]` - Botón del navbar "Ofertas y destinos"
- `//button[contains(@class, 'main-header_nav-primary_item_link')]//span[contains(text(), 'Tu reserva')]` - Botón del navbar "Tu reserva"
- `//button[contains(@class, 'main-header_nav-primary_item_link')]//span[contains(text(), 'Información y ayuda')]` - Botón del navbar "Información y ayuda"
- `//span[@class='link_label' and contains(text(), 'Reserva de hoteles')]` - Link del submenú
- `//span[@class='link_label' and contains(text(), 'avianca credits')]` - Link del submenú
- `//span[@class='link_label' and contains(text(), 'Equipaje')]` - Link del submenú

**Validaciones implementadas:**
- Verificación de que la URL cambió después del click
- Validación de que la URL final contiene la parte esperada:
  - hoteles → debe contener "booking.com"
  - credits → debe contener "avianca-credits"
  - equipaje → debe contener "equipaje"
- Manejo automático de pestañas nuevas (target="_blank")
- Cierre de pestañas extras y regreso a pestaña principal
- Resultados guardados en SQLite database con campo `case_number`
- Logs detallados de cada paso con validación de URL

**Características técnicas:**
- Reutiliza infraestructura de Casos 4 y 5 (POM, fixtures, CLI options)
- Click en navbar button para abrir dropdown (no hover)
- Explicit waits (WebDriverWait) para elementos del submenú
- JavaScript click para mayor confiabilidad con links target="_blank"
- Manejo de múltiples pestañas con switch_to.window()
- Validación robusta de URLs de destino
- Parametrización dinámica vía pytest_generate_tests
- Allure decorators avanzados (tags, labels, dynamic titles)

**Comandos de ejecución:**
```bash
# Ejecución básica (todos los browsers, header links y ambientes)
pytest tests/nuxqa/test_header_redirections_Case6.py --browser=all --header-link=all --env=all -v

# Con video y screenshots completos para Allure
pytest tests/nuxqa/test_header_redirections_Case6.py --browser=all --header-link=all --env=all --video=enabled --screenshots=all --alluredir=reports/allure

# Solo un header link específico
pytest tests/nuxqa/test_header_redirections_Case6.py --browser=chrome --header-link=hoteles --env=qa5 -v

# Ejecución paralela
pytest tests/nuxqa/test_header_redirections_Case6.py --browser=all --header-link=all --env=all -n auto
```

**Desafíos técnicos resueltos:**
1. **Menú dropdown aparece con CLICK, no con hover** - Solución: Cambiar de ActionChains hover a click directo
2. **Elementos no visibles inicialmente** - Solución: Explicit waits con EC.visibility_of_element_located
3. **Selectores incorrectos inicialmente** - Solución: Inspección del HTML real del sitio y ajuste de XPath
4. **Links con target="_blank" abren pestañas nuevas** - Solución: Detección automática y cambio a nueva pestaña
5. **Validación débil (solo verificaba cambio de URL)** - Solución: Validación robusta que verifica URL esperada

-------------------------------

### Caso 7: Redirecciones Footer con Validación de Idioma
**Estado:** ✅ Completado
**Objetivo:** Usar links del footer para acceder a 4 sitios diferentes con validación de idioma
**Footer Links:** Vuelos baratos, Noticias corporativas, aviancadirect, Contáctanos
**Language Validation:** Selección de idioma (random por defecto, configurable con --language) con verificación del código en URL
**Navegadores:** Chrome, Edge, Firefox
**Ambientes:** QA4, QA5
**Total tests:**
- Por defecto: 24 (4 links × 2 ambientes × 3 navegadores × random language)
- Con --language=all: 96 (4 links × 2 ambientes × 3 navegadores × 4 idiomas)

**Archivos implementados:**
- `pages/nuxqa/home_page.py` - Page Object con locators de footer (actualizado)
- `tests/nuxqa/test_footer_redirections_Case7.py` - Test parametrizado dinámicamente

**CLI Options utilizadas:**
- `--browser` (chrome | edge | firefox | all)
- `--footer-link` (vuelos | noticias | aviancadirect | contactanos | all)
- `--env` (qa4 | qa5 | all)
- `--language` (Español | English | Français | Português | all) - **Default: random per test**
- `--screenshots` (none | on-failure | all) - Captura de screenshots condicional
- `--video` (none | enabled) - Grabación de video en formato MP4

**Selectores utilizados:**
- `//span[@class='link-label' and contains(text(), 'Vuelos baratos')]` - Link del footer
- `//span[@class='link-label' and contains(text(), 'Trabaja con nosotros')]` - Link del footer
- `//span[@class='link-label' and contains(text(), 'aviancadirect')]` - Link del footer
- `//span[@class='link-label' and contains(text(), 'Artículos restringidos')]` - Link del footer

**Validaciones implementadas:**
- Verificación de que la URL cambió después del click
- Validación multi-parte de URL final (similar a Case 6):
  - vuelos → debe contener "ofertas-destinos" y "ofertas-de-vuelos"
  - trabajos → debe contener "jobs.avianca.com"
  - aviancadirect → debe contener "portales-aliados" y "aviancadirect-ndc"
  - articulos → debe contener "ayuda.avianca.com" y "/hc/"
- Manejo automático de pestañas nuevas (target="_blank")
- Cierre de pestañas extras y regreso a pestaña principal
- Resultados guardados en SQLite database con campo `case_number`
- Logs detallados de cada paso con validación de URL

**Características técnicas:**
- Reutiliza infraestructura de Casos 4, 5 y 6 (POM, fixtures, CLI options)
- Scroll automático hacia el footer para visibilidad del elemento
- Explicit waits (WebDriverWait) para elementos del footer
- JavaScript click para mayor confiabilidad con links externos
- Manejo de múltiples pestañas con switch_to.window()
- Validación robusta multi-parte de URLs de destino
- Parametrización dinámica vía pytest_generate_tests
- Allure decorators avanzados (tags, labels, dynamic titles)

**Comandos de ejecución:**
```bash
# Ejecución básica (todos los browsers, footer links y ambientes)
pytest tests/nuxqa/test_footer_redirections_Case7.py --browser=all --footer-link=all --env=all -v

# Con video y screenshots completos para Allure
pytest tests/nuxqa/test_footer_redirections_Case7.py --browser=all --footer-link=all --env=all --video=enabled --screenshots=all --alluredir=reports/allure

# Solo un footer link específico
pytest tests/nuxqa/test_footer_redirections_Case7.py --browser=chrome --footer-link=vuelos --env=qa5 -v

# Ejecución paralela
pytest tests/nuxqa/test_footer_redirections_Case7.py --browser=all --footer-link=all --env=all -n auto
```

**Desafíos técnicos resueltos:**
1. **Footer no visible inicialmente** - Solución: Scroll automático hacia el footer con JavaScript
2. **Elementos del footer tardan en cargar** - Solución: Explicit waits con EC.visibility_of_element_located
3. **Links externos abren en nueva pestaña** - Solución: Detección automática y switch a nueva pestaña
4. **Diferentes dominios de destino** - Solución: Validación multi-parte adaptada a cada link (internos y externos)

-------------------------------

### Caso 3: Flight Search & Network Session Capture
**Estado:** ✅ Completado
**Objetivo:** Realizar búsqueda de vuelos y capturar evento Session del Network usando CDP
**Environment:** UAT1 (nuxqa.avtest.ink)
**Language/POS:** French, France
**Navegadores:** Chrome ✅, Edge ✅ (Firefox ❌ - CDP no soportado)
**Total tests:** 2 (Chrome + Edge)

**Archivos implementados:**
- `pages/nuxqa/login_page.py` - Page Object heredando de HomePage (configuración idioma/POS + búsqueda vuelos)
- `pages/nuxqa/select_flight_page.py` - Page Object para selección de vuelos con plan FLEX
- `utils/network_capture.py` - Utilidad para capturar tráfico de red usando Chrome DevTools Protocol (CDP)
- `tests/nuxqa/test_login_network_Case3.py` - Test parametrizado dinámicamente con captura de red

**CLI Options implementadas:**
- `--browser` (chrome | edge) - Firefox no soporta CDP
- `--env` (uat1) - Ambiente UAT1 específico para Case 3
- `--origin` (BOG | MDE | CLO | MAD | etc.) - Código IATA del aeropuerto de origen
- `--destination` (BOG | MDE | CLO | MAD | etc.) - Código IATA del aeropuerto de destino
- `--departure-days` (4) - Días desde HOY para fecha de salida
- `--return-days` (5) - Días desde HOY para fecha de regreso
- `--screenshots` (none | on-failure | all) - Captura de screenshots condicional
- `--video` (none | enabled) - Grabación de video en formato MP4

**Selectores utilizados:**

*Login Page (heredados de HomePage):*
- `//button[contains(@class, 'dropdown_trigger')]` - Botón de idioma
- `//span[contains(text(), 'Français')]` - Selección de idioma Francés
- `//button[@id='pointOfSaleSelectorId']` - Botón de POS
- `//span[contains(text(), 'France')]` - Selección de POS France

*Formulario de búsqueda (LoginPage):*
- `//span[@class='label_text' and contains(text(), 'Aller-retour')]` - Tipo de viaje: ida y vuelta
- `//input[@id='originBtn']` - Botón de origen (con fix de visibilidad JavaScript)
- `//input[@id='departureStationInputId']` - Input de búsqueda origen
- `//input[@id='arrivalStationInputId']` - Input de búsqueda destino
- `//div[@id='{IATA_CODE}']` - Selección de aeropuerto por código IATA (BOG, MDE, etc.)
- `//div[contains(@class, 'ngb-dp-day')]//span[contains(text(), ' {day} ')]` - Selección de día (dinámico)
- `//button[contains(@class, 'ui-num-ud_button') and contains(@class, 'plus')]` - Botones + para pasajeros
- `//button[contains(@class, 'control_options_selector_action_button')]//span[contains(text(), 'Confirmer')]` - Confirmar pasajeros
- `//button[@id='searchButton']` - Botón de búsqueda

*Select Flight Page:*
- `button.journey_price_button` - Botones de vuelos disponibles
- `button.fare_button` - Botones de planes tarifarios (Basic, Classic, Flex)
- `div.page-loader` - Loader de página (avión en movimiento)
- Filtro por texto: `"Choisir le tarif"` - Para identificar vuelos de vuelta visibles

**Validaciones implementadas:**
- ✅ Configuración correcta de idioma (Francés) y POS (France)
- ✅ Selección dinámica de fechas (TODAY + N días) para evitar fallos futuros
- ✅ Selección de aeropuertos por código IATA con mapeo interno
- ✅ Configuración de 9 pasajeros (3 adultos + 3 teens + 3 children + 0 infants)
- ✅ Selección de vuelo de IDA + plan FLEX (click 1 y 2)
- ✅ Espera de 25-30 segundos del page loader (avión en movimiento)
- ✅ Scroll automático a 80% de página para ver vuelos de vuelta
- ✅ Filtrado de vuelos de vuelta por texto "Choisir le tarif" (evita seleccionar vuelos ocultos de ida)
- ✅ Selección de vuelo de VUELTA + plan FLEX (click 3 y 4)
- ✅ Captura de evento Session usando CDP
- ✅ Extracción de 4 campos específicos del JSON del PDF:
  1. `origin` - Aeropuerto de origen
  2. `destination` - Aeropuerto de destino
  3. `std` - Standard Departure Time
  4. `productClass` - Clase del producto (FLEX)
- ✅ Navegación de estructura JSON anidada: `response.result.data.journeys[]`
- ✅ Validación de 2 journeys (ida y vuelta) en el JSON
- ✅ Resultados guardados en SQLite con 7 campos adicionales del Case 3
- ✅ Logs detallados de captura de red y extracción de campos
- ✅ Allure report con attachment dedicado para los 4 campos del PDF

**Características técnicas:**
- **Page Object Model (POM)**:
  - LoginPage hereda de HomePage para reutilizar métodos de idioma/POS
  - SelectFlightPage maneja selección compleja de vuelos con timeouts largos
  - NetworkCapture clase dedicada para CDP
- **Chrome DevTools Protocol (CDP)**:
  - `driver.execute_cdp_cmd('Network.enable', {})` - Habilita monitoreo de red
  - Captura en tiempo real de response bodies (evita problemas de cache de Chrome)
  - Filtrado de eventos "Session" por URL y mimeType JSON
  - Almacenamiento inmediato de bodies en diccionario `session_response_bodies`
- **Parametrización dinámica**:
  - Fechas calculadas dinámicamente: `datetime.now() + timedelta(days=N)`
  - Códigos IATA mapeados a strings de búsqueda: `{"BOG": "Bogo", "MDE": "Mede"}`
  - CLI permite cambiar origen, destino y fechas sin modificar código
- **Manejo de timing crítico**:
  - Page loader (avión): `WebDriverWait(driver, 40).until(EC.invisibility_of_element_located())`
  - Espera de 10 segundos adicionales para renderizado completo de vuelos de vuelta
  - Timeouts extendidos: 25 segundos para fare buttons de vuelta
- **Estrategias de selección robustas**:
  - JavaScript para forzar visibilidad del botón origen (CSS hidden)
  - Filtrado por texto "Choisir le tarif" para evitar clicks en elementos ocultos
  - Scroll automático a 80% para traer vuelos de vuelta al viewport
- **Extracción de JSON compleja**:
  - Parseo de estructura anidada: `response → result → data → journeys[]`
  - Iteración sobre múltiples response bodies capturados
  - Búsqueda de body con 2 journeys (completo) vs 1 journey (parcial)
  - Extracción de arrays: `fares[]` (paxCode, id, productClass), `segments[]` (etd, status, std)
- **Database SQLite extendida**:
  - 7 nuevos campos Case 3: origin_city, destination_city, departure_date, return_date, passenger_count, session_journey_count, session_data_json
  - Total campos: 30 (antes: 23)
- **Allure decorators avanzados**:
  - Tags dinámicos (browser, environment, case_number)
  - Attachment dedicado "🎯 PDF REQUIRED FIELDS" con formato limpio
  - Separación clara entre debug info y campos requeridos del PDF
  - Configuración detallada en attachment "Configuration"

**Comandos de ejecución:**
```bash
# Ejecución básica (Chrome, BOG→MDE, 4 días ida, 5 días vuelta)
pytest tests/nuxqa/test_login_network_Case3.py --browser=chrome --origin=BOG --destination=MDE --departure-days=4 --return-days=5 --env=uat1 -v

# Edge con diferentes ciudades y fechas
pytest tests/nuxqa/test_login_network_Case3.py --browser=edge --origin=BOG --destination=MAD --departure-days=7 --return-days=10 --env=uat1 -v

# Con video y screenshots completos para Allure
pytest tests/nuxqa/test_login_network_Case3.py --browser=chrome --origin=BOG --destination=MDE --departure-days=4 --return-days=5 --env=uat1 --video=enabled --screenshots=all --alluredir=reports/allure

# Ambos browsers (Chrome + Edge)
pytest tests/nuxqa/test_login_network_Case3.py --browser=all --origin=BOG --destination=MDE --departure-days=4 --return-days=5 --env=uat1 -v
```

**Desafíos técnicos resueltos:**

1. **Botón de origen no visible inicialmente**
   - **Problema:** Después de seleccionar POS France, el botón origen tenía `is_displayed(): False` y `location: {'x': 0, 'y': 0}`
   - **Solución:** Forzar visibilidad con JavaScript antes del click
   ```python
   self.driver.execute_script("arguments[0].style.display='block'; arguments[0].style.visibility='visible';", origin_btn)
   self.driver.execute_script("arguments[0].click();", origin_btn)
   ```

2. **Modal de pasajeros se abre automáticamente**
   - **Problema:** Intentar hacer click en botón de pasajeros cerraba el modal
   - **Descubrimiento:** El modal se abre AUTOMÁTICAMENTE después de seleccionar fechas
   - **Solución:** Eliminar click en botón, solo esperar 3 segundos a que se abra solo

3. **Exceso de pasajeros causa error "Code 101"**
   - **Problema:** 12 pasajeros (3+3+3+3) causaba error y redirect a home
   - **Solución:** Reducir a 9 pasajeros (3 adultos + 3 teens + 3 children + 0 infants)

4. **Vuelos de vuelta no aparecen o se seleccionan vuelos incorrectos**
   - **Problema:** Después de seleccionar FLEX para ida, había 62 botones `journey_price_button` en DOM (ocultos de ida + visibles de vuelta)
   - **Timing:** Page loader de 25-30 segundos con animación de avión
   - **Ubicación:** Vuelos de vuelta están DEBAJO del calendario (scroll necesario)
   - **Solución multi-paso:**
     1. Esperar a que `div.page-loader` desaparezca (40s timeout)
     2. Scroll a 80% de altura de página
     3. Esperar 10 segundos adicionales para renderizado completo
     4. **Filtrar por texto "Choisir le tarif"** para obtener SOLO botones visibles de vuelta
   ```python
   return_flight_buttons = []
   for btn in all_journey_buttons:
       if btn.is_displayed() and "Choisir le tarif" in btn.text:
           return_flight_buttons.append(btn)
   ```

5. **Response bodies vacíos al intentar capturarlos después**
   - **Problema:** Chrome descarta response bodies del cache cuando se intenta capturar DESPUÉS del evento
   - **Solución:** Capturar response body INMEDIATAMENTE cuando se recibe el evento `Network.responseReceived`
   ```python
   if message['method'] == 'Network.responseReceived':
       request_id = message.get('params', {}).get('requestId')
       if request_id and 'application/json' in mime_type:
           response_body = self.driver.execute_cdp_cmd('Network.getResponseBody', {'requestId': request_id})
           self.session_response_bodies[request_id] = response_body.get('body', '')
   ```

6. **Estructura JSON anidada compleja**
   - **Problema:** Campos del PDF están en: `response.result.data.journeys[].{origin, destination, std, fares[].productClass}`
   - **Solución:** Navegación progresiva con verificaciones:
   ```python
   response_json = json.loads(body_content)
   session_data = response_json
   if 'result' in response_json:
       session_data = response_json['result']
       if 'data' in session_data:
           session_data = session_data['data']
   journeys = session_data.get('journeys', [])
   ```

7. **Primeras responses tienen solo 1 journey (ida), queremos 2 (ida + vuelta)**
   - **Problema:** CDP captura múltiples responses, primeras contienen solo vuelo de ida
   - **Solución:** Continuar iterando sobre responses capturadas hasta encontrar una con 2 journeys
   ```python
   if len(journeys) == 1:
       logger.info("Only 1 journey found, continuing to search for complete session with 2 journeys...")
       continue  # Seguir buscando
   ```

8. **Reporte Allure con demasiada información**
   - **Problema:** Usuario no encontraba los 4 campos del PDF entre tanta información de debug
   - **Solución:** Crear attachment dedicado "🎯 PDF REQUIRED FIELDS" con SOLO los 4 campos
   ```python
   pdf_fields = "   📋 PDF REQUIRED FIELDS - Session JSON Extraction\n"
   pdf_fields += f"  1. origin: {journey.get('origin')}\n"
   pdf_fields += f"  2. destination: {journey.get('destination')}\n"
   pdf_fields += f"  3. std: {journey.get('std')}\n"
   pdf_fields += f"  4. productClass: {product_class}\n"
   allure.attach(pdf_fields, name="🎯 PDF REQUIRED FIELDS", attachment_type=allure.attachment_type.TEXT)
   ```

9. **Compatibilidad con Firefox**
   - **Problema:** `AssertionError: Unrecognised command executeCdpCommand`
   - **Causa:** Firefox no soporta Chrome DevTools Protocol (CDP es exclusivo de Chromium)
   - **Resultado:** ❌ Firefox no soportado (limitación técnica esperada)
   - **Alternativa potencial:** BrowserMob Proxy o HAR file export (no implementado)

10. **Database schema sin columnas de Case 3**
    - **Problema:** `sqlite3.OperationalError: table test_executions has no column named origin_city`
    - **Causa:** Database existente con schema antiguo de 23 campos
    - **Solución:** Eliminar database antigua para permitir recreación con schema de 30 campos
    ```bash
    rm test_results.db
    ```

**Browser Compatibility Testing:**
- ✅ **Chrome**: PASSED (142.26s) - CDP funcional, 2 journeys extraídos
- ✅ **Edge**: PASSED (142.26s) - CDP funcional (basado en Chromium), 2 journeys extraídos
- ❌ **Firefox**: FAILED (esperado) - CDP no soportado, error en `execute_cdp_cmd`

**Key Learnings:**
- CDP solo funciona con navegadores Chromium (Chrome, Edge, Opera, Brave)
- Response bodies deben capturarse en tiempo real (Chrome los descarta del cache)
- Elementos visibles (`is_displayed()`) ≠ elementos en DOM (`find_elements`)
- Page loaders de larga duración (25-30s) requieren timeouts extendidos (40s)
- Filtrado por texto es más confiable que filtrado por índice para elementos dinámicos
- Estructura JSON puede tener múltiples niveles de wrapping (result → data → content)
- APIs incrementales retornan datos parciales primero, datos completos después

-------------------------------

### Caso 1: Booking One-way
**Estado:** ⏳ Pendiente
**Objetivo:** Realizar booking de solo ida completo
**Páginas:**
- Home: Idioma, POS, origen, destino, 1 pasajero de cada tipo
- Select flight: Tarifa Basic
- Passengers: Información de pasajeros
- Services: No seleccionar ninguno
- Seatmap: Asiento economy
- Payments: Pago con tarjeta fake (puede ser rechazado)

-------------------------------

### Caso 2: Booking Round-trip
**Estado:** ⏳ Pendiente
**Objetivo:** Realizar booking de ida y vuelta completo
**Páginas:**
- Home: Idioma, POS, origen, destino, 1 pasajero de cada tipo
- Select flight: Tarifa Basic (ida) y Flex (vuelta)
- Passengers: Información de pasajeros
- Services: Avianca Lounges (o cualquier otro si no disponible)
- Seatmap: Plus, Economy, Premium, Economy (si disponible)
- Payments: Llenar información pero NO enviar

-------------------------------

## NOTAS TÉCNICAS

### Gestión de Drivers: Selenium Manager

**¿Qué se usa?**
- Selenium Manager (incluido en Selenium 4.6+)
- No requiere instalación de librerías adicionales

**¿Por qué este cambio?**
Durante el desarrollo, Chrome se actualizó a la versión 141. Las herramientas externas solo podían descargar drivers hasta la versión 114, causando errores de compatibilidad. Selenium Manager resuelve esto descargando automáticamente el driver correcto de cualquier versión.

**Ventajas:**
- Funciona con cualquier versión de navegador
- No requiere configuración manual
- Solución oficial de Selenium

**Para más detalles técnicos:** Ver [Glossary and Definitions.md](Glossary and Definitions.md) - Sección "SELENIUM MANAGER"

-------------------------------

### Orden de Implementación Recomendado
1. Caso 4 (simple - cambio idioma)
2. Caso 5 (simple - cambio POS)
3. Caso 6 (medio - navbar)
4. Caso 7 (medio - footer)
5. Caso 3 (medio - login + network)
6. Caso 1 (complejo - one-way)
7. Caso 2 (complejo - round-trip)

### Elementos a Documentar por Cada Test
- Archivo creado (ubicación)
- Page Objects creados (si aplica)
- Selectores utilizados
- Validaciones implementadas
- Problemas encontrados y soluciones

### Estado Actual
- **Fase conceptual:** ✅ Completada (85% comprensión alcanzado)
- **Repositorio GitHub:** ✅ Configurado y actualizado (https://github.com/cesarcardona-ux/selenium-technical-test)
- **Fase de implementación:** ✅ En progreso (71% completado)
- **Casos completados:** 5/7 (Cases 3, 4, 5, 6, 7 con video evidence)
  - ✅ Case 3: Flight Search & Network Capture (UAT1, CDP)
  - ✅ Case 4: Language Change Validation (24 tests)
  - ✅ Case 5: POS Change Validation (18 tests)
  - ✅ Case 6: Header Redirections (18 tests)
  - ✅ Case 7: Footer Redirections (24 tests)
- **Total Tests:** 86 combinaciones (2 + 24 + 18 + 18 + 24)
- **Database:** ✅ SQLite con 30 campos comprehensivos (extendida de 23)
- **Video Evidence:** ✅ Implementado
  - Grabación MP4 con OpenCV
  - Screenshots condicionales (none, on-failure, all)
  - Integración completa con Allure
- **Network Capture:** ✅ Chrome DevTools Protocol (CDP) implementado
  - Captura en tiempo real
  - Extracción de JSON complejo
  - Compatible con Chrome y Edge
- **CLI Parameters:** 12 opciones configurables
- **Próximos pasos:**
  - Implementar Caso 1 (One-way Booking - complejo)
  - Implementar Caso 2 (Round-trip Booking - complejo)

-------------------------------

## CONFIGURACIÓN DE GIT Y GITHUB

### Paso 1: Verificar si existe repositorio Git
```bash
git status
```
**Resultado esperado:** Si no existe → "fatal: not a git repository"

-------------------------------

### Paso 2: Verificar .gitignore
Asegurarse que el archivo `.gitignore` existe y contiene:
```
# Entorno virtual
venv/
env/

# Python
__pycache__/
*.pyc

# Base de datos
*.db
*.sqlite

# Reportes
reports/
allure-results/

# IDEs
.vscode/
.idea/
.claude/
```

**Propósito:** Evitar subir archivos innecesarios o sensibles a GitHub

-------------------------------

### Paso 3: Inicializar repositorio Git local
```bash
git init
```
**Qué hace:** Crea carpeta oculta `.git/` que trackea todos los cambios

**Resultado:** "Initialized empty Git repository in..."

-------------------------------

### Paso 4: Crear repositorio en GitHub (web)

**Instrucciones:**
1. Ir a https://github.com
2. Login con tu cuenta
3. Click en **"+"** → **"New repository"**
4. Configuración:
   - **Repository name:** `selenium-technical-test` (o nombre deseado)
   - **Description:** "Technical test - Selenium WebDriver automation for Avianca"
   - **Public:** ✅ (para que evaluadores puedan verlo)
   - **NO marcar:** "Add a README file"
   - **NO marcar:** "Add .gitignore"
   - **NO marcar:** "Choose a license"
5. Click en **"Create repository"**
6. **Copiar la URL** que aparece: `https://github.com/cesarcardona-ux/selenium-technical-test.git`

-------------------------------

### Paso 5: Conectar repositorio local con GitHub
```bash
git remote add origin https://github.com/cesarcardona-ux/selenium-technical-test.git
```
**Qué hace:** Conecta tu carpeta local con el repositorio en GitHub

**Verificar conexión:**
```bash
git remote -v
```
**Resultado:** Debe mostrar la URL del repositorio (fetch y push)

-------------------------------

### Paso 6: Preparar archivos para primer commit

**Ver qué archivos serán agregados:**
```bash
git status
```
**Verificar:** venv/, *.db, reports/ NO deben aparecer (están en .gitignore)

**Agregar todos los archivos al staging area:**
```bash
git add .
```
**Advertencias sobre LF/CRLF son normales en Windows** (ignorar)

-------------------------------

### Paso 7: Crear primer commit
```bash
git commit -m "Initial commit: Project setup and configuration"
```
**Qué hace:** Guarda un "snapshot" de todos los archivos preparados

**Resultado:** Debe mostrar cantidad de archivos y líneas agregadas

-------------------------------

### Paso 8: Subir archivos a GitHub
```bash
git branch -M main
git push -u origin main
```
**Qué hace:**
- `git branch -M main`: Renombra rama a "main" (estándar actual)
- `git push -u origin main`: Sube todos los archivos a GitHub

**Resultado:** "Branch 'main' set up to track 'origin/main'"

-------------------------------

### Paso 9: Verificar en GitHub
Abrir navegador → Ir a la URL del repositorio → Actualizar página

**Debe aparecer:**
- Estructura de carpetas (Docs/, utils/, pages/, tests/)
- Archivos de configuración (conftest.py, pytest.ini, requirements.txt)
- Documentación (.md files)

**NO debe aparecer:**
- venv/ (entorno virtual)
- *.db (bases de datos)
- reports/ (reportes temporales)

-------------------------------

### Comandos para futuras actualizaciones

Cada vez que hagas cambios y quieras actualizar GitHub:

```bash
# 1. Ver qué archivos cambiaron
git status

# 2. Agregar cambios
git add .

# 3. Crear commit con mensaje descriptivo
git commit -m "Descripción de los cambios"

# 4. Subir a GitHub
git push
```

**Ejemplos de mensajes de commit:**
- "Add test case 4: Language change validation"
- "Implement HomePage Page Object"
- "Fix selector for language dropdown"
- "Update documentation with test results"

-------------------------------

*Última actualización: Repositorio GitHub configurado. Listo para implementación de tests*
