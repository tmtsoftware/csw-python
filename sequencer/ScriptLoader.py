import importlib.util
import sys
from types import ModuleType


class ScriptLoader:

    @staticmethod
    def _loadModule(source: str, moduleName: str = "scripts") -> ModuleType:
        """
        reads file source and loads it as a module

        :param source: file to load
        :param moduleName: name of module to register in sys.modules
        :return: loaded module
        """
        spec = importlib.util.spec_from_file_location(moduleName, source)
        module = importlib.util.module_from_spec(spec)
        sys.modules[moduleName] = module
        spec.loader.exec_module(module)
        return module

    @classmethod
    def loadPythonScript(cls, fileName: str) -> ModuleType:
        """
        Loads a Python script
        """
        module = cls._loadModule(fileName)
        return module

