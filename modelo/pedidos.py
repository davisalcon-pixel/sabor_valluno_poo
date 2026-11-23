CANTIDAD_MINIMA = 1
CANTIDAD_MAXIMA = 20


class EstadoPedido:
    # Cada estado es un texto fijo. Se usa así: EstadoPedido.REGISTRADO
    REGISTRADO = "REGISTRADO"
    EN_PREPARACION = "EN_PREPARACION"
    LISTO = "LISTO"
    ENTREGADO = "ENTREGADO"
    CANCELADO = "CANCELADO"

    TODOS = [REGISTRADO, EN_PREPARACION, LISTO, ENTREGADO, CANCELADO]


class ItemPedido:
    def __init__(self, producto, cantidad):
        if producto is None:
            raise ValueError("El ítem necesita un producto")
        self._producto = producto
        self.cantidad = cantidad  # usa el setter, así se valida

    @property
    def producto(self):
        return self._producto

    @property
    def cantidad(self):
        return self._cantidad

    @cantidad.setter
    def cantidad(self, valor):
        if not isinstance(valor, int):
            raise ValueError("La cantidad debe ser un número entero")
        if valor < CANTIDAD_MINIMA or valor > CANTIDAD_MAXIMA:
            raise ValueError("La cantidad debe estar entre 1 y 20")
        self._cantidad = valor

    def calcular_subtotal(self):
        return round(self._producto.calcular_precio() * self._cantidad, 2)

    def contar_platos(self):
        return self._producto.contar_platos() * self._cantidad

    def contar_productos(self):
        return self._producto.contar_productos() * self._cantidad