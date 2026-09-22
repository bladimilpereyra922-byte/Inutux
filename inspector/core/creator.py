from pathlib import Path


class Creator:

    def __init__(self):
        self.root = Path(__file__).resolve().parents[1]

    def create(self, name):

        template = (
            self.root /
            "templates" /
            "agent.py"
        ).read_text(encoding="utf-8")

        class_name = "".join(
            x.capitalize() for x in name.split("_")
        ) + "Agent"

        code = (
            template
            .replace("class Agent:", f"class {class_name}:")
            .replace("{{NAME}}", name)
            .replace(
                "{{DESCRIPTION}}",
                f"Agente {name}"
            )
        )

        destination = (
            self.root /
            "agents" /
            f"{name}.py"
        )

        destination.write_text(
            code,
            encoding="utf-8"
        )

        print(f"[OK] Agente creado: {destination}")