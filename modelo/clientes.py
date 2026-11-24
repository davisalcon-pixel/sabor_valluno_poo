class Cliente:
    def __init__(self, nombre, telefono):
        self.nombre = nombre
        self.telefono = telefono

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

    @property
    def telefono(self):
        return self._telefono

    @telefono.setter
    def telefono(self, valor):
        tel = str(valor).strip()
        if len(tel) != 8:
            raise ValueError("El teléfono debe tener 8 dígitos")
        if not tel.isdigit():
            raise ValueError("El teléfono solo puede tener números")
        if tel[0] != "6" and tel[0] != "7":
            raise ValueError("El teléfono debe empezar con 6 o 7")
        self._telefono = tel

    def __str__(self):
        return f"{self._nombre} (Tel: {self._telefono})"