# Prueba Técnica Selenium - FLYR Inc

Suite de pruebas automatizadas para la aplicación web nuxqa utilizando Selenium WebDriver, Python y pytest.

## Inicio Rápido

### Prerrequisitos
- Python 3.9+
- Navegadores Chrome, Edge y Firefox
- Git

### Configuración

```bash
# Clonar repositorio
git clone https://github.com/cesarcardona-ux/selenium-technical-test.git
cd selenium-technical-test

# Crear entorno virtual
python -m venv venv
source venv/bin/activate  # MacOS/Linux
venv\Scripts\activate     # Windows

# Instalar dependencias
pip install -r requirements.txt
```

### Gestión de Drivers

Este proyecto utiliza **Selenium Manager** (incluido en Selenium 4.6+) para descargar y gestionar automáticamente los drivers de navegadores.

**¿Qué significa esto?**
- No se necesita instalación manual de drivers
- Funciona con cualquier versión de Chrome/Edge/Firefox
- Descarga automáticamente el driver correcto cuando ejecutas los tests

**¿Por qué Selenium Manager?**
Durante el desarrollo, encontramos que Chrome se actualizó a la versión 141, pero las herramientas externas solo podían descargar drivers hasta la versión 114. Selenium Manager resuelve esto obteniendo siempre la versión correcta del driver directamente de los proveedores del navegador.

**Para evaluadores:** No necesitas descargar o configurar drivers manualmente. Solo instala los requisitos y ejecuta los tests.

## GUI Pytest Command Generator

Este proyecto incluye una aplicación GUI moderna para generar y ejecutar comandos pytest sin necesidad de escribir comandos manualmente.

### Características del GUI

- **Interfaz moderna** con CustomTkinter
- **3 paneles principales:**
  - Test Parameters: Configuración de parámetros CLI (browser, language, POS, env, etc.)
  - Pytest Flags: Opciones de ejecución (verbose, parallel, allure, etc.)
  - Test Data: Editor de datos de prueba (pasajeros, pago, facturación)
- **7 casos de prueba** configurables con parámetros específicos
- **Auto-carga de configuración** al iniciar la aplicación
- **Guardado simplificado** - 1 botón guarda toda la configuración en `testdata.json`
- **Copiar/Ejecutar comandos** con un solo clic
- **Tema claro/oscuro**

### Cómo usar el GUI

```bash
# 1. Ir al directorio
cd ide_test

# 2. Instalar dependencias (solo primera vez)
pip install -r requirements.txt

# 3. Ejecutar la aplicación
python main.py
```

**Documentación completa:** Ver [ide_test/README.md](ide_test/README.md) para guía detallada de uso.

**Restauración:** Si necesitas restaurar la versión original del GUI, consulta [RESTORE_PYTEST_GENERATOR.md](RESTORE_PYTEST_GENERATOR.md).

## Ejecutar Tests

### Ejecución Básica

```bash
# Ejecutar todos los tests implementados
pytest tests/

# Ejecutar caso específico con todas las combinaciones
pytest tests/nuxqa/test_language_change_Case4.py

# Generar reporte Allure
pytest tests/
allure serve reports/allure
```

### Opciones CLI

| Opción            | Valores                                           | Descripción                                              |
|-------------------|---------------------------------------------------|----------------------------------------------------------|
| `--browser`       | chrome, edge, firefox, all                        | Selección de navegador (por defecto: all)                |
| `--language`      | Español, English, Français, Português, all        | Selección de idioma (varía por caso)                     |
| `--pos`           | Chile, España, Francia, Peru, Otros países, all   | Selección de POS (por defecto: all)                      |
| `--header-link`   | ofertas-vuelos, credits, equipaje, all            | Selección de link de header (por defecto: all)           |
| `--footer-link`   | vuelos, noticias, aviancadirect, contactanos, all | Selección de link de footer (por defecto: all)           |
| `--env`           | qa4, qa5, uat1, all                               | Selección de ambiente (por defecto: all)                 |
| `--origin`        | BOG, MDE, CLO, MAD, etc. (códigos IATA)           | Aeropuerto de origen (Casos 1 y 3, por defecto: BOG)     |
| `--destination`   | BOG, MDE, CLO, MAD, etc. (códigos IATA)           | Aeropuerto de destino (Casos 1 y 3, por defecto: MDE)    |
| `--departure-days`| Entero (días desde hoy)                           | Offset de fecha de ida (Casos 1 y 3, por defecto: 4)     |
| `--return-days`   | Entero (días desde hoy)                           | Offset de fecha de vuelta (Caso 2 y 3, por defecto: 5)   |
| `--screenshots`   | none, on-failure, all                             | Modo de captura de screenshots (por defecto: on-failure) |
| `--video`         | none, enabled                                     | Grabación de video (por defecto: none)                   |

**Nota sobre el parámetro `--language`:**
- **Caso 4**: Por defecto es `all` (prueba los 4 idiomas)
- **Casos 6 y 7**: Por defecto es selección aleatoria de idioma por test
  - Omitir `--language` para selección aleatoria
  - Usar `--language=English` (u otro idioma) para idioma específico
  - Usar `--language=all` para probar los 4 idiomas

**Ejemplos con opciones:**
```bash
# Caso 1: Reserva Solo Ida (flujo completo con ciudades y fechas dinámicas)
pytest tests/nuxqa/test_oneway_booking_Case1.py --browser=chrome --language=Español --pos=Chile --env=qa4 --origin=BOG --destination=MDE --departure-days=4 -v

# Caso 1: Con video y screenshots para debugging
pytest tests/nuxqa/test_oneway_booking_Case1.py --browser=chrome --language=Español --pos=Chile --env=qa5 --origin=BOG --destination=MDE --departure-days=4 --video=enabled --screenshots=all --alluredir=reports/allure

# Caso 1: Ejecutar en todos los navegadores y ambientes
pytest tests/nuxqa/test_oneway_booking_Case1.py --browser=all --language=Español --pos=Chile --env=all --origin=BOG --destination=MDE --departure-days=4 -v

# Caso 4: Cambio de idioma
pytest tests/nuxqa/test_language_change_Case4.py --browser=chrome --language=English --env=qa5 --video=enabled --screenshots=all

# Caso 5: Cambio de POS
pytest tests/nuxqa/test_pos_change_Case5.py --browser=chrome --pos=Chile --env=qa5 --video=enabled --screenshots=all

# Caso 6: Redirecciones de header (idioma aleatorio)
pytest tests/nuxqa/test_header_redirections_Case6.py --browser=chrome --header-link=ofertas-vuelos --env=qa5 -v

# Caso 6: Redirecciones de header (idioma específico)
pytest tests/nuxqa/test_header_redirections_Case6.py --browser=chrome --header-link=ofertas-vuelos --env=qa5 --language=Français -v

# Caso 6: Redirecciones de header (todos los idiomas - genera 4 tests)
pytest tests/nuxqa/test_header_redirections_Case6.py --browser=chrome --header-link=ofertas-vuelos --env=qa5 --language=all -v

# Caso 7: Redirecciones de footer (idioma aleatorio)
pytest tests/nuxqa/test_footer_redirections_Case7.py --browser=chrome --footer-link=noticias --env=qa5 -v

# Caso 7: Redirecciones de footer (idioma específico)
pytest tests/nuxqa/test_footer_redirections_Case7.py --browser=chrome --footer-link=noticias --env=qa5 --language=English -v

# Caso 3: Búsqueda de vuelos y captura de red (fechas y ciudades dinámicas)
pytest tests/nuxqa/test_login_network_Case3.py --browser=chrome --origin=BOG --destination=MDE --departure-days=4 --return-days=5 --env=uat1 -v

# Caso 3: Con video y reporte Allure
pytest tests/nuxqa/test_login_network_Case3.py --browser=chrome --origin=BOG --destination=MAD --departure-days=7 --return-days=10 --env=uat1 --video=enabled --screenshots=all --alluredir=reports/allure
```

**Ejecución paralela:**
```bash
pytest tests/ -n auto
```

## Parámetros Útiles de Pytest

```bash
# -v (verbose): Muestra detalles de cada test
pytest tests/nuxqa/test_language_change_Case4.py -v

# -s (no capture): Muestra prints en tiempo real (útil para debugging)
pytest tests/nuxqa/test_oneway_booking_Case1.py --browser=chrome --language=Español --env=qa4 -v -s

# -x: Detiene ejecución al primer fallo
pytest tests/ -x

# --lf (last failed): Ejecuta solo los tests que fallaron en la última ejecución
pytest tests/ --lf

# -k: Filtra tests por nombre (ejemplo: solo tests de Chrome)
pytest tests/ -k "chrome"

# Combinación útil para debugging
pytest tests/nuxqa/test_oneway_booking_Case1.py -v -s -x
```

**Ejecución en background (segundo plano):**

```bash
# Windows - ejecuta tests en background
start /b pytest tests/ -v

# Linux/Mac - ejecuta tests en background
pytest tests/ -v &

# Ver procesos en ejecución: usar /bashes en Claude Code
```

> **⚠️ Nota:** Ejecutar en background libera la terminal pero puede dificultar ver errores en tiempo real.

## Terminar Procesos en Ejecución

Si necesitas detener todos los procesos de tests y navegadores que puedan estar ejecutándose:

### Windows
```bash
# Terminar procesos de Chrome y drivers
taskkill /F /IM chrome.exe /T
taskkill /F /IM chromedriver.exe /T

# Terminar procesos de Edge y drivers
taskkill /F /IM msedge.exe /T
taskkill /F /IM msedgedriver.exe /T

# Terminar procesos de Firefox y drivers
taskkill /F /IM firefox.exe /T
taskkill /F /IM geckodriver.exe /T

# Terminar procesos de Python/Pytest
taskkill /F /IM python.exe /T

# Comando completo para terminar todo
taskkill /F /IM chrome.exe /T & taskkill /F /IM chromedriver.exe /T & taskkill /F /IM msedge.exe /T & taskkill /F /IM msedgedriver.exe /T & taskkill /F /IM firefox.exe /T & taskkill /F /IM geckodriver.exe /T & taskkill /F /IM python.exe /T
```

### Linux/Mac
```bash
# Terminar procesos de Chrome
pkill -9 chrome
pkill -9 chromedriver

# Terminar procesos de Edge
pkill -9 msedge
pkill -9 msedgedriver

# Terminar procesos de Firefox
pkill -9 firefox
pkill -9 geckodriver

# Terminar procesos de Python
pkill -9 python

# Comando completo para terminar todo
pkill -9 chrome; pkill -9 chromedriver; pkill -9 msedge; pkill -9 msedgedriver; pkill -9 firefox; pkill -9 geckodriver; pkill -9 python
```

**Nota:** Estos comandos terminarán TODOS los procesos de navegadores y Python en tu sistema. Úsalos con precaución si tienes otras sesiones importantes abiertas.

## Estado de Casos de Prueba

| Caso   | Estado       | Descripción                            | Tests | Multi-idioma |
|--------|--------------|----------------------------------------|-------|--------------|
| Caso 1 | ✅ Completo  | Reserva Solo Ida (Flujo Completo)      |   6   | -            |
| Caso 2 | ✅ Completo  | Reserva Ida y Vuelta (Flujo Completo)  |  12   | 4 idiomas    |
| Caso 3 | ✅ Completo  | Búsqueda de Vuelos y Captura de Red    |   2   | -            |
| Caso 4 | ✅ Completo  | Validación de Cambio de Idioma         |  24   | 4 idiomas    |
| Caso 5 | ✅ Completo  | Validación de Cambio de POS            |  18   | -            |
| Caso 6 | ✅ Completo  | Redirecciones de Header (Multi-idioma) |  12   | 4 idiomas (OR logic, JSON-driven) |
| Caso 7 | ✅ Completo  | Redirecciones de Footer (Multi-idioma) |  16   | 4 idiomas (OR logic, JSON-driven) |

### Caso 1: Reserva Solo Ida ✅
- **Flujo:** Flujo de reserva completo (6 páginas)
- **Páginas:** Home → Seleccionar Vuelo → Pasajeros → Servicios → Mapa de Asientos → Pago
- **Configuración:** Idioma, POS, 4 pasajeros (1 Adulto, 1 Adolescente, 1 Niño, 1 Infante)
- **Tipo de Vuelo:** Solo ida
- **Tarifa:** Basic
- **Servicios:** Ninguno seleccionado (omitir todos)
- **Asientos:** Economy
- **Pago:** Datos de tarjeta de crédito de prueba (rechazo aceptable)
- **Navegadores:** Chrome, Edge, Firefox
- **Ambientes:** QA4, QA5
- **Total de tests:** 6 (3 navegadores × 2 ambientes)
- **Archivo:** `tests/nuxqa/test_oneway_booking_Case1.py`
- **Parámetros CLI:** `--browser`, `--language`, `--pos`, `--env`, `--origin`, `--destination`, `--departure-days`, `--video`, `--screenshots`
- **Parametrización:** 100% - Sin valores hardcodeados. Todos los valores (POS, ciudades, fechas) son dinámicos y configurables vía CLI y JSON
- **Estado:** ✅ Completado - Framework implementado, manejo de iframes, optimizaciones de tiempo, tests funcionales, parametrización completa

**Page Objects Creados:**
- `pages/nuxqa/passengers_page.py` - Formularios de información de pasajeros
- `pages/nuxqa/services_page.py` - Selección de servicios adicionales
- `pages/nuxqa/seatmap_page.py` - Selección de asientos
- `pages/nuxqa/payment_page.py` - Información de pago con manejo de iframes

**Aspectos Técnicos Destacados:**
- Automatización completa del flujo de reserva de 6 páginas
- Manejo dinámico de datos de pasajeros (4 tipos diferentes de pasajeros)
- Mecanismo de omisión de servicios
- Selección de asientos Economy
- Llenado de formulario de pago con datos de prueba
- Reportes Allure comprehensivos para cada paso
- Seguimiento en base de datos con campos específicos del caso

**Implementación Crítica de la Página de Pago:**

La página de Pago presenta desafíos únicos que requirieron manejo avanzado de iframes:

1. **Modal de Consentimiento de Cookies (Framework OneTrust):**
   - El modal aparece como overlay en la página de Pago con fondo oscuro
   - Se implementó detección de doble estrategia:
     - **Estrategia 1:** Buscar botón `#onetrust-accept-btn-handler` en el DOM principal
     - **Estrategia 2:** Si no se encuentra, buscar en iframe de OneTrust y cambiar contexto
   - Después de hacer clic en "Aceptar", retorna al contexto del DOM principal
   - El modal desaparece completamente antes de proceder con el llenado del formulario

2. **Iframe Externo de Pasarela de Pago:**
   - **Descubrimiento Crítico:** Los campos del formulario de tarjeta (Titular, Número de Tarjeta, CVV, Expiración) NO están en el DOM principal de la página de Pago
   - Los campos están alojados en un iframe externo de pasarela de pago: `api-pay.avtest.ink`
   - Clase del iframe: `payment-forms-layout_iframe`
   - Implementado por cumplimiento PCI (manejo seguro de datos de tarjeta de crédito)

3. **Estrategia de Cambio de Contexto:**
   ```
   DOM Principal → Aceptar Cookies (si está presente) → Retornar al DOM Principal →
   Cambiar a Iframe de Pago → Llenar Campos de Tarjeta → Retornar al DOM Principal →
   Llenar Campos de Facturación (email, dirección, ciudad, país)
   ```

4. **Por Qué Es Importante:**
   - Usar `driver.find_element()` directamente en la página de Pago NO encontrará los campos de tarjeta
   - Debe cambiar explícitamente al contexto del iframe: `driver.switch_to.frame(payment_iframe)`
   - Después de llenar los campos de tarjeta, debe retornar al DOM principal: `driver.switch_to.default_content()`
   - Los campos de facturación (email, dirección, ciudad, país, términos) permanecen en el DOM principal

5. **Detalles de Implementación:**
   - Espera de 15 segundos agregada para que Angular inyecte el iframe de pago en el DOM
   - Detectar iframe usando `By.CLASS_NAME, "payment-forms-layout_iframe"`
   - Esperar presencia del iframe, luego cambiar contexto
   - Llenar campos de tarjeta con esperas explícitas dentro del iframe
   - Cambiar de vuelta al DOM principal antes de llenar campos de facturación
   - Todos los cambios de contexto correctamente registrados para debugging

**Archivo:** `pages/nuxqa/payment_page.py` (líneas 97-352)

### Caso 2: Reserva Ida y Vuelta ✅
- **Flujo:** Flujo de reserva completo ida y vuelta (6 páginas)
- **Páginas:** Home → Seleccionar Vuelo (Ida + Vuelta) → Pasajeros → Servicios → Mapa de Asientos → Pago
- **Configuración:** Idioma (4 opciones), POS dinámico, 4 pasajeros (1 Adulto, 1 Adolescente, 1 Niño, 1 Infante)
- **Tipo de Vuelo:** Ida y vuelta (Round-trip)
- **Tarifas:** Basic (Ida) + Flex (Vuelta)
- **Servicios:** Avianca Lounges (si disponible), o cualquier otro servicio
- **Asientos:** Plus, Economy, Premium, Economy (si hay disponibilidad para 4 pasajeros)
- **Pago:** Llenar información pero NO enviar formulario
- **Navegadores:** Chrome, Edge, Firefox
- **Idiomas:** Español, English, Français, Português
- **Ambientes:** QA4
- **Total de tests:** 12 (3 navegadores × 4 idiomas × 1 ambiente)
- **Archivo:** `tests/nuxqa/test_roundtrip_booking_Case2.py`
- **Parámetros CLI:** `--browser`, `--language`, `--pos`, `--env`, `--origin`, `--destination`, `--departure-days`, `--return-days`, `--video`, `--screenshots`
- **Parametrización:** 100% - Multi-idioma con POS dinámico según idioma. Todos los valores configurables vía CLI y JSON
- **Estado:** ✅ Completado - Flujo completo implementado, selección de 2 vuelos (Ida y Vuelta), multi-idioma funcional

**Diferencias Clave con Caso 1:**
- **Tipo de Vuelo:** Round-trip (requiere seleccionar 2 vuelos: ida y vuelta)
- **Tarifas Mixtas:** Basic para ida + Flex para vuelta (requisito del PDF)
- **Servicios:** Debe seleccionar Avianca Lounges (no omitir como en Caso 1)
- **Asientos Variados:** Selección de diferentes tipos de asientos (Plus, Economy, Premium, Economy)
- **Multi-idioma:** Parametrizado para los 4 idiomas (Español, English, Français, Português)
- **POS Dinámico:** El POS se selecciona automáticamente según el idioma seleccionado
- **Pago:** Solo llenar formulario, NO hacer submit (a diferencia del Caso 1)

**Page Objects Utilizados:**
- `pages/nuxqa/home_page.py` - Búsqueda de vuelos ida y vuelta
- `pages/nuxqa/select_flight_page.py` - Selección de 2 vuelos (Ida Basic + Vuelta Flex)
- `pages/nuxqa/passengers_page.py` - Formularios de 4 pasajeros
- `pages/nuxqa/services_page.py` - Selección de Avianca Lounges
- `pages/nuxqa/seatmap_page.py` - Selección de 4 asientos variados
- `pages/nuxqa/payment_page.py` - Llenado de formulario de pago (sin submit)

**Aspectos Técnicos Destacados:**
- Automatización completa del flujo round-trip de 6 páginas
- Selección inteligente de 2 vuelos con tarifas diferentes (Basic ida, Flex vuelta)
- Manejo multi-idioma con POS dinámico (4 combinaciones de idioma)
- Selección de servicios específicos (Avianca Lounges con fallback)
- Estrategia de selección de asientos variados para 4 pasajeros
- Llenado completo de formulario de pago sin envío
- Reportes Allure con información de 2 vuelos seleccionados
- Seguimiento en base de datos con información de vuelo de ida y vuelta

### Caso 3: Búsqueda de Vuelos y Captura de Red ✅
- **Ambiente:** UAT1 (nuxqa.avtest.ink)
- **Idioma/POS:** Mapeo dinámico desde `parameter_options.json` (Español→Chile, English→Chile, Français→Francia, Português→Chile)
- **Búsqueda de Vuelos:** Fechas dinámicas (HOY + N días), ciudades parametrizables (códigos IATA)
- **Selección de Vuelos:** 4 clics - FLEX Ida, FLEX Vuelta
- **Pasajeros:** 9 (3 adultos + 3 adolescentes + 3 niños)
- **Captura de Red:** Chrome DevTools Protocol (CDP) para extracción de JSON de sesión
- **Campos Extraídos:** origin, destination, std, productClass (4 campos de requisitos del PDF)
- **Navegadores:** Chrome ✅, Edge ✅ (Solo basados en Chromium - limitación CDP)
- **Total de tests:** 2 (Chrome + Edge)
- **Archivo:** `tests/nuxqa/test_login_network_Case3.py`
- **Parámetros CLI:** `--browser`, `--language`, `--env`, `--origin`, `--destination`, `--departure-days`, `--return-days`, `--video`, `--screenshots`
- **Parametrización:** 100% - Sin valores hardcodeados. Mapeo idioma→POS cargado dinámicamente desde JSON, ciudades desde JSON

**Aspectos Técnicos Destacados:**
- Captura de red en tiempo real usando CDP (captura cuerpos de respuesta inmediatamente)
- Cálculo dinámico de fechas para prevenir fallos de tests en fechas futuras
- Selección compleja de vuelos con manejo de cargador de página de 25-30 segundos
- Filtrado basado en texto para vuelos de vuelta ("Choisir le tarif")
- Análisis de JSON de sesión desde estructura anidada: `response.result.data.journeys[]`
- Adjunto dedicado de Allure para campos requeridos del PDF
- 7 campos adicionales de base de datos para seguimiento del Caso 3

**Compatibilidad de Navegadores:**
- ✅ Chrome: Totalmente funcional con CDP
- ✅ Edge: Totalmente funcional con CDP
- ❌ Firefox: No soportado (CDP es solo para Chromium)

### Caso 4: Validación de Cambio de Idioma ✅
- **Idiomas:** Español, Inglés, Francés, Portugués
- **Navegadores:** Chrome, Edge, Firefox
- **Ambientes:** QA4, QA5
- **Combinaciones totales:** 24 tests
- **Archivo:** `tests/nuxqa/test_language_change_Case4.py`

### Caso 5: Validación de Cambio de POS ✅
- **POS:** Chile, España, Otros países
- **Navegadores:** Chrome, Edge, Firefox
- **Ambientes:** QA4, QA5
- **Combinaciones totales:** 18 tests
- **Archivo:** `tests/nuxqa/test_pos_change_Case5.py`

### Caso 6: Redirecciones de Header con Validación Multi-idioma ✅
- **Links de Header:** Ofertas de vuelos, Avianca Credits, Equipaje
- **Validación Multi-idioma:** Soporte completo para Español, English, Français, Português con validación OR logic
- **Configuración JSON:** Patrones de URL multi-idioma desde `parameter_options.json` (sin valores hardcodeados)
- **Language Exceptions:** Sistema dinámico de excepciones por idioma (ej: Français + credits → LifeMiles)
- **Navegadores:** Chrome, Edge, Firefox
- **Ambientes:** QA4, QA5
- **Combinaciones de tests:**
  - **Con --language=all:** 12 tests (3 links × 4 idiomas)
  - **Con todos los navegadores:** 36 tests (3 links × 4 idiomas × 3 navegadores)
  - **Máximo total:** 72 tests (3 links × 4 idiomas × 3 navegadores × 2 ambientes)
- **Archivo:** `tests/nuxqa/test_header_redirections_Case6.py`
- **Parametrización:** 100% - Patrones de validación completamente configurables desde JSON

### Caso 7: Redirecciones de Footer con Validación Multi-idioma ✅
- **Links de Footer:** Vuelos baratos, Noticias corporativas, aviancadirect, Contáctanos
- **Validación Multi-idioma:** Soporte completo para Español, English, Français, Português con validación OR logic
- **Configuración JSON:** Patrones de URL multi-idioma desde `parameter_options.json` (sin valores hardcodeados)
- **Patrones extensos:** Hasta 7 variaciones de URL por link para soportar todos los idiomas
- **Navegadores:** Chrome, Edge, Firefox
- **Ambientes:** QA4, QA5
- **Combinaciones de tests:**
  - **Con --language=all:** 16 tests (4 links × 4 idiomas)
  - **Con todos los navegadores:** 48 tests (4 links × 4 idiomas × 3 navegadores)
  - **Máximo total:** 96 tests (4 links × 4 idiomas × 3 navegadores × 2 ambientes)
- **Archivo:** `tests/nuxqa/test_footer_redirections_Case7.py`
- **Parametrización:** 100% - Patrones de validación completamente configurables desde JSON

## Implementación Técnica

### Características
- ✅ Page Object Model (POM)
- ✅ Soporte multi-navegador (Chrome, Edge, Firefox)
- ✅ Tests parametrizados con pytest
- ✅ ConfigManager y sistema de configuración JSON centralizado
- ✅ 100% parametrización - Sin valores hardcodeados
- ✅ GUI Pytest Command Generator para generar comandos fácilmente
- ✅ Reportes Allure con visualizaciones ricas
- ✅ Grabación de video (MP4 con OpenCV)
- ✅ Captura de screenshots (modos configurables)
- ✅ Base de datos SQLite para seguimiento de resultados
- ✅ Registro detallado
- ✅ Ejecución paralela (pytest-xdist)

### Estructura del Proyecto
```
├── pages/                  # Page Objects
├── tests/                  # Casos de prueba
├── utils/                  # Base de datos y utilidades
├── ide_test/               # GUI Pytest Command Generator
│   ├── gui/                # Interfaz gráfica (CustomTkinter)
│   ├── core/               # ConfigManager, CaseMapper, CommandBuilder
│   └── config/             # JSON: testdata, parameter_options, case_mappings
├── Docs/                   # Documentación adicional
├── conftest.py             # Configuración de Pytest
└── requirements.txt        # Dependencias
```

### Resultados de Tests

**Reporte Allure:**
```bash
allure serve reports/allure
```

**Base de Datos:** Los resultados de tests se guardan en `test_results.db`

### Esquema de Base de Datos

Los resultados de tests se almacenan en SQLite con **30 campos comprehensivos** para seguimiento y análisis detallado:

**Campos Generales (10):**
- `id`: Clave primaria
- `case_number`: Número de caso de prueba (1, 3, 4, 5, 6, 7) - posicionado como 2da columna para filtrado fácil
- `test_name`: Identificador único de test
- `status`: Resultado del test (PASSED, FAILED, SKIPPED)
- `execution_time`: Duración en segundos
- `error_message`: Detalles del error si falló
- `timestamp`: Fecha/hora de ejecución
- `browser`: Navegador usado (chrome, edge, firefox)
- `url`: URL final después de la acción del test
- `language`: Idioma usado en el test

**Campos de Seguimiento (7):**
- `environment`: Ambiente de prueba (qa4, qa5, uat1)
- `screenshots_mode`: Configuración de screenshots (none, on-failure, all)
- `video_enabled`: Estado de grabación de video (enabled, none)
- `expected_value`: Valor de validación esperado
- `actual_value`: Valor real obtenido
- `validation_result`: Resultado de validación (PASSED, FAILED)
- `initial_url`: URL antes de la acción del test

**Campos Específicos de Casos 4, 5, 6, 7 (6):**
- `pos`: Caso 5 - POS seleccionado (Chile, España, Otros países)
- `header_link`: Caso 6 - Link de header probado
- `footer_link`: Caso 7 - Link de footer probado
- `link_name`: Casos 6 y 7 - Nombre descriptivo del link
- `language_mode`: Casos 6 y 7 - Modo de selección de idioma (Random, Specific, All Languages)
- `validation_message`: Mensaje de validación detallado

**Campos Específicos del Caso 3 (7):**
- `origin_city`: Código IATA de aeropuerto de origen (BOG, MDE, etc.)
- `destination_city`: Código IATA de aeropuerto de destino
- `departure_date`: Fecha de salida calculada (HOY + N días)
- `return_date`: Fecha de retorno calculada (HOY + N días)
- `passenger_count`: Total de pasajeros (adultos + adolescentes + niños)
- `session_journey_count`: Número de viajes extraídos del JSON de sesión (debe ser 2)
- `session_data_json`: Datos completos de JSON de sesión con todos los campos extraídos

**Beneficios:**
- Consultas SQL avanzadas para análisis
- Trazabilidad completa de tests
- Debugging fácil con valores esperados vs reales
- Seguimiento de configuración por test
- Datos específicos del caso correctamente estructurados

**Consultas de ejemplo:**
```sql
-- Filtrar por ambiente
SELECT * FROM test_executions WHERE environment = 'qa5';

-- Filtrar por número de caso
SELECT * FROM test_executions WHERE case_number = 1;

-- Filtrar por Caso 1 y navegador específico
SELECT * FROM test_executions WHERE case_number = 1 AND browser = 'chrome';

-- Ver tiempo de ejecución promedio del Caso 1
SELECT browser, environment, AVG(execution_time) as avg_time
FROM test_executions
WHERE case_number = 1
GROUP BY browser, environment;

-- Ver todos los tests del Caso 1 con sus estados
SELECT test_name, browser, environment, status, execution_time, timestamp
FROM test_executions
WHERE case_number = 1
ORDER BY timestamp DESC;

-- Ver tests fallidos del Caso 1
SELECT test_name, browser, environment, error_message
FROM test_executions
WHERE case_number = 1 AND status = 'FAILED';

-- Filtrar por POS (Caso 5)
SELECT * FROM test_executions WHERE pos = 'Chile';

-- Filtrar por modo de idioma (Casos 6 y 7)
SELECT * FROM test_executions WHERE language_mode = 'Random';

-- Filtrar por origen/destino (Caso 3)
SELECT * FROM test_executions WHERE origin_city = 'BOG' AND destination_city = 'MDE';

-- Ver datos de sesión del Caso 3
SELECT test_name, session_journey_count, session_data_json FROM test_executions WHERE case_number = 3;
```

**Registros:** Logs de ejecución detallados en `reports/test_execution.log`

## Repositorio

https://github.com/cesarcardona-ux/selenium-technical-test

---

🤖 *Generado con Claude Code*
