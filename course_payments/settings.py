INSTALLED_APPS = [
    ...
    'payments',
    'crispy_forms',
    'django.contrib.staticfiles',
]

STATIC_URL = '/static/'
STATICFILES_DIRS = [BASE_DIR / "static"]

MEDIA_URL = '/media/'
MEDIA_ROOT = BASE_DIR / "media"

TEMPLATES[0]['DIRS'] = [BASE_DIR / 'payments' / 'templates']
