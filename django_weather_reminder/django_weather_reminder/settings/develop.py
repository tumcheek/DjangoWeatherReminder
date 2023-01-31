from .base import *
DEBUG = True
REST_FRAMEWORK['DEFAULT_RENDERER_CLASSES'].append('rest_framework.renderers.BrowsableAPIRenderer')
EMAIL_BACKEND = 'django.core.mail.backends.console.EmailBackend'
