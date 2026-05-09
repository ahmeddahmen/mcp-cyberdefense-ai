"""
MCP Server - Network Surveillance
Partie 2 du projet : Serveur MCP de Surveillance Réseau
Outils exposés : scan_ports, check_connections, ping_host, get_network_stats
"""

from mcp.server.fastmcp import FastMCP
import subprocess
import socket
import json
import platform
import psutil
import time

mcp = FastMCP(name="network-security")


@mcp.tool()
def scan_ports(host: str, port_range: str = "1-50") -> dict:
    """
    Scanne les ports ouverts sur un hôte cible (max 50 ports).
    Args:
        host: L'adresse IP ou le nom d'hôte à scanner
        port_range: La plage de ports (ex: '1-50'). Max 50 ports.
    Returns:
        dict avec l'hôte et les ports ouverts
    """
    try:
        start_port, end_port = map(int, port_range.split("-"))
        # Hard limit: never scan more than 50 ports
        end_port = min(end_port, start_port + 49)
        open_ports = []

        for port in range(start_port, end_port + 1):
            sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            sock.settimeout(0.05)
            if sock.connect_ex((host, port)) == 0:
                try:
                    service = socket.getservbyport(port)
                except:
                    service = "unknown"
                open_ports.append({"port": port, "service": service})
            sock.close()

        return {
            "host": host,
            "scanned_range": f"{start_port}-{end_port}",
            "open_ports": open_ports,
            "total_open": len(open_ports)
        }
    except Exception as e:
        return {"error": str(e), "host": host}


@mcp.tool()
def check_connections() -> dict:
    """
    Liste les connexions réseau actives et détecte les connexions suspectes.
    Utilise psutil pour récupérer les connexions réseau actives.
    
    Returns:
        dict avec les connexions actives et les connexions suspectes identifiées
    """
    try:
        connections = []
        suspicious = []

        # Ports considérés comme suspects si en écoute depuis l'extérieur
        suspicious_ports = {4444, 1337, 31337, 8080, 9090, 6666, 6667, 6668, 6669}

        for conn in psutil.net_connections(kind='inet'):
            entry = {
                "fd": conn.fd,
                "family": str(conn.family),
                "type": str(conn.type),
                "local_address": f"{conn.laddr.ip}:{conn.laddr.port}" if conn.laddr else "N/A",
                "remote_address": f"{conn.raddr.ip}:{conn.raddr.port}" if conn.raddr else "N/A",
                "status": conn.status,
                "pid": conn.pid
            }
            connections.append(entry)

            # Détection de connexions suspectes
            if conn.raddr and conn.raddr.port in suspicious_ports:
                suspicious.append({
                    "reason": f"Connexion vers port suspect {conn.raddr.port}",
                    **entry
                })
            elif conn.status == "ESTABLISHED" and conn.raddr:
                ip = conn.raddr.ip
                # Connexions vers des IPs non-locales sur des ports élevés
                if not ip.startswith("127.") and not ip.startswith("192.168.") and not ip.startswith("10."):
                    if conn.raddr.port > 10000:
                        suspicious.append({
                            "reason": "Connexion externe sur port élevé",
                            **entry
                        })

        return {
            "total_connections": len(connections),
            "established": len([c for c in connections if c["status"] == "ESTABLISHED"]),
            "suspicious_count": len(suspicious),
            "suspicious_connections": suspicious[:5],
            "sample_connections": connections[:5]
        }
    except Exception as e:
        return {"error": str(e)}


@mcp.tool()
def ping_host(host: str) -> dict:
    """
    Vérifie la disponibilité d'un hôte et retourne le temps de réponse.
    
    Args:
        host: L'adresse IP ou le nom d'hôte à pinguer
    
    Returns:
        dict avec le statut de disponibilité et le temps de réponse
    """
    try:
        system = platform.system().lower()
        if system == "windows":
            cmd = ["ping", "-n", "4", host]
        else:
            cmd = ["ping", "-c", "4", host]

        result = subprocess.run(cmd, capture_output=True, text=True, timeout=15)
        output = result.stdout

        # Parse response time
        avg_time = None
        if system == "windows":
            for line in output.splitlines():
                if "Average" in line or "Moyenne" in line:
                    parts = line.split("=")
                    if len(parts) > 1:
                        avg_time = parts[-1].strip()
        else:
            for line in output.splitlines():
                if "avg" in line or "rtt" in line:
                    parts = line.split("/")
                    if len(parts) >= 5:
                        avg_time = f"{parts[4]}ms"

        return {
            "host": host,
            "reachable": result.returncode == 0,
            "average_response_time": avg_time,
            "raw_output": output
        }
    except subprocess.TimeoutExpired:
        return {"host": host, "reachable": False, "error": "Timeout"}
    except Exception as e:
        return {"host": host, "reachable": False, "error": str(e)}


@mcp.tool()
def get_network_stats() -> dict:
    """
    Retourne les statistiques réseau globales : paquets envoyés/reçus, erreurs, interfaces.
    
    Returns:
        dict avec les statistiques réseau par interface et les totaux
    """
    try:
        net_io = psutil.net_io_counters(pernic=True)
        interfaces = {}

        for iface, stats in net_io.items():
            interfaces[iface] = {
                "bytes_sent": stats.bytes_sent,
                "bytes_recv": stats.bytes_recv,
                "packets_sent": stats.packets_sent,
                "packets_recv": stats.packets_recv,
                "errors_in": stats.errin,
                "errors_out": stats.errout,
                "drop_in": stats.dropin,
                "drop_out": stats.dropout
            }

        # Global totals
        total = psutil.net_io_counters()
        global_stats = {
            "total_bytes_sent_MB": round(total.bytes_sent / 1024 / 1024, 2),
            "total_bytes_recv_MB": round(total.bytes_recv / 1024 / 1024, 2),
            "total_packets_sent": total.packets_sent,
            "total_packets_recv": total.packets_recv,
            "total_errors_in": total.errin,
            "total_errors_out": total.errout
        }

        return {
            "global": global_stats
        }
    except Exception as e:
        return {"error": str(e)}


if __name__ == "__main__":
    mcp.run(transport="stdio")
