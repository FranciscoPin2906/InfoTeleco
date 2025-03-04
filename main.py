from databases import connect_to_database
from models import Router, Switch, Modem, AccessPoint, Company, Route

def obtener_empresa_fabricante(connection):
    """Solicita al usuario un ID de empresa fabricante válido antes de agregar un dispositivo."""
    while True:
        company_id = input("Ingrese el ID de la empresa fabricante: ")
        if verificar_existencia(connection, "company", company_id):
            return company_id
        print(f"Error: La empresa con ID {company_id} no existe. Intente nuevamente.")

def verificar_existencia(connection, tabla, id):
    """Verifica si un ID existe en la tabla especificada."""
    cursor = connection.cursor()
    cursor.execute(f"SELECT id FROM {tabla} WHERE id = %s", (id,))
    return cursor.fetchone() is not None

def menu():
    connection = connect_to_database()
    while True:
        print("\n--- Menú de Gestión ---")
        print("1. Agregar elemento")
        print("2. Listar elementos")
        print("3. Buscar elemento por ID")
        print("4. Actualizar elemento")
        print("5. Eliminar elemento")
        print("6. Consultas avanzadas")  # <--- NUEVO
        print("7. Salir")

        opcion = input("Seleccione una opción: ")

        if opcion == "1":
            agregar_elemento(connection)
        elif opcion == "2":
            listar_elementos(connection)
        elif opcion == "3":
            buscar_elemento(connection)
        elif opcion == "4":
            actualizar_elemento(connection)
        elif opcion == "5":
            eliminar_elemento(connection)
        elif opcion == "6":
            menu_consultas_avanzadas(connection)  # <--- NUEVO
        elif opcion == "7":
            print("Saliendo del programa...")
            connection.close()
            break
        else:
            print("Opción no válida, intente nuevamente.")

def agregar_elemento(connection):
    print("\nSeleccione el tipo de elemento:")
    print("1. Router")
    print("2. Switch")
    print("3. Modem")
    print("4. Access Point")
    print("5. Empresa")
    print("6. Ruta")
    tipo = input("Ingrese el número de opción: ")

    # Verificamos si el usuario quiere agregar un dispositivo de red
    if tipo in ["1", "2", "3", "4"]:
        # Revisamos si existen empresas en el sistema
        lista_empresas = Company(connection).getAll()
        if not lista_empresas:
            print("No hay empresas registradas. No se puede agregar un dispositivo de red.")
            return
        
        # De lo contrario, sí hay empresas; pedimos el ID de la empresa fabricante
        company_id = obtener_empresa_fabricante(connection)

    if tipo == "1":
        router = Router(
            connection, device_name=input("Nombre: "), manufacturer=input("Fabricante: "),
            model=input("Modelo: "), company_id=company_id, routing_protocols=input("Protocolos: "),
            num_ports=input("Número de puertos: "), firmware_version=input("Versión del firmware: "),
            bandwidth=input("Ancho de banda: ")
        )
        router.put()

    elif tipo == "2":
        switch = Switch(
            connection, device_name=input("Nombre: "), manufacturer=input("Fabricante: "),
            model=input("Modelo: "), company_id=company_id, ports=input("Número de puertos: "),
            switching_capacity=input("Capacidad de conmutación: "),
            mac_address_table_size=input("Tamaño de la tabla MAC: ")
        )
        switch.put()

    elif tipo == "3":
        modem = Modem(
            connection, device_name=input("Nombre: "), manufacturer=input("Fabricante: "),
            model=input("Modelo: "), company_id=company_id, max_speed=input("Velocidad máxima: "),
            connection_type=input("Tipo de conexión: "), ipv6_support=input("Soporte IPv6 (Sí/No): ")
        )
        modem.put()

    elif tipo == "4":
        access_point = AccessPoint(
            connection, device_name=input("Nombre: "), manufacturer=input("Fabricante: "),
            model=input("Modelo: "), company_id=company_id, frequency=input("Frecuencia: "),
            max_clients=input("Máximo de clientes: "), security_protocols=input("Protocolos de seguridad: "),
            range_=input("Rango de cobertura: ")
        )
        access_point.put()

    elif tipo == "5":
        company = Company(
            connection, name=input("Nombre de la empresa: "), city=input("Ciudad: ")
        )
        company.put()

    elif tipo == "6":
        router_id = input("ID del Router: ")
        if not verificar_existencia(connection, "networkdevice", router_id):
            print(f"Error: El router con ID {router_id} no existe.")
            return
        route = Route(
            connection, router_id=router_id, destination_address=input("Dirección destino: "),
            next_hop=input("Salto siguiente: "), metric=input("Métrica: "), interface=input("Interfaz: ")
        )
        route.put()

    else:
        print("Opción no válida.")

def listar_elementos(connection):
    print("\n--- Listado de Elementos ---")

    # Obtener elementos únicos de cada tipo
    routers = Router(connection).getAll()
    switches = Switch(connection).getAll()
    modems = Modem(connection).getAll()
    access_points = AccessPoint(connection).getAll()
    companies = Company(connection).getAll()
    routes = Route(connection).getAll()

    # Unir todas las listas sin duplicados
    elementos = {e["id"]: e for e in routers + switches + modems + access_points + companies + routes}.values()

    for elemento in elementos:
        print(elemento)

def buscar_elemento(connection):
    elemento_id = input("Ingrese el ID del elemento: ")
    dispositivos = Router(connection).getAll() + Switch(connection).getAll() + Modem(connection).getAll() + AccessPoint(connection).getAll()
    empresas = Company(connection).getAll()
    rutas = Route(connection).getAll()

    elementos = dispositivos + empresas + rutas
    encontrado = next((e for e in elementos if e["id"] == int(elemento_id)), None)

    if encontrado:
        print(encontrado)
    else:
        print("Elemento no encontrado.")

def actualizar_elemento(connection):
    elemento_id = input("Ingrese el ID del elemento a actualizar: ")
    
    # 1. Buscar si es una Empresa
    empresas = Company(connection).getAll()
    empresa = next((e for e in empresas if e["id"] == int(elemento_id)), None)
    if empresa:
        # Actualizamos la Empresa
        print("\n-- Actualizar Empresa --")
        new_name = input("Nuevo nombre de la empresa: ")
        new_city = input("Nueva ciudad: ")
        c = Company(connection)
        c.post(elemento_id, new_name, new_city)
        print("Empresa actualizada correctamente.")
        return

    # 2. Buscar si es un Router
    routers = Router(connection).getAll()
    router_data = next((r for r in routers if r["id"] == int(elemento_id)), None)
    if router_data:
        print("\n-- Actualizar Router --")
        new_devicename = input("Nuevo nombre del router: ")
        new_manufacturer = input("Nuevo fabricante: ")
        new_model = input("Nuevo modelo: ")
        new_company_id = input("Nuevo company_id: ")
        new_routing_protocols = input("Nuevos protocolos de enrutamiento: ")
        new_num_ports = input("Nuevo número de puertos: ")
        new_firmware_version = input("Nueva versión de firmware: ")
        new_bandwidth = input("Nuevo ancho de banda: ")
        
        r = Router(connection)
        r.post(elemento_id, new_devicename, new_manufacturer, new_model, new_company_id,
               new_routing_protocols, new_num_ports, new_firmware_version, new_bandwidth)
        print("Router actualizado correctamente.")
        return

    # 3. Buscar si es un Switch
    switches = Switch(connection).getAll()
    switch_data = next((s for s in switches if s["id"] == int(elemento_id)), None)
    if switch_data:
        print("\n-- Actualizar Switch --")
        new_devicename = input("Nuevo nombre del switch: ")
        new_manufacturer = input("Nuevo fabricante: ")
        new_model = input("Nuevo modelo: ")
        new_company_id = input("Nuevo company_id: ")
        new_ports = input("Nuevo número de puertos: ")
        new_switching_capacity = input("Nueva capacidad de conmutación: ")
        new_mac_table_size = input("Nuevo tamaño de la tabla MAC: ")

        sw = Switch(connection)
        sw.post(elemento_id, new_devicename, new_manufacturer, new_model, new_company_id,
                new_ports, new_switching_capacity, new_mac_table_size)
        print("Switch actualizado correctamente.")
        return

    # 4. Buscar si es un Modem
    modems = Modem(connection).getAll()
    modem_data = next((m for m in modems if m["id"] == int(elemento_id)), None)
    if modem_data:
        print("\n-- Actualizar Modem --")
        new_devicename = input("Nuevo nombre del modem: ")
        new_manufacturer = input("Nuevo fabricante: ")
        new_model = input("Nuevo modelo: ")
        new_company_id = input("Nuevo company_id: ")
        new_max_speed = input("Nueva velocidad máxima: ")
        new_connection_type = input("Nuevo tipo de conexión: ")
        new_ipv6_support = input("Soporte IPv6 (Sí/No): ")

        mo = Modem(connection)
        mo.post(elemento_id, new_devicename, new_manufacturer, new_model, new_company_id,
                new_max_speed, new_connection_type, new_ipv6_support)
        print("Modem actualizado correctamente.")
        return

    # 5. Buscar si es un AccessPoint
    aps = AccessPoint(connection).getAll()
    ap_data = next((ap for ap in aps if ap["id"] == int(elemento_id)), None)
    if ap_data:
        print("\n-- Actualizar Access Point --")
        new_devicename = input("Nuevo nombre del AP: ")
        new_manufacturer = input("Nuevo fabricante: ")
        new_model = input("Nuevo modelo: ")
        new_company_id = input("Nuevo company_id: ")
        new_frequency = input("Nueva frecuencia: ")
        new_max_clients = input("Nuevo máximo de clientes: ")
        new_security_protocols = input("Nuevos protocolos de seguridad: ")
        new_range = input("Nuevo rango de cobertura: ")

        ap = AccessPoint(connection)
        ap.post(elemento_id, new_devicename, new_manufacturer, new_model, new_company_id,
                new_frequency, new_max_clients, new_security_protocols, new_range)
        print("Access Point actualizado correctamente.")
        return

    # 6. Buscar si es una Route
    rutas = Route(connection).getAll()
    ruta_data = next((r for r in rutas if r["id"] == int(elemento_id)), None)
    if ruta_data:
        print("\n-- Actualizar Ruta --")
        new_router_id = input("Nuevo ID del router: ")
        new_dest_address = input("Nueva dirección destino: ")
        new_next_hop = input("Nuevo salto siguiente: ")
        new_metric = input("Nueva métrica: ")
        new_interface = input("Nueva interfaz: ")

        rt = Route(connection)
        rt.post(elemento_id, new_router_id, new_dest_address, new_next_hop, new_metric, new_interface)
        print("Ruta actualizada correctamente.")
        return

    # Si no se encontró en ninguna tabla
    print("No se puede actualizar este tipo de elemento (ID no encontrado).")



def eliminar_elemento(connection):
    elemento_id = input("Ingrese el ID del elemento a eliminar: ")

    if Company(connection).delete(elemento_id) or Router(connection).delete(elemento_id) or Switch(connection).delete(elemento_id) or Modem(connection).delete(elemento_id) or AccessPoint(connection).delete(elemento_id) or Route(connection).delete(elemento_id):
        print("Elemento eliminado correctamente.")
    else:
        print("No se encontró el elemento.")

def menu_consultas_avanzadas(connection):
    while True:
        print("\n--- Consultas Avanzadas ---")
        print("1. Mostrar todos los dispositivos con el nombre de su empresa")
        print("2. Mostrar rutas con detalles del router")
        print("3. Mostrar empresas que no tienen routers")
        print("4. Contar cuántos dispositivos tiene cada empresa")
        print("5. Encontrar la interfaz más usada en las rutas")
        print("6. Encontrar el promedio (mean) de la métrica en cada router")
        print("7. [Extra] Mostrar cuántas rutas tiene cada router")
        print("8. [Extra] Mostrar top 3 empresas con más dispositivos")
        print("9. Volver al menú principal")

        opcion = input("Seleccione una consulta: ")

        if opcion == "1":
            consulta_dispositivos_con_empresa(connection)
        elif opcion == "2":
            consulta_rutas_con_detalles(connection)
        elif opcion == "3":
            consulta_empresas_sin_routers(connection)
        elif opcion == "4":
            consulta_dispositivos_por_empresa(connection)
        elif opcion == "5":
            consulta_interfaz_mas_usada(connection)
        elif opcion == "6":
            consulta_promedio_metrica_por_router(connection)
        elif opcion == "7":
            consulta_rutas_por_router(connection)
        elif opcion == "8":
            consulta_top3_empresas(connection)
        elif opcion == "9":
            break
        else:
            print("Opción no válida, intente nuevamente.")

def consulta_dispositivos_con_empresa(connection):
    query = """
        SELECT N.id AS device_id,
               N.device_name,
               N.manufacturer,
               N.model,
               C.name AS company_name
        FROM NetworkDevice N
        JOIN Company C ON N.company_id = C.id
    """
    cursor = connection.cursor(dictionary=True)
    cursor.execute(query)
    filas = cursor.fetchall()
    cursor.close()

    print("\n--- Dispositivos con su Empresa ---")
    for fila in filas:
        print(fila)

def consulta_rutas_con_detalles(connection):
    query = """
        SELECT R.id AS route_id,
               R.destination_address,
               R.next_hop,
               R.metric,
               R.interface,
               ND.device_name AS router_name,
               ND.model AS router_model
        FROM Route R
        JOIN Router RT ON R.router_id = RT.id
        JOIN NetworkDevice ND ON RT.id = ND.id
    """
    cursor = connection.cursor(dictionary=True)
    cursor.execute(query)
    filas = cursor.fetchall()
    cursor.close()

    print("\n--- Rutas con Detalles del Router ---")
    for fila in filas:
        print(fila)

def consulta_empresas_sin_routers(connection):
    query = """
        SELECT C.id, C.name
        FROM Company C
        LEFT JOIN NetworkDevice ND ON C.id = ND.company_id
        LEFT JOIN Router RT ON ND.id = RT.id
        WHERE RT.id IS NULL
    """
    cursor = connection.cursor(dictionary=True)
    cursor.execute(query)
    filas = cursor.fetchall()
    cursor.close()

    print("\n--- Empresas sin Routers ---")
    for fila in filas:
        print(fila)

def consulta_dispositivos_por_empresa(connection):
    query = """
        SELECT C.id AS company_id,
               C.name AS company_name,
               COUNT(N.id) AS total_devices
        FROM Company C
        LEFT JOIN NetworkDevice N ON C.id = N.company_id
        GROUP BY C.id, C.name
        ORDER BY total_devices DESC
    """
    cursor = connection.cursor(dictionary=True)
    cursor.execute(query)
    filas = cursor.fetchall()
    cursor.close()

    print("\n--- Cantidad de Dispositivos por Empresa ---")
    for fila in filas:
        print(fila)

def consulta_interfaz_mas_usada(connection):
    query = """
        SELECT interface,
               COUNT(*) AS count_interface
        FROM Route
        GROUP BY interface
        ORDER BY count_interface DESC
        LIMIT 1
    """
    cursor = connection.cursor(dictionary=True)
    cursor.execute(query)
    fila = cursor.fetchone()
    cursor.close()

    print("\n--- Interfaz Más Usada ---")
    if fila:
        print(f"La interfaz '{fila['interface']}' se usa {fila['count_interface']} veces.")
    else:
        print("No hay rutas registradas.")

def consulta_promedio_metrica_por_router(connection):
    query = """
        SELECT R.router_id,
               ND.device_name AS router_name,
               AVG(R.metric) AS avg_metric
        FROM Route R
        JOIN Router RT ON R.router_id = RT.id
        JOIN NetworkDevice ND ON RT.id = ND.id
        GROUP BY R.router_id, ND.device_name
        ORDER BY avg_metric
    """
    cursor = connection.cursor(dictionary=True)
    cursor.execute(query)
    filas = cursor.fetchall()
    cursor.close()

    print("\n--- Promedio de Métrica por Router ---")
    for fila in filas:
        print(f"Router '{fila['router_name']}' (ID: {fila['router_id']}): métrica promedio = {fila['avg_metric']}")

def consulta_rutas_por_router(connection):
    query = """
        SELECT R.router_id,
               ND.device_name AS router_name,
               COUNT(R.id) AS total_routes
        FROM Route R
        JOIN Router RT ON R.router_id = RT.id
        JOIN NetworkDevice ND ON RT.id = ND.id
        GROUP BY R.router_id, ND.device_name
        ORDER BY total_routes DESC
    """
    cursor = connection.cursor(dictionary=True)
    cursor.execute(query)
    filas = cursor.fetchall()
    cursor.close()

    print("\n--- Número de Rutas por Router ---")
    for fila in filas:
        print(f"Router '{fila['router_name']}' (ID: {fila['router_id']}): {fila['total_routes']} rutas")

def consulta_top3_empresas(connection):
    query = """
        SELECT C.name AS company_name,
               COUNT(N.id) AS total_devices
        FROM Company C
        LEFT JOIN NetworkDevice N ON C.id = N.company_id
        GROUP BY C.id
        ORDER BY total_devices DESC
        LIMIT 3
    """
    cursor = connection.cursor(dictionary=True)
    cursor.execute(query)
    filas = cursor.fetchall()
    cursor.close()

    print("\n--- Top 3 Empresas con más Dispositivos ---")
    for fila in filas:
        print(f"Empresa: {fila['company_name']} - Dispositivos: {fila['total_devices']}")



if __name__ == "__main__":
    menu()
