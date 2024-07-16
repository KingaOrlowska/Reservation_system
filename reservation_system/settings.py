import os
from pathlib import Path

# Szybkie ustawienia deweloperskie - nieodpowiednie do produkcji
# Zobacz https://docs.djangoproject.com/en/5.0/howto/deployment/checklist/

# OSTRZEŻENIE BEZPIECZEŃSTWA: przechowuj klucz tajny używany w produkcji w tajemnicy!
SECRET_KEY = (
    'django-insecure-r3z3g-7b%!85**%m6(7nct@0tj%i+l&0rk9gf)ca3b@aiil5$('
)

# OSTRZEŻENIE BEZPIECZEŃSTWA: nie uruchamiaj aplikacji w trybie debug w produkcji!
DEBUG = True

ALLOWED_HOSTS = []

# URL logowania
LOGIN_URL = '/login/'
LOGIN_REDIRECT_URL = '/dashboard/'  # URL przekierowania po zalogowaniu

# Definicja aplikacji

INSTALLED_APPS = [
    'django.contrib.admin',  # Aplikacja admina, pozwala zarządzać aplikacją przez interfejs admina.
    'django.contrib.auth',  # System uwierzytelniania użytkowników.
    'django.contrib.contenttypes',  # Framework do dynamicznego modelowania i uprawnień.
    'django.contrib.sessions',  # Zarządzanie sesjami użytkowników.
    'django.contrib.messages',  # Obsługa wiadomości.
    'django.contrib.staticfiles',  # Obsługa plików statycznych.
    'reservations',  # Twoje aplikacje.
    'reservation_system',
    'schedule',
]

MIDDLEWARE = [
    'django.middleware.security.SecurityMiddleware',  # Środki bezpieczeństwa.
    'django.contrib.sessions.middleware.SessionMiddleware',  # Zarządzanie sesjami.
    'django.middleware.common.CommonMiddleware',  # Ogólne middleware.
    'django.middleware.csrf.CsrfViewMiddleware',  # Ochrona przed CSRF.
    'django.contrib.auth.middleware.AuthenticationMiddleware',  # Uwierzytelnianie użytkowników.
    'django.contrib.messages.middleware.MessageMiddleware',  # Obsługa wiadomości.
    'django.middleware.clickjacking.XFrameOptionsMiddleware',  # Ochrona przed clickjackingiem.
]

ROOT_URLCONF = 'reservation_system.urls'

# Ścieżka bazowa projektu
BASE_DIR = Path(__file__).resolve().parent.parent

# Konfiguracja szablonów
TEMPLATES = [
    {
        'BACKEND': 'django.template.backends.django.DjangoTemplates',
        'DIRS': [os.path.join(BASE_DIR, 'templates')],
        'APP_DIRS': True,
        'OPTIONS': {
            'context_processors': [
                'django.template.context_processors.debug',
                'django.template.context_processors.request',
                'django.contrib.auth.context_processors.auth',
                'django.contrib.messages.context_processors.messages',
            ],
        },
    },
]

WSGI_APPLICATION = 'reservation_system.wsgi.application'

# Baza danych
# https://docs.djangoproject.com/en/5.0/ref/settings/#databases

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.postgresql',  # Silnik bazy danych PostgreSQL
        'NAME': 'reservation',  # Nazwa bazy danych
        'USER': 'myuser',  # Użytkownik bazy danych
        'PASSWORD': 'newpassword',  # Hasło użytkownika bazy danych
        'HOST': 'localhost',  # Host bazy danych
        'PORT': '5432',  # Port bazy danych
        'ATOMIC_REQUESTS': True,  # Obsługa atomicznych zapytań
    }
}

# Walidacja haseł
# https://docs.djangoproject.com/en/5.0/ref/settings/#auth-password-validators

AUTH_PASSWORD_VALIDATORS = [
    {
        'NAME': (
            'django.contrib.auth.password_validation.'
            'UserAttributeSimilarityValidator'
        ),  # Walidator podobieństwa atrybutów użytkownika
    },
    {
        'NAME': (
            'django.contrib.auth.password_validation.'
            'MinimumLengthValidator'
        ),  # Walidator minimalnej długości hasła
    },
    {
        'NAME': (
            'django.contrib.auth.password_validation.'
            'CommonPasswordValidator'
        ),  # Walidator powszechnych haseł
    },
    {
        'NAME': (
            'django.contrib.auth.password_validation.'
            'NumericPasswordValidator'
        ),  # Walidator haseł numerycznych
    },
]

# Międzynarodowość
# https://docs.djangoproject.com/en/5.0/topics/i18n/

LANGUAGE_CODE = 'pl-pl'  # Kod języka

TIME_ZONE = 'UTC'  # Strefa czasowa

USE_I18N = True  # Używanie międzynarodowości

USE_TZ = True  # Używanie stref czasowych

# Pliki statyczne (CSS, JavaScript, Images)
# https://docs.djangoproject.com/en/5.0/howto/static-files/

STATIC_URL = '/static/'  # URL plików statycznych
STATICFILES_DIRS = [
    BASE_DIR / "static",  # Katalog plików statycznych
]

# Domyślny typ pola klucza głównego
# https://docs.djangoproject.com/en/5.0/ref/settings/#default-auto-field

DEFAULT_AUTO_FIELD = 'django.db.models.BigAutoField'

# Ustawienia e-mail
EMAIL_BACKEND = 'django.core.mail.backends.smtp.EmailBackend'
EMAIL_HOST = 'smtp.gmail.com'
EMAIL_PORT = 587
EMAIL_USE_TLS = True
EMAIL_HOST_USER = 'podkotwica@gmail.com'
EMAIL_HOST_PASSWORD = 'ypvc qzty ckdu wdae'
DEFAULT_FROM_EMAIL = 'podkotwica@gmail.com'
