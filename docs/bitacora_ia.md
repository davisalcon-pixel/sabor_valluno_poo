# Bitácora de Uso de Inteligencia Artificial

* **Herramienta utilizada:** Gemini
* **Propósito general:** Apoyo en la estructuración de clases POO, depuración de errores y redacción de casos de prueba.

## Registro de interacciones

1. **Estructura del proyecto y resolución de errores de importación**
   * **Consulta:** Cómo organizar los archivos dentro de la carpeta `modelo/` y solución al error de importación circular en `modelo/productos.py`.
   * **Aporte recibido:** Se eliminó el `import` redundante dentro de `productos.py` y se definió la separación de responsabilidades entre `productos.py`, `clientes.py`, `pedidos.py`, `pagos.py` y `restaurante.py`.

2. **Diseño polimórfico y encapsulación**
   * **Consulta:** Implementación de `Pedido`, `MetodoPago` y `Combo` cumpliendo las reglas de la Variante A sin usar `isinstance()`.
   * **Aporte recibido:** Uso de clases abstractas (`ABC`), `@property` con validaciones en setters, y métodos polimórficos (`calcular_cargos`, `contar_platos`, `es_valido_para_delivery`).

3. **Depuración en `Combo.__init__`**
   * **Consulta:** Error `ValueError: El precio debe ser mayor que cero` al ejecutar `pruebas.py`.
   * **Aporte recibido:** Identificación del conflicto con `super().__init__(nombre, 0.0)` y corrección asignando `self.nombre` y `self._precio` directamente.

4. **Pruebas unitarias y menú de consola**
   * **Consulta:** Creación de `pruebas.py` con 10 pruebas usando `assert` y menú interactivo en `main.py`.
   * **Verificación:** Se ejecutaron todas las pruebas localmente con `python pruebas.py` confirmando que los 10 casos pasan correctamente.