from os import path

import eduserver

_package_dir = path.abspath(path.dirname(eduserver.__file__))

SECRET_KEY = 'super-secret'
JWT_AUTH_USERNAME_KEY = 'login'
JWT_AUTH_PASSWORD_KEY = 'password'
