from django.http import HttpResponseNotFound

from lagoinfo.settings import ALLOWED_IP_BLOCKS

def ip_checker(func):
    def check_ip(request, *args, **kwargs):
        if request.META['REMOTE_ADDR'] not in ALLOWED_IP_BLOCKS:
            return HttpResponseNotFound("Not Allowed to Access!")
        return func(request, *args, **kwargs)
    return check_ip