from netmiko import ConnectHandler

# Definir los parámetros de conexión al router CSR1000v
router = {
    'device_type': 'cisco_ios',
    'host': '192.168.56.102',        # Usa la misma IP que te funcionó en Ansible
    'username': 'cisco',    # Usa el mismo usuario que te funcionó en Ansible
    'password': 'cisco123!',   # Usa la misma contraseña de Ansible
}

# Comandos de configuración para OSPF clásico (IPv4 e IPv6)
ospf_config = [
    'router ospf 1',
    ' router-id 1.1.1.1',
    ' passive-interface GigabitEthernet1',
    ' exit',
    'ipv6 router ospf 1',
    ' router-id 1.1.1.1',
    ' passive-interface GigabitEthernet1',
    ' exit',
    'interface GigabitEthernet1',
    ' ip ospf 1 area 0',
    ' ipv6 ospf 1 area 0',
    'interface Loopback44',
    ' ipv6 ospf 1 area 0'
]

try:
    print("Conectando al dispositivo con Netmiko...")
    net_connect = ConnectHandler(**router)
    net_connect.enable()

    # 1. Configurar OSPF clásico
    print("\n--- Configurando OSPF (IPv4/IPv6) ---")
    output_config = net_connect.send_config_set(ospf_config)
    print(output_config)

    # Demostrar OSPF con show running-config | section ospf
    print("\n--- Verificación de OSPF ---")
    show_ospf = net_connect.send_command("show running-config | section ospf")
    print(show_ospf)

    # 2. Obtener información de IPs y estado de interfaces
    print("\n--- Estado de Interfaces e IPs ---")
    show_interfaces_v4 = net_connect.send_command("show ip interface brief")
    show_interfaces_v6 = net_connect.send_command("show ipv6 interface brief")
    print(show_interfaces_v4)
    print(show_interfaces_v6)

    # 3. Obtener el running-config completo y guardarlo
    print("\n--- Obteniendo Running Configuration ---")
    running_config = net_connect.send_command("show running-config")
    with open("netmiko_running_config.txt", "w") as f:
        f.write(running_config)
    print("¡Running-config guardado con éxito en 'netmiko_running_config.txt'!")

    # 4. Obtener show version
    print("\n--- Mostrando versión del sistema ---")
    show_version = net_connect.send_command("show version")
    print(show_version)

    # Cerrar conexión
    net_connect.disconnect()
    print("\n¡Proceso de Netmiko finalizado correctamente!")

except Exception as e:
    print(f"Error durante la ejecución: {e}")
