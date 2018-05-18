from config.default_settings import *

ENV = os.environ.get("DJANGO_SETTINGS_ENV", "dev").lower()
if ENV == "dev":
    from config.dev import *
elif ENV == "test":
    from config.sprd import *
elif ENV == "sprd":
    from config.sprd import *
elif ENV == "prd":
    from config.prd import *
elif ENV == "quxf":
    from config.quxf import *
