# Valdara: el viajero y los Nevarios

Petición de Carlos del 23/10/2026: el profesor deja de presentar la partida. La bienvenida la realiza el viajero que entrega el inicial en Puerto Brisa. Las criaturas se llaman **Nevarios**. Después de la bienvenida se pasa a la elección del protagonista.

## Secuencia

1. El viajero aparece solo, utilizando el retrato nativo de excursionista de Esmeralda (sombrero, mochila y bastón). Es la representación nativa seleccionada para esta implementación; no un nuevo diseño aprobado de personaje.
2. «¡Bienvenido a Valdara!»
3. «Una historia fantástica te espera en esta región.»
4. «Una región que aún no ha sido explorada por completo.»
5. «Aquí habitan unas criaturas llamadas Nevarios.»
6. «Ahora elige a tu protagonista.» Opciones Chico / Chica con los retratos ya preparados del proyecto.
7. Nombre y confirmación. Al cancelar, se conserva el regreso nativo a la selección.
8. «¡Tu historia en Valdara comienza ahora!» y comienzo en Puerto Brisa.

Se omite el discurso del profesor, su investigación, la demostración de Lotad y la referencia posterior a Littleroot y al laboratorio. La entrega y elección del inicial permanecen en Puerto Brisa; no ocurren en la presentación. El personaje del puerto utiliza el mismo tipo gráfico que el viajero de la introducción.

## Integración sin generar ROM

El proyecto ya materializa los mapas y las animaciones mediante instaladores. Este cambio sigue ese flujo:

```sh
python3 valdara/install_port.py
python3 valdara/install_motion.py
python3 valdara/intro/install.py
python3 valdara/intro/test_intro.py
```

El instalador aplica cambios comprobados a `src/main_menu.c`, genera `src/valdara_intro_text.h` y actualiza el gráfico del viajero en el mapa generado. El texto editable está en `dialogue.json`. El workflow de Puerto Brisa incluye esta etapa para la futura compilación; su filtro de ramas NO activa compilaciones al editar `valdara-inicio-logo-aprobado`.

No se compila ni enlaza ninguna ROM en esta entrega. Se mantienen intactos el logo aprobado, su pantalla inicial, las tablas de animación, los combates y los datos de guardado. Los nombres técnicos históricos Birch, Lotad y Pokémon que quedan en código no son texto mostrado por la nueva secuencia. La nueva introducción usa Nevarios; la traducción de todas las interfaces heredadas no forma parte de esta modificación.

## Comprobaciones

`test_intro.py` comprueba los enlaces de la secuencia, ambas opciones, el texto y su ancho con la fuente original, la coherencia del viajero, la entrega posterior del inicial y la idempotencia. Las imágenes entregadas son vistas previas montadas con los recursos y la fuente del juego, no capturas de una ROM ejecutada.

Queda pendiente la prueba completa de entrada, texto, elección, nombre y llegada al puerto dentro del emulador, en la fase de pruebas de ROM acordada.
