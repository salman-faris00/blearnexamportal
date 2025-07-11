from datetime import datetime, time
from django.http import HttpResponse
from django.shortcuts import render

class TimeRestrictionMiddleware:
    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):
        now = datetime.now().time()  # current time only

        start_time = time(0, 0)  # 5:00 PM
        end_time = time(23, 59)    # 6:00 PM

        # Allow access only between 5:00 PM and 6:00 PM
        if start_time <= now <= end_time:
            return self.get_response(request)

        # Block access otherwise
        return render(request,"site_cant_reached.html",status=403)
    
