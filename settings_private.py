# Settings for Django that should not be shared.

# The connection details for the Guyton database.
DATABASES = {
    'default': {
        # Choose an engine from 'django.db.backends.
        'ENGINE': '',
        # Set to database name, or path to database file if using sqlite3.
        'NAME': '',
        # Not used with sqlite3.
        'USER': '',
        # Not used with sqlite3.
        'PASSWORD': '',
        # Set to empty string for localhost. Not used with sqlite3.
        'HOST': '',
        # Set to empty string for default. Not used with sqlite3.
        'PORT': '',
    }
}

# Make this unique, and don't share it with anybody.
SECRET_KEY = ''
