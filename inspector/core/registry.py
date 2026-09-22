import importlib
import inspect
import pkgutil

import inspector.agents


class Registry:
    def __init__(self):
        self._agents = {}
        self.load()

    def load(self):
        for _, module_name, _ in pkgutil.iter_modules(inspector.agents.__path__):

            module = importlib.import_module(
                f"inspector.agents.{module_name}"
            )

            for _, cls in inspect.getmembers(module, inspect.isclass):

                if (
                    hasattr(cls, "name")
                    and callable(getattr(cls, "run", None))
                ):
                    self._agents[cls.name] = cls()

    def get(self, name):
        return self._agents.get(name)

    def list(self):
        return sorted(self._agents.keys())