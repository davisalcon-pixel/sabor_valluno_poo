from abc import ABC, abstractmethod


class Producto(ABC):
    def __init__(self, nombre: str, precio: float):
        self.nombre = nombre
        self.precio = precio

    @property
    def nombre(self):
        return self._nombre

    @nombre.setter
    def nombre(self, valor: str):
        if not valor or not valor.strip():
            raise ValueError("El nombre del producto no puede estar vacío.")
        self._nombre = valor.strip()

    @property
    def precio(self):
        return self._precio

    @precio.setter
    def precio(self, valor: float):
        if valor <= 0:
            raise ValueError("El precio debe ser mayor que cero.")
        self._precio = round(float(valor), 2)

    @abstractmethod
    def calcular_precio(self, dia: str):
        pass

    @abstractmethod
    def esta_disponible(self, dia: str):
        pass

    @abstractmethod
    def contar_platos(self):
        pass

    def __str__(self):
        return f"{self._nombre} - Bs {self._precio:.2f}"


class Plato(Producto):
    def __init__(self, nombre: str, precio: float, dias_disponibles: list[str] = None):
        super().__init__(nombre, precio)
        if dias_disponibles:
            self._dias_disponibles = [d.strip().lower() for d in dias_disponibles]
        else:
            self._dias_disponibles = []  # Lista vacía = disponible todos los días

    @property
    def dias_disponibles(self) -> list[str]:
        return list(self._dias_disponibles)

    def calcular_precio(self, dia: str):
        return self._precio

    def esta_disponible(self, dia: str):
        if not self._dias_disponibles:
            return True
        return dia.strip().lower() in self._dias_disponibles

    def contar_platos(self):
        return 1


class Bebida(Producto):
    FACTOR_JARRA = 3  

    def __init__(self, nombre: str, precio: float, es_jarra: bool = False):
        super().__init__(nombre, precio)
        self._es_jarra = bool(es_jarra)

    @property
    def es_jarra(self):
        return self._es_jarra

    def calcular_precio(self, dia: str):
        if self._es_jarra:
            return round(self._precio * self.FACTOR_JARRA, 2)
        return self._precio

    def esta_disponible(self, dia: str):
        return True

    def contar_platos(self):
        return 0

    def __str__(self):
        presentacion = "Jarra" if self._es_jarra else "Vaso"
        return f"{self._nombre} ({presentacion}) - Bs {self.calcular_precio(''):.2f}"


class Combo(Producto):
    DESCUENTO = 0.10 

    def __init__(self, nombre: str, productos: list[Producto]):
        if self in productos:
            raise ValueError("Un combo no puede contenerse a sí mismo.")
        if len(productos) < 2:
            raise ValueError("Un combo debe tener al menos 2 productos.")

        self.nombre = nombre
        self._precio = 0.0  
        self._productos = list(productos)

    @property
    def productos(self) -> list[Producto]:
        return list(self._productos)

    def calcular_precio(self, dia: str):
        suma = sum(p.calcular_precio(dia) for p in self._productos)
        return round(suma * (1 - self.DESCUENTO), 2)

    def esta_disponible(self, dia: str):
        return all(p.esta_disponible(dia) for p in self._productos)

    def contar_platos(self):
        return sum(p.contar_platos() for p in self._productos)

    def __str__(self):
        return f"{self._nombre} (Combo) - Bs {self.calcular_precio(''):.2f}"