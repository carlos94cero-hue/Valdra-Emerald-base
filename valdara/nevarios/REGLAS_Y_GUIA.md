# Valdara · Bestiario de Nevarios · sprites GBA v1

Esta primera adaptación reúne **11 entradas visuales** (una especie inicial con variantes sexuales y tres ramas de evolución, más tres integrantes del Trío Místico). No son 11 especies independientes: las ocho formas del tiburón pertenecen al **mismo linaje**. Los nombres del tiburón y de sus tres evoluciones son etiquetas provisionales, no nombres oficiales.

## Conceptos establecidos el 23 de octubre de 2026

- **Nevarios** = criaturas del mundo de Valdara. En singular **Nevario**.
- **Criadores** = personas que cuidan y entrenan a los Nevarios. «Domador» queda disponible para un perfil adversarial, pero no sustituye el nombre de la clase general.
- **Cristales de vínculo** = objeto de captura y sello del vínculo; se diseñaron iconos de cristal común, claro y oscuro. Reglas de obtención, uso y rareza por cerrar.
- **Veloria** = herramienta/registro **inventado por el protagonista y el investigador de fauna en el Camino del Investigador**, inspirada en conocimientos antiguos; no un dispositivo equivalente dado a todos los protagonistas. En Héroe y Villano usarán cuadernos sencillos. Esto sustituye la propuesta de que Veloria ya fuera un artefacto disponible en todas las rutas.
- El **Camino Neutral** queda renombrado como **Camino del Investigador**.
- El **Envés** = nuevo nombre del lugar antes llamado Mundo Distorsión.

## El inicial: la misma especie, macho y hembra

| Forma | Sexo | Tipos acordados | Crianzas y rasgos |
| --- | --- | --- | --- |
| Tiburón inicial | ♂ azul / ♀ coral | Agua | Cría de tiburón anfibia con patas/aletas para caminar por tierra |
| Protector heroico | ♂ / ♀ | Agua / Acero | Placas protectoras azul o coral y armadura de detalles dorados |
| Guerrero abisal | ♂ / ♀ | Agua / Siniestro | Marcas violetas de Névara, aletas de obsidiana y sombra |
| Explorador pétreo | ♂ / ♀ | Agua / Tierra | Piel mineral y aletas excavadoras adaptadas a cuevas y ruinas |

La evolución depende de **la crianza, los vínculos y las acciones del jugador** en cada camino. El camino abre condiciones narrativas; no fuerza automáticamente una transformación. El sexo no determina el camino ni cambia los tipos. Nombres, niveles, objetos, valores y mecánicas específicas de desbloqueo **no están cerrados**.

## El Trío Místico

| Nevario | Función confirmada | Refugio o mundo |
| --- | --- | --- |
| **Umbrálix** | Portales y vínculos entre lugares | Jardín de los Umbrales |
| **Nevarión** | Pesadillas, manifestaciones nocturnas, ligado a Névara | Bosque del Sueño |
| **Límbora** | Guardiana de la frontera entre mundos | El Envés |

Los tres sustituyen narrativamente a Hoopa, Darkrai y Giratina, pero no copiamos sus sprites. **Los tipos concretos del Trío Místico permanecen pendientes de aprobación**, así como cifras de combate, habilidades y niveles.

## Contenido técnico de cada carpeta

- `front.png` y `back.png`: PNG indexados **64×64**, máximo 16 colores, índice 0 transparente.
- `anim_front.png`: **64×128**, dos fotogramas verticales GBA de 64×64.
- `icon.png`: **32×64**, dos fotogramas de 32×32.
- `normal.pal`: paleta textual JASC de 16 entradas.
- `*.4bpp` y `normal.gbapal`: datos crudos de Game Boy Advance (4 bits/píxel y BGR555), orden por tiles de 8×8. La paleta binaria pesa 32 bytes.
- `manifest.json`: nombres, tipos, rutas, sexo, relación de linaje, roles legendarios y hashes de recursos.
- `assets/items/*`: iconos GBA **24×24** para los tres cristales y la Veloria.

**El pack está listo para insertar como recursos de arte en el repositorio de Esmeralda.** No significa que ya sean seleccionables, capturables o estén registrados como especies en las tablas de batalla del motor: eso exige editar IDs, datos de especie, evoluciones, movimientos, iconos de combate, tablas de animación y encuentros, que se harán una vez se aprueben las formas y nombres definitivos.

## Pruebas y estado

`python validate_nevarios.py` verifica formatos, paletas, alpha, tamaños, orden 4bpp con ida y vuelta, sexo, rutas, tipos y elementos del inventario. Estas son **pruebas estáticas de recursos**; todavía no se han probado los Neverios en una ROM. No se ha generado ninguna ROM.

Los dibujos se han adaptado a partir del concepto visual del proyecto y las espaldas se han construido como recursos GBA provisionales. Este es un **primer pase visual**: la aprobación artística final corresponde al usuario. Para mantener la calidad, la siguiente iteración se centrará en limpieza de las siluetas, sombreado, animaciones e iconos.
