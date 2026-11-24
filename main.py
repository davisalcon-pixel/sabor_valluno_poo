from restaurante import Restaurante
from modelo.productos import Plato, Bebida, Combo
from modelo.pagos import PagoEfectivo, PagoQR, PagoTarjeta


def leer_entero(mensaje: str) -> int:
    while True:
        try:
            return int(input(mensaje).strip())
        except ValueError:
            print("  [Aviso] Ingrese un número entero válido.")


def leer_flotante(mensaje: str) -> float:
    while True:
        try:
            return float(input(mensaje).strip())
        except ValueError:
            print("  [Aviso] Ingrese un monto numérico válido.")


def seleccionar_cliente(rest: Restaurante):
    if not rest.clientes:
        print("  No hay clientes registrados. Registre uno primero (opción 3).")
        return None
    print("\n--- Clientes registrados ---")
    for i, c in enumerate(rest.clientes, 1):
        print(f"  {i}. {c}")
    idx = leer_entero("Seleccione el número de cliente (0 para cancelar): ")
    if idx == 0:
        return None
    if 1 <= idx <= len(rest.clientes):
        return rest.clientes[idx - 1]
    print("  [Aviso] Número de cliente inválido.")
    return None


def seleccionar_pedido(rest: Restaurante):
    if not rest.pedidos:
        print("  No hay pedidos registrados.")
        return None
    print("\n--- Pedidos registrados ---")
    for p in rest.pedidos:
        pagado = "PAGADO" if p.comprobante_pago else "PENDIENTE"
        print(f"  #{p.id_pedido} | {p.tipo_pedido()} | {p.cliente.nombre} | Día: {p.dia} | {p.estado} | {pagado}")
    id_pedido = leer_entero("Ingrese el ID del pedido (0 para cancelar): ")
    if id_pedido == 0:
        return None
    return rest.buscar_pedido(id_pedido)


def mostrar_menu_principal():
    print("\n" + "=" * 48)
    print("   SISTEMA DE PEDIDOS - SABOR VALLUNO (Var. A)")
    print("=" * 48)
    print("1. Ver menú disponible por día")
    print("2. Registrar producto (Plato / Bebida / Combo)")
    print("3. Registrar cliente")
    print("4. Crear pedido")
    print("5. Ver detalle de un pedido")
    print("6. Modificar productos de un pedido")
    print("7. Cambiar estado de un pedido")
    print("8. Cobrar pedido")
    print("9. Reporte de ventas del día")
    print("0. Salir")
    print("=" * 48)


def ver_menu(rest: Restaurante):
    dia = input("Ingrese el día (ej. lunes, domingo): ").strip()
    disponibles = rest.listar_menu_disponible(dia)
    print(f"\n--- Menú disponible ({dia.capitalize()}) ---")
    if not disponibles:
        print("  No hay productos disponibles.")
        return
    for i, prod in enumerate(disponibles, 1):
        print(f"  {i}. {prod.nombre} - Bs {prod.calcular_precio(dia):.2f}")


def registrar_producto(rest: Restaurante):
    print("\nTipo de producto: 1) Plato  2) Bebida  3) Combo")
    tipo = input("Seleccione (1-3): ").strip()

    if tipo == "1":
        nombre = input("Nombre del plato: ")
        precio = leer_flotante("Precio (Bs): ")
        dias_txt = input("Días disponibles separados por coma (vacío = todos): ").strip()
        dias = [d.strip() for d in dias_txt.split(",") if d.strip()] if dias_txt else []
        rest.registrar_producto(Plato(nombre, precio, dias))
        print("  Plato registrado correctamente.")

    elif tipo == "2":
        nombre = input("Nombre de la bebida: ")
        precio = leer_flotante("Precio por vaso (Bs): ")
        es_jarra = input("¿Es jarra? (s/n): ").strip().lower() == "s"
        rest.registrar_producto(Bebida(nombre, precio, es_jarra))
        print("  Bebida registrada correctamente.")

    elif tipo == "3":
        nombre = input("Nombre del combo: ")
        catalogo = rest.menu
        if len(catalogo) < 2:
            print("  Se necesitan al menos 2 productos en el menú para armar un combo.")
            return

        productos_combo = []
        print("\n--- Productos disponibles para el combo ---")
        for i, p in enumerate(catalogo, 1):
            print(f"  {i}. {p.nombre}")

        while True:
            idx = leer_entero("Número de producto a incluir (0 para terminar): ")
            if idx == 0:
                break
            if 1 <= idx <= len(catalogo):
                productos_combo.append(catalogo[idx - 1])
                print(f"  + Añadido: {catalogo[idx - 1].nombre}")
            else:
                print("  [Aviso] Número fuera de rango.")

        rest.registrar_producto(Combo(nombre, productos_combo))
        print(f"  Combo '{nombre}' registrado correctamente.")
    else:
        print("  Opción no válida.")


def registrar_cliente(rest: Restaurante):
    nombre = input("Nombre del cliente: ")
    telefono = input("Teléfono (8 dígitos, inicia en 6 o 7): ")
    cliente = rest.registrar_cliente(nombre, telefono)
    print(f"  Cliente registrado: {cliente}")


def agregar_productos_a_pedido(rest: Restaurante, pedido):
    disponibles = rest.listar_menu_disponible(pedido.dia)
    if not disponibles:
        print("  No hay productos disponibles para ese día.")
        return

    print(f"\n--- Menú disponible ({pedido.dia.capitalize()}) ---")
    for i, p in enumerate(disponibles, 1):
        print(f"  {i}. {p.nombre} - Bs {p.calcular_precio(pedido.dia):.2f}")

    while True:
        idx = leer_entero("Elija el número del producto (0 para terminar): ")
        if idx == 0:
            break
        if not (1 <= idx <= len(disponibles)):
            print("  [Aviso] Número fuera de rango.")
            continue
        cantidad = leer_entero("Cantidad (1-20): ")
        try:
            prod = disponibles[idx - 1]
            pedido.agregar_producto(prod, cantidad)
            print(f"  + Agregado: {cantidad}x {prod.nombre}")
        except ValueError as e:
            print(f"  [Error]: {e}")


def crear_pedido(rest: Restaurante):
    cliente = seleccionar_cliente(rest)
    if not cliente:
        return

    dia = input("Día del pedido (ej. lunes, domingo): ").strip()
    print("Tipo de pedido: 1) Local  2) Para llevar  3) Delivery")
    tipo = input("Seleccione (1-3): ").strip()

    if tipo == "1":
        mesa = leer_entero("Número de mesa (1-15): ")
        pedido = rest.crear_pedido_local(cliente, dia, mesa)
    elif tipo == "2":
        pedido = rest.crear_pedido_para_llevar(cliente, dia)
    elif tipo == "3":
        zona = input("Zona (Cercado, Quillacollo, Sacaba, Vinto): ")
        pedido = rest.crear_pedido_delivery(cliente, dia, zona)
    else:
        print("  Tipo de pedido no válido.")
        return

    print(f"\nPedido #{pedido.id_pedido} creado ({pedido.tipo_pedido()}).")
    agregar_productos_a_pedido(rest, pedido)
    print(f"Pedido #{pedido.id_pedido} guardado. Subtotal actual: Bs {pedido.calcular_subtotal():.2f}")


def ver_detalle_pedido(rest: Restaurante):
    pedido = seleccionar_pedido(rest)
    if not pedido:
        return

    print(f"\n--- Detalle del Pedido #{pedido.id_pedido} ---")
    print(f"Cliente: {pedido.cliente} | Tipo: {pedido.tipo_pedido()} | Día: {pedido.dia} | Estado: {pedido.estado}")
    if not pedido.items:
        print("  (Pedido sin productos)")
        return

    for item in pedido.items:
        prod = item["producto"]
        cant = item["cantidad"]
        precio_u = prod.calcular_precio(pedido.dia)
        print(f"  - {cant}x {prod.nombre} (Bs {precio_u:.2f} c/u) = Bs {precio_u * cant:.2f}")

    subtotal = pedido.calcular_subtotal()
    print(f"Subtotal: Bs {subtotal:.2f}")
    try:
        cargos = pedido.calcular_cargos()
        total = pedido.calcular_total()
        print(f"Cargos (envase/envío): Bs {cargos:.2f}")
        print(f"TOTAL: Bs {total:.2f}")
    except ValueError as e:
        print(f"Cargos/Total pendiente: {e}")


def modificar_pedido(rest: Restaurante):
    pedido = seleccionar_pedido(rest)
    if not pedido:
        return

    print("1) Agregar productos  2) Quitar producto")
    accion = input("Seleccione (1-2): ").strip()

    if accion == "1":
        agregar_productos_a_pedido(rest, pedido)
    elif accion == "2":
        if not pedido.items:
            print("  El pedido no tiene productos.")
            return
        for i, item in enumerate(pedido.items, 1):
            print(f"  {i}. {item['cantidad']}x {item['producto'].nombre}")
        idx = leer_entero("Número del producto a quitar (0 para cancelar): ")
        if idx == 0:
            return
        if 1 <= idx <= len(pedido.items):
            nombre_prod = pedido.items[idx - 1]["producto"].nombre
            pedido.quitar_producto(nombre_prod)
            print(f"  Producto '{nombre_prod}' quitado.")
        else:
            print("  [Aviso] Número fuera de rango.")
    else:
        print("  Opción no válida.")


def cambiar_estado(rest: Restaurante):
    pedido = seleccionar_pedido(rest)
    if not pedido:
        return
    print(f"Estado actual: {pedido.estado}")
    print("Estados posibles: EN_PREPARACION, LISTO, ENTREGADO, CANCELADO")
    nuevo_estado = input("Nuevo estado: ")
    pedido.cambiar_estado(nuevo_estado)
    print(f"  Estado actualizado a: {pedido.estado}")


def cobrar_pedido(rest: Restaurante):
    pedido = seleccionar_pedido(rest)
    if not pedido:
        return

    subtotal = pedido.calcular_subtotal()
    cargos = pedido.calcular_cargos()
    total = pedido.calcular_total()
    print(f"\nSubtotal: Bs {subtotal:.2f} | Cargos: Bs {cargos:.2f} | Total: Bs {total:.2f}")

    print("Método de pago: 1) Efectivo  2) QR  3) Tarjeta")
    metodo = input("Seleccione (1-3): ").strip()

    if metodo == "1":
        recibido = leer_flotante("Monto recibido (Bs): ")
        comprobante = pedido.cobrar(PagoEfectivo(recibido))
    elif metodo == "2":
        codigo = input("Código de transacción QR (10 dígitos): ")
        comprobante = pedido.cobrar(PagoQR(codigo))
    elif metodo == "3":
        comprobante = pedido.cobrar(PagoTarjeta())
    else:
        print("  Método de pago no válido.")
        return

    print("\n--- Comprobante de Pago ---")
    for clave, valor in comprobante.items():
        print(f"  {clave.capitalize()}: {valor}")


def ver_reporte(rest: Restaurante):
    dia = input("Día para el reporte (ej. lunes, sabado): ").strip()
    reporte = rest.generar_reporte_dia(dia)
    print(f"\n--- Reporte de Ventas ({reporte['dia'].capitalize()}) ---")
    for tipo, monto in reporte["ventas_por_tipo"].items():
        print(f"  {tipo}: Bs {monto:.2f}")
    print(f"TOTAL DEL DÍA: Bs {reporte['total_dia']:.2f}")

    print("\nTop 3 productos más vendidos:")
    if not reporte["top_3_productos"]:
        print("  Sin ventas registradas.")
    else:
        for i, (nombre, cant) in enumerate(reporte["top_3_productos"], 1):
            print(f"  {i}. {nombre} ({cant} unidades)")


def main():
    rest = Restaurante()
    rest.cargar_menu_base()

    while True:
        mostrar_menu_principal()
        opcion = input("Elija una opción (0-9): ").strip()

        try:
            if opcion == "1":
                ver_menu(rest)
            elif opcion == "2":
                registrar_producto(rest)
            elif opcion == "3":
                registrar_cliente(rest)
            elif opcion == "4":
                crear_pedido(rest)
            elif opcion == "5":
                ver_detalle_pedido(rest)
            elif opcion == "6":
                modificar_pedido(rest)
            elif opcion == "7":
                cambiar_estado(rest)
            elif opcion == "8":
                cobrar_pedido(rest)
            elif opcion == "9":
                ver_reporte(rest)
            elif opcion == "0":
                print("Saliendo del sistema...")
                break
            else:
                print("  Opción inválida. Intente nuevamente.")
        except ValueError as e:
            print(f"\n[Error]: {e}")


if __name__ == "__main__":
    main()