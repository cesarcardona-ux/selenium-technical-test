# Advance Test - Selenium Technical Test

**Test cases implementation log**

> **📚 Concepts and definitions:** See [Glossary and Definitions.md](Glossary and Definitions.md)
> **📖 Step by step guide:** See [Technical Test - Selenium.md](Technical Test - Selenium.md)

---

## CASOS IMPLEMENTADOS

### Caso 4: Verificar Cambio de Idioma (5 pts)
**Estado:** ⏳ Pendiente
**Objetivo:** Seleccionar los 4 idiomas y verificar que el cambio se hace correctamente
**Idiomas:** Español, Inglés, Francés, Portugués

---

### Caso 5: Verificar Cambio de POS (5 pts)
**Estado:** ⏳ Pendiente
**Objetivo:** Seleccionar 3 POS y verificar que el cambio se hace correctamente
**POS:** Otros países, España, Chile

---

### Caso 6: Redirecciones Header (5 pts)
**Estado:** ⏳ Pendiente
**Objetivo:** Usar opciones del Navbar para acceder a 3 sitios diferentes
**Validación:** URLs cargan correctamente según idioma y sitio seleccionado

---

### Caso 7: Redirecciones Footer (5 pts)
**Estado:** ⏳ Pendiente
**Objetivo:** Usar links del footer para acceder a 4 sitios diferentes
**Validación:** URLs cargan correctamente según idioma y sitio seleccionado

---

### Caso 3: Login en UAT1 (10 pts)
**Estado:** ⏳ Pendiente
**Objetivo:** Realizar login y capturar campos del Network
**Detalles:**
- Login con credenciales específicas
- Seleccionar idioma: Francés, POS: France
- Capturar evento "Session" desde DevTools > Network

---

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

---

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

---

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
- **Fase de implementación:** ⏳ Lista para comenzar
- **Próximo paso:** Implementar Caso 4 (Verificar Cambio de Idioma)

---

*Última actualización: Fase de aprendizaje completada. Listo para implementación de tests*
