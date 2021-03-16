from django.http import HttpResponseNotFound

from lagoinfo.settings import ALLOWED_IP_BLOCKS

def ip_checker(func):
    def check_ip(request, *args, **kwargs):
        x_forwarded_for = request.META.get('HTTP_X_FORWARDED_FOR')
        if x_forwarded_for:
            ip = x_forwarded_for.split(',')[0]
        else:
            ip = request.META.get('REMOTE_ADDR')
        if ip not in ALLOWED_IP_BLOCKS:
            return HttpResponseNotFound("Not Allowed to Access from {}!".format(ip))
        return func(request, *args, **kwargs)
    return check_ip