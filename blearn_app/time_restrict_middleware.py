from django.utils.timezone import localtime
from datetime import time
from django.shortcuts import render

class TimeRestrictionMiddleware:
    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):
        now = localtime().time()  # Gets the current time in the local timezone

        start_time = time(13, 50)   # 10:00 AM
        end_time = time(15, 5)    # 12:30 PM

        if start_time <= now <= end_time:
            return self.get_response(request)

        # Access blocked outside allowed time
        return render(request, "site_cant_reached.html", status=403)
