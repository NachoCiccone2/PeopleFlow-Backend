class Empleado:
    def __init__(self, nombre, apellido, email, puesto, salario, fecha_ingreso):
        self.nombre = nombre
        self.apellido = apellido
        self.email = email
        self.puesto = puesto
        self.salario = salario
        self.fecha_ingreso = fecha_ingreso
        self.id = None

    def obtener_salario(self):
        return self.salario
    
    def __repr__(self):
        # Representación útil para depuración
        return f"Empleado(id='{self.id}', nombre='{self.nombre}', email='{self.email}')"