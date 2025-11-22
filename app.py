import os
import sys

# Add the current directory to Python path
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

from flask import Flask, render_template, request, redirect, url_for, flash
from database import Database
from models.empleado import Empleado
from models.nomina import Nomina
from datetime import datetime

app = Flask(__name__)
app.secret_key = 'clave_secreta_nomina_rd_2024'

# Configuración de la base de datos
db = Database()

# ========== FUNCIÓN PARA CALCULAR ISR ==========
def calcular_isr(salario_bruto):
    """
    Calcula el Impuesto Sobre la Renta (ISR) según la tabla progresiva 
    de República Dominicana para el año 2024
    """
    try:
        # Convertir a float por seguridad
        salario = float(salario_bruto)
        salario_anual = salario * 12
        
        # Tabla progresiva de ISR 2024 República Dominicana (valores anuales)
        if salario_anual <= 416220.00:
            return 0.0
        elif salario_anual <= 624329.00:
            excedente = salario_anual - 416220.00
            isr_anual = excedente * 0.15
        elif salario_anual <= 867123.00:
            excedente = salario_anual - 624329.00
            isr_anual = 31216.00 + (excedente * 0.20)
        else:
            excedente = salario_anual - 867123.00
            isr_anual = 79776.00 + (excedente * 0.25)
        
        # Convertir a mensual y redondear
        isr_mensual = isr_anual / 12
        return round(isr_mensual, 2)
        
    except Exception as e:
        print(f"Error calculando ISR: {e}")
        return 0.0

@app.route('/')
def index():
    return render_template('index.html')

# ========== RUTAS PARA EMPLEADOS ==========
@app.route('/empleados')
def listar_empleados():
    try:
        empleados = Empleado.obtener_todos(db)
        return render_template('empleados/listar.html', empleados=empleados)
    except Exception as e:
        flash(f'❌ Error cargando empleados: {str(e)}', 'error')
        return render_template('empleados/listar.html', empleados=[])

@app.route('/empleados/crear', methods=['GET', 'POST'])
def crear_empleado():
    if request.method == 'POST':
        try:
            empleado = Empleado(
                cedula=request.form['cedula'],
                nombre=request.form['nombre'],
                apellido=request.form['apellido'],
                salario_base=float(request.form['salario_base']),
                departamento=request.form['departamento'],
                puesto=request.form['puesto'],
                fecha_contratacion=datetime.strptime(request.form['fecha_contratacion'], '%Y-%m-%d'),
                estado='Activo'
            )
            empleado.insertar(db)
            flash('✅ Empleado creado exitosamente', 'success')
            return redirect(url_for('listar_empleados'))
        except Exception as e:
            flash(f'❌ Error al crear empleado: {str(e)}', 'error')
    
    return render_template('empleados/crear.html')

@app.route('/empleados/editar/<int:id>', methods=['GET', 'POST'])
def editar_empleado(id):
    try:
        empleado = Empleado.obtener_por_id(db, id)
        if not empleado:
            flash('❌ Empleado no encontrado', 'error')
            return redirect(url_for('listar_empleados'))
        
        if request.method == 'POST':
            try:
                empleado.cedula = request.form['cedula']
                empleado.nombre = request.form['nombre']
                empleado.apellido = request.form['apellido']
                empleado.salario_base = float(request.form['salario_base'])
                empleado.departamento = request.form['departamento']
                empleado.puesto = request.form['puesto']
                empleado.fecha_contratacion = datetime.strptime(request.form['fecha_contratacion'], '%Y-%m-%d')
                empleado.estado = request.form['estado']
                
                empleado.actualizar(db)
                flash('✅ Empleado actualizado exitosamente', 'success')
                return redirect(url_for('listar_empleados'))
            except Exception as e:
                flash(f'❌ Error al actualizar empleado: {str(e)}', 'error')
        
        return render_template('empleados/editar.html', empleado=empleado)
    
    except Exception as e:
        flash(f'❌ Error: {str(e)}', 'error')
        return redirect(url_for('listar_empleados'))

@app.route('/empleados/eliminar/<int:id>')
def eliminar_empleado(id):
    try:
        Empleado.eliminar(db, id)
        flash('✅ Empleado eliminado exitosamente', 'success')
    except Exception as e:
        flash(f'❌ Error al eliminar empleado: {str(e)}', 'error')
    
    return redirect(url_for('listar_empleados'))

# ========== RUTAS PARA NÓMINAS ==========
@app.route('/nominas/calcular', methods=['GET', 'POST'])
def calcular_nomina():
    if request.method == 'POST':
        try:
            periodo = request.form['periodo']
            fecha_pago = datetime.strptime(request.form['fecha_pago'], '%Y-%m-%d')
            
            empleados_activos = Empleado.obtener_activos(db)
            
            if not empleados_activos:
                flash('❌ No hay empleados activos para calcular nómina', 'warning')
                return redirect(url_for('calcular_nomina'))
            
            nominas_creadas = 0
            errores = 0
            
            for empleado in empleados_activos:
                try:
                    # Cálculos según normativa dominicana
                    salario_bruto = empleado.salario_base
                    
                    # AFP (2.87%)
                    afp = round(salario_bruto * 0.0287, 2)
                    
                    # SFS (3.04%)
                    sfs = round(salario_bruto * 0.0304, 2)
                    
                    # ISR (según tabla progresiva)
                    isr = calcular_isr(salario_bruto)
                    
                    salario_neto = round(salario_bruto - afp - sfs - isr, 2)
                    
                    nomina = Nomina(
                        empleado_id=empleado.id,
                        periodo=periodo,
                        fecha_pago=fecha_pago,
                        salario_bruto=salario_bruto,
                        afp=afp,
                        sfs=sfs,
                        isr=isr,
                        salario_neto=salario_neto,
                        estado='Pendiente'
                    )
                    
                    if nomina.insertar(db):
                        nominas_creadas += 1
                        print(f"✅ Nómina creada para empleado {empleado.id}")
                    else:
                        errores += 1
                        print(f"❌ Error creando nómina para empleado {empleado.id}")
                        
                except Exception as e:
                    print(f"❌ Error calculando nómina para empleado {empleado.id}: {e}")
                    errores += 1
            
            if nominas_creadas > 0:
                flash(f'✅ Nómina calculada exitosamente para {nominas_creadas} empleados', 'success')
            if errores > 0:
                flash(f'⚠️ Hubo {errores} errores al calcular algunas nóminas', 'warning')
                
            return redirect(url_for('listar_nominas'))
            
        except Exception as e:
            flash(f'❌ Error al calcular nómina: {str(e)}', 'error')
    
    return render_template('nominas/calcular.html')

@app.route('/nominas')
def listar_nominas():
    try:
        nominas = Nomina.obtener_todas(db)
        print(f"📊 Se encontraron {len(nominas)} nóminas en la base de datos")
        return render_template('nominas/listar.html', nominas=nominas)
    except Exception as e:
        flash(f'❌ Error cargando nóminas: {str(e)}', 'error')
        # Aún con error, pasar una lista vacía para que la plantilla funcione
        return render_template('nominas/listar.html', nominas=[])

if __name__ == '__main__':
    print("🚀 Iniciando servidor de nómina RD...")
    print("📊 Servidor: DESKTOP-O8K0FTD")
    print("🗃️ Base de datos: NominaRD")
    print("🔗 Autenticación: Windows")
    app.run(debug=True, host='0.0.0.0', port=5000)