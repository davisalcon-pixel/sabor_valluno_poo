from abc import ABC, abstractmethod

DESCUENTO_COMBO = 0.10
FACTOR_JARRA = 3

DIAS_SEMANA = ["lunes", "martes", "miercoles", "jueves", "viernes", "sabado", "domingo"]

class Producto(ABC):
    def __init__(self, nombre):
        self.nombre = nombre 

    @property
    def nombre(self):
        return self._nombre

    @nombre.setter
    def nombre(self, valor):
        if not isinstance(valor, str):
            raise ValueError("El nombre debe ser texto")
        valor = valor.strip()
        if valor == "":
            raise ValueError("El nombre no puede estar vacío")
        self._nombre = valor

    # Métodos abstractos: cada subclase está obligada a escribirlos
    @abstractmethod
    def calcular_precio(self):
        pass

    @abstractmethod
    def esta_disponible(self, dia):
        pass

    @abstractmethod
    def contar_platos(self):
        pass

    @abstractmethod
    def contar_productos(self):
        pass

    # Método normal: sirve para que un combo no se contenga a sí mismo
    def contiene(self, otro):
        return self is otro


class ProductoSimple(Producto):
    def __init__(self, nombre, precio):
        super().__init__(nombre)
        self.precio = precio

    @property
    def precio(self):
        return self._precio

    @precio.setter
    def precio(self, valor):
        if not isinstance(valor, (int, float)):
            raise ValueError("El precio debe ser un número")
        if valor <= 0:
            raise ValueError("El precio debe ser mayor que cero")
        self._precio = valor


class Plato(ProductoSimple):
    def __init__(self, nombre, precio, dias_venta=None):
        super().__init__(nombre, precio)
        if dias_venta is None:
            dias_venta = []
        self.dias_venta = dias_venta

    @property
    def dias_venta(self):
        return list(self._dias_venta)  

    @dias_venta.setter
    def dias_venta(self, valor):
        if isinstance(valor, str):
            valor = [valor]
        dias_validos = []
        for dia in valor:
            dia = dia.strip().lower()
            if dia not in DIAS_SEMANA:
                raise ValueError("Día inválido: " + dia)
            dias_validos.append(dia)
        self._dias_venta = dias_validos

    def calcular_precio(self):
        return round(self._precio, 2)

    def esta_disponible(self, dia):
        if len(self._dias_venta) == 0:
            return True  
        dia = dia.strip().lower()
        return dia in self._dias_venta

    def contar_platos(self):
        return 1

    def contar_productos(self):
        return 1


class Bebida(ProductoSimple):
    def __init__(self, nombre, precio_vaso, es_jarra=False):
        super().__init__(nombre, precio_vaso) 
        self.es_jarra = es_jarra

    @property
    def es_jarra(self):
        return self._es_jarra

    @es_jarra.setter
    def es_jarra(self, valor):
        if not isinstance(valor, bool):
            raise ValueError("es_jarra debe ser True o False")
        self._es_jarra = valor

    def calcular_precio(self):
        if self._es_jarra:
            return round(self._precio * FACTOR_JARRA, 2)
        return round(self._precio, 2)

    def esta_disponible(self, dia):
        return True

    def contar_platos(self):
        return 0

    def contar_productos(self):
        return 1


class Combo(Producto):
    def __init__(self, nombre, productos, descuento=DESCUENTO_COMBO):
        super().__init__(nombre)
        self.descuento = descuento
        self._productos = []
        for producto in productos:
            self.agregar_producto(producto)
        if len(self._productos) < 2:
            raise ValueError("Un combo necesita al menos 2 productos")

    @property
    def descuento(self):
        return self._descuento

    @descuento.setter
    def descuento(self, valor):
        if not isinstance(valor, (int, float)):
            raise ValueError("El descuento debe ser un número")
        if valor < 0 or valor >= 1:
            raise ValueError("El descuento debe estar entre 0 y 1 (por ejemplo 0.10)")
        self._descuento = valor

    @property
    def productos(self):
        return list(self._productos)  # devuelve una copia

    def agregar_producto(self, producto):
        if producto.contiene(self):
            raise ValueError("Un combo no puede contenerse a sí mismo")
        self._productos.append(producto)

    def contiene(self, otro):
        if self is otro:
            return True
        for producto in self._productos:
            if producto.contiene(otro):
                return True
        return False

    def calcular_subtotal(self):
        total = 0
        for producto in self._productos:
            total = total + producto.calcular_precio()
        return round(total, 2)

    def calcular_descuento(self):
        return round(self.calcular_subtotal() * self._descuento, 2)

    def calcular_precio(self):
        return round(self.calcular_subtotal() - self.calcular_descuento(), 2)

    def esta_disponible(self, dia):
        for producto in self._productos:
            if not producto.esta_disponible(dia):
                return False
        return True

    def contar_platos(self):
        total = 0
        for producto in self._productos:
            total = total + producto.contar_platos()
        return total

    def contar_productos(self):
        total = 0
        for producto in self._productos:
            total = total + producto.contar_productos()
        return total