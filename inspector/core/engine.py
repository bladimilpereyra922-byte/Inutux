from inspector.core.registry import Registry


class Engine:
    def __init__(self):
        self.registry = Registry()

    def run(self, command: str):
        agent = self.registry.get(command)

        if agent is None:
            print(f"[ERROR] Agente '{command}' no encontrado.")
            return

        print(f"[INFO] Ejecutando agente: {command}")
        agent.run()