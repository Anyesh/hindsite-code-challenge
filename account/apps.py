from django.apps import AppConfig


class AccountConfig(AppConfig):
    default_auto_field = "django.db.models.BigAutoField"
    name = "account"

    def ready(self):
        # signals are imported, so that they are defined and can be used
        import account.signals  # noqa
