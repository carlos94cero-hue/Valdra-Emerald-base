# Valdara R10 — Estado de integración

Esta rama está separada de `master`, que conserva la compilación funcional.

## Preparado
- `valdara/instalar_revision10.py`: valida dimensiones 144x32, índices de 0 a 15 y paletas JASC-PAL.
- `.github/workflows/valdara-build.yml`: usa el instalador R10 en lugar del generador geométrico antiguo.
- `valdara/inspeccionar_hojas_originales.py`: comprueba el formato de las hojas originales.

## Falta incorporar los cuatro recursos gráficos
Subir estos archivos **descomprimidos** a `valdara/assets/`:

- `brendan_walking_144x32.png`
- `may_walking_144x32.png`
- `brendan.pal`
- `may.pal`

Se encuentran en el ZIP `Valdara_Revision_10_Emerald.zip` entregado en el chat.

No ejecutar el flujo hasta subirlos: el instalador se detendrá deliberadamente si faltan.

## Pendiente después de la primera prueba
Confirmar orden de fotogramas, alineación y transparencia dentro de Manic. Los retratos de elección de personaje no están incluidos en R10: requieren un recurso separado de 64x64 para cada protagonista.

No fusionar a `master` hasta confirmar una ROM funcional y una inspección visual satisfactoria.
