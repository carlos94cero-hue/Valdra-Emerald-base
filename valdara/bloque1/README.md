# Valdara · Bloque 1 — Crianzas y Trío Místico

**Estado:** recursos y lógica de origen preparados y comprobados sin crear ROM ni ejecutar emulador.

## Datos y gráficos anteriores preservados

- **8 sprites aprobados** del tiburón Escualín macho y hembra, y seis evoluciones: Guardal (Agua/Acero), Abiskar (Agua/Siniestro), Terraleta (Agua/Tierra).
- **3 sprites del Trío Místico:** Umbrálix (Jardín de los Umbrales), Nevarión (Bosque del Sueño), Límbora (el Envés).
- 11 conjuntos de frente, espalda, animación e icono ya enlazados en la rama `valdara-registro-250`.
- **690 puntos exactos** en cada variante final, preservando sus seis estadísticas. Se preservan 12 perfiles intermedios diferentes por sexo/ruta aprobados en la ficha original.
- El Trío Místico debe tener **800 puntos cada uno**, pero el reparto de las seis estadísticas no quedó numéricamente cerrado; por ahora NO se inventa.

## Mecánica real incluida en código

Ruta persistente en `VAR_VALDARA_CAMINO` (0 indeciso, 1 Héroe, 2 Villano, 3 Investigador). Son valores ya disponibles en la base de Esmeralda. Las dos pruebas usan `FLAG_VALDARA_PRIMERA_PRUEBA` y `FLAG_VALDARA_SEGUNDA_PRUEBA`.

- Nivel 18 **solo después de elegir ruta**: Escualín macho → Escualito (macho); Escualín hembra → Escualita (hembra).
- Primera prueba completada: Escualito → Escuarón; Escualita → Escuarina (en el siguiente nivel que active la evolución).
- Segunda prueba completada: macho → Guardal/Abiskar/Terraleta (macho) según ruta; hembra → Guardal/Abiskar/Terraleta (hembra) según ruta.
- Las pruebas no admiten saltos de ruta ni cruces macho/hembra. El sistema respeta el bloqueo de evolución por Piedra Eterna del motor.
- `src/pokemon.c` calcula los valores intermedios por ruta en los seis atributos, sin cambiar los finales ni modificar las demás 238 especies de la tabla.

Los scripts `route_events.inc` aportan **entradas para conectar a las escenas de misión**, pero todavía no hay misiones completas implementadas para activar automáticamente esos hitos. Se llaman desde un evento mediante `call Valdara_CaminoHeroe` / `call Valdara_PrimeraPruebaCompletada`, etc.

## Habilidades

Se han registrado **24 nombres con descripciones y símbolos numéricos**. Las habilidades normales intermedias varían según la ruta en tiempo de ejecución; los finales registran su habilidad normal. **11 efectos cuentan con lógica activa de combate**, incluidos multiplicadores exactos de potencia/protección, aura en dobles y curación por turno.

**Faltan** el efecto por KO de Voluntad Umbría, el sistema real de habilidades ocultas de tercera generación (las 6 aprobadas permanecen en el catálogo, sin activarse fraudulentamente) y las habilidades místicas cuyo efecto preciso está todavía por aprobar. Las habilidades no implementadas se marcan como pendientes en `abilities.json`.

## Movimientos

`movimientos_aprobados.json` conserva todos los números de la ficha V01–V15 y los tres nombres de movimientos del Trío Místico (con 5 PP). Se han integrado como **movimientos nuevos y utilizables en las tablas**:

- Eclipse Absoluto — Siniestro / Físico / potencia 120 / precisión 90 / 5 PP / 20 % de bajar Defensa.
- Noche Eterna — Siniestro / Especial / potencia 100 / precisión 100 / 5 PP / 30 % de bajar Defensa Especial.
- Furia Continental — Tierra / Físico / potencia 110 / precisión 95 / 5 PP / 20 % de subir Ataque propio.

Las animaciones utilizan recursos existentes de Esmeralda **provisionalmente**, todavía no efectos de partículas únicos. Hay una excepción específica en cálculo físico para Eclipse Absoluto, porque Esmeralda clásico clasifica todo Siniestro como especial. Los otros doce movimientos V y los tres del Trío aún requieren lógica adicional o tipo Hada, que la base original no incluye. No se simulan como golpes distintos.

## Pruebas ejecutables SIN ROM

```
python3 valdara/bloque1/apply_patch.py
python3 valdara/bloque1/validate_block1.py
```

`apply_patch.py` comprueba **SHA256 previo y posterior de 14 archivos** y realiza `patch --dry-run` antes de modificar. Es idempotente; no pisa archivos con cambios ajenos. La prueba valida la tabla de especies, 12 estadísticas por ruta, habilidades, movimientos, entrada del trío y compilación/ejecución de pruebas C puras con GCC. No compila ni produce ningún archivo `.gba`.

**Aún pendiente:** comprobar sintaxis con la toolchain GBA real y probar ataques/evoluciones con el emulador en la única ROM de integración que decida el usuario más adelante.