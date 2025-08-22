# netbox/constants.py
from enum import Enum

class API_ENDPOINT(Enum):
    netbox_devices = "/api/dcim/devices/"
    netbox_prefixes = "/api/ipam/prefixes/"
    netbox_ip_addresses = "/api/ipam/ip-addresses/"