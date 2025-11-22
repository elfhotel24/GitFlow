from datetime import datetime

class Empleado:
    def __init__(self, id=None, cedula=None, nombre=None, apellido=None, 
                 salario_base=None, departamento=None, puesto=None, 
                 fecha_contratacion=None, estado=None):
        self.id = id
        self.cedula = cedula
        self.nombre = nombre
        self.apellido = apellido
        self.salario_base = salario_base
        self.departamento = departamento
        self.puesto = puesto
        # Asegurar que fecha_contratacion sea datetime
        if isinstance(fecha_contratacion, str):
            try:
                self.fecha_contratacion = datetime.strptime(fecha_contratacion, '%Y-%m-%d')
            except:
                self.fecha_contratacion = None
        else:
            self.fecha_contratacion = fecha_contratacion
        self.estado = estado
    
    def insertar(self, db):
        query = """
        INSERT INTO Empleados (cedula, nombre, apellido, salario_base, departamento, puesto, fecha_contratacion, estado)
        VALUES (?, ?, ?, ?, ?, ?, ?, ?)
        """
        # Convertir datetime a string para SQL Server
        fecha_str = self.fecha_contratacion.strftime('%Y-%m-%d') if self.fecha_contratacion else None
        
        db.execute_query(query, (
            self.cedula, self.nombre, self.apellido, self.salario_base,
            self.departamento, self.puesto, fecha_str, self.estado
        ))
    
    def actualizar(self, db):
        query = """
        UPDATE Empleados 
        SET cedula=?, nombre=?, apellido=?, salario_base=?, departamento=?, puesto=?, fecha_contratacion=?, estado=?
        WHERE id=?
        """
        # Convertir datetime a string para SQL Server
        fecha_str = self.fecha_contratacion.strftime('%Y-%m-%d') if self.fecha_contratacion else None
        
        db.execute_query(query, (
            self.cedula, self.nombre, self.apellido, self.salario_base,
            self.departamento, self.puesto, fecha_str, self.estado, self.id
        ))
    
    @staticmethod
    def obtener_todos(db):
        query = "SELECT * FROM Empleados ORDER BY id DESC"
        resultados = db.fetch_all(query)
        empleados = []
        if resultados:
            for row in resultados:
                empleados.append(Empleado(
                    id=row[0],
                    cedula=row[1],
                    nombre=row[2],
                    apellido=row[3],
                    salario_base=float(row[4]) if row[4] else 0.0,
                    departamento=row[5],
                    puesto=row[6],
                    fecha_contratacion=row[7],  # Esto puede ser string o datetime
                    estado=row[8]
                ))
        return empleados
    
    @staticmethod
    def obtener_por_id(db, id):
        query = "SELECT * FROM Empleados WHERE id = ?"
        resultado = db.fetch_one(query, (id,))
        if resultado:
            return Empleado(
                id=resultado[0],
                cedula=resultado[1],
                nombre=resultado[2],
                apellido=resultado[3],
                salario_base=float(resultado[4]) if resultado[4] else 0.0,
                departamento=resultado[5],
                puesto=resultado[6],
                fecha_contratacion=resultado[7],  # Esto puede ser string o datetime
                estado=resultado[8]
            )
        return None
    
    @staticmethod
    def obtener_activos(db):
        query = "SELECT * FROM Empleados WHERE estado = 'Activo'"
        resultados = db.fetch_all(query)
        empleados = []
        if resultados:
            for row in resultados:
                empleados.append(Empleado(
                    id=row[0],
                    cedula=row[1],
                    nombre=row[2],
                    apellido=row[3],
                    salario_base=float(row[4]) if row[4] else 0.0,
                    departamento=row[5],
                    puesto=row[6],
                    fecha_contratacion=row[7],  # Esto puede ser string o datetime
                    estado=row[8]
                ))
        return empleados
    
    @staticmethod
    def eliminar(db, id):
        query = "DELETE FROM Empleados WHERE id = ?"
        db.execute_query(query, (id,))
    
    def get_fecha_contratacion_formateada(self):
        """Método seguro para obtener la fecha formateada"""
        if self.fecha_contratacion:
            if isinstance(self.fecha_contratacion, str):
                try:
                    fecha_obj = datetime.strptime(self.fecha_contratacion, '%Y-%m-%d')
                    return fecha_obj.strftime('%d/%m/%Y')
                except:
                    return self.fecha_contratacion
            else:
                return self.fecha_contratacion.strftime('%d/%m/%Y')
        return "N/A"
    
    def get_fecha_contratacion_input(self):
        """Método seguro para formularios HTML"""
        if self.fecha_contratacion:
            if isinstance(self.fecha_contratacion, str):
                return self.fecha_contratacion
            else:
                return self.fecha_contratacion.strftime('%Y-%m-%d')
        return ""