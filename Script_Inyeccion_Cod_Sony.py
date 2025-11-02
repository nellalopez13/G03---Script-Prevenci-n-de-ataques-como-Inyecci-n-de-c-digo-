import sqlite3, datetime, re

# Conexión y creación de tablas
conn = sqlite3.connect('sony_accesos.db')
cursor = conn.cursor()
cursor.execute('''CREATE TABLE IF NOT EXISTS accesos (
    id INTEGER PRIMARY KEY, usuario TEXT, proyecto TEXT, rol TEXT, fecha TEXT)''')
cursor.execute('''CREATE TABLE IF NOT EXISTS auditoria (
    id INTEGER PRIMARY KEY, usuario TEXT, accion TEXT, fecha TEXT)''')

# Validación básica
def validar(texto): 
    if not re.match("^[a-zA-Z0-9_ -]{3,50}$", texto): raise ValueError("Entrada inválida.")

# Entrada del usuario
try:
    usuario = input("Usuario Sony: ").strip()
    proyecto = input("Proyecto: ").strip()
    rol = input("Rol (desarrollador/tester/admin): ").strip().lower()
    validar(usuario); validar(proyecto)
    if rol not in ['desarrollador','tester','admin']: raise ValueError("Rol no permitido.")
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