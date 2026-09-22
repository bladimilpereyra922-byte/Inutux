import json
from pathlib import Path


class IntelligenceEngine:

    def __init__(self):

        self.root = (
            Path(__file__)
            .resolve()
            .parents[1]
            / "intelligence"
        )

        self.cache = {}

    def load(self, name):

        if name in self.cache:
            return self.cache[name]

        file = self.root / f"{name}.json"

        if not file.exists():

            self.cache[name] = []

            return []

        try:

            data = json.loads(
                file.read_text(
                    encoding="utf-8"
                )
            )

        except Exception:

            data = []

        self.cache[name] = data

        return data

    def clear(self):

        self.cache.clear()