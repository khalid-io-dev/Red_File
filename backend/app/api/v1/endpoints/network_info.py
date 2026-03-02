import socket
import ipaddress
from fastapi import APIRouter

router = APIRouter()

@router.get("/network-info")
async def get_network_info():
    """Get host machine network information"""
    try:
        # Get host machine IP
        s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        s.connect(("8.8.8.8", 80))
        host_ip = s.getsockname()[0]
        s.close()
        
        # Calculate network range
        network = ipaddress.IPv4Network(f"{host_ip}/24", strict=False)
        
        return {
            "host_ip": host_ip,
            "network_range": str(network),
            "gateway": str(network.network_address + 1)  # Usually .1
        }
    except Exception as e:
        return {
            "host_ip": "127.0.0.1",
            "network_range": "192.168.1.0/24",
            "error": str(e)
        }
