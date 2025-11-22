from datetime import datetime

class Nomina:
    def __init__(self, id=None, empleado_id=None, periodo=None, fecha_pago=None,
                 salario_bruto=None, afp=None, sfs=None, isr=None, salario_neto=None, estado=None):
        self.id = id
        self.empleado_id = empleado_id
        self.periodo = periodo
        # Manejar fecha_pago como datetime
        if isinstance(fecha_pago, str):
            try:
                self.fecha_pago = datetime.strptime(fecha_pago, '%Y-%m-%d')
            except:
                self.fecha_pago = None
        else:
            self.fecha_pago = fecha_pago
        self.salario_bruto = salario_bruto or 0.0
        self.afp = afp or 0.0
        self.sfs = sfs or 0.0
        self.isr = isr or 0.0
        self.salario_neto = salario_neto or 0.0
        self.estado = estado or 'Pendiente'
    
    def insertar(self, db):
        query = """
        INSERT INTO Nominas (empleado_id, periodo, fecha_pago, salario_bruto, afp, sfs, isr, salario_neto, estado)
        VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?)
        """
        # Convertir datetime a string para SQL Server
        fecha_str = self.fecha_pago.strftime('%Y-%m-%d') if self.fecha_pago else None
        
        try:
            db.execute_query(query, (
                self.empleado_id, self.periodo, fecha_str, self.salario_bruto,
                self.afp, self.sfs, self.isr, self.salario_neto, self.estado
            ))
            return True
        except Exception as e:
            print(f"Error insertando nómina: {e}")
            return False
    
    @staticmethod
    def obtener_todas(db):
        try:
            query = "SELECT * FROM Nominas ORDER BY id DESC"
            resultados = db.fetch_all(query)
            nominas = []
            if resultados:
                for row in resultados:
                    # Asegurar que todos los valores numéricos tengan valor por defecto
                    nominas.append(Nomina(
                        id=row[0],
                        empleado_id=row[1],
                        periodo=row[2],
                        fecha_pago=row[3],
                        salario_bruto=float(row[4]) if row[4] is not None else 0.0,
                        afp=float(row[5]) if row[5] is not None else 0.0,
                        sfs=float(row[6]) if row[6] is not None else 0.0,
                        isr=float(row[7]) if row[7] is not None else 0.0,
                        salario_neto=float(row[8]) if row[8] is not None else 0.0,
                        estado=row[9] if row[9] else 'Pendiente'
                    ))
            return nominas
        except Exception as e:
            print(f"Error obteniendo nóminas: {e}")
            return []
    
    @staticmethod
    def obtener_por_id(db, id):
        try:
            query = "SELECT * FROM Nominas WHERE id = ?"
            resultado = db.fetch_one(query, (id,))
            if resultado:
                return Nomina(
                    id=resultado[0],
                    empleado_id=resultado[1],
                    periodo=resultado[2],
                    fecha_pago=resultado[3],
                    salario_bruto=float(resultado[4]) if resultado[4] is not None else 0.0,
                    afp=float(resultado[5]) if resultado[5] is not None else 0.0,
                    sfs=float(resultado[6]) if resultado[6] is not None else 0.0,
                    isr=float(resultado[7]) if resultado[7] is not None else 0.0,
                    salario_neto=float(resultado[8]) if resultado[8] is not None else 0.0,
                    estado=resultado[9] if resultado[9] else 'Pendiente'
                )
            return None
        except Exception as e:
            print(f"Error obteniendo nómina por ID: {e}")
            return None
    
    @staticmethod
    def eliminar(db, id):
        try:
            query = "DELETE FROM Nominas WHERE id = ?"
            db.execute_query(query, (id,))
            return True
        except Exception as e:
            print(f"Error eliminando nómina: {e}")
            return False
    
    def get_fecha_pago_formateada(self):
        """Método seguro para obtener la fecha formateada"""
        if self.fecha_pago:
            if isinstance(self.fecha_pago, str):
                try:
                    fecha_obj = datetime.strptime(self.fecha_pago, '%Y-%m-%d')
                    return fecha_obj.strftime('%d/%m/%Y')
                except:
                    return self.fecha_pago
            else:
                return self.fecha_pago.strftime('%d/%m/%Y')
        return "N/A"