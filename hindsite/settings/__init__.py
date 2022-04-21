try:
    from .settings_local import *  # noqa
except Exception:
    from .settings_prod import *  # noqa
