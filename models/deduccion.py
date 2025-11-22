class Deduccion:
    def __init__(self, id=None, nomina_id=None, tipo=None, monto=None, descripcion=None):
        self.id = id
        self.nomina_id = nomina_id
        self.tipo = tipo
        self.monto = monto
        self.descripcion = descripcion
    
    def insertar(self, db):
        query = """
        INSERT INTO Deducciones (nomina_id, tipo, monto, descripcion)
        VALUES (?, ?, ?, ?)
        """
        db.execute_query(query, (self.nomina_id, self.tipo, self.monto, self.descripcion))
    
    @staticmethod
    def obtener_por_nomina(db, nomina_id):
        query = "SELECT * FROM Deducciones WHERE nomina_id = ?"
        resultados = db.fetch_all(query, (nomina_id,))
        deducciones = []
        if resultados:
            for row in resultados:
                deducciones.append(Deduccion(*row))
        return deducciones