# Protagonistas Valdara — adaptación GBA aprobada

Aprobado por Carlos el 23/10/2026.

Los protagonistas definitivos mantienen la identidad visual aprobada:
- masculino: azul, blanco, gris oscuro, detalles dorados; gorra y mochila.
- femenino: rosa, blanco, negro, cabello largo castaño; gorra y mochila.

## Recursos integrados
Los archivos reales del proyecto ya contienen las hojas de caminar y correr:
- 144×32 px.
- 9 fotogramas de 16×32 por hoja, en el orden que espera Esmeralda.
- 16 colores contando transparencia.
- la carrera es una animación diferente de la caminata.
- Esmeralda refleja la vista izquierda para producir la derecha.

Los retratos de 64×64 usados por la selección del protagonista también están sustituidos.

Las acciones especiales (bicicleta, surf, pesca, etc.) conservan las poses nativas de Esmeralda y se remapean a la identidad/paleta del personaje al preparar la compilación. Las espaldas de batalla mantienen las poses nativas y reciben la paleta del protagonista.

## Estado
Los recursos se han integrado en el código fuente. Esta entrega NO compila ni genera una ROM.

La validación de esta fase es exclusivamente de assets: tamaños, formato indexado, transparencia, número de colores, hashes, diferencias entre caminar/correr y coincidencia entre los recursos aprobados y los archivos reales del juego.
