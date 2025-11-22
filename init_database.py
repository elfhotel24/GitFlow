from database import Database

def crear_tablas():
    db = Database()
    
    # Script para crear tablas
    scripts = [
        """
        IF NOT EXISTS (SELECT * FROM sysobjects WHERE name='Empleados' AND xtype='U')
        CREATE TABLE Empleados (
            id INT IDENTITY(1,1) PRIMARY KEY,
            cedula VARCHAR(20) UNIQUE NOT NULL,
            nombre VARCHAR(100) NOT NULL,
            apellido VARCHAR(100) NOT NULL,
            salario_base DECIMAL(10,2) NOT NULL,
            departamento VARCHAR(100) NOT NULL,
            puesto VARCHAR(100) NOT NULL,
            fecha_contratacion DATE NOT NULL,
            estado VARCHAR(20) CHECK (estado IN ('Activo', 'Inactivo')) NOT NULL
        )
        """,
        """
        IF NOT EXISTS (SELECT * FROM sysobjects WHERE name='Nominas' AND xtype='U')
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
        """,
        """
        IF NOT EXISTS (SELECT * FROM sysobjects WHERE name='Deducciones' AND xtype='U')
        CREATE TABLE Deducciones (
            id INT IDENTITY(1,1) PRIMARY KEY,
            nomina_id INT FOREIGN KEY REFERENCES Nominas(id),
            tipo VARCHAR(50) NOT NULL,
            monto DECIMAL(10,2) NOT NULL,
            descripcion VARCHAR(255)
        )
        """
    ]
    
    try:
        for script in scripts:
            db.execute_query(script)
        print("✅ Tablas creadas exitosamente!")
        
        # Insertar datos de prueba
        insertar_datos_prueba(db)
        
    except Exception as e:
        print(f"Error creando tablas: {e}")

def insertar_datos_prueba(db):
    try:
        # Verificar si ya existen empleados
        resultado = db.fetch_one("SELECT COUNT(*) FROM Empleados")
        if resultado and resultado[0] == 0:
            # Insertar empleados de prueba
            empleados_prueba = [
                ("40212345678", "Juan", "Pérez", 35000.00, "TI", "Desarrollador", "2023-01-15", "Activo"),
                ("40287654321", "María", "Rodríguez", 42000.00, "RRHH", "Gerente", "2022-05-20", "Activo"),
                ("40211223344", "Carlos", "García", 28000.00, "Ventas", "Asesor", "2023-03-10", "Activo")
            ]
            
            for emp in empleados_prueba:
                db.execute_query(
                    "INSERT INTO Empleados (cedula, nombre, apellido, salario_base, departamento, puesto, fecha_contratacion, estado) VALUES (?, ?, ?, ?, ?, ?, ?, ?)",
                    emp
                )
            
            print("✅ Datos de prueba insertados exitosamente!")
        else:
            print("ℹ️  Ya existen datos en la base de datos")
            
    except Exception as e:
        print(f"Error insertando datos de prueba: {e}")

if __name__ == "__main__":
    crear_tablas()