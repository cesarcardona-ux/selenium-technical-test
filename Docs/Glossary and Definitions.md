# Glosario y Definiciones - Selenium + Pytest

**Conceptos técnicos clave del proyecto**

------------------------------------------

## PYTHON

**Qué es:** Lenguaje de programación de alto nivel

**Para qué se usa en este proyecto:** Escribir los scripts de automatización y tests

**Versión del proyecto:** Python 3.9.13

------------------------------------------

## PIP

**Qué es:** Gestor de paquetes de Python (Package Installer for Python)

**Para qué sirve:** Instalar, actualizar y desinstalar librerías de Python

**Comandos básicos:**
```bash
pip install selenium      # Instala una librería
pip install --upgrade pip # Actualiza pip
pip list                  # Lista librerías instaladas
pip freeze                # Lista con versiones exactas
```

**En el proyecto:** Se usa para instalar selenium, pytest, allure-pytest, etc.

------------------------------------------

## VIRTUAL ENVIRONMENT (Entorno Virtual)

**Qué es:** Entorno aislado de Python con sus propias librerías

**Para qué sirve:** Evitar conflictos entre versiones de librerías de diferentes proyectos

**Problema que resuelve:**
- Proyecto A necesita selenium 4.15
- Proyecto B necesita selenium 3.0
- Sin entorno virtual: solo puedes tener una versión instalada
- Con entorno virtual: cada proyecto tiene su propia versión

**Crear entorno virtual:**
```bash
python -m venv venv  # Crea carpeta "venv" con Python aislado
```

**Activar entorno virtual:**
```bash
# Windows:
venv\Scripts\activate

# Linux/Mac:
source venv/bin/activate
```

**Resultado:** Aparece `(venv)` en el prompt

**Desactivar:**
```bash
deactivate
```

**Importante:**
- Cada proyecto debe tener su propio entorno virtual
- El entorno virtual NO se sube a Git (está en .gitignore)
- Otras personas crean su propio entorno con `pip install -r requirements.txt`

------------------------------------------

## SELENIUM WEBDRIVER

**Qué es:** Biblioteca de Python que permite automatizar navegadores web

**Para qué sirve:** Controlar navegadores de forma programática (sin intervención humana)

**Qué puede hacer:**
- Abrir páginas web
- Hacer clicks en botones
- Llenar formularios
- Extraer información de páginas
- Tomar screenshots
- Navegar entre páginas
- Validar contenido

**Instalación:**
```bash
pip install selenium
```

**Uso básico:**
```python
from selenium import webdriver

driver = webdriver.Chrome()
driver.get("https://google.com")
driver.quit()
```

**Componentes principales:**
- `webdriver`: Módulo principal
- `driver`: Objeto que controla el navegador
- Métodos comunes: `get()`, `find_element()`, `click()`, `send_keys()`, `quit()`

**Diferencia con otros tools:**
- **Selenium:** Automatización completa del navegador (simula usuario real)
- **Requests:** Solo hace peticiones HTTP (no ejecuta JavaScript, no renderiza)
- **Beautiful Soup:** Solo parsea HTML (no interactúa con la página)

------------------------------------------

## PYTEST

**Qué es:** Librería de Python para escribir y ejecutar pruebas automáticas

**Para qué sirve:** Automatizar verificación de que el código funciona correctamente

**Cómo funciona:**
1. Busca archivos `test_*.py`
2. Encuentra funciones `test_*()`
3. Ejecuta fixtures necesarias
4. Corre cada test
5. Reporta resultados (PASSED/FAILED/SKIPPED)

**Convención de nombres:**
- Archivos: `test_*.py`
- Funciones: `test_*()`

**Ejecutar:**
```bash
pytest                # Todos los tests
pytest tests/         # Solo carpeta tests
pytest test_login.py  # Un archivo específico
```

**Aserciones (validaciones):**
```python
assert resultado == 4  # Si True → PASSED, si False → FAILED
```

------------------------------------------

## FIXTURE

**Qué es:** Función especial de pytest que prepara recursos para tests

**Para qué:** Evitar repetir código de preparación en cada test

**Cómo se identifica:**
- Lleva decorador `@pytest.fixture`
- Nombre libre (tú lo decides)

**Cómo funciona:**
```python
@pytest.fixture
def driver():
    driver = webdriver.Chrome()
    yield driver
    driver.quit()

def test_ejemplo(driver):  # Pide fixture como parámetro
    driver.get("https://...")
```

**Parámetros válidos en fixtures:**
- Otras fixtures (las que defines)
- Objetos especiales de pytest: `request`, `config`, `monkeypatch`, `tmpdir`, `capsys`, etc.
- **NO puede tener parámetros arbitrarios** (nombre, edad, etc.)

**SCOPE ("alcance" o "duración de vida" de la fixture. Define CUÁNDO se crea y CUÁNDO se destruye la fixture.):**
- `scope="function"`: 
    Cuándo se crea:     Antes de CADA test individual 
    Cuándo se destruye: Después de CADA test individual 

    @pytest.fixture(scope="function")
    def driver():
        print(">>> Abriendo navegador")
        driver = webdriver.Chrome()
        yield driver
        print(">>> Cerrando navegador")
        driver.quit()

    def test_login(driver):
        print("Test login ejecutándose")
        
    def test_logout(driver):
        print("Test logout ejecutándose")

    Uso: Cuando cada test necesita un estado limpio (ej: navegador nuevo)

- `scope="class"`:    Una por clase de tests
    Cuándo se crea:     Antes de la PRIMERA función de una clase 
    Cuándo se destruye: Después de la ÚLTIMA función de esa clase 

    @pytest.fixture(scope="class")
    def driver():
        print(">>> Abriendo navegador")
        driver = webdriver.Chrome()
        yield driver
        print(">>> Cerrando navegador")
        driver.quit()

    class TestLogin:
        def test_login_correcto(self, driver):
            print("Test login correcto")
            
        def test_login_incorrecto(self, driver):
            print("Test login incorrecto")

    class TestLogout:
        def test_logout(self, driver):
            print("Test logout")

- `scope="module"`:   Una por archivo
    Cuándo se crea:     Al inicio del ARCHIVO de test 
    Cuándo se destruye: Al final del ARCHIVO de test

    # archivo: test_login.py

    @pytest.fixture(scope="module")
    def driver():
        print(">>> Abriendo navegador")
        driver = webdriver.Chrome()
        yield driver
        print(">>> Cerrando navegador")
        driver.quit()

    def test_login(driver):
        print("Test 1")
        
    def test_logout(driver):
        print("Test 2")
        
    def test_profile(driver):
        print("Test 3")

- `scope="session"`:  Una para toda la sesión de tests (ej: base de datos)
    Cuándo se crea:     Al inicio de TODA la sesión de pytest 
    Cuándo se destruye: Al final de TODA la sesión de pytest Ejemplo visual:
    # conftest.py

    @pytest.fixture(scope="session")
    def db():
        print(">>> Conectando a base de datos")
        database = TestDatabase()
        yield database
        print(">>> Cerrando base de datos")
        database.close()

    # test_login.py
    def test_login(db):
        print("Test login")
        
    # test_products.py  
    def test_productos(db):
        print("Test productos")
        
    # test_checkout.py
    def test_checkout(db):
        print("Test checkout")

**yield vs return:**
- `return`: Entrega valor y **TERMINA la ejecución** - no hay código después
- `yield`: Entrega valor, **PAUSA**, espera que termine el test, luego **CONTINÚA** (limpieza)

```python
# CON RETURN - NO HAY TEARDOWN
@pytest.fixture
def driver():
    driver = webdriver.Chrome()
    return driver
    driver.quit()  # ❌ NUNCA SE EJECUTA (código después de return es inalcanzable)

# CON YIELD - SÍ HAY TEARDOWN
@pytest.fixture
def driver():
    driver = webdriver.Chrome()  # SETUP
    yield driver                 # PAUSA - entrega al test
    driver.quit()                # ✅ TEARDOWN - se ejecuta después del test
```

**Importante:** Después de `return`, la función termina inmediatamente. El código que sigue nunca se ejecuta.

------------------------------------------

## TEARDOWN

**Qué es:** Fase de limpieza que se ejecuta DESPUÉS de que un test termina

**Dónde ocurre:** En fixtures, después del `yield`

**Cuándo se ejecuta:** SIEMPRE, incluso si el test falla

**Fases de una fixture:**
```python
@pytest.fixture
def driver():
    # FASE 1: SETUP (preparación)
    print(">>> Abriendo navegador")
    driver = webdriver.Chrome()
    driver.implicitly_wait(10)

    # FASE 2: YIELD (pausa - entrega recurso)
    yield driver  # Aquí pytest PAUSA la fixture y ejecuta el test

    # FASE 3: TEARDOWN (limpieza)
    print(">>> Cerrando navegador")
    driver.quit()  # Se ejecuta SIEMPRE, incluso si test falló
```

**Ejecución visual:**
```
1. pytest inicia test
2. Ejecuta SETUP de fixture → abre navegador
3. PAUSA en yield → entrega driver al test
4. Ejecuta el test → puede PASAR o FALLAR
5. Continúa después del yield → ejecuta TEARDOWN
6. Cierra navegador SIEMPRE
```

**Ejemplo con fallo:**
```python
def test_login(driver):
    driver.get("https://wrong-url")
    assert 1 == 2  # ❌ TEST FALLA
    # ¿Se ejecuta driver.quit()?  → SÍ ✅

# Output:
# >>> Abriendo navegador
# TEST FAILED
# >>> Cerrando navegador  ← Teardown se ejecutó a pesar del fallo
```

**Recursos comunes que necesitan teardown:**
- **Navegador:** `driver.quit()`
- **Base de datos:** `db.close()`, `connection.commit()`
- **Archivos:** `file.close()`
- **Conexiones API:** `session.close()`
- **Carpetas temporales:** `shutil.rmtree(temp_folder)`

**Diferencia importante:**
- `.quit()` es una **ACCIÓN** (método que cierra navegador)
- Teardown es una **FASE** (momento en que se ejecuta esa acción)
- La acción `.quit()` puede ejecutarse en cualquier momento
- Pero en fixtures, se ejecuta durante la fase de TEARDOWN

------------------------------------------

## STATE CONTAMINATION (Contaminación de Estado)

**Qué es:** Problema que ocurre cuando datos de un test afectan a otro test

**Por qué es un problema:** Tests deben ser independientes (resultado no debe depender de orden de ejecución)

**Ejemplo concreto con cookies:**
```python
# ❌ PROBLEMA: scope="session" para driver
@pytest.fixture(scope="session")
def driver():
    driver = webdriver.Chrome()
    yield driver
    driver.quit()

def test_login(driver):
    driver.get("https://example.com/login")
    # Usuario inicia sesión → se crea cookie de sesión
    driver.find_element(By.ID, "username").send_keys("user")
    driver.find_element(By.ID, "password").send_keys("pass")
    driver.find_element(By.ID, "login").click()
    # Cookie guardada: session_id=abc123

def test_debe_pedir_login(driver):
    driver.get("https://example.com/dashboard")
    # ❌ FALLA: Cookie de test anterior PERSISTE
    # Navegador ya está autenticado → no pide login
    # Test debería ver página de login pero ve dashboard
```

**Consecuencia:** `test_debe_pedir_login` pasa o falla dependiendo del orden de ejecución

**Solución: scope="function"**
```python
# ✅ SOLUCIÓN: Navegador nuevo para cada test
@pytest.fixture(scope="function")
def driver():
    driver = webdriver.Chrome()
    yield driver
    driver.quit()  # Cierra navegador → borra cookies/sesiones

def test_login(driver):
    # Navegador limpio
    pass

def test_debe_pedir_login(driver):
    # Navegador NUEVO limpio (sin cookies del test anterior) ✅
    pass
```

**Otros ejemplos de contaminación:**
- **LocalStorage/SessionStorage** persistiendo datos
- **Caché de navegador** mostrando contenido antiguo
- **Formularios pre-llenados** con datos de test anterior
- **Estado de aplicación** (carrito de compra, filtros aplicados, etc.)

**Cuándo usar cada scope:**
- `scope="function"` → Para navegador (necesita estado limpio)
- `scope="session"` → Para base de datos (conexión se puede reutilizar)

**Pregunta clave:** ¿Si reutilizo este recurso, puede afectar resultados de otros tests?
- SÍ → `scope="function"`
- NO → `scope="session"` (más eficiente)

------------------------------------------

## HOOK

**Qué es:** Función con nombre especial que pytest llama automáticamente en momentos específicos

**Cómo se identifica:**
- Nombre empieza con `pytest_`
- NO lleva decorador
- Nombre debe ser exacto (de la lista oficial de pytest)

**Ejemplos de hooks:**
```python
# Se ejecuta después de cada test
def pytest_runtest_makereport(item, call):
    if call.excinfo is not None:  # Test falló
        # Guardar screenshot
        pass

# Se ejecuta al inicio de la sesión
def pytest_sessionstart(session):
    print("Iniciando tests")

# Se ejecuta al final de la sesión
def pytest_sessionfinish(session):
    print("Finalizando tests")
```

**Parámetros en hooks:**
- Firma fija definida por pytest
- NO puedes cambiar parámetros
- Consultar documentación del hook específico

**Diferencia con fixture:**
- Fixture: TÚ la llamas (como parámetro)
- Hook: PYTEST la llama automáticamente

------------------------------------------

## CHROME, CHROMEDRIVER Y DRIVER

### Chrome (Navegador)
**Qué es:** Aplicación de Google instalada en el computador

**Ubicación:** `C:\Program Files\Google\Chrome\Application\chrome.exe`

**Qué hace:** Muestra páginas web, permite navegación manual

------------------------------------------

### ChromeDriver (Intermediario)
**Qué es:** Archivo ejecutable (.exe) que traduce comandos de Selenium a acciones en Chrome

**Ubicación:** Carpeta temporal (auto-descarga con webdriver-manager)

**Qué hace:** Recibe instrucciones de Selenium → las ejecuta en Chrome

**Analogía:** Intérprete entre Selenium (Python) y Chrome (navegador)

**Importante:** Cada versión de Chrome necesita ChromeDriver compatible (webdriver-manager lo gestiona automáticamente)

------------------------------------------

### driver (Objeto Python)
**Qué es:** Variable en el código que representa la conexión activa al navegador

**Tipo:** Objeto de la clase `webdriver.Chrome()`

**Qué hace:** Permite controlar el navegador desde Python

**Flujo:**
```
Código Python (driver) → ChromeDriver → Chrome
```

**Ejemplo:**
```python
driver = webdriver.Chrome()  # Crea conexión
driver.get("https://...")    # Navega
driver.find_element(...)     # Busca elementos
driver.quit()                # Cierra navegador
```

------------------------------------------

## SELENIUM CON OTROS NAVEGADORES

**Navegadores soportados:**

| Navegador | Driver       | Clase Selenium        |
|-----------|--------------|-----------------------|
| Chrome    | ChromeDriver | `webdriver.Chrome()`  |
| Firefox   | GeckoDriver  | `webdriver.Firefox()` |
| Edge      | EdgeDriver   | `webdriver.Edge()`    |
| Safari    | SafariDriver | `webdriver.Safari()`  |

**Patrón:**
```
CHROME:   Python → ChromeDriver → Chrome
FIREFOX:  Python → GeckoDriver → Firefox
EDGE:     Python → EdgeDriver → Edge
```

**Lo que cambia:**
- Import del driver manager
- Clase del Service
- Clase del webdriver

**El código de test es idéntico** para todos los navegadores

**Instalación:**
```bash
pip install webdriver-manager  # Soporta todos los navegadores
```

**Requisito:** Tener el navegador instalado en el sistema

------------------------------------------

## PAGE OBJECT MODEL (POM)

**Qué es:** Patrón de diseño que separa lógica de prueba de elementos de página

**Estructura:**
- `pages/` → Clases que representan cada página web
- `tests/` → Casos de prueba que usan las páginas

**Beneficio:** Código más limpio, reutilizable y mantenible

**Ejemplo:**
```python
# pages/login_page.py
class LoginPage:
    def __init__(self, driver):
        self.driver = driver

    def login(self, user, password):
        # Lógica de login aquí
        pass

# tests/test_login.py
def test_login(driver):
    page = LoginPage(driver)
    page.login("user", "pass")
```

------------------------------------------

## ESPERAS IMPLÍCITAS

**Qué es:** Tiempo que Selenium espera antes de fallar al buscar un elemento

**Configuración:**
```python
driver.implicitly_wait(10)  # Espera hasta 10 segundos
```

**Cuándo se usa:** Elementos que tardan en cargar (AJAX, animaciones, etc.)

**Funcionamiento:** Si un elemento no se encuentra inmediatamente, Selenium reintenta durante N segundos antes de lanzar error

------------------------------------------

## REQUEST (Parámetro Especial)

**Qué es:** Objeto de pytest con información del test que solicita la fixture

**Atributos útiles:**
- `request.node.name` → Nombre del test
- `request.param` → Parámetros si la fixture es parametrizada
- `request.config` → Configuración de pytest

**Uso en fixture:**
```python
@pytest.fixture
def driver(request):
    test_name = request.node.name
    print(f"Test {test_name} pidió el driver")
    # ...
```

------------------------------------------

## SQLITE

**Qué es:** Base de datos ligera que se guarda en un solo archivo (.db)

**Ventajas:**
- No requiere servidor (como MySQL o PostgreSQL)
- Perfecta para datos locales

**En el proyecto:** Almacena resultados de ejecuciones de tests (requisito técnico)

------------------------------------------

## ALLURE REPORTS

**Qué es:** Sistema de reportes visuales y detallados para pruebas

**Ventaja:** Genera reportes HTML con gráficos, pasos, screenshots

**Configuración en pytest.ini:**
```ini
addopts = --alluredir=reports/allure
```

**Generar reporte:**
```bash
allure serve reports/allure
```

------------------------------------------

## XDIST (Ejecución Paralela)

**Qué es:** Plugin de pytest para ejecutar tests en paralelo

**Beneficio:** Reduce tiempo total de ejecución

**Instalación:**
```bash
pip install pytest-xdist
```

**Uso:**
```bash
pytest -n auto  # Usa todos los cores disponibles
pytest -n 4     # Usa 4 workers
```

------------------------------------------

## WEBDRIVER-MANAGER

**Qué es:** Librería que descarga automáticamente drivers de navegadores

**Ventaja:** No necesitas descargar manualmente ChromeDriver, GeckoDriver, etc.

**Uso:**
```python
from webdriver_manager.chrome import ChromeDriverManager

service = Service(ChromeDriverManager().install())
driver = webdriver.Chrome(service=service)
```

**Soporta:** Chrome, Firefox, Edge, Opera, IE

------------------------------------------

## CONFTEST.PY

**Qué es:** Archivo especial de pytest para configuración compartida

**Características:**
- Se ejecuta automáticamente antes de los tests
- No necesita ser importado
- pytest lo busca y carga solo
- Define fixtures y hooks compartidos

**Ubicación:** Raíz del proyecto

------------------------------------------

## PYTEST.INI

**Qué es:** Archivo de configuración de pytest

**Formato:** INI (clave=valor)

**Configuraciones comunes:**
- `testpaths`: Dónde buscar tests
- `python_files`: Patrón de archivos (test_*.py)
- `addopts`: Opciones por defecto
- `markers`: Etiquetas personalizadas

------------------------------------------

## .GITIGNORE

**Qué es:** Archivo que le dice a Git qué NO subir al repositorio

**Propósito:** Evitar subir archivos innecesarios/sensibles

**Categorías comunes:**
- Entornos virtuales: venv/, env/
- Cache Python: __pycache__/, *.pyc
- Bases de datos: *.db, *.sqlite
- Reportes temporales: reports/
- IDEs: .vscode/, .idea/

------------------------------------------

## GIT

**Qué es:** Sistema de control de versiones

**Para qué sirve:** Rastrear cambios en el código a lo largo del tiempo

**Conceptos clave:**
- **Repositorio:** Carpeta con historial de cambios
- **Commit:** Captura de cambios en un momento específico
- **Branch:** Línea de desarrollo independiente

**Comandos básicos:**
```bash
git init                    # Inicializa repositorio
git add .                   # Prepara archivos para commit
git commit -m "mensaje"     # Guarda cambios con mensaje
git status                  # Ve estado actual
git log                     # Ve historial de commits
```

**Flujo básico:**
```
1. Haces cambios en archivos
2. git add . (preparas cambios)
3. git commit -m "mensaje" (guardas snapshot)
4. git push (subes a GitHub)
```

------------------------------------------

## GITHUB

**Qué es:** Plataforma web para alojar repositorios de Git

**Para qué sirve:**
- Almacenar código en la nube
- Colaborar con otros desarrolladores
- Compartir código con terceros (como en esta prueba técnica)

**Diferencia con Git:**
- **Git:** Software local en tu computadora
- **GitHub:** Servicio web que usa Git

**Comandos para GitHub:**
```bash
git remote add origin <URL>  # Conecta repo local con GitHub
git push -u origin main      # Sube cambios a GitHub
git pull                     # Descarga cambios de GitHub
git clone <URL>              # Descarga repo completo
```

**En la prueba técnica:** Se requiere crear repo en GitHub y compartir el enlace

------------------------------------------

## REQUIREMENTS.TXT

**Qué es:** Archivo de texto que lista todas las dependencias del proyecto

**Formato:**
```
selenium==4.15.2
pytest==7.4.3
allure-pytest==2.13.2
```

**Para qué sirve:**
- Documentar qué librerías usa el proyecto
- Permitir que otros instalen las mismas versiones
- Garantizar reproducibilidad del entorno

**Crear requirements.txt:**
```bash
pip freeze > requirements.txt
```

**Instalar desde requirements.txt:**
```bash
pip install -r requirements.txt
```

**Buena práctica:** Especificar versiones exactas (con ==) para evitar incompatibilidades

------------------------------------------

## VSCODE (Visual Studio Code)

**Qué es:** Editor de código (IDE ligero)

**Para qué se usa:** Escribir y editar código Python, archivos de configuración, etc.

**Alternativas:** PyCharm, Sublime Text, Atom, Vim

**Ventajas para Python:**
- Resaltado de sintaxis
- Autocompletado
- Terminal integrada
- Extensiones para pytest, Git, etc.

------------------------------------------

*Última actualización: Agregados conceptos de TEARDOWN, STATE CONTAMINATION y explicaciones detalladas de yield vs return*
