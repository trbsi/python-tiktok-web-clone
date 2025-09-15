import os


def environment_variables(request):
    return {
        'APP_NAME': os.getenv('APP_NAME'),
        'SUPPORT_EMAIL': os.getenv('SUPPORT_EMAIL'),
    }
