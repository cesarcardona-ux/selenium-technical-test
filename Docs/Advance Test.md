# Advance Test - Selenium Technical Test

**Test cases implementation log**

> **📚 Concepts and definitions:** See [Glossary and Definitions.md](Glossary and Definitions.md)
> **📖 Step by step guide:** See [Technical Test - Selenium.md](Technical Test - Selenium.md)

-------------------------------

## CASOS IMPLEMENTADOS

### Caso 4: Verificar Cambio de Idioma (5 pts)
**Estado:** ⏳ Pendiente
**Objetivo:** Seleccionar los 4 idiomas y verificar que el cambio se hace correctamente
**Idiomas:** Español, Inglés, Francés, Portugués

-------------------------------

### Caso 5: Verificar Cambio de POS (5 pts)
**Estado:** ⏳ Pendiente
**Objetivo:** Seleccionar 3 POS y verificar que el cambio se hace correctamente
**POS:** Otros países, España, Chile

-------------------------------

### Caso 6: Redirecciones Header (5 pts)
**Estado:** ⏳ Pendiente
**Objetivo:** Usar opciones del Navbar para acceder a 3 sitios diferentes
**Validación:** URLs cargan correctamente según idioma y sitio seleccionado

-------------------------------

### Caso 7: Redirecciones Footer (5 pts)
**Estado:** ⏳ Pendiente
**Objetivo:** Usar links del footer para acceder a 4 sitios diferentes
**Validación:** URLs cargan correctamente según idioma y sitio seleccionado

-------------------------------

### Caso 3: Login en UAT1 (10 pts)
**Estado:** ⏳ Pendiente
**Objetivo:** Realizar login y capturar campos del Network
**Detalles:**
- Login con credenciales específicas
- Seleccionar idioma: Francés, POS: France
- Capturar evento "Session" desde DevTools > Network

-------------------------------

### Caso 1: Booking One-way (15 pts)
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

### Caso 2: Booking Round-trip (15 pts)
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
- **Fase de implementación:** ⏳ Lista para comenzar
- **Próximo paso:** Implementar Caso 4 (Verificar Cambio de Idioma)

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
