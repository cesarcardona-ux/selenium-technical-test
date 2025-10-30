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

### Caso 6: Redirecciones Header
**Estado:** ✅ Completado
**Objetivo:** Usar opciones del Navbar para acceder a 3 sitios diferentes
**Header Links:** Reserva de hoteles (booking.com), Avianca Credits, Equipaje
**Navegadores:** Chrome, Edge, Firefox
**Ambientes:** QA4, QA5
**Total tests:** 18 (3 links × 2 ambientes × 3 navegadores)

**Archivos implementados:**
- `pages/nuxqa/home_page.py` - Page Object con locators de navbar y submenús (actualizado)
- `tests/nuxqa/test_header_redirections_Case6.py` - Test parametrizado dinámicamente

**CLI Options utilizadas:**
- `--browser` (chrome | edge | firefox | all)
- `--header-link` (hoteles | credits | equipaje | all)
- `--env` (qa4 | qa5 | all)
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

### Caso 7: Redirecciones Footer
**Estado:** ⏳ Pendiente
**Objetivo:** Usar links del footer para acceder a 4 sitios diferentes
**Validación:** URLs cargan correctamente según idioma y sitio seleccionado

-------------------------------

### Caso 3: Login en UAT1
**Estado:** ⏳ Pendiente
**Objetivo:** Realizar login y capturar campos del Network
**Detalles:**
- Login con credenciales específicas
- Seleccionar idioma: Francés, POS: France
- Capturar evento "Session" desde DevTools > Network

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
- **Repositorio GitHub:** ✅ Configurado (https://github.com/cesarcardona-ux/selenium-technical-test)
- **Fase de implementación:** ✅ En progreso
- **Casos completados:** 3/7 (Cases 4, 5 y 6 con video evidence)
- **Video Evidence:** ✅ Implementado
  - Grabación MP4 con OpenCV
  - Screenshots condicionales
  - Integración completa con Allure
- **Próximo paso:** Implementar Caso 7 (Redirecciones Footer)

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
