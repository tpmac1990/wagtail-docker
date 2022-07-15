from .base import *

# SECURITY WARNING: don't run with debug turned on in production!
# # DEBUG = True
# DEBUG = bool(int(os.environ.get('DEBUG', 0)))

# SECURITY WARNING: keep the secret key used in production secret!
# SECRET_KEY = "django-insecure-2t%jr0x$kh&8gmz_8qnd#@w=@p))f^0&crgqq19wk^hfh8kdg5"
# SECRET_KEY = os.environ.get('SECRET_KEY')

# SECURITY WARNING: define the correct hosts in production!
# ALLOWED_HOSTS = ["*"]

# ALLOWED_HOSTS = []
# # filter out all 'None' values
# # default to '' so we don't have to provide ALLOWED_HOSTS in the docker-compose file for development
# ALLOWED_HOSTS.extend(
#     filter(
#         None,
#         os.environ.get('ALLOWED_HOSTS', '').split(','),
#     )
# )

EMAIL_BACKEND = "django.core.mail.backends.console.EmailBackend"


try:
    from .local import *
except ImportError:
    pass
