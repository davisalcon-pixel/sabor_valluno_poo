from restaurante import Restaurante
from modelo.productos import Plato, Bebida, Combo
from modelo.pagos import PagoEfectivo, PagoQR, PagoTarjeta


def mostrar_menu_principal():
    print("\n" + "=" * 45)
    print("   SISTEMA DE GESTIÓN - SABOR VALLUNO")
    print("=" * 45)
    print("1. Ver menú disponible por día")
    print("2. Registrar producto (Plato / Bebida / Combo)")
    print("3. Registrar cliente")
    print("4. Crear pedido")
    print("5. Modificar productos de un pedido")
    print("6. Cambiar estado de un pedido")
    print("7. Cobrar pedido")
    print("8. Reporte de ventas del día")
    print("9. Salir")
    print("=" * 45)


def ver_menu(rest: Restaurante):
    dia = input("Ingrese el día (ej. lunes, domingo): ").strip()
    disponibles = rest.listar_menu_disponible(dia)
    print(f"\n--- Menú disponible ({dia.capitalize()}) ---")
    if not disponibles:
        print("No hay productos disponibles.")
        return
    for i, prod in enumerate(disponibles, 1):
        print(f"{i}. {prod.nombre} - Bs {prod.calcular_precio(dia):.2f}")


def registrar_producto(rest: Restaurante):
    print("\nTipo de producto: 1) Plato  2) Bebida  3) Combo")
    tipo = input("Seleccione (1-3): ").strip()

    if tipo == "1":
        nombre = input("Nombre del plato: ")
        precio = float(input("Precio (Bs): "))
        dias_txt = input("Días disponibles separados por coma (vacío = todos los días): ").strip()
        dias = [d.strip() for d in dias_txt.split(",") if d.strip()] if dias_txt else []
        rest.registrar_producto(Plato(nombre, precio, dias))
        print("Plato registrado correctamente.")

    elif tipo == "2":
        nombre = input("Nombre de la bebida: ")
        precio = float(input("Precio por vaso (Bs): "))
        es_jarra = input("¿Es jarra? (s/n): ").strip().lower() == "s"
        rest.registrar_producto(Bebida(nombre, precio, es_jarra))
        print("Bebida registrada correctamente.")

    elif tipo == "3":
        nombre = input("Nombre del combo: ")
        productos_combo = []
        print("Ingrese los nombres de los productos del combo (escriba 'fin' para terminar):")
        while True:
            nom_prod = input("Producto: ").strip()
            if nom_prod.lower() == "fin":
                break
            productos_combo.append(rest.buscar_producto(nom_prod))
        rest.registrar_producto(Combo(nombre, productos_combo))
        print("Combo registrado correctamente.")

    else:
        print("Opción no válida.")


def registrar_cliente(rest: Restaurante):
    nombre = input("Nombre del cliente: ")
    telefono = input("Teléfono (8 dígitos, inicia en 6 o 7): ")
    cliente = rest.registrar_cliente(nombre, telefono)
    print(f"Cliente registrado: {cliente}")


def crear_pedido(rest: Restaurante):
    telefono = input("Teléfono del cliente: ")
    cliente = rest.buscar_cliente(telefono)
    dia = input("Día del pedido (ej. lunes, domingo): ")

    print("Tipo de pedido: 1) Local  2) Para llevar  3) Delivery")
    tipo = input("Seleccione (1-3): ").strip()

    if tipo == "1":
        mesa = int(input("Número de mesa (1-15): "))
        pedido = rest.crear_pedido_local(cliente, dia, mesa)
    elif tipo == "2":
        pedido = rest.crear_pedido_para_llevar(cliente, dia)
    elif tipo == "3":
        zona = input("Zona (Cercado, Quillacollo, Sacaba, Vinto): ")
        pedido = rest.crear_pedido_delivery(cliente, dia, zona)
    else:
        print("Tipo de pedido no válido.")
        return

    print(f"\nPedido #{pedido.id_pedido} creado ({pedido.tipo_pedido()}). Agregue productos:")
    while True:
        nom_prod = input("Nombre del producto (o 'fin' para terminar): ").strip()
        if nom_prod.lower() == "fin":
            break
        cantidad = int(input("Cantidad (1-20): "))
        prod = rest.buscar_producto(nom_prod)
        pedido.agregar_producto(prod, cantidad)
        print(f"Agregado: {cantidad}x {prod.nombre}")

    print(f"Pedido #{pedido.id_pedido} guardado. Subtotal actual: Bs {pedido.calcular_subtotal():.2f}")


def modificar_pedido(rest: Restaurante):
    id_pedido = int(input("ID del pedido: "))
    pedido = rest.buscar_pedido(id_pedido)
    print(f"Pedido #{pedido.id_pedido} | Estado: {pedido.estado}")
    print("1) Agregar producto  2) Quitar producto")
    accion = input("Seleccione (1-2): ").strip()

    if accion == "1":
        nom_prod = input("Nombre del producto: ")
        cantidad = int(input("Cantidad (1-20): "))
        prod = rest.buscar_producto(nom_prod)
        pedido.agregar_producto(prod, cantidad)
        print("Producto agregado.")
    elif accion == "2":
        nom_prod = input("Nombre del producto a quitar: ")
        pedido.quitar_producto(nom_prod)
        print("Producto quitado.")
    else:
        print("Opción no válida.")


def cambiar_estado(rest: Restaurante):
    id_pedido = int(input("ID del pedido: "))
    pedido = rest.buscar_pedido(id_pedido)
    print(f"Estado actual: {pedido.estado}")
    nuevo_estado = input("Nuevo estado (EN_PREPARACION, LISTO, ENTREGADO, CANCELADO): ")
    pedido.cambiar_estado(nuevo_estado)
    print(f"Estado actualizado a: {pedido.estado}")


def cobrar_pedido(rest: Restaurante):
    id_pedido = int(input("ID del pedido: "))
    pedido = rest.buscar_pedido(id_pedido)

    subtotal = pedido.calcular_subtotal()
    cargos = pedido.calcular_cargos()
    total = pedido.calcular_total()
    print(f"\nSubtotal: Bs {subtotal:.2f} | Cargos: Bs {cargos:.2f} | Total: Bs {total:.2f}")

    print("Método de pago: 1) Efectivo  2) QR  3) Tarjeta")
    metodo = input("Seleccione (1-3): ").strip()

    if metodo == "1":
        recibido = float(input("Monto recibido (Bs): "))
        comprobante = pedido.cobrar(PagoEfectivo(recibido))
    elif metodo == "2":
        codigo = input("Código de transacción QR (10 dígitos): ")
        comprobante = pedido.cobrar(PagoQR(codigo))
    elif metodo == "3":
        comprobante = pedido.cobrar(PagoTarjeta())
    else:
        print("Método de pago no válido.")
        return

    print("\n--- Comprobante de Pago ---")
    for clave, valor in comprobante.items():
        print(f"{clave.capitalize()}: {valor}")


def ver_reporte(rest: Restaurante):
    dia = input("Día para el reporte (ej. sabado): ")
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
        opcion = input("Elija una opción (1-9): ").strip()

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
                modificar_pedido(rest)
            elif opcion == "6":
                cambiar_estado(rest)
            elif opcion == "7":
                cobrar_pedido(rest)
            elif opcion == "8":
                ver_reporte(rest)
            elif opcion == "9":
                print("Saliendo del sistema...")
                break
            else:
                print("Opción inválida. Intente nuevamente.")
        except ValueError as e:
            print(f"\n[Error]: {e}")


if __name__ == "__main__":
    main()