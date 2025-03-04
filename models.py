from databases import connect_to_database

class NetworkDB:
    def __init__(self, connection):
        self.__connection = connection

    def execute_query(self, query, params=None, fetch=False):
        cursor = self.__connection.cursor(dictionary=True)
        cursor.execute(query, params or ())
        if fetch:
            result = cursor.fetchall()
        else:
            self.__connection.commit()
            result = None
        cursor.close()
        return result

# --------------------------------------------------------------------------
# Clase Company
# --------------------------------------------------------------------------
class Company(NetworkDB):
    def __init__(self, connection, id=None, name=None, city=None):
        super().__init__(connection)
        self.__id = id
        self.__name = name
        self.__city = city

    def put(self):
        query = "INSERT INTO Company (name, city) VALUES (%s, %s)"
        params = (self.__name, self.__city)
        self.execute_query(query, params)

    def post(self, id, name, city):
        query = "UPDATE Company SET name=%s, city=%s WHERE id=%s"
        params = (name, city, id)
        self.execute_query(query, params)

    def delete(self, id):
        query = "DELETE FROM Company WHERE id=%s"
        self.execute_query(query, (id,))

    def getAll(self):
        query = "SELECT * FROM Company"
        return self.execute_query(query, fetch=True)

# --------------------------------------------------------------------------
# Clase base NetworkDevice
# --------------------------------------------------------------------------
class NetworkDevice(NetworkDB):
    def __init__(self, connection, id=None, device_name=None, manufacturer=None, model=None, company_id=None):
        super().__init__(connection)
        self.__id = id
        self.__device_name = device_name
        self.__manufacturer = manufacturer
        self.__model = model
        self.__company_id = company_id

    def put(self):
        query = """
            INSERT INTO NetworkDevice (device_name, manufacturer, model, company_id)
            VALUES (%s, %s, %s, %s)
        """
        params = (self.__device_name, self.__manufacturer, self.__model, self.__company_id)
        self.execute_query(query, params)

    def post(self, id, device_name, manufacturer, model, company_id):
        query = """
            UPDATE NetworkDevice
            SET device_name=%s, manufacturer=%s, model=%s, company_id=%s
            WHERE id=%s
        """
        params = (device_name, manufacturer, model, company_id, id)
        self.execute_query(query, params)

    def delete(self, id):
        query = "DELETE FROM NetworkDevice WHERE id=%s"
        self.execute_query(query, (id,))

    def getAll(self):
        query = "SELECT * FROM NetworkDevice"
        return self.execute_query(query, fetch=True)

# --------------------------------------------------------------------------
# Router
# --------------------------------------------------------------------------
class Router(NetworkDevice):
    def __init__(self, connection, id=None, routing_protocols=None, num_ports=None,
                 firmware_version=None, bandwidth=None, **kwargs):
        super().__init__(connection, id, **kwargs)
        self.__routing_protocols = routing_protocols
        self.__num_ports = num_ports
        self.__firmware_version = firmware_version
        self.__bandwidth = bandwidth

    def put(self):
        super().put()
        query = """
            INSERT INTO Router (id, routing_protocols, num_ports, firmware_version, bandwidth)
            VALUES (LAST_INSERT_ID(), %s, %s, %s, %s)
        """
        params = (self.__routing_protocols, self.__num_ports, self.__firmware_version, self.__bandwidth)
        self.execute_query(query, params)

    def post(self, id, device_name, manufacturer, model, company_id,
             routing_protocols, num_ports, firmware_version, bandwidth):
        super().post(id, device_name, manufacturer, model, company_id)
        query = """
            UPDATE Router
            SET routing_protocols=%s, num_ports=%s, firmware_version=%s, bandwidth=%s
            WHERE id=%s
        """
        params = (routing_protocols, num_ports, firmware_version, bandwidth, id)
        self.execute_query(query, params)

# --------------------------------------------------------------------------
# Switch
# --------------------------------------------------------------------------
class Switch(NetworkDevice):
    def __init__(self, connection, id=None, ports=None, switching_capacity=None,
                 mac_address_table_size=None, **kwargs):
        super().__init__(connection, id, **kwargs)
        self.__ports = ports
        self.__switching_capacity = switching_capacity
        self.__mac_address_table_size = mac_address_table_size

    def put(self):
        super().put()
        query = """
            INSERT INTO Switch (id, ports, switching_capacity, mac_address_table_size)
            VALUES (LAST_INSERT_ID(), %s, %s, %s)
        """
        params = (self.__ports, self.__switching_capacity, self.__mac_address_table_size)
        self.execute_query(query, params)

    def post(self, id, device_name, manufacturer, model, company_id,
             ports, switching_capacity, mac_address_table_size):
        super().post(id, device_name, manufacturer, model, company_id)
        query = """
            UPDATE Switch
            SET ports=%s, switching_capacity=%s, mac_address_table_size=%s
            WHERE id=%s
        """
        params = (ports, switching_capacity, mac_address_table_size, id)
        self.execute_query(query, params)

# --------------------------------------------------------------------------
# Modem
# --------------------------------------------------------------------------
class Modem(NetworkDevice):
    def __init__(self, connection, id=None, max_speed=None, connection_type=None,
                 ipv6_support=None, **kwargs):
        super().__init__(connection, id, **kwargs)
        self.__max_speed = max_speed
        self.__connection_type = connection_type
        self.__ipv6_support = ipv6_support

    def put(self):
        super().put()
        query = """
            INSERT INTO Modem (id, max_speed, connection_type, ipv6_support)
            VALUES (LAST_INSERT_ID(), %s, %s, %s)
        """
        params = (self.__max_speed, self.__connection_type, self.__ipv6_support)
        self.execute_query(query, params)

    def post(self, id, device_name, manufacturer, model, company_id,
             max_speed, connection_type, ipv6_support):
        super().post(id, device_name, manufacturer, model, company_id)
        query = """
            UPDATE Modem
            SET max_speed=%s, connection_type=%s, ipv6_support=%s
            WHERE id=%s
        """
        params = (max_speed, connection_type, ipv6_support, id)
        self.execute_query(query, params)

# --------------------------------------------------------------------------
# AccessPoint
# --------------------------------------------------------------------------
class AccessPoint(NetworkDevice):
    def __init__(self, connection, id=None, frequency=None, max_clients=None,
                 security_protocols=None, range_=None, **kwargs):
        super().__init__(connection, id, **kwargs)
        self.__frequency = frequency
        self.__max_clients = max_clients
        self.__security_protocols = security_protocols
        self.__range = range_

    def put(self):
        super().put()
        query = """
            INSERT INTO AccessPoint (id, frequency, max_clients, security_protocols, range)
            VALUES (LAST_INSERT_ID(), %s, %s, %s, %s)
        """
        params = (self.__frequency, self.__max_clients, self.__security_protocols, self.__range)
        self.execute_query(query, params)

    def post(self, id, device_name, manufacturer, model, company_id,
             frequency, max_clients, security_protocols, range_):
        super().post(id, device_name, manufacturer, model, company_id)
        query = """
            UPDATE AccessPoint
            SET frequency=%s, max_clients=%s, security_protocols=%s, range=%s
            WHERE id=%s
        """
        params = (frequency, max_clients, security_protocols, range_, id)
        self.execute_query(query, params)

# --------------------------------------------------------------------------
# Route
# --------------------------------------------------------------------------
class Route(NetworkDB):
    def __init__(self, connection, id=None, router_id=None, destination_address=None,
                 next_hop=None, metric=None, interface=None):
        super().__init__(connection)
        self.__id = id
        self.__router_id = router_id
        self.__destination_address = destination_address
        self.__next_hop = next_hop
        self.__metric = metric
        self.__interface = interface

    def put(self):
        query = """
            INSERT INTO Route (router_id, destination_address, next_hop, metric, interface)
            VALUES (%s, %s, %s, %s, %s)
        """
        params = (self.__router_id, self.__destination_address, self.__next_hop,
                  self.__metric, self.__interface)
        self.execute_query(query, params)

    def post(self, id, router_id, destination_address, next_hop, metric, interface):
        query = """
            UPDATE Route
            SET router_id=%s, destination_address=%s, next_hop=%s, metric=%s, interface=%s
            WHERE id=%s
        """
        params = (router_id, destination_address, next_hop, metric, interface, id)
        self.execute_query(query, params)

    def delete(self, id):
        query = "DELETE FROM Route WHERE id=%s"
        self.execute_query(query, (id,))

    def getAll(self):
        query = "SELECT * FROM Route"
        return self.execute_query(query, fetch=True)
