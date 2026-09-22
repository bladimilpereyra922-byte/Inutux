"""
Plantilla oficial de Inspector
"""

from inspector.core.base import AgentBase


class Agent(AgentBase):

    name = "{{NAME}}"
    description = "{{DESCRIPTION}}"

    def execute(self):

        return {
            "status": "ok",
            "message": "Agente ejecutado correctamente",
            "errors": [],
            "warnings": [],
            "info": [],
        }