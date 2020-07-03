from django.conf import settings

def static_root(request):
    return {
        'GENERAL_STATIC_ROOT': settings.GENERAL_STATIC_ROOT,
        'APPCONTROL_STATIC_ROOT': settings.APPCONTROL_STATIC_ROOT,
        'FRONTEND_STATIC_ROOT': settings.FRONTEND_STATIC_ROOT,
    }

def settings_constants(request):
    return {
        'APP_NAME': settings.APP_NAME,        
    }