# Параметры запроса
APPCENTER_URL = "/appcenter/cisco/ndfc/api/v1/lan-fabric/rest/top-down/fabrics"
BASE_URL = "https://10.36.0.104"
VERIFY_SSL = False

# Имя фабрики
FABRIC_NAME = "IX"

# Параметры сети
GATEWAY_IP_ADDRESS = ''
ISLAYER2_ONLY = 'true'
NETWORK_ID = 36000
NETWORK_NAME = 'TEST'
FIRST_VLAN = 501
LAST_VLAN = 502
VLANS = range(FIRST_VLAN, LAST_VLAN+1)
VRF_NAME = 'NA'

# Параметры коммутаторов
SERIAL_NUMBERS = ('FDO21150FB5', 'FDO21150FFG')
PORTS = 'Ethernet1/9,Ethernet1/10'
