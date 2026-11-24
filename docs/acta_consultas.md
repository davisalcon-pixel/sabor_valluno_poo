# Acta de Consultas y Decisiones de Diseño

| Fecha | Tema / Consulta | Resolución / Decisión tomada |
| :--- | :--- | :--- |
| 23/11/26 | **Combos anidados y conteo de platos** | Se implementó el método polimórfico `contar_platos()` en `Producto` para que `Combo` sume recursivamente los platos de sus sub-productos y `PedidoParaLlevar` cobre Bs 2.00 por cada plato real sin usar `isinstance()`. |
| 23/11/26 | **Restricción de Tarjeta en Delivery** | Se definió el método abstracto `es_valido_para_delivery()` en `MetodoPago` para validar el método de pago por polimorfismo dentro de `PedidoDelivery.cobrar()`. |
| 23/11/26 | **Precio inicial de `Combo`** | Al heredar de `Producto`, el setter de `precio` rechaza `0.0`. Se inicializó `_precio = 0.0` internamente en `Combo` ya que su valor real se calcula dinámicamente en `calcular_precio(dia)`. |
| 23/11/26 | **Disponibilidad de mesas** | Una mesa se considera ocupada mientras tenga un pedido en estado `REGISTRADO`, `EN_PREPARACION` o `LISTO`. Se libera automáticamente al pasar a `ENTREGADO` o `CANCELADO`. |