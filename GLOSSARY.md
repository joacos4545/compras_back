# Lista de compras

Este contexto reúne los artículos que se planea comprar y permite registrar cuáles ya se compraron.

## Lenguaje

**Lista de compras**:
Conjunto compartido de elementos que se planea comprar.

**Elemento de lista**:
Artículo anotado en la lista con su cantidad, unidad opcional, nota opcional y precio unitario opcional. Puede estar pendiente o comprado.
_Evitar_: producto, artículo de catálogo

**Cantidad**:
Número positivo de unidades que se planea comprar. Puede incluir fracciones, como medio kilogramo.

**Precio unitario**:
Importe de una unidad del elemento, expresado en bolivianos. Puede desconocerse al añadir el elemento y corregirse después.
_Evitar_: precio total

**Total del elemento**:
Importe de la cantidad completa de un elemento, calculado a partir de su cantidad y precio unitario. No existe mientras se desconozca el precio unitario.

**Comprado**:
Estado de un elemento que indica que ya se adquirió; puede volver a quedar pendiente.

