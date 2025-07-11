from django.utils.timezone import localtime
from datetime import time
from django.shortcuts import render
from functools import wraps

def time_restricted(start_hour, start_minute, end_hour, end_minute):
    def decorator(view_func):
        @wraps(view_func)
        def _wrapped_view(request, *args, **kwargs):
            now = localtime().time()
            start = time(start_hour, start_minute)
            end = time(end_hour, end_minute)

            print("=== DEBUG: Time Check ===")
            print("Now:", now)
            print("Start:", start)
            print("End:", end)

            if start <= end:
                allowed = start <= now <= end
            else:
                allowed = now >= start or now <= end

            print("Allowed:", allowed)

            if allowed:
                return view_func(request, *args, **kwargs)
            return render(request, 'site_cant_reached.html', status=403)
        return _wrapped_view
    return decorator
