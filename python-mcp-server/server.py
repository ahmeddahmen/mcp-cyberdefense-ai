from typing import Dict
from mcp.server.fastmcp import FastMCP

# Création du serveur MCP
mcp = FastMCP("Python MCP Server")

# Déclaration d'un outil MCP
@mcp.tool()
def get_employee_info(name: str) -> Dict[str, str | int]:
    """
    Get information about a given employee name :
    - name
    - salary
    """
    return {
        "employee_name": name,
        "salary": 5400
    }
