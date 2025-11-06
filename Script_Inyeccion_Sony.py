import sqlite3, datetime, re

# Conexion y creacion de tablas
conn = sqlite3.connect('sony_accesos.db')
cursor = conn.cursor()
cursor.execute('''CREATE TABLE IF NOT EXISTS accesos (
    id INTEGER PRIMARY KEY, usuario TEXT, proyecto TEXT, rol TEXT, fecha TEXT)''')
cursor.execute('''CREATE TABLE IF NOT EXISTS auditoria (
    id INTEGER PRIMARY KEY, usuario TEXT, accion TEXT, fecha TEXT)''')

# Validación estricta: corta ejecución si hay caracteres no permitidos
def validar(texto, campo):
    if not (3 <= len(texto) <= 50):
        raise ValueError(f"{campo} inválido: debe tener entre 3 y 50 caracteres.")
    if re.search(r'[^a-zA-Z0-9_ \-]', texto):
        raise ValueError(f" ALERTA! {campo} inválido: contiene caracteres no permitidos.")

# Entrada del usuario
try:
    usuario = input("Usuario Sony: ").strip()
    validar(usuario, "Usuario")

    proyecto = input("Proyecto: ").strip()
    validar(proyecto, "Proyecto")

    rol = input("Rol (desarrollador/tester/admin): ").strip().lower()
    if rol not in ['desarrollador', 'tester', 'admin']:
        raise ValueError("Rol no permitido.")

    fecha = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")

    # Inserción segura
    cursor.execute("INSERT INTO accesos (usuario, proyecto, rol, fecha) VALUES (?, ?, ?, ?)",
                   (usuario, proyecto, rol, fecha))
    cursor.execute("INSERT INTO auditoria (usuario, accion, fecha) VALUES (?, ?, ?)",
                   (usuario, f"Solicitud acceso a '{proyecto}' como '{rol}'", fecha))
    conn.commit()
    print("Solicitud registrada correctamente.")

except Exception as e:
    print(f"Error: {e}")
finally:
    conn.close()