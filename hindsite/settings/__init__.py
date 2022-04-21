try:

    from .settings_prod import *  # noqa

    if DEBUG:
        raise Exception("ERROR")
except Exception:
    from .settings_local import *  # noqa
