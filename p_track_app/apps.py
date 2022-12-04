from django.apps import AppConfig


class PTrackAppConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'p_track_app'

    def ready(self):
        import p_track_app.signals
