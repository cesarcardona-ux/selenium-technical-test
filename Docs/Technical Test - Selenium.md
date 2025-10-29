# Technical Test - Selenium WebDriver with Python

**Quick reference guide for the automation project**

> **📚 Concepts and definitions:** See [Glossary and Definitions.md](Glossary and Definitions.md)
> **📝 Test progress log:** See [Advance Test.md](Advance Test.md)

----------------------------------------------------------

## PASO A PASO DESDE CERO

### 1. Instalar Python
- Descargar desde: https://www.python.org/downloads/
- Ejecutar instalador
- ✅ **IMPORTANTE:** Marcar "Add Python to PATH"
- Verificar instalación:
```bash
python --version
```

### 2. Crear carpeta del proyecto
```bash
# Navegar a la ubicación deseada y crear carpeta
mkdir AUTOMATICACION - SELENIUM
cd "AUTOMATICACION - SELENIUM"
```

### 3. Crear entorno virtual
```bash
python -m venv venv
```
**Objetivo:** Aislar dependencias del proyecto

### 4. Activar entorno virtual
```bash
venv\Scripts\activate
```
**Resultado:** Aparece `(venv)` al inicio del prompt

### 5. Actualizar pip (opcional, puede dar error de permisos - ignorar)
```bash
pip install --upgrade pip
```

### 6. Instalar dependencias
```bash
pip install selenium pytest pytest-xdist allure-pytest webdriver-manager
```
**Objetivo:** Instalar todas las librerías necesarias para el proyecto

### 7. Crear estructura de carpetas
```bash
mkdir pages
mkdir tests
mkdir utils
mkdir reports
mkdir Docs
```

### 8. Crear archivos de configuración
**En VSCode o editor de texto, crear los siguientes archivos en la raíz:**

**requirements.txt:**
```
selenium==4.15.2
webdriver-manager==4.0.1
pytest==7.4.3
pytest-xdist==3.5.0
allure-pytest==2.13.2
python-dotenv==1.0.0
```

**pytest.ini:** (ver archivo en el proyecto)

**conftest.py:** (ver archivo en el proyecto - contiene fixtures)

**utils/database.py:** (ver archivo en el proyecto - manejo de SQLite)

**utils/__init__.py:** (archivo vacío)

**.gitignore:** (ver archivo en el proyecto)

### 9. Verificar que todo funciona
```bash
# Con el entorno virtual activado
python -c "import selenium; import pytest; print('Todo OK')"
```

----------------------------------------------------------

## SETUP INICIAL REALIZADO

### 1. Instalación de Python
- **Versión:** Python 3.9.13
- **Verificación:** `python --version`

### 2. Entorno Virtual
```bash
python -m venv venv
venv\Scripts\activate  # Windows
```
**Por qué:** Aísla dependencias del proyecto

### 3. Dependencias Instaladas
```bash
pip install selenium pytest pytest-xdist allure-pytest webdriver-manager
```

### 4. Estructura Creada
```
proyecto/
├── Docs/           # Documentación del proyecto
│   ├── Technical Test - Selenium.md  # Esta guía
│   ├── Advance Test.md               # Registro de tests
│   └── Glossary and Definitions.md   # Glosario
├── pages/          # Page Objects (POM)
├── tests/          # Casos de prueba
├── utils/          # database.py
├── reports/        # Reportes Allure
├── conftest.py     # Fixtures de pytest
├── pytest.ini      # Config pytest
└── requirements.txt
```

----------------------------------------------------------

## ARCHIVOS CLAVE

### conftest.py
- **Qué hace:** Configuración automática de pytest
- **Fixtures:**
  - `driver`: Crea/cierra navegador para cada test
  - `base_url`: URL del ambiente
  - `db`: Conexión SQLite compartida
- **Concepto clave:** `yield` pausa, entrega recurso, luego limpia
- **Scopes:** `function` (nuevo por test) vs `session` (uno para todos)

### utils/database.py
- **Qué hace:** Guarda resultados en SQLite (requisito técnico)
- **Métodos:** `save_test_result()`, `get_all_results()`

### pytest.ini
- Configura pytest: carpeta reportes, patrón de archivos (test_*.py)

### requirements.txt
- Lista de dependencias. Instalar: `pip install -r requirements.txt`

### .gitignore
- Excluye: venv/, *.db, reports/, __pycache__/

----------------------------------------------------------

## DATOS DE LA PRUEBA

**URLs:**
- QA4: https://nuxqa4.avtest.ink/
- QA5: https://nuxqa5.avtest.ink/

**Credenciales (Caso 3):**
- Username: 21734198706
- Password: Lifemiles1

----------------------------------------------------------

## REQUISITOS TÉCNICOS (Puntaje)

- [x] Allure Reports (10 pts)
- [x] Logs detallados (5 pts)
- [x] BD SQLite (5 pts)
- [x] QA4 y QA5 (5 pts)
- [ ] Ejecución paralela - xdist (5 pts)
- [ ] Aserciones claras (5 pts)
- [ ] Video + Allure (15 pts extra)

## CASOS DE PRUEBA

1. **Caso 1 (15 pts):** One-way booking completo
2. **Caso 2 (15 pts):** Round-trip booking completo
3. **Caso 3 (10 pts):** Login + captura Network
4. **Caso 4 (5 pts):** Cambio idioma (4 idiomas)
5. **Caso 5 (5 pts):** Cambio POS (3 países)
6. **Caso 6 (5 pts):** Redirecciones Header (3 sitios)
7. **Caso 7 (5 pts):** Redirecciones Footer (4 sitios)

**Buenas prácticas valoradas:** POM, comentarios claros, nombres significativos, múltiples navegadores

----------------------------------------------------------

## COMANDOS ÚTILES

```bash
# Activar entorno
venv\Scripts\activate

# Ejecutar tests
pytest tests/

# Ejecutar en paralelo
pytest tests/ -n auto

# Generar reporte Allure
allure serve reports/allure
```

----------------------------------------------------------

## PROGRESO

### ✅ Completado
- Setup Python + entorno virtual
- Instalación de dependencias
- Estructura de carpetas
- Archivos de configuración documentados
- **Fase de aprendizaje conceptual:**
  - Comprensión de fixtures y scopes
  - Entendimiento de yield vs return
  - Concepto de teardown y ejecución garantizada
  - State contamination y cuándo usar cada scope
  - Verificación de comprensión: 85% alcanzado
  - **Estado:** Listo para comenzar implementación de tests

### ⏳ Pendiente
- Implementar 7 casos de prueba (empezar por Caso 4 - más simple)
- Configurar ejecución paralela
- Grabación de video (extra)
- Repositorio GitHub + README.md

----------------------------------------------------------

*Última actualización: Fase de aprendizaje conceptual completada. Documentación actualizada con TEARDOWN y STATE CONTAMINATION*
