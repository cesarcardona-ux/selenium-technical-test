# Pytest Command Generator

**Generador visual de comandos pytest para Test Automation Suite**

---

## 📋 Descripción

Aplicación de escritorio que permite configurar y generar comandos pytest de forma visual mediante una interfaz gráfica profesional.

**Características principales:**
- ✅ Selección visual de 7 casos de prueba
- ✅ Configuración de 12 parámetros CLI mediante dropdowns
- ✅ Panel de datos de prueba editable (pasajeros, pago, facturación)
- ✅ Generación automática de comando pytest
- ✅ Copiar comando al portapapeles
- ✅ Ejecución directa desde la aplicación
- ✅ Guardado de configuraciones
- ✅ Tema claro/oscuro
- ✅ Todo parametrizado en JSON (sin hardcode)

---

## 🚀 Instalación

### 1. Requisitos Previos
- Python 3.9 o superior
- pip (gestor de paquetes de Python)

### 2. Instalar Dependencias

**Opción A: Instalación directa**
```bash
cd test_command_generator
pip install -r requirements.txt
```

**Opción B: Con entorno virtual (recomendado)**
```bash
cd test_command_generator
python -m venv venv_generator
venv_generator\Scripts\activate  # Windows
source venv_generator/bin/activate  # MacOS/Linux
pip install -r requirements.txt
```

---

## 💻 Uso

### Ejecutar la Aplicación

**Desde la carpeta raíz:**
```bash
python test_command_generator/main.py
```

**Desde la carpeta del generador:**
```bash
cd test_command_generator
python main.py
```

### Flujo de Uso

1. **Seleccionar Caso de Prueba**
   - Usar el dropdown "Select Test Case"
   - Elegir entre los 7 casos disponibles

2. **Configurar Parámetros**
   - Los parámetros aplicables se habilitan automáticamente
   - Parámetros no aplicables están deshabilitados
   - Configurar valores en cada dropdown/input

3. **Configurar Datos de Prueba** (opcional)
   - Solo para Cases 1 y 2
   - Editar información de pasajeros, pago, facturación
   - Hacer clic en "Save Test Data Changes" para guardar

4. **Configurar Flags de Pytest**
   - Habilitar/deshabilitar flags según necesidad
   - Ver explicación detallada en sección "Pytest Flags"

5. **Generar Comando**
   - El comando se genera automáticamente en tiempo real
   - Se muestra en formato multilínea legible

6. **Ejecutar o Copiar**
   - **Copy to Clipboard**: Copia comando al portapapeles
   - **Execute Command**: Abre nueva terminal y ejecuta el test
   - **Save Configuration**: Guarda configuración actual para uso futuro

---

## 🚩 Pytest Flags

### **Verbose (-v)**
- Muestra información detallada de cada test
- Útil para ver qué test está ejecutando y su resultado
- **Ejemplo:** `test_login[chrome-English] PASSED`

### **Show Prints (-s)**
- Muestra `print()` y logs en tiempo real
- Por defecto, pytest oculta los prints hasta que un test falle
- **Uso:** Debugging y ver logs de Selenium

### **Stop on Fail (-x)**
- Detiene ejecución en el primer test que falle
- Ahorra tiempo cuando quieres arreglar errores uno por uno
- **Ejemplo:** Si falla test #3 de 50, no ejecuta los 47 restantes

### **Allure Report**
- Genera reportes visuales interactivos
- Incluye: gráficos, capturas, videos, logs, timeline
- **Ver reporte:** `allure serve reports/allure`

### **Parallel (-n auto)**
- Ejecuta tests en paralelo usando múltiples CPUs
- Reduce tiempo de ejecución significativamente
- **Ejemplo:** 100 tests en 50 min → 8 min (con 8 CPUs)

---

## 📂 Estructura del Proyecto

```
test_command_generator/
├── main.py                          # Punto de entrada
├── requirements.txt                 # Dependencias
├── README.md                        # Esta documentación
│
├── gui/                             # Interfaz gráfica
│   ├── __init__.py
│   └── main_window.py               # Ventana principal
│
├── core/                            # Lógica de negocio
│   ├── __init__.py
│   ├── config_manager.py            # Gestión de JSON
│   ├── case_mapper.py               # Mapeo caso → parámetros
│   └── command_builder.py           # Construcción de comandos
│
├── config/                          # Configuración JSON
│   ├── case_mappings.json           # Casos y parámetros aplicables
│   ├── parameter_options.json       # Opciones de cada parámetro
│   ├── testdata.json                # Datos de prueba
│   └── saved_configs/               # Configuraciones guardadas
│
└── assets/                          # Recursos (iconos, logos)
```

---

## ⚙️ Archivos de Configuración

### `config/case_mappings.json`
Define qué parámetros aplican a cada caso de prueba.

### `config/parameter_options.json`
Contiene todas las opciones disponibles para cada parámetro:
- Browsers (Chrome, Edge, Firefox, All)
- Languages (Español, English, Français, Português, All)
- POS (Chile, España, Otros países, All)
- Environments (QA4, QA5, UAT1, All)
- Cities (10 ciudades con códigos IATA)
- Header/Footer links
- Screenshots modes
- Video recording options

### `config/testdata.json`
Datos de prueba para Cases 1 y 2:
- Pasajeros (Adult, Teen, Child, Infant)
- Pago (tarjeta de crédito)
- Facturación (email, dirección, ciudad, país)

---

## 🎨 Temas

La aplicación soporta dos temas:

- **🌙 Dark Mode** (por defecto)
- **☀️ Light Mode**

Cambiar tema usando el botón en el header.

---

## 💾 Configuraciones Guardadas

Las configuraciones se guardan en `config/saved_configs/` con:
- Nombre descriptivo
- Timestamp de creación
- Caso seleccionado
- Parámetros configurados
- Flags de pytest

**Formato de archivo:** `{nombre}_{timestamp}.json`

---

## 📝 Ejemplos de Comandos Generados

### Case 1: One-way Booking
```bash
pytest tests/nuxqa/test_oneway_booking_Case1.py \
  --browser=chrome \
  --language=Español \
  --pos=Chile \
  --env=qa5 \
  --origin=BOG \
  --destination=MDE \
  --departure-days=4 \
  --video=enabled \
  --screenshots=all \
  -v --alluredir=reports/allure
```

### Case 3: Flight Search & Network Capture
```bash
pytest tests/nuxqa/test_login_network_Case3.py \
  --browser=chrome \
  --language=Français \
  --pos=France \
  --env=uat1 \
  --origin=BOG \
  --destination=MAD \
  --departure-days=7 \
  --return-days=10 \
  --video=enabled \
  --screenshots=on-failure \
  -v -s
```

### Case 4: Language Change
```bash
pytest tests/nuxqa/test_language_change_Case4.py \
  --browser=all \
  --language=all \
  --env=all \
  --screenshots=on-failure \
  -v -n auto
```

---

## 🐛 Troubleshooting

### Error: "No module named 'customtkinter'"
```bash
pip install customtkinter
```

### Error: "No module named 'pyperclip'"
```bash
pip install pyperclip
```

### Error al ejecutar comando
- Verificar que estás en el directorio correcto del proyecto de tests
- El comando ejecuta en la carpeta donde está el ejecutable `pytest`
- Asegúrate de tener el entorno virtual de tests activado antes de ejecutar

### Tema no cambia
- Reinicia la aplicación
- Verifica que customtkinter está actualizado: `pip install --upgrade customtkinter`

---

## 🔄 Actualizar Configuración

### Agregar Nueva Ciudad
Editar `config/parameter_options.json` → sección `cities`:
```json
"GDL": {
  "iata_code": "GDL",
  "city_name": "Guadalajara",
  "search_string": "Guad",
  "country": "México",
  "country_code": "MX",
  "flag": "🇲🇽",
  "display_name": "Guadalajara (GDL)",
  "timezone": "America/Mexico_City"
}
```

### Agregar Nuevo Parámetro a un Caso
Editar `config/case_mappings.json` → agregar parámetro a `applicable_parameters`:
```json
"case_5": {
  "applicable_parameters": [
    "browser",
    "pos",
    "env",
    "new-parameter",  // ← Nuevo parámetro
    "video",
    "screenshots"
  ]
}
```

---

## 📞 Soporte

**Desarrollador:** César Cardona
**Empresa:** FLYR Inc / Avianca
**Repositorio:** [GitHub - selenium-technical-test](https://github.com/cesarcardona-ux/selenium-technical-test)

---

## 📄 Licencia

© 2025 César Cardona - FLYR Inc

---

🤖 *Generado con Claude Code*
