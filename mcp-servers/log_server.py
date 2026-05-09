"""
MCP Server - Log Analysis
Partie 3 du projet : Serveur MCP d'Analyse de Logs
Outils exposés : parse_auth_logs, detect_bruteforce, get_failed_logins, search_log_pattern
"""

from mcp.server.fastmcp import FastMCP
from collections import Counter
from pathlib import Path
import re
import os
import platform
import json
from datetime import datetime

mcp = FastMCP(name="log-security")

# Simulated auth log for Windows (since /var/log/auth.log is Linux-only)
SIMULATED_AUTH_LOG = """
May  4 10:01:23 server sshd[1234]: Failed password for root from 192.168.1.45 port 22 ssh2
May  4 10:01:25 server sshd[1234]: Failed password for root from 192.168.1.45 port 22 ssh2
May  4 10:01:27 server sshd[1234]: Failed password for admin from 192.168.1.45 port 22 ssh2
May  4 10:01:29 server sshd[1234]: Failed password for root from 192.168.1.45 port 22 ssh2
May  4 10:01:31 server sshd[1234]: Failed password for root from 192.168.1.45 port 22 ssh2
May  4 10:01:33 server sshd[1234]: Failed password for root from 192.168.1.45 port 22 ssh2
May  4 10:02:10 server sshd[1235]: Failed password for ubuntu from 10.0.0.23 port 22 ssh2
May  4 10:02:12 server sshd[1235]: Failed password for ubuntu from 10.0.0.23 port 22 ssh2
May  4 10:02:14 server sshd[1235]: Failed password for pi from 10.0.0.23 port 22 ssh2
May  4 10:02:16 server sshd[1235]: Failed password for admin from 10.0.0.23 port 22 ssh2
May  4 10:02:18 server sshd[1235]: Failed password for root from 10.0.0.23 port 22 ssh2
May  4 10:02:20 server sshd[1235]: Failed password for test from 10.0.0.23 port 22 ssh2
May  4 10:02:22 server sshd[1235]: Failed password for user from 10.0.0.23 port 22 ssh2
May  4 10:02:24 server sshd[1235]: Failed password for root from 10.0.0.23 port 22 ssh2
May  4 10:03:05 server sshd[1236]: Failed password for root from 172.16.0.7 port 22 ssh2
May  4 10:03:07 server sshd[1236]: Failed password for admin from 172.16.0.7 port 22 ssh2
May  4 10:03:09 server sshd[1236]: Failed password for root from 172.16.0.7 port 22 ssh2
May  4 10:03:11 server sshd[1236]: Failed password for root from 172.16.0.7 port 22 ssh2
May  4 10:03:13 server sshd[1236]: Failed password for root from 172.16.0.7 port 22 ssh2
May  4 10:03:15 server sshd[1236]: Failed password for root from 172.16.0.7 port 22 ssh2
May  4 10:04:00 server sshd[1237]: Accepted password for john from 192.168.1.100 port 22 ssh2
May  4 10:05:00 server sshd[1238]: Failed password for root from 203.0.113.5 port 22 ssh2
May  4 10:05:02 server sshd[1238]: Failed password for root from 203.0.113.5 port 22 ssh2
May  4 10:05:04 server sshd[1238]: Failed password for root from 203.0.113.5 port 22 ssh2
May  4 10:06:00 server sudo[1239]: john : TTY=pts/0 ; PWD=/home/john ; USER=root ; COMMAND=/bin/ls
May  4 10:07:00 server sshd[1240]: Invalid user hacker from 198.51.100.1 port 22 ssh2
May  4 10:07:02 server sshd[1240]: Failed password for invalid user hacker from 198.51.100.1 port 22 ssh2
"""

def _get_auth_log_path() -> str:
    """Returns the path to auth.log or uses simulated data on Windows."""
    if platform.system() != "Windows":
        paths = ["/var/log/auth.log", "/var/log/secure"]
        for p in paths:
            if Path(p).exists():
                return p
    return None


def _read_log_lines(n_lines: int = 100) -> list:
    """Read log lines from auth.log or simulated data."""
    log_path = _get_auth_log_path()
    if log_path:
        try:
            with open(log_path, "r", errors="ignore") as f:
                lines = f.readlines()
                return lines[-n_lines:]
        except Exception:
            pass
    # Use simulated log
    return SIMULATED_AUTH_LOG.strip().splitlines()[-n_lines:]


@mcp.tool()
def parse_auth_logs(n_lines: int = 50) -> dict:
    """
    Lit les dernières n lignes du journal d'authentification et détecte les tentatives SSH échouées.
    Sur Windows, utilise des logs simulés réalistes.
    
    Args:
        n_lines: Nombre de lignes à analyser (défaut: 50)
    
    Returns:
        dict avec les tentatives échouées, les connexions réussies et un résumé
    """
    try:
        lines = _read_log_lines(n_lines)
        failed_attempts = []
        successful_logins = []
        invalid_users = []

        failed_pattern = re.compile(
            r"(\w+\s+\d+\s+\d+:\d+:\d+).*Failed password for (?:invalid user )?(\w+) from ([\d.]+)"
        )
        success_pattern = re.compile(
            r"(\w+\s+\d+\s+\d+:\d+:\d+).*Accepted \w+ for (\w+) from ([\d.]+)"
        )
        invalid_pattern = re.compile(
            r"(\w+\s+\d+\s+\d+:\d+:\d+).*Invalid user (\w+) from ([\d.]+)"
        )

        for line in lines:
            m = failed_pattern.search(line)
            if m:
                failed_attempts.append({
                    "timestamp": m.group(1),
                    "user": m.group(2),
                    "source_ip": m.group(3)
                })
            m = success_pattern.search(line)
            if m:
                successful_logins.append({
                    "timestamp": m.group(1),
                    "user": m.group(2),
                    "source_ip": m.group(3)
                })
            m = invalid_pattern.search(line)
            if m:
                invalid_users.append({
                    "timestamp": m.group(1),
                    "user": m.group(2),
                    "source_ip": m.group(3)
                })

        return {
            "lines_analyzed": len(lines),
            "failed_attempts_count": len(failed_attempts),
            "successful_logins_count": len(successful_logins),
            "invalid_user_attempts": len(invalid_users),
            "failed_attempts": failed_attempts[:20],  # limit to 20
            "successful_logins": successful_logins[:10],
            "invalid_users": invalid_users[:10],
            "source": "simulated" if not _get_auth_log_path() else _get_auth_log_path()
        }
    except Exception as e:
        return {"error": str(e)}


@mcp.tool()
def detect_bruteforce(threshold: int = 5) -> dict:
    """
    Détecte les IPs suspectes ayant dépassé un seuil de tentatives de connexion échouées (force brute SSH).
    
    Args:
        threshold: Nombre minimum de tentatives pour considérer une IP suspecte (défaut: 5)
    
    Returns:
        dict avec les IPs suspectes, leur nombre de tentatives et une recommandation
    """
    try:
        lines = _read_log_lines(200)
        ip_counts = Counter()
        ip_users = {}

        failed_pattern = re.compile(
            r"Failed password for (?:invalid user )?(\w+) from ([\d.]+)"
        )

        for line in lines:
            m = failed_pattern.search(line)
            if m:
                user = m.group(1)
                ip = m.group(2)
                ip_counts[ip] += 1
                if ip not in ip_users:
                    ip_users[ip] = set()
                ip_users[ip].add(user)

        suspects = {}
        for ip, count in ip_counts.items():
            if count >= threshold:
                suspects[ip] = {
                    "attempts": count,
                    "targeted_users": list(ip_users.get(ip, [])),
                    "risk_level": "CRITICAL" if count >= 20 else "HIGH" if count >= 10 else "MEDIUM"
                }

        # Sort by attempts descending
        sorted_suspects = dict(sorted(suspects.items(), key=lambda x: x[1]["attempts"], reverse=True))

        recommendation = ""
        if sorted_suspects:
            ips = list(sorted_suspects.keys())
            if platform.system() == "Windows":
                recommendation = f"Bloquer ces IPs via le pare-feu Windows : netsh advfirewall firewall add rule name='Block Brute Force' dir=in action=block remoteip={','.join(ips)}"
            else:
                recommendation = f"Bloquer ces IPs via iptables : " + " && ".join([f"iptables -A INPUT -s {ip} -j DROP" for ip in ips])

        return {
            "threshold": threshold,
            "total_suspects": len(sorted_suspects),
            "suspects": sorted_suspects,
            "recommendation": recommendation
        }
    except Exception as e:
        return {"error": str(e)}


@mcp.tool()
def get_failed_logins() -> dict:
    """
    Retourne la liste des utilisateurs avec des tentatives de connexion échouées et leurs statistiques.
    
    Returns:
        dict avec les utilisateurs ciblés, le nombre de tentatives par utilisateur et les IPs sources
    """
    try:
        lines = _read_log_lines(200)
        user_counts = Counter()
        user_ips = {}

        failed_pattern = re.compile(
            r"Failed password for (?:invalid user )?(\w+) from ([\d.]+)"
        )

        for line in lines:
            m = failed_pattern.search(line)
            if m:
                user = m.group(1)
                ip = m.group(2)
                user_counts[user] += 1
                if user not in user_ips:
                    user_ips[user] = set()
                user_ips[user].add(ip)

        failed_users = []
        for user, count in user_counts.most_common():
            failed_users.append({
                "username": user,
                "failed_attempts": count,
                "source_ips": list(user_ips.get(user, [])),
                "is_system_account": user in ["root", "admin", "administrator", "ubuntu", "pi", "test"]
            })

        return {
            "total_targeted_users": len(failed_users),
            "most_targeted": failed_users[0]["username"] if failed_users else None,
            "failed_logins": failed_users
        }
    except Exception as e:
        return {"error": str(e)}


@mcp.tool()
def search_log_pattern(pattern: str, logfile: str = "auth") -> dict:
    """
    Recherche un motif regex dans un fichier de log donné.
    
    Args:
        pattern: Expression régulière à rechercher
        logfile: Nom du fichier de log ('auth', 'syslog', ou chemin absolu)
    
    Returns:
        dict avec les lignes correspondantes et le nombre de correspondances
    """
    try:
        # Resolve log file
        if logfile == "auth":
            log_path = _get_auth_log_path()
            if not log_path:
                lines = SIMULATED_AUTH_LOG.strip().splitlines()
            else:
                with open(log_path, "r", errors="ignore") as f:
                    lines = f.readlines()
        elif logfile == "syslog":
            syslog_path = "/var/log/syslog"
            if Path(syslog_path).exists():
                with open(syslog_path, "r", errors="ignore") as f:
                    lines = f.readlines()
            else:
                lines = SIMULATED_AUTH_LOG.strip().splitlines()
        elif Path(logfile).exists():
            with open(logfile, "r", errors="ignore") as f:
                lines = f.readlines()
        else:
            return {"error": f"Log file '{logfile}' not found"}

        compiled = re.compile(pattern, re.IGNORECASE)
        matches = []
        for i, line in enumerate(lines, 1):
            if compiled.search(line):
                matches.append({"line_number": i, "content": line.strip()})

        return {
            "pattern": pattern,
            "logfile": logfile,
            "total_lines": len(lines),
            "matches_count": len(matches),
            "matches": matches[:100]  # limit to 100 results
        }
    except re.error as e:
        return {"error": f"Invalid regex pattern: {str(e)}"}
    except Exception as e:
        return {"error": str(e)}


if __name__ == "__main__":
    mcp.run(transport="stdio")
