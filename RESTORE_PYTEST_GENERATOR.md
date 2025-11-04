# 🔄 Instrucciones de Restauración: Pytest Command Generator v1.0.0

**Commit ID:** `1349165`
**Tag:** `v1.0.0-pytest-generator`
**Fecha:** 2025-11-03
**Autor:** César Cardona - FLYR Inc

---

## 📋 ¿Qué se guardó en este punto?

Esta versión incluye la **aplicación completa de Pytest Command Generator** con:

✅ GUI moderna con CustomTkinter
✅ 3 paneles: Test Parameters, Pytest Flags, Test Data
✅ Sistema simplificado: **1 solo botón** guarda todo en `testdata.json`
✅ Auto-carga de configuración al iniciar
✅ 7 casos de prueba configurables
✅ 12 parámetros CLI
✅ 5 pytest flags
✅ Editor de test data completo
✅ Copiar/ejecutar comandos
✅ Tema claro/oscuro

---

## 🔄 MÉTODO 1: Checkout del Tag (Recomendado)

### Ver el tag
```bash
git tag -l
git show v1.0.0-pytest-generator
```

### Restaurar temporalmente (estado detached)
```bash
git checkout v1.0.0-pytest-generator
```

### Crear una nueva rama desde este punto
```bash
git checkout -b feature/pytest-generator v1.0.0-pytest-generator
```

---

## 🔄 MÉTODO 2: Ver el Commit Completo

### Ver el mensaje completo del commit
```bash
git log --format=full 1349165
```

### Ver archivos modificados
```bash
git show --name-only 1349165
```

### Ver diferencias completas
```bash
git show 1349165
```

---

## 🔄 MÉTODO 3: Restaurar Archivos Específicos

### Restaurar solo un archivo
```bash
git checkout v1.0.0-pytest-generator -- test_command_generator/main.py
```

### Restaurar todo el directorio
```bash
git checkout v1.0.0-pytest-generator -- test_command_generator/
```

### Restaurar múltiples archivos
```bash
git checkout v1.0.0-pytest-generator -- \
  test_command_generator/gui/main_window.py \
  test_command_generator/core/config_manager.py
```

---

## 🔄 MÉTODO 4: Hard Reset (⚠️ DESTRUCTIVO)

**ADVERTENCIA:** Esto borrará todos los cambios no commiteados.

### Backup primero (recomendado)
```bash
git branch backup-antes-reset
```

### Hard reset al tag
```bash
git reset --hard v1.0.0-pytest-generator
```

### Soft reset (mantiene cambios en staging)
```bash
git reset --soft v1.0.0-pytest-generator
```

---

## 🔄 MÉTODO 5: Crear Rama sin Cambiar Main

```bash
# Crear rama de backup
git branch backup-pytest-gen v1.0.0-pytest-generator

# Cambiar a la rama
git checkout backup-pytest-gen

# O todo en un comando
git checkout -b backup-pytest-gen v1.0.0-pytest-generator
```

---

## 🔄 MÉTODO 6: Ver Diferencias sin Restaurar

### Ver qué cambió desde este tag
```bash
git diff v1.0.0-pytest-generator
```

### Ver solo nombres de archivos modificados
```bash
git diff --name-only v1.0.0-pytest-generator
```

### Ver estadísticas
```bash
git diff --stat v1.0.0-pytest-generator
```

### Ver contenido de un archivo en este tag (sin modificar tu working tree)
```bash
git show v1.0.0-pytest-generator:test_command_generator/main.py
git show v1.0.0-pytest-generator:test_command_generator/README.md
```

---

## 📦 Archivos Incluidos en este Commit

```
test_command_generator/
├── main.py                          # Punto de entrada principal
├── requirements.txt                 # Dependencias (customtkinter, pyperclip)
├── README.md                        # Documentación completa
├── INSTALL.md                       # Guía de instalación
├── __init__.py
│
├── gui/                             # Interfaz gráfica
│   ├── __init__.py
│   └── main_window.py               # Ventana principal (755 líneas)
│
├── core/                            # Lógica de negocio
│   ├── __init__.py
│   ├── config_manager.py            # Gestión de archivos JSON
│   ├── case_mapper.py               # Mapeo de casos a parámetros
│   └── command_builder.py           # Construcción de comandos pytest
│
├── config/                          # Configuración JSON
│   ├── case_mappings.json           # Mapeo de 7 casos
│   ├── parameter_options.json       # Opciones de parámetros
│   └── testdata.json                # Datos de prueba + sesión actual
│
└── assets/                          # Recursos
    └── logo_placeholder.txt
```

**Total:** 15 archivos creados, 2,444 líneas de código

---

## 🚀 Cómo Usar la Aplicación Restaurada

```bash
# 1. Ir al directorio
cd test_command_generator

# 2. Instalar dependencias (solo primera vez)
pip install -r requirements.txt

# 3. Ejecutar la aplicación
python main.py
```

---

## 📊 Estadísticas del Commit

- **Archivos creados:** 15
- **Líneas añadidas:** 2,444
- **Módulos core:** 3 (config_manager, case_mapper, command_builder)
- **Archivos de configuración JSON:** 3
- **Tamaño del GUI:** 755 líneas
- **Parametrización:** 100% (sin hardcode)

---

## 🔍 Comandos Útiles Adicionales

### Ver mensaje completo del tag anotado
```bash
git tag -n999 v1.0.0-pytest-generator
```

### Ver cuándo se creó el tag
```bash
git for-each-ref --format='%(refname:short) %(taggerdate)' refs/tags/v1.0.0-pytest-generator
```

### Comparar con versión actual
```bash
git diff v1.0.0-pytest-generator..HEAD
```

### Ver historial desde este tag
```bash
git log v1.0.0-pytest-generator..HEAD --oneline
```

---

## 📞 Soporte

**Desarrollador:** César Cardona
**Empresa:** FLYR Inc / Avianca
**Tag:** v1.0.0-pytest-generator
**Commit:** 1349165

---

**Nota:** Este archivo se puede eliminar si ya no se necesita. Está aquí solo como referencia rápida.
