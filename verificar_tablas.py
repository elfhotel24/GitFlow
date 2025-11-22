from database import Database

def verificar_tabla_nominas():
    db = Database()
    
    # Verificar si la tabla Nominas existe
    check_query = """
    IF NOT EXISTS (SELECT * FROM sysobjects WHERE name='Nominas' AND xtype='U')
    BEGIN
        CREATE TABLE Nominas (
            id INT IDENTITY(1,1) PRIMARY KEY,
            empleado_id INT FOREIGN KEY REFERENCES Empleados(id),
            periodo VARCHAR(20) NOT NULL,
            fecha_pago DATE NOT NULL,
            salario_bruto DECIMAL(10,2) NOT NULL,
            afp DECIMAL(10,2) NOT NULL,
            sfs DECIMAL(10,2) NOT NULL,
            isr DECIMAL(10,2) NOT NULL,
            salario_neto DECIMAL(10,2) NOT NULL,
            estado VARCHAR(20) CHECK (estado IN ('Pendiente', 'Pagado')) NOT NULL,
            fecha_creacion DATETIME DEFAULT GETDATE()
        )
        PRINT 'Tabla Nominas creada exitosamente'
    END
    ELSE
        PRINT 'La tabla Nominas ya existe'
    """
    
    try:
        db.execute_query(check_query)
        print("✅ Verificación de tabla Nominas completada")
    except Exception as e:
        print(f"❌ Error verificando tabla Nominas: {e}")

if __name__ == "__main__":
    verificar_tabla_nominas()