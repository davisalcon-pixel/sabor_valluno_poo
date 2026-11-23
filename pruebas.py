from modelo.productos import Producto, Plato, Bebida, Combo
from modelo.clientes import Cliente
from modelo.pedidos import ItemPedido


def crear_combo_referencia():
    silpancho = Plato("Silpancho", 35)
    mocochinchi = Bebida("Mocochinchi", 6)
    return Combo("Combo Valluno", [silpancho, mocochinchi])


def prueba_producto_es_abstracto():
    lanzo_error = False
    try:
        Producto("x")
    except TypeError:
        lanzo_error = True
    assert lanzo_error


def prueba_chicharron_solo_domingos():
    # Regla adicional de la variante A
    chicharron = Plato("Chicharron", 45.5, ["domingo"])
    assert chicharron.esta_disponible("domingo")
    assert not chicharron.esta_disponible("lunes")


def prueba_plato_sin_restriccion():
    silpancho = Plato("Silpancho", 35)
    assert silpancho.esta_disponible("martes")


def prueba_plato_dia_invalido():
    lanzo_error = False
    try:
        Plato("Sopa", 20, ["funday"])
    except ValueError:
        lanzo_error = True
    assert lanzo_error


def prueba_jarra_cuesta_tres_vasos():
    vaso = Bebida("Mocochinchi", 6)
    jarra = Bebida("Mocochinchi", 6, es_jarra=True)
    assert vaso.calcular_precio() == 6.0
    assert jarra.calcular_precio() == 18.0


def prueba_bebida_no_es_plato():
    bebida = Bebida("Coca", 8)
    assert bebida.contar_platos() == 0
    assert bebida.contar_productos() == 1


def prueba_precio_invalido():
    lanzo_error = False
    try:
        Bebida("Coca", 0)
    except ValueError:
        lanzo_error = True
    assert lanzo_error


def prueba_combo_precio_referencia():
    # 35 + 6 = 41, con 10 % de descuento: 41 - 4.10 = 36.90
    combo = crear_combo_referencia()
    assert combo.calcular_precio() == 36.90


def prueba_combo_dentro_de_combo():
    # 36.90 + 20 = 56.90, con 10 % de descuento: 56.90 - 5.69 = 51.21
    combo = crear_combo_referencia()
    grande = Combo("Combo Grande", [combo, Plato("Sopa de mani", 20)])
    assert grande.calcular_precio() == 51.21
    assert grande.contar_platos() == 2
    assert grande.contar_productos() == 3


def prueba_combo_no_se_contiene_a_si_mismo():
    combo = crear_combo_referencia()
    grande = Combo("Combo Grande", [combo, Plato("Sopa de mani", 20)])

    error_directo = False
    try:
        combo.agregar_producto(combo)
    except ValueError:
        error_directo = True
    assert error_directo

    error_indirecto = False
    try:
        combo.agregar_producto(grande)
    except ValueError:
        error_indirecto = True
    assert error_indirecto


def prueba_combo_minimo_dos_productos():
    lanzo_error = False
    try:
        Combo("Solo", [Plato("Silpancho", 35)])
    except ValueError:
        lanzo_error = True
    assert lanzo_error


def prueba_combo_disponibilidad():
    chicharron = Plato("Chicharron", 45, ["domingo"])
    combo = Combo("Combo Domingo", [chicharron, Bebida("Coca", 8)])
    assert combo.esta_disponible("domingo")
    assert not combo.esta_disponible("lunes")


def prueba_cliente_telefono_valido():
    assert Cliente("Ana", "71234567").telefono == "71234567"
    assert Cliente("Luis", "61234567").telefono == "61234567"


def prueba_cliente_telefono_invalido():
    telefonos_malos = ["51234567", "7123456", "7123456a", "712345678"]
    for telefono in telefonos_malos:
        lanzo_error = False
        try:
            Cliente("Ana", telefono)
        except ValueError:
            lanzo_error = True
        assert lanzo_error


def prueba_cliente_nombre_vacio():
    lanzo_error = False
    try:
        Cliente("   ", "71234567")
    except ValueError:
        lanzo_error = True
    assert lanzo_error


def prueba_item_cantidad_limites():
    plato = Plato("Silpancho", 35)
    assert ItemPedido(plato, 1).cantidad == 1
    assert ItemPedido(plato, 20).cantidad == 20
    for cantidad in [0, 21]:
        lanzo_error = False
        try:
            ItemPedido(plato, cantidad)
        except ValueError:
            lanzo_error = True
        assert lanzo_error


def prueba_item_subtotal_y_conteos():
    item = ItemPedido(crear_combo_referencia(), 3)
    assert item.calcular_subtotal() == 110.7
    assert item.contar_platos() == 3
    assert item.contar_productos() == 6


if __name__ == "__main__":
    prueba_producto_es_abstracto()
    prueba_chicharron_solo_domingos()
    prueba_plato_sin_restriccion()
    prueba_plato_dia_invalido()
    prueba_jarra_cuesta_tres_vasos()
    prueba_bebida_no_es_plato()
    prueba_precio_invalido()
    prueba_combo_precio_referencia()
    prueba_combo_dentro_de_combo()
    prueba_combo_no_se_contiene_a_si_mismo()
    prueba_combo_minimo_dos_productos()
    prueba_combo_disponibilidad()
    prueba_cliente_telefono_valido()
    prueba_cliente_telefono_invalido()
    prueba_cliente_nombre_vacio()
    prueba_item_cantidad_limites()
    prueba_item_subtotal_y_conteos()
    print("Todas las pruebas pasaron")