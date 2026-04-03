import os
import environ
from .base import *

DEBUG = True

# When DJANGO_SETTINGS_MODULE points to a specific sub-module (e.g. settings.test,
# settings.dev, settings.docker), that sub-module provides all required settings.
# Only do the dynamic env-based loading when the package itself is the target.
_target = os.environ.get('DJANGO_SETTINGS_MODULE', '')
if _target in ('', 'habaneras_de_lino_drf_api.settings'):
    env = environ.Env()
    environ.Env.read_env()

    # Get current environment to load configs
    try:
        CURRENT_ENV = env("CURRENT_ENV")
    except Exception:
        CURRENT_ENV = 'DEVELOPMENT'

    # Load configs
    if CURRENT_ENV == "DEVELOPMENT":
        from .dev import *
    elif CURRENT_ENV == "PRODUCTION":
        from .prod import *
    else:
        from .docker import *
