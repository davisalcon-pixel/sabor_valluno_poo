from abc import ABC, abstractmethod

class MetodoPago(ABC):
    @property
    @abstractmethod
    def nombre(self):
        pass

    @abstractmethod
    def es_valido_para_delivery(self):
        pass

    @abstractmethod
    def procesar_pago(self, total: float):
        pass

class PagoEfectivo(MetodoPago):
    def __init__(self, monto_recibido: float):
        if monto_recibido <= 0:
            raise ValueError("El monto recibido debe ser mayor que cero.")
        self._monto_recibido = round(float(monto_recibido), 2)

    @property
    def nombre(self):
        return "Efectivo"

    @property
    def monto_recibido(self):
        return self._monto_recibido

    def es_valido_para_delivery(self):
        return True

    def procesar_pago(self, total: float):
        total = round(total, 2)
        if self._monto_recibido < total:
            raise ValueError(
                f"Monto insuficiente. Total: Bs {total:.2f}, recibido: Bs {self._monto_recibido:.2f}."
            )
        cambio = round(self._monto_recibido - total, 2)
        return {
            "metodo": self.nombre,
            "total": total,
            "monto_recibido": self._monto_recibido,
            "cambio": cambio,
        }


class PagoQR(MetodoPago):
    def __init__(self, codigo_transaccion: str):
        codigo = codigo_transaccion.strip()
        if not (codigo.isdigit() and len(codigo) == 10):
            raise ValueError("El código de transacción QR debe tener exactamente 10 dígitos.")
        self._codigo_transaccion = codigo

    @property
    def nombre(self):
        return "QR"

    @property
    def codigo_transaccion(self):
        return self._codigo_transaccion

    def es_valido_para_delivery(self):
        return True

    def procesar_pago(self, total: float):
        total = round(total, 2)
        return {
            "metodo": self.nombre,
            "total": total,
            "codigo_transaccion": self._codigo_transaccion,
        }


class PagoTarjeta(MetodoPago):
    COMISION = 0.03

    @property
    def nombre(self):
        return "Tarjeta"

    def es_valido_para_delivery(self):
        # El delivery solo acepta efectivo o QR
        return False

    def procesar_pago(self, total: float):
        total = round(total, 2)
        comision = round(total * self.COMISION, 2)
        total_final = round(total + comision, 2)
        return {
            "metodo": self.nombre,
            "subtotal_pago": total,
            "comision": comision,
            "total": total_final,
        }