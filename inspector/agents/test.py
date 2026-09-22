"""
Plantilla oficial de Inspector
"""

from pathlib import Path


class TestAgent:

    name = "test"
    description = "Agente test"

    def __init__(self):
        self.root = Path.cwd()

    def run(self):

        print("=" * 60)
        print(self.name.upper())
        print("=" * 60)

        print(f"Proyecto: {self.root}")
        print(f"Descripción: {self.description}")

        result = self.execute()

        print()

        print("Estado :", result["status"])
        print("Mensaje:", result["message"])

        if result["warnings"]:
            print("\nWarnings")
            for warning in result["warnings"]:
                print("  •", warning)

        if result["errors"]:
            print("\nErrores")
            for error in result["errors"]:
                print("  •", error)

        if result["info"]:
            print("\nInformación")
            for info in result["info"]:
                print("  •", info)

        print()
        print("=" * 60)
        print("Finalizado.")
        print("=" * 60)

    def execute(self):
        return {
            "status": "ok",
            "message": "Agente ejecutado correctamente",
            "errors": [],
            "warnings": [],
            "info": [],
        }