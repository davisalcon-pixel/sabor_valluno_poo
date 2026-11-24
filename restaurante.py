from modelo.productos import Producto, Plato, Bebida, Combo
from modelo.clientes import Cliente
from modelo.pedidos import Pedido, PedidoLocal, PedidoParaLlevar, PedidoDelivery


class Restaurante:
    def __init__(self, nombre: str = "Sabor Valluno"):
        self._nombre = nombre
        self._menu: list[Producto] = []
        self._clientes: list[Cliente] = []
        self._pedidos: list[Pedido] = []
        self._contador_pedidos = 1

    @property
    def nombre(self) -> str:
        return self._nombre

    @property
    def menu(self) -> list[Producto]:
        return list(self._menu)

    @property
    def clientes(self) -> list[Cliente]:
        return list(self._clientes)

    @property
    def pedidos(self) -> list[Pedido]:
        return list(self._pedidos)

    # --- Gestión del Menú ---
    def registrar_producto(self, producto: Producto):
        self._menu.append(producto)

    def buscar_producto(self, nombre: str) -> Producto:
        for p in self._menu:
            if p.nombre.lower() == nombre.strip().lower():
                return p
        raise ValueError(f"Producto '{nombre}' no encontrado en el menú.")

    def listar_menu_disponible(self, dia: str) -> list[Producto]:
        return [p for p in self._menu if p.esta_disponible(dia)]

    def cargar_menu_base(self):
        self.registrar_producto(Plato("Silpancho", 35.0, []))
        self.registrar_producto(Plato("Pique Macho", 50.0, []))
        self.registrar_producto(Plato("Chicharrón", 45.0, ["domingo"]))
        self.registrar_producto(Plato("Sopa de Maní", 20.0, []))
        self.registrar_producto(Bebida("Mocochinchi", 6.0, es_jarra=False))
        self.registrar_producto(Bebida("Jarra de Mocochinchi", 6.0, es_jarra=True))
        self.registrar_producto(Bebida("Gaseosa", 8.0, es_jarra=False))

    # --- Gestión de Clientes ---
    def registrar_cliente(self, nombre: str, telefono: str) -> Cliente:
        for c in self._clientes:
            if c.telefono == telefono.strip():
                raise ValueError(f"Ya existe un cliente registrado con el teléfono {telefono}.")
        cliente = Cliente(nombre, telefono)
        self._clientes.append(cliente)
        return cliente

    def buscar_cliente(self, telefono: str) -> Cliente:
        for c in self._clientes:
            if c.telefono == telefono.strip():
                return c
        raise ValueError(f"No existe un cliente con el teléfono {telefono}.")

    # --- Gestión de Pedidos ---
    def _mesa_ocupada(self, mesa: int) -> bool:
        for p in self._pedidos:
            # Una mesa está ocupada si tiene un pedido abierto (ni ENTREGADO ni CANCELADO)
            if getattr(p, "mesa", None) == mesa and p.estado not in ("ENTREGADO", "CANCELADO"):
                return True
        return False

    def crear_pedido_local(self, cliente: Cliente, dia: str, mesa: int) -> PedidoLocal:
        if self._mesa_ocupada(mesa):
            raise ValueError(f"La mesa {mesa} ya tiene un pedido abierto.")
        pedido = PedidoLocal(self._contador_pedidos, cliente, dia, mesa)
        self._pedidos.append(pedido)
        self._contador_pedidos += 1
        return pedido

    def crear_pedido_para_llevar(self, cliente: Cliente, dia: str) -> PedidoParaLlevar:
        pedido = PedidoParaLlevar(self._contador_pedidos, cliente, dia)
        self._pedidos.append(pedido)
        self._contador_pedidos += 1
        return pedido

    def crear_pedido_delivery(self, cliente: Cliente, dia: str, zona: str) -> PedidoDelivery:
        pedido = PedidoDelivery(self._contador_pedidos, cliente, dia, zona)
        self._pedidos.append(pedido)
        self._contador_pedidos += 1
        return pedido

    def buscar_pedido(self, id_pedido: int) -> Pedido:
        for p in self._pedidos:
            if p.id_pedido == id_pedido:
                return p
        raise ValueError(f"Pedido #{id_pedido} no encontrado.")

    # --- Reporte de Ventas del Día ---
    def generar_reporte_dia(self, dia: str) -> dict:
        dia_limpio = dia.strip().lower()
        ventas_por_tipo = {"Local": 0.0, "Para llevar": 0.0, "Delivery": 0.0}
        conteo_productos = {}

        for p in self._pedidos:
            # Solo contamos pedidos del día indicado que no estén cancelados y ya hayan sido cobrados
            if p.dia == dia_limpio and p.estado != "CANCELADO" and p.comprobante_pago is not None:
                tipo = p.tipo_pedido()
                ventas_por_tipo[tipo] = round(ventas_por_tipo[tipo] + p.comprobante_pago["total"], 2)

                for item in p.items:
                    nombre_prod = item["producto"].nombre
                    conteo_productos[nombre_prod] = conteo_productos.get(nombre_prod, 0) + item["cantidad"]

        # Ordenamos de mayor a menor cantidad vendida y tomamos los 3 primeros
        top_3 = sorted(conteo_productos.items(), key=lambda x: x[1], reverse=True)[:3]

        return {
            "dia": dia_limpio,
            "ventas_por_tipo": ventas_por_tipo,
            "total_dia": round(sum(ventas_por_tipo.values()), 2),
            "top_3_productos": top_3,
        }