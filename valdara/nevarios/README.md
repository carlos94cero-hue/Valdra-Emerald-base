# Valdara: Nevarios y Trío Místico

Recursos preparados para el proyecto de Pokémon Esmeralda decompilado, sin compilar ninguna ROM. Este directorio contiene **arte original en formato técnico Game Boy Advance**, no Pokémon sustituidos a ciegas ni especies activadas prematuramente.

1. `sprite_payload.json` almacena el arte fuente indexado y comprimido de 11 variantes/personajes y cuatro iconos de objetos.
2. `python3 valdara/nevarios/rebuild.py` reconstruye los PNG 4bpp, datos tileados y paletas compatibles con GBA sin dependencias externas.
3. `python3 valdara/nevarios/validate_static.py` comprueba colores, tamaños, transparencia, datos 4bpp, tipos y variantes sexuales.
4. `manifest.json` define el linaje y el Trío Místico; `REGLAS_Y_GUIA.md` recoge el diseño acordado.

**Estado:** los recursos gráficos están incorporados a la rama de desarrollo y pueden verse y modificarse. No se han añadido todavía nuevos IDs de especie ni evoluciones a `src/data/pokemon/`, ni se ha sustituido el Nidoran temporal que todavía emplea el prólogo de la ROM anterior. Esto se hará junto con las mecánicas de crianza cuando se aprueben los sprites finales. La presentación usará «Nevarios» como nombre de las criaturas; las clases de juego se traducirán a «Criador» cuando se revise el resto de interfaces. El antiguo Camino Neutral se denomina Camino del Investigador.

Esta rama tiene un workflow de **arte exclusivamente**: produce y valida las imágenes y las añade al repositorio, pero **no genera archivos `.gba`**.
