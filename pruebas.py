from modelo.productos import Producto, Plato, Bebida, Combo
from modelo.clientes import Cliente
from modelo.pedidos import Pedido, PedidoLocal, PedidoParaLlevar, PedidoDelivery
from modelo.pagos import MetodoPago, PagoEfectivo, PagoQR, PagoTarjeta
from restaurante import Restaurante


def verificar_error(excepcion_esperada, funcion, *args, **kwargs):
    """Ayudante para verificar con assert que una operación lanza el error esperado."""
    try:
        funcion(*args, **kwargs)
    except excepcion_esperada:
        return
    raise AssertionError(f"Se esperaba {excepcion_esperada.__name__}, pero no ocurrió ningún error.")


def prueba_1_caso_referencia_variante_a():
    # Silpancho (35) + Mocochinchi vaso (6) = 41 -> con 10% desc = Bs 36.90
    silpancho = Plato("Silpancho", 35.0, [])
    mocochinchi = Bebida("Mocochinchi", 6.0, es_jarra=False)
    combo = Combo("Combo Valluno", [silpancho, mocochinchi])

    assert combo.calcular_precio("lunes") == 36.90

    # Dos combos por delivery a Quillacollo: 73.80 + 15.00 = Bs 88.80
    cliente = Cliente("Carlos Mamani", "71234567")
    pedido = PedidoDelivery(1, cliente, "lunes", "Quillacollo")
    pedido.agregar_producto(combo, 2)

    assert pedido.calcular_subtotal() == 73.80
    assert pedido.calcular_cargos() == 15.00
    assert pedido.calcular_total() == 88.80


def prueba_2_combo_dentro_de_combo():
    silpancho = Plato("Silpancho", 35.0, [])
    mocochinchi = Bebida("Mocochinchi", 6.0, es_jarra=False)
    pique = Plato("Pique Macho", 50.0, [])

    combo_personal = Combo("Combo Personal", [silpancho, mocochinchi])  # 36.90, 1 plato
    # Mega Combo: (36.90 + 50.00) * 0.90 = 78.21, 2 platos
    mega_combo = Combo("Mega Combo", [combo_personal, pique])

    assert mega_combo.calcular_precio("martes") == 78.21
    assert mega_combo.contar_platos() == 2


def prueba_3_para_llevar_envases_y_jarra():
    silpancho = Plato("Silpancho", 35.0, [])
    pique = Plato("Pique Macho", 50.0, [])
    mocochinchi_vaso = Bebida("Mocochinchi", 6.0, es_jarra=False)
    jarra = Bebida("Jarra Mocochinchi", 6.0, es_jarra=True)  # 6 * 3 = Bs 18.00

    combo_personal = Combo("Combo Personal", [silpancho, mocochinchi_vaso])  # 1 plato
    mega_combo = Combo("Mega Combo", [combo_personal, pique])                # 2 platos

    cliente = Cliente("Ana Quispe", "68765432")
    pedido = PedidoParaLlevar(2, cliente, "miercoles")
    pedido.agregar_producto(mega_combo, 1)  # Bs 78.21 (2 platos)
    pedido.agregar_producto(jarra, 1)       # Bs 18.00 (0 platos)

    assert pedido.calcular_subtotal() == 96.21
    assert pedido.calcular_cargos() == 4.00   # Variante A: 2 platos * Bs 2.00
    assert pedido.calcular_total() == 100.21


def prueba_4_delivery_envio_gratis_solo_cercado():
    pique = Plato("Pique Macho", 50.0, [])
    cliente = Cliente("Luis Rojas", "70001122")

    # Bs 150 en Cercado -> envío gratis
    pedido_cercado = PedidoDelivery(3, cliente, "jueves", "Cercado")
    pedido_cercado.agregar_producto(pique, 3)
    assert pedido_cercado.calcular_subtotal() == 150.00
    assert pedido_cercado.calcular_cargos() == 0.00
    assert pedido_cercado.calcular_total() == 150.00

    # Bs 150 en Quillacollo -> paga Bs 15 igual (Variante A: gratis solo Cercado)
    pedido_quilla = PedidoDelivery(4, cliente, "jueves", "Quillacollo")
    pedido_quilla.agregar_producto(pique, 3)
    assert pedido_quilla.calcular_cargos() == 15.00
    assert pedido_quilla.calcular_total() == 165.00


def prueba_5_delivery_minimo_y_restriccion_tarjeta():
    silpancho = Plato("Silpancho", 35.0, [])
    pique = Plato("Pique Macho", 50.0, [])
    cliente = Cliente("Maria Vargas", "61234567")

    # Pedido menor al mínimo de Bs 40
    pedido_chico = PedidoDelivery(5, cliente, "viernes", "Cercado")
    pedido_chico.agregar_producto(silpancho, 1)
    verificar_error(ValueError, pedido_chico.calcular_cargos)

    # Delivery no acepta pago con tarjeta
    pedido_valido = PedidoDelivery(6, cliente, "viernes", "Cercado")
    pedido_valido.agregar_producto(pique, 1)
    verificar_error(ValueError, pedido_valido.cobrar, PagoTarjeta())


def prueba_6_disponibilidad_chicharron_domingos():
    chicharron = Plato("Chicharrón", 45.0, ["domingo"])
    gaseosa = Bebida("Gaseosa", 8.0, es_jarra=False)
    combo_dominguero = Combo("Combo Dominguero", [chicharron, gaseosa])

    assert chicharron.esta_disponible("domingo") is True
    assert chicharron.esta_disponible("lunes") is False
    assert combo_dominguero.esta_disponible("domingo") is True
    assert combo_dominguero.esta_disponible("lunes") is False

    # No se puede agregar el combo en lunes
    cliente = Cliente("Pedro Flores", "76543210")
    pedido_lunes = PedidoLocal(7, cliente, "lunes", 1)
    verificar_error(ValueError, pedido_lunes.agregar_producto, combo_dominguero, 1)


def prueba_7_estados_y_mesa_ocupada():
    rest = Restaurante()
    rest.cargar_menu_base()
    cliente = rest.registrar_cliente("Sofia Torrico", "72223333")
    silpancho = rest.buscar_producto("Silpancho")

    pedido = rest.crear_pedido_local(cliente, "lunes", 5)
    pedido.agregar_producto(silpancho, 2)

    # La mesa 5 ya está ocupada
    verificar_error(ValueError, rest.crear_pedido_local, cliente, "lunes", 5)

    # Transición inválida: saltar directo a ENTREGADO
    verificar_error(ValueError, pedido.cambiar_estado, "ENTREGADO")

    # Transición válida a EN_PREPARACION
    pedido.cambiar_estado("EN_PREPARACION")

    # Ya no se pueden agregar productos ni cancelar
    verificar_error(ValueError, pedido.agregar_producto, silpancho, 1)
    verificar_error(ValueError, pedido.cambiar_estado, "CANCELADO")

    # Al entregar el pedido, la mesa 5 queda libre
    pedido.cambiar_estado("LISTO")
    pedido.cambiar_estado("ENTREGADO")
    nuevo_pedido = rest.crear_pedido_local(cliente, "lunes", 5)
    assert nuevo_pedido.mesa == 5


def prueba_8_pagos_y_validaciones_cliente():
    # Teléfonos inválidos
    verificar_error(ValueError, Cliente, "Juan", "51234567")  # No empieza en 6 o 7
    verificar_error(ValueError, Cliente, "Juan", "712345")    # Menos de 8 dígitos

    # Pago efectivo con cambio
    comp_ef = PagoEfectivo(100.0).procesar_pago(88.80)
    assert comp_ef["cambio"] == 11.20
    verificar_error(ValueError, PagoEfectivo(50.0).procesar_pago, 88.80)

    # Pago QR (10 dígitos)
    comp_qr = PagoQR("1234567890").procesar_pago(50.0)
    assert comp_qr["codigo_transaccion"] == "1234567890"
    verificar_error(ValueError, PagoQR, "12345")

    # Pago tarjeta (3% comisión)
    comp_tj = PagoTarjeta().procesar_pago(100.0)
    assert comp_tj["comision"] == 3.00
    assert comp_tj["total"] == 103.00


def prueba_9_abstraccion_no_instanciable():
    verificar_error(TypeError, Producto, "Test", 10.0)
    verificar_error(TypeError, Pedido, 1, None, "lunes")
    verificar_error(TypeError, MetodoPago)


def prueba_10_reporte_del_dia():
    rest = Restaurante()
    rest.cargar_menu_base()
    cliente = rest.registrar_cliente("Elena Paz", "69998888")

    silpancho = rest.buscar_producto("Silpancho")
    pique = rest.buscar_producto("Pique Macho")
    gaseosa = rest.buscar_producto("Gaseosa")

    p1 = rest.crear_pedido_local(cliente, "sabado", 1)
    p1.agregar_producto(silpancho, 3)  # Bs 105
    p1.cobrar(PagoEfectivo(110.0))

    p2 = rest.crear_pedido_para_llevar(cliente, "sabado")
    p2.agregar_producto(pique, 1)      # Bs 50 + Bs 2 envase = Bs 52
    p2.agregar_producto(gaseosa, 2)    # Bs 16 -> Total Bs 68
    p2.cobrar(PagoQR("0987654321"))

    reporte = rest.generar_reporte_dia("sabado")
    assert reporte["ventas_por_tipo"]["Local"] == 105.00
    assert reporte["ventas_por_tipo"]["Para llevar"] == 68.00
    assert reporte["total_dia"] == 173.00
    assert reporte["top_3_productos"][0] == ("Silpancho", 3)


if __name__ == "__main__":
    prueba_1_caso_referencia_variante_a()
    prueba_2_combo_dentro_de_combo()
    prueba_3_para_llevar_envases_y_jarra()
    prueba_4_delivery_envio_gratis_solo_cercado()
    prueba_5_delivery_minimo_y_restriccion_tarjeta()
    prueba_6_disponibilidad_chicharron_domingos()
    prueba_7_estados_y_mesa_ocupada()
    prueba_8_pagos_y_validaciones_cliente()
    prueba_9_abstraccion_no_instanciable()
    prueba_10_reporte_del_dia()
    print("Todas las 10 pruebas pasaron correctamente (Variante A).")