import importlib.util
import sys
import string
import secrets


class ScriptLoader:

    @staticmethod
    def _load_module(source: str, module_name: str = "scripts"):
        """
        reads file source and loads it as a module

        :param source: file to load
        :param module_name: name of module to register in sys.modules
        :return: loaded module
        """
        spec = importlib.util.spec_from_file_location(module_name, source)
        module = importlib.util.module_from_spec(spec)
        sys.modules[module_name] = module
        spec.loader.exec_module(module)
        return module

    @staticmethod
    def loadPythonScript(fileName: str):
        """
        Loads a Python script
        """
        module = ScriptLoader._load_module(fileName)

