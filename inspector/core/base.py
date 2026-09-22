from pathlib import Path


class AgentBase:

    name = "agent"
    description = "Base Agent"

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
        print(f"Estado : {result['status']}")
        print(f"Mensaje: {result['message']}")

        if result["info"]:
            print("\nInformación")
            for item in result["info"]:
                print(f"  ✔ {item}")

        if result["warnings"]:
            print("\nAdvertencias")
            for item in result["warnings"]:
                print(f"  ⚠ {item}")

        if result["errors"]:
            print("\nErrores")
            for item in result["errors"]:
                print(f"  ✖ {item}")

        print("\n" + "=" * 60)

    def execute(self):
        raise NotImplementedError(
            "Cada agente debe implementar execute()."
        )

    def ok(self, message, info=None):
        return {
            "status": "ok",
            "message": message,
            "errors": [],
            "warnings": [],
            "info": info or [],
        }

    def warning(self, message, warnings, info=None):
        return {
            "status": "warning",
            "message": message,
            "errors": [],
            "warnings": warnings,
            "info": info or [],
        }

    def error(self, message, errors, info=None):
        return {
            "status": "error",
            "message": message,
            "errors": errors,
            "warnings": [],
            "info": info or [],
        }