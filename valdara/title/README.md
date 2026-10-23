# Inicio de Valdara — logo aprobado

Diseño aprobado por Carlos el 23 de octubre de 2026. Se utiliza el emblema original VALDARA con letras doradas, olas turquesa, estrella y fondo oscuro, sin redibujar el logo. Se recortan solamente los márgenes exteriores y se adapta a la pantalla nativa de 240×160.

## Integración

`src/title_screen.c` mantiene la entrada pública `CB2_InitTitleScreen` y la tabla `gTitleScreenAlphaBlend` compartida con la presentación original. La nueva pantalla está en `src/valdara_title_screen.inc`. El PNG indexado está en `graphics/title_screen/valdara/title.png`; el sistema de recursos de Esmeralda convierte el mismo archivo a 8bpp LZ77 y una paleta de 256 colores. No es un motor alternativo.

El emblema queda centrado y completo. Debajo aparece PULSA START, con parpadeo lento. START o A se dirigen al menú existente; se conservan las pantallas de confirmación de mantenimiento. No se alteran mapas, combates, datos de guardado ni la presentación anterior al título.

## Verificación sin crear ROM

Ejecutar `python3 valdara/title/validate.py`. Esta comprobación usa la herramienta gráfica del propio repositorio, comprueba dimensiones, paleta, disposición de los 600 tiles, descompresión sin pérdida y separación de la memoria del mapa. Genera únicamente recursos y una vista previa temporal; nunca enlaza una ROM.

Esta rama es de diseño. No se activó ningún workflow de compilación y no se generó ninguna ROM nueva. La prueba de arranque, transición y controles dentro del juego queda pendiente para la fase de pruebas acordada. Las imágenes son vistas previas decodificadas del recurso preparado, no capturas de una ROM nueva.
