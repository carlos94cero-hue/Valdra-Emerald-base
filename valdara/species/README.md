# Registro de especies nativas — Valdara (250)

Fase de desarrollo de **Pokémon Esmeralda**, sin generar nuevas ROM.

La región mantiene **250 especies/entradas acordadas**, con las primeras doce
plazas adaptadas al tiburón inicial y sus ramas según la crianza. Las 37
sustituciones de nombres heredados se marcan como alias **provisionales** cuando
el nombre no había sido aprobado expresamente. El Trío Místico conserva sus
nombres: **Umbrálix**, **Nevarión**, **Límbora**. La antigua ruta Neutral se
llama **Camino del Investigador**.

## Qué se registra realmente en tablas activas

`unpack.py` restaura sin pérdida el catálogo humano completo; `install_native.py`
actualiza las tablas de Esmeralda:

- `src/data/text/species_names.h`: 250 nombres de especies del juego (máximo diez caracteres).
- `src/data/pokemon/species_info.h`: **55 perfiles numéricos completos APROBADOS** (PS, Ataque, Defensa, At. Esp., Def. Esp. y Velocidad) sin modificar sus sumas; tipos exactos de los 160 casos compatibles con Esmeralda.
- `include/constants/valdara_species.h`: 250 alias nativos para acceder a cada entrada de Valdara sin mover la estructura de guardados.
- `src/data/pokemon/evolution.h`: se desactivan evoluciones heredadas de otros Pokémon y se habilitan solo las dos relaciones simples confirmadas; 14 relaciones aprobadas con pruebas/misiones quedan para implementar sus disparadores.
- `graphics/pokemon/...` + coordenadas/iconos: **11 sprites originales** ya terminados (dos iniciales, seis ramas y trío místico), incluidos gráficos de frente/espalda/animación y los índices de paleta de icono nativos.
- `valdara/port_scripts.inc`: el viajero entrega Escualín macho o hembra mediante los alias de Valdara.

## Datos diseñados conservados, todavía no implementados en combate

Los libros anteriores contienen **250 nombres, pero no 250 fichas numéricas y habilidades completas**. No se rellenan huecos inventando estadísticas ni se sustituyen habilidades aprobadas por otras diferentes. En las entradas incompletas se conserva *temporalmente* el valor mecánico preexistente del slot de Esmeralda, explícitamente señalado en el manifiesto.

Las **52 especificaciones de habilidades** (de las cuales varias son propuestas, no aprobaciones) y los 94 movimientos exclusivos con sus PP originales están transcritos en `catalog_250.json`; **sus efectos especiales NO están conectados aún al motor**, porque exigirían añadir códigos de habilidad/ataque y eventos concretos. No llamarlos «habilidades ya funcionales».

La mecánica de tipo **Hada** aún no existe en esta versión de Esmeralda y se mantiene como decisión de diseño; las especies afectadas requieren ampliar la tabla de tipos y de efectividades antes de programarse. No se remapea Hada a otro tipo ocultamente.

**Arte pendiente:** existen sprites originales para 11 formas; las otras 239 entradas requieren dibujos originales y conservan provisionalmente los archivos de arte del slot para no romper la estructura. Esos dibujos temporales **no son el diseño final de los Nevarios**. Tampoco están cerradas las evoluciones por camino ni los encuentros de los trío místico.

## Pruebas

```
python3 valdara/species/unpack.py
python3 valdara/species/install_native.py
python3 valdara/species/test_native.py
```

Las pruebas revisan cada alias, nombre, stat confirmado, tipo soportado,
transparencia, formato gráfico, evoluciones simples, sprites y ausencia de
nuevas ROM. La rama registra el resultado en `native_validation.json` y
`test_results.json`. Son **pruebas estáticas**, no pruebas de comportamiento de
combate o de guardados en mGBA; esto queda para una ROM de prueba conjunta.