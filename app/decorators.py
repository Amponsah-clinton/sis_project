from functools import wraps
from django.http import HttpResponseNotFound
from app.models import SiteSettings

def check_page_enabled(page_setting_name):
    """Decorator to check if a page is enabled before allowing access"""
    def decorator(view_func):
        @wraps(view_func)
        def wrapper(request, *args, **kwargs):
            site_settings = SiteSettings.get_settings()
            if not getattr(site_settings, page_setting_name, True):
                return HttpResponseNotFound("Page not found")
            return view_func(request, *args, **kwargs)
        return wrapper
    return decorator

