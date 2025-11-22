from database import Database
from models.empleado import Empleado
from models.nomina import Nomina

def test_system():
    db = Database()
    
    # Test empleados
    print("=== TESTEANDO EMPLEADOS ===")
    empleados = Empleado.obtener_todos(db)
    print(f"Empleados en BD: {len(empleados)}")
    for emp in empleados:
        print(f"  - {emp.nombre} {emp.apellido} - RD$ {emp.salario_base}")
    
    # Test nóminas
    print("\n=== TESTEANDO NÓMINAS ===")
    nominas = Nomina.obtener_todas(db)
    print(f"Nóminas en BD: {len(nominas)}")
    for nom in nominas:
        print(f"  - ID: {nom.id}, Periodo: {nom.periodo}, Neto: RD$ {nom.salario_neto}")
    
    # Test cálculo ISR
    print("\n=== TESTEANDO CÁLCULO ISR ===")
    test_salarios = [25000, 35000, 50000, 80000, 100000]
    for salario in test_salarios:
        from app import calcular_isr
        isr = calcular_isr(salario)
        print(f"  - Salario RD$ {salario:,} -> ISR: RD$ {isr:,.2f}")

if __name__ == "__main__":
    test_system()