from abc import ABC, abstractmethod
from modelo.productos import Producto
from modelo.pagos import MetodoPago

class Pedido(ABC):
    TRANSICIONES_VALIDAS = {
        "REGISTRADO": ["EN_PREPARACION", "CANCELADO"],
        "EN_PREPARACION": ["LISTO"],
        "LISTO": ["ENTREGADO"],
        "ENTREGADO": [],
        "CANCELADO": [],
    }

    def __init__(self, id_pedido: int, cliente, dia: str):
        self._id_pedido = id_pedido
        self._cliente = cliente
        self._dia = dia.strip().lower()
        self._estado = "REGISTRADO"
        self._items = [] 
        self._comprobante_pago = None

    @property
    def id_pedido(self):
        return self._id_pedido

    @property
    def cliente(self):
        return self._cliente

    @property
    def dia(self):
        return self._dia

    @property
    def estado(self):
        return self._estado

    @property
    def items(self):
        return list(self._items)

    @property
    def comprobante_pago(self):
        return self._comprobante_pago

    def cambiar_estado(self, nuevo_estado: str):
        nuevo_estado = nuevo_estado.strip().upper()
        if nuevo_estado not in self.TRANSICIONES_VALIDAS[self._estado]:
            raise ValueError(
                f"Transición inválida: no se puede pasar de {self._estado} a {nuevo_estado}."
            )
        self._estado = nuevo_estado

    def agregar_producto(self, producto: Producto, cantidad: int):
        if self._estado != "REGISTRADO":
            raise ValueError("Solo se pueden agregar productos cuando el pedido está en REGISTRADO.")
        if not (1 <= cantidad <= 20):
            raise ValueError("La cantidad debe estar entre 1 y 20.")
        if not producto.esta_disponible(self._dia):
            raise ValueError(f"El producto '{producto.nombre}' no está disponible el día {self._dia}.")

        # Si el producto ya existe en el pedido, sumamos la cantidad validando el máximo de 20
        for item in self._items:
            if item["producto"] is producto:
                nueva_cantidad = item["cantidad"] + cantidad
                if nueva_cantidad > 20:
                    raise ValueError("La cantidad total de un producto no puede superar 20.")
                item["cantidad"] = nueva_cantidad
                return

        self._items.append({"producto": producto, "cantidad": cantidad})

    def quitar_producto(self, nombre_producto: str):
        if self._estado != "REGISTRADO":
            raise ValueError("Solo se pueden quitar productos cuando el pedido está en REGISTRADO.")
        for i, item in enumerate(self._items):
            if item["producto"].nombre.lower() == nombre_producto.strip().lower():
                self._items.pop(i)
                return
        raise ValueError(f"El producto '{nombre_producto}' no está en el pedido.")

    def calcular_subtotal(self):
        subtotal = sum(
            item["producto"].calcular_precio(self._dia) * item["cantidad"]
            for item in self._items
        )
        return round(subtotal, 2)

    @abstractmethod
    def calcular_cargos(self):
        pass

    @abstractmethod
    def tipo_pedido(self):
        pass

    def calcular_total(self):
        return round(self.calcular_subtotal() + self.calcular_cargos(), 2)

    def cobrar(self, metodo_pago: MetodoPago) -> dict:
        if self._estado == "CANCELADO":
            raise ValueError("No se puede cobrar un pedido cancelado.")
        if not self._items:
            raise ValueError("No se puede cobrar un pedido sin productos.")
        total = self.calcular_total()
        self._comprobante_pago = metodo_pago.procesar_pago(total)
        return self._comprobante_pago


class PedidoLocal(Pedido):
    def __init__(self, id_pedido: int, cliente, dia: str, mesa: int):
        super().__init__(id_pedido, cliente, dia)
        if not (1 <= mesa <= 15):
            raise ValueError("El número de mesa debe estar entre 1 y 15.")
        self._mesa = mesa

    @property
    def mesa(self):
        return self._mesa

    def tipo_pedido(self):
        return "Local"

    def calcular_cargos(self):
        return 0.0


class PedidoParaLlevar(Pedido):
    COSTO_ENVASE = 2.0  # Variante A: Bs 2 por plato

    def tipo_pedido(self):
        return "Para llevar"

    def calcular_cargos(self):
        total_platos = sum(
            item["producto"].contar_platos() * item["cantidad"]
            for item in self._items
        )
        return round(total_platos * self.COSTO_ENVASE, 2)


class PedidoDelivery(Pedido):
    TARIFAS_ZONA = {
        "cercado": 8.0,
        "quillacollo": 15.0,
        "sacaba": 15.0,
        "vinto": 20.0,
    }
    PEDIDO_MINIMO = 40.0       # Variante A: Bs 40
    ENVIO_GRATIS_DESDE = 150.0 # Variante A: Bs 150, solo Cercado

    def __init__(self, id_pedido: int, cliente, dia: str, zona: str):
        super().__init__(id_pedido, cliente, dia)
        zona_limpia = zona.strip().lower()
        if zona_limpia not in self.TARIFAS_ZONA:
            raise ValueError(
                f"Zona inválida. Zonas válidas: {', '.join(self.TARIFAS_ZONA.keys())}."
            )
        self._zona = zona_limpia

    @property
    def zona(self):
        return self._zona

    def tipo_pedido(self):
        return "Delivery"

    def calcular_cargos(self):
        subtotal = self.calcular_subtotal()
        if subtotal < self.PEDIDO_MINIMO:
            raise ValueError(f"El pedido mínimo para delivery es de Bs {self.PEDIDO_MINIMO:.2f}.")
        if self._zona == "cercado" and subtotal >= self.ENVIO_GRATIS_DESDE:
            return 0.0
        return self.TARIFAS_ZONA[self._zona]

    def cobrar(self, metodo_pago: MetodoPago):
        if not metodo_pago.es_valido_para_delivery():
            raise ValueError("Los pedidos por delivery solo aceptan pago en Efectivo o QR.")
        return super().cobrar(metodo_pago)