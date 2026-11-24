# Sistema de Gestión - Restaurante "Sabor Valluno"

Sistema de gestión de menú, clientes, pedidos, pagos y reportes diarios desarrollado en Python aplicando los 4 pilares de la Programación Orientada a Objetos (Encapsulación, Herencia, Polimorfismo y Abstracción).

## Datos del Proyecto 
* **Variante asignada:** Variante A
* **Estudiante(s):** Davis Guido Alcon Poma
* **Lenguaje:** Python 

## Reglas de Negocio (Variante A)
* **Envase (Para llevar):** Bs 2.00 por cada plato (incluyendo los platos contenidos dentro de combos).
* **Pedido mínimo (Delivery):** Bs 40.00.
* **Envío gratis (Delivery):** Desde Bs 150.00, únicamente para la zona **Cercado**.
* **Disponibilidad:** El plato *Chicharrón* (y cualquier combo que lo incluya) solo está disponible los días **domingo**.
* **Combos:** 10% de descuento sobre la suma de sus productos; soporta combos anidados (combo dentro de combo).
* **Pagos:** Efectivo (con cálculo de cambio), QR (código de 10 dígitos) y Tarjeta (3% de comisión, no aceptada en delivery).

## Estructura del Proyecto
```text
├── main.py              # Menú interactivo de consola
├── restaurante.py       # Clase gestora (menú, clientes, pedidos y reportes)
├── pruebas.py           # 10 pruebas unitarias con assert
├── README.md            # Documentación del proyecto
├── acta_consultas.md    # Registro de dudas y aclaraciones
├── bitacora_ia.md       # Registro de uso de herramientas de IA
└── modelo/
    ├── __init__.py
    ├── productos.py     # Producto (ABC), Plato, Bebida, Combo
    ├── clientes.py      # Cliente (encapsulación y validación de teléfono)
    ├── pedidos.py       # Pedido (ABC), PedidoLocal, PedidoParaLlevar, PedidoDelivery
    └── pagos.py         # MetodoPago (ABC), PagoEfectivo, PagoQR, PagoTarjeta