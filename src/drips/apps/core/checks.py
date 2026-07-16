import importlib
import pkgutil

import drips


def check_imports(package=drips):
    for _importer, modname, _ispkg in pkgutil.iter_modules(package.__path__):
        current_module = f"{package.__name__}.{modname}"
        m = importlib.import_module(current_module)
        if hasattr(m, "__path__"):  # pragma: no cover
            for _, sub_mod, __ in pkgutil.iter_modules(m.__path__):
                sub_module = f"{current_module}.{sub_mod}"
                sm = importlib.import_module(sub_module)
                if hasattr(sm, "__path__"):
                    for _, ssm_name, __ in pkgutil.iter_modules(sm.__path__):
                        s_sub_mod = f"{current_module}.{sub_mod}.{ssm_name}"
                        try:
                            importlib.import_module(s_sub_mod)
                        except Exception as e:  # pragma: no cover  # noqa: BLE001
                            raise Exception(
                                f"""Error importing '{s_sub_mod}'.
    {e}
    """
                            )
