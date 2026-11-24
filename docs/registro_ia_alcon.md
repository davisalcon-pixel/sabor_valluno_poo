# Registro personal de uso de IA

**Estudiante:** Davis Guido Alcon Poma 
**Variante:** A  

| N.º | Fecha | Herramienta | Tipo de uso | Consulta textual | Qué acepté | Qué modifiqué y por qué | Archivo o clase | ¿Lo explico sin ayuda? |
| :--- | :--- | :--- | :--- | :--- | :--- | :--- | :--- | :--- |
| 1 | 23/11/2026 | Gemini | Revisión | "reviso lo que es mi diagrama UML si hay malo lo corriges y me lo decis" | Corregir atributos públicos (+) a protegidos (#), eliminar la clase redundante `ComboProducto`, quitar atributos duplicados y agregar la clase gestora `Restaurante`. | Adapté todas las reglas, constantes y atributos del diagrama final a la Variante A (10% descuento en combos, envase Bs 2, envío gratis desde Bs 150 solo Cercado, chicharrón solo domingos). | `docs/diagrama_v2.png` | Sí |
| 2 | 23/11/2026 | Gemini | Error / Generación de código | "empecemos con las clases abstractas de producto, pedidos, pagos" | La estructura con `ABC` y `@abstractmethod` en `Producto`, y eliminar la importación circular `from modelo.producto import Producto` dentro del mismo archivo. | Al ejecutar `pruebas.py` saltó `ValueError` porque `Combo.__init__` enviaba precio `0.0` al setter de `Producto`; lo corregí asignando `self.nombre` y `self._precio = 0.0` directamente en `Combo`. | `modelo/productos.py` (`Producto`, `Plato`, `Bebida`, `Combo`) | Sí |
| 3 | 23/11/2026 | Gemini | Concepto | "cómo estaríamos controlando que un combo puede tener varios combos" | Uso del polimorfismo en `Combo` (combos anidados), `contar_platos()` para envases y `es_valido_para_delivery()` en `MetodoPago` para evitar `isinstance()`. | Verifiqué y ajusté las tarifas de delivery, el mínimo de Bs 40 y las transiciones de estado (`REGISTRADO` → `EN_PREPARACION` → `LISTO` → `ENTREGADO` / `CANCELADO`) según la Variante A. | `modelo/pedidos.py`, `modelo/pagos.py` | Sí |
| 4 | 24/11/2026 | Gemini | Error / Revisión | "cuando ingresé mi teléfono apareció todo ese formato hexadecimal" y "no me gusta el código de main.py, vuelve a revisar y mejorar" | Implementar `__str__` en `Cliente` para mostrar nombre y teléfono legibles, y refactorizar `main.py` para elegir clientes y productos por número en vez de escribir nombres exactos. | Probé el flujo completo en consola y ejecuté los 10 casos con `assert` en `pruebas.py` para confirmar que todas las validaciones de la Variante A pasan correctamente. | `modelo/clientes.py`, `restaurante.py`, `main.py`, `pruebas.py` | Sí |

**Declaración.** Declaro que este registro incluye todos mis usos de IA en el proyecto y que puedo explicar el código que entrego.  

**Firma:** Davis Guido Alcon Poma