# Pokémon Valdara — Integración de protagonistas

Estado: **preparación técnica**. La ROM compilada hasta ahora es la base de Emerald, sin sprites personalizados.

## Origen de los recursos
Repositorio de diseño: `carlos94cero-hue/pokemon-valdara`.
Los archivos `male_base_overworld_16x32_4dir_3frames.png` y `female_base_overworld_16x32_4dir_3frames.png` son prototipos de 48×128 píxeles, indexados a 16 colores. Filas: frente, espalda, izquierda, derecha; columnas: quieto, paso A, paso B.

## Destinos de integración
- `graphics/object_events/pics/people/brendan/walking.png`
- `graphics/object_events/pics/people/may/walking.png`
- `graphics/object_events/palettes/brendan.pal`
- `graphics/object_events/palettes/may.pal`

**No sobrescribir aún los originales.** El motor usa una secuencia y cantidad de fotogramas concreta. Hay que reorganizar las 12 celdas del prototipo al orden exigido por las tablas de animación del proyecto, además de generar la paleta compatible y comprobar reflejos. Las imágenes de correr, bicicleta, surf, pesca, movimientos de campo y batalla requieren recursos adicionales.

## Prueba prevista
1. Incorporar PNG y paletas compatibles.
2. Ejecutar `Valdara - compilacion de prueba` en GitHub Actions.
3. Descargar el artefacto generado y probar en Manic.
4. Verificar cuatro direcciones, tres fotogramas y transiciones; corregir si es necesario.

No se considera integrado hasta que una ROM recompilada muestre los protagonistas nuevos.
