import json

from parts.config import (
    FABRIC_NAME,
    GATEWAY_IP_ADDRESS,
    PORTS,
    SERIAL_NUMBERS,
    ISLAYER2_ONLY,
    VRF_NAME
)


def networks_payload_gen(network_name, network_id, vlan_id):
    network_template_config = {
        'secondaryGW3': '',
        'suppressArp': '',
        'secondaryGW2': '',
        'secondaryGW1': '',
        'loopbackId': '',
        'enableL3OnBorder': 'false',
        'networkName': network_name,
        'gen_address': '',
        'type': 'Normal',
        'SVI_NETFLOW_MONITOR': '',
        'enableIR': 'false',
        'rtBothAuto': 'false',
        'isLayer2Only': ISLAYER2_ONLY,
        'ENABLE_NETFLOW': 'false',
        'segmentId': network_id,
        'dhcpServerAddr3': '',
        'gatewayIpV6Address': '',
        'dhcpServerAddr2': '',
        'tag': '12345',
        'flagSet': '',
        'nveId': '1',
        'secondaryGW4': '',
        'vlanId': vlan_id,
        'gatewayIpAddress': GATEWAY_IP_ADDRESS,
        'vlanName': network_name,
        'gen_mask': '',
        'mtu': '',
        'intfDescription': '',
        'mcastGroup': '239.1.1.0',
        'igmpVersion': '',
        'trmEnabled': '',
        'VLAN_NETFLOW_MONITOR': '',
        'dhcpServers': '',
        'vrfName': VRF_NAME
    }

    payload = {
        'fabric': FABRIC_NAME,
        'networkName': network_name,
        'displayName': network_name,
        'networkId': network_id,
        'networkTemplate': 'Default_Network_Universal',
        'networkExtensionTemplate': 'Default_Network_Extension_Universal',
        'networkTemplateConfig': json.dumps(network_template_config),
        'vrf': VRF_NAME,
        'primaryNetworkId': -1,
        'type': 'Normal'
    }

    return payload


def attach_payload_gen(network_name, vlan_id):
    ports = PORTS
    lan_attach_list = []
    for serial_number in SERIAL_NUMBERS:
        switch_template = {
            'fabric': FABRIC_NAME,
            'networkName': network_name,
            'serialNumber': None,
            'switchPorts': ports,
            'vlan': vlan_id,
            'deployment': True,
            'instanceValues': 'isActive = false'
        }

        switch_template['serialNumber'] = serial_number
        lan_attach_list.append(switch_template)

    payload = [
        {
            'networkName': network_name,
            'lanAttachList': lan_attach_list
        }
    ]

    return payload
